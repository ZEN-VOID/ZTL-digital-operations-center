"""
Figma业务逻辑服务
提供批量处理、任务管理和状态跟踪功能
"""

import asyncio
import logging
import os
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Tuple
from uuid import uuid4
import aiofiles
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_
from sqlalchemy.orm import selectinload

from ..models.figma import FigmaBatchTask, FigmaBatch, FigmaTaskStatus, FigmaBatchStatus
from ..schemas.figma import BatchExportRequest, FigmaTaskResponse, FigmaBatchResponse
from .figma_client import FigmaClient, FigmaAPIError
from ..config import Settings


logger = logging.getLogger(__name__)


class FigmaService:
    """
    Figma业务逻辑服务
    
    负责:
    - 批量导出任务管理
    - 任务状态跟踪
    - 文件下载和存储
    - 错误处理和重试
    """

    def __init__(self, db_session: AsyncSession, settings: Settings):
        """
        初始化Figma服务
        
        Args:
            db_session: 数据库会话
            settings: 应用设置
        """
        self.db = db_session
        self.settings = settings
        self._figma_client: Optional[FigmaClient] = None

    async def get_figma_client(self) -> FigmaClient:
        """获取Figma客户端实例"""
        if self._figma_client is None:
            from .figma_client import FigmaClientConfig
            config = FigmaClientConfig(
                figma_api_token=self.settings.figma_api_token,
                figma_api_base_url=self.settings.figma_api_base_url,
                figma_timeout=self.settings.figma_timeout,
                figma_max_retries=self.settings.figma_max_retries,
                figma_rate_limit_per_minute=self.settings.figma_rate_limit_per_minute,
                figma_concurrent_requests=self.settings.figma_concurrent_requests
            )
            self._figma_client = FigmaClient(config)
        return self._figma_client

    async def create_batch_export_task(self, request: BatchExportRequest) -> FigmaTaskResponse:
        """
        创建批量导出任务
        
        Args:
            request: 批量导出请求
            
        Returns:
            任务响应信息
        """
        try:
            # 验证Figma文件是否存在
            figma_client = await self.get_figma_client()
            async with figma_client:
                file_info = await figma_client.get_file(request.file_key)
                if not file_info:
                    raise ValueError(f"Figma文件不存在: {request.file_key}")

            # 计算批次数量
            total_nodes = len(request.node_ids)
            batch_size = min(request.batch_size, self.settings.max_batch_size)
            total_batches = (total_nodes + batch_size - 1) // batch_size

            # 创建主任务
            task = FigmaBatchTask(
                id=str(uuid4()),
                file_key=request.file_key,
                status=FigmaTaskStatus.PENDING,
                total_batches=total_batches,
                export_format=request.export_format,
                scale=request.scale,
                output_directory=request.output_directory or self.settings.export_dir,
                total_nodes=total_nodes,
                batch_size=batch_size
            )

            self.db.add(task)
            await self.db.flush()

            # 创建批次
            batches = []
            for i in range(0, total_nodes, batch_size):
                batch_node_ids = request.node_ids[i:i + batch_size]
                batch = FigmaBatch(
                    id=str(uuid4()),
                    task_id=task.id,
                    batch_index=len(batches),
                    node_ids=batch_node_ids,
                    status=FigmaBatchStatus.PENDING
                )
                batches.append(batch)
                self.db.add(batch)

            await self.db.commit()

            logger.info(f"Created batch export task {task.id} with {total_batches} batches")

            # 异步启动处理
            asyncio.create_task(self._process_batch_export_async(task.id))

            return await self._task_to_response(task)

        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to create batch export task: {e}")
            raise

    async def _process_batch_export_async(self, task_id: str) -> None:
        """异步处理批量导出任务"""
        try:
            await self.process_batch_export(task_id)
        except Exception as e:
            logger.error(f"Async batch export processing failed for task {task_id}: {e}")
            # 更新任务状态为失败
            await self._update_task_status(task_id, FigmaTaskStatus.FAILED, str(e))

    async def process_batch_export(self, task_id: str) -> None:
        """
        处理批量导出任务
        
        Args:
            task_id: 任务ID
        """
        # 获取任务和批次
        task = await self._get_task_with_batches(task_id)
        if not task:
            raise ValueError(f"Task not found: {task_id}")

        if task.status != FigmaTaskStatus.PENDING:
            logger.warning(f"Task {task_id} is not in pending status: {task.status}")
            return

        try:
            # 更新任务状态为处理中
            await self._update_task_status(task_id, FigmaTaskStatus.PROCESSING)
            task.started_at = datetime.utcnow()
            await self.db.commit()

            figma_client = await self.get_figma_client()
            async with figma_client:
                # 处理所有待处理的批次
                pending_batches = [b for b in task.batches if b.status == FigmaBatchStatus.PENDING]
                
                # 使用信号量控制并发
                semaphore = asyncio.Semaphore(self.settings.figma_concurrent_requests)
                
                # 并发处理批次
                batch_tasks = [
                    self._process_single_batch(figma_client, task, batch, semaphore)
                    for batch in pending_batches
                ]
                
                await asyncio.gather(*batch_tasks, return_exceptions=True)

            # 检查任务完成状态
            await self._check_task_completion(task_id)

        except Exception as e:
            logger.error(f"Batch export processing failed for task {task_id}: {e}")
            await self._update_task_status(task_id, FigmaTaskStatus.FAILED, str(e))

    async def _process_single_batch(
        self,
        figma_client: FigmaClient,
        task: FigmaBatchTask,
        batch: FigmaBatch,
        semaphore: asyncio.Semaphore
    ) -> None:
        """处理单个批次"""
        async with semaphore:
            try:
                # 更新批次状态
                batch.status = FigmaBatchStatus.PROCESSING
                batch.started_at = datetime.utcnow()
                await self.db.commit()

                # 调用Figma API导出图片
                export_result = await figma_client.export_images(
                    file_key=task.file_key,
                    node_ids=batch.node_ids,
                    format=task.export_format,
                    scale=task.scale
                )

                if export_result.get("err"):
                    raise FigmaAPIError(f"Export failed: {export_result['err']}")

                # 保存导出URL
                batch.export_urls = list(export_result.get("images", {}).values())
                
                # 下载图片文件
                downloaded_files = await self._download_batch_images(task, batch)
                batch.downloaded_files = downloaded_files

                # 更新批次状态为完成
                batch.status = FigmaBatchStatus.COMPLETED
                batch.completed_at = datetime.utcnow()
                
                # 更新任务进度
                await self._update_task_progress(task.id)
                
                await self.db.commit()
                
                logger.info(f"Batch {batch.id} completed successfully")

            except Exception as e:
                logger.error(f"Batch {batch.id} processing failed: {e}")
                
                # 更新批次状态为失败
                batch.status = FigmaBatchStatus.FAILED
                batch.error_message = str(e)
                batch.retry_count += 1
                
                await self.db.commit()

    async def _download_batch_images(self, task: FigmaBatchTask, batch: FigmaBatch) -> List[str]:
        """下载批次中的图片文件"""
        downloaded_files = []
        
        if not batch.export_urls:
            return downloaded_files

        # 创建任务专用目录
        task_dir = os.path.join(task.output_directory, task.id)
        os.makedirs(task_dir, exist_ok=True)

        async with httpx.AsyncClient() as client:
            for i, url in enumerate(batch.export_urls):
                try:
                    # 生成文件名
                    node_id = batch.node_ids[i] if i < len(batch.node_ids) else f"node_{i}"
                    filename = f"{node_id}.{task.export_format}"
                    filepath = os.path.join(task_dir, filename)

                    # 下载文件
                    response = await client.get(url)
                    response.raise_for_status()

                    # 保存文件
                    async with aiofiles.open(filepath, "wb") as f:
                        await f.write(response.content)

                    downloaded_files.append(filepath)
                    logger.debug(f"Downloaded image: {filepath}")

                except Exception as e:
                    logger.error(f"Failed to download image from {url}: {e}")

        return downloaded_files

    async def _update_task_progress(self, task_id: str) -> None:
        """更新任务进度"""
        # 获取任务的批次统计
        result = await self.db.execute(
            select(FigmaBatch.status, FigmaBatch.task_id)
            .where(FigmaBatch.task_id == task_id)
        )
        batches = result.fetchall()

        completed_count = sum(1 for batch in batches if batch.status == FigmaBatchStatus.COMPLETED)
        failed_count = sum(1 for batch in batches if batch.status == FigmaBatchStatus.FAILED)

        # 更新任务统计
        await self.db.execute(
            update(FigmaBatchTask)
            .where(FigmaBatchTask.id == task_id)
            .values(
                completed_batches=completed_count,
                failed_batches=failed_count,
                updated_at=datetime.utcnow()
            )
        )

    async def _check_task_completion(self, task_id: str) -> None:
        """检查任务是否完成"""
        task = await self._get_task_with_batches(task_id)
        if not task:
            return

        total_processed = task.completed_batches + task.failed_batches

        if total_processed >= task.total_batches:
            # 所有批次都已处理完成
            if task.failed_batches == 0:
                # 全部成功
                task.status = FigmaTaskStatus.COMPLETED
            else:
                # 有失败的批次
                task.status = FigmaTaskStatus.FAILED
                task.error_message = f"Failed batches: {task.failed_batches}/{task.total_batches}"

            task.completed_at = datetime.utcnow()
            await self.db.commit()

            logger.info(f"Task {task_id} completed with status: {task.status}")

    async def _update_task_status(
        self,
        task_id: str,
        status: FigmaTaskStatus,
        error_message: Optional[str] = None
    ) -> None:
        """更新任务状态"""
        update_data = {
            "status": status,
            "updated_at": datetime.utcnow()
        }

        if error_message:
            update_data["error_message"] = error_message

        await self.db.execute(
            update(FigmaBatchTask)
            .where(FigmaBatchTask.id == task_id)
            .values(**update_data)
        )
        await self.db.commit()

    async def get_task_status(self, task_id: str) -> Optional[FigmaTaskResponse]:
        """
        获取任务状态

        Args:
            task_id: 任务ID

        Returns:
            任务状态信息
        """
        task = await self._get_task_with_batches(task_id)
        if not task:
            return None

        return await self._task_to_response(task)

    async def retry_failed_batch(self, task_id: str, batch_id: Optional[str] = None) -> bool:
        """
        重试失败的批次

        Args:
            task_id: 任务ID
            batch_id: 批次ID，为空则重试所有失败批次

        Returns:
            是否成功启动重试
        """
        task = await self._get_task_with_batches(task_id)
        if not task:
            return False

        # 找到可重试的批次
        if batch_id:
            batches_to_retry = [b for b in task.batches if b.id == batch_id and b.can_retry]
        else:
            batches_to_retry = [b for b in task.batches if b.can_retry]

        if not batches_to_retry:
            logger.warning(f"No retryable batches found for task {task_id}")
            return False

        # 重置批次状态
        for batch in batches_to_retry:
            batch.status = FigmaBatchStatus.PENDING
            batch.error_message = None
            batch.export_urls = None
            batch.downloaded_files = None

        # 如果任务状态是失败，重置为处理中
        if task.status == FigmaTaskStatus.FAILED:
            task.status = FigmaTaskStatus.PROCESSING
            task.error_message = None

        await self.db.commit()

        # 异步启动重试处理
        asyncio.create_task(self._process_batch_export_async(task_id))

        logger.info(f"Started retry for {len(batches_to_retry)} batches in task {task_id}")
        return True

    async def _get_task_with_batches(self, task_id: str) -> Optional[FigmaBatchTask]:
        """获取包含批次信息的任务"""
        result = await self.db.execute(
            select(FigmaBatchTask)
            .options(selectinload(FigmaBatchTask.batches))
            .where(FigmaBatchTask.id == task_id)
        )
        return result.scalar_one_or_none()

    async def _task_to_response(self, task: FigmaBatchTask) -> FigmaTaskResponse:
        """将任务模型转换为响应模型"""
        return FigmaTaskResponse(
            task_id=task.id,
            status=task.status,
            message=self._get_status_message(task),
            file_key=task.file_key,
            total_batches=task.total_batches,
            completed_batches=task.completed_batches,
            failed_batches=task.failed_batches,
            progress=task.progress,
            total_nodes=task.total_nodes,
            export_format=task.export_format,
            scale=task.scale,
            created_at=task.created_at,
            updated_at=task.updated_at,
            started_at=task.started_at,
            completed_at=task.completed_at,
            error_message=task.error_message
        )

    def _get_status_message(self, task: FigmaBatchTask) -> str:
        """获取任务状态消息"""
        if task.status == FigmaTaskStatus.PENDING:
            return "任务等待处理"
        elif task.status == FigmaTaskStatus.PROCESSING:
            return f"正在处理 ({task.completed_batches}/{task.total_batches} 批次完成)"
        elif task.status == FigmaTaskStatus.COMPLETED:
            return "任务已完成"
        elif task.status == FigmaTaskStatus.FAILED:
            return f"任务失败 ({task.failed_batches} 批次失败)"
        elif task.status == FigmaTaskStatus.CANCELLED:
            return "任务已取消"
        else:
            return "未知状态"

    async def list_tasks(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[FigmaTaskStatus] = None
    ) -> Tuple[List[FigmaTaskResponse], int]:
        """
        获取任务列表

        Args:
            page: 页码
            page_size: 每页大小
            status: 状态过滤

        Returns:
            任务列表和总数
        """
        # 构建查询
        query = select(FigmaBatchTask)

        if status:
            query = query.where(FigmaBatchTask.status == status)

        # 获取总数
        count_query = select(FigmaBatch.id)
        if status:
            count_query = count_query.where(FigmaBatchTask.status == status)

        total_result = await self.db.execute(count_query)
        total = len(total_result.fetchall())

        # 分页查询
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size).order_by(FigmaBatchTask.created_at.desc())

        result = await self.db.execute(query)
        tasks = result.scalars().all()

        # 转换为响应模型
        task_responses = [await self._task_to_response(task) for task in tasks]

        return task_responses, total

    async def cleanup_old_tasks(self, days: int = 7) -> int:
        """
        清理旧任务

        Args:
            days: 保留天数

        Returns:
            清理的任务数量
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        # 查找要删除的任务
        result = await self.db.execute(
            select(FigmaBatchTask.id)
            .where(
                and_(
                    FigmaBatchTask.created_at < cutoff_date,
                    FigmaBatchTask.status.in_([
                        FigmaTaskStatus.COMPLETED,
                        FigmaTaskStatus.FAILED,
                        FigmaTaskStatus.CANCELLED
                    ])
                )
            )
        )

        task_ids = [row[0] for row in result.fetchall()]

        if not task_ids:
            return 0

        # 删除相关文件
        for task_id in task_ids:
            task_dir = os.path.join(self.settings.export_dir, task_id)
            if os.path.exists(task_dir):
                import shutil
                shutil.rmtree(task_dir, ignore_errors=True)

        # 删除数据库记录（级联删除批次）
        from sqlalchemy import delete
        await self.db.execute(
            delete(FigmaBatchTask).where(FigmaBatchTask.id.in_(task_ids))
        )

        await self.db.commit()

        logger.info(f"Cleaned up {len(task_ids)} old tasks")
        return len(task_ids)

    async def get_file_info(self, file_key: str) -> Optional[Dict[str, Any]]:
        """
        获取Figma文件信息

        Args:
            file_key: Figma文件键

        Returns:
            文件信息
        """
        try:
            figma_client = await self.get_figma_client()
            async with figma_client:
                return await figma_client.get_file(file_key)
        except Exception as e:
            logger.error(f"Failed to get file info for {file_key}: {e}")
            return None

    async def health_check(self) -> Dict[str, Any]:
        """
        健康检查

        Returns:
            健康状态信息
        """
        health_status = {
            "status": "healthy",
            "figma_api_available": False,
            "database_connected": False,
            "timestamp": datetime.utcnow(),
            "version": "1.0.0"
        }

        # 检查数据库连接
        try:
            await self.db.execute(select(1))
            health_status["database_connected"] = True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            health_status["status"] = "unhealthy"

        # 检查Figma API
        try:
            figma_client = await self.get_figma_client()
            async with figma_client:
                health_status["figma_api_available"] = await figma_client.health_check()
        except Exception as e:
            logger.error(f"Figma API health check failed: {e}")
            health_status["status"] = "unhealthy"

        if not health_status["figma_api_available"]:
            health_status["status"] = "unhealthy"

        return health_status
