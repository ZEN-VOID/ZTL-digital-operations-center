#!/usr/bin/env python3
"""
验证不同marketplace目录位置的配置可行性

测试场景:
1. 根目录: .claude-plugin/
2. .claude内: .claude/marketplace/
3. config内: config/claude-plugins/
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

def test_path_resolution(
    marketplace_path: str,
    plugin_source: str,
    description: str
) -> Tuple[bool, str, Dict]:
    """
    测试marketplace路径配置的可行性

    Args:
        marketplace_path: marketplace.json所在目录(相对于项目根)
        plugin_source: plugin的source路径(相对于marketplace.json)
        description: 测试场景描述

    Returns:
        (是否可行, 原因, 路径信息)
    """
    print(f"\n{'='*70}")
    print(f"测试场景: {description}")
    print(f"{'='*70}")

    # 解析marketplace完整路径
    marketplace_full = PROJECT_ROOT / marketplace_path / "marketplace.json"
    marketplace_dir = marketplace_full.parent

    # 解析plugin source完整路径
    plugin_full = (marketplace_dir / plugin_source).resolve()

    # 路径信息
    paths = {
        "marketplace_relative": marketplace_path,
        "marketplace_absolute": str(marketplace_full),
        "plugin_source": plugin_source,
        "plugin_resolved": str(plugin_full),
        "settings_path": f"./{marketplace_path}"
    }

    print(f"\n路径配置:")
    print(f"  settings.json中的path: '{paths['settings_path']}'")
    print(f"  marketplace.json位置: {marketplace_full}")
    print(f"  plugin source配置: '{plugin_source}'")
    print(f"  plugin解析后路径: {plugin_full}")

    # 验证marketplace目录是否可以创建
    marketplace_exists = marketplace_dir.exists()
    marketplace_can_create = True

    if not marketplace_exists:
        try:
            # 测试是否可以创建(不实际创建)
            marketplace_dir.parent.exists()
        except Exception as e:
            marketplace_can_create = False

    # 验证plugin路径是否存在
    plugin_exists = plugin_full.exists()

    # 计算相对路径层级
    try:
        levels_up = plugin_source.count("../")
        print(f"\n  source路径层级: 向上 {levels_up} 级")
    except:
        levels_up = 0

    # 判断可行性
    reasons = []
    is_valid = True

    if not marketplace_can_create:
        is_valid = False
        reasons.append("❌ marketplace目录无法创建(父目录不存在)")
    else:
        reasons.append("✅ marketplace目录路径有效")

    if not plugin_exists:
        is_valid = False
        reasons.append(f"❌ plugin路径不存在: {plugin_full}")
    else:
        reasons.append(f"✅ plugin路径存在: {plugin_full}")

    # 检查路径简洁度
    if levels_up <= 1:
        reasons.append(f"✅ source路径简洁(仅{levels_up}级)")
    elif levels_up == 2:
        reasons.append(f"⚠️  source路径稍长(需要{levels_up}级)")
    else:
        reasons.append(f"⚠️  source路径过长(需要{levels_up}级)")

    print(f"\n可行性分析:")
    for reason in reasons:
        print(f"  {reason}")

    print(f"\n结论: {'✅ 配置可行' if is_valid else '❌ 配置不可行'}")

    return is_valid, "\n".join(reasons), paths


def generate_config_examples(marketplace_path: str, plugin_source: str) -> Dict:
    """生成完整的配置示例"""

    settings_config = {
        "extraKnownMarketplaces": [
            {
                "type": "directory",
                "path": f"./{marketplace_path}",
                "description": "Local ZTL plugin marketplace"
            }
        ]
    }

    marketplace_config = {
        "name": "ztl-local-plugins",
        "plugins": [
            {
                "name": "strategy-team",
                "source": plugin_source,
                "description": "Strategic planning team"
            }
        ]
    }

    return {
        "settings.json": settings_config,
        "marketplace.json": marketplace_config
    }


def main():
    print("\n" + "="*70)
    print("Claude Code Marketplace 路径配置可行性测试")
    print("="*70)

    # 测试场景
    scenarios = [
        {
            "marketplace": ".claude-plugin",
            "source": "../plugins/战略组",
            "description": "方案1: 根目录 (当前配置, 官方推荐)"
        },
        {
            "marketplace": ".claude/marketplace",
            "source": "../../plugins/战略组",
            "description": "方案2: .claude目录内 (集中管理)"
        },
        {
            "marketplace": "config/claude-plugins",
            "source": "../../plugins/战略组",
            "description": "方案3: config目录 (通用配置目录)"
        },
        {
            "marketplace": ".claude-plugin",
            "source": "./plugins/战略组",  # 错误配置示例
            "description": "错误示例: source路径错误(./相对于marketplace.json)"
        }
    ]

    results = []

    for scenario in scenarios:
        valid, reason, paths = test_path_resolution(
            scenario["marketplace"],
            scenario["source"],
            scenario["description"]
        )

        results.append({
            "scenario": scenario["description"],
            "valid": valid,
            "reason": reason,
            "paths": paths
        })

        if valid:
            print(f"\n配置示例:")
            configs = generate_config_examples(
                scenario["marketplace"],
                scenario["source"]
            )
            print(f"\n  settings.json:")
            print(f"  {json.dumps(configs['settings.json'], indent=2, ensure_ascii=False)}")
            print(f"\n  marketplace.json:")
            print(f"  {json.dumps(configs['marketplace.json'], indent=2, ensure_ascii=False)}")

    # 总结
    print(f"\n\n{'='*70}")
    print("测试总结")
    print(f"{'='*70}\n")

    valid_count = sum(1 for r in results if r["valid"])

    print(f"可行方案: {valid_count}/{len(results)}\n")

    for i, result in enumerate(results, 1):
        status = "✅" if result["valid"] else "❌"
        print(f"{status} 方案{i}: {result['scenario']}")

    print(f"\n{'='*70}")
    print("推荐建议")
    print(f"{'='*70}\n")

    print("1. 【最推荐】保持当前配置 (.claude-plugin/)")
    print("   - 官方标准位置")
    print("   - source路径最简洁")
    print("   - 团队熟悉度高\n")

    print("2. 【可选】迁移到 .claude/marketplace/")
    print("   - 集中所有Claude配置")
    print("   - 需要更新source路径(多一层../)")
    print("   - 适合配置文件较多的项目\n")

    print("3. 【不推荐】使用config/等自定义目录")
    print("   - 离散度高,不易发现")
    print("   - 需要额外文档说明")
    print("   - 团队协作成本较高\n")


if __name__ == "__main__":
    main()
