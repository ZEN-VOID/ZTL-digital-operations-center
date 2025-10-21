---
name: HTML页面创建指令
description: 将数据内容转化为专业的HTML可视化页面，支持15+图表类型和4种设计风格
version: 2.1.0
last_updated: 2025-10-11
architecture: 三层架构 - 智能理解层 + 参数配置层 + 脚本执行层
mcp_integration: chart-generator-mcp
output_directory: output/html/
screenshot_directory: output/screenshots/
screenshot_format: png
---

# J - HTML页面创建指令

> 专业的HTML页面生成工具，支持数据可视化、图表生成、响应式设计和交互功能

## 📋 概述

**功能定位**: 将用户提供的数据、内容或需求转化为专业美观的HTML页面，集成chart-generator-mcp实现强大的数据可视化能力。

**核心能力**:
- 15+种图表类型支持（折线图、柱状图、饼图、雷达图、热力图、词云、网络图等）
- 4种专业设计风格（商务报告、暗黑仪表盘、清新文档、创意展示）
- 响应式布局设计（移动端/平板/PC端自适应）
- 交互功能集成（图表联动、数据筛选、导出功能）
- 标准化输出结构

## 🎯 核心职责

### 1. 数据分析与处理
- 理解用户提供的原始数据结构
- 识别数据类型和适合的可视化方式
- 数据清洗和格式转换
- 计算统计指标和衍生数据

### 2. 可视化方案设计
- 根据数据特征选择最佳图表类型
- 设计页面布局和信息架构
- 确定配色方案和视觉风格
- 规划交互逻辑和用户体验

### 3. HTML页面生成
- 使用chart-generator-mcp生成图表
- 编写符合标准的HTML5结构
- 实现响应式CSS样式
- 集成JavaScript交互功能

### 4. 质量保证
- 验证页面在不同浏览器的兼容性
- 测试响应式布局效果
- 检查数据准确性
- 优化页面加载性能

### 5. 文档输出
- 生成标准化的HTML文件
- 创建页面使用说明文档
- 提供数据更新指南
- 输出技术实现文档

## 🔄 工作流程

### 标准五步流程

#### 步骤1: 需求分析（2-5分钟）
**输入**: 用户描述或数据文件
**处理**:
- 理解用户需求和目标受众
- 分析数据结构和字段含义
- 识别关键指标和展示重点
- 确定页面功能需求

**输出**: 结构化的需求文档

#### 步骤2: 方案设计（3-8分钟）
**输入**: 需求文档
**处理**:
- 选择合适的图表类型组合
- 设计页面布局和信息层级
- 确定视觉风格和配色方案
- 规划交互功能

**输出**: 可视化设计方案（包含图表类型、布局草图、风格定义）

#### 步骤3: 图表生成（5-15分钟）
**输入**: 设计方案 + 数据
**处理**:
- 准备符合chart-generator-mcp格式的数据
- 调用相应的图表生成工具
- 配置图表参数（标题、坐标轴、颜色、尺寸）
- 生成所有需要的图表

**输出**: 图表文件集合（SVG/PNG格式）

#### 步骤4: 页面集成（10-20分钟）
**输入**: 图表文件 + 设计方案
**处理**:
- 编写HTML5页面结构
- 实现响应式CSS样式
- 集成生成的图表
- 添加JavaScript交互功能
- 优化页面性能

**输出**: 完整的HTML页面文件

#### 步骤5: 测试与交付（3-5分钟）
**输入**: HTML页面
**处理**:
- 在不同浏览器测试显示效果
- 验证响应式布局
- 检查数据准确性
- 生成使用文档

**输出**: 最终交付包（HTML + 资源文件 + 文档）

### 快速三步流程（简单场景）

**适用场景**: 单一图表、简单数据、标准模板

1. **数据准备**（1-2分钟）: 格式化数据
2. **图表生成**（2-5分钟）: 调用chart-generator-mcp
3. **页面封装**（3-5分钟）: 套用标准模板

### 高级七步流程（复杂场景）

**适用场景**: 多图表组合、复杂交互、定制化需求

