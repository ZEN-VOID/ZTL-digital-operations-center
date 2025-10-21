"""
Example: Template-based PPT Generation

This example demonstrates creating presentations using predefined templates.
"""

import sys
from pathlib import Path

# Add skill to path
skill_path = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(skill_path))

from ppt_generator import create_from_template


def create_business_report():
    """Create a business report using the business-report template."""

    data = {
        "title": "2025年Q3经营报告",
        "subtitle": "ZTL餐饮连锁集团",
        "period": "2025年7月-9月",
        "executive_summary": "Q3季度整体表现优异，营业额达到450万元，同比增长25%。新店C店成功开业，线上渠道增长迅猛。",
        "metrics": {
            "总营业额": "450万元 (+25%)",
            "门店数量": "4家 (+1)",
            "客单价": "85元 (+5%)",
            "会员数": "15,000人 (+30%)",
            "净利润率": "28% (+3%)"
        },
        "achievements": [
            "成功开设C店（新店），第一个月达到目标的80%",
            "线上渠道营业额突破100万，占总营业额22%",
            "推出3款新品，麻辣小龙虾火锅贡献15%营业额",
            "会员营销活动效果显著，新增会员5000人"
        ],
        "challenges": [
            "人力成本上升5%，员工流失率偏高需要改进",
            "部分食材价格上涨，影响利润率2个百分点",
            "竞争对手在B店附近开业，对B店造成一定影响",
            "新店C店运营经验不足，需要总部更多支持"
        ],
        "next_steps": [
            "优化薪酬体系，加强员工培训和激励机制",
            "与核心供应商签订长期合作协议锁定价格",
            "加强品牌营销，突出差异化优势",
            "派遣资深店长支持C店，建立标准化运营体系",
            "Q4目标：营业额600万，同比增长30%"
        ]
    }

    result = create_from_template(
        template_type="business-report",
        data=data,
        output_path="output/行政组/经营分析/q3-report-template.pptx"
    )

    if result["success"]:
        print(f"✅ Q3经营报告已生成: {result['file_path']}")
        print(f"📊 幻灯片数量: {result['slide_count']}")
        print(f"📄 文件大小: {result['size_bytes']:,} bytes")
    else:
        print(f"❌ 生成失败: {result['error']}")


def create_product_launch():
    """Create a product launch presentation using the product-launch template."""

    data = {
        "title": "秋冬新品发布",
        "subtitle": "ZTL 2025秋冬季限定系列",
        "product_name": "养生菌汤锅底",
        "tagline": "健康·养生·美味",
        "problem": "传统火锅油腻重口，缺乏健康养生选择，年轻消费者越来越注重饮食健康。",
        "solution": "推出养生菌汤锅底，精选8种珍稀菌菇，低脂低钠高营养，满足健康饮食需求。",
        "features": [
            "精选8种珍稀菌菇：羊肚菌、松茸、竹荪、猴头菇等",
            "72小时慢火熬制，保留菌菇精华营养",
            "0添加剂，低脂低钠，热量仅为传统锅底的1/3",
            "独特的复合鲜味，无需添加味精提鲜",
            "适合各年龄段，特别是注重养生的消费者"
        ],
        "benefits": [
            "健康养生：丰富的多糖和氨基酸，提升免疫力",
            "低卡路里：适合减脂人群，无负担享受美食",
            "鲜美可口：天然菌菇香气，层次丰富",
            "四季适宜：秋冬暖身，春夏清爽",
            "高性价比：定价88元/份，低于市场同类产品"
        ],
        "target_audience": "25-45岁都市白领，注重健康饮食，追求生活品质，愿意为健康支付溢价。",
        "timeline": [
            {"date": "10月15日", "milestone": "新品发布会"},
            {"date": "10月20日", "milestone": "全渠道上架销售"},
            {"date": "10月25日", "milestone": "KOL试吃活动"},
            {"date": "11月1日", "milestone": "会员专享优惠"},
            {"date": "11月11日", "milestone": "双11促销活动"}
        ]
    }

    result = create_from_template(
        template_type="product-launch",
        data=data,
        output_path="output/行政组/营销方案/autumn-new-product-launch.pptx"
    )

    if result["success"]:
        print(f"✅ 新品发布演示已生成: {result['file_path']}")
        print(f"📊 幻灯片数量: {result['slide_count']}")
        print(f"📄 文件大小: {result['size_bytes']:,} bytes")
    else:
        print(f"❌ 生成失败: {result['error']}")


if __name__ == "__main__":
    print("=" * 60)
    print("生成Q3经营报告...")
    print("=" * 60)
    create_business_report()

    print("\n" + "=" * 60)
    print("生成秋冬新品发布演示...")
    print("=" * 60)
    create_product_launch()
