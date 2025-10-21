"""
量产设计工作流服务
"""

import asyncio
import logging
import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.figma import (
    ProductionWorkflowRequest,
    ProductionWorkflowResponse,
    ProductionWorkflowStatus,
    ProductionBatch,
    ImageReplaceItem,
    BulkOperationRequest,
    BulkOperationResponse
)
from ..config import Settings
from .batch_replace_service import BatchReplaceService
from .figma_service import FigmaService

logger = logging.getLogger(__name__)


class ProductionWorkflowService:
    """量产设计工作流服务"""
    
    def __init__(self, db: AsyncSession, settings: Settings):
        self.db = db
        self.settings = settings
        self.batch_replace_service = BatchReplaceService(db, settings)
        self.figma_service = FigmaService(db, settings)
        # 内存中的工作流存储（生产环境应使用数据库）
        self._workflows: Dict[str, ProductionWorkflowResponse] = {}
        self._bulk_operations: Dict[str, BulkOperationResponse] = {}
        
    async def create_workflow(
        self, 
        request: ProductionWorkflowRequest
    ) -> ProductionWorkflowResponse:
        """创建量产设计工作流"""
        workflow_id = str(uuid.uuid4())
        
        # 验证输入参数
        if len(request.image_urls) != len(request.target_node_ids):
            raise ValueError("图片URL数量必须与目标节点ID数量相等")
        
        # 计算批次数量
        total_images = len(request.image_urls)
        total_batches = (total_images + request.batch_size - 1) // request.batch_size
        
        # 创建批次
        batches = []
        for i in range(total_batches):
            start_idx = i * request.batch_size
            end_idx = min(start_idx + request.batch_size, total_images)
            
            batch_replacements = []
            for j in range(start_idx, end_idx):
                batch_replacements.append(ImageReplaceItem(
                    node_id=request.target_node_ids[j],
                    image_url=request.image_urls[j],
                    image_name=f"image_{j+1}"
                ))
            
            batch = ProductionBatch(
                batch_id=f"{workflow_id}_batch_{i+1}",
                frame_id=request.template_frame_id,
                replacements=batch_replacements,
                batch_size=len(batch_replacements)
            )
            batches.append(batch)
        
        # 创建工作流
        workflow = ProductionWorkflowResponse(
            workflow_id=workflow_id,
            status=ProductionWorkflowStatus.PENDING,
            file_key=request.file_key,
            total_batches=total_batches,
            completed_batches=0,
            failed_batches=0,
            total_images=total_images,
            completed_images=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            estimated_completion=datetime.now() + timedelta(
                seconds=total_batches * (request.throttle_delay + 10)  # 估算时间
            ),
            export_urls=[],
            batches=batches
        )
        
        # 存储工作流信息
        self._workflows[workflow_id] = workflow
        self._store_workflow_request(workflow_id, request)
        
        logger.info(f"Created production workflow {workflow_id} with {total_batches} batches")
        return workflow
    
    def _store_workflow_request(self, workflow_id: str, request: ProductionWorkflowRequest):
        """存储工作流请求详情"""
        setattr(self._workflows[workflow_id], '_request', request)
    
    def _get_workflow_request(self, workflow_id: str) -> Optional[ProductionWorkflowRequest]:
        """获取工作流请求详情"""
        workflow = self._workflows.get(workflow_id)
        return getattr(workflow, '_request', None) if workflow else None
    
    async def execute_workflow(self, workflow_id: str):
        """执行量产设计工作流"""
        workflow = self._workflows.get(workflow_id)
        request = self._get_workflow_request(workflow_id)
        
        if not workflow or not request:
            logger.error(f"Workflow {workflow_id} not found")
            return
        
        try:
            workflow.status = ProductionWorkflowStatus.PROCESSING
            workflow.updated_at = datetime.now()
            
            logger.info(f"Starting production workflow {workflow_id}")
            
            # 逐批处理
            for i, batch in enumerate(workflow.batches):
                # 检查是否被暂停或取消
                current_workflow = self._workflows.get(workflow_id)
                if not current_workflow or current_workflow.status == ProductionWorkflowStatus.PAUSED:
                    logger.info(f"Workflow {workflow_id} paused at batch {i+1}")
                    return
                
                try:
                    logger.info(f"Processing batch {i+1}/{workflow.total_batches} for workflow {workflow_id}")
                    
                    # 执行批次替换和导出
                    await self._process_batch(workflow_id, batch, request)
                    
                    # 更新进度
                    workflow.completed_batches += 1
                    workflow.completed_images += batch.batch_size
                    workflow.updated_at = datetime.now()
                    
                    # 批次间延迟
                    if i < len(workflow.batches) - 1:  # 不是最后一批
                        await asyncio.sleep(request.throttle_delay)
                    
                except Exception as e:
                    logger.error(f"Batch {i+1} failed in workflow {workflow_id}: {e}")
                    workflow.failed_batches += 1
                    workflow.updated_at = datetime.now()
            
            # 工作流完成
            if workflow.failed_batches == 0:
                workflow.status = ProductionWorkflowStatus.COMPLETED
            else:
                workflow.status = ProductionWorkflowStatus.FAILED
                workflow.error_message = f"{workflow.failed_batches} 个批次失败"
            
            workflow.updated_at = datetime.now()
            
            logger.info(f"Production workflow {workflow_id} completed")
            
            # 发送回调通知
            if request.callback_url:
                await self._send_workflow_callback(request.callback_url, workflow)
                
        except Exception as e:
            logger.error(f"Production workflow {workflow_id} failed: {e}")
            workflow.status = ProductionWorkflowStatus.FAILED
            workflow.error_message = str(e)
            workflow.updated_at = datetime.now()
    
    async def _process_batch(
        self,
        workflow_id: str,
        batch: ProductionBatch,
        request: ProductionWorkflowRequest
    ):
        """处理单个批次"""
        workflow = self._workflows[workflow_id]
        
        # 模拟批次处理
        await asyncio.sleep(2)  # 模拟替换时间
        
        # 模拟导出
        export_urls = await self._export_batch(
            request.file_key,
            [item.node_id for item in batch.replacements],
            request.export_format,
            request.export_scale
        )
        
        # 添加导出URL到工作流
        workflow.export_urls.extend(export_urls)
        
        logger.debug(f"Batch {batch.batch_id} processed, exported {len(export_urls)} images")
    
    async def _export_batch(
        self,
        file_key: str,
        node_ids: List[str],
        format: str,
        scale: float
    ) -> List[str]:
        """导出批次图片"""
        try:
            figma_client = await self.figma_service.get_figma_client()
            async with figma_client:
                export_data = await figma_client.export_images(
                    file_key=file_key,
                    node_ids=node_ids,
                    format=format,
                    scale=scale
                )
                
                if export_data and 'images' in export_data:
                    return list(export_data['images'].values())
                return []
                
        except Exception as e:
            logger.error(f"Batch export failed: {e}")
            return []
    
    async def _send_workflow_callback(
        self, 
        callback_url: str, 
        workflow: ProductionWorkflowResponse
    ):
        """发送工作流回调通知"""
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                await client.post(
                    callback_url,
                    json=workflow.dict(),
                    timeout=30
                )
            logger.info(f"Workflow callback sent to {callback_url}")
        except Exception as e:
            logger.error(f"Failed to send workflow callback to {callback_url}: {e}")
    
    async def get_workflow_status(self, workflow_id: str) -> Optional[ProductionWorkflowResponse]:
        """获取工作流状态"""
        return self._workflows.get(workflow_id)
    
    async def pause_workflow(self, workflow_id: str) -> bool:
        """暂停工作流"""
        workflow = self._workflows.get(workflow_id)
        if not workflow:
            return False
        
        if workflow.status == ProductionWorkflowStatus.PROCESSING:
            workflow.status = ProductionWorkflowStatus.PAUSED
            workflow.updated_at = datetime.now()
            return True
        
        return False
    
    async def resume_workflow(self, workflow_id: str):
        """恢复工作流"""
        workflow = self._workflows.get(workflow_id)
        if not workflow or workflow.status != ProductionWorkflowStatus.PAUSED:
            return
        
        workflow.status = ProductionWorkflowStatus.PROCESSING
        workflow.updated_at = datetime.now()
        
        # 继续执行工作流
        await self.execute_workflow(workflow_id)
    
    async def cancel_workflow(self, workflow_id: str) -> bool:
        """取消工作流"""
        workflow = self._workflows.get(workflow_id)
        if not workflow:
            return False
        
        if workflow.status in [ProductionWorkflowStatus.PENDING, ProductionWorkflowStatus.PROCESSING, ProductionWorkflowStatus.PAUSED]:
            workflow.status = ProductionWorkflowStatus.FAILED
            workflow.error_message = "工作流已被取消"
            workflow.updated_at = datetime.now()
            return True
        
        return False
    
    async def list_workflows(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[ProductionWorkflowStatus] = None,
        file_key: Optional[str] = None
    ) -> List[ProductionWorkflowResponse]:
        """获取工作流列表"""
        workflows = list(self._workflows.values())
        
        # 状态过滤
        if status:
            workflows = [wf for wf in workflows if wf.status == status]
        
        # 文件键过滤
        if file_key:
            workflows = [wf for wf in workflows if wf.file_key == file_key]
        
        # 按创建时间倒序排序
        workflows.sort(key=lambda x: x.created_at, reverse=True)
        
        # 分页
        start = (page - 1) * page_size
        end = start + page_size
        return workflows[start:end]
    
    async def get_workflow_batches(self, workflow_id: str) -> Optional[List[ProductionBatch]]:
        """获取工作流批次详情"""
        workflow = self._workflows.get(workflow_id)
        return workflow.batches if workflow else None
    
    async def create_bulk_operation(
        self, 
        request: BulkOperationRequest
    ) -> BulkOperationResponse:
        """创建批量操作"""
        operation_id = str(uuid.uuid4())
        
        operation = BulkOperationResponse(
            operation_id=operation_id,
            status="pending",
            total_files=len(request.file_keys),
            completed_files=0,
            failed_files=0,
            created_at=datetime.now(),
            estimated_completion=datetime.now() + timedelta(
                minutes=len(request.file_keys) * 5  # 估算每个文件5分钟
            ),
            results=[]
        )
        
        self._bulk_operations[operation_id] = operation
        
        logger.info(f"Created bulk operation {operation_id} for {len(request.file_keys)} files")
        return operation
    
    async def execute_bulk_operation(self, operation_id: str):
        """执行批量操作"""
        # 这里应该实现具体的批量操作逻辑
        # 暂时只是模拟
        operation = self._bulk_operations.get(operation_id)
        if not operation:
            return
        
        operation.status = "processing"
        await asyncio.sleep(5)  # 模拟处理时间
        operation.status = "completed"
        operation.completed_files = operation.total_files
    
    async def get_bulk_operation_status(self, operation_id: str) -> Optional[BulkOperationResponse]:
        """获取批量操作状态"""
        return self._bulk_operations.get(operation_id)
