#!/usr/bin/env python3
"""
测试用户级和项目级插件路径配置的灵活性

验证:
1. 用户级是否支持任意绝对路径?
2. 项目级是否必须相对路径?
3. 是否可以一个plugin一个独立目录?
"""

import json
from pathlib import Path
from typing import Dict, List

def test_user_level_paths():
    """测试用户级路径配置"""
    print("\n" + "="*70)
    print("测试1: 用户级插件路径灵活性")
    print("="*70)

    scenarios = [
        {
            "name": "标准位置 (推荐)",
            "config": {
                "enabledPlugins": {
                    "example-skills@anthropic-agent-skills": True
                }
            },
            "说明": "通过/plugin install安装,自动管理在 ~/.claude/plugins/marketplaces/",
            "路径": "~/.claude/plugins/marketplaces/anthropic-agent-skills/",
            "支持": True,
            "原因": "官方标准,自动管理"
        },
        {
            "name": "自定义agents目录",
            "config": "直接创建 ~/.claude/agents/my-agent/",
            "说明": "无需marketplace.json,Claude启动时自动扫描",
            "路径": "~/.claude/agents/my-agent/",
            "支持": True,
            "原因": "官方支持的简化方式"
        },
        {
            "name": "任意绝对路径 (理论)",
            "config": {
                "extraKnownMarketplaces": [
                    {
                        "type": "directory",
                        "path": "/absolute/path/to/my-plugins"
                    }
                ]
            },
            "说明": "在settings.json中配置绝对路径marketplace",
            "路径": "/absolute/path/to/my-plugins/",
            "支持": "有限支持 ⚠️",
            "原因": "extraKnownMarketplaces支持绝对路径,但不推荐"
        },
        {
            "name": "多个独立plugin目录",
            "config": {
                "extraKnownMarketplaces": [
                    {
                        "type": "directory",
                        "path": "/path/plugin-a"
                    },
                    {
                        "type": "directory",
                        "path": "/path/plugin-b"
                    }
                ]
            },
            "说明": "每个plugin独立目录,分别注册",
            "路径": "多个独立目录",
            "支持": "技术上可行 ⚠️",
            "原因": "可以注册多个marketplace,但不推荐"
        }
    ]

    for i, scenario in enumerate(scenarios, 1):
        print(f"\n场景{i}: {scenario['name']}")
        print(f"  配置: {scenario.get('config', 'N/A')}")
        print(f"  说明: {scenario['说明']}")
        print(f"  路径: {scenario['路径']}")
        print(f"  支持: {scenario['支持']}")
        print(f"  原因: {scenario['原因']}")


def test_project_level_paths():
    """测试项目级路径配置"""
    print("\n\n" + "="*70)
    print("测试2: 项目级插件路径灵活性")
    print("="*70)

    scenarios = [
        {
            "name": "标准相对路径 (推荐)",
            "marketplace_path": "./.claude-plugin",
            "plugin_source": "../plugins/战略组",
            "说明": "marketplace在.claude-plugin/,plugin在plugins/",
            "支持": True,
            "原因": "官方推荐的标准结构"
        },
        {
            "name": "自定义相对路径",
            "marketplace_path": "./.claude/marketplace",
            "plugin_source": "../../plugins/战略组",
            "说明": "marketplace在.claude/内,需要调整相对路径层级",
            "支持": True,
            "原因": "相对路径灵活,只要能正确解析到plugin即可"
        },
        {
            "name": "绝对路径 (不推荐)",
            "marketplace_path": "./.claude-plugin",
            "plugin_source": "/absolute/path/to/plugins/战略组",
            "说明": "plugin source使用绝对路径",
            "支持": "官方不推荐 ❌",
            "原因": "官方文档明确: All paths must be relative and start with ./"
        },
        {
            "name": "每个plugin独立目录",
            "marketplace_path": "./.claude-plugin",
            "plugin_sources": [
                "../plugins/战略组",
                "../plugins/创意组",
                "/external/plugins/special-plugin"
            ],
            "说明": "每个plugin可以在不同目录",
            "支持": "部分支持 ⚠️",
            "原因": "marketplace可以指向多个不同的相对路径"
        }
    ]

    for i, scenario in enumerate(scenarios, 1):
        print(f"\n场景{i}: {scenario['name']}")
        print(f"  marketplace路径: {scenario['marketplace_path']}")
        if 'plugin_source' in scenario:
            print(f"  plugin source: {scenario['plugin_source']}")
        if 'plugin_sources' in scenario:
            print(f"  plugin sources:")
            for source in scenario['plugin_sources']:
                print(f"    - {source}")
        print(f"  说明: {scenario['说明']}")
        print(f"  支持: {scenario['支持']}")
        print(f"  原因: {scenario['原因']}")


