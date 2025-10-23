---
description: HTML项目综合介绍页面智能更新优化器 - 全面扫描项目最新状态，结合Context7最佳实践，智能更新HTML项目展示页面，增强图表化表现和设计感
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "WebSearch", "mcp__context7__resolve-library-id", "mcp__context7__get-library-docs"]
model: claude-sonnet-4.5
---

# HTML项目综合介绍页面智能更新优化器

## 命令定位

**快捷键**: `/J`
**版本**: v1.0.0
**使用语法**: `/J [HTML文件路径]`

自动更新和优化HTML项目综合介绍页面，保持设计风格一致性，同步项目最新状态，增强数据可视化和设计感。

---

## 执行流程

### Phase 1: 项目状态全面扫描 (20%)

**目标**: 获取项目最新状态的完整快照

#### 1.1 读取并分析目标HTML

```yaml
任务:
  - 读取指定HTML文件: $1 (用户提供的文件路径)
  - 解析HTML结构和内容
  - 提取现有设计风格特征:
      - 色彩方案 (主色、辅色、强调色)
      - 字体系统 (标题、正文、代码)
      - 布局模式 (Grid/Flex、间距系统)
      - 图表类型 (Chart.js/ECharts/D3.js)
      - 交互效果 (动画、过渡、响应式)

  - 提取现有内容结构:
      - 章节组织 (Hero、Features、Stats、Tech Stack等)
      - 数据点 (智能体数量、命令数量、技能包数量等)
      - 图表配置 (图表类型、数据源、样式)

输出:
  - HTML设计风格档案
  - 现有内容清单
```

#### 1.2 扫描项目核心配置文件

```yaml
必读文件列表:
  1. CLAUDE.md (项目级配置)
     - 提取: 项目概述、业务矩阵、智能体总数、快捷键系统

  2. OVERVIEW.md (项目概览)
     - 提取: 项目架构、核心特性、技术栈、设计理念

  3. README.md (项目说明)
     - 提取: 项目简介、主要功能、使用指南

  4. .claude/CLAUDE.md (系统级配置)
     - 提取: 系统智能体、系统命令、框架描述

扫描目录结构:
  1. .claude/agents/ (智能体配置)
     - 统计: 各组智能体数量 (G/X/E/R/M/Z/F系列)
     - 提取: 智能体名称、功能定位

  2. .claude/commands/ (命令配置)
     - 统计: 系统命令、项目命令数量
     - 提取: 命令名称、功能分类

  3. .claude/skills/ (技能包配置)
     - 统计: 技能包总数、分类统计
     - 提取: 技能包名称、功能描述

  4. PRPs/ (功能规划文档)
     - 统计: 已完成、进行中、待开始的PRP数量

  5. reports/ (执行报告)
     - 统计: 报告数量、类型分布

技术栈检测:
  1. 检查 package.json (如存在)
     - 提取: dependencies、devDependencies

  2. 检查 requirements.txt (如存在)
     - 提取: Python依赖包

  3. 检查 .claude/settings.json
     - 提取: MCP服务器列表、已启用插件

输出:
  - 项目数据快照 (JSON格式)
  - 技术栈清单
  - 目录统计数据
```

#### 1.3 提取项目核心特征

```yaml
数据提取清单:
  项目基础信息:
    - 项目名称
    - 项目版本
    - 核心定位
    - 技术架构

  业务组织结构:
    - 业务组数量 (战略/创意/情报/行政/中台/筹建/框架)
    - 每组智能体数量
    - 组长智能体名称

  能力矩阵:
    - 智能体总数 (按系列分类)
    - 命令总数 (按类别分类)
    - 技能包总数 (按分类统计)
    - MCP服务器数量

  项目活跃度:
    - PRP文档数量 (已完成/进行中)
    - 报告数量
    - 最后更新时间

输出:
  - 核心数据集 (用于图表生成)
  - 特征标签云 (技术栈、功能特性)
```

---

### Phase 2: 设计风格研究与优化方案 (30%)

**目标**: 基于Context7最佳实践，设计一致性优化方案

#### 2.1 Context7 最佳实践搜索

