#!/usr/bin/env python3
"""
Canvas Design Engine for Restaurant Branding
==============================================
Generates visual designs (posters, menu covers, packaging) using Claude's
canvas design capabilities. Implements design philosophy principles from
SKILL.md and outputs production-ready PNG/PDF files.

Core Capabilities:
- Poster design generation
- Menu cover creation
- Packaging design
- Digital marketing graphics
"""

import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Literal


# ============================================
# Configuration and Data Classes
# ============================================

@dataclass
class ColorPalette:
    """Design color palette"""
    primary: str  # Hex color
    secondary: str
    accent: str
    neutral: str
    background: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "primary": self.primary,
            "secondary": self.secondary,
            "accent": self.accent,
            "neutral": self.neutral,
            "background": self.background
        }


@dataclass
class Typography:
    """Typography system"""
    heading_font: str
    body_font: str
    accent_font: Optional[str] = None
    heading_size: int = 48
    body_size: int = 16

    def to_dict(self) -> Dict:
        return {
            "heading": {"font": self.heading_font, "size": self.heading_size},
            "body": {"font": self.body_font, "size": self.body_size},
            "accent": {"font": self.accent_font} if self.accent_font else None
        }


@dataclass
class DesignConfig:
    """Complete design configuration"""
    design_type: Literal["poster", "menu-cover", "packaging", "digital-graphic"]
    cuisine_type: str  # "chinese", "japanese", "italian", etc.
    dimensions: str  # "1920x1080", "A3", "A4", etc.
    resolution: int = 300  # DPI
    color_mode: Literal["RGB", "CMYK"] = "RGB"
    output_format: Literal["PNG", "PDF", "both"] = "PNG"


# ============================================
# Pre-defined Restaurant Palettes
# ============================================

RESTAURANT_PALETTES = {
    "chinese": ColorPalette(
        primary="#DC143C",    # Crimson Red
        secondary="#FFD700",  # Gold
        accent="#8B0000",     # Dark Red
        neutral="#F5F5DC",    # Beige
        background="#FFFAF0"  # Floral White
    ),
    "japanese": ColorPalette(
        primary="#000000",    # Black
        secondary="#FFFFFF",  # White
        accent="#D4AF37",     # Metallic Gold
        neutral="#F5F5F5",    # Off-white
        background="#FAFAFA"
    ),
    "italian": ColorPalette(
        primary="#228B22",    # Forest Green
        secondary="#DC143C",  # Red
        accent="#F5DEB3",     # Wheat
        neutral="#8B4513",    # Saddle Brown
        background="#FFFAF0"  # Floral White
    ),
    "french": ColorPalette(
        primary="#002395",    # Blue
        secondary="#ED2939",  # Red
        accent="#B8860B",     # Dark Gold
        neutral="#4A4A4A",    # Charcoal
        background="#F8F8F8"
    ),
    "hotpot": ColorPalette(
        primary="#FF4500",    # Flame Orange
        secondary="#DC143C",  # Hot Red
        accent="#FFD700",     # Gold
        neutral="#2F1B1B",    # Dark Brown
        background="#FFF8F0"
    ),
    "cafe": ColorPalette(
        primary="#6F4E37",    # Coffee Brown
        secondary="#D2B48C",  # Tan
        accent="#F4A460",     # Sandy Brown
        neutral="#4A4A4A",
        background="#FFFAF0"
    ),
}


# ============================================
# Design Brief Generator
# ============================================