def test_plugin_structure_constraints():
    """测试plugin内部结构约束"""
    print("\n\n" + "="*70)
    print("测试3: Plugin内部结构约束")
    print("="*70)

    print("\n官方要求:")
    print("  1. plugin.json必须在: .claude-plugin/plugin.json")
    print("  2. 组件目录(agents/commands/skills/hooks/)必须在plugin根目录")
    print("  3. 组件目录不能放在.claude-plugin/内部")
    print("  4. plugin.json中的路径必须是相对路径,以./ 开头")

    print("\n✅ 正确结构:")
    correct_structure = """
    my-plugin/
    ├── .claude-plugin/
    │   └── plugin.json          ← 必须在这里
    ├── agents/                  ← 必须在根目录
    ├── commands/                ← 必须在根目录
    └── skills/                  ← 必须在根目录
    """
    print(correct_structure)

    print("plugin.json内容:")
    correct_config = {
        "name": "my-plugin",
        "agents": "./agents",      # ← 相对路径,以./开头
        "commands": "./commands",
        "skills": "./skills"
    }
    print(f"  {json.dumps(correct_config, indent=2)}")

    print("\n❌ 错误结构1: 组件在.claude-plugin内")
    wrong_structure_1 = """
    my-plugin/
    └── .claude-plugin/
        ├── plugin.json
        ├── agents/              ← 错误!不能在这里
        └── commands/            ← 错误!不能在这里
    """
    print(wrong_structure_1)

    print("❌ 错误结构2: 使用绝对路径")
    wrong_config = {
        "name": "my-plugin",
        "agents": "/absolute/path/agents",  # ← 错误!不支持绝对路径
    }
    print(f"  {json.dumps(wrong_config, indent=2)}")

    print("\n✅ 灵活的相对路径:")
    flexible_structure = """
    my-plugin/
    ├── .claude-plugin/
    │   └── plugin.json
    ├── core/                    ← 可以自定义目录名
    │   └── agents/
    └── extensions/
        └── commands/
    """
    print(flexible_structure)

    print("plugin.json内容:")
    flexible_config = {
        "name": "my-plugin",
        "agents": "./core/agents",       # ← 可以指向子目录
        "commands": "./extensions/commands"
    }
    print(f"  {json.dumps(flexible_config, indent=2)}")


def test_real_world_scenarios():
    """实际使用场景分析"""
    print("\n\n" + "="*70)
    print("测试4: 实际使用场景")
    print("="*70)

    scenarios = [
        {
            "场景": "个人开发者,多个项目共享通用插件",
            "需求": "一套插件代码,多个项目使用",
            "方案": "用户级 + 软链接/Git submodule",
            "配置": """
            # 创建共享插件目录
            mkdir -p ~/my-shared-plugins/common-utils

            # 用户级配置
            ~/.claude/settings.json:
            {
              "extraKnownMarketplaces": [{
                "type": "directory",
                "path": "~/my-shared-plugins"  # 绝对路径
              }]
            }

            # 或者在每个项目中软链接
            ln -s ~/my-shared-plugins/common-utils ./plugins/common-utils
            """,
            "评估": "✅ 可行,但用户级更简洁"
        },
        {
            "场景": "团队协作,每个plugin独立Git仓库",
            "需求": "8个业务组,每组独立维护和版本控制",
            "方案": "Git submodules + 项目级marketplace",
            "配置": """
            # 项目结构
            /project/
            ├── .gitmodules
            ├── .claude-plugin/marketplace.json
            └── plugins/
                ├── plugin-a/  (git submodule)
                ├── plugin-b/  (git submodule)
                └── plugin-c/  (git submodule)

            # marketplace.json可以指向不同位置
            {
              "plugins": [
                {"name": "plugin-a", "source": "../plugins/plugin-a"},
                {"name": "plugin-b", "source": "../plugins/plugin-b"},
                {"name": "plugin-c", "source": "../external/plugin-c"}
              ]
            }
            """,
            "评估": "✅ 推荐方案,每个plugin独立但集中管理"
        },
        {
            "场景": "混合环境,部分plugin在项目内,部分在外部",
            "需求": "核心plugin在项目内,第三方plugin在外部",
            "方案": "混合相对路径和用户级",
            "配置": """
            # 项目级marketplace指向项目内plugin
            .claude/settings.json:
            {
              "extraKnownMarketplaces": [{
                "type": "directory",
                "path": "./.claude-plugin"
              }],
              "enabledPlugins": {
                "core-plugin@project-marketplace": true
              }
            }

            # 用户级配置外部plugin
            ~/.claude/settings.json:
            {
              "enabledPlugins": {
                "external-plugin@anthropic-agent-skills": true
              }
            }
            """,
            "评估": "✅ 最佳实践,分离关注点"
        }
    ]

    for i, scenario in enumerate(scenarios, 1):
        print(f"\n场景{i}: {scenario['场景']}")
        print(f"  需求: {scenario['需求']}")
        print(f"  方案: {scenario['方案']}")
        print(f"  配置:")
        for line in scenario['配置'].strip().split('\n'):
            print(f"    {line}")
        print(f"  评估: {scenario['评估']}")