```yaml
搜索策略:
  关键词组合1: "html project showcase"
    - 解析库ID
    - 获取文档: 项目展示页面设计模式

  关键词组合2: "interactive data visualization"
    - 解析库ID
    - 获取文档: 数据可视化最佳实践

  关键词组合3: "modern web design patterns"
    - 解析库ID
    - 获取文档: 现代化Web设计趋势

工具调用:
  1. mcp__context7__resolve-library-id
     - libraryName: 根据搜索关键词动态确定

  2. mcp__context7__get-library-docs
     - context7CompatibleLibraryID: 从步骤1获取
     - topic: "project showcase", "data visualization", "design patterns"
     - tokens: 3000

输出:
  - 设计模式参考列表
  - 可视化最佳实践
  - 现代化设计趋势
```

#### 2.2 分析现有HTML设计风格

```yaml
分析维度:
  1. 色彩系统:
     - 提取: 主色值、辅助色、强调色、背景色
     - 评估: 色彩对比度、可访问性
     - 建议: 色彩优化方案 (如需要)

  2. 排版系统:
     - 提取: 字体族、字号层级、行高、字重
     - 评估: 可读性、层级清晰度
     - 建议: 排版优化方案 (如需要)

  3. 布局系统:
     - 提取: 栅格系统、间距规范、断点设置
     - 评估: 响应式表现、视觉节奏
     - 建议: 布局优化方案 (如需要)

  4. 图表系统:
     - 提取: 使用的图表库、图表类型、配色方案
     - 评估: 数据表现力、视觉美感
     - 建议: 图表优化方案

输出:
  - 设计风格分析报告
  - 优化建议清单
```

#### 2.3 整理优质设计方案

```yaml
设计方案要素:
  1. 保持一致性原则:
     - 沿用现有色彩方案 (除非明显不合理)
     - 保持现有布局模式 (除非存在可访问性问题)
     - 延续现有交互风格

  2. 增强数据可视化:
     方案A - Chart.js增强:
       - 饼图: 智能体组别分布
       - 柱状图: 各组智能体数量对比
       - 雷达图: 能力矩阵 (Agents/Commands/Skills/MCP)
       - 折线图: 项目活跃度趋势 (如有历史数据)

     方案B - 统计卡片:
       - 大数字卡片: 总智能体数、总命令数、总技能包数
       - 进度条卡片: PRP完成度、测试覆盖率
       - 徽章卡片: 技术栈标签云

     方案C - 交互式元素:
       - 时间线: 项目里程碑
       - 手风琴: 业务组详细信息
       - 标签页: 分类展示Agents/Commands/Skills

  3. 提升设计感:
     - 渐变背景 (subtle gradient)
     - 卡片阴影和悬停效果
     - 平滑过渡动画
     - 图标系统 (Font Awesome / Lucide)
     - 呼吸灯效果 (关键指标)

输出:
  - 设计方案文档
  - CSS样式规范
  - 图表配置模板
```

---

### Phase 3: 内容对比与更新计划 (20%)

**目标**: 识别过时内容，生成精确更新计划

#### 3.1 数据点对比

```yaml
对比维度:
  1. 数字指标:
     HTML现有 vs 项目实际:
       - 智能体总数
       - 各组智能体数量 (G/X/E/R/M/Z/F)
       - 命令总数
       - 技能包总数
       - MCP服务器数量
       - PRP文档数量

  2. 文本内容:
     HTML现有 vs 项目实际:
       - 项目简介
       - 核心定位
       - 技术栈列表
       - 主要功能特性

  3. 结构元素:
     HTML现有 vs 项目实际:
       - 业务组列表
       - 智能体名称
       - 命令名称
       - 技能包名称

标记策略:
  - ✅ 最新: 数据一致，无需更新
  - 🔄 过时: 数据不一致，需要更新
  - ➕ 新增: HTML缺失，需要添加
  - ➖ 移除: 项目已删除，需要移除

输出:
  - 数据对比报告
  - 更新清单 (标记每个数据点的状态)
```

#### 3.2 生成更新计划

```yaml
更新计划结构:
  1. 高优先级更新 (数字指标):
     - 更新智能体总数: 47 → 60 (示例)
     - 更新命令总数: 23 → 26 (示例)
     - 更新技能包总数: 30 → 33 (示例)

  2. 中优先级更新 (文本内容):
     - 更新项目简介 (如有变化)
     - 更新技术栈列表 (如有新增/移除)
     - 更新功能特性描述

  3. 低优先级更新 (视觉优化):
     - 新增图表: 智能体分布饼图
     - 优化卡片: 添加hover效果
     - 增强动画: 数字滚动效果

输出:
  - 结构化更新计划 (JSON格式)
  - 优先级排序
```

---

