#!/usr/bin/env python3
"""
美团报表中心 - SOP Skills 批量生成脚本
为每个报表类型自动生成 skill-seeker 配置文件
"""

import os
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any

# 报表基础URL模板
BASE_URL = "https://pos.meituan.com/web/report/main#/rms-report"

# 报表类型与URL映射(基于实际页面结构)
REPORT_CATEGORIES = {
    "财务报表": {
        "发票": {
            "发票统计": {
                "url": f"{BASE_URL}/invoice-statistics",
                "description": "查看和导出发票统计数据",
                "form_fields": [
                    {"name": "time_range", "type": "daterange", "label": "查询时间", "required": True},
                    {"name": "store_ids", "type": "multiselect", "label": "门店选择", "required": True},
                    {"name": "invoice_type", "type": "select", "label": "发票类型", "options": ["普通发票", "专用发票", "电子发票"]},
                ]
            },
            "发票明细": {
                "url": f"{BASE_URL}/invoice-detail",
                "description": "查看和导出发票开具明细数据",
                "form_fields": [
                    {"name": "time_range", "type": "daterange", "label": "开票时间", "required": True},
                    {"name": "store_ids", "type": "multiselect", "label": "门店选择", "required": True},
                    {"name": "invoice_status", "type": "select", "label": "发票状态", "options": ["已开具", "已作废", "待开具"]},
                ]
            }
        },
        "记账本": {
            "利润表": {
                "url": f"{BASE_URL}/profit-statement",
                "description": "查看和导出门店利润表",
                "form_fields": [
                    {"name": "time_range", "type": "daterange", "label": "统计时间", "required": True},
                    {"name": "store_ids", "type": "multiselect", "label": "门店选择", "required": True},
                    {"name": "report_type", "type": "select", "label": "报表类型", "options": ["日报", "月报", "年报"]},
                ]
            },
            "记账本支出统计": {
                "url": f"{BASE_URL}/expense-statistics",
                "description": "统计门店各项支出情况",
                "form_fields": [
                    {"name": "time_range", "type": "daterange", "label": "统计时间", "required": True},
                    {"name": "store_ids", "type": "multiselect", "label": "门店选择", "required": True},
                    {"name": "expense_type", "type": "select", "label": "支出类型", "options": ["原材料", "人工", "房租", "水电", "其他"]},
                ]
            }
        },
        "财务稽核": {
            "菜品叫损统计": {
                "url": f"{BASE_URL}/dish-loss-statistics",
                "description": "统计菜品叫起后损耗情况",
                "form_fields": [
                    {"name": "time_range", "type": "daterange", "label": "统计时间", "required": True},
                    {"name": "store_ids", "type": "multiselect", "label": "门店选择", "required": True},
                    {"name": "dish_category", "type": "select", "label": "菜品分类", "required": False},
                ]
            }
        }
    },
    "营业报表": {
        "营业统计": {
            "综合营业统计": {
                "url": f"{BASE_URL}/businessSummary",
                "description": "查看门店综合营业数据统计",
                "form_fields": [
                    {"name": "time_range", "type": "daterange", "label": "营业时间", "required": True},
                    {"name": "store_ids", "type": "multiselect", "label": "门店选择", "required": True},
                    {"name": "data_type", "type": "select", "label": "数据维度", "options": ["日报", "周报", "月报"]},
                ]
            },
            "部门营业统计": {
                "url": f"{BASE_URL}/department-sales",
                "description": "按部门统计营业数据",
                "form_fields": [
                    {"name": "time_range", "type": "daterange", "label": "营业时间", "required": True},
                    {"name": "store_ids", "type": "multiselect", "label": "门店选择", "required": True},
                    {"name": "department_ids", "type": "multiselect", "label": "部门选择", "required": False},
                ]
            }
        },
        "订单": {
            "全渠道订单明细": {
                "url": f"{BASE_URL}/all-order-detail",
                "description": "查看所有渠道订单明细",
                "form_fields": [
                    {"name": "time_range", "type": "daterange", "label": "下单时间", "required": True},
                    {"name": "store_ids", "type": "multiselect", "label": "门店选择", "required": True},
                    {"name": "order_channel", "type": "select", "label": "订单渠道", "options": ["堂食", "外卖", "自提", "平台外卖"]},
                    {"name": "order_status", "type": "select", "label": "订单状态", "options": ["已完成", "已取消", "进行中"]},
                ]
            }
        }
    },
    "菜品报表": {
        "菜品销售": {
            "菜品销售统计": {
                "url": f"{BASE_URL}/dishSale",
                "description": "统计各菜品销售情况",
                "form_fields": [
                    {"name": "time_range", "type": "daterange", "label": "销售时间", "required": True},
                    {"name": "store_ids", "type": "multiselect", "label": "门店选择", "required": True},
                    {"name": "dish_category", "type": "select", "label": "菜品分类", "required": False},
                    {"name": "sort_by", "type": "select", "label": "排序方式", "options": ["销量", "销售额", "利润"]},
                ]
            }
        }
    },
    "收款报表": {
        "平台结算": {
            "支付明细": {
                "url": f"{BASE_URL}/payment",
                "description": "查看每笔订单的支付明细",
                "form_fields": [
                    {"name": "time_range", "type": "daterange", "label": "支付时间", "required": True},
                    {"name": "store_ids", "type": "multiselect", "label": "门店选择", "required": True},
                    {"name": "payment_method", "type": "select", "label": "支付方式", "options": ["微信", "支付宝", "现金", "银行卡", "团购券"]},
                ]
            },
            "支付结算": {
                "url": f"{BASE_URL}/settlement-list",
                "description": "查看美团金融每日结算明细",
                "form_fields": [
                    {"name": "time_range", "type": "daterange", "label": "结算时间", "required": True},
                    {"name": "store_ids", "type": "multiselect", "label": "门店选择", "required": True},
                    {"name": "settlement_status", "type": "select", "label": "结算状态", "options": ["已结算", "结算中", "待结算"]},
                ]
            }
        }
    }
}


