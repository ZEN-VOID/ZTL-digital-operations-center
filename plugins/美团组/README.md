# 美团组 Plugin

> 美团平台运营插件 - 从店铺运营到数据分析的完整运营体系

[![Agents](https://img.shields.io/badge/agents-6-blue)](agents/)
[![Commands](https://img.shields.io/badge/commands-0-green)](commands/)
[![Skills](https://img.shields.io/badge/skills-3-orange)](skills/)

## 📋 概述

专业美团运营插件,提供平台运营、营销推广、数据分析、报表生成等能力。

本插件包含 **6个专业智能体**,0个斜杠命令,3个技能包,提供完整的业务流程支持。

## 🤖 智能体架构

### 组织结构

本组共有6个智能体:

1. **V0-办公业务需求分析员** - meituan-butler-requirement-analyst
2. **V1-运营管理员** - meituan-butler-ops-manager
3. **V2-营销管理员** - meituan-marketing-manager
4. **V4-报表管理员** - meituan-report-analyst
5. **V5-网页自动化** - meituan-butler-automation
6. **VV-美团组组长** - VV-美团组组长

### 智能体详情

#### V0-办公业务需求分析员

**名称**: meituan-butler-requirement-analyst

**何时使用**:
- Use this agent when you need to analyze business requirements for the Meituan Butler (美团管家) system a

**调用方式**:
```python
Task(subagent_type="V0-办公业务需求分析员",
     prompt="您的任务描述")
```

---

#### V1-运营管理员

**名称**: meituan-butler-ops-manager

**何时使用**:
- Use this agent when you need to create operational management plans for the Meituan Butler (美团管家) SA

**调用方式**:
```python
Task(subagent_type="V1-运营管理员",
     prompt="您的任务描述")
```

---

#### V2-营销管理员

**名称**: meituan-marketing-manager

**何时使用**:
- Use this agent when you need to **plan and design marketing strategies** for restaurant businesses u

**调用方式**:
```python
Task(subagent_type="V2-营销管理员",
     prompt="您的任务描述")
```

---

#### V4-报表管理员

**名称**: meituan-report-analyst

**何时使用**:
- Use this agent when you need to **plan and design comprehensive data analysis and reporting strategi

**调用方式**:
```python
Task(subagent_type="V4-报表管理员",
     prompt="您的任务描述")
```

---

#### V5-网页自动化

**名称**: meituan-butler-automation

**何时使用**:
- Use this agent when you need to automate operations in the Meituan Butler (美团管家) SAAS system. This i

**调用方式**:
```python
Task(subagent_type="V5-网页自动化",
     prompt="您的任务描述")
```

---

#### VV-美团组组长

**名称**: VV-美团组组长

**何时使用**:
- 美团组总指挥官,负责美团管家数据中台系统的战略规划、业务系统集成和数据流程自动化,统筹协调V0-V8专业智能体。主动用于战略级决策、跨组协调、重大问题升级等场景。 Examples:

**调用方式**:
```python
Task(subagent_type="VV-美团组组长",
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
Task(subagent_type="VV-美团组组长",
     prompt="需要团队协作的复杂任务")
```

## 📁 项目结构

```
plugins/美团组/
├── .claude-plugin/
│   └── plugin.json              # 插件配置
│
├── agents/                      # 6个智能体
│   ├── V0-办公业务需求分析员.md
│   ├── V1-运营管理员.md
│   ├── V2-营销管理员.md
│   ├── V4-报表管理员.md
│   ├── V5-网页自动化.md
│   ├── VV-美团组组长.md
│
├── commands/                    # 0个命令
│   └── README.md
│
├── skills/                      # 3个技能包
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

- **智能体数量**: 6个
- **命令数量**: 0个
- **技能包数量**: 3个
- **维护状态**: ✅ 活跃维护
- **最后更新**: 2025-11-01

---

**Created by**: ZTL Digital Intelligence Operations Center
**Plugin Type**: Professional Domain Plugin (Meituan Operations Team)
**Status**: Production Ready ✅
