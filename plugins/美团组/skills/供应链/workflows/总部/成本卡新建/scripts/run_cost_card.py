"""
临时执行脚本 - 创建成本卡
Temporary Execution Script - Create Cost Card
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from matchers.dish_matcher import DishMatcher
from matchers.item_matcher import ItemMatcher
from restructurers.data_restructurer import DataRestructurer
from generators.excel_generator import ExcelGenerator
from typing import Dict, Any
import json
from datetime import datetime


def create_cost_card(data: Dict[str, Any], project_name: str = "成本卡项目"):
    """
    创建成本卡的核心逻辑

    Args:
        data: 包含dish_name和ingredients的字典
        project_name: 项目名称
    """
    # 初始化匹配器
    dish_matcher = DishMatcher()
    item_matcher = ItemMatcher()

    # Step 1: 匹配菜品SPU编码
    print(f"\n📋 Step 1: 匹配菜品 '{data['dish_name']}'...")
    dish_result = dish_matcher.match(data["dish_name"])

    if dish_result["status"] == "error":
        return {
            "status": "error",
            "message": f"菜品匹配失败: {dish_result.get('message')}"
        }

    if dish_result["status"] == "pending_confirm":
        print(f"⚠️ 菜品匹配度低于70%，需要人工确认")
        print(f"输入菜品: {data['dish_name']}")
        print(f"\n候选项:")
        for idx, candidate in enumerate(dish_result.get("candidates", [])[:5], 1):
            print(f"  {idx}. {candidate['dish_name']} (相似度: {candidate['similarity']:.2%})")
        return {
            "status": "pending_confirm",
            "message": "菜品匹配需要人工确认",
            "candidates": dish_result.get("candidates", [])
        }

    print(f"✅ 菜品匹配成功: {dish_result['dish_name']} (SPU: {dish_result['dish_code']})")

    # Step 2: 匹配物品编码
    print(f"\n📋 Step 2: 匹配 {len(data['ingredients'])} 个物品...")
    matched_ingredients = []
    failed_items = []

    for ingredient in data["ingredients"]:
        item_name = ingredient["item_name"]
        item_result = item_matcher.match(item_name)

        if item_result["status"] == "success":
            matched_ingredients.append({
                **ingredient,
                "item_code": item_result["item_code"],
                "cost_unit": item_result["cost_unit"]
            })
            print(f"  ✅ {item_name} → {item_result['item_code']}")
        else:
            failed_items.append(item_name)
            print(f"  ❌ {item_name}: {item_result.get('message')}")

    if failed_items:
        return {
            "status": "error",
            "message": f"以下物品匹配失败: {', '.join(failed_items)}"
        }

    # Step 3: 数据重构
    print(f"\n📋 Step 3: 重构数据...")
    restructurer = DataRestructurer()
    restructured_data = restructurer.restructure(
        dish_info=dish_result,
        ingredients=matched_ingredients
    )
    print(f"✅ 已生成 {len(restructured_data)} 行Excel数据")

    # Step 4: 生成Excel
    print(f"\n📋 Step 4: 生成Excel文件...")

    # 创建输出目录
    output_base = Path("/Users/vincentlee/Desktop/ZTL数智化作战中心/output")
    output_dir = output_base / project_name / "成本卡生成"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"成本卡_{data['dish_name']}_{timestamp}.xlsx"

    generator = ExcelGenerator()
    generator.generate(
        data=restructured_data,
        output_path=str(output_file)
    )

    print(f"✅ Excel文件已生成: {output_file}")

    # 保存元数据
    metadata_file = output_dir / f"元数据_{data['dish_name']}_{timestamp}.json"
    metadata = {
        "project_name": project_name,
        "dish_info": dish_result,
        "ingredients_count": len(matched_ingredients),
        "excel_rows": len(restructured_data),
        "output_file": str(output_file),
        "created_at": datetime.now().isoformat()
    }

    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"✅ 元数据已保存: {metadata_file}")

    return {
        "status": "success",
        "output_path": str(output_file),
        "metadata_path": str(metadata_file),
        "message": "成本卡创建成功"
    }


if __name__ == "__main__":
    # 测试数据
    data = {
        "dish_name": "山野菌菇鸡汤米线",
        "ingredients": [
            {"item_name": "菌菇酱", "quantity": 25, "unit": "g"},
            {"item_name": "米线", "quantity": 280, "unit": "g"},
            {"item_name": "鸡汤", "quantity": 500, "unit": "g"},
            {"item_name": "鸡块", "quantity": 0, "unit": "g"},
            {"item_name": "鸡蛋", "quantity": 0.5, "unit": "个"},
            {"item_name": "小葱", "quantity": 5, "unit": "g"},
            {"item_name": "青菜", "quantity": 50, "unit": "g"},
            {"item_name": "鸡油黄", "quantity": 5, "unit": "g"},
            {"item_name": "蟹味菇", "quantity": 5, "unit": "g"},
            {"item_name": "虫草花", "quantity": 2, "unit": "g"}
        ]
    }

    result = create_cost_card(data, project_name="米线成本管理")

    print("\n" + "="*50)
    if result["status"] == "success":
        print("🎉 成本卡创建成功!")
        print(f"📁 输出文件: {result['output_path']}")
        print(f"📊 元数据: {result['metadata_path']}")
    elif result["status"] == "pending_confirm":
        print(f"⚠️ {result['message']}")
    else:
        print(f"❌ 创建失败: {result['message']}")