1. **深度需求调研**（5-10分钟）
2. **数据探索分析**（5-10分钟）
3. **原型设计**（10-15分钟）
4. **图表批量生成**（10-30分钟）
5. **页面开发**（20-40分钟）
6. **交互功能实现**（10-20分钟）
7. **全面测试与优化**（10-15分钟）

## 💼 使用场景

### 场景1: 数据报告生成
**需求**: 将业务数据转化为可视化报告

**示例**:
```
用户: "帮我创建一个销售数据报告页面，包含月度趋势、区域对比、产品排名"

执行流程:
1. 分析销售数据结构（时间、区域、产品、金额）
2. 设计方案: 折线图（趋势）+ 柱状图（区域对比）+ 饼图（产品占比）
3. 调用chart-generator-mcp生成三个图表
4. 创建响应式HTML页面，使用"商务报告"风格
5. 添加数据筛选和导出功能
6. 输出: output/html/sales-report-2024.html
```

### 场景2: 仪表盘页面
**需求**: 创建实时数据监控仪表盘

**示例**:
```
用户: "制作一个系统监控仪表盘，显示CPU、内存、网络、磁盘使用情况"

执行流程:
1. 理解监控指标和实时更新需求
2. 设计方案: 仪表盘（当前值）+ 折线图（历史趋势）+ 环形图（资源占比）
3. 使用chart-generator-mcp生成基础图表
4. 创建HTML页面，使用"暗黑仪表盘"风格
5. 实现JavaScript定时刷新功能
6. 输出: output/html/system-monitor.html
```

### 场景3: 数据分析展示
**需求**: 展示数据分析结果和洞察

**示例**:
```
用户: "基于用户行为数据，创建一个分析展示页面"

执行流程:
1. 分析用户行为数据（访问路径、停留时间、转化漏斗）
2. 设计方案: 桑基图（流量路径）+ 漏斗图（转化分析）+ 热力图（活跃时段）
3. 调用chart-generator-mcp生成复杂图表
4. 创建HTML页面，使用"清新文档"风格
5. 添加交互式筛选和钻取功能
6. 输出: output/html/user-behavior-analysis.html
```

### 场景4: 知识可视化
**需求**: 将概念、关系转化为可视化内容

**示例**:
```
用户: "创建一个技术架构可视化页面"

执行流程:
1. 理解技术组件和依赖关系
2. 设计方案: 网络图（组件关系）+ 思维导图（架构层级）+ 旭日图（模块结构）
3. 使用chart-generator-mcp生成图表
4. 创建HTML页面，使用"创意展示"风格
5. 实现节点点击展开/收起功能
6. 输出: output/html/tech-architecture.html
```

### 场景5: 数据对比展示
**需求**: 多维度数据对比分析

**示例**:
```
用户: "对比三个产品的各项指标"

执行流程:
1. 整理产品指标数据（性能、价格、用户评分等）
2. 设计方案: 雷达图（综合对比）+ 组合柱状图（指标对比）+ 评分卡片
3. 调用chart-generator-mcp生成图表
4. 创建HTML页面，使用"商务报告"风格
5. 添加产品切换和指标筛选功能
6. 输出: output/html/product-comparison.html
```

## 🛠️ chart-generator-mcp工具集成

### 可用图表类型（15+种）

#### 1. 折线图 (Line Chart)
**工具**: `mcp__chart-generator__generate_line_chart`
**适用场景**: 时间序列趋势、连续数据变化
**数据格式**:
```json
{
  "data": [
    {"time": "2024-01", "value": 120},
    {"time": "2024-02", "value": 145}
  ],
  "title": "月度销售趋势",
  "axisXTitle": "月份",
  "axisYTitle": "销售额（万元）"
}
```

#### 2. 柱状图 (Bar/Column Chart)
**工具**: `mcp__chart-generator__generate_column_chart` / `generate_bar_chart`
**适用场景**: 分类数据对比、排名展示
**数据格式**:
```json
{
  "data": [
    {"category": "北京", "value": 825, "group": "油车"},
    {"category": "上海", "value": 920, "group": "油车"}
  ],
  "group": true,
  "title": "各城市销量对比"
}
```

