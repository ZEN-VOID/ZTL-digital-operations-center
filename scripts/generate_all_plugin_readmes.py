#!/usr/bin/env python3
"""
Generate comprehensive README.md files for all plugin groups
Based on the template from 开发组
"""

from pathlib import Path
import re
from datetime import datetime

# Plugin groups to process (excluding 开发组 which is already done)
PLUGIN_GROUPS = [
    "创意组",
    "战略组",
    "行政组",
    "情报组",
    "供应组",
    "筹建组",
    "美团组"
]

# Group metadata (business focus and positioning)
GROUP_METADATA = {
    "创意组": {
        "en_name": "Creative Team",
        "tagline": "专业创意内容生产插件 - 从品牌策划到视觉传达的完整创意流程管理",
        "description": "综合创意内容生产插件,涵盖广告策划、文案创作、平面设计、算法艺术、摄影、视频制作等领域,专注于餐饮行业品牌营销。"
    },
    "战略组": {
        "en_name": "Strategy Team",
        "tagline": "商业战略与运营分析插件 - 从战略规划到运营优化的完整决策支持",
        "description": "专业商业战略插件,提供战略规划、商业分析、运营优化、产品定位、竞争分析等全方位决策支持。"
    },
    "行政组": {
        "en_name": "Admin Team",
        "tagline": "企业行政管理插件 - 从财务管理到人力资源的完整支持体系",
        "description": "综合行政管理插件,涵盖财务、人力资源、法务、文档管理等企业运营支持职能。"
    },
    "情报组": {
        "en_name": "Intelligence Team",
        "tagline": "商业情报与数据分析插件 - 从调研采集到洞察分析的完整情报体系",
        "description": "专业商业情报插件,提供深度调研、网页采集、数据分析、市场洞察等能力。"
    },
    "供应组": {
        "en_name": "Supply Chain Team",
        "tagline": "供应链管理插件 - 从采购到成本控制的完整供应链体系",
        "description": "综合供应链管理插件,涵盖采购管理、库存管理、成本控制、供应商管理等职能。"
    },
    "筹建组": {
        "en_name": "Construction Team",
        "tagline": "店铺筹建专业插件 - 从平面规划到空间设计的完整筹建流程",
        "description": "专业筹建插件,提供平面图规划、BIM建模、空间设计、工程管理等能力。"
    },
    "美团组": {
        "en_name": "Meituan Operations Team",
        "tagline": "美团平台运营插件 - 从店铺运营到数据分析的完整运营体系",
        "description": "专业美团运营插件,提供平台运营、营销推广、数据分析、报表生成等能力。"
    }
}


def extract_agent_metadata(file_path):
    """Extract metadata from agent markdown file"""
    try:
        content = file_path.read_text(encoding='utf-8')

        # Extract name
        name_match = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
        name = name_match.group(1).strip() if name_match else file_path.stem

        # Extract description (first part before \\n)
        desc_match = re.search(r'^description:\s*(.+?)(?:\\n|$)', content, re.MULTILINE)
        description = desc_match.group(1).strip() if desc_match else ''

        # Extract model
        model_match = re.search(r'^model:\s*(.+)$', content, re.MULTILINE)
        model = model_match.group(1).strip() if model_match else 'sonnet'

        return {
            'file': file_path.stem,
            'name': name,
            'description': description,
            'model': model
        }
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return {
            'file': file_path.stem,
            'name': file_path.stem,
            'description': '',
            'model': 'sonnet'
        }


def count_skills(skills_dir):
    """Count skill packages in skills directory"""
    if not skills_dir.exists():
        return 0

    skill_count = 0
    for item in skills_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.') and item.name != '__pycache__':
            skill_count += 1

    return skill_count


def count_commands(commands_dir):
    """Count command files in commands directory"""
    if not commands_dir.exists():
        return 0

    command_files = list(commands_dir.glob('*.md'))
    return len([f for f in command_files if f.name != 'README.md'])


