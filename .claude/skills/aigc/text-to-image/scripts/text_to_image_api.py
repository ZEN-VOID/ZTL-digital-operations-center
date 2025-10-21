"""
E1 文生图 Skill专用API

提供便捷的文生图调用接口,封装共享核心库。
"""
import sys
from pathlib import Path

# 导入共享核心库
shared_lib = Path(__file__).parent.parent.parent / "_shared"
sys.path.insert(0, str(shared_lib))

from banana_api_core import NanoBananaAPI
from plan_executor import execute_plan

# Skill便捷函数
def generate_text_to_image(prompt: str, design_type: str, **kwargs):
    """
    便捷函数:生成文生图

    Args:
        prompt: 文字描述
        design_type: 设计类型(1-poster, 2-menu等)
        **kwargs: 其他参数

    Returns:
        结果字典
    """
    api = NanoBananaAPI()
    return api.generate_text_to_image(prompt, design_type, **kwargs)

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
__all__ = ['generate_text_to_image', 'execute_plan_from_file', 'NanoBananaAPI']
