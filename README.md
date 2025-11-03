# ZTL数智化作战中心

> Multi-Agent Orchestration Platform for Restaurant Industry Digital Transformation

[![Claude Code](https://img.shields.io/badge/Claude-Code-8B5CF6)](https://claude.ai/code)
[![Agents](https://img.shields.io/badge/Agents-77-blue)](.claude/agents/)
[![Commands](https://img.shields.io/badge/Commands-12-green)](.claude/commands/)
[![Skills](https://img.shields.io/badge/Skills-11-orange)](.claude/skills/)

## 📖 项目简介

ZTL数智化作战中心是基于Claude Code + Sonnet 4.5构建的**多智能体编排平台**,专为餐饮行业数字化转型设计。通过协调**77个专业智能体**分布在**7个业务组**,实现从战略规划到门店筹建的全流程智能化。

### 核心理念

这不是传统的单体应用,而是一个**智能体编排框架**。Claude通过动态组合专业智能体,每个智能体都拥有领域专业知识编码在其Markdown定义中。

## ✨ 核心特性

- 🤖 **60+专业智能体** - 覆盖战略、创意、情报、筹建、开发、美团、供应、行政8大业务组
- 🎯 **三层架构** - 知识层(Agents+Skills) → 编排层(Claude推理) → 执行层(Tools+Output)
- 🔄 **多模式执行** - 支持三层架构、直接执行、混合协调三种模式
- 📊 **智能调度** - QQ-总指挥官统筹多智能体协作
- 🛠️ **工具生态** - 集成7+ MCP服务器(chrome, playwright, github, context7, lark, cos, supabase)
- 📁 **标准化输出** - output/[项目名]/[agent-name]/ 结构化输出路径

## 🏗️ 技术架构

### 架构层次

```
Layer 1: 知识层 (.claude/agents/ + .claude/skills/)
  ├── Agents: 角色决策框架和领域知识
  └── Skills: 自包含能力包和执行引擎

Layer 2: 编排层 (Claude推理)
  ├── 运行时推理和动态能力组合
  └── 智能路由和任务调度

Layer 3: 执行层 (Tools + Output)
  ├── 工具执行(Bash, Python, API, MCP)
  └── 结果持久化到 output/[项目名]/[agent-name]/
```

### 技术栈

| 类别 | 技术 |
|------|------|
| AI核心 | Claude Code, Sonnet 4.5 |
| 智能体架构 | Multi-Agent System, Task-based Delegation |
| 协议标准 | Model Context Protocol (MCP) |
| 开发语言 | Python, TypeScript, Markdown |
| 浏览器自动化 | chrome-mcp, playwright-mcp |
| 版本控制 | Git, GitHub API (github-mcp) |
| 云服务 | Tencent COS (cos-mcp), Supabase (supabase-mcp) |
| 企业协作 | Feishu/Lark (lark-mcp) |

## 📁 项目结构

基于最新快照生成时间: 2025-11-03 02:23:30

```
.
├── .claude/              # Claude Code配置
│   ├── agents/          # 智能体定义(77个)
│   ├── commands/        # 斜杠命令(12个)
│   ├── hooks/           # 生命周期钩子
│   └── skills/          # 技能包(11个)
├── plugins/             # 业务组插件(7个)
│   ├── 战略组/
│   ├── 创意组/
│   ├── 情报组/
│   ├── 筹建组/
│   ├── 开发组/
│   ├── 美团组/
│   ├── 供应组/
│   └── 行政组/
├── output/              # 智能体输出目录
├── reports/             # 执行报告
├── trees/               # 目录快照
├── PRPs/                # PRP文档
└── project/             # 项目代码
```

详细目录树参见: [trees/tree_structure_*.md](trees/)

## 🚀 快速开始

### 环境要求

- Claude Code CLI
- Python 3.12+
- Node.js 18+ (可选,用于MCP服务器)
- Git

### 使用指南

1. **调用智能体**:
```python
# 通过Task工具调用专业智能体
Task(subagent_type="G1-经营分析优化师",
     prompt="分析本月门店经营数据")
```

2. **使用命令**:
```bash
/prp <feature-description>     # 生成PRP文档
/test                           # 运行测试套件
/context-aware                  # 8维度项目分析
/github-pull                    # 同步到GitHub
```

3. **协调多智能体**:
```python
# 复杂任务调用总指挥官
Task(subagent_type="QQ-总指挥官",
     prompt="为新开的火锅店做完整的开业筹备方案")
```

## 🤖 智能体系统

### 业务组概览

| 业务组 | 智能体数量 | 核心职能 |
|--------|-----------|----------|
| 情报组 | 8个 | 专业领域智能体 |
| 筹建组 | 6个 | 专业领域智能体 |
| 开发组 | 20个 | 专业领域智能体 |
| 行政组 | 9个 | 专业领域智能体 |
| 美团组 | 5个 | 专业领域智能体 |
| 战略组 | 11个 | 专业领域智能体 |
| 创意组 | 18个 | 专业领域智能体 |


详细信息请参阅: [OVERVIEW.md](OVERVIEW.md#智能体系统)

## 📜 命令系统

项目包含**12个斜杠命令**,分为以下类别:

- **PRP工作流**: `/prp`, `/test`
- **上下文管理**: `/context-aware`, `/manus`
- **项目管理**: `/github-pull`, `/github-issue`, `/readme-generator`, `/claude`
- **智能体编排**: `/trees`, `/trees-clean`

完整命令列表参见: [.claude/commands/](.claude/commands/)

## 📊 项目统计

- **总目录数**: 426
- **智能体数**: 77个(7个业务组)
- **命令数**: 12个
- **技能包数**: 11个
- **MCP服务器**: 7+个

## 🛣️ 开发指南

### 创建新智能体

智能体是`.claude/agents/[业务组]/`下的Markdown文件:

```markdown
---
name: 智能体名称
description: 简短描述
model: claude-sonnet-4.5
tools: ["*"]
---

# 角色定位

[智能体的专业领域和职责]

# 工作流程

1. 分析需求
2. 执行任务
3. 输出结果

# 输出规范

[输出格式和质量标准]
```

创建后运行 `/claude` 同步文档。

### 创建新技能包

技能包位于 `.claude/skills/[category]/[skill-name]/`:

```
skill-name/
├── SKILL.md              # 元数据(YAML) + 使用指南
├── scripts/              # 执行引擎(Python)
│   └── core_engine.py
└── reference.md          # 扩展文档(可选)
```

技能包使用**渐进披露原则**:Claude先加载SKILL.md(~500-2000 tokens),然后按需加载scripts/reference。

### 最佳实践

- ✅ 复杂功能先使用 `/prp` 生成PRP文档
- ✅ 所有改动通过 `/test` 验证
- ✅ 提交前使用 `/github-pull` 同步
- ✅ 定期执行 `/context-aware` 刷新上下文
- ✅ 手动修改配置后运行 `/claude` 更新文档

## 📄 相关文档

- [OVERVIEW.md](OVERVIEW.md) - 技术深度文档
- [CLAUDE.md](CLAUDE.md) - 项目配置指南
- [~/.claude/CLAUDE.md](~/.claude/CLAUDE.md) - 全局配置文档

## 📄 许可证

本项目为私有项目,未经授权不得复制、修改或分发。

---

**⭐ 最后更新**: 2025-11-03 02:23:30
**🔧 生成工具**: `/readme-generator` 命令

*这是一个活文档。运行 `/readme-generator` 在重大配置更改后保持其与实际项目状态同步。*
