# 开发组 Plugin

> 全栈开发专业插件 - 从需求到交付的完整开发流程管理

[![Agents](https://img.shields.io/badge/agents-19-blue)](agents/)
[![Commands](https://img.shields.io/badge/commands-6-green)](commands/)
[![Skills](https://img.shields.io/badge/skills-1-orange)](skills/)
[![Model](https://img.shields.io/badge/model-sonnet%204.5-purple)](https://www.anthropic.com)

## 📋 概述

开发组插件是ZTL数智化作战中心的**核心开发引擎**,提供从产品规划到云部署的全流程开发能力。通过19个专业智能体的协同工作,实现高效、高质量的软件交付。

### 核心能力

- 🎯 **产品管理**: PRD文档、用户故事、需求分析
- 🎨 **前端开发**: React组件、响应式设计、UI/UX
- 🏗️ **后端架构**: 微服务、API设计、数据库架构
- 💻 **编程专家**: Python/TypeScript/JavaScript深度优化
- ✅ **质量保障**: 代码审查、自动化测试、性能优化
- 🐛 **调试排查**: 日志分析、错误追踪、问题诊断
- 🎯 **团队协作**: 多智能体编排、项目管理

## 🤖 智能体架构

### 组织结构 (19个智能体)

```
FF-开发组组长 (Team Leader)
│
├── 产品规划层 (1人)
│   └── F0-产品经理: PRD文档、用户故事、产品路线图
│
├── 前端开发层 (4人)
│   ├── F1-前端开发: React应用、响应式设计
│   ├── F2-UI设计师: 界面和交互设计
│   ├── F3-全栈开发: 全栈应用开发
│   └── F4-文档报告生成: 技术文档和报告
│
├── 后端架构层 (5人)
│   ├── F5-后端架构师: 后端架构设计
│   ├── F6-数据库架构师: 数据库设计优化
│   ├── F7-API文档生成: API文档编写
│   ├── F8-云架构师: 云基础设施架构
│   └── F9-架构评审: 架构评审和优化
│
├── 编程语言专家层 (3人)
│   ├── F10-Python专家: Python深度开发
│   ├── F11-TypeScript专家: TypeScript类型系统
│   └── F12-JavaScript专家: 现代JavaScript
│
├── 质量保障层 (3人)
│   ├── F13-代码审查专家: 代码质量审查
│   ├── F14-测试工程师: 自动化测试
│   └── F15-性能工程师: 性能优化监控
│
└── 调试排查层 (2人)
    ├── F16-调试专家: 问题诊断修复
    └── F17-错误侦探: 错误追踪调试
```

### 智能体详情

<details>
<summary><b>产品规划层 (1人)</b></summary>

| 智能体 | 职责 | 模型 |
|--------|------|------|
| F0-产品经理 | 需求分析、PRD文档、用户故事、RICE评分 | Sonnet |

**核心能力**:
- PRD文档编写 (包含产品概述、功能需求、非功能需求)
- 用户故事 (As a... I want... So that...)
- 产品路线图 (季度/年度规划)
- 需求优先级 (MoSCoW、RICE评分)

</details>

<details>
<summary><b>前端开发层 (4人)</b></summary>

| 智能体 | 职责 | 模型 |
|--------|------|------|
| F1-前端开发 | React应用、响应式设计、组件架构 | Sonnet |
| F2-UI设计师 | 界面设计、交互流程、原型设计 | Sonnet |
| F3-全栈开发 | 全栈应用、前后端集成 | Opus |
| F4-文档报告生成 | 技术文档、API文档、用户手册 | Haiku |

**核心能力**:
- 现代前端框架 (React, Next.js, Vue.js)
- 状态管理 (Redux, Zustand, Context API)
- UI组件库 (Material-UI, shadcn/ui, Tailwind CSS)
- 性能优化 (代码分割、懒加载、缓存策略)

</details>

<details>
<summary><b>后端架构层 (5人)</b></summary>

| 智能体 | 职责 | 模型 |
|--------|------|------|
| F5-后端架构师 | 微服务、RESTful API、系统设计 | Sonnet |
| F6-数据库架构师 | 数据库设计、查询优化、迁移 | Opus |
| F7-API文档生成 | OpenAPI规范、Swagger、SDK生成 | Haiku |
| F8-云架构师 | 云基础设施、容器化、CI/CD | Opus |
| F9-架构评审 | SOLID原则、设计模式、架构审查 | Opus |

**核心能力**:
- 后端框架 (Node.js/Express, Python/FastAPI, Go)
- 数据库 (PostgreSQL, MongoDB, Redis)
- 云服务 (AWS, Azure, GCP, Vercel, Supabase)
- 容器化 (Docker, Kubernetes)

</details>

<details>
<summary><b>编程语言专家层 (3人)</b></summary>

| 智能体 | 职责 | 模型 |
|--------|------|------|
| F10-Python专家 | 装饰器、生成器、异步编程 | Sonnet |
| F11-TypeScript专家 | 类型系统、泛型、高级类型 | Sonnet |
| F12-JavaScript专家 | ES6+、异步模式、Node.js | Sonnet |

**核心能力**:
- Python: 惯用法、性能优化、异步编程
- TypeScript: 严格类型、泛型、类型推导
- JavaScript: 现代语法、Promise/async、函数式编程

</details>

<details>
<summary><b>质量保障层 (3人)</b></summary>

| 智能体 | 职责 | 模型 |
|--------|------|------|
| F13-代码审查专家 | 代码质量、安全审查、可维护性 | Sonnet |
| F14-测试工程师 | 单元测试、集成测试、E2E测试 | Sonnet |
| F15-性能工程师 | 性能分析、瓶颈优化、缓存策略 | Opus |

**核心能力**:
- 代码审查: SOLID原则、设计模式、安全漏洞
- 自动化测试: Jest, Pytest, Playwright
- 性能优化: Profiling, 缓存, 数据库优化

</details>

<details>
<summary><b>调试排查层 (2人)</b></summary>

| 智能体 | 职责 | 模型 |
|--------|------|------|
| F16-调试专家 | 错误诊断、断点调试、问题修复 | Sonnet |
| F17-错误侦探 | 日志分析、错误模式识别 | Sonnet |

**核心能力**:
- 调试工具: Chrome DevTools, pdb, gdb
- 日志分析: 错误模式识别、根因分析
- 问题修复: 系统性修复、防止复发

</details>

<details>
<summary><b>团队管理层 (1人)</b></summary>

| 智能体 | 职责 | 模型 | 特殊工具 |
|--------|------|------|----------|
| FF-开发组组长 | 项目规划、任务分配、质量把控 | Sonnet | Task (编排) |

**核心能力**:
- 项目管理: WBS分解、里程碑定义、进度跟踪
- 任务分配: 智能体调度、并行优化
- 质量把控: 质量门控、验收标准
- 团队协作: 跨组协调、资源调配

**特殊说明**: FF是唯一拥有`Task`工具的智能体,负责协调所有F0-F17智能体

</details>

## 🛠️ 命令与技能

### 命令 (6个)

#### Next.js工具链 (4个)

| 命令 | 功能 | 使用场景 |
|------|------|----------|
| nextjs-scaffold | Next.js项目脚手架 | 创建新的Next.js项目 |
| nextjs-component-generator | 组件生成器 | 快速创建React组件 |
| nextjs-api-tester | API测试工具 | 测试Next.js API路由 |
| nextjs-performance-audit | 性能审计 | 分析和优化性能 |

#### Supabase工具链 (2个)

| 命令 | 功能 | 使用场景 |
|------|------|----------|
| supabase-data-explorer | 数据浏览器 | 查询和管理Supabase数据 |
| supabase-performance-optimizer | 性能优化器 | 优化数据库查询和索引 |

### 技能包 (1个)

| 技能包 | 功能描述 |
|--------|----------|
| webapp-testing | Web应用测试工具包 - Playwright集成,支持UI测试、网络监控、截图、日志查看 |

## 📦 安装配置

### 方法1: 项目级安装 (推荐)

1. **保持插件在项目目录**:
   ```
   plugins/开发组/
   ```

2. **配置项目级设置** (`.claude/settings.json`):
   ```json
   {
     "enabledPlugins": ["./plugins/开发组"]
   }
   ```

3. **重启Claude Code**

### 方法2: 全局安装

1. **复制到全局插件目录**:
   ```bash
   cp -r plugins/开发组 ~/.claude/plugins/development-team
   ```

2. **配置全局设置** (`~/.claude/settings.json`):
   ```json
   {
     "enabledPlugins": ["development-team"]
   }
   ```

3. **重启Claude Code**

## 🚀 使用指南

### 智能体调用方式

#### 1. 自动委派 (推荐)

Claude会根据任务内容自动选择合适的智能体:

```
用户: "帮我设计一个用户登录功能的PRD"
→ Claude自动委派给 F0-产品经理

用户: "优化这段Python代码的性能"
→ Claude自动委派给 F10-Python专家

用户: "审查这个PR的代码质量"
→ Claude自动委派给 F13-代码审查专家
```

#### 2. 显式调用

使用Task工具明确指定智能体:

```python
# 调用产品经理
Task(subagent_type="F0-产品经理",
     prompt="分析用户需求,编写PRD文档")

# 调用前端开发
Task(subagent_type="F1-前端开发",
     prompt="开发React登录组件")

# 调用组长编排多个智能体
Task(subagent_type="FF-开发组组长",
     prompt="为新功能制定完整的开发计划")
```

### 多智能体协作

#### 场景1: Web应用全栈开发

```yaml
需求阶段: [F0-产品经理]
设计阶段: [F2-UI设计师, F5-后端架构师, F6-数据库架构师, F9-架构评审]
开发阶段: [F1-前端开发, F3-全栈开发, F10-Python专家, F11-TypeScript专家]
测试阶段: [F13-代码审查专家, F14-测试工程师, F15-性能工程师]
部署阶段: [F8-云架构师, F4-文档报告生成]
```

#### 场景2: 性能优化项目

```yaml
诊断阶段: [F15-性能工程师, F16-调试专家, F17-错误侦探]
优化阶段: [F10-Python专家, F11-TypeScript专家, F12-JavaScript专家, F6-数据库架构师]
验证阶段: [F14-测试工程师, F15-性能工程师]
文档阶段: [F4-文档报告生成]
```

#### 场景3: Bug修复与问题排查

```yaml
问题定位: [F16-调试专家, F17-错误侦探]
代码修复: [F10-Python专家, F11-TypeScript专家, F12-JavaScript专家]
测试验证: [F14-测试工程师]
代码审查: [F13-代码审查专家]
```

### 输出路径规范

所有智能体的输出遵循统一路径规范:

```
output/[项目名]/[智能体名]/
├── plans/              # 执行计划配置 (JSON/YAML)
├── results/            # 执行结果 (代码、文档、报告)
├── logs/               # 执行日志
└── metadata/           # 元数据 (版本、参数、追溯)
```

**示例**:
```
output/用户登录功能开发/F0-产品经理/
├── plans/login-feature-prd.json
├── results/用户登录功能PRD.md
├── logs/execution.log
└── metadata/version.json

output/用户登录功能开发/F1-前端开发/
├── plans/login-component-plan.json
├── results/LoginForm.tsx
├── logs/build.log
└── metadata/dependencies.json
```

## 📁 项目结构

```
plugins/开发组/
├── .claude-plugin/
│   └── plugin.json           # 插件元数据
├── agents/                   # 19个智能体
│   ├── F0-产品经理.md
│   ├── F1-前端开发.md
│   ├── F2-UI设计师.md
│   ├── ...
│   ├── F17-错误侦探.md
│   └── FF-开发组组长.md
├── commands/                 # 6个命令
│   ├── nextjs-scaffold.md
│   ├── nextjs-component-generator.md
│   ├── nextjs-api-tester.md
│   ├── nextjs-performance-audit.md
│   ├── supabase-data-explorer.md
│   └── supabase-performance-optimizer.md
├── skills/                   # 1个技能包
│   └── webapp-testing/
│       └── SKILL.md
├── hooks/
│   └── hooks.json           # 钩子配置
├── scripts/                 # 工具脚本
├── .mcp.json               # MCP服务器配置
├── README.md               # 本文件
├── CHANGELOG.md            # 版本历史
└── LICENSE                 # MIT许可证
```

## 🎯 最佳实践

### 1. 选择合适的智能体

```yaml
需求不明确:
  → F0-产品经理 (PRD文档、需求分析)

UI/UX设计:
  → F2-UI设计师 (界面设计、交互流程)

前端开发:
  简单组件 → F1-前端开发
  全栈应用 → F3-全栈开发

后端开发:
  新架构 → F5-后端架构师 + F9-架构评审
  数据库 → F6-数据库架构师
  API → F7-API文档生成
  云部署 → F8-云架构师

编程优化:
  Python → F10-Python专家
  TypeScript → F11-TypeScript专家
  JavaScript → F12-JavaScript专家

质量保障:
  代码审查 → F13-代码审查专家
  测试 → F14-测试工程师
  性能 → F15-性能工程师

问题排查:
  调试 → F16-调试专家
  日志分析 → F17-错误侦探

复杂项目:
  → FF-开发组组长 (多智能体编排)
```

### 2. 并行执行策略

```yaml
架构设计并行:
  - F5-后端架构师
  - F6-数据库架构师
  - F8-云架构师

开发实现并行:
  - F1-前端开发
  - F10-Python专家 (后端API)
  - F6-数据库架构师 (数据库脚本)

质量保障并行:
  - F13-代码审查专家
  - F14-测试工程师
  - F15-性能工程师
```

### 3. 质量门控

每个阶段设置质量检查点:

```yaml
需求评审:
  - F0的PRD必须通过F9架构评审

代码评审:
  - F13代码审查必须通过

测试通过:
  - F14测试工程师所有测试用例通过

性能达标:
  - F15性能工程师确认性能指标达标
```

## 🔧 系统需求

- **Claude Code版本**: v1.0.124+
- **推荐模型**: Sonnet 4.5 (部分智能体使用Opus/Haiku)
- **必需工具**: Task, Read, Write, Edit, Grep, Glob, Bash

## 📊 成功指标

### 项目成功标准
- **按时交付率**: ≥90%
- **质量达标率**: 100% (所有质量门控通过)
- **用户满意度**: ≥8/10
- **缺陷密度**: ≤5个/千行代码

### 团队效能指标
- **智能体利用率**: 各智能体工作负载均衡
- **并行效率**: 并行任务比例 ≥60%
- **返工率**: ≤10%
- **知识复用率**: ≥30%

## 📝 版本信息

- **当前版本**: v2.0.0
- **最后更新**: 2025-11-01
- **兼容性**: Claude Code v1.0.124+
- **智能体数量**: 19个
- **命令数量**: 6个
- **技能包数量**: 1个

## 🔗 相关资源

- **更新日志**: [CHANGELOG.md](CHANGELOG.md)
- **许可证**: [LICENSE](LICENSE)
- **项目主页**: [ZTL数智化作战中心](../../README.md)
- **全局配置**: [~/.claude/CLAUDE.md](~/.claude/CLAUDE.md)

## 🤝 支持与贡献

- **问题反馈**: [GitHub Issues](https://github.com/ztl-digital/development-team-plugin/issues)
- **功能建议**: 欢迎提交Pull Request
- **文档**: 查看各智能体的详细文档 (`agents/` 目录)

---

**创建者**: ZTL Digital Intelligence Operations Center
**插件类型**: 专业领域插件 (开发组)
**状态**: 生产就绪
**模式**: 多智能体协作编排
