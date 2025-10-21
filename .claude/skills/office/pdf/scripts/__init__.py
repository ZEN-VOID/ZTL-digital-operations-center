"""
PDF Document Generator Skill

A comprehensive PDF generation skill supporting 3 methods:
1. Direct generation with ReportLab (recommended)
2. HTML to PDF with WeasyPrint
3. Markdown to PDF with Pandoc

Author: ZTL数智化作战中心
Version: 1.0.0
"""

from .pdf_generator import (
    # Method 1: Direct (ReportLab)
    create_pdf_direct,
    PDFBuilder,

    # Method 2: HTML→PDF
    create_pdf_from_html,
    create_pdf_from_html_file,
    create_pdf_from_url,

    # Method 3: Markdown→PDF
    create_pdf_from_markdown,
    create_pdf_from_markdown_file,

    # Auto-detect
    create_pdf_auto,

    # Utilities
    quick_report,
    quick_certificate,
    check_dependencies
)

__version__ = "1.0.0"
__all__ = [
    "create_pdf_direct",
    "PDFBuilder",
    "create_pdf_from_html",
    "create_pdf_from_html_file",
    "create_pdf_from_url",
    "create_pdf_from_markdown",
    "create_pdf_from_markdown_file",
    "create_pdf_auto",
    "quick_report",
    "quick_certificate",
    "check_dependencies"
]
