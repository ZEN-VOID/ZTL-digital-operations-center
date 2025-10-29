#!/usr/bin/env python3
"""
Theme Factory Application Engine for Restaurant Branding
=========================================================
Applies professional design themes to restaurant materials.
Includes 10 pre-designed themes + custom theme generation.

Core Capabilities:
- Theme selection and application
- CSS variable generation
- Theme consistency validation
- Custom theme creation
"""

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Literal


# ============================================
# Theme Data Classes
# ============================================

@dataclass
class ColorPalette:
    """Theme color palette"""
    primary: str
    secondary: str
    accent: str
    neutral: str
    background: str
    text: Optional[str] = None

    # Additional optional colors
    warm: Optional[str] = None
    dark: Optional[str] = None
    highlight: Optional[str] = None
    natural: Optional[str] = None

    def to_css_vars(self) -> str:
        """Generate CSS variable declarations"""
        vars_list = [
            f"  --theme-primary: {self.primary};",
            f"  --theme-secondary: {self.secondary};",
            f"  --theme-accent: {self.accent};",
            f"  --theme-neutral: {self.neutral};",
            f"  --theme-bg: {self.background};"
        ]

        if self.text:
            vars_list.append(f"  --theme-text: {self.text};")
        if self.warm:
            vars_list.append(f"  --theme-warm: {self.warm};")
        if self.dark:
            vars_list.append(f"  --theme-dark: {self.dark};")
        if self.highlight:
            vars_list.append(f"  --theme-highlight: {self.highlight};")
        if self.natural:
            vars_list.append(f"  --theme-natural: {self.natural};")

        return "\n".join(vars_list)


@dataclass
class Typography:
    """Theme typography system"""
    heading_font: str
    body_font: str
    accent_font: Optional[str] = None
    heading_fallback: str = "serif"
    body_fallback: str = "sans-serif"
    accent_fallback: str = "cursive"

    def to_css_vars(self) -> str:
        """Generate CSS font variable declarations"""
        vars_list = [
            f"  --font-heading: '{self.heading_font}', {self.heading_fallback};",
            f"  --font-body: '{self.body_font}', {self.body_fallback};"
        ]

        if self.accent_font:
            vars_list.append(f"  --font-accent: '{self.accent_font}', {self.accent_fallback};")

        return "\n".join(vars_list)


@dataclass
class VisualStyle:
    """Theme visual style guidelines"""
    description: str
    patterns: List[str]
    photography_style: str
    textures: List[str]


@dataclass
class Theme:
    """Complete restaurant design theme"""
    name: str
    category: str
    brand_personality: str
    colors: ColorPalette
    typography: Typography
    visual_style: VisualStyle
    use_cases: str

    def to_css_file(self) -> str:
        """Generate complete CSS theme file"""
        return f"""/* ============================================
   Restaurant Theme: {self.name}
   Category: {self.category}
   Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
   ============================================ */

:root {{
  /* === Color Palette === */
{self.colors.to_css_vars()}

  /* === Typography === */
{self.typography.to_css_vars()}
}}

/* === Theme Application Notes ===
Brand Personality: {self.brand_personality}
Visual Style: {self.visual_style.description}
Use Cases: {self.use_cases}
*/
"""

    def to_dict(self) -> Dict:
        """Convert theme to dictionary"""
        return {
            "name": self.name,
            "category": self.category,
            "brand_personality": self.brand_personality,
            "colors": asdict(self.colors),
            "typography": asdict(self.typography),
            "visual_style": asdict(self.visual_style),
            "use_cases": self.use_cases
        }


# ============================================
# Pre-Designed Theme Library
# ============================================