def generate_skill_config(category: str, subcategory: str, report_name: str, report_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    生成单个报表的 skill-seeker 配置
    """
    # 构建skill名称(kebab-case)
    skill_name = f"{report_name.lower().replace(' ', '-')}"

    # 生成SKILL.md的内容
    skill_md_content = f"""---
name: {report_name}导出
description: 美团管家报表中心 - {category}/{subcategory}/{report_name} 报表导出SOP
---

# {report_name}导出

## 🎯 功能概述

从美团管家报表中心导出{report_name}数据。

**报表路径**: {category} > {subcategory} > {report_name}

**直接访问URL**: [{report_config['url']}]({report_config['url']})

## 📋 操作步骤

### 1. 访问报表页面

```
访问URL: {report_config['url']}
等待页面加载完成
```

### 2. 填写筛选条件

"""

    # 添加表单字段说明
    for field in report_config['form_fields']:
        required_mark = "✅ 必填" if field.get('required', False) else "⭕ 可选"
        skill_md_content += f"\n**{field['label']}** ({required_mark})\n"
        skill_md_content += f"- 字段名: `{field['name']}`\n"
        skill_md_content += f"- 类型: `{field['type']}`\n"

        if 'options' in field:
            skill_md_content += f"- 可选值: {', '.join(field['options'])}\n"

        # 添加字段操作提示
        if field['type'] == 'daterange':
            skill_md_content += f"- 操作: 点击日期选择器,选择起始和结束日期\n"
        elif field['type'] == 'multiselect':
            skill_md_content += f"- 操作: 勾选需要查询的{field['label']}\n"
        elif field['type'] == 'select':
            skill_md_content += f"- 操作: 从下拉菜单中选择\n"

        skill_md_content += "\n"

    skill_md_content += """
### 3. 查询数据

```
点击"查询"按钮
等待数据加载完成
检查数据是否正确显示
```

### 4. 导出报表

```
点击"导出"按钮
选择导出格式(通常为Excel)
确认导出
等待下载完成
```

### 5. 验证导出结果

```
打开下载的文件
检查数据完整性
确认时间范围和筛选条件正确
```

## 🔧 Chrome MCP 自动化脚本

使用 chrome-mcp 工具自动化执行导出流程:

```python
# 1. 导航到报表页面
chrome_navigate(url="{report_config['url']}")

# 2. 等待页面加载
wait_for_element(selector=".report-container")

"""

    # 添加表单填写自动化脚本
    for field in report_config['form_fields']:
        if field['type'] == 'daterange':
            skill_md_content += f"""
# 3. 填写{field['label']}
click_element(selector="[placeholder*='{field['label']}']")
fill_daterange(start_date="{{start_date}}", end_date="{{end_date}}")
"""
        elif field['type'] == 'multiselect':
            skill_md_content += f"""
# 4. 选择{field['label']}
click_element(selector="[placeholder*='{field['label']}']")
select_options(values="{{selected_{field['name']}}}")
"""
        elif field['type'] == 'select':
            skill_md_content += f"""
# 5. 选择{field['label']}
select_option(selector="[name='{field['name']}']", value="{{selected_value}}")
"""

    skill_md_content += """
# 6. 点击查询按钮
click_element(selector="button:has-text('查询')")
wait_for_data_load()

# 7. 点击导出按钮
click_element(selector="button:has-text('导出')")
wait_for_download()
```

## 📝 注意事项

- ✅ 确保已登录美团管家系统
- ✅ 确保有权限访问该报表
- ✅ 导出大量数据时需要等待较长时间
- ✅ 建议在营业结束后导出以获取完整数据
- ⚠️ 跨天结账的门店注意营业日的定义
- ⚠️ 数据更新可能有延迟,建议查询前一天的数据

## 🔗 相关文档

- [美团管家报表中心使用指南](https://pos.meituan.com/web/report/main#/rms-report/help)
- [报表数据说明](https://h5.dianping.com/app/cs-faas-page/saas-mvp/video-list.html)
"""

    return {
        "skill_name": skill_name,
        "skill_md_content": skill_md_content,
        "config": report_config
    }


def create_skill_directory(base_path: Path, category: str, subcategory: str, report_name: str, skill_config: Dict[str, Any]):
    """
    创建skill目录结构并写入配置文件
    """
    # 构建目录路径
    skill_dir = base_path / category / subcategory / report_name
    skill_dir.mkdir(parents=True, exist_ok=True)

    # 写入SKILL.md
    skill_md_path = skill_dir / "SKILL.md"
    with open(skill_md_path, 'w', encoding='utf-8') as f:
        f.write(skill_config['skill_md_content'])

    # 写入config.json(用于skill-seeker)
    config_json_path = skill_dir / "config.json"
    config_data = {
        "name": f"{report_name}导出",
        "url": skill_config['config']['url'],
        "description": skill_config['config']['description'],
        "max_pages": 1,
        "rate_limit": 0.5,
        "selectors": {
            "query_button": "button:has-text('查询')",
            "export_button": "button:has-text('导出')",
            "form_fields": skill_config['config']['form_fields']
        }
    }

    with open(config_json_path, 'w', encoding='utf-8') as f:
        json.dump(config_data, f, ensure_ascii=False, indent=2)

    return skill_dir


def process_report(args):
    """
    处理单个报表的skill生成(用于多线程)
    """
    category, subcategory, report_name, report_config, base_path = args

    try:
        # 生成skill配置
        skill_config = generate_skill_config(category, subcategory, report_name, report_config)

        # 创建目录和文件
        skill_dir = create_skill_directory(base_path, category, subcategory, report_name, skill_config)

        return {
            "success": True,
            "report": f"{category}/{subcategory}/{report_name}",
            "path": str(skill_dir)
        }
    except Exception as e:
        return {
            "success": False,
            "report": f"{category}/{subcategory}/{report_name}",
            "error": str(e)
        }


def main():
    """
    主函数 - 批量生成所有报表的skill配置
    """
    base_path = Path("plugins/美团组/skills/报表中心/workflows/报表导出")

    # 收集所有报表任务
    tasks = []
    for category, subcategories in REPORT_CATEGORIES.items():
        for subcategory, reports in subcategories.items():
            for report_name, report_config in reports.items():
                tasks.append((category, subcategory, report_name, report_config, base_path))

    print(f"🚀 开始生成 {len(tasks)} 个报表的SOP型skills配置...")
    print(f"📁 输出目录: {base_path}")
    print("=" * 80)

    # 使用线程池并发处理
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_report, task) for task in tasks]

        for future in as_completed(futures):
            result = future.result()
            results.append(result)

            if result['success']:
                print(f"✅ {result['report']} -> {result['path']}")
            else:
                print(f"❌ {result['report']} -> 错误: {result['error']}")

    # 统计结果
    success_count = sum(1 for r in results if r['success'])
    fail_count = len(results) - success_count

    print("=" * 80)
    print(f"📊 生成完成!")
    print(f"   ✅ 成功: {success_count}")
    print(f"   ❌ 失败: {fail_count}")
    print(f"   📁 总计: {len(results)}")


if __name__ == "__main__":
    main()
