#!/usr/bin/env python3
"""
Universal Concurrent Executor - 通用并发执行引擎核心
=================================================

为**所有技能包**提供标准化的并发执行能力:
- AIGC: 图片/音乐/视频/语音生成
- Data Processing: Excel分析、数据清洗、批量转换
- Web Scraping: 网页爬虫、数据采集
- Automation: 自动化测试、批量操作

核心特性:
- 并发可行性分析 (前置环节,评估任务并行潜力)
- 智能依赖分析 (显式 + 隐式)
- 分层并发执行 (同层并发,层间串行)
- 健壮错误处理 (单任务失败不影响其他)
- 详细执行报告 (JSON 格式)

Author: ZTL Digital Intelligence Operations Center - 幻影之舞
Version: 1.1.0
Date: 2025-11-01
"""

import json
import logging
import os
import time
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from collections import defaultdict

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


# ============================================
# 通用数据类
# ============================================

@dataclass
class TaskDefinition:
    """
    任务定义 - 通用基类

    所有技能包的任务定义都应包含这些字段
    """
    task_id: str  # 唯一任务标识
    params: Dict[str, Any]  # 任务参数 (技能包特定)
    depends_on: Optional[List[str]] = None  # 依赖的任务 ID 列表
    metadata: Optional[Dict] = None  # 额外元数据


@dataclass
class BatchDefinition:
    """批次定义"""
    batch_id: str
    batch_name: str
    description: Optional[str] = None
    tasks: List[TaskDefinition] = None


@dataclass
class ExecutionPlan:
    """执行计划"""
    plan_id: str
    project_name: str
    batches: List[BatchDefinition]
    total_tasks: int
    total_batches: int
    created_at: Optional[str] = None
    config: Optional[Dict] = None  # 全局配置


@dataclass
class TaskResult:
    """任务执行结果"""
    task_id: str
    status: str  # success, failed, skipped
    start_time: float
    end_time: float
    duration: float
    output_files: Optional[List[str]] = None
    error_message: Optional[str] = None
    api_response: Optional[Dict] = None


@dataclass
class ExecutionReport:
    """执行报告"""
    plan_id: str
    project_name: str
    execution_started: str
    execution_finished: str
    total_duration_seconds: float
    total_tasks: int
    successful_tasks: int
    failed_tasks: int
    skipped_tasks: int
    success_rate: float
    average_duration_seconds: float
    task_results: List[TaskResult]
    errors: List[Dict]


@dataclass
class ExecutionLayer:
    """执行层定义"""
    layer: int
    tasks: List[str]  # task_id列表
    can_parallel: bool
    estimated_duration: float


@dataclass
class ConcurrencyAnalysis:
    """并发可行性分析报告"""
    total_tasks: int
    independent_tasks: int
    dependent_tasks: int
    execution_layers: List[ExecutionLayer]
    recommended_workers: int
    parallelization_ratio: float
    recommendations: List[str]
    estimated_memory_gb: Optional[float] = None
    estimated_duration: Optional[float] = None


# ============================================
# 智能依赖分析器
# ============================================

