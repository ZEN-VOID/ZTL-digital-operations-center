#!/usr/bin/env python3
"""
美团报表中心 - 完整SOP Skills 批量生成脚本
基于实际目录结构生成所有90+个报表的skill配置
"""

import os
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# 报表基础URL
BASE_URL = "https://pos.meituan.com/web/report/main#/rms-report"

# 通用表单字段模板(所有报表都包含这些基础字段)
COMMON_FORM_FIELDS = [
    {"name": "time_range", "type": "daterange", "label": "查询时间", "required": True, "description": "选择报表统计的时间范围"},
    {"name": "store_ids", "type": "multiselect", "label": "门店选择", "required": True, "description": "选择需要查询的门店"},
]

# 特定报表类型的额外字段
CATEGORY_SPECIFIC_FIELDS = {
    "财务报表": {
        "发票": [
            {"name": "invoice_type", "type": "select", "label": "发票类型", "options": ["普通发票", "专用发票", "电子发票"]},
            {"name": "invoice_status", "type": "select", "label": "发票状态", "options": ["已开具", "已作废", "待开具"]},
        ],
        "记账本": [
            {"name": "account_type", "type": "select", "label": "账目类型", "options": ["收入", "支出", "全部"]},
        ],
        "财务稽核": [
            {"name": "audit_type", "type": "select", "label": "稽核类型", "options": ["菜品操作", "订单操作", "交班操作"]},
        ]
    },
    "营业报表": {
        "营业统计": [
            {"name": "time_dimension", "type": "select", "label": "时间维度", "options": ["按日", "按周", "按月"]},
            {"name": "department_ids", "type": "multiselect", "label": "部门选择", "required": False},
        ],
        "订单": [
            {"name": "order_channel", "type": "select", "label": "订单渠道", "options": ["堂食", "外卖", "自提", "平台外卖", "全部"]},
            {"name": "order_status", "type": "select", "label": "订单状态", "options": ["已完成", "已取消", "进行中", "全部"]},
        ],
        "收入优惠": [
            {"name": "discount_type", "type": "select", "label": "优惠类型", "options": ["折扣", "券", "赠送", "全部"]},
        ]
    },
    "菜品报表": {
        "菜品销售": [
            {"name": "dish_category", "type": "select", "label": "菜品分类", "required": False},
            {"name": "sort_by", "type": "select", "label": "排序方式", "options": ["销量", "销售额", "利润"]},
        ],
        "菜品属性": [
            {"name": "attribute_type", "type": "select", "label": "属性类型", "options": ["规格", "做法", "加料", "餐盒"]},
        ]
    },
    "收款报表": {
        "平台结算": [
            {"name": "payment_method", "type": "select", "label": "支付方式", "options": ["微信", "支付宝", "现金", "银行卡", "团购券", "全部"]},
            {"name": "settlement_status", "type": "select", "label": "结算状态", "options": ["已结算", "结算中", "待结算"]},
        ],
        "营业收款": [
            {"name": "cashier_id", "type": "select", "label": "收银员", "required": False},
        ]
    },
    "运营报表": {
        "活消后厨": [
            {"name": "kitchen_area", "type": "select", "label": "后厨区域", "required": False},
        ],
        "门店运营": [
            {"name": "operation_type", "type": "select", "label": "运营类型", "options": ["制作", "叫号", "配送"]},
        ]
    }
}

