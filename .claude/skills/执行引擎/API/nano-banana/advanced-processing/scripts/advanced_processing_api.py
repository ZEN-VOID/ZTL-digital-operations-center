"""
E4-E9 高级处理 Skill专用API

提供便捷的高级处理调用接口,封装共享核心库。
支持智能修复、结构控制、图像融合、角色一致性、设计迭代、超分增强。
"""
import sys
from pathlib import Path

# 导入共享核心库
shared_lib = Path(__file__).parent.parent.parent / "_shared"
sys.path.insert(0, str(shared_lib))

from banana_api_core import NanoBananaAPI
from plan_executor import execute_plan

# E4: 智能修复
def generate_smart_repair(image_path: str, repair_type: str, **kwargs):
    """智能修复"""
    api = NanoBananaAPI()
    return api.generate_smart_repair(image_path, repair_type, **kwargs)

# E5: 结构控制
def generate_structure_control(image_path: str, control_type: str, **kwargs):
    """结构控制"""
    api = NanoBananaAPI()
    return api.generate_structure_control(image_path, control_type, **kwargs)

# E6: 图像融合
def generate_image_fusion(images: list, fusion_type: str, **kwargs):
    """图像融合"""
    api = NanoBananaAPI()
    return api.generate_image_fusion(images, fusion_type, **kwargs)

# E7: 角色一致性
def generate_character_consistency(reference_image: str, character_type: str, **kwargs):
    """角色一致性"""
    api = NanoBananaAPI()
    return api.generate_character_consistency(reference_image, character_type, **kwargs)

# E8: 设计迭代
def generate_design_iteration(base_image: str, iteration_type: str, **kwargs):
    """设计迭代"""
    api = NanoBananaAPI()
    return api.generate_design_iteration(base_image, iteration_type, **kwargs)

# E9: 超分增强
def generate_super_resolution(image_path: str, enhancement_type: str, **kwargs):
    """超分增强"""
    api = NanoBananaAPI()
    return api.generate_super_resolution(image_path, enhancement_type, **kwargs)

def execute_plan_from_file(plan_path: str):
    """
    便捷函数:从JSON执行计划生成

    Args:
        plan_path: JSON计划文件路径

    Returns:
        结果字典
    """
    return execute_plan(plan_path)

# 导出主要接口
__all__ = [
    'generate_smart_repair',
    'generate_structure_control',
    'generate_image_fusion',
    'generate_character_consistency',
    'generate_design_iteration',
    'generate_super_resolution',
    'execute_plan_from_file',
    'NanoBananaAPI'
]
