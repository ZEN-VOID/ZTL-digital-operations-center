# ZTL数智化作战中心

[![Claude Code](https://img.shields.io/badge/Claude-Code-8A2BE2?logo=claude)](https://claude.ai/code)
[![Sonnet 4.5](https://img.shields.io/badge/Sonnet-4.5-blue)](https://www.anthropic.com)
[![Agent Framework](https://img.shields.io/badge/Framework-Multi--Agent-orange)](https://docs.claude.com/en/docs/claude-code/)
[![License](https://img.shields.io/badge/License-MIT-green)](#)

ZTL数智化作战中心 (ZTL Digital Intelligence Operations Center) 是面向餐饮行业数字化转型的多智能体协同平台,基于 Claude Code + Sonnet 4.5 构建,协调 **93个专业智能体** 横跨 **8大业务组**,处理从战略规划到门店筹建的全链条业务。

---

## 📖 项目简介

这不是传统的单体应用,而是一个**智能体编排框架**,Claude 通过动态组合专业智能体来构建解决方案,每个智能体都在其 Markdown 定义中编码了领域专业知识。

**核心价值**:
- 🎯 **领域专精**: 93个专业智能体覆盖餐饮全业态
- 🔄 **动态协同**: 智能体按需组合,灵活应对复杂场景
- 📊 **数据驱动**: 整合多个MCP服务器实现外部系统访问
- 🚀 **快速迭代**: PRP工作流确保功能开发的高质量交付

---

## ✨ 核心特性

### 🤖 多智能体架构
- **8大业务组**: 战略、创意、情报、筹建、开发、美团、供应、行政
- **93个专业智能体**: 84个业务组智能体 + 9个系统级智能体
- **动态编排**: QQ-总指挥官智能体协调跨组任务执行

### 📜 命令系统
- **13个斜杠命令**: `/prp`, `/test`, `/context-aware`, `/github-pull` 等
- **工作流自动化**: PRP开发流程、并行任务探索、测试迭代修复
- **上下文管理**: MANUS系统整合注意力管理、错误学习、知识沉淀

### 🛠️ 技能包生态
- **22个技能包**: 覆盖办公、AIGC、爬虫、元系统、文档同步等
- **渐进披露**: 按需加载技能包内容,优化token使用
- **自主发现**: Claude自动匹配并调用相关技能

### 🌐 MCP服务器集成
- **7+外部系统**: GitHub、Chrome、Playwright、Feishu、腾讯云COS、Context7、Supabase
- **无缝集成**: 统一工具接口访问浏览器、数据库、云存储等

---

## 🏗️ 技术架构

### 三层智能体架构

```
Layer 1: 知识层 (.claude/agents/ + .claude/skills/)
  ├── Agents: 基于角色的决策框架和领域知识
  └── Skills: 自包含能力包和执行引擎

Layer 2: 编排层 (Claude 推理)
  ├── 运行时推理和动态能力组合
  └── 智能路由和任务调度

Layer 3: 执行层 (工具 + 输出)
  ├── 工具执行 (Bash, Python, API, MCP)
  └── 结果持久化到 output/[项目名]/[agent-name]/
```

### 技术栈

| 类别 | 技术 |
|------|------|
| **AI引擎** | Claude Sonnet 4.5 |
| **框架** | Claude Code (Multi-Agent Framework) |
| **协议** | Model Context Protocol (MCP) |
| **语言** | Python, Bash, Markdown |
| **存储** | 腾讯云COS, Supabase PostgreSQL |
| **自动化** | Chrome DevTools, Playwright |
| **协作** | Feishu/Lark API |

---

## 📁 项目结构

```
ZTL数智化作战中心/
├── .claude/              # Claude Code配置目录
│   ├── agents/           # 系统级智能体 (9个 Q系列)
│   ├── commands/         # 斜杠命令 (13个)
│   ├── skills/           # 技能包 (22个)
│   └── hooks/            # 生命周期钩子
├── plugins/              # 业务组插件 (8个)
│   ├── 战略组/          # 9个智能体
│   ├── 创意组/          # 16个智能体
│   ├── 情报组/          # 8个智能体
│   ├── 筹建组/          # 6个智能体
│   ├── 开发组/          # 20个智能体
│   ├── 美团组/          # 6个智能体
│   ├── 供应组/          # 7个智能体
│   └── 行政组/          # 9个智能体
├── PRPs/                 # Plan-Research-Plan文档
├── output/               # 智能体输出目录
├── reports/              # 执行报告
├── learning/             # 知识积累 (ASDW系统)
├── trees/                # 目录结构快照
├── scripts/              # 实用脚本
├── context/              # 上下文快照
└── project/              # 项目文档
```

---

## 🚀 快速开始

### 环境要求

- **Claude Code**: [安装指南](https://docs.claude.com/en/docs/claude-code/)
- **Python**: 3.8+ (用于脚本执行)
- **Git**: 用于版本控制

### 使用指南

**1. 理解智能体系统**
```bash
# 查看项目概览
/context-aware

# 浏览智能体组织
ls -la plugins/*/agents/
```

**2. 调用单个智能体**
```python
# 战略分析
Task(subagent_type="G1-经营分析优化师",
     prompt="分析本月门店经营数据")

# 创意设计
Task(subagent_type="X3-设计模板解构师",
     prompt="设计新品海报")
```

**3. 调用总指挥官协调多智能体**
```python
Task(subagent_type="QQ-总指挥官",
     prompt="为新开的火锅店做完整的开业筹备方案")
```

**4. 使用命令系统**
```bash
/prp <feature-description>    # 生成PRP文档
/test                          # 运行测试套件
/github-pull                   # 同步到GitHub
/trees <feature> <count> <desc> # 并行任务探索
```

---

## 🤖 智能体系统

本项目采用多智能体协作架构,共有 **69个专业智能体** 分布在 **8个业务组**。

### 业务组概览

| 业务组 | 智能体数量 | 核心职能 |
|--------|-----------|----------|
| **战略组** (Strategy) | 9个 | 商业战略、经营分析、产品定位 |
| **创意组** (Creative) | 13个 | 广告策划、文案设计、视频制作、AIGC |
| **情报组** (Intelligence) | 8个 | 市场调研、网页采集、数据分析 |
| **筹建组** (Construction) | 6个 | 平面规划、空间设计、BIM建模 |
| **开发组** (Development) | 11个 | 全栈开发、测试、部署 |
| **美团组** (Meituan Ops) | 6个 | 平台运营、营销、报表 |
| **供应组** (Supply Chain) | 7个 | 采购、库存、成本管理 |
| **行政组** (Admin) | 9个 | 财务、人事、法务、文档管理 |

详细信息请参阅 [OVERVIEW.md](OVERVIEW.md#智能体系统)

---

## 📜 命令系统

提供 **14个斜杠命令** 用于一键式工作流:

| 命令 | 功能 |
|------|------|
| `/prp <description>` | 生成Plan-Research-Plan文档 |
| `/test` | 运行完整测试套件并迭代修复 |
| `/context-aware` | 8维度项目全面分析 |
| `/manus <type>` | 统一上下文管理系统 |
| `/github-pull` | 同步项目到GitHub |
| `/github-issue <url>` | 系统化Issue分析和修复 |
| `/readme-generator` | 自动更新README文档 |
| `/trees <feature> <count> <desc>` | 并行任务探索 |
| `/trees-clean` | 清理worktrees和分支 |
| `/links <paths>` | 跨工作区同步文件 |
| `/project-instructions` | 更新项目指令文档 |
| `/learn [step]` | 从组件学习转向生态研究 |
| `/github-start` | 初始化GitHub仓库 |
| `/context-aware` | 项目上下文分析 |

详细说明请参阅 [OVERVIEW.md](OVERVIEW.md#命令系统)

---

## 📊 项目统计

### 系统规模

- **智能体总数**: 69个 (8个业务组)
- **斜杠命令**: 14个
- **技能包**: 21个
- **MCP服务器**: 7个
- **生命周期钩子**: 1个 (PreCompact)

### 代码规模

- **总目录数**: ~500+
- **配置文件**: Markdown (agents, commands, skills)
- **执行引擎**: Python, Bash脚本
- **文档系统**: PRPs, README, OVERVIEW

---

## 🛣️ 开发流程

### PRP-驱动开发

```
1. /prp <feature> → 生成研究驱动的计划
2. 审查PRP,确保评分 ≥8/10
3. 按照PRP蓝图实现
4. /test → 使用自动化门控验证
5. 迭代直到所有测试通过
```

### 多智能体工作流

```
1. 总指挥官分析需求 → 生成JSON作战计划
2. 情报组 → 收集数据
3. 战略组 → 分析数据,创建建议
4. 创意组 → 制作营销材料
5. 总指挥官 → 整合所有输出
```

---

## 📄 相关文档

- **OVERVIEW.md**: 深度技术文档
- **CLAUDE.md**: 项目指令和约定
- **.claude/commands/README.md**: 命令系统文档
- **PRPs/**: 功能规划文档
- **reports/**: 执行报告和分析

---

## 📄 许可证

MIT License

---

**⭐ 如果这个项目对您有帮助,请给我们一个Star!**

**文档生成**: 自动更新于 2025-11-01 by `/github-pull` 命令
**版本**: v1.1.0
**最后更新**: 2025-11-01
**更新内容**: 新增9个Q系列系统级智能体、创意组重构(16个)、开发组重构(20个)、新增2个技能包
