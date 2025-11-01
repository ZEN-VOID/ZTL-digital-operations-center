"""
Figma REST API客户端
提供异步HTTP客户端，封装Figma API调用
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin
import httpx
from httpx import AsyncClient, Response
import backoff
from pydantic_settings import BaseSettings


logger = logging.getLogger(__name__)


class FigmaClientConfig(BaseSettings):
    """Figma客户端配置"""
    figma_api_token: str = ""
    figma_api_base_url: str = "https://api.figma.com/v1/"
    figma_timeout: int = 30
    figma_max_retries: int = 3
    figma_rate_limit_per_minute: int = 60
    figma_concurrent_requests: int = 5

    class Config:
        env_prefix = "FIGMA_"


class FigmaAPIError(Exception):
    """Figma API错误基类"""
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[Dict] = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)


class FigmaRateLimitError(FigmaAPIError):
    """Figma API速率限制错误"""
    pass


class FigmaAuthenticationError(FigmaAPIError):
    """Figma API认证错误"""
    pass


class FigmaNotFoundError(FigmaAPIError):
    """Figma资源未找到错误"""
    pass


class FigmaClient:
    """
    Figma REST API异步客户端
    
    特性:
    - 异步HTTP请求
    - 自动重试和指数退避
    - 速率限制控制
    - 完整的错误处理
    - 并发控制
    """

    def __init__(self, config: Optional[FigmaClientConfig] = None):
        """
        初始化Figma客户端
        
        Args:
            config: Figma客户端配置
        """
        self.config = config or FigmaClientConfig()
        self._client: Optional[AsyncClient] = None
        self._semaphore = asyncio.Semaphore(self.config.figma_concurrent_requests)
        
        # 验证配置
        if not self.config.figma_api_token:
            raise ValueError("Figma API token is required")

    async def __aenter__(self):
        """异步上下文管理器入口"""
        await self._ensure_client()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.close()

    async def _ensure_client(self):
        """确保HTTP客户端已初始化"""
        if self._client is None:
            headers = {
                "X-Figma-Token": self.config.figma_api_token,
                "Content-Type": "application/json",
                "User-Agent": "ZTL-Design-Platform/1.0"
            }
            
            timeout = httpx.Timeout(self.config.figma_timeout)
            
            self._client = AsyncClient(
                base_url=self.config.figma_api_base_url,
                headers=headers,
                timeout=timeout,
                follow_redirects=True
            )

    async def close(self):
        """关闭HTTP客户端"""
        if self._client:
            await self._client.aclose()
            self._client = None

    def _handle_response_error(self, response: Response) -> None:
        """处理HTTP响应错误"""
        try:
            error_data = response.json()
        except Exception:
            error_data = {"message": response.text}

        error_message = error_data.get("message", f"HTTP {response.status_code}")

        if response.status_code == 401:
            raise FigmaAuthenticationError(
                f"Authentication failed: {error_message}",
                status_code=response.status_code,
                response_data=error_data
            )
        elif response.status_code == 403:
            raise FigmaAuthenticationError(
                f"Access forbidden: {error_message}",
                status_code=response.status_code,
                response_data=error_data
            )
        elif response.status_code == 404:
            raise FigmaNotFoundError(
                f"Resource not found: {error_message}",
                status_code=response.status_code,
                response_data=error_data
            )
        elif response.status_code == 429:
            raise FigmaRateLimitError(
                f"Rate limit exceeded: {error_message}",
                status_code=response.status_code,
                response_data=error_data
            )
        else:
            raise FigmaAPIError(
                f"API request failed: {error_message}",
                status_code=response.status_code,
                response_data=error_data
            )

    @backoff.on_exception(
        backoff.expo,
        (httpx.RequestError, FigmaRateLimitError),
        max_tries=3,
        max_time=60
    )
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        发起HTTP请求
        
        Args:
            method: HTTP方法
            endpoint: API端点
            params: 查询参数
            json_data: JSON数据
            
        Returns:
            API响应数据
            
        Raises:
            FigmaAPIError: API请求失败
        """
        async with self._semaphore:
            await self._ensure_client()
            
            try:
                logger.debug(f"Making {method} request to {endpoint}")
                
                response = await self._client.request(
                    method=method,
                    url=endpoint,
                    params=params,
                    json=json_data
                )
                
                if not response.is_success:
                    self._handle_response_error(response)
                
                return response.json()
                
            except httpx.RequestError as e:
                logger.error(f"Request error: {e}")
                raise FigmaAPIError(f"Request failed: {str(e)}")

    async def get_file(self, file_key: str) -> Dict[str, Any]:
        """
        获取Figma文件信息
        
        Args:
            file_key: Figma文件键
            
        Returns:
            文件信息
        """
        return await self._make_request("GET", f"files/{file_key}")

    async def get_file_nodes(
        self,
        file_key: str,
        node_ids: List[str]
    ) -> Dict[str, Any]:
        """
        获取Figma文件中的特定节点
        
        Args:
            file_key: Figma文件键
            node_ids: 节点ID列表
            
        Returns:
            节点信息
        """
        params = {"ids": ",".join(node_ids)}
        return await self._make_request("GET", f"files/{file_key}/nodes", params=params)

    async def export_images(
        self,
        file_key: str,
        node_ids: List[str],
        format: str = "png",
        scale: float = 1.0,
        version: Optional[str] = None,
        svg_outline_text: bool = True,
        svg_include_id: bool = False,
        svg_include_node_id: bool = False,
        svg_simplify_stroke: bool = True,
        contents_only: bool = True,
        use_absolute_bounds: bool = False
    ) -> Dict[str, Any]:
        """
        导出Figma节点为图片 - 符合官方API规范

        Args:
            file_key: Figma文件键
            node_ids: 要导出的节点ID列表
            format: 导出格式 (png, jpg, svg, pdf)
            scale: 缩放比例 (0.01-4.0)
            version: 特定版本ID
            svg_outline_text: SVG中文本是否渲染为轮廓
            svg_include_id: 是否为SVG元素包含id属性
            svg_include_node_id: 是否为SVG元素包含node-id属性
            svg_simplify_stroke: 是否简化SVG描边
            contents_only: 是否排除重叠内容
            use_absolute_bounds: 是否使用绝对边界

        Returns:
            导出结果，包含图片URL映射
        """
        params = {
            "ids": ",".join(node_ids),
            "format": format,
            "scale": str(scale)
        }

        # 添加可选参数
        if version:
            params["version"] = version
        if format == "svg":
            params["svg_outline_text"] = str(svg_outline_text).lower()
            params["svg_include_id"] = str(svg_include_id).lower()
            params["svg_include_node_id"] = str(svg_include_node_id).lower()
            params["svg_simplify_stroke"] = str(svg_simplify_stroke).lower()

        params["contents_only"] = str(contents_only).lower()
        params["use_absolute_bounds"] = str(use_absolute_bounds).lower()

        return await self._make_request("GET", f"images/{file_key}", params=params)

    async def get_file_versions(self, file_key: str) -> Dict[str, Any]:
        """
        获取Figma文件版本历史
        
        Args:
            file_key: Figma文件键
            
        Returns:
            版本历史信息
        """
        return await self._make_request("GET", f"files/{file_key}/versions")

    async def health_check(self) -> bool:
        """
        检查Figma API连接状态
        
        Returns:
            连接是否正常
        """
        try:
            # 使用一个简单的API调用来检查连接
            await self._make_request("GET", "me")
            return True
        except Exception as e:
            logger.error(f"Figma API health check failed: {e}")
            return False
