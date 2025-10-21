"""
量产设计工作流端点
"""

import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Path, BackgroundTasks, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.schemas.figma import (
    ProductionWorkflowRequest,
    ProductionWorkflowResponse,
    ProductionWorkflowStatus,
    ProductionBatch,
    TaskOrchestrationConfig,
    TaskQueueStatus,
    BulkOperationRequest,
    BulkOperationResponse
)
from ....core.services.production_workflow_service import ProductionWorkflowService
from ....core.services.task_orchestration_service import TaskOrchestrationService
from ....core.config import get_settings
from ....core.database import get_db_session

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/production", tags=["production-workflow"])


def get_production_service(
    db: AsyncSession = Depends(get_db_session),
    settings = Depends(get_settings)
) -> ProductionWorkflowService:
    """获取量产工作流服务实例"""
    return ProductionWorkflowService(db, settings)


def get_orchestration_service(
    db: AsyncSession = Depends(get_db_session),
    settings = Depends(get_settings)
) -> TaskOrchestrationService:
    """获取任务编排服务实例"""
    return TaskOrchestrationService(db, settings)


@router.post(
    "/workflow",
    response_model=ProductionWorkflowResponse,
    summary="创建量产设计工作流",
    description="创建一个量产设计工作流，支持6张一批的批量处理"
)
async def create_production_workflow(
    request: ProductionWorkflowRequest,
    background_tasks: BackgroundTasks,
    service: ProductionWorkflowService = Depends(get_production_service)
) -> ProductionWorkflowResponse:
    """
    创建量产设计工作流
    
    - **file_key**: Figma文件键
    - **template_frame_id**: 模板画板ID
    - **image_urls**: 要替换的图片URL列表
    - **target_node_ids**: 目标节点ID列表
    - **batch_size**: 每批处理数量 (1-24)
    - **export_format**: 导出格式 (png, jpg, svg, pdf)
    - **export_scale**: 导出缩放比例 (0.1-4.0)
    - **throttle_delay**: 批次间延迟(秒)
    - **callback_url**: 进度回调URL
    - **workflow_name**: 工作流名称
    """
    try:
        # 验证输入参数
        if len(request.image_urls) != len(request.target_node_ids):
            raise HTTPException(
                status_code=400, 
                detail="图片URL数量必须与目标节点ID数量相等"
            )
        
        # 创建工作流
        workflow = await service.create_workflow(request)
        
        # 在后台执行工作流
        background_tasks.add_task(service.execute_workflow, workflow.workflow_id)
        
        return workflow
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to create production workflow: {e}")
        raise HTTPException(status_code=500, detail="创建工作流失败")


@router.get(
    "/workflow/{workflow_id}",
    response_model=ProductionWorkflowResponse,
    summary="获取量产工作流状态",
    description="获取指定量产工作流的详细状态信息"
)
async def get_workflow_status(
    workflow_id: str = Path(..., description="工作流ID"),
    service: ProductionWorkflowService = Depends(get_production_service)
) -> ProductionWorkflowResponse:
    """
    获取量产工作流状态
    
    返回工作流的详细信息，包括批次进度和导出结果
    """
    workflow = await service.get_workflow_status(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="工作流不存在")
    return workflow


@router.post(
    "/workflow/{workflow_id}/pause",
    summary="暂停量产工作流",
    description="暂停指定的量产工作流"
)
async def pause_workflow(
    workflow_id: str = Path(..., description="工作流ID"),
    service: ProductionWorkflowService = Depends(get_production_service)
) -> dict:
    """
    暂停量产工作流
    
    暂停当前正在执行的工作流，可以稍后恢复
    """
    workflow = await service.get_workflow_status(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="工作流不存在")
    
    if workflow.status != ProductionWorkflowStatus.PROCESSING:
        raise HTTPException(status_code=400, detail="只能暂停正在处理的工作流")
    
    success = await service.pause_workflow(workflow_id)
    if not success:
        raise HTTPException(status_code=400, detail="暂停工作流失败")
    
    return {"message": "工作流已暂停", "workflow_id": workflow_id}


@router.post(
    "/workflow/{workflow_id}/resume",
    summary="恢复量产工作流",
    description="恢复已暂停的量产工作流"
)
async def resume_workflow(
    workflow_id: str,
    background_tasks: BackgroundTasks,
    service: ProductionWorkflowService = Depends(get_production_service)
) -> dict:
    """
    恢复量产工作流
    
    恢复已暂停的工作流继续执行
    """
    workflow = await service.get_workflow_status(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="工作流不存在")
    
    if workflow.status != ProductionWorkflowStatus.PAUSED:
        raise HTTPException(status_code=400, detail="只能恢复已暂停的工作流")
    
    # 在后台恢复执行
    background_tasks.add_task(service.resume_workflow, workflow_id)
    
    return {"message": "工作流已恢复", "workflow_id": workflow_id}


