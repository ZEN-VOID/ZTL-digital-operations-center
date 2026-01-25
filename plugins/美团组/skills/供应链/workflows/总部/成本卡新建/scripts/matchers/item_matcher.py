"""
物品匹配器 - 物品编码匹配
ItemMatcher - Item Code Matching

功能:
1. 基于物品清单匹配物品编码
2. 精确匹配物品名称
3. 获取物品的成本单位信息
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Any


class ItemMatcher:
    """物品编码匹配器"""

    def __init__(self):
        """初始化匹配器"""
        self.item_db = self._load_item_database()

    def _load_item_database(self) -> pd.DataFrame:
        """
        加载物品清单

        数据源:
        - plugins/美团组/templates/物品导出清单-总部.xlsx
        """
        # 使用绝对路径(从项目根目录计算)
        script_dir = Path(__file__).parent
        item_db_path = script_dir / "../../../../../../templates/物品导出清单-总部.xlsx"
        item_db_path = item_db_path.resolve()

        if item_db_path.exists():
            df = pd.read_excel(item_db_path, header=2)
        else:
            # 数据源不存在,返回空DataFrame
            df = pd.DataFrame(columns=["物品编码", "物品名称", "成本单位"])

        return df

    def match(self, item_name: str) -> Dict[str, Any]:
        """
        匹配物品编码

        Args:
            item_name: 物品名称

        Returns:
            匹配结果字典:
            {
                "status": "success" | "error",
                "item_code": "物品编码",
                "item_name": "物品名称",
                "cost_unit": "成本单位"
            }
        """
        if self.item_db.empty:
            return {
                "status": "error",
                "message": "物品清单为空,请检查数据源文件"
            }

        # 精确匹配
        exact_match = self._exact_match(item_name)
        if exact_match:
            return {
                "status": "success",
                **exact_match
            }

        # 无法匹配
        return {
            "status": "error",
            "message": f"无法找到匹配的物品: {item_name}"
        }

    def _exact_match(self, item_name: str) -> Dict[str, Any]:
        """精确匹配物品名称"""
        if "物品名称" not in self.item_db.columns:
            return None

        matches = self.item_db[self.item_db["物品名称"] == item_name]

        if matches.empty:
            return None

        # 取第一条记录
        row = matches.iloc[0]
        return {
            "item_code": row.get("物品编码", ""),
            "item_name": row.get("物品名称", ""),
            "cost_unit": row.get("成本单位", "")
        }
