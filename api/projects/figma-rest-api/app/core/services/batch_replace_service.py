"""
批量替换图片服务
"""

import asyncio
import logging
import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.figma import (
    BatchReplaceRequest,
    BatchReplaceResponse,
    BatchReplaceStatus,
    PluginReplaceRequest,
    PluginReplaceResponse,
    ImageReplaceItem
)
from ..config import Settings
from .figma_service import FigmaService

logger = logging.getLogger(__name__)


class BatchReplaceService:
    """批量替换图片服务"""
    
    def __init__(self, db: AsyncSession, settings: Settings):
        self.db = db
        self.settings = settings
        self.figma_service = FigmaService(db, settings)
        # 内存中的任务存储（生产环境应使用数据库）
        self._tasks: Dict[str, BatchReplaceResponse] = {}
        
    async def create_batch_replace_task(
        self, 
        request: BatchReplaceRequest
    ) -> BatchReplaceResponse:
        """创建批量替换任务"""
        task_id = str(uuid.uuid4())
        
        # 验证替换项数量
        if len(request.replacements) > 50:
            raise ValueError("单次替换项数量不能超过50个")
        
        # 验证图片URL
        for item in request.replacements:
            if not item.image_url.startswith(('http://', 'https://')):
                raise ValueError(f"无效的图片URL: {item.image_url}")
        
        # 创建任务
        task = BatchReplaceResponse(
            task_id=task_id,
            status=BatchReplaceStatus.PENDING,
            file_key=request.file_key,
            total_items=len(request.replacements),
            completed_items=0,
            failed_items=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            export_urls=[]
        )
        
        # 存储任务信息（包含请求详情）
        self._tasks[task_id] = task
        self._store_task_request(task_id, request)
        
        logger.info(f"Created batch replace task {task_id} for file {request.file_key}")
        return task
    
    def _store_task_request(self, task_id: str, request: BatchReplaceRequest):
        """存储任务请求详情"""
        # 在实际实现中，这应该存储到数据库
        setattr(self._tasks[task_id], '_request', request)
    
    def _get_task_request(self, task_id: str) -> Optional[BatchReplaceRequest]:
        """获取任务请求详情"""
        task = self._tasks.get(task_id)
        return getattr(task, '_request', None) if task else None
    
    async def execute_batch_replace(self, task_id: str):
        """执行批量替换任务"""
        task = self._tasks.get(task_id)
        if not task:
            logger.error(f"Task {task_id} not found")
            return
        
        request = self._get_task_request(task_id)
        if not request:
            logger.error(f"Task request {task_id} not found")
            return
        
        try:
            # 更新任务状态为替换中
            task.status = BatchReplaceStatus.REPLACING
            task.updated_at = datetime.now()
            
            logger.info(f"Starting batch replace for task {task_id}")
            
            # 模拟插件替换过程
            await self._simulate_plugin_replace(task_id, request.replacements)
            
            # 如果启用自动导出
            if request.auto_export:
                task.status = BatchReplaceStatus.EXPORTING
                task.updated_at = datetime.now()

                # 执行导出
                export_urls = await self._export_nodes(
                    request.file_key,
                    [item.node_id for item in request.replacements],
                    request.export_format,
                    request.export_scale
                )

                # 下载并保存导出的图片到本地
                if export_urls:
                    local_paths = await self._save_to_local(
                        export_urls=export_urls,
                        file_key=request.file_key
                    )
                    task.export_urls = local_paths if local_paths else export_urls
                else:
                    task.export_urls = []
            
            # 任务完成
            task.status = BatchReplaceStatus.COMPLETED
            task.updated_at = datetime.now()
            
            logger.info(f"Batch replace task {task_id} completed successfully")
            
            # 发送回调通知
            if request.callback_url:
                await self._send_callback(request.callback_url, task)
                
        except Exception as e:
            logger.error(f"Batch replace task {task_id} failed: {e}")
            task.status = BatchReplaceStatus.FAILED
            task.error_message = str(e)
            task.updated_at = datetime.now()
    
    async def _simulate_plugin_replace(
        self, 
        task_id: str, 
        replacements: List[ImageReplaceItem]
    ):
        """模拟插件替换过程"""
        task = self._tasks[task_id]
        
        for i, item in enumerate(replacements):
            try:
                # 模拟替换延迟
                await asyncio.sleep(0.5)
                
                # 模拟替换成功（90%成功率）
                import random
                if random.random() < 0.9:
                    task.completed_items += 1
                    logger.debug(f"Replaced image for node {item.node_id}")
                else:
                    task.failed_items += 1
                    logger.warning(f"Failed to replace image for node {item.node_id}")
                
                task.updated_at = datetime.now()
                
            except Exception as e:
                logger.error(f"Error replacing node {item.node_id}: {e}")
                task.failed_items += 1
                task.updated_at = datetime.now()
    
    async def _export_nodes(
        self,
        file_key: str,
        node_ids: List[str],
        format: str,
        scale: float
    ) -> List[str]:
        """导出节点为图片"""
        try:
            # 使用Figma服务导出图片
            figma_client = await self.figma_service.get_figma_client()
            async with figma_client:
                export_data = await figma_client.export_images(
                    file_key=file_key,
                    node_ids=node_ids,
                    format=format,
                    scale=scale
                )
                
                # 返回导出URL列表
                if export_data and 'images' in export_data:
                    return list(export_data['images'].values())
                return []
                
        except Exception as e:
            logger.error(f"Export failed: {e}")
            return []

    async def _save_to_local(
        self,
        export_urls: List[str],
        file_key: str
    ) -> List[str]:
        """
        将导出的图片下载并保存到本地output目录

        Args:
            export_urls: Figma导出的图片URL列表
            file_key: Figma文件ID

        Returns:
            本地文件路径列表
        """
        try:
            import httpx
            from pathlib import Path
            from datetime import datetime

            # 创建输出目录: output/model/[figma-id]/
            project_root = Path(__file__).parent.parent.parent.parent.parent.parent
            output_dir = project_root / 'output' / 'model' / file_key
            output_dir.mkdir(parents=True, exist_ok=True)

            logger.info(f"Saving {len(export_urls)} images to local: {output_dir}")

            local_paths = []
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

            # 下载并保存每张图片
            async with httpx.AsyncClient(timeout=60.0) as http_client:
                for i, figma_url in enumerate(export_urls):
                    try:
                        # 从Figma下载图片
                        response = await http_client.get(figma_url)
                        response.raise_for_status()

                        # 生成本地文件名
                        file_ext = 'png'  # 默认png
                        file_name = f"export_{i + 1}_{timestamp}.{file_ext}"
                        local_path = output_dir / file_name

                        # 保存到本地
                        with open(local_path, 'wb') as f:
                            f.write(response.content)

                        # 转换为相对路径字符串
                        relative_path = str(local_path.relative_to(project_root))
                        local_paths.append(relative_path)

                        logger.info(f"Saved {i + 1}/{len(export_urls)}: {relative_path}")

                    except Exception as e:
                        logger.error(f"Failed to save image {i + 1}: {e}")
                        # 失败时保留原URL
                        local_paths.append(figma_url)

            logger.info(f"Successfully saved {len([p for p in local_paths if not p.startswith('http')])}/ {len(export_urls)} images to local")

            # 保存图片URL到JSON文件（固定格式）
            await self._save_urls_to_json(local_paths, file_key, timestamp)

            return local_paths

        except Exception as e:
            logger.error(f"Local save failed: {e}")
            return []

    async def _save_urls_to_json(
        self,
        local_paths: List[str],
        file_key: str,
        timestamp: str
    ):
        """
        保存图片URL到标准格式的JSON文件

        Args:
            local_paths: 本地文件路径列表
            file_key: Figma文件ID
            timestamp: 时间戳
        """
        try:
            import json
            from pathlib import Path

            # 创建JSON保存目录: input/明红/图片URL/
            project_root = Path(__file__).parent.parent.parent.parent.parent.parent
            json_dir = project_root / 'input' / '明红' / '图片URL'
            json_dir.mkdir(parents=True, exist_ok=True)

            # JSON文件名: figma-{file_key}-{timestamp}.json
            json_filename = f"figma-{file_key}-{timestamp}.json"
            json_path = json_dir / json_filename

            # 构建标准格式的JSON数据
            json_data = {
                "metadata": {
                    "source": "figma",
                    "file_key": file_key,
                    "export_time": timestamp,
                    "total_images": len([p for p in local_paths if not p.startswith('http')]),
                    "version": "1.0"
                },
                "images": []
            }

            # 添加每张图片的信息
            for i, local_path in enumerate(local_paths, 1):
                if not local_path.startswith('http'):  # 只记录成功保存的本地文件
                    # 生成完整路径（用于访问）
                    full_path = project_root / local_path

                    # 预先转换路径格式
                    relative_path_unix = local_path.replace('\\', '/')
                    absolute_path_unix = str(full_path.absolute()).replace('\\', '/')

                    json_data["images"].append({
                        "id": i,
                        "filename": Path(local_path).name,
                        "relative_path": relative_path_unix,
                        "absolute_path": absolute_path_unix,
                        "url": f"file:///{absolute_path_unix}"
                    })

            # 保存JSON文件
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)

            logger.info(f"Saved image URLs to JSON: {json_path}")

        except Exception as e:
            logger.error(f"Failed to save URLs to JSON: {e}")

    async def _send_callback(self, callback_url: str, task: BatchReplaceResponse):
        """发送回调通知"""
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                await client.post(
                    callback_url,
                    json=task.dict(),
                    timeout=30
                )
            logger.info(f"Callback sent to {callback_url}")
        except Exception as e:
            logger.error(f"Failed to send callback to {callback_url}: {e}")
    
    async def get_task_status(self, task_id: str) -> Optional[BatchReplaceResponse]:
        """获取任务状态"""
        return self._tasks.get(task_id)
    
    async def retry_failed_items(
        self, 
        task_id: str, 
        failed_node_ids: Optional[List[str]] = None
    ):
        """重试失败的替换项"""
        task = self._tasks.get(task_id)
        request = self._get_task_request(task_id)
        
        if not task or not request:
            logger.error(f"Task or request {task_id} not found for retry")
            return
        
        try:
            # 重置失败计数
            if failed_node_ids:
                # 重试指定节点
                retry_items = [
                    item for item in request.replacements 
                    if item.node_id in failed_node_ids
                ]
            else:
                # 重试所有失败项（这里简化处理）
                retry_items = request.replacements[-task.failed_items:]
            
            task.status = BatchReplaceStatus.REPLACING
            task.updated_at = datetime.now()
            
            # 执行重试
            await self._simulate_plugin_replace(task_id, retry_items)
            
            # 更新状态
            if task.failed_items == 0:
                task.status = BatchReplaceStatus.COMPLETED
            else:
                task.status = BatchReplaceStatus.FAILED
            
            task.updated_at = datetime.now()
            
        except Exception as e:
            logger.error(f"Retry failed for task {task_id}: {e}")
            task.status = BatchReplaceStatus.FAILED
            task.error_message = str(e)
            task.updated_at = datetime.now()
    
    async def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        task = self._tasks.get(task_id)
        if not task:
            return False
        
        if task.status in [BatchReplaceStatus.PENDING, BatchReplaceStatus.REPLACING]:
            task.status = BatchReplaceStatus.FAILED
            task.error_message = "任务已被取消"
            task.updated_at = datetime.now()
            return True
        
        return False
    
    async def list_tasks(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[BatchReplaceStatus] = None,
        file_key: Optional[str] = None
    ) -> List[BatchReplaceResponse]:
        """获取任务列表"""
        tasks = list(self._tasks.values())
        
        # 状态过滤
        if status:
            tasks = [task for task in tasks if task.status == status]
        
        # 文件键过滤
        if file_key:
            tasks = [task for task in tasks if task.file_key == file_key]
        
        # 按创建时间倒序排序
        tasks.sort(key=lambda x: x.created_at, reverse=True)
        
        # 分页
        start = (page - 1) * page_size
        end = start + page_size
        return tasks[start:end]
    
    async def handle_plugin_replace(
        self, 
        request: PluginReplaceRequest
    ) -> PluginReplaceResponse:
        """处理插件替换请求"""
        try:
            # 更新任务状态
            task = self._tasks.get(request.task_id)
            if task:
                task.status = BatchReplaceStatus.REPLACING
                task.updated_at = datetime.now()
            
            # 模拟插件处理
            await asyncio.sleep(1)
            
            # 返回成功响应
            return PluginReplaceResponse(
                success=True,
                task_id=request.task_id,
                completed_count=len(request.replacements),
                failed_count=0,
                error_message=None,
                failed_items=[]
            )
            
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
    
    async def handle_plugin_callback(
        self,
        task_id: str,
        success: bool,
        completed_count: int = 0,
        failed_count: int = 0,
        error_message: Optional[str] = None,
        export_urls: Optional[List[str]] = None
    ):
        """处理插件回调"""
        task = self._tasks.get(task_id)
        if not task:
            logger.error(f"Task {task_id} not found for callback")
            return
        
        # 更新任务状态
        task.completed_items = completed_count
        task.failed_items = failed_count
        task.updated_at = datetime.now()
        
        if success and failed_count == 0:
            task.status = BatchReplaceStatus.COMPLETED
        else:
            task.status = BatchReplaceStatus.FAILED
            task.error_message = error_message
        
        if export_urls:
            task.export_urls = export_urls
        
        logger.info(f"Plugin callback processed for task {task_id}")
