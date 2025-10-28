#!/usr/bin/env python3
"""
Plugin Initialization Script

Creates a new Claude Code plugin with standard structure and template files.

Usage:
    python3 init_plugin.py --name my-plugin --description "My plugin description" --author "Your Name"
"""

import argparse
import json
import os
from pathlib import Path
from datetime import datetime


PLUGIN_JSON_TEMPLATE = {
    "name": "",
    "version": "1.0.0",
    "description": "",
    "author": {
        "name": "",
        "email": "",
        "url": ""
    },
    "homepage": "",
    "repository": "",
    "license": "MIT",
    "keywords": []
}

README_TEMPLATE = """# {plugin_name}

{description}

## Installation

### Method 1: Git Clone

```bash
git clone {repository}
cp -r {plugin_name} ~/.claude/plugins/
```

### Method 2: Manual Installation

1. Download the latest release
2. Extract to `~/.claude/plugins/`
3. Restart Claude Code

## Configuration

Add to your `.claude/settings.json`:

```json
{{
  "enabledPlugins": ["{plugin_name}"]
}}
```

**Important**: Restart Claude Code completely for the plugin to load.

## Components

### Commands

{commands_description}

### Agents

{agents_description}

### Skills

{skills_description}

### Hooks

{hooks_description}

## Usage

{usage_examples}

## Development

### Testing

```bash
# Copy to test location
cp -r ./{plugin_name} ~/.claude/plugins/

# Restart Claude Code

# Run with debug
claude --debug
```

### Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

## License

{license}

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.
"""

CHANGELOG_TEMPLATE = """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial plugin structure

## [1.0.0] - {date}

### Added
- Initial release
- Basic plugin structure
- Example components
"""

LICENSE_MIT_TEMPLATE = """MIT License

Copyright (c) {year} {author}

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

COMMAND_TEMPLATE = """---
description: {description}
---

# {title}

{content}
"""

AGENT_TEMPLATE = """---
name: {name}
description: {description}
tools: Read, Write, Edit, Grep, Glob, Bash
model: inherit
---

# {title}

## Role & Goals

You are {role_description}.

## Core Capabilities

{capabilities}

## Workflow

{workflow}

## Examples

<example>
<user_request>
{example_request}
</user_request>

<agent_response>
{example_response}
</agent_response>
</example>
"""

SKILL_TEMPLATE = """---
name: {name}
description: {description}
---

# {title}

{content}

## Quick Start

{quickstart}

## API Reference

