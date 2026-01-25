#!/usr/bin/env python3
"""
字段验证器
负责验证字段完整性、格式和业务规则
"""

from typing import Dict, Any, List, Optional


class FieldValidator:
    """字段验证器"""

    # 必填字段
    REQUIRED_FIELDS = [
        "dish_name",      # 菜品名称
        "brand",          # 所属品牌
        "category",       # 分类
        "selling_price",  # 售卖价
    ]

    # 枚举字段
    ENUM_FIELDS = {
        "pricing_method": ["按份销售", "称重销售"],
        "spicy_level": ["不辣", "微微辣", "微辣", "中辣", "重辣", "爆辣"],
        "selling_status": ["在售", "停售"],
        "is_print": ["是", "否"],
        "display_unified": ["是", "否"],
        "allow_temp_price": ["允许", "不允许"],
        "allow_manual_discount": ["允许", "不允许"],
        "combo_only": ["是", "否"],
        "shelf_life_unit": ["年", "天", "自然日", "小时", "分钟"]
    }

    # 品类与单位映射
    CATEGORY_UNIT_MAP = {
        "饮料": "杯",
        "主食": "份",
        "水果": "斤",
        "海鲜": "斤",
        "汤品": "碗",
        "凉菜": "份",
        "热菜": "份"
    }

    def __init__(self):
        """初始化验证器"""
        pass

    def validate_batch(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        批量验证所有字段

        Args:
            data: 菜品数据

        Returns:
            错误列表
        """
        errors = []

        # 1. 验证必填字段
        missing_errors = self._validate_required_fields(data)
        errors.extend(missing_errors)

        # 2. 验证字段格式
        format_errors = self._validate_field_formats(data)
        errors.extend(format_errors)

        # 3. 验证业务规则
        business_errors = self._validate_business_rules(data)
        errors.extend(business_errors)

        return errors

    def _validate_required_fields(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """验证必填字段"""
        errors = []

        for field in self.REQUIRED_FIELDS:
            if field not in data or data[field] is None or data[field] == "":
                errors.append({
                    "error_type": "MissingRequiredFieldError",
                    "field": field,
                    "message": f"缺少必填字段: {field}"
                })

        return errors

    def _validate_field_formats(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """验证字段格式"""
        errors = []

        # 1. 验证价格字段
        if "selling_price" in data and data["selling_price"] is not None:
            if not isinstance(data["selling_price"], (int, float)) or data["selling_price"] <= 0:
                errors.append({
                    "error_type": "FieldFormatError",
                    "field": "selling_price",
                    "value": data["selling_price"],
                    "message": "售卖价必须是大于0的数值"
                })

        # 2. 验证会员价
        if "member_price" in data and data["member_price"] is not None:
            selling_price = data.get("selling_price", 0)
            if data["member_price"] > selling_price:
                errors.append({
                    "error_type": "FieldFormatError",
                    "field": "member_price",
                    "value": data["member_price"],
                    "message": f"会员价({data['member_price']})不能大于售卖价({selling_price})"
                })

        # 3. 验证保质期
        if "shelf_life" in data and data["shelf_life"] is not None:
            if not isinstance(data["shelf_life"], int) or not (1 <= data["shelf_life"] <= 999):
                errors.append({
                    "error_type": "FieldFormatError",
                    "field": "shelf_life",
                    "value": data["shelf_life"],
                    "message": "保质期必须是1-999的整数"
                })

            # 保质期存在时,保质期单位必填
            if "shelf_life_unit" not in data or not data["shelf_life_unit"]:
                errors.append({
                    "error_type": "MissingRequiredFieldError",
                    "field": "shelf_life_unit",
                    "message": "输入保质期后,保质期单位必填"
                })

        # 4. 验证条形码
        if "barcode" in data and data["barcode"]:
            barcode = str(data["barcode"])
            if not (5 <= len(barcode) <= 30) or not barcode.isalnum():
                errors.append({
                    "error_type": "FieldFormatError",
                    "field": "barcode",
                    "value": barcode,
                    "message": "条形码必须是5-30位的数字或字母"
                })

        # 5. 验证枚举字段
        for field, valid_values in self.ENUM_FIELDS.items():
            if field in data and data[field] is not None:
                if data[field] not in valid_values:
                    errors.append({
                        "error_type": "InvalidEnumValueError",
                        "field": field,
                        "value": data[field],
                        "valid_values": valid_values,
                        "message": f"{field}的值'{data[field]}'不合法,可选值: {', '.join(valid_values)}"
                    })

        # 6. 验证描述长度
        if "description" in data and data["description"]:
            if len(data["description"]) > 50:
                errors.append({
                    "error_type": "FieldFormatError",
                    "field": "description",
                    "value": data["description"],
                    "message": f"菜品描述不能超过50字,当前{len(data['description'])}字"
                })

        if "detailed_description" in data and data["detailed_description"]:
            if len(data["detailed_description"]) > 200:
                errors.append({
                    "error_type": "FieldFormatError",
                    "field": "detailed_description",
                    "value": data["detailed_description"],
                    "message": f"菜品详细描述不能超过200字,当前{len(data['detailed_description'])}字"
                })

        return errors

    def _validate_business_rules(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """验证业务规则"""
        errors = []

        # 1. 计价方式与单位的匹配
        pricing_method = data.get("pricing_method")
        unit = data.get("unit")

        if pricing_method == "称重销售":
            if unit and unit not in ["斤", "两", "公斤", "克"]:
                errors.append({
                    "error_type": "BusinessRuleError",
                    "field": "unit",
                    "message": f"称重销售的单位应为'斤'、'两'、'公斤'、'克',当前为'{unit}'"
                })

        return errors

    def infer_pricing_method(self, unit: Optional[str]) -> str:
        """
        推断计价方式

        Args:
            unit: 单位

        Returns:
            计价方式
        """
        if unit and unit in ["斤", "两", "公斤", "克"]:
            return "称重销售"
        else:
            return "按份销售"

    def infer_unit(
        self,
        pricing_method: Optional[str],
        category: Optional[str]
    ) -> str:
        """
        推断单位

        Args:
            pricing_method: 计价方式
            category: 分类

        Returns:
            单位
        """
        if pricing_method == "称重销售":
            return "斤"

        # 根据分类推断
        if category:
            for cat_key, unit in self.CATEGORY_UNIT_MAP.items():
                if cat_key in category:
                    return unit

        # 默认
        return "份"

    def infer_spicy_level(self, dish_name: str) -> str:
        """
        推断辣度

        Args:
            dish_name: 菜品名称

        Returns:
            辣度级别
        """
        if "爆辣" in dish_name or "变态辣" in dish_name or "超辣" in dish_name:
            return "爆辣"
        elif "重辣" in dish_name or "麻辣" in dish_name or "香辣" in dish_name:
            return "重辣"
        elif "中辣" in dish_name or "酸辣" in dish_name:
            return "中辣"
        elif "微辣" in dish_name:
            return "微辣"
        elif "微微辣" in dish_name:
            return "微微辣"
        else:
            return "不辣"


# 测试
if __name__ == "__main__":
    validator = FieldValidator()

    # 测试1: 完整数据验证
    test_data = {
        "dish_name": "麻辣小龙虾",
        "brand": "吼巷",
        "category": "招牌菜/海鲜",
        "selling_price": 88,
        "member_price": 78
    }

    errors = validator.validate_batch(test_data)
    print("验证结果:")
    if errors:
        for error in errors:
            print(f"  ❌ {error['message']}")
    else:
        print("  ✅ 验证通过")

    # 测试2: 推断功能
    print(f"\n推断计价方式('斤'): {validator.infer_pricing_method('斤')}")
    print(f"推断单位('按份销售', '招牌菜/海鲜'): {validator.infer_unit('按份销售', '招牌菜/海鲜')}")
    print(f"推断辣度('麻辣小龙虾'): {validator.infer_spicy_level('麻辣小龙虾')}")