#### 3. 饼图 (Pie Chart)
**工具**: `mcp__chart-generator__generate_pie_chart`
**适用场景**: 占比分析、构成展示
**数据格式**:
```json
{
  "data": [
    {"category": "产品A", "value": 35},
    {"category": "产品B", "value": 25}
  ],
  "title": "市场份额分布",
  "innerRadius": 0.6
}
```

#### 4. 散点图 (Scatter Chart)
**工具**: `mcp__chart-generator__generate_scatter_chart`
**适用场景**: 相关性分析、分布展示
**数据格式**:
```json
{
  "data": [
    {"x": 120, "y": 80},
    {"x": 150, "y": 95}
  ],
  "title": "身高体重关系",
  "axisXTitle": "身高(cm)",
  "axisYTitle": "体重(kg)"
}
```

#### 5. 雷达图 (Radar Chart)
**工具**: `mcp__chart-generator__generate_radar_chart`
**适用场景**: 多维度对比、能力评估
**数据格式**:
```json
{
  "data": [
    {"name": "性能", "value": 85, "group": "产品A"},
    {"name": "价格", "value": 70, "group": "产品A"}
  ],
  "title": "产品综合评分"
}
```

#### 6. 面积图 (Area Chart)
**工具**: `mcp__chart-generator__generate_area_chart`
**适用场景**: 累积趋势、量级变化
**数据格式**:
```json
{
  "data": [
    {"time": "2024-01", "value": 100, "group": "渠道A"},
    {"time": "2024-01", "value": 80, "group": "渠道B"}
  ],
  "stack": true,
  "title": "渠道销售累积"
}
```

#### 7. 直方图 (Histogram Chart)
**工具**: `mcp__chart-generator__generate_histogram_chart`
**适用场景**: 分布分析、频率统计
**数据格式**:
```json
{
  "data": [78, 88, 60, 100, 95, 82, 91],
  "binNumber": 5,
  "title": "考试成绩分布",
  "axisXTitle": "分数区间",
  "axisYTitle": "人数"
}
```

#### 8. 词云图 (Word Cloud)
**工具**: `mcp__chart-generator__generate_word_cloud_chart`
**适用场景**: 文本分析、关键词展示
**数据格式**:
```json
{
  "data": [
    {"text": "人工智能", "value": 95},
    {"text": "机器学习", "value": 80}
  ],
  "title": "技术热词"
}
```

#### 9. 网络图 (Network Graph)
**工具**: `mcp__chart-generator__generate_network_graph`
**适用场景**: 关系展示、节点连接
**数据格式**:
```json
{
  "data": {
    "nodes": [
      {"name": "节点A"},
      {"name": "节点B"}
    ],
    "edges": [
      {"source": "节点A", "target": "节点B", "name": "关系1"}
    ]
  },
  "title": "技术架构关系图"
}
```

#### 10. 思维导图 (Mind Map)
**工具**: `mcp__chart-generator__generate_mind_map`
**适用场景**: 层级结构、知识组织
**数据格式**:
```json
{
  "data": {
    "name": "主题",
    "children": [
      {
        "name": "子主题1",
        "children": [
          {"name": "细节1-1"}
        ]
      }
    ]
  }
}
```

#### 11. 流程图 (Flow Diagram)
**工具**: `mcp__chart-generator__generate_flow_diagram`
**适用场景**: 流程展示、步骤说明
**数据格式**:
```json
{
  "data": {
    "nodes": [
      {"name": "开始"},
      {"name": "步骤1"}
    ],
    "edges": [
      {"source": "开始", "target": "步骤1", "name": "执行"}
    ]
  }
}
```

#### 12. 鱼骨图 (Fishbone Diagram)
**工具**: `mcp__chart-generator__generate_fishbone_diagram`
**适用场景**: 因果分析、问题诊断
**数据格式**:
```json
{
  "data": {
    "name": "核心问题",
    "children": [
      {
        "name": "原因类别1",
        "children": [
          {"name": "具体原因1-1"}
        ]
      }
    ]
  }
}
```

#### 13. 树形图 (Treemap Chart)
**工具**: `mcp__chart-generator__generate_treemap_chart`
**适用场景**: 层级占比、空间分配
**数据格式**:
```json
{
  "data": [
    {
      "name": "模块A",
      "value": 100,
      "children": [
        {"name": "子模块A1", "value": 40}
      ]
    }
  ],
  "title": "代码模块占比"
}
```

