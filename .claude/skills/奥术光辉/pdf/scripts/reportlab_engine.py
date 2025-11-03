"""
ReportLab PDF Direct Generation Engine

Professional PDF generation with precise layout control using ReportLab.
Recommended for business reports, certificates, invoices, and forms.

Author: ZTL数智化作战中心
Version: 1.0.0
"""

from reportlab.lib.pagesizes import A4, LETTER, landscape
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image as RLImage, KeepTogether
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChineseFontManager:
    """Manage Chinese fonts for PDF generation."""

    _fonts_registered = False

    @classmethod
    def register_fonts(cls):
        """Register Chinese fonts."""
        if cls._fonts_registered:
            return

        try:
            # Try to register common Chinese fonts
            # macOS: /System/Library/Fonts/
            # Windows: C:/Windows/Fonts/
            # Linux: /usr/share/fonts/

            fonts_to_try = [
                ("SimHei", "/System/Library/Fonts/STHeiti Light.ttc", "Heiti SC"),
                ("SimSun", "/System/Library/Fonts/Songti.ttc", "Songti SC"),
                ("KaiTi", "/System/Library/Fonts/Kaiti.ttc", "Kaiti SC"),
            ]

            for font_name, mac_path, _ in fonts_to_try:
                try:
                    if Path(mac_path).exists():
                        pdfmetrics.registerFont(TTFont(font_name, mac_path))
                        logger.info(f"Registered font: {font_name}")
                except Exception as e:
                    logger.warning(f"Failed to register {font_name}: {e}")

            cls._fonts_registered = True

        except Exception as e:
            logger.error(f"Font registration error: {e}")

    @classmethod
    def get_chinese_font(cls) -> str:
        """Get available Chinese font name."""
        cls.register_fonts()
        # Return first available font
        for font in ["SimHei", "SimSun", "KaiTi"]:
            try:
                pdfmetrics.getFont(font)
                return font
            except:
                continue
        return "Helvetica"  # Fallback


