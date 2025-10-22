"""
Example: Business Report Generation

This example demonstrates creating a comprehensive business report
with various formatting elements.
"""

import sys
from pathlib import Path

# Add skill to path
skill_path = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(skill_path))

from word_generator import create_document


def create_business_report():
    """Create a sample business report."""

    content = [
        # Executive Summary
        {"type": "heading", "level": 1, "text": "执行摘要"},
        {
            "type": "paragraph",
            "text": "本报告总结了2025年第三季度的经营情况。整体业绩良好，营业额同比增长25%，达到450万元。主要增长来自新品推出和线上渠道扩张。"
        },

        # Section 1: Sales Performance
        {"type": "heading", "level": 1, "text": "一、销售业绩"},
        {"type": "heading", "level": 2, "text": "1.1 总体情况"},
        {
            "type": "paragraph",
            "text": "Q3季度各门店销售情况如下："
        },
        {
            "type": "table",
            "headers": ["门店", "营业额(万元)", "同比增长", "环比增长"],
            "rows": [
                ["A店(总店)", "150", "+25%", "+10%"],
                ["B店(分店)", "120", "+20%", "+8%"],
                ["C店(新店)", "80", "新开", "新开"],
                ["线上渠道", "100", "+50%", "+20%"],
                ["合计", "450", "+25%", "+12%"]
            ]
        },

        {"type": "heading", "level": 2, "text": "1.2 关键洞察"},
        {
            "type": "bullet_list",
            "items": [
                "新店C店开业第一个月即达到预期目标的80%",
                "线上渠道增长迅猛，占总营业额的22%",
                "A店作为旗舰店保持稳定增长",
                "外卖业务占比提升至35%"
            ]
        },

        # Section 2: Product Analysis
        {"type": "heading", "level": 1, "text": "二、产品分析"},
        {"type": "heading", "level": 2, "text": "2.1 新品表现"},
        {
            "type": "paragraph",
            "text": "Q3推出的3款新品表现优异："
        },
        {
            "type": "numbered_list",
            "items": [
                "麻辣小龙虾火锅 - 销量第1，贡献营业额15%",
                "养生菌汤锅底 - 客单价最高，提升品牌形象",
                "夏日特饮系列 - 带动饮品销售增长40%"
            ]
        },

        {"type": "heading", "level": 2, "text": "2.2 产品优化建议"},
        {
            "type": "bullet_list",
            "items": [
                "继续推广新品，建议增加促销力度",
                "优化传统菜品，降低成本提升利润",
                "开发秋冬季节限定产品",
                "加强产品质量管控"
            ]
        },

        # Section 3: Cost Analysis
        {"type": "heading", "level": 1, "text": "三、成本分析"},
        {
            "type": "paragraph",
            "text": "主要成本项目占比如下："
        },
        {
            "type": "table",
            "headers": ["成本项目", "金额(万元)", "占营业额比例", "同比变化"],
            "rows": [
                ["食材成本", "135", "30%", "+2%"],
                ["人力成本", "90", "20%", "+5%"],
                ["房租水电", "45", "10%", "持平"],
                ["营销费用", "27", "6%", "+3%"],
                ["其他费用", "18", "4%", "+1%"],
                ["合计", "315", "70%", "+2.5%"]
            ]
        },

        # Section 4: Issues and Solutions
        {"type": "heading", "level": 1, "text": "四、问题与对策"},
        {"type": "heading", "level": 2, "text": "4.1 主要问题"},
        {
            "type": "numbered_list",
            "items": [
                "人力成本上升明显，员工流失率偏高",
                "部分食材价格上涨，影响利润率",
                "竞争对手开业，对B店产生一定影响",
                "新店运营经验不足，需要总部支持"
            ]
        },

        {"type": "heading", "level": 2, "text": "4.2 应对措施"},
        {
            "type": "bullet_list",
            "items": [
                "优化薪酬体系，加强员工培训和激励",
                "与供应商谈判，签订长期合作协议锁定价格",
                "加强品牌营销，突出差异化优势",
                "派遣资深店长支持新店，建立标准化运营体系"
            ]
        },

        # Section 5: Q4 Plan
        {"type": "heading", "level": 1, "text": "五、Q4行动计划"},
        {
            "type": "table",
            "headers": ["行动项", "负责人", "完成时间", "预期效果"],
            "rows": [
                ["推出秋冬新品3款", "产品部", "10月底", "提升10%营业额"],
                ["启动会员营销活动", "营销部", "11月初", "增加5000会员"],
                ["优化供应链成本", "采购部", "持续进行", "降低2%成本"],
                ["新店运营培训", "运营部", "10月中", "提升新店效率"]
            ]
        },

        # Conclusion
        {"type": "heading", "level": 1, "text": "六、总结"},
        {
            "type": "paragraph",
            "text": "Q3整体表现良好，达成了季度目标。Q4将继续保持增长势头，重点关注成本控制和新店运营，力争全年营业额突破1800万元，实现30%的同比增长。"
        }
    ]

    result = create_document(
        title="2025年Q3经营分析报告",
        content=content,
        output_path="output/行政组/经营分析/q3-business-report.docx",
        author="数据分析组"
    )

    if result["success"]:
        print(f"✅ 报告已生成: {result['file_path']}")
        print(f"📄 文件大小: {result['size_bytes']:,} bytes")
    else:
        print(f"❌ 生成失败: {result['error']}")


if __name__ == "__main__":
    create_business_report()
