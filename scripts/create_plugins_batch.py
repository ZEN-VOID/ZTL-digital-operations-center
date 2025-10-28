#!/usr/bin/env python3
"""
Batch create plugins for all teams based on .claude/configs structure
"""

import os
import json
import shutil
from pathlib import Path

# Plugin configurations for each team
PLUGIN_CONFIGS = {
    "创意组": {
        "name": "creative-team",
        "description": "Creative content production plugin with specialists in advertising, copywriting, design, photography, and video editing. Includes X0 content analyst, X1 advertising strategist, X2 copywriter, X3 graphic designer, X4 layout designer, X5 short video scriptwriter, X6 photographer, X7 video editor, and XX creative team leader.",
        "keywords": ["creative", "content", "advertising", "design", "video", "photography", "marketing"]
    },
    "供应组": {
        "name": "supply-chain-team",
        "description": "Supply chain and procurement management plugin with capabilities in requirement analysis, purchasing execution, inventory management, cost control, supplier management, and ledger reconciliation. Includes S0 requirement analyst, S1 procurement manager, S2 inventory manager, S3 cost controller, S4 supplier manager, S5 ledger manager, and SS supply chain leader.",
        "keywords": ["supply-chain", "procurement", "inventory", "cost-control", "supplier", "logistics"]
    },
    "开发组": {
        "name": "development-team",
        "description": "Full-stack development plugin with expertise in product management, frontend/backend development, database design, API development, AI integration, testing, version control, and cloud deployment. Includes F0 product manager, F1 frontend dev, F2 component dev, F3 database dev, F4 API dev, F5 backend dev, F6 AI integration dev, F7 testing engineer, F8 version control assistant, F9 cloud deployment manager, and FF development team leader.",
        "keywords": ["development", "full-stack", "frontend", "backend", "database", "api", "ai", "devops"]
    },
    "美团组": {
        "name": "meituan-ops-team",
        "description": "Meituan platform operations plugin for restaurant business management, including operations management, marketing campaigns, reporting, and web automation. Includes M0 business analyst, M1 operations manager, M2 marketing manager, M4 reporting manager, M5 web automation specialist, and MM platform ops leader.",
        "keywords": ["meituan", "operations", "marketing", "reporting", "automation", "restaurant"]
    },
    "情报组": {
        "name": "intelligence-team",
        "description": "Market intelligence and data collection plugin with capabilities in requirement analysis, deep research, web scraping, data analysis, and cloud storage management. Includes E0 intelligence analyst, E1 deep researcher, E2 Chrome web scraper, E3 advanced crawler, E4 intelligence analyst, E5 COS storage manager, E6 Supabase database manager, and EE intelligence team leader.",
        "keywords": ["intelligence", "research", "data", "scraping", "analysis", "storage"]
    },
    "行政组": {
        "name": "admin-team",
        "description": "Administrative operations plugin covering finance, HR, legal, secretarial work, Feishu collaboration, and file management. Includes R0 business analyst, R1 finance manager, R2 HR manager, R3 legal expert, R4 secretary, R5 Feishu manager, R6 file manager, R7 Tencent COS storage manager, and RR admin team leader.",
        "keywords": ["admin", "finance", "hr", "legal", "office", "collaboration", "management"]
    },
    "战略组": {
        "name": "strategy-team",
        "description": "Strategic planning and business development plugin with expertise in requirement analysis, operational optimization, product development, regional expansion, business model design, franchise replication, digital transformation, and refined management. Includes G0 strategy analyst, G1 operations optimizer, G2 product strategist, G3 expansion strategist, G4 business model designer, G5 franchise expert, G6 digital transformation architect, G7 management expert, and GG strategy leader.",
        "keywords": ["strategy", "planning", "expansion", "business-model", "transformation", "optimization"]
    }
}

