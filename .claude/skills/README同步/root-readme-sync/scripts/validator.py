#!/usr/bin/env python3
"""
README准确性验证器 - 验证README中的统计数据与实际项目状态一致

用途: 在生成README后运行,确保所有统计信息准确无误
作者: ZTL Digital Intelligence Operations Center
版本: 1.0.0
"""

from pathlib import Path
from typing import List, Dict, Tuple
import re
import json


class READMEValidator:
    """README准确性验证器"""

    def __init__(self, readme_path: Path, project_root: Path):
        self.readme = readme_path
        self.root = project_root
        self.errors = []
        self.warnings = []
        self.info = []

    def validate_all(self) -> bool:
        """运行所有验证检查"""
        print("🔍 开始验证README准确性...\n")

        self.validate_agent_counts()
        self.validate_command_counts()
        self.validate_skill_counts()
        self.validate_plugin_table()
        self.validate_links()
        self.validate_markdown_syntax()

        return len(self.errors) == 0

    def validate_agent_counts(self):
        """验证agent计数准确性"""
        content = self.readme.read_text(encoding='utf-8')

        # 1. 提取README中声明的总数
        declared_match = re.search(r'\*\*(\d+)个专业智能体\*\*', content)
        if not declared_match:
            self.errors.append("❌ 未找到智能体总数声明 (格式: **XX个专业智能体**)")
            return

        declared_total = int(declared_match.group(1))

        # 2. 实际扫描计数
        actual_business = self._count_business_agents()
        actual_system = self._count_system_agents()
        actual_total = actual_business + actual_system

        # 3. 对比验证
        if declared_total != actual_total:
            self.errors.append(
                f"❌ 智能体总数不准确:\n"
                f"   README声明: {declared_total}个\n"
                f"   实际统计: {actual_total}个 (业务组{actual_business} + 系统级{actual_system})"
            )
        else:
            self.info.append(f"✅ 智能体总数准确: {actual_total}个")

        # 4. 验证业务组/系统级智能体分类声明
        declared_breakdown = re.search(
            r'(\d+)个业务组智能体\s*\+\s*(\d+)个系统级智能体',
            content
        )
        if declared_breakdown:
            declared_business = int(declared_breakdown.group(1))
            declared_system = int(declared_breakdown.group(2))

            if declared_business != actual_business or declared_system != actual_system:
                self.errors.append(
                    f"❌ 智能体分类不准确:\n"
                    f"   README声明: {declared_business}个业务组 + {declared_system}个系统级\n"
                    f"   实际统计: {actual_business}个业务组 + {actual_system}个系统级"
                )
        else:
            self.warnings.append("⚠️  未找到智能体分类声明 (业务组 + 系统级)")

    def validate_command_counts(self):
        """验证command计数"""
        content = self.readme.read_text(encoding='utf-8')

        # 从README提取声明
        declared_match = re.search(r'\*\*(\d+)个斜杠命令\*\*', content)
        if not declared_match:
            self.errors.append("❌ 未找到命令数量声明 (格式: **XX个斜杠命令**)")
            return

        declared_count = int(declared_match.group(1))

        # 实际扫描
        commands_dir = self.root / '.claude' / 'commands'
        if not commands_dir.exists():
            actual_count = 0
        else:
            actual_count = len(list(commands_dir.glob('*.md')))

        if declared_count != actual_count:
            self.errors.append(
                f"❌ 命令数量不准确:\n"
                f"   README声明: {declared_count}个\n"
                f"   实际统计: {actual_count}个"
            )
        else:
            self.info.append(f"✅ 命令数量准确: {actual_count}个")

    def validate_skill_counts(self):
        """验证skill计数"""
        content = self.readme.read_text(encoding='utf-8')

        # 从README提取声明
        declared_match = re.search(r'\*\*(\d+)个技能包\*\*', content)
        if not declared_match:
            self.warnings.append("⚠️  未找到技能包数量声明")
            return

        declared_count = int(declared_match.group(1))

        # 实际扫描
        actual_count = self._count_all_skills()

        if declared_count != actual_count:
            self.errors.append(
                f"❌ 技能包数量不准确:\n"
                f"   README声明: {declared_count}个\n"
                f"   实际统计: {actual_count}个"
            )
        else:
            self.info.append(f"✅ 技能包数量准确: {actual_count}个")

    def validate_plugin_table(self):
        """验证业务组表格数据"""
        content = self.readme.read_text(encoding='utf-8')

        # 查找业务组表格
        # 格式: | **战略组** (Strategy) | 9个 | ...
        plugin_table_pattern = r'\|\s*\*\*(.+?)\*\*.*?\|\s*(\d+)个\s*\|'
        matches = re.findall(plugin_table_pattern, content)

        if not matches:
            self.warnings.append("⚠️  未找到业务组表格")
            return

        # 实际统计各组agents数量
        actual_counts = {}
        plugins_dir = self.root / 'plugins'

        if plugins_dir.exists():
            for plugin_dir in plugins_dir.iterdir():
                if not plugin_dir.is_dir():
                    continue
                agents_dir = plugin_dir / 'agents'
                if agents_dir.exists():
                    count = len(list(agents_dir.glob('*.md')))
                    actual_counts[plugin_dir.name] = count

        # 系统级agents
        system_agents_dir = self.root / '.claude' / 'agents'
        if system_agents_dir.exists():
            actual_counts['系统级'] = len(list(system_agents_dir.glob('Q*.md')))

        # 对比验证
        table_errors = []
        for group_name, declared_count in matches:
            # 清理组名 (去掉括号内容)
            clean_name = re.sub(r'\s*\([^)]+\)', '', group_name).strip()

            # 查找对应的实际统计
            found = False
            for actual_name, actual_count in actual_counts.items():
                if clean_name in actual_name or actual_name in clean_name:
                    if int(declared_count) != actual_count:
                        table_errors.append(
                            f"  • {clean_name}: 声明{declared_count}个, 实际{actual_count}个"
                        )
                    found = True
                    break

            if not found and clean_name != '系统级':
                self.warnings.append(f"⚠️  表格中的'{clean_name}'在实际目录中未找到")

        if table_errors:
            self.errors.append(
                "❌ 业务组表格数据不准确:\n" + "\n".join(table_errors)
            )
        else:
            self.info.append("✅ 业务组表格数据准确")

    def validate_links(self):
        """验证内部链接有效性"""
        content = self.readme.read_text(encoding='utf-8')

        # 查找markdown链接: [text](path)
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        matches = re.findall(link_pattern, content)

        broken_links = []
        for link_text, link_path in matches:
            # 跳过外部链接
            if link_path.startswith(('http://', 'https://', '#')):
                continue

            # 检查文件是否存在
            full_path = self.root / link_path
            if not full_path.exists():
                broken_links.append(f"  • [{link_text}]({link_path})")

        if broken_links:
            self.warnings.append(
                "⚠️  发现失效链接:\n" + "\n".join(broken_links)
            )
        else:
            self.info.append("✅ 所有内部链接有效")

    def validate_markdown_syntax(self):
        """基础Markdown语法检查"""
        content = self.readme.read_text(encoding='utf-8')

        # 检查标题层级
        lines = content.split('\n')
        prev_level = 0
        for i, line in enumerate(lines, 1):
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                if level > prev_level + 1 and prev_level > 0:
                    self.warnings.append(
                        f"⚠️  第{i}行: 标题层级跳跃 (从H{prev_level}跳到H{level})"
                    )
                prev_level = level

        self.info.append("✅ Markdown语法检查完成")

    def _count_business_agents(self) -> int:
        """扫描业务组agents"""
        total = 0
        plugins_dir = self.root / 'plugins'

        if not plugins_dir.exists():
            return 0

        for plugin_dir in plugins_dir.iterdir():
            if not plugin_dir.is_dir():
                continue
            agents_dir = plugin_dir / 'agents'
            if agents_dir.exists():
                total += len(list(agents_dir.glob('*.md')))

        return total

    def _count_system_agents(self) -> int:
        """扫描系统级agents"""
        system_dir = self.root / '.claude' / 'agents'
        if system_dir.exists():
            return len(list(system_dir.glob('Q*.md')))
        return 0

    def _count_all_skills(self) -> int:
        """扫描所有skills"""
        total = 0

        # 全局skills
        global_skills = self.root / '.claude' / 'skills'
        if global_skills.exists():
            total += len(list(global_skills.rglob('SKILL.md')))

        # 插件skills
        plugins_dir = self.root / 'plugins'
        if plugins_dir.exists():
            for plugin_dir in plugins_dir.iterdir():
                if not plugin_dir.is_dir():
                    continue
                skills_dir = plugin_dir / 'skills'
                if skills_dir.exists():
                    total += len(list(skills_dir.rglob('SKILL.md')))

        return total

    def report(self):
        """生成验证报告"""
        print("\n" + "="*70)
        print("📊 README准确性验证报告")
        print("="*70)

        if self.errors:
            print(f"\n❌ 发现 {len(self.errors)} 个错误:\n")
            for error in self.errors:
                print(error)
                print()

        if self.warnings:
            print(f"\n⚠️  发现 {len(self.warnings)} 个警告:\n")
            for warning in self.warnings:
                print(warning)

        if self.info:
            print(f"\n✅ 验证通过的项目 ({len(self.info)}个):\n")
            for info in self.info:
                print(info)

        print("\n" + "="*70)

        if not self.errors and not self.warnings:
            print("✨ 完美! README信息准确无误,所有检查通过。")
        elif not self.errors:
            print("✅ 验证通过! 仅有少量警告,不影响准确性。")
        else:
            print("❌ 验证失败! 请修正上述错误后重新生成README。")

        print("="*70 + "\n")


def main():
    """主入口"""
    import sys

    # 获取参数
    if len(sys.argv) > 1:
        readme_path = Path(sys.argv[1])
    else:
        readme_path = Path.cwd() / 'README.md'

    if len(sys.argv) > 2:
        project_root = Path(sys.argv[2])
    else:
        project_root = Path.cwd()

    # 运行验证
    validator = READMEValidator(readme_path, project_root)
    is_valid = validator.validate_all()
    validator.report()

    # 返回退出码
    sys.exit(0 if is_valid else 1)


if __name__ == '__main__':
    main()
