# Word Document Generator Skill

Professional Word document generation with python-docx library.

## Overview

This skill provides comprehensive capabilities for generating .docx documents with precise formatting control, including:

- **Rich Text Formatting**: Headings, paragraphs, lists with full font control
- **Tables**: Professional table creation with styling
- **Images**: Image insertion with size and caption control
- **Page Layout**: Headers, footers, margins, page breaks
- **Templates**: Predefined templates for common business documents

## Installation

Install required dependencies:

```bash
pip install python-docx pillow
```

## Quick Start

### Basic Document Creation

```python
import sys
sys.path.append('./.claude/skills/office/word/scripts')
from word_generator import create_document

result = create_document(
    title="项目报告",
    content=[
        {"type": "heading", "level": 1, "text": "项目概述"},
        {"type": "paragraph", "text": "这是项目的基本介绍..."},
        {"type": "bullet_list", "items": ["完成功能A", "完成功能B"]}
    ],
    output_path="output/reports/项目报告.docx"
)

if result["success"]:
    print(f"文档已生成: {result['file_path']}")
```

### Using Document Builder

```python
from word_generator import WordDocumentBuilder

builder = WordDocumentBuilder()
builder.add_title("我的文档")
builder.add_heading("第一章", level=1)
builder.add_paragraph("内容文本...")
builder.add_table(
    headers=["列1", "列2", "列3"],
    rows=[["A1", "B1", "C1"], ["A2", "B2", "C2"]]
)
builder.save("output/my-document.docx")
```

### Using Templates

```python
from word_generator import create_from_template

result = create_from_template(
    template_type="report",
    data={
        "title": "月度经营报告",
        "summary": "本月业绩良好...",
        "sections": [
            {
                "title": "销售数据",
                "table": {
                    "headers": ["门店", "销售额", "增长率"],
                    "rows": [["A店", "100万", "+20%"]]
                }
            }
        ]
    },
    output_path="output/reports/monthly-report.docx"
)
```

## Available Templates

| Template | Use Case |
|----------|----------|
| `report` | Business reports, analysis reports |
| `proposal` | Project proposals, planning documents |
| `contract` | Contracts and agreements |
| `meeting-minutes` | Meeting records and action items |
| `manual` | User manuals and guides |
| `letter` | Business letters |

## Content Element Types

### Headings
```python
{"type": "heading", "level": 1, "text": "Chapter Title"}
```

### Paragraphs
```python
{
    "type": "paragraph",
    "text": "Content text...",
    "bold": True,
    "font_size": 12,
    "color": "FF0000"
}
```

### Lists
```python
{"type": "bullet_list", "items": ["Item 1", "Item 2", "Item 3"]}
{"type": "numbered_list", "items": ["Step 1", "Step 2", "Step 3"]}
```

### Tables
```python
{
    "type": "table",
    "headers": ["Column 1", "Column 2"],
    "rows": [["A1", "B1"], ["A2", "B2"]]
}
```

### Images
```python
{
    "type": "image",
    "path": "charts/graph.png",
    "width": 6,
    "caption": "Figure 1: Sales Trend"
}
```

### Page Breaks
```python
{"type": "page_break"}
```

## Advanced Features

### Custom Styling
```python
builder.add_paragraph(
    "Important text",
    font_name="Arial",
    font_size=14,
    bold=True,
    color="FF0000",
    align="center"
)
```

### Page Setup
```python
builder.set_page_margins(top=2.5, bottom=2.5, left=3, right=2)
builder.add_header("公司机密文件")
builder.add_footer("第 {page} 页")
```

### Table Styling
```python
builder.add_table(
    headers=["Name", "Value"],
    rows=[["Item", "100"]],
    style="Light Grid Accent 1"
)
```

## Output Structure

Documents are organized by type:

```
output/
├── reports/          # Business reports
├── proposals/        # Project proposals
├── contracts/        # Contracts
├── meetings/         # Meeting minutes
├── manuals/          # User manuals
└── letters/          # Business letters
```

## Error Handling

All functions return a result dictionary:

```python
result = create_document(...)

if result["success"]:
    print(f"Success: {result['file_path']}")
    print(f"Size: {result['size_bytes']} bytes")
else:
    print(f"Error: {result['error']}")
```

## Examples

See `examples/` directory for complete examples:

- `example_report.py` - Business report generation
- `example_proposal.py` - Project proposal creation
- `example_meeting.py` - Meeting minutes
- `example_contract.py` - Contract generation
- `example_manual.py` - User manual creation

## API Reference

### `WordDocumentBuilder`

Main class for building documents with fluent API.

**Methods:**
- `add_title(text, align="left")` - Add document title
- `add_heading(text, level=1, align="left")` - Add heading
- `add_paragraph(text, **kwargs)` - Add paragraph with formatting
- `add_bullet_list(items, style="List Bullet")` - Add bullet list
- `add_numbered_list(items, style="List Number")` - Add numbered list
- `add_table(headers, rows, style="Light Grid Accent 1")` - Add table
- `add_image(path, width_inches=None, height_inches=None, caption=None)` - Add image
- `add_page_break()` - Add page break
- `set_page_margins(top, bottom, left, right)` - Set margins
- `add_header(text)` - Add header
- `add_footer(text)` - Add footer
- `save(output_path)` - Save document

### `create_document(title, content, output_path, author=None, template_path=None)`

Create document from structured content.

**Args:**
- `title` (str): Document title
- `content` (List[Dict]): List of content elements
- `output_path` (str): Output file path
- `author` (str, optional): Document author
- `template_path` (str, optional): Template file path

**Returns:** Result dictionary with success status and file path

### `create_from_template(template_type, data, output_path)`

Create document from predefined template.

**Args:**
- `template_type` (str): Template type (report, proposal, etc.)
- `data` (Dict): Template data
- `output_path` (str): Output file path

**Returns:** Result dictionary with success status and file path

### `quick_create(title, sections, output_path)`

Quick document creation with simple section tuples.

**Args:**
- `title` (str): Document title
- `sections` (List[tuple]): List of (heading, content) tuples
- `output_path` (str): Output file path

**Returns:** Result dictionary with success status and file path

## Best Practices

1. **Use templates** for standardized documents
2. **Validate content** before generation
3. **Manage styles** consistently throughout the document
4. **Handle images** properly - ensure they exist and have correct dimensions
5. **Test output** in Word before distributing

## Limitations

- Maximum document size: ~100MB (Word limitation)
- Complex formulas not supported (use tables instead)
- Limited support for interactive elements (forms, macros)
- Generated files are Office 2007+ compatible (.docx format)

## License

© 2025 ZTL数智化作战中心. All rights reserved.

## Version History

- **1.0.0** (2025-10-21): Initial release
  - Core document generation
  - 6 predefined templates
  - Rich formatting support
  - Image and table support
