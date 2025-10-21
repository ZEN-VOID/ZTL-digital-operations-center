"""
Figma API路由端点
"""

import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Path, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.schemas.figma import (
    BatchExportRequest,
    FigmaExportImagesRequest,
    FigmaTaskResponse,
    FigmaBatchResponse,
    FigmaFileResponse,
    FigmaExportResponse,
    FigmaGetFileResponse,
    FigmaGetFileNodesResponse,
    FigmaFileMetaResponse,
    TaskRetryRequest,
    TaskListResponse,
    FigmaHealthResponse,
    FigmaTaskStatus
)
from ....core.services.figma_service import FigmaService
from ....core.config import get_settings
from ....core.database import get_db_session


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/figma", tags=["figma"])

# 官方Figma API兼容路由
figma_api_router = APIRouter(prefix="/v1", tags=["figma-api"])


def get_figma_service(
    db: AsyncSession = Depends(get_db_session),
    settings = Depends(get_settings)
) -> FigmaService:
    """获取Figma服务实例"""
    return FigmaService(db, settings)


@router.post(
    "/batch-export",
    response_model=FigmaTaskResponse,
    summary="创建批量导出任务",
    description="创建一个新的Figma批量导出任务，支持多节点并发导出"
)
async def create_batch_export(
    request: BatchExportRequest,
    figma_service: FigmaService = Depends(get_figma_service)
) -> FigmaTaskResponse:
    """
    创建批量导出任务
    
    - **file_key**: Figma文件键
    - **node_ids**: 要导出的节点ID列表
    - **export_format**: 导出格式 (png, jpg, svg, pdf)
    - **batch_size**: 批次大小 (1-20)
    - **scale**: 缩放比例 (0.1-4.0)
    - **output_directory**: 输出目录路径 (可选)
    """
    try:
        return await figma_service.create_batch_export_task(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to create batch export task: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/task/{task_id}",
    response_model=FigmaTaskResponse,
    summary="获取任务状态",
    description="获取指定任务的详细状态信息"
)
async def get_task_status(
    task_id: str = Path(..., description="任务ID"),
    figma_service: FigmaService = Depends(get_figma_service)
) -> FigmaTaskResponse:
    """
    获取任务状态
    
    返回任务的详细信息，包括进度、状态和错误信息
    """
    task = await figma_service.get_task_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post(
    "/task/{task_id}/retry",
    response_model=dict,
    summary="重试失败任务",
    description="重试指定任务中失败的批次"
)
async def retry_task(
    task_id: str = Path(..., description="任务ID"),
    retry_request: TaskRetryRequest = None,
    figma_service: FigmaService = Depends(get_figma_service)
) -> dict:
    """
    重试失败的批次
    
    - **batch_ids**: 要重试的批次ID列表 (可选，为空则重试所有失败批次)
    - **reset_retry_count**: 是否重置重试计数
    """
    if retry_request and retry_request.batch_ids:
        # 重试指定批次
        success = False
        for batch_id in retry_request.batch_ids:
            batch_success = await figma_service.retry_failed_batch(task_id, batch_id)
            success = success or batch_success
    else:
        # 重试所有失败批次
        success = await figma_service.retry_failed_batch(task_id)
    
    if not success:
        raise HTTPException(status_code=400, detail="No retryable batches found")
    
    return {"message": "Retry started successfully", "task_id": task_id}


@router.get(
    "/tasks",
    response_model=TaskListResponse,
    summary="获取任务列表",
    description="分页获取任务列表，支持状态过滤"
)
async def list_tasks(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页大小"),
    status: Optional[FigmaTaskStatus] = Query(None, description="状态过滤"),
    figma_service: FigmaService = Depends(get_figma_service)
) -> TaskListResponse:
    """
    获取任务列表
    
    支持分页和状态过滤
    """
    tasks, total = await figma_service.list_tasks(page, page_size, status)
    
    has_next = (page * page_size) < total
    
    return TaskListResponse(
        tasks=tasks,
        total=total,
        page=page,
        page_size=page_size,
        has_next=has_next
    )


@router.get(
    "/files/{file_key}",
    response_model=dict,
    summary="获取文件信息",
    description="获取Figma文件的基本信息"
)
async def get_file_info(
    file_key: str = Path(..., description="Figma文件键"),
    figma_service: FigmaService = Depends(get_figma_service)
) -> dict:
    """
    获取Figma文件信息
    
    返回文件的基本信息和结构
    """
    file_info = await figma_service.get_file_info(file_key)
    if not file_info:
        raise HTTPException(status_code=404, detail="File not found or access denied")
    return file_info


