# 战略组 Plugin

> 商业战略与运营分析插件 - 从战略规划到运营优化的完整决策支持

[![Agents](https://img.shields.io/badge/agents-11-blue)](agents/)
[![Commands](https://img.shields.io/badge/commands-0-green)](commands/)
[![Skills](https://img.shields.io/badge/skills-0-orange)](skills/)

## 📋 概述

专业商业战略插件,提供战略规划、商业分析、运营优化、产品定位、竞争分析等全方位决策支持。

本插件包含 **11个专业智能体**,0个斜杠命令,0个技能包,提供完整的业务流程支持。

## 🤖 智能体架构

### 组织结构

本组共有11个智能体:

1. **G0-战略需求解析师** - strategic-needs-analyzer
2. **G1-经营分析优化师** - g1-business-analyst
3. **G2-产品力打造专家** - g2-product-strategy
4. **G3-区域扩张策略师** - g3-regional-expansion-strategist
5. **G4-商业模式设计师** - business-model-designer
6. **G5-连锁复制专家** - franchise-standardization-architect
7. **G6-数字化转型架构师** - strategic-dashboard-architect
8. **G7-精细化管理专家** - g7-sop-specialist
9. **G8-商业数据分析师** - g8-business-data-analyst
10. **G9-营销归因分析师** - g9-marketing-attribution-strategist
11. **GG-战略组组长** - gg-strategic-director

### 智能体详情

#### G0-战略需求解析师

**名称**: strategic-needs-analyzer

**何时使用**:
- Use this agent when the user needs to analyze strategic requirements, break down high-level goals in

**调用方式**:
```python
Task(subagent_type="G0-战略需求解析师",
     prompt="您的任务描述")
```

---

#### G1-经营分析优化师

**名称**: g1-business-analyst

**何时使用**:
- Use this agent when you need to design business analysis frameworks, plan data-driven decision syste

**调用方式**:
```python
Task(subagent_type="G1-经营分析优化师",
     prompt="您的任务描述")
```

---

#### G2-产品力打造专家

**名称**: g2-product-strategy

**何时使用**:
- Use this agent when the user needs strategic product development and optimization for restaurant bus

**调用方式**:
```python
Task(subagent_type="G2-产品力打造专家",
     prompt="您的任务描述")
```

---

#### G3-区域扩张策略师

**名称**: g3-regional-expansion-strategist

**何时使用**:
- Use this agent when the user needs strategic regional expansion planning, market entry frameworks, s

**调用方式**:
```python
Task(subagent_type="G3-区域扩张策略师",
     prompt="您的任务描述")
```

---

#### G4-商业模式设计师

**名称**: business-model-designer

**何时使用**:
- Use this agent when you need to design business model architectures, develop profit structure framew

**调用方式**:
```python
Task(subagent_type="G4-商业模式设计师",
     prompt="您的任务描述")
```

---

#### G5-连锁复制专家

**名称**: franchise-standardization-architect

**何时使用**:
- Use this agent when you need to design standardization system architectures, develop SOP frameworks,

**调用方式**:
```python
Task(subagent_type="G5-连锁复制专家",
     prompt="您的任务描述")
```

---

#### G6-数字化转型架构师

**名称**: strategic-dashboard-architect

**何时使用**:
- Use this agent when the user needs to design strategic data dashboards, plan digital transformation 

**调用方式**:
```python
Task(subagent_type="G6-数字化转型架构师",
     prompt="您的任务描述")
```

---

#### G7-精细化管理专家

**名称**: g7-sop-specialist

**何时使用**:
- Use this agent when you need to standardize restaurant operations through SOP (Standard Operating Pr

**调用方式**:
```python
Task(subagent_type="G7-精细化管理专家",
     prompt="您的任务描述")
```

---

#### G8-商业数据分析师

**名称**: g8-business-data-analyst

**何时使用**:
- Use this agent when you need to execute data analysis, generate business reports, create visualizati

**调用方式**:
```python
Task(subagent_type="G8-商业数据分析师",
     prompt="您的任务描述")
```

---

#### G9-营销归因分析师

**名称**: g9-marketing-attribution-strategist

**何时使用**:
- Use this agent when you need to design comprehensive marketing attribution frameworks, multi-channel

**调用方式**:
```python
Task(subagent_type="G9-营销归因分析师",
     prompt="您的任务描述")
```

---

#### GG-战略组组长

**名称**: gg-strategic-director

**何时使用**:
- Use this agent when you need strategic planning oversight, multi-agent orchestration for complex str

**调用方式**:
```python
Task(subagent_type="GG-战略组组长",
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
Task(subagent_type="GG-战略组组长",
     prompt="需要团队协作的复杂任务")
```

## 📁 项目结构

```
plugins/战略组/
├── .claude-plugin/
│   └── plugin.json              # 插件配置
│
├── agents/                      # 11个智能体
│   ├── G0-战略需求解析师.md
│   ├── G1-经营分析优化师.md
│   ├── G2-产品力打造专家.md
│   ├── G3-区域扩张策略师.md
│   ├── G4-商业模式设计师.md
│   ├── G5-连锁复制专家.md
│   ├── G6-数字化转型架构师.md
│   ├── G7-精细化管理专家.md
│   ├── G8-商业数据分析师.md
│   ├── G9-营销归因分析师.md
│   ├── GG-战略组组长.md
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

- **智能体数量**: 11个
- **命令数量**: 0个
- **技能包数量**: 0个
- **维护状态**: ✅ 活跃维护
- **最后更新**: 2025-11-01

---

**Created by**: ZTL Digital Intelligence Operations Center
**Plugin Type**: Professional Domain Plugin (Strategy Team)
**Status**: Production Ready ✅
