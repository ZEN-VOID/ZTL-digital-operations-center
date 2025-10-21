"""
完整的Figma官方API服务
基于Figma官方REST API规范的完整服务实现
"""

import logging
from typing import Optional, Dict, Any
import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.figma_complete import (
    # Files
    GetFileResponse,
    GetFileNodesResponse,
    GetFileVersionsResponse,
    
    # Images
    GetImagesResponse,
    
    # Comments
    GetCommentsResponse,
    PostCommentRequest,
    PostCommentResponse,
    DeleteCommentResponse,
    
    # Users
    GetUserResponse,
    
    # Projects
    GetTeamProjectsResponse,
    GetProjectFilesResponse,
    
    # Component Types
    GetTeamComponentsResponse,
    GetComponentResponse,
    
    # Variables
    GetLocalVariablesResponse,
    GetPublishedVariablesResponse,
    PostVariablesRequest,
    PostVariablesResponse,
    
    # Webhooks
    GetWebhooksResponse,
    PostWebhookRequest,
    PostWebhookResponse,
    PutWebhookRequest,
    PutWebhookResponse,
    DeleteWebhookResponse,
    GetWebhookRequestsResponse,
    
    # Activity Logs
    GetActivityLogsResponse,
    
    # Discovery
    GetDiscoveryResponse,
    
    # Payments
    GetPaymentsResponse,
    
    # Library Analytics
    GetLibraryAnalyticsResponse,
    
    # Dev Resources
    GetDevResourcesResponse,
    PostDevResourceRequest,
    PostDevResourceResponse,
    PutDevResourceRequest,
    PutDevResourceResponse,
    DeleteDevResourceResponse
)
from ..config import Settings

logger = logging.getLogger(__name__)