#### 14. 双轴图 (Dual Axes Chart)
**工具**: `mcp__chart-generator__generate_dual_axes_chart`
**适用场景**: 双指标对比、趋势+占比
**数据格式**:
```json
{
  "categories": ["2020", "2021", "2022"],
  "series": [
    {
      "type": "column",
      "data": [100, 120, 150],
      "axisYTitle": "销售额"
    },
    {
      "type": "line",
      "data": [0.05, 0.06, 0.07],
      "axisYTitle": "利润率"
    }
  ],
  "title": "销售与利润趋势"
}
```

#### 15. 漏斗图 (Funnel Chart)
**用途**: 转化分析、流程阶段
**实现方式**: 使用柱状图变体或自定义SVG

#### 16. 热力图 (Heatmap)
**用途**: 密度分析、时间分布
**实现方式**: 基于散点图扩展

### 图表配置参数

**通用参数**:
- `title`: 图表标题
- `width`: 图表宽度（默认600px）
- `height`: 图表高度（默认400px）
- `theme`: 主题风格（default/academy）

**坐标轴参数**:
- `axisXTitle`: X轴标题
- `axisYTitle`: Y轴标题

**高级参数**:
- `stack`: 是否堆叠（面积图、柱状图）
- `group`: 是否分组（柱状图）
- `innerRadius`: 内半径（饼图，用于环形图）
- `binNumber`: 区间数量（直方图）

## 🎨 设计风格库

### 风格1: 商务报告 (Professional Report)
**配色方案**: 蓝色系（#1f77b4, #ff7f0e, #2ca02c）
**字体**: Arial, "Microsoft YaHei"
**布局**: 网格布局，清晰分区
**适用场景**: 企业报告、数据分析、商务展示

**CSS样式**:
```css
body {
  font-family: Arial, "Microsoft YaHei", sans-serif;
  background: #f5f5f5;
  color: #333;
}
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
.chart-section {
  background: white;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
```

### 风格2: 暗黑仪表盘 (Dark Dashboard)
**配色方案**: 深色背景（#1a1a1a）+ 荧光色点缀
**字体**: "Courier New", monospace
**布局**: 流式布局，全屏展示
**适用场景**: 监控面板、实时数据、科技感展示

**CSS样式**:
```css
body {
  font-family: "Courier New", monospace;
  background: #1a1a1a;
  color: #00ff00;
}
.dashboard {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
  padding: 20px;
}
.widget {
  background: #2a2a2a;
  border: 1px solid #00ff00;
  padding: 15px;
  border-radius: 4px;
}
```

### 风格3: 清新文档 (Clean Document)
**配色方案**: 淡色系（#e8f4f8, #d4edda）
**字体**: "Segoe UI", Tahoma, sans-serif
**布局**: 单列布局，文档流
**适用场景**: 分析报告、知识文档、教学材料

**CSS样式**:
```css
body {
  font-family: "Segoe UI", Tahoma, sans-serif;
  background: white;
  color: #333;
  line-height: 1.6;
}
.document {
  max-width: 900px;
  margin: 40px auto;
  padding: 40px;
}
.chart-wrapper {
  margin: 30px 0;
  padding: 20px;
  background: #f9f9f9;
  border-left: 4px solid #4CAF50;
}
```

### 风格4: 创意展示 (Creative Showcase)
**配色方案**: 渐变色+高对比度
**字体**: "Helvetica Neue", Arial, sans-serif
**布局**: 不规则布局，视觉冲击
**适用场景**: 作品展示、创意提案、品牌宣传

**CSS样式**:
```css
body {
  font-family: "Helvetica Neue", Arial, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}
.showcase {
  padding: 40px;
}
.item {
  background: rgba(255,255,255,0.1);
  backdrop-filter: blur(10px);
  padding: 30px;
  margin: 20px 0;
  border-radius: 20px;
  transform: rotate(-2deg);
}
.item:nth-child(even) {
  transform: rotate(2deg);
}
```

## ✅ 质量标准

### 必须达标（强制要求）

