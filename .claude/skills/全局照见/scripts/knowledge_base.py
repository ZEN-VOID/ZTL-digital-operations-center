#!/usr/bin/env python3
"""
知识库管理器 (Knowledge Base Manager)

功能：
1. 加载/保存插件索引文件
2. 提供结构化查询接口
3. 生成Markdown格式的报告
4. 支持多种查询模式
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class KnowledgeBase:
    """全局插件知识库管理器"""

    def __init__(self, knowledge_dir: Optional[Path] = None):
        """
        初始化知识库

        Args:
            knowledge_dir: 知识库目录路径，默认为当前技能包的knowledge目录
        """
        if knowledge_dir is None:
            # 默认路径：.claude/skills/全局照见/knowledge/
            skill_dir = Path(__file__).parent.parent
            knowledge_dir = skill_dir / "knowledge"

        self.knowledge_dir = knowledge_dir
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)

        # 索引文件路径
        self.plugins_registry_file = self.knowledge_dir / "plugins_registry.json"
        self.skills_index_file = self.knowledge_dir / "skills_index.json"
        self.last_sync_file = self.knowledge_dir / "last_sync.json"

    def save_plugins_registry(self, registry: Dict[str, Any]):
        """保存插件注册表"""
        with open(self.plugins_registry_file, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)
        print(f"✅ 插件注册表已保存: {self.plugins_registry_file}")

    def load_plugins_registry(self) -> Optional[Dict[str, Any]]:
        """加载插件注册表"""
        if not self.plugins_registry_file.exists():
            return None

        try:
            with open(self.plugins_registry_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  加载插件注册表失败: {e}")
            return None

    def save_skills_index(self, skills_index: Dict[str, Any]):
        """保存技能包索引"""
        with open(self.skills_index_file, 'w', encoding='utf-8') as f:
            json.dump(skills_index, f, indent=2, ensure_ascii=False)
        print(f"✅ 技能包索引已保存: {self.skills_index_file}")

    def load_skills_index(self) -> Optional[Dict[str, Any]]:
        """加载技能包索引"""
        if not self.skills_index_file.exists():
            return None

        try:
            with open(self.skills_index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  加载技能包索引失败: {e}")
            return None

    def save_sync_record(self, sync_info: Dict[str, Any]):
        """保存同步记录"""
        with open(self.last_sync_file, 'w', encoding='utf-8') as f:
            json.dump(sync_info, f, indent=2, ensure_ascii=False)

    def load_sync_record(self) -> Optional[Dict[str, Any]]:
        """加载同步记录"""
        if not self.last_sync_file.exists():
            return None

        try:
            with open(self.last_sync_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  加载同步记录失败: {e}")
            return None

    def build_skills_index(self, registry: Dict[str, Any]) -> Dict[str, Any]:
        """
        从插件注册表构建技能包索引

        Args:
            registry: 插件注册表

        Returns:
            技能包索引
        """
        skills_index = {
            "build_time": datetime.now().isoformat(),
            "total_skills": 0,
            "skills": {}
        }

        for plugin_id, plugin_data in registry.get("plugins", {}).items():
            for skill in plugin_data.get("skills", []):
                skill_id = skill.get("skill_id")
                if not skill_id:
                    continue

                # 添加来源信息
                skill["plugin_id"] = plugin_id
                skill["plugin_source"] = plugin_data.get("source", "unknown")

                skills_index["skills"][skill_id] = skill
                skills_index["total_skills"] += 1

        return skills_index

    def query_all_plugins(self) -> str:
        """查询所有插件，返回Markdown格式"""
        registry = self.load_plugins_registry()
        if not registry:
            return "⚠️ 知识库未初始化，请先运行同步。"

        output = ["# 全局插件清单\n"]
        output.append(f"**扫描时间**: {registry.get('scan_time', 'Unknown')}\n")
        output.append(f"**总插件数**: {registry.get('total_plugins', 0)}")
        output.append(f"**已启用**: {registry.get('enabled_plugins', 0)}")
        output.append(f"**总技能包**: {registry.get('total_skills', 0)}")
        output.append(f"**总智能体**: {registry.get('total_agents', 0)}\n")

        plugins = registry.get("plugins", {})
        for i, (plugin_id, plugin_data) in enumerate(plugins.items(), 1):
            output.append(f"\n## {i}. {plugin_id}")
            output.append(f"- **状态**: {'✅ 已启用' if plugin_data['enabled'] else '⏸️  已禁用'}")
            output.append(f"- **版本**: {plugin_data['version']}")
            output.append(f"- **来源**: {plugin_data['source']}")
            output.append(f"- **安装位置**: `{plugin_data['install_path']}`")
            output.append(f"- **最后更新**: {plugin_data['last_updated']}")

            skills = plugin_data.get("skills", [])
            if skills:
                output.append(f"\n**技能包** ({len(skills)}个):")
                for skill in skills:
                    output.append(f"- **{skill['skill_id']}** - {skill['description'][:100]}...")

            agents = plugin_data.get("agents", [])
            if agents:
                output.append(f"\n**智能体** ({len(agents)}个):")
                for agent in agents[:5]:  # 只显示前5个
                    output.append(f"- {agent.get('agent_id', 'Unknown')}")

        return "\n".join(output)

    def query_plugin_by_id(self, plugin_id: str) -> str:
        """查询特定插件的详细信息"""
        registry = self.load_plugins_registry()
        if not registry:
            return "⚠️ 知识库未初始化，请先运行同步。"

        plugin_data = registry.get("plugins", {}).get(plugin_id)
        if not plugin_data:
            return f"⚠️ 未找到插件: {plugin_id}"

        output = [f"# {plugin_id}\n"]
        output.append(f"**状态**: {'✅ 已启用' if plugin_data['enabled'] else '⏸️  已禁用'}")
        output.append(f"**版本**: {plugin_data['version']}")
        output.append(f"**来源**: {plugin_data['source']}")
        output.append(f"**安装位置**: `{plugin_data['install_path']}`")
        output.append(f"**最后更新**: {plugin_data['last_updated']}")
        output.append(f"**Git Commit**: `{plugin_data.get('git_commit_sha', 'N/A')[:8]}`\n")

        # README摘要
        readme_excerpt = plugin_data.get("metadata", {}).get("readme_excerpt")
        if readme_excerpt:
            output.append("## 简介\n")
            output.append(readme_excerpt)
            output.append("")

        # 技能包列表
        skills = plugin_data.get("skills", [])
        if skills:
            output.append(f"## 技能包 ({len(skills)}个)\n")
            for skill in skills:
                output.append(f"### {skill['display_name']}")
                output.append(f"**ID**: `{skill['skill_id']}`")
                output.append(f"**描述**: {skill['description']}")
                if skill.get('allowed_tools'):
                    output.append(f"**工具**: {skill['allowed_tools']}")
                output.append("")

        # 智能体列表
        agents = plugin_data.get("agents", [])
        if agents:
            output.append(f"## 智能体 ({len(agents)}个)\n")
            for agent in agents:
                output.append(f"- **{agent.get('agent_id')}**: {agent.get('name', 'N/A')}")

        # 命令列表
        commands = plugin_data.get("commands", [])
        if commands:
            output.append(f"\n## 命令 ({len(commands)}个)\n")
            for cmd in commands:
                output.append(f"- **/{cmd['command_id']}**: {cmd.get('description', 'N/A')}")

        return "\n".join(output)

    def query_skill_by_id(self, skill_id: str) -> str:
        """查询特定技能包的详细信息"""
        skills_index = self.load_skills_index()
        if not skills_index:
            return "⚠️ 技能包索引未初始化，请先运行同步。"

        skill = skills_index.get("skills", {}).get(skill_id)
        if not skill:
            return f"⚠️ 未找到技能包: {skill_id}"

        output = [f"# {skill['display_name']}\n"]
        output.append(f"**ID**: `{skill['skill_id']}`")
        output.append(f"**所属插件**: {skill['plugin_id']}")
        output.append(f"**来源**: {skill['plugin_source']}")
        output.append(f"**描述**: {skill['description']}")

        if skill.get('allowed_tools'):
            output.append(f"\n**允许的工具**:")
            output.append(f"```\n{skill['allowed_tools']}\n```")

        output.append(f"\n**文件路径**: `{skill['file_path']}`")

        return "\n".join(output)

    def search_skills(self, keyword: str) -> str:
        """搜索包含特定关键词的技能包"""
        skills_index = self.load_skills_index()
        if not skills_index:
            return "⚠️ 技能包索引未初始化，请先运行同步。"

        keyword_lower = keyword.lower()
        matches = []

        for skill_id, skill in skills_index.get("skills", {}).items():
            # 搜索skill_id、display_name、description
            if (keyword_lower in skill_id.lower() or
                keyword_lower in skill.get("display_name", "").lower() or
                keyword_lower in skill.get("description", "").lower()):
                matches.append(skill)

        if not matches:
            return f"⚠️ 未找到包含关键词 '{keyword}' 的技能包。"

        output = [f"# 搜索结果: '{keyword}'\n"]
        output.append(f"找到 {len(matches)} 个匹配的技能包:\n")

        for skill in matches:
            output.append(f"## {skill['display_name']}")
            output.append(f"**ID**: `{skill['skill_id']}`")
            output.append(f"**插件**: {skill['plugin_id']}")
            output.append(f"**描述**: {skill['description'][:150]}...")
            output.append("")

        return "\n".join(output)

    def generate_summary_report(self) -> str:
        """生成摘要报告"""
        registry = self.load_plugins_registry()
        sync_record = self.load_sync_record()

        if not registry:
            return "⚠️ 知识库未初始化，请先运行同步。"

        output = ["# 全局插件摘要报告\n"]

        # 统计信息
        output.append("## 📊 统计信息\n")
        output.append(f"- **总插件数**: {registry.get('total_plugins', 0)}")
        output.append(f"- **已启用**: {registry.get('enabled_plugins', 0)}")
        output.append(f"- **总技能包**: {registry.get('total_skills', 0)}")
        output.append(f"- **总智能体**: {registry.get('total_agents', 0)}")
        output.append(f"- **扫描时间**: {registry.get('scan_time', 'Unknown')}")

        if sync_record:
            output.append(f"- **最后同步**: {sync_record.get('sync_time', 'Unknown')}")

        # 插件列表
        output.append("\n## 📦 已安装插件\n")
        plugins = registry.get("plugins", {})

        for plugin_id, plugin_data in plugins.items():
            status = "✅" if plugin_data['enabled'] else "⏸️ "
            skills_count = len(plugin_data.get("skills", []))
            output.append(f"- {status} **{plugin_id}** (v{plugin_data['version']}) - {skills_count} 个技能包")

        # 技能包分类
        output.append("\n## 🎯 技能包分类\n")
        all_skills = []
        for plugin_data in plugins.values():
            all_skills.extend(plugin_data.get("skills", []))

        if all_skills:
            output.append(f"共 {len(all_skills)} 个技能包:\n")
            for skill in all_skills[:10]:  # 显示前10个
                output.append(f"- **{skill['skill_id']}** ({skill.get('plugin_id', 'Unknown')})")

            if len(all_skills) > 10:
                output.append(f"\n... 还有 {len(all_skills) - 10} 个技能包未列出")

        return "\n".join(output)


def main():
    """主函数 - 用于命令行测试"""
    kb = KnowledgeBase()

    # 测试查询
    print("="*60)
    print("测试查询所有插件:")
    print(kb.query_all_plugins())

    print("\n" + "="*60)
    print("测试摘要报告:")
    print(kb.generate_summary_report())


if __name__ == "__main__":
    main()
