#!/usr/bin/env python3
"""
Plugin Status Verification Core Engine

This module provides the execution engine for the plugin-status skill.
It performs comprehensive health checks on the ZTL project's plugin system.

Usage:
    python verify_plugins_core.py [--json]

Options:
    --json    Output results in JSON format for programmatic use
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


class PluginStatusChecker:
    """Main verification engine for plugin system status"""

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize with project root path"""
        self.project_root = project_root or Path.cwd()
        self.settings_path = self.project_root / ".claude" / "settings.json"
        self.marketplace_path = self.project_root / ".claude-plugin" / "marketplace.json"

    def check_settings(self) -> Tuple[bool, Dict[str, bool]]:
        """Check settings.json for enabled plugins configuration"""
        if not self.settings_path.exists():
            print(f"{RED}✗ settings.json does not exist{RESET}")
            return False, {}

        with open(self.settings_path) as f:
            settings = json.load(f)

        enabled_plugins = settings.get("enabledPlugins", {})

        print(f"\n{BLUE}=== 1. Settings Configuration Check ==={RESET}")
        print(f"Config file: .claude/settings.json")
        print(f"Enabled plugins: {len(enabled_plugins)}")

        all_enabled = all(enabled_plugins.values())

        for plugin_id, enabled in enabled_plugins.items():
            status = f"{GREEN}✓{RESET}" if enabled else f"{RED}✗{RESET}"
            print(f"  {status} {plugin_id}: {enabled}")

        return all_enabled, enabled_plugins

    def check_marketplace(self) -> Tuple[bool, List[Dict]]:
        """Check marketplace.json for plugin definitions"""
        if not self.marketplace_path.exists():
            print(f"{RED}✗ marketplace.json does not exist{RESET}")
            return False, []

        with open(self.marketplace_path) as f:
            marketplace = json.load(f)

        plugins = marketplace.get("plugins", [])

        print(f"\n{BLUE}=== 2. Marketplace Configuration Check ==={RESET}")
        print(f"Config file: .claude-plugin/marketplace.json")
        print(f"Defined plugins: {len(plugins)}")

        for plugin in plugins:
            name = plugin.get("name", "unnamed")
            source = plugin.get("source", "")

            source_path = self.project_root / source if source else None
            source_exists = source_path.exists() if source_path else False
            status = f"{GREEN}✓{RESET}" if source_exists else f"{RED}✗{RESET}"

            print(f"  {status} {name}")
            print(f"      Path: {source}")
            print(f"      Exists: {source_exists}")

        return True, plugins

    def check_plugin_structure(self, plugin_source: str) -> Dict:
        """Check structure of a single plugin directory"""
        plugin_path = self.project_root / plugin_source

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

    def generate_report(
        self,
        enabled_plugins: Dict[str, bool],
        plugins: List[Dict],
        plugin_details: List[Dict]
    ) -> Dict:
        """Generate comprehensive status report"""
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
        total_agents = sum(p["structure"]["agent_count"] for p in plugin_details)

        # Business group mapping
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

        group_stats = {}
        for cn_name, en_name in business_groups.items():
            detail = next((p for p in plugin_details if p["name"] == en_name), None)
            if detail:
                group_stats[cn_name] = detail["structure"]["agent_count"]

        # Overall health check
        all_ok = (
            enabled_count == len(expected_plugins) and
            all(p["structure"]["exists"] and p["structure"]["agents_dir"] for p in plugin_details)
        )

        return {
            "overall_status": "healthy" if all_ok else "issues_detected",
            "enabled_count": enabled_count,
            "expected_count": len(expected_plugins),
            "total_agents": total_agents,
            "plugin_details": plugin_details,
            "group_stats": group_stats,
            "all_ok": all_ok
        }

    def print_summary(self, report: Dict):
        """Print human-readable summary report"""
        print(f"\n{BLUE}{'='*70}{RESET}")
        print(f"{BLUE}=== Summary Report ==={RESET}")
        print(f"{BLUE}{'='*70}{RESET}")

        # Plugin activation status
        print(f"\nPlugin Activation Status:")
        print(f"  Enabled: {report['enabled_count']}/{report['expected_count']}")
        status_color = GREEN if report['enabled_count'] == report['expected_count'] else RED
        status_text = "All enabled" if report['enabled_count'] == report['expected_count'] else "Partially disabled"
        print(f"  Status: {status_color}{status_text}{RESET}")

        # Plugin definition status
        plugin_count = len(report['plugin_details'])
        exists_count = sum(1 for p in report['plugin_details'] if p['structure']['exists'])
        print(f"\nPlugin Definition Status:")
        print(f"  Marketplace definitions: {plugin_count} plugins")
        print(f"  Directories exist: {exists_count}/{plugin_count}")

        # Agent statistics
        print(f"\nAgent Statistics:")
        print(f"  Total: {report['total_agents']} agents")

        print(f"\nAgents per Business Group:")
        for group_name, count in report['group_stats'].items():
            print(f"  {group_name}: {count} agents")

        # Final status
        print(f"\n{BLUE}{'='*70}{RESET}")
        if report['all_ok']:
            print(f"{GREEN}✓ All plugins operational, system ready!{RESET}")
        else:
            print(f"{YELLOW}⚠ Issues detected, please review the report above{RESET}")
        print(f"{BLUE}{'='*70}{RESET}\n")

    def run(self, json_output: bool = False) -> int:
        """Execute full verification workflow"""
        if not json_output:
            print(f"{BLUE}{'='*70}{RESET}")
            print(f"{BLUE}ZTL Digital Intelligence Operations Center - Plugin Status Verification{RESET}")
            print(f"{BLUE}{'='*70}{RESET}")

        # Step 1: Check settings
        settings_ok, enabled_plugins = self.check_settings()

        # Step 2: Check marketplace
        marketplace_ok, plugins = self.check_marketplace()

        # Step 3: Check plugin structures
        if not json_output:
            print(f"\n{BLUE}=== 3. Plugin Structure Integrity Check ==={RESET}")

        plugin_details = []
        for plugin in plugins:
            plugin_name = plugin.get("name", "")
            plugin_source = plugin.get("source", "")

            structure = self.check_plugin_structure(plugin_source)

            if not json_output:
                status = f"{GREEN}✓{RESET}" if structure["exists"] and structure["agents_dir"] else f"{RED}✗{RESET}"
                print(f"\n  {status} {plugin_name}")
                print(f"      Path: {plugin_source}")
                print(f"      agents/ directory: {'Exists' if structure['agents_dir'] else 'Missing'}")
                print(f"      Agent count: {structure['agent_count']}")

                if structure["agents"]:
                    print(f"      Agent list:")
                    for agent in structure["agents"]:
                        print(f"        - {agent}")

            plugin_details.append({
                "name": plugin_name,
                "source": plugin_source,
                "structure": structure
            })

        # Step 4: Generate report
        report = self.generate_report(enabled_plugins, plugins, plugin_details)

        # Output
        if json_output:
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            self.print_summary(report)

        return 0 if report['all_ok'] else 1


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="ZTL Plugin System Status Verification"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format"
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        help="Project root directory (default: current directory)"
    )

    args = parser.parse_args()

    checker = PluginStatusChecker(project_root=args.project_root)
    return checker.run(json_output=args.json)


if __name__ == "__main__":
    sys.exit(main())
