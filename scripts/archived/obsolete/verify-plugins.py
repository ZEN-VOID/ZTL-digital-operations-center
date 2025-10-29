#!/usr/bin/env python3
"""
验证ZTL项目所有plugins是否已正确启动

检查项:
1. .claude/settings.json中enabledPlugins配置
2. .claude-plugin/marketplace.json中的插件定义
3. 每个plugin目录的结构完整性
4. agents文件数量统计
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple

# ANSI颜色代码
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def check_settings() -> Tuple[bool, Dict[str, bool]]:
    """检查settings.json中的enabledPlugins"""
    settings_path = Path(".claude/settings.json")

    if not settings_path.exists():
        print(f"{RED}✗ settings.json不存在{RESET}")
        return False, {}

    with open(settings_path) as f:
        settings = json.load(f)

    enabled_plugins = settings.get("enabledPlugins", {})

    print(f"\n{BLUE}=== 1. Settings配置检查 ==={RESET}")
    print(f"配置文件: .claude/settings.json")
    print(f"启用的插件数: {len(enabled_plugins)}")

    all_enabled = all(enabled_plugins.values())

    for plugin_id, enabled in enabled_plugins.items():
        status = f"{GREEN}✓{RESET}" if enabled else f"{RED}✗{RESET}"
        print(f"  {status} {plugin_id}: {enabled}")

    return all_enabled, enabled_plugins


def check_marketplace() -> Tuple[bool, List[Dict]]:
    """检查marketplace.json中的插件定义"""
    marketplace_path = Path(".claude-plugin/marketplace.json")

    if not marketplace_path.exists():
        print(f"{RED}✗ marketplace.json不存在{RESET}")
        return False, []

    with open(marketplace_path) as f:
        marketplace = json.load(f)

    plugins = marketplace.get("plugins", [])

    print(f"\n{BLUE}=== 2. Marketplace配置检查 ==={RESET}")
    print(f"配置文件: .claude-plugin/marketplace.json")
    print(f"定义的插件数: {len(plugins)}")

    for plugin in plugins:
        name = plugin.get("name", "未命名")
        source = plugin.get("source", "")
        description = plugin.get("description", "")

        source_exists = Path(source).exists() if source else False
        status = f"{GREEN}✓{RESET}" if source_exists else f"{RED}✗{RESET}"

        print(f"  {status} {name}")
        print(f"      路径: {source}")
        print(f"      存在: {source_exists}")

    return True, plugins


def check_plugin_structure(plugin_source: str) -> Dict:
    """检查单个plugin的目录结构"""
    plugin_path = Path(plugin_source)

    if not plugin_path.exists():
        return {
            "exists": False,
            "agents_dir": False,
            "agent_count": 0,
            "agents": []
        }

    agents_dir = plugin_path / "agents"
    agents_exist = agents_dir.exists()

    agent_files = []
    if agents_exist:
        agent_files = sorted([f.name for f in agents_dir.glob("*.md")])

    return {
        "exists": True,
        "agents_dir": agents_exist,
        "agent_count": len(agent_files),
        "agents": agent_files
    }


def main():
    print(f"{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}ZTL数智化作战中心 - Plugin启动状态验证{RESET}")
    print(f"{BLUE}{'='*70}{RESET}")

    # 1. 检查settings.json
    settings_ok, enabled_plugins = check_settings()

    # 2. 检查marketplace.json
    marketplace_ok, plugins = check_marketplace()

    # 3. 检查每个plugin的详细结构
    print(f"\n{BLUE}=== 3. Plugin结构完整性检查 ==={RESET}")

    total_agents = 0
    plugin_details = []

    for plugin in plugins:
        plugin_name = plugin.get("name", "")
        plugin_source = plugin.get("source", "")

        structure = check_plugin_structure(plugin_source)

        status = f"{GREEN}✓{RESET}" if structure["exists"] and structure["agents_dir"] else f"{RED}✗{RESET}"

        print(f"\n  {status} {plugin_name}")
        print(f"      路径: {plugin_source}")
        print(f"      agents目录: {'存在' if structure['agents_dir'] else '不存在'}")
        print(f"      agents数量: {structure['agent_count']}")

        if structure["agents"]:
            print(f"      agents列表:")
            for agent in structure["agents"]:
                print(f"        - {agent}")

        total_agents += structure["agent_count"]

        plugin_details.append({
            "name": plugin_name,
            "source": plugin_source,
            "structure": structure
        })

    # 4. 生成总结报告
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}=== 总结报告 ==={RESET}")
    print(f"{BLUE}{'='*70}{RESET}")

    # 统计启用状态
    expected_plugins = [
        "strategy-team@ztl-local-plugins",
        "creative-team@ztl-local-plugins",
        "intelligence-team@ztl-local-plugins",
        "construction-team@ztl-local-plugins",
        "development-team@ztl-local-plugins",
        "meituan-ops-team@ztl-local-plugins",
        "supply-chain-team@ztl-local-plugins",
        "admin-team@ztl-local-plugins"
    ]

    enabled_count = sum(1 for p in expected_plugins if enabled_plugins.get(p, False))

    print(f"\n插件启用状态:")
    print(f"  启用数量: {enabled_count}/{len(expected_plugins)}")
    print(f"  状态: {GREEN if enabled_count == len(expected_plugins) else RED}{'全部启用' if enabled_count == len(expected_plugins) else '部分未启用'}{RESET}")

    print(f"\n插件定义状态:")
    print(f"  Marketplace定义: {len(plugins)}个插件")
    print(f"  目录存在: {sum(1 for p in plugin_details if p['structure']['exists'])}/{len(plugins)}")

    print(f"\nAgents统计:")
    print(f"  总计: {total_agents}个agents")

    # 按业务组分组统计
    print(f"\n各业务组agents数量:")
    business_groups = {
        "战略组": "strategy-team",
        "创意组": "creative-team",
        "情报组": "intelligence-team",
        "筹建组": "construction-team",
        "开发组": "development-team",
        "美团组": "meituan-ops-team",
        "供应组": "supply-chain-team",
        "行政组": "admin-team"
    }

    for cn_name, en_name in business_groups.items():
        detail = next((p for p in plugin_details if p["name"] == en_name), None)
        if detail:
            count = detail["structure"]["agent_count"]
            print(f"  {cn_name}: {count}个")

    # 最终判断
    all_ok = (
        settings_ok and
        marketplace_ok and
        enabled_count == len(expected_plugins) and
        all(p["structure"]["exists"] and p["structure"]["agents_dir"] for p in plugin_details)
    )

    print(f"\n{BLUE}{'='*70}{RESET}")
    if all_ok:
        print(f"{GREEN}✓ 所有plugins已正确启动,系统就绪!{RESET}")
    else:
        print(f"{YELLOW}⚠ 部分plugins存在问题,请检查上述报告{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")

    return 0 if all_ok else 1


if __name__ == "__main__":
    exit(main())
