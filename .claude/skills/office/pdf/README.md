# PDF Document Generator Skill

Professional PDF generation with 3 powerful methods.

## Overview

This skill provides comprehensive PDF generation capabilities using 3 different approaches:

1. **Direct Generation (ReportLab)** ⭐ Recommended
   - Precise layout control
   - Complex data reports
   - Certificates and forms

2. **HTML to PDF (WeasyPrint)**
   - Web-style documents
   - CSS styling control
   - Marketing materials

3. **Markdown to PDF (Pandoc)**
   - Technical documentation
   - Academic papers
   - Simple and clean

## Installation

### Method 1: ReportLab (Recommended)
```bash
pip install reportlab pillow
```

### Method 2: WeasyPrint
```bash
pip install weasyprint
```

### Method 3: Pandoc
```bash
# macOS
brew install pandoc

# Linux
sudo apt-get install pandoc

# Windows
choco install pandoc

# Python wrapper
pip install pypandoc
```

## Quick Start

### Direct PDF Generation (ReportLab)

```python
import sys
sys.path.append('./.claude/skills/office/pdf/scripts')
from pdf_generator import create_pdf_direct

content = [
    {"type": "heading", "text": "Q3销售报告", "level": 1},
    {"type": "paragraph", "text": "本季度销售额达到450万元"},
    {"type": "table",
     "headers": ["门店", "销售额", "增长率"],
     "data": [["A店", "150万", "+25%"], ["B店", "120万", "+20%"]]}
]

result = create_pdf_direct(
    title="销售报告",
    content=content,
    output_path="output/行政组/销售报告/sales-report.pdf"
)
```

### HTML to PDF

```python
from pdf_generator import create_pdf_from_html

html = """
<html>
<head>
    <style>
        body { font-family: 'SimHei'; }
        h1 { color: #333; text-align: center; }
    </style>
</head>
<body>
    <h1>销售报告</h1>
    <p>内容...</p>
</body>
</html>
"""

result = create_pdf_from_html(
    html_content=html,
    output_path="output/report.pdf"
)
```

### Markdown to PDF

```python
from pdf_generator import create_pdf_from_markdown

markdown = """
# Technical Documentation

## Overview

This is a sample technical document.

### Features

- Feature 1
- Feature 2
- Feature 3
"""

result = create_pdf_from_markdown(
    markdown_content=markdown,
    output_path="output/docs.pdf",
    toc=True
)
```

## Method Comparison

| Method | Complexity | Flexibility | Best For |
|--------|------------|-------------|----------|
| ReportLab | Medium | High | Reports, Forms, Certificates |
| HTML | Low | Medium | Marketing, Web-style docs |
| Markdown | Low | Low | Technical docs, Papers |

## Key Features

### ReportLab Features
- ✅ Precise layout control
- ✅ Complex table rendering
- ✅ Chinese font support
- ✅ Image insertion
- ✅ Page headers/footers
- ✅ Custom page sizes

### HTML→PDF Features
- ✅ CSS styling
- ✅ Web fonts
- ✅ Responsive layouts
- ✅ SVG graphics
- ✅ Print media queries

### Markdown→PDF Features
- ✅ Simple syntax
- ✅ Auto table of contents
- ✅ Code highlighting
- ✅ Math formulas (LaTeX)
- ✅ Citations support

## Examples

See `examples/` directory for complete examples:

- `example_direct.py` - Business report with ReportLab
- `example_html.py` - Marketing brochure with HTML
- `example_markdown.py` - Technical documentation

## Use Cases

### Business Reports (ReportLab)
```python
from pdf_generator import quick_report

result = quick_report(
    title="Monthly Report",
    sections=[
        ("Sales Overview", "Sales reached $450k..."),
        ("Cost Analysis", "Costs were controlled at...")
    ],
    output_path="output/monthly-report.pdf"
)
```

### Certificates (ReportLab)
```python
from pdf_generator import quick_certificate

result = quick_certificate(
    recipient_name="张三",
    award_title="荣获2025年度优秀员工称号",
    date="2025-10-21",
    output_path="output/certificate.pdf"
)
```

### Web Page to PDF (HTML)
```python
from pdf_generator import create_pdf_from_url

result = create_pdf_from_url(
    url="https://example.com/report",
    output_path="output/webpage.pdf"
)
```

## API Reference

### `create_pdf_direct(title, content, output_path, **kwargs)`

Create PDF from structured content using ReportLab.

**Args:**
- `title` (str): Document title
- `content` (List[Dict]): List of content elements
- `output_path` (str): Output file path
- `page_size` (str): Page size (A4, LETTER)
- `orientation` (str): Page orientation (portrait, landscape)
- `author` (str): Document author

