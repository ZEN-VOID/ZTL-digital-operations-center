"""
完整的Figma官方API数据模型
基于Figma官方REST API规范的完整数据模型定义
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field


# ==================== 基础类型 ====================

class NodeType(str, Enum):
    """节点类型枚举"""
    DOCUMENT = "DOCUMENT"
    CANVAS = "CANVAS"
    FRAME = "FRAME"
    GROUP = "GROUP"
    VECTOR = "VECTOR"
    BOOLEAN_OPERATION = "BOOLEAN_OPERATION"
    STAR = "STAR"
    LINE = "LINE"
    ELLIPSE = "ELLIPSE"
    REGULAR_POLYGON = "REGULAR_POLYGON"
    RECTANGLE = "RECTANGLE"
    TEXT = "TEXT"
    SLICE = "SLICE"
    COMPONENT = "COMPONENT"
    COMPONENT_SET = "COMPONENT_SET"
    INSTANCE = "INSTANCE"
    STICKY = "STICKY"
    SHAPE_WITH_TEXT = "SHAPE_WITH_TEXT"
    CONNECTOR = "CONNECTOR"


class BlendMode(str, Enum):
    """混合模式枚举"""
    PASS_THROUGH = "PASS_THROUGH"
    NORMAL = "NORMAL"
    DARKEN = "DARKEN"
    MULTIPLY = "MULTIPLY"
    LINEAR_BURN = "LINEAR_BURN"
    COLOR_BURN = "COLOR_BURN"
    LIGHTEN = "LIGHTEN"
    SCREEN = "SCREEN"
    LINEAR_DODGE = "LINEAR_DODGE"
    COLOR_DODGE = "COLOR_DODGE"
    OVERLAY = "OVERLAY"
    SOFT_LIGHT = "SOFT_LIGHT"
    HARD_LIGHT = "HARD_LIGHT"
    DIFFERENCE = "DIFFERENCE"
    EXCLUSION = "EXCLUSION"
    HUE = "HUE"
    SATURATION = "SATURATION"
    COLOR = "COLOR"
    LUMINOSITY = "LUMINOSITY"


class LayoutConstraint(BaseModel):
    """布局约束"""
    vertical: str = Field(..., description="垂直约束")
    horizontal: str = Field(..., description="水平约束")


class Rectangle(BaseModel):
    """矩形"""
    x: float = Field(..., description="X坐标")
    y: float = Field(..., description="Y坐标")
    width: float = Field(..., description="宽度")
    height: float = Field(..., description="高度")


class Transform(BaseModel):
    """变换矩阵"""
    matrix: List[List[float]] = Field(..., description="3x2变换矩阵")


class Paint(BaseModel):
    """填充样式"""
    type: str = Field(..., description="填充类型")
    visible: Optional[bool] = Field(True, description="是否可见")
    opacity: Optional[float] = Field(1.0, description="不透明度")
    color: Optional[Dict[str, float]] = Field(None, description="颜色")
    blendMode: Optional[BlendMode] = Field(None, description="混合模式")


class Effect(BaseModel):
    """效果"""
    type: str = Field(..., description="效果类型")
    visible: Optional[bool] = Field(True, description="是否可见")
    radius: Optional[float] = Field(None, description="半径")
    color: Optional[Dict[str, float]] = Field(None, description="颜色")
    offset: Optional[Dict[str, float]] = Field(None, description="偏移")
    spread: Optional[float] = Field(None, description="扩散")


class Node(BaseModel):
    """基础节点"""
    id: str = Field(..., description="节点ID")
    name: str = Field(..., description="节点名称")
    type: NodeType = Field(..., description="节点类型")
    visible: Optional[bool] = Field(True, description="是否可见")
    locked: Optional[bool] = Field(False, description="是否锁定")
    children: Optional[List['Node']] = Field(None, description="子节点")
    absoluteBoundingBox: Optional[Rectangle] = Field(None, description="绝对边界框")
    absoluteRenderBounds: Optional[Rectangle] = Field(None, description="绝对渲染边界")
    constraints: Optional[LayoutConstraint] = Field(None, description="布局约束")
    layoutAlign: Optional[str] = Field(None, description="布局对齐")
    layoutGrow: Optional[float] = Field(None, description="布局增长")
    layoutSizingHorizontal: Optional[str] = Field(None, description="水平尺寸")
    layoutSizingVertical: Optional[str] = Field(None, description="垂直尺寸")
    clipsContent: Optional[bool] = Field(None, description="是否裁剪内容")
    background: Optional[List[Paint]] = Field(None, description="背景")
    backgroundColor: Optional[Dict[str, float]] = Field(None, description="背景颜色")
    fills: Optional[List[Paint]] = Field(None, description="填充")
    strokes: Optional[List[Paint]] = Field(None, description="描边")
    strokeWeight: Optional[float] = Field(None, description="描边粗细")
    strokeAlign: Optional[str] = Field(None, description="描边对齐")
    strokeCap: Optional[str] = Field(None, description="描边端点")
    strokeJoin: Optional[str] = Field(None, description="描边连接")
    strokeDashes: Optional[List[float]] = Field(None, description="描边虚线")
    cornerRadius: Optional[float] = Field(None, description="圆角半径")
    rectangleCornerRadii: Optional[List[float]] = Field(None, description="矩形圆角半径")
    effects: Optional[List[Effect]] = Field(None, description="效果")
    isMask: Optional[bool] = Field(None, description="是否为蒙版")
    isMaskOutline: Optional[bool] = Field(None, description="是否为蒙版轮廓")
    styles: Optional[Dict[str, str]] = Field(None, description="样式")
    exportSettings: Optional[List[Dict[str, Any]]] = Field(None, description="导出设置")
    blendMode: Optional[BlendMode] = Field(None, description="混合模式")
    preserveRatio: Optional[bool] = Field(None, description="保持比例")
    layoutMode: Optional[str] = Field(None, description="布局模式")
    primaryAxisSizingMode: Optional[str] = Field(None, description="主轴尺寸模式")
    counterAxisSizingMode: Optional[str] = Field(None, description="交叉轴尺寸模式")
    primaryAxisAlignItems: Optional[str] = Field(None, description="主轴对齐")
    counterAxisAlignItems: Optional[str] = Field(None, description="交叉轴对齐")
    paddingLeft: Optional[float] = Field(None, description="左内边距")
    paddingRight: Optional[float] = Field(None, description="右内边距")
    paddingTop: Optional[float] = Field(None, description="上内边距")
    paddingBottom: Optional[float] = Field(None, description="下内边距")
    itemSpacing: Optional[float] = Field(None, description="项目间距")
    overflowDirection: Optional[str] = Field(None, description="溢出方向")
    numberOfFixedChildren: Optional[int] = Field(None, description="固定子项数量")
    overlayPositionType: Optional[str] = Field(None, description="覆盖位置类型")
    overlayBackground: Optional[Dict[str, Any]] = Field(None, description="覆盖背景")
    overlayBackgroundInteraction: Optional[str] = Field(None, description="覆盖背景交互")


# ==================== Files API 响应模型 ====================

class Document(BaseModel):
    """文档"""
    id: str = Field(..., description="文档ID")
    name: str = Field(..., description="文档名称")
    type: str = Field(..., description="文档类型")
    children: List[Node] = Field(..., description="子节点")


class GetFileResponse(BaseModel):
    """获取文件响应"""
    name: str = Field(..., description="文件名称")
    role: str = Field(..., description="用户角色")
    lastModified: str = Field(..., description="最后修改时间")
    editorType: str = Field(..., description="编辑器类型")
    thumbnailUrl: str = Field(..., description="缩略图URL")
    version: str = Field(..., description="版本")
    document: Document = Field(..., description="文档内容")
    components: Dict[str, Any] = Field(default_factory=dict, description="组件")
    componentSets: Dict[str, Any] = Field(default_factory=dict, description="组件集")
    schemaVersion: int = Field(..., description="模式版本")
    styles: Dict[str, Any] = Field(default_factory=dict, description="样式")
    mainFileKey: Optional[str] = Field(None, description="主文件键")
    branches: Optional[List[Dict[str, Any]]] = Field(None, description="分支")


class GetFileNodesResponse(BaseModel):
    """获取文件节点响应"""
    name: str = Field(..., description="文件名称")
    role: str = Field(..., description="用户角色")
    lastModified: str = Field(..., description="最后修改时间")
    editorType: str = Field(..., description="编辑器类型")
    thumbnailUrl: str = Field(..., description="缩略图URL")
    version: str = Field(..., description="版本")
    nodes: Dict[str, Optional[Node]] = Field(..., description="节点映射")
    components: Dict[str, Any] = Field(default_factory=dict, description="组件")
    componentSets: Dict[str, Any] = Field(default_factory=dict, description="组件集")
    schemaVersion: int = Field(..., description="模式版本")
    styles: Dict[str, Any] = Field(default_factory=dict, description="样式")


class FileVersion(BaseModel):
    """文件版本"""
    id: str = Field(..., description="版本ID")
    created_at: str = Field(..., description="创建时间")
    label: Optional[str] = Field(None, description="版本标签")
    description: Optional[str] = Field(None, description="版本描述")
    user: Dict[str, Any] = Field(..., description="用户信息")


class GetFileVersionsResponse(BaseModel):
    """获取文件版本响应"""
    versions: List[FileVersion] = Field(..., description="版本列表")
    pagination: Optional[Dict[str, Any]] = Field(None, description="分页信息")


# ==================== Images API 响应模型 ====================

class GetImagesResponse(BaseModel):
    """获取图片响应"""
    err: Optional[str] = Field(None, description="错误信息")
    images: Dict[str, Optional[str]] = Field(..., description="图片URL映射")
    status: Optional[int] = Field(None, description="状态码")


# ==================== Comments API 模型 ====================

class User(BaseModel):
    """用户"""
    id: str = Field(..., description="用户ID")
    handle: str = Field(..., description="用户句柄")
    img_url: str = Field(..., description="头像URL")
    email: Optional[str] = Field(None, description="邮箱")


class Comment(BaseModel):
    """评论"""
    id: str = Field(..., description="评论ID")
    file_key: str = Field(..., description="文件键")
    parent_id: Optional[str] = Field(None, description="父评论ID")
    user: User = Field(..., description="用户")
    created_at: str = Field(..., description="创建时间")
    resolved_at: Optional[str] = Field(None, description="解决时间")
    message: str = Field(..., description="评论内容")
    client_meta: Optional[Dict[str, Any]] = Field(None, description="客户端元数据")
    order_id: Optional[str] = Field(None, description="排序ID")


class GetCommentsResponse(BaseModel):
    """获取评论响应"""
    comments: List[Comment] = Field(..., description="评论列表")


class PostCommentRequest(BaseModel):
    """发布评论请求"""
    message: str = Field(..., description="评论内容")
    client_meta: Optional[Dict[str, Any]] = Field(None, description="客户端元数据")
    comment_id: Optional[str] = Field(None, description="回复的评论ID")


class PostCommentResponse(BaseModel):
    """发布评论响应"""
    id: str = Field(..., description="评论ID")
    file_key: str = Field(..., description="文件键")
    parent_id: Optional[str] = Field(None, description="父评论ID")
    user: User = Field(..., description="用户")
    created_at: str = Field(..., description="创建时间")
    resolved_at: Optional[str] = Field(None, description="解决时间")
    message: str = Field(..., description="评论内容")
    client_meta: Optional[Dict[str, Any]] = Field(None, description="客户端元数据")
    order_id: Optional[str] = Field(None, description="排序ID")


class DeleteCommentResponse(BaseModel):
    """删除评论响应"""
    success: bool = Field(..., description="是否成功")


# ==================== Users API 响应模型 ====================

class GetUserResponse(BaseModel):
    """获取用户响应"""
    id: str = Field(..., description="用户ID")
    handle: str = Field(..., description="用户句柄")
    img_url: str = Field(..., description="头像URL")
    email: str = Field(..., description="邮箱")


# ==================== Projects API 响应模型 ====================

class Project(BaseModel):
    """项目"""
    id: str = Field(..., description="项目ID")
    name: str = Field(..., description="项目名称")


class GetTeamProjectsResponse(BaseModel):
    """获取团队项目响应"""
    projects: List[Project] = Field(..., description="项目列表")


class ProjectFile(BaseModel):
    """项目文件"""
    key: str = Field(..., description="文件键")
    name: str = Field(..., description="文件名称")
    thumbnail_url: str = Field(..., description="缩略图URL")
    last_modified: str = Field(..., description="最后修改时间")
    branches: Optional[List[Dict[str, Any]]] = Field(None, description="分支")


class GetProjectFilesResponse(BaseModel):
    """获取项目文件响应"""
    files: List[ProjectFile] = Field(..., description="文件列表")


# ==================== Component Types API 响应模型 ====================

class Component(BaseModel):
    """组件"""
    key: str = Field(..., description="组件键")
    file_key: str = Field(..., description="文件键")
    node_id: str = Field(..., description="节点ID")
    thumbnail_url: str = Field(..., description="缩略图URL")
    name: str = Field(..., description="组件名称")
    description: str = Field(..., description="组件描述")
    created_at: str = Field(..., description="创建时间")
    updated_at: str = Field(..., description="更新时间")
    user: User = Field(..., description="创建用户")
    containing_frame: Optional[Dict[str, Any]] = Field(None, description="包含框架")
    containing_page: Optional[Dict[str, Any]] = Field(None, description="包含页面")


class GetTeamComponentsResponse(BaseModel):
    """获取团队组件响应"""
    status: int = Field(..., description="状态码")
    error: bool = Field(..., description="是否有错误")
    meta: Dict[str, Any] = Field(..., description="元数据")
    components: List[Component] = Field(..., description="组件列表")


class GetComponentResponse(BaseModel):
    """获取组件响应"""
    status: int = Field(..., description="状态码")
    error: bool = Field(..., description="是否有错误")
    meta: Component = Field(..., description="组件信息")


class ComponentSet(BaseModel):
    """组件集"""
    key: str = Field(..., description="组件集键")
    file_key: str = Field(..., description="文件键")
    node_id: str = Field(..., description="节点ID")
    thumbnail_url: str = Field(..., description="缩略图URL")
    name: str = Field(..., description="组件集名称")
    description: str = Field(..., description="组件集描述")
    created_at: str = Field(..., description="创建时间")
    updated_at: str = Field(..., description="更新时间")
    user: User = Field(..., description="创建用户")
    containing_frame: Optional[Dict[str, Any]] = Field(None, description="包含框架")
    containing_page: Optional[Dict[str, Any]] = Field(None, description="包含页面")


class GetTeamComponentSetsResponse(BaseModel):
    """获取团队组件集响应"""
    status: int = Field(..., description="状态码")
    error: bool = Field(..., description="是否有错误")
    meta: Dict[str, Any] = Field(..., description="元数据")
    component_sets: List[ComponentSet] = Field(..., description="组件集列表")


class GetComponentSetResponse(BaseModel):
    """获取组件集响应"""
    status: int = Field(..., description="状态码")
    error: bool = Field(..., description="是否有错误")
    meta: ComponentSet = Field(..., description="组件集信息")


# ==================== Styles API 响应模型 ====================

class Style(BaseModel):
    """样式"""
    key: str = Field(..., description="样式键")
    file_key: str = Field(..., description="文件键")
    node_id: str = Field(..., description="节点ID")
    style_type: str = Field(..., description="样式类型")
    thumbnail_url: str = Field(..., description="缩略图URL")
    name: str = Field(..., description="样式名称")
    description: str = Field(..., description="样式描述")
    created_at: str = Field(..., description="创建时间")
    updated_at: str = Field(..., description="更新时间")
    user: User = Field(..., description="创建用户")
    sort_position: str = Field(..., description="排序位置")


class GetTeamStylesResponse(BaseModel):
    """获取团队样式响应"""
    status: int = Field(..., description="状态码")
    error: bool = Field(..., description="是否有错误")
    meta: Dict[str, Any] = Field(..., description="元数据")
    styles: List[Style] = Field(..., description="样式列表")


class GetStyleResponse(BaseModel):
    """获取样式响应"""
    status: int = Field(..., description="状态码")
    error: bool = Field(..., description="是否有错误")
    meta: Style = Field(..., description="样式信息")


# ==================== Variables API 模型 ====================

class Variable(BaseModel):
    """变量"""
    id: str = Field(..., description="变量ID")
    name: str = Field(..., description="变量名称")
    key: str = Field(..., description="变量键")
    variableCollectionId: str = Field(..., description="变量集合ID")
    resolvedType: str = Field(..., description="解析类型")
    valuesByMode: Dict[str, Any] = Field(..., description="按模式的值")
    remote: bool = Field(..., description="是否远程")
    description: str = Field(..., description="描述")
    hiddenFromPublishing: bool = Field(..., description="是否隐藏发布")
    scopes: List[str] = Field(..., description="作用域")
    codeSyntax: Dict[str, Any] = Field(..., description="代码语法")


class VariableCollection(BaseModel):
    """变量集合"""
    id: str = Field(..., description="集合ID")
    name: str = Field(..., description="集合名称")
    key: str = Field(..., description="集合键")
    modes: List[Dict[str, Any]] = Field(..., description="模式")
    defaultModeId: str = Field(..., description="默认模式ID")
    remote: bool = Field(..., description="是否远程")
    hiddenFromPublishing: bool = Field(..., description="是否隐藏发布")
    variableIds: List[str] = Field(..., description="变量ID列表")


class GetLocalVariablesResponse(BaseModel):
    """获取本地变量响应"""
    status: int = Field(..., description="状态码")
    error: bool = Field(..., description="是否有错误")
    meta: Dict[str, Any] = Field(..., description="元数据")
    variables: Dict[str, Variable] = Field(..., description="变量映射")
    variableCollections: Dict[str, VariableCollection] = Field(..., description="变量集合映射")


class GetPublishedVariablesResponse(BaseModel):
    """获取已发布变量响应"""
    status: int = Field(..., description="状态码")
    error: bool = Field(..., description="是否有错误")
    meta: Dict[str, Any] = Field(..., description="元数据")
    variables: Dict[str, Variable] = Field(..., description="变量映射")
    variableCollections: Dict[str, VariableCollection] = Field(..., description="变量集合映射")


class PostVariablesRequest(BaseModel):
    """创建变量请求"""
    variableCollections: Optional[Dict[str, Any]] = Field(None, description="变量集合")
    variables: Optional[Dict[str, Any]] = Field(None, description="变量")


class PostVariablesResponse(BaseModel):
    """创建变量响应"""
    status: int = Field(..., description="状态码")
    error: bool = Field(..., description="是否有错误")
    meta: Dict[str, Any] = Field(..., description="元数据")
    variables: Dict[str, Variable] = Field(..., description="变量映射")
    variableCollections: Dict[str, VariableCollection] = Field(..., description="变量集合映射")


# ==================== Webhooks API 模型 ====================

class Webhook(BaseModel):
    """Webhook"""
    id: str = Field(..., description="Webhook ID")
    team_id: str = Field(..., description="团队ID")
    event_type: str = Field(..., description="事件类型")
    client_id: str = Field(..., description="客户端ID")
    endpoint: str = Field(..., description="端点URL")
    passcode: str = Field(..., description="密码")
    status: str = Field(..., description="状态")
    description: str = Field(..., description="描述")


class GetWebhooksResponse(BaseModel):
    """获取Webhooks响应"""
    webhooks: List[Webhook] = Field(..., description="Webhook列表")


class PostWebhookRequest(BaseModel):
    """创建Webhook请求"""
    event_type: str = Field(..., description="事件类型")
    team_id: str = Field(..., description="团队ID")
    endpoint: str = Field(..., description="端点URL")
    passcode: Optional[str] = Field(None, description="密码")
    description: Optional[str] = Field(None, description="描述")


class PostWebhookResponse(BaseModel):
    """创建Webhook响应"""
    id: str = Field(..., description="Webhook ID")
    team_id: str = Field(..., description="团队ID")
    event_type: str = Field(..., description="事件类型")
    client_id: str = Field(..., description="客户端ID")
    endpoint: str = Field(..., description="端点URL")
    passcode: str = Field(..., description="密码")
    status: str = Field(..., description="状态")
    description: str = Field(..., description="描述")


class PutWebhookRequest(BaseModel):
    """更新Webhook请求"""
    event_type: Optional[str] = Field(None, description="事件类型")
    endpoint: Optional[str] = Field(None, description="端点URL")
    passcode: Optional[str] = Field(None, description="密码")
    description: Optional[str] = Field(None, description="描述")
    status: Optional[str] = Field(None, description="状态")


class PutWebhookResponse(BaseModel):
    """更新Webhook响应"""
    id: str = Field(..., description="Webhook ID")
    team_id: str = Field(..., description="团队ID")
    event_type: str = Field(..., description="事件类型")
    client_id: str = Field(..., description="客户端ID")
    endpoint: str = Field(..., description="端点URL")
    passcode: str = Field(..., description="密码")
    status: str = Field(..., description="状态")
    description: str = Field(..., description="描述")


class DeleteWebhookResponse(BaseModel):
    """删除Webhook响应"""
    success: bool = Field(..., description="是否成功")


class WebhookRequest(BaseModel):
    """Webhook请求"""
    id: str = Field(..., description="请求ID")
    webhook_id: str = Field(..., description="Webhook ID")
    timestamp: str = Field(..., description="时间戳")
    status: int = Field(..., description="状态码")
    response_body: str = Field(..., description="响应体")


class GetWebhookRequestsResponse(BaseModel):
    """获取Webhook请求响应"""
    requests: List[WebhookRequest] = Field(..., description="请求列表")


# ==================== Activity Logs API 模型 ====================

class ActivityLog(BaseModel):
    """活动日志"""
    id: str = Field(..., description="日志ID")
    timestamp: str = Field(..., description="时间戳")
    user: User = Field(..., description="用户")
    action: str = Field(..., description="操作")
    resource: Dict[str, Any] = Field(..., description="资源")
    metadata: Dict[str, Any] = Field(..., description="元数据")


class GetActivityLogsResponse(BaseModel):
    """获取活动日志响应"""
    logs: List[ActivityLog] = Field(..., description="日志列表")
    cursor: Optional[str] = Field(None, description="游标")
    has_more: bool = Field(..., description="是否有更多")


# ==================== Discovery API 模型 ====================

class DiscoveryItem(BaseModel):
    """发现项目"""
    id: str = Field(..., description="项目ID")
    name: str = Field(..., description="项目名称")
    type: str = Field(..., description="项目类型")
    thumbnail_url: str = Field(..., description="缩略图URL")
    description: str = Field(..., description="描述")
    tags: List[str] = Field(..., description="标签")
    created_at: str = Field(..., description="创建时间")
    updated_at: str = Field(..., description="更新时间")


class GetDiscoveryResponse(BaseModel):
    """获取发现响应"""
    items: List[DiscoveryItem] = Field(..., description="发现项目列表")
    total: int = Field(..., description="总数")


# ==================== Payments API 模型 ====================

class PaymentInfo(BaseModel):
    """支付信息"""
    plan: str = Field(..., description="计划")
    status: str = Field(..., description="状态")
    billing_cycle: str = Field(..., description="计费周期")
    amount: float = Field(..., description="金额")
    currency: str = Field(..., description="货币")
    next_billing_date: str = Field(..., description="下次计费日期")


class GetPaymentsResponse(BaseModel):
    """获取支付响应"""
    payment_info: PaymentInfo = Field(..., description="支付信息")


# ==================== Library Analytics API 模型 ====================

class LibraryAnalytics(BaseModel):
    """库分析"""
    component_usage: Dict[str, int] = Field(..., description="组件使用情况")
    style_usage: Dict[str, int] = Field(..., description="样式使用情况")
    total_components: int = Field(..., description="总组件数")
    total_styles: int = Field(..., description="总样式数")
    active_users: int = Field(..., description="活跃用户数")


class GetLibraryAnalyticsResponse(BaseModel):
    """获取库分析响应"""
    analytics: LibraryAnalytics = Field(..., description="分析数据")
    period: str = Field(..., description="时间段")


# ==================== Dev Resources API 模型 ====================

class DevResource(BaseModel):
    """开发资源"""
    id: str = Field(..., description="资源ID")
    name: str = Field(..., description="资源名称")
    url: str = Field(..., description="资源URL")
    file_key: str = Field(..., description="文件键")
    node_id: str = Field(..., description="节点ID")
    created_at: str = Field(..., description="创建时间")
    updated_at: str = Field(..., description="更新时间")


class GetDevResourcesResponse(BaseModel):
    """获取开发资源响应"""
    resources: List[DevResource] = Field(..., description="资源列表")


class PostDevResourceRequest(BaseModel):
    """创建开发资源请求"""
    name: str = Field(..., description="资源名称")
    url: str = Field(..., description="资源URL")
    file_key: str = Field(..., description="文件键")
    node_id: str = Field(..., description="节点ID")


class PostDevResourceResponse(BaseModel):
    """创建开发资源响应"""
    id: str = Field(..., description="资源ID")
    name: str = Field(..., description="资源名称")
    url: str = Field(..., description="资源URL")
    file_key: str = Field(..., description="文件键")
    node_id: str = Field(..., description="节点ID")
    created_at: str = Field(..., description="创建时间")
    updated_at: str = Field(..., description="更新时间")


class PutDevResourceRequest(BaseModel):
    """更新开发资源请求"""
    name: Optional[str] = Field(None, description="资源名称")
    url: Optional[str] = Field(None, description="资源URL")


class PutDevResourceResponse(BaseModel):
    """更新开发资源响应"""
    id: str = Field(..., description="资源ID")
    name: str = Field(..., description="资源名称")
    url: str = Field(..., description="资源URL")
    file_key: str = Field(..., description="文件键")
    node_id: str = Field(..., description="节点ID")
    created_at: str = Field(..., description="创建时间")
    updated_at: str = Field(..., description="更新时间")


class DeleteDevResourceResponse(BaseModel):
    """删除开发资源响应"""
    success: bool = Field(..., description="是否成功")


# 更新Node模型以支持自引用
Node.model_rebuild()
