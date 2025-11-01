# 行政组 Plugin

> 企业行政管理插件 - 从财务管理到人力资源的完整支持体系

[![Agents](https://img.shields.io/badge/agents-9-blue)](agents/)
[![Commands](https://img.shields.io/badge/commands-0-green)](commands/)
[![Skills](https://img.shields.io/badge/skills-0-orange)](skills/)

## 📋 概述

综合行政管理插件,涵盖财务、人力资源、法务、文档管理等企业运营支持职能。

本插件包含 **9个专业智能体**,0个斜杠命令,0个技能包,提供完整的业务流程支持。

## 🤖 智能体架构

### 组织结构

本组共有9个智能体:

1. **R0-办公业务需求分析员** - r0-admin-requirements-analyst
2. **R1-财务管理员** - r1-finance-planner
3. **R2-人事管理员** - r2-hr-planner
4. **R3-法务专家** - r3-legal-planner
5. **R4-秘书** - r4-secretary-planner
6. **R5-飞书管理员** - r5-feishu-planner
7. **R6-文件管理员** - r6-file-planner
8. **R7-存储管理员** - r7-storage-planner
9. **RR-行政组组长** - rr-admin-orchestrator

### 智能体详情

#### R0-办公业务需求分析员

**名称**: r0-admin-requirements-analyst

**何时使用**:
- Use this agent when users need to analyze administrative or office management requirements, break do

**调用方式**:
```python
Task(subagent_type="R0-办公业务需求分析员",
     prompt="您的任务描述")
```

---

#### R1-财务管理员

**名称**: r1-finance-planner

**何时使用**:
- Use this agent when you need professional financial planning and budgeting support for administrativ

**调用方式**:
```python
Task(subagent_type="R1-财务管理员",
     prompt="您的任务描述")
```

---

#### R2-人事管理员

**名称**: r2-hr-planner

**何时使用**:
- Use this agent when you need professional human resources planning and workforce management support 

**调用方式**:
```python
Task(subagent_type="R2-人事管理员",
     prompt="您的任务描述")
```

---

#### R3-法务专家

**名称**: r3-legal-planner

**何时使用**:
- Use this agent when you need professional legal planning and risk management support for administrat

**调用方式**:
```python
Task(subagent_type="R3-法务专家",
     prompt="您的任务描述")
```

---

#### R4-秘书

**名称**: r4-secretary-planner

**何时使用**:
- Use this agent when you need professional executive assistance and coordination planning support for

**调用方式**:
```python
Task(subagent_type="R4-秘书",
     prompt="您的任务描述")
```

---

#### R5-飞书管理员

**名称**: r5-feishu-planner

**何时使用**:
- Use this agent when you need professional Feishu platform coordination planning support for administ

**调用方式**:
```python
Task(subagent_type="R5-飞书管理员",
     prompt="您的任务描述")
```

---

#### R6-文件管理员

**名称**: r6-file-planner

**何时使用**:
- Use this agent when you need professional file and document management planning support for administ

**调用方式**:
```python
Task(subagent_type="R6-文件管理员",
     prompt="您的任务描述")
```

---

#### R7-存储管理员

**名称**: r7-storage-planner

**何时使用**:
- Use this agent when you need professional storage infrastructure planning and management support for

**调用方式**:
```python
Task(subagent_type="R7-存储管理员",
     prompt="您的任务描述")
```

---

#### RR-行政组组长

**名称**: rr-admin-orchestrator

**何时使用**:
- Use this agent when you need to manage administrative tasks across finance, HR, legal, secretarial, 

**调用方式**:
```python
Task(subagent_type="RR-行政组组长",
     prompt="您的任务描述")
```

---

## 🚀 使用指南

### 自动委派

Claude会根据您的需求自动选择合适的智能体:

```
用户: [描述您的需求]
→ Claude自动委派给相关智能体
```

### 显式调用

使用Task工具显式调用特定智能体:

```python
Task(subagent_type="智能体ID",
     prompt="详细任务描述")
```

### 多智能体协作

复杂任务可能需要多个智能体协同工作。组长智能体可以协调团队:

```python
Task(subagent_type="RR-行政组组长",
     prompt="需要团队协作的复杂任务")
```

## 📁 项目结构

```
plugins/行政组/
├── .claude-plugin/
│   └── plugin.json              # 插件配置
│
├── agents/                      # 9个智能体
│   ├── R0-办公业务需求分析员.md
│   ├── R1-财务管理员.md
│   ├── R2-人事管理员.md
│   ├── R3-法务专家.md
│   ├── R4-秘书.md
│   ├── R5-飞书管理员.md
│   ├── R6-文件管理员.md
│   ├── R7-存储管理员.md
│   ├── RR-行政组组长.md
│
├── commands/                    # 0个命令
│   └── README.md
│
├── skills/                      # 0个技能包
│   └── README.md
│
├── hooks/                       # 钩子配置
├── scripts/                     # 工具脚本
└── README.md                    # 本文件
```

## 🎯 最佳实践

### 智能体选择决策树

1. **明确任务类型** - 是什么类别的工作?(分析、设计、执行等)
2. **查看智能体列表** - 找到最匹配的专业智能体
3. **优先单一智能体** - 简单任务直接调用单个智能体
4. **复杂任务协调** - 多阶段任务找组长协调

### 质量保障

- ✅ 所有智能体输出遵循标准化路径规范
- ✅ 任务执行前明确需求和预期输出
- ✅ 使用适当的模型(sonnet/opus)
- ✅ 复杂任务启用TodoWrite跟踪进度

### 输出路径规范

所有智能体输出遵循统一路径规范:

```
output/[项目名]/[智能体ID]/
├── plans/      # 执行计划
├── results/    # 实际输出
├── logs/       # 执行日志
└── metadata/   # 元数据
```

## 🔧 扩展点

本插件支持以下扩展:

1. **Commands** (commands/*.md) - 频繁使用的工作流快捷命令
2. **Skills** (skills/*/SKILL.md) - 复杂自动化能力
3. **Hooks** (hooks/hooks.json) - 事件驱动自动化
4. **MCP Servers** (.mcp.json) - 外部工具集成

## 📚 相关文档

- **智能体文档**: [agents/README.md](agents/README.md)
- **命令文档**: [commands/README.md](commands/README.md)
- **技能包文档**: [skills/README.md](skills/README.md)
- **主文档**: [../../README.md](../../README.md)

## 🔗 依赖与要求

- **Claude Code**: v1.0.124+
- **模型**: Sonnet 4.5 (推荐)
- **工具**: Task, Read, Write, Edit, Grep, Glob, Bash
- **技能包依赖**: 无(所有技能包独立)

## 📊 统计信息

- **智能体数量**: 9个
- **命令数量**: 0个
- **技能包数量**: 0个
- **维护状态**: ✅ 活跃维护
- **最后更新**: 2025-11-01

---

**Created by**: ZTL Digital Intelligence Operations Center
**Plugin Type**: Professional Domain Plugin (Admin Team)
**Status**: Production Ready ✅
