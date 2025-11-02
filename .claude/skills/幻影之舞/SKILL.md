---
name: universal-concurrent-executor
description: Universal concurrent execution engine for ALL skills (AIGC, data processing, web scraping, automation, etc.). Provides intelligent dependency analysis, layered concurrent scheduling, progress tracking, and robust error handling. Automatically parallelizes independent tasks while respecting dependencies.
---
# 幻影之舞 - 通用并发执行引擎（Universal Concurrent Executor）

> **核心理念**: 一次编写,处处复用。为**所有技能包**(AIGC、数据处理、网页爬虫、自动化等)提供标准化的并发执行能力。

## 🎯 Quick Start

### 基础使用 (Nano-Banana)

```python
from .claude.skills.幻影之舞.universal_concurrent_executor.core import execute_plan
from .claude.skills.幻影之舞.universal_concurrent_executor.adapters import NanoBananaAdapter

# 创建适配器
adapter = NanoBananaAdapter()

# 一行代码执行计划
report = execute_plan(
    plan_path="output/项目名/nano-banana/plans/execution_plan.json",
    adapter=adapter,
    max_workers=4,
    enable_dependency_analysis=True
)

print(f"✅ 成功: {report.successful_tasks}/{report.total_tasks}")
print(f"⏱️  总耗时: {report.total_duration_seconds:.2f}s")
```

### 基础使用 (MiniMax)

```python
from .claude.skills.幻影之舞.universal_concurrent_executor.core import execute_plan
from .claude.skills.幻影之舞.universal_concurrent_executor.adapters import MinimaxAdapter

# 创建适配器
adapter = MinimaxAdapter()

# 一行代码执行计划
report = execute_plan(
    plan_path="output/项目名/minimax/plans/execution_plan.json",
    adapter=adapter,
    max_workers=4
)

print(f"✅ 成功: {report.successful_tasks}/{report.total_tasks}")
```

## 🔍 并发可行性分析 (前置环节)

> **为什么需要**: 在生成执行计划之前,先分析任务需求的并发潜力,避免盲目并发导致资源浪费或依赖冲突。

### 分析目标

✅ **识别独立任务**
- 分析哪些任务之间没有因果依赖关系
- 标识可以完全并行执行的任务组
- 检测潜在的隐式依赖(如文件路径引用)

✅ **评估并发度**
- 根据任务类型(CPU密集/IO密集)推荐并发线程数
- 考虑API限流和系统资源限制
- 平衡性能与稳定性

✅ **制定并行策略**
- 生成任务执行层次图(拓扑排序)
- 规划批次划分方案
- 预估执行时间和资源消耗

### 使用方式

```python
from .claude.skills.幻影之舞.scripts.core import analyze_concurrency_feasibility

# 分析原始任务需求
analysis = analyze_concurrency_feasibility(
    tasks=[
        {"id": "task1", "type": "text-to-image", "params": {...}},
        {"id": "task2", "type": "text-to-image", "params": {...}},
        {"id": "task3", "type": "image-to-video", "params": {"source": "task1"}},
    ]
)

# 查看分析结果
print(f"可并发任务组: {analysis.independent_groups}")
print(f"推荐并发度: {analysis.recommended_workers}")
print(f"执行层次: {analysis.execution_layers}")
print(f"预估耗时: {analysis.estimated_duration}秒")
```

### 分析输出

```json
{
  "total_tasks": 20,
  "independent_tasks": 17,
  "dependent_tasks": 3,
  "execution_layers": [
    {
      "layer": 0,
      "tasks": ["task1", "task2", ...],
      "can_parallel": true,
      "estimated_duration": 10.5
    },
    {
      "layer": 1,
      "tasks": ["task3"],
      "can_parallel": false,
      "estimated_duration": 8.0
    }
  ],
  "recommended_workers": 4,
  "parallelization_ratio": 0.85,
  "recommendations": [
    "任务高度独立,建议并发度4-6",
    "第0层可完全并行,预计节省70%时间",
    "task3依赖task1,需串行执行"
  ]
}
```

