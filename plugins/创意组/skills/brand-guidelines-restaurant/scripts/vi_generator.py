#!/usr/bin/env python3
"""
VI Document Generator for Restaurant Brands
============================================
Automatically generates comprehensive brand visual identity (VI) documents
including logo usage, color systems, typography standards, and application guidelines.

Core Capabilities:
- Complete VI document generation (Markdown format)
- Color palette with full specifications (Hex, RGB, CMYK, Pantone)
- Typography hierarchy and usage rules
- Logo usage guidelines and restrictions
- Asset organization structure
- Quality assurance checklists
"""

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Literal


# ============================================
# Configuration Data Classes
# ============================================

@dataclass
class ColorSpec:
    """Complete color specification"""
    name: str
    hex: str
    rgb: str  # "R### G### B###"
    cmyk: str  # "C## M## Y## K##"
    pantone: Optional[str] = None
    usage: str = ""
    percentage: str = ""  # "20-30%"


@dataclass
class TypefaceSpec:
    """Typography specification"""
    font_family: str
    weights: List[str]  # ["Light (300)", "Regular (400)", "Bold (700)"]
    designer: Optional[str] = None
    license: str = "Commercial License"


@dataclass
class TypeLevel:
    """Typography hierarchy level"""
    level: str  # "Hero Headline", "Major Headline", etc.
    font: str
    weight: str
    size_print: str  # "72pt"
    size_digital: str  # "48px"
    usage: str
    example: str


@dataclass
class BrandIdentity:
    """Core brand identity"""
    name: str
    tagline: Optional[str] = None
    promise: str = ""
    personality: List[str] = None  # 3-5 adjectives
    target_audience: str = ""
    positioning: str = ""


@dataclass
class VIConfig:
    """Complete VI system configuration"""
    brand_identity: BrandIdentity
    primary_colors: List[ColorSpec]
    secondary_colors: List[ColorSpec]
    neutral_colors: List[ColorSpec]
    primary_typeface: TypefaceSpec
    secondary_typeface: TypefaceSpec
    type_hierarchy: List[TypeLevel]
    cuisine_type: str
    photography_style: str
    version: str = "1.0"


# ============================================
# Cuisine-Specific Templates
# ============================================

