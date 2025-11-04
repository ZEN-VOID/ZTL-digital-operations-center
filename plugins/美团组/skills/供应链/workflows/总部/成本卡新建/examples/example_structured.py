"""
结构化数据示例 - 从字典创建成本卡
Structured Data Example - Create Cost Card from Dictionary
"""

import sys
from pathlib import Path

skill_path = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(skill_path))

from cost_card_generator import CostCardGenerator


def example_structured():
    """结构化数据示例"""
    generator = CostCardGenerator()

    # 结构化数据
    data = {
        "dish_name": "酸菜鱼",
        "dish_spec": "标准",
        "processing_servings": 1,
        "recipe_name": "标准成本配方",
        "target_profit_rate": "60%",
        "ingredients": [
            {
                "item_name": "草鱼",
                "quantity": 800,
                "unit": "g",
                "yield_rate": "80%",
                "is_main_ingredient": "是"
            },
            {
                "item_name": "酸菜",
                "quantity": 200,
                "unit": "g",
                "yield_rate": "100%"
            },
            {
                "item_name": "金针菇",
                "quantity": 100,
                "unit": "g",
                "yield_rate": "100%"
            },
            {
                "item_name": "豆腐",
                "quantity": 150,
                "unit": "g",
                "yield_rate": "100%"
            }
        ]
    }

    # 创建成本卡
    result = generator.create_from_dict(
        data=data,
        project_name="火锅店成本管理"
    )

    # 输出结果
    if result["status"] == "success":
        print("✅ 成本卡创建成功!")
        print(f"📁 输出文件: {result['output_path']}")
        print(f"📊 元数据: {result['metadata_path']}")
    else:
        print(f"❌ 创建失败: {result.get('message')}")


if __name__ == "__main__":
    example_structured()
