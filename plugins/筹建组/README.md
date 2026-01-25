# 筹建组 Plugin

> 店铺筹建专业插件 - 从平面规划到空间设计的完整筹建流程

[![Agents](https://img.shields.io/badge/agents-6-blue)](agents/)
[![Commands](https://img.shields.io/badge/commands-0-green)](commands/)
[![Skills](https://img.shields.io/badge/skills-2-orange)](skills/)

## 📋 概述

专业筹建插件,提供平面图规划、BIM建模、空间设计、工程管理等能力。

本插件包含 **6个专业智能体**,0个斜杠命令,2个技能包,提供完整的业务流程支持。

## 🤖 智能体架构

### 组织结构

本组共有6个智能体:

1. **Z0-筹建项目需求分析师** - Z0-筹建项目需求分析师
2. **Z1-平面图计划师** - Z1-平面图计划师
3. **Z2-空间设计师** - Z2-空间设计师
4. **Z3-3D生成AIGC助手** - Z3-3D生成AIGC助手
5. **Z4-建筑动画AIGC助手** - Z4-建筑动画AIGC助手
6. **ZZ-筹建组组长** - ZZ - 筹建组组长

### 智能体详情

#### Z0-筹建项目需求分析师

**名称**: Z0-筹建项目需求分析师

**何时使用**:
- 筹建项目需求分析师,负责筹建需求分析与项目规划,制定详细的门店筹建方案和时间表。是筹建流程的Phase 0,为后续施工和装修奠定基础。

**调用方式**:
```python
Task(subagent_type="Z0-筹建项目需求分析师",
     prompt="您的任务描述")
```

---

#### Z1-平面图计划师

**名称**: Z1-平面图计划师

**何时使用**:
- 平面图计划师,负责创建餐厅平面图配置和空间布局规划。提供功能分区、动线设计、尺寸标注方案。适用于餐厅筹建、空间规划等场景。

**调用方式**:
```python
Task(subagent_type="Z1-平面图计划师",
     prompt="您的任务描述")
```

---

#### Z2-空间设计师

**名称**: Z2-空间设计师

**何时使用**:
- 空间设计师,负责使用Midjourney生成餐厅空间设计效果图。提供室内设计方案、风格定位、视觉呈现。适用于空间设计、效果图制作等场景。

**调用方式**:
```python
Task(subagent_type="Z2-空间设计师",
     prompt="您的任务描述")
```

---

#### Z3-3D生成AIGC助手

**名称**: Z3-3D生成AIGC助手

**何时使用**:
- 3D生成AIGC助手,负责将2D室内设计效果图转换为3D模型。提供3D建模、虚拟漫游、空间可视化方案。适用于3D建模、空间展示等场景。

**调用方式**:
```python
Task(subagent_type="Z3-3D生成AIGC助手",
     prompt="您的任务描述")
```

---

#### Z4-建筑动画AIGC助手

**名称**: Z4-建筑动画AIGC助手

**何时使用**:
- 建筑动画AIGC助手,负责建筑动画与AIGC辅助设计,使用AI技术生成设计方案和效果图。适用于设计可视化、方案比选、客户提案等场景。

**调用方式**:
```python
Task(subagent_type="Z4-建筑动画AIGC助手",
     prompt="您的任务描述")
```

---

#### ZZ-筹建组组长

**名称**: ZZ - 筹建组组长

**何时使用**:
- 筹建组AIGC总指挥官，负责门店筹建全流程管理，统筹协调Z0需求分析、Z1平面图设计、Z2空间设计AIGC、Z3三维重建AIGC、Z4动画生成AIGC，实现从需求分析到视觉交付的高效AIGC工作流

**调用方式**:
```python
Task(subagent_type="ZZ-筹建组组长",
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
Task(subagent_type="ZZ-筹建组组长",
     prompt="需要团队协作的复杂任务")
```

## 📁 项目结构

```
plugins/筹建组/
├── .claude-plugin/
│   └── plugin.json              # 插件配置
│
├── agents/                      # 6个智能体
│   ├── Z0-筹建项目需求分析师.md
│   ├── Z1-平面图计划师.md
│   ├── Z2-空间设计师.md
│   ├── Z3-3D生成AIGC助手.md
│   ├── Z4-建筑动画AIGC助手.md
│   ├── ZZ-筹建组组长.md
│
├── commands/                    # 0个命令
│   └── README.md
│
├── skills/                      # 2个技能包
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
- **技能包数量**: 2个
- **维护状态**: ✅ 活跃维护
- **最后更新**: 2025-11-01

---

**Created by**: ZTL Digital Intelligence Operations Center
**Plugin Type**: Professional Domain Plugin (Construction Team)
**Status**: Production Ready ✅
