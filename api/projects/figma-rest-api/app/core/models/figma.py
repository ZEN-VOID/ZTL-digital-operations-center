"""
Figma相关数据库模型
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from sqlalchemy import Column, String, Integer, DateTime, Text, Float, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()


class FigmaTaskStatus(str, Enum):
    """Figma任务状态枚举"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class FigmaBatchStatus(str, Enum):
    """Figma批次状态枚举"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


class FigmaBatchTask(Base):
    """
    Figma批量导出任务模型
    
    管理整个批量导出任务的生命周期，包括任务状态、进度跟踪和元数据。
    """
    __tablename__ = "figma_batch_tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    file_key = Column(String, nullable=False, index=True, comment="Figma文件键")
    status = Column(String, nullable=False, default=FigmaTaskStatus.PENDING, comment="任务状态")
    total_batches = Column(Integer, nullable=False, default=0, comment="总批次数")
    completed_batches = Column(Integer, nullable=False, default=0, comment="已完成批次数")
    failed_batches = Column(Integer, nullable=False, default=0, comment="失败批次数")
    export_format = Column(String, nullable=False, default="png", comment="导出格式")
    scale = Column(Float, nullable=False, default=1.0, comment="导出缩放比例")
    output_directory = Column(String, nullable=True, comment="输出目录路径")
    total_nodes = Column(Integer, nullable=False, default=0, comment="总节点数")
    batch_size = Column(Integer, nullable=False, default=6, comment="批次大小")
    
    # 元数据
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    started_at = Column(DateTime, nullable=True, comment="开始处理时间")
    completed_at = Column(DateTime, nullable=True, comment="完成时间")
    
    # 错误信息
    error_message = Column(Text, nullable=True, comment="错误消息")
    error_details = Column(JSON, nullable=True, comment="详细错误信息")
    
    # 关联关系
    batches = relationship("FigmaBatch", back_populates="task", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<FigmaBatchTask(id={self.id}, file_key={self.file_key}, status={self.status})>"

    @property
    def progress(self) -> float:
        """计算任务进度百分比"""
        if self.total_batches == 0:
            return 0.0
        return (self.completed_batches / self.total_batches) * 100

    @property
    def is_completed(self) -> bool:
        """检查任务是否已完成"""
        return self.status == FigmaTaskStatus.COMPLETED

    @property
    def is_failed(self) -> bool:
        """检查任务是否失败"""
        return self.status == FigmaTaskStatus.FAILED

    @property
    def can_retry(self) -> bool:
        """检查任务是否可以重试"""
        return self.status in [FigmaTaskStatus.FAILED, FigmaTaskStatus.CANCELLED]


class FigmaBatch(Base):
    """
    Figma批次处理模型
    
    管理单个批次的处理状态，包括节点ID、导出URL和重试逻辑。
    """
    __tablename__ = "figma_batches"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String, ForeignKey("figma_batch_tasks.id"), nullable=False, index=True, comment="关联任务ID")
    batch_index = Column(Integer, nullable=False, comment="批次索引")
    node_ids = Column(JSON, nullable=False, comment="节点ID列表")
    status = Column(String, nullable=False, default=FigmaBatchStatus.PENDING, comment="批次状态")
    
    # 导出结果
    export_urls = Column(JSON, nullable=True, comment="导出URL列表")
    downloaded_files = Column(JSON, nullable=True, comment="已下载文件路径列表")
    
    # 重试机制
    retry_count = Column(Integer, nullable=False, default=0, comment="重试次数")
    max_retries = Column(Integer, nullable=False, default=3, comment="最大重试次数")
    
    # 时间戳
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    started_at = Column(DateTime, nullable=True, comment="开始处理时间")
    completed_at = Column(DateTime, nullable=True, comment="完成时间")
    
    # 错误信息
    error_message = Column(Text, nullable=True, comment="错误消息")
    error_details = Column(JSON, nullable=True, comment="详细错误信息")
    
    # 关联关系
    task = relationship("FigmaBatchTask", back_populates="batches")

    def __repr__(self):
        return f"<FigmaBatch(id={self.id}, task_id={self.task_id}, status={self.status})>"

    @property
    def can_retry(self) -> bool:
        """检查批次是否可以重试"""
        return (
            self.status == FigmaBatchStatus.FAILED and 
            self.retry_count < self.max_retries
        )

    @property
    def is_completed(self) -> bool:
        """检查批次是否已完成"""
        return self.status == FigmaBatchStatus.COMPLETED

    @property
    def node_count(self) -> int:
        """获取节点数量"""
        return len(self.node_ids) if self.node_ids else 0
