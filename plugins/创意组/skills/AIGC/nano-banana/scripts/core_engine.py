#!/usr/bin/env python3
"""
Nano-Banana AIGC 核心执行引擎
====================================
基于 Google Gemini 2.5 Flash Image (OpenRouter)
支持多种图像生成和编辑能力

能力矩阵:
- 文生图 (Text-to-Image)
- 图生图 (Image-to-Image)
- 图像编辑 (Editing)
- 风格迁移 (Style Transfer)
- 多图合成 (Multi-Image Composition)
- 角色一致性 (Character Consistency)
- 背景替换 (Background Replacement)
- 局部优化 (Local Enhancement)
"""

import base64
import json
import os
import requests
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Literal, Optional, Dict, Any


# ============================================
# 环境变量加载
# ============================================

def load_env_from_root():
    """从项目根目录的 .env 文件加载环境变量"""
    # 查找项目根目录（包含 .env 的目录）
    current_dir = Path(__file__).resolve()
    for parent in [current_dir] + list(current_dir.parents):
        env_file = parent / ".env"
        if env_file.exists():
            # 读取 .env 文件
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    # 跳过空行和注释
                    if not line or line.startswith("#"):
                        continue
                    # 解析 KEY=VALUE
                    if "=" in line:
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip()
                        # 只设置未设置的环境变量
                        if key not in os.environ:
                            os.environ[key] = value
            return True
    return False


# 自动加载根目录 .env
load_env_from_root()


# ============================================
# 配置和数据类
# ============================================

@dataclass
class ImageConfig:
    """图像生成配置"""
    aspect_ratio: str = "1:1"  # 1:1, 16:9, 4:3, 3:2, 2:3, 3:4, 9:16, 21:9
    max_tokens: int = 8192
    temperature: float = 1.0
    top_p: float = 0.95
    seed: Optional[int] = None


@dataclass
class PromptOptimizationConfig:
    """提示词优化配置"""
    task_type: Literal[
        "text-to-image",
        "image-to-image",
        "editing",
        "style-transfer",
        "multi-composition",
        "character-consistency",
        "background-replacement",
        "local-enhancement"
    ]
    context: str  # 业务场景描述 (如: "餐饮行业海报设计")
    target_style: Optional[str] = None  # 目标风格 (如: "摄影级", "卡通风格", "水彩画")
    requirements: List[str] = None  # 特殊要求列表


@dataclass
class ImageInput:
    """图像输入"""
    path: Optional[str] = None  # 本地路径
    url: Optional[str] = None  # 网络URL
    base64_data: Optional[str] = None  # Base64编码
    description: Optional[str] = None  # 图像描述 (用于多图合成时的语义理解)


# ============================================
# 提示词优化引擎
# ============================================

