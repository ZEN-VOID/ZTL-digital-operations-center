# PowerPoint Generator Skill

专业的PowerPoint演示文稿生成技能包，提供三种强大的生成方法，适用于各种商务场景。

## 🎯 核心特性

- **三种生成方法**：直接生成、HTML转换、模板生成
- **丰富的幻灯片类型**：标题、内容、双栏、表格、图片、图表
- **预定义模板**：商业报告、产品发布、培训材料、投资路演
- **流畅的API**：支持方法链式调用，代码简洁优雅
- **完整的日志**：详细的执行日志，便于调试和监控
- **统一输出路径**：按业务类型自动分类存储

## 📦 依赖安装

```bash
pip install python-pptx beautifulsoup4 lxml pillow
```

## 🚀 快速开始

### 方法1：直接生成（推荐）

最灵活的方法，完全编程化控制每个元素。

```python
import sys
sys.path.append('./.claude/skills/office/ppt/scripts')
from ppt_generator import PPTGenerator

# 创建生成器
generator = PPTGenerator()

# 添加标题页
generator.add_title_slide(
    title="ZTL数智化作战中心",
    subtitle="餐饮行业数智化转型平台"
)

# 添加内容页
generator.add_content_slide(
    title="核心优势",
    content=[
        "66个专业智能体协同工作",
        "6大业务组全链路覆盖",
        "基于Claude Sonnet 4.5"
    ]
)

# 添加表格页
generator.add_table_slide(
    title="业务矩阵",
    headers=["业务组", "智能体数量", "核心职能"],
    rows=[
        ["战略组", "9个", "战略规划、经营分析"],
        ["创意组", "9个", "广告策划、内容创作"]
    ]
)

# 保存演示文稿
generator.save("output/行政组/营销宣传/presentation.pptx")
```

### 方法2：HTML转PPT

适合已有HTML内容的场景，快速转换。

```python
from html_to_ppt_converter import convert_html_to_ppt

html_content = """
<section>
    <h1>项目概述</h1>
    <p>这是一个餐饮数智化项目</p>
    <ul>
        <li>智能体协作</li>
        <li>数据分析</li>
        <li>自动化运营</li>
    </ul>
</section>
"""

convert_html_to_ppt(
    html_content=html_content,
    output_path="output/行政组/技术手册/presentation.pptx"
)
```

### 方法3：模板生成

使用预定义模板快速创建标准化演示文稿。

```python
from ppt_generator import create_from_template

result = create_from_template(
    template_type="business-report",
    data={
        "title": "Q3经营报告",
        "period": "2025年第三季度",
        "executive_summary": "业绩良好，同比增长25%",
        "metrics": {
            "营业额": "450万",
            "增长率": "+25%"
        },
        "achievements": [
            "新店成功开业",
            "线上渠道增长迅猛"
        ]
    },
    output_path="output/行政组/经营分析/q3-report.pptx"
)
```

## 📊 幻灯片类型

### 1. 标题页
```python
generator.add_title_slide(
    title="主标题",
    subtitle="副标题"
)
```

### 2. 内容页（要点列表）
```python
generator.add_content_slide(
    title="幻灯片标题",
    content=["要点1", "要点2", "要点3"]
)
```

### 3. 双栏页
```python
generator.add_two_column_slide(
    title="对比分析",
    left_content=["优点1", "优点2"],
    right_content=["缺点1", "缺点2"]
)
```

### 4. 表格页
```python
generator.add_table_slide(
    title="数据表格",
    headers=["列1", "列2", "列3"],
    rows=[
        ["A1", "B1", "C1"],
        ["A2", "B2", "C2"]
    ]
)
```

### 5. 图片页
```python
generator.add_image_slide(
    title="图表展示",
    image_path="charts/sales-trend.png",
    width=6.0,
    caption="销售趋势图"
)
```

### 6. 图表页
```python
generator.add_chart_slide(
    title="销售趋势",
    chart_type="line",  # line, bar, column, pie
    data={
        "categories": ["Q1", "Q2", "Q3", "Q4"],
        "series": [
            {"name": "2024", "values": [100, 120, 150, 180]},
            {"name": "2025", "values": [120, 150, 180, 220]}
        ]
    }
)
```

## 📋 预定义模板

### 1. business-report（商业报告）
适用于季度报告、年度总结等。

**必需字段**：
- `title`: 报告标题
- `period`: 报告期间
- `executive_summary`: 执行摘要
- `metrics`: 关键指标（字典）
- `achievements`: 主要成就（列表）
- `challenges`: 挑战与问题（列表）
- `next_steps`: 下一步行动（列表）

### 2. product-launch（产品发布）
适用于新品发布、营销活动等。

**必需字段**：
- `product_name`: 产品名称
- `problem`: 问题描述
- `solution`: 解决方案
- `features`: 功能特性（列表）
- `benefits`: 客户收益（列表）
- `timeline`: 发布时间线（列表字典）