#### 1. 数据准确性
- 图表数据与源数据100%一致
- 计算结果准确无误
- 单位标注清晰正确

#### 2. 浏览器兼容
- 支持Chrome、Firefox、Safari、Edge最新版本
- 降级支持IE11（可选）
- 移动端浏览器正常显示

#### 3. 响应式设计
- 手机端（< 768px）单列布局
- 平板端（768px-1024px）双列布局
- 桌面端（> 1024px）多列布局
- 图表尺寸自适应

#### 4. 代码规范
- 使用HTML5语义化标签
- CSS符合BEM命名规范
- JavaScript使用ES6+语法
- 代码有适当注释

#### 5. 性能要求
- 页面加载时间 < 3秒
- 图表渲染时间 < 1秒
- 交互响应时间 < 200ms
- 页面总大小 < 2MB

### 卓越标准（追求目标）

#### 1. 视觉设计
- 配色符合品牌规范或设计美学
- 图表样式统一协调
- 视觉层级清晰合理
- 留白和间距恰当

#### 2. 用户体验
- 交互反馈及时明确
- 操作流程简洁直观
- 错误提示友好清晰
- 支持键盘导航

#### 3. 可访问性
- 支持屏幕阅读器
- 颜色对比度符合WCAG标准
- 图表提供文本替代说明
- 支持高对比度模式

#### 4. 可维护性
- 代码结构清晰模块化
- 变量和函数命名语义化
- 配置与代码分离
- 提供完整的技术文档

#### 5. 扩展性
- 支持自定义主题
- 预留数据更新接口
- 支持插件扩展
- 配置参数化

## 🔗 协作接口

### 上游智能体

**数据提供方**:
- E3（图片识别）: 提供图片分析数据
- R0（数据分析）: 提供Figma设计数据
- 任何提供结构化数据的智能体

**调用方式**: 接收JSON格式数据或数据文件路径

### 下游智能体

**内容消费方**:
- K（网页自动化）: 自动化测试生成的HTML页面
- 任何需要可视化展示的智能体

**输出格式**: 标准HTML文件 + 资源文件包

### 并行协作

**同级智能体**:
- R3（批量替换）: 批量生成多个数据页面
- E1（文生图）: 为页面生成配图素材

## 📁 输出规范

### 目录结构
```
output/html/
├── {project-name}/
│   ├── index.html           # 主页面
│   ├── css/
│   │   ├── main.css         # 主样式
│   │   └── charts.css       # 图表样式
│   ├── js/
│   │   ├── main.js          # 主脚本
│   │   └── charts.js        # 图表交互
│   ├── images/              # 图表图片
│   │   ├── chart1.svg
│   │   └── chart2.png
│   ├── data/                # 数据文件（可选）
│   │   └── data.json
│   └── README.md            # 页面说明文档
```

### 文件命名规范
- **HTML文件**: `{purpose}-{date}.html` (如 sales-report-2024.html)
- **图表文件**: `chart-{type}-{index}.{format}` (如 chart-line-01.svg)
- **样式文件**: `{purpose}.css` (如 main.css, theme-dark.css)
- **脚本文件**: `{purpose}.js` (如 main.js, interactions.js)

### HTML模板结构
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{页面标题}</title>
    <link rel="stylesheet" href="css/main.css">
</head>
<body>
    <header>
        <h1>{报告标题}</h1>
        <p class="meta">{日期} | {创建者}</p>
    </header>

    <main class="container">
        <section class="chart-section">
            <h2>{章节标题}</h2>
            <div class="chart-container">
                <img src="images/chart1.svg" alt="{图表描述}">
            </div>
            <p class="description">{数据说明}</p>
        </section>

        <!-- 更多章节... -->
    </main>

    <footer>
        <p>Generated by HTML页面创建指令 | Version 2.0.0</p>
    </footer>

    <script src="js/main.js"></script>
</body>
</html>
```

### README文档模板
```markdown
# {页面名称}

## 页面信息
- **创建时间**: {YYYY-MM-DD HH:mm:ss}
- **数据来源**: {数据来源说明}
- **设计风格**: {风格名称}
- **图表数量**: {数量}