class PromptOptimizer:
    """
    提示词自动优化引擎
    根据不同任务类型和业务场景,优化用户输入的提示词
    """

    # 摄影术语库
    PHOTOGRAPHY_TERMS = {
        "lighting": [
            "golden hour light", "soft diffused lighting", "dramatic side lighting",
            "three-point lighting", "softbox setup", "natural window light",
            "rim lighting", "ambient occlusion"
        ],
        "lens": [
            "85mm portrait lens", "24mm wide-angle", "macro lens", "50mm prime",
            "telephoto zoom", "fisheye lens"
        ],
        "shot_type": [
            "close-up", "medium shot", "wide shot", "bird's eye view",
            "low-angle shot", "Dutch angle", "over-the-shoulder"
        ],
        "depth": [
            "shallow depth of field", "bokeh background", "f/1.8 aperture",
            "sharp focus foreground", "blurred background"
        ]
    }

    # 设计风格库
    DESIGN_STYLES = {
        "photorealistic": (
            "ultra-realistic commercial photography, 8K resolution, shot on medium format digital camera, "
            "professional studio lighting, high dynamic range, physical material textures, "
            "editorial magazine quality, NOT illustration, NOT vector graphics, NOT CGI rendering, "
            "authentic photographic grain, real-world lighting physics"
        ),
        "kawaii": "cute kawaii style, bold outlines, pastel colors, chibi proportions",
        "minimalist": "clean minimalist design, simple composition, negative space, modern aesthetic",
        "vintage": "vintage aesthetic, film grain, retro color grading, nostalgic mood",
        "watercolor": "watercolor painting style, soft edges, flowing colors, artistic brush strokes",
        "corporate": "professional corporate style, clean lines, trustworthy aesthetic, brand-focused"
    }

    # 餐饮行业专用优化模板
    RESTAURANT_TEMPLATES = {
        "poster": {
            "prefix": "Commercial restaurant promotional poster shot on Hasselblad medium format camera,",
            "suffix": (
                "CRITICAL: photorealistic poster (NOT vector graphics, NOT SVG, NOT web design), "
                "professional studio lighting setup, editorial photography quality, "
                "physical material textures, billboard advertising style, "
                "shot with 85mm portrait lens, f/2.8 aperture, shallow depth of field, "
                "magazine cover aesthetics, high-end commercial photography"
            )
        },
        "menu": {
            "prefix": "Professional restaurant menu photography shot in commercial food studio,",
            "suffix": (
                "appetizing food styling, three-point studio lighting, "
                "medium format camera quality, 100mm macro lens, "
                "Michelin-star presentation, editorial food photography"
            )
        },
        "social_media": {
            "prefix": "Eye-catching social media restaurant photography,",
            "suffix": (
                "natural lighting, smartphone-native aesthetic, "
                "Instagram-worthy composition, authentic candid style, "
                "mobile-optimized, vibrant colors, shareable visual storytelling"
            )
        }
    }

    def optimize(
        self,
        user_prompt: str,
        config: PromptOptimizationConfig
    ) -> str:
        """
        优化用户提示词

        Args:
            user_prompt: 用户原始输入
            config: 优化配置

        Returns:
            优化后的提示词
        """
        # 根据任务类型选择优化策略
        if config.task_type == "text-to-image":
            return self._optimize_text_to_image(user_prompt, config)
        elif config.task_type in ["editing", "local-enhancement"]:
            return self._optimize_editing(user_prompt, config)
        elif config.task_type == "style-transfer":
            return self._optimize_style_transfer(user_prompt, config)
        elif config.task_type == "multi-composition":
            return self._optimize_multi_composition(user_prompt, config)
        else:
            return self._optimize_general(user_prompt, config)

    def _optimize_text_to_image(
        self,
        user_prompt: str,
        config: PromptOptimizationConfig
    ) -> str:
        """文生图优化策略"""
        optimized = []

        # 1. 添加业务场景上下文
        if "餐饮" in config.context or "restaurant" in config.context.lower():
            template_type = self._detect_restaurant_type(user_prompt)
            if template_type:
                template = self.RESTAURANT_TEMPLATES[template_type]
                optimized.append(template["prefix"])

        # 2. 增强用户原始描述
        optimized.append(self._enhance_description(user_prompt))

        # 3. 添加风格术语
        if config.target_style:
            style_key = self._map_style_to_key(config.target_style)
            if style_key in self.DESIGN_STYLES:
                optimized.append(self.DESIGN_STYLES[style_key])

        # 4. 添加摄影技术细节 (如果是摄影级风格)
        if config.target_style and "摄影" in config.target_style:
            optimized.extend([
                self._select_lighting(),
                self._select_lens(),
                self._select_composition()
            ])

        # 5. 添加特殊要求
        if config.requirements:
            optimized.extend(config.requirements)

        # 6. 添加业务场景后缀
        if "餐饮" in config.context:
            template_type = self._detect_restaurant_type(user_prompt)
            if template_type:
                optimized.append(self.RESTAURANT_TEMPLATES[template_type]["suffix"])

        return ", ".join(filter(None, optimized))

    def _optimize_editing(
        self,
        user_prompt: str,
        config: PromptOptimizationConfig
    ) -> str:
        """图像编辑优化策略"""
        # 编辑类提示词需要明确的动作指令
        action_verbs = {
            "添加": "Add", "删除": "Remove", "替换": "Replace",
            "修改": "Modify", "增强": "Enhance", "模糊": "Blur"
        }

        optimized_prompt = user_prompt
        for zh, en in action_verbs.items():
            if zh in user_prompt:
                optimized_prompt = f"{en} {optimized_prompt.replace(zh, '')}"
                break

        # 添加保留语义
        optimized_prompt += ", preserve other elements unchanged, maintain original lighting and perspective"

        return optimized_prompt

    def _optimize_style_transfer(
        self,
        user_prompt: str,
        config: PromptOptimizationConfig
    ) -> str:
        """风格迁移优化策略"""
        if not config.target_style:
            return user_prompt

        style_key = self._map_style_to_key(config.target_style)
        style_desc = self.DESIGN_STYLES.get(style_key, config.target_style)

        return f"Transform the image to {style_desc}, {user_prompt}, preserve subject composition"

    def _optimize_multi_composition(
        self,
        user_prompt: str,
        config: PromptOptimizationConfig
    ) -> str:
        """多图合成优化策略"""
        return f"Seamlessly compose multiple images: {user_prompt}, maintain consistent lighting across all elements, natural perspective blending, cohesive color harmony"

    def _optimize_general(
        self,
        user_prompt: str,
        config: PromptOptimizationConfig
    ) -> str:
        """通用优化策略"""
        return self._enhance_description(user_prompt)

    # ========== 辅助方法 ==========

    def _enhance_description(self, prompt: str) -> str:
        """增强描述的具体性"""
        # 如果提示词过短,提醒用户提供更多细节
        if len(prompt) < 20:
            return f"{prompt}, detailed scene description, specific visual characteristics"
        return prompt

    def _detect_restaurant_type(self, prompt: str) -> Optional[str]:
        """检测餐饮场景类型"""
        # 优先级: 社交媒体 > 菜单 > 海报 (避免"朋友圈宣传图"被错误识别为海报)
        if any(kw in prompt for kw in ["朋友圈", "社交", "social"]):
            return "social_media"
        elif any(kw in prompt for kw in ["菜单", "menu", "菜品"]):
            return "menu"
        elif any(kw in prompt for kw in ["海报", "poster", "宣传"]):
            return "poster"
        return None

    def _map_style_to_key(self, style: str) -> str:
        """映射风格描述到样式键"""
        mapping = {
            "摄影": "photorealistic",
            "卡通": "kawaii",
            "简约": "minimalist",
            "复古": "vintage",
            "水彩": "watercolor",
            "商务": "corporate"
        }
        for zh, en in mapping.items():
            if zh in style:
                return en
        return style.lower()

    def _select_lighting(self) -> str:
        """智能选择光照术语"""
        return self.PHOTOGRAPHY_TERMS["lighting"][0]  # 默认金色时光

    def _select_lens(self) -> str:
        """智能选择镜头术语"""
        return self.PHOTOGRAPHY_TERMS["lens"][0]  # 默认85mm人像镜头

    def _select_composition(self) -> str:
        """智能选择构图术语"""
        return self.PHOTOGRAPHY_TERMS["shot_type"][0]  # 默认特写


