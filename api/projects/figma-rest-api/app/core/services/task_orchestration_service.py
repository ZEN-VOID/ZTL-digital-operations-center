"""
任务编排服务
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.figma import (
    TaskOrchestrationConfig,
    TaskQueue,
    TaskQueueStatus
)
from ..config import Settings

logger = logging.getLogger(__name__)


class TaskOrchestrationService:
    """任务编排服务"""
    
    def __init__(self, db: AsyncSession, settings: Settings):
        self.db = db
        self.settings = settings
        
        # 默认配置
        self.config = TaskOrchestrationConfig()
        
        # 任务队列（内存存储，生产环境应使用Redis等）
        self._queues: Dict[str, TaskQueue] = {
            "batch_replace": TaskQueue(
                queue_id="batch_replace",
                queue_name="批量替换队列",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            "production_workflow": TaskQueue(
                queue_id="production_workflow", 
                queue_name="量产工作流队列",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            "bulk_operation": TaskQueue(
                queue_id="bulk_operation",
                queue_name="批量操作队列", 
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        }
        
        # 运行中的任务
        self._running_tasks: Dict[str, Dict] = {}
        
        # 系统负载
        self._system_load = 0.0
        
    async def get_queue_status(self) -> TaskQueueStatus:
        """获取任务队列状态"""
        # 更新队列状态
        for queue in self._queues.values():
            queue.updated_at = datetime.now()
        
        # 计算总数
        total_pending = sum(q.pending_tasks for q in self._queues.values())
        total_running = sum(q.running_tasks for q in self._queues.values())
        
        # 更新系统负载
        max_concurrent = self.config.max_concurrent_tasks
        self._system_load = min(total_running / max_concurrent, 1.0) if max_concurrent > 0 else 0.0
        
        return TaskQueueStatus(
            queues=list(self._queues.values()),
            total_pending=total_pending,
            total_running=total_running,
            system_load=self._system_load,
            last_updated=datetime.now()
        )
    
    async def update_config(self, config: TaskOrchestrationConfig):
        """更新任务编排配置"""
        self.config = config
        logger.info(f"Task orchestration config updated: {config.dict()}")
    
    async def add_task_to_queue(
        self, 
        queue_name: str, 
        task_id: str, 
        task_data: Dict
    ) -> bool:
        """添加任务到队列"""
        queue = self._queues.get(queue_name)
        if not queue:
            logger.error(f"Queue {queue_name} not found")
            return False
        
        # 检查系统负载
        if self._system_load >= 0.9:
            logger.warning(f"System load too high ({self._system_load:.2f}), rejecting task {task_id}")
            return False
        
        # 添加到队列
        queue.pending_tasks += 1
        queue.updated_at = datetime.now()
        
        logger.info(f"Task {task_id} added to queue {queue_name}")
        return True
    
    async def start_task(self, queue_name: str, task_id: str, task_data: Dict) -> bool:
        """开始执行任务"""
        queue = self._queues.get(queue_name)
        if not queue:
            return False
        
        # 检查并发限制
        if len(self._running_tasks) >= self.config.max_concurrent_tasks:
            logger.warning(f"Max concurrent tasks reached, cannot start task {task_id}")
            return False
        
        # 从待处理移到运行中
        if queue.pending_tasks > 0:
            queue.pending_tasks -= 1
        queue.running_tasks += 1
        queue.updated_at = datetime.now()
        
        # 记录运行中的任务
        self._running_tasks[task_id] = {
            "queue": queue_name,
            "start_time": datetime.now(),
            "data": task_data
        }
        
        logger.info(f"Task {task_id} started in queue {queue_name}")
        return True
    
    async def complete_task(
        self, 
        task_id: str, 
        success: bool = True, 
        error_message: Optional[str] = None
    ):
        """完成任务"""
        if task_id not in self._running_tasks:
            logger.warning(f"Task {task_id} not found in running tasks")
            return
        
        task_info = self._running_tasks.pop(task_id)
        queue_name = task_info["queue"]
        queue = self._queues.get(queue_name)
        
        if queue:
            queue.running_tasks = max(0, queue.running_tasks - 1)
            if success:
                queue.completed_tasks += 1
            else:
                queue.failed_tasks += 1
            queue.updated_at = datetime.now()
        
        # 记录任务完成时间
        duration = datetime.now() - task_info["start_time"]
        
        if success:
            logger.info(f"Task {task_id} completed successfully in {duration.total_seconds():.2f}s")
        else:
            logger.error(f"Task {task_id} failed after {duration.total_seconds():.2f}s: {error_message}")
    
    async def get_task_info(self, task_id: str) -> Optional[Dict]:
        """获取任务信息"""
        return self._running_tasks.get(task_id)
    
    async def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        if task_id not in self._running_tasks:
            return False
        
        task_info = self._running_tasks.pop(task_id)
        queue_name = task_info["queue"]
        queue = self._queues.get(queue_name)
        
        if queue:
            queue.running_tasks = max(0, queue.running_tasks - 1)
            queue.failed_tasks += 1
            queue.updated_at = datetime.now()
        
        logger.info(f"Task {task_id} cancelled")
        return True
    
    async def retry_failed_task(
        self, 
        queue_name: str, 
        task_id: str, 
        task_data: Dict,
        retry_count: int = 0
    ) -> bool:
        """重试失败的任务"""
        if retry_count >= self.config.max_retries:
            logger.error(f"Task {task_id} exceeded max retries ({self.config.max_retries})")
            return False
        
        # 等待重试延迟
        await asyncio.sleep(self.config.retry_delay * (2 ** retry_count))  # 指数退避
        
        # 重新添加到队列
        return await self.add_task_to_queue(queue_name, f"{task_id}_retry_{retry_count + 1}", task_data)
    
    async def cleanup_old_tasks(self, days: int = 7):
        """清理旧任务"""
        cutoff_time = datetime.now() - timedelta(days=days)
        
        # 清理运行时间过长的任务
        expired_tasks = []
        for task_id, task_info in self._running_tasks.items():
            if task_info["start_time"] < cutoff_time:
                expired_tasks.append(task_id)
        
        for task_id in expired_tasks:
            await self.cancel_task(task_id)
            logger.warning(f"Cancelled expired task {task_id}")
        
        logger.info(f"Cleaned up {len(expired_tasks)} expired tasks")
    
    async def get_queue_metrics(self, queue_name: str) -> Optional[Dict]:
        """获取队列指标"""
        queue = self._queues.get(queue_name)
        if not queue:
            return None
        
        total_tasks = queue.pending_tasks + queue.running_tasks + queue.completed_tasks + queue.failed_tasks
        success_rate = queue.completed_tasks / total_tasks if total_tasks > 0 else 0.0
        
        return {
            "queue_name": queue_name,
            "total_tasks": total_tasks,
            "success_rate": success_rate,
            "average_wait_time": 0.0,  # 需要实际统计
            "throughput": 0.0,  # 需要实际统计
            "last_updated": queue.updated_at
        }
    
    async def set_queue_priority(self, queue_name: str, priority: int):
        """设置队列优先级"""
        queue = self._queues.get(queue_name)
        if queue:
            # 在实际实现中，这里应该设置队列的优先级属性
            logger.info(f"Queue {queue_name} priority set to {priority}")
    
    async def pause_queue(self, queue_name: str) -> bool:
        """暂停队列"""
        queue = self._queues.get(queue_name)
        if not queue:
            return False
        
        # 在实际实现中，这里应该设置队列的暂停状态
        logger.info(f"Queue {queue_name} paused")
        return True
    
    async def resume_queue(self, queue_name: str) -> bool:
        """恢复队列"""
        queue = self._queues.get(queue_name)
        if not queue:
            return False
        
        # 在实际实现中，这里应该恢复队列的运行状态
        logger.info(f"Queue {queue_name} resumed")
        return True
    
    async def get_system_health(self) -> Dict:
        """获取系统健康状态"""
        status = await self.get_queue_status()
        
        # 计算健康分数
        health_score = 1.0
        if status.system_load > 0.8:
            health_score -= 0.3
        if status.total_pending > 100:
            health_score -= 0.2
        
        # 检查队列健康状态
        unhealthy_queues = []
        for queue in status.queues:
            total_tasks = queue.pending_tasks + queue.running_tasks + queue.completed_tasks + queue.failed_tasks
            if total_tasks > 0:
                failure_rate = queue.failed_tasks / total_tasks
                if failure_rate > 0.1:  # 失败率超过10%
                    unhealthy_queues.append(queue.queue_name)
                    health_score -= 0.2
        
        health_status = "healthy"
        if health_score < 0.7:
            health_status = "unhealthy"
        elif health_score < 0.9:
            health_status = "degraded"
        
        return {
            "status": health_status,
            "health_score": max(0.0, health_score),
            "system_load": status.system_load,
            "total_pending": status.total_pending,
            "total_running": status.total_running,
            "unhealthy_queues": unhealthy_queues,
            "last_check": datetime.now()
        }
