#!/usr/bin/env python3
"""
全局插件扫描引擎 (Global Plugins Scanner)

功能：
1. 扫描全局Claude Code插件配置
2. 提取插件元数据、技能列表、智能体列表
3. 生成结构化的插件索引

扫描位置：
- ~/.claude/settings.json - 已启用的插件
- ~/.claude/plugins/installed_plugins.json - 安装记录
- ~/.claude/plugins/marketplaces/ - Marketplace插件
- ~/.claude/plugins/cache/ - 缓存插件
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import re


class PluginsScanner:
    """全局插件扫描器"""

    def __init__(self):
        self.home_dir = Path.home()
        self.claude_dir = self.home_dir / ".claude"
        self.plugins_dir = self.claude_dir / "plugins"
        self.settings_file = self.claude_dir / "settings.json"
        self.installed_file = self.plugins_dir / "installed_plugins.json"

    def scan_all(self) -> Dict[str, Any]:
        """
        扫描所有全局插件

        Returns:
            完整的插件注册表
        """
        print("🔍 开始扫描全局插件...")

        # 1. 读取已启用的插件列表
        enabled_plugins = self._read_enabled_plugins()
        print(f"   已启用插件: {len(enabled_plugins)} 个")

        # 2. 读取安装记录
        installed_plugins = self._read_installed_plugins()
        print(f"   已安装插件: {len(installed_plugins)} 个")

        # 3. 扫描每个插件的详细信息
        plugins_registry = {}
        for plugin_id, install_info in installed_plugins.items():
            print(f"\n   📦 扫描: {plugin_id}")

            plugin_data = {
                "plugin_id": plugin_id,
                "enabled": plugin_id in enabled_plugins,
                "version": install_info.get("version", "unknown"),
                "install_path": install_info.get("installPath", ""),
                "installed_at": install_info.get("installedAt", ""),
                "last_updated": install_info.get("lastUpdated", ""),
                "git_commit_sha": install_info.get("gitCommitSha", ""),
                "is_local": install_info.get("isLocal", False),
                "source": self._extract_source(plugin_id),
                "skills": [],
                "agents": [],
                "commands": [],
                "metadata": {}
            }

            # 扫描插件目录
            install_path = Path(install_info.get("installPath", "")).expanduser()
            if install_path.exists():
                # 扫描skills
                plugin_data["skills"] = self._scan_skills(install_path)
                print(f"      技能包: {len(plugin_data['skills'])} 个")

                # 扫描agents
                plugin_data["agents"] = self._scan_agents(install_path)
                if plugin_data["agents"]:
                    print(f"      智能体: {len(plugin_data['agents'])} 个")

                # 扫描commands
                plugin_data["commands"] = self._scan_commands(install_path)
                if plugin_data["commands"]:
                    print(f"      命令: {len(plugin_data['commands'])} 个")

                # 读取README
                readme_path = install_path / "README.md"
                if readme_path.exists():
                    plugin_data["metadata"]["readme_excerpt"] = self._extract_readme_excerpt(readme_path)
            else:
                print(f"      ⚠️  安装路径不存在: {install_path}")

            plugins_registry[plugin_id] = plugin_data

        # 构建最终结果
        result = {
            "scan_time": datetime.now().isoformat(),
            "total_plugins": len(plugins_registry),
            "enabled_plugins": len([p for p in plugins_registry.values() if p["enabled"]]),
            "total_skills": sum(len(p["skills"]) for p in plugins_registry.values()),
            "total_agents": sum(len(p["agents"]) for p in plugins_registry.values()),
            "plugins": plugins_registry
        }

        print(f"\n✅ 扫描完成:")
        print(f"   总插件数: {result['total_plugins']}")
        print(f"   已启用: {result['enabled_plugins']}")
        print(f"   总技能包: {result['total_skills']}")
        print(f"   总智能体: {result['total_agents']}")

        return result

    def _read_enabled_plugins(self) -> List[str]:
        """读取已启用的插件列表"""
        if not self.settings_file.exists():
            return []

        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)

            enabled_plugins = settings.get("enabledPlugins", {})
            # 可能是 {"plugin-id": true} 或 ["plugin-id"] 格式
            if isinstance(enabled_plugins, dict):
                return [k for k, v in enabled_plugins.items() if v]
            elif isinstance(enabled_plugins, list):
                return enabled_plugins
            else:
                return []
        except Exception as e:
            print(f"⚠️  无法读取settings.json: {e}")
            return []

    def _read_installed_plugins(self) -> Dict[str, Any]:
        """读取已安装的插件记录"""
        if not self.installed_file.exists():
            return {}

        try:
            with open(self.installed_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get("plugins", {})
        except Exception as e:
            print(f"⚠️  无法读取installed_plugins.json: {e}")
            return {}

    def _extract_source(self, plugin_id: str) -> str:
        """从plugin_id中提取来源信息"""
        # 格式: plugin-name@marketplace-name
        if "@" in plugin_id:
            parts = plugin_id.split("@")
            if len(parts) == 2:
                return parts[1]
        return "unknown"

    def _scan_skills(self, plugin_path: Path) -> List[Dict[str, Any]]:
        """扫描插件中的技能包"""
        skills = []
        skills_dir = plugin_path / "skills"

        if not skills_dir.exists():
            # 检查是否是单skill插件（直接包含SKILL.md）
            skill_file = plugin_path / "SKILL.md"
            if skill_file.exists():
                skill_data = self._parse_skill_file(skill_file)
                if skill_data:
                    skill_data["skill_path"] = str(plugin_path)
                    skills.append(skill_data)

            # 检查Anthropic Agent Skills结构（每个子目录是一个skill）
            # 例如: algorithmic-art/, canvas-design/, 等直接在根目录下
            for item in plugin_path.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    skill_file = item / "SKILL.md"
                    if skill_file.exists():
                        skill_data = self._parse_skill_file(skill_file)
                        if skill_data:
                            skill_data["skill_path"] = str(item)
                            skills.append(skill_data)

            return skills

        # 遍历skills目录
        for item in skills_dir.iterdir():
            if item.is_dir():
                skill_file = item / "SKILL.md"
                if skill_file.exists():
                    skill_data = self._parse_skill_file(skill_file)
                    if skill_data:
                        skill_data["skill_path"] = str(item)
                        skills.append(skill_data)

        return skills

    def _scan_agents(self, plugin_path: Path) -> List[Dict[str, Any]]:
        """扫描插件中的智能体"""
        agents = []
        agents_dir = plugin_path / "agents"

        if not agents_dir.exists():
            return agents

        # 遍历agents目录
        for agent_file in agents_dir.glob("*.md"):
            agent_data = self._parse_agent_file(agent_file)
            if agent_data:
                agents.append(agent_data)

        return agents

    def _scan_commands(self, plugin_path: Path) -> List[Dict[str, Any]]:
        """扫描插件中的命令"""
        commands = []
        commands_dir = plugin_path / "commands"

        if not commands_dir.exists():
            return commands

        # 遍历commands目录
        for cmd_file in commands_dir.glob("*.md"):
            cmd_data = self._parse_command_file(cmd_file)
            if cmd_data:
                commands.append(cmd_data)

        return commands

    def _parse_skill_file(self, skill_file: Path) -> Optional[Dict[str, Any]]:
        """解析SKILL.md文件"""
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 提取YAML frontmatter
            yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if not yaml_match:
                return None

            yaml_content = yaml_match.group(1)

            # 简单解析YAML (仅提取name和description)
            name_match = re.search(r'^name:\s*(.+)$', yaml_content, re.MULTILINE)
            desc_match = re.search(r'^description:\s*(.+)$', yaml_content, re.MULTILINE)
            tools_match = re.search(r'^allowed-tools:\s*(.+)$', yaml_content, re.MULTILINE)

            skill_name = name_match.group(1).strip() if name_match else skill_file.stem
            skill_desc = desc_match.group(1).strip() if desc_match else ""
            allowed_tools = tools_match.group(1).strip() if tools_match else ""

            # 提取第一个标题作为显示名称
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            display_name = title_match.group(1).strip() if title_match else skill_name

            return {
                "skill_id": skill_name,
                "display_name": display_name,
                "description": skill_desc,
                "allowed_tools": allowed_tools,
                "file_path": str(skill_file)
            }
        except Exception as e:
            print(f"      ⚠️  解析失败: {skill_file.name} - {e}")
            return None

    def _parse_agent_file(self, agent_file: Path) -> Optional[Dict[str, Any]]:
        """解析智能体.md文件"""
        try:
            with open(agent_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 提取YAML frontmatter (如有)
            yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)

            agent_data = {
                "agent_id": agent_file.stem,
                "file_path": str(agent_file)
            }

            if yaml_match:
                yaml_content = yaml_match.group(1)
                name_match = re.search(r'^name:\s*(.+)$', yaml_content, re.MULTILINE)
                desc_match = re.search(r'^description:\s*(.+)$', yaml_content, re.MULTILINE)

                if name_match:
                    agent_data["name"] = name_match.group(1).strip()
                if desc_match:
                    agent_data["description"] = desc_match.group(1).strip()

            # 提取第一个标题
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if title_match and "name" not in agent_data:
                agent_data["name"] = title_match.group(1).strip()

            return agent_data
        except Exception as e:
            print(f"      ⚠️  解析失败: {agent_file.name} - {e}")
            return None

    def _parse_command_file(self, cmd_file: Path) -> Optional[Dict[str, Any]]:
        """解析命令.md文件"""
        try:
            with open(cmd_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 提取YAML frontmatter
            yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)

            cmd_data = {
                "command_id": cmd_file.stem,
                "file_path": str(cmd_file)
            }

            if yaml_match:
                yaml_content = yaml_match.group(1)
                desc_match = re.search(r'^description:\s*(.+)$', yaml_content, re.MULTILINE)

                if desc_match:
                    cmd_data["description"] = desc_match.group(1).strip()

            return cmd_data
        except Exception as e:
            print(f"      ⚠️  解析失败: {cmd_file.name} - {e}")
            return None

    def _extract_readme_excerpt(self, readme_path: Path, max_lines: int = 10) -> str:
        """提取README的前几行作为摘要"""
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # 提取前max_lines行，跳过空行
            excerpt_lines = []
            for line in lines[:max_lines * 2]:  # 读取更多行以应对空行
                line = line.strip()
                if line:
                    excerpt_lines.append(line)
                if len(excerpt_lines) >= max_lines:
                    break

            return "\n".join(excerpt_lines)
        except Exception:
            return ""


def main():
    """主函数 - 用于命令行调用"""
    scanner = PluginsScanner()
    result = scanner.scan_all()

    # 输出到标准输出
    print("\n" + "="*60)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