### 分析策略

#### 1. 依赖关系检测

```python
# 显式依赖
if "depends_on" in task:
    # 标记为依赖任务
    add_dependency(task, task["depends_on"])

# 隐式依赖(文件路径引用)
for param_value in task["params"].values():
    if isinstance(param_value, str) and "output/" in param_value:
        # 自动检测文件路径依赖
        source_task = extract_task_id_from_path(param_value)
        add_dependency(task, source_task)
```

#### 2. 并发度推荐

```python
# 根据任务类型推荐
if task_type == "text-to-image":  # IO密集型
    base_workers = os.cpu_count() * 2
elif task_type == "image-processing":  # CPU密集型
    base_workers = os.cpu_count()

# 考虑API限流
if has_api_rate_limit:
    max_workers = min(base_workers, api_rate_limit_per_second * 2)

# 考虑内存限制
available_memory_gb = get_available_memory()
task_memory_gb = estimate_task_memory(task)
max_workers = min(max_workers, available_memory_gb // task_memory_gb)
```

#### 3. 批次划分策略

```python
# 按业务逻辑分组
if "category" in task:
    batch_by_category(tasks)

# 按执行层次分组
for layer in execution_layers:
    batches.append({
        "batch_id": f"L{layer.id}",
        "tasks": layer.tasks,
        "can_parallel": layer.can_parallel
    })

# 动态批次大小(避免单批过大)
if len(layer.tasks) > 10:
    split_into_sub_batches(layer.tasks, batch_size=5)
```

### 最佳实践

✅ **先分析再执行**
```python
# 1. 并发可行性分析
analysis = analyze_concurrency_feasibility(raw_tasks)

# 2. 根据分析结果生成执行计划
plan = generate_execution_plan(
    tasks=raw_tasks,
    max_workers=analysis.recommended_workers,
    batches=analysis.execution_layers
)

# 3. 执行计划
report = execute_plan(plan, adapter)
```

✅ **动态调整策略**
```python
# 根据实时性能调整
if analysis.parallelization_ratio < 0.3:
    print("⚠️  任务依赖度高,并发收益低,考虑串行执行")
elif analysis.parallelization_ratio > 0.8:
    print("✅ 任务高度独立,可充分并发")
    max_workers = analysis.recommended_workers
```

✅ **预估资源消耗**
```python
# 检查资源充足性
if analysis.estimated_memory_gb > available_memory_gb:
    print("⚠️  内存不足,降低并发度")
    max_workers = max(1, max_workers // 2)

if analysis.estimated_duration > timeout_seconds:
    print("⚠️  预计超时,考虑增加并发度")
    max_workers = min(max_workers * 2, os.cpu_count() * 4)
```

## 📐 核心架构

### 三层设计

```
┌────────────────────────────────────────────────────────┐
│              Skill-Specific Adapters                   │
│  (Nano-Banana, MiniMax, Future Skills)                 │
│  • execute_task() - 调用特定 API                        │
│  • validate_params() - 验证参数                         │
│  • pre/post hooks - 自定义逻辑                          │
└──────────────────┬─────────────────────────────────────┘
                   │
┌──────────────────▼─────────────────────────────────────┐
│           Universal Concurrent Core                    │
│  • TaskDefinition, ExecutionPlan - 通用数据类           │
│  • DependencyAnalyzer - 智能依赖分析                    │
│  • UniversalConcurrentExecutor - 并发引擎               │
│  • ThreadPoolExecutor - 线程池管理                      │
└────────────────────────────────────────────────────────┘
```

### 核心特性

✅ **智能依赖分析**

- 显式依赖: 通过 `depends_on` 字段指定
- 隐式依赖: 自动检测文件路径引用(如视频任务依赖图片任务)

✅ **分层并发执行**

- 拓扑排序生成执行层
- 同层任务并发执行(ThreadPoolExecutor)
- 跨层任务串行执行(保证依赖顺序)

