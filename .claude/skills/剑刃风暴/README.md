# 剑刃风暴 - 多线程执行器

> **版本**: 1.0.0 | **创建时间**: 2025-11-01

## 概述

剑刃风暴是突破Claude Code 200K token限制的智能任务分割与并行执行系统。

### 核心能力

- ✅ 智能任务分割(4种专业策略)
- ✅ 并行Worker执行(每个200K token)
- ✅ 自动结果汇总
- ✅ PreCompact Hook集成

## 快速开始

### 自动触发

上下文达到180K时自动启动,无需手动操作。

### 手动触发

```bash
# 1. 分割任务
python3 scripts/task_splitter.py "项目名" "任务描述"

# 2. 启动Worker
bash scripts/launch_workers.sh "项目名"

# 3. 监控结果
python3 scripts/result_aggregator.py "项目名" --monitor
```

## 目录结构

```
output/[项目名]/
├── task-queue/      # 任务配置
├── results/         # 执行结果
└── final-report.md  # 最终报告
```

## 配置

编辑 `config.yaml`:

```yaml
worker_launcher:
  max_workers: 3
  worker_startup_delay: 5
  claude_init_delay: 20
```

## 文档

- [SKILL.md](./SKILL.md) - 完整文档
- [设计报告](../../../../reports/multi-threading-analysis-20251101.md)
