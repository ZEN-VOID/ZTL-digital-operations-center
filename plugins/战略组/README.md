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
- 战略需求解析师,负责战略需求的深度分析与澄清,通过系统性访谈和需求建模,将模糊的业务目标转化为清晰的执行方案。适用于项目启动、战略规划、需求定义等场景。

**调用方式**:
```python
Task(subagent_type="G0-战略需求解析师",
     prompt="您的任务描述")
```

---

#### G1-经营分析优化师

**名称**: g1-business-analyst

**何时使用**:
- 经营分析优化师,专注于经营数据分析与业务优化,通过数据驱动的方法识别经营问题、提供改进建议。适用于门店经营分析、成本优化、效率提升等场景。

**调用方式**:
```python
Task(subagent_type="G1-经营分析优化师",
     prompt="您的任务描述")
```

---

#### G2-产品力打造专家

**名称**: g2-product-strategy

**何时使用**:
- 产品力打造专家,负责产品定位与优化策略,基于市场分析和用户洞察,提供产品创新和差异化竞争方案。适用于新品开发、产品重塑、市场定位等场景。

**调用方式**:
```python
Task(subagent_type="G2-产品力打造专家",
     prompt="您的任务描述")
```

---

#### G3-区域扩张策略师

**名称**: g3-regional-expansion-strategist

**何时使用**:
- 区域扩张策略师,专注于选址策略与区域扩张规划,通过商圈分析、人流预测、竞争评估,提供科学的选址决策支持。适用于新店选址、区域拓展、门店布局等场景。

**调用方式**:
```python
Task(subagent_type="G3-区域扩张策略师",
     prompt="您的任务描述")
```

---

#### G4-商业模式设计师

**名称**: business-model-designer

**何时使用**:
- 商业模式设计师,负责商业模式创新与盈利模式设计,通过价值链分析和商业逻辑重构,提供可持续的商业模式方案。适用于商业模式创新、盈利能力提升等场景。

**调用方式**:
```python
Task(subagent_type="G4-商业模式设计师",
     prompt="您的任务描述")
```

---

#### G5-连锁复制专家

**名称**: franchise-standardization-architect

**何时使用**:
- 连锁复制专家,专注于连锁复制与标准化体系建设,将成功经验模式化,支持快速规模化扩张。适用于连锁扩张、标准化管理、复制体系建设等场景。

**调用方式**:
```python
Task(subagent_type="G5-连锁复制专家",
     prompt="您的任务描述")
```

---

#### G6-数字化转型架构师

**名称**: strategic-dashboard-architect

**何时使用**:
- 数字化转型架构师,负责数字化转型战略规划与IT架构设计,推动企业数字化升级和智能化改造。适用于数字化转型、系统规划、技术架构设计等场景。

**调用方式**:
```python
Task(subagent_type="G6-数字化转型架构师",
     prompt="您的任务描述")
```

---

#### G7-精细化管理专家

**名称**: g7-sop-specialist

**何时使用**:
- 精细化管理专家,专注于流程优化与精细化管理,通过精益管理方法提升运营效率和管理水平。适用于流程优化、成本控制、效率提升等场景。

**调用方式**:
```python
Task(subagent_type="G7-精细化管理专家",
     prompt="您的任务描述")
```

---

#### G8-商业数据分析师

**名称**: g8-business-data-analyst

**何时使用**:
- 商业数据分析师,负责执行数据分析和生成商业报告,提供数据驱动的业务洞察。擅长数据可视化、趋势分析、业务建议。适用于数据分析、报告生成、决策支持等场景。

**调用方式**:
```python
Task(subagent_type="G8-商业数据分析师",
     prompt="您的任务描述")
```

---

#### G9-营销归因分析师

**名称**: g9-marketing-attribution-strategist

**何时使用**:
- 营销归因分析师,负责设计全面的营销归因框架,分析营销渠道效果和ROI。提供多触点归因模型、营销效果评估、预算优化方案。适用于营销分析、渠道优化、ROI提升等场景。

**调用方式**:
```python
Task(subagent_type="G9-营销归因分析师",
     prompt="您的任务描述")
```

---

#### GG-战略组组长

**名称**: gg-strategic-director

**何时使用**:
- 战略组组长,负责战略组整体规划与协调,统筹G0-G9专业智能体,提供战略级决策支持和多智能体编排能力。适用于复杂战略项目、业务转型规划、跨部门协作等场景。

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
