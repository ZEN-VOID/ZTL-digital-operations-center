"""
PDF Generator - Main Control Module

Unified interface for 3 PDF generation methods:
1. Direct generation with ReportLab (recommended)
2. HTML to PDF with WeasyPrint
3. Markdown to PDF with Pandoc

Author: ZTL数智化作战中心
Version: 1.0.0
"""

from typing import Dict, Any, Optional, List
from pathlib import Path
import logging

# Import engines
from reportlab_engine import create_pdf_direct, PDFBuilder
from html_engine import (
    create_pdf_from_html,
    create_pdf_from_html_file,
    create_pdf_from_url
)
from markdown_engine import (
    create_pdf_from_markdown,
    create_pdf_from_markdown_file
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

__version__ = "1.0.0"

# Re-export main functions
__all__ = [
    # ReportLab (Method 1 - Recommended)
    "create_pdf_direct",
    "PDFBuilder",

    # HTML→PDF (Method 2)
    "create_pdf_from_html",
    "create_pdf_from_html_file",
    "create_pdf_from_url",

    # Markdown→PDF (Method 3)
    "create_pdf_from_markdown",
    "create_pdf_from_markdown_file",

    # Auto-detect
    "create_pdf_auto"
]


def create_pdf_auto(
    content: Any,
    output_path: str,
    method: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Auto-detect content type and generate PDF.

    Args:
        content: Content (can be dict/list for direct, string for HTML/Markdown)
        output_path: Output PDF file path
        method: Force specific method (direct, html, markdown)
        **kwargs: Additional parameters for specific method

    Returns:
        Result dictionary with success status and file info
    """
    try:
        # Force specific method
        if method:
            if method == "direct" or method == "reportlab":
                if not isinstance(content, (list, dict)):
                    raise ValueError("Direct method requires list or dict content")

                # If dict, convert to list
                if isinstance(content, dict):
                    title = content.get("title", "Untitled")
                    elements = content.get("content", [])
                    return create_pdf_direct(
                        title=title,
                        content=elements,
                        output_path=output_path,
                        **kwargs
                    )
                else:
                    # Assume first element is title
                    return create_pdf_direct(
                        title="Document",
                        content=content,
                        output_path=output_path,
                        **kwargs
                    )

            elif method == "html" or method == "weasyprint":
                if not isinstance(content, str):
                    raise ValueError("HTML method requires string content")
                return create_pdf_from_html(
                    html_content=content,
                    output_path=output_path,
                    **kwargs
                )

            elif method == "markdown" or method == "pandoc":
                if not isinstance(content, str):
                    raise ValueError("Markdown method requires string content")
                return create_pdf_from_markdown(
                    markdown_content=content,
                    output_path=output_path,
                    **kwargs
                )

        # Auto-detect based on content type
        if isinstance(content, (list, dict)):
            # Structured content → Direct method
            logger.info("Auto-detected: Direct PDF generation (ReportLab)")
            if isinstance(content, dict):
                title = content.get("title", "Document")
                elements = content.get("content", [])
                return create_pdf_direct(
                    title=title,
                    content=elements,
                    output_path=output_path,
                    **kwargs
                )
            else:
                return create_pdf_direct(
                    title="Document",
                    content=content,
                    output_path=output_path,
                    **kwargs
                )

        elif isinstance(content, str):
            # String content → Detect HTML vs Markdown
            if content.strip().startswith('<'):
                logger.info("Auto-detected: HTML→PDF (WeasyPrint)")
                return create_pdf_from_html(
                    html_content=content,
                    output_path=output_path,
                    **kwargs
                )
            else:
                logger.info("Auto-detected: Markdown→PDF (Pandoc)")
                return create_pdf_from_markdown(
                    markdown_content=content,
                    output_path=output_path,
                    **kwargs
                )

        else:
            raise ValueError(f"Unsupported content type: {type(content)}")

    except Exception as e:
        logger.error(f"Auto PDF generation failed: {e}")
        return {
            "success": False,
            "error": str(e)
        }


# Convenience functions

def quick_report(
    title: str,
    sections: List[tuple],
    output_path: str
) -> Dict[str, Any]:
    """
    Quick report generation from simple sections.

    Args:
        title: Report title
        sections: List of (heading, content) tuples
        output_path: Output file path

    Example:
        >>> quick_report(
        ...     "Q3 Report",
        ...     [
        ...         ("Overview", "Q3 performance was excellent..."),
        ...         ("Sales", "Sales reached $450k...")
        ...     ],
        ...     "output/q3-report.pdf"
        ... )
    """
    content = []
    for heading, text in sections:
        content.append({"type": "heading", "text": heading, "level": 1})
        content.append({"type": "paragraph", "text": text})

    return create_pdf_direct(
        title=title,
        content=content,
        output_path=output_path
    )


def quick_certificate(
    recipient_name: str,
    award_title: str,
    date: str,
    output_path: str,
    seal_image: Optional[str] = None
) -> Dict[str, Any]:
    """
    Quick certificate generation.

    Args:
        recipient_name: Recipient name
        award_title: Award title
        date: Award date
        output_path: Output file path
        seal_image: Optional company seal image

    Returns:
        Result dictionary
    """
    builder = PDFBuilder(page_size="A4", orientation="landscape")

    builder.add_spacer(2)
    builder.add_paragraph("证书", align="center", font_size=36)
    builder.add_spacer(1)
    builder.add_paragraph("兹证明", align="center", font_size=16)
    builder.add_spacer(0.5)
    builder.add_paragraph(recipient_name, align="center", font_size=24)
    builder.add_spacer(0.5)
    builder.add_paragraph(award_title, align="center", font_size=16)
    builder.add_spacer(1)
    builder.add_paragraph(f"颁发日期: {date}", align="center", font_size=12)

    if seal_image and Path(seal_image).exists():
        builder.add_spacer(1)
        builder.add_image(seal_image, width=100, align="center")

    return builder.save(output_path)


def check_dependencies() -> Dict[str, Any]:
    """
    Check which PDF generation methods are available.

    Returns:
        Dictionary of available methods and their status
    """
    status = {
        "reportlab": False,
        "weasyprint": False,
        "pandoc": False
    }

    # Check ReportLab
    try:
        import reportlab
        status["reportlab"] = True
    except ImportError:
        pass

    # Check WeasyPrint
    try:
        import weasyprint
        status["weasyprint"] = True
    except ImportError:
        pass

    # Check Pandoc
    from markdown_engine import check_pandoc_installed
    status["pandoc"] = check_pandoc_installed()

    return {
        "available_methods": status,
        "recommended": "reportlab" if status["reportlab"] else None,
        "install_commands": {
            "reportlab": "pip install reportlab pillow",
            "weasyprint": "pip install weasyprint",
            "pandoc": "brew install pandoc (macOS) / apt-get install pandoc (Linux)"
        }
    }