# URL路径映射(根据报表名称推断URL)
def generate_url_from_name(report_name: str) -> str:
    """根据报表名称生成URL路径"""
    # 简单的URL映射规则
    url_mapping = {
        "发票统计": "invoice-statistics",
        "发票明细": "invoice-detail",
        "利润表": "profit-statement",
        "记账本支出统计": "expense-statistics",
        "记账本收支统计": "income-expense-statistics",
        "营业收入与收款统计": "income-collection-statistics",
        "记账本收支明细": "income-expense-detail",
        "门店收支统计": "store-income-expense",
        "菜品叫损统计": "dish-loss-statistics",
        "缴惠操作统计": "discount-operation-statistics",
        "订单敏感操作明细": "order-sensitive-operation-detail",
        "交班统计": "shift-handover-statistics",
        "菜品敏感操作明细": "dish-sensitive-operation-detail",
        "时段开台分析": "time-slot-table-analysis",
        "餐区桌台营业统计": "dining-area-table-statistics",
        "组织营业统计": "organization-sales-statistics",
        "综合营业统计": "businessSummary",
        "营业指标同环比": "sales-indicator-comparison",
        "部门餐段营业统计": "department-meal-period-statistics",
        "餐区部门营业统计": "dining-area-department-statistics",
        "部门营业统计": "department-sales-statistics",
        "促销活动统计": "promotion-activity-statistics",
        "桌渠营业统计": "table-channel-statistics",
        "餐厅线营业统计": "restaurant-line-statistics",
        "订单来源统计": "order-source-statistics",
        "区域营业统计": "region-sales-statistics",
        "收银员优惠统计": "cashier-discount-statistics",
        "收入优惠统计": "income-discount-statistics",
        "收入优惠明细": "income-discount-detail",
        "券收入统计": "voucher-income-statistics",
        "多店营业指标对比": "multi-store-sales-comparison",
        "营业指标统计": "sales-indicator-statistics",
        "自营外卖订单明细": "self-operated-takeout-order-detail",
        "平台外卖订单明细": "platform-takeout-order-detail",
        "团购配送订单明细": "group-buying-delivery-order-detail",
        "店内订单明细": "in-store-order-detail",
        "全渠道订单明细": "all-channel-order-detail",
        "菜品销售统计": "dishSale",
        "菜品销售明细": "dish-sale-detail",
        "支付明细": "payment",
        "支付结算": "settlement-list",
        "营业收款统计": "business-collection-statistics",
        "综合收款统计": "comprehensive-collection-statistics",
    }

    # 尝试精确匹配
    if report_name in url_mapping:
        return f"{BASE_URL}/{url_mapping[report_name]}"

    # 否则生成通用URL
    url_slug = report_name.lower()
    # 移除常见词汇
    url_slug = re.sub(r'(统计|明细|分析|报表)', '', url_slug)
    # 转换为kebab-case
    url_slug = re.sub(r'[^\w\s-]', '', url_slug)
    url_slug = re.sub(r'[\s_]+', '-', url_slug)
    return f"{BASE_URL}/{url_slug}"


def get_form_fields_for_report(category: str, subcategory: str) -> list:
    """
    根据报表分类获取对应的表单字段
    """
    fields = COMMON_FORM_FIELDS.copy()

    # 添加分类特定的字段
    if category in CATEGORY_SPECIFIC_FIELDS:
        category_fields = CATEGORY_SPECIFIC_FIELDS[category]
        if subcategory in category_fields:
            fields.extend(category_fields[subcategory])
        elif "__default__" in category_fields:
            fields.extend(category_fields["__default__"])

    return fields


