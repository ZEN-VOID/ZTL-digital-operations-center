#!/usr/bin/env python3
"""
Canvas Design Execution Engine
==============================

Implements the canvas-design skill's two-phase workflow:
1. Design Philosophy Creation (.md file)
2. Visual Expression (PDF/PNG generation using reportlab/PIL)

Output Path Convention (follows global CLAUDE.md rules):
    output/[项目名]/X4-平面设计师/canvas-design/[design-type]/

Usage:
    from scripts.canvas_designer import CanvasDesigner

    designer = CanvasDesigner(
        project_name="火锅店开业筹备",
        agent_name="X4-平面设计师"
    )

    result = designer.create_design(
        user_prompt="为新开的川味火锅店设计一张开业海报",
        design_type="poster",
        output_format="png"
    )
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Literal, Optional, Dict, Any
from dataclasses import dataclass, asdict

# PDF/PNG generation libraries
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import inch
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("⚠️  reportlab not installed. Run: pip install reportlab")

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️  Pillow not installed. Run: pip install Pillow")


@dataclass
class DesignSpec:
    """Design specification following Layer 2 (Plan/Configuration Layer)"""

    # Identity
    project_name: str
    agent_name: str
    design_type: Literal["poster", "menu-cover", "packaging", "logo", "flyer", "banner"]

    # Philosophy
    movement_name: str  # e.g., "Brutalist Joy", "Chromatic Silence"
    philosophy_content: str  # 4-6 paragraphs

    # Visual Parameters
    canvas_size: tuple[int, int]  # (width, height) in pixels
    output_format: Literal["pdf", "png"]
    color_palette: list[str]  # Hex colors

    # Typography
    primary_font: str  # Font file name from canvas-fonts/
    secondary_font: Optional[str] = None

    # Content
    text_elements: Dict[str, str] = None  # {"title": "...", "subtitle": "..."}

    # Metadata
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")


class CanvasDesigner:
    """
    Main execution engine for canvas-design skill.

    Follows three-layer architecture:
    - Layer 1: Design philosophy (SKILL.md rules)
    - Layer 2: Design specifications (this class, JSON config)
    - Layer 3: Actual rendering (reportlab/PIL)
    """

    def __init__(
        self,
        project_name: str,
        agent_name: str = "X4-平面设计师",
        fonts_dir: Optional[Path] = None
    ):
        """
        Initialize designer with output path configuration.

        Args:
            project_name: 项目名称 (e.g., "火锅店开业筹备")
            agent_name: 智能体名称 (default: "X4-平面设计师")
            fonts_dir: Path to canvas-fonts directory
        """
        self.project_name = project_name
        self.agent_name = agent_name

        # Locate fonts directory
        if fonts_dir is None:
            skill_dir = Path(__file__).parent.parent
            self.fonts_dir = skill_dir / "canvas-fonts"
        else:
            self.fonts_dir = Path(fonts_dir)

        if not self.fonts_dir.exists():
            raise FileNotFoundError(f"Fonts directory not found: {self.fonts_dir}")

        # Output base path (following global convention)
        self.output_base = Path("output") / project_name / agent_name / "canvas-design"

    def _get_output_paths(self, design_type: str) -> Dict[str, Path]:
        """
        Generate standard output paths following global CLAUDE.md convention.

        Returns dict with keys: plans, results, logs, metadata
        """
        design_dir = self.output_base / design_type

        return {
            "plans": design_dir / "plans",
            "results": design_dir / "results",
            "logs": design_dir / "logs",
            "metadata": design_dir / "metadata"
        }

    def _ensure_output_dirs(self, design_type: str):
        """Create output directory structure if not exists."""
        paths = self._get_output_paths(design_type)
        for path in paths.values():
            path.mkdir(parents=True, exist_ok=True)

    def create_design(
        self,
        user_prompt: str,
        design_type: Literal["poster", "menu-cover", "packaging", "logo", "flyer", "banner"],
        output_format: Literal["pdf", "png"] = "png",
        philosophy: Optional[Dict[str, str]] = None,
        canvas_size: Optional[tuple[int, int]] = None
    ) -> Dict[str, Any]:
        """
        Complete two-phase workflow: philosophy → visual expression.

        Args:
            user_prompt: User's design request
            design_type: Type of design to create
            output_format: Output file format
            philosophy: Pre-generated philosophy (if None, prompts Claude to generate)
            canvas_size: Canvas dimensions in pixels (if None, uses defaults)

        Returns:
            Dict with result metadata including file paths
        """
        # Ensure output directories exist
        self._ensure_output_dirs(design_type)
        paths = self._get_output_paths(design_type)

        # Phase 1: Philosophy Creation
        if philosophy is None:
            # Return guidance for Claude to generate philosophy
            return {
                "status": "needs_philosophy",
                "message": (
                    "Please generate a design philosophy following SKILL.md guidelines:\n"
                    "1. Name the movement (1-2 words)\n"
                    "2. Write 4-6 paragraphs describing visual essence\n"
                    "3. Emphasize craftsmanship and expert execution\n"
                    "4. Keep text minimal - visual expression over words\n"
                    "\nThen call this method again with philosophy parameter."
                ),
                "user_prompt": user_prompt,
                "design_type": design_type
            }

        # Set default canvas sizes based on design type
        if canvas_size is None:
            size_defaults = {
                "poster": (2480, 3508),  # A4 @ 300 DPI (portrait)
                "menu-cover": (2480, 3508),  # A4 @ 300 DPI
                "packaging": (2000, 2000),  # Square
                "logo": (1000, 1000),  # Square
                "flyer": (1754, 2480),  # A5 @ 300 DPI
                "banner": (3000, 1000)  # Wide banner
            }
            canvas_size = size_defaults.get(design_type, (2480, 3508))

        # Create design specification
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        spec = DesignSpec(
            project_name=self.project_name,
            agent_name=self.agent_name,
            design_type=design_type,
            movement_name=philosophy["movement_name"],
            philosophy_content=philosophy["philosophy_content"],
            canvas_size=canvas_size,
            output_format=output_format,
            color_palette=philosophy.get("color_palette", ["#000000", "#FFFFFF"]),
            primary_font=philosophy.get("primary_font", "WorkSans-Regular.ttf"),
            secondary_font=philosophy.get("secondary_font"),
            text_elements=philosophy.get("text_elements", {}),
            timestamp=timestamp
        )

        # Save design specification to plans/ directory
        spec_filename = f"{design_type}_{philosophy['movement_name'].lower().replace(' ', '-')}_{timestamp}_spec.json"
        spec_path = paths["plans"] / spec_filename

        with open(spec_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(spec), f, ensure_ascii=False, indent=2)

        # Phase 2: Visual Expression
        if output_format == "pdf":
            output_file = self._render_pdf(spec, paths)
        else:  # png
            output_file = self._render_png(spec, paths)

        # Save philosophy as .md file in results/
        philosophy_file = paths["results"] / f"{design_type}_{timestamp}_philosophy.md"
        with open(philosophy_file, 'w', encoding='utf-8') as f:
            f.write(f"# {philosophy['movement_name']}\n\n")
            f.write(philosophy["philosophy_content"])

        # Save metadata
        metadata = {
            "project_name": self.project_name,
            "agent_name": self.agent_name,
            "design_type": design_type,
            "movement_name": philosophy["movement_name"],
            "timestamp": timestamp,
            "user_prompt": user_prompt,
            "output_file": str(output_file),
            "philosophy_file": str(philosophy_file),
            "spec_file": str(spec_path),
            "canvas_size": canvas_size,
            "output_format": output_format
        }

        metadata_file = paths["metadata"] / f"{design_type}_{timestamp}_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        return {
            "status": "success",
            "output_file": output_file,
            "philosophy_file": philosophy_file,
            "metadata_file": metadata_file,
            "spec_file": spec_path,
            "message": f"✅ Design created: {output_file}"
        }

    def _render_pdf(self, spec: DesignSpec, paths: Dict[str, Path]) -> Path:
        """
        Render design as PDF using reportlab.

        This is a basic implementation. Claude should enhance this
        based on the specific design philosophy.
        """
        if not REPORTLAB_AVAILABLE:
            raise RuntimeError("reportlab not installed")

        # Output filename
        filename = (
            f"{spec.design_type}_{spec.movement_name.lower().replace(' ', '-')}_"
            f"{spec.timestamp}.pdf"
        )
        output_path = paths["results"] / filename

        # Create canvas
        c = canvas.Canvas(
            str(output_path),
            pagesize=(spec.canvas_size[0], spec.canvas_size[1])
        )

        # Register fonts
        try:
            font_path = self.fonts_dir / spec.primary_font
            if font_path.exists():
                pdfmetrics.registerFont(TTFont('PrimaryFont', str(font_path)))
            else:
                print(f"⚠️  Font not found: {font_path}, using default")
        except Exception as e:
            print(f"⚠️  Font registration failed: {e}")

        # Basic rendering (Claude should enhance this based on philosophy)
        width, height = spec.canvas_size

        # Background
        c.setFillColorRGB(*self._hex_to_rgb_normalized(spec.color_palette[0]))
        c.rect(0, 0, width, height, fill=1)

        # Text elements
        if spec.text_elements:
            c.setFillColorRGB(*self._hex_to_rgb_normalized(spec.color_palette[-1]))
            y_position = height * 0.7

            for key, text in spec.text_elements.items():
                c.setFont('PrimaryFont' if 'PrimaryFont' in c.getAvailableFonts() else 'Helvetica', 48)
                c.drawCentredString(width / 2, y_position, text)
                y_position -= 80

        c.save()

        return output_path

    def _render_png(self, spec: DesignSpec, paths: Dict[str, Path]) -> Path:
        """
        Render design as PNG using PIL.

        This is a basic implementation. Claude should enhance this
        based on the specific design philosophy.
        """
        if not PIL_AVAILABLE:
            raise RuntimeError("Pillow not installed")

        # Output filename
        filename = (
            f"{spec.design_type}_{spec.movement_name.lower().replace(' ', '-')}_"
            f"{spec.timestamp}.png"
        )
        output_path = paths["results"] / filename

        # Create image
        img = Image.new('RGB', spec.canvas_size, self._hex_to_rgb(spec.color_palette[0]))
        draw = ImageDraw.Draw(img)

        # Load font
        try:
            font_path = self.fonts_dir / spec.primary_font
            if font_path.exists():
                font = ImageFont.truetype(str(font_path), 72)
            else:
                font = ImageFont.load_default()
                print(f"⚠️  Font not found: {font_path}, using default")
        except Exception as e:
            font = ImageFont.load_default()
            print(f"⚠️  Font loading failed: {e}")

        # Text elements (basic implementation)
        if spec.text_elements:
            y_position = spec.canvas_size[1] * 0.4
            text_color = self._hex_to_rgb(spec.color_palette[-1])

            for key, text in spec.text_elements.items():
                # Center text
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                x_position = (spec.canvas_size[0] - text_width) / 2

                draw.text((x_position, y_position), text, fill=text_color, font=font)
                y_position += 100

        # Save
        img.save(output_path, 'PNG', dpi=(300, 300))

        return output_path

    @staticmethod
    def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
        """Convert hex color to RGB tuple (0-255 range)."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    @staticmethod
    def _hex_to_rgb_normalized(hex_color: str) -> tuple[float, float, float]:
        """Convert hex color to RGB tuple (0-1 range for reportlab)."""
        r, g, b = CanvasDesigner._hex_to_rgb(hex_color)
        return (r / 255, g / 255, b / 255)


if __name__ == "__main__":
    print("Canvas Designer Execution Engine")
    print("See README.md or reference.md for usage examples")
