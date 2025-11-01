---
name: 项目介绍文档目录智能管理器
description: 全面管理project/instructions目录下的完整文档体系，包括多个HTML页面、支持脚本、样式文件和配置，智能同步项目最新状态，保持设计风格一致性
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "WebSearch", "mcp__context7__resolve-library-id", "mcp__context7__get-library-docs"]
model: claude-sonnet-4.5
argument-hint: ""
version: 2.0.0
last_updated: 2025-10-24
---

# 项目介绍文档目录智能管理器

## 📋 命令概述

**命令名称**: 项目介绍文档目录智能管理器
**快捷键**: `/project/instructions`
**版本**: v2.0.0
**使用语法**: `/project/instructions`

智能管理整个`project/instructions/`目录，自动更新所有HTML页面、同步项目数据、优化视觉设计、维护一致性风格。

### 核心特性
- **完整目录管理**: 管理整个project/instructions目录而非单个HTML文件
- **多页面协同**: 同步更新所有HTML页面（主页、架构图、命令列表、用例展示等）
- **智能数据同步**: 自动从项目配置中提取最新数据
- **风格一致性**: 保持所有页面的设计风格统一
- **脚本与样式维护**: 管理共享的JavaScript和CSS资源
- **文档化完整**: 自动生成和更新使用说明文档

---

## 🎯 核心功能

### 功能1: 目录结构智能管理

**目标**: 维护完整的project/instructions目录体系

**目录结构**:
```yaml
project/instructions/
├── 主入口文件:
│   └── ZTL数智化作战中心项目介绍.html  # 项目主页
│
├── 功能页面:
│   ├── architecture.html               # 架构设计页面
│   ├── commands.html                   # 命令系统页面
│   ├── mcp-servers.html                # MCP服务器页面
│   ├── use-cases.html                  # 用例展示页面
│   └── test-functions.html             # 功能测试页面
│
├── 子页面目录:
│   └── pages/                          # 详细子页面
│       ├── agents-detail.html          # 智能体详情
│       ├── skills-detail.html          # 技能包详情
│       └── [其他详细页面]
│
├── 脚本目录:
│   └── scripts/                        # JavaScript资源
│       ├── main.js                     # 主脚本
│       ├── charts.js                   # 图表配置
│       ├── data-sync.js                # 数据同步
│       └── utils.js                    # 工具函数
│
├── 样式目录:
│   └── styles/                         # CSS资源
│       ├── main.css                    # 主样式
│       ├── components.css              # 组件样式
│       ├── charts.css                  # 图表样式
│       └── responsive.css              # 响应式样式
│
├── 文档说明:
│   └── OUTPUT页面使用说明.md           # 使用指南
│
└── 启动脚本:
    └── start-server.sh                 # 本地服务器启动脚本
```

### 功能2: 项目数据全面扫描

**目标**: 从项目配置中提取完整的数据快照

**扫描范围**:
```yaml
配置文件:
  1. CLAUDE.md (项目根目录)
     - 项目概述、业务矩阵、智能体系统
     - 命令系统、技能包体系
     - MCP服务器配置

  2. OVERVIEW.md
     - 项目架构、核心特性
     - 技术栈、设计理念

  3. README.md
     - 项目简介、主要功能
     - 快速开始、使用指南

目录结构:
  1. .claude/agents/
     - 统计各组智能体数量(G/X/E/R/M/Z/F系列)
     - 提取智能体名称、功能定位、文件路径

  2. .claude/commands/
     - 统计命令总数、分类统计
     - 提取命令名称、快捷键、功能描述

  3. .claude/skills/
     - 统计技能包总数、分类统计
     - 提取技能包名称、功能描述

  4. .claude/settings.json
     - 提取MCP服务器列表
     - 提取已启用插件配置

  5. PRPs/
     - 统计PRP文档数量(completed/in-progress)

技术栈检测:
  - package.json: JavaScript依赖
  - requirements.txt: Python依赖
  - 项目实际使用的技术框架

输出:
  - 结构化JSON数据快照
  - 统计数据汇总
  - 技术栈清单
```

### 功能3: 多页面协同更新

**目标**: 智能更新所有HTML页面的相关数据