class PDFBuilder:
    """
    Advanced PDF builder with precise layout control.

    Example:
        >>> builder = PDFBuilder()
        >>> builder.add_title("My PDF")
        >>> builder.add_paragraph("Content here...")
        >>> builder.add_table(headers=[...], data=[...])
        >>> builder.save("output.pdf")
    """

    def __init__(
        self,
        page_size: str = "A4",
        orientation: str = "portrait"
    ):
        """
        Initialize PDF builder.

        Args:
            page_size: Page size (A4, LETTER, etc.)
            orientation: Page orientation (portrait, landscape)
        """
        # Register Chinese fonts
        ChineseFontManager.register_fonts()

        # Set page size
        if page_size == "A4":
            self.page_size = A4
        elif page_size == "LETTER":
            self.page_size = LETTER
        else:
            self.page_size = A4

        if orientation == "landscape":
            self.page_size = landscape(self.page_size)

        self.width, self.height = self.page_size

        # Story (content elements)
        self.story = []

        # Styles
        self.styles = getSampleStyleSheet()
        self._setup_chinese_styles()

        # Metadata
        self.title = ""
        self.author = ""

        logger.info(f"PDF Builder initialized: {page_size} {orientation}")

    def _setup_chinese_styles(self):
        """Setup Chinese font styles."""
        chinese_font = ChineseFontManager.get_chinese_font()

        # Title style
        self.styles.add(ParagraphStyle(
            name='ChineseTitle',
            parent=self.styles['Title'],
            fontName=chinese_font,
            fontSize=24,
            leading=30,
            alignment=TA_CENTER
        ))

        # Heading1 style
        self.styles.add(ParagraphStyle(
            name='ChineseHeading1',
            parent=self.styles['Heading1'],
            fontName=chinese_font,
            fontSize=18,
            leading=22,
            spaceAfter=12
        ))

        # Heading2 style
        self.styles.add(ParagraphStyle(
            name='ChineseHeading2',
            parent=self.styles['Heading2'],
            fontName=chinese_font,
            fontSize=14,
            leading=18,
            spaceAfter=10
        ))

        # Body style
        self.styles.add(ParagraphStyle(
            name='ChineseBody',
            parent=self.styles['BodyText'],
            fontName=chinese_font,
            fontSize=12,
            leading=16,
            spaceAfter=8
        ))

    def add_title(self, text: str, align: str = "center") -> "PDFBuilder":
        """Add document title."""
        alignment = {
            "left": TA_LEFT,
            "center": TA_CENTER,
            "right": TA_RIGHT
        }.get(align, TA_CENTER)

        style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['ChineseTitle'],
            alignment=alignment
        )

        self.story.append(Paragraph(text, style))
        self.story.append(Spacer(1, 0.3 * inch))
        self.title = text
        logger.info(f"Added title: {text}")
        return self

    def add_heading(
        self,
        text: str,
        level: int = 1,
        align: str = "left"
    ) -> "PDFBuilder":
        """Add heading."""
        if level == 1:
            style_name = 'ChineseHeading1'
        elif level == 2:
            style_name = 'ChineseHeading2'
        else:
            style_name = 'ChineseBody'

        alignment = {
            "left": TA_LEFT,
            "center": TA_CENTER,
            "right": TA_RIGHT
        }.get(align, TA_LEFT)

        style = ParagraphStyle(
            f'CustomHeading{level}',
            parent=self.styles[style_name],
            alignment=alignment
        )

        self.story.append(Paragraph(text, style))
        logger.info(f"Added heading (level {level}): {text}")
        return self

    def add_paragraph(
        self,
        text: str,
        align: str = "left",
        font_size: int = 12
    ) -> "PDFBuilder":
        """Add paragraph."""
        alignment = {
            "left": TA_LEFT,
            "center": TA_CENTER,
            "right": TA_RIGHT,
            "justify": TA_JUSTIFY
        }.get(align, TA_LEFT)

        style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['ChineseBody'],
            alignment=alignment,
            fontSize=font_size,
            leading=font_size * 1.3
        )

        self.story.append(Paragraph(text, style))
        logger.info(f"Added paragraph: {text[:50]}...")
        return self

    def add_bullet_list(self, items: List[str]) -> "PDFBuilder":
        """Add bullet list."""
        for item in items:
            bullet = "•"
            text = f"{bullet} {item}"
            style = self.styles['ChineseBody']
            self.story.append(Paragraph(text, style))

        self.story.append(Spacer(1, 0.1 * inch))
        logger.info(f"Added bullet list with {len(items)} items")
        return self

    def add_numbered_list(self, items: List[str]) -> "PDFBuilder":
        """Add numbered list."""
        for i, item in enumerate(items, 1):
            text = f"{i}. {item}"
            style = self.styles['ChineseBody']
            self.story.append(Paragraph(text, style))

        self.story.append(Spacer(1, 0.1 * inch))
        logger.info(f"Added numbered list with {len(items)} items")
        return self

    def add_table(
        self,
        headers: List[str],
        data: List[List[str]],
        col_widths: Optional[List[float]] = None
    ) -> "PDFBuilder":
        """Add table."""
        # Prepare table data
        table_data = [headers] + data

        # Create table
        if col_widths:
            widths = [w * inch for w in col_widths]
            table = Table(table_data, colWidths=widths)
        else:
            table = Table(table_data)

        # Style table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), ChineseFontManager.get_chinese_font()),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTNAME', (0, 1), (-1, -1), ChineseFontManager.get_chinese_font()),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        table.setStyle(style)

        self.story.append(table)
        self.story.append(Spacer(1, 0.2 * inch))
        logger.info(f"Added table: {len(headers)} columns × {len(data)} rows")
        return self

    def add_image(
        self,
        image_path: str,
        width: Optional[float] = None,
        height: Optional[float] = None,
        align: str = "center"
    ) -> "PDFBuilder":
        """Add image."""
        if not Path(image_path).exists():
            logger.error(f"Image not found: {image_path}")
            raise FileNotFoundError(f"Image not found: {image_path}")

        # Create image
        if width and height:
            img = RLImage(image_path, width=width, height=height)
        elif width:
            img = RLImage(image_path, width=width, height=width)
        else:
            img = RLImage(image_path, width=4*inch, height=3*inch)

        # Alignment
        if align == "center":
            img.hAlign = 'CENTER'
        elif align == "right":
            img.hAlign = 'RIGHT'
        else:
            img.hAlign = 'LEFT'

        self.story.append(img)
        self.story.append(Spacer(1, 0.2 * inch))
        logger.info(f"Added image: {image_path}")
        return self

    def add_page_break(self) -> "PDFBuilder":
        """Add page break."""
        self.story.append(PageBreak())
        logger.info("Added page break")
        return self

    def add_spacer(self, height: float = 0.2) -> "PDFBuilder":
        """Add vertical spacer."""
        self.story.append(Spacer(1, height * inch))
        return self

    def save(self, output_path: str) -> Dict[str, Any]:
        """
        Save PDF to file.

        Args:
            output_path: Output file path

        Returns:
            Result dictionary with success status and file info
        """
        try:
            # Ensure output directory exists
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)

            # Build PDF
            doc = SimpleDocTemplate(
                str(output_file),
                pagesize=self.page_size,
                title=self.title,
                author=self.author
            )

            # Build story
            doc.build(self.story)

            logger.info(f"PDF saved: {output_path}")
            return {
                "success": True,
                "file_path": str(output_file.absolute()),
                "size_bytes": output_file.stat().st_size,
                "page_count": len([e for e in self.story if isinstance(e, PageBreak)]) + 1
            }

        except Exception as e:
            logger.error(f"Failed to save PDF: {e}")
            return {
                "success": False,
                "error": str(e)
            }


