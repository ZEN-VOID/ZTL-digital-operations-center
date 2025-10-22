"""
E2 图生图 Skill专用API

提供便捷的图生图调用接口,封装共享核心库。
"""
import sys
from pathlib import Path

# 导入共享核心库
shared_lib = Path(__file__).parent.parent.parent / "_shared"
sys.path.insert(0, str(shared_lib))

from banana_api_core import NanoBananaAPI
from plan_executor import execute_plan

# Skill便捷函数
def generate_image_to_image(source_image: str, processing_type: str, prompt: str = "", **kwargs):
    """
    便捷函数:生成图生图

    Args:
        source_image: 源图片路径
        processing_type: 处理类型
        prompt: 提示词(可选)
        **kwargs: 其他参数

    Returns:
        结果字典
    """
    api = NanoBananaAPI()
    return api.generate_image_to_image(source_image, processing_type, prompt, **kwargs)

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
__all__ = ['generate_image_to_image', 'execute_plan_from_file', 'NanoBananaAPI']
