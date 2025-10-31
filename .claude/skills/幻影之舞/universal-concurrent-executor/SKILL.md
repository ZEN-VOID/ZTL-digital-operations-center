---
name: universal-concurrent-executor
description: Universal concurrent execution engine for ALL skills (AIGC, data processing, web scraping, automation, etc.). Provides intelligent dependency analysis, layered concurrent scheduling, progress tracking, and robust error handling. Automatically parallelizes independent tasks while respecting dependencies.
---

# Universal Concurrent Executor - 通用并发执行引擎

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
