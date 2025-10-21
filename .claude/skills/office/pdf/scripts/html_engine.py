"""
HTML to PDF Conversion Engine

Convert HTML/CSS to PDF using WeasyPrint.
Best for web-style documents and marketing materials.

Author: ZTL数智化作战中心
Version: 1.0.0
"""

from pathlib import Path
from typing import Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_pdf_from_html(
    html_content: str,
    output_path: str,
    css_file: Optional[str] = None,
    base_url: Optional[str] = None
) -> Dict[str, Any]:
    """
    Convert HTML to PDF using WeasyPrint.

    Args:
        html_content: HTML content string
        output_path: Output PDF file path
        css_file: Optional external CSS file path
        base_url: Base URL for resolving relative paths

    Returns:
        Result dictionary with success status and file info
    """
    try:
        from weasyprint import HTML, CSS

        # Ensure output directory exists
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Prepare CSS
        stylesheets = []
        if css_file and Path(css_file).exists():
            stylesheets.append(CSS(filename=css_file))

        # Create HTML object
        html_obj = HTML(string=html_content, base_url=base_url)

        # Generate PDF
        html_obj.write_pdf(
            str(output_file),
            stylesheets=stylesheets
        )

        logger.info(f"HTML→PDF generated: {output_path}")
        return {
            "success": True,
            "file_path": str(output_file.absolute()),
            "size_bytes": output_file.stat().st_size,
            "method": "HTML→PDF (WeasyPrint)"
        }

    except ImportError:
        error_msg = "WeasyPrint not installed. Install with: pip install weasyprint"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "install_command": "pip install weasyprint"
        }

    except Exception as e:
        logger.error(f"Failed to convert HTML to PDF: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def create_pdf_from_html_file(
    html_file: str,
    output_path: str,
    css_file: Optional[str] = None
) -> Dict[str, Any]:
    """
    Convert HTML file to PDF.

    Args:
        html_file: Path to HTML file
        output_path: Output PDF file path
        css_file: Optional external CSS file path

    Returns:
        Result dictionary with success status and file info
    """
    try:
        from weasyprint import HTML, CSS

        if not Path(html_file).exists():
            raise FileNotFoundError(f"HTML file not found: {html_file}")

        # Read HTML content
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Get base URL from file path
        base_url = Path(html_file).parent.as_uri()

        # Use main function
        return create_pdf_from_html(
            html_content=html_content,
            output_path=output_path,
            css_file=css_file,
            base_url=base_url
        )

    except Exception as e:
        logger.error(f"Failed to convert HTML file to PDF: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def create_pdf_from_url(
    url: str,
    output_path: str
) -> Dict[str, Any]:
    """
    Convert web page to PDF.

    Args:
        url: Web page URL
        output_path: Output PDF file path

    Returns:
        Result dictionary with success status and file info
    """
    try:
        from weasyprint import HTML

        # Ensure output directory exists
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Fetch and convert
        html_obj = HTML(url=url)
        html_obj.write_pdf(str(output_file))

        logger.info(f"Web page→PDF generated: {output_path}")
        return {
            "success": True,
            "file_path": str(output_file.absolute()),
            "size_bytes": output_file.stat().st_size,
            "method": "URL→PDF (WeasyPrint)",
            "source_url": url
        }

    except ImportError:
        error_msg = "WeasyPrint not installed. Install with: pip install weasyprint"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "install_command": "pip install weasyprint"
        }

    except Exception as e:
        logger.error(f"Failed to convert URL to PDF: {e}")
        return {
            "success": False,
            "error": str(e)
        }
