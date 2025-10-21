"""
批量处理相关API数据模式

增强版批量替换和导出功能的数据模型定义
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class ReplacementRule(BaseModel):
    """图片替换规则

    支持精确匹配和模式匹配两种方式：
    - 精确匹配：target_node_path为具体节点ID
    - 模式匹配：target_node_path为匹配规则（如 "dish-*"）
    """
    target_node_path: str = Field(
        ...,
        description="节点路径或匹配规则（如 'dish-*' 匹配所有以dish-开头的节点）",
        min_length=1
    )
    image_url: str = Field(
        ...,
        description="替换的图片URL",
        min_length=1
    )

    @field_validator('image_url')
    @classmethod
    def validate_image_url(cls, v: str) -> str:
        """验证图片URL格式"""
        if not v.startswith(('http://', 'https://')):
            raise ValueError("image_url必须是有效的HTTP(S) URL")
        return v


class ExportFormat(str, Enum):
    """导出格式枚举"""
    PNG = "png"
    JPG = "jpg"
    SVG = "svg"
    PDF = "pdf"


class ExportConfig(BaseModel):
    """导出配置

    定义图片导出的格式、质量和存储选项
    """
    format: ExportFormat = Field(
        default=ExportFormat.PNG,
        description="导出格式"
    )
    scale: float = Field(
        default=1.0,
        description="导出缩放比例（1.0-4.0）",
        ge=1.0,
        le=4.0
    )
    scales: Optional[List[float]] = Field(
        default=None,
        description="多分辨率导出（如 [1.0, 2.0, 3.0]），覆盖scale参数"
    )
    save_to_cloud: bool = Field(
        default=False,
        description="是否上传到云盘"
    )
    cloud_dir: Optional[str] = Field(
        default=None,
        description="云盘目录路径（当save_to_cloud为true时必填）"
    )

    # SVG特定选项
    svg_outline_text: bool = Field(
        default=True,
        description="SVG中文本是否渲染为轮廓"
    )
    svg_include_id: bool = Field(
        default=False,
        description="是否为SVG元素包含id属性"
    )
    svg_include_node_id: bool = Field(
        default=False,
        description="是否为SVG元素包含node-id属性"
    )
    svg_simplify_stroke: bool = Field(
        default=True,
        description="是否简化SVG描边"
    )

    # 通用导出选项
    contents_only: bool = Field(
        default=True,
        description="是否排除重叠内容"
    )
    use_absolute_bounds: bool = Field(
        default=False,
        description="是否使用绝对边界"
    )

    @field_validator('scales')
    @classmethod
    def validate_scales(cls, v: Optional[List[float]]) -> Optional[List[float]]:
        """验证多分辨率配置"""
        if v is not None:
            if not v:
                raise ValueError("scales列表不能为空")
            if len(v) > 5:
                raise ValueError("最多支持5个分辨率")
            for scale in v:
                if scale < 1.0 or scale > 4.0:
                    raise ValueError(f"缩放比例必须在1.0-4.0之间，当前值: {scale}")
        return v

    def model_post_init(self, __context) -> None:
        """验证云盘配置"""
        if self.save_to_cloud and not self.cloud_dir:
            raise ValueError("当save_to_cloud为true时，必须提供cloud_dir")


class BatchReplaceRequest(BaseModel):
    """批量替换请求

    支持复杂的批量替换和导出工作流
    """
    figma_file_id: str = Field(
        ...,
        description="Figma文件ID",
        min_length=10
    )
    replacement_rules: List[ReplacementRule] = Field(
        ...,
        description="替换规则列表",
        min_items=1,
        max_items=50
    )
    export_config: ExportConfig = Field(
        default_factory=ExportConfig,
        description="导出配置"
    )

    @field_validator('figma_file_id')
    @classmethod
    def validate_file_id(cls, v: str) -> str:
        """验证Figma文件ID格式"""
        # Figma文件ID通常是22个字符的字母数字组合
        if len(v) < 10:
            raise ValueError("无效的Figma文件ID")
        return v


class ExportedFile(BaseModel):
    """导出文件信息"""
    filename: str = Field(..., description="文件名")
    local_path: str = Field(..., description="本地文件路径")
    cloud_url: Optional[str] = Field(None, description="云盘URL（如果已上传）")
    format: str = Field(..., description="文件格式")
    scale: float = Field(..., description="导出缩放比例")
    size_bytes: int = Field(..., description="文件大小（字节）")
    node_id: str = Field(..., description="源节点ID")


class ProcessingStatus(str, Enum):
    """处理状态枚举"""
    PENDING = "pending"
    VALIDATING = "validating"
    REPLACING = "replacing"
    EXPORTING = "exporting"
    UPLOADING = "uploading"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class BatchReplaceResponse(BaseModel):
    """批量替换响应

    包含完整的处理结果和导出文件信息
    """
    success: bool = Field(..., description="整体操作是否成功")
    message: str = Field(..., description="状态消息")
    task_id: str = Field(..., description="任务ID，用于查询进度")
    status: ProcessingStatus = Field(..., description="处理状态")

    # 统计信息
    total_replacements: int = Field(..., description="总替换数量")
    successful_replacements: int = Field(default=0, description="成功替换数量")
    failed_replacements: int = Field(default=0, description="失败替换数量")

    # 导出文件信息
    exported_files: List[ExportedFile] = Field(
        default_factory=list,
        description="导出的文件列表"
    )

    # 性能指标
    processing_time: float = Field(default=0.0, description="处理耗时（秒）")

    # 时间戳
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")
    completed_at: Optional[datetime] = Field(None, description="完成时间")

    # 错误信息
    error_message: Optional[str] = Field(None, description="错误消息")
    failed_nodes: List[Dict[str, str]] = Field(
        default_factory=list,
        description="失败的节点列表，包含节点ID和错误原因"
    )

    class Config:
        from_attributes = True


class BatchTaskStatusResponse(BaseModel):
    """批量任务状态查询响应"""
    task_id: str = Field(..., description="任务ID")
    status: ProcessingStatus = Field(..., description="当前状态")
    progress: float = Field(..., description="进度百分比（0-100）", ge=0.0, le=100.0)
    current_step: str = Field(..., description="当前处理步骤描述")
    estimated_time_remaining: Optional[float] = Field(
        None,
        description="预计剩余时间（秒）"
    )
    result: Optional[BatchReplaceResponse] = Field(
        None,
        description="处理结果（仅在完成或失败时返回）"
    )


class NodeMatchResult(BaseModel):
    """节点匹配结果

    用于返回模式匹配找到的节点信息
    """
    pattern: str = Field(..., description="匹配模式")
    matched_nodes: List[str] = Field(..., description="匹配到的节点ID列表")
    count: int = Field(..., description="匹配数量")