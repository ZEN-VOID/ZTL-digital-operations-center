# Construction Team Plugin (筹建组插件)

> Comprehensive restaurant construction project management plugin for Claude Code

## Overview

The Construction Team Plugin provides a complete suite of specialized agents for managing restaurant construction projects from initial requirement analysis to final 3D visualization and animation. This plugin integrates six professional agents working in coordinated workflows to deliver high-quality construction documentation.

## Features

### 🤖 Specialized Agents

#### Z0 - Construction Requirement Analyst (筹建项目需求分析师)
- Site selection and property evaluation
- Functional requirement gathering
- Space planning recommendations
- Technical roadmap design
- Budget and timeline planning
- Project initiation documentation

#### Z1 - Floor Plan Designer (平面图设计师)
- CAD measurement and surveying
- Floor plan drafting
- Functional zoning layouts
- Furniture arrangement plans
- Technical drawing standards

#### Z2 - Space Designer (空间设计师)
- Interior design conceptualization
- Brand identity integration
- Material and color specification
- Lighting and atmosphere design
- Design documentation and presentations

#### Z3 - BIM Modeler (BIM建模师)
- Building Information Modeling
- Construction document generation
- Clash detection and resolution
- Material quantity takeoffs
- MEP system coordination

#### Z4 - Architectural Animator (建筑动画师)
- Photorealistic rendering
- Architectural walkthroughs
- Marketing materials creation
- VR/AR experiences
- Presentation animations

#### ZZ - Construction Team Leader (筹建组组长)
- Project orchestration and coordination
- Multi-agent task scheduling
- Quality control and review
- Budget and timeline management
- Stakeholder communication

## Installation

### Method 1: Local Installation

1. Copy the plugin to your Claude Code plugins directory:
```bash
cp -r plugins/筹建组 ~/.claude/plugins/construction-team
```

2. Enable the plugin in your `.claude/settings.json`:
```json
{
  "enabledPlugins": ["construction-team"]
}
```

3. Restart Claude Code (complete exit and restart required)

### Method 2: Project-Level Installation

1. Keep the plugin in your project directory: `plugins/筹建组/`

2. Add to project-level `.claude/settings.json`:
```json
{
  "enabledPlugins": ["./plugins/筹建组"]
}
```

3. Restart Claude Code

## Usage

### Standard Construction Project Workflow

```yaml
Phase 1 - Requirement Analysis (Week 1):
  ZZ → Z0: Site evaluation and functional requirements
  Output: Project initiation brief, requirement analysis report

Phase 2 - Design Development (Week 2-3):
  ZZ → Z1: CAD floor plans and technical drawings
  ZZ → Z2: Interior design concepts and specifications
  Output: Design proposal package

Phase 3 - Design Documentation (Week 4-5):
  ZZ → Z3: BIM model and construction documents
  Output: Complete construction drawing set, material quantities

Phase 4 - Visualization (Week 6):
  ZZ → Z4: Renderings and animations
  Output: Marketing materials, walkthrough animations

Phase 5 - Construction Support (Week 7-12):
  ZZ: Ongoing technical support and coordination
  Output: As-built drawings, project closeout documentation
```

### Example Use Cases

**New Restaurant Opening**:
```
User: "I need to design a 300㎡ hotpot restaurant"
→ ZZ orchestrates: Z0 (requirements) → Z1 (floor plan) → Z2 (interior design)
  → Z3 (BIM model) → Z4 (animations)
```

**Renovation Project**:
```
User: "Upgrade our existing 250㎡ tea restaurant"
→ ZZ orchestrates: Z0 (current status survey) → Z1 (as-built drawings)
  → Z2 (renovation design) → Z3 (renovation model) → Z4 (before/after comparison)
```

**Marketing Materials**:
```
User: "Create impressive visuals for investor presentation"
→ ZZ orchestrates: Z2 (design highlights) → Z3 (model refinement)
  → Z4 (high-quality renderings and walkthrough)
```

## Agent Capabilities