# ============================================
# API 客户端
# ============================================

class NanoBananaClient:
    """
    Nano-Banana API 客户端
    封装 OpenRouter 的 Google Gemini 2.5 Flash Image 调用
    """

    API_BASE = "https://openrouter.ai/api/v1"
    MODEL = "google/gemini-2.5-flash-image"

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化客户端

        Args:
            api_key: OpenRouter API Key (如未提供则从环境变量读取)
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("未找到 OPENROUTER_API_KEY, 请设置环境变量或传入参数")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/anthropics/claude-code",
            "X-Title": "ZTL-Digital-Operations-Center-Nano-Banana-AIGC"
        }

    def generate(
        self,
        prompt: str,
        images: Optional[List[ImageInput]] = None,
        config: Optional[ImageConfig] = None
    ) -> Dict[str, Any]:
        """
        生成图像

        Args:
            prompt: 优化后的提示词
            images: 输入图像列表 (用于图生图、编辑等任务)
            config: 生成配置

        Returns:
            API 响应 (包含生成的图像)
        """
        if config is None:
            config = ImageConfig()

        # 构建消息内容
        content_parts = []

        # 添加输入图像 (如有)
        if images:
            for img in images:
                img_part = self._prepare_image_part(img)
                if img_part:
                    content_parts.append(img_part)
                    # 添加图像描述 (如有)
                    if img.description:
                        content_parts.append({
                            "type": "text",
                            "text": f"[Image context: {img.description}]"
                        })

        # 添加文本提示词
        content_parts.append({
            "type": "text",
            "text": prompt
        })

        # 构建请求体
        payload = {
            "model": self.MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": content_parts
                }
            ],
            "max_tokens": config.max_tokens,
            "temperature": config.temperature,
            "top_p": config.top_p
        }

        # 添加可选参数
        if config.seed is not None:
            payload["seed"] = config.seed

        # 发送请求
        response = requests.post(
            f"{self.API_BASE}/chat/completions",
            headers=self.headers,
            json=payload,
            timeout=120
        )

        response.raise_for_status()
        return response.json()

    def _prepare_image_part(self, image_input: ImageInput) -> Optional[Dict[str, Any]]:
        """准备图像内容部分"""
        # 优先使用 base64 数据
        if image_input.base64_data:
            return {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_input.base64_data}"
                }
            }

        # 如果提供了本地路径,读取并转换为 base64
        if image_input.path:
            path = Path(image_input.path)
            if not path.exists():
                print(f"警告: 图像文件不存在: {image_input.path}")
                return None

            with open(path, "rb") as f:
                img_data = base64.b64encode(f.read()).decode("utf-8")

            mime_type = self._get_mime_type(path.suffix)
            return {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{img_data}"
                }
            }

        # 如果提供了 URL
        if image_input.url:
            return {
                "type": "image_url",
                "image_url": {
                    "url": image_input.url
                }
            }

        return None

    @staticmethod
    def _get_mime_type(suffix: str) -> str:
        """根据文件后缀获取 MIME 类型"""
        mime_map = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp"
        }
        return mime_map.get(suffix.lower(), "image/jpeg")


