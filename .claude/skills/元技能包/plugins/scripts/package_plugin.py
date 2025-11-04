#!/usr/bin/env python3
"""
Plugin Packaging Script

Validates and packages a Claude Code plugin into a distributable zip file.

Usage:
    python3 package_plugin.py /path/to/plugin --output ./dist
"""

import argparse
import json
import os
import shutil
import zipfile
from pathlib import Path
from typing import List, Tuple


class PluginValidator:
    """Validates plugin structure and configuration."""

    def __init__(self, plugin_path: Path):
        self.plugin_path = plugin_path
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self) -> bool:
        """Run all validation checks."""
        print(f"🔍 Validating plugin at: {self.plugin_path}\n")

        self._check_directory_structure()
        self._validate_plugin_json()
        self._validate_components()
        self._check_file_permissions()

        # Print results
        if self.errors:
            print("\n❌ Validation failed with errors:\n")
            for error in self.errors:
                print(f"  • {error}")

        if self.warnings:
            print("\n⚠️  Warnings:\n")
            for warning in self.warnings:
                print(f"  • {warning}")

        if not self.errors:
            print("\n✅ Validation passed!")
            return True

        return False

    def _check_directory_structure(self):
        """Check required directory structure."""
        # Required: .claude-plugin directory
        claude_plugin_dir = self.plugin_path / ".claude-plugin"
        if not claude_plugin_dir.exists():
            self.errors.append("Missing required .claude-plugin/ directory")

        # Check for plugin.json
        plugin_json = claude_plugin_dir / "plugin.json"
        if not plugin_json.exists():
            self.errors.append("Missing required .claude-plugin/plugin.json")

        # Recommended directories
        recommended_dirs = ["commands", "agents", "skills", "hooks", "scripts"]
        for dir_name in recommended_dirs:
            if not (self.plugin_path / dir_name).exists():
                self.warnings.append(f"Missing recommended directory: {dir_name}/")

    def _validate_plugin_json(self):
        """Validate plugin.json structure."""
        plugin_json_path = self.plugin_path / ".claude-plugin" / "plugin.json"

        if not plugin_json_path.exists():
            return  # Already reported in structure check

        try:
            with open(plugin_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Check required fields
            required_fields = ["name", "version", "description", "author"]
            for field in required_fields:
                if field not in data:
                    self.errors.append(f"plugin.json missing required field: {field}")

            # Validate name format
            if "name" in data:
                name = data["name"]
                if not name.islower() or ' ' in name:
                    self.errors.append(
                        f"plugin.json 'name' must be lowercase with hyphens (kebab-case): {name}"
                    )

            # Validate version format
            if "version" in data:
                version = data["version"]
                parts = version.split('.')
                if len(parts) != 3 or not all(part.isdigit() for part in parts):
                    self.errors.append(
                        f"plugin.json 'version' must follow semantic versioning (X.Y.Z): {version}"
                    )

            # Validate author structure
            if "author" in data:
                author = data["author"]
                if not isinstance(author, dict):
                    self.errors.append("plugin.json 'author' must be an object")
                elif "name" not in author:
                    self.errors.append("plugin.json 'author' must have 'name' field")

            # Validate custom paths
            path_fields = ["commands", "agents", "hooks", "mcpServers"]
            for field in path_fields:
                if field in data:
                    path = data[field]
                    if not path.startswith("./"):
                        self.errors.append(
                            f"plugin.json '{field}' path must start with ./: {path}"
                        )

                    # Check if path exists
                    full_path = self.plugin_path / path.lstrip("./")
                    if not full_path.exists():
                        self.warnings.append(
                            f"plugin.json '{field}' path does not exist: {path}"
                        )

            # Recommended fields
            recommended_fields = ["homepage", "repository", "license", "keywords"]
            for field in recommended_fields:
                if field not in data:
                    self.warnings.append(f"plugin.json missing recommended field: {field}")

        except json.JSONDecodeError as e:
            self.errors.append(f"plugin.json is not valid JSON: {e}")
        except Exception as e:
            self.errors.append(f"Error reading plugin.json: {e}")

    def _validate_components(self):
        """Validate component files."""
        # Validate commands
        commands_dir = self.plugin_path / "commands"
        if commands_dir.exists():
            command_files = list(commands_dir.glob("*.md"))
            for cmd_file in command_files:
                self._validate_command(cmd_file)

        # Validate agents
        agents_dir = self.plugin_path / "agents"
        if agents_dir.exists():
            agent_files = list(agents_dir.glob("*.md"))
            for agent_file in agent_files:
                self._validate_agent(agent_file)

        # Validate skills
        skills_dir = self.plugin_path / "skills"
        if skills_dir.exists():
            for skill_dir in skills_dir.iterdir():
                if skill_dir.is_dir():
                    self._validate_skill(skill_dir)

        # Validate hooks
        hooks_dir = self.plugin_path / "hooks"
        if hooks_dir.exists():
            hooks_json = hooks_dir / "hooks.json"
            if hooks_json.exists():
                self._validate_hooks_json(hooks_json)

        # Validate MCP config
        mcp_json = self.plugin_path / ".mcp.json"
        if mcp_json.exists():
            self._validate_mcp_json(mcp_json)

    def _validate_command(self, command_file: Path):
        """Validate a command file."""
        try:
            content = command_file.read_text(encoding='utf-8')

            # Check for YAML frontmatter
            if not content.startswith('---'):
                self.warnings.append(
                    f"Command {command_file.name} missing YAML frontmatter"
                )
        except Exception as e:
            self.errors.append(f"Error reading command {command_file.name}: {e}")

    def _validate_agent(self, agent_file: Path):
        """Validate an agent file."""
        try:
            content = agent_file.read_text(encoding='utf-8')

            # Check for YAML frontmatter
            if not content.startswith('---'):
                self.errors.append(
                    f"Agent {agent_file.name} missing YAML frontmatter"
                )
                return

            # Extract frontmatter
            parts = content.split('---', 2)
            if len(parts) < 3:
                self.errors.append(
                    f"Agent {agent_file.name} has malformed YAML frontmatter"
                )
                return

            # Check for required fields
            frontmatter = parts[1]
            if 'name:' not in frontmatter:
                self.errors.append(
                    f"Agent {agent_file.name} missing 'name' in frontmatter"
                )
            if 'description:' not in frontmatter:
                self.errors.append(
                    f"Agent {agent_file.name} missing 'description' in frontmatter"
                )
        except Exception as e:
            self.errors.append(f"Error reading agent {agent_file.name}: {e}")

    def _validate_skill(self, skill_dir: Path):
        """Validate a skill directory."""
        skill_md = skill_dir / "SKILL.md"

        if not skill_md.exists():
            self.errors.append(
                f"Skill {skill_dir.name} missing required SKILL.md"
            )
            return

        try:
            content = skill_md.read_text(encoding='utf-8')

            # Check for YAML frontmatter
            if not content.startswith('---'):
                self.errors.append(
                    f"Skill {skill_dir.name} SKILL.md missing YAML frontmatter"
                )
                return

            # Extract frontmatter
            parts = content.split('---', 2)
            if len(parts) < 3:
                self.errors.append(
                    f"Skill {skill_dir.name} SKILL.md has malformed YAML frontmatter"
                )
                return

            # Check for required fields
            frontmatter = parts[1]
            if 'name:' not in frontmatter:
                self.errors.append(
                    f"Skill {skill_dir.name} SKILL.md missing 'name' in frontmatter"
                )
            if 'description:' not in frontmatter:
                self.errors.append(
                    f"Skill {skill_dir.name} SKILL.md missing 'description' in frontmatter"
                )
        except Exception as e:
            self.errors.append(f"Error reading skill {skill_dir.name}: {e}")

    def _validate_hooks_json(self, hooks_json: Path):
        """Validate hooks.json configuration."""
        try:
            with open(hooks_json, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if "hooks" not in data:
                self.errors.append("hooks.json missing 'hooks' root object")
        except json.JSONDecodeError as e:
            self.errors.append(f"hooks.json is not valid JSON: {e}")
        except Exception as e:
            self.errors.append(f"Error reading hooks.json: {e}")

    def _validate_mcp_json(self, mcp_json: Path):
        """Validate .mcp.json configuration."""
        try:
            with open(mcp_json, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if "mcpServers" not in data:
                self.errors.append(".mcp.json missing 'mcpServers' root object")
        except json.JSONDecodeError as e:
            self.errors.append(f".mcp.json is not valid JSON: {e}")
        except Exception as e:
            self.errors.append(f"Error reading .mcp.json: {e}")

    def _check_file_permissions(self):
        """Check file permissions for scripts."""
        scripts_dir = self.plugin_path / "scripts"
        if not scripts_dir.exists():
            return

        for script_file in scripts_dir.rglob("*.sh"):
            if not os.access(script_file, os.X_OK):
                self.warnings.append(
                    f"Script {script_file.relative_to(self.plugin_path)} not executable"
                )


def package_plugin(plugin_path: Path, output_dir: Path) -> Tuple[bool, Path]:
    """Package plugin into a zip file."""
    # Read plugin.json to get name and version
    plugin_json_path = plugin_path / ".claude-plugin" / "plugin.json"

    try:
        with open(plugin_json_path, 'r', encoding='utf-8') as f:
            plugin_data = json.load(f)

        plugin_name = plugin_data.get("name", plugin_path.name)
        plugin_version = plugin_data.get("version", "1.0.0")
    except Exception as e:
        print(f"Error reading plugin.json: {e}")
        return False, None

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create zip file
    zip_filename = f"{plugin_name}-{plugin_version}.zip"
    zip_path = output_dir / zip_filename

    print(f"\n📦 Packaging plugin: {plugin_name} v{plugin_version}")
    print(f"📁 Output: {zip_path}\n")

    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through plugin directory
            for root, dirs, files in os.walk(plugin_path):
                # Skip hidden directories and __pycache__
                dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']

                for file in files:
                    # Skip hidden files and cache files
                    if file.startswith('.') or file.endswith('.pyc'):
                        continue

                    file_path = Path(root) / file
                    arcname = file_path.relative_to(plugin_path.parent)
                    zipf.write(file_path, arcname)
                    print(f"  ✓ Added: {arcname}")

        print(f"\n✅ Plugin packaged successfully: {zip_path}")
        print(f"📊 Size: {zip_path.stat().st_size / 1024:.2f} KB")

        return True, zip_path

    except Exception as e:
        print(f"\n❌ Error packaging plugin: {e}")
        return False, None


def main():
    parser = argparse.ArgumentParser(
        description="Validate and package a Claude Code plugin"
    )
    parser.add_argument(
        "plugin_path",
        help="Path to plugin directory"
    )
    parser.add_argument(
        "--output",
        default="./dist",
        help="Output directory for zip file (default: ./dist)"
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip validation and package anyway"
    )

    args = parser.parse_args()

    plugin_path = Path(args.plugin_path).resolve()
    output_dir = Path(args.output).resolve()

    if not plugin_path.exists():
        print(f"Error: Plugin path does not exist: {plugin_path}")
        return 1

    if not plugin_path.is_dir():
        print(f"Error: Plugin path is not a directory: {plugin_path}")
        return 1

    # Validate plugin
    if not args.skip_validation:
        validator = PluginValidator(plugin_path)
        if not validator.validate():
            print("\n❌ Validation failed. Fix errors and try again.")
            print("   Use --skip-validation to package anyway (not recommended)")
            return 1

    # Package plugin
    success, zip_path = package_plugin(plugin_path, output_dir)

    if success:
        print(f"\n📤 Ready for distribution!")
        print(f"\n📝 Next steps:")
        print(f"   1. Test installation: unzip {zip_path.name} -d ~/.claude/plugins/")
        print(f"   2. Restart Claude Code")
        print(f"   3. Verify components loaded: claude --debug")
        print(f"   4. Distribute via Git, npm, or direct download")
        return 0
    else:
        return 1


if __name__ == "__main__":
    exit(main())
