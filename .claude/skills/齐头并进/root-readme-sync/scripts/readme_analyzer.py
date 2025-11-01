#!/usr/bin/env python3
"""
README统计分析引擎 - 自动扫描项目结构并生成准确统计

用途: 为root-readme-sync skill提供实时、准确的项目统计数据
作者: ZTL Digital Intelligence Operations Center
版本: 1.0.0
"""

from pathlib import Path
from typing import Dict, List
from collections import defaultdict
from datetime import datetime
import yaml
import json
import re


class ProjectAnalyzer:
    """项目结构分析器 - 实时扫描统计"""

    def __init__(self, project_root: Path):
        self.root = project_root
        self.stats = {
            'agents': defaultdict(list),      # 按业务组分类的agents
            'commands': [],                    # 全局commands
            'skills': [],                      # 全局skills
            'plugins': {},                     # 插件信息
            'mcp_servers': [],                 # MCP服务器
        }

    def scan_all_agents(self) -> Dict[str, int]:
        """扫描所有agents - 返回准确计数"""

        # 1. 扫描插件级agents
        plugins_dir = self.root / 'plugins'
        if plugins_dir.exists():
            for plugin_dir in plugins_dir.iterdir():
                if not plugin_dir.is_dir():
                    continue

                agents_dir = plugin_dir / 'agents'
                if agents_dir.exists():
                    agent_files = list(agents_dir.glob('*.md'))
                    plugin_name = plugin_dir.name
                    self.stats['agents'][plugin_name] = [
                        self._extract_agent_metadata(f) for f in agent_files
                    ]

        # 2. 扫描系统级agents (.claude/agents/)
        system_agents_dir = self.root / '.claude' / 'agents'
        if system_agents_dir.exists():
            system_agent_files = list(system_agents_dir.glob('Q*.md'))
            self.stats['agents']['系统级'] = [
                self._extract_agent_metadata(f) for f in system_agent_files
            ]

        # 3. 计算总数
        total_business_agents = sum(
            len(agents) for group, agents in self.stats['agents'].items()
            if group != '系统级'
        )
        total_system_agents = len(self.stats['agents'].get('系统级', []))

        return {
            'business_agents': total_business_agents,
            'system_agents': total_system_agents,
            'total_agents': total_business_agents + total_system_agents,
            'by_group': {
                group: len(agents)
                for group, agents in self.stats['agents'].items()
            }
        }

    def scan_all_commands(self) -> Dict[str, int]:
        """扫描所有commands - 去重计数"""
        commands_dir = self.root / '.claude' / 'commands'

        if not commands_dir.exists():
            return {'total': 0, 'commands': []}

        # 扫描所有.md文件
        command_files = list(commands_dir.glob('*.md'))

        # 提取命令名称 (去掉.md后缀)
        command_names = sorted(set(f.stem for f in command_files))

        return {
            'total': len(command_names),
            'commands': command_names
        }

    def scan_all_skills(self) -> Dict[str, int]:
        """扫描所有skills - 包括.claude/skills/和plugins/*/skills/"""
        all_skills = []

        # 1. 全局skills (.claude/skills/)
        global_skills_dir = self.root / '.claude' / 'skills'
        if global_skills_dir.exists():
            # 递归查找所有SKILL.md
            for skill_file in global_skills_dir.rglob('SKILL.md'):
                skill_name = skill_file.parent.name
                # 跳过中间目录层级,只统计有SKILL.md的目录
                all_skills.append({
                    'name': skill_name,
                    'path': str(skill_file.parent.relative_to(self.root)),
                    'type': 'global'
                })

        # 2. 插件级skills (plugins/*/skills/)
        plugins_dir = self.root / 'plugins'
        if plugins_dir.exists():
            for plugin_dir in plugins_dir.iterdir():
                if not plugin_dir.is_dir():
                    continue
                skills_dir = plugin_dir / 'skills'
                if skills_dir.exists():
                    for skill_file in skills_dir.rglob('SKILL.md'):
                        skill_name = skill_file.parent.name
                        all_skills.append({
                            'name': skill_name,
                            'path': str(skill_file.parent.relative_to(self.root)),
                            'type': f'plugin:{plugin_dir.name}'
                        })

        return {
            'total': len(all_skills),
            'skills': all_skills
        }

    def scan_mcp_servers(self) -> Dict[str, int]:
        """扫描settings.json获取MCP服务器配置"""
        settings_file = self.root / '.claude' / 'settings.json'

        if not settings_file.exists():
            return {'total': 0, 'servers': []}

        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)

            mcp_servers = settings.get('mcpServers', {})

            return {
                'total': len(mcp_servers),
                'servers': list(mcp_servers.keys())
            }
        except (json.JSONDecodeError, IOError) as e:
            return {
                'total': 0,
                'servers': [],
                'error': str(e)
            }

    def scan_plugins(self) -> Dict:
        """扫描所有业务组插件"""
        plugins = {}
        plugins_dir = self.root / 'plugins'

        if not plugins_dir.exists():
            return plugins

        for plugin_dir in plugins_dir.iterdir():
            if not plugin_dir.is_dir():
                continue

            plugin_info = self._extract_plugin_info(plugin_dir)
            plugins[plugin_dir.name] = plugin_info

        return plugins

    def generate_complete_stats(self) -> Dict:
        """生成完整项目统计 - 一次性返回所有准确数据"""
        return {
            'agents': self.scan_all_agents(),
            'commands': self.scan_all_commands(),
            'skills': self.scan_all_skills(),
            'mcp_servers': self.scan_mcp_servers(),
            'plugins': self.scan_plugins(),
            'timestamp': datetime.now().isoformat(),
            'version': self._detect_project_version()
        }

    def _extract_agent_metadata(self, agent_file: Path) -> Dict:
        """从agent文件提取元数据"""
        try:
            content = agent_file.read_text(encoding='utf-8')

            # 提取YAML frontmatter
            match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
            if match:
                metadata = yaml.safe_load(match.group(1))
                if metadata:
                    metadata['filename'] = agent_file.name
                    return metadata
        except Exception as e:
            pass

        # 如果提取失败,返回基础信息
        return {
            'filename': agent_file.name,
            'name': agent_file.stem
        }

    def _extract_plugin_info(self, plugin_dir: Path) -> Dict:
        """提取插件信息"""
        plugin_info = {
            'name': plugin_dir.name,
            'agents_count': 0,
            'commands_count': 0,
            'skills_count': 0
        }

        # 统计agents
        agents_dir = plugin_dir / 'agents'
        if agents_dir.exists():
            plugin_info['agents_count'] = len(list(agents_dir.glob('*.md')))

        # 统计commands
        commands_dir = plugin_dir / 'commands'
        if commands_dir.exists():
            plugin_info['commands_count'] = len(list(commands_dir.glob('*.md')))

        # 统计skills
        skills_dir = plugin_dir / 'skills'
        if skills_dir.exists():
            plugin_info['skills_count'] = len(list(skills_dir.rglob('SKILL.md')))

        # 读取plugin.json
        plugin_json = plugin_dir / '.claude-plugin' / 'plugin.json'
        if plugin_json.exists():
            try:
                with open(plugin_json, 'r', encoding='utf-8') as f:
                    plugin_data = json.load(f)
                    plugin_info['description'] = plugin_data.get('description', '')
            except:
                pass

        return plugin_info

    def _detect_project_version(self) -> str:
        """从README.md检测项目版本"""
        readme = self.root / 'README.md'
        if readme.exists():
            try:
                content = readme.read_text(encoding='utf-8')

                # 查找版本标记
                version_patterns = [
                    r'\*\*版本\*\*:\s*v?([\d.]+)',
                    r'\*\*Version\*\*:\s*v?([\d.]+)',
                    r'版本:\s*v?([\d.]+)'
                ]

                for pattern in version_patterns:
                    match = re.search(pattern, content)
                    if match:
                        return match.group(1)
            except:
                pass

        return '1.0.0'


def main():
    """主入口 - Claude调用此函数获取统计数据"""
    import sys

    # 获取项目根目录
    if len(sys.argv) > 1:
        project_root = Path(sys.argv[1])
    else:
        project_root = Path.cwd()

    # 创建分析器
    analyzer = ProjectAnalyzer(project_root)

    # 生成完整统计
    stats = analyzer.generate_complete_stats()

    # 输出为JSON (Claude可以解析)
    output = json.dumps(stats, ensure_ascii=False, indent=2)
    print(output)

    # 可选: 同时保存到文件
    output_file = project_root / 'output' / 'project-stats.json'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(output, encoding='utf-8')

    return stats


if __name__ == '__main__':
    main()