### Phase 4: 智能优化生成 (25%)

**目标**: 生成优化后的HTML，保持风格一致性

#### 4.1 执行数据更新

```yaml
更新策略:
  1. 精确替换:
     - 使用Edit工具定位精确位置
     - 替换过时数据为最新值
     - 示例:
         old_string: "<span class='count'>47</span>"
         new_string: "<span class='count'>60</span>"

  2. 批量更新:
     - 智能体数量: 各组数量同步更新
     - 技术栈标签: 添加新技术、移除已弃用
     - 统计卡片: 更新所有数值

  3. 动态生成:
     - 图表数据: 根据最新统计生成Chart.js配置
     - 表格行: 根据智能体/命令清单生成HTML行
     - 标签云: 根据技术栈生成徽章HTML

输出:
  - 更新后的HTML内容 (中间态)
```

#### 4.2 增强图表化表现

```yaml
图表增强方案:
  1. Chart.js图表 (如HTML使用Chart.js):
     饼图示例 - 智能体组别分布:
       ```javascript
       {
         type: 'doughnut',
         data: {
           labels: ['战略组(G)', '创意组(X)', '情报组(E)', '行政组(R)', '中台组(M)', '筹建组(Z)', '框架组(F)'],
           datasets: [{
             data: [9, 9, 8, 8, 9, 6, 11],  // 从项目扫描获取
             backgroundColor: ['#9333ea', '#ec4899', '#06b6d4', '#3b82f6', '#10b981', '#f59e0b', '#f97316']
           }]
         }
       }
       ```

     柱状图示例 - 能力矩阵:
       ```javascript
       {
         type: 'bar',
         data: {
           labels: ['智能体', '命令', '技能包', 'MCP服务器'],
           datasets: [{
             label: '数量',
             data: [60, 26, 33, 8],  // 从项目扫描获取
             backgroundColor: '#3b82f6'
           }]
         }
       }
       ```

  2. 统计卡片 (如HTML使用卡片布局):
     ```html
     <div class="stat-card">
       <div class="stat-icon">🤖</div>
       <div class="stat-number" data-target="60">0</div>
       <div class="stat-label">智能体总数</div>
     </div>
     ```

     CSS动画:
     ```css
     @keyframes countUp {
       from { opacity: 0; transform: translateY(20px); }
       to { opacity: 1; transform: translateY(0); }
     }
     ```

  3. 进度条组件:
     ```html
     <div class="progress-bar">
       <div class="progress-fill" style="width: 85%"></div>
       <span class="progress-label">PRP完成度: 85%</span>
     </div>
     ```

输出:
  - 增强后的图表HTML代码
  - Chart.js配置对象
  - CSS动画代码
```

#### 4.3 优化设计感

```yaml
视觉优化清单:
  1. 色彩增强:
     - 渐变背景:
       ```css
       background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
       ```
     - 卡片阴影:
       ```css
       box-shadow: 0 10px 30px rgba(0,0,0,0.1);
       ```

  2. 交互效果:
     - 卡片悬停:
       ```css
       .card:hover {
         transform: translateY(-5px);
         box-shadow: 0 15px 40px rgba(0,0,0,0.15);
       }
       ```
     - 按钮涟漪:
       ```css
       .button::after {
         content: '';
         position: absolute;
         background: rgba(255,255,255,0.5);
         border-radius: 50%;
         animation: ripple 0.6s ease-out;
       }
       ```

  3. 动画过渡:
     - 平滑滚动:
       ```css
       html { scroll-behavior: smooth; }
       ```
     - 元素淡入:
       ```css
       @keyframes fadeInUp {
         from { opacity: 0; transform: translateY(30px); }
         to { opacity: 1; transform: translateY(0); }
       }
       ```

  4. 图标系统:
     - 添加Font Awesome CDN (如未使用):
       ```html
       <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
       ```
     - 业务组图标映射:
       - 战略组: <i class="fas fa-chess-king"></i>
       - 创意组: <i class="fas fa-palette"></i>
       - 情报组: <i class="fas fa-search"></i>
       - 行政组: <i class="fas fa-briefcase"></i>
       - 中台组: <i class="fas fa-database"></i>
       - 筹建组: <i class="fas fa-hammer"></i>
       - 框架组: <i class="fas fa-code"></i>

输出:
  - 完整优化后的HTML文件
```

---

### Phase 5: 输出与验证 (5%)

**目标**: 保存优化结果，生成更新报告

