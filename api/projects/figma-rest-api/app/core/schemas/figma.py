"""
Figma相关API数据模式
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


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


class BatchReplaceStatus(str, Enum):
    """批量替换状态枚举"""
    PENDING = "pending"
    REPLACING = "replacing"
    EXPORTING = "exporting"
    COMPLETED = "completed"
    FAILED = "failed"


class ProductionWorkflowStatus(str, Enum):
    """量产工作流状态枚举"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


# 官方Figma API兼容的请求模型
class FigmaExportImagesRequest(BaseModel):
    """Figma图片导出请求模型 - 符合官方API规范"""
    ids: str = Field(..., description="逗号分隔的节点ID列表", min_length=1)
    version: Optional[str] = Field(None, description="特定版本ID")
    scale: Optional[float] = Field(default=1.0, description="图像缩放因子", ge=0.01, le=4.0)
    format: Optional[str] = Field(default="png", description="图像输出格式")
    svg_outline_text: Optional[bool] = Field(default=True, description="SVG中文本是否渲染为轮廓")
    svg_include_id: Optional[bool] = Field(default=False, description="是否为SVG元素包含id属性")
    svg_include_node_id: Optional[bool] = Field(default=False, description="是否为SVG元素包含node-id属性")
    svg_simplify_stroke: Optional[bool] = Field(default=True, description="是否简化SVG描边")
    contents_only: Optional[bool] = Field(default=True, description="是否排除重叠内容")
    use_absolute_bounds: Optional[bool] = Field(default=False, description="是否使用绝对边界")

    @field_validator('format')
    @classmethod
    def validate_format(cls, v):
        """验证导出格式"""
        allowed_formats = ["jpg", "png", "svg", "pdf"]
        if v not in allowed_formats:
            raise ValueError(f"格式必须是以下之一: {allowed_formats}")
        return v

    @field_validator('ids')
    @classmethod
    def validate_ids(cls, v):
        """验证节点ID格式"""
        if not v or not v.strip():
            raise ValueError("节点ID列表不能为空")

        # 验证逗号分隔的ID格式
        node_ids = [id.strip() for id in v.split(',')]
        for node_id in node_ids:
            if not node_id:
                raise ValueError("节点ID不能为空")

        return v

# 批量导出请求模型（内部使用）
class BatchExportRequest(BaseModel):
    """批量导出请求模型 - 内部任务管理使用"""
    file_key: str = Field(..., description="Figma文件键", min_length=1)
    node_ids: List[str] = Field(..., description="要导出的节点ID列表", min_items=1)
    export_format: str = Field(default="png", description="导出格式", pattern="^(png|jpg|svg|pdf)$")
    batch_size: int = Field(default=6, description="批次大小", ge=1, le=20)
    scale: float = Field(default=1.0, description="导出缩放比例", ge=0.1, le=4.0)
    output_directory: Optional[str] = Field(None, description="输出目录路径")

    # 新增官方API参数支持
    svg_outline_text: Optional[bool] = Field(default=True, description="SVG中文本是否渲染为轮廓")
    svg_include_id: Optional[bool] = Field(default=False, description="是否为SVG元素包含id属性")
    svg_include_node_id: Optional[bool] = Field(default=False, description="是否为SVG元素包含node-id属性")
    svg_simplify_stroke: Optional[bool] = Field(default=True, description="是否简化SVG描边")
    contents_only: Optional[bool] = Field(default=True, description="是否排除重叠内容")
    use_absolute_bounds: Optional[bool] = Field(default=False, description="是否使用绝对边界")

    @field_validator('node_ids')
    @classmethod
    def validate_node_ids(cls, v):
        """验证节点ID格式"""
        if not v:
            raise ValueError("节点ID列表不能为空")

        for node_id in v:
            if not node_id or not isinstance(node_id, str):
                raise ValueError(f"无效的节点ID: {node_id}")

        return v

    @field_validator('file_key')
    @classmethod
    def validate_file_key(cls, v):
        """验证Figma文件键格式"""
        if not v or len(v) < 10:
            raise ValueError("无效的Figma文件键")
        return v