CUISINE_TEMPLATES = {
    "chinese": {
        "colors": {
            "primary": [
                ColorSpec(
                    name="Prosperity Red",
                    hex="#DC143C",
                    rgb="R220 G20 B60",
                    cmyk="C0 M100 Y80 K0",
                    pantone="1935 C",
                    usage="Primary branding, major accents, calls-to-action",
                    percentage="20-30%"
                ),
                ColorSpec(
                    name="Fortune Gold",
                    hex="#FFD700",
                    rgb="R255 G215 B0",
                    cmyk="C0 M16 Y100 K0",
                    pantone="109 C",
                    usage="Secondary accents, premium elements, highlights",
                    percentage="15-20%"
                )
            ],
            "secondary": [
                ColorSpec(
                    name="Imperial Black",
                    hex="#2C2416",
                    rgb="R44 G36 B22",
                    cmyk="C0 M18 Y50 K86",
                    usage="Text, sophisticated accents",
                    percentage="10-15%"
                )
            ],
            "neutral": [
                ColorSpec(name="Beige Background", hex="#F5F5DC", rgb="R245 G245 B220", cmyk="C0 M0 Y10 K4", usage="Backgrounds, panels"),
                ColorSpec(name="White", hex="#FFFFFF", rgb="R255 G255 B255", cmyk="C0 M0 Y0 K0", usage="Clean backgrounds"),
                ColorSpec(name="Dark Text", hex="#333333", rgb="R51 G51 B51", cmyk="C0 M0 Y0 K80", usage="Body text")
            ]
        },
        "personality": ["Traditional", "Celebratory", "Prosperous", "Authentic", "Communal"],
        "photography": "Emphasize steam, heat, and communal dining. Show vibrant colors and generous portions. Include cultural elements subtly."
    },

    "japanese": {
        "colors": {
            "primary": [
                ColorSpec(
                    name="Zen Black",
                    hex="#1A1A1A",
                    rgb="R26 G26 B26",
                    cmyk="C0 M0 Y0 K90",
                    pantone="Black C",
                    usage="Primary branding, elegance, sophistication",
                    percentage="30-40%"
                ),
                ColorSpec(
                    name="Accent Red",
                    hex="#DC143C",
                    rgb="R220 G20 B60",
                    cmyk="C0 M100 Y80 K0",
                    usage="Minimal accents, energy points",
                    percentage="5-10%"
                )
            ],
            "secondary": [
                ColorSpec(
                    name="Natural Wood",
                    hex="#D2B48C",
                    rgb="R210 G180 B140",
                    cmyk="C0 M14 Y33 K18",
                    usage="Warmth, natural materials",
                    percentage="10-15%"
                )
            ],
            "neutral": [
                ColorSpec(name="Pure White", hex="#FFFFFF", rgb="R255 G255 B255", cmyk="C0 M0 Y0 K0", usage="Backgrounds, negative space"),
                ColorSpec(name="Off-White", hex="#F5F5F5", rgb="R245 G245 G245", cmyk="C0 M0 Y0 K4", usage="Subtle backgrounds"),
                ColorSpec(name="Charcoal", hex="#4A4A4A", rgb="R74 G74 B74", cmyk="C0 M0 Y0 K71", usage="Body text")
            ]
        },
        "personality": ["Minimalist", "Elegant", "Refined", "Precise", "Zen"],
        "photography": "Clean, minimalist compositions. Asymmetrical balance. Show craftsmanship and precision. Natural materials and textures."
    },

    "italian": {
        "colors": {
            "primary": [
                ColorSpec(
                    name="Basil Green",
                    hex="#228B22",
                    rgb="R34 G139 B34",
                    cmyk="C76 M0 Y100 K45",
                    pantone="355 C",
                    usage="Primary branding, freshness",
                    percentage="25-30%"
                ),
                ColorSpec(
                    name="Tomato Red",
                    hex="#DC143C",
                    rgb="R220 G20 B60",
                    cmyk="C0 M100 Y80 K0",
                    usage="Passion, Italian flag, accents",
                    percentage="20-25%"
                )
            ],
            "secondary": [
                ColorSpec(
                    name="Wheat Cream",
                    hex="#F5DEB3",
                    rgb="R245 G222 B179",
                    cmyk="C0 M9 Y27 K4",
                    usage="Warmth, bread, pasta",
                    percentage="15-20%"
                )
            ],
            "neutral": [
                ColorSpec(name="Warm White", hex="#FFFAF0", rgb="R255 G250 B240", cmyk="C0 M2 Y6 K0", usage="Backgrounds"),
                ColorSpec(name="Olive Black", hex="#3B3B2F", rgb="R59 G59 B47", cmyk="C0 M0 Y20 K77", usage="Text, earthy tones")
            ]
        },
        "personality": ["Rustic", "Warm", "Family-Oriented", "Authentic", "Passionate"],
        "photography": "Show fresh ingredients, rustic textures (wood, stone). Emphasize family and sharing. Warm, inviting atmosphere."
    },

    "french": {
        "colors": {
            "primary": [
                ColorSpec(
                    name="French Blue",
                    hex="#002395",
                    rgb="R0 G35 B149",
                    cmyk="C100 M77 Y0 K42",
                    pantone="Reflex Blue C",
                    usage="Sophistication, trust, French flag",
                    percentage="25-30%"
                ),
                ColorSpec(
                    name="Burgundy Red",
                    hex="#8B0000",
                    rgb="R139 G0 B0",
                    cmyk="C0 M100 Y100 K45",
                    usage="Elegance, wine, passion",
                    percentage="20-25%"
                )
            ],
            "secondary": [
                ColorSpec(
                    name="Champagne Gold",
                    hex="#D4AF37",
                    rgb="R212 G175 B55",
                    cmyk="C0 M17 Y74 K17",
                    usage="Luxury, quality, accents",
                    percentage="10-15%"
                )
            ],
            "neutral": [
                ColorSpec(name="Cream", hex="#FFF8DC", rgb="R255 G248 B220", cmyk="C0 M3 Y14 K0", usage="Elegant backgrounds"),
                ColorSpec(name="Charcoal", hex="#333333", rgb="R51 G51 B51", cmyk="C0 M0 Y0 K80", usage="Text")
            ]
        },
        "personality": ["Elegant", "Refined", "Sophisticated", "Classic", "Luxurious"],
        "photography": "Refined plating, soft lighting. Show elegance and attention to detail. Include wine and French cultural elements."
    },

    "hotpot": {
        "colors": {
            "primary": [
                ColorSpec(
                    name="Fiery Red",
                    hex="#FF4500",
                    rgb="R255 G69 B0",
                    cmyk="C0 M73 Y100 K0",
                    pantone="Orange 021 C",
                    usage="Heat, excitement, primary branding",
                    percentage="30-35%"
                ),
                ColorSpec(
                    name="Celebration Gold",
                    hex="#FFD700",
                    rgb="R255 G215 B0",
                    cmyk="C0 M16 Y100 K0",
                    usage="Joy, celebration, accents",
                    percentage="15-20%"
                )
            ],
            "secondary": [
                ColorSpec(
                    name="Chili Red",
                    hex="#DC143C",
                    rgb="R220 G20 B60",
                    cmyk="C0 M100 Y80 K0",
                    usage="Spice, intensity",
                    percentage="10-15%"
                )
            ],
            "neutral": [
                ColorSpec(name="Warm Cream", hex="#FFF8F0", rgb="R255 G248 B240", cmyk="C0 M3 Y6 K0", usage="Backgrounds"),
                ColorSpec(name="Dark Brown", hex="#4A3C28", rgb="R74 G60 B40", cmyk="C0 M19 Y46 K71", usage="Text")
            ]
        },
        "personality": ["Energetic", "Social", "Bold", "Spicy", "Lively"],
        "photography": "Show bubbling broth, steam, vibrant ingredients. Capture social dining and excitement. Use warm, energetic lighting."
    },

    "cafe": {
        "colors": {
            "primary": [
                ColorSpec(
                    name="Espresso Brown",
                    hex="#6F4E37",
                    rgb="R111 G78 B55",
                    cmyk="C0 M30 Y50 K56",
                    pantone="7504 C",
                    usage="Coffee, warmth, primary branding",
                    percentage="25-30%"
                ),
                ColorSpec(
                    name="Latte Cream",
                    hex="#F5E6D3",
                    rgb="R245 G230 B211",
                    cmyk="C0 M6 Y14 K4",
                    usage="Softness, comfort, backgrounds",
                    percentage="20-25%"
                )
            ],
            "secondary": [
                ColorSpec(
                    name="Caramel",
                    hex="#D2691E",
                    rgb="R210 G105 B30",
                    cmyk="C0 M50 Y86 K18",
                    usage="Warmth, sweetness, accents",
                    percentage="15-20%"
                )
            ],
            "neutral": [
                ColorSpec(name="Cream White", hex="#FFFAF0", rgb="R255 G250 B240", cmyk="C0 M2 Y6 K0", usage="Backgrounds"),
                ColorSpec(name="Dark Coffee", hex="#3E2723", rgb="R62 G39 B35", cmyk="C0 M37 Y44 K76", usage="Text")
            ]
        },
        "personality": ["Cozy", "Approachable", "Artisanal", "Warm", "Inviting"],
        "photography": "Soft, natural lighting. Show coffee art, pastries, cozy interiors. Emphasize warmth and craftsmanship."
    }
}