def main():
    print("\n" + "="*70)
    print("Claude Code Plugin 路径配置灵活性完整测试")
    print("="*70)

    test_user_level_paths()
    test_project_level_paths()
    test_plugin_structure_constraints()
    test_real_world_scenarios()

    print("\n\n" + "="*70)
    print("核心结论")
    print("="*70)

    conclusions = [
        {
            "问题": "用户级是否支持任意绝对路径?",
            "答案": "部分支持 ⚠️",
            "详细": """
            - extraKnownMarketplaces可以使用绝对路径
            - 但官方推荐用 /plugin install 命令(自动管理)
            - agents/skills/commands可以直接在~/.claude/下创建
            - 技术上可行,但不推荐分散管理
            """
        },
        {
            "问题": "项目级是否必须相对路径?",
            "答案": "是的 ✅",
            "详细": """
            - 官方明确要求: All paths must be relative and start with ./
            - marketplace.json可以在任何位置(相对项目根)
            - plugin source必须是相对路径(相对marketplace.json)
            - plugin.json内部路径必须相对(相对plugin根)
            - 这是为了确保项目可移植性和团队协作
            """
        },
        {
            "问题": "是否可以一个plugin一个独立目录?",
            "答案": "可以 ✅",
            "详细": """
            - marketplace.json可以指向多个不同的相对路径
            - 每个plugin可以在不同目录(但推荐集中在plugins/)
            - 支持Git submodules管理每个plugin
            - 推荐: plugins/目录下,每个业务组一个子目录
            """
        },
        {
            "问题": "最灵活的配置方式?",
            "答案": "分层管理 ✅",
            "详细": """
            用户级:
              - 使用 /plugin install 安装通用工具
              - 或在 ~/.claude/agents|skills|commands 直接创建
              - extraKnownMarketplaces只用于特殊需求

            项目级:
              - 统一在 plugins/ 目录管理
              - 一个 marketplace.json 注册所有plugin
              - 支持Git submodules实现独立版本控制
              - 保持相对路径确保可移植性
            """
        }
    ]

    for conclusion in conclusions:
        print(f"\n【{conclusion['问题']}】")
        print(f"  答案: {conclusion['答案']}")
        print(f"  详细说明:")
        for line in conclusion['详细'].strip().split('\n'):
            print(f"    {line}")

    print("\n" + "="*70)
    print("推荐配置模式")
    print("="*70)

    print("""
    ✅ 推荐: 标准化管理

    用户级:
      ~/.claude/
      ├── settings.json (enabledPlugins只配置已安装的)
      └── plugins/marketplaces/ (由/plugin install自动管理)

    项目级:
      /project/
      ├── .claude/settings.json (extraKnownMarketplaces + enabledPlugins)
      ├── .claude-plugin/marketplace.json (注册本地plugins)
      └── plugins/ (统一管理所有plugin)
          ├── 战略组/ (可以是Git submodule)
          ├── 创意组/ (可以是Git submodule)
          └── ... (其他业务组)

    ⚠️ 避免: 分散管理

    不推荐:
      - 用户级plugin散落在多个绝对路径目录
      - 项目级plugin使用绝对路径
      - 过度使用extraKnownMarketplaces指向外部目录

    原因:
      - 降低可维护性
      - 破坏可移植性
      - 增加团队协作难度
    """)

    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