@router.post(
    "/workflow/{workflow_id}/cancel",
    summary="取消量产工作流",
    description="取消指定的量产工作流"
)
async def cancel_workflow(
    workflow_id: str = Path(..., description="工作流ID"),
    service: ProductionWorkflowService = Depends(get_production_service)
) -> dict:
    """
    取消量产工作流
    
    取消当前工作流，已完成的批次不会回滚
    """
    workflow = await service.get_workflow_status(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="工作流不存在")
    
    if workflow.status in [ProductionWorkflowStatus.COMPLETED, ProductionWorkflowStatus.FAILED]:
        raise HTTPException(status_code=400, detail="工作流已完成或失败，无法取消")
    
    success = await service.cancel_workflow(workflow_id)
    if not success:
        raise HTTPException(status_code=400, detail="取消工作流失败")
    
    return {"message": "工作流已取消", "workflow_id": workflow_id}


@router.get(
    "/workflows",
    response_model=List[ProductionWorkflowResponse],
    summary="获取量产工作流列表",
    description="分页获取量产工作流列表，支持状态过滤"
)
async def list_workflows(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页大小"),
    status: Optional[ProductionWorkflowStatus] = Query(None, description="状态过滤"),
    file_key: Optional[str] = Query(None, description="文件键过滤"),
    service: ProductionWorkflowService = Depends(get_production_service)
) -> List[ProductionWorkflowResponse]:
    """
    获取量产工作流列表
    
    支持分页和状态过滤
    """
    workflows = await service.list_workflows(page, page_size, status, file_key)
    return workflows


@router.get(
    "/workflow/{workflow_id}/batches",
    response_model=List[ProductionBatch],
    summary="获取工作流批次详情",
    description="获取指定工作流的所有批次详情"
)
async def get_workflow_batches(
    workflow_id: str = Path(..., description="工作流ID"),
    service: ProductionWorkflowService = Depends(get_production_service)
) -> List[ProductionBatch]:
    """
    获取工作流批次详情
    
    返回工作流中所有批次的详细信息
    """
    batches = await service.get_workflow_batches(workflow_id)
    if batches is None:
        raise HTTPException(status_code=404, detail="工作流不存在")
    return batches


# ==================== 任务编排管理端点 ====================

@router.get(
    "/orchestration/status",
    response_model=TaskQueueStatus,
    summary="获取任务编排状态",
    description="获取任务编排系统的整体状态"
)
async def get_orchestration_status(
    service: TaskOrchestrationService = Depends(get_orchestration_service)
) -> TaskQueueStatus:
    """
    获取任务编排状态
    
    返回任务队列的整体状态信息
    """
    status = await service.get_queue_status()
    return status


@router.post(
    "/orchestration/config",
    summary="更新任务编排配置",
    description="更新任务编排系统的配置参数"
)
async def update_orchestration_config(
    config: TaskOrchestrationConfig,
    service: TaskOrchestrationService = Depends(get_orchestration_service)
) -> dict:
    """
    更新任务编排配置
    
    更新并发数、批次大小、节流延迟等配置参数
    """
    try:
        await service.update_config(config)
        return {"message": "配置更新成功", "config": config.dict()}
    except Exception as e:
        logger.error(f"Failed to update orchestration config: {e}")
        raise HTTPException(status_code=500, detail="配置更新失败")


@router.post(
    "/orchestration/cleanup",
    summary="清理已完成任务",
    description="清理指定天数前的已完成任务"
)
async def cleanup_completed_tasks(
    background_tasks: BackgroundTasks,
    service: TaskOrchestrationService = Depends(get_orchestration_service),
    days: int = Query(7, ge=1, le=365, description="保留天数")
) -> dict:
    """
    清理已完成任务
    
    在后台异步清理指定天数前的已完成任务
    """
    background_tasks.add_task(service.cleanup_old_tasks, days)
    return {"message": f"清理任务已启动，将清理{days}天前的已完成任务"}


# ==================== 批量操作端点 ====================

@router.post(
    "/bulk-operation",
    response_model=BulkOperationResponse,
    summary="创建批量操作",
    description="创建跨多个文件的批量操作"
)
async def create_bulk_operation(
    request: BulkOperationRequest,
    background_tasks: BackgroundTasks,
    service: ProductionWorkflowService = Depends(get_production_service)
) -> BulkOperationResponse:
    """
    创建批量操作
    
    支持跨多个Figma文件的批量替换、导出或工作流操作
    """
    try:
        operation = await service.create_bulk_operation(request)
        
        # 在后台执行批量操作
        background_tasks.add_task(service.execute_bulk_operation, operation.operation_id)
        
        return operation
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to create bulk operation: {e}")
        raise HTTPException(status_code=500, detail="创建批量操作失败")


@router.get(
    "/bulk-operation/{operation_id}",
    response_model=BulkOperationResponse,
    summary="获取批量操作状态",
    description="获取指定批量操作的状态信息"
)
async def get_bulk_operation_status(
    operation_id: str = Path(..., description="操作ID"),
    service: ProductionWorkflowService = Depends(get_production_service)
) -> BulkOperationResponse:
    """
    获取批量操作状态
    
    返回批量操作的详细状态信息
    """
    operation = await service.get_bulk_operation_status(operation_id)
    if not operation:
        raise HTTPException(status_code=404, detail="批量操作不存在")
    return operation
