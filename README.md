# ZTL数智化作战中心

<div align="center">

![Version](https://img.shields.io/badge/version-v2.1.2-blue.svg)
![Claude Code](https://img.shields.io/badge/Claude_Code-v1.0+-orange.svg)
![Sonnet](https://img.shields.io/badge/Claude-Sonnet_4.5-purple.svg)
![Python](https://img.shields.io/badge/Python-3.10+-green.svg)
![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)
![MCP](https://img.shields.io/badge/MCP-Protocol-red.svg)

**餐饮行业数智化转型的智能体协作平台**

基于Claude Code + Sonnet 4.5 + MCP生态的多智能体系统，提供从战略规划到门店筹建的全链路数智化支持

[快速开始](#-快速开始) • [智能体系统](#-智能体系统) • [命令系统](#-命令系统) • [技术架构](#-技术架构)

</div>

---

## 📖 项目简介

ZTL数智化作战中心是一个基于Claude Code和多智能体协作的餐饮行业数智化转型平台。通过**8大业务组**和**67个专业智能体**的协同工作，实现从战略规划、品牌营销、数据分析、行政管理、运营中台、门店筹建到系统开发的**全链路数智化支持**。

### 核心价值

- 🎯 **智能决策**: 基于Claude Sonnet 4.5的深度推理能力
- 🤖 **多智能体协作**: 66个业务智能体 + 1个指挥智能体协同工作
- 🔌 **MCP生态集成**: 7+ MCP服务器无缝对接外部系统
- 📊 **数据驱动**: 全流程数据采集、分析和可视化
- 🚀 **快速响应**: 通过17+斜杠命令实现一键式工作流
- 🔄 **持续进化**: Hooks系统和上下文管理支持自动化
- 🪝 **零损失**: PreCompact Hook自动保存上下文并启动并行实例

---

## ✨ 核心特性

### 1. 八大业务组智能体系统

- **战略组 (G系列)** - 9个智能体：战略规划、经营分析、产品力打造、精细化管理
- **创意组 (X系列)** - 10个智能体：广告策划、文案创作、平面设计、AIGC图片生成、视频制作
- **情报组 (E系列)** - 8个智能体：深度调研、Chrome网页采集、Playwright爬虫、数据管理
- **筹建组 (Z系列)** - 6个智能体：平面图设计、BIM建模、空间设计、动画渲染
- **开发组 (F系列)** - 11个智能体：产品经理、前后端开发、数据库、API、测试、版本控制、云部署
- **美团组 (V系列)** - 6个智能体：美团管家运营、营销、供应链、数据报表、网页自动化
- **供应组 (C系列)** - 7个智能体：采购执行、库存管理、成本卡管理、供应商管理、分账管理
- **行政组 (R系列)** - 9个智能体：财务管理、人事管理、法务支持、飞书协同、文件管理

### 2. Hooks自动化系统

**PreCompact Hook** - 零人工干预的上下文保护和并行协作：

- ✅ **自动保存上下文**: 在Compact前自动保存完整对话快照到 `context/snapshots/`
- ✅ **并行实例启动**: 自动创建新iTerm窗口并启动Claude
- ✅ **上下文注入**: 自动将上下文摘要注入到新实例
- ✅ **锁机制**: 防止重复执行的原子锁机制
- ✅ **深渊凝视集成**: 使用深渊凝视skill控制iTerm终端

**效果**:
- 上下文保留: ❌ 部分丢失 → ✅ 100%保留
- 任务连续性: ❌ 中断 → ✅ 无缝衔接
- 并行能力: ❌ 不支持 → ✅ 支持
- 启动时间: 🐢 ~2分钟 → ⚡ ~25秒

### 3. 17个斜杠命令系统

一键式工作流程，覆盖上下文管理、执行控制和项目管理：

- **PRP工作流**: `/prp` - 生成PRP文档 (研究+规划)
- **测试验证**: `/test` - 运行完整测试套件并迭代修复
- **上下文管理**: `/context-aware` - 8维度项目分析, `/manus` - 统一上下文管理
- **项目管理**: `/github-pull` - GitHub完整同步, `/github-issue` - Issue分析修复, `/github-start` - 仓库初始化
- **文档生成**: `/readme-generator` - 自动更新README, `/claude` - 更新CLAUDE.md配置
- **并行执行**: `/trees` - 多方案并行探索工作流
- **跨工作区同步**: `/links` - 基于相对路径的新增或覆盖操作
- **项目指令生成**: `/project-instructions` - 全面管理project/instructions文档体系

### 4. 6+技能包库

可复用的自包含能力包，支持渐进披露和自动发现：

- **全局照见**: 全局插件可视化查询系统，自动扫描和索引全局Claude Code插件
- **深渊凝视**: iTerm终端控制与输出捕获，支持新建窗口、指定窗口、多窗口管理
- **创意组技能包**: AIGC文生图、图片处理、Artifacts构建等
- **情报组技能包**: 网页爬虫、数据采集、COS存储管理
- **筹建组技能包**: Canvas设计、3D生成、空间设计、平面图规划
- **办公系列**: Word文档处理、Excel数据分析等

### 5. MCP服务集成

7+ MCP服务器提供外部系统集成：

- **chrome-devtools**: Chrome浏览器自动化 (20+ tools)
- **playwright-mcp**: Playwright深度爬虫 (30+ tools)
- **github-mcp**: GitHub操作 (25+ tools)
- **context7**: 实时库文档 (2 tools)
- **lark-mcp**: 飞书/Lark协同 (15+ tools)
- **cos-mcp**: 腾讯云COS存储 (10+ tools)
- **supabase-mcp**: Supabase PostgreSQL数据库
- **skill-seeker**: 文档抓取和技能包生成
- **chart-generator**: 图表生成工具
- **minimax-mcp**: Minimax AI能力集成

---

## 🏗️ 技术架构

### 技术栈

| 类别             | 技术          | 版本  | 用途             |
| ---------------- | ------------- | ----- | ---------------- |
| **AI引擎** | Claude Sonnet | 4.5   | 核心推理引擎     |
| **框架**   | Claude Code   | v1.0+ | 智能体开发框架   |
| **语言**   | Python        | 3.10+ | 后端开发         |
| **语言**   | Markdown      | -     | 配置和文档       |
| **协议**   | MCP           | v1.0  | 模型上下文协议   |
| **数据库** | PostgreSQL    | -     | Supabase云数据库 |
| **存储**   | COS           | -     | 腾讯云对象存储   |
| **协作**   | Lark/Feishu   | -     | 飞书企业协同     |

### 架构模式

本项目采用**三层智能体架构**：

```
Layer 1: 知识层 (Agents + Skills)
  - Agents: 角色化决策框架和专业领域知识
  - Skills: 工具/流程能力包和执行引擎
  ↓
Layer 2: 决策编排层 (Claude Reasoning)
  - 运行时推理和动态能力组合
  - 智能路由和任务调度
  ↓
Layer 3: 执行输出层 (Tools + Output)
  - Bash, Python, API, MCP工具执行
  - 结果持久化到output/目录
```

---

## 📁 项目结构

```
ZTL数智化作战中心/
├── .claude/                    # Claude Code配置中心
│   ├── agents/                 # 通用智能体 (1个)
│   │   └── QQ-总指挥官.md
│   ├── commands/              # 斜杠命令 (17个)
│   │   ├── prp.md
│   │   ├── test.md
│   │   ├── context-aware.md
│   │   ├── manus.md
│   │   ├── github-pull.md
│   │   ├── github-issue.md
│   │   ├── github-start.md
│   │   ├── readme-generator.md
│   │   ├── claude.md
│   │   ├── trees.md
│   │   ├── links.md
│   │   ├── project-instructions.md
│   │   └── ...
│   ├── skills/                # 技能包库 (6+个)
│   │   ├── 全局照见/
│   │   ├── 深渊凝视/
│   │   └── ...
│   ├── hooks/                 # Hooks系统
│   │   ├── parallel-claude-after-compact.sh
│   │   ├── README.md
│   │   └── QUICKSTART.md
│   └── logs/                  # Hook执行日志
│
├── plugins/                   # 业务智能体插件 (8组67智能体)
│   ├── 战略组/
│   │   ├── agents/ (9个)
│   │   └── README.md
│   ├── 创意组/
│   │   ├── agents/ (10个)
│   │   ├── skills/
│   │   └── README.md
│   ├── 情报组/
│   │   ├── agents/ (8个)
│   │   └── README.md
│   ├── 筹建组/
│   │   ├── agents/ (6个)
│   │   ├── skills/
│   │   └── README.md
│   ├── 开发组/
│   │   ├── agents/ (11个)
│   │   └── README.md
│   ├── 美团组/
│   │   ├── agents/ (6个)
│   │   └── README.md
│   ├── 供应组/
│   │   ├── agents/ (7个)
│   │   └── README.md
│   └── 行政组/
│       ├── agents/ (9个)
│       └── README.md
│
├── context/                   # 上下文管理
│   └── snapshots/             # PreCompact hook上下文快照
│
├── output/                    # 智能体执行输出
│   └── [项目名]/
│       └── [agent-name]/
│           ├── plans/
│           ├── results/
│           ├── logs/
│           └── metadata/
│
├── scripts/                   # 项目脚本库
│   ├── iTerm集成/
│   └── archived/              # 归档脚本
│
├── PRPs/                      # Plan-Research-Plan文档
├── reports/                   # 执行报告和分析
├── learning/                  # 知识积累
├── trees/                     # 并行执行工作区
├── CLAUDE.md                  # 项目级配置文档
└── README.md                  # 本文件 (自动生成)
```

---

## 🚀 快速开始

### 环境要求

- **macOS**: Darwin 24.3.0+
- **Claude Code**: v1.0+
- **Python**: 3.10+
- **Git**: 2.0+

### 安装步骤

1. **克隆项目**

   ```bash
   git clone https://github.com/yourusername/ZTL数智化作战中心.git
   cd ZTL数智化作战中心
   ```
2. **配置Claude Code**

   - 确保已安装Claude Code
   - 项目配置文件位于 `.claude/`目录
3. **安装依赖** (如需要)

   ```bash
   # Python依赖
   pip install -r requirements.txt

   # MCP服务器配置
   # 参考 .claude/CLAUDE.md 中的MCP配置说明
   ```

### 使用指南

#### 通过斜杠命令使用

在Claude Code中直接调用命令：

```bash
# PRP工作流
/prp <feature-description>    # 生成PRP文档 (研究+规划)

# 测试与质量
/test                         # 运行完整测试套件并迭代修复

# 上下文管理
/context-aware                # 8维度项目全面分析
/manus                        # 统一上下文管理系统

# 项目管理
/github-pull                  # 完整同步到GitHub
/github-issue <issue-url>     # Issue分析修复
/github-start                 # GitHub仓库初始化
/readme-generator             # 自动更新README
/claude                       # 更新CLAUDE.md配置

# 并行执行
/trees <feature> <n> <desc>   # 多方案并行探索

# 跨工作区同步
/links <path1> [path2] ...    # 基于相对路径同步文件

# 项目指令
/project-instructions         # 生成project/instructions文档
```

#### 通过智能体使用

**方式1: QQ-总指挥官协调多智能体** (推荐用于复杂任务)

```python
Task(subagent_type="QQ-总指挥官",
     prompt="我需要为新开的火锅店做一个完整的开业筹备方案")
```

**方式2: 直接调用专业智能体** (用于单一领域任务)

```python
# 战略分析
Task(subagent_type="G1-经营分析优化师",
     prompt="分析本月门店经营数据")

# AIGC设计
Task(subagent_type="X5-AIGC图片生成师",
     prompt="生成火锅店开业海报")

# Chrome采集
Task(subagent_type="E2-Chrome网页采集",
     prompt="采集美团火锅店竞品数据")
```

---

## 🤖 智能体系统

### 总览

- **总计**: 67个专业智能体
- **指挥级**: 1个 (QQ-总指挥官)
- **业务级**: 66个 (分布在8大业务组)
  - 战略组 (G系列): 9个
  - 创意组 (X系列): 10个
  - 情报组 (E系列): 8个
  - 筹建组 (Z系列): 6个
  - 开发组 (F系列): 11个
  - 美团组 (V系列): 6个
  - 供应组 (C系列): 7个
  - 行政组 (R系列): 9个

### 战略组 (G系列) - 9个智能体

| ID | 名称               | 功能定位                         |
| -- | ------------------ | -------------------------------- |
| G0 | 战略需求解析师     | 战略需求收集、目标分解、任务规划 |
| G1 | 经营分析优化师     | 门店经营数据深度分析、趋势预测   |
| G2 | 产品力打造专家     | 产品体系设计、菜品研发           |
| G3 | 门店选址评估专家   | 商圈分析、选址评估               |
| G4 | 竞争情报分析师     | 竞品监测、市场动态分析           |
| G5 | 加盟政策设计师     | 加盟模式设计、政策制定           |
| G6 | 战略数据看板设计师 | 战略指标体系设计                 |
| G7 | 精细化管理专家     | SOP流程设计、操作手册            |
| GG | 战略规划总监       | 战略任务智能调度、质量把控       |

### 创意组 (X系列) - 10个智能体

| ID | 名称               | 功能定位                   |
| -- | ------------------ | -------------------------- |
| X0 | 内容创意需求分析师 | 创意需求分析、Brief输出    |
| X1 | 广告策划师         | 广告创意策划、营销Campaign |
| X2 | 文案创作师         | 品牌文案、产品文案创作     |
| X3 | Canvas图文排版师   | Canvas图文排版、菜单设计   |
| X4 | Algorithmic数字艺术设计师 | p5.js算法艺术、生成艺术 |
| X5 | AIGC图片生成师     | AIGC文生图、餐饮专业设计   |
| X6 | React前端设计师    | React artifacts构建、交互设计 |
| X7 | 品牌Style策划师    | 品牌色彩、视觉风格设计     |
| X8 | 短视频脚本创作师   | 抖音/快手/小红书脚本       |
| XX | 创意组组长         | 创意任务智能分解、质量把控 |

### 情报组 (E系列) - 8个智能体

| ID | 名称               | 功能定位                 |
| -- | ------------------ | ------------------------ |
| E0 | 情报任务需求分析员 | 情报需求解析、任务拆解   |
| E1 | 公开资料调研员     | 学术论文、技术博客调研   |
| E2 | 网站情报采集员     | Chrome MCP网站数据采集   |
| E3 | 网站深度爬虫员     | Playwright MCP企业级爬虫 |
| E4 | 深度情报分析员     | 数据清洗、语义分析       |
| E5 | 云数据库管理员     | Supabase PostgreSQL管理  |
| E6 | 云存储管理员       | 腾讯云COS存储管理        |
| EE | 情报组组长         | 情报任务智能分解、/R并行 |

### 行政组 (R系列) - 9个智能体

| ID | 名称               | 功能定位               |
| -- | ------------------ | ---------------------- |
| R0 | 办公业务需求分析员 | 行政需求分析、任务拆解 |
| R1 | 财务管理员         | 预算管理、费用报销     |
| R2 | 人事管理员         | 招聘、入离职、考勤薪酬 |
| R3 | 法务专家           | 合同审核、法律咨询     |
| R4 | 秘书               | 日程管理、会议组织     |
| R5 | 飞书管理员         | 消息推送、群聊管理     |
| R6 | 文件管理员         | 文件分类、归档存储     |
| R7 | 存储管理员         | 腾讯云COS/本地存储管理 |
| RR | 行政组组长         | 行政任务编排、质量把控 |

### 美团组 (V系列) - 6个智能体

| ID | 名称                       | 功能定位                     |
| -- | -------------------------- | ---------------------------- |
| V0 | 美团管家系统业务需求分析员 | 业务需求转化、任务拆解       |
| V1 | 美团管家运营管理员         | 餐厅/菜品/外卖管理 (11模块)  |
| V2 | 美团管家营销管理员         | 会员营销、卡券管理 (11模块)  |
| V4 | 美团管家报表管理员         | 经营分析、财务报表 (9模块)   |
| V5 | 美团管家网页自动化操作助手 | Chrome MCP网页自动化         |
| VV | 美团组组长                 | 系统战略规划、数据流程自动化 |

### 筹建组 (Z系列) - 6个智能体

| ID | 名称               | 功能定位                 |
| -- | ------------------ | ------------------------ |
| Z0 | 筹建项目需求分析师 | 新店筹建需求调研         |
| Z1 | 平面图设计师       | CAD平面图绘制            |
| Z2 | 空间设计师         | 空间设计方案             |
| Z3 | BIM建模师          | BIM模型、机电管线建模    |
| Z4 | 建筑动画师         | 建筑漫游动画、效果图渲染 |
| ZZ | 筹建组组长         | 筹建全流程管理、质量把控 |

### 开发组 (F系列) - 11个智能体

| ID | 名称               | 功能定位                     |
| -- | ------------------ | ---------------------------- |
| F0 | 产品经理           | 产品需求分析、原型设计       |
| F1 | 前端开发           | React/Vue前端应用开发        |
| F2 | 组件开发           | UI组件库开发与维护           |
| F3 | 数据库开发         | PostgreSQL/MySQL数据库设计   |
| F4 | API开发            | RESTful API设计与实现        |
| F5 | 后端开发           | Node.js/Python后端服务       |
| F6 | AI集成开发         | Claude/OpenRouter API集成    |
| F7 | 测试性能工程师     | 单元测试、性能优化           |
| F8 | 版本控制助手       | Git工作流、代码审查          |
| F9 | 云部署管理         | Docker/K8s容器化部署         |
| FF | 开发团队组长       | 技术架构、任务分配           |

### 供应组 (C系列) - 7个智能体

| ID | 名称               | 功能定位                 |
| -- | ------------------ | ------------------------ |
| C0 | 供应需求分析师     | 供应链需求分析、采购规划 |
| C1 | 采购执行经理       | 供应商对接、订单执行     |
| C2 | 库存管理员         | 库存监控、补货预警       |
| C3 | 成本卡管理员       | 菜品成本核算、成本优化   |
| C4 | 供应商管理员       | 供应商评估、关系维护     |
| C5 | 分账管理员         | 供应商结算、分账管理     |
| CC | 供应组组长         | 供应链全流程协调管理     |

---

## 📜 命令系统

### 总览

- **总计**: 17个斜杠命令
- **PRP工作流**: `/prp` - 生成PRP文档 (研究+规划)
- **测试验证**: `/test` - 运行完整测试套件并迭代修复
- **上下文管理**: `/context-aware` (8维度分析), `/manus` (统一上下文)
- **项目管理**: `/github-pull`, `/github-issue`, `/github-start`, `/readme-generator`, `/claude`
- **并行执行**: `/trees` - 多方案并行探索工作流
- **跨工作区同步**: `/links` - 基于相对路径的同步操作
- **项目指令生成**: `/project-instructions` - 管理project/instructions文档体系
- **终端测试**: `/trigger-terminal-test`, `/test-task-trigger`, `/test-session-end`

### 核心命令详解

#### PRP工作流

| 命令  | 功能             | 特点                       |
| ----- | ---------------- | -------------------------- |
| /prp  | PRP文档生成      | 研究+规划，不执行实现      |
| /test | 测试与质量验证   | 全面测试+迭代修复直到通过  |
| /trees| 并行执行工作流   | 环境准备→多方案并行探索   |

#### 上下文管理

| 命令            | 功能               | 输出                     |
| --------------- | ------------------ | ------------------------ |
| /context-aware  | 8维度项目分析      | agents/commands/hooks等  |
| /manus          | 统一上下文管理系统 | 注意力管理+错误学习      |

#### 文档管理

| 命令                 | 功能                   | 输出                     |
| -------------------- | ---------------------- | ------------------------ |
| /readme-generator    | 生成README.md          | GitHub专业主页级文档     |
| /claude              | 更新CLAUDE.md配置      | 全局和项目级配置同步     |
| /project-instructions| 生成项目指令文档       | project/instructions/    |

#### 项目管理

| 命令          | 功能              | 用途                    |
| ------------- | ----------------- | ----------------------- |
| /github-pull  | GitHub完整同步    | 确保远程与本地完全一致  |
| /github-start | GitHub仓库创建    | 自动化仓库初始化        |
| /github-issue | Issue分析修复     | 系统化Issue处理流程     |
| /links        | 跨工作区同步      | 新增或覆盖式文件同步    |

---

## 📊 项目统计

### 智能体分布

| 业务组               | 智能体数量     | 占比           |
| -------------------- | -------------- | -------------- |
| 开发组 (F系列)       | 11个           | 16.4%          |
| 创意组 (X系列)       | 10个           | 14.9%          |
| 战略组 (G系列)       | 9个            | 13.4%          |
| 行政组 (R系列)       | 9个            | 13.4%          |
| 情报组 (E系列)       | 8个            | 11.9%          |
| 供应组 (C系列)       | 7个            | 10.4%          |
| 美团组 (V系列)       | 6个            | 9.0%           |
| 筹建组 (Z系列)       | 6个            | 9.0%           |
| **业务层合计** | **66个** | **100%** |
| 指挥级 (QQ系列)      | 1个            | -              |
| **项目总计**   | **67个** | -              |

### 资源统计

| 资源类型   | 数量   | 说明                          |
| ---------- | ------ | ----------------------------- |
| 智能体文件 | 67个   | 1个指挥 + 66个业务            |
| 命令文件   | 17个   | .claude/commands/             |
| 技能包     | 6+个   | .claude/skills/               |
| Python脚本 | 70+个  | scripts/, api/                |
| MCP服务器  | 10个   | chrome-devtools, playwright等 |
| Hooks钩子  | 1个    | PreCompact自动化Hook          |

### 技术能力

- **编程语言**: Python, Markdown, JavaScript
- **数据处理**: PostgreSQL, COS云存储
- **自动化**: Chrome/Playwright浏览器自动化
- **协作平台**: 飞书/Lark集成
- **AI能力**: Claude Sonnet 4.5, OpenRouter API
- **文档系统**: Markdown, PDF, Office套件

---

## 🛣️ 开发路线图

### v2.1.x (当前版本)

- ✅ 完成agents系统性重构v2.1
- ✅ 统一智能体命名规范
- ✅ 创建8大业务组组长智能体
- ✅ 新增网页自动化智能体
- ✅ 新增意图分析图谱和路由规则
- ✅ 集成Hooks系统 (PreCompact自动化)
- ✅ 新增深渊凝视iTerm控制skill
- ✅ 扩展至67个专业智能体 (66业务+1指挥)
- ✅ 完善17个斜杠命令系统
- ✅ 集成10个MCP服务器

### v2.2 (规划中)

- ⏳ 增强AIGC技能包能力
- ⏳ 完善美团组业务流程
- ⏳ 优化情报组并行采集
- ⏳ 扩展筹建组BIM功能

### v3.0 (未来)

- 📋 多租户支持
- 📋 企业级权限管理
- 📋 实时协作能力
- 📋 移动端支持

---

## 📦 版本历史

### v2.1.2 (2025-10-30)

- ✅ 集成Hooks自动化系统 (PreCompact Hook)
- ✅ 新增深渊凝视iTerm控制skill
- ✅ 更新总智能体数量: 66业务智能体 + 1指挥智能体 = 67个
- ✅ 新增开发组 (F系列) 11个智能体
- ✅ 新增供应组 (C系列) 7个智能体
- ✅ 更新创意组数量: 9个 → 10个
- ✅ 更新行政组数量: 8个 → 9个
- ✅ 更新美团组数量: 7个 → 6个
- ✅ 更新命令系统数量: 13个 → 17个
- ✅ 更新技能包数量: 4个 → 6+个
- ✅ 更新MCP服务器数量: 7个 → 10个
- ✅ 完善README.md文档结构和统计信息

### v2.1.1 (2025-10-21)

- ✅ 新增V5-美团管家网页自动化操作助手
- ✅ 更新美团组智能体数量: 6个 → 7个
- ✅ 更新总智能体数量: 66个 → 47个 (修正统计错误)
- ✅ 完善美团组意图映射表,新增自动化操作场景

### v2.1.0 (2025-10-21)

- ✅ 完成agents系统性重构v2.1
- ✅ 统一智能体命名规范为 [字母][数字]-名称 格式
- ✅ 创建6大业务组组长智能体 (GG/XX/EE/RR/MM/ZZ)
- ✅ 整合47个项目智能体完整说明
- ✅ 新增意图分析图谱和路由规则

### v2.0.0 (2025-10-20)

- ✅ 完成F系列系统智能体创建 (15个)
- ✅ 建立三级CLAUDE.md配置体系
- ✅ 整合MCP生态 (7个服务器)

---

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

---

## 👥 贡献者

感谢所有为ZTL数智化作战中心做出贡献的开发者！

### 项目维护

- **核心开发**: Vincent Lee
- **AI引擎**: Claude Sonnet 4.5
- **技术栈**: Claude Code + MCP生态

### 如何贡献

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 🔗 相关链接

- **项目配置**: [CLAUDE.md](CLAUDE.md) - 项目级配置文档
- **系统配置**: [.claude/CLAUDE.md](.claude/CLAUDE.md) - 系统级配置文档
- **项目概览**: [OVERVIEW.md](OVERVIEW.md) - 项目架构详解
- **技能包库**: [.claude/skills/](.claude/skills/) - 可复用能力包
- **执行报告**: [reports/](reports/) - 历史执行记录

---

## 📞 联系方式

如有问题或建议，欢迎通过以下方式联系：

- **Issues**: [GitHub Issues](https://github.com/yourusername/ZTL数智化作战中心/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ZTL数智化作战中心/discussions)

---

<div align="center">

**⭐ 如果这个项目对您有帮助，请给我们一个Star！**

Made with ❤️ by ZTL Team

Powered by Claude Code + Sonnet 4.5 + MCP

</div>