def create_pdf_direct(
    title: str,
    content: List[Dict[str, Any]],
    output_path: str,
    page_size: str = "A4",
    orientation: str = "portrait",
    author: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create PDF from structured content using ReportLab.

    Args:
        title: Document title
        content: List of content elements
        output_path: Output file path
        page_size: Page size (A4, LETTER)
        orientation: Page orientation (portrait, landscape)
        author: Document author

    Content elements:
        {"type": "heading", "text": "Title", "level": 1}
        {"type": "paragraph", "text": "Content...", "align": "left"}
        {"type": "bullet_list", "items": ["Item 1", "Item 2"]}
        {"type": "numbered_list", "items": ["Step 1", "Step 2"]}
        {"type": "table", "headers": [...], "data": [[...]]}
        {"type": "image", "path": "image.png", "width": 400}
        {"type": "page_break"}

    Returns:
        Result dictionary with success status and file info
    """
    try:
        builder = PDFBuilder(page_size=page_size, orientation=orientation)

        # Set author
        if author:
            builder.author = author

        # Add title
        builder.add_title(title)

        # Process content elements
        for element in content:
            element_type = element.get("type")

            if element_type == "heading":
                builder.add_heading(
                    element["text"],
                    level=element.get("level", 1),
                    align=element.get("align", "left")
                )

            elif element_type == "paragraph":
                builder.add_paragraph(
                    element["text"],
                    align=element.get("align", "left"),
                    font_size=element.get("font_size", 12)
                )

            elif element_type == "bullet_list":
                builder.add_bullet_list(element["items"])

            elif element_type == "numbered_list":
                builder.add_numbered_list(element["items"])

            elif element_type == "table":
                builder.add_table(
                    headers=element["headers"],
                    data=element["data"],
                    col_widths=element.get("col_widths")
                )

            elif element_type == "image":
                builder.add_image(
                    image_path=element["path"],
                    width=element.get("width"),
                    height=element.get("height"),
                    align=element.get("align", "center")
                )

            elif element_type == "page_break":
                builder.add_page_break()

            elif element_type == "spacer":
                builder.add_spacer(element.get("height", 0.2))

        # Save PDF
        return builder.save(output_path)

    except Exception as e:
        logger.error(f"Failed to create PDF: {e}")
        return {
            "success": False,
            "error": str(e)
        }
