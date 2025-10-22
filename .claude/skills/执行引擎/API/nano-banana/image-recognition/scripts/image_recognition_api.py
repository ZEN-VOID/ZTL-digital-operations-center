"""
E3 图片识别 Skill专用API

提供便捷的图片识别调用接口,封装共享核心库。
"""
import sys
from pathlib import Path

# 导入共享核心库
shared_lib = Path(__file__).parent.parent.parent / "_shared"
sys.path.insert(0, str(shared_lib))

from banana_api_core import NanoBananaAPI
from plan_executor import execute_plan

# Skill便捷函数
def generate_image_recognition(image_path: str, analysis_type: str, **kwargs):
    """
    便捷函数:生成图片识别分析

    Args:
        image_path: 图片路径
        analysis_type: 分析类型
        **kwargs: 其他参数

    Returns:
        结果字典
    """
    api = NanoBananaAPI()
    return api.generate_image_recognition(image_path, analysis_type, **kwargs)

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
__all__ = ['generate_image_recognition', 'execute_plan_from_file', 'NanoBananaAPI']
