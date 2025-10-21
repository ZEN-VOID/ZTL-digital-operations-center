"""
批量处理端点

提供增强版的批量替换和导出API
"""

import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Path as PathParam, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.schemas.batch import (
    BatchReplaceRequest,
    BatchReplaceResponse,
    BatchTaskStatusResponse,
    ProcessingStatus,
)
from ....core.services.batch_processor import FigmaBatchProcessor
from ....core.config import get_settings, Settings
from ....core.database import get_db_session

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/batch", tags=["batch"])


def get_batch_processor(
    db: AsyncSession = Depends(get_db_session),
    settings: Settings = Depends(get_settings),
) -> FigmaBatchProcessor:
    """获取批量处理服务实例"""
    return FigmaBatchProcessor(db, settings)


@router.post(
    "/replace-and-export",
    response_model=BatchReplaceResponse,
    summary="批量替换图片并导出",
    description="""
    批量替换Figma文件中的图片并导出处理后的设计稿

    ## 功能特性

    - **节点匹配规则**: 支持精确匹配和模式匹配（通配符*和?）
    - **批量替换**: 一次性替换多个图片节点
    - **多分辨率导出**: 支持同时导出多种分辨率（1x, 2x, 3x等）
    - **云盘集成**: 可选上传到云存储
    - **异步处理**: 后台异步处理，立即返回任务ID

    ## 工作流程

    1. 验证Figma文件访问权限
    2. 解析节点匹配规则，获取实际节点ID
    3. 批量替换图片节点
    4. 导出处理后的设计稿
    5. （可选）上传到云盘
    6. 返回完整结果

    ## 节点匹配规则示例

    - `"dish-001"`: 精确匹配节点ID为dish-001的节点
    - `"dish-*"`: 匹配所有以dish-开头的节点
    - `"*-photo"`: 匹配所有以-photo结尾的节点
    - `"dish-?-photo"`: 匹配dish-单字符-photo格式的节点

    ## 导出配置示例

    ```json
    {
        "format": "png",
        "scales": [1.0, 2.0, 3.0],
        "save_to_cloud": true,
        "cloud_dir": "/projects/restaurant-menu/2025-09"
    }
    ```
    """,
    responses={
        200: {
            "description": "成功创建任务并处理",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Completed successfully",
                        "task_id": "550e8400-e29b-41d4-a716-446655440000",
                        "status": "completed",
                        "total_replacements": 12,
                        "successful_replacements": 12,
                        "failed_replacements": 0,
                        "exported_files": [
                            {
                                "filename": "dish-001_1.0x.png",
                                "local_path": "./exports/file123/20250930_120000/dish-001_1.0x.png",
                                "cloud_url": "https://cloud.example.com/path/to/dish-001_1.0x.png",
                                "format": "png",
                                "scale": 1.0,
                                "size_bytes": 524288,
                                "node_id": "dish-001",
                            }
                        ],
                        "processing_time": 15.32,
                    }
                }
            },
        },
        400: {"description": "请求参数无效"},
        404: {"description": "文件不存在或无访问权限"},
        500: {"description": "服务器内部错误"},
    },
)
async def batch_replace_and_export(
    request: BatchReplaceRequest,
    background_tasks: BackgroundTasks,
    processor: FigmaBatchProcessor = Depends(get_batch_processor),
) -> BatchReplaceResponse:
    """
    批量替换图片并导出

    此端点支持同步和异步两种处理模式：
    - 同步模式：等待处理完成后返回完整结果（适合小批量）
    - 异步模式：立即返回任务ID，通过状态查询端点获取结果（适合大批量）

    当前实现为同步模式，可根据需要扩展为异步模式。
    """
    try:
        logger.info(
            f"Starting batch replace for file {request.figma_file_id} "
            f"with {len(request.replacement_rules)} rules"
        )

        # 验证请求参数
        if len(request.replacement_rules) > 50:
            raise HTTPException(
                status_code=400, detail="Maximum 50 replacement rules per request"
            )

        # 处理批量替换（同步执行）
        result = await processor.process_batch_replace(request)

        # 根据结果返回相应的HTTP状态码
        if result.status == ProcessingStatus.FAILED:
            raise HTTPException(status_code=500, detail=result.error_message or "Processing failed")

        logger.info(
            f"Batch replace completed for task {result.task_id}: "
            f"{result.successful_replacements}/{result.total_replacements} successful"
        )

        return result

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in batch replace: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/task/{task_id}",
    response_model=BatchTaskStatusResponse,
    summary="查询任务状态",
    description="""
    查询批量处理任务的当前状态和进度

    用于异步处理模式下的状态查询
    """,
)
async def get_task_status(
    task_id: str = PathParam(..., description="任务ID"),
    processor: FigmaBatchProcessor = Depends(get_batch_processor),
) -> BatchTaskStatusResponse:
    """
    查询任务状态

    返回任务的详细状态信息，包括进度、当前步骤和结果
    """
    task = processor.get_task_status(task_id)

    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    # 计算进度
    if task.status == ProcessingStatus.COMPLETED:
        progress = 100.0
    elif task.status == ProcessingStatus.FAILED:
        progress = 0.0
    elif task.total_replacements > 0:
        progress = (task.successful_replacements / task.total_replacements) * 100.0
    else:
        progress = 0.0

    # 当前步骤描述
    step_descriptions = {
        ProcessingStatus.PENDING: "等待处理",
        ProcessingStatus.VALIDATING: "验证文件访问权限",
        ProcessingStatus.REPLACING: "替换图片节点",
        ProcessingStatus.EXPORTING: "导出设计稿",
        ProcessingStatus.UPLOADING: "上传到云盘",
        ProcessingStatus.COMPLETED: "处理完成",
        ProcessingStatus.FAILED: "处理失败",
        ProcessingStatus.CANCELLED: "已取消",
    }

    return BatchTaskStatusResponse(
        task_id=task_id,
        status=task.status,
        progress=progress,
        current_step=step_descriptions.get(task.status, "未知状态"),
        estimated_time_remaining=None,  # TODO: 实现时间估算
        result=task if task.status in [ProcessingStatus.COMPLETED, ProcessingStatus.FAILED] else None,
    )