# ============================================
# VI Document Generator
# ============================================

class VIDocumentGenerator:
    """Generate comprehensive VI documents"""

    def __init__(self):
        pass

    def generate_complete_vi_document(self, config: VIConfig) -> str:
        """Generate complete VI document in Markdown"""

        doc = f"""# {config.brand_identity.name}
## Brand Visual Identity Guidelines

**Version**: {config.version}
**Date**: {datetime.now().strftime("%Y-%m-%d")}
**Cuisine Type**: {config.cuisine_type.capitalize()}
**Status**: Active

---

## Table of Contents

1. [Introduction](#1-introduction)
   - 1.1 Brand Story
   - 1.2 Brand Values
   - 1.3 How to Use This Guide

2. [Brand Identity](#2-brand-identity)
   - 2.1 Brand Essence
   - 2.2 Brand Personality
   - 2.3 Target Audience

3. [Logo System](#3-logo-system)
   - 3.1 Primary Logo
   - 3.2 Logo Variations
   - 3.3 Logo Usage Rules
   - 3.4 Logo Don'ts

4. [Color Palette](#4-color-palette)
   - 4.1 Primary Colors
   - 4.2 Secondary Colors
   - 4.3 Neutral Colors
   - 4.4 Color Usage Guidelines
   - 4.5 Accessibility Standards

5. [Typography](#5-typography)
   - 5.1 Primary Typeface
   - 5.2 Secondary Typeface
   - 5.3 Type Hierarchy
   - 5.4 Typography Best Practices

6. [Imagery Guidelines](#6-imagery-guidelines)
   - 6.1 Photography Style
   - 6.2 Food Photography
   - 6.3 People & Ambiance
   - 6.4 Image Treatments

7. [Application Standards](#7-application-standards)
   - 7.1 Print Materials
   - 7.2 Digital Applications
   - 7.3 Environmental Graphics

8. [Quality Assurance](#8-quality-assurance)
   - 8.1 Brand Compliance Checklist
   - 8.2 Common Violations
   - 8.3 Approval Workflow

9. [Appendix](#9-appendix)
   - 9.1 File Formats
   - 9.2 Asset Organization
   - 9.3 Contact Information

---

## 1. Introduction

### 1.1 Brand Story

{config.brand_identity.name} represents {config.brand_identity.promise}. Our brand embodies {config.cuisine_type} culinary tradition with a focus on {", ".join(config.brand_identity.personality[:3])}.

### 1.2 Brand Values

Our brand is built on these core values:

"""

        for trait in config.brand_identity.personality:
            doc += f"- **{trait}**: Reflected in our visual identity through thoughtful design choices\n"

        doc += f"""

### 1.3 How to Use This Guide

This guide ensures consistent application of the {config.brand_identity.name} brand across all touchpoints. All materials representing the brand must follow these guidelines. For questions or exceptions, contact the brand manager.

**Required for**:
- All marketing materials
- Menu designs and printed collateral
- Digital presence (website, social media)
- Physical environment (signage, interiors)
- Uniforms and merchandise

---

## 2. Brand Identity

### 2.1 Brand Essence

- **Brand Name**: {config.brand_identity.name}
"""

        if config.brand_identity.tagline:
            doc += f"- **Tagline**: {config.brand_identity.tagline}\n"

        doc += f"""- **Brand Promise**: {config.brand_identity.promise}
- **Competitive Positioning**: {config.brand_identity.positioning}

### 2.2 Brand Personality

{config.brand_identity.name} is:

"""

        for trait in config.brand_identity.personality:
            doc += f"- **{trait}**\n"

        doc += f"""

These personality traits guide all visual and verbal communication decisions.

### 2.3 Target Audience

{config.brand_identity.target_audience}

---

## 3. Logo System

### 3.1 Primary Logo

The primary logo is our most important brand asset. It should be used prominently on all major brand materials.

**Logo Construction**:
- Carefully balanced proportions
- Clear, readable at all sizes
- Distinctive and memorable

### 3.2 Logo Variations

#### Horizontal Lockup
**Usage**: Wide formats (website headers, storefront signs, banners)
**Minimum Width**: 100px (digital), 30mm (print)

#### Vertical Lockup
**Usage**: Tall formats (menus, posters, packaging)
**Minimum Height**: 100px (digital), 30mm (print)

#### Icon Only
**Usage**: Social media profiles, app icons, favicons, small applications
**Minimum Size**: 50px × 50px (digital), 15mm × 15mm (print)

#### Monochrome Versions
**Usage**: Single-color printing, embossing, engraving, stamps
**Available**: Black, white

### 3.3 Logo Usage Rules

#### Clear Space
The logo must have adequate clear space on all sides to maintain visibility and impact.

**Clear Space Rule**: Use the X-height method
- Measure the height of the logo's main element (X)
- Apply X-height space on all four sides
- Never place text, images, or other elements within this zone

#### Minimum Sizes

**Print**:
- Horizontal: 30mm width minimum
- Vertical: 30mm height minimum
- Icon: 15mm × 15mm minimum

**Digital**:
- Horizontal: 100px width minimum
- Vertical: 100px height minimum
- Icon: 50px × 50px minimum
- Social media profile: 400px × 400px recommended

#### Approved Backgrounds

✅ **Do Use On**:
- White or light neutral backgrounds
- Brand primary color (with reversed/white logo)
- Photography with semi-transparent panel (80-90% opacity)
- Subtle patterns that don't compete visually

❌ **Don't Use On**:
- Busy photographs without protective panel
- Clashing colors
- Low-contrast backgrounds
- Gradients that reduce readability

### 3.4 Logo Don'ts

**Never**:

❌ **Don't stretch or distort** - Maintain original aspect ratio always
❌ **Don't change colors** - Use only approved color variations
❌ **Don't add effects** - No shadows, glows, outlines, bevels
❌ **Don't outline** - Logo has been designed with proper weights
❌ **Don't rotate** - Keep logo horizontal or vertical
❌ **Don't place on busy backgrounds** - Use protective panel if necessary
❌ **Don't use low-resolution files** - Always use vector or high-res raster
❌ **Don't recreate or modify** - Use provided logo files only

---

## 4. Color Palette

### 4.1 Primary Colors

"""

        # Primary Colors
        for color in config.primary_colors:
            doc += f"""
#### {color.name}

**Specifications**:
- **Hex**: `{color.hex}`
- **RGB**: {color.rgb}
- **CMYK**: {color.cmyk}
"""
            if color.pantone:
                doc += f"- **Pantone**: {color.pantone}\n"

            doc += f"""
**Usage**: {color.usage}
**Percentage in Layouts**: {color.percentage}

"""

        doc += "\n### 4.2 Secondary Colors\n\n"

        # Secondary Colors
        for color in config.secondary_colors:
            doc += f"""
#### {color.name}

**Specifications**:
- **Hex**: `{color.hex}`
- **RGB**: {color.rgb}
- **CMYK**: {color.cmyk}

**Usage**: {color.usage}

"""

        doc += "\n### 4.3 Neutral Colors\n\n"

        # Neutral Colors
        for color in config.neutral_colors:
            doc += f"""
#### {color.name}

- **Hex**: `{color.hex}`
- **RGB**: {color.rgb}
- **CMYK**: {color.cmyk}
- **Usage**: {color.usage}

"""

        doc += """
### 4.4 Color Usage Guidelines

**Hierarchy**:
1. **Primary colors** for main brand elements and calls-to-action (30-40% of layout)
2. **Secondary colors** for supporting information and variety (15-20% of layout)
3. **Neutral colors** for text, backgrounds, and subtle elements (40-50% of layout)

**Print vs. Digital**:
- Always use **CMYK** for print production
- Use **RGB/Hex** for all digital applications
- Request **Pantone** matching for brand-critical print items (business cards, signage)

**Color Combinations**:
- Primary + Neutral: High impact, clear communication
- Primary + Secondary: Balanced, visually rich
- Secondary + Neutral: Sophisticated, understated

### 4.5 Accessibility Standards

All color combinations must meet WCAG 2.1 accessibility standards:

- **Normal text** (< 18pt): Minimum 4.5:1 contrast ratio
- **Large text** (≥ 18pt or 14pt bold): Minimum 3:1 contrast ratio
- **UI components**: Minimum 3:1 contrast ratio

**Approved Text Combinations**:
✅ Dark text on light backgrounds
✅ Light text on dark backgrounds
✅ Brand colors on neutral backgrounds (verify contrast)

**Test all color combinations** before finalizing designs.

---

## 5. Typography

### 5.1 Primary Typeface

**Font Family**: {config.primary_typeface.font_family}
"""

        if config.primary_typeface.designer:
            doc += f"**Designed By**: {config.primary_typeface.designer}\n"

        doc += f"""**License**: {config.primary_typeface.license}

#### Weights Available

"""

        for weight in config.primary_typeface.weights:
            doc += f"- {weight}\n"

        doc += f"""

**Usage**: Headlines, major branding, menu categories, impactful statements

### 5.2 Secondary Typeface

**Font Family**: {config.secondary_typeface.font_family}
**License**: {config.secondary_typeface.license}

#### Weights Available

"""

        for weight in config.secondary_typeface.weights:
            doc += f"- {weight}\n"

        doc += """

**Usage**: Body copy, descriptions, long-form content, supporting text

### 5.3 Type Hierarchy

"""

        # Type Hierarchy
        for level in config.type_hierarchy:
            doc += f"""
#### {level.level}

- **Font**: {level.font}
- **Weight**: {level.weight}
- **Size**: {level.size_print} (print), {level.size_digital} (digital)
- **Usage**: {level.usage}
- **Example**: "{level.example}"

"""

        doc += """
### 5.4 Typography Best Practices

**Readability**:
- Minimum body text size: 10pt (print), 16px (digital)
- Line length: 50-75 characters optimal
- Line height: 1.4-1.6 for body text
- Letter spacing: Use default (optical) for most applications

**Hierarchy**:
- Use size, weight, and color to establish clear hierarchy
- Maintain consistent vertical rhythm
- Limit to 3-4 different text styles per layout

**Do's**:
✅ Use approved fonts only
✅ Maintain consistent sizes across materials
✅ Ensure sufficient contrast for readability
✅ Test readability at actual size

**Don'ts**:
❌ Don't stretch or condense type
❌ Don't use too many weights in one piece
❌ Don't use all caps for long passages
❌ Don't use decorative fonts for functional text

---

## 6. Imagery Guidelines

### 6.1 Photography Style

**Overall Aesthetic**: {config.photography_style}

**Lighting**:
- Natural light preferred for food photography
- Soft, diffused lighting (avoid harsh shadows)
- Consistent color temperature (warm, ~3500K-4500K for {config.cuisine_type})

**Composition**:
- Rule of thirds
- Overhead shots for sharing dishes
- 45-degree angle for individual plates
- Include context (utensils, ingredients, table setting)

**Color Grading**:
- Warm tones emphasized (+10-15% saturation)
- Subtle vignette for focus
- Consistent filter across all images
- True-to-life food colors (avoid over-saturation)

### 6.2 Food Photography

**Must-Haves**:
✅ High resolution (300 DPI minimum for print, 150 DPI for digital)
✅ Well-plated, garnished appropriately
✅ Fresh, appetizing appearance
✅ Good focus on hero dish
✅ Steam or freshness indicators (when appropriate)

**Avoid**:
❌ Flash photography (harsh shadows)
❌ Wilted garnishes or dried-out food
❌ Cluttered backgrounds
❌ Inconsistent plate styles
❌ Unappetizing colors (grayish, dull)

### 6.3 People & Ambiance

**Staff Photography**:
- Smiling, approachable expressions
- Clean, well-fitted uniforms
- Natural poses (working, interacting)
- Diverse representation

**Customer Photography**:
- Genuine moments (not overly posed)
- Enjoying food and atmosphere
- Family/friends/groups sharing
- Obtain necessary model releases

**Interior/Ambiance**:
- Well-lit, clean spaces
- Show brand elements (logo, colors, design)
- Capture atmosphere (busy/cozy/elegant)
- Highlight unique architectural features

### 6.4 Image Treatments

**Approved Treatments**:
- Subtle warm filter (consistent with brand palette)
- Soft vignette for depth (10-15% opacity)
- Gentle overlay of brand colors (15-20% opacity maximum)

**Prohibited**:
❌ Heavy filters or Instagram-style effects
❌ Black and white (except specific campaigns with approval)
❌ Distortion or skewing
❌ Low-quality stock photos or clipart

---

## 7. Application Standards

### 7.1 Print Materials

**Business Cards**:
- Size: 90mm × 54mm (standard) or 88mm × 55mm (US)
- Resolution: 300 DPI
- Bleed: 3mm
- Format: PDF (CMYK, outlined fonts)

**Menus**:
- Sizes: A4 (210mm × 297mm), US Letter (8.5" × 11"), or custom
- Resolution: 300 DPI
- Material recommendations: Laminated, matte finish for durability
- Update frequency: Quarterly or as needed

**Packaging**:
- Consistent brand colors and logo
- Clear product identification
- Food-safe materials and inks
- Functional design (easy to open, stackable)

**Signage**:
- High contrast for visibility
- Weather-resistant materials for outdoor
- Illuminated options where appropriate
- Comply with local regulations

### 7.2 Digital Applications

**Website**:
- Responsive design (mobile-first)
- Brand colors in UI elements
- Typography hierarchy maintained
- High-quality imagery (optimized for web)

**Social Media**:
- Profile images: Logo icon, 400px × 400px
- Cover/banner: Follow platform specifications
- Post templates: Consistent brand elements
- Stories/reels: Vertical format optimization

**Email**:
- Header: Logo + brand colors
- Body: Secondary typeface, readable sizes
- Footer: Contact info, social links
- Mobile-responsive layout

### 7.3 Environmental Graphics

**Exterior Signage**:
- Prominently display logo
- High visibility from street
- Illuminated for night visibility
- Weather-resistant materials

**Interior Design**:
- Brand colors in accents (walls, furniture)
- Typography on menu boards
- Imagery guidelines for wall art
- Cohesive brand experience

**Uniforms**:
- Logo embroidered (preferred) or printed
- Brand colors incorporated
- Professional, comfortable, durable
- Consistent across all staff

---

## 8. Quality Assurance

### 8.1 Brand Compliance Checklist

Before approving any material, verify:

✅ **Logo**:
- [ ] Correct logo variation used
- [ ] Adequate clear space maintained
- [ ] Minimum size requirements met
- [ ] Logo not distorted or modified

✅ **Colors**:
- [ ] Brand colors used correctly (Hex/RGB/CMYK values)
- [ ] Sufficient contrast for readability
- [ ] Appropriate color mode for medium (CMYK/RGB)
- [ ] Accessibility standards met

✅ **Typography**:
- [ ] Approved fonts used only
- [ ] Type hierarchy followed
- [ ] Sizes within specified ranges
- [ ] No unauthorized modifications

✅ **Imagery**:
- [ ] Matches photography style guidelines
- [ ] High-resolution (300 DPI for print, optimized for digital)
- [ ] Approved treatments applied
- [ ] Necessary usage rights secured

✅ **Overall**:
- [ ] Aligns with brand personality
- [ ] Appropriate for target audience
- [ ] Consistent with other brand materials
- [ ] Meets technical specifications

### 8.2 Common Violations

❌ **Frequent Mistakes**:
1. Using low-resolution or pixelated logos
2. Changing brand colors arbitrarily
3. Using unauthorized fonts or font substitutions
4. Stretching or distorting logos
5. Poor color contrasts (inaccessibility)
6. Inconsistent photography styles
7. Mixing old and new brand elements
8. Ignoring clear space requirements

**Corrective Actions**:
- Educate team on brand guidelines
- Provide easy access to approved assets
- Implement approval workflows
- Conduct regular brand audits

### 8.3 Approval Workflow

**For Major Materials** (print runs > 500, permanent signage, core marketing):
1. Designer creates following guidelines
2. Internal review by brand manager
3. Revisions if needed
4. Final approval
5. Production

**For Minor Materials** (social posts, email, temporary signage):
1. Designer creates following guidelines
2. Self-check against compliance checklist
3. Proceed if compliant
4. Periodic audits to ensure quality

---

## 9. Appendix

### 9.1 File Formats

**Logo Files**:
- Vector: AI, EPS, SVG (for scaling)
- Raster: PNG (transparent), JPG (with background)
- Resolution: 300 DPI minimum for raster

**Print Production**:
- PDF (CMYK, outlined fonts, embedded images)
- Bleed: 3-5mm
- Crop marks included

**Digital**:
- PNG (transparent backgrounds)
- JPG (photographs, backgrounds)
- SVG (logos, icons for web)

### 9.2 Asset Organization

All brand assets organized in:

```
brand-assets/
├── logos/
│   ├── primary/
│   ├── variations/
│   └── usage-examples/
├── colors/
│   ├── color-swatches.ase
│   └── color-palette.pdf
├── typography/
│   ├── fonts/
│   └── font-licenses.pdf
├── imagery/
│   ├── photography-guidelines.pdf
│   └── approved-photography/
└── templates/
    ├── business-card/
    ├── menu/
    ├── poster/
    └── social-media/
```

### 9.3 Contact Information

**Brand Manager**: [Name]
**Email**: [Email]
**Phone**: [Phone]

**For Brand Questions**:
- Logo usage queries
- Color or typography clarifications
- New material approvals
- Brand guideline exceptions

**Asset Requests**:
Contact brand manager for access to:
- High-resolution logo files
- Font files and licenses
- Photography library
- Design templates

---

**Document Version**: {config.version}
**Last Updated**: {datetime.now().strftime("%Y-%m-%d")}
**Next Review**: {(datetime.now().replace(year=datetime.now().year + 1)).strftime("%Y-%m-%d")}

---

*These guidelines ensure consistent, professional, and recognizable brand expression across all touchpoints. Strong brand consistency builds trust, recognition, and long-term brand value.*
"""

        return doc

    def generate_quick_reference(self, config: VIConfig) -> str:
        """Generate quick reference sheet"""

        quick_ref = f"""# {config.brand_identity.name} - Quick Reference

## Logo
- **Clear Space**: X-height on all sides
- **Min Size (Print)**: 30mm width
- **Min Size (Digital)**: 100px width

## Primary Colors
"""

        for color in config.primary_colors[:2]:  # Top 2 primary colors
            quick_ref += f"- **{color.name}**: {color.hex} (RGB: {color.rgb})\n"

        quick_ref += f"""

## Typography
- **Headlines**: {config.primary_typeface.font_family}
- **Body**: {config.secondary_typeface.font_family}
- **Min Body Size**: 10pt (print), 16px (digital)

## Photography
{config.photography_style}

## Key Personality Traits
{", ".join(config.brand_identity.personality)}

## Contact
Brand Manager: [Contact Info]
"""

        return quick_ref