class DesignBriefGenerator:
    """
    Generates comprehensive design briefs for Claude to execute
    Translates user requirements into detailed design specifications
    """

    def generate_poster_brief(
        self,
        content: str,
        palette: ColorPalette,
        style: str = "modern"
    ) -> str:
        """Generate promotional poster design brief"""
        return f"""Design a professional restaurant promotional poster with the following specifications:

**Content**:
{content}

**Visual Style**: {style}

**Color Palette**:
- Primary: {palette.primary} (main brand color, use for headline and key elements)
- Secondary: {palette.secondary} (supporting color, accents)
- Accent: {palette.accent} (highlights, call-to-action)
- Background: {palette.background} (base canvas)

**Layout Requirements**:
- Use Z-pattern or F-pattern for eye flow
- Bold headline (minimum 48pt equivalent)
- Hero visual (food or promotional graphic) at 40% of canvas
- Clear call-to-action button or text
- 30-40% white space for breathing room

**Typography Hierarchy**:
- Headline: Large, bold, attention-grabbing
- Subheading: Medium, clear information
- Body: Readable details
- CTA: Prominent, contrasting color

**Design Principles**:
- High contrast for readability
- Appetite appeal (warm colors, inviting)
- Clear visual hierarchy
- Professional, print-ready quality

**Technical Specs**:
- Resolution: Print quality (300 DPI equivalent)
- Color mode: {palette.primary} palette strictly enforced
- Composition: Balanced, professional
"""

    def generate_menu_cover_brief(
        self,
        restaurant_name: str,
        palette: ColorPalette,
        style: str = "elegant"
    ) -> str:
        """Generate menu cover design brief"""
        return f"""Design an elegant restaurant menu cover with the following specifications:

**Restaurant Name**: {restaurant_name}

**Visual Style**: {style}, sophisticated, premium

**Color Palette**:
- Primary: {palette.primary} (brand identity)
- Secondary: {palette.secondary}
- Background: {palette.background} (clean, inviting)
- Accent: {palette.accent} (subtle highlights)

**Layout Requirements**:
- Centered or asymmetric composition with strong focal point
- Restaurant name prominently displayed
- Logo placement (if provided, reserve space)
- Minimal text (let design breathe)
- 50%+ white space for sophistication

**Design Elements**:
- Subtle background texture or pattern (10-15% opacity)
- Premium feel appropriate to restaurant tier
- Cultural elements if applicable (e.g., Chinese motifs, Japanese minimalism)
- Professional, refined aesthetic

**Typography**:
- Restaurant name: Large, elegant, readable
- Tagline (if any): Subtle, complementary
- No body text on cover

**Technical Specs**:
- Print-ready quality
- Color harmony and brand consistency
- Scalable design (various menu sizes)
"""

    def generate_packaging_brief(
        self,
        item_type: str,
        palette: ColorPalette,
        pattern_style: str = "geometric"
    ) -> str:
        """Generate packaging design brief"""
        return f"""Design restaurant packaging/branding elements with the following specifications:

**Packaging Type**: {item_type} (e.g., takeout box, bag, cup)

**Visual Style**: {pattern_style}, brand-consistent, practical

**Color Palette**:
- Primary: {palette.primary} (dominant brand color)
- Secondary: {palette.secondary}
- Pattern/Background: {palette.neutral}
- Accent: {palette.accent}

**Design Requirements**:
- Repeatable pattern or focused brand mark
- Logo placement (prominent but not overwhelming)
- Brand colors consistently applied
- Design works at multiple scales

**Pattern/Texture**:
- If pattern: Tileable, brand-consistent
- If brand mark: Clear, scalable, recognizable
- Cultural appropriateness

**Practical Considerations**:
- Design readable on physical materials
- Works with various production methods
- Clear brand identification at distance

**Technical Specs**:
- Production-ready
- Scalable design
- Color mode appropriate for printing
"""


# ============================================
# Canvas Executor
# ============================================

class CanvasDesignExecutor:
    """
    Executes canvas design generation using Claude
    Manages design brief → execution → output workflow
    """

    def __init__(self):
        self.brief_generator = DesignBriefGenerator()

    def execute(
        self,
        design_brief: str,
        config: DesignConfig,
        output_dir: Optional[Path] = None,
        project_name: str = "未命名项目"
    ) -> Dict:
        """
        Execute design generation

        Args:
            design_brief: Detailed design brief for Claude
            config: Design configuration
            output_dir: Output directory (default: output/[项目名]/X4-平面设计师/canvas-design/)
            project_name: Project name for path organization

        Returns:
            Execution result with file paths and metadata
        """
        # Set output directory
        if output_dir is None:
            output_dir = Path("output") / project_name / "X4-平面设计师" / "canvas-design" / config.design_type

        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_base = f"{config.design_type}_{config.cuisine_type}_{timestamp}"

        # Build metadata
        metadata = {
            "project_name": project_name,
            "design_type": config.design_type,
            "cuisine_type": config.cuisine_type,
            "dimensions": config.dimensions,
            "resolution": config.resolution,
            "color_mode": config.color_mode,
            "timestamp": datetime.now().isoformat(),
            "design_brief": design_brief
        }

        # Save design brief for reference
        brief_path = output_dir / f"{filename_base}_brief.md"
        brief_path.write_text(design_brief, encoding="utf-8")

        # Save metadata
        metadata_path = output_dir / f"{filename_base}_metadata.json"
        metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

        print(f"✅ Design brief generated: {brief_path}")
        print(f"📋 Metadata saved: {metadata_path}")
        print(f"\n{'='*60}")
        print("📢 MANUAL STEP REQUIRED:")
        print("="*60)
        print(f"\nThe design brief has been generated at:")
        print(f"  {brief_path}")
        print(f"\nTo complete the design:")
        print(f"1. Review the brief in the file above")
        print(f"2. Use Claude's canvas design capabilities to create the visual")
        print(f"3. Export as PNG/PDF to: {output_dir}/")
        print(f"4. Name the file: {filename_base}.png or {filename_base}.pdf")
        print(f"\n{'='*60}\n")

        return {
            "success": True,
            "brief_path": str(brief_path),
            "metadata_path": str(metadata_path),
            "output_dir": str(output_dir),
            "expected_filename": f"{filename_base}.png",
            "metadata": metadata,
            "message": "Design brief generated. Manual canvas design step required."
        }


# ============================================
# High-Level API Functions
# ============================================