**更新策略**:
```yaml
主页面 (ZTL数智化作战中心项目介绍.html):
  更新内容:
    - 项目概述数据
    - 核心统计数字(智能体/命令/技能包总数)
    - 业务组分布图表
    - 技术栈徽章
    - 主要功能特性

architecture.html:
  更新内容:
    - 架构图数据
    - 业务组详细信息
    - 智能体协作流程
    - 技术架构说明

commands.html:
  更新内容:
    - 命令列表(按分类)
    - 命令使用示例
    - 快捷键映射表
    - 命令功能描述

mcp-servers.html:
  更新内容:
    - MCP服务器列表
    - 服务器功能描述
    - 工具数量统计
    - 集成状态

use-cases.html:
  更新内容:
    - 用例场景列表
    - 智能体协同示例
    - 工作流程图
    - 最佳实践

pages/子页面:
  更新内容:
    - 详细数据表格
    - 深度功能说明
    - API文档
    - 示例代码
```

### 功能4: 脚本与样式维护

**目标**: 维护共享的JavaScript和CSS资源

**脚本管理**:
```yaml
scripts/main.js:
  功能:
    - 页面导航逻辑
    - 动态数据加载
    - 用户交互处理

scripts/charts.js:
  功能:
    - Chart.js图表配置
    - 数据可视化逻辑
    - 图表主题管理

scripts/data-sync.js:
  功能:
    - 从JSON加载项目数据
    - 动态更新页面内容
    - 数据缓存管理

scripts/utils.js:
  功能:
    - 通用工具函数
    - 日期格式化
    - 字符串处理
```

**样式管理**:
```yaml
styles/main.css:
  内容:
    - 全局变量(颜色、字体、间距)
    - 基础布局
    - 通用组件样式

styles/components.css:
  内容:
    - 卡片组件
    - 按钮样式
    - 表单元素
    - 导航栏

styles/charts.css:
  内容:
    - 图表容器样式
    - 图例样式
    - 工具提示样式

styles/responsive.css:
  内容:
    - 移动端适配
    - 平板端适配
    - 断点定义
```

---

## 📊 执行流程

### 阶段1: 环境检测与数据扫描 (20%)

```yaml
步骤1: 检测project/instructions目录
  - 验证目录存在性
  - 扫描所有HTML文件
  - 识别脚本和样式文件
  - 检查文档说明文件

步骤2: 扫描项目配置
  - 读取CLAUDE.md、OVERVIEW.md、README.md
  - 扫描.claude/目录结构
  - 统计智能体/命令/技能包数量
  - 提取MCP服务器配置

步骤3: 生成数据快照
  - 创建JSON格式的数据快照
  - 保存到scripts/project-data.json
  - 供前端JavaScript动态加载

输出:
  - 目录结构清单
  - 项目数据快照(JSON)
  - 文件更新清单
```

### 阶段2: 设计风格研究 (25%)

```yaml
步骤1: 分析现有设计风格
  - 读取主页面HTML
  - 提取色彩方案
  - 识别布局模式
  - 分析图表类型

步骤2: Context7最佳实践搜索
  工具调用:
    - mcp__context7__resolve-library-id
    - mcp__context7__get-library-docs

  搜索主题:
    - "multi-page documentation design"
    - "project showcase best practices"
    - "interactive data visualization"

步骤3: 整理设计方案
  - 保持现有风格一致性
  - 优化图表表现力
  - 增强交互体验
  - 改进响应式设计

输出:
  - 设计风格档案
  - 优化方案文档
  - CSS更新计划
```

### 阶段3: 内容对比与更新计划 (20%)

```yaml
步骤1: 逐页对比数据
  对每个HTML页面:
    - 提取现有数据点
    - 对比项目实际数据
    - 标记过时内容
    - 识别新增内容

步骤2: 生成更新计划
  分优先级:
    - P0 (高): 核心统计数字
    - P1 (中): 文本内容描述
    - P2 (低): 视觉优化项

  列出更新清单:
    - 每个文件的更新项
    - 预计更新工作量
    - 依赖关系

输出:
  - 数据对比报告
  - 结构化更新计划
```

### 阶段4: 智能更新执行 (30%)

```yaml
步骤1: 更新数据快照文件
  - 生成scripts/project-data.json
  - 包含所有最新数据

步骤2: 更新HTML页面
  主页面:
    - 更新核心统计数字
    - 更新业务组信息
    - 更新技术栈徽章
    - 更新图表数据源

  功能页面:
    - architecture.html: 更新架构图数据
    - commands.html: 更新命令列表
    - mcp-servers.html: 更新服务器清单
    - use-cases.html: 更新用例场景

  子页面:
    - 更新详细数据表格
    - 更新API文档
    - 更新示例代码

步骤3: 优化JavaScript脚本
  - 更新charts.js的图表配置
  - 优化data-sync.js的数据加载
  - 增强main.js的交互逻辑

步骤4: 优化CSS样式
  - 保持色彩一致性
  - 增强组件样式
  - 改进响应式布局

输出:
  - 更新后的所有HTML文件
  - 更新后的脚本文件
  - 更新后的样式文件
```

