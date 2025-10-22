"""
Example: Meeting Minutes Generation

This example demonstrates creating meeting minutes using the template system.
"""

import sys
from pathlib import Path

# Add skill to path
skill_path = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(skill_path))

from word_generator import create_from_template


def create_meeting_minutes():
    """Create sample meeting minutes."""

    data = {
        "title": "战略规划会议纪要",
        "date": "2025-10-21",
        "time": "14:00-16:30",
        "location": "总部会议室A",
        "host": "张总经理",
        "attendees": [
            "张总经理",
            "李运营总监",
            "王产品经理",
            "赵营销经理",
            "孙财务经理"
        ],
        "topics": [
            {
                "topic": "Q4战略目标讨论",
                "discussion": """
各位与会人员就Q4战略目标进行了深入讨论:

1. 张总经理提出Q4要实现营业额600万的目标,同比增长30%
2. 李运营总监分析了当前运营状况,认为目标具有挑战性但可实现
3. 王产品经理建议推出3款秋冬新品,预计贡献15%增量
4. 赵营销经理提出加大会员营销力度,提升复购率
5. 孙财务经理强调要严控成本,确保利润率不低于25%

经讨论,一致通过Q4战略目标及实施方案。
                """,
                "action_items": [
                    {
                        "task": "制定详细的Q4运营计划",
                        "owner": "李运营总监",
                        "deadline": "10-25"
                    },
                    {
                        "task": "完成新品研发和上市准备",
                        "owner": "王产品经理",
                        "deadline": "10-31"
                    },
                    {
                        "task": "策划会员营销活动方案",
                        "owner": "赵营销经理",
                        "deadline": "10-28"
                    },
                    {
                        "task": "制定成本控制措施",
                        "owner": "孙财务经理",
                        "deadline": "10-26"
                    }
                ]
            },
            {
                "topic": "新店选址评估",
                "discussion": """
讨论了D店和E店两个潜在选址方案:

D店方案(市中心商圈):
- 优点: 人流量大,品牌曝光度高,周边消费能力强
- 缺点: 租金较高(2.5万/月),竞争激烈
- 预估月营业额: 50-60万

E店方案(大学城商圈):
- 优点: 租金适中(1.5万/月),年轻客群多,消费潜力大
- 缺点: 消费能力相对较弱,季节性波动大
- 预估月营业额: 35-45万

经综合评估,初步倾向D店方案,但需进一步市场调研。
                """,
                "action_items": [
                    {
                        "task": "完成D店和E店详细商圈分析",
                        "owner": "李运营总监",
                        "deadline": "11-05"
                    },
                    {
                        "task": "制定两个方案的财务模型",
                        "owner": "孙财务经理",
                        "deadline": "11-08"
                    },
                    {
                        "task": "与房东进行租金谈判",
                        "owner": "张总经理",
                        "deadline": "11-10"
                    }
                ]
            },
            {
                "topic": "供应链优化方案",
                "discussion": """
孙财务经理提出当前供应链存在以下问题:
1. 食材成本占比30%,略高于行业平均水平
2. 部分食材浪费率达到8%,需要改进
3. 供应商较为分散,议价能力不足

提出优化方案:
1. 整合供应商,与3-5家核心供应商建立长期战略合作
2. 引入智能库存管理系统,降低损耗率
3. 建立中央厨房,统一初加工,提高效率
4. 探索产地直采模式,降低中间环节成本

预期效果: 降低食材成本2-3个百分点,年节约成本30-40万元
                """,
                "action_items": [
                    {
                        "task": "完成供应商整合方案",
                        "owner": "采购部经理",
                        "deadline": "11-15"
                    },
                    {
                        "task": "调研库存管理系统",
                        "owner": "IT部经理",
                        "deadline": "11-20"
                    },
                    {
                        "task": "评估中央厨房可行性",
                        "owner": "李运营总监",
                        "deadline": "11-30"
                    }
                ]
            }
        ],
        "next_meeting": "下次会议定于11月15日14:00,地点待定,议题为Q4中期进展review和新店选址最终决策。"
    }

    result = create_from_template(
        template_type="meeting-minutes",
        data=data,
        output_path="output/行政组/会议纪要/strategy-meeting-20251021.docx"
    )

    if result["success"]:
        print(f"✅ 会议纪要已生成: {result['file_path']}")
        print(f"📄 文件大小: {result['size_bytes']:,} bytes")
    else:
        print(f"❌ 生成失败: {result['error']}")


if __name__ == "__main__":
    create_meeting_minutes()
