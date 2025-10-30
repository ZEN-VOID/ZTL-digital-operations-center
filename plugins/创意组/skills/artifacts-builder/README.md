# Artifacts Builder Skill

Create elaborate, multi-component claude.ai HTML artifacts using modern frontend technologies (React, Tailwind CSS, shadcn/ui).

## Overview

The artifacts-builder skill enables Claude to build complex interactive web applications that can be shared as single-file HTML artifacts in claude.ai conversations.

**Use for**: Complex artifacts requiring state management, routing, or shadcn/ui components
**Don't use for**: Simple single-file HTML/JSX artifacts

## Quick Start

### For Claude

```python
from scripts.artifact_builder import ArtifactBuilder

# Initialize
builder = ArtifactBuilder(
    project_name="餐饮网站原型",
    agent_name="X4-平面设计师"
)

# Step 1: Initialize artifact
result = builder.create_artifact(
    artifact_name="hotpot-menu-app",
    description="交互式火锅菜单应用",
    components=["button", "card", "dialog", "tabs"]
)

# Step 2: Develop (edit files in workspace)
# workspace = result["workspace"]

# Step 3: Bundle to single HTML
bundle_result = builder.bundle_artifact("hotpot-menu-app")

print(bundle_result["bundle_file"])
# → output/餐饮网站原型/X4-平面设计师/artifacts-builder/hotpot-menu-app/...html
```

### For Users

Simply ask Claude to create an interactive web application:

```
"帮我创建一个火锅店的交互式菜单应用"
"设计一个餐厅预订系统的原型"
"生成一个展示餐饮数据的仪表板"
```

## Tech Stack

- **React 18** + **TypeScript** (via Vite)
- **Tailwind CSS 3.4.1** with shadcn/ui theming
- **40+ shadcn/ui components** pre-installed
- **Parcel** for bundling to single HTML file
- **Node 18+** compatibility

## Output Structure

```
output/[项目名]/X4-平面设计师/artifacts-builder/[artifact-name]/
├── plans/      # JSON specifications
├── results/    # Final bundle.html files
├── logs/       # Execution logs
├── metadata/   # Traceability metadata
└── workspace/  # Development files (React project)
    └── [artifact-name]/
        ├── src/
        ├── public/
        ├── index.html
        └── package.json
```

## Key Features

- **Single HTML Output**: All JavaScript, CSS bundled into one file
- **40+ shadcn/ui Components**: Pre-installed and ready to use
- **Path Aliases**: `@/` configured for clean imports
- **TypeScript Support**: Full type safety
- **Responsive Design**: Tailwind CSS built-in
- **Modern Stack**: React 18 + Vite + ESBuild

## Design Guidelines

**IMPORTANT**: To avoid "AI slop", avoid:
- ❌ Excessive centered layouts
- ❌ Purple gradients everywhere
- ❌ Uniform rounded corners
- ❌ Inter font (overused)

**Do instead**:
- ✅ Varied layouts and asymmetry
- ✅ Purposeful color choices
- ✅ Mix of sharp and rounded elements
- ✅ Diverse typography

## Workflow

1. **Initialize**: Create React project structure
2. **Develop**: Edit files in workspace (Claude or user)
3. **Bundle**: Package into single HTML file
4. **Share**: Display artifact to user
5. **Test** (optional): Validate functionality

## Available shadcn/ui Components

**Form Controls**: button, checkbox, radio-group, select, switch, slider, input, textarea, label

**Data Display**: card, table, badge, avatar, separator, progress, skeleton

**Feedback**: alert, alert-dialog, dialog, toast, tooltip, popover

**Navigation**: tabs, dropdown-menu, menubar, navigation-menu, breadcrumb, pagination

**Layout**: accordion, collapsible, resizable, scroll-area, sheet, sidebar

**Advanced**: calendar, carousel, chart, command, context-menu, data-table, date-picker, drawer, form, hover-card, input-otp, sonner

## Examples

### Example 1: Restaurant Menu App

```python
builder = ArtifactBuilder("火锅店开业筹备", "X4-平面设计师")

result = builder.create_artifact(
    artifact_name="hotpot-menu",
    description="交互式火锅菜单,包含分类、搜索、购物车",
    components=["card", "tabs", "button", "dialog", "badge", "input"],
    state_management="useState"
)

# Develop: Edit workspace files to build the UI
# Bundle: Create single HTML file
bundle_result = builder.bundle_artifact("hotpot-menu")
```

### Example 2: Data Dashboard

```python
result = builder.create_artifact(
    artifact_name="restaurant-dashboard",
    description="餐厅数据仪表板,展示销售、订单、评价",
    components=["chart", "card", "table", "tabs", "calendar"],
    state_management="useState"
)
```

## Installation

### Shell Scripts
The skill includes two bash scripts:
- `scripts/init-artifact.sh` - Initialize React project
- `scripts/bundle-artifact.sh` - Bundle to single HTML

### Python Engine
Optional Python wrapper for programmatic control:
```bash
pip install pathlib  # Standard library, usually pre-installed
```

## Integration

This skill is designed to work with:
- **X4-平面设计师** agent (primary invoker)
- **algorithmic-art** skill (for generated visuals)
- **theme-factory-restaurant** skill (for theming)

## Architecture

Follows the three-layer architecture:

1. **Layer 1 (Knowledge)**: Development guidelines in SKILL.md
2. **Layer 2 (Configuration)**: JSON specs in `output/**/`
3. **Layer 3 (Execution)**: Shell scripts + Python orchestration

## Best Practices

1. **Use for complex artifacts**: Don't overkill simple needs
2. **Choose appropriate components**: Start with 3-5 components max
3. **Test incrementally**: Bundle often during development
4. **Responsive design**: Always test mobile layouts
5. **Performance**: Minimize unnecessary re-renders

## Troubleshooting

**Node version issues?**
- Requires Node 18+
- Script auto-detects and pins Vite version

**Bundle script fails?**
- Check that `index.html` exists in project root
- Ensure all imports are valid
- Review logs in `output/**/`

**shadcn/ui component missing?**
- All components are pre-installed via `shadcn-components.tar.gz`
- Check `workspace/[artifact]/src/components/ui/`

## Version

- **Version**: 1.0.0
- **Last Updated**: 2025-10-29
- **License**: See LICENSE.txt

## Support

For detailed documentation, see `reference.md`.

---

**Maintained by**: X4-平面设计师 (via Claude Code)