{api_reference}
"""

HOOKS_JSON_TEMPLATE = {
    "hooks": {
        "PreToolUse": [],
        "PostToolUse": [],
        "UserPromptSubmit": [],
        "SubagentStop": [],
        "Stop": [],
        "Notification": [],
        "PreCompact": [],
        "SessionStart": []
    }
}

MCP_JSON_TEMPLATE = {
    "mcpServers": {}
}


def create_directory_structure(plugin_path: Path):
    """Create the plugin directory structure."""
    directories = [
        plugin_path / ".claude-plugin",
        plugin_path / "commands",
        plugin_path / "agents",
        plugin_path / "skills",
        plugin_path / "hooks",
        plugin_path / "scripts",
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory.relative_to(plugin_path)}")


def create_plugin_json(plugin_path: Path, name: str, description: str, author_info: dict):
    """Create plugin.json manifest."""
    plugin_json = PLUGIN_JSON_TEMPLATE.copy()
    plugin_json["name"] = name
    plugin_json["description"] = description
    plugin_json["author"] = author_info

    plugin_json_path = plugin_path / ".claude-plugin" / "plugin.json"
    with open(plugin_json_path, 'w', encoding='utf-8') as f:
        json.dump(plugin_json, f, indent=2, ensure_ascii=False)

    print(f"✓ Created plugin.json")


def create_readme(plugin_path: Path, name: str, description: str, license: str):
    """Create README.md."""
    readme_content = README_TEMPLATE.format(
        plugin_name=name,
        description=description,
        repository=f"https://github.com/yourteam/{name}",
        commands_description="TODO: Describe available commands",
        agents_description="TODO: Describe available agents",
        skills_description="TODO: Describe available skills",
        hooks_description="TODO: Describe configured hooks",
        usage_examples="TODO: Add usage examples",
        license=license
    )

    readme_path = plugin_path / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print(f"✓ Created README.md")


def create_changelog(plugin_path: Path):
    """Create CHANGELOG.md."""
    changelog_content = CHANGELOG_TEMPLATE.format(
        date=datetime.now().strftime("%Y-%m-%d")
    )

    changelog_path = plugin_path / "CHANGELOG.md"
    with open(changelog_path, 'w', encoding='utf-8') as f:
        f.write(changelog_content)

    print(f"✓ Created CHANGELOG.md")


def create_license(plugin_path: Path, license_type: str, author: str):
    """Create LICENSE file."""
    if license_type == "MIT":
        license_content = LICENSE_MIT_TEMPLATE.format(
            year=datetime.now().year,
            author=author
        )
    else:
        license_content = f"{license_type} License\n\nTODO: Add license text"

    license_path = plugin_path / "LICENSE"
    with open(license_path, 'w', encoding='utf-8') as f:
        f.write(license_content)

    print(f"✓ Created LICENSE ({license_type})")


def create_example_command(plugin_path: Path):
    """Create an example command."""
    command_content = COMMAND_TEMPLATE.format(
        description="Example command - replace with your own",
        title="Example Command",
        content="TODO: Replace this with your command prompt content"
    )

    command_path = plugin_path / "commands" / "example.md"
    with open(command_path, 'w', encoding='utf-8') as f:
        f.write(command_content)

    print(f"✓ Created example command: commands/example.md")


def create_example_agent(plugin_path: Path):
    """Create an example agent."""
    agent_content = AGENT_TEMPLATE.format(
        name="example-agent",
        description="Example agent - replace with your own",
        title="Example Agent",
        role_description="an example agent that demonstrates the structure",
        capabilities="TODO: List agent capabilities",
        workflow="TODO: Describe agent workflow",
        example_request="TODO: Add example request",
        example_response="TODO: Add example response"
    )

    agent_path = plugin_path / "agents" / "example-agent.md"
    with open(agent_path, 'w', encoding='utf-8') as f:
        f.write(agent_content)

    print(f"✓ Created example agent: agents/example-agent.md")


def create_example_skill(plugin_path: Path):
    """Create an example skill."""
    skill_dir = plugin_path / "skills" / "example-skill"
    skill_dir.mkdir(parents=True, exist_ok=True)

    skill_content = SKILL_TEMPLATE.format(
        name="example-skill",
        description="Example skill - replace with your own",
        title="Example Skill",
        content="TODO: Describe what this skill does",
        quickstart="TODO: Add quick start guide",
        api_reference="TODO: Add API reference"
    )

    skill_path = skill_dir / "SKILL.md"
    with open(skill_path, 'w', encoding='utf-8') as f:
        f.write(skill_content)

    # Create subdirectories
    (skill_dir / "scripts").mkdir(exist_ok=True)
    (skill_dir / "references").mkdir(exist_ok=True)
    (skill_dir / "assets").mkdir(exist_ok=True)

    print(f"✓ Created example skill: skills/example-skill/")


def create_hooks_config(plugin_path: Path):
    """Create hooks.json configuration."""
    hooks_path = plugin_path / "hooks" / "hooks.json"
    with open(hooks_path, 'w', encoding='utf-8') as f:
        json.dump(HOOKS_JSON_TEMPLATE, f, indent=2)

    print(f"✓ Created hooks.json")


def create_mcp_config(plugin_path: Path):
    """Create .mcp.json configuration."""
    mcp_path = plugin_path / ".mcp.json"
    with open(mcp_path, 'w', encoding='utf-8') as f:
        json.dump(MCP_JSON_TEMPLATE, f, indent=2)

    print(f"✓ Created .mcp.json")


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a new Claude Code plugin with standard structure"
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Plugin name (kebab-case, e.g., 'my-plugin')"
    )
    parser.add_argument(
        "--description",
        required=True,
        help="Brief plugin description"
    )
    parser.add_argument(
        "--author",
        required=True,
        help="Author name"
    )
    parser.add_argument(
        "--email",
        default="",
        help="Author email (optional)"
    )
    parser.add_argument(
        "--url",
        default="",
        help="Author URL (optional)"
    )
    parser.add_argument(
        "--output",
        default=".",
        help="Output directory (default: current directory)"
    )
    parser.add_argument(
        "--license",
        default="MIT",
        help="License type (default: MIT)"
    )

    args = parser.parse_args()

    # Validate plugin name
    if not args.name.islower() or ' ' in args.name:
        print("Error: Plugin name must be lowercase with hyphens (kebab-case)")
        return 1

    # Create plugin path
    output_path = Path(args.output).resolve()
    plugin_path = output_path / args.name

    if plugin_path.exists():
        print(f"Error: Directory {plugin_path} already exists")
        return 1

    print(f"\n🚀 Initializing plugin: {args.name}")
    print(f"📁 Output path: {plugin_path}\n")

    # Create structure
    create_directory_structure(plugin_path)

    # Create configuration files
    author_info = {
        "name": args.author,
        "email": args.email,
        "url": args.url
    }
    create_plugin_json(plugin_path, args.name, args.description, author_info)

    # Create documentation
    create_readme(plugin_path, args.name, args.description, args.license)
    create_changelog(plugin_path)
    create_license(plugin_path, args.license, args.author)

    # Create example components
    create_example_command(plugin_path)
    create_example_agent(plugin_path)
    create_example_skill(plugin_path)
    create_hooks_config(plugin_path)
    create_mcp_config(plugin_path)

    print(f"\n✅ Plugin '{args.name}' initialized successfully!")
    print(f"\n📝 Next steps:")
    print(f"   1. cd {plugin_path}")
    print(f"   2. Customize plugin.json with your details")
    print(f"   3. Replace example components with your own")
    print(f"   4. Update README.md with usage instructions")
    print(f"   5. Test: cp -r . ~/.claude/plugins/{args.name} && restart Claude Code")

    return 0


if __name__ == "__main__":
    exit(main())