### Z0 Outputs
- Site Evaluation Report (markdown)
- Functional Requirement List (Excel)
- Space Planning Proposal (PDF)
- Investment Estimate (Excel)
- Technical Roadmap (markdown)
- Project Schedule (Excel)

### Z1 Outputs
- CAD Floor Plans (.dwg)
- Furniture Layout Plans
- Reflected Ceiling Plans
- As-Built Drawings
- Technical Detail Drawings

### Z2 Outputs
- Design Concept Boards (PDF)
- Material Specifications
- Color and Finish Schedules
- Lighting Design Plans
- Design Presentation Decks

### Z3 Outputs
- BIM Models (.rvt, .ifc)
- Construction Drawing Sets (PDF)
- Material Quantity Takeoffs (Excel)
- Clash Detection Reports
- Shop Drawings

### Z4 Outputs
- Photorealistic Renderings (PNG, JPG)
- Walkthrough Animations (MP4)
- 360° Panoramas
- VR Experiences
- Marketing Collateral

## Configuration

### Customizing Agent Behavior

Agent configurations are located in `agents/*.md`. Each agent file contains:
- Agent description and invocation triggers
- System prompt and role definition
- Tool permissions
- Output specifications

### Adding Commands

Create `.md` files in `commands/` directory following the standard format:
```markdown
---
description: Command description
allowed-tools: Tool1, Tool2
---

# Command content
```

### Adding Skills

Create skill directories in `skills/` with `SKILL.md` and supporting resources.

### Configuring Hooks

Edit `hooks/hooks.json` to add event-driven automation.

### Integrating MCP Servers

Edit `.mcp.json` to add external tool integrations.

## Project Structure

```
plugins/筹建组/
├── .claude-plugin/
│   └── plugin.json           # Plugin manifest
├── agents/
│   ├── Z0-筹建项目需求分析师.md
│   ├── Z1-平面图设计师.md
│   ├── Z2-空间设计师.md
│   ├── Z3-BIM建模师.md
│   ├── Z4-建筑动画师.md
│   └── ZZ-筹建组组长.md
├── commands/
│   └── README.md             # Commands placeholder
├── skills/
│   └── README.md             # Skills placeholder
├── hooks/
│   └── hooks.json            # Hooks configuration
├── scripts/                  # Utility scripts
├── .mcp.json                # MCP servers configuration
├── README.md                # This file
├── CHANGELOG.md             # Version history
└── LICENSE                  # MIT License
```

## Output Standards

All agent outputs are saved to structured directories:

```
output/筹建组/
├── Z0-requirement-analysis/[project-name]-[date]/
├── Z1-floor-plans/[project-name]-[date]/
├── Z2-space-design/[project-name]-[date]/
├── Z3-bim-models/[project-name]-[date]/
├── Z4-visualizations/[project-name]-[date]/
└── ZZ-orchestration/[project-name]-[date]/
```

## Best Practices

1. **Always start with Z0**: Proper requirement analysis prevents costly redesigns
2. **Use ZZ for coordination**: Let the team leader orchestrate complex projects
3. **Parallel workflows**: Z1 and Z2 can work simultaneously on independent tasks
4. **Iterative refinement**: Use Z4 renderings to validate Z2/Z3 designs early
5. **Document everything**: Maintain complete project documentation for future reference

## Requirements

- Claude Code v1.0.124+
- Sonnet 4.5 model (recommended)
- Tools: Task, Read, Write, Edit, Grep, Glob, Bash
- Optional: CAD software for .dwg file viewing
- Optional: BIM software (Revit, ArchiCAD) for .rvt/.ifc models

## Support

For issues, questions, or contributions:

- GitHub Issues: [construction-team-plugin/issues](https://github.com/ztl-digital/construction-team-plugin/issues)
- Documentation: See individual agent files in `agents/` directory
- Examples: See `output/` directory for sample project structures

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Version

**Current Version**: 1.0.0
**Last Updated**: 2025-10-28
**Compatibility**: Claude Code v1.0.124+

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

---

**Created by**: ZTL Digital Intelligence Operations Center
**Plugin Type**: Professional Domain Plugin (Restaurant Construction)
**Agent Count**: 6 specialized agents
**Status**: Production Ready