## 图表说明
1. **{图表1名称}**: {图表1说明}
2. **{图表2名称}**: {图表2说明}

## 使用方法
1. 在浏览器中打开 `index.html`
2. 查看各个数据可视化图表
3. 使用交互功能（如有）筛选和探索数据

## 数据更新
如需更新数据，请修改 `data/data.json` 文件，然后刷新页面。

## 技术说明
- 图表生成工具: chart-generator-mcp
- 响应式框架: 自定义CSS Grid
- 交互功能: Vanilla JavaScript

## 联系方式
如有问题，请联系 {创建者}
```

## 🎯 使用方法

### 基本调用
```
/J 创建一个销售数据报告页面，包含月度趋势和区域对比
```

### 指定风格
```
/J 使用暗黑仪表盘风格，创建系统监控页面
```

### 复杂需求
```
/J 基于以下数据创建多图表分析页面：
[数据内容或文件路径]

要求：
- 使用商务报告风格
- 包含折线图、柱状图、饼图
- 添加数据筛选功能
- 支持导出为PDF
```

### 指定输出位置
```
/J 创建产品对比页面，输出到 output/html/product-comparison/
```

## 📚 实际案例

### 案例1: 销售数据报告
**输入**:
```json
{
  "monthly_sales": [
    {"month": "2024-01", "amount": 1200000},
    {"month": "2024-02", "amount": 1350000}
  ],
  "regional_sales": [
    {"region": "华东", "amount": 3500000},
    {"region": "华北", "amount": 2800000}
  ]
}
```

**输出**: `output/html/sales-report-2024/index.html`
- 折线图: 月度销售趋势
- 柱状图: 区域销售对比
- 饼图: 区域销售占比
- 商务报告风格
- 响应式布局

### 案例2: 技术架构可视化
**输入**: "展示微服务架构的组件和依赖关系"

**输出**: `output/html/architecture-diagram/index.html`
- 网络图: 服务依赖关系
- 思维导图: 技术栈层级
- 创意展示风格
- 节点交互功能

### 案例3: 用户行为分析
**输入**: 用户行为日志数据（CSV文件）

**输出**: `output/html/user-behavior/index.html`
- 漏斗图: 转化路径
- 热力图: 活跃时段
- 桑基图: 流量来源
- 清新文档风格
- 时间范围筛选

## ❓ 常见问题

### Q1: 如何选择合适的图表类型？
**A**: 根据数据特征和展示目标：
- 趋势变化 → 折线图/面积图
- 分类对比 → 柱状图/条形图
- 占比构成 → 饼图/环形图
- 相关分析 → 散点图
- 多维对比 → 雷达图
- 层级结构 → 树形图/思维导图
- 关系网络 → 网络图

### Q2: 如何处理大数据量？
**A**: 采用以下策略：
- 数据聚合: 按时间段或分类聚合
- 分页展示: 将数据分批加载
- 懒加载: 滚动时加载图表
- 采样显示: 显示代表性数据点
- 服务端渲染: 预生成静态图表

### Q3: 如何自定义主题？
**A**: 修改CSS变量或覆盖样式：
```css
:root {
  --primary-color: #your-color;
  --background-color: #your-bg;
  --text-color: #your-text;
}
```

### Q4: 如何更新页面数据？
**A**: 三种方式：
1. 重新运行指令生成新页面
2. 修改data.json后刷新页面（需实现动态加载）
3. 使用API接口定时更新（高级功能）

### Q5: 如何导出或分享页面？
**A**:
- 直接分享HTML文件包（需服务器托管）
- 转换为PDF（使用浏览器打印功能）
- 生成静态截图（使用截图工具）
- 部署到Web服务器（支持在线访问）

## 📖 相关资源

### 官方文档
- chart-generator-mcp使用文档
- HTML5/CSS3标准规范
- 响应式设计最佳实践

### 参考教程
- 数据可视化设计指南
- 图表选择决策树
- Web性能优化手册

### 工具推荐
- 在线配色工具: coolors.co
- 响应式测试: responsively.app
- 图表灵感: datavizproject.com

---

**版本**: 2.0.0
**更新日期**: 2025-10-11
**维护者**: Claude Code Framework
**协议**: MIT License