def generate_skill_md(category: str, subcategory: str, report_name: str, url: str, form_fields: list) -> str:
    """
    生成SKILL.md内容
    """
    content = f"""---
name: {report_name}导出
description: 美团管家报表中心 - {category}/{subcategory}/{report_name} 报表导出SOP
---

# {report_name}导出

## 🎯 功能概述

从美团管家报表中心导出{report_name}数据。

**报表路径**: {category} > {subcategory} > {report_name}

**直接访问URL**: [{url}]({url})

## 📋 操作步骤

### 1. 访问报表页面

```
访问URL: {url}
等待页面加载完成
确认页面标题显示"{report_name}"
```

### 2. 填写筛选条件

"""

    # 添加表单字段说明
    for i, field in enumerate(form_fields, 1):
        required_mark = "✅ 必填" if field.get('required', False) else "⭕ 可选"
        content += f"\n**{i}. {field['label']}** ({required_mark})\n"
        content += f"- 字段名: `{field['name']}`\n"
        content += f"- 类型: `{field['type']}`\n"

        if 'options' in field:
            content += f"- 可选值: {', '.join(field['options'])}\n"

        if 'description' in field:
            content += f"- 说明: {field['description']}\n"

        # 添加字段操作提示
        if field['type'] == 'daterange':
            content += f"- 操作: 点击日期选择器,选择起始日期和结束日期\n"
        elif field['type'] == 'multiselect':
            content += f"- 操作: 勾选需要查询的{field['label']}\n"
        elif field['type'] == 'select':
            content += f"- 操作: 从下拉菜单中选择{field['label']}\n"

    content += """
### 3. 查询数据

```
点击"查询"按钮
等待数据加载完成(通常1-5秒)
检查数据表格是否正确显示
确认数据条数和时间范围
```

### 4. 导出报表

```
点击"导出"或"下载"按钮
选择导出格式(Excel/CSV)
确认导出
等待下载完成(大数据量可能需要几分钟)
```

### 5. 验证导出结果

```
打开下载的Excel文件
检查数据完整性:
  - 表头字段是否完整
  - 数据行数是否正确
  - 数值计算是否准确
确认时间范围和筛选条件正确
```

## 🔧 Chrome MCP 自动化脚本

使用 chrome-mcp 工具自动化执行导出流程:

```javascript
// 1. 导航到报表页面
await chrome_navigate({
  url: "{url}",
  waitForSelector: ".report-container"
});

"""

    # 添加表单填写自动化脚本
    for field in form_fields:
        if field['type'] == 'daterange':
            content += f"""
// 2. 填写{field['label']}
await chrome_click_element({{
  selector: "[placeholder*='{field['label']}']"
}});
await chrome_fill_form({{
  fields: [
    {{selector: "input[name='startDate']", value: "{{{{start_date}}}}" }},
    {{selector: "input[name='endDate']", value: "{{{{end_date}}}}" }}
  ]
}});
"""
        elif field['type'] == 'multiselect':
            content += f"""
// 3. 选择{field['label']}
await chrome_click_element({{
  selector: "[placeholder*='{field['label']}']"
}});
// 勾选所有选项或指定选项
await chrome_click_element({{
  selector: ".ant-select-dropdown .ant-checkbox-wrapper"
}});
"""
        elif field['type'] == 'select':
            content += f"""
// 4. 选择{field['label']}
await chrome_click_element({{
  selector: "[name='{field['name']}']"
}});
await chrome_click_element({{
  textQuery: "{{{{selected_value}}}}"
}});
"""

    content += """
// 5. 点击查询按钮
await chrome_click_element({
  selector: "button:has-text('查询')"
});

// 6. 等待数据加载
await chrome_wait_for({
  text: "查询成功",
  timeout: 30000
});

// 7. 点击导出按钮
await chrome_click_element({
  selector: "button:has-text('导出')"
});

// 8. 等待下载完成
await chrome_wait_for({
  text: "导出成功",
  timeout: 60000
});
```

## 📝 注意事项

### 权限要求
- ✅ 确保已登录美团管家系统
- ✅ 确保有权限访问该报表
- ✅ 确认账号具有数据导出权限

### 数据时效性
- ⚠️ 数据更新延迟: T+1天(建议查询前一天的数据)
- ⚠️ 跨天结账: 注意营业日的定义(结账时间决定营业日)
- ⚠️ 实时数据: 当天数据可能不完整

### 性能建议
- 💡 单次导出不超过3个月数据(避免超时)
- 💡 大数据量分批导出(按月/按周)
- 💡 避开营业高峰时段导出
- 💡 建议在营业结束后(22:00后)导出完整数据

### 常见问题
1. **导出超时**: 缩小时间范围或减少门店数量
2. **数据为空**: 检查时间范围和筛选条件
3. **数据不一致**: 等待数据同步完成后重新导出
4. **下载失败**: 检查浏览器下载设置和磁盘空间

## 🔗 相关文档

- [美团管家报表中心帮助文档](https://pos.meituan.com/web/report/main#/rms-report/help)
- [报表数据说明视频](https://h5.dianping.com/app/cs-faas-page/saas-mvp/video-list.html)
- [常见问题FAQ](https://h5.dianping.com/app/cs-faas-page/saas-mvp/video-list.html?id=2)

## 📊 字段说明

"""

    # 根据报表类型添加关键字段说明
    if "营业" in report_name or "收入" in report_name:
        content += """
### 关键指标定义
- **营业额**: 订单原价总和
- **营业收入**: 实际到账金额 = 营业额 - 优惠金额
- **营业收款**: 实际收到的现金流
- **优惠金额**: 各类折扣、券、赠送等优惠总额
"""
    elif "菜品" in report_name:
        content += """
### 关键指标定义
- **销量**: 菜品销售份数
- **销售额**: 菜品销售总金额
- **成本**: 菜品原材料成本
- **毛利**: 销售额 - 成本
- **毛利率**: (毛利 / 销售额) × 100%
"""
    elif "收款" in report_name or "支付" in report_name:
        content += """
### 关键指标定义
- **应收金额**: 订单应收款项
- **实收金额**: 实际收到的款项
- **支付方式**: 现金、微信、支付宝、银行卡等
- **结算金额**: 平台结算给商家的金额
- **手续费**: 平台收取的服务费
"""

    content += """
## 📈 数据用途

本报表数据可用于:
"""

    # 根据报表类型添加数据用途说明
    if "财务" in category or "收款" in category:
        content += """
- ✅ 财务对账和结算核对
- ✅ 成本控制和利润分析
- ✅ 资金流水管理
- ✅ 税务申报数据准备
"""
    elif "营业" in category:
        content += """
- ✅ 门店经营分析
- ✅ 销售趋势预测
- ✅ 营业目标达成跟踪
- ✅ 多店对比分析
"""
    elif "菜品" in category:
        content += """
- ✅ 菜品销售分析
- ✅ 菜单优化决策
- ✅ 库存采购计划
- ✅ 定价策略调整
"""
    elif "运营" in category:
        content += """
- ✅ 运营效率分析
- ✅ 人力资源配置
- ✅ 后厨效能提升
- ✅ 服务质量监控
"""

    content += """
---

*本文档由 ZTL数智化作战中心 自动生成*
*最后更新: 2025-11-04*
"""

    return content


