---
name: 剑刃风暴-多线程执行器
description: 智能任务分割 + 并行Worker执行 + 自动结果汇总 - 突破200K token限制,实现超长任务无限制执行
version: 1.0.0
category: task-orchestration
tags: [multi-threading, parallel-execution, task-splitting, worker-pool, context-management]
author: Claude Code + ZTL Team
created: 2025-11-01
allowed-tools: [Bash, Read, Write, Task]
---

# 剑刃风暴 - 多线程执行器 (Blade Storm Multi-Threading Executor)

> "当单一上下文无法容纳时,剑刃风暴将任务分割为千万碎片,并行斩落"

## 📋 Quick Start

### 场景1: 自动触发(PreCompact Hook)

```yaml
用户请求: "帮我完成一个超长的数据分析任务"

系统行为:
  1. 任务执行,消耗token
  2. 达到180K → 触发PreCompact
  3. 剑刃风暴自动启动:
     - TaskSplitter分析并分割任务
     - Worker启动器创建多个Worker实例
     - ResultAggregator监控并汇总结果
  4. 主窗口compact完成后继续工作
  5. 最终在主窗口展示完整报告

用户体验: 完全无感知,任务自动完成
```

### 场景2: 手动触发(显式调用)

```python
# 方式1: 通过TaskSplitter手动分割
from task_splitter import TaskSplitter

splitter = TaskSplitter(project_name="美团数据分析")
subtasks = splitter.analyze_and_split(
    context="当前上下文...",
    task_description="分析全年门店营业数据"
)
splitter.save_subtasks(subtasks)

# 方式2: 通过Bash启动Worker
Bash("bash .claude/skills/剑刃风暴/multi-threading-executor/scripts/launch_workers.sh 美团数据分析")

# 方式3: 通过ResultAggregator监控
Bash("python3 .claude/skills/剑刃风暴/multi-threading-executor/scripts/result_aggregator.py 美团数据分析 --monitor")
```

## 🎯 Core Features

### 1. 智能任务分割 (TaskSplitter)

**核心能力**:
- ✅ 自动识别任务类型(数据分析、内容生成、调研、开发)
- ✅ 应用专业分割策略
- ✅ 生成结构化子任务配置(JSON)
- ✅ 支持任务依赖关系管理
- ✅ 自动估算执行时间

**支持的任务类型**:

| 任务类型 | 典型流程 | 子任务数 |
|---------|---------|---------|
| **数据分析** | 采集 → 清洗 → 分析 → 报告 | 4 |
| **内容生成** | 需求分析 → 创作 → 审核优化 | 3 |
| **调研任务** | 信息收集 → 整理 → 分析 → 报告 | 4 |
| **开发任务** | 需求 → 设计 → 编码 → 测试 | 4 |
| **通用任务** | 自定义N阶段 | 可配置 |

**子任务数据结构**:
```json
{
  "task_id": "T1",
  "description": "数据采集",
  "dependencies": [],
  "status": "pending",
  "input_data": {
    "source": "meituan_api"
  },
  "execution_plan": "调用API采集数据...",
  "output_path": "output/项目名/results/T1-result.json",
  "created_at": "2025-11-01T10:00:00Z",
  "estimated_duration": 300
}
```

### 2. Worker启动器 (launch_workers.sh)

**核心能力**:
- ✅ 扫描任务队列,识别待执行任务
- ✅ 检查任务依赖,确保执行顺序
- ✅ 创建新iTerm窗口,启动Claude实例
- ✅ 注入任务配置到Worker窗口
- ✅ 并发控制(最多N个Worker同时运行)
- ✅ 自动更新任务状态

**工作流程**:
```
1. 扫描 output/{项目名}/task-queue/*.json
   ↓
2. 过滤 status=pending 的任务
   ↓
3. 检查依赖关系(dependencies已完成)
   ↓
4. 启动Worker实例(最多MAX_WORKERS个)
   ↓
5. 使用深渊凝视创建新iTerm窗口
   ↓
6. 发送任务提示到Worker窗口
   ↓
7. 更新任务状态: pending → running
```

**配置参数**:
```bash
MAX_WORKERS=3              # 最大并发Worker数
WORKER_STARTUP_DELAY=5     # Worker启动间隔(秒)
CLAUDE_INIT_DELAY=20       # Claude初始化等待(秒)
```

### 3. 结果汇总器 (ResultAggregator)

**核心能力**:
- ✅ 持续监控任务队列
- ✅ 收集已完成任务的结果文件
- ✅ 按依赖关系拓扑排序
- ✅ 整合为完整Markdown报告
- ✅ 生成执行摘要和统计信息
- ✅ 自动识别失败任务并汇总错误