### 阶段5: 文档化与验证 (5%)

```yaml
步骤1: 更新使用说明
  - 更新OUTPUT页面使用说明.md
  - 记录最新的页面结构
  - 说明启动方法
  - 列出功能特性

步骤2: 创建备份
  - 备份整个project/instructions目录
  - 保存到backups/project/instructions-backup-[时间戳]/

步骤3: 生成更新报告
  - 列出所有更新的文件
  - 统计更新数据点
  - 记录设计优化项
  - 输出Markdown报告

输出:
  - OUTPUT页面使用说明.md (更新)
  - 备份目录
  - 更新报告 (Markdown)
```

---

## 🎨 设计原则

### 1. 多页面一致性

```yaml
色彩系统:
  - 所有页面使用统一的CSS变量
  - 主色、辅色、强调色保持一致
  - 渐变背景风格统一

排版系统:
  - 统一的字体族和字号层级
  - 一致的标题样式
  - 统一的段落间距

组件系统:
  - 共享的卡片组件
  - 统一的按钮样式
  - 一致的表格样式

交互系统:
  - 统一的hover效果
  - 一致的过渡动画
  - 共享的图标库
```

### 2. 数据驱动更新

```yaml
数据源:
  - scripts/project-data.json作为单一数据源
  - JavaScript动态加载数据
  - 避免硬编码数据在HTML中

更新策略:
  - 数据快照更新后，所有页面自动同步
  - 使用模板引擎或JavaScript渲染
  - 保持数据与展示分离
```

### 3. 模块化管理

```yaml
HTML模块化:
  - 共享的header导航
  - 共享的footer信息
  - 可复用的组件块

JavaScript模块化:
  - 功能分模块
  - 避免全局污染
  - 依赖关系清晰

CSS模块化:
  - 按功能分文件
  - BEM命名规范
  - 避免样式冲突
```

---

## 🔧 工具使用清单

```yaml
文件操作:
  - Read: 读取所有HTML、JS、CSS文件
  - Write: 写入更新后的文件
  - Edit: 精确更新特定内容
  - Glob: 扫描project/instructions目录
  - Grep: 搜索特定内容

项目扫描:
  - Bash: 执行目录统计命令
  - Glob: 递归扫描.claude目录

MCP工具:
  - mcp__context7__resolve-library-id: 设计参考库解析
  - mcp__context7__get-library-docs: 获取设计文档

搜索工具:
  - WebSearch: 补充设计灵感(如Context7无结果)
```

---

## 🌟 典型使用场景

### 场景1: 定期同步项目状态

```bash
# 每周执行一次，保持所有文档页面与项目同步
/project/instructions

# 自动执行:
# - 扫描所有项目配置
# - 更新所有HTML页面
# - 同步数据快照
# - 优化设计风格
```

### 场景2: 重大版本发布前全面更新

```bash
# 在v2.0发布前，全面刷新项目介绍文档
/project/instructions

# 执行内容:
# - 同步v2.0新功能数据
# - 更新所有页面内容
# - 优化视觉设计
# - 验证所有链接
```

### 场景3: 新增功能页面

```bash
# 添加新的功能展示页面后
/project/instructions

# 自动处理:
# - 检测新增的HTML文件
# - 更新导航链接
# - 同步数据到新页面
# - 保持风格一致性
```

---

## ⚙️ 配置项

```yaml
目录配置:
  project_instructions_dir: "./project/instructions/"
  backup_dir: "./backups/"
  data_snapshot_path: "./project/instructions/scripts/project-data.json"

HTML页面:
  main_pages:
    - ZTL数智化作战中心项目介绍.html
    - architecture.html
    - commands.html
    - mcp-servers.html
    - use-cases.html
    - test-functions.html

  sub_pages_dir: pages/

资源目录:
  scripts_dir: scripts/
  styles_dir: styles/

文档:
  usage_doc: OUTPUT页面使用说明.md
  start_script: start-server.sh

备份配置:
  enable_backup: true
  backup_retention: 5  # 保留最近5次备份
  auto_cleanup: true
```

---

## 🎯 成功标准

```yaml
数据同步:
  ✅ 所有HTML页面的数据与项目配置一致
  ✅ scripts/project-data.json包含最新数据
  ✅ 无遗漏的数据点

风格一致性:
  ✅ 所有页面使用统一的色彩方案
  ✅ 所有页面使用统一的组件样式
  ✅ 所有页面的交互效果一致

功能完整性:
  ✅ 所有页面的导航链接正常工作
  ✅ 所有JavaScript脚本正常加载
  ✅ 所有CSS样式正确应用
  ✅ 所有图表正常渲染

文档化:
  ✅ OUTPUT页面使用说明.md已更新
  ✅ 包含最新的目录结构说明
  ✅ 包含启动和使用指南
```

