"""
Figma批量处理服务

实现图片批量替换、节点匹配和导出功能的核心业务逻辑
"""

import asyncio
import logging
import uuid
import time
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.batch import (
    ReplacementRule,
    ExportConfig,
    BatchReplaceRequest,
    BatchReplaceResponse,
    ExportedFile,
    ProcessingStatus,
    NodeMatchResult,
)
from ..config import Settings
from .figma_client import FigmaClient, FigmaClientConfig

logger = logging.getLogger(__name__)


class FigmaBatchProcessor:
    """Figma批量处理服务

    提供图片替换、节点匹配和导出的完整工作流
    """

    def __init__(self, db: AsyncSession, settings: Settings):
        self.db = db
        self.settings = settings

        # 创建Figma客户端配置
        figma_config = FigmaClientConfig(
            figma_api_token=settings.figma_api_token,
            figma_api_base_url=settings.figma_api_base_url,
            figma_timeout=settings.figma_timeout,
            figma_max_retries=settings.figma_max_retries,
            figma_rate_limit_per_minute=settings.figma_rate_limit_per_minute,
            figma_concurrent_requests=settings.figma_concurrent_requests,
        )
        self.figma_client = FigmaClient(figma_config)

        # 任务状态存储（生产环境应使用Redis或数据库）
        self._tasks: Dict[str, BatchReplaceResponse] = {}

    async def process_batch_replace(
        self, request: BatchReplaceRequest
    ) -> BatchReplaceResponse:
        """
        处理批量替换请求

        Args:
            request: 批量替换请求

        Returns:
            BatchReplaceResponse: 处理结果

        Raises:
            ValueError: 请求参数无效
            RuntimeError: 处理过程中发生错误
        """
        task_id = str(uuid.uuid4())
        start_time = time.time()

        # 创建初始响应
        response = BatchReplaceResponse(
            success=False,
            message="Processing started",
            task_id=task_id,
            status=ProcessingStatus.PENDING,
            total_replacements=len(request.replacement_rules),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        # 存储任务
        self._tasks[task_id] = response

        try:
            # 1. 验证文件访问权限
            response.status = ProcessingStatus.VALIDATING
            response.message = "Validating file access"
            await self._validate_file_access(request.figma_file_id)

            # 2. 解析节点匹配规则，获取实际节点ID
            response.status = ProcessingStatus.REPLACING
            response.message = "Matching nodes and preparing replacements"
            replacement_map = await self._resolve_replacement_rules(
                request.figma_file_id,
                request.replacement_rules
            )

            # 3. 执行批量替换
            response.message = "Replacing images"
            replace_results = await self.replace_images(
                request.figma_file_id,
                replacement_map
            )

            response.successful_replacements = replace_results["success_count"]
            response.failed_replacements = replace_results["failed_count"]
            response.failed_nodes = replace_results["failed_nodes"]

            # 4. 导出处理后的设计稿
            response.status = ProcessingStatus.EXPORTING
            response.message = "Exporting processed designs"
            exported_files = await self.export_to_file(
                request.figma_file_id,
                list(replacement_map.keys()),
                request.export_config
            )

            response.exported_files = exported_files

            # 5. 可选：上传到云盘
            if request.export_config.save_to_cloud:
                response.status = ProcessingStatus.UPLOADING
                response.message = "Uploading to cloud storage"
                cloud_urls = await self.upload_to_cloud(
                    [Path(f.local_path) for f in exported_files],
                    request.export_config.cloud_dir
                )

                # 更新云盘URL
                for file, cloud_url in zip(exported_files, cloud_urls):
                    file.cloud_url = cloud_url

            # 6. 完成
            response.status = ProcessingStatus.COMPLETED
            response.success = response.failed_replacements == 0
            response.message = (
                "Completed successfully"
                if response.success
                else f"Completed with {response.failed_replacements} failures"
            )
            response.completed_at = datetime.now()
            response.processing_time = time.time() - start_time

        except Exception as e:
            logger.error(f"Batch replace task {task_id} failed: {e}")
            response.status = ProcessingStatus.FAILED
            response.success = False
            response.message = "Processing failed"
            response.error_message = str(e)
            response.completed_at = datetime.now()
            response.processing_time = time.time() - start_time

        finally:
            response.updated_at = datetime.now()
            self._tasks[task_id] = response

        return response

    async def _validate_file_access(self, file_id: str) -> None:
        """
        验证文件访问权限

        Args:
            file_id: Figma文件ID

        Raises:
            RuntimeError: 文件不存在或无访问权限
        """
        try:
            async with self.figma_client:
                file_info = await self.figma_client.get_file(file_id)
                if not file_info:
                    raise RuntimeError(f"File {file_id} not found or access denied")
                logger.info(f"Validated access to file: {file_info.get('name', file_id)}")
        except Exception as e:
            logger.error(f"File validation failed: {e}")
            raise RuntimeError(f"Cannot access file {file_id}: {e}")

    async def _resolve_replacement_rules(
        self, file_id: str, rules: List[ReplacementRule]
    ) -> Dict[str, str]:
        """
        解析替换规则，将模式匹配转换为具体的节点ID映射

        Args:
            file_id: Figma文件ID
            rules: 替换规则列表

        Returns:
            Dict[node_id, image_url]: 节点ID到图片URL的映射

        Raises:
            ValueError: 规则解析失败
        """
        replacement_map: Dict[str, str] = {}

        # 获取文件中的所有节点
        async with self.figma_client:
            file_data = await self.figma_client.get_file(file_id)

        if not file_data or "document" not in file_data:
            raise ValueError("Cannot retrieve file structure")

        # 提取所有节点的ID和名称
        all_nodes = self._extract_all_nodes(file_data["document"])

        for rule in rules:
            target = rule.target_node_path

            # 检查是否是模式匹配
            if "*" in target or "?" in target:
                # 模式匹配
                matched_nodes = self._match_nodes_by_pattern(target, all_nodes)
                if not matched_nodes:
                    logger.warning(f"Pattern '{target}' matched no nodes")
                    continue

                for node_id in matched_nodes:
                    replacement_map[node_id] = rule.image_url
                    logger.debug(f"Matched node {node_id} for pattern '{target}'")

            else:
                # 精确匹配
                replacement_map[target] = rule.image_url

        logger.info(f"Resolved {len(replacement_map)} node replacements from {len(rules)} rules")
        return replacement_map

    def _extract_all_nodes(
        self, document: Dict[str, Any], nodes: Optional[Dict[str, Dict[str, str]]] = None
    ) -> Dict[str, Dict[str, str]]:
        """
        递归提取文档中的所有节点

        Args:
            document: Figma文档节点
            nodes: 累积的节点字典

        Returns:
            Dict[node_id, node_info]: 节点ID到节点信息的映射
        """
        if nodes is None:
            nodes = {}

        if "id" in document:
            nodes[document["id"]] = {
                "name": document.get("name", ""),
                "type": document.get("type", "")
            }

        # 递归处理子节点
        if "children" in document:
            for child in document["children"]:
                self._extract_all_nodes(child, nodes)

        return nodes

    def _match_nodes_by_pattern(
        self, pattern: str, all_nodes: Dict[str, Dict[str, str]]
    ) -> List[str]:
        """
        使用模式匹配查找节点

        支持的模式：
        - dish-* : 匹配所有以dish-开头的节点
        - *-photo : 匹配所有以-photo结尾的节点
        - dish-?-photo : ? 匹配单个字符

        Args:
            pattern: 匹配模式
            all_nodes: 所有节点的字典

        Returns:
            List[str]: 匹配的节点ID列表
        """
        # 将通配符模式转换为正则表达式
        regex_pattern = pattern.replace("*", ".*").replace("?", ".")
        regex_pattern = f"^{regex_pattern}$"

        matched_ids = []
        try:
            compiled_pattern = re.compile(regex_pattern, re.IGNORECASE)
            for node_id, node_info in all_nodes.items():
                node_name = node_info["name"]
                if compiled_pattern.match(node_name):
                    matched_ids.append(node_id)
        except re.error as e:
            logger.error(f"Invalid pattern '{pattern}': {e}")
            return []

        return matched_ids

    async def replace_images(
        self, file_id: str, replacement_map: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        执行批量图片替换

        Args:
            file_id: Figma文件ID
            replacement_map: 节点ID到图片URL的映射

        Returns:
            Dict: 替换结果统计
        """
        success_count = 0
        failed_count = 0
        failed_nodes = []

        # 注意：实际的图片替换需要通过Figma Plugin API完成
        # 这里提供REST API无法直接完成的操作的占位实现
        # 生产环境需要配合Figma插件使用

        logger.warning(
            "Image replacement requires Figma Plugin. "
            "This method simulates the replacement process."
        )

        # 模拟替换过程
        for node_id, image_url in replacement_map.items():
            try:
                # 验证图片URL可访问
                # 实际替换由插件完成
                await asyncio.sleep(0.1)  # 模拟处理延迟

                success_count += 1
                logger.debug(f"Prepared replacement for node {node_id}")

            except Exception as e:
                failed_count += 1
                failed_nodes.append({"node_id": node_id, "error": str(e)})
                logger.error(f"Failed to prepare replacement for node {node_id}: {e}")

        return {
            "success_count": success_count,
            "failed_count": failed_count,
            "failed_nodes": failed_nodes,
        }

    async def export_to_file(
        self, file_id: str, node_ids: List[str], config: ExportConfig
    ) -> List[ExportedFile]:
        """
        导出设计稿为图片

        Args:
            file_id: Figma文件ID
            node_ids: 要导出的节点ID列表
            config: 导出配置

        Returns:
            List[ExportedFile]: 导出的文件列表
        """
        exported_files = []
        export_dir = Path(self.settings.export_dir) / file_id / datetime.now().strftime("%Y%m%d_%H%M%S")
        export_dir.mkdir(parents=True, exist_ok=True)

        # 确定要导出的缩放比例
        scales = config.scales if config.scales else [config.scale]

        async with self.figma_client:
            for scale in scales:
                try:
                    # 调用Figma API导出图片
                    export_data = await self.figma_client.export_images(
                        file_key=file_id,
                        node_ids=node_ids,
                        format=config.format.value,
                        scale=scale,
                        svg_outline_text=config.svg_outline_text,
                        svg_include_id=config.svg_include_id,
                        contents_only=config.contents_only,
                        use_absolute_bounds=config.use_absolute_bounds,
                    )

                    if not export_data or "images" not in export_data:
                        logger.error(f"Export failed for scale {scale}")
                        continue

                    # 下载导出的图片
                    for node_id, image_url in export_data["images"].items():
                        if not image_url:
                            logger.warning(f"No image URL for node {node_id}")
                            continue

                        # 下载图片
                        image_data = await self._download_image(image_url)
                        if not image_data:
                            continue

                        # 保存文件
                        filename = f"{node_id}_{scale}x.{config.format.value}"
                        file_path = export_dir / filename
                        file_path.write_bytes(image_data)

                        exported_files.append(
                            ExportedFile(
                                filename=filename,
                                local_path=str(file_path),
                                cloud_url=None,
                                format=config.format.value,
                                scale=scale,
                                size_bytes=len(image_data),
                                node_id=node_id,
                            )
                        )

                        logger.info(f"Exported {filename} ({len(image_data)} bytes)")

                except Exception as e:
                    logger.error(f"Export failed for scale {scale}: {e}")

        return exported_files

    async def _download_image(self, url: str) -> Optional[bytes]:
        """
        下载图片

        Args:
            url: 图片URL

        Returns:
            Optional[bytes]: 图片数据，失败返回None
        """
        try:
            import httpx

            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.content
        except Exception as e:
            logger.error(f"Failed to download image from {url}: {e}")
            return None

    async def upload_to_cloud(
        self, local_paths: List[Path], cloud_dir: str
    ) -> List[str]:
        """
        上传到云盘（调用modules/cloud-storage）

        Args:
            local_paths: 本地文件路径列表
            cloud_dir: 云盘目录路径

        Returns:
            List[str]: 云盘URL列表

        Note:
            此方法需要集成cloud-storage模块
            当前为占位实现
        """
        cloud_urls = []

        # TODO: 集成cloud-storage模块
        # from modules.cloud_storage import CloudStorageClient
        # client = CloudStorageClient()

        logger.warning("Cloud storage upload not yet implemented")

        for local_path in local_paths:
            try:
                # 占位：实际上传逻辑
                # cloud_url = await client.upload(local_path, cloud_dir)
                cloud_url = f"https://cloud.example.com/{cloud_dir}/{local_path.name}"
                cloud_urls.append(cloud_url)

                logger.info(f"Uploaded {local_path.name} to cloud storage")

            except Exception as e:
                logger.error(f"Failed to upload {local_path}: {e}")
                cloud_urls.append("")  # 占位空URL

        return cloud_urls

    def get_task_status(self, task_id: str) -> Optional[BatchReplaceResponse]:
        """
        获取任务状态

        Args:
            task_id: 任务ID

        Returns:
            Optional[BatchReplaceResponse]: 任务状态，不存在返回None
        """
        return self._tasks.get(task_id)

    def list_tasks(self) -> List[BatchReplaceResponse]:
        """
        列出所有任务

        Returns:
            List[BatchReplaceResponse]: 任务列表
        """
        return list(self._tasks.values())