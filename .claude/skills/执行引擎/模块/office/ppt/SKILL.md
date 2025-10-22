---
name: PowerPoint Generator
description: Generate professional PowerPoint presentations (.pptx) with two powerful methods - Direct generation (python-pptx) for programmatic control, HTML→PPT conversion for web-style content. Supports templates, tables, images, and complex layouts.
category: office
version: 1.0.0
---

# PowerPoint Generator

## Quick Start

### Method 1: Direct Generation (Recommended)

```python
import sys
sys.path.append('./.claude/skills/office/ppt/scripts')
from ppt_generator import PPTGenerator

# Create generator
generator = PPTGenerator()

# Add title slide
generator.add_title_slide(
    title="ZTL数智化作战中心",
    subtitle="餐饮行业数智化转型平台"
)

# Add content slide
generator.add_content_slide(
    title="项目概述",
    content=[
        "基于Claude Code和多智能体协作",
        "6大业务组、66个专业智能体",
        "覆盖战略、创意、情报、行政、中台、筹建"
    ]
)

# Add table slide
generator.add_table_slide(
    title="业务矩阵",
    headers=["业务组", "系列", "数量", "核心职能"],
    rows=[
        ["战略组", "G系列", "9个", "战略规划、经营分析"],
        ["创意组", "X系列", "9个", "品牌营销、内容创作"]
    ]
)

# Save
generator.save("output/行政组/营销宣传/presentation.pptx")
```

### Method 2: HTML to PPT Conversion

```python
from html_to_ppt_converter import HTMLtoPPTConverter

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
<section>
    <h2>技术架构</h2>
    <p>基于Claude Code和MCP协议</p>
</section>
"""

converter = HTMLtoPPTConverter()
prs = converter.convert(html_content)
converter.save("output/行政组/营销宣传/presentation.pptx")
```

### Method 3: Template-Based Generation

```python
from ppt_generator import create_from_template

result = create_from_template(
    template_type="business-report",
    data={
        "title": "Q3经营报告",
        "subtitle": "2025年第三季度",
        "slides": [
            {
                "type": "content",
                "title": "业绩概览",
                "content": ["营业额450万", "同比增长25%", "利润率28%"]
            },
            {
                "type": "table",
                "title": "门店数据",
                "headers": ["门店", "营业额", "增长率"],
                "rows": [
                    ["A店", "150万", "+25%"],
                    ["B店", "120万", "+20%"]
                ]
            }
        ]
    },
    output_path="output/行政组/经营分析/q3-report.pptx"
)
```

## Generation Methods Comparison

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| **Direct Generation** | Business reports, data presentations | Full control, programmatic, supports all features | Requires Python coding |
| **HTML→PPT** | Web content, existing HTML | Easy conversion, familiar HTML/CSS | Limited layout control |
| **Template-Based** | Standardized reports | Quick generation, consistent style | Less flexible |

## Slide Types

### 1. Title Slide
```python
generator.add_title_slide(
    title="主标题",
    subtitle="副标题"
)
```

### 2. Content Slide (Bullet Points)
```python
generator.add_content_slide(
    title="幻灯片标题",
    content=[
        "要点1",
        "要点2",
        "要点3"
    ]
)
```

### 3. Two-Column Slide
```python
generator.add_two_column_slide(
    title="对比分析",
    left_content=["优点1", "优点2", "优点3"],
    right_content=["缺点1", "缺点2", "缺点3"]
)
```

### 4. Table Slide
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

### 5. Image Slide
```python
generator.add_image_slide(
    title="图表展示",
    image_path="charts/sales-trend.png"
)
```

### 6. Chart Slide
```python
generator.add_chart_slide(
    title="销售趋势",
    chart_type="line",  # line, bar, pie, column
    data={
        "categories": ["Q1", "Q2", "Q3", "Q4"],
        "series": [
            {"name": "2024", "values": [100, 120, 150, 180]},
            {"name": "2025", "values": [120, 150, 180, 220]}
        ]
    }
)
```

## Template Types

| Template | Use Case | Included Slides |
|----------|----------|-----------------|
| `business-report` | Business presentations, quarterly reports | Title, overview, data tables, charts |
| `product-launch` | Product launches, marketing campaigns | Title, features, benefits, timeline |
| `training` | Training materials, workshops | Title, agenda, content, exercises |
| `pitch` | Investor pitches, proposals | Title, problem, solution, market, team |

## Advanced Features

### Custom Styling

```python
from ppt_generator import PPTGenerator
from pptx.util import Pt
from pptx.dml.color import RGBColor

generator = PPTGenerator()

# Custom font and color
slide = generator.add_content_slide("标题", ["内容"])
for shape in slide.shapes:
    if hasattr(shape, "text_frame"):
        for paragraph in shape.text_frame.paragraphs:
            paragraph.font.size = Pt(24)
            paragraph.font.color.rgb = RGBColor(255, 0, 0)
            paragraph.font.bold = True
```

### Using Custom Templates

```python
# Load existing template
generator = PPTGenerator(template_path="templates/corporate-template.pptx")

# All slides will use the template's layouts and styling
generator.add_title_slide("New Presentation", "Using Corporate Template")
```

### HTML Structure for Conversion

```html
<!DOCTYPE html>
<html>
<body>
    <!-- Each section = one slide -->
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

## Output Structure

Presentations are organized by type:

```
output/行政组/
├── 营销宣传/          # Marketing presentations
├── 经营分析/          # Business analysis reports
├── 培训材料/          # Training materials
├── 产品发布/          # Product launches
└── 战略规划/          # Strategic planning
```

## Dependencies

```bash
pip install python-pptx beautifulsoup4 lxml pillow
```

## Error Handling

```python
result = create_from_template(...)

if result["success"]:
    print(f"Presentation created: {result['file_path']}")
    print(f"Slides: {result['slide_count']}")
else:
    print(f"Error: {result['error']}")
```

## Best Practices

1. **Use templates** for consistent branding
2. **Limit text** per slide (5-7 bullet points max)
3. **Use high-quality images** (at least 1024x768)
4. **Test on actual PowerPoint** before distributing
5. **Keep file size reasonable** (<50MB for email)

## Limitations

- Maximum slides per presentation: ~200 (practical limit)
- Embedded video: Limited support (use links instead)
- Animations: Not supported (static presentations only)
- Master slide editing: Use template files instead
- 3D charts: Not supported (use 2D charts)

## Related Skills

- **word**: Generate Word documents from similar data
- **pdf**: Convert presentations to PDF format
- **excel-data-analyzer**: Generate data for charts
