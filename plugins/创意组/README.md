# 创意组 Plugin

> Professional creative production plugin for Claude Code with restaurant industry specialization

## Overview

Comprehensive creative content production plugin featuring advertising strategy, copywriting, graphic design, photography, and video production. Includes **9 specialized agents** and **7 professional skills** tailored for restaurant branding and marketing.

### Core Capabilities

**Agent Expertise**:
- X0: Creative Content Analyst
- X1: Advertising Strategist
- X2: Copywriter
- X3: Graphic Designer & Layout Specialist (integrated design + typesetting)
- X5: Short Video Scriptwriter
- X6: Photographer
- X7: Video Editor
- XX: Creative Team Director

**Specialized Skills**:
- 5 Restaurant Design Skills (algorithmic art, canvas design, brand guidelines, theme factory, artifacts builder)
- Figma Integration (file management, design system, image export)
- Social Platform Content Library

## Features

### 🤖 Specialized Agents (9 Total)

This plugin includes **9 specialized agents** covering all aspects of creative operations:

| Agent | Role | Key Capabilities |
|-------|------|------------------|
| **X0** | 创意内容分析师 | Creative brief analysis, requirement clarification |
| **X1** | 广告策划师 | Advertising strategy, campaign planning, creative briefs |
| **X2** | 文案撰稿人 | Copywriting, storytelling, multi-platform content |
| **X3** | 平面设计与排版师 | **Integrated design + layout** (logo, VI, posters, menus, H5 pages) |
| **X5** | 短视频脚本创作师 | Short video scripts, storyboards, platform optimization |
| **X6** | 摄影师 | Photography art direction, food photography, brand imagery |
| **X7** | 剪辑师 | Video editing, post-production, motion graphics |
| **XX** | 创意总监 | Creative direction, quality control, team coordination |

**⭐ X3 Enhanced**: Now combines graphic design expertise with professional layout skills, providing end-to-end design solutions from brand identity to final production files.

See `agents/` directory for complete agent documentation.

### 🎨 Restaurant Design Skills (5 Specialized Skills)

**NEW**: X3-平面设计与排版师 now has access to 5 专属餐饮设计技能包:

#### 1. `algorithmic-art-restaurant`
Generate unique, reproducible patterns using p5.js for restaurant branding.

**Use Cases**:
- Menu background textures and patterns
- Packaging design elements
- Brand visual identity patterns
- Store decoration graphics

**Key Features**:
- Flow fields, particle systems, geometric patterns
- Seeded randomness for reproducibility
- Cuisine-specific themes (Chinese, Japanese, Italian, etc.)
- 300 DPI print-ready output

#### 2. `canvas-design-restaurant`
Create visual art following professional design philosophy for restaurant materials.

**Use Cases**:
- Promotional posters and marketing materials
- Menu covers and packaging designs
- Digital marketing graphics (social media, web)
- Brand experience materials

**Key Features**:
- Design philosophy principles (hierarchy, balance, color theory)
- Cuisine-specific color palettes
- Typography pairings and systems
- Multi-format output (PDF, PNG)

#### 3. `brand-guidelines-restaurant`
Manage and enforce comprehensive brand visual identity systems.

**Use Cases**:
- Create brand guidelines documents
- Ensure brand consistency across materials
- Logo usage rules and specifications
- Color, typography, and imagery standards

**Key Features**:
- Complete VI system development
- Logo system management
- Color palette specifications (Hex, RGB, CMYK, Pantone)
- Cuisine-specific brand guidelines
- Asset library management

#### 4. `theme-factory-restaurant`
Apply cohesive design themes across all restaurant materials.

**Use Cases**:
- Select from 10 pre-designed cuisine themes
- Generate custom themes on-demand
- Ensure visual consistency across touchpoints
- Themed design systems

**Pre-Designed Themes**:
1. Chinese Imperial (traditional fine dining)
2. Japanese Zen (minimalist aesthetic)
3. Italian Rustico (rustic trattoria)
4. French Elegance (sophisticated bistro)
5. American Classic (retro diner)
6. Hotpot Fiesta (vibrant hotpot)
7. Cafe Moderne (contemporary coffee shop)
8. BBQ Smokehouse (bold BBQ joint)
9. Fine Dining Luxury (upscale elegance)
10. Fast Casual Fresh (healthy, modern)

#### 5. `artifacts-builder-restaurant`
Build interactive HTML artifacts for restaurant digital presence.

**Use Cases**:
- H5 promotional pages (grand opening, campaigns)
- Digital menu interfaces
- Brand experience pages
- Online reservation and ordering forms

**Key Features**:
- React + Tailwind CSS + shadcn/ui
- Mobile-optimized, responsive design
- Interactive components and animations
- Fast loading, accessible

### 🔧 Additional Skills

#### Figma Integration
- **figma/file-management-v2**: Manage Figma projects and files
- **figma/design-system-v2**: Maintain design systems and components
- **figma/image-export-v2**: Export production-ready assets