#### 5.1 保存优化后的HTML

```yaml
保存策略:
  1. 备份原文件:
     - 备份路径: 原文件路径 + ".backup-" + 时间戳
     - 示例: "project-intro.html.backup-20251023-143000"

  2. 写入新内容:
     - 使用Write工具覆盖原文件
     - 保持文件权限和编码格式

输出:
  - 优化后的HTML文件 (保存到原路径)
  - 备份文件 (用于回滚)
```

#### 5.2 生成更新摘要报告

```yaml
报告内容:
  1. 执行摘要:
     - 目标文件: $1
     - 执行时间: 2025-10-23 14:30:00
     - 总耗时: 45秒

  2. 更新统计:
     - 数据点更新数量: 15个
     - 新增图表数量: 3个
     - 视觉优化项: 8个

  3. 关键更新明细:
     - ✅ 智能体总数: 47 → 60
     - ✅ 命令总数: 23 → 26
     - ✅ 技能包总数: 30 → 33
     - ➕ 新增饼图: 智能体组别分布
     - ➕ 新增柱状图: 能力矩阵
     - 🎨 优化卡片hover效果
     - 🎨 添加数字滚动动画

  4. 设计优化亮点:
     - 保持原有紫色渐变主题
     - 新增Chart.js交互式图表
     - 增强卡片阴影和悬停效果
     - 添加Font Awesome图标系统

  5. 文件位置:
     - 优化后文件: $1
     - 备份文件: $1.backup-20251023-143000

输出格式: Markdown

示例:
---

# /J 命令执行报告

**目标文件**: `ZTL数智化作战中心.html`
**执行时间**: 2025-10-23 14:30:00
**总耗时**: 45秒
**状态**: ✅ 成功

## 📊 更新统计

- 数据点更新: **15个**
- 新增图表: **3个**
- 视觉优化: **8项**

## 🔄 关键更新明细

### 数据同步
- ✅ 智能体总数: `47` → `60`
- ✅ 命令总数: `23` → `26`
- ✅ 技能包总数: `30` → `33`
- ✅ MCP服务器: `7` → `8`

### 图表增强
- ➕ 饼图: 智能体组别分布 (7组)
- ➕ 柱状图: 能力矩阵 (Agents/Commands/Skills/MCP)
- ➕ 进度条: PRP完成度 (85%)

### 视觉优化
- 🎨 卡片hover效果增强
- 🎨 数字滚动动画
- 🎨 Font Awesome图标系统
- 🎨 渐变背景优化

## 🎨 设计方案

**保持一致性**:
- ✅ 沿用紫色渐变主题 (#667eea → #764ba2)
- ✅ 保持卡片布局模式
- ✅ 延续现有排版系统

**增强表现力**:
- Chart.js 2.9.4 交互式图表
- CSS Grid 响应式布局
- Smooth scrolling 平滑滚动

## 📁 文件位置

- **优化后文件**: `ZTL数智化作战中心.html`
- **备份文件**: `ZTL数智化作战中心.html.backup-20251023-143000`

---

✨ **优化完成！** HTML项目综合介绍页面已更新至最新状态。

---
```

---

## 参数说明

**$1 (必需)**: HTML文件路径

```bash
示例:
  /J ZTL数智化作战中心.html
  /J output/project-showcase.html
  /J docs/index.html
```

---

## 工具使用清单

```yaml
文件操作工具:
  - Read: 读取HTML文件、项目配置文件
  - Write: 保存优化后的HTML
  - Edit: 精确更新特定数据点
  - Glob: 扫描项目目录结构
  - Grep: 搜索特定内容

MCP工具:
  - mcp__context7__resolve-library-id: 解析设计参考库ID
  - mcp__context7__get-library-docs: 获取设计最佳实践文档

搜索工具:
  - WebSearch: 补充搜索设计灵感 (如Context7无结果)
```

---

## 设计原则

### 1. 保持一致性优先

```yaml
原则:
  - 尊重现有设计风格，不做颠覆性改动
  - 色彩方案延续，除非存在可访问性问题
  - 布局模式保持，除非存在响应式缺陷
  - 交互风格一致，避免混乱的用户体验

示例:
  ✅ 好的做法:
    - 原HTML用紫色主题 → 保持紫色系，优化色阶
    - 原HTML用卡片布局 → 保持卡片，增强阴影效果
    - 原HTML用Chart.js → 保持Chart.js，添加新图表

  ❌ 不好的做法:
    - 原HTML用紫色主题 → 改为绿色主题 (除非用户明确要求)
    - 原HTML用卡片布局 → 改为列表布局
    - 原HTML用Chart.js → 改为D3.js
```