class DependencyAnalyzer:
    """智能任务依赖分析器"""

    @staticmethod
    def analyze_dependencies(tasks: List[TaskDefinition]) -> Dict[str, List[str]]:
        """
        分析任务之间的依赖关系

        Args:
            tasks: 任务定义列表

        Returns:
            依赖关系图 {task_id: [依赖的任务ID列表]}
        """
        dependency_graph = {}

        for task in tasks:
            task_id = task.task_id
            depends_on = task.depends_on or []

            # 自动检测隐式依赖 (基于文件路径)
            implicit_deps = DependencyAnalyzer._detect_implicit_dependencies(
                task, tasks
            )

            # 合并显式和隐式依赖
            all_deps = list(set(depends_on + implicit_deps))
            dependency_graph[task_id] = all_deps

        return dependency_graph

    @staticmethod
    def _detect_implicit_dependencies(
        task: TaskDefinition,
        all_tasks: List[TaskDefinition]
    ) -> List[str]:
        """
        检测隐式依赖关系

        规则:
        1. 如果任务参数中包含其他任务的输出路径,则隐式依赖该任务
        2. 支持嵌套参数检测

        示例:
        任务A输出: output/task-a/result.png
        任务B参数: {"first_frame_image": "output/task-a/result.png"}
        → 任务B隐式依赖任务A
        """
        implicit_deps = []

        # 递归提取所有参数值(支持嵌套字典)
        def extract_values(obj):
            if isinstance(obj, dict):
                for value in obj.values():
                    yield from extract_values(value)
            elif isinstance(obj, list):
                for item in obj:
                    yield from extract_values(item)
            elif isinstance(obj, str):
                yield obj

        # 提取当前任务的所有字符串参数
        param_values = list(extract_values(task.params))

        # 检查是否引用其他任务的输出
        for other_task in all_tasks:
            if other_task.task_id == task.task_id:
                continue

            # 检查参数中是否包含其他任务ID
            for value in param_values:
                if other_task.task_id in value:
                    implicit_deps.append(other_task.task_id)
                    break

        return implicit_deps

    @staticmethod
    def get_execution_order(tasks: List[TaskDefinition]) -> List[List[TaskDefinition]]:
        """
        拓扑排序 + 分层

        返回执行层列表,每层包含可以并发执行的任务

        Args:
            tasks: 任务定义列表

        Returns:
            执行层列表 [[Layer1 tasks], [Layer2 tasks], ...]
        """
        # 构建依赖图
        dependency_graph = DependencyAnalyzer.analyze_dependencies(tasks)

        # 任务ID到任务对象的映射
        task_map = {task.task_id: task for task in tasks}

        # 计算每个任务的入度
        # 入度 = 该任务依赖的任务数量
        in_degree = {task_id: len(deps) for task_id, deps in dependency_graph.items()}

        # Kahn算法 - 拓扑排序 + 分层
        layers = []
        processed = set()

        while len(processed) < len(tasks):
            # 当前层:所有入度为0的任务
            current_layer = [
                task_map[task_id]
                for task_id, degree in in_degree.items()
                if degree == 0 and task_id not in processed
            ]

            if not current_layer:
                # 检测到循环依赖
                remaining = [t for t in tasks if t.task_id not in processed]
                logger.error(f"检测到循环依赖,剩余任务: {[t.task_id for t in remaining]}")
                break

            layers.append(current_layer)

            # 更新入度
            for task in current_layer:
                processed.add(task.task_id)
                for dependent_id in task_map:
                    if task.task_id in dependency_graph.get(dependent_id, []):
                        in_degree[dependent_id] -= 1

        return layers


# ============================================
# 适配器接口
# ============================================

class SkillAdapter(ABC):
    """技能包适配器抽象基类"""

    @abstractmethod
    def execute_task(self, task: TaskDefinition) -> TaskResult:
        """
        执行单个任务 (必须实现)

        这是技能包特定的核心逻辑:
        - Nano-Banana: 调用 OpenRouter API
        - MiniMax: 调用 MCP Tools
        - Future Skills: 调用其他 API

        Args:
            task: 任务定义

        Returns:
            TaskResult: 执行结果
        """
        pass

    def validate_params(self, params: Dict[str, Any]) -> bool:
        """
        验证任务参数 (可选覆盖)

        默认实现: 总是返回 True

        Args:
            params: 任务参数

        Returns:
            bool: 参数是否有效
        """
        return True

    def pre_execute_hook(self, task: TaskDefinition) -> None:
        """执行前钩子 (可选覆盖)"""
        pass

    def post_execute_hook(self, task: TaskDefinition, result: TaskResult) -> None:
        """执行后钩子 (可选覆盖)"""
        pass


# ============================================
# 通用并发执行引擎
# ============================================