#### Content Library
- **社交平台文案知识库**: Social media content templates and best practices

## Installation

### Method 1: Project-Level (Recommended)

1. Keep the plugin in your project directory: `plugins/创意组/`

2. The plugin is automatically discovered by Claude Code (no configuration needed)

3. Restart Claude Code (complete exit and restart required)

### Method 2: Global Installation

1. Copy the plugin to your Claude Code plugins directory:
```bash
cp -r "plugins/创意组" ~/.claude/plugins/creative-team
```

2. Enable the plugin in your `~/.claude/settings.json`:
```json
{
  "enabledPlugins": ["creative-team"]
}
```

3. Restart Claude Code

## Usage

### Agent Invocation

Agents can be invoked in two ways:

1. **Automatic Delegation**: Claude automatically selects the appropriate agent based on your request
   ```
   User: "设计一张火锅店的开业海报"
   → Claude delegates to X3-平面设计与排版师
   ```

2. **Explicit Invocation**: Use the Task tool to explicitly call a specific agent
   ```python
   Task(subagent_type="X3-平面设计与排版师",
        prompt="设计一套火锅店的品牌视觉系统")
   ```

### Skills Integration

X3-平面设计与排版师 automatically leverages specialized skills as needed:

**Example Workflow**:
```
User: "Create a Chinese restaurant poster with branded patterns"

X3 Workflow:
1. Uses theme-factory-restaurant → Selects "Chinese Imperial" theme
2. Uses algorithmic-art-restaurant → Generates branded background pattern
3. Uses canvas-design-restaurant → Creates poster design
4. Uses brand-guidelines-restaurant → Ensures brand consistency
5. Delivers final print-ready PDF + specifications
```

### Output Structure

All agent outputs follow standardized path convention:

```
output/[项目名]/X3-平面设计与排版师/
├── 01-planning/
│   ├── 设计方案.md
│   └── 参考灵感.md
├── 02-concepts/
│   ├── concept-A/
│   ├── concept-B/
│   └── concept-C/
├── 03-refinements/
├── 04-layouts/
├── 05-finals/
│   ├── print-ready/
│   └── digital-optimized/
└── 06-specs/
    ├── 设计说明.md
    └── production-notes.md
```

**Skill-Specific Outputs**:
- `algorithmic-art/patterns/`: Generated patterns with metadata
- `canvas-design/`: Visual designs (posters, covers, graphics)
- `brand-guidelines/`: Guidelines documents and asset libraries
- `themed-designs/`: Theme-applied designs with specs
- `artifacts/`: HTML artifacts (H5 pages, digital menus)

## Project Structure

```
plugins/创意组/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
│
├── agents/
│   ├── X0-创意内容分析师.md
│   ├── X1-广告策划师.md
│   ├── X2-文案撰稿人.md
│   ├── X3-平面设计与排版师.md    # ⭐ NEW: Integrated design + layout
│   ├── X3-平面设计师.md          # Legacy (deprecated)
│   ├── X4-图文排版师.md          # Legacy (merged into X3)
│   ├── X5-短视频脚本创作师.md
│   ├── X6-摄影师.md
│   ├── X7-剪辑师.md
│   └── XX-创意总监.md
│
├── skills/
│   ├── algorithmic-art-restaurant/      # ⭐ NEW
│   │   └── SKILL.md
│   ├── canvas-design-restaurant/        # ⭐ NEW
│   │   └── SKILL.md
│   ├── brand-guidelines-restaurant/     # ⭐ NEW
│   │   ├── SKILL.md
│   │   └── templates/
│   ├── theme-factory-restaurant/        # ⭐ NEW
│   │   ├── SKILL.md
│   │   └── themes/
│   ├── artifacts-builder-restaurant/    # ⭐ NEW
│   │   ├── SKILL.md
│   │   └── templates/
│   ├── figma/
│   │   ├── file-management-v2/
│   │   ├── design-system-v2/
│   │   └── image-export-v2/
│   └── 社交平台文案知识库/
│
├── commands/
│   └── README.md
│
├── hooks/
│   └── hooks.json
│
├── scripts/                            # Utility scripts
├── .mcp.json                          # MCP servers configuration
├── README.md                          # This file
├── CHANGELOG.md                       # Version history
└── LICENSE                            # MIT License
```

## Extension Points

This plugin can be extended with:

1. **Commands** (commands/*.md) - Slash commands for frequent workflows
2. **Skills** (skills/*/SKILL.md) - Complex automated capabilities
3. **Hooks** (hooks/hooks.json) - Event-driven automation
4. **MCP Servers** (.mcp.json) - External tool integrations

## Design Workflow Example

### Complete Brand Design Project

**User Request**: "为新开的川味火锅店设计一套完整的品牌视觉系统"

**X3-平面设计与排版师 Workflow**:

