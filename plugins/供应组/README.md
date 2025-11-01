# 供应组 Plugin

> 供应链管理插件 - 从采购到成本控制的完整供应链体系

[![Agents](https://img.shields.io/badge/agents-7-blue)](agents/)
[![Commands](https://img.shields.io/badge/commands-0-green)](commands/)
[![Skills](https://img.shields.io/badge/skills-0-orange)](skills/)

## 📋 概述

综合供应链管理插件,涵盖采购管理、库存管理、成本控制、供应商管理等职能。

本插件包含 **7个专业智能体**,0个斜杠命令,0个技能包,提供完整的业务流程支持。

## 🤖 智能体架构

### 组织结构

本组共有7个智能体:

1. **C0-供应需求分析师** - C0-supply-demand-analyst
2. **C1-采购执行经理** - C1-procurement-manager
3. **C2-库存管理员** - C2-inventory-manager
4. **C3-成本卡管理员** - C3-cost-card-manager
5. **C4-供应商管理员** - C4-supplier-manager
6. **C5-分账管理员** - C5-revenue-split-manager
7. **CC-供应组组长** - CC-supply-chain-leader

### 智能体详情

#### C0-供应需求分析师

**名称**: C0-supply-demand-analyst

**何时使用**:
- 餐饮供应链需求分析与规划专家,负责供应需求预测、库存优化规划、供应商绩效评估和成本优化方案。主动用于季节性菜单调整、食材消耗异常检测、批量采购成本评估、节假日/促销活动备货规划等场景。

**调用方式**:
```python
Task(subagent_type="C0-供应需求分析师",
     prompt="您的任务描述")
```

---

#### C1-采购执行经理

**名称**: C1-procurement-manager

**何时使用**:
- 采购执行经理,负责餐饮企业采购计划制定、供应商订单管理、采购流程优化、交付协调。主动用于采购计划生成、批量订单规划、供应商协调、紧急采购响应、采购成本优化等场景。

**调用方式**:
```python
Task(subagent_type="C1-采购执行经理",
     prompt="您的任务描述")
```

---

#### C2-库存管理员

**名称**: C2-inventory-manager

**何时使用**:
- 库存管理员,负责餐饮企业库存优化规划、补货策略设计、库存周转率分析、损耗控制方案。主动用于库存策略优化、补货计划生成、库存预警设置、跨店调拨规划、损耗分析等场景。

**调用方式**:
```python
Task(subagent_type="C2-库存管理员",
     prompt="您的任务描述")
```

---

#### C3-成本卡管理员

**名称**: C3-cost-card-manager

**何时使用**:
- 成本卡管理员,负责餐饮企业菜品成本核算规划、成本卡体系设计、成本优化分析、定价策略制定。主动用于成本卡创建规划、成本差异分析、成本优化方案、定价模型设计、成本预算编制等场景。

**调用方式**:
```python
Task(subagent_type="C3-成本卡管理员",
     prompt="您的任务描述")
```

---

#### C4-供应商管理员

**名称**: C4-supplier-manager

**何时使用**:
- 供应商关系管理与绩效评估规划专家,负责供应商准入评估方案、供应商绩效评估体系、供应商风险管理策略、合同管理与谈判策略。主动用于供应商准入评审、季度绩效考核规划、供应商风险预警、合同续签谈判等场景。

**调用方式**:
```python
Task(subagent_type="C4-供应商管理员",
     prompt="您的任务描述")
```

---

#### C5-分账管理员

**名称**: C5-revenue-split-manager

**何时使用**:
- 分账规则设计与利润分配规划专家,负责分账规则设计、利润分配计算方案、多方财务分配机制、分账透明度审计。主动用于合伙人分账规则配置、平台抽佣分账设计、员工提成方案设计、供应商返点分配规划等场景。

**调用方式**:
```python
Task(subagent_type="C5-分账管理员",
     prompt="您的任务描述")
```

---

#### CC-供应组组长

**名称**: CC-supply-chain-leader

**何时使用**:
- 供应组战略规划与协调指挥官,负责供应链全局战略规划、统筹协调C0-C5专业智能体、供应链数字化转型和持续优化。主动用于供应链战略制定、跨智能体协同调度、重大供应链问题决策、供应链系统性优化等场景。

**调用方式**:
```python
Task(subagent_type="CC-供应组组长",
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
Task(subagent_type="CC-供应组组长",
     prompt="需要团队协作的复杂任务")
```

## 📁 项目结构

```
plugins/供应组/
├── .claude-plugin/
│   └── plugin.json              # 插件配置
│
├── agents/                      # 7个智能体
│   ├── C0-供应需求分析师.md
│   ├── C1-采购执行经理.md
│   ├── C2-库存管理员.md
│   ├── C3-成本卡管理员.md
│   ├── C4-供应商管理员.md
│   ├── C5-分账管理员.md
│   ├── CC-供应组组长.md
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

- **智能体数量**: 7个
- **命令数量**: 0个
- **技能包数量**: 0个
- **维护状态**: ✅ 活跃维护
- **最后更新**: 2025-11-01

---

**Created by**: ZTL Digital Intelligence Operations Center
**Plugin Type**: Professional Domain Plugin (Supply Chain Team)
**Status**: Production Ready ✅
