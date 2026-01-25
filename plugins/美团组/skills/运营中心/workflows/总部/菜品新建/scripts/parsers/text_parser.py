#!/usr/bin/env python3
"""
文本解析器
负责将自然语言描述解析为结构化数据
"""

import re
from typing import Dict, Any, Optional


class TextParser:
    """自然语言文本解析器"""

    def __init__(self):
        """初始化解析器"""
        pass

    def parse(self, text: str) -> Dict[str, Any]:
        """
        解析自然语言文本

        Args:
            text: 自然语言描述

        Returns:
            结构化数据字典
        """
        data = {}

        # 1. 提取菜品名称
        data["dish_name"] = self._extract_dish_name(text)

        # 2. 提取品牌
        data["brand"] = self._extract_brand(text)

        # 3. 提取分类
        data["category"] = self._extract_category(text)

        # 4. 提取价格信息
        data["selling_price"] = self._extract_selling_price(text)
        data["member_price"] = self._extract_member_price(text)
        data["estimated_cost"] = self._extract_estimated_cost(text)

        # 5. 提取规格
        data["spec"] = self._extract_spec(text)

        # 6. 提取辣度
        data["spicy_level"] = self._extract_spicy_level(text)

        # 7. 提取描述
        data["description"] = self._extract_description(text)

        # 8. 提取其他字段
        data["dish_badge"] = self._extract_badge(text)

        return data

    def _extract_dish_name(self, text: str) -> Optional[str]:
        """提取菜品名称"""
        # 模式1: "创建菜品\"xxx\""
        match = re.search(r'创建.*?["\'](.+?)["\']', text)
        if match:
            return match.group(1)

        # 模式2: "菜品名称: xxx"
        match = re.search(r'菜品名称[:=]\s*(.+?)(?:\n|$|[,;])', text)
        if match:
            return match.group(1).strip()

        # 模式3: "\"xxx\"创建"
        match = re.search(r'["\'](.+?)["\']', text)
        if match:
            return match.group(1)

        return None

    def _extract_brand(self, text: str) -> Optional[str]:
        """提取品牌"""
        match = re.search(r'品牌[:=]\s*(.+?)(?:\n|$|[,;])', text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        match = re.search(r'所属品牌[:=]\s*(.+?)(?:\n|$|[,;])', text)
        if match:
            return match.group(1).strip()

        return None

    def _extract_category(self, text: str) -> Optional[str]:
        """提取分类"""
        match = re.search(r'分类[:=]\s*(.+?)(?:\n|$|[,;])', text)
        if match:
            return match.group(1).strip()

        return None

    def _extract_selling_price(self, text: str) -> Optional[float]:
        """提取售卖价"""
        # 模式1: "售价: 88元"
        match = re.search(r'售[价卖][:=]\s*(\d+(?:\.\d+)?)\s*元?', text)
        if match:
            return float(match.group(1))

        # 模式2: "售卖价: 88"
        match = re.search(r'售卖价[:=]\s*(\d+(?:\.\d+)?)', text)
        if match:
            return float(match.group(1))

        # 模式3: "88元"
        match = re.search(r'(\d+(?:\.\d+)?)\s*元', text)
        if match:
            return float(match.group(1))

        return None

    def _extract_member_price(self, text: str) -> Optional[float]:
        """提取会员价"""
        match = re.search(r'会员价[:=]\s*(\d+(?:\.\d+)?)\s*元?', text)
        if match:
            return float(match.group(1))

        return None

    def _extract_estimated_cost(self, text: str) -> Optional[float]:
        """提取预估成本"""
        match = re.search(r'(?:预估)?成本[:=]\s*(\d+(?:\.\d+)?)\s*元?', text)
        if match:
            return float(match.group(1))

        return None

    def _extract_spec(self, text: str) -> Optional[str]:
        """提取规格"""
        match = re.search(r'规格[:=]\s*(.+?)(?:\n|$|[,;])', text)
        if match:
            return match.group(1).strip()

        return None

    def _extract_spicy_level(self, text: str) -> Optional[str]:
        """提取辣度"""
        match = re.search(r'辣度[:=]\s*(.+?)(?:\n|$|[,;])', text)
        if match:
            return match.group(1).strip()

        # 从文本中推断
        if "爆辣" in text or "变态辣" in text:
            return "爆辣"
        elif "重辣" in text or "麻辣" in text or "香辣" in text:
            return "重辣"
        elif "中辣" in text or "酸辣" in text:
            return "中辣"
        elif "微辣" in text:
            return "微辣"
        elif "微微辣" in text:
            return "微微辣"

        return None

    def _extract_description(self, text: str) -> Optional[str]:
        """提取描述"""
        match = re.search(r'描述[:=]\s*(.+?)(?:\n\n|$)', text, re.DOTALL)
        if match:
            return match.group(1).strip()

        return None

    def _extract_badge(self, text: str) -> Optional[str]:
        """提取角标"""
        if "新品" in text or "新菜" in text or "新上" in text:
            return "新菜"
        elif "招牌" in text or "爆款" in text or "必点" in text:
            return "招牌菜"
        elif "特价" in text or "促销" in text or "优惠" in text:
            return "特价"

        return None

    def generate_pinyin_memo(self, dish_name: str) -> str:
        """
        生成拼音助记码

        Args:
            dish_name: 菜品名称

        Returns:
            拼音助记码 (大写首字母)
        """
        try:
            from pypinyin import lazy_pinyin
            pinyin = lazy_pinyin(dish_name)
            return ''.join([py[0].upper() for py in pinyin])
        except ImportError:
            # 如果没有安装pypinyin,返回简化版
            return ''.join([c for c in dish_name if c.isalpha()])[:10].upper()


# 测试
if __name__ == "__main__":
    parser = TextParser()

    test_text = """
    请创建一个新菜品"麻辣小龙虾":
    - 品牌: 吼巷
    - 分类: 招牌菜/海鲜
    - 售价: 88元
    - 会员价: 78元
    - 辣度: 重辣
    - 描述: 精选优质小龙虾,秘制麻辣调料,鲜香麻辣
    """

    result = parser.parse(test_text)
    print("解析结果:")
    for key, value in result.items():
        print(f"  {key}: {value}")

    print(f"\n拼音助记码: {parser.generate_pinyin_memo('麻辣小龙虾')}")
