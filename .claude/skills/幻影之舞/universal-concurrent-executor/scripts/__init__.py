"""Universal Concurrent Executor - 通用并发执行引擎"""

from .core import (
    # 数据类
    TaskDefinition,
    BatchDefinition,
    ExecutionPlan,
    TaskResult,
    ExecutionReport,

    # 核心类
    DependencyAnalyzer,
    SkillAdapter,
    UniversalConcurrentExecutor,

    # 便捷函数
    load_plan,
    save_report,
    execute_plan,
)

__version__ = "1.0.0"
__all__ = [
    # 数据类
    "TaskDefinition",
    "BatchDefinition",
    "ExecutionPlan",
    "TaskResult",
    "ExecutionReport",

    # 核心类
    "DependencyAnalyzer",
    "SkillAdapter",
    "UniversalConcurrentExecutor",

    # 便捷函数
    "load_plan",
    "save_report",
    "execute_plan",
]
