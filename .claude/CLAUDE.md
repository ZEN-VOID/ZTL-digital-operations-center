# ZTL数智化作战中心 - 系统架构配置文档

> Claude Code框架智能体系统总配置文档

---

## 目录导航

1. [系统概述](#系统概述)
2. [系统AGENTS说明](#系统agents说明)
3. [系统COMMANDS说明](#系统commands说明)
4. [三层架构标准](#三层架构标准)
5. [执行流程标准](#执行流程标准)
6. [Agents与Skills关系](#agents与skills关系)
7. [目录结构规范](#目录结构规范)
8. [开发标准](#开发标准)

---

## 系统概述

### 核心定位

ZTL数智化作战中心基于Claude Code框架，采用**智能体编排+能力包执行**的分层架构：

- **Agents (智能体)**: 角色化的决策和编排层
- **Skills (技能包)**: 自包含的工具/流程能力包
- **Commands (斜杠命令)**: 快速触发的工作流程
- **Hooks (钩子函数)**: 事件驱动的自动化

### 技术栈

```yaml
项目定位: 餐饮行业数智化管理平台
核心技术:
  - 智能引擎: Claude Sonnet 4.5
  - 开发框架: Claude Code
  - 编程语言: Python 3.10+, Markdown
  - 集成能力: MCP协议, OpenRouter API
```

---

## 系统AGENTS说明

### F系列通用框架智能体

F系列智能体是Claude Code框架的基础设施建设者，负责开发工具、系统能力和智能体工程的全生命周期管理。

| 快捷键 | 智能体名称 | 功能定位 | 文件路径 |
|-------|-----------|---------|----------|
| F1 | Agents智能体创建工程师 | 专家级subagent创建，基于2025最新prompt engineering规范和context engineering原则 | `.claude/agents/system/F1-Agents智能体创建工程师.md` |
| F2 | Commands斜杠命令创建工程师 | 自定义斜杠命令设计、创建和优化，支持参数化、Bash执行和文件引用 | `.claude/agents/system/F2-Commands斜杆命令创建工程师.md` |
| F3 | Hooks创建工程师 | 事件驱动钩子系统开发，提供从设计到调试的全流程指导 | `.claude/agents/system/F3-Hooks创建工程师.md` |
| F4 | Output-style输出样式设计师 | 自定义输出格式配置，基于2025最新output styles规范 | `.claude/agents/system/F4-Output-style输出样式设计师.md` |
| F5 | Skills技能包创建工程师 | 自包含技能包开发，基于渐进披露和官方规范 | `.claude/agents/system/F5-Skills技能包创建工程师.md` |
| F6 | API工具创建工程师 | 基于E5 Nano Banana最佳实践的三层架构API工具标准化创建 | `.claude/agents/system/F6-API工具创建工程师.md` |
| F7 | Python开发专家 | 现代Python生态系统开发，遵循KISS和YAGNI原则 | `.claude/agents/system/F7-Python开发专家.md` |
| F8 | FastMCP开发专家 | 符合MCP协议规范的高性能服务器开发 | `.claude/agents/system/F8-FastMCP开发专家.md` |
| F9 | OpenAI-Agent-SDK开发专家 | 基于OpenAI Agent框架和Swarm多智能体系统开发 | `.claude/agents/system/F9-OpenAI-Agent-SDK开发专家.md` |
| F10 | 文档管理员 | 确保项目文档与代码同步，智能归类README vs CLAUDE.md | `.claude/agents/system/F10-文档管理员.md` |
| F11 | 上下文管理员 | 智能决策者，将经验、决策、错误分配到机器级/系统级/项目级知识库 | `.claude/agents/system/F11-上下文管理员.md` |
| F12 | 测试工程师 | 质量守门员，通过自动化测试、覆盖率管理确保代码质量 | `.claude/agents/system/F12-测试工程师.md` |
| F13 | 学习工程师 | 践行"知行合一"，通过ASDW学习闭环(What-Why-How-Wield)转化为系统改进 | `.claude/agents/system/F13-学习工程师.md` |
| F14 | Claude-code寻路者 | 技术资源探路者，使用GitHub搜索发现和推荐高质量项目、库和学习资源 | `.claude/agents/system/F14-Claude-code寻路者.md` |
| FF | 系统总指挥官 | F系列总指挥，负责智能体工程、开发工具和系统能力的战略规划和智能调度 | `.claude/agents/system/FF-系统总指挥官.md` |

**使用说明**：
- **调用方式**: 通过Task工具指定`subagent_type`参数调用对应智能体
- **编排协作**: FF作为总指挥可智能编排F1-F14协同完成复杂工程任务
- **独立上下文**: 每个F系列智能体拥有独立上下文窗口，保护主对话上下文

---

## 系统COMMANDS说明

### 上下文与学习管理类

专注于项目认知、问题分析、知识积累和智慧沉淀的学习型命令。

| 快捷键 | 命令名称 | 功能定位 | 版本 |
|-------|---------|---------|------|
| /A | ASDW学习系统 - What (是什么) | ASDW学习系统第一步，通过现状考察和目标识别建立项目认知基础 | v2.0.0 |
| /S | ASDW学习系统 - Why (为什么) | ASDW第二步，通过内外因深度分析定位问题根源和优化机会 | v2.0.0 |
| /D | ASDW学习系统 - How (怎么做) | ASDW第三步，通过方法论研究和实践策略制定，将理论理解转化为可执行的行动方案 | v2.0.0 |
| /W | ASDW学习系统 - Wield (整合执行) | ASDW第四步，将ASD三阶段的学习成果整合并转化为实际的系统改进和配置优化 | v2.0.0 |
| /C | 基于文档化结构的有机生长注意力管理 | 支持持续更新和自然演进的注意力管理系统 | v2.0.0 |
| /V | 高级压缩引擎 | 专注于信息压缩、编排优化和智能去重 | v2.0.0 |
| /X | MANUS错误纠正与学习优化 | 基于MANUS技巧的错误纠正、学习与适应优化系统 | v2.0.0 |
| /Z | 主动学习的知识积累系统 | 知识积累、技术洞察与智慧沉淀 | v2.0.0 |

### 执行与状态管理类

专注于任务执行、项目状态同步和系统配置管理的操作型命令。

| 快捷键 | 命令名称 | 功能定位 | 版本 |
|-------|---------|---------|------|
| /E | PRP生成与执行引擎 | 端到端PRP工作流：研究 → 生成 → 执行，实现一次性成功的功能开发 | v2.0.0 |
| /F | PRP快速创建 | 快速生成功能规划文档，专注研究和规划阶段，不执行实现 | v2.0.0 |
| /R | 完整的并行执行工作流 | 环境准备 → 并行执行，实现多方案探索 | v2.0.0 |
| /M | 项目级CLAUDE.md自动更新 | 自动扫描项目专属智能体、命令和目录结构，同步更新项目级CLAUDE.md | v2.0.0 |
| /N | 系统级CLAUDE.md自动更新 | 自动扫描框架通用智能体和系统命令，同步更新系统级CLAUDE.md | v2.0.0 |
| /B | 机器级配置管理与同步 | 管理和更新机器级Claude配置文件，实现跨所有框架和项目的全局配置管理和自动同步 | v2.0.0 |
| /Q | 全面分析项目结构 | 全面分析项目结构、目标和关键文件，建立深度项目理解 | v2.0.0 |

### 代码与项目管理类

专注于代码生成、项目构建、版本控制和自动化的工程型命令。

| 快捷键 | 命令名称 | 功能定位 | 版本 |
|-------|---------|---------|------|
| /I | 自动生成GitHub专业主页级README | 自动生成包含徽章系统、技术栈说明、功能特性、使用指南和数据可视化的README。执行前自动更新trees目录快照 | v2.0.0 |
| /O | 自动生成项目OVERVIEW.md | 提供全面的项目架构、智能体系统、命令系统、技术栈和开发指南的深度文档 | v2.0.0 |
| /Y | Issue分析、修复和关闭 | 系统化的Issue分析、修复和关闭流程，确保问题解决的完整性和可追溯性 | v2.0.0 |
| /G | 完整同步推送到GitHub | 将本地项目完整同步推送到GitHub仓库，确保远程与本地完全一致 | v2.0.0 |
| /H | GitHub仓库创建与初始化 | 自动化GitHub仓库创建、初始化和首次推送流程，支持公开/私有仓库配置 | v2.0.0 |
| /P | 多工作区文件智能同步 | 实现多工作区项目间的文件/文件夹智能同步，基于配置文件进行目标识别和批量操作 | v2.0.0 |
| /T | TodoWrite任务拆解与执行 | 对指定内容启用TodoWrite工具进行任务拆解和执行，配合日志监控和Hooks自动化 | v2.0.0 |
| /U | 清理并行工作空间 | 清理trees/目录中的并行工作空间，删除所有worktree和对应分支，保留trees目录本身和README.md文档 | v2.0.0 |
| /J | HTML数据可视化生成器 | 将数据内容转化为专业的HTML可视化页面，支持15+图表类型和4种设计风格 | v2.0.0 |
| /K | 基于chrome-mcp的浏览器自动化 | 浏览器自动化操作，支持页面导航、元素交互、数据采集和测试验证 | v2.0.0 |
| /L | Windows系统自动化 | 基于windows-mcp的Windows系统自动化操作，支持应用控制、UI交互、文件管理和PowerShell执行 | v2.0.0 |

---

## 三层架构标准

### 架构总览

根据Claude Code官方设计理念，智能体系统遵循明确的三层架构：

```yaml
Layer 1 - 知识层 (Agents + Skills):
  角色:
    - Agents: 提供角色决策框架和专业领域知识
    - Skills: 提供工具/流程能力包和执行引擎

  位置:
    - .claude/agents/  (智能体配置)
    - .claude/skills/  (技能包)

  特征:
    - 静态: Claude通过"读取"获得"身份认知"和"能力认知"
    - Agents提供"我是谁,我做什么"的角色定位
    - Skills提供"能力说明,(可选)如何执行"

  交互:
    - 通过工具调用(Read等)
    - 加载能力包
    - 接收指令,设置上下文

Layer 2 - 决策编排层 (Claude Reasoning):
  本质: Claude Sonnet 4.5运行时

  流程步骤:
    1. 理解用户需求
    2. 发现可用资源(搜索Agents和Skills)
    3. 构建决策和执行框架
    4. 能力编排
    5. 动态执行能力包
    6. 监控反馈

  特征:
    - 非静态: "决策过程"本身不是文件
    - 是运行时,不是配置
    - 是智能层,连接知识和执行

  交互:
    - 运行时推理(非代码调用)
    - 动态组合
    - 工具发现与调用

Layer 3 - 执行输出层 (Tools + Output):
  执行工具:
    - Bash: 命令行执行
    - Python: 代码运行
    - API: 外部调用
    - MCP: 协议工具(扩展外部系统集成)
    - Read/Write/Edit: 文件操作

  输出目录:
    - output/: 按业务分类存储
    - reports/: 执行报告
    - logs/: 执行日志

  特征:
    - 是"实际执行"与"最终结果产出"
    - 持续更新的工作区
    - 真实产出物

  交互:
    - 真实执行(调用真实工具或API)
    - 持续输出数据
    - 结果持久化
```

### 架构层级关系

```
用户需求层级
  ↓
Layer 1 知识层(Agents+Skills提供知识)
  ↓
Layer 2 决策编排层(Claude运行时决策)
  ↓
Layer 3 执行输出层(工具执行+输出结果)
```

### 常见误区

#### ❌ 错误理解 1:

```yaml
误区1: "Agents输出plan文件"
  错误: Agents不应输出静态文件
  正确: Agents在运行时提供决策框架,Claude动态生成执行代码

误区2: "Skills执行plan"
  错误: Skills不是plan的被动执行器
  正确: Skills是包含知识+工具的主动能力包,Claude读取后调用其工具

误区3: "output是plan的存储"
  错误: output不存储计划
  正确: output存储执行结果和产出物
```

#### ✅ 正确理解:

```yaml
Agents角色:
  - 定位: 智能体决策者身份
  - 内容: 角色定位、专业领域指导
  - 输出: 运行时决策框架(非静态文件)
  - 调用: 用户通过Task工具主动调用

Skills角色:
  - 定位: 自包含能力包
  - 内容: SKILL.md(说明) + scripts/(执行引擎)
  - 输出: 执行结果(通过工具调用)
  - 调用: Claude自动发现调用

Output角色:
  - 定位: 结果存储层
  - 内容: 报告、图片、数据等
  - 输出: 持续更新的工作产出/项目文档
  - 调用: 被动存储
```

---

## 执行流程标准

### 通用执行流程(标准化流程)

通用项目智能体调用的执行流程:

```

 1. 用户需求层级
    - 明确问题描述
    - 提供必要上下文
                ↓


 2. Layer 1: 知识发现

  Claude自动执行:
    Skills Discovery
    - 扫描.claude/skills/目录
    - 匹配description搜索
    - 读取匹配SKILL.md

    Agent Reading
     - 如有必要读取智能体
     - 获取专业领域指导
     - 加载工具配置
                ↓


 3. Layer 2: 运行时决策

  Claude推理:
    理解: 分析用户需求层级
    编排: Agent(角色) + Skill(工具/流程)
    计划: 明确执行策略
    验证: 检查可行性
    编码: 生成动态调用代码
                ↓


 4. Layer 3: 工具执行

  $根据能力类型:

  路径A - 直接执行 (通用工具)
    Claude调用
    Bash工具调用
    Python代码执行
    API调用(可选)

  路径B - 引擎执行 (含API能力,如AIGC)
    Claude生成JSON执行配置
    调用Skills内置执行引擎
    执行引擎调用API
    调用外部API
    返回结果
                ↓


 5. 结果与反馈

    结果存储output/目录
    - 持续更新工作产出/项目文档
    - 按业务分类存储

    反馈给Claude
    - 执行状态
    - 错误信息
    - 常见误区

    呈现给用户
     - 总结执行结果
     - 提供下一步操作指引

```

### AIGC智能体流程(特殊化)

以创意组AIGC智能体(V3-V6)为例的能力包执行流程:

```
用户需求层级: "生成一张海报"
  ↓

 Skills自动发现
 text-to-image/SKILL.md
 - 匹配常见误区: "文生图","海报"
 - 读取API调用说明
              ↓


 Agent角色赋能
 V3-AIGC文生图设计师.md
 - 读取角色认知与专业知识
 - 提供参数优化建议
 - 指导调用最佳策略
              ↓


 Claude运行时决策
 - 分析输入需求与上下文: 1-poster
 - 编排:角色(专业调参指导)+能力包(工具引擎)
 - 生成执行代码/配置
              ↓


 执行引擎调用
 Skills内置scripts/
 - banana_api_core.py
 - OpenRouter API调用
 - Gemini 2.5 Flash生成
              ↓


 结果输出
 output/images/e1-text-to-image/
 - 接收Base64编码图
 - 解码存储PNG文件
 - 记录元数据:提示词、参数等

```

---

## Agents与Skills关系

### 定位对比

| 维度 | Agents智能体 | Skills技能包 |
|-----|-------------|-------------|
| **定位(Positioning)** | 智能体决策者身份 | 工具能力包 |
| **调用方式** | 用户主动 | Claude发现 |
| **输出内容** | 角色定位+专业领域指导 | 工具/流程+执行引擎 |
| **调用方式** | 用户通过Task | Claude自动发现 |
| **流程定位** | "我是谁?我做什么?" | "能力说明?如何调用?" |
| **位置** | 固定配置目录 | 动态检索 |
| **示例** | V3-AIGC文生图设计师 | text-to-image Skill |

### 协作关系

```yaml
单独调用 (AIGC创意类):
  V3-AIGC文生图设计师 → text-to-image Skill
  V4-AIGC图生图设计师 → image-to-image Skill
  V5-AIGC图片识别分析师 → image-recognition Skill
  V6-AIGC高级图片处理师 → advanced-processing Skill

复合调用 (情报类):
  E0-情报任务需求拆解员 调度 → {
    web-scraping Skill,
    data-analysis Skill,
    report-generation Skill
  }

共享调用 (行政事务):
  {
    R1-财务管理员,
    R2-人事管理员,
    R4-秘书
  } → excel-data-analyzer Skill
```

### Skills自包含设计

根据Anthropic官方文档，Skills应该是/**自包含的能力包**:

```yaml
Skills目录结构:
  skill-name/
    ├── SKILL.md              # 必需: 能力说明
    │   ├── YAML frontmatter  # name + description
    │   ├── Quick Start       # 快速开始:示例
    │   └── API Reference     # 详细参数
    │
    ├── scripts/              # 推荐: 执行引擎
    │   ├── core_engine.py    # 核心引擎
    │   ├── helpers.py        # 辅助函数
    │   └── __init__.py       # Python模块
    │
    ├── templates/            # 可选: 模板文件
    ├── reference.md          # 可选: 扩展说明
    └── README.md             # 可选: 项目说明

常见误区vs正确理解:
  1. ❌ 执行引擎Δ(Skills外部 (scripts/)
  2. ❌ 通过符号链接引用外部代码库
  3. ✅ 将执行代码*Skill目录内,实现自包含
  4. ✅ 允许在共享核心库(如_shared/)
  5. ✅ 遵循渐进披露原则
```

### 渐进披露原则

Skills信息分层加载机制,按需提供不同详细程度的知识:

```yaml
Level 1 - Metadata (最小元数据):
  位置: SKILL.md的YAML frontmatter
  大小: ~50 tokens
  内容: name + description
  特征: Claude根据"能力"("匹配")

Level 2 - Core Instructions (核心指令文档):
  位置: SKILL.md本体
  大小: ~500-2000 tokens
  内容: 快速开始、核心API、示例
  特征: 提供"能力说明"("如何调用")

Level 3 - Extended Context (扩展上下文):
  位置: reference.md, 其他附加文档
  大小: ~1000-5000 tokens/文件
  内容: 详细API、高级配置、架构设计
  特征: 深度专业能力的"完整知识库"

Level 4 - Executable Code (可执行代码):
  位置: scripts/目录
  大小: 依赖实际代码
  内容: 真实执行引擎、Python/Bash代码
  特征: 持续更新的工作区,Claude可执行
```

---

## 目录结构规范

### 目录树概览

```
项目根目录/
├── .claude/
│   ├── agents/              # 智能体配置
│   │   ├── system/          # F系列: Framework智能体
│   │   ├── 战略组/          # G系列: 战略智能体
│   │   ├── 创意组/          # X系列: 创意智能体
│   │   ├── 情报组/          # E系列: 情报智能体
│   │   ├── 中台组/          # M系列: 数据中台智能体
│   │   ├── 行政组/          # R系列: 行政智能体
│   │   └── 筹建组/          # Z系列: 筹建智能体
│   │
│   ├── skills/              # 技能包
│   │   ├── aigc/            # AIGC相关Skills
│   │   ├── figma/           # Figma设计
│   │   └── [其他Skills]
│   │
│   ├── commands/            # 斜杠命令
│   └── hooks/               # 钩子函数
│
├── output/                  # 输出层
│   ├── 战略组/
│   ├── 创意组/
│   ├── 情报组/
│   └── [其他业务组]/
│
├── project/                 # 项目规划文档
│   └── prp-*.md            # PRP规划文档
│
├── reports/                 # 执行结果报告
└── CLAUDE.md               # 系统配置文档
```

### 命名规范

```yaml
Agents命名:
  格式: [字母][数字序号]-名称
  示例:
    - G0-战略需求解析师
    - X3-平面设计师
    - E1-公开资料调研员

  字母前缀分类:
    - F: Framework (框架通用)
    - G: Group (战略组)
    - X: Creative (创意组)
    - E: Intelligence (情报组)
    - M: Middleware (中台组)
    - R: Administration (行政组)
    - Z: Construction (筹建组)

Skills命名:
  格式: kebab-case (全小写-横杠分隔)
  示例:
    - text-to-image
    - excel-data-analyzer
    - pdf-processing

  要求:
    - 语义清晰 (不超过30字符)
    - 用连字符 (不使用t2i)
    - 避免缩写

Output命名:
  格式: [业务组]/[功能模块]/[时间戳]_[描述]
  示例:
    - 创意组/images/e1-text-to-image/20251020_103000_poster.png
    - 情报组/reports/competitor-analysis-20251020.md
```

### 文档标准

```yaml
Agents文档结构:
  必需字段:
    - 定位与核心职责
    - 角色认知与专业知识
    - 工具配置与核心能力
    - 工作流程
    - 输出规范

Skills文档结构:
  必需字段:
    - YAML frontmatter (name, description)
    - Quick Start
    - API Reference (可选)
    - Examples

  可选附加:
    - reference.md (扩展说明)
    - scripts/ (执行引擎)
    - templates/ (模板文件)

代码规范:
  - Python: Docstring (Google格式)
  - Markdown: 数学公式标准
  - 常见误区;确保专业词汇统一
```

### Git工作流程

```yaml
分支策略:
  - main: 稳定主分支,生产就绪
  - feature/*: 功能开发分支
  - hotfix/*: 紧急修复分支

提交规范:
  格式: <type>(<scope>): <subject>

  类型标记:
    - feat: 新功能
    - fix: 修复
    - docs: 文档
    - refactor: 重构
    - test: 测试
    - chore: 构建/工具

  示例:
    - feat(agents): 新增G3-产品力打造专家智能体
    - fix(skills): 修复text-to-image调用错误
    - docs(claude): 更新三层架构说明

Hooks位置:
  - pre-compact: 上下文压缩前自动备份
  - user-prompt-submit: 提示词提交
```

---

## 开发标准

### 相关文档

- [AIGC技能包架构](.claude/skills/aigc/ARCHITECTURE.md)
- [Skills技能包创建工程师](.claude/agents/system/F5-Skills技能包创建工程师.md)
- [代码迁移PRP](project/prp-skills-code-migration-to-self-contained.md)

### 版本历史

```yaml
v2.0 (2025-10-21):
  - 修正三层架构定义理解
  - 明确Agents与Skills关系
  - 整合标准执行流程
  - 集成F系列智能体说明
  - 集成系统Commands说明

v1.0 (2025-10-20):
  - 初始三层架构定义
  - 建立Agents与Skills关系
  - 定义标准执行流程
  - 规范目录结构

v0.1 (2024-12):
  - 项目启动
  - 初始化项目结构
```

---

**项目名称**: ZTL数智化作战中心
**最后更新**: 2025-10-21
**兼容版本**: Claude Code v1.0+, Sonnet 4.5