PRESET_THEMES = {
    "chinese-imperial": Theme(
        name="Chinese Imperial",
        category="chinese",
        brand_personality="Traditional, prestigious, celebratory, family-oriented",
        colors=ColorPalette(
            primary="#DC143C",
            secondary="#FFD700",
            accent="#8B0000",
            neutral="#F5F5DC",
            background="#FFFAF0",
            text="#2C2416"
        ),
        typography=Typography(
            heading_font="Noto Serif SC",
            body_font="Noto Sans SC",
            accent_font="Ma Shan Zheng",
            heading_fallback="serif",
            body_fallback="sans-serif",
            accent_fallback="cursive"
        ),
        visual_style=VisualStyle(
            description="Flowing patterns, auspicious symbols, symmetrical balance, warm atmospheric photography",
            patterns=["clouds", "waves", "dragons", "lanterns", "coins", "knots"],
            photography_style="Warm atmospheric with rich textures",
            textures=["silk", "lacquer", "gold leaf"]
        ),
        use_cases="Dim sum restaurants, Cantonese dining, hotpot chains, Chinese New Year promotions"
    ),

    "japanese-zen": Theme(
        name="Japanese Zen",
        category="japanese",
        brand_personality="Minimalist, refined, authentic, tranquil",
        colors=ColorPalette(
            primary="#000000",
            secondary="#FFFFFF",
            accent="#D4AF37",
            neutral="#F5F5F5",
            background="#FAFAFA",
            natural="#8FBC8F"
        ),
        typography=Typography(
            heading_font="Noto Serif JP",
            body_font="Noto Sans JP",
            accent_font="Shippori Mincho",
            heading_fallback="serif",
            body_fallback="sans-serif"
        ),
        visual_style=VisualStyle(
            description="Abundant white space (ma), asymmetric balance, natural materials, minimalist photography",
            patterns=["asymmetric balance", "negative space"],
            photography_style="Minimalist with single subject focus",
            textures=["washi paper", "bamboo", "wood", "stone"]
        ),
        use_cases="Sushi bars, ramen shops, kaiseki restaurants, Japanese tea houses"
    ),

    "italian-rustico": Theme(
        name="Italian Rustico",
        category="italian",
        brand_personality="Warm, family-friendly, authentic, hearty",
        colors=ColorPalette(
            primary="#228B22",
            secondary="#DC143C",
            accent="#F5DEB3",
            neutral="#8B4513",
            background="#FFFAF0"
        ),
        typography=Typography(
            heading_font="Playfair Display",
            body_font="Open Sans",
            accent_font="Pacifico"
        ),
        visual_style=VisualStyle(
            description="Rustic textures, checkered patterns, family-style food photography, natural lighting",
            patterns=["red/white checkered tablecloths", "Italian flag colors"],
            photography_style="Family-style with warm tones and natural lighting",
            textures=["wood grain", "burlap", "terracotta"]
        ),
        use_cases="Italian trattorias, pizza restaurants, family-style Italian dining, pasta bars"
    ),

    "french-elegance": Theme(
        name="French Elegance",
        category="french",
        brand_personality="Sophisticated, refined, romantic, upscale",
        colors=ColorPalette(
            primary="#002395",
            secondary="#ED2939",
            accent="#B8860B",
            neutral="#4A4A4A",
            background="#F8F8F8"
        ),
        typography=Typography(
            heading_font="Cormorant Garamond",
            body_font="Lato",
            accent_font="Allura"
        ),
        visual_style=VisualStyle(
            description="Clean uncluttered layouts, high-contrast B&W photography, elegant plating",
            patterns=["French motifs", "fleur-de-lis", "Eiffel Tower"],
            photography_style="High-contrast black and white, sophisticated plating",
            textures=["sophisticated color blocking"]
        ),
        use_cases="French bistros, patisseries, fine dining, wine bars"
    ),

    "american-classic": Theme(
        name="American Classic",
        category="american",
        brand_personality="Nostalgic, friendly, fun, comfortable",
        colors=ColorPalette(
            primary="#FF0000",
            secondary="#0047AB",
            accent="#FFD700",
            neutral="#FFFFFF",
            background="#FFFFFF",
            dark="#000000"
        ),
        typography=Typography(
            heading_font="Bebas Neue",
            body_font="Roboto",
            accent_font="Pacifico",
            heading_fallback="sans-serif"
        ),
        visual_style=VisualStyle(
            description="Bold colors, retro 50s/60s diner aesthetics, checkered floors, neon signs",
            patterns=["checkered floors", "American flag motifs"],
            photography_style="Abundant appetizing food photography with high contrast",
            textures=["retro diner elements"]
        ),
        use_cases="Diners, burger joints, American BBQ, sports bars"
    ),

    "hotpot-fiesta": Theme(
        name="Hotpot Fiesta",
        category="hotpot",
        brand_personality="Energetic, communal, vibrant, exciting",
        colors=ColorPalette(
            primary="#FF4500",
            secondary="#DC143C",
            accent="#FFD700",
            neutral="#2F1B1B",
            background="#FFF8F0",
            warm="#FF6347"
        ),
        typography=Typography(
            heading_font="Anton",
            body_font="Noto Sans SC",
            accent_font="Fredoka One",
            heading_fallback="sans-serif"
        ),
        visual_style=VisualStyle(
            description="Dynamic flowing patterns (fire, steam), vibrant overlays, communal dining photography",
            patterns=["fire", "steam", "flowing energy"],
            photography_style="Steam and bubbling broth imagery, energetic compositions",
            textures=["vibrant color overlays"]
        ),
        use_cases="Hotpot restaurants, Szechuan spicy cuisine, BBQ hotpot, shabu-shabu"
    ),

    "cafe-moderne": Theme(
        name="Cafe Moderne",
        category="cafe",
        brand_personality="Contemporary, cozy, Instagram-worthy, artisanal",
        colors=ColorPalette(
            primary="#6F4E37",
            secondary="#D2B48C",
            accent="#F4A460",
            neutral="#FFFAF0",
            background="#FFFAF0",
            highlight="#FF6B9D"
        ),
        typography=Typography(
            heading_font="Montserrat",
            body_font="Lora",
            accent_font="Satisfy",
            heading_fallback="sans-serif",
            body_fallback="serif"
        ),
        visual_style=VisualStyle(
            description="Clean minimalist layouts, flat lay photography, natural light, plants and lifestyle",
            patterns=["handwritten accents"],
            photography_style="Overhead flat lay shots with natural light, bright and airy",
            textures=["plants", "lifestyle elements"]
        ),
        use_cases="Coffee shops, cafes, brunch spots, bakeries, tea houses"
    ),

    "bbq-smokehouse": Theme(
        name="BBQ Smokehouse",
        category="bbq",
        brand_personality="Bold, masculine, rustic, authentic",
        colors=ColorPalette(
            primary="#8B4513",
            secondary="#FF4500",
            accent="#FFD700",
            neutral="#F5DEB3",
            background="#F5DEB3",
            dark="#2C1810"
        ),
        typography=Typography(
            heading_font="Bungee",
            body_font="Oswald",
            accent_font="Permanent Marker",
            heading_fallback="sans-serif"
        ),
        visual_style=VisualStyle(
            description="Rustic wood textures, charred smoky effects, close-up meat photography, dark moody lighting",
            patterns=["wood grain", "vintage Americana"],
            photography_style="Close-up meat with grill marks and bark, dark moody lighting",
            textures=["rustic wood", "charred effects"]
        ),
        use_cases="BBQ restaurants, steakhouses, grills, smokehouse, Texas BBQ"
    ),

    "fine-dining-luxury": Theme(
        name="Fine Dining Luxury",
        category="fine-dining",
        brand_personality="Exclusive, sophisticated, premium, refined",
        colors=ColorPalette(
            primary="#1C1C1C",
            secondary="#B8860B",
            accent="#800020",
            neutral="#E5E5E5",
            background="#FFFFFF"
        ),
        typography=Typography(
            heading_font="Bodoni Moda",
            body_font="Futura",
            accent_font="Tangerine",
            heading_fallback="serif",
            body_fallback="sans-serif"
        ),
        visual_style=VisualStyle(
            description="Abundant white space, minimalist plating, high contrast B&W, subtle gold accents",
            patterns=["gold foil effects", "elegant understated design"],
            photography_style="Minimalist plating photography with high contrast",
            textures=["gold accents", "foil effects"]
        ),
        use_cases="Michelin-starred restaurants, upscale dining, tasting menus, luxury hotels"
    ),

    "fast-casual-fresh": Theme(
        name="Fast Casual Fresh",
        category="fast-casual",
        brand_personality="Healthy, vibrant, modern, transparent",
        colors=ColorPalette(
            primary="#7CB342",
            secondary="#FF6F00",
            accent="#FDD835",
            neutral="#5D4037",
            background="#FAFAFA"
        ),
        typography=Typography(
            heading_font="Poppins",
            body_font="Raleway",
            accent_font="Caveat",
            heading_fallback="sans-serif"
        ),
        visual_style=VisualStyle(
            description="Bright natural colors, ingredient-focused photography, clean modern layouts",
            patterns=["transparent honest messaging"],
            photography_style="Fresh produce and healthy eating focused",
            textures=["natural", "organic"]
        ),
        use_cases="Salad bars, healthy bowls, smoothie shops, farm-to-table, organic cafes"
    )
}


