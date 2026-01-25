"""
批量处理示例 - 批量创建多个成本卡
Batch Processing Example - Create Multiple Cost Cards
"""

import sys
from pathlib import Path

skill_path = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(skill_path))

from cost_card_generator import CostCardGenerator


def example_batch():
    """批量处理示例"""
    generator = CostCardGenerator()

    # 批量数据
    batch_data = [
        {
            "dish_name": "麻辣牛肉",
            "ingredients": [
                {"item_name": "牛肉", "quantity": 500, "unit": "g", "yield_rate": "85%"},
                {"item_name": "辣椒油", "quantity": 50, "unit": "ml", "yield_rate": "100%"}
            ]
        },
        {
            "dish_name": "酸菜鱼",
            "ingredients": [
                {"item_name": "草鱼", "quantity": 800, "unit": "g", "yield_rate": "80%"},
                {"item_name": "酸菜", "quantity": 200, "unit": "g", "yield_rate": "100%"}
            ]
        },
        {
            "dish_name": "水煮肉片",
            "ingredients": [
                {"item_name": "猪肉", "quantity": 400, "unit": "g", "yield_rate": "90%"},
                {"item_name": "青菜", "quantity": 200, "unit": "g", "yield_rate": "100%"}
            ]
        }
    ]

    # 批量创建
    print(f"开始批量创建 {len(batch_data)} 个成本卡...")
    results = generator.create_batch(
        batch_data=batch_data,
        project_name="火锅店成本管理"
    )

    # 统计结果
    success_count = sum(1 for r in results if r["status"] == "success")
    pending_count = sum(1 for r in results if r["status"] == "pending_confirm")
    error_count = sum(1 for r in results if r["status"] == "error")

    print("\n📊 批量处理结果:")
    print(f"✅ 成功: {success_count}")
    print(f"⚠️  待确认: {pending_count}")
    print(f"❌ 失败: {error_count}")

    # 输出详细结果
    for idx, result in enumerate(results, 1):
        dish_name = batch_data[idx - 1]["dish_name"]
        status_icon = {
            "success": "✅",
            "pending_confirm": "⚠️ ",
            "error": "❌"
        }.get(result["status"], "❓")

        print(f"{status_icon} {idx}. {dish_name}: {result.get('message', result['status'])}")


if __name__ == "__main__":
    example_batch()
