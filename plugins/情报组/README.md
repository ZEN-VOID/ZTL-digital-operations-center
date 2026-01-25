# 情报组 Plugin

> 商业情报与数据分析插件 - 从调研采集到洞察分析的完整情报体系

[![Agents](https://img.shields.io/badge/agents-8-blue)](agents/)
[![Commands](https://img.shields.io/badge/commands-0-green)](commands/)
[![Skills](https://img.shields.io/badge/skills-0-orange)](skills/)

## 📋 概述

专业商业情报插件,提供深度调研、网页采集、数据分析、市场洞察等能力。

本插件包含 **8个专业智能体**,0个斜杠命令,0个技能包,提供完整的业务流程支持。

## 🤖 智能体架构

### 组织结构

本组共有8个智能体:

1. **E0-情报需求分析师** - E0-情报需求分析师
2. **E1-深度调研员** - E1-深度调研员
3. **E2-Chrome网页采集** - E2-Chrome网页采集
4. **E3-深度爬虫** - E3-深度爬虫
5. **E4-深度情报分析** - E4-深度情报分析
6. **E5-COS存储管理** - E5-COS存储管理
7. **E6-Supabase数据库管理** - E6-Supabase数据库管理
8. **EE-情报组组长** - EE-情报组组长

### 智能体详情

#### E0-情报需求分析师

**名称**: E0-情报需求分析师

**何时使用**:
- 情报需求分析师,负责调研需求分析与项目规划,设计调研方案和数据采集策略。是情报获取流程的Phase 0,为数据收集和分析奠定基础。

**调用方式**:
```python
Task(subagent_type="E0-情报需求分析师",
     prompt="您的任务描述")
```

---

#### E1-深度调研员

**名称**: E1-深度调研员

**何时使用**:
- 深度调研员,专注于行业深度调研与竞品分析,通过多维度研究提供战略洞察。适用于市场调研、竞品分析、行业研究等场景。

**调用方式**:
```python
Task(subagent_type="E1-深度调研员",
     prompt="您的任务描述")
```

---

#### E2-Chrome网页采集

**名称**: E2-Chrome网页采集

**何时使用**:
- Chrome网页采集,专注于网页数据采集策略规划与浏览器自动化方案设计。通过反爬策略、选择器设计、质量验证框架提供完整的采集计划。适用于电商数据采集、竞品信息抓取、行业资讯监控等场景。

**调用方式**:
```python
Task(subagent_type="E2-Chrome网页采集",
     prompt="您的任务描述")
```

---

#### E3-深度爬虫

**名称**: E3-深度爬虫

**何时使用**:
- 深度爬虫,负责企业级网页爬取策略规划,处理复杂的多页面导航、动态内容加载、反爬虫机制。提供分布式爬虫架构设计和大规模数据采集方案。适用于行业数据库构建、市场数据监控等场景。

**调用方式**:
```python
Task(subagent_type="E3-深度爬虫",
     prompt="您的任务描述")
```

---

#### E4-深度情报分析

**名称**: E4-深度情报分析

**何时使用**:
- 深度情报分析,负责综合情报分析策略规划,整合多源数据进行深度洞察。提供竞品分析框架、市场趋势预测、战略决策支持。适用于战略研究、市场分析、风险评估等场景。

**调用方式**:
```python
Task(subagent_type="E4-深度情报分析",
     prompt="您的任务描述")
```

---

#### E5-COS存储管理

**名称**: E5-COS存储管理

**何时使用**:
- COS存储管理,负责腾讯云对象存储(COS)管理策略规划,提供文件上传、下载、图片处理、数据归档方案。支持AIGC内容存储、数据备份、CDN加速。适用于媒体资产管理、数据湖构建等场景。

**调用方式**:
```python
Task(subagent_type="E5-COS存储管理",
     prompt="您的任务描述")
```

---

#### E6-Supabase数据库管理

**名称**: E6-Supabase数据库管理

**何时使用**:
- Supabase数据库管理,负责Supabase PostgreSQL数据库管理策略规划,提供表结构设计、查询优化、数据迁移方案。支持实时数据订阅、行级安全策略。适用于应用数据管理、数据分析等场景。

**调用方式**:
```python
Task(subagent_type="E6-Supabase数据库管理",
     prompt="您的任务描述")
```

---

#### EE-情报组组长

**名称**: EE-情报组组长

**何时使用**:
- 情报组组长,负责情报组整体战略规划与协调,统筹E0-E6专业智能体,提供情报级决策支持和多智能体编排能力。适用于复杂情报项目、市场研究、数据采集等场景。

**调用方式**:
```python
Task(subagent_type="EE-情报组组长",
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
Task(subagent_type="EE-情报组组长",
     prompt="需要团队协作的复杂任务")
```

## 📁 项目结构

```
plugins/情报组/
├── .claude-plugin/
│   └── plugin.json              # 插件配置
│
├── agents/                      # 8个智能体
│   ├── E0-情报需求分析师.md
│   ├── E1-深度调研员.md
│   ├── E2-Chrome网页采集.md
│   ├── E3-深度爬虫.md
│   ├── E4-深度情报分析.md
│   ├── E5-COS存储管理.md
│   ├── E6-Supabase数据库管理.md
│   ├── EE-情报组组长.md
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

- **智能体数量**: 8个
- **命令数量**: 0个
- **技能包数量**: 0个
- **维护状态**: ✅ 活跃维护
- **最后更新**: 2025-11-01

---

**Created by**: ZTL Digital Intelligence Operations Center
**Plugin Type**: Professional Domain Plugin (Intelligence Team)
**Status**: Production Ready ✅
