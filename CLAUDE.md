# ZTL数智化作战中心 - 项目配置文档

> 餐饮行业数智化转型的智能体协作平台
> **技术栈**: Claude Code + Sonnet 4.5 + MCP生态

---

## 📋 目录导航

- [1. 项目概述](#1-项目概述)
  - [1.1 开发物料管理规范](#11-开发物料管理规范)
- [2. 项目AGENTS说明](#2-项目agents说明)
  - [2.1 战略组 (G系列)](#21-战略组-g系列)
  - [2.2 创意组 (X系列)](#22-创意组-x系列)
  - [2.3 情报组 (E系列)](#23-情报组-e系列)
  - [2.4 行政组 (R系列)](#24-行政组-r系列)
  - [2.5 中台组 (M系列)](#25-中台组-m系列)
  - [2.6 筹建组 (Z系列)](#26-筹建组-z系列)
- [3. 意图分析图谱](#3-意图分析图谱)
- [4. 项目快捷键系统](#4-项目快捷键系统)

---

## 1. 项目概述

### 核心定位

ZTL数智化作战中心是一个基于Claude Code和多智能体协作的餐饮行业数智化转型平台。通过7大业务组(战略/创意/情报/行政/中台/筹建/框架)、60个专业智能体的协同工作,实现从战略规划、品牌营销、数据分析、行政管理、运营中台、门店筹建到系统开发的全链路数智化支持。

### 技术架构

```yaml
AI基础设施:
  核心引擎: Claude Sonnet 4.5
  开发框架: Claude Code v1.0+
  协议标准: MCP (Model Context Protocol)

智能体生态:
  系统层: .claude/agents/system/ (F系列通用框架智能体)
  业务层: G/X/E/R/M/Z/F系列 (60个) - 业务专业能力

MCP服务集成:
  - chrome-mcp: 浏览器自动化
  - playwright-mcp: 深度爬虫
  - context7: 实时文档库
  - lark-mcp: 飞书协同
  - github-mcp: 代码协作
  - cos-mcp: 云存储管理
  - supabase-mcp: 云数据库
```

### 业务矩阵

| 业务组 | 系列标识 | 智能体数量 | 核心职能                                         | 组长 |
| ------ | -------- | ---------- | ------------------------------------------------ | ---- |
| 战略组 | G系列    | 9个        | 战略规划、经营分析、产品力打造、精细化管理       | GG   |
| 创意组 | X系列    | 9个        | 广告策划、文案创作、平面设计、短视频制作         | XX   |
| 情报组 | E系列    | 8个        | 公开调研、网站采集、深度分析、数据管理           | EE   |
| 行政组 | R系列    | 8个        | 财务管理、人事管理、法务支持、飞书协同           | RR   |
| 中台组 | M系列    | 9个        | 美团管家运营、营销、供应链、报表、小程序、成本卡 | MM   |
| 筹建组 | Z系列    | 6个        | 平面图设计、BIM建模、空间设计、动画渲染          | ZZ   |
| 框架组 | F系列    | 11个       | 产品管理、前后端开发、数据库、API、测试部署      | FF   |

---

### 1.1 开发物料管理规范

#### 目录结构

```
ZTL数智化作战中心/
├── .claude/                    # Claude Code配置中心
│   ├── agents/                 # 智能体定义
│   │   ├── system/            # F系列系统智能体 (15个)
│   │   ├── 战略组/            # G系列战略智能体 (9个)
│   │   ├── 创意组/            # X系列创意智能体 (9个)
│   │   ├── 情报组/            # E系列情报智能体 (8个)
│   │   ├── 行政组/            # R系列行政智能体 (8个)
│   │   ├── 中台组/            # M系列中台智能体 (7个)
│   │   └── 筹建组/            # Z系列筹建智能体 (6个)
│   ├── commands/              # 斜杆命令定义 (26个)
│   ├── skills/                # 技能包库
│   └── CLAUDE.md              # 系统级配置文档
│
├── PRPs/                      # 功能规划文档 (164KB)
│   ├── completed/             # 已完成的PRP
│   ├── in-progress/           # 进行中的PRP
│   └── archived/              # 归档的PRP
│
├── reports/                   # 执行报告 (444KB)
│   ├── agents/                # 智能体创建报告
│   ├── commands/              # 命令执行报告
│   └── system/                # 系统更新报告
│
├── output/                    # 智能体输出目录 (4.0KB)
│   ├── 战略组/                # G系列输出
│   ├── 创意组/                # X系列输出
│   ├── 情报组/                # E系列输出
│   └── [其他组别]/
│
├── api/                       # API接口与工具 (90MB)
│   ├── mcp-servers/           # MCP服务器
│   ├── integrations/          # 第三方集成
│   └── scripts/               # 辅助脚本
│
├── scripts/                   # 项目脚本库 (332KB)
│   ├── automation/            # 自动化脚本
│   ├── data-processing/       # 数据处理
│   └── deployment/            # 部署脚本
│
├── input/                     # 输入素材目录
│   ├── images/                # 图片素材
│   ├── documents/             # 文档素材
│   └── data/                  # 数据文件
│
├── project/                   # 项目临时工作区 (4.0KB)
│
├── learning/                  # 学习与知识沉淀
│   ├── insights/              # 项目洞察
│   ├── decisions/             # 决策记录
│   └── errors/                # 错误与修正
│
├── trees/                     # Git并行工作空间
│   └── README.md              # worktree使用说明
│
├── backups/                   # 备份文件
│
└── CLAUDE.md                  # 项目级配置文档 (本文件)
```

#### 开发物料分类

| 物料类型             | 存储位置           | 命名规范                          | 生命周期               |
| -------------------- | ------------------ | --------------------------------- | ---------------------- |
| **功能规划**   | `PRPs/`          | `[功能名称]-v[版本号].md`       | 创建→评审→实现→归档 |
| **执行报告**   | `reports/`       | `[任务类型]-[日期]-report.md`   | 实时生成→永久保留     |
| **智能体输出** | `output/[组别]/` | `[智能体ID]-[任务名]-[时间戳]/` | 实时生成→定期清理     |
| **API工具**    | `api/`           | `[工具名]/`                     | 版本管理→持续迭代     |
| **自动化脚本** | `scripts/`       | `[功能]-[版本].py/sh`           | 版本管理→文档化       |
| **输入素材**   | `input/[类型]/`  | `[日期]-[描述].[ext]`           | 按需存储→项目结束清理 |
| **知识沉淀**   | `learning/`      | `[类型]/[主题].md`              | 持续积累→定期整理     |

#### 文件命名规范

```yaml
Markdown文档:
  PRP文档: "[功能名]-PRP-v1.0.md"
  报告文档: "[类型]-report-20251021.md"
  知识文档: "[主题]-insights.md"

智能体文件:
  格式: "[序号]-[名称].md"
  示例: "G1-经营分析优化师.md"

命令文件:
  格式: "[快捷键].md"
  示例: "E.md" (PRP生成与执行)

输出目录:
  格式: "[智能体ID]-[任务]-[时间戳]/"
  示例: "G1-monthly-analysis-20251021-1430/"
```

#### Git工作流程

```yaml
主分支保护:
  main: 生产环境分支,仅接受PR合并
  develop: 开发分支,日常开发基线

功能开发:
  分支命名: "feature/[功能名]-v[版本号]"
  工作模式: 使用 /R 命令创建worktree并行开发
  提交规范:
    - "feat: 新增功能"
    - "fix: 修复问题"
    - "docs: 文档更新"
    - "refactor: 代码重构"

发布流程:
  1. 功能开发完成后创建PR
  2. Code Review通过后合并到develop
  3. 定期从develop合并到main发布
  4. 使用 /G 命令完整同步到GitHub
```
### 1.2 技能包与钩子配置

#### Skills技能包体系

本项目集成**33个技能包**,分为4大类别,提供可复用的能力模块:

##### 元skills (6个)

提供框架级能力包，包含智能体创建、命令创建、钩子创建等元能力。

| 技能包名称 | 功能描述 | 文件路径 |
|-----------|---------|---------|
| agents | Design, create, and optimize Claude Code subagents based on 2025 prompt engineering and context engineering best practices. Use when building new intelligent agents or improving existing agent configurations. | `.claude/skills/元skills/agents/SKILL.md` |
| commands | Design, create, and optimize Claude Code slash commands based on official specifications and best practices. Use when building reusable command workflows or optimizing command configurations. | `.claude/skills/元skills/commands/SKILL.md` |
| hooks | Design, create, and debug Claude Code hooks for event-driven automation. Covers 8 lifecycle events, script development, testing strategies, and real-world best practices. Use when building hooks or troubleshooting hook systems. | `.claude/skills/元skills/hooks/SKILL.md` |
| output-styles | Design, create, and optimize Claude Code output styles based on official specifications and user experience best practices. Use when customizing output formats, creating style templates, or optimizing output experience. | `.claude/skills/元skills/output-styles/SKILL.md` |
| skill-creator | Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations. | `.claude/skills/元skills/skills/skill-creator/SKILL.md` |
| template-skill | Replace with description of the skill and when Claude should use it. | `.claude/skills/元skills/skills/template-skill/SKILL.md` |

##### 工作流 (1个)

业务流程和方法论技能包。

| 技能包名称 | 功能描述 | 文件路径 |
|-----------|---------|---------|
| meituan-operations-center-knowledge | 美团管家运营中心完整知识库，包含12个核心运营模块（餐厅管理、菜品管理、手机点餐、二维码管理、外卖管理、财务管理、分账管理、数智督导、效期管理、组织机构、系统设置）的详细功能说明、导航结构、表单定义、业务流程和自动化指南 | `.claude/skills/工作流/业务/美团管家/运营中心/SKILL.md` |

##### 知识库 (9个)

知识型技能包和配置模板，包含领域知识、资源模板和配置模板。

| 技能包名称 | 功能描述 | 文件路径 |
|-----------|---------|---------|
| Marketing Genius | 餐饮行业创意广告策划案例库,收集整理创意性、反传统、神来之笔、颠覆性且卓有奇效的广告策划案例。用于广告策划时的灵感参考和创意借鉴。当用户需要创意灵感、案例参考、或策划反传统营销活动时使用。基于deep-research-mcp实时更新案例库。 | `.claude/skills/知识库/知识/marketing-genius/SKILL.md` |
| Cyberpunk Neon Design | Create cyberpunk-inspired UI with neon colors (pink/purple/cyan), dark backgrounds, glowing effects, retro-futuristic animations, and metallic accents. Use when designing sci-fi games, tech websites, or when user mentions cyberpunk, neon, synthwave, or retro-futuristic design. High-impact visual style. | `.claude/skills/知识库/配置/html/cyberpunk-neon/SKILL.md` |
| Premium Dark Mode Design | Create sophisticated dark mode interfaces with refined color palettes, subtle gradients, strategic accents, and reduced eye strain. Use when designing modern apps, dashboards, or when user mentions dark mode, dark theme, or night mode. Includes automatic system preference detection. | `.claude/skills/知识库/配置/html/dark-mode-premium/SKILL.md` |
| Glassmorphism Design | Create glassmorphism UI with frosted glass surfaces, transparency, layering, and background blur. Use when designing modern SaaS platforms, card layouts, or when user mentions glassmorphism, frosted glass, or translucent UI. Pure CSS, cross-browser compatible. | `.claude/skills/知识库/配置/html/glassmorphism/SKILL.md` |
| iOS Liquid Glass Design | Create iOS-style liquid glass UI components with frosted glass effects, backdrop blur, transparency, and depth layering. Use when designing modern modals, navigation bars, cards, or when user mentions iOS design, liquid glass, frosted glass, or glassmorphism effects. Pure CSS implementation, no dependencies. | `.claude/skills/知识库/配置/html/ios-liquid-glass/SKILL.md` |
| Minimalist Gradient Design | Create elegant minimalist interfaces with subtle gradients, clean layouts, muted color palettes, and strategic bold accents. Use when designing corporate websites, product pages, or when user mentions minimalist design, subtle gradients, or clean UI. Professional and sophisticated aesthetic. | `.claude/skills/知识库/配置/html/minimalist-gradient/SKILL.md` |
| Neubrutalism Design | Create neubrutalism (brutalist revival) UI with bold colors, heavy fonts, sharp borders, raw aesthetic, and strong shadows. Use when designing creative portfolios, art platforms, or when user mentions neubrutalism, brutalism, or raw minimalist design. High contrast and accessibility-focused. | `.claude/skills/知识库/配置/html/neubrutalism/SKILL.md` |
| Neumorphism Design | Create neumorphism (soft UI) with realistic 3D embossed elements, dual shadows, and tactile interfaces. Use when designing minimalist tools, health apps, buttons, or when user mentions neumorphism, soft UI, or skeuomorphic design. Improved accessibility with better contrast. | `.claude/skills/知识库/配置/html/neumorphism/SKILL.md` |
| claude-code-pathfinder | 专业的技术资源探路者，通过深度理解用户需求，使用GitHub搜索引擎发现和推荐高质量项目、库和学习资源。主动用于技术选型、框架调研、最佳实践查找等场景。优先引导Claude Code Skills社区资源查找。 | `.claude/skills/知识库/配置/plugins/claude-code-pathfinder/SKILL.md` |

##### 执行引擎 (17个)

可执行的API工具和模块，包含API工具集成、MCP服务器和通用执行模块。

| 技能包名称 | 功能描述 | 文件路径 |
|-----------|---------|---------|
| Figma Analytics | Analyze Figma files for structure, quality, component usage, and design patterns. Use when auditing designs, assessing quality, discovering reusable patterns, or when user mentions design analysis, quality check, or component audit. Requires Figma API token. | `.claude/skills/执行引擎/API/figma/analytics-v2/SKILL.md` |
| Figma Batch Replace | Batch replace images in Figma with task orchestration, progress tracking, and retry mechanisms. Use when batch updating images, 6-batch production workflows, or when user mentions batch replace, bulk update, or template automation. Requires Figma API token and backend API. | `.claude/skills/执行引擎/API/figma/batch-replace-v2/SKILL.md` |
| Figma Design System Management | Manage enterprise-grade design systems including component libraries, style libraries, variables, and theme systems. Use when building design systems, managing components and styles, creating themes, or when user mentions design tokens, component libraries, style guides, variables, themes, dark mode, or brand consistency. Requires Figma API token. | `.claude/skills/执行引擎/API/figma/design-system-v2/SKILL.md` |
| Figma File Management | Retrieve Figma file information, query node details, get version history, navigate document structure. Use when working with Figma files, analyzing design structure, or when user mentions Figma documents, file structure, nodes, layers, or version control. Requires Figma API token. | `.claude/skills/执行引擎/API/figma/file-management-v2/SKILL.md` |
| Figma Image Export | Export Figma nodes as PNG, JPG, SVG, or PDF images with quality control, batch export, multi-size generation. Use when exporting design assets, generating images from Figma, or when user mentions image export, asset generation, download images, or format conversion. Requires Figma API token. | `.claude/skills/执行引擎/API/figma/image-export-v2/SKILL.md` |
| Figma Workflow Orchestration | Orchestrate complex multi-step Figma workflows with parallel execution, dependency management, and status monitoring. Use when automating complex production processes, managing multi-batch workflows, or when user mentions workflow automation, task orchestration, or production pipelines. Requires backend API. | `.claude/skills/执行引擎/API/figma/workflow-orchestration-v2/SKILL.md` |
| AIGC Advanced Image Processing | Professional restaurant image processing with 6 advanced capabilities - smart repair, structure control, multi-image fusion, character consistency, design iteration, and super-resolution enhancement. Use when performing complex image operations, creating brand IP, or when user mentions advanced editing, image fusion, upscaling, or professional post-production. Requires OpenRouter API key. | `.claude/skills/执行引擎/API/nano-banana/advanced-processing/SKILL.md` |
| AIGC Image Recognition Analyzer | Analyze restaurant images with AI-powered recognition for food content, scene understanding, quality assessment, and commercial insights. Supports comprehensive analysis, content recognition, scene detection, and quality evaluation. Use when analyzing restaurant images, evaluating food photos, or when user mentions image recognition, photo analysis, or visual assessment. Requires OpenRouter API key. | `.claude/skills/执行引擎/API/nano-banana/image-recognition/SKILL.md` |
| AIGC Image-to-Image Processor | Process and transform existing restaurant images with AI-powered optimization, style transfer, and creative modifications. Supports local edits, enhancements, multi-image processing, and style transfer. Use when modifying restaurant images, enhancing food photos, or when user mentions image-to-image, photo editing, or visual optimization. Requires OpenRouter API key. | `.claude/skills/执行引擎/API/nano-banana/image-to-image/SKILL.md` |
| AIGC Text-to-Image Generator | Generate professional restaurant design images from text descriptions. Supports 9 design types (poster, menu, storefront, panel, magazine, icon, typography, main-image, detail). Use when generating restaurant visuals, marketing materials, or when user mentions text-to-image, design generation, or restaurant graphics. Requires OpenRouter API key. | `.claude/skills/执行引擎/API/nano-banana/text-to-image/SKILL.md` |
| html-to-ppt | Complete HTML-to-PPT workflow including content analysis, HTML slide design (1920x1080), screenshot capture, PPT assembly, and quality verification. Use for presentation generation, marketing proposals, design mockups, and visual reports. | `.claude/skills/执行引擎/MCP/playwright-mcp/html-to-ppt/SKILL.md` |
| screenshots | Playwright-MCP screenshot capability for capturing web pages with full page support, viewport configuration, and load waiting. Use for web page screenshots, HTML rendering capture, full-page captures, and quality verification. | `.claude/skills/执行引擎/MCP/playwright-mcp/screenshots/SKILL.md` |
| excel-automation | Excel文件智能处理和自动化，支持数据读取、分析、清洗、报表生成和批量处理 | `.claude/skills/执行引擎/模块/office/excel/SKILL.md` |
| PDF Document Generator | Generate professional PDF documents using 3 methods - direct generation with ReportLab (recommended for reports/certificates), HTML-to-PDF with WeasyPrint (for web-style documents), and Markdown-to-PDF with Pandoc (for technical docs). Use when creating invoices, reports, certificates, forms, or any formatted PDF documents. Supports Chinese fonts, tables, images, and complex layouts. | `.claude/skills/执行引擎/模块/office/pdf/SKILL.md` |
| PowerPoint Generator | Generate professional PowerPoint presentations (.pptx) with two powerful methods - Direct generation (python-pptx) for programmatic control, HTML→PPT conversion for web-style content. Supports templates, tables, images, and complex layouts. | `.claude/skills/执行引擎/模块/office/ppt/SKILL.md` |
| Word Document Generator | Generate professional Word documents (.docx) with precise formatting control. Supports document creation, style management, tables, images, headers/footers, and template-based generation. Use when creating reports, proposals, contracts, or any formatted Word documents. Requires python-docx library. | `.claude/skills/执行引擎/模块/office/word/SKILL.md` |
| web-crawling-advanced | 基于Crawlee-Python的企业级网页爬虫框架，支持静态和动态网页采集、反反爬机制、代理轮换、数据持久化，适用于竞品监控、市场调研、数据采集等场景 | `.claude/skills/执行引擎/模块/web-crawling-advanced/SKILL.md` |

**调用机制**: Skills采用Claude自动发现机制，基于description字段自动匹配并按需加载。

#### Hooks钩子配置

本项目配置**3个事件驱动钩子**,提供自动化能力:

```yaml
Stop Hook - 智能任务延续:
  触发: 用户点击Stop按钮时
  命令: python3 .claude/hooks/stop_handler.py
  功能: 基于类型安全的任务状态检测,智能保存任务进度
  来源: fish895623/claude-hook

PreCompact Hook - 智能记忆提取:
  触发: 上下文压缩前(PreCompact事件)
  命令: python3 ~/.claude/memory-hooks/precompact_memory_extractor.py
  功能: 自动提取、评分和保存重要上下文信息
  来源: rhowardstone/memory-system

SessionStart Hook - 智能记忆注入:
  触发: 会话启动时(SessionStart事件)
  命令: python3 ~/.claude/memory-hooks/sessionstart_memory_injector.py
  功能: 自动加载相关历史上下文,实现跨会话记忆
  来源: rhowardstone/memory-system
```

**配置位置**: `.claude/settings.json`

**注意**: 本项目当前未启用Anthropic Agent Skills插件(enabledPlugins字段为空)。

---

## 2. 项目AGENTS说明

### 2.1 战略组 (G系列)

**组长**: GG - 战略规划总监
**定位**: 企业战略规划、经营分析、产品力打造、精细化管理
**颜色标识**: Purple (紫色)

| 快捷键 | 智能体名称         | 功能定位                                           | 文件路径                                           |
| ------ | ------------------ | -------------------------------------------------- | -------------------------------------------------- |
| G0     | 战略需求解析师     | 战略需求收集、目标分解、任务规划和智能体匹配       | `.claude/agents/战略组/G0-战略需求解析师.md`     |
| G1     | 经营分析优化师     | 门店经营数据深度分析、趋势预测、问题诊断和决策建议 | `.claude/agents/战略组/G1-经营分析优化师.md`     |
| G2     | 产品力打造专家     | 产品体系设计、菜品研发、产品组合优化和生命周期管理 | `.claude/agents/战略组/G2-产品力打造专家.md`     |
| G3     | 门店选址评估专家   | 商圈分析、选址评估、市场调研和开店决策支持         | `.claude/agents/战略组/G3-门店选址评估专家.md`   |
| G4     | 竞争情报分析师     | 竞品监测、市场动态分析、竞争策略研究               | `.claude/agents/战略组/G4-竞争情报分析师.md`     |
| G5     | 加盟政策设计师     | 加盟模式设计、政策制定、合作伙伴管理               | `.claude/agents/战略组/G5-加盟政策设计师.md`     |
| G6     | 战略数据看板设计师 | 战略指标体系设计、数据看板开发、决策支持           | `.claude/agents/战略组/G6-战略数据看板设计师.md` |
| G7     | 精细化管理专家     | SOP流程设计、操作手册编制、管理工具开发            | `.claude/agents/战略组/G7-精细化管理专家.md`     |
| GG     | 战略规划总监       | 战略任务智能调度、执行监督和质量把控               | `.claude/agents/战略组/GG-战略规划总监.md`       |

**典型工作流**:

```
战略需求 → G0解析分解 → GG调度编排 → G1-G7专业执行 → GG质量整合 → 战略方案输出
```

---

### 2.2 创意组 (X系列)

**组长**: XX - 创意组组长
**定位**: 品牌营销、广告策划、内容创作、视觉设计、短视频制作
**颜色标识**: Pink (粉色)

| 快捷键 | 智能体名称         | 功能定位                                         | 文件路径                                           |
| ------ | ------------------ | ------------------------------------------------ | -------------------------------------------------- |
| X0     | 内容创意需求分析师 | 创意需求分析、Brief输出、创意方案规划            | `.claude/agents/创意组/X0-内容创意需求分析师.md` |
| X1     | 广告策划师         | 广告创意策划、营销Campaign设计、品牌推广方案制定 | `.claude/agents/创意组/X1-广告策划师.md`         |
| X2     | 文案创作师         | 品牌文案、产品文案、营销文案、社交媒体文案创作   | `.claude/agents/创意组/X2-文案创作师.md`         |
| X3     | 平面设计师         | 品牌视觉设计、海报设计、菜单设计、包装设计       | `.claude/agents/创意组/X3-平面设计师.md`         |
| X4     | 图文排版师         | 菜单排版、宣传册设计、H5页面排版                 | `.claude/agents/创意组/X4-图文排版师.md`         |
| X5     | 短视频脚本创作师   | 抖音/快手/小红书/B站短视频脚本创作               | `.claude/agents/创意组/X5-短视频脚本创作师.md`   |
| X6     | 摄影师             | 菜品摄影、环境摄影、人像摄影                     | `.claude/agents/创意组/X6-摄影师.md`             |
| X7     | 剪辑师             | 短视频剪辑、宣传片制作、直播素材剪辑             | `.claude/agents/创意组/X7-剪辑师.md`             |
| XX     | 创意组组长         | 创意任务智能分解、X0-X7智能体调度、质量把控      | `.claude/agents/创意组/XX-创意组组长.md`         |

**典型工作流**:

```
创意需求 → X0分析Brief → XX调度编排 → X1-X7专业执行 → XX质量审核 → 创意作品交付
```

---

### 2.3 情报组 (E系列)

**组长**: EE - 情报组组长
**定位**: 公开资料调研、网站数据采集、深度情报分析、云存储管理
**颜色标识**: Cyan (青色)

| 快捷键 | 智能体名称         | 功能定位                                       | 文件路径                                           |
| ------ | ------------------ | ---------------------------------------------- | -------------------------------------------------- |
| E0     | 情报任务需求分析员 | 情报需求解析、任务拆解为E1-E9标准化执行参数    | `.claude/agents/情报组/E0-情报任务需求分析员.md` |
| E1     | 公开资料调研员     | 学术论文、技术博客、新闻报道、行业报告调研     | `.claude/agents/情报组/E1-公开资料调研员.md`     |
| E2     | 网站情报采集员     | 基于Chrome MCP的网站数据采集和交互操作         | `.claude/agents/情报组/E2-网站情报采集员.md`     |
| E3     | 网站深度爬虫员     | 基于Playwright MCP的企业级爬虫和批量采集       | `.claude/agents/情报组/E3-网站深度爬虫员.md`     |
| E4     | 深度情报分析员     | 数据清洗、语义分析、价值评估、关联发现         | `.claude/agents/情报组/E4-深度情报分析员.md`     |
| E5     | 云数据库管理员     | Supabase PostgreSQL数据库管理和双向处理        | `.claude/agents/情报组/E5-云数据库管理员.md`     |
| E6     | 云存储管理员       | 腾讯云COS存储管理、图表/PDF等附件存储          | `.claude/agents/情报组/E6-云存储管理员.md`       |
| EE     | 情报组组长         | 情报任务智能分解、多智能体协作调度、/R并行编排 | `.claude/agents/情报组/EE-情报组组长.md`         |

**典型工作流**:

```
情报需求 → E0任务拆解 → EE并行调度 → E1-E6专业采集 → E4深度分析 → E5/E6数据存储 → 情报报告交付
```

**特色能力**: 内置 `/R`命令并行协作能力,支持多情报源并行采集和实时整合。

---

### 2.4 行政组 (R系列)

**组长**: RR - 行政组组长
**定位**: 财务管理、人事管理、法务支持、秘书服务、飞书协同
**颜色标识**: Blue (蓝色)

| 快捷键 | 智能体名称         | 功能定位                                           | 文件路径                                           |
| ------ | ------------------ | -------------------------------------------------- | -------------------------------------------------- |
| R0     | 办公业务需求分析员 | 行政需求分析、任务拆解、优先级排序、执行计划       | `.claude/agents/行政组/R0-办公业务需求分析员.md` |
| R1     | 财务管理员         | 预算管理、费用报销、财务分析、成本控制             | `.claude/agents/行政组/R1-财务管理员.md`         |
| R2     | 人事管理员         | 招聘、入离职、考勤薪酬、培训发展                   | `.claude/agents/行政组/R2-人事管理员.md`         |
| R3     | 法务专家           | 合同审核、法律咨询、风险防控、纠纷处理             | `.claude/agents/行政组/R3-法务专家.md`           |
| R4     | 秘书               | 日程管理、会议组织、文档管理、接待协调             | `.claude/agents/行政组/R4-秘书.md`               |
| R5     | 飞书管理员         | 消息推送、群聊管理、文档管理、审批流程、通讯录     | `.claude/agents/行政组/R5-飞书管理员.md`         |
| R6     | 文件管理员         | 文件分类、归档存储、检索查询、权限控制、Office处理 | `.claude/agents/行政组/R6-文件管理员.md`         |
| RR     | 行政组组长         | 行政任务编排、R0-R6智能体调度、质量把控            | `.claude/agents/行政组/RR-行政组组长.md`         |

**典型工作流**:

```
行政需求 → R0需求分析 → RR任务编排 → R1-R6专业执行 → RR质量监督 → 行政服务交付
```

**集成能力**: 深度集成飞书MCP,支持消息推送、多维表格、云文档、审批流程等全套协同功能。

---

### 2.5 中台组 (M系列)

**组长**: MM - 中台组组长
**定位**: 美团管家运营管理、营销管理、供应链管理、数据报表、小程序管理、成本卡管理
**颜色标识**: Green (绿色)

| 快捷键 | 智能体名称                 | 功能定位                                                           | 文件路径                                                   |
| ------ | -------------------------- | ------------------------------------------------------------------ | ---------------------------------------------------------- |
| M0     | 美团管家系统业务需求分析员 | 业务需求转化、任务拆解、智能体匹配                                 | `.claude/agents/中台组/M0-美团管家系统业务需求分析员.md` |
| M1     | 美团管家运营管理员         | 餐厅管理、菜品管理、外卖管理、财务管理 (11个模块)                  | `.claude/agents/中台组/M1-美团管家运营管理员.md`         |
| M2     | 美团管家营销管理员         | 会员营销、卡券管理、大促活动 (11个模块)                            | `.claude/agents/中台组/M2-美团管家营销管理员.md`         |
| M3     | 美团管家报表管理员         | 经营分析、财务报表、运营洞察、商圈选址 (9个模块)                   | `.claude/agents/中台组/M3-美团管家报表管理员.md`         |
| M4     | 美团管家网页自动化操作助手 | 基于chrome-mcp的网页自动化，支持脚本模式和自由模式操作美团管家系统 | `.claude/agents/中台组/M4-美团管家网页自动化操作助手.md` |
| M5     | 小程序管理员               | 点餐小程序、会员小程序、营销小程序等全流程数字化管理               | `.claude/agents/中台组/M5-小程序管理员.md`               |
| M6     | 成本卡管理员               | 菜品成本卡精细化管理、配方管理、成本核算、成本分析                 | `.claude/agents/中台组/M6-成本卡管理员.md`               |
| M7     | 供应链管理员               | 供应商管理、采购管理、库存管理、成本控制、质量管理                 | `.claude/agents/中台组/M7-供应链管理员.md`               |
| MM     | 中台组组长                 | 美团管家系统战略规划、业务系统集成、数据流程自动化                 | `.claude/agents/中台组/MM-中台组组长.md`                 |

**典型工作流**:

```
业务需求 → M0需求分析 → MM战略规划 → M1-M7专业执行 → MM数据整合 → 运营决策支持
```

**核心价值**:

- 运营效率提升 30%+
- 运营成本降低 15%+
- 营销ROI提升 50%+
- 数据驱动决策

---

### 2.6 筹建组 (Z系列)

**组长**: ZZ - 筹建组组长
**定位**: 门店筹建全流程管理 - 平面图设计、空间设计、BIM建模、动画渲染
**颜色标识**: Yellow (黄色)

| 快捷键 | 智能体名称         | 功能定位                                         | 文件路径                                           |
| ------ | ------------------ | ------------------------------------------------ | -------------------------------------------------- |
| Z0     | 筹建项目需求分析师 | 新店筹建需求调研、空间规划、技术路线选择         | `.claude/agents/筹建组/Z0-筹建项目需求分析师.md` |
| Z1     | 平面图设计师       | 现场测量和CAD平面图绘制 (原始结构图、平面布置图) | `.claude/agents/筹建组/Z1-平面图设计师.md`       |
| Z2     | 空间设计师         | 空间设计方案 (风格定位、功能分区、色彩搭配)      | `.claude/agents/筹建组/Z2-空间设计师.md`         |
| Z3     | BIM建模师          | 基于CAD图纸创建BIM模型、机电管线建模、碰撞检测   | `.claude/agents/筹建组/Z3-BIM建模师.md`          |
| Z4     | 建筑动画师         | 基于BIM模型制作建筑漫游动画和效果图渲染          | `.claude/agents/筹建组/Z4-建筑动画师.md`         |
| ZZ     | 筹建组组长         | 筹建全流程管理、C1-C4智能体调度、质量把控        | `.claude/agents/筹建组/ZZ-筹建组组长.md`         |

**典型工作流**:

```
筹建需求 → Z0项目分析 → ZZ项目管理 → Z1平面图 → Z2空间设计 → Z3 BIM建模 → Z4动画渲染 → 筹建交付
```

**交付物**:

- CAD施工图纸 (平面/天花/立面)
- BIM精确模型 (含机电管线)
- 3D效果图渲染
- VR漫游动画
- 材料清单和预算

---

### 2.7 开发组 (F系列)

**组长**: FF - 开发组组长
**定位**: 产品开发、技术架构、前后端开发、数据库设计、API开发、测试部署
**颜色标识**: Orange (橙色)

| 快捷键 | 智能体名称       | 功能定位                                       | 文件路径                                         |
| ------ | ---------------- | ---------------------------------------------- | ------------------------------------------------ |
| F0     | 产品经理         | 产品需求分析、功能规划、原型设计、产品路线图   | `.claude/agents/开发组/F0-产品经理.md`         |
| F1     | 前端开发师       | React/Vue/Next.js前端开发、响应式Web应用       | `.claude/agents/开发组/F1-前端开发师.md`       |
| F2     | 组件开发师       | UI组件库开发、shadcn/ui、Ant Design企业级组件  | `.claude/agents/开发组/F2-组件开发师.md`       |
| F3     | 数据库开发师     | PostgreSQL/MySQL/MongoDB数据库设计、优化、管理 | `.claude/agents/开发组/F3-数据库开发师.md`     |
| F4     | API开发师        | RESTful API和GraphQL接口设计与开发             | `.claude/agents/开发组/F4-API开发师.md`        |
| F5     | 后端开发师       | 业务逻辑、微服务架构、系统集成                 | `.claude/agents/开发组/F5-后端开发师.md`       |
| F6     | 智能集成开发师   | Claude API、OpenAI API、MCP等AI服务集成        | `.claude/agents/开发组/F6-智能集成开发师.md`   |
| F7     | 测试与性能优化师 | 自动化测试、覆盖率管理、性能优化               | `.claude/agents/开发组/F7-测试与性能优化师.md` |
| F8     | 版本管理助手     | Git管理、代码审查、发布流程                    | `.claude/agents/开发组/F8-版本管理助手.md`     |
| F9     | 云部署管理员     | 应用部署、监控运维、故障处理                   | `.claude/agents/开发组/F9-云部署管理员.md`     |
| FF     | 框架组组长       | 技术架构规划、团队协作调度、项目质量把控       | `.claude/agents/开发组/FF-开发组组长.md`       |

**典型工作流**:

```yaml
Stage 1 - 需求分析: F0产品经理 → 产品需求文档
Stage 2 - 数据库与API设计: F3数据库 + F4 API → Schema + API文档
Stage 3 - 前端开发: F2组件库 → F1前端实现
Stage 4 - 后端开发: F5后端逻辑 + F6智能集成
Stage 5 - 测试优化: F7测试验证
Stage 6 - 部署上线: F8版本管理 → F9云部署
```

**核心价值**:

- 全栈技术支撑，从产品到上线
- 现代化技术栈（React/Next.js/PostgreSQL）
- AI能力深度集成（Claude/MCP）
- 企业级质量保障（测试覆盖率≥80%）

---

## 3. 意图分析图谱

### 意图识别原则

当用户提出需求时,系统通过关键词、任务类型和业务领域自动识别应该调用哪个业务组的智能体:

```yaml
意图分析流程:
  1. 关键词匹配: 提取用户需求中的业务关键词
  2. 任务类型识别: 判断是战略/创意/情报/行政/运营/筹建类任务
  3. 智能体路由: 自动调用对应组别的组长智能体
  4. 任务执行: 组长负责分解任务并调度专业智能体
```

### 意图映射表

#### 战略类意图 → G系列

| 用户意图示例           | 关键词             | 路由智能体 | 执行流程                             |
| ---------------------- | ------------------ | ---------- | ------------------------------------ |
| "分析本月门店经营数据" | 经营分析、数据分析 | GG → G1   | G0需求解析 → G1经营分析 → 报告输出 |
| "优化菜单产品结构"     | 产品、菜单、优化   | GG → G2   | G0需求解析 → G2产品设计 → 方案输出 |
| "评估新店选址"         | 选址、商圈、评估   | GG → G3   | G0需求解析 → G3选址分析 → 决策建议 |
| "研究竞品策略"         | 竞品、竞争、对手   | GG → G4   | G0需求解析 → G4竞争分析 → 情报报告 |
| "制定加盟政策"         | 加盟、合作、招商   | GG → G5   | G0需求解析 → G5政策设计 → 政策文档 |
| "设计战略看板"         | 看板、指标、BI     | GG → G6   | G0需求解析 → G6看板开发 → 数据看板 |
| "编写SOP手册"          | SOP、流程、标准化  | GG → G7   | G0需求解析 → G7流程设计 → SOP文档  |

#### 创意类意图 → X系列

| 用户意图示例   | 关键词             | 路由智能体 | 执行流程                             |
| -------------- | ------------------ | ---------- | ------------------------------------ |
| "策划开业活动" | 活动、策划、营销   | XX → X1   | X0 Brief → X1策划方案 → X2文案支持 |
| "撰写产品文案" | 文案、介绍、slogan | XX → X2   | X0 Brief → X2文案创作 → 文案交付   |
| "设计菜单海报" | 设计、海报、菜单   | XX → X3   | X0 Brief → X3设计 → 视觉稿交付     |
| "排版宣传册"   | 排版、宣传册、画册 | XX → X4   | X0 Brief → X4排版 → 排版稿交付     |
| "写短视频脚本" | 短视频、脚本、抖音 | XX → X5   | X0 Brief → X5脚本创作 → 脚本交付   |
| "拍摄菜品照片" | 拍摄、摄影、照片   | XX → X6   | X0 Brief → X6摄影 → 照片交付       |
| "剪辑宣传片"   | 剪辑、视频、后期   | XX → X7   | X0 Brief → X7剪辑 → 视频交付       |

#### 情报类意图 → E系列

| 用户意图示例       | 关键词           | 路由智能体  | 执行流程                                      |
| ------------------ | ---------------- | ----------- | --------------------------------------------- |
| "调研行业趋势"     | 调研、研究、报告 | EE → E1    | E0任务拆解 → E1公开调研 → 报告输出          |
| "采集竞品网站数据" | 采集、网站、爬取 | EE → E2/E3 | E0任务拆解 → E2/E3采集 → E4分析 → 情报报告 |
| "分析市场数据"     | 分析、数据、洞察 | EE → E4    | E0任务拆解 → E1采集 → E4分析 → 报告输出    |

#### 行政类意图 → R系列

| 用户意图示例   | 关键词           | 路由智能体 | 执行流程                             |
| -------------- | ---------------- | ---------- | ------------------------------------ |
| "制定年度预算" | 预算、财务、规划 | RR → R1   | R0需求分析 → R1财务管理 → 预算方案 |
| "发布招聘岗位" | 招聘、岗位、HR   | RR → R2   | R0需求分析 → R2人事管理 → 招聘发布 |
| "审核合同"     | 合同、法务、审核 | RR → R3   | R0需求分析 → R3法务审核 → 审核意见 |
| "安排会议"     | 会议、日程、安排 | RR → R4   | R0需求分析 → R4秘书服务 → 会议组织 |
| "发送飞书通知" | 飞书、消息、通知 | RR → R5   | R0需求分析 → R5飞书推送 → 消息发送 |
| "归档文件"     | 文件、归档、管理 | RR → R6   | R0需求分析 → R6文档管理 → 归档完成 |

#### 中台类意图 → M系列

| 用户意图示例         | 关键词             | 路由智能体 | 执行流程                               |
| -------------------- | ------------------ | ---------- | -------------------------------------- |
| "配置外卖菜品"       | 外卖、菜品、美团   | MM → M1   | M0需求分析 → M1运营管理 → 配置完成   |
| "设计会员活动"       | 会员、营销、活动   | MM → M2   | M0需求分析 → M2营销管理 → 活动上线   |
| "管理库存"           | 库存、采购、供应链 | MM → M3   | M0需求分析 → M3供应管理 → 库存优化   |
| "生成经营报表"       | 报表、数据、分析   | MM → M4   | M0需求分析 → M4报表生成 → 数据看板   |
| "自动化操作美团管家" | 自动化、网页、操作 | MM → M5   | M0需求分析 → M5网页自动化 → 任务完成 |

#### 筹建类意图 → Z系列

| 用户意图示例   | 关键词             | 路由智能体 | 执行流程                                   |
| -------------- | ------------------ | ---------- | ------------------------------------------ |
| "设计新店布局" | 新店、布局、设计   | ZZ → Z2   | Z0需求分析 → Z1平面图 → Z2空间设计       |
| "绘制CAD图纸"  | CAD、图纸、施工图  | ZZ → Z1   | Z0需求分析 → Z1 CAD绘图 → 图纸交付       |
| "创建BIM模型"  | BIM、建模、3D      | ZZ → Z3   | Z0需求分析 → Z1图纸 → Z3建模 → 模型交付 |
| "制作效果图"   | 效果图、渲染、动画 | ZZ → Z4   | Z0需求分析 → Z3模型 → Z4渲染 → 动画交付 |

#### 框架类意图 → F系列

| 用户意图示例   | 关键词               | 路由智能体  | 执行流程                                                           |
| -------------- | -------------------- | ----------- | ------------------------------------------------------------------ |
| "开发排班系统" | 开发、系统、功能     | FF → F0    | F0需求分析 → F3/F4设计 → F1/F2前端 → F5后端 → F7测试 → F9部署 |
| "设计数据库"   | 数据库、Schema、模型 | FF → F3    | F0需求分析 → F3数据库设计 → Schema交付                           |
| "开发API接口"  | API、接口、RESTful   | FF → F4    | F0需求分析 → F4 API设计 → 接口文档                               |
| "前端页面开发" | 前端、页面、React    | FF → F1    | F0需求分析 → F2组件 → F1页面 → 前端应用                         |
| "集成AI能力"   | AI、集成、智能       | FF → F6    | F0需求分析 → F6智能集成 → AI功能上线                             |
| "性能优化"     | 性能、优化、测试     | FF → F7    | F7性能测试 → 优化建议 → 性能提升                                 |
| "部署上线"     | 部署、上线、发布     | FF → F8/F9 | F8版本管理 → F9云部署 → 生产环境                                 |

### 多智能体协同场景

某些复杂任务需要跨组协同:

```yaml
场景1: 新品上市全流程
  触发: "策划新品上市活动"
  协同:
    - G2 (产品设计) → X1 (营销策划) → X2 (文案) → X3 (设计) → M2 (活动上线)

场景2: 新店筹建全流程
  触发: "筹建新门店"
  协同:
    - G3 (选址评估) → Z0 (需求分析) → Z1-Z4 (筹建执行) → M1 (系统配置)

场景3: 竞品情报分析
  触发: "全面分析竞品"
  协同:
    - E1 (公开调研) → E2/E3 (网站采集) → E4 (深度分析) → G4 (竞争策略)
```

---

## 4. 项目快捷键系统

### 项目级快捷键 (60个智能体)

#### 战略组 (G系列 - 紫色 Purple)

- **G0-G7**: 战略需求解析、经营分析、产品力、选址、竞品、加盟、看板、精细化管理
- **GG**: 战略组组长 (总调度)

#### 创意组 (X系列 - 粉色 Pink)

- **X0-X7**: 需求分析、广告策划、文案、设计、排版、脚本、摄影、剪辑
- **XX**: 创意组组长 (总调度)

#### 情报组 (E系列 - 青色 Cyan)

- **E0-E6**: 需求分析、公开调研、网站采集、深度爬虫、情报分析、数据库、存储
- **EE**: 情报组组长 (总调度,内置/R并行能力)

#### 行政组 (R系列 - 蓝色 Blue)

- **R0-R6**: 需求分析、财务、人事、法务、秘书、飞书、文件管理
- **RR**: 行政组组长 (总调度)

#### 中台组 (M系列 - 绿色 Green)

- **M0-M7**: 需求分析、运营、营销、报表、网页自动化、小程序、成本卡、供应链
- **MM**: 中台组组长 (总调度)

#### 筹建组 (Z系列 - 黄色 Yellow)

- **Z0-Z4**: 需求分析、平面图、空间设计、BIM建模、动画渲染
- **ZZ**: 筹建组组长 (总调度)

#### 开发组 (F系列 - 橙色 Orange)

- **F0-F9**: 产品管理、前端、组件、数据库、API、后端、AI集成、测试、版本、部署
- **FF**: 框架组组长 (总调度)

### 系统级快捷键 (23个命令)

详见系统级配置文档 [`.claude/CLAUDE.md`](.claude/CLAUDE.md)

```yaml
上下文与学习管理: /A /C /D /S /V /W /X /Z
执行与状态管理: /B /E /F /M /N /Q /R
代码与项目管理: /G /H /I /J /K /L /O /P /T /U /Y
```

---

## 附录

### 相关文档

- **系统级配置**: [`.claude/CLAUDE.md`](.claude/CLAUDE.md) - F系列智能体和系统命令
- **技能包文档**: [`.claude/skills/`](.claude/skills/) - 可复用能力包
- **项目概览**: [`OVERVIEW.md`](OVERVIEW.md) - 项目架构和功能特性

---

**文档维护**: 定期更新以保持与项目实际配置同步
**更新命令**: `/M` - 项目级CLAUDE.md自动更新
**兼容版本**: Claude Code v1.0+, Sonnet 4.5
**编码格式**: UTF-8