class FigmaTaskResponse(BaseModel):
    """Figma任务响应模型"""
    task_id: str = Field(..., description="任务ID")
    status: FigmaTaskStatus = Field(..., description="任务状态")
    message: str = Field(..., description="状态消息")
    file_key: str = Field(..., description="Figma文件键")
    total_batches: int = Field(..., description="总批次数")
    completed_batches: int = Field(..., description="已完成批次数")
    failed_batches: int = Field(..., description="失败批次数")
    progress: float = Field(..., description="进度百分比", ge=0.0, le=100.0)
    total_nodes: int = Field(..., description="总节点数")
    export_format: str = Field(..., description="导出格式")
    scale: float = Field(..., description="导出缩放比例")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    started_at: Optional[datetime] = Field(None, description="开始处理时间")
    completed_at: Optional[datetime] = Field(None, description="完成时间")
    error_message: Optional[str] = Field(None, description="错误消息")

    class Config:
        from_attributes = True


class FigmaBatchResponse(BaseModel):
    """Figma批次响应模型"""
    batch_id: str = Field(..., description="批次ID")
    task_id: str = Field(..., description="关联任务ID")
    batch_index: int = Field(..., description="批次索引")
    status: FigmaBatchStatus = Field(..., description="批次状态")
    node_ids: List[str] = Field(..., description="节点ID列表")
    export_urls: Optional[List[str]] = Field(None, description="导出URL列表")
    downloaded_files: Optional[List[str]] = Field(None, description="已下载文件路径列表")
    retry_count: int = Field(..., description="重试次数")
    max_retries: int = Field(..., description="最大重试次数")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    error_message: Optional[str] = Field(None, description="错误消息")

    class Config:
        from_attributes = True


class FigmaFileResponse(BaseModel):
    """Figma文件信息响应模型"""
    file_key: str = Field(..., description="文件键")
    name: str = Field(..., description="文件名")
    thumbnail_url: Optional[str] = Field(None, description="缩略图URL")
    last_modified: Optional[datetime] = Field(None, description="最后修改时间")
    version: Optional[str] = Field(None, description="文件版本")
    document: Optional[Dict[str, Any]] = Field(None, description="文档结构")


class FigmaNodeResponse(BaseModel):
    """Figma节点信息响应模型"""
    node_id: str = Field(..., description="节点ID")
    name: str = Field(..., description="节点名称")
    type: str = Field(..., description="节点类型")
    visible: bool = Field(..., description="是否可见")
    absolute_bounding_box: Optional[Dict[str, float]] = Field(None, description="绝对边界框")
    children: Optional[List[str]] = Field(None, description="子节点ID列表")


# 官方Figma API响应格式
class FigmaExportResponse(BaseModel):
    """Figma导出响应模型 - 符合官方API规范"""
    err: Optional[str] = Field(None, description="错误信息")
    images: Dict[str, Optional[str]] = Field(..., description="节点ID到图片URL的映射，失败的节点值为null")
    status: int = Field(..., description="HTTP状态码")

class FigmaFileMetaResponse(BaseModel):
    """Figma文件元数据响应模型"""
    name: str = Field(..., description="文件名")
    lastModified: str = Field(..., description="最后修改时间")
    thumbnailUrl: str = Field(..., description="缩略图URL")
    version: str = Field(..., description="文件版本")
    role: str = Field(..., description="用户角色")
    editorType: str = Field(..., description="编辑器类型")
    linkAccess: str = Field(..., description="链接访问权限")

class FigmaGetFileResponse(BaseModel):
    """Figma获取文件响应模型"""
    document: Dict[str, Any] = Field(..., description="文档结构")
    components: Dict[str, Any] = Field(..., description="组件映射")
    componentSets: Dict[str, Any] = Field(default_factory=dict, description="组件集映射")
    schemaVersion: int = Field(..., description="模式版本")
    styles: Dict[str, Any] = Field(default_factory=dict, description="样式映射")
    name: str = Field(..., description="文件名")
    lastModified: str = Field(..., description="最后修改时间")
    thumbnailUrl: str = Field(..., description="缩略图URL")
    version: str = Field(..., description="文件版本")
    role: str = Field(..., description="用户角色")
    editorType: str = Field(..., description="编辑器类型")
    linkAccess: str = Field(..., description="链接访问权限")