```
Phase 1: Strategic Foundation
├─ Analyze brief and research
├─ Define brand personality: Bold, Energetic, Communal
├─ Select theme: "Hotpot Fiesta" (vibrant, warm colors)
└─ Plan deliverables: Logo, VI, menu, poster, packaging

Phase 2: Brand Identity Creation
├─ Design logo (primary, variations)
├─ Generate brand guidelines using brand-guidelines-restaurant
│   ├─ Color palette: #FF4500, #DC143C, #FFD700
│   ├─ Typography: Anton (headings), Noto Sans SC (body)
│   └─ Usage rules and specifications
└─ Create VI system materials

Phase 3: Marketing Materials
├─ Poster design using canvas-design-restaurant
│   ├─ Apply "Hotpot Fiesta" theme
│   ├─ Generate background pattern with algorithmic-art-restaurant
│   └─ Export print-ready PDF (300 DPI, CMYK)
│
├─ Menu design (integrated layout)
│   ├─ Category organization
│   ├─ Typography hierarchy
│   ├─ Dish photography guidelines
│   └─ Print and digital versions
│
└─ Packaging design
    ├─ Takeout box pattern
    ├─ Brand consistency check
    └─ Production specifications

Phase 4: Digital Presence
├─ H5 grand opening page using artifacts-builder-restaurant
│   ├─ Hero section with countdown
│   ├─ Opening offers
│   ├─ Location map
│   └─ Social sharing
│
└─ Digital menu interface
    ├─ Category tabs
    ├─ Dish cards with photos
    ├─ Dietary filters
    └─ Mobile-optimized

Phase 5: Delivery
├─ All print-ready files (PDF, CMYK, 300 DPI)
├─ Digital assets (PNG, RGB, optimized)
├─ HTML artifacts (H5 page, digital menu)
├─ Brand guidelines document
├─ Design specifications
└─ Asset library
```

## Quality Standards

All deliverables meet these standards:

### Design Quality
✅ Brand consistency across all materials
✅ Clear visual hierarchy and typography
✅ Appropriate color harmony and contrast
✅ Cultural sensitivity and market appropriateness
✅ Professional composition and balance

### Technical Quality
✅ Print: 300 DPI minimum, CMYK, proper bleeds
✅ Digital: Optimized resolution, RGB, web-safe formats
✅ Files: Proper naming, version control, organized structure
✅ Accessibility: WCAG AA contrast ratios (4.5:1 minimum)

### Production Readiness
✅ Complete specifications documented
✅ Font embedding and licensing
✅ Material recommendations
✅ Vendor production notes

## Requirements

- **Claude Code**: v1.0.124+
- **Model**: Sonnet 4.5 (recommended)
- **Tools**: Task, Read, Write, Edit, Grep, Glob, Bash, WebFetch
- **Skills Dependencies**: None (all skills self-contained)

## Compatibility

**Cuisine Types Supported**:
- Chinese (traditional, Szechuan, Cantonese, hotpot)
- Japanese (sushi, ramen, kaiseki, izakaya)
- Italian (trattoria, pizzeria, fine dining)
- French (bistro, brasserie, patisserie)
- American (diner, BBQ, steakhouse, fast casual)
- Cafe & Coffee Shop
- Fast Casual & Healthy Dining

**Output Formats**:
- Print: PDF (CMYK, 300 DPI), AI, EPS
- Digital: PNG, JPG, SVG (RGB, optimized)
- Web: HTML, CSS, JavaScript (React artifacts)
- Documents: Markdown, DOCX, PDF

## Support

For issues, questions, or contributions:

- **GitHub Issues**: [ZTL-Digital/creative-team-plugin/issues](https://github.com/ZTL-Digital/creative-team-plugin/issues)
- **Documentation**: See individual agent files in `agents/` directory
- **Skills Documentation**: See `skills/[skill-name]/SKILL.md` for each skill
- **Examples**: Check `output/` directory for sample projects

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Version

**Current Version**: 2.0.0 (Major Update)
**Last Updated**: 2025-10-29
**Compatibility**: Claude Code v1.0.124+

### What's New in 2.0

✨ **Major Updates**:
- **X3 Enhancement**: Merged X3 (Graphic Designer) and X4 (Layout Designer) into unified X3-平面设计与排版师
- **5 New Skills**: Added restaurant-specific design skills (algorithmic-art, canvas-design, brand-guidelines, theme-factory, artifacts-builder)
- **Integrated Workflow**: Seamless design + layout workflow from concept to production
- **Theme System**: 10 pre-designed cuisine-specific themes
- **Interactive Artifacts**: HTML/React artifact building capability

🔧 **Improvements**:
- Enhanced output path conventions
- Comprehensive design specifications
- Quality assurance checklists
- Mobile-first design principles
- Brand consistency enforcement

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed version history and updates.

---

**Created by**: ZTL Digital Intelligence Operations Center
**Plugin Type**: Professional Domain Plugin (Creative Team)
**Agent Count**: 9 specialized agents
**Skill Count**: 7 specialized skills (5 new restaurant design skills)
**Status**: Production Ready ⭐ Enhanced
