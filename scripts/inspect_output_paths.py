#!/usr/bin/env python3
"""
巡检并修复 agents 和 skills 中的输出路径规范
检查是否使用了旧的子目录模式 (plans/, results/, logs/, metadata/)
"""

import re
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PathIssue:
    """路径问题记录"""
    file_path: str
    line_number: int
    old_pattern: str
    suggested_fix: str
    context: str


class OutputPathInspector:
    """输出路径巡检器"""

    # 旧的子目录模式
    OLD_SUBDIR_PATTERNS = [
        r'output/.*?/plans/',
        r'output/.*?/results/',
        r'output/.*?/logs/',
        r'output/.*?/metadata/',
    ]

    def __init__(self):
        self.issues: List[PathIssue] = []
        self.stats = {
            'total_files': 0,
            'files_with_issues': 0,
            'total_issues': 0,
            'by_pattern': {}
        }

    def inspect_file(self, file_path: Path) -> List[PathIssue]:
        """巡检单个文件"""
        file_issues = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, 1):
                for pattern in self.OLD_SUBDIR_PATTERNS:
                    matches = re.finditer(pattern, line)
                    for match in matches:
                        old_text = match.group(0)

                        # 生成修复建议
                        suggested = self._generate_fix(old_text)

                        issue = PathIssue(
                            file_path=str(file_path),
                            line_number=line_num,
                            old_pattern=old_text,
                            suggested_fix=suggested,
                            context=line.strip()
                        )
                        file_issues.append(issue)

                        # 统计
                        pattern_key = old_text.split('/')[-2] + '/'
                        self.stats['by_pattern'][pattern_key] = \
                            self.stats['by_pattern'].get(pattern_key, 0) + 1

            if file_issues:
                self.stats['files_with_issues'] += 1
                self.stats['total_issues'] += len(file_issues)

        except Exception as e:
            print(f"⚠️  读取文件失败: {file_path} - {e}")

        return file_issues

    def _generate_fix(self, old_path: str) -> str:
        """生成修复建议"""
        # 移除子目录,保留基础路径
        base_path = re.sub(r'/(plans|results|logs|metadata)/', '/', old_path)

        # 根据子目录类型添加文件名前缀建议
        if '/plans/' in old_path:
            return f"{base_path}plan_*.json"
        elif '/results/' in old_path:
            return f"{base_path}*.png (或其他结果文件)"
        elif '/logs/' in old_path:
            return f"{base_path}log_*.txt"
        elif '/metadata/' in old_path:
            return f"{base_path}metadata_*.json"

        return base_path

    def inspect_agents(self, base_path: Path = Path("plugins")) -> Dict:
        """巡检所有 agents 文件"""
        print("🔍 开始巡检 agents 文件...")

        agent_files = list(base_path.glob("*/agents/*.md"))
        self.stats['total_files'] += len(agent_files)

        for agent_file in agent_files:
            issues = self.inspect_file(agent_file)
            self.issues.extend(issues)

        print(f"✅ agents 巡检完成: {len(agent_files)} 个文件")
        return self.stats

    def inspect_skills(self, base_path: Path = Path(".claude/skills")) -> Dict:
        """巡检所有 skills 文件"""
        print("\n🔍 开始巡检 skills 文件...")

        skill_files = list(base_path.glob("*/*/SKILL.md"))
        self.stats['total_files'] += len(skill_files)

        for skill_file in skill_files:
            issues = self.inspect_file(skill_file)
            self.issues.extend(issues)

        print(f"✅ skills 巡检完成: {len(skill_files)} 个文件")
        return self.stats

    def generate_report(self, output_file: Path = Path("reports/path-inspection-report.md")):
        """生成巡检报告"""
        output_file.parent.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 输出路径规范巡检报告\n\n")
            f.write(f"**巡检时间**: {timestamp}\n\n")

            # 统计摘要
            f.write("## 📊 统计摘要\n\n")
            f.write(f"- **总文件数**: {self.stats['total_files']}\n")
            f.write(f"- **存在问题的文件数**: {self.stats['files_with_issues']}\n")
            f.write(f"- **问题总数**: {self.stats['total_issues']}\n\n")

            # 按问题类型统计
            f.write("### 问题类型分布\n\n")
            for pattern, count in sorted(self.stats['by_pattern'].items(),
                                        key=lambda x: x[1], reverse=True):
                f.write(f"- `{pattern}`: {count} 处\n")

            # 详细问题列表
            f.write("\n## 📝 详细问题列表\n\n")

            # 按文件分组
            issues_by_file = {}
            for issue in self.issues:
                if issue.file_path not in issues_by_file:
                    issues_by_file[issue.file_path] = []
                issues_by_file[issue.file_path].append(issue)

            for file_path, file_issues in sorted(issues_by_file.items()):
                f.write(f"### {file_path}\n\n")
                f.write(f"发现 {len(file_issues)} 处问题:\n\n")

                for issue in file_issues:
                    f.write(f"**行 {issue.line_number}**:\n")
                    f.write(f"- 旧模式: `{issue.old_pattern}`\n")
                    f.write(f"- 建议修复: `{issue.suggested_fix}`\n")
                    f.write(f"- 上下文: `{issue.context[:80]}...`\n\n")

            # 修复建议
            f.write("\n## 🔧 修复建议\n\n")
            f.write("### 统一修复规则\n\n")
            f.write("1. **移除所有子目录**: 不再使用 `plans/`, `results/`, `logs/`, `metadata/`\n")
            f.write("2. **使用文件名前缀区分类型**:\n")
            f.write("   - 计划文件: `plan_*.json`\n")
            f.write("   - 结果文件: `*.png`, `*.pdf` 等(直接使用描述性名称)\n")
            f.write("   - 日志文件: `log_*.txt`\n")
            f.write("   - 元数据: `metadata_*.json`\n\n")
            f.write("3. **标准路径格式**: `output/[项目名]/[agent或skill名]/[文件名]`\n\n")

            f.write("### 批量修复命令\n\n")
            f.write("```bash\n")
            f.write("# 替换 /plans/ 为 /\n")
            f.write("find plugins .claude/skills -name '*.md' -exec sed -i '' 's|/plans/|/|g' {} +\n\n")
            f.write("# 替换 /results/ 为 /\n")
            f.write("find plugins .claude/skills -name '*.md' -exec sed -i '' 's|/results/|/|g' {} +\n\n")
            f.write("# 替换 /logs/ 为 /\n")
            f.write("find plugins .claude/skills -name '*.md' -exec sed -i '' 's|/logs/|/|g' {} +\n\n")
            f.write("# 替换 /metadata/ 为 /\n")
            f.write("find plugins .claude/skills -name '*.md' -exec sed -i '' 's|/metadata/|/|g' {} +\n")
            f.write("```\n\n")

            f.write("### 手动修复检查清单\n\n")
            f.write("修复后需要检查:\n\n")
            f.write("- [ ] 所有示例路径已移除子目录\n")
            f.write("- [ ] 文件命名示例包含正确的前缀 (plan_, log_, etc.)\n")
            f.write("- [ ] 文档说明已更新为新的路径规范\n")
            f.write("- [ ] 代码示例中的路径已更新\n")

        print(f"\n📄 报告已生成: {output_file}")
        return output_file


def main():
    """主函数"""
    inspector = OutputPathInspector()

    # 巡检 agents
    inspector.inspect_agents()

    # 巡检 skills
    inspector.inspect_skills()

    # 生成报告
    report_file = inspector.generate_report()

    # 打印摘要
    print(f"\n{'='*60}")
    print("📊 巡检统计摘要")
    print(f"{'='*60}")
    print(f"总文件数: {inspector.stats['total_files']}")
    print(f"存在问题的文件数: {inspector.stats['files_with_issues']}")
    print(f"问题总数: {inspector.stats['total_issues']}")
    print(f"\n问题类型分布:")
    for pattern, count in sorted(inspector.stats['by_pattern'].items(),
                                key=lambda x: x[1], reverse=True):
        print(f"  - {pattern}: {count} 处")
    print(f"\n详细报告: {report_file}")


if __name__ == "__main__":
    main()