✅ **健壮错误处理**

- 单任务失败不影响其他任务
- 详细错误日志和追踪
- 自动跳过依赖失败的任务

✅ **详细执行报告**

- JSON 格式报告
- 包含每个任务的状态、耗时、输出
- 成功率统计和性能分析

## 🔌 适配器接口

### 创建新适配器

```python
from .claude.skills.幻影之舞.universal_concurrent_executor.core import (
    SkillAdapter, TaskDefinition, TaskResult
)

class YourSkillAdapter(SkillAdapter):
    """你的技能包适配器"""

    def execute_task(self, task: TaskDefinition) -> TaskResult:
        """
        执行单个任务 (必须实现)

        Args:
            task: 任务定义,包含所有参数

        Returns:
            TaskResult: 执行结果
        """
        # 1. 解析任务参数
        params = task.params

        # 2. 调用你的 API/工具
        result = your_api_call(**params)

        # 3. 包装为 TaskResult
        return TaskResult(
            task_id=task.task_id,
            status="success" if result.success else "failed",
            output_files=[result.output_path],
            api_response=result.data
        )

    def validate_params(self, params: Dict[str, Any]) -> bool:
        """验证参数 (可选覆盖)"""
        required = ["param1", "param2"]
        return all(key in params for key in required)

    def pre_execute_hook(self, task: TaskDefinition) -> None:
        """执行前钩子 (可选覆盖)"""
        print(f"准备执行任务: {task.task_id}")

    def post_execute_hook(self, task: TaskDefinition, result: TaskResult) -> None:
        """执行后钩子 (可选覆盖)"""
        print(f"任务完成: {task.task_id}, 状态: {result.status}")
```

### 使用你的适配器

```python
from .claude.skills.幻影之舞.universal_concurrent_executor.core import execute_plan

adapter = YourSkillAdapter()
report = execute_plan("plan.json", adapter, max_workers=4)
```

## 📋 执行计划 JSON 结构

### 通用结构

```json
{
  "plan_id": "plan_YYYYMMDD_001",
  "project_name": "项目名称",
  "created_at": "2025-10-31T10:00:00",
  "total_tasks": 20,
  "total_batches": 10,
  "config": {
    "max_workers": 4,
    "enable_dependency_analysis": true
  },
  "batches": [
    {
      "batch_id": "B01",
      "batch_name": "批次名称",
      "tasks": [
        {
          "task_id": "01-A-任务名",
          "params": {
            "param1": "value1",
            "param2": "value2"
          },
          "depends_on": null,
          "metadata": {}
        }
      ]
    }
  ]
}
```

### Nano-Banana 特定字段

```json
{
  "task_id": "01-A-包子非点击态",
  "params": {
    "task_type": "text-to-image",
    "user_prompt": "中餐菜品Icon设计...",
    "context": "餐饮行业APP",
    "target_style": "中国动漫风格",
    "config": {
      "aspect_ratio": "1:1"
    }
  }
}
```

### MiniMax 特定字段

```json
{
  "task_id": "01-A-生成海报",
  "params": {
    "task_type": "text_to_image",
    "api_params": {
      "model": "image-01",
      "prompt": "火锅店开业海报...",
      "aspect_ratio": "1:1",
      "n": 1,
      "prompt_optimizer": true
    },
    "use_prompt_optimizer": true,
    "prompt_optimizer_params": {
      "design_type": "poster",
      "restaurant_type": "hotpot"
    }
  }
}
```

## 🚀 性能优化

### 自动并发度调优

```python
# 根据 CPU 核心数自动设置
import os
max_workers = min(os.cpu_count() * 2, 8)

report = execute_plan(
    plan_path="plan.json",
    adapter=adapter,
    max_workers=max_workers  # 自动优化
)
```

### 依赖分析优化

```python
# 关闭依赖分析(如果任务完全独立)
report = execute_plan(
    plan_path="plan.json",
    adapter=adapter,
    enable_dependency_analysis=False  # 提升性能
)
```