def create_poster(
    content: str,
    cuisine_type: str = "chinese",
    dimensions: str = "1920x1080",
    style: str = "modern",
    project_name: str = "海报设计"
) -> Dict:
    """
    Create a promotional poster

    Args:
        content: Poster content (headline, details, offer)
        cuisine_type: Cuisine type (for palette selection)
        dimensions: Output dimensions
        style: Visual style ("modern", "traditional", "minimalist")
        project_name: Project name for organization

    Returns:
        Execution result
    """
    palette = RESTAURANT_PALETTES.get(cuisine_type, RESTAURANT_PALETTES["chinese"])
    brief_gen = DesignBriefGenerator()
    executor = CanvasDesignExecutor()

    brief = brief_gen.generate_poster_brief(content, palette, style)

    config = DesignConfig(
        design_type="poster",
        cuisine_type=cuisine_type,
        dimensions=dimensions,
        resolution=300,
        color_mode="RGB",
        output_format="PNG"
    )

    return executor.execute(brief, config, project_name=project_name)


def create_menu_cover(
    restaurant_name: str,
    cuisine_type: str = "chinese",
    style: str = "elegant",
    project_name: str = "菜单封面设计"
) -> Dict:
    """
    Create a menu cover

    Args:
        restaurant_name: Restaurant name
        cuisine_type: Cuisine type (for palette selection)
        style: Visual style
        project_name: Project name for organization

    Returns:
        Execution result
    """
    palette = RESTAURANT_PALETTES.get(cuisine_type, RESTAURANT_PALETTES["chinese"])
    brief_gen = DesignBriefGenerator()
    executor = CanvasDesignExecutor()

    brief = brief_gen.generate_menu_cover_brief(restaurant_name, palette, style)

    config = DesignConfig(
        design_type="menu-cover",
        cuisine_type=cuisine_type,
        dimensions="A4",
        resolution=300,
        color_mode="CMYK",
        output_format="PDF"
    )

    return executor.execute(brief, config, project_name=project_name)


def create_packaging(
    item_type: str,
    cuisine_type: str = "chinese",
    pattern_style: str = "geometric",
    project_name: str = "包装设计"
) -> Dict:
    """
    Create packaging design

    Args:
        item_type: Packaging type (e.g., "外卖盒", "购物袋", "纸杯")
        cuisine_type: Cuisine type (for palette selection)
        pattern_style: Pattern style ("geometric", "organic", "minimalist")
        project_name: Project name for organization

    Returns:
        Execution result
    """
    palette = RESTAURANT_PALETTES.get(cuisine_type, RESTAURANT_PALETTES["chinese"])
    brief_gen = DesignBriefGenerator()
    executor = CanvasDesignExecutor()

    brief = brief_gen.generate_packaging_brief(item_type, palette, pattern_style)

    config = DesignConfig(
        design_type="packaging",
        cuisine_type=cuisine_type,
        dimensions="custom",
        resolution=300,
        color_mode="CMYK",
        output_format="PDF"
    )

    return executor.execute(brief, config, project_name=project_name)


# ============================================
# CLI Interface
# ============================================

def main():
    """Command-line interface for canvas design generation"""
    import argparse

    parser = argparse.ArgumentParser(description="Canvas Design Engine for Restaurant Branding")
    parser.add_argument("type", choices=["poster", "menu-cover", "packaging"],
                       help="Design type")
    parser.add_argument("--content", help="Design content (for poster)")
    parser.add_argument("--name", help="Restaurant name (for menu cover)")
    parser.add_argument("--item", help="Item type (for packaging)")
    parser.add_argument("--cuisine", default="chinese",
                       choices=list(RESTAURANT_PALETTES.keys()),
                       help="Cuisine type")
    parser.add_argument("--style", default="modern", help="Visual style")
    parser.add_argument("--project", default="设计项目", help="Project name")

    args = parser.parse_args()

    if args.type == "poster":
        if not args.content:
            print("❌ Error: --content required for poster design")
            sys.exit(1)
        result = create_poster(
            content=args.content,
            cuisine_type=args.cuisine,
            style=args.style,
            project_name=args.project
        )
    elif args.type == "menu-cover":
        if not args.name:
            print("❌ Error: --name required for menu cover design")
            sys.exit(1)
        result = create_menu_cover(
            restaurant_name=args.name,
            cuisine_type=args.cuisine,
            style=args.style,
            project_name=args.project
        )
    elif args.type == "packaging":
        if not args.item:
            print("❌ Error: --item required for packaging design")
            sys.exit(1)
        result = create_packaging(
            item_type=args.item,
            cuisine_type=args.cuisine,
            pattern_style=args.style,
            project_name=args.project
        )

    if result["success"]:
        print(f"\n✨ Design brief generated successfully!")
        print(f"📁 Brief: {result['brief_path']}")
        print(f"📋 Metadata: {result['metadata_path']}")
        print(f"💡 Follow the instructions above to complete the design.")
    else:
        print(f"\n❌ Design generation failed: {result.get('error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
