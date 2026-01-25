"""
菜品匹配器 - 菜品SPU编码匹配
DishMatcher - Dish SPU Code Matching

功能:
1. 基于菜品库匹配菜品SPU编码
2. 支持精确匹配和模糊匹配
3. 相似度阈值控制 (≥70%自动采用, <70%人工确认)
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional
try:
    from Levenshtein import ratio
except ImportError:
    # Fallback: 使用difflib.SequenceMatcher
    from difflib import SequenceMatcher
    def ratio(a: str, b: str) -> float:
        return SequenceMatcher(None, a, b).ratio()


class DishMatcher:
    """菜品SPU编码匹配器"""

    def __init__(self, threshold: float = 0.7):
        """
        初始化匹配器

        Args:
            threshold: 相似度阈值 (默认0.7)
        """
        self.threshold = threshold
        self.dish_db = self._load_dish_database()

    def _load_dish_database(self) -> pd.DataFrame:
        """
        加载菜品库

        数据源:
        - plugins/美团组/templates/吼巷_菜品库_总部.xlsx
        - plugins/美团组/templates/吼巷_菜品库_总部_做法及加料.xlsx
        """
        # 使用绝对路径(从项目根目录计算)
        script_dir = Path(__file__).parent
        base_path = script_dir / "../../../../../../templates"
        base_path = base_path.resolve()

        # 读取主菜品库
        main_db_path = base_path / "吼巷_菜品库_总部.xlsx"
        df_main = pd.read_excel(main_db_path, header=2) if main_db_path.exists() else pd.DataFrame()

        # 读取做法及加料库
        addon_db_path = base_path / "吼巷_菜品库_总部_做法及加料.xlsx"
        df_addon = pd.read_excel(addon_db_path, header=2) if addon_db_path.exists() else pd.DataFrame()

        # 合并两个库
        if not df_main.empty and not df_addon.empty:
            df = pd.concat([df_main, df_addon], ignore_index=True)
        elif not df_main.empty:
            df = df_main
        elif not df_addon.empty:
            df = df_addon
        else:
            # 数据源不存在,返回空DataFrame
            df = pd.DataFrame(columns=["菜品SPU编码", "菜品名称", "菜品规格"])

        return df

    def match(
        self,
        dish_name: str,
        dish_spec: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        匹配菜品SPU编码

        Args:
            dish_name: 菜品名称
            dish_spec: 菜品规格 (可选)

        Returns:
            匹配结果字典:
            {
                "status": "success" | "pending_confirm" | "error",
                "dish_code": "菜品SPU编码",
                "dish_name": "菜品名称",
                "dish_spec": "菜品规格",
                "similarity": 相似度 (0-1),
                "candidates": [候选项列表] (如果需要人工确认)
            }
        """
        if self.dish_db.empty:
            return {
                "status": "error",
                "message": "菜品库为空,请检查数据源文件"
            }

        # 策略1: 精确匹配
        exact_match = self._exact_match(dish_name, dish_spec)
        if exact_match:
            return {
                "status": "success",
                **exact_match,
                "similarity": 1.0
            }

        # 策略2: 模糊匹配
        fuzzy_matches = self._fuzzy_match(dish_name, dish_spec)

        if not fuzzy_matches:
            return {
                "status": "error",
                "message": f"无法找到匹配的菜品: {dish_name}"
            }

        # 取相似度最高的候选项
        best_match = fuzzy_matches[0]

        if best_match["similarity"] >= self.threshold:
            return {
                "status": "success",
                **best_match
            }
        else:
            return {
                "status": "pending_confirm",
                "message": f"菜品匹配度低于{self.threshold*100}%,需要人工确认",
                "input": dish_name,
                "candidates": fuzzy_matches[:5]  # 返回前5个候选项
            }

    def _exact_match(
        self,
        dish_name: str,
        dish_spec: Optional[str]
    ) -> Optional[Dict[str, Any]]:
        """精确匹配"""
        # 匹配菜品名称
        if "菜品名称" not in self.dish_db.columns:
            return None

        matches = self.dish_db[self.dish_db["菜品名称"] == dish_name]

        if matches.empty:
            return None

        # 如果指定了规格,进一步过滤
        if dish_spec and "菜品规格" in self.dish_db.columns:
            spec_matches = matches[matches["菜品规格"] == dish_spec]
            if not spec_matches.empty:
                matches = spec_matches

        # 取第一条记录
        row = matches.iloc[0]
        return {
            "dish_code": row.get("菜品SPU编码", ""),
            "dish_name": row.get("菜品名称", ""),
            "dish_spec": row.get("菜品规格", "")
        }

    def _fuzzy_match(
        self,
        dish_name: str,
        dish_spec: Optional[str]
    ) -> list:
        """
        模糊匹配

        使用Levenshtein距离算法计算相似度
        """
        if "菜品名称" not in self.dish_db.columns:
            return []

        candidates = []

        for _, row in self.dish_db.iterrows():
            db_dish_name = str(row.get("菜品名称", ""))
            db_dish_spec = str(row.get("菜品规格", ""))

            # 计算名称相似度
            name_similarity = ratio(dish_name, db_dish_name)

            # 如果指定了规格,同时考虑规格相似度
            if dish_spec and db_dish_spec:
                spec_similarity = ratio(dish_spec, db_dish_spec)
                # 综合相似度: 名称70% + 规格30%
                total_similarity = name_similarity * 0.7 + spec_similarity * 0.3
            else:
                total_similarity = name_similarity

            candidates.append({
                "dish_code": row.get("菜品SPU编码", ""),
                "dish_name": db_dish_name,
                "dish_spec": db_dish_spec,
                "similarity": total_similarity
            })

        # 按相似度降序排序
        candidates.sort(key=lambda x: x["similarity"], reverse=True)

        return candidates
