"""
Markdown to PDF Conversion Engine

Convert Markdown to PDF using Pandoc.
Best for technical documentation and academic papers.

Author: ZTL数智化作战中心
Version: 1.0.0
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_pandoc_installed() -> bool:
    """Check if Pandoc is installed."""
    try:
        result = subprocess.run(
            ['pandoc', '--version'],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def create_pdf_from_markdown(
    markdown_content: str,
    output_path: str,
    toc: bool = False,
    number_sections: bool = False,
    highlight_style: str = "pygments",
    template: Optional[str] = None
) -> Dict[str, Any]:
    """
    Convert Markdown to PDF using Pandoc.

    Args:
        markdown_content: Markdown content string
        output_path: Output PDF file path
        toc: Generate table of contents
        number_sections: Number sections automatically
        highlight_style: Code highlighting style (pygments, tango, etc.)
        template: Optional LaTeX template file

    Returns:
        Result dictionary with success status and file info
    """
    try:
        # Check Pandoc installation
        if not check_pandoc_installed():
            return {
                "success": False,
                "error": "Pandoc not installed",
                "install_instructions": {
                    "macOS": "brew install pandoc",
                    "Linux": "sudo apt-get install pandoc",
                    "Windows": "choco install pandoc"
                }
            }

        # Ensure output directory exists
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Write markdown to temp file
        temp_md = output_file.parent / f"temp_{output_file.stem}.md"
        with open(temp_md, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        # Build Pandoc command
        cmd = [
            'pandoc',
            str(temp_md),
            '-o', str(output_file),
            '--pdf-engine=xelatex',  # Better Unicode support
            f'--highlight-style={highlight_style}'
        ]

        if toc:
            cmd.append('--toc')

        if number_sections:
            cmd.append('--number-sections')

        if template and Path(template).exists():
            cmd.extend(['--template', template])

        # Execute Pandoc
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        # Clean up temp file
        temp_md.unlink()

        if result.returncode != 0:
            raise Exception(f"Pandoc error: {result.stderr}")

        logger.info(f"Markdown→PDF generated: {output_path}")
        return {
            "success": True,
            "file_path": str(output_file.absolute()),
            "size_bytes": output_file.stat().st_size,
            "method": "Markdown→PDF (Pandoc)",
            "toc": toc,
            "numbered": number_sections
        }

    except Exception as e:
        logger.error(f"Failed to convert Markdown to PDF: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def create_pdf_from_markdown_file(
    markdown_file: str,
    output_path: str,
    toc: bool = False,
    number_sections: bool = False,
    highlight_style: str = "pygments"
) -> Dict[str, Any]:
    """
    Convert Markdown file to PDF.

    Args:
        markdown_file: Path to Markdown file
        output_path: Output PDF file path
        toc: Generate table of contents
        number_sections: Number sections automatically
        highlight_style: Code highlighting style

    Returns:
        Result dictionary with success status and file info
    """
    try:
        if not Path(markdown_file).exists():
            raise FileNotFoundError(f"Markdown file not found: {markdown_file}")

        # Read Markdown content
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # Use main function
        return create_pdf_from_markdown(
            markdown_content=markdown_content,
            output_path=output_path,
            toc=toc,
            number_sections=number_sections,
            highlight_style=highlight_style
        )

    except Exception as e:
        logger.error(f"Failed to convert Markdown file to PDF: {e}")
        return {
            "success": False,
            "error": str(e)
        }