class FigmaGetFileNodesResponse(BaseModel):
    """Figma获取文件节点响应模型"""
    name: str = Field(..., description="文件名")
    lastModified: str = Field(..., description="最后修改时间")
    thumbnailUrl: str = Field(..., description="缩略图URL")
    version: str = Field(..., description="文件版本")
    role: str = Field(..., description="用户角色")
    editorType: str = Field(..., description="编辑器类型")
    linkAccess: str = Field(..., description="链接访问权限")
    nodes: Dict[str, Optional[Dict[str, Any]]] = Field(..., description="节点映射，失败的节点值为null")
    components: Dict[str, Any] = Field(default_factory=dict, description="组件映射")
    componentSets: Dict[str, Any] = Field(default_factory=dict, description="组件集映射")
    schemaVersion: int = Field(..., description="模式版本")
    styles: Dict[str, Any] = Field(default_factory=dict, description="样式映射")


class TaskRetryRequest(BaseModel):
    """任务重试请求模型"""
    batch_ids: Optional[List[str]] = Field(None, description="要重试的批次ID列表，为空则重试所有失败批次")
    reset_retry_count: bool = Field(default=False, description="是否重置重试计数")


class TaskListResponse(BaseModel):
    """任务列表响应模型"""
    tasks: List[FigmaTaskResponse] = Field(..., description="任务列表")
    total: int = Field(..., description="总任务数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页大小")
    has_next: bool = Field(..., description="是否有下一页")


class BatchListResponse(BaseModel):
    """批次列表响应模型"""
    batches: List[FigmaBatchResponse] = Field(..., description="批次列表")
    total: int = Field(..., description="总批次数")
    task_id: str = Field(..., description="关联任务ID")


class FigmaHealthResponse(BaseModel):
    """Figma服务健康检查响应"""
    status: str = Field(..., description="服务状态")
    figma_api_available: bool = Field(..., description="Figma API是否可用")
    database_connected: bool = Field(..., description="数据库是否连接")
    timestamp: datetime = Field(..., description="检查时间")
    version: str = Field(..., description="服务版本")


# ==================== 批量替换图片相关模型 ====================

class ImageReplaceItem(BaseModel):
    """图片替换项"""
    node_id: Optional[str] = Field(None, description="要替换的节点ID")
    figma_url: Optional[str] = Field(None, description="Figma URL (自动提取node_id)")
    image_url: str = Field(..., description="新图片URL")
    image_name: Optional[str] = Field(None, description="图片名称")

    def model_post_init(self, __context) -> None:
        """验证和处理URL"""
        if not self.node_id and not self.figma_url:
            raise ValueError("必须提供 node_id 或 figma_url")

        if self.figma_url and not self.node_id:
            # 从URL提取node_id
            from ..utils.figma_url_parser import extract_node_ids
            try:
                node_ids = extract_node_ids(self.figma_url)
                if node_ids:
                    self.node_id = node_ids[0]
                else:
                    raise ValueError("无法从URL中提取node_id")
            except Exception as e:
                raise ValueError(f"URL解析失败: {e}")


class BatchReplaceRequest(BaseModel):
    """批量替换图片请求"""
    file_key: Optional[str] = Field(None, description="Figma文件键")
    figma_url: Optional[str] = Field(None, description="Figma文件URL (自动提取file_key)")
    replacements: List[ImageReplaceItem] = Field(..., description="替换项列表", min_items=1, max_items=50)
    batch_name: Optional[str] = Field(None, description="批次名称")
    callback_url: Optional[str] = Field(None, description="完成后回调URL")

    def model_post_init(self, __context) -> None:
        """验证和处理URL"""
        if not self.file_key and not self.figma_url:
            raise ValueError("必须提供 file_key 或 figma_url")

        if self.figma_url and not self.file_key:
            # 从URL提取file_key
            from ..utils.figma_url_parser import extract_file_key
            try:
                self.file_key = extract_file_key(self.figma_url)
            except Exception as e:
                raise ValueError(f"URL解析失败: {e}")
    auto_export: bool = Field(default=True, description="替换完成后是否自动导出")
    export_format: str = Field(default="png", description="导出格式")
    export_scale: float = Field(default=1.0, description="导出缩放", ge=0.1, le=4.0)

    # COS云存储配置（动态入参）
    save_to_cos: bool = Field(default=False, description="是否保存到COS云存储")
    cos_bucket: Optional[str] = Field(None, description="COS存储桶名称（如：minghong-redbook-1353737511）")
    cos_directory: Optional[str] = Field(None, description="COS目录路径（如：minghong/food-exploration/）")
    cos_region: Optional[str] = Field(None, description="COS地域（如：ap-chengdu，为空则使用默认配置）")

    @field_validator('export_format')
    @classmethod
    def validate_export_format(cls, v):
        allowed_formats = ["png", "jpg", "svg", "pdf"]
        if v not in allowed_formats:
            raise ValueError(f"导出格式必须是以下之一: {allowed_formats}")
        return v

    @field_validator('cos_directory')
    @classmethod
    def validate_cos_directory(cls, v, info):
        """验证COS目录配置"""
        if info.data.get('save_to_cos') and not v:
            raise ValueError("启用COS存储时必须提供cos_directory")
        return v

    @field_validator('cos_bucket')
    @classmethod
    def validate_cos_bucket(cls, v, info):
        """验证COS存储桶配置"""
        if info.data.get('save_to_cos') and not v:
            raise ValueError("启用COS存储时必须提供cos_bucket")
        return v


