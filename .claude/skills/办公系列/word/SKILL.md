---
name: Word Document Generator
description: Generate professional Word documents (.docx) with precise formatting control. Supports document creation, style management, tables, images, headers/footers, and template-based generation. Use when creating reports, proposals, contracts, or any formatted Word documents. Requires python-docx library.
---

# Word Document Generator

## Quick Start

### Method 1: Simple Document Creation (Recommended)
```python
import sys
sys.path.append('./.claude/skills/office/word/scripts')
from word_generator import create_document

result = create_document(
    title="项目报告",
    content=[
        {"type": "heading", "level": 1, "text": "项目概述"},
        {"type": "paragraph", "text": "这是项目的基本介绍..."},
        {"type": "heading", "level": 2, "text": "主要成果"},
        {"type": "bullet_list", "items": ["完成功能A", "完成功能B", "完成功能C"]}
    ],
    output_path="output/reports/项目报告.docx"
)

if result["success"]:
    print(f"文档已生成: {result['file_path']}")
```

### Method 2: Template-Based Generation
```python
from word_generator import create_from_template

result = create_from_template(
    template_type="report",  # report, proposal, contract, meeting-minutes
    data={
        "title": "月度经营分析报告",
        "author": "数据分析组",
        "date": "2025-10-21",
        "sections": [...]
    },
    output_path="output/reports/monthly-report.docx"
)
```

### Method 3: Advanced Document Builder
```python
from word_generator import WordDocumentBuilder

builder = WordDocumentBuilder()
builder.add_title("产品规划文档")
builder.add_heading("第一章 市场分析", level=1)
builder.add_paragraph("市场调研结果显示...")
builder.add_table(
    headers=["指标", "Q1", "Q2", "Q3", "Q4"],
    rows=[
        ["销售额", "100万", "120万", "150万", "180万"],
        ["增长率", "10%", "20%", "25%", "20%"]
    ]
)
builder.add_image("charts/sales-trend.png", width_inches=6)
builder.save("output/product-plan.docx")
```

## Document Types

This skill supports 6 professional document templates:

| Type | Code | Use Case |
|------|------|----------|
| **Report** | `report` | Business reports, analysis reports, project reports |
| **Proposal** | `proposal` | Project proposals, business proposals, planning documents |
| **Contract** | `contract` | Contracts, agreements, legal documents |
| **Meeting Minutes** | `meeting-minutes` | Meeting records, discussion summaries |
| **Manual** | `manual` | User manuals, operation guides, SOP documents |
| **Letter** | `letter` | Business letters, formal correspondence |

## Key Features

### 1. **Rich Text Formatting**
- Multiple heading levels (H1-H6)
- Paragraph styles (alignment, spacing, indentation)
- Font customization (family, size, color, bold, italic)
- Text highlighting and underline

### 2. **Lists and Tables**
- Bullet lists and numbered lists
- Multi-level nested lists
- Professional table creation
- Table styling (borders, shading, cell merging)

### 3. **Images and Graphics**
- Image insertion with size control
- Image alignment and wrapping
- Caption support
- Chart integration

### 4. **Page Layout**
- Headers and footers
- Page numbers
- Section breaks
- Page orientation (portrait/landscape)
- Margins and page size

### 5. **Document Metadata**
- Title, author, subject
- Keywords and comments
- Creation/modification date
- Custom properties

## Documentation

- **[API Reference](reference.md)**: Complete API documentation and parameter guide
- **[Template Guide](templates.md)**: Document template usage and customization
- **[Style Guide](styles.md)**: Font, paragraph, and table styling reference

## Bundled Scripts

- **`scripts/word_generator.py`**: Main document generation engine
- **`scripts/templates.py`**: Template management and rendering
- **`scripts/styles.py`**: Style definitions and utilities
- **`scripts/utils.py`**: Helper functions and utilities

## Common Tasks

### Create a business report
```python
from word_generator import create_document

content = [
    {"type": "title", "text": "Q3经营分析报告"},
    {"type": "heading", "level": 1, "text": "一、经营概况"},
    {"type": "paragraph", "text": "本季度营业额达到..."},
    {"type": "table", "headers": ["门店", "营业额", "同比增长"],
     "rows": [["A店", "150万", "+25%"], ["B店", "120万", "+15%"]]},
    {"type": "heading", "level": 1, "text": "二、问题分析"},
    {"type": "bullet_list", "items": ["成本上升", "人员流失", "竞争加剧"]}
]

result = create_document(
    title="Q3经营分析报告",
    content=content,
    output_path="output/reports/q3-analysis.docx"
)
```

