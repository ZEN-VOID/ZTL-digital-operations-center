#!/usr/bin/env python3
"""
同步管理器 (Sync Manager)

功能：
1. 检测全局插件配置的变更
2. 触发增量或完整同步
3. 记录同步历史
4. 提供智能同步策略
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from plugins_scanner import PluginsScanner
from knowledge_base import KnowledgeBase


class SyncManager:
    """全局插件同步管理器"""

    def __init__(self):
        self.scanner = PluginsScanner()
        self.kb = KnowledgeBase()
        self.home_dir = Path.home()
        self.claude_dir = self.home_dir / ".claude"

    def check_need_sync(self, force: bool = False) -> tuple[bool, str]:
        """
        检查是否需要同步

        Args:
            force: 是否强制同步

        Returns:
            (需要同步, 原因说明)
        """
        if force:
            return True, "用户强制同步"

        # 检查知识库是否存在
        if not self.kb.plugins_registry_file.exists():
            return True, "知识库未初始化"

        # 读取上次同步记录
        sync_record = self.kb.load_sync_record()
        if not sync_record:
            return True, "无同步记录"

        # 检查配置文件修改时间
        settings_file = self.claude_dir / "settings.json"
        installed_file = self.claude_dir / "plugins" / "installed_plugins.json"

        last_sync_time = datetime.fromisoformat(sync_record.get("sync_time", "2000-01-01T00:00:00"))

        # 检查settings.json
        if settings_file.exists():
            settings_mtime = datetime.fromtimestamp(settings_file.stat().st_mtime)
            if settings_mtime > last_sync_time:
                return True, f"settings.json已更新 ({settings_mtime.isoformat()})"

        # 检查installed_plugins.json
        if installed_file.exists():
            installed_mtime = datetime.fromtimestamp(installed_file.stat().st_mtime)
            if installed_mtime > last_sync_time:
                return True, f"installed_plugins.json已更新 ({installed_mtime.isoformat()})"

        # 检查Git commit SHA
        if self._check_git_commits_changed(sync_record):
            return True, "检测到插件Git commit变更"

        return False, "知识库已是最新"

    def _check_git_commits_changed(self, sync_record: Dict[str, Any]) -> bool:
        """检查插件的Git commit SHA是否有变更"""
        # 读取当前安装记录
        installed_file = self.claude_dir / "plugins" / "installed_plugins.json"
        if not installed_file.exists():
            return False

        import json
        try:
            with open(installed_file, 'r') as f:
                installed_data = json.load(f)

            current_plugins = installed_data.get("plugins", {})
            previous_commits = sync_record.get("git_commits", {})

            # 比对每个插件的commit SHA
            for plugin_id, plugin_info in current_plugins.items():
                current_sha = plugin_info.get("gitCommitSha", "")
                previous_sha = previous_commits.get(plugin_id, "")

                if current_sha and current_sha != previous_sha:
                    print(f"   检测到变更: {plugin_id} ({previous_sha[:8]} -> {current_sha[:8]})")
                    return True

            return False
        except Exception as e:
            print(f"⚠️  检查Git commits失败: {e}")
            return False

    def sync(self, force: bool = False) -> Dict[str, Any]:
        """
        执行同步

        Args:
            force: 是否强制同步（忽略检查）

        Returns:
            同步结果
        """
        # 检查是否需要同步
        need_sync, reason = self.check_need_sync(force)

        if not need_sync:
            print(f"✅ {reason}，无需同步")
            return {
                "synced": False,
                "reason": reason,
                "registry": self.kb.load_plugins_registry()
            }

        print(f"🔄 开始同步: {reason}")

        # 执行扫描
        start_time = datetime.now()
        registry = self.scanner.scan_all()
        scan_duration = (datetime.now() - start_time).total_seconds()

        # 保存插件注册表
        self.kb.save_plugins_registry(registry)

        # 构建并保存技能包索引
        skills_index = self.kb.build_skills_index(registry)
        self.kb.save_skills_index(skills_index)

        # 保存同步记录
        sync_record = {
            "sync_time": datetime.now().isoformat(),
            "scan_duration_seconds": scan_duration,
            "trigger_reason": reason,
            "total_plugins": registry.get("total_plugins", 0),
            "total_skills": registry.get("total_skills", 0),
            "total_agents": registry.get("total_agents", 0),
            "git_commits": self._extract_git_commits(registry)
        }
        self.kb.save_sync_record(sync_record)

        print(f"\n✅ 同步完成，耗时 {scan_duration:.2f} 秒")

        return {
            "synced": True,
            "reason": reason,
            "registry": registry,
            "sync_record": sync_record
        }

    def _extract_git_commits(self, registry: Dict[str, Any]) -> Dict[str, str]:
        """从注册表中提取每个插件的Git commit SHA"""
        commits = {}
        for plugin_id, plugin_data in registry.get("plugins", {}).items():
            sha = plugin_data.get("git_commit_sha", "")
            if sha:
                commits[plugin_id] = sha
        return commits

    def get_sync_status(self) -> str:
        """获取同步状态的Markdown报告"""
        need_sync, reason = self.check_need_sync()
        sync_record = self.kb.load_sync_record()

        output = ["# 同步状态\n"]

        if sync_record:
            output.append(f"**最后同步**: {sync_record.get('sync_time', 'Unknown')}")
            output.append(f"**触发原因**: {sync_record.get('trigger_reason', 'Unknown')}")
            output.append(f"**扫描耗时**: {sync_record.get('scan_duration_seconds', 0):.2f} 秒")
            output.append(f"**插件数量**: {sync_record.get('total_plugins', 0)}")
            output.append(f"**技能包数量**: {sync_record.get('total_skills', 0)}")
            output.append(f"**智能体数量**: {sync_record.get('total_agents', 0)}\n")

        if need_sync:
            output.append(f"**当前状态**: ⚠️  需要同步")
            output.append(f"**原因**: {reason}")
        else:
            output.append(f"**当前状态**: ✅ 已是最新")

        return "\n".join(output)


def main():
    """主函数 - 用于命令行调用"""
    import sys

    manager = SyncManager()

    # 解析命令行参数
    force = "--force" in sys.argv or "-f" in sys.argv

    if "--status" in sys.argv or "-s" in sys.argv:
        # 显示同步状态
        print(manager.get_sync_status())
    else:
        # 执行同步
        result = manager.sync(force=force)

        # 显示摘要报告
        if result["synced"]:
            print("\n" + "="*60)
            print(manager.kb.generate_summary_report())


if __name__ == "__main__":
    main()