# ============================================
# Theme Applier Engine
# ============================================

class ThemeApplier:
    """
    Apply themes to restaurant design materials
    Manages theme selection, application, and validation
    """

    def __init__(self):
        self.themes = PRESET_THEMES

    def get_theme(self, theme_id: str) -> Optional[Theme]:
        """Get theme by ID"""
        return self.themes.get(theme_id)

    def list_themes(self) -> List[str]:
        """List all available theme IDs"""
        return list(self.themes.keys())

    def apply_theme(
        self,
        theme_id: str,
        project_name: str,
        output_dir: Optional[Path] = None
    ) -> Dict:
        """
        Apply a theme to a project

        Args:
            theme_id: Theme identifier (e.g., "chinese-imperial")
            project_name: Project name for organization
            output_dir: Output directory (default: output/[项目名]/X4-平面设计师/themed-designs/)

        Returns:
            Application result with file paths
        """
        theme = self.get_theme(theme_id)
        if not theme:
            return {
                "success": False,
                "error": f"Theme '{theme_id}' not found. Available themes: {self.list_themes()}"
            }

        # Set output directory
        if output_dir is None:
            output_dir = Path("output") / project_name / "X4-平面设计师" / "themed-designs"

        # Create subdirectories
        theme_specs_dir = output_dir / "theme-specs"
        theme_specs_dir.mkdir(parents=True, exist_ok=True)

        # Generate timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Generate CSS file
        css_content = theme.to_css_file()
        css_path = theme_specs_dir / f"{theme_id}-variables_{timestamp}.css"
        css_path.write_text(css_content, encoding="utf-8")

        # Generate theme JSON metadata
        theme_json = theme.to_dict()
        theme_json["applied_at"] = datetime.now().isoformat()
        theme_json["project_name"] = project_name

        json_path = theme_specs_dir / f"{theme_id}-metadata_{timestamp}.json"
        json_path.write_text(json.dumps(theme_json, ensure_ascii=False, indent=2), encoding="utf-8")

        # Generate application guide
        guide_content = self._generate_application_guide(theme, project_name)
        guide_path = output_dir / "theme-documentation" / f"{theme_id}-application-guide_{timestamp}.md"
        guide_path.parent.mkdir(parents=True, exist_ok=True)
        guide_path.write_text(guide_content, encoding="utf-8")

        print(f"✅ Theme '{theme.name}' applied successfully!")
        print(f"📁 CSS Variables: {css_path}")
        print(f"📋 Metadata: {json_path}")
        print(f"📖 Application Guide: {guide_path}")

        return {
            "success": True,
            "theme_name": theme.name,
            "theme_id": theme_id,
            "css_path": str(css_path),
            "metadata_path": str(json_path),
            "guide_path": str(guide_path),
            "output_dir": str(output_dir),
            "theme": theme_json
        }

    def _generate_application_guide(self, theme: Theme, project_name: str) -> str:
        """Generate theme application guide in Markdown"""
        return f"""# Theme Application Guide: {theme.name}

**Project**: {project_name}
**Applied**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Category**: {theme.category}

---

## Brand Personality

{theme.brand_personality}

---

## Color Palette

| Role | Color | Hex Code | Usage |
|------|-------|----------|-------|
| Primary | {theme.colors.primary} | `{theme.colors.primary}` | Main brand color, headlines, key elements |
| Secondary | {theme.colors.secondary} | `{theme.colors.secondary}` | Supporting color, accents |
| Accent | {theme.colors.accent} | `{theme.colors.accent}` | Highlights, call-to-action |
| Neutral | {theme.colors.neutral} | `{theme.colors.neutral}` | Backgrounds, supporting elements |
| Background | {theme.colors.background} | `{theme.colors.background}` | Base canvas |

---

## Typography

- **Heading Font**: `{theme.typography.heading_font}` - Use for titles, headlines, and primary messages
- **Body Font**: `{theme.typography.body_font}` - Use for body text, descriptions, details
{f"- **Accent Font**: `{theme.typography.accent_font}` - Use sparingly for decorative elements" if theme.typography.accent_font else ""}

---

## Visual Style

### Description
{theme.visual_style.description}

### Key Patterns
{chr(10).join(f"- {pattern}" for pattern in theme.visual_style.patterns)}

### Photography Style
{theme.visual_style.photography_style}

### Textures
{chr(10).join(f"- {texture}" for texture in theme.visual_style.textures)}

---

## Use Cases

{theme.use_cases}

---

## Application Steps

1. **Import CSS Variables**: Load the generated CSS file into your design tool
2. **Install Fonts**: Ensure theme fonts are installed and accessible
3. **Apply Colors**: Use theme color palette exclusively
4. **Set Typography**: Apply heading and body fonts according to hierarchy
5. **Follow Visual Style**: Adhere to photography and texture guidelines
6. **Validate Consistency**: Check theme checklist before finalizing

---

## Theme Consistency Checklist

Before finalizing design, verify:

✅ **Colors**:
- [ ] All colors match theme specifications
- [ ] Contrast ratios meet accessibility standards (WCAG AA minimum)
- [ ] Color usage follows guidelines (primary/secondary/accent)

✅ **Typography**:
- [ ] Correct fonts applied (heading/body/accent)
- [ ] Type hierarchy follows theme scale
- [ ] Fallback fonts specified

✅ **Visual Style**:
- [ ] Photography style matches theme direction
- [ ] Patterns and textures align with theme
- [ ] Overall aesthetic consistent with theme personality

✅ **Layout**:
- [ ] Spacing follows theme principles
- [ ] Component styles match theme standards
- [ ] Responsive behavior maintains theme integrity

---

## Next Steps

1. Review this guide thoroughly
2. Apply theme to design brief using `canvas-design-restaurant` or other skills
3. Validate with checklist above
4. Document any customizations made
5. Archive final themed designs in `output/{project_name}/X4-平面设计师/themed-designs/applied-designs/`

---

**Remember**: Consistency is key! Once applied, maintain theme integrity across all materials.
"""


