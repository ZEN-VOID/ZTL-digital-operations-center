# 行政组 Plugin

> Professional 行政组 operations plugin for Claude Code

## Overview

Administrative operations plugin covering finance, HR, legal, secretarial work, Feishu collaboration, and file management. Includes R0 business analyst, R1 finance manager, R2 HR manager, R3 legal expert, R4 secretary, R5 Feishu manager, R6 file manager, R7 Tencent COS storage manager, and RR admin team leader.

## Features

### 🤖 Specialized Agents

This plugin includes **9 specialized agents** covering all aspects of 行政组 operations.

See `agents/` directory for complete agent documentation.

## Installation

### Method 1: Local Installation

1. Copy the plugin to your Claude Code plugins directory:
```bash
cp -r plugins/行政组 ~/.claude/plugins/admin-team
```

2. Enable the plugin in your `.claude/settings.json`:
```json
{
  "enabledPlugins": ["admin-team"]
}
```

3. Restart Claude Code (complete exit and restart required)

### Method 2: Project-Level Installation

1. Keep the plugin in your project directory: `plugins/行政组/`

2. Add to project-level `.claude/settings.json`:
```json
{
  "enabledPlugins": ["./plugins/行政组"]
}
```

3. Restart Claude Code

## Usage

### Agent Invocation

Agents can be invoked in two ways:

1. **Automatic Delegation**: Claude automatically selects the appropriate agent based on your request
2. **Explicit Invocation**: Use the Task tool to explicitly call a specific agent

Example:
```
User: [Task description matching agent capability]
→ Claude automatically delegates to appropriate 行政组 agent
```

### Output Structure

All agent outputs are saved to structured directories:

```
output/行政组/
├── [agent-id]-[task-name]/
│   ├── plans/
│   ├── results/
│   ├── logs/
│   └── metadata/
```

## Project Structure

```
plugins/行政组/
├── .claude-plugin/
│   └── plugin.json           # Plugin manifest
├── agents/
│   └── *.md                  # 9 specialized agents
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

## Extension Points

This plugin can be extended with:

1. **Commands** (commands/*.md) - Slash commands for frequent workflows
2. **Skills** (skills/*/SKILL.md) - Complex automated capabilities
3. **Hooks** (hooks/hooks.json) - Event-driven automation
4. **MCP Servers** (.mcp.json) - External tool integrations

See `.claude/skills/元skills/plugins/` for extension guidance.

## Requirements

- Claude Code v1.0.124+
- Sonnet 4.5 model (recommended)
- Tools: Task, Read, Write, Edit, Grep, Glob, Bash

## Support

For issues, questions, or contributions:

- GitHub Issues: [admin-team-plugin/issues](https://github.com/ztl-digital/admin-team-plugin/issues)
- Documentation: See individual agent files in `agents/` directory

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
**Plugin Type**: Professional Domain Plugin (行政组)
**Agent Count**: 9 specialized agents
**Status**: Production Ready
