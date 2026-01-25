#!/usr/bin/env python3
"""
基础示例: 单个菜品创建
"""

from scripts.dish_creator import DishCreator


def example_basic():
    """基础用法示例"""
    # 初始化创建器
    creator = DishCreator()

    # 方式1: 从自然语言创建
    print("=" * 60)
    print("示例1: 从自然语言创建菜品")
    print("=" * 60)

    result = creator.create_from_text(
        text="""
        请创建一个新菜品"麻辣小龙虾":
        - 品牌: 吼巷
        - 分类: 招牌菜/海鲜
        - 售价: 88元
        - 会员价: 78元
        - 辣度: 重辣
        - 描述: 精选优质小龙虾,秘制麻辣调料,鲜香麻辣
        """,
        project_name="新菜品上架"
    )

    if result["status"] == "success":
        print(f"✅ 创建成功!")
        print(f"📁 输出路径: {result['output_path']}")
        print(f"📋 计划路径: {result['plan_path']}")
    else:
        print(f"❌ 创建失败: {result.get('error')}")

    # 方式2: 从结构化数据创建
    print("\n" + "=" * 60)
    print("示例2: 从结构化数据创建菜品")
    print("=" * 60)

    data = {
        "dish_name": "酸菜鱼",
        "brand": "吼巷",
        "category": "招牌菜/川菜",
        "selling_price": 68,
        "member_price": 58,
        "spicy_level": "中辣",
        "description": "正宗四川酸菜鱼,酸辣开胃"
    }

    result = creator.create_from_dict(
        data=data,
        project_name="新菜品上架"
    )

    if result["status"] == "success":
        print(f"✅ 创建成功!")
        print(f"📁 输出路径: {result['output_path']}")
    else:
        print(f"❌ 创建失败: {result.get('error')}")


if __name__ == "__main__":
    example_basic()