class BatchReplaceResponse(BaseModel):
    """批量替换响应"""
    task_id: str = Field(..., description="任务ID")
    status: BatchReplaceStatus = Field(..., description="任务状态")
    file_key: str = Field(..., description="Figma文件键")
    total_items: int = Field(..., description="总替换项数")
    completed_items: int = Field(default=0, description="已完成项数")
    failed_items: int = Field(default=0, description="失败项数")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    error_message: Optional[str] = Field(None, description="错误信息")
    export_urls: List[str] = Field(default_factory=list, description="导出图片URL列表")


# ==================== 量产设计工作流相关模型 ====================

class ProductionBatch(BaseModel):
    """量产批次"""
    batch_id: str = Field(..., description="批次ID")
    frame_id: str = Field(..., description="画板/Frame节点ID")
    replacements: List[ImageReplaceItem] = Field(..., description="本批次的替换项")
    batch_size: int = Field(default=6, description="批次大小", ge=1, le=24)


class ProductionWorkflowRequest(BaseModel):
    """量产设计工作流请求"""
    file_key: str = Field(..., description="Figma文件键")
    template_frame_id: str = Field(..., description="模板画板ID")
    image_urls: List[str] = Field(..., description="要替换的图片URL列表", min_items=1)
    target_node_ids: List[str] = Field(..., description="目标节点ID列表", min_items=1)
    batch_size: int = Field(default=6, description="每批处理数量", ge=1, le=24)
    export_format: str = Field(default="png", description="导出格式")
    export_scale: float = Field(default=1.0, description="导出缩放", ge=0.1, le=4.0)
    throttle_delay: float = Field(default=1.0, description="批次间延迟(秒)", ge=0.1, le=10.0)
    callback_url: Optional[str] = Field(None, description="进度回调URL")
    workflow_name: Optional[str] = Field(None, description="工作流名称")

    @field_validator('export_format')
    @classmethod
    def validate_export_format(cls, v):
        allowed_formats = ["png", "jpg", "svg", "pdf"]
        if v not in allowed_formats:
            raise ValueError(f"导出格式必须是以下之一: {allowed_formats}")
        return v


class ProductionWorkflowResponse(BaseModel):
    """量产设计工作流响应"""
    workflow_id: str = Field(..., description="工作流ID")
    status: ProductionWorkflowStatus = Field(..., description="工作流状态")
    file_key: str = Field(..., description="Figma文件键")
    total_batches: int = Field(..., description="总批次数")
    completed_batches: int = Field(default=0, description="已完成批次数")
    failed_batches: int = Field(default=0, description="失败批次数")
    total_images: int = Field(..., description="总图片数")
    completed_images: int = Field(default=0, description="已完成图片数")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    estimated_completion: Optional[datetime] = Field(None, description="预计完成时间")
    error_message: Optional[str] = Field(None, description="错误信息")
    export_urls: List[str] = Field(default_factory=list, description="已导出图片URL列表")
    batches: List[ProductionBatch] = Field(default_factory=list, description="批次详情")


# ==================== 插件桥接相关模型 ====================

class PluginMessage(BaseModel):
    """插件消息"""
    type: str = Field(..., description="消息类型")
    data: Dict[str, Any] = Field(..., description="消息数据")
    timestamp: datetime = Field(default_factory=datetime.now, description="时间戳")