class UniversalConcurrentExecutor:
    """通用并发执行引擎"""

    def __init__(
        self,
        adapter: SkillAdapter,
        max_workers: int = 4,
        enable_dependency_analysis: bool = True
    ):
        """
        Args:
            adapter: 技能包适配器实例
            max_workers: 最大并发线程数
            enable_dependency_analysis: 是否启用依赖分析
        """
        self.adapter = adapter
        self.max_workers = max_workers
        self.enable_dependency_analysis = enable_dependency_analysis

    def execute_plan(self, plan: ExecutionPlan) -> ExecutionReport:
        """
        执行完整执行计划

        核心流程:
        1. 提取所有任务
        2. 依赖分析 (如启用)
        3. 拓扑排序生成执行层
        4. 分层并发执行
        5. 生成执行报告

        Args:
            plan: 执行计划

        Returns:
            ExecutionReport: 执行报告
        """
        logger.info(f"开始执行计划: {plan.plan_id}")
        logger.info(f"项目名称: {plan.project_name}")
        logger.info(f"任务总数: {plan.total_tasks}")
        logger.info(f"批次数: {plan.total_batches}")
        logger.info(f"最大并发线程数: {self.max_workers}")

        start_time = time.time()

        # 1. 提取所有任务
        all_tasks = []
        for batch in plan.batches:
            all_tasks.extend(batch.tasks)

        # 2. 依赖分析 + 拓扑排序
        if self.enable_dependency_analysis:
            logger.info("启用依赖分析...")
            execution_layers = DependencyAnalyzer.get_execution_order(all_tasks)
            logger.info(f"生成 {len(execution_layers)} 个执行层")
        else:
            # 不分析依赖,所有任务在一层
            execution_layers = [all_tasks]
            logger.info("依赖分析已禁用,所有任务将并发执行")

        # 3. 分层并发执行
        all_results = []
        for layer_idx, layer in enumerate(execution_layers, 1):
            logger.info(f"执行第 {layer_idx}/{len(execution_layers)} 层, 包含 {len(layer)} 个任务")
            layer_results = self.execute_layer(layer)
            all_results.extend(layer_results)

        end_time = time.time()

        # 4. 生成执行报告
        report = self._generate_report(
            plan=plan,
            results=all_results,
            start_time=start_time,
            end_time=end_time
        )

        logger.info(f"执行完成!")
        logger.info(f"成功: {report.successful_tasks}/{report.total_tasks}")
        logger.info(f"失败: {report.failed_tasks}/{report.total_tasks}")
        logger.info(f"成功率: {report.success_rate:.2f}%")
        logger.info(f"总耗时: {report.total_duration_seconds:.2f}s")

        return report

    def execute_layer(self, layer: List[TaskDefinition]) -> List[TaskResult]:
        """
        执行单个并发层

        使用 ThreadPoolExecutor 并发执行同层任务

        Args:
            layer: 任务列表

        Returns:
            List[TaskResult]: 执行结果列表
        """
        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._execute_single_task, task): task
                for task in layer
            }

            for future in as_completed(futures):
                task = futures[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logger.error(f"任务 {task.task_id} 执行异常: {e}")
                    results.append(TaskResult(
                        task_id=task.task_id,
                        status="failed",
                        start_time=time.time(),
                        end_time=time.time(),
                        duration=0.0,
                        error_message=str(e)
                    ))

        return results

    def _execute_single_task(self, task: TaskDefinition) -> TaskResult:
        """
        执行单个任务 (内部方法)

        流程:
        1. pre_execute_hook
        2. validate_params
        3. adapter.execute_task() <-- 技能包特定逻辑
        4. post_execute_hook
        5. 错误处理和日志

        Args:
            task: 任务定义

        Returns:
            TaskResult: 执行结果
        """
        start_time = time.time()

        try:
            # 1. 执行前钩子
            self.adapter.pre_execute_hook(task)

            # 2. 验证参数
            if not self.adapter.validate_params(task.params):
                raise ValueError(f"任务 {task.task_id} 参数验证失败")

            # 3. 执行任务 (技能包特定逻辑)
            logger.info(f"开始执行任务: {task.task_id}")
            result = self.adapter.execute_task(task)

            # 4. 执行后钩子
            self.adapter.post_execute_hook(task, result)

            end_time = time.time()
            result.start_time = start_time
            result.end_time = end_time
            result.duration = end_time - start_time

            logger.info(f"✅ 任务完成: {task.task_id} ({result.duration:.2f}s)")

            return result

        except Exception as e:
            end_time = time.time()
            logger.error(f"❌ 任务失败: {task.task_id}, 错误: {e}")

            return TaskResult(
                task_id=task.task_id,
                status="failed",
                start_time=start_time,
                end_time=end_time,
                duration=end_time - start_time,
                error_message=str(e)
            )

    def _generate_report(
        self,
        plan: ExecutionPlan,
        results: List[TaskResult],
        start_time: float,
        end_time: float
    ) -> ExecutionReport:
        """
        生成执行报告

        Args:
            plan: 执行计划
            results: 所有任务结果
            start_time: 开始时间戳
            end_time: 结束时间戳

        Returns:
            ExecutionReport: 执行报告
        """
        total_tasks = len(results)
        successful_tasks = sum(1 for r in results if r.status == "success")
        failed_tasks = sum(1 for r in results if r.status == "failed")
        skipped_tasks = sum(1 for r in results if r.status == "skipped")

        success_rate = (successful_tasks / total_tasks * 100) if total_tasks > 0 else 0.0

        total_duration = end_time - start_time
        avg_duration = (
            sum(r.duration for r in results) / total_tasks
            if total_tasks > 0 else 0.0
        )

        errors = [
            {
                "task_id": r.task_id,
                "error_message": r.error_message
            }
            for r in results if r.status == "failed"
        ]

        return ExecutionReport(
            plan_id=plan.plan_id,
            project_name=plan.project_name,
            execution_started=datetime.fromtimestamp(start_time).isoformat(),
            execution_finished=datetime.fromtimestamp(end_time).isoformat(),
            total_duration_seconds=total_duration,
            total_tasks=total_tasks,
            successful_tasks=successful_tasks,
            failed_tasks=failed_tasks,
            skipped_tasks=skipped_tasks,
            success_rate=success_rate,
            average_duration_seconds=avg_duration,
            task_results=results,
            errors=errors
        )


# ============================================
# 便捷函数
# ============================================

def load_plan(plan_path: str) -> ExecutionPlan:
    """
    从 JSON 文件加载执行计划

    Args:
        plan_path: JSON 文件路径

    Returns:
        ExecutionPlan: 执行计划对象
    """
    with open(plan_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 转换 batches
    batches = []
    for batch_data in data.get("batches", []):
        tasks = [
            TaskDefinition(**task_data)
            for task_data in batch_data.get("tasks", [])
        ]
        batches.append(BatchDefinition(
            batch_id=batch_data["batch_id"],
            batch_name=batch_data["batch_name"],
            description=batch_data.get("description"),
            tasks=tasks
        ))

    return ExecutionPlan(
        plan_id=data["plan_id"],
        project_name=data["project_name"],
        batches=batches,
        total_tasks=data["total_tasks"],
        total_batches=data["total_batches"],
        created_at=data.get("created_at"),
        config=data.get("config")
    )


def save_report(report: ExecutionReport, output_path: str) -> None:
    """
    保存执行报告到 JSON 文件

    Args:
        report: 执行报告
        output_path: 输出文件路径
    """
    # 确保输出目录存在
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # 转换为可序列化的字典
    report_dict = asdict(report)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report_dict, f, indent=2, ensure_ascii=False)

    logger.info(f"执行报告已保存: {output_path}")


def execute_plan(
    plan_path: str,
    adapter: SkillAdapter,
    max_workers: int = 4,
    enable_dependency_analysis: bool = True,
    save_report_to: Optional[str] = None
) -> ExecutionReport:
    """
    一行代码执行计划 (便捷函数)

    Args:
        plan_path: JSON 执行计划路径
        adapter: 技能包适配器实例
        max_workers: 最大并发线程数
        enable_dependency_analysis: 是否启用依赖分析
        save_report_to: 报告保存路径 (可选)

    Returns:
        ExecutionReport: 执行报告
    """
    # 加载计划
    plan = load_plan(plan_path)

    # 创建执行器
    executor = UniversalConcurrentExecutor(
        adapter=adapter,
        max_workers=max_workers,
        enable_dependency_analysis=enable_dependency_analysis
    )

    # 执行计划
    report = executor.execute_plan(plan)

    # 保存报告
    if save_report_to:
        save_report(report, save_report_to)

    return report


def analyze_concurrency_feasibility(
    tasks: List[Union[Dict[str, Any], TaskDefinition]],
    default_task_duration: float = 10.0,
    default_task_memory_gb: float = 0.5
) -> ConcurrencyAnalysis:
    """
    并发可行性分析 (前置环节)

    在生成执行计划之前,分析任务的并发潜力,避免盲目并发导致资源浪费或依赖冲突。

    Args:
        tasks: 任务列表,可以是字典或TaskDefinition对象
        default_task_duration: 默认任务耗时(秒),用于预估
        default_task_memory_gb: 默认任务内存占用(GB),用于预估

    Returns:
        ConcurrencyAnalysis: 并发可行性分析报告

    示例:
        >>> tasks = [
        ...     {"id": "task1", "type": "text-to-image", "params": {...}},
        ...     {"id": "task2", "type": "text-to-image", "params": {...}},
        ...     {"id": "task3", "type": "image-to-video",
        ...      "params": {"source": "task1"}, "depends_on": ["task1"]},
        ... ]
        >>> analysis = analyze_concurrency_feasibility(tasks)
        >>> print(f"推荐并发度: {analysis.recommended_workers}")
        >>> print(f"并行化比率: {analysis.parallelization_ratio:.2%}")
    """

    # 1. 转换为 TaskDefinition 对象
    task_definitions = []
    for task in tasks:
        if isinstance(task, TaskDefinition):
            task_definitions.append(task)
        elif isinstance(task, dict):
            task_definitions.append(TaskDefinition(
                task_id=task.get("id", task.get("task_id", f"task_{len(task_definitions)}")),
                params=task.get("params", {}),
                depends_on=task.get("depends_on"),
                metadata=task.get("metadata")
            ))
        else:
            raise ValueError(f"不支持的任务类型: {type(task)}")

    total_tasks = len(task_definitions)

    # 2. 依赖分析
    dependency_graph = DependencyAnalyzer.analyze_dependencies(task_definitions)

    # 计算独立任务数(无依赖的任务)
    independent_tasks = sum(1 for deps in dependency_graph.values() if not deps)
    dependent_tasks = total_tasks - independent_tasks

    # 3. 拓扑排序生成执行层
    execution_layers_raw = DependencyAnalyzer.get_execution_order(task_definitions)

    # 转换为 ExecutionLayer 对象
    execution_layers = []
    for idx, layer in enumerate(execution_layers_raw):
        layer_task_ids = [task.task_id for task in layer]
        can_parallel = len(layer) > 1
        estimated_duration = default_task_duration if can_parallel else default_task_duration * len(layer)

        execution_layers.append(ExecutionLayer(
            layer=idx,
            tasks=layer_task_ids,
            can_parallel=can_parallel,
            estimated_duration=estimated_duration
        ))

    # 4. 推荐并发度
    # 基础并发度:根据任务类型和CPU核心数
    cpu_count = os.cpu_count() or 4

    # 检测任务类型(从第一个任务的params推断)
    task_type = "io-intensive"  # 默认IO密集型(如API调用)
    if task_definitions:
        first_task_type = task_definitions[0].params.get("task_type", "")
        if "process" in first_task_type.lower() or "compute" in first_task_type.lower():
            task_type = "cpu-intensive"

    # 并发度推荐
    if task_type == "io-intensive":
        base_workers = min(cpu_count * 2, 8)
    else:
        base_workers = cpu_count

    # 考虑任务独立性
    if independent_tasks < 4:
        recommended_workers = min(base_workers, independent_tasks)
    else:
        recommended_workers = base_workers

    # 5. 计算并行化比率
    # 并行化比率 = 可并行任务数 / 总任务数
    parallelizable_tasks = sum(len(layer.tasks) for layer in execution_layers if layer.can_parallel)
    parallelization_ratio = parallelizable_tasks / total_tasks if total_tasks > 0 else 0.0

    # 6. 生成建议
    recommendations = []

    if parallelization_ratio < 0.3:
        recommendations.append("⚠️  任务依赖度高,并发收益低(<30%),建议优化任务设计或考虑串行执行")
    elif parallelization_ratio >= 0.8:
        recommendations.append(f"✅ 任务高度独立(≥80%),建议并发度{recommended_workers}-{recommended_workers + 2}")
        time_saved_percent = int((1 - 1/recommended_workers) * 100)
        recommendations.append(f"📈 预计可节省{time_saved_percent}%执行时间")
    else:
        recommendations.append(f"⚡ 任务部分独立({parallelization_ratio:.0%}),建议并发度{recommended_workers}")

    # 层级建议
    if len(execution_layers) > 1:
        for layer in execution_layers:
            if layer.can_parallel and len(layer.tasks) > 1:
                recommendations.append(
                    f"🔄 第{layer.layer}层包含{len(layer.tasks)}个独立任务,可完全并行"
                )
            elif not layer.can_parallel or len(layer.tasks) == 1:
                task_ids_str = ", ".join(layer.tasks[:3])
                if len(layer.tasks) > 3:
                    task_ids_str += f"... (共{len(layer.tasks)}个)"
                recommendations.append(
                    f"⚙️  第{layer.layer}层任务需串行执行: {task_ids_str}"
                )

    # 依赖关系建议
    dep_tasks = [task_id for task_id, deps in dependency_graph.items() if deps]
    if dep_tasks:
        recommendations.append(
            f"🔗 {len(dep_tasks)}个任务存在依赖关系,执行顺序受限"
        )

    # 7. 资源预估
    estimated_memory_gb = default_task_memory_gb * recommended_workers
    estimated_duration = sum(layer.estimated_duration for layer in execution_layers)

    # 内存检查
    if estimated_memory_gb > 4.0:
        recommendations.append(
            f"⚠️  预估内存占用{estimated_memory_gb:.1f}GB,请确保系统资源充足"
        )

    return ConcurrencyAnalysis(
        total_tasks=total_tasks,
        independent_tasks=independent_tasks,
        dependent_tasks=dependent_tasks,
        execution_layers=execution_layers,
        recommended_workers=recommended_workers,
        parallelization_ratio=parallelization_ratio,
        recommendations=recommendations,
        estimated_memory_gb=estimated_memory_gb,
        estimated_duration=estimated_duration
    )