**Content Elements:**
- `{"type": "heading", "text": "...", "level": 1}`
- `{"type": "paragraph", "text": "..."}`
- `{"type": "bullet_list", "items": [...]}`
- `{"type": "numbered_list", "items": [...]}`
- `{"type": "table", "headers": [...], "data": [[...]]}`
- `{"type": "image", "path": "...", "width": 400}`
- `{"type": "page_break"}`

### `PDFBuilder()`

Advanced PDF builder with fluent API.

**Methods:**
- `add_title(text, align="center")`
- `add_heading(text, level=1, align="left")`
- `add_paragraph(text, align="left", font_size=12)`
- `add_bullet_list(items)`
- `add_numbered_list(items)`
- `add_table(headers, data, col_widths=None)`
- `add_image(path, width=None, height=None)`
- `add_page_break()`
- `save(output_path)`

### `create_pdf_from_html(html_content, output_path, **kwargs)`

Convert HTML to PDF using WeasyPrint.

**Args:**
- `html_content` (str): HTML content string
- `output_path` (str): Output file path
- `css_file` (str): Optional external CSS file
- `base_url` (str): Base URL for relative paths

### `create_pdf_from_markdown(markdown_content, output_path, **kwargs)`

Convert Markdown to PDF using Pandoc.

**Args:**
- `markdown_content` (str): Markdown content string
- `output_path` (str): Output file path
- `toc` (bool): Generate table of contents
- `number_sections` (bool): Number sections
- `highlight_style` (str): Code highlighting style

## Utilities

### Check Available Methods

```python
from pdf_generator import check_dependencies

status = check_dependencies()
print(status)
# {
#     "available_methods": {
#         "reportlab": True,
#         "weasyprint": False,
#         "pandoc": True
#     },
#     "recommended": "reportlab"
# }
```

### Auto-detect Method

```python
from pdf_generator import create_pdf_auto

# Auto-detect from content type
result = create_pdf_auto(
    content=[...],  # List → Direct
    output_path="output.pdf"
)

result = create_pdf_auto(
    content="<html>...</html>",  # HTML string → HTML
    output_path="output.pdf"
)

result = create_pdf_auto(
    content="# Markdown",  # Markdown string → Markdown
    output_path="output.pdf"
)
```

## Output Structure

```
output/
└── 行政组/
    ├── 经营分析/           # 经营分析报告
    ├── 财务报表/           # 财务报表、费用报销
    ├── 人事文档/           # 人事管理文档
    ├── 会议纪要/           # 会议记录
    ├── 合同文档/           # 合同、协议
    ├── 营销宣传/           # 营销材料
    ├── 技术文档/           # API文档、技术手册
    ├── 证书奖状/           # 证书、荣誉
    └── [自定义项目名]/     # 其他项目
```

> **说明**: 所有PDF输出统一到 `output/行政组/[项目名]/` 目录。详见 [OUTPUT_PATH_CONFIG.md](OUTPUT_PATH_CONFIG.md)

## Best Practices

1. **Choose the Right Method**
   - Complex layouts → ReportLab
   - Web-style → HTML
   - Simple text → Markdown

2. **Font Management**
   - Always specify Chinese fonts
   - Test before production
   - Embed fonts for portability

3. **Image Optimization**
   - Compress images first
   - Use correct formats
   - Specify dimensions

4. **Performance**
   - Generate async for batches
   - Cache when possible
   - Use compression

5. **Testing**
   - Test in multiple PDF readers
   - Verify print output
   - Check file sizes

## Troubleshooting

### ReportLab: Chinese text not showing
```python
# Ensure Chinese fonts are registered
from reportlab_engine import ChineseFontManager
ChineseFontManager.register_fonts()
```

### WeasyPrint: CSS not applied
```python
# Use external CSS file
create_pdf_from_html(
    html_content=html,
    css_file="styles.css",
    output_path="output.pdf"
)
```

### Pandoc: Command not found
```bash
# Install Pandoc
brew install pandoc  # macOS
```

## Dependencies Summary

| Method | Required | Optional |
|--------|----------|----------|
| ReportLab | `reportlab` | `pillow` |
| HTML | `weasyprint` | - |
| Markdown | `pandoc` (CLI) | `pypandoc` |

## Related Skills

- `word-generator` - Generate Word documents
- `excel-data-analyzer` - Create Excel reports
- `chart-generator` - Generate charts for PDFs

## License

© 2025 ZTL数智化作战中心. All rights reserved.

## Version History

- **1.0.0** (2025-10-21): Initial release
  - 3 generation methods
  - Chinese font support
  - Complete API