class PluginReplaceRequest(BaseModel):
    """插件替换请求"""
    task_id: str = Field(..., description="任务ID")
    replacements: List[ImageReplaceItem] = Field(..., description="替换项列表")
    callback_url: Optional[str] = Field(None, description="完成回调URL")


class PluginReplaceResponse(BaseModel):
    """插件替换响应"""
    success: bool = Field(..., description="是否成功")
    task_id: str = Field(..., description="任务ID")
    completed_count: int = Field(..., description="完成数量")
    failed_count: int = Field(..., description="失败数量")
    error_message: Optional[str] = Field(None, description="错误信息")
    failed_items: List[str] = Field(default_factory=list, description="失败的节点ID列表")


class PluginExportRequest(BaseModel):
    """插件导出请求"""
    task_id: str = Field(..., description="任务ID")
    node_ids: List[str] = Field(..., description="要导出的节点ID列表")
    format: str = Field(default="png", description="导出格式")
    scale: float = Field(default=1.0, description="导出缩放", ge=0.1, le=4.0)
    callback_url: Optional[str] = Field(None, description="完成回调URL")


class PluginExportResponse(BaseModel):
    """插件导出响应"""
    success: bool = Field(..., description="是否成功")
    task_id: str = Field(..., description="任务ID")
    export_urls: List[str] = Field(..., description="导出URL列表")
    failed_nodes: List[str] = Field(default_factory=list, description="导出失败的节点ID")
    error_message: Optional[str] = Field(None, description="错误信息")


# ==================== 任务编排相关模型 ====================

class TaskOrchestrationConfig(BaseModel):
    """任务编排配置"""
    max_concurrent_tasks: int = Field(default=3, description="最大并发任务数", ge=1, le=10)
    batch_size: int = Field(default=6, description="批次大小", ge=1, le=24)
    throttle_delay: float = Field(default=1.0, description="节流延迟(秒)", ge=0.1, le=10.0)
    max_retries: int = Field(default=3, description="最大重试次数", ge=0, le=10)
    retry_delay: float = Field(default=2.0, description="重试延迟(秒)", ge=0.5, le=30.0)
    timeout_seconds: int = Field(default=300, description="任务超时时间(秒)", ge=30, le=3600)


class TaskQueue(BaseModel):
    """任务队列"""
    queue_id: str = Field(..., description="队列ID")
    queue_name: str = Field(..., description="队列名称")
    pending_tasks: int = Field(default=0, description="待处理任务数")
    running_tasks: int = Field(default=0, description="运行中任务数")
    completed_tasks: int = Field(default=0, description="已完成任务数")
    failed_tasks: int = Field(default=0, description="失败任务数")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")


class TaskQueueStatus(BaseModel):
    """任务队列状态"""
    queues: List[TaskQueue] = Field(..., description="队列列表")
    total_pending: int = Field(..., description="总待处理任务数")
    total_running: int = Field(..., description="总运行中任务数")
    system_load: float = Field(..., description="系统负载", ge=0.0, le=1.0)
    last_updated: datetime = Field(..., description="最后更新时间")


# ==================== 高级功能相关模型 ====================

class BulkOperationRequest(BaseModel):
    """批量操作请求"""
    operation_type: str = Field(..., description="操作类型: replace, export, workflow")
    file_keys: List[str] = Field(..., description="文件键列表", min_items=1, max_items=10)
    operation_config: Dict[str, Any] = Field(..., description="操作配置")
    priority: int = Field(default=5, description="优先级(1-10)", ge=1, le=10)
    callback_url: Optional[str] = Field(None, description="完成回调URL")


class BulkOperationResponse(BaseModel):
    """批量操作响应"""
    operation_id: str = Field(..., description="操作ID")
    status: str = Field(..., description="操作状态")
    total_files: int = Field(..., description="总文件数")
    completed_files: int = Field(default=0, description="已完成文件数")
    failed_files: int = Field(default=0, description="失败文件数")
    created_at: datetime = Field(..., description="创建时间")
    estimated_completion: Optional[datetime] = Field(None, description="预计完成时间")
    results: List[Dict[str, Any]] = Field(default_factory=list, description="操作结果列表")