**监控机制**:
```python
while not all_tasks_completed():
    sleep(10)  # 每10秒检查一次

    # 扫描results/目录
    for task in tasks:
        if task.status == 'completed':
            result = load_result(task.output_path)
            collected_results[task.task_id] = result

# 生成最终报告
report = generate_report(tasks, collected_results)
save_report("output/{项目名}/final-report.md")
```

**报告格式**:
```markdown
# 任务执行总报告

**项目名称**: 美团数据分析
**总任务数**: 4
**已完成**: 4/4
**总执行时间**: 1020秒 (17分钟)

## 详细结果

### 阶段1: 数据采集 (T1)
- 执行时间: 2025-11-01 10:05:00
- 采集记录: 1000条
- 输出文件: output/.../T1-raw-data.csv

### 阶段2: 数据清洗 (T2)
...
```

### 4. PreCompact Hook集成

**自动触发机制**:
```
Context达到180K
  ↓
PreCompact Hook触发
  ↓
保存上下文快照
  ↓
调用TaskSplitter分割任务
  ↓
调用Worker启动器创建Worker
  ↓
启动ResultAggregator监控
  ↓
原窗口compact继续执行
```

**Hook版本对比**:

| 版本 | 功能 | 优势 |
|------|------|------|
| v2.0 | 启动单个并行Claude | 简单,保留上下文 |
| **v3.0** | 智能分割 + 多Worker | 突破token限制 ⭐ |

## 📚 API Reference

### TaskSplitter

```python
class TaskSplitter:
    def __init__(self, project_name: str):
        """初始化任务分割器"""

    def analyze_and_split(
        self,
        context: str,
        task_description: str,
        max_subtasks: int = 10
    ) -> List[SubTask]:
        """分析上下文并智能分割任务"""

    def save_subtasks(self, subtasks: List[SubTask]) -> List[Path]:
        """保存子任务到task-queue目录"""

    def load_all_tasks(self) -> List[SubTask]:
        """加载所有任务"""

    def update_task_status(
        self,
        task_id: str,
        status: str,
        worker_window_index: Optional[int] = None
    ):
        """更新任务状态"""
```

### ResultAggregator

```python
class ResultAggregator:
    def __init__(self, project_name: str):
        """初始化结果汇总器"""

    def monitor_and_aggregate(
        self,
        check_interval: int = 10,
        max_wait_time: int = 3600
    ) -> str:
        """持续监控并生成最终报告"""

    def generate_summary_report(self) -> Dict[str, Any]:
        """生成JSON格式摘要报告"""
```

### Worker启动器

```bash
# 命令行调用
bash launch_workers.sh <project_name>

# 配置环境变量
export MAX_WORKERS=5
export WORKER_STARTUP_DELAY=10
export CLAUDE_INIT_DELAY=30

bash launch_workers.sh 美团数据分析
```

## 🎨 Usage Examples

### 示例1: 数据分析任务(自动触发)

```yaml
用户请求: "分析过去一年所有门店的营业数据,生成详细报告"

系统行为:
  1. 任务开始执行,逐步消耗token
  2. 达到180K → PreCompact Hook触发
  3. TaskSplitter分割为4个子任务:
     - T1: 采集Q1-Q4数据
     - T2: 数据清洗
     - T3: 统计分析
     - T4: 生成报告
  4. Worker启动器创建3个Worker并行执行T1-T3
  5. T4等待T3完成后执行
  6. ResultAggregator汇总所有结果
  7. 主窗口展示最终报告

最终输出: output/营业数据分析/final-report.md
```

### 示例2: 内容生成任务(手动触发)

```python
# Step 1: 手动分割任务
from task_splitter import TaskSplitter

splitter = TaskSplitter(project_name="火锅店开业海报")
subtasks = splitter.analyze_and_split(
    context="需要为火锅店开业设计海报...",
    task_description="设计10张不同风格的开业海报"
)
splitter.save_subtasks(subtasks)

# Step 2: 启动Worker
Bash("bash .claude/skills/剑刃风暴/multi-threading-executor/scripts/launch_workers.sh 火锅店开业海报")

# Step 3: 监控结果
Bash("python3 .claude/skills/剑刃风暴/multi-threading-executor/scripts/result_aggregator.py 火锅店开业海报 --monitor")
```

### 示例3: 开发任务(完整流程)

```python
# 场景: 实现一个复杂的用户认证系统

# Step 1: 创建任务分割器
splitter = TaskSplitter(project_name="用户认证系统开发")

# Step 2: 分割任务
subtasks = splitter.analyze_and_split(
    context="当前项目需要实现用户认证...",
    task_description="实现完整的用户认证系统,包括注册、登录、JWT、权限管理"
)

# Step 3: 保存任务
splitter.save_subtasks(subtasks)

# Step 4: 启动Worker(自动处理依赖)
Bash("bash .claude/skills/剑刃风暴/multi-threading-executor/scripts/launch_workers.sh 用户认证系统开发")

# Step 5: 等待完成并查看报告
# ResultAggregator会自动生成:
# output/用户认证系统开发/final-report.md
```

