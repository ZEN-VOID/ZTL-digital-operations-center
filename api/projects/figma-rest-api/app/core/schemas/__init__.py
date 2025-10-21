"""
数据模式模块
"""

from .figma import (
    BatchExportRequest,
    FigmaTaskResponse,
    FigmaTaskStatus,
    FigmaBatchResponse,
    FigmaFileResponse,
    FigmaNodeResponse
)

from .batch import (
    ReplacementRule,
    ExportConfig,
    ExportFormat,
    BatchReplaceRequest,
    BatchReplaceResponse,
    ExportedFile,
    ProcessingStatus,
    BatchTaskStatusResponse,
    NodeMatchResult,
)

__all__ = [
    # figma模式
    "BatchExportRequest",
    "FigmaTaskResponse",
    "FigmaTaskStatus",
    "FigmaBatchResponse",
    "FigmaFileResponse",
    "FigmaNodeResponse",
    # batch模式
    "ReplacementRule",
    "ExportConfig",
    "ExportFormat",
    "BatchReplaceRequest",
    "BatchReplaceResponse",
    "ExportedFile",
    "ProcessingStatus",
    "BatchTaskStatusResponse",
    "NodeMatchResult",
]
