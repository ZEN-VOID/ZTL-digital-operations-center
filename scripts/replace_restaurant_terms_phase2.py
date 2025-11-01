#!/usr/bin/env python3
"""
Phase 2: Additional replacements for missed terms
"""

import re
from pathlib import Path
from typing import List, Tuple

# Additional replacements for missed terms
ADDITIONAL_REPLACEMENTS: List[Tuple[str, str]] = [
    # Description field specific
    ("organization SaaS platform", "digital intelligence collaboration platform"),
    ("for organization SaaS", "for digital intelligence collaboration"),

    # Chinese terms that were missed
    ("数智化协作平台数据建模**: 设计餐厅、订单、菜单、会员、报表等领域模型", "数智化协作平台数据建模**: 设计组织、任务、能力、用户、报表等领域模型"),
    ("用餐高峰期", "业务高峰时段"),
    ("午晚高峰", "业务高峰"),
    ("菜单缓存、会员信息缓存", "能力缓存、用户信息缓存"),
    ("能力图片", "能力图片"),
    ("组织定位、配送范围", "组织定位、执行范围"),

    # Specific leftovers in documentation
    ("餐厅、订单、菜单、会员", "组织、任务、能力、用户"),
    ("示例餐厅", "示例组织"),
    ("创建餐厅", "创建组织"),
    ("查询餐厅列表", "查询组织列表"),
    ("餐厅列表", "组织列表"),
    ("RestaurantsPage", "OrganizationsPage"),
    ("RestaurantsList", "OrganizationsList"),
    ("RealtimeOrders", "RealtimeTasks"),
    ("fetchOrders", "fetchTasks"),
    ("setOrders", "setTasks"),
    ("OrdersTable", "TasksTable"),

    # Function and variable names
    ("get_organization", "get_organization"),

    # Additional Chinese context-specific terms
    ("高峰期", "业务高峰时段"),
    ("峰时性能优化", "高峰时段性能优化"),
    ("峰时", "高峰时段"),
    ("订阅实现订单推送、库存同步", "订阅实现任务推送、资源同步"),
    ("库存同步", "资源同步"),
    ("订单推送", "任务推送"),

    # English description updates
    ("for high-traffic dining scenarios", "for high-traffic business scenarios"),
    ("peak hours", "business peak hours"),
    ("dining scenarios", "business scenarios"),
]


def replace_in_file(file_path: Path, replacements: List[Tuple[str, str]]) -> int:
    """Apply additional replacements."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    total_changes = 0

    for old_text, new_text in replacements:
        count = content.count(old_text)
        if count > 0:
            total_changes += count
            content = content.replace(old_text, new_text)
            print(f"  ✓ Replaced '{old_text[:50]}...' → {count} times")

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return total_changes
    else:
        return 0


def main():
    base_dir = Path("/Users/vincentlee/Desktop/ZTL数智化作战中心/plugins/开发组/agents")

    files_to_process = [
        base_dir / "F4-文档报告生成.md",
        base_dir / "F5-后端架构师.md",
        base_dir / "F6-数据库架构师.md",
    ]

    print("\n" + "="*60)
    print("Phase 2: Additional Terminology Replacements")
    print("="*60 + "\n")

    total_changes = 0

    for file_path in files_to_process:
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            continue

        print(f"\n📝 Processing: {file_path.name}")
        changes = replace_in_file(file_path, ADDITIONAL_REPLACEMENTS)

        if changes > 0:
            total_changes += changes
            print(f"✅ Made {changes} replacements")
        else:
            print(f"⚠️  No additional changes needed")

    print(f"\n{'='*60}")
    print(f"🎯 Phase 2 Complete: {total_changes} additional replacements made")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