def process_single_report(args):
    """
    处理单个报表的skill生成(用于多线程)
    """
    base_path, category, subcategory, report_name = args

    try:
        # 生成URL
        url = generate_url_from_name(report_name)

        # 获取表单字段
        form_fields = get_form_fields_for_report(category, subcategory)

        # 生成SKILL.md内容
        skill_md_content = generate_skill_md(category, subcategory, report_name, url, form_fields)

        # 创建目录
        skill_dir = base_path / category / subcategory / report_name
        skill_dir.mkdir(parents=True, exist_ok=True)

        # 写入SKILL.md
        skill_md_path = skill_dir / "SKILL.md"
        with open(skill_md_path, 'w', encoding='utf-8') as f:
            f.write(skill_md_content)

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


def scan_existing_directories(base_path: Path) -> list:
    """
    扫描现有的报表目录结构
    """
    reports = []

    # 遍历所有三级目录
    for category_dir in base_path.iterdir():
        if not category_dir.is_dir():
            continue

        category = category_dir.name

        for subcategory_dir in category_dir.iterdir():
            if not subcategory_dir.is_dir():
                continue

            subcategory = subcategory_dir.name

            for report_dir in subcategory_dir.iterdir():
                if not report_dir.is_dir():
                    continue

                report_name = report_dir.name
                reports.append((base_path, category, subcategory, report_name))

    return reports


def main():
    """
    主函数 - 扫描现有目录并生成所有报表的skill配置
    """
    base_path = Path("plugins/美团组/skills/报表中心/workflows/报表导出")

    print("📁 扫描现有报表目录结构...")
    reports = scan_existing_directories(base_path)

    print(f"🚀 找到 {len(reports)} 个报表目录")
    print(f"📁 输出目录: {base_path}")
    print("=" * 80)

    # 使用线程池并发处理
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_single_report, report) for report in reports]

        for future in as_completed(futures):
            result = future.result()
            results.append(result)

            if result['success']:
                print(f"✅ {result['report']}")
            else:
                print(f"❌ {result['report']} -> {result['error']}")

    # 统计结果
    success_count = sum(1 for r in results if r['success'])
    fail_count = len(results) - success_count

    print("=" * 80)
    print(f"📊 生成完成!")
    print(f"   ✅ 成功: {success_count}")
    print(f"   ❌ 失败: {fail_count}")
    print(f"   📁 总计: {len(results)}")

    # 列出所有成功生成的报表
    if success_count > 0:
        print("\n✅ 成功生成的报表:")
        for result in results:
            if result['success']:
                print(f"   - {result['report']}")


if __name__ == "__main__":
    main()
