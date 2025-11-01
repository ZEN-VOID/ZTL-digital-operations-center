#!/usr/bin/env python3
"""
Systematic replacement script for converting restaurant SaaS platform terminology
to digital intelligence platform terminology in agent configuration files.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple

# Define replacement mappings
REPLACEMENTS: List[Tuple[str, str]] = [
    # Global replacements
    ("餐饮SaaS平台", "ZTL数智化作战中心"),
    ("餐饮SaaS", "数智化协作平台"),
    ("餐饮行业", "多智能体协作"),

    # Business entities (database tables, API endpoints)
    ("restaurants", "organizations"),
    ("restaurant_id", "organization_id"),
    ("restaurant", "organization"),
    ("menu_items", "agents"),
    ("menu_item", "agent"),
    ("orders", "tasks"),
    ("order_id", "task_id"),
    ("order", "task"),
    ("order_items", "task_items"),
    ("order_item", "task_item"),
    ("members", "users"),
    ("member_id", "user_id"),
    ("member", "user"),

    # API endpoints
    ("/api/restaurants", "/api/organizations"),
    ("/api/orders", "/api/tasks"),
    ("/api/menu-items", "/api/agents"),
    ("/api/members", "/api/users"),

    # Business logic
    ("订单处理流程", "任务处理流程"),
    ("订单管理", "任务管理"),
    ("订单创建", "任务创建"),
    ("订单查询", "任务查询"),
    ("订单状态", "任务状态"),
    ("库存管理", "资源管理"),
    ("会员积分", "用户积分"),
    ("营业额统计", "业务指标统计"),
    ("营业额", "业务指标"),
    ("菜品库存", "资源配置"),
    ("菜品销售", "能力使用"),
    ("菜品", "能力"),
    ("餐厅管理", "组织管理"),
    ("餐厅基础信息", "组织基础信息"),
    ("餐厅不存在", "组织不存在"),
    ("餐厅ID", "组织ID"),
    ("实时订单系统", "实时任务系统"),
    ("日营业报表", "日业务报表"),
    ("店长", "管理员"),
    ("门店", "组织"),
    ("门店表现", "组织表现"),
    ("支付方式", "结算方式"),
    ("客单价", "任务均值"),
    ("热销菜品", "高频能力"),
    ("高峰时段", "高峰时段"),
    ("11-14点、17-21点", "业务高峰时段"),

    # Database schema specific
    ("business_license", "registration_id"),
    ("contact_phone", "contact_info"),
    ("menu_category", "capability_category"),
    ("dish_name", "capability_name"),
    ("price", "cost"),
    ("payment_method", "settlement_method"),
    ("delivery_address", "execution_location"),
    ("table_number", "workspace_id"),
    ("chef", "executor"),
    ("waiter", "coordinator"),

    # Email/URL domain
    ("restaurant-saas.com", "zt l-platform.com"),
    ("餐饮数字化", "数智化协作"),

    # Documentation specific
    ("店铺运营", "组织运营"),
    ("运营数据", "业务数据"),
]


def replace_in_file(file_path: Path, replacements: List[Tuple[str, str]]) -> Dict[str, int]:
    """
    Apply systematic replacements to a file.

    Args:
        file_path: Path to the file to process
        replacements: List of (old_text, new_text) tuples

    Returns:
        Dictionary with replacement statistics
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    stats = {}

    for old_text, new_text in replacements:
        # Count occurrences before replacement
        count = content.count(old_text)
        if count > 0:
            stats[old_text] = count
            content = content.replace(old_text, new_text)

    # Only write if content changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return stats
    else:
        return {}


def main():
    """Main execution function."""
    base_dir = Path("/Users/vincentlee/Desktop/ZTL数智化作战中心/plugins/开发组/agents")

    files_to_process = [
        base_dir / "F4-文档报告生成.md",
        base_dir / "F5-后端架构师.md",
        base_dir / "F6-数据库架构师.md",
    ]

    results = {}

    for file_path in files_to_process:
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            continue

        print(f"\n📝 Processing: {file_path.name}")
        stats = replace_in_file(file_path, REPLACEMENTS)

        if stats:
            results[file_path.name] = stats
            print(f"✅ Completed {len(stats)} replacement types")
            for old_text, count in sorted(stats.items(), key=lambda x: -x[1])[:10]:
                print(f"   - '{old_text}' → {count} occurrences")
        else:
            print(f"⚠️  No changes needed")

    # Generate JSON report
    import json
    from datetime import datetime

    report = {
        "task": "Restaurant SaaS to Digital Intelligence Platform Terminology Replacement",
        "timestamp": datetime.now().isoformat(),
        "files_processed": len(files_to_process),
        "files_modified": len(results),
        "details": {
            filename: {
                "replacement_types": len(stats),
                "total_replacements": sum(stats.values()),
                "top_replacements": [
                    {"term": term, "count": count}
                    for term, count in sorted(stats.items(), key=lambda x: -x[1])[:10]
                ]
            }
            for filename, stats in results.items()
        },
        "summary": {
            "total_replacement_types": sum(len(stats) for stats in results.values()),
            "total_replacements": sum(sum(stats.values()) for stats in results.values()),
        }
    }

    report_path = Path("/Users/vincentlee/Desktop/ZTL数智化作战中心/reports/terminology-replacement-report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n\n📊 Report saved to: {report_path}")
    print(f"\n{'='*60}")
    print(f"🎯 SUMMARY")
    print(f"{'='*60}")
    print(f"Files processed: {report['files_processed']}")
    print(f"Files modified: {report['files_modified']}")
    print(f"Total replacement types: {report['summary']['total_replacement_types']}")
    print(f"Total replacements: {report['summary']['total_replacements']}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