## 📊 执行报告

### 报告结构

```json
{
  "plan_id": "plan_20251031_001",
  "project_name": "中餐菜品Icon设计",
  "execution_started": "2025-10-31T03:01:17",
  "execution_finished": "2025-10-31T03:02:08",
  "total_duration_seconds": 51.92,
  "total_tasks": 20,
  "successful_tasks": 20,
  "failed_tasks": 0,
  "skipped_tasks": 0,
  "success_rate": 100.0,
  "average_duration_seconds": 2.60,
  "task_results": [
    {
      "task_id": "01-A-包子非点击态",
      "batch_id": "B01",
      "status": "success",
      "start_time": "2025-10-31T03:01:17",
      "end_time": "2025-10-31T03:01:26",
      "duration_seconds": 9.0,
      "result": {
        "output_path": "output/.../image.png"
      }
    }
  ],
  "errors": []
}
```

### 报告使用

```python
report = execute_plan(...)

# 访问统计信息
print(f"成功率: {report.success_rate}%")
print(f"平均耗时: {report.average_duration_seconds}s")

# 查找失败任务
failed = [r for r in report.task_results if r.status == "failed"]
for task in failed:
    print(f"失败任务: {task.task_id}, 错误: {task.error}")
```

## 🛠️ 最佳实践

### 1. 合理设置并发数

```python
# CPU 密集型任务
max_workers = os.cpu_count()

# IO 密集型任务 (API 调用)
max_workers = os.cpu_count() * 2

# 限制最大并发(避免API限流)
max_workers = min(os.cpu_count() * 2, 4)
```

### 2. 使用批次组织任务

```python
# 按业务逻辑分批
batches = [
    {"batch_id": "B01", "batch_name": "包子类", "tasks": [...]},
    {"batch_id": "B02", "batch_name": "烧麦类", "tasks": [...]},
]
```

### 3. 利用依赖分析

```python
# 显式依赖
{
  "task_id": "video-task",
  "depends_on": ["image-task"],  # 视频依赖图片
  "params": {
    "first_frame_image": "output/image-task/result.png"
  }
}

# 隐式依赖会自动检测
# video-task 自动等待 image-task 完成
```

### 4. 错误处理

```python
report = execute_plan(...)

if report.failed_tasks > 0:
    # 保存失败任务列表
    failed_ids = [r.task_id for r in report.task_results if r.status == "failed"]

    # 生成重试计划
    retry_plan = create_retry_plan(original_plan, failed_ids)

    # 重试失败任务
    retry_report = execute_plan(retry_plan, adapter)
```

## 📚 扩展阅读

- **架构分析**: `reports/并发执行器架构分析-通用vs专属-20251031.md`
- **适配器开发指南**: `.claude/skills/幻影之舞/universal-concurrent-executor/ADAPTER_DEVELOPMENT_GUIDE.md`
- **Nano-Banana 集成示例**: `plugins/创意组/skills/AIGC/nano-banana/`
- **MiniMax 集成示例**: `plugins/创意组/skills/AIGC/minimax/`

## 🔄 版本历史

- **v1.1.0** (2025-11-01): 新增并发可行性分析前置环节
  - ✨ 新增 `analyze_concurrency_feasibility()` API
  - 🔍 智能识别独立任务和依赖关系
  - 📊 自动评估并发度和资源消耗
  - 🎯 生成执行层次图和批次划分方案
  - 💡 提供并行化策略建议

- **v1.0.0** (2025-10-31): 初始版本
  - 通用执行器核心
  - Nano-Banana 适配器
  - MiniMax 适配器
  - 智能依赖分析
  - 分层并发执行

## 🤝 贡献

创建新适配器时,请参考 `ADAPTER_DEVELOPMENT_GUIDE.md` 中的模板和最佳实践。

---

**作者**: ZTL Digital Intelligence Operations Center - 幻影之舞团队
**许可**: MIT License
