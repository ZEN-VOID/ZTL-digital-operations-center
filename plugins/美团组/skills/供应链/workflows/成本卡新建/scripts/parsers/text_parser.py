"""
文本解析器 - 自然语言解析
TextParser - Natural Language Parsing

功能:
1. 解析自然语言描述的菜品配方
2. 提取菜品名称、物品名称、用量、单位等信息
3. 支持中文/英文混合输入
"""

import re
from typing import Dict, List, Any, Optional


class TextParser:
    """自然语言文本解析器"""

    def __init__(self):
        """初始化解析器"""
        # 常见单位模式
        self.unit_pattern = r'(g|克|kg|千克|ml|毫升|l|升|个|只|根|片|条|包|袋|瓶|罐|斤|两)'

        # 用量模式: 数字 + 单位
        self.quantity_pattern = rf'(\d+(?:\.\d+)?)\s*({self.unit_pattern})'

    def parse(self, text: str) -> Dict[str, Any]:
        """
        解析自然语言文本

        Args:
            text: 自然语言描述

        Returns:
            结构化数据字典:
            {
                "dish_name": "菜品名称",
                "dish_spec": "规格",
                "ingredients": [
                    {
                        "item_name": "物品名称",
                        "quantity": 数量,
                        "unit": "单位",
                        "yield_rate": "净料率"
                    },
                    ...
                ]
            }
        """
        result = {
            "dish_name": "",
            "dish_spec": "标准",
            "ingredients": []
        }

        # 提取菜品名称
        result["dish_name"] = self._extract_dish_name(text)

        # 提取配料信息
        result["ingredients"] = self._extract_ingredients(text)

        # 提取其他可选字段
        result.update(self._extract_optional_fields(text))

        return result

    def _extract_dish_name(self, text: str) -> str:
        """
        提取菜品名称

        策略:
        1. 查找"为xxx创建成本卡"、"xxx的成本卡"等模式
        2. 查找双引号内的菜品名
        3. 查找第一行的主要关键词
        """
        # 模式1: "为xxx创建成本卡"
        match = re.search(r'为["""]?([^"""\n]+?)["""]?创建成本卡', text)
        if match:
            return match.group(1).strip()

        # 模式2: "xxx的成本卡"
        match = re.search(r'["""]?([^"""\n]+?)["""]?的成本卡', text)
        if match:
            return match.group(1).strip()

        # 模式3: 双引号内的第一个词
        match = re.search(r'["""]([^"""]+)["""]', text)
        if match:
            return match.group(1).strip()

        # 模式4: 第一行的关键词 (fallback)
        first_line = text.split('\n')[0].strip()
        return first_line[:20]  # 取前20个字符作为菜品名

    def _extract_ingredients(self, text: str) -> List[Dict[str, Any]]:
        """
        提取配料信息

        策略:
        1. 查找列表项 (- xxx, 1. xxx等)
        2. 提取物品名称、用量、单位
        3. 提取净料率 (如果有)
        """
        ingredients = []

        # 查找所有列表项
        lines = text.split('\n')
        for line in lines:
            line = line.strip()

            # 跳过空行和非列表项
            if not line or not self._is_ingredient_line(line):
                continue

            # 解析配料
            ingredient = self._parse_ingredient_line(line)
            if ingredient:
                ingredients.append(ingredient)

        return ingredients

    def _is_ingredient_line(self, line: str) -> bool:
        """判断是否为配料行"""
        # 列表标记
        list_markers = ['-', '*', '•', '·']
        if any(line.startswith(marker) for marker in list_markers):
            return True

        # 数字序号
        if re.match(r'^\d+[\.、]', line):
            return True

        # 包含"使用"、"加入"等关键词
        if any(keyword in line for keyword in ['使用', '加入', '需要', '放入']):
            return True

        return False

    def _parse_ingredient_line(self, line: str) -> Optional[Dict[str, Any]]:
        """
        解析单行配料信息

        示例:
        - "- 牛肉 500g"
        - "使用辣椒油50ml"
        - "花椒10g (净料率85%)"
        """
        # 移除列表标记
        line = re.sub(r'^[-*•·\d+\.、]\s*', '', line)

        # 提取用量和单位
        quantity_match = re.search(self.quantity_pattern, line)
        if not quantity_match:
            return None

        quantity = float(quantity_match.group(1))
        unit = quantity_match.group(2)

        # 提取物品名称 (用量之前的文本)
        item_name = line[:quantity_match.start()].strip()
        # 移除"使用"、"加入"等关键词
        item_name = re.sub(r'(使用|加入|需要|放入)', '', item_name).strip()

        # 提取净料率 (如果有)
        yield_rate = "100%"
        yield_match = re.search(r'净料率[:\s]*(\d+)%', line)
        if yield_match:
            yield_rate = f"{yield_match.group(1)}%"

        return {
            "item_name": item_name,
            "quantity": quantity,
            "unit": unit,
            "yield_rate": yield_rate
        }

    def _extract_optional_fields(self, text: str) -> Dict[str, Any]:
        """
        提取其他可选字段

        如: 目标毛利率、配方名称、规格等
        """
        optional = {}

        # 提取目标毛利率
        profit_rate_match = re.search(r'目标毛利率[:\s]*(\d+)%', text)
        if profit_rate_match:
            optional["target_profit_rate"] = f"{profit_rate_match.group(1)}%"

        # 提取规格
        spec_match = re.search(r'规格[:\s]*([^\n]+)', text)
        if spec_match:
            optional["dish_spec"] = spec_match.group(1).strip()

        # 提取配方名称
        recipe_match = re.search(r'配方名称[:\s]*([^\n]+)', text)
        if recipe_match:
            optional["recipe_name"] = recipe_match.group(1).strip()

        return optional