@router.get(
    "/tasks",
    response_model=list[BatchReplaceResponse],
    summary="列出所有任务",
    description="获取所有批量处理任务的列表（支持分页和过滤）",
)
async def list_tasks(
    status: Optional[ProcessingStatus] = None,
    limit: int = 20,
    offset: int = 0,
    processor: FigmaBatchProcessor = Depends(get_batch_processor),
) -> list[BatchReplaceResponse]:
    """
    列出批量处理任务

    支持按状态过滤和分页
    """
    all_tasks = processor.list_tasks()

    # 状态过滤
    if status:
        all_tasks = [t for t in all_tasks if t.status == status]

    # 排序（最新的在前）
    all_tasks.sort(key=lambda t: t.created_at, reverse=True)

    # 分页
    return all_tasks[offset : offset + limit]


@router.delete(
    "/task/{task_id}",
    summary="取消任务",
    description="取消正在处理的批量替换任务",
)
async def cancel_task(
    task_id: str = PathParam(..., description="任务ID"),
    processor: FigmaBatchProcessor = Depends(get_batch_processor),
) -> dict:
    """
    取消任务

    只能取消状态为PENDING、VALIDATING或REPLACING的任务
    """
    task = processor.get_task_status(task_id)

    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    if task.status in [ProcessingStatus.COMPLETED, ProcessingStatus.FAILED, ProcessingStatus.CANCELLED]:
        raise HTTPException(
            status_code=400, detail=f"Cannot cancel task with status {task.status}"
        )

    # 更新任务状态
    task.status = ProcessingStatus.CANCELLED
    task.message = "Task cancelled by user"
    task.success = False

    logger.info(f"Task {task_id} cancelled")

    return {"message": "Task cancelled successfully", "task_id": task_id}


@router.post(
    "/validate-rules",
    summary="验证替换规则",
    description="""
    验证替换规则并返回匹配的节点信息

    在实际执行替换前，可以使用此端点预览哪些节点会被匹配
    """,
)
async def validate_replacement_rules(
    figma_file_id: str,
    target_patterns: list[str],
    processor: FigmaBatchProcessor = Depends(get_batch_processor),
) -> dict:
    """
    验证替换规则

    返回每个模式匹配到的节点列表
    """
    try:
        # 验证文件访问
        await processor._validate_file_access(figma_file_id)

        # 获取文件结构
        async with processor.figma_client:
            file_data = await processor.figma_client.get_file(figma_file_id)

        if not file_data or "document" not in file_data:
            raise HTTPException(status_code=500, detail="Cannot retrieve file structure")

        # 提取所有节点
        all_nodes = processor._extract_all_nodes(file_data["document"])

        # 匹配每个模式
        match_results = []
        for pattern in target_patterns:
            if "*" in pattern or "?" in pattern:
                matched = processor._match_nodes_by_pattern(pattern, all_nodes)
            else:
                matched = [pattern] if pattern in all_nodes else []

            match_results.append(
                {"pattern": pattern, "matched_nodes": matched, "count": len(matched)}
            )

        return {
            "file_id": figma_file_id,
            "total_nodes": len(all_nodes),
            "match_results": match_results,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Rule validation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))