---

## ⚠️ 注意事项

```yaml
执行环境:
  - 确保在项目根目录执行
  - 确保project/instructions目录存在
  - 确保有文件读写权限

依赖检查:
  - Context7 MCP服务器需正常运行
  - 如使用Chart.js，建议2.9.4+版本
  - 确保所有MCP工具可用

备份管理:
  - 备份会自动创建但不会自动删除
  - 建议定期清理旧备份(保留最近5次)
  - 备份目录: backups/project/instructions-backup-*/

浏览器兼容:
  - 生成的HTML兼容现代浏览器
  - 建议使用Chrome/Firefox/Safari/Edge
  - 移动端响应式支持

本地预览:
  - 执行 bash project/instructions/start-server.sh
  - 在浏览器访问 http://localhost:8000
  - 实时查看更新效果
```

---

## 📝 更新报告示例

```markdown
# /project/instructions 执行报告

**执行时间**: 2025-10-24 15:30:00
**总耗时**: 90秒
**状态**: ✅ 成功

## 📊 扫描统计

### 项目数据
- 智能体总数: **60个** (G9 + X9 + E8 + R8 + M9 + Z6 + F11)
- 命令总数: **26个**
- 技能包总数: **33个**
- MCP服务器: **8个**
- PRP文档: **15个** (已完成: 12, 进行中: 3)

### 目录结构
- HTML页面: **11个** (主页6个 + 子页面5个)
- JavaScript文件: **12个**
- CSS文件: **13个**
- 文档文件: **1个**

## 🔄 更新明细

### 主页面更新
**ZTL数智化作战中心项目介绍.html**
- ✅ 智能体总数: 55 → 60
- ✅ 命令总数: 23 → 26
- ✅ 技能包总数: 30 → 33
- ✅ 更新业务组分布饼图
- ✅ 更新技术栈徽章

**architecture.html**
- ✅ 更新智能体协作流程图
- ✅ 新增M系列(中台组)详细说明
- ✅ 更新技术架构图

**commands.html**
- ✅ 新增3个命令条目
- ✅ 更新命令分类统计
- ✅ 更新快捷键映射表

**mcp-servers.html**
- ✅ 更新MCP服务器数量
- ✅ 更新MCP服务器配置状态

**use-cases.html**
- ✅ 新增2个典型用例场景
- ✅ 更新智能体协同示例

### 数据快照更新
**scripts/project-data.json**
- ✅ 完整的项目数据快照
- ✅ 7大业务组详细数据
- ✅ 所有智能体/命令/技能包列表

### 样式优化
**styles/main.css**
- 🎨 优化CSS变量定义
- 🎨 增强响应式断点

**styles/components.css**
- 🎨 优化卡片hover效果
- 🎨 增强按钮交互反馈

## 📁 输出文件

- **更新的HTML页面**: 11个
- **更新的数据快照**: scripts/project-data.json
- **更新的使用说明**: OUTPUT页面使用说明.md
- **备份目录**: backups/project/instructions-backup-20251024-153000/

## 🎨 设计优化

**保持一致性**:
- ✅ 统一的紫色渐变主题
- ✅ 一致的卡片布局风格
- ✅ 统一的导航交互

**增强表现力**:
- Chart.js交互式图表
- 平滑的页面过渡动画
- 响应式设计优化

---

✨ **更新完成！** 所有project/instructions目录下的文档已同步至最新状态。

💡 **本地预览**:
```bash
cd project/instructions
bash start-server.sh
# 访问 http://localhost:8000
```
```

---

**命令名称**: 项目介绍文档目录智能管理器
**快捷键**: `/project/instructions`
**版本**: v2.0.0
**最后更新**: 2025-10-24
**作者**: ZTL数智化作战中心
**兼容**: Claude Code v1.0+, Sonnet 4.5

---

## 版本历史

```yaml
v2.0.0 (2025-10-24):
  - 🚀 重大更新: 从单HTML文件管理扩展到完整目录管理
  - ✅ 支持多页面协同更新
  - ✅ JavaScript/CSS资源管理
  - ✅ 数据快照自动生成
  - ✅ 使用说明文档自动更新
  - ✅ 完整备份机制
  - ✅ 模块化设计原则

v1.0.0 (2025-10-23):
  - ✅ 初始版本 (单HTML文件管理)
  - ✅ 项目数据扫描
  - ✅ Context7集成
  - ✅ 图表优化
```
