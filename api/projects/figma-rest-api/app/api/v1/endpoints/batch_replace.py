"""
批量替换图片功能端点
"""

import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Path, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.schemas.figma import (
    BatchReplaceRequest,
    BatchReplaceResponse,
    BatchReplaceStatus,
    PluginReplaceRequest,
    PluginReplaceResponse,
    ImageReplaceItem
)
from ....core.services.figma_service import FigmaService
from ....core.services.batch_replace_service import BatchReplaceService
from ....core.config import get_settings
from ....core.database import get_db_session

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/batch-replace", tags=["batch-replace"])


def get_batch_replace_service(
    db: AsyncSession = Depends(get_db_session),
    settings = Depends(get_settings)
) -> BatchReplaceService:
    """获取批量替换服务实例"""
    return BatchReplaceService(db, settings)


@router.post(
    "/",
    response_model=BatchReplaceResponse,
    summary="创建批量替换任务",
    description="创建一个批量替换图片的任务，支持自动导出"
)
async def create_batch_replace_task(
    request: BatchReplaceRequest,
    background_tasks: BackgroundTasks,
    service: BatchReplaceService = Depends(get_batch_replace_service)
) -> BatchReplaceResponse:
    """
    创建批量替换任务
    
    - **file_key**: Figma文件键
    - **replacements**: 替换项列表，每项包含节点ID和新图片URL
    - **batch_name**: 批次名称（可选）
    - **callback_url**: 完成后回调URL（可选）
    - **auto_export**: 替换完成后是否自动导出
    - **export_format**: 导出格式 (png, jpg, svg, pdf)
    - **export_scale**: 导出缩放比例 (0.1-4.0)
    """
    try:
        # 验证文件访问权限
        figma_service = FigmaService(service.db, service.settings)
        file_info = await figma_service.get_file_info(request.file_key)
        if not file_info:
            raise HTTPException(status_code=404, detail="文件不存在或无访问权限")
        
        # 创建批量替换任务
        task = await service.create_batch_replace_task(request)
        
        # 在后台执行替换任务
        background_tasks.add_task(service.execute_batch_replace, task.task_id)
        
        return task
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to create batch replace task: {e}")
        raise HTTPException(status_code=500, detail="创建任务失败")


@router.get(
    "/{task_id}",
    response_model=BatchReplaceResponse,
    summary="获取批量替换任务状态",
    description="获取指定批量替换任务的详细状态信息"
)
async def get_batch_replace_status(
    task_id: str = Path(..., description="任务ID"),
    service: BatchReplaceService = Depends(get_batch_replace_service)
) -> BatchReplaceResponse:
    """
    获取批量替换任务状态
    
    返回任务的详细信息，包括进度、状态和导出结果
    """
    task = await service.get_task_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task


@router.post(
    "/{task_id}/retry",
    response_model=dict,
    summary="重试失败的替换项",
    description="重试指定任务中失败的替换项"
)
async def retry_failed_items(
    task_id: str,
    background_tasks: BackgroundTasks,
    service: BatchReplaceService = Depends(get_batch_replace_service),
    failed_node_ids: Optional[List[str]] = None
) -> dict:
    """
    重试失败的替换项
    
    - **failed_node_ids**: 要重试的节点ID列表（可选，为空则重试所有失败项）
    """
    task = await service.get_task_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    if task.status == BatchReplaceStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="任务已完成，无需重试")
    
    # 在后台执行重试
    background_tasks.add_task(service.retry_failed_items, task_id, failed_node_ids)
    
    return {"message": "重试已开始", "task_id": task_id}


@router.delete(
    "/{task_id}",
    summary="取消批量替换任务",
    description="取消指定的批量替换任务"
)
async def cancel_batch_replace_task(
    task_id: str = Path(..., description="任务ID"),
    service: BatchReplaceService = Depends(get_batch_replace_service)
) -> dict:
    """
    取消批量替换任务
    
    只能取消状态为PENDING或REPLACING的任务
    """
    task = await service.get_task_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    if task.status in [BatchReplaceStatus.COMPLETED, BatchReplaceStatus.FAILED]:
        raise HTTPException(status_code=400, detail="任务已完成或失败，无法取消")
    
    success = await service.cancel_task(task_id)
    if not success:
        raise HTTPException(status_code=400, detail="取消任务失败")
    
    return {"message": "任务已取消", "task_id": task_id}


@router.get(
    "/",
    response_model=List[BatchReplaceResponse],
    summary="获取批量替换任务列表",
    description="分页获取批量替换任务列表，支持状态过滤"
)
async def list_batch_replace_tasks(
    page: int = 1,
    page_size: int = 20,
    status: Optional[BatchReplaceStatus] = None,
    file_key: Optional[str] = None,
    service: BatchReplaceService = Depends(get_batch_replace_service)
) -> List[BatchReplaceResponse]:
    """
    获取批量替换任务列表
    
    支持分页和状态过滤
    """
    tasks = await service.list_tasks(page, page_size, status, file_key)
    return tasks


# ==================== 插件桥接端点 ====================

@router.post(
    "/plugin/replace",
    response_model=PluginReplaceResponse,
    summary="插件替换图片接口",
    description="供Figma插件调用的图片替换接口"
)
async def plugin_replace_images(
    request: PluginReplaceRequest,
    service: BatchReplaceService = Depends(get_batch_replace_service)
) -> PluginReplaceResponse:
    """
    插件替换图片接口
    
    由Figma插件调用，执行实际的图片替换操作
    """
    try:
        result = await service.handle_plugin_replace(request)
        return result
    except Exception as e:
        logger.error(f"Plugin replace failed: {e}")
        return PluginReplaceResponse(
            success=False,
            task_id=request.task_id,
            completed_count=0,
            failed_count=len(request.replacements),
            error_message=str(e),
            failed_items=[item.node_id for item in request.replacements]
        )


@router.post(
    "/plugin/callback",
    summary="插件回调接口",
    description="插件操作完成后的回调接口"
)
async def plugin_callback(
    task_id: str,
    success: bool,
    completed_count: int = 0,
    failed_count: int = 0,
    error_message: Optional[str] = None,
    export_urls: Optional[List[str]] = None,
    service: BatchReplaceService = Depends(get_batch_replace_service)
) -> dict:
    """
    插件回调接口
    
    插件完成操作后调用此接口更新任务状态
    """
    try:
        await service.handle_plugin_callback(
            task_id=task_id,
            success=success,
            completed_count=completed_count,
            failed_count=failed_count,
            error_message=error_message,
            export_urls=export_urls or []
        )
        return {"message": "回调处理成功", "task_id": task_id}
    except Exception as e:
        logger.error(f"Plugin callback failed: {e}")
        raise HTTPException(status_code=500, detail="回调处理失败")


@router.get(
    "/plugin/health",
    summary="插件健康检查",
    description="检查插件桥接服务的健康状态"
)
async def plugin_health_check() -> dict:
    """
    插件健康检查
    
    检查插件桥接服务是否正常运行
    """
    return {
        "status": "healthy",
        "service": "batch-replace-plugin-bridge",
        "timestamp": "2025-09-28T11:00:00Z",
        "version": "1.0.0"
    }
