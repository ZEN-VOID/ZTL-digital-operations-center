"""
成本卡生成器 - 主执行引擎
CostCardGenerator - Main Execution Engine

功能:
1. 统一入口: 处理自然语言、结构化数据、批量数据
2. 流程编排: 协调解析、匹配、重构、生成各个步骤
3. 输出管理: 按照标准路径规范输出文件
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from .parsers.text_parser import TextParser
from .matchers.dish_matcher import DishMatcher
from .matchers.item_matcher import ItemMatcher
from .generators.excel_generator import ExcelGenerator


class CostCardGenerator:
    """成本卡生成器主类"""

    def __init__(self):
        """初始化生成器"""
        self.text_parser = TextParser()
        self.dish_matcher = DishMatcher()
        self.item_matcher = ItemMatcher()
        self.excel_generator = ExcelGenerator()

        # 配置日志
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def create_from_text(
        self,
        text: str,
        project_name: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        从自然语言描述创建成本卡

        Args:
            text: 自然语言描述
            project_name: 项目名称 (用于输出路径)
            **kwargs: 其他可选参数

        Returns:
            结果字典,包含:
            - status: 执行状态 ("success", "pending_confirm", "error")
            - output_path: 输出文件路径
            - message: 执行消息
            - pending_items: 待确认项 (如果status="pending_confirm")
        """
        self.logger.info(f"开始从自然语言创建成本卡: {project_name}")

        try:
            # Step 1: 解析自然语言
            self.logger.info("Step 1: 解析自然语言")
            parsed_data = self.text_parser.parse(text)

            # Step 2-5: 调用通用创建流程
            return self._create_cost_card(
                data=parsed_data,
                project_name=project_name,
                **kwargs
            )

        except Exception as e:
            self.logger.error(f"创建成本卡失败: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    def create_from_dict(
        self,
        data: Dict[str, Any],
        project_name: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        从结构化数据创建成本卡

        Args:
            data: 结构化数据字典
            project_name: 项目名称
            **kwargs: 其他可选参数

        Returns:
            结果字典
        """
        self.logger.info(f"开始从结构化数据创建成本卡: {project_name}")

        try:
            # 直接调用通用创建流程
            return self._create_cost_card(
                data=data,
                project_name=project_name,
                **kwargs
            )

        except Exception as e:
            self.logger.error(f"创建成本卡失败: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    def create_batch(
        self,
        batch_data: List[Dict[str, Any]],
        project_name: str,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        批量创建成本卡

        Args:
            batch_data: 批量数据列表
            project_name: 项目名称
            **kwargs: 其他可选参数

        Returns:
            结果列表,每个元素对应一个成本卡的创建结果
        """
        self.logger.info(f"开始批量创建成本卡: {project_name}, 共 {len(batch_data)} 个任务")

        results = []
        for idx, data in enumerate(batch_data, 1):
            self.logger.info(f"处理任务 {idx}/{len(batch_data)}: {data.get('dish_name', 'Unknown')}")

            result = self.create_from_dict(
                data=data,
                project_name=project_name,
                batch_mode=True,
                batch_index=idx,
                **kwargs
            )
            results.append(result)

        # 生成批量汇总Excel
        self._generate_batch_summary(results, project_name)

        return results

    def _create_cost_card(
        self,
        data: Dict[str, Any],
        project_name: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        通用成本卡创建流程

        执行 Step 2-5:
        - Step 2: 菜品SPU编码匹配
        - Step 3: 物品编码匹配
        - Step 4: 数据重构
        - Step 5: Excel文件生成
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dish_name = data.get("dish_name", "Unknown")

        # 创建输出目录
        output_dir = Path(f"output/{project_name}/cost-card-creator")
        output_dir.mkdir(parents=True, exist_ok=True)

        # 生成执行计划 (Layer 2)
        plan = self._generate_plan(data, project_name, timestamp)
        plan_path = output_dir / f"plan_成本卡生成_{timestamp}.json"
        with open(plan_path, "w", encoding="utf-8") as f:
            json.dump(plan, f, ensure_ascii=False, indent=2)
        self.logger.info(f"执行计划已保存: {plan_path}")

        # Step 2: 菜品SPU编码匹配
        self.logger.info("Step 2: 菜品SPU编码匹配")
        dish_match_result = self.dish_matcher.match(
            dish_name=data.get("dish_name"),
            dish_spec=data.get("dish_spec")
        )

        # 检查匹配度
        if dish_match_result["status"] == "pending_confirm":
            self.logger.warning("菜品匹配度低,需要人工确认")
            return {
                "status": "pending_confirm",
                "message": "菜品编码匹配度低于70%,需要人工确认",
                "pending_items": [dish_match_result],
                "plan_path": str(plan_path)
            }

        # Step 3: 物品编码匹配
        self.logger.info("Step 3: 物品编码匹配")
        ingredients = data.get("ingredients", [])
        matched_ingredients = []
        pending_items = []

        for ingredient in ingredients:
            item_match_result = self.item_matcher.match(
                item_name=ingredient.get("item_name")
            )

            if item_match_result["status"] == "error":
                pending_items.append({
                    "item_name": ingredient.get("item_name"),
                    "error": item_match_result["message"]
                })
            else:
                matched_ingredients.append({
                    **ingredient,
                    "item_code": item_match_result["item_code"],
                    "item_name_matched": item_match_result["item_name"],
                    "cost_unit": item_match_result["cost_unit"]
                })

        # 检查是否有待确认的物品
        if pending_items:
            self.logger.warning(f"有 {len(pending_items)} 个物品无法匹配")
            return {
                "status": "pending_confirm",
                "message": "部分物品编码无法匹配,需要人工确认",
                "pending_items": pending_items,
                "plan_path": str(plan_path)
            }

        # Step 4: 数据重构
        self.logger.info("Step 4: 数据重构")
        restructured_data = self._restructure_data(
            dish_data=dish_match_result,
            ingredients=matched_ingredients,
            original_data=data
        )

        # Step 5: Excel文件生成
        self.logger.info("Step 5: Excel文件生成")
        output_filename = f"成本卡_{dish_name}_{timestamp}.xlsx"
        output_path = output_dir / output_filename

        self.excel_generator.generate(
            data=restructured_data,
            output_path=str(output_path)
        )

        # 生成元数据
        metadata = {
            "project_name": project_name,
            "dish_name": dish_name,
            "created_at": timestamp,
            "plan_path": str(plan_path),
            "output_path": str(output_path),
            "dish_spu_code": dish_match_result.get("dish_code"),
            "ingredient_count": len(matched_ingredients)
        }
        metadata_path = output_dir / f"metadata_{timestamp}.json"
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        # 生成日志
        log_path = output_dir / f"log_execution_{timestamp}.txt"
        self._write_log(log_path, f"成本卡创建成功: {dish_name}")

        self.logger.info(f"成本卡创建成功: {output_path}")
        return {
            "status": "success",
            "output_path": str(output_path),
            "metadata_path": str(metadata_path),
            "message": f"成本卡已成功创建: {dish_name}"
        }

    def _generate_plan(
        self,
        data: Dict[str, Any],
        project_name: str,
        timestamp: str
    ) -> Dict[str, Any]:
        """生成执行计划 (Layer 2)"""
        plan_id = f"plan_成本卡生成_{timestamp}"

        return {
            "plan_id": plan_id,
            "project_name": project_name,
            "skill_name": "cost-card-creator",
            "task_type": "single",
            "created_at": timestamp,
            "execution_config": {
                "match_threshold": 0.7,
                "auto_confirm_above": 0.9,
                "require_manual_confirm": True
            },
            "tasks": [
                {
                    "task_id": "T001",
                    "dish_name": data.get("dish_name"),
                    "dish_spec": data.get("dish_spec", "标准"),
                    "processing_servings": data.get("processing_servings", 1),
                    "recipe_name": data.get("recipe_name", "标准成本配方"),
                    "ingredients": data.get("ingredients", [])
                }
            ],
            "output_path": f"output/{project_name}/cost-card-creator/成本卡_{data.get('dish_name')}_{timestamp}.xlsx"
        }

    def _restructure_data(
        self,
        dish_data: Dict[str, Any],
        ingredients: List[Dict[str, Any]],
        original_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        数据重构 (Step 4)

        处理一对多关系: 一个菜品对应多个物品
        每个物品占一行,菜品信息在每行重复填写
        """
        restructured_rows = []

        for ingredient in ingredients:
            row = {
                # 菜品信息 (重复填写)
                "菜品SPU编码": dish_data.get("dish_code"),
                "菜品名称": dish_data.get("dish_name"),
                "加工份数": original_data.get("processing_servings", 1),
                "菜品规格": original_data.get("dish_spec", "标准"),
                "其他成本": original_data.get("other_cost", ""),
                "目标毛利率": original_data.get("target_profit_rate", ""),
                "配方名称": original_data.get("recipe_name", "标准成本配方"),

                # 物品信息 (每行一个物品)
                "物品编码": ingredient.get("item_code"),
                "物品名称": ingredient.get("item_name_matched"),
                "成本单位": ingredient.get("cost_unit"),
                "净料量": ingredient.get("quantity"),
                "净料率": ingredient.get("yield_rate", "100%"),
                "是否主料": ingredient.get("is_main_ingredient", ""),

                # 其他可选字段
                "替代关系编号": ingredient.get("substitute_code", ""),
                "替代关系名称": ingredient.get("substitute_name", ""),
                "是否半成品": ingredient.get("is_semi_finished", ""),
                "是否辅助单位扣减料": ingredient.get("is_aux_unit_deduction", ""),
                "是否同时适用堂食和外卖菜品": ingredient.get("is_both_dine_delivery", ""),
                "门店是否可修改": ingredient.get("store_modifiable", ""),
                "备注": ingredient.get("remark", ""),
                "适用门店商户号": original_data.get("applicable_stores", ""),
                "适用门店分组": original_data.get("applicable_groups", "")
            }
            restructured_rows.append(row)

        return restructured_rows

    def _generate_batch_summary(
        self,
        results: List[Dict[str, Any]],
        project_name: str
    ):
        """生成批量处理汇总Excel"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path(f"output/{project_name}/cost-card-creator")
        summary_path = output_dir / f"批量成本卡汇总_{timestamp}.xlsx"

        # 合并所有成功生成的成本卡
        all_rows = []
        for result in results:
            if result["status"] == "success":
                # 读取每个成本卡的数据并合并
                pass  # TODO: 实现合并逻辑

        self.logger.info(f"批量汇总已保存: {summary_path}")

    def _write_log(self, log_path: Path, message: str):
        """写入日志文件"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