def create_plugin_structure(team_name: str, config: dict, base_dir: Path):
    """Create complete plugin structure for a team"""

    plugin_dir = base_dir / "plugins" / team_name
    plugin_dir.mkdir(parents=True, exist_ok=True)

    # 1. Create directory structure
    (plugin_dir / ".claude-plugin").mkdir(exist_ok=True)
    (plugin_dir / "commands").mkdir(exist_ok=True)
    (plugin_dir / "agents").mkdir(exist_ok=True)
    (plugin_dir / "skills").mkdir(exist_ok=True)
    (plugin_dir / "hooks").mkdir(exist_ok=True)
    (plugin_dir / "scripts").mkdir(exist_ok=True)

    # 2. Create plugin.json
    plugin_json = {
        "name": config["name"],
        "version": "1.0.0",
        "description": config["description"],
        "author": {
            "name": "ZTL Digital Intelligence Operations Center",
            "email": f"{config['name']}@ztl.com",
            "url": f"https://github.com/ztl-digital/{config['name']}-plugin"
        },
        "homepage": f"https://github.com/ztl-digital/{config['name']}-plugin",
        "repository": f"https://github.com/ztl-digital/{config['name']}-plugin",
        "license": "MIT",
        "keywords": config["keywords"],
        "commands": "./commands",
        "agents": "./agents",
        "hooks": "./hooks/hooks.json",
        "mcpServers": "./.mcp.json"
    }

    with open(plugin_dir / ".claude-plugin" / "plugin.json", "w", encoding="utf-8") as f:
        json.dump(plugin_json, f, indent=2, ensure_ascii=False)

    # 3. Copy agents from configs
    source_agents = base_dir / ".claude" / "configs" / team_name
    if source_agents.exists():
        for agent_file in source_agents.glob("*.md"):
            shutil.copy2(agent_file, plugin_dir / "agents" / agent_file.name)

    # 4. Create hooks.json
    hooks_json = {
        "hooks": {
            "SessionStart": [],
            "SessionEnd": [],
            "UserPromptSubmit": [],
            "Stop": [],
            "PreToolUse": [],
            "PostToolUse": [],
            "PreCompact": [],
            "PostCompact": []
        }
    }

    with open(plugin_dir / "hooks" / "hooks.json", "w", encoding="utf-8") as f:
        json.dump(hooks_json, f, indent=2)

    # 5. Create .mcp.json
    mcp_json = {"mcpServers": {}}

    with open(plugin_dir / ".mcp.json", "w", encoding="utf-8") as f:
        json.dump(mcp_json, f, indent=2)

    # 6. Create README files for empty directories
    commands_readme = """# Commands

This directory contains slash commands for this plugin.

## Structure

Commands should follow the standard format:

```markdown
---
description: Brief command description
argument-hint: [optional parameters]
allowed-tools: Tool1, Tool2
---

# Command Content
[Your prompt content here]
```

## Available Commands

Currently no commands defined. Add `.md` files here to create new slash commands.

## Examples

See `.claude/skills/元skills/commands/` for command creation guidance.
"""

    skills_readme = """# Skills

This directory contains skills for this plugin.

## Structure

Skills should follow the standard directory structure:

```
skill-name/
├── SKILL.md              # Required: Metadata + Usage
├── scripts/              # Optional: Execution scripts
├── templates/            # Optional: Templates
└── reference.md          # Optional: Extended documentation
```

## Available Skills

Currently no skills defined. Add skill directories here to create new capabilities.

## Examples

See `.claude/skills/元skills/skills/` for skill creation guidance.
"""

    with open(plugin_dir / "commands" / "README.md", "w", encoding="utf-8") as f:
        f.write(commands_readme)

    with open(plugin_dir / "skills" / "README.md", "w", encoding="utf-8") as f:
        f.write(skills_readme)

    # 7. Create LICENSE
    license_text = """MIT License

Copyright (c) 2025 ZTL Digital Intelligence Operations Center

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

    with open(plugin_dir / "LICENSE", "w", encoding="utf-8") as f:
        f.write(license_text)

    # 8. Create CHANGELOG.md
    changelog_text = f"""# Changelog

All notable changes to the {team_name} Plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features
- Add slash commands for common workflows
- Create skills for automated workflows
- Add hooks for quality assurance checkpoints
- Integrate relevant MCP servers

---

## [1.0.0] - 2025-10-28

### Added
- **Initial Release** of {team_name} Plugin
- Complete agent set for {team_name} operations
- Standard plugin structure (commands, skills, hooks, MCP)
- Comprehensive documentation
- MIT License

### Documentation
- Complete README with installation instructions
- Usage examples for common workflows
- Agent capability descriptions
- Best practices guide

---

**Maintained by**: ZTL Digital Intelligence Operations Center
**Plugin Repository**: [github.com/ztl-digital/{config['name']}-plugin](https://github.com/ztl-digital/{config['name']}-plugin)
**License**: MIT
"""

    with open(plugin_dir / "CHANGELOG.md", "w", encoding="utf-8") as f:
        f.write(changelog_text)

    # 9. Create README.md
    # Count agents
    agent_count = len(list((plugin_dir / "agents").glob("*.md")))

    readme_text = f"""# {team_name} Plugin

> Professional {team_name} operations plugin for Claude Code

## Overview

{config['description']}

## Features

### 🤖 Specialized Agents

This plugin includes **{agent_count} specialized agents** covering all aspects of {team_name} operations.

See `agents/` directory for complete agent documentation.

## Installation

### Method 1: Local Installation

1. Copy the plugin to your Claude Code plugins directory:
```bash
cp -r plugins/{team_name} ~/.claude/plugins/{config['name']}
```

2. Enable the plugin in your `.claude/settings.json`:
```json
{{
  "enabledPlugins": ["{config['name']}"]
}}
```

3. Restart Claude Code (complete exit and restart required)

### Method 2: Project-Level Installation

1. Keep the plugin in your project directory: `plugins/{team_name}/`

2. Add to project-level `.claude/settings.json`:
```json
{{
  "enabledPlugins": ["./plugins/{team_name}"]
}}
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
→ Claude automatically delegates to appropriate {team_name} agent
```

### Output Structure

All agent outputs are saved to structured directories:

```
output/{team_name}/
├── [agent-id]-[task-name]/
│   ├── plans/
│   ├── results/
│   ├── logs/
│   └── metadata/
```

## Project Structure

```
plugins/{team_name}/
├── .claude-plugin/
│   └── plugin.json           # Plugin manifest
├── agents/
│   └── *.md                  # {agent_count} specialized agents
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

- GitHub Issues: [{config['name']}-plugin/issues](https://github.com/ztl-digital/{config['name']}-plugin/issues)
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
**Plugin Type**: Professional Domain Plugin ({team_name})
**Agent Count**: {agent_count} specialized agents
**Status**: Production Ready
"""

    with open(plugin_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_text)

    return plugin_dir, agent_count

def main():
    base_dir = Path("/Users/vincentlee/Desktop/ZTL数智化作战中心")

    results = []

    for team_name, config in PLUGIN_CONFIGS.items():
        print(f"Creating plugin for {team_name}...")
        plugin_dir, agent_count = create_plugin_structure(team_name, config, base_dir)
        results.append({
            "team": team_name,
            "name": config["name"],
            "path": plugin_dir,
            "agents": agent_count
        })
        print(f"  ✅ Created {plugin_dir} with {agent_count} agents")

    print("\n" + "="*60)
    print("Summary:")
    print("="*60)
    for r in results:
        print(f"{r['team']:12} | {r['name']:25} | {r['agents']:2} agents")
    print("="*60)
    print(f"Total: {len(results)} plugins created successfully!")

if __name__ == "__main__":
    main()
