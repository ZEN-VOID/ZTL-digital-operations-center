"""
Canvas-Design Floor Plan Generator
专为筹建组Z1-平面图计划师定制的建筑平面图生成技能包

Core Modules:
- floor_plan_generator: 主生成引擎
- config_parser: 配置文档解析
- render_engine: SVG/PNG/PDF渲染
- symbols: 建筑符号库
"""

__version__ = "1.0.0"
__author__ = "Z1-平面图计划师团队"
__last_updated__ = "2025-10-28"

from .floor_plan_generator import generate_floor_plan, batch_generate
from .config_parser import parse_config, validate_config

__all__ = [
    "generate_floor_plan",
    "batch_generate",
    "parse_config",
    "validate_config"
]
