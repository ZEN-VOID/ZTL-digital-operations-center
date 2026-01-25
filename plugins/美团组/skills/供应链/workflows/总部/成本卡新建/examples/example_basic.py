"""
基础使用示例 - 从自然语言创建单个成本卡
Basic Usage Example - Create Single Cost Card from Natural Language
"""

import sys
from pathlib import Path

# 添加脚本路径
skill_path = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(skill_path))

from cost_card_generator import CostCardGenerator


def example_basic():
    """基础示例: 从自然语言创建成本卡"""
    # 初始化生成器
    generator = CostCardGenerator()

    # 自然语言描述
    text = """
    为"麻辣牛肉"创建成本卡:
    - 使用牛肉 500g (净料率85%)
    - 使用辣椒油 50ml
    - 使用花椒 10g
    - 目标毛利率: 65%
    """

    # 创建成本卡
    result = generator.create_from_text(
        text=text,
        project_name="火锅店成本管理"
    )

    # 检查结果
    if result["status"] == "success":
        print(f"✅ 成本卡创建成功!")
        print(f"📁 输出路径: {result['output_path']}")
    elif result["status"] == "pending_confirm":
        print(f"⚠️  需要人工确认:")
        print(f"原因: {result['message']}")
        for item in result.get("pending_items", []):
            print(f"- {item}")
    else:
        print(f"❌ 创建失败: {result.get('message')}")


if __name__ == "__main__":
    example_basic()
