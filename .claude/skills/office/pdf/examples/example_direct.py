"""
Example: Direct PDF Generation with ReportLab

Demonstrates creating a professional business report using direct PDF generation.
This is the recommended method for complex layouts and precise control.
"""

import sys
from pathlib import Path

# Add skill to path
skill_path = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(skill_path))

from pdf_generator import create_pdf_direct


def create_business_report():
    """Create a comprehensive business report PDF."""

    content = [
        # Executive Summary
        {"type": "heading", "text": "执行摘要", "level": 1},
        {
            "type": "paragraph",
            "text": "2025年Q3季度业绩优异，营业额达到450万元，同比增长25%。主要增长来自新品推出和线上渠道扩张。"
        },

        {"type": "spacer", "height": 0.3},

        # Sales Data
        {"type": "heading", "text": "一、销售数据", "level": 1},
        {"type": "heading", "text": "1.1 门店销售情况", "level": 2},

        {
            "type": "table",
            "headers": ["门店", "营业额(万元)", "同比增长", "环比增长"],
            "data": [
                ["A店(总店)", "150", "+25%", "+10%"],
                ["B店(分店)", "120", "+20%", "+8%"],
                ["C店(新店)", "80", "新开", "新开"],
                ["线上渠道", "100", "+50%", "+20%"],
                ["合计", "450", "+25%", "+12%"]
            ]
        },

        {"type": "heading", "text": "1.2 关键洞察", "level": 2},
        {
            "type": "bullet_list",
            "items": [
                "新店C店开业第一个月即达到预期目标的80%",
                "线上渠道增长迅猛，占总营业额的22%",
                "A店作为旗舰店保持稳定增长",
                "外卖业务占比提升至35%"
            ]
        },

        # Product Analysis
        {"type": "page_break"},
        {"type": "heading", "text": "二、产品分析", "level": 1},

        {"type": "heading", "text": "2.1 新品表现", "level": 2},
        {
            "type": "numbered_list",
            "items": [
                "麻辣小龙虾火锅 - 销量第1，贡献营业额15%",
                "养生菌汤锅底 - 客单价最高，提升品牌形象",
                "夏日特饮系列 - 带动饮品销售增长40%"
            ]
        },

        # Cost Analysis
        {"type": "heading", "text": "三、成本分析", "level": 1},
        {
            "type": "table",
            "headers": ["成本项目", "金额(万元)", "占比", "同比"],
            "data": [
                ["食材成本", "135", "30%", "+2%"],
                ["人力成本", "90", "20%", "+5%"],
                ["房租水电", "45", "10%", "持平"],
                ["营销费用", "27", "6%", "+3%"],
                ["其他费用", "18", "4%", "+1%"],
                ["合计", "315", "70%", "+2.5%"]
            ]
        },

        # Recommendations
        {"type": "heading", "text": "四、建议", "level": 1},
        {
            "type": "bullet_list",
            "items": [
                "继续加大新品研发力度，保持产品竞争力",
                "优化供应链，控制食材成本上涨",
                "加强员工培训，降低人员流失率",
                "扩大线上渠道投入，抓住数字化机遇"
            ]
        }
    ]

    result = create_pdf_direct(
        title="2025年Q3经营分析报告",
        content=content,
        output_path="output/行政组/经营分析/q3-business-report.pdf",
        page_size="A4",
        orientation="portrait",
        author="数据分析组"
    )

    if result["success"]:
        print(f"✅ PDF generated successfully")
        print(f"   File: {result['file_path']}")
        print(f"   Size: {result['size_bytes']:,} bytes")
        print(f"   Pages: {result.get('page_count', 'N/A')}")
    else:
        print(f"❌ Generation failed: {result['error']}")


if __name__ == "__main__":
    create_business_report()