class FigmaCompleteService:
    """完整的Figma官方API服务"""
    
    def __init__(self, db: AsyncSession, settings: Settings):
        self.db = db
        self.settings = settings
        self.base_url = "https://api.figma.com/v1"
        
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        token: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """发起HTTP请求"""
        url = f"{self.base_url}{endpoint}"
        headers = {
            "X-Figma-Token": token,
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json_data,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    # ==================== Files API ====================
    
    async def get_file(
        self,
        file_key: str,
        token: str,
        version: Optional[str] = None,
        ids: Optional[str] = None,
        depth: Optional[int] = None,
        geometry: Optional[str] = None,
        plugin_data: Optional[str] = None,
        branch_data: Optional[bool] = None
    ) -> GetFileResponse:
        """获取文件信息"""
        params = {}
        if version:
            params["version"] = version
        if ids:
            params["ids"] = ids
        if depth is not None:
            params["depth"] = depth
        if geometry:
            params["geometry"] = geometry
        if plugin_data:
            params["plugin_data"] = plugin_data
        if branch_data:
            params["branch_data"] = branch_data
            
        data = await self._make_request("GET", f"/files/{file_key}", token, params)
        return GetFileResponse(**data)
    
    async def get_file_nodes(
        self,
        file_key: str,
        ids: str,
        token: str,
        version: Optional[str] = None,
        depth: Optional[int] = None,
        geometry: Optional[str] = None,
        plugin_data: Optional[str] = None
    ) -> GetFileNodesResponse:
        """获取文件节点"""
        params = {"ids": ids}
        if version:
            params["version"] = version
        if depth is not None:
            params["depth"] = depth
        if geometry:
            params["geometry"] = geometry
        if plugin_data:
            params["plugin_data"] = plugin_data
            
        data = await self._make_request("GET", f"/files/{file_key}/nodes", token, params)
        return GetFileNodesResponse(**data)
    
    async def get_file_versions(
        self,
        file_key: str,
        token: str
    ) -> GetFileVersionsResponse:
        """获取文件版本历史"""
        data = await self._make_request("GET", f"/files/{file_key}/versions", token)
        return GetFileVersionsResponse(**data)
    
    # ==================== Images API ====================
    
    async def get_images(
        self,
        file_key: str,
        ids: str,
        token: str,
        scale: Optional[float] = None,
        format: Optional[str] = None,
        svg_outline_text: Optional[bool] = None,
        svg_include_id: Optional[bool] = None,
        svg_include_node_id: Optional[bool] = None,
        svg_simplify_stroke: Optional[bool] = None,
        contents_only: Optional[bool] = None,
        use_absolute_bounds: Optional[bool] = None,
        version: Optional[str] = None
    ) -> GetImagesResponse:
        """渲染图片"""
        params = {"ids": ids}
        if scale is not None:
            params["scale"] = scale
        if format:
            params["format"] = format
        if svg_outline_text is not None:
            params["svg_outline_text"] = svg_outline_text
        if svg_include_id is not None:
            params["svg_include_id"] = svg_include_id
        if svg_include_node_id is not None:
            params["svg_include_node_id"] = svg_include_node_id
        if svg_simplify_stroke is not None:
            params["svg_simplify_stroke"] = svg_simplify_stroke
        if contents_only is not None:
            params["contents_only"] = contents_only
        if use_absolute_bounds is not None:
            params["use_absolute_bounds"] = use_absolute_bounds
        if version:
            params["version"] = version
            
        data = await self._make_request("GET", f"/images/{file_key}", token, params)
        return GetImagesResponse(**data)
    
    # ==================== Comments API ====================
    
    async def get_comments(
        self,
        file_key: str,
        token: str
    ) -> GetCommentsResponse:
        """获取评论"""
        data = await self._make_request("GET", f"/files/{file_key}/comments", token)
        return GetCommentsResponse(**data)
    
    async def post_comment(
        self,
        file_key: str,
        request: PostCommentRequest,
        token: str
    ) -> PostCommentResponse:
        """发布评论"""
        data = await self._make_request(
            "POST", 
            f"/files/{file_key}/comments", 
            token, 
            json_data=request.dict()
        )
        return PostCommentResponse(**data)
    
    async def delete_comment(
        self,
        comment_id: str,
        token: str
    ) -> DeleteCommentResponse:
        """删除评论"""
        data = await self._make_request("DELETE", f"/comments/{comment_id}", token)
        return DeleteCommentResponse(**data)
    
    # ==================== Users API ====================
    
    async def get_me(self, token: str) -> GetUserResponse:
        """获取当前用户信息"""
        data = await self._make_request("GET", "/me", token)
        return GetUserResponse(**data)
    
    # ==================== Projects API ====================
    
    async def get_team_projects(
        self,
        team_id: str,
        token: str
    ) -> GetTeamProjectsResponse:
        """获取团队项目"""
        data = await self._make_request("GET", f"/teams/{team_id}/projects", token)
        return GetTeamProjectsResponse(**data)
    
    async def get_project_files(
        self,
        project_id: str,
        token: str,
        branch_data: Optional[bool] = None
    ) -> GetProjectFilesResponse:
        """获取项目文件"""
        params = {}
        if branch_data:
            params["branch_data"] = branch_data
            
        data = await self._make_request("GET", f"/projects/{project_id}/files", token, params)
        return GetProjectFilesResponse(**data)
    
    # ==================== Component Types API ====================
    
    async def get_team_components(
        self,
        team_id: str,
        token: str,
        page_size: Optional[int] = None,
        after: Optional[str] = None,
        before: Optional[str] = None
    ) -> GetTeamComponentsResponse:
        """获取团队组件"""
        params = {}
        if page_size is not None:
            params["page_size"] = page_size
        if after:
            params["after"] = after
        if before:
            params["before"] = before
            
        data = await self._make_request("GET", f"/teams/{team_id}/components", token, params)
        return GetTeamComponentsResponse(**data)
    
    async def get_component(
        self,
        component_key: str,
        token: str
    ) -> GetComponentResponse:
        """获取组件信息"""
        data = await self._make_request("GET", f"/components/{component_key}", token)
        return GetComponentResponse(**data)
    
    # ==================== Variables API ====================
    
    async def get_local_variables(
        self,
        file_key: str,
        token: str
    ) -> GetLocalVariablesResponse:
        """获取本地变量"""
        data = await self._make_request("GET", f"/files/{file_key}/variables/local", token)
        return GetLocalVariablesResponse(**data)
    
    async def get_published_variables(
        self,
        file_key: str,
        token: str
    ) -> GetPublishedVariablesResponse:
        """获取已发布变量"""
        data = await self._make_request("GET", f"/files/{file_key}/variables/published", token)
        return GetPublishedVariablesResponse(**data)
    
    async def post_variables(
        self,
        file_key: str,
        request: PostVariablesRequest,
        token: str
    ) -> PostVariablesResponse:
        """创建或更新变量"""
        data = await self._make_request(
            "POST",
            f"/files/{file_key}/variables",
            token,
            json_data=request.dict()
        )
        return PostVariablesResponse(**data)

    # ==================== Webhooks API ====================

    async def get_webhooks(
        self,
        team_id: str,
        token: str
    ) -> GetWebhooksResponse:
        """获取Webhooks列表"""
        params = {"team_id": team_id}
        data = await self._make_request("GET", "/webhooks", token, params)
        return GetWebhooksResponse(**data)

    async def post_webhook(
        self,
        request: PostWebhookRequest,
        token: str
    ) -> PostWebhookResponse:
        """创建Webhook"""
        data = await self._make_request(
            "POST",
            "/webhooks",
            token,
            json_data=request.dict()
        )
        return PostWebhookResponse(**data)

    async def put_webhook(
        self,
        webhook_id: str,
        request: PutWebhookRequest,
        token: str
    ) -> PutWebhookResponse:
        """更新Webhook"""
        data = await self._make_request(
            "PUT",
            f"/webhooks/{webhook_id}",
            token,
            json_data=request.dict()
        )
        return PutWebhookResponse(**data)

    async def delete_webhook(
        self,
        webhook_id: str,
        token: str
    ) -> DeleteWebhookResponse:
        """删除Webhook"""
        data = await self._make_request("DELETE", f"/webhooks/{webhook_id}", token)
        return DeleteWebhookResponse(**data)

    async def get_webhook_requests(
        self,
        webhook_id: str,
        token: str
    ) -> GetWebhookRequestsResponse:
        """获取Webhook请求历史"""
        data = await self._make_request("GET", f"/webhooks/{webhook_id}/requests", token)
        return GetWebhookRequestsResponse(**data)

    # ==================== Activity Logs API ====================

    async def get_activity_logs(
        self,
        team_id: str,
        token: str,
        cursor: Optional[str] = None,
        limit: Optional[int] = None
    ) -> GetActivityLogsResponse:
        """获取活动日志"""
        params = {"team_id": team_id}
        if cursor:
            params["cursor"] = cursor
        if limit is not None:
            params["limit"] = limit

        data = await self._make_request("GET", "/activity_logs", token, params)
        return GetActivityLogsResponse(**data)

    # ==================== Discovery API ====================

    async def get_discovery(
        self,
        team_id: str,
        token: str
    ) -> GetDiscoveryResponse:
        """获取发现信息"""
        params = {"team_id": team_id}
        data = await self._make_request("GET", "/discovery", token, params)
        return GetDiscoveryResponse(**data)

    # ==================== Payments API ====================

    async def get_payments(
        self,
        team_id: str,
        token: str
    ) -> GetPaymentsResponse:
        """获取支付信息"""
        params = {"team_id": team_id}
        data = await self._make_request("GET", "/payments", token, params)
        return GetPaymentsResponse(**data)

    # ==================== Library Analytics API ====================

    async def get_library_analytics(
        self,
        team_id: str,
        token: str
    ) -> GetLibraryAnalyticsResponse:
        """获取库分析数据"""
        params = {"team_id": team_id}
        data = await self._make_request("GET", "/library_analytics", token, params)
        return GetLibraryAnalyticsResponse(**data)

    # ==================== Dev Resources API ====================

    async def get_dev_resources(
        self,
        file_key: str,
        token: str,
        node_ids: Optional[str] = None
    ) -> GetDevResourcesResponse:
        """获取开发资源"""
        params = {"file_key": file_key}
        if node_ids:
            params["node_ids"] = node_ids

        data = await self._make_request("GET", "/dev_resources", token, params)
        return GetDevResourcesResponse(**data)

    async def post_dev_resource(
        self,
        request: PostDevResourceRequest,
        token: str
    ) -> PostDevResourceResponse:
        """创建开发资源"""
        data = await self._make_request(
            "POST",
            "/dev_resources",
            token,
            json_data=request.dict()
        )
        return PostDevResourceResponse(**data)

    async def put_dev_resource(
        self,
        dev_resource_id: str,
        request: PutDevResourceRequest,
        token: str
    ) -> PutDevResourceResponse:
        """更新开发资源"""
        data = await self._make_request(
            "PUT",
            f"/dev_resources/{dev_resource_id}",
            token,
            json_data=request.dict()
        )
        return PutDevResourceResponse(**data)

    async def delete_dev_resource(
        self,
        dev_resource_id: str,
        token: str
    ) -> DeleteDevResourceResponse:
        """删除开发资源"""
        data = await self._make_request("DELETE", f"/dev_resources/{dev_resource_id}", token)
        return DeleteDevResourceResponse(**data)
