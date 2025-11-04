#!/usr/bin/env python3
"""
菜品创建主引擎
负责协调整个菜品创建流程
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from parsers.text_parser import TextParser
from validators.field_validator import FieldValidator
from generators.excel_generator import ExcelGenerator


class DishCreator:
    """菜品创建主类"""

    def __init__(
        self,
        template_path: str = None,
        use_cache: bool = True
    ):
        """
        初始化菜品创建器

        Args:
            template_path: 模板文件路径(默认自动查找项目根目录)
            use_cache: 是否启用缓存
        """
        # 如果未指定模板路径,自动查找项目根目录
        if template_path is None:
            # 查找项目根目录(包含plugins目录的目录)
            current_dir = Path(__file__).resolve().parent
            while current_dir.parent != current_dir:
                if (current_dir / "plugins").exists():
                    template_path = str(current_dir / "plugins/美团组/templates/菜品导入模板.xlsx")
                    break
                current_dir = current_dir.parent

            if template_path is None:
                template_path = "plugins/美团组/templates/菜品导入模板.xlsx"

        self.template_path = template_path
        self.use_cache = use_cache

        # 初始化各模块
        self.text_parser = TextParser()
        self.field_validator = FieldValidator()
        self.excel_generator = ExcelGenerator(template_path)

        # 缓存
        self._cache = {} if use_cache else None

    def create_from_text(
        self,
        text: str,
        project_name: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        从自然语言文本创建菜品

        Args:
            text: 自然语言描述
            project_name: 项目名称
            **kwargs: 额外参数

        Returns:
            执行结果字典
        """
        # Step 1: 解析文本
        print(f"📝 解析文本内容...")
        parsed_data = self.text_parser.parse(text)

        # Step 2: 调用结构化数据创建
        return self.create_from_dict(
            data=parsed_data,
            project_name=project_name,
            **kwargs
        )

    def create_from_dict(
        self,
        data: Dict[str, Any],
        project_name: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        从结构化数据创建菜品

        Args:
            data: 菜品数据字典
            project_name: 项目名称
            **kwargs: 额外参数

        Returns:
            执行结果字典
        """
        task_id = f"T{datetime.now().strftime('%Y%m%d%H%M%S')}"

        try:
            # Step 1: 字段验证
            print(f"✅ 验证字段...")
            validation_errors = self.field_validator.validate_batch(data)
            if validation_errors:
                return {
                    "status": "validation_error",
                    "task_id": task_id,
                    "errors": validation_errors
                }

            # Step 2: 智能字段推断
            print(f"🧠 智能推断可选字段...")
            enriched_data = self._enrich_data(data)

            # Step 3: 生成执行计划
            print(f"📋 生成执行计划...")
            plan = self._generate_plan(
                task_id=task_id,
                data=enriched_data,
                project_name=project_name
            )

            # Step 4: 保存执行计划
            plan_path = self._save_plan(plan, project_name)
            print(f"💾 执行计划已保存: {plan_path}")

            # Step 5: 生成Excel文件
            print(f"📊 生成Excel文件...")
            output_path = self.excel_generator.generate(
                data=enriched_data,
                project_name=project_name,
                task_id=task_id
            )

            # Step 6: 生成元数据
            print(f"📝 生成元数据...")
            metadata_path = self._save_metadata(
                task_id=task_id,
                data=enriched_data,
                output_path=output_path,
                project_name=project_name
            )

            return {
                "status": "success",
                "task_id": task_id,
                "output_path": output_path,
                "plan_path": plan_path,
                "metadata_path": metadata_path,
                "dish_name": enriched_data.get("dish_name")
            }

        except Exception as e:
            print(f"❌ 错误: {str(e)}")
            return {
                "status": "error",
                "task_id": task_id,
                "error": str(e)
            }

    def create_batch(
        self,
        batch_data: List[Dict[str, Any]],
        project_name: str,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        批量创建菜品

        Args:
            batch_data: 批量菜品数据列表
            project_name: 项目名称
            **kwargs: 额外参数

        Returns:
            执行结果列表
        """
        print(f"🔄 开始批量创建 {len(batch_data)} 个菜品...")

        results = []
        for i, data in enumerate(batch_data, 1):
            print(f"\n[{i}/{len(batch_data)}] 创建菜品: {data.get('dish_name', 'Unknown')}")

            result = self.create_from_dict(
                data=data,
                project_name=project_name,
                **kwargs
            )

            results.append(result)

            # 简单进度展示
            if result["status"] == "success":
                print(f"✅ 成功")
            else:
                print(f"❌ 失败: {result.get('error', 'Unknown error')}")

        # 统计
        success_count = sum(1 for r in results if r["status"] == "success")
        print(f"\n📊 批量创建完成: {success_count}/{len(batch_data)} 成功")

        return results

    def _enrich_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        智能推断和填充可选字段

        Args:
            data: 原始数据

        Returns:
            丰富后的数据
        """
        enriched = data.copy()

        # 1. 推断计价方式
        if "pricing_method" not in enriched or not enriched["pricing_method"]:
            enriched["pricing_method"] = self.field_validator.infer_pricing_method(
                enriched.get("unit")
            )

        # 2. 推断单位
        if "unit" not in enriched or not enriched["unit"]:
            enriched["unit"] = self.field_validator.infer_unit(
                enriched.get("pricing_method"),
                enriched.get("category")
            )

        # 3. 生成拼音助记码
        if "pinyin_memo" not in enriched or not enriched["pinyin_memo"]:
            enriched["pinyin_memo"] = self.text_parser.generate_pinyin_memo(
                enriched.get("dish_name", "")
            )

        # 4. 推断辣度
        if "spicy_level" not in enriched or not enriched["spicy_level"]:
            enriched["spicy_level"] = self.field_validator.infer_spicy_level(
                enriched.get("dish_name", "")
            )

        # 5. 填充默认值
        defaults = {
            "member_price": enriched.get("selling_price"),  # 默认等于售卖价
            "is_print": "是",
            "selling_status": "在售",
            "display_unified": "是",
            "allow_temp_price": "不允许",
            "allow_manual_discount": "允许",
            "min_order_qty": 1,
            "increment_qty": 1,
            "combo_only": "否"
        }

        for key, default_value in defaults.items():
            if key not in enriched or enriched[key] is None:
                enriched[key] = default_value

        return enriched

    def _generate_plan(
        self,
        task_id: str,
        data: Dict[str, Any],
        project_name: str
    ) -> Dict[str, Any]:
        """
        生成执行计划

        Args:
            task_id: 任务ID
            data: 菜品数据
            project_name: 项目名称

        Returns:
            执行计划字典
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        return {
            "plan_id": f"plan_菜品创建_{timestamp}",
            "project_name": project_name,
            "skill_name": "dish-creator",
            "task_type": "single",
            "execution_config": {
                "auto_fill_optional": True,
                "validate_before_save": True,
                "use_intelligent_inference": True
            },
            "tasks": [
                {
                    "task_id": task_id,
                    **data
                }
            ],
            "output_path": self._get_output_path(
                project_name=project_name,
                dish_name=data.get("dish_name"),
                timestamp=timestamp
            ),
            "created_at": datetime.now().isoformat()
        }

    def _save_plan(self, plan: Dict[str, Any], project_name: str) -> str:
        """
        保存执行计划到JSON文件

        Args:
            plan: 执行计划
            project_name: 项目名称

        Returns:
            计划文件路径
        """
        output_dir = self._get_output_dir(project_name)
        output_dir.mkdir(parents=True, exist_ok=True)

        plan_filename = f"{plan['plan_id']}.json"
        plan_path = output_dir / plan_filename

        with open(plan_path, 'w', encoding='utf-8') as f:
            json.dump(plan, f, ensure_ascii=False, indent=2)

        return str(plan_path)

    def _save_metadata(
        self,
        task_id: str,
        data: Dict[str, Any],
        output_path: str,
        project_name: str
    ) -> str:
        """
        保存元数据

        Args:
            task_id: 任务ID
            data: 菜品数据
            output_path: 输出文件路径
            project_name: 项目名称

        Returns:
            元数据文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        metadata = {
            "task_id": task_id,
            "project_name": project_name,
            "skill_name": "dish-creator",
            "dish_name": data.get("dish_name"),
            "output_path": output_path,
            "created_at": datetime.now().isoformat(),
            "data_summary": {
                "brand": data.get("brand"),
                "category": data.get("category"),
                "selling_price": data.get("selling_price"),
                "spicy_level": data.get("spicy_level")
            }
        }

        output_dir = self._get_output_dir(project_name)
        metadata_path = output_dir / f"metadata_{timestamp}.json"

        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        return str(metadata_path)

    def _get_output_dir(self, project_name: str) -> Path:
        """获取输出目录"""
        return Path("output") / project_name / "dish-creator"

    def _get_output_path(
        self,
        project_name: str,
        dish_name: str,
        timestamp: str
    ) -> str:
        """获取输出文件路径"""
        output_dir = self._get_output_dir(project_name)
        filename = f"菜品导入_{dish_name}_{timestamp}.xlsx"
        return str(output_dir / filename)


# 命令行接口
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("用法: python dish_creator.py <project_name> <dish_name> [selling_price]")
        sys.exit(1)

    project_name = sys.argv[1]
    dish_name = sys.argv[2]
    selling_price = float(sys.argv[3]) if len(sys.argv) > 3 else 0

    creator = DishCreator()
    result = creator.create_from_dict(
        data={
            "dish_name": dish_name,
            "brand": "吼巷",
            "category": "招牌菜",
            "selling_price": selling_price
        },
        project_name=project_name
    )

    print(f"\n结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