# ============================================
# High-Level API
# ============================================

def generate_vi_document(
    restaurant_name: str,
    cuisine_type: str = "chinese",
    tagline: Optional[str] = None,
    brand_promise: str = "",
    custom_colors: Optional[Dict] = None,
    project_name: str = "品牌VI系统"
) -> Dict:
    """
    Generate complete VI document for a restaurant brand

    Args:
        restaurant_name: Name of the restaurant
        cuisine_type: Type of cuisine (chinese, japanese, italian, french, hotpot, cafe)
        tagline: Brand tagline (optional)
        brand_promise: What the brand stands for
        custom_colors: Custom color specifications (optional, overrides template)
        project_name: Project name for output path

    Returns:
        Result dictionary with paths and metadata
    """

    # Load cuisine template
    if cuisine_type not in CUISINE_TEMPLATES:
        raise ValueError(f"Unsupported cuisine type: {cuisine_type}. Choose from: {list(CUISINE_TEMPLATES.keys())}")

    template = CUISINE_TEMPLATES[cuisine_type]

    # Build brand identity
    brand_identity = BrandIdentity(
        name=restaurant_name,
        tagline=tagline,
        promise=brand_promise or f"Excellence in {cuisine_type} cuisine and hospitality",
        personality=template["personality"],
        target_audience=f"Food enthusiasts seeking authentic {cuisine_type} dining experiences",
        positioning=f"Premium {cuisine_type} restaurant combining tradition with modern appeal"
    )

    # Use custom colors or template colors
    if custom_colors:
        # Allow user to override colors
        primary_colors = custom_colors.get("primary", template["colors"]["primary"])
        secondary_colors = custom_colors.get("secondary", template["colors"]["secondary"])
        neutral_colors = custom_colors.get("neutral", template["colors"]["neutral"])
    else:
        primary_colors = template["colors"]["primary"]
        secondary_colors = template["colors"]["secondary"]
        neutral_colors = template["colors"]["neutral"]

    # Typography (standard for restaurant industry)
    primary_typeface = TypefaceSpec(
        font_family="Noto Serif SC" if cuisine_type in ["chinese", "japanese"] else "Playfair Display",
        weights=["Light (300)", "Regular (400)", "Medium (500)", "Bold (700)", "Black (900)"],
        designer="Google Fonts" if "Noto" in ("Noto Serif SC" if cuisine_type in ["chinese", "japanese"] else "Playfair Display") else "Claus Eggers Sørensen",
        license="Open Font License"
    )

    secondary_typeface = TypefaceSpec(
        font_family="Noto Sans SC" if cuisine_type in ["chinese", "japanese"] else "Open Sans",
        weights=["Light (300)", "Regular (400)", "SemiBold (600)", "Bold (700)"],
        designer="Google Fonts",
        license="Open Font License"
    )

    # Type hierarchy
    type_hierarchy = [
        TypeLevel(
            level="Hero Headline",
            font=f"{primary_typeface.font_family} Bold",
            weight="Bold (700)",
            size_print="72pt",
            size_digital="48px",
            usage="Posters, major announcements, grand statements",
            example="Grand Opening"
        ),
        TypeLevel(
            level="Major Headline",
            font=f"{primary_typeface.font_family} Bold",
            weight="Bold (700)",
            size_print="48pt",
            size_digital="32px",
            usage="Menu categories, section headers, event titles",
            example="Appetizers"
        ),
        TypeLevel(
            level="Subheading",
            font=f"{primary_typeface.font_family} Medium",
            weight="Medium (500)",
            size_print="24pt",
            size_digital="20px",
            usage="Dish names, subsections, highlights",
            example="Kung Pao Chicken"
        ),
        TypeLevel(
            level="Body Text",
            font=f"{secondary_typeface.font_family} Regular",
            weight="Regular (400)",
            size_print="12pt",
            size_digital="16px",
            usage="Descriptions, long-form copy, menu details",
            example="Wok-fried chicken with peanuts and chili peppers"
        ),
        TypeLevel(
            level="Caption",
            font=f"{secondary_typeface.font_family} Regular",
            weight="Regular (400)",
            size_print="10pt",
            size_digital="14px",
            usage="Prices, footnotes, nutritional info, fine print",
            example="$18.99"
        )
    ]

    # Build complete config
    config = VIConfig(
        brand_identity=brand_identity,
        primary_colors=primary_colors,
        secondary_colors=secondary_colors,
        neutral_colors=neutral_colors,
        primary_typeface=primary_typeface,
        secondary_typeface=secondary_typeface,
        type_hierarchy=type_hierarchy,
        cuisine_type=cuisine_type,
        photography_style=template["photography"],
        version="1.0"
    )

    # Generate documents
    generator = VIDocumentGenerator()
    vi_document = generator.generate_complete_vi_document(config)
    quick_reference = generator.generate_quick_reference(config)

    # Set output directory
    output_dir = Path("output") / project_name / "X4-平面设计师" / "brand-guidelines"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save VI document
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    vi_doc_filename = f"{restaurant_name.replace(' ', '-')}_brand-guidelines_v1.0_{timestamp}.md"
    vi_doc_path = output_dir / vi_doc_filename
    vi_doc_path.write_text(vi_document, encoding="utf-8")

    # Save quick reference
    quick_ref_filename = f"{restaurant_name.replace(' ', '-')}_quick-reference_{timestamp}.md"
    quick_ref_path = output_dir / quick_ref_filename
    quick_ref_path.write_text(quick_reference, encoding="utf-8")

    # Build metadata
    metadata = {
        "restaurant_name": restaurant_name,
        "cuisine_type": cuisine_type,
        "tagline": tagline,
        "brand_promise": brand_promise,
        "version": "1.0",
        "timestamp": datetime.now().isoformat(),
        "vi_document_path": str(vi_doc_path),
        "quick_reference_path": str(quick_ref_path),
        "color_palette": {
            "primary": [{"name": c.name, "hex": c.hex} for c in primary_colors],
            "secondary": [{"name": c.name, "hex": c.hex} for c in secondary_colors],
            "neutral": [{"name": c.name, "hex": c.hex} for c in neutral_colors]
        },
        "typography": {
            "primary": primary_typeface.font_family,
            "secondary": secondary_typeface.font_family
        }
    }

    # Save metadata
    metadata_filename = f"{restaurant_name.replace(' ', '-')}_vi-metadata_{timestamp}.json"
    metadata_path = output_dir / metadata_filename
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✅ VI Document generated: {vi_doc_path}")
    print(f"📋 Quick Reference: {quick_ref_path}")
    print(f"📊 Metadata saved: {metadata_path}")
    print(f"\n{'='*60}")
    print("📢 VI DOCUMENT READY:")
    print("="*60)
    print(f"\nComplete brand visual identity guidelines generated for {restaurant_name}.")
    print(f"\nThe VI document includes:")
    print(f"  - Complete brand identity system")
    print(f"  - Logo usage guidelines and restrictions")
    print(f"  - Full color palette with Hex/RGB/CMYK/Pantone specs")
    print(f"  - Typography hierarchy and usage standards")
    print(f"  - Photography guidelines")
    print(f"  - Application standards (print, digital, environmental)")
    print(f"  - Quality assurance checklist")
    print(f"\nOutput location: {output_dir}/")
    print(f"\nNext steps:")
    print(f"  1. Review the VI document: {vi_doc_path.name}")
    print(f"  2. Use quick reference for day-to-day design: {quick_ref_path.name}")
    print(f"  3. Share with design team and stakeholders")
    print(f"  4. Create logo files and asset library based on specifications")
    print(f"  5. Begin applying guidelines to all brand materials")
    print(f"\n{'='*60}\n")

    return {
        "success": True,
        "vi_document_path": str(vi_doc_path),
        "quick_reference_path": str(quick_ref_path),
        "metadata_path": str(metadata_path),
        "output_dir": str(output_dir),
        "metadata": metadata,
        "message": "VI document generated successfully"
    }