## ⚙️ Configuration

### 目录结构

```
output/
└── [项目名]/
    ├── task-queue/          # 任务队列
    │   ├── task-T1.json
    │   ├── task-T2.json
    │   └── task-T3.json
    ├── results/             # 结果输出
    │   ├── T1-result.json
    │   ├── T2-result.json
    │   └── T3-result.json
    ├── project-info.json    # 项目元数据
    └── final-report.md      # 最终报告
```

### 环境变量配置

```bash
# Worker启动器配置
export MAX_WORKERS=3
export WORKER_STARTUP_DELAY=5
export CLAUDE_INIT_DELAY=20

# 调试模式
export DEBUG=true
```

### Hook配置

```bash
# 启用v3.0 Hook
mv .claude/hooks/parallel-claude-after-compact.sh \
   .claude/hooks/parallel-claude-after-compact-v2.sh.bak

cp .claude/hooks/parallel-claude-after-compact-v3.sh \
   .claude/hooks/parallel-claude-after-compact.sh

chmod +x .claude/hooks/parallel-claude-after-compact.sh
```

## ⚠️ Important Notes

### 使用场景

**✅ 适用**:
- 超长任务(预计超过200K token)
- 可分割的复杂任务
- 需要并行处理的多阶段任务
- 数据分析、内容生成、调研、开发等

**❌ 不适用**:
- 简单快速任务(< 50K token)
- 高度依赖上下文连续性的任务
- 需要实时交互的任务

### 性能考虑

| 维度 | 建议 |
|------|------|
| **MAX_WORKERS** | 3-5个(取决于机器性能) |
| **任务粒度** | 每个子任务200-500秒 |
| **依赖深度** | 最多3-4层依赖 |
| **监控间隔** | 10-30秒 |

### Worker任务规范

Worker必须严格按照以下规范工作:

1. **读取任务配置**: 从task-queue/task-{id}.json读取
2. **执行任务**: 按execution_plan执行
3. **保存结果**: 写入results/{id}-result.json
4. **更新状态**: 更新task-queue/task-{id}.json的status字段

**结果文件格式**:
```json
{
  "task_id": "T1",
  "status": "completed",
  "execution_time": "2025-11-01T10:05:00Z",
  "duration_seconds": 300,
  "output_data": {
    "records_count": 1000,
    "data_file": "output/.../data.csv"
  },
  "summary": "成功完成任务",
  "errors": [],
  "warnings": [],
  "next_steps": []
}
```

### 故障排查

**问题1: Worker未启动**
```bash
# 检查深渊凝视是否可用
python3 .claude/skills/深渊凝视/scripts/abyss_gaze.py list_windows

# 检查日志
tail -f .claude/logs/launch-workers.log
```

**问题2: 任务未执行**
```bash
# 检查任务状态
cat output/{项目名}/task-queue/task-T1.json | jq '.status'

# 检查依赖关系
cat output/{项目名}/task-queue/task-T1.json | jq '.dependencies'
```

**问题3: 结果未汇总**
```bash
# 检查结果文件是否存在
ls output/{项目名}/results/

# 手动触发汇总
python3 .claude/skills/剑刃风暴/multi-threading-executor/scripts/result_aggregator.py {项目名}
```

## 🔗 Related Resources

### 内部文档
- [深渊凝视 Skill](.claude/skills/深渊凝视/SKILL.md) - iTerm控制
- [PreCompact Hook](../../hooks/README.md) - Hook系统文档
- [设计报告](../../../../reports/multi-threading-analysis-20251101.md)
- [反馈机制分析](../../../../reports/worker-feedback-mechanism-analysis.md)

### 组件文档
- [task_splitter.py](scripts/task_splitter.py) - 任务分割器源码
- [result_aggregator.py](scripts/result_aggregator.py) - 结果汇总器源码
- [launch_workers.sh](scripts/launch_workers.sh) - Worker启动器源码

## 📝 Changelog

### v1.0.0 (2025-11-01)
- ✅ 初始版本发布
- ✅ TaskSplitter智能任务分割
- ✅ Worker启动器并行执行
- ✅ ResultAggregator自动汇总
- ✅ PreCompact Hook v3.0集成
- ✅ 完整的错误处理和日志
- ✅ 支持4种任务类型专业分割策略

---

**Skill Category**: Task Orchestration & Parallel Execution
**Maintenance**: Active
**Status**: Production Ready ✅
**代号**: 剑刃风暴 (Blade Storm)