# ============================================
# 图像提取和保存
# ============================================

class ImageExtractor:
    """从 API 响应中提取和保存图像"""

    @staticmethod
    def extract_image_from_response(response: Dict[str, Any]) -> Optional[str]:
        """
        从 API 响应中提取图像数据

        Returns:
            Base64 编码的图像数据 (不含前缀)
        """
        try:
            # Gemini 2.5 Flash Image 返回的图像在 choices[0].message.images 中
            choices = response.get("choices", [])
            if not choices:
                print("API 响应中没有生成内容")
                return None

            message = choices[0].get("message", {})

            # 优先检查 images 字段
            images = message.get("images", [])
            if images:
                image_url = images[0].get("image_url", {}).get("url", "")
                if image_url.startswith("data:image"):
                    # 提取 base64 部分
                    return image_url.split(",", 1)[1]

            # 兼容旧格式: 检查 content 字段
            content = message.get("content", "")
            if isinstance(content, str):
                # 提取 markdown 中的图像 URL
                import re
                img_pattern = r'!\[.*?\]\((data:image/[^;]+;base64,([^)]+))\)'
                matches = re.findall(img_pattern, content)
                if matches:
                    return matches[0][1]  # 返回 base64 部分

                # 或者直接是 base64 数据
                if content.startswith("data:image"):
                    return content.split(",", 1)[1]

            return None

        except Exception as e:
            print(f"提取图像失败: {e}")
            return None

    @staticmethod
    def save_image(
        base64_data: str,
        output_dir: Path,
        filename: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Path:
        """
        保存图像到文件

        Args:
            base64_data: Base64 编码的图像数据
            output_dir: 输出目录
            filename: 文件名 (如未提供则自动生成)
            metadata: 元数据 (保存为 JSON)

        Returns:
            保存的文件路径
        """
        # 确保输出目录存在
        output_dir.mkdir(parents=True, exist_ok=True)

        # 生成文件名
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"nano_banana_{timestamp}.png"

        # 保存图像
        img_path = output_dir / filename
        img_data = base64.b64decode(base64_data)
        img_path.write_bytes(img_data)

        # 保存元数据
        if metadata:
            meta_path = output_dir / f"{img_path.stem}_metadata.json"
            meta_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2))

        return img_path


