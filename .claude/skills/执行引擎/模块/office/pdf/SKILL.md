---
name: PDF Document Generator
description: Generate professional PDF documents using 3 methods - direct generation with ReportLab (recommended for reports/certificates), HTML-to-PDF with WeasyPrint (for web-style documents), and Markdown-to-PDF with Pandoc (for technical docs). Use when creating invoices, reports, certificates, forms, or any formatted PDF documents. Supports Chinese fonts, tables, images, and complex layouts.
---

# PDF Document Generator

## Quick Start

### Method 1: Direct PDF Generation with ReportLab ⭐ Recommended
```python
import sys
sys.path.append('./.claude/skills/office/pdf/scripts')
from pdf_generator import create_pdf_direct

result = create_pdf_direct(
    title="销售报表",
    content=[
        {"type": "heading", "text": "Q3销售数据", "level": 1},
        {"type": "paragraph", "text": "本季度销售额达到450万元"},
        {"type": "table",
         "headers": ["门店", "销售额", "增长率"],
         "data": [["A店", "150万", "+25%"], ["B店", "120万", "+20%"]]},
        {"type": "image", "path": "charts/sales.png", "width": 400}
    ],
    output_path="output/reports/q3-sales.pdf"
)
```

**优势**: 精确控制、复杂排版、适合数据报表/证书/发票

### Method 2: HTML to PDF Conversion
```python
from pdf_generator import create_pdf_from_html

html_content = """
<html>
<head>
    <style>
        body { font-family: 'SimHei'; }
        h1 { color: #333; text-align: center; }
        table { width: 100%; border-collapse: collapse; }
        td, th { border: 1px solid #ddd; padding: 8px; }
    </style>
</head>
<body>
    <h1>销售报表</h1>
    <table>
        <tr><th>门店</th><th>销售额</th></tr>
        <tr><td>A店</td><td>150万</td></tr>
    </table>
</body>
</html>
"""

result = create_pdf_from_html(
    html_content=html_content,
    output_path="output/reports/sales.pdf"
)
```

**优势**: CSS样式控制、网页风格、前端开发者友好

### Method 3: Markdown to PDF
```python
from pdf_generator import create_pdf_from_markdown

markdown_content = """
# 技术文档

## 概述

这是一份技术文档示例。

### 功能特性

- 支持Markdown语法
- 自动生成目录
- 代码高亮

```python
def hello():
    print("Hello, World!")
```

## 表格示例

| 功能 | 状态 |
|------|------|
| 文本 | ✓ |
| 图片 | ✓ |
"""

result = create_pdf_from_markdown(
    markdown_content=markdown_content,
    output_path="output/docs/technical-doc.pdf"
)
```

**优势**: 最简洁、适合技术文档、学术论文

## Generation Methods Comparison

| Method | Tool | Best For | Complexity | Flexibility |
|--------|------|----------|------------|-------------|
| **Direct** | ReportLab | Reports, Certificates, Invoices | Medium | High |
| **HTML** | WeasyPrint | Web-style docs, Marketing | Low | Medium |
| **Markdown** | Pandoc | Technical docs, Papers | Low | Low |

## Use Cases

### Use Case 1: Business Reports (ReportLab)
- Financial reports
- Sales analytics
- Performance dashboards
- Executive summaries

### Use Case 2: Certificates & Forms (ReportLab)
- Training certificates
- Award certificates
- Registration forms
- Invoices and receipts

### Use Case 3: Marketing Materials (HTML→PDF)
- Product brochures
- Event flyers
- Email templates
- Promotional materials

### Use Case 4: Technical Documentation (Markdown→PDF)
- API documentation
- User manuals
- Research papers
- Technical specifications

## Key Features

### ReportLab Features
- **Precise Layout Control**: Position elements at exact coordinates
- **Rich Typography**: Multiple fonts, sizes, colors, styles
- **Tables**: Professional table rendering with styling
- **Graphics**: Shapes, lines, charts integration
- **Images**: PNG, JPEG with size/position control
- **Page Control**: Headers, footers, page numbers, watermarks
- **Chinese Support**: Built-in Chinese font support

### HTML→PDF Features
- **CSS Styling**: Full CSS2.1 + CSS3 selectors support
- **Responsive**: Media queries for print
- **Web Fonts**: Custom font loading
- **Modern HTML**: HTML5 elements support
- **Charts**: SVG and canvas rendering
- **Print-specific**: Page breaks, margins control

### Markdown→PDF Features
- **Simple Syntax**: Write in plain Markdown
- **Auto TOC**: Automatic table of contents
- **Code Highlighting**: Syntax highlighting for code blocks
- **Math Formulas**: LaTeX math support
- **Citations**: Bibliography management
- **Templates**: Custom LaTeX templates

## Documentation

- **[API Reference](reference.md)**: Complete API documentation
- **[ReportLab Guide](reportlab-guide.md)**: Advanced ReportLab techniques
- **[HTML Styling Guide](html-styling.md)**: CSS best practices for PDF
- **[Markdown Reference](markdown-ref.md)**: Markdown syntax and extensions

## Bundled Scripts

- **`scripts/pdf_generator.py`**: Main PDF generation engine (all 3 methods)
- **`scripts/reportlab_engine.py`**: ReportLab direct generation
- **`scripts/html_engine.py`**: HTML to PDF conversion
- **`scripts/markdown_engine.py`**: Markdown to PDF conversion
- **`scripts/templates.py`**: PDF template system
- **`scripts/fonts.py`**: Font management and Chinese support
- **`scripts/utils.py`**: Helper utilities

