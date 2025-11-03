# Claude Code Plugins Skill

> Comprehensive guide for creating professional Claude Code plugins with standardized structure

## Overview

This skill provides complete guidance for building production-ready Claude Code plugins that package commands, agents, skills, hooks, and MCP servers into distributable packages.

## What's Included

### Core Documentation

- **SKILL.md**: Complete plugin creation guide
  - Plugin architecture and structure
  - Step-by-step creation process
  - Component integration patterns
  - Testing and packaging workflows
  - Best practices and examples

### Scripts

- **init_plugin.py**: Initialize new plugin with standard structure
- **package_plugin.py**: Validate and package plugin into distributable zip

### References

- **plugin-json-reference.md**: Complete `plugin.json` specification
- **mcp-integration-guide.md**: MCP server integration guide

### Templates

- **plugin.json.template**: Plugin manifest template
- **.mcp.json.template**: MCP servers configuration template
- **hooks.json.template**: Hooks configuration template

## Quick Start

### Create New Plugin

```bash
# Initialize plugin structure
python3 .claude/skills/元skills/plugins/scripts/init_plugin.py \
  --name "my-plugin" \
  --description "My awesome plugin" \
  --author "Your Name" \
  --email "your@email.com" \
  --output "./plugins"

# Navigate to plugin
cd plugins/my-plugin

# Customize components
# - Edit .claude-plugin/plugin.json
# - Add commands in commands/
# - Add agents in agents/
# - Add skills in skills/
# - Configure hooks in hooks/
# - Configure MCP in .mcp.json
```

### Package Plugin

```bash
# Validate and package
python3 .claude/skills/元skills/plugins/scripts/package_plugin.py \
  ./plugins/my-plugin \
  --output ./dist

# This creates: dist/my-plugin-1.0.0.zip
```

### Test Plugin

```bash
# Install locally
unzip dist/my-plugin-1.0.0.zip -d ~/.claude/plugins/

# Add to settings.json
cat >> .claude/settings.json <<EOF
{
  "enabledPlugins": ["my-plugin"]
}
EOF

# Restart Claude Code
# Complete exit and restart required!

# Verify loading
claude --debug
```

## Component Creation

This skill integrates with other meta-skills for component creation:

### Commands

Use the **commands** meta-skill to create slash commands:

```bash
# Reference: .claude/skills/元skills/commands/
# Creates: commands/*.md
```

See: [Commands Meta-Skill](../commands/SKILL.md)

### Agents

Use the **agents** meta-skill to create subagents:

```bash
# Reference: .claude/skills/元skills/agents/
# Creates: agents/*.md
```

See: [Agents Meta-Skill](../agents/SKILL.md)

### Skills

Use the **skill-creator** meta-skill to create skills:

```bash
# Reference: .claude/skills/元skills/skills/
# Creates: skills/*/SKILL.md
```

See: [Skill Creator Meta-Skill](../skills/skill-creator/SKILL.md)

### Hooks

Use the **hooks** meta-skill to create event hooks:

```bash
# Reference: .claude/skills/元skills/hooks/
# Creates: hooks/hooks.json + scripts/
```

See: [Hooks Meta-Skill](../hooks/SKILL.md)

## Plugin Structure

```
my-plugin/
├── .claude-plugin/           # Metadata
│   └── plugin.json          # Plugin manifest
│
├── commands/                 # Slash commands
│   └── *.md
│
├── agents/                   # Subagents
│   └── *.md
│
├── skills/                   # Skills
│   └── */SKILL.md
│
├── hooks/                    # Event hooks
│   ├── hooks.json
│   └── *.json
│
├── scripts/                  # Hook & utility scripts
│   └── *.{sh,py,js}
│
├── .mcp.json                # MCP servers
│
├── README.md                # Documentation
├── CHANGELOG.md             # Version history
└── LICENSE                  # License file
```

## Key Features

- ✅ **Complete Structure**: Standard directory layout and configuration
- ✅ **Component Integration**: Seamless integration with other meta-skills
- ✅ **Validation**: Automatic validation before packaging
- ✅ **Distribution**: Create distributable zip packages
- ✅ **Documentation**: Template README and CHANGELOG
- ✅ **MCP Support**: Integrate external tools via MCP servers

## Best Practices

1. **Single Responsibility**: Each plugin has a clear, focused purpose
2. **Modular Components**: Use commands, agents, skills appropriately
3. **Version Control**: Follow semantic versioning strictly
4. **Documentation**: Provide clear installation and usage instructions
5. **Testing**: Validate all components before distribution
6. **Security**: Never commit secrets, use environment variables

## Examples

### Security Plugin

```
security-plugin/
├── commands/scan.md, audit.md
├── agents/security-reviewer.md
├── skills/security-analysis/
└── hooks/block-dangerous-ops.sh
```

### Data Analysis Plugin

```
data-analysis-plugin/
├── commands/analyze.md, visualize.md
├── agents/data-scientist.md, statistician.md
├── skills/data-pipeline/, chart-generator/
└── .mcp.json (database connections)
```

### DevOps Plugin

```
devops-plugin/
├── commands/deploy.md, rollback.md
├── agents/deployment-manager.md
├── skills/kubernetes-ops/
├── hooks/pre-deploy-checks.sh
└── .mcp.json (k8s, AWS tools)
```

## Troubleshooting

### Plugin Not Loading

- Verify `.claude-plugin/plugin.json` exists
- Check JSON syntax: `cat plugin.json | jq .`
- Ensure required fields present
- Restart Claude Code completely

### Components Not Registering

- Check YAML frontmatter in component files
- Verify file naming conventions
- Review custom paths in plugin.json
- Run with `claude --debug`

### MCP Servers Not Starting

- Verify script paths use `${CLAUDE_PLUGIN_ROOT}`
- Check scripts are executable
- Validate environment variables
- Review server logs

## Resources

### Official Documentation

- [Claude Code Plugins Reference](https://docs.claude.com/zh-CN/docs/claude-code/plugins-reference)
- [MCP Documentation](https://modelcontextprotocol.io)

### Related Skills

- [Commands Meta-Skill](../commands/)
- [Agents Meta-Skill](../agents/)
- [Skill Creator](../skills/skill-creator/)
- [Hooks Meta-Skill](../hooks/)

## Version

**Version**: 1.0.0
**Last Updated**: 2025-10-28
**Compatibility**: Claude Code v1.0.124+
**Based On**: Claude Code Official Documentation (2025-10-23)

## License

MIT License - See LICENSE file for details