# ============================================
# 统一任务执行器
# ============================================

class NanoBananaExecutor:
    """
    Nano-Banana 统一任务执行器
    集成提示词优化、API调用、图像保存的完整流程
    """

    def __init__(self, api_key: Optional[str] = None):
        self.client = NanoBananaClient(api_key)
        self.optimizer = PromptOptimizer()
        self.extractor = ImageExtractor()

    def execute(
        self,
        user_prompt: str,
        task_type: str = "text-to-image",
        context: str = "",
        target_style: Optional[str] = None,
        requirements: Optional[List[str]] = None,
        images: Optional[List[ImageInput]] = None,
        config: Optional[ImageConfig] = None,
        output_dir: Optional[Path] = None,
        project_name: str = "未命名项目"
    ) -> Dict[str, Any]:
        """
        执行完整的图像生成流程

        Args:
            user_prompt: 用户输入的提示词
            task_type: 任务类型
            context: 业务场景上下文
            target_style: 目标风格
            requirements: 特殊要求列表
            images: 输入图像列表
            config: 生成配置
            output_dir: 输出目录 (如未提供则使用默认路径)
            project_name: 项目名称 (用于输出路径)

        Returns:
            执行结果 (包含图像路径、元数据等)
        """
        # 1. 提示词优化
        opt_config = PromptOptimizationConfig(
            task_type=task_type,
            context=context,
            target_style=target_style,
            requirements=requirements or []
        )
        optimized_prompt = self.optimizer.optimize(user_prompt, opt_config)

        print(f"原始提示词: {user_prompt}")
        print(f"优化后提示词: {optimized_prompt}")
        print("-" * 60)

        # 2. API 调用
        print("正在调用 Nano-Banana API...")
        response = self.client.generate(
            prompt=optimized_prompt,
            images=images,
            config=config
        )

        # 3. 提取图像
        base64_data = self.extractor.extract_image_from_response(response)
        if not base64_data:
            return {
                "success": False,
                "error": "未能从响应中提取图像",
                "response": response
            }

        # 4. 保存图像
        if output_dir is None:
            # 使用标准化输出路径: output/[项目名]/nano-banana/
            output_dir = Path("output") / project_name / "nano-banana" / "results"

        metadata = {
            "task_type": task_type,
            "user_prompt": user_prompt,
            "optimized_prompt": optimized_prompt,
            "context": context,
            "target_style": target_style,
            "requirements": requirements,
            "timestamp": datetime.now().isoformat(),
            "model": NanoBananaClient.MODEL,
            "api_response": response
        }

        img_path = self.extractor.save_image(
            base64_data=base64_data,
            output_dir=output_dir,
            metadata=metadata
        )

        print(f"✅ 图像已保存到: {img_path}")

        return {
            "success": True,
            "image_path": str(img_path),
            "optimized_prompt": optimized_prompt,
            "metadata": metadata
        }


# ============================================
# 命令行接口 (供测试使用)
# ============================================

def main():
    """命令行测试接口"""
    import argparse

    parser = argparse.ArgumentParser(description="Nano-Banana AIGC 核心引擎")
    parser.add_argument("prompt", help="图像生成提示词")
    parser.add_argument("--type", default="text-to-image",
                       choices=["text-to-image", "image-to-image", "editing",
                               "style-transfer", "multi-composition"],
                       help="任务类型")
    parser.add_argument("--context", default="", help="业务场景上下文")
    parser.add_argument("--style", help="目标风格")
    parser.add_argument("--output", help="输出目录")
    parser.add_argument("--project", default="测试项目", help="项目名称")

    args = parser.parse_args()

    executor = NanoBananaExecutor()
    result = executor.execute(
        user_prompt=args.prompt,
        task_type=args.type,
        context=args.context,
        target_style=args.style,
        output_dir=Path(args.output) if args.output else None,
        project_name=args.project
    )

    if result["success"]:
        print(f"\n✨ 成功生成图像!")
        print(f"📁 文件位置: {result['image_path']}")
    else:
        print(f"\n❌ 生成失败: {result.get('error')}")


if __name__ == "__main__":
    main()
