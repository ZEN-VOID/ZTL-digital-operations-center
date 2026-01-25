# Changelog

All notable changes to the Construction Team Plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features
- Add slash commands for common workflows
- Integrate AutoCAD MCP server for direct .dwg editing
- Add Revit MCP server for BIM model manipulation
- Create skills for automated clash detection
- Add hooks for quality assurance checkpoints
- Develop template library for common restaurant types

---

## [1.0.0] - 2025-10-28

### Added
- **Initial Release** of Construction Team Plugin
- **Z0 Agent**: Construction Requirement Analyst
  - Site selection and property evaluation
  - Functional requirement gathering
  - Space planning methodology
  - Technical roadmap design
  - Budget and timeline planning
  - Project initiation documentation
- **Z1 Agent**: Floor Plan Designer
  - CAD measurement and surveying capabilities
  - Floor plan drafting standards
  - Functional zoning layouts
  - Furniture arrangement planning
  - Technical drawing specifications
- **Z2 Agent**: Space Designer
  - Interior design conceptualization
  - Brand identity integration
  - Material and color specification
  - Lighting and atmosphere design
  - Design documentation and presentations
- **Z3 Agent**: BIM Modeler
  - Building Information Modeling workflows
  - Construction document generation
  - Clash detection and resolution
  - Material quantity takeoffs
  - MEP system coordination
- **Z4 Agent**: Architectural Animator
  - Photorealistic rendering capabilities
  - Architectural walkthrough animations
  - Marketing materials creation
  - VR/AR experience development
  - Presentation animation workflows
- **ZZ Agent**: Construction Team Leader
  - Project orchestration and coordination
  - Multi-agent task scheduling
  - Quality control and review processes
  - Budget and timeline management
  - Stakeholder communication protocols
- **Plugin Infrastructure**:
  - Standard plugin.json manifest
  - Empty commands directory with README
  - Empty skills directory with README
  - Empty hooks configuration (hooks.json)
  - Empty MCP servers configuration (.mcp.json)
  - Comprehensive README documentation
  - MIT License
  - This CHANGELOG

### Documentation
- Complete README with installation instructions
- Usage examples for common workflows
- Agent capability descriptions
- Output structure specifications
- Best practices guide
- Project structure documentation

### Configuration
- Standard plugin manifest (plugin.json)
- Six specialized agents in agents/ directory
- Placeholder directories for future expansion
- Output path standards: `output/筹建组/[agent]/[project]-[date]/`

---

## Version History Summary

| Version | Date | Description |
|---------|------|-------------|
| 1.0.0 | 2025-10-28 | Initial release with 6 agents |

---

## Migration Guide

### From Individual Agents to Plugin

If you were previously using individual agent files from `.claude/configs/筹建组/`:

1. **No Action Required**: The plugin preserves all original agent functionality
2. **Benefits**:
   - Centralized configuration via plugin.json
   - Easier distribution and updates
   - Consistent agent versioning
   - Standardized output paths
   - Future extensibility with commands/skills/hooks

3. **Enable Plugin**:
   ```json
   // .claude/settings.json
   {
     "enabledPlugins": ["construction-team"]
   }
   ```

4. **Restart Claude Code** (complete exit and restart)

### Future Upgrade Path

- **1.x.x releases**: Backward-compatible additions (new commands, skills)
- **2.x.x releases**: May include breaking changes to agent interfaces
- Always review CHANGELOG before upgrading

---

## Contributing

Contributions are welcome! For major changes:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Update CHANGELOG.md under [Unreleased]
5. Submit a pull request

For bug fixes:
1. Report via GitHub Issues
2. Include steps to reproduce
3. Specify Claude Code version and model

---

**Maintained by**: ZTL Digital Intelligence Operations Center
**Plugin Repository**: [github.com/ztl-digital/construction-team-plugin](https://github.com/ztl-digital/construction-team-plugin)
**License**: MIT
