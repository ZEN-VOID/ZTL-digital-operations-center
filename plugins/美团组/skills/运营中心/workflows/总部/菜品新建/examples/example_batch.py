#!/usr/bin/env python3
"""
批量示例: 批量创建菜品
"""

from scripts.dish_creator import DishCreator


def example_batch():
    """批量创建示例"""
    # 初始化创建器
    creator = DishCreator()

    print("=" * 60)
    print("示例: 批量创建菜品")
    print("=" * 60)

    # 准备批量数据
    batch_data = [
        {
            "dish_name": "麻辣小龙虾",
            "brand": "吼巷",
            "category": "招牌菜/海鲜",
            "selling_price": 88,
            "member_price": 78,
            "spicy_level": "重辣"
        },
        {
            "dish_name": "蒜蓉小龙虾",
            "brand": "吼巷",
            "category": "招牌菜/海鲜",
            "selling_price": 88,
            "member_price": 78,
            "spicy_level": "不辣"
        },
        {
            "dish_name": "十三香小龙虾",
            "brand": "吼巷",
            "category": "招牌菜/海鲜",
            "selling_price": 88,
            "member_price": 78,
            "spicy_level": "微辣"
        },
        {
            "dish_name": "酸菜鱼",
            "brand": "吼巷",
            "category": "招牌菜/川菜",
            "selling_price": 68,
            "member_price": 58,
            "spicy_level": "中辣"
        },
        {
            "dish_name": "水煮肉片",
            "brand": "吼巷",
            "category": "热菜/川菜",
            "selling_price": 48,
            "member_price": 43,
            "spicy_level": "重辣"
        }
    ]

    # 批量创建
    results = creator.create_batch(
        batch_data=batch_data,
        project_name="夏季新品批量上架"
    )

    # 统计结果
    success_count = sum(1 for r in results if r["status"] == "success")
    print(f"\n📊 批量创建完成:")
    print(f"  总数: {len(results)}")
    print(f"  成功: {success_count}")
    print(f"  失败: {len(results) - success_count}")

    # 显示详细结果
    print(f"\n详细结果:")
    for i, result in enumerate(results, 1):
        if result["status"] == "success":
            print(f"  [{i}] ✅ {result['dish_name']}: {result['output_path']}")
        else:
            print(f"  [{i}] ❌ {result.get('dish_name', 'Unknown')}: {result.get('error')}")


if __name__ == "__main__":
    example_batch()
