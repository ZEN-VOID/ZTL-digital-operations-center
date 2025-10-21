"""AIGC API配置管理"""
import os
from pathlib import Path

class AIGCConfig:
    """统一配置管理"""

    # OpenRouter配置
    API_KEY = "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"
    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
    MODEL = "google/gemini-2.5-flash-image-preview"

    # 项目根目录
    # __file__ 在 .claude/skills/aigc/_shared/config.py
    # parent -> _shared, parent -> aigc, parent -> skills, parent -> .claude, parent -> 项目根目录
    PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent

    # 输出路径 - 按部门组织
    OUTPUT_BASE = PROJECT_ROOT / "output"
    CREATIVE_TEAM_DIR = OUTPUT_BASE / "创意组"

    # 默认项目名称(可通过环境变量覆盖)
    DEFAULT_PROJECT_NAME = os.getenv("AIGC_PROJECT_NAME", "AIGC生成")

    @classmethod
    def get_output_path(cls, project_name: str = None, subfolder: str = "images"):
        """
        获取输出路径

        Args:
            project_name: 项目名称,默认使用DEFAULT_PROJECT_NAME
            subfolder: 子文件夹名称 (images/prompts/metadata等)

        Returns:
            Path对象,格式为 output/创意组/[项目名]/[subfolder]/
        """
        proj_name = project_name or cls.DEFAULT_PROJECT_NAME
        return cls.CREATIVE_TEAM_DIR / proj_name / subfolder

    @classmethod
    def get_images_dir(cls, project_name: str = None):
        """获取图片输出目录"""
        return cls.get_output_path(project_name, "images")

    @classmethod
    def get_prompts_dir(cls, project_name: str = None):
        """获取提示词输出目录"""
        return cls.get_output_path(project_name, "prompts")

    @classmethod
    def get_metadata_dir(cls, project_name: str = None):
        """获取元数据输出目录"""
        return cls.get_output_path(project_name, "metadata")