# ============================================
# High-Level API Functions
# ============================================

def apply_preset_theme(
    theme_id: str,
    project_name: str
) -> Dict:
    """
    Apply a pre-designed theme

    Args:
        theme_id: Theme identifier from PRESET_THEMES
        project_name: Project name for organization

    Returns:
        Application result
    """
    applier = ThemeApplier()
    return applier.apply_theme(theme_id, project_name)


def list_available_themes() -> Dict[str, str]:
    """
    List all available themes with descriptions

    Returns:
        Dictionary of theme_id: theme_name
    """
    applier = ThemeApplier()
    return {
        theme_id: theme.name
        for theme_id, theme in applier.themes.items()
    }


# ============================================
# CLI Interface
# ============================================

def main():
    """Command-line interface for theme application"""
    import argparse

    parser = argparse.ArgumentParser(description="Restaurant Theme Factory - Apply Design Themes")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # List themes
    subparsers.add_parser("list", help="List all available themes")

    # Apply theme
    apply_parser = subparsers.add_parser("apply", help="Apply a theme to a project")
    apply_parser.add_argument("theme_id", help="Theme ID (e.g., chinese-imperial)")
    apply_parser.add_argument("--project", required=True, help="Project name")

    args = parser.parse_args()

    if args.command == "list":
        themes = list_available_themes()
        print("\n🎨 Available Themes:\n")
        for theme_id, theme_name in themes.items():
            print(f"  • {theme_id:25s} - {theme_name}")
        print(f"\n📊 Total: {len(themes)} themes available\n")

    elif args.command == "apply":
        result = apply_preset_theme(args.theme_id, args.project)

        if result["success"]:
            print(f"\n✨ Theme applied successfully!")
            print(f"📁 Output directory: {result['output_dir']}")
        else:
            print(f"\n❌ Failed to apply theme: {result.get('error')}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
