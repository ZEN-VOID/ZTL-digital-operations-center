"""
Example: Direct PPT Generation

This example demonstrates creating a presentation programmatically
using the PPTGenerator class with fluent API.
"""

import sys
from pathlib import Path

# Add skill to path
skill_path = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(skill_path))

from ppt_generator import PPTGenerator


def create_marketing_presentation():
    """Create a marketing presentation using direct generation."""

    generator = PPTGenerator()

    # Title slide
    generator.add_title_slide(
        title="ZTL数智化作战中心",
        subtitle="餐饮行业数智化转型解决方案"
    )

    # Overview slide
    generator.add_content_slide(
        title="产品概述",
        content=[
            "基于Claude Code的智能体协作平台",
            "6大业务组、66个专业智能体",
            "覆盖战略、创意、情报、行政、中台、筹建",
            "实现餐饮行业全链路数智化管理"
        ]
    )

    # Two-column comparison
    generator.add_two_column_slide(
        title="传统模式 vs 数智化模式",
        left_content=[
            "人工决策，效率低",
            "数据分散，难以分析",
            "经验驱动，缺乏科学性",
            "响应慢，错过商机"
        ],
        right_content=[
            "AI辅助，智能决策",
            "数据集中，实时分析",
            "数据驱动，精准决策",
            "快速响应，抓住机会"
        ]
    )

    # Business matrix table
    generator.add_table_slide(
        title="业务矩阵",
        headers=["业务组", "系列", "智能体数量", "核心职能"],
        rows=[
            ["战略组", "G系列", "9个", "战略规划、经营分析、产品力打造"],
            ["创意组", "X系列", "9个", "广告策划、文案创作、视觉设计"],
            ["情报组", "E系列", "8个", "数据采集、深度分析、情报研究"],
            ["行政组", "R系列", "8个", "财务管理、人事管理、行政协同"],
            ["中台组", "M系列", "6个", "美团运营、营销管理、数据报表"],
            ["筹建组", "Z系列", "6个", "平面设计、BIM建模、空间设计"]
        ]
    )

    # Chart slide - Growth metrics
    generator.add_chart_slide(
        title="效率提升数据",
        chart_type="column",
        data={
            "categories": ["决策效率", "运营效率", "营销ROI", "成本节约"],
            "series": [
                {
                    "name": "传统模式",
                    "values": [100, 100, 100, 100]
                },
                {
                    "name": "数智化模式",
                    "values": [300, 130, 150, 115]
                }
            ]
        }
    )

    # Success cases
    generator.add_content_slide(
        title="成功案例",
        content=[
            "某连锁火锅品牌：3个月内新开5家门店，筹建周期缩短40%",
            "某茶饮品牌：营销活动ROI提升50%，会员增长200%",
            "某快餐品牌：供应链成本降低15%，库存周转率提升30%",
            "某咖啡品牌：经营数据实时分析，决策效率提升3倍"
        ]
    )

    # Contact slide
    generator.add_content_slide(
        title="联系我们",
        content=[
            "产品咨询：contact@ztl.com",
            "技术支持：support@ztl.com",
            "商务合作：business@ztl.com",
            "官方网站：www.ztl.com"
        ]
    )

    # Save presentation
    result = generator.save("output/行政组/营销宣传/ztl-marketing-direct.pptx")

    if result["success"]:
        print(f"✅ 营销演示已生成: {result['file_path']}")
        print(f"📊 幻灯片数量: {result['slide_count']}")
        print(f"📄 文件大小: {result['size_bytes']:,} bytes")
    else:
        print(f"❌ 生成失败: {result['error']}")


if __name__ == "__main__":
    create_marketing_presentation()