### 2. 数据准确性至上

```yaml
原则:
  - 所有数字指标必须与项目实际状态一致
  - 定期执行/J命令，保持HTML与项目同步
  - 优先更新核心数据，其次优化视觉

验证清单:
  ✅ 智能体总数 = .claude/agents/ 目录下所有.md文件数量
  ✅ 命令总数 = .claude/commands/ 目录下所有.md文件数量
  ✅ 技能包总数 = .claude/skills/ 目录下所有SKILL.md文件数量
  ✅ 技术栈 = package.json + requirements.txt + settings.json
```

### 3. 渐进增强，避免过度设计

```yaml
原则:
  - 增强应该是subtle（微妙）的，不是dramatic（戏剧性）的
  - 优先添加实用的图表，而非装饰性的动画
  - 保持加载速度，避免引入大型库

示例:
  ✅ 好的增强:
    - 添加饼图展示智能体分布 (实用)
    - 卡片hover时轻微上浮 (subtle)
    - 数字滚动动画 (轻量级)

  ❌ 过度设计:
    - 添加3D粒子背景效果 (装饰性，影响性能)
    - 引入Three.js做3D可视化 (大型库，非必需)
    - 每个元素都有复杂动画 (影响可读性)
```

---

## 典型使用场景

### 场景1: 定期同步项目状态

```bash
# 每周执行一次，保持HTML与项目同步
/J ZTL数智化作战中心.html

# 自动检测更新:
# - 智能体数量变化
# - 命令新增/移除
# - 技能包更新
# - MCP服务器变化
```

### 场景2: 重大版本发布前优化

```bash
# 在v2.0发布前，全面优化项目展示页面
/J docs/project-showcase.html

# 自动执行:
# 1. 同步最新数据 (v2.0新功能)
# 2. 研究最新设计趋势 (Context7)
# 3. 增强图表表现力
# 4. 优化视觉设计感
```

### 场景3: 首次创建项目展示页面

```bash
# 如果HTML是空白模板或基础版本
/J output/new-project-intro.html

# 自动生成:
# - 完整的项目数据展示
# - 多类型图表 (饼图、柱状图、进度条)
# - 现代化设计风格
# - 响应式布局
```

---

## 错误处理

### 常见错误与解决方案

```yaml
错误1: HTML文件不存在
  提示: "❌ 错误: 找不到HTML文件 'xxx.html'"
  解决: 检查文件路径是否正确，使用绝对路径或相对于项目根目录的路径

错误2: HTML格式损坏
  提示: "⚠️ 警告: HTML结构不完整，可能影响更新效果"
  解决: 手动修复HTML语法错误，或使用HTML验证工具检查

错误3: Context7无相关文档
  提示: "⚠️ 未找到相关设计参考，将使用内置设计方案"
  解决: 正常情况，使用内置的设计优化策略

错误4: 项目配置文件缺失
  提示: "⚠️ CLAUDE.md不存在，无法提取项目信息"
  解决: 确保在ZTL项目根目录执行命令，或手动创建CLAUDE.md
```

---

## 版本历史

```yaml
v1.0.0 (2025-10-23):
  - ✅ 初始版本发布
  - ✅ 支持项目状态全面扫描
  - ✅ 集成Context7最佳实践搜索
  - ✅ 智能数据对比与更新
  - ✅ 图表化表现增强
  - ✅ 设计感优化
  - ✅ 自动备份机制
```

---

## 注意事项

1. **执行前确认**: 命令会覆盖原HTML文件（已创建备份），确保文件路径正确
2. **Context7依赖**: 需要Context7 MCP服务器正常运行
3. **Chart.js版本**: 如HTML使用Chart.js，建议使用2.9.4+版本
4. **浏览器兼容**: 生成的HTML兼容现代浏览器 (Chrome/Firefox/Safari/Edge)
5. **备份保留**: 备份文件不会自动删除，建议定期清理旧备份

---

**命令名称**: HTML项目综合介绍页面智能更新优化器
**快捷键**: `/J`
**版本**: v1.0.0
**最后更新**: 2025-10-23
**作者**: ZTL数智化作战中心
**兼容**: Claude Code v1.0+, Sonnet 4.5