## Common Tasks

### Create a financial report
```python
from pdf_generator import create_pdf_direct

content = [
    {"type": "heading", "text": "2025年Q3财务报告", "level": 1},
    {"type": "paragraph", "text": "报告期间: 2025年7月1日 - 2025年9月30日"},
    {"type": "heading", "text": "财务概况", "level": 2},
    {"type": "table",
     "headers": ["项目", "金额(万元)", "同比增长"],
     "data": [
         ["营业收入", "450", "+25%"],
         ["营业成本", "315", "+18%"],
         ["净利润", "90", "+35%"]
     ]},
    {"type": "chart", "path": "charts/revenue-trend.png", "caption": "营收趋势"}
]

result = create_pdf_direct(
    title="财务报告",
    content=content,
    output_path="output/finance/q3-report.pdf",
    page_size="A4",
    add_page_numbers=True
)
```

### Generate a certificate
```python
from pdf_generator import PDFBuilder

builder = PDFBuilder(page_size="A4", orientation="landscape")
builder.add_centered_text("优秀员工证书", y=500, font_size=36, bold=True)
builder.add_centered_text("兹证明", y=400, font_size=16)
builder.add_centered_text("张三", y=350, font_size=24, bold=True)
builder.add_centered_text("荣获2025年度优秀员工称号", y=300, font_size=16)
builder.add_centered_text("特发此证", y=200, font_size=14)
builder.add_image("assets/company-seal.png", x=450, y=100, width=100)
builder.save("output/certificates/award-zhang.pdf")
```

### Convert HTML email template to PDF
```python
from pdf_generator import create_pdf_from_html

with open("templates/email-campaign.html", "r") as f:
    html = f.read()

result = create_pdf_from_html(
    html_content=html,
    css_file="templates/email-styles.css",
    output_path="output/marketing/campaign.pdf"
)
```

### Generate technical documentation from Markdown
```python
from pdf_generator import create_pdf_from_markdown

with open("docs/api-reference.md", "r") as f:
    markdown = f.read()

result = create_pdf_from_markdown(
    markdown_content=markdown,
    toc=True,
    number_sections=True,
    highlight_style="monokai",
    output_path="output/docs/api-reference.pdf"
)
```

## Advanced Features

### Custom Page Layouts (ReportLab)
```python
from reportlab_engine import PDFBuilder

builder = PDFBuilder()
builder.set_page_size(width=600, height=800)
builder.set_margins(top=50, bottom=50, left=40, right=40)
builder.add_header("公司机密", align="right")
builder.add_footer("第 {page} 页 共 {total} 页", align="center")
builder.add_watermark("CONFIDENTIAL", opacity=0.1)
```

### Multi-column Layouts (HTML)
```python
html = """
<style>
    .two-column {
        column-count: 2;
        column-gap: 20px;
    }
</style>
<div class="two-column">
    <p>Content in two columns...</p>
</div>
"""
```

### Custom Fonts
```python
from fonts import FontManager

fm = FontManager()
fm.register_font("楷体", "fonts/kaiti.ttf")
fm.set_default_font("楷体")

builder.add_text("使用自定义字体", font="楷体")
```

## Dependencies

### Required
```bash
# For ReportLab method
pip install reportlab pillow

# For HTML→PDF method
pip install weasyprint

# For Markdown→PDF method
pip install pandoc pypandoc
# Also requires: pandoc (install via brew/apt/choco)
```

### Optional
```bash
# For enhanced features
pip install matplotlib  # Chart generation
pip install qrcode      # QR code generation
```

## Output Structure

```
output/
├── reports/          # Business reports
├── certificates/     # Certificates and awards
├── invoices/         # Invoices and receipts
├── marketing/        # Marketing materials
├── docs/             # Technical documentation
└── forms/            # Forms and applications
```

## Error Handling

All generation functions return a result dictionary:

```python
result = create_pdf_direct(...)

if result["success"]:
    print(f"PDF generated: {result['file_path']}")
    print(f"Size: {result['size_bytes']} bytes")
    print(f"Pages: {result['page_count']}")
else:
    print(f"Error: {result['error']}")
    print(f"Details: {result.get('details', 'N/A')}")
```

## Best Practices

1. **Choose the Right Method**:
   - ReportLab: Complex layouts, precise control needed
   - HTML: Web-style documents, CSS familiarity
   - Markdown: Simple text-heavy documents

2. **Font Management**:
   - Always specify Chinese fonts for Chinese content
   - Test fonts before production use
   - Embed fonts for portability

3. **Image Optimization**:
   - Compress images before PDF generation
   - Use appropriate image formats (PNG for graphics, JPEG for photos)
   - Specify image dimensions to avoid distortion

4. **Performance**:
   - Generate PDFs asynchronously for large batches
   - Cache generated PDFs when possible
   - Use compression for file size optimization

5. **Testing**:
   - Test PDFs in multiple PDF readers
   - Verify print output for print-ready PDFs
   - Check file sizes for distribution

## Limitations

- **ReportLab**: Steeper learning curve for complex layouts
- **HTML→PDF**: Some CSS features not supported (flexbox, grid)
- **Markdown→PDF**: Requires Pandoc installation, limited styling control

## Related Skills

- **word-generator**: Generate Word documents (.docx)
- **excel-data-analyzer**: Create Excel spreadsheets
- **image-processor**: Process images for PDF inclusion
- **chart-generator**: Generate charts for reports
