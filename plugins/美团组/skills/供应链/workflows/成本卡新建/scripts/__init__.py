"""
成本卡创建技能包 - 执行层
Cost Card Creator Skill - Execution Layer

提供完整的成本卡自动化创建能力,包括:
- 信息解析 (自然语言/结构化数据)
- 智能编码匹配 (菜品SPU/物品编码)
- Excel文件生成 (基于总部模板)
"""

__version__ = "1.0.0"
__author__ = "ZTL数智化作战中心"

from .cost_card_generator import CostCardGenerator

__all__ = ["CostCardGenerator"]