@router.get(
    "/download/{task_id}",
    summary="下载导出结果",
    description="下载指定任务的导出结果压缩包"
)
async def download_export_results(
    task_id: str = Path(..., description="任务ID"),
    figma_service: FigmaService = Depends(get_figma_service)
):
    """
    下载导出结果
    
    返回包含所有导出图片的ZIP文件
    """
    task = await figma_service.get_task_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.status != FigmaTaskStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Task not completed yet")
    
    # TODO: 实现ZIP文件创建和下载逻辑
    # 这里需要创建一个包含所有导出图片的ZIP文件
    raise HTTPException(status_code=501, detail="Download feature not implemented yet")


@router.delete(
    "/task/{task_id}",
    summary="删除任务",
    description="删除指定任务及其相关文件"
)
async def delete_task(
    task_id: str = Path(..., description="任务ID"),
    figma_service: FigmaService = Depends(get_figma_service)
) -> dict:
    """
    删除任务
    
    删除任务记录和相关的导出文件
    """
    # TODO: 实现任务删除逻辑
    raise HTTPException(status_code=501, detail="Delete feature not implemented yet")


@router.post(
    "/cleanup",
    summary="清理旧任务",
    description="清理指定天数前的已完成任务"
)
async def cleanup_old_tasks(
    days: int = Query(7, ge=1, le=365, description="保留天数"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    figma_service: FigmaService = Depends(get_figma_service)
) -> dict:
    """
    清理旧任务
    
    在后台异步清理指定天数前的已完成任务
    """
    # 在后台执行清理任务
    background_tasks.add_task(figma_service.cleanup_old_tasks, days)
    
    return {"message": f"Cleanup task started for tasks older than {days} days"}


@router.get(
    "/health",
    response_model=FigmaHealthResponse,
    summary="健康检查",
    description="检查Figma服务的健康状态"
)
async def health_check(
    figma_service: FigmaService = Depends(get_figma_service)
) -> FigmaHealthResponse:
    """
    健康检查
    
    检查Figma API连接和数据库连接状态
    """
    health_data = await figma_service.health_check()
    
    return FigmaHealthResponse(
        status=health_data["status"],
        figma_api_available=health_data["figma_api_available"],
        database_connected=health_data["database_connected"],
        timestamp=health_data["timestamp"],
        version=health_data["version"]
    )


# ==================== 官方Figma API兼容端点 ====================

@figma_api_router.get(
    "/files/{file_key}",
    response_model=FigmaGetFileResponse,
    summary="Get file JSON",
    description="获取Figma文件的JSON数据 - 官方API兼容端点"
)
async def get_file_official(
    file_key: str = Path(..., description="Figma文件键"),
    version: Optional[str] = Query(None, description="特定版本ID"),
    ids: Optional[str] = Query(None, description="逗号分隔的节点ID列表"),
    depth: Optional[int] = Query(None, description="遍历深度"),
    geometry: Optional[str] = Query(None, description="几何数据类型"),
    plugin_data: Optional[str] = Query(None, description="插件数据"),
    branch_data: Optional[bool] = Query(False, description="分支数据"),
    figma_service: FigmaService = Depends(get_figma_service)
) -> FigmaGetFileResponse:
    """
    获取Figma文件JSON - 官方API兼容

    符合官方API规范的文件获取端点
    """
    try:
        figma_client = await figma_service.get_figma_client()
        async with figma_client:
            # 构建查询参数
            params = {}
            if version:
                params["version"] = version
            if ids:
                params["ids"] = ids
            if depth is not None:
                params["depth"] = str(depth)
            if geometry:
                params["geometry"] = geometry
            if plugin_data:
                params["plugin_data"] = plugin_data
            if branch_data:
                params["branch_data"] = str(branch_data).lower()

            # 调用官方API
            if params:
                file_data = await figma_client._make_request("GET", f"files/{file_key}", params=params)
            else:
                file_data = await figma_client.get_file(file_key)

            return FigmaGetFileResponse(**file_data)

    except Exception as e:
        logger.error(f"Failed to get file {file_key}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@figma_api_router.get(
    "/files/{file_key}/nodes",
    response_model=FigmaGetFileNodesResponse,
    summary="Get file JSON for specific nodes",
    description="获取Figma文件中特定节点的JSON数据 - 官方API兼容端点"
)
async def get_file_nodes_official(
    file_key: str = Path(..., description="Figma文件键"),
    ids: str = Query(..., description="逗号分隔的节点ID列表"),
    version: Optional[str] = Query(None, description="特定版本ID"),
    depth: Optional[int] = Query(None, description="遍历深度"),
    geometry: Optional[str] = Query(None, description="几何数据类型"),
    plugin_data: Optional[str] = Query(None, description="插件数据"),
    figma_service: FigmaService = Depends(get_figma_service)
) -> FigmaGetFileNodesResponse:
    """
    获取文件节点JSON - 官方API兼容

    符合官方API规范的节点获取端点
    """
    try:
        figma_client = await figma_service.get_figma_client()
        async with figma_client:
            # 构建查询参数
            params = {"ids": ids}
            if version:
                params["version"] = version
            if depth is not None:
                params["depth"] = str(depth)
            if geometry:
                params["geometry"] = geometry
            if plugin_data:
                params["plugin_data"] = plugin_data

            # 调用官方API
            nodes_data = await figma_client._make_request("GET", f"files/{file_key}/nodes", params=params)

            return FigmaGetFileNodesResponse(**nodes_data)

    except Exception as e:
        logger.error(f"Failed to get file nodes {file_key}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@figma_api_router.get(
    "/images/{file_key}",
    response_model=FigmaExportResponse,
    summary="Render images of file nodes",
    description="渲染Figma文件节点为图片 - 官方API兼容端点"
)
async def export_images_official(
    file_key: str = Path(..., description="Figma文件键"),
    ids: str = Query(..., description="逗号分隔的节点ID列表"),
    version: Optional[str] = Query(None, description="特定版本ID"),
    scale: Optional[float] = Query(1.0, description="图像缩放因子", ge=0.01, le=4.0),
    format: Optional[str] = Query("png", description="图像输出格式"),
    svg_outline_text: Optional[bool] = Query(True, description="SVG中文本是否渲染为轮廓"),
    svg_include_id: Optional[bool] = Query(False, description="是否为SVG元素包含id属性"),
    svg_include_node_id: Optional[bool] = Query(False, description="是否为SVG元素包含node-id属性"),
    svg_simplify_stroke: Optional[bool] = Query(True, description="是否简化SVG描边"),
    contents_only: Optional[bool] = Query(True, description="是否排除重叠内容"),
    use_absolute_bounds: Optional[bool] = Query(False, description="是否使用绝对边界"),
    figma_service: FigmaService = Depends(get_figma_service)
) -> FigmaExportResponse:
    """
    导出图片 - 官方API兼容

    符合官方API规范的图片导出端点
    """
    try:
        # 验证格式
        allowed_formats = ["jpg", "png", "svg", "pdf"]
        if format not in allowed_formats:
            raise HTTPException(status_code=400, detail=f"格式必须是以下之一: {allowed_formats}")

        # 解析节点ID
        node_ids = [id.strip() for id in ids.split(',')]
        if not node_ids or not all(node_ids):
            raise HTTPException(status_code=400, detail="节点ID列表不能为空")

        figma_client = await figma_service.get_figma_client()
        async with figma_client:
            # 调用官方API
            export_data = await figma_client.export_images(
                file_key=file_key,
                node_ids=node_ids,
                format=format,
                scale=scale,
                version=version,
                svg_outline_text=svg_outline_text,
                svg_include_id=svg_include_id,
                svg_include_node_id=svg_include_node_id,
                svg_simplify_stroke=svg_simplify_stroke,
                contents_only=contents_only,
                use_absolute_bounds=use_absolute_bounds
            )

            return FigmaExportResponse(**export_data)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to export images from {file_key}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@figma_api_router.get(
    "/files/{file_key}/meta",
    response_model=FigmaFileMetaResponse,
    summary="Get file metadata",
    description="获取Figma文件元数据 - 官方API兼容端点"
)
async def get_file_meta_official(
    file_key: str = Path(..., description="Figma文件键"),
    figma_service: FigmaService = Depends(get_figma_service)
) -> FigmaFileMetaResponse:
    """
    获取文件元数据 - 官方API兼容

    符合官方API规范的文件元数据端点
    """
    try:
        figma_client = await figma_service.get_figma_client()
        async with figma_client:
            # 调用官方API
            meta_data = await figma_client._make_request("GET", f"files/{file_key}/meta")

            return FigmaFileMetaResponse(**meta_data)

    except Exception as e:
        logger.error(f"Failed to get file meta {file_key}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