### Create a meeting minutes document
```python
from word_generator import create_from_template

result = create_from_template(
    template_type="meeting-minutes",
    data={
        "title": "战略规划会议纪要",
        "date": "2025-10-21",
        "attendees": ["张三", "李四", "王五"],
        "topics": [
            {
                "topic": "新品上市计划",
                "discussion": "讨论新品定价策略...",
                "action_items": [
                    {"task": "完成市场调研", "owner": "张三", "deadline": "10-30"}
                ]
            }
        ]
    },
    output_path="output/meetings/strategy-meeting-20251021.docx"
)
```

### Create a styled contract
```python
from word_generator import WordDocumentBuilder

builder = WordDocumentBuilder()
builder.set_page_margins(top=2.5, bottom=2.5, left=3, right=2)
builder.add_title("加盟合作协议", align="center")
builder.add_paragraph("甲方(授权方):__________", style="contract_party")
builder.add_paragraph("乙方(加盟方):__________", style="contract_party")
builder.add_heading("第一条 合作内容", level=1)
builder.add_paragraph("1.1 甲方授予乙方在指定区域内...")
builder.add_page_break()
builder.add_heading("第二条 权利义务", level=1)
builder.add_paragraph("2.1 甲方的权利和义务...")
builder.save("output/contracts/franchise-agreement.docx")
```

### Add images and charts
```python
from word_generator import WordDocumentBuilder

builder = WordDocumentBuilder()
builder.add_heading("数据分析报告", level=1)
builder.add_paragraph("以下是销售趋势分析:")
builder.add_image(
    "charts/sales-trend.png",
    width_inches=6,
    caption="图1: 季度销售趋势"
)
builder.add_paragraph("关键洞察:")
builder.add_bullet_list([
    "Q3销售额同比增长25%",
    "线上渠道占比提升至40%",
    "新品贡献率达到30%"
])
builder.save("output/reports/sales-analysis.docx")
```

## Advanced Features

### Custom Styles
```python
from word_generator import WordDocumentBuilder

builder = WordDocumentBuilder()
builder.add_paragraph(
    "This is important text",
    font_name="Arial",
    font_size=14,
    bold=True,
    color="FF0000",  # Red color
    align="center"
)
```

### Multi-column Layout
```python
builder.set_page_columns(2)  # 2-column layout
builder.add_paragraph("Column content...")
```

### Header and Footer
```python
builder.add_header("公司机密文件 - 仅限内部使用")
builder.add_footer("第 {page} 页 共 {total_pages} 页")
```

## Dependencies

This skill requires:
- **python-docx**: Core Word document library
- **Pillow**: Image processing (optional, for image features)

Install with:
```bash
pip install python-docx pillow
```

## Output Structure

Generated documents are organized by type:
```
output/
├── reports/          # Business reports
├── proposals/        # Project proposals
├── contracts/        # Contracts and agreements
├── meetings/         # Meeting minutes
├── manuals/          # User manuals and guides
└── letters/          # Business letters
```

## Error Handling

The skill provides detailed error messages and validation:
```python
result = create_document(...)

if not result["success"]:
    print(f"Error: {result['error']}")
    print(f"Details: {result.get('details', 'N/A')}")
else:
    print(f"Success: {result['file_path']}")
    print(f"Pages: {result.get('page_count', 'N/A')}")
```

## Best Practices

1. **Use Templates**: For standardized documents, use template-based generation
2. **Validate Content**: Check content structure before generation
3. **Manage Styles**: Define consistent styles for professional appearance
4. **Handle Images**: Ensure images exist and have appropriate dimensions
5. **Test Output**: Verify generated documents in Word before distribution

## Limitations

- Maximum document size: ~100MB (Word limitation)
- Complex formulas: Use tables for calculations, not Word equations
- Interactive elements: Limited support for forms and macros
- Version compatibility: Generated .docx files are Office 2007+ compatible

## Related Skills

- **excel-data-analyzer**: Generate Excel reports with data analysis
- **pdf-converter**: Convert Word documents to PDF format
- **template-manager**: Manage and version control document templates
