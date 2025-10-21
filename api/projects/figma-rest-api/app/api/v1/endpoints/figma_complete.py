"""
完整的Figma官方API端点集成
基于Figma官方REST API规范的完整实现
"""

import logging
from typing import List, Optional, Dict, Any, Union
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Body, Header
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.schemas.figma_complete import (
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
    GetTeamComponentSetsResponse,
    GetComponentResponse,
    GetComponentSetResponse,
    
    # Styles
    GetTeamStylesResponse,
    GetStyleResponse,
    
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
from ....core.services.figma_complete_service import FigmaCompleteService
from ....core.config import get_settings
from ....core.database import get_db_session

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/figma-complete", tags=["figma-complete"])


def get_figma_complete_service(
    db: AsyncSession = Depends(get_db_session),
    settings = Depends(get_settings)
) -> FigmaCompleteService:
    """获取完整Figma服务实例"""
    return FigmaCompleteService(db, settings)


def get_figma_token(x_figma_token: str = Header(..., description="Figma API Token")) -> str:
    """获取Figma API Token"""
    return x_figma_token


# ==================== Files API ====================

@router.get(
    "/files/{file_key}",
    response_model=GetFileResponse,
    summary="Get file",
    description="Returns the document referred to by :key as a JSON object"
)
async def get_file(
    file_key: str = Path(..., description="File key"),
    version: Optional[str] = Query(None, description="A specific version ID to get"),
    ids: Optional[str] = Query(None, description="A comma separated list of node IDs to retrieve"),
    depth: Optional[int] = Query(None, description="Positive integer representing how deep into the document tree to traverse"),
    geometry: Optional[str] = Query(None, description="Set to 'paths' to export vector data"),
    plugin_data: Optional[str] = Query(None, description="A comma separated list of plugin IDs and/or the string 'shared'"),
    branch_data: Optional[bool] = Query(False, description="Returns branch metadata for the requested file"),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> GetFileResponse:
    """获取文件信息"""
    return await service.get_file(
        file_key=file_key,
        version=version,
        ids=ids,
        depth=depth,
        geometry=geometry,
        plugin_data=plugin_data,
        branch_data=branch_data,
        token=token
    )


@router.get(
    "/files/{file_key}/nodes",
    response_model=GetFileNodesResponse,
    summary="Get file nodes",
    description="Returns the nodes referenced by :ids as a JSON object"
)
async def get_file_nodes(
    file_key: str = Path(..., description="File key"),
    ids: str = Query(..., description="A comma separated list of node IDs to retrieve"),
    version: Optional[str] = Query(None, description="A specific version ID to get"),
    depth: Optional[int] = Query(None, description="Positive integer representing how deep into the document tree to traverse"),
    geometry: Optional[str] = Query(None, description="Set to 'paths' to export vector data"),
    plugin_data: Optional[str] = Query(None, description="A comma separated list of plugin IDs and/or the string 'shared'"),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> GetFileNodesResponse:
    """获取文件节点"""
    return await service.get_file_nodes(
        file_key=file_key,
        ids=ids,
        version=version,
        depth=depth,
        geometry=geometry,
        plugin_data=plugin_data,
        token=token
    )


@router.get(
    "/files/{file_key}/versions",
    response_model=GetFileVersionsResponse,
    summary="Get file versions",
    description="A list of the version history of a file"
)
async def get_file_versions(
    file_key: str = Path(..., description="File key"),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> GetFileVersionsResponse:
    """获取文件版本历史"""
    return await service.get_file_versions(file_key=file_key, token=token)


# ==================== Images API ====================

@router.get(
    "/images/{file_key}",
    response_model=GetImagesResponse,
    summary="Get image",
    description="Renders images from a file"
)
async def get_images(
    file_key: str = Path(..., description="File key"),
    ids: str = Query(..., description="A comma separated list of node IDs to render"),
    scale: Optional[float] = Query(1, description="A number between 0.01 and 4, the image scaling factor"),
    format: Optional[str] = Query("png", description="A string enum for the image output format"),
    svg_outline_text: Optional[bool] = Query(True, description="Whether text elements are rendered as outlines"),
    svg_include_id: Optional[bool] = Query(False, description="Whether to include id attributes for all SVG elements"),
    svg_include_node_id: Optional[bool] = Query(False, description="Whether to include node id attributes for all SVG elements"),
    svg_simplify_stroke: Optional[bool] = Query(True, description="Whether to simplify inside/outside strokes"),
    contents_only: Optional[bool] = Query(True, description="Whether to exclude overlapping content"),
    use_absolute_bounds: Optional[bool] = Query(False, description="Use absolute bounding box for each node"),
    version: Optional[str] = Query(None, description="A specific version ID to get"),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> GetImagesResponse:
    """渲染图片"""
    return await service.get_images(
        file_key=file_key,
        ids=ids,
        scale=scale,
        format=format,
        svg_outline_text=svg_outline_text,
        svg_include_id=svg_include_id,
        svg_include_node_id=svg_include_node_id,
        svg_simplify_stroke=svg_simplify_stroke,
        contents_only=contents_only,
        use_absolute_bounds=use_absolute_bounds,
        version=version,
        token=token
    )


# ==================== Comments API ====================

@router.get(
    "/files/{file_key}/comments",
    response_model=GetCommentsResponse,
    summary="Get comments",
    description="A list of comments left on the file"
)
async def get_comments(
    file_key: str = Path(..., description="File key"),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> GetCommentsResponse:
    """获取评论"""
    return await service.get_comments(file_key=file_key, token=token)


@router.post(
    "/files/{file_key}/comments",
    response_model=PostCommentResponse,
    summary="Post comment",
    description="Posts a new comment on the file"
)
async def post_comment(
    file_key: str = Path(..., description="File key"),
    request: PostCommentRequest = Body(...),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> PostCommentResponse:
    """发布评论"""
    return await service.post_comment(file_key=file_key, request=request, token=token)


@router.delete(
    "/comments/{comment_id}",
    response_model=DeleteCommentResponse,
    summary="Delete comment",
    description="Deletes a specific comment"
)
async def delete_comment(
    comment_id: str = Path(..., description="Comment ID"),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> DeleteCommentResponse:
    """删除评论"""
    return await service.delete_comment(comment_id=comment_id, token=token)


# ==================== Users API ====================

@router.get(
    "/me",
    response_model=GetUserResponse,
    summary="Get current user",
    description="Returns the user information for the currently authenticated user"
)
async def get_me(
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> GetUserResponse:
    """获取当前用户信息"""
    return await service.get_me(token=token)


# ==================== Projects API ====================

@router.get(
    "/teams/{team_id}/projects",
    response_model=GetTeamProjectsResponse,
    summary="Get team projects",
    description="Lists the projects for a specified team"
)
async def get_team_projects(
    team_id: str = Path(..., description="Team ID"),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> GetTeamProjectsResponse:
    """获取团队项目"""
    return await service.get_team_projects(team_id=team_id, token=token)


@router.get(
    "/projects/{project_id}/files",
    response_model=GetProjectFilesResponse,
    summary="Get project files",
    description="List the files in a given project"
)
async def get_project_files(
    project_id: str = Path(..., description="Project ID"),
    branch_data: Optional[bool] = Query(False, description="Returns branch metadata for the requested files"),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> GetProjectFilesResponse:
    """获取项目文件"""
    return await service.get_project_files(
        project_id=project_id,
        branch_data=branch_data,
        token=token
    )


# ==================== Component Types API ====================

@router.get(
    "/teams/{team_id}/components",
    response_model=GetTeamComponentsResponse,
    summary="Get team components",
    description="Get a paginated list of published components within a team library"
)
async def get_team_components(
    team_id: str = Path(..., description="Team ID"),
    page_size: Optional[int] = Query(30, description="Number of items in a paged list of results"),
    after: Optional[str] = Query(None, description="The pagination cursor value for the next page"),
    before: Optional[str] = Query(None, description="The pagination cursor value for the previous page"),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> GetTeamComponentsResponse:
    """获取团队组件"""
    return await service.get_team_components(
        team_id=team_id,
        page_size=page_size,
        after=after,
        before=before,
        token=token
    )


@router.get(
    "/components/{component_key}",
    response_model=GetComponentResponse,
    summary="Get component",
    description="Get metadata on a component by key"
)
async def get_component(
    component_key: str = Path(..., description="Component key"),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> GetComponentResponse:
    """获取组件信息"""
    return await service.get_component(component_key=component_key, token=token)


# ==================== Variables API ====================

@router.get(
    "/files/{file_key}/variables/local",
    response_model=GetLocalVariablesResponse,
    summary="Get local variables",
    description="Get local variables from a file"
)
async def get_local_variables(
    file_key: str = Path(..., description="File key"),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> GetLocalVariablesResponse:
    """获取本地变量"""
    return await service.get_local_variables(file_key=file_key, token=token)


@router.get(
    "/files/{file_key}/variables/published",
    response_model=GetPublishedVariablesResponse,
    summary="Get published variables",
    description="Get published variables from a file"
)
async def get_published_variables(
    file_key: str = Path(..., description="File key"),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> GetPublishedVariablesResponse:
    """获取已发布变量"""
    return await service.get_published_variables(file_key=file_key, token=token)


@router.post(
    "/files/{file_key}/variables",
    response_model=PostVariablesResponse,
    summary="Post variables",
    description="Create or update variables in a file"
)
async def post_variables(
    file_key: str = Path(..., description="File key"),
    request: PostVariablesRequest = Body(...),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> PostVariablesResponse:
    """创建或更新变量"""
    return await service.post_variables(file_key=file_key, request=request, token=token)


# ==================== Webhooks API ====================

@router.get(
    "/webhooks",
    response_model=GetWebhooksResponse,
    summary="Get webhooks",
    description="Get a list of webhooks"
)
async def get_webhooks(
    team_id: str = Query(..., description="Team ID"),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> GetWebhooksResponse:
    """获取Webhooks列表"""
    return await service.get_webhooks(team_id=team_id, token=token)


@router.post(
    "/webhooks",
    response_model=PostWebhookResponse,
    summary="Create webhook",
    description="Create a new webhook"
)
async def post_webhook(
    request: PostWebhookRequest = Body(...),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> PostWebhookResponse:
    """创建Webhook"""
    return await service.post_webhook(request=request, token=token)


@router.put(
    "/webhooks/{webhook_id}",
    response_model=PutWebhookResponse,
    summary="Update webhook",
    description="Update a webhook"
)
async def put_webhook(
    webhook_id: str = Path(..., description="Webhook ID"),
    request: PutWebhookRequest = Body(...),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> PutWebhookResponse:
    """更新Webhook"""
    return await service.put_webhook(webhook_id=webhook_id, request=request, token=token)


@router.delete(
    "/webhooks/{webhook_id}",
    response_model=DeleteWebhookResponse,
    summary="Delete webhook",
    description="Delete a webhook"
)
async def delete_webhook(
    webhook_id: str = Path(..., description="Webhook ID"),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> DeleteWebhookResponse:
    """删除Webhook"""
    return await service.delete_webhook(webhook_id=webhook_id, token=token)


@router.get(
    "/webhooks/{webhook_id}/requests",
    response_model=GetWebhookRequestsResponse,
    summary="Get webhook requests",
    description="Get recent requests for a webhook"
)
async def get_webhook_requests(
    webhook_id: str = Path(..., description="Webhook ID"),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> GetWebhookRequestsResponse:
    """获取Webhook请求历史"""
    return await service.get_webhook_requests(webhook_id=webhook_id, token=token)


# ==================== Activity Logs API ====================

@router.get(
    "/activity_logs",
    response_model=GetActivityLogsResponse,
    summary="Get activity logs",
    description="Get activity logs for a team"
)
async def get_activity_logs(
    team_id: str = Query(..., description="Team ID"),
    cursor: Optional[str] = Query(None, description="Pagination cursor"),
    limit: Optional[int] = Query(100, description="Number of results to return"),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> GetActivityLogsResponse:
    """获取活动日志"""
    return await service.get_activity_logs(
        team_id=team_id,
        cursor=cursor,
        limit=limit,
        token=token
    )


# ==================== Discovery API ====================

@router.get(
    "/discovery",
    response_model=GetDiscoveryResponse,
    summary="Get discovery",
    description="Get discovery information"
)
async def get_discovery(
    team_id: str = Query(..., description="Team ID"),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> GetDiscoveryResponse:
    """获取发现信息"""
    return await service.get_discovery(team_id=team_id, token=token)


# ==================== Payments API ====================

@router.get(
    "/payments",
    response_model=GetPaymentsResponse,
    summary="Get payments",
    description="Get payment information"
)
async def get_payments(
    team_id: str = Query(..., description="Team ID"),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> GetPaymentsResponse:
    """获取支付信息"""
    return await service.get_payments(team_id=team_id, token=token)


# ==================== Library Analytics API ====================

@router.get(
    "/library_analytics",
    response_model=GetLibraryAnalyticsResponse,
    summary="Get library analytics",
    description="Get library analytics data"
)
async def get_library_analytics(
    team_id: str = Query(..., description="Team ID"),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> GetLibraryAnalyticsResponse:
    """获取库分析数据"""
    return await service.get_library_analytics(team_id=team_id, token=token)


# ==================== Dev Resources API ====================

@router.get(
    "/dev_resources",
    response_model=GetDevResourcesResponse,
    summary="Get dev resources",
    description="Get development resources"
)
async def get_dev_resources(
    file_key: str = Query(..., description="File key"),
    node_ids: Optional[str] = Query(None, description="Comma-separated list of node IDs"),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> GetDevResourcesResponse:
    """获取开发资源"""
    return await service.get_dev_resources(
        file_key=file_key,
        node_ids=node_ids,
        token=token
    )


@router.post(
    "/dev_resources",
    response_model=PostDevResourceResponse,
    summary="Create dev resource",
    description="Create a development resource"
)
async def post_dev_resource(
    request: PostDevResourceRequest = Body(...),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> PostDevResourceResponse:
    """创建开发资源"""
    return await service.post_dev_resource(request=request, token=token)


@router.put(
    "/dev_resources/{dev_resource_id}",
    response_model=PutDevResourceResponse,
    summary="Update dev resource",
    description="Update a development resource"
)
async def put_dev_resource(
    dev_resource_id: str = Path(..., description="Dev resource ID"),
    request: PutDevResourceRequest = Body(...),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> PutDevResourceResponse:
    """更新开发资源"""
    return await service.put_dev_resource(
        dev_resource_id=dev_resource_id,
        request=request,
        token=token
    )


@router.delete(
    "/dev_resources/{dev_resource_id}",
    response_model=DeleteDevResourceResponse,
    summary="Delete dev resource",
    description="Delete a development resource"
)
async def delete_dev_resource(
    dev_resource_id: str = Path(..., description="Dev resource ID"),
    token: str = Depends(get_figma_token),
    service: FigmaCompleteService = Depends(get_figma_complete_service)
) -> DeleteDevResourceResponse:
    """删除开发资源"""
    return await service.delete_dev_resource(dev_resource_id=dev_resource_id, token=token)