def list_cuisine_types() -> Dict[str, str]:
    """List all available cuisine types and their descriptions"""
    return {
        "chinese": "Traditional Chinese restaurant with red and gold palette",
        "japanese": "Zen-inspired Japanese restaurant with minimalist aesthetic",
        "italian": "Rustic Italian trattoria with warm, inviting colors",
        "french": "Elegant French bistro with sophisticated palette",
        "hotpot": "Energetic hotpot restaurant with bold, fiery colors",
        "cafe": "Cozy coffee shop with warm, earthy tones"
    }


# ============================================
# CLI Interface
# ============================================

def main():
    """Command-line interface"""
    import argparse

    parser = argparse.ArgumentParser(description="VI Document Generator for Restaurant Brands")
    parser.add_argument("restaurant_name", help="Name of the restaurant")
    parser.add_argument("--cuisine", default="chinese",
                       choices=list(CUISINE_TEMPLATES.keys()),
                       help="Cuisine type (default: chinese)")
    parser.add_argument("--tagline", help="Brand tagline (optional)")
    parser.add_argument("--promise", help="Brand promise statement")
    parser.add_argument("--project", default="品牌VI系统", help="Project name")
    parser.add_argument("--list-cuisines", action="store_true",
                       help="List available cuisine types")

    args = parser.parse_args()

    if args.list_cuisines:
        print("\nAvailable Cuisine Types:")
        print("="*60)
        for cuisine, description in list_cuisine_types().items():
            print(f"  {cuisine:15s} - {description}")
        print("="*60)
        return

    result = generate_vi_document(
        restaurant_name=args.restaurant_name,
        cuisine_type=args.cuisine,
        tagline=args.tagline,
        brand_promise=args.promise,
        project_name=args.project
    )

    if result["success"]:
        print(f"\n✨ VI Document generated successfully!")
        print(f"📁 VI Document: {result['vi_document_path']}")
        print(f"📋 Quick Reference: {result['quick_reference_path']}")
        print(f"📊 Metadata: {result['metadata_path']}")
    else:
        print(f"\n❌ VI generation failed: {result.get('error')}")


if __name__ == "__main__":
    main()