### 3. training（培训材料）
适用于员工培训、工作坊等。

**必需字段**：
- `course_name`: 课程名称
- `objectives`: 学习目标（列表）
- `modules`: 培训模块（列表字典）
- `resources`: 额外资源（列表）

### 4. pitch（投资路演）
适用于融资路演、商业提案等。

**必需字段**：
- `company_name`: 公司名称
- `problem`: 问题陈述
- `solution`: 解决方案
- `market_size`: 市场机会
- `business_model`: 商业模式
- `traction`: 业务进展
- `team`: 团队成员（列表字典）
- `ask`: 融资需求

## 📁 输出路径规范

所有PPT文件统一输出到：`output/行政组/[项目名]/`

### 标准项目分类

```
output/行政组/
├── 营销宣传/           # 营销演示、品牌宣传
├── 经营分析/           # 经营报告、数据分析
├── 培训材料/           # 培训课程、工作坊
├── 产品发布/           # 产品发布、新品推广
├── 技术手册/           # 技术文档、架构介绍
└── 战略规划/           # 战略规划、年度计划
```

详细的输出路径配置说明请参考 [OUTPUT_PATH_CONFIG.md](OUTPUT_PATH_CONFIG.md)

## 🎨 高级功能

### 自定义样式

```python
from ppt_generator import PPTGenerator
from pptx.util import Pt
from pptx.dml.color import RGBColor

generator = PPTGenerator()
slide = generator.add_content_slide("标题", ["内容"])

# 自定义字体和颜色
for shape in slide.shapes:
    if hasattr(shape, "text_frame"):
        for paragraph in shape.text_frame.paragraphs:
            paragraph.font.size = Pt(24)
            paragraph.font.color.rgb = RGBColor(255, 0, 0)
            paragraph.font.bold = True
```

### 使用自定义模板

```python
# 加载现有模板
generator = PPTGenerator(template_path="templates/corporate-template.pptx")

# 所有幻灯片将使用模板的布局和样式
generator.add_title_slide("New Presentation", "Using Corporate Template")
```

### HTML结构说明

```html
<!DOCTYPE html>
<html>
<body>
    <!-- 每个section = 一张幻灯片 -->
    <section>
        <h1>Slide Title</h1>
        <p>Slide content paragraph</p>
        <ul>
            <li>Bullet point 1</li>
            <li>Bullet point 2</li>
        </ul>
    </section>

    <section>
        <h2>Another Slide</h2>
        <table>
            <tr>
                <th>Header 1</th>
                <th>Header 2</th>
            </tr>
            <tr>
                <td>Data 1</td>
                <td>Data 2</td>
            </tr>
        </table>
    </section>
</body>
</html>
```

## 🔧 错误处理

```python
result = create_from_template(...)

if result["success"]:
    print(f"演示文稿已创建: {result['file_path']}")
    print(f"幻灯片数量: {result['slide_count']}")
    print(f"文件大小: {result['size_bytes']:,} bytes")
else:
    print(f"创建失败: {result['error']}")
```

## 💡 最佳实践

1. **使用模板**：为一致性品牌形象使用企业模板
2. **限制文本**：每页5-7个要点为佳
3. **高质量图片**：至少1024x768分辨率
4. **实际测试**：在PowerPoint中测试后再分发
5. **控制文件大小**：建议<50MB以便邮件传输

## ⚠️ 限制说明

- 最大幻灯片数：约200张（实用限制）
- 嵌入视频：支持有限（建议使用链接）
- 动画效果：不支持（仅静态演示文稿）
- 母版编辑：请使用模板文件
- 3D图表：不支持（使用2D图表）

## 📚 示例文件

- `examples/example_direct.py` - 直接生成示例
- `examples/example_html.py` - HTML转换示例
- `examples/example_template.py` - 模板生成示例

## 🔗 相关Skills

- **word**: 生成Word文档
- **pdf**: 转换为PDF格式
- **excel-data-analyzer**: 为图表生成数据

## 📖 API参考

完整的API文档请参考 [SKILL.md](SKILL.md)

## 🆘 常见问题

**Q: 如何添加自定义模板？**
A: 使用 `PPTGenerator(template_path="your-template.pptx")` 加载自定义模板。

**Q: 支持哪些图表类型？**
A: 支持折线图(line)、柱状图(column)、条形图(bar)、饼图(pie)。

**Q: 如何添加图片？**
A: 使用 `add_image_slide(title, image_path)` 方法，图片需要是本地文件路径。

**Q: 可以自定义输出路径吗？**
A: 可以，但推荐使用统一的 `output/行政组/[项目名]/` 格式。

**Q: HTML转换支持哪些标签？**
A: 支持h1/h2、p、ul/ol、table、img等常用标签。

---

**版本**: v1.0.0
**最后更新**: 2025-10-21
**维护**: F5-Skills技能包创建工程师