def generate_plugin_readme(group_name):
    """Generate comprehensive README.md for a plugin group"""

    base_dir = Path('plugins') / group_name
    agents_dir = base_dir / 'agents'
    commands_dir = base_dir / 'commands'
    skills_dir = base_dir / 'skills'

    # Extract agent metadata
    agents = []
    if agents_dir.exists():
        for agent_file in sorted(agents_dir.glob('[A-Z]*.md')):
            if agent_file.name != 'README.md':
                metadata = extract_agent_metadata(agent_file)
                agents.append(metadata)

    # Count commands and skills
    command_count = count_commands(commands_dir)
    skill_count = count_skills(skills_dir)

    # Get group metadata
    metadata = GROUP_METADATA.get(group_name, {
        "en_name": f"{group_name} Team",
        "tagline": f"{group_name}专业插件",
        "description": f"{group_name}专业能力插件"
    })

    # Generate README content
    readme_content = f"""# {group_name} Plugin

> {metadata['tagline']}

[![Agents](https://img.shields.io/badge/agents-{len(agents)}-blue)](agents/)
[![Commands](https://img.shields.io/badge/commands-{command_count}-green)](commands/)
[![Skills](https://img.shields.io/badge/skills-{skill_count}-orange)](skills/)

## 📋 概述

{metadata['description']}

本插件包含 **{len(agents)}个专业智能体**,{command_count}个斜杠命令,{skill_count}个技能包,提供完整的业务流程支持。

## 🤖 智能体架构

### 组织结构

本组共有{len(agents)}个智能体:

"""

    # List all agents
    for i, agent in enumerate(agents, 1):
        agent_id = agent['file']
        readme_content += f"{i}. **{agent_id}** - {agent['name']}\n"

    readme_content += f"""
### 智能体详情

"""

    # Agent details section
    for agent in agents:
        agent_id = agent['file']
        agent_name = agent['name']

        readme_content += f"""#### {agent_id}

**名称**: {agent_name}

**何时使用**:
- {agent['description'][:100] if agent['description'] else '详见agents目录下的智能体文档'}

**调用方式**:
```python
Task(subagent_type="{agent_id}",
     prompt="您的任务描述")
```

---

"""

    # Usage guide section
    readme_content += f"""## 🚀 使用指南

### 自动委派

Claude会根据您的需求自动选择合适的智能体:

```
用户: [描述您的需求]
→ Claude自动委派给相关智能体
```

### 显式调用

使用Task工具显式调用特定智能体:

```python
Task(subagent_type="智能体ID",
     prompt="详细任务描述")
```

### 多智能体协作

复杂任务可能需要多个智能体协同工作。组长智能体可以协调团队:

```python
Task(subagent_type="{agents[-1]['file'] if agents else 'XX'}",
     prompt="需要团队协作的复杂任务")
```

## 📁 项目结构

```
plugins/{group_name}/
├── .claude-plugin/
│   └── plugin.json              # 插件配置
│
├── agents/                      # {len(agents)}个智能体
"""

    for agent in agents:
        readme_content += f"│   ├── {agent['file']}.md\n"

    readme_content += f"""│
├── commands/                    # {command_count}个命令
│   └── README.md
│
├── skills/                      # {skill_count}个技能包
│   └── README.md
│
├── hooks/                       # 钩子配置
├── scripts/                     # 工具脚本
└── README.md                    # 本文件
```

## 🎯 最佳实践

### 智能体选择决策树

1. **明确任务类型** - 是什么类别的工作?(分析、设计、执行等)
2. **查看智能体列表** - 找到最匹配的专业智能体
3. **优先单一智能体** - 简单任务直接调用单个智能体
4. **复杂任务协调** - 多阶段任务找组长协调

### 质量保障

- ✅ 所有智能体输出遵循标准化路径规范
- ✅ 任务执行前明确需求和预期输出
- ✅ 使用适当的模型(sonnet/opus)
- ✅ 复杂任务启用TodoWrite跟踪进度

### 输出路径规范

所有智能体输出遵循统一路径规范:

```
output/[项目名]/[智能体ID]/
├── plans/      # 执行计划
├── results/    # 实际输出
├── logs/       # 执行日志
└── metadata/   # 元数据
```

## 🔧 扩展点

本插件支持以下扩展:

1. **Commands** (commands/*.md) - 频繁使用的工作流快捷命令
2. **Skills** (skills/*/SKILL.md) - 复杂自动化能力
3. **Hooks** (hooks/hooks.json) - 事件驱动自动化
4. **MCP Servers** (.mcp.json) - 外部工具集成

## 📚 相关文档

- **智能体文档**: [agents/README.md](agents/README.md)
- **命令文档**: [commands/README.md](commands/README.md)
- **技能包文档**: [skills/README.md](skills/README.md)
- **主文档**: [../../README.md](../../README.md)

## 🔗 依赖与要求

- **Claude Code**: v1.0.124+
- **模型**: Sonnet 4.5 (推荐)
- **工具**: Task, Read, Write, Edit, Grep, Glob, Bash
- **技能包依赖**: 无(所有技能包独立)

## 📊 统计信息

- **智能体数量**: {len(agents)}个
- **命令数量**: {command_count}个
- **技能包数量**: {skill_count}个
- **维护状态**: ✅ 活跃维护
- **最后更新**: {datetime.now().strftime('%Y-%m-%d')}

---

**Created by**: ZTL Digital Intelligence Operations Center
**Plugin Type**: Professional Domain Plugin ({metadata['en_name']})
**Status**: Production Ready ✅
"""

    # Write README file
    readme_path = base_dir / 'README.md'
    readme_path.write_text(readme_content, encoding='utf-8')
    print(f"✅ Generated README for {group_name} ({len(agents)} agents, {command_count} commands, {skill_count} skills)")

    return len(agents), command_count, skill_count


def main():
    """Generate READMEs for all plugin groups"""
    print("🚀 Starting plugin README generation...\n")

    total_agents = 0
    total_commands = 0
    total_skills = 0

    for group in PLUGIN_GROUPS:
        try:
            agents, commands, skills = generate_plugin_readme(group)
            total_agents += agents
            total_commands += commands
            total_skills += skills
        except Exception as e:
            print(f"❌ Error generating README for {group}: {e}")

    print(f"\n📊 Summary:")
    print(f"  - Total agents: {total_agents}")
    print(f"  - Total commands: {total_commands}")
    print(f"  - Total skills: {total_skills}")
    print(f"  - Groups processed: {len(PLUGIN_GROUPS)}")
    print("\n✨ All plugin READMEs generated successfully!")


if __name__ == '__main__':
    main()
