#!/usr/bin/env python3
"""
Nano-Banana AIGC 核心执行引擎 v2.0
====================================
基于 Google Gemini 2.5 Flash Image (OpenRouter)
支持9种图片处理工作流,每种工作流都有专属提示词优化策略

工作流矩阵:
1. 文生图 (text-to-image)
2. 风格参考生图 (style-reference)
3. 主体参考生图 (subject-reference)
4. 背景替换 (background-replace)
5. 主体替换 (subject-replace)
6. 局部修改 (local-edit)
7. 调整动作/角度/空间 (pose-angle-space)
8. 风格转绘 (style-transfer)
9. 提示词优化器 (自动集成到所有工作流)
"""

import base64
import json
import os
import requests
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Literal, Optional, Dict, Any


# ============================================
# 环境变量加载
# ============================================

def load_env_from_root():
    """从项目根目录的 .env 文件加载环境变量"""
    current_dir = Path(__file__).resolve()
    for parent in [current_dir] + list(current_dir.parents):
        env_file = parent / ".env"
        if env_file.exists():
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip()
                        if key not in os.environ:
                            os.environ[key] = value
            return True
    return False


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
        "style-reference",
        "subject-reference",
        "background-replace",
        "subject-replace",
        "local-edit",
        "pose-angle-space",
        "style-transfer"
    ]
    context: str  # 业务场景描述 (如: "餐饮行业海报设计")
    target_style: Optional[str] = None  # 目标风格
    requirements: List[str] = field(default_factory=list)  # 特殊要求列表


@dataclass
class ImageInput:
    """图像输入"""
    path: Optional[str] = None  # 本地路径
    url: Optional[str] = None  # 网络URL
    base64_data: Optional[str] = None  # Base64编码
    description: Optional[str] = None  # 图像描述


# ============================================
# 提示词优化引擎 v2.0 (9种工作流专属优化)
# ============================================

class PromptOptimizer:
    """
    提示词自动优化引擎 v2.0
    为9种图片处理工作流提供专属优化策略
    """

    # 摄影术语库
    PHOTOGRAPHY_TERMS = {
        "lighting": [
            "golden hour light", "soft diffused lighting", "dramatic side lighting",
            "three-point lighting", "softbox setup", "natural window light"
        ],
        "lens": [
            "85mm portrait lens", "24mm wide-angle", "macro lens",
            "50mm prime", "telephoto zoom"
        ],
        "shot_type": [
            "close-up", "medium shot", "wide shot", "bird's eye view",
            "45-degree angle", "overhead shot"
        ],
        "depth": [
            "shallow depth of field", "bokeh background", "f/2.8 aperture",
            "sharp focus", "natural depth"
        ]
    }

    # 设计风格库
    DESIGN_STYLES = {
        "photorealistic": (
            "ultra-realistic commercial photography, 8K resolution, "
            "shot on medium format camera, professional studio lighting, "
            "high dynamic range, physical material textures, "
            "NOT illustration, NOT CGI, authentic photographic quality"
        ),
        "水彩": "watercolor painting style, soft edges, flowing colors, artistic brush strokes",
        "卡通": "kawaii cartoon style, bold outlines, vibrant colors, cute aesthetic",
        "简约": "minimalist design, clean lines, negative space, modern aesthetic",
        "复古": "vintage aesthetic, film grain, retro color grading, nostalgic mood"
    }

    # 餐饮行业场景模板
    RESTAURANT_SCENARIOS = {
        "海报设计": {
            "keywords": ["海报", "poster", "宣传"],
            "prefix": "Commercial restaurant promotional poster,",
            "suffix": "professional poster photography, billboard quality, high-resolution"
        },
        "菜单摄影": {
            "keywords": ["菜单", "menu", "菜品"],
            "prefix": "Professional restaurant menu photography,",
            "suffix": "appetizing presentation, three-point lighting, Michelin-star quality"
        },
        "社交媒体": {
            "keywords": ["朋友圈", "社交", "social", "抖音"],
            "prefix": "Eye-catching social media restaurant content,",
            "suffix": "Instagram-worthy, mobile-optimized, shareable aesthetic"
        },
        "产品图": {
            "keywords": ["产品", "商品", "展示"],
            "prefix": "Professional product photography,",
            "suffix": "clean background, studio lighting, commercial quality"
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
        task_type = config.task_type

        if task_type == "text-to-image":
            return self._optimize_text_to_image(user_prompt, config)
        elif task_type == "style-reference":
            return self._optimize_style_reference(user_prompt, config)
        elif task_type == "subject-reference":
            return self._optimize_subject_reference(user_prompt, config)
        elif task_type == "background-replace":
            return self._optimize_background_replace(user_prompt, config)
        elif task_type == "subject-replace":
            return self._optimize_subject_replace(user_prompt, config)
        elif task_type == "local-edit":
            return self._optimize_local_edit(user_prompt, config)
        elif task_type == "pose-angle-space":
            return self._optimize_pose_angle_space(user_prompt, config)
        elif task_type == "style-transfer":
            return self._optimize_style_transfer(user_prompt, config)
        else:
            return self._enhance_description(user_prompt)

    # ========== 1. 文生图优化策略 ==========
    def _optimize_text_to_image(
        self,
        user_prompt: str,
        config: PromptOptimizationConfig
    ) -> str:
        """文生图: Subject + Composition + Style + Lighting + Colors + Quality"""
        parts = []

        # 1. 餐饮场景前缀
        scenario = self._detect_restaurant_scenario(user_prompt)
        if scenario:
            template = self.RESTAURANT_SCENARIOS[scenario]
            parts.append(template["prefix"])

        # 2. 增强用户描述
        parts.append(self._enhance_description(user_prompt))

        # 3. 风格术语
        if config.target_style:
            style_key = self._map_style_key(config.target_style)
            if style_key in self.DESIGN_STYLES:
                parts.append(self.DESIGN_STYLES[style_key])
            else:
                parts.append(config.target_style)

        # 4. 摄影技术细节
        if config.target_style and "摄影" in config.target_style:
            parts.extend([
                self.PHOTOGRAPHY_TERMS["lighting"][0],
                self.PHOTOGRAPHY_TERMS["lens"][0],
                self.PHOTOGRAPHY_TERMS["depth"][0]
            ])

        # 5. 特殊要求
        if config.requirements:
            parts.extend(config.requirements)

        # 6. 餐饮场景后缀
        if scenario:
            parts.append(self.RESTAURANT_SCENARIOS[scenario]["suffix"])

        return ", ".join(filter(None, parts))

    # ========== 2. 风格参考生图优化策略 ==========
    def _optimize_style_reference(
        self,
        user_prompt: str,
        config: PromptOptimizationConfig
    ) -> str:
        """风格参考: 风格特征提取 + 风格一致性指令"""
        parts = [
            "Match the visual style of the reference image exactly,",
            "preserve color palette, composition style, texture quality,",
            user_prompt,
            "maintain brand consistency, style coherence priority"
        ]
        return " ".join(parts)

    # ========== 3. 主体参考生图优化策略 ==========
    def _optimize_subject_reference(
        self,
        user_prompt: str,
        config: PromptOptimizationConfig
    ) -> str:
        """主体参考: 主体特征锁定 + 场景融合"""
        parts = [
            "Keep the subject character/object from reference image EXACTLY the same,",
            "preserve all visual features (appearance, clothing, details),",
            user_prompt,
            "natural scene integration, consistent lighting with environment,",
            "character/product consistency is critical priority"
        ]
        return " ".join(parts)

    # ========== 4. 背景替换优化策略 ==========
    def _optimize_background_replace(
        self,
        user_prompt: str,
        config: PromptOptimizationConfig
    ) -> str:
        """背景替换: 主体保护 + 新背景描述 + 光照一致性"""
        parts = [
            "Preserve the main subject completely unchanged (keep all details intact),",
            f"replace background with: {user_prompt},",
            "seamless lighting transition between subject and new background,",
            "natural compositing, realistic integration, coherent atmosphere"
        ]
        return " ".join(parts)

    # ========== 5. 主体替换优化策略 ==========
    def _optimize_subject_replace(
        self,
        user_prompt: str,
        config: PromptOptimizationConfig
    ) -> str:
        """主体替换: 背景保护 + 新主体描述 + 透视一致性"""
        parts = [
            "Preserve the background environment completely unchanged,",
            f"replace the main subject with: {user_prompt},",
            "maintain consistent lighting and perspective with original scene,",
            "natural integration, realistic shadows and reflections"
        ]
        return " ".join(parts)

    # ========== 6. 局部修改优化策略 ==========
    def _optimize_local_edit(
        self,
        user_prompt: str,
        config: PromptOptimizationConfig
    ) -> str:
        """局部修改: 精确区域定位 + 保护非修改区 + 自然过渡"""
        parts = [
            f"Precisely edit the specified region: {user_prompt},",
            "keep ALL other elements completely unchanged,",
            "seamless transition with surrounding areas,",
            "natural blending, invisible editing, preserve original quality"
        ]
        return " ".join(parts)

    # ========== 7. 动作/角度/空间调整优化策略 ==========
    def _optimize_pose_angle_space(
        self,
        user_prompt: str,
        config: PromptOptimizationConfig
    ) -> str:
        """动作/角度/空间: 视角变换 + 主体一致性 + 物理合理性"""
        parts = [
            "Keep the subject's appearance, textures, colors EXACTLY the same,",
            f"adjust the pose/angle/spatial relationship: {user_prompt},",
            "maintain consistent lighting direction and quality,",
            "physically plausible transformation, realistic shadows and perspective"
        ]
        return " ".join(parts)

    # ========== 8. 风格转绘优化策略 ==========
    def _optimize_style_transfer(
        self,
        user_prompt: str,
        config: PromptOptimizationConfig
    ) -> str:
        """风格转绘: 风格详细描述 + 内容保留 + 风格化程度"""
        target_style = config.target_style or "artistic style"

        # 详细风格描述
        style_details = self.DESIGN_STYLES.get(
            self._map_style_key(target_style),
            target_style
        )

        parts = [
            f"Transform the image to {style_details},",
            "preserve ALL scene content and composition structure,",
            user_prompt,
            "maintain recognizability of original subjects,",
            "balanced stylization level, artistic yet coherent"
        ]
        return " ".join(parts)

    # ========== 辅助方法 ==========

    def _enhance_description(self, prompt: str) -> str:
        """增强描述的具体性"""
        if len(prompt) < 20:
            return f"{prompt}, detailed scene description, specific visual characteristics"
        return prompt

    def _detect_restaurant_scenario(self, prompt: str) -> Optional[str]:
        """检测餐饮场景类型 (优先级: 社交媒体 > 菜单 > 产品 > 海报)"""
        for scenario_name, scenario_data in self.RESTAURANT_SCENARIOS.items():
            if any(kw in prompt for kw in scenario_data["keywords"]):
                return scenario_name
        return None

    def _map_style_key(self, style: str) -> str:
        """映射风格描述到样式键"""
        mapping = {
            "摄影": "photorealistic",
            "写实": "photorealistic",
            "水彩": "水彩",
            "卡通": "卡通",
            "简约": "简约",
            "复古": "复古"
        }
        for zh, key in mapping.items():
            if zh in style:
                return key
        return style


# ============================================
# 任务类型推荐配置
# ============================================

TASK_TYPE_CONFIGS = {
    "text-to-image": {
        "temperature": 1.0,
        "aspect_ratio": "16:9"
    },
    "style-reference": {
        "temperature": 0.8,  # 风格一致性需要更低温度
        "aspect_ratio": None  # 继承参考图比例
    },
    "subject-reference": {
        "temperature": 0.7,  # 角色一致性优先
        "aspect_ratio": None
    },
    "background-replace": {
        "temperature": 0.8,
        "aspect_ratio": None
    },
    "subject-replace": {
        "temperature": 0.8,
        "aspect_ratio": None
    },
    "local-edit": {
        "temperature": 0.6,  # 精确编辑需要低温度
        "aspect_ratio": None
    },
    "pose-angle-space": {
        "temperature": 0.7,
        "aspect_ratio": None
    },
    "style-transfer": {
        "temperature": 1.0,  # 风格转换允许更高创意度
        "aspect_ratio": None
    }
}


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
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("未找到 OPENROUTER_API_KEY, 请设置环境变量或传入参数")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/anthropics/claude-code",
            "X-Title": "ZTL-Digital-Operations-Center-Nano-Banana-AIGC-v2"
        }

    def generate(
        self,
        prompt: str,
        images: Optional[List[ImageInput]] = None,
        config: Optional[ImageConfig] = None
    ) -> Dict[str, Any]:
        """生成图像"""
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

        # 本地路径转 base64
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

        # URL 图像
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
                    return image_url.split(",", 1)[1]

            # 兼容旧格式: content 字段
            content = message.get("content", "")
            if isinstance(content, str):
                import re
                img_pattern = r'!\[.*?\]\((data:image/[^;]+;base64,([^)]+))\)'
                matches = re.findall(img_pattern, content)
                if matches:
                    return matches[0][1]

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
        task_type: str,
        filename: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Path:
        """
        保存图像到文件

        Args:
            base64_data: Base64 编码的图像数据
            output_dir: 输出目录
            task_type: 任务类型 (用于文件名)
            filename: 文件名 (如未提供则自动生成)
            metadata: 元数据 (保存为 JSON)

        Returns:
            保存的文件路径
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        # 生成文件名
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"nano_banana_{task_type}_{timestamp}.png"

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
    Nano-Banana 统一任务执行器 v2.0
    支持9种图片处理工作流,自动提示词优化
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
            task_type: 任务类型 (支持9种工作流)
            context: 业务场景上下文
            target_style: 目标风格
            requirements: 特殊要求列表
            images: 输入图像列表
            config: 生成配置
            output_dir: 输出目录
            project_name: 项目名称

        Returns:
            执行结果
        """
        # 验证 task_type
        valid_types = [
            "text-to-image", "style-reference", "subject-reference",
            "background-replace", "subject-replace", "local-edit",
            "pose-angle-space", "style-transfer"
        ]
        if task_type not in valid_types:
            raise ValueError(f"不支持的任务类型: {task_type}. 支持的类型: {valid_types}")

        # 1. 自动应用推荐配置
        if config is None:
            config = ImageConfig()
            recommended = TASK_TYPE_CONFIGS.get(task_type, {})
            if "temperature" in recommended:
                config.temperature = recommended["temperature"]
            if "aspect_ratio" in recommended and recommended["aspect_ratio"]:
                config.aspect_ratio = recommended["aspect_ratio"]

        # 2. 提示词优化
        opt_config = PromptOptimizationConfig(
            task_type=task_type,
            context=context,
            target_style=target_style,
            requirements=requirements or []
        )
        optimized_prompt = self.optimizer.optimize(user_prompt, opt_config)

        print(f"[任务类型] {task_type}")
        print(f"[原始提示词] {user_prompt}")
        print(f"[优化后提示词] {optimized_prompt}")
        print("-" * 80)

        # 3. API 调用
        print("正在调用 Nano-Banana API...")
        response = self.client.generate(
            prompt=optimized_prompt,
            images=images,
            config=config
        )

        # 4. 提取图像
        base64_data = self.extractor.extract_image_from_response(response)
        if not base64_data:
            return {
                "success": False,
                "error": "未能从响应中提取图像",
                "response": response
            }

        # 5. 保存图像
        if output_dir is None:
            # 标准化输出路径: output/[项目名]/nano-banana/results/
            output_dir = Path("output") / project_name / "nano-banana" / "results"

        metadata = {
            "task_type": task_type,
            "original_prompt": user_prompt,
            "optimized_prompt": optimized_prompt,
            "context": context,
            "target_style": target_style,
            "requirements": requirements,
            "input_images": [img.path for img in (images or []) if img.path],
            "config": {
                "aspect_ratio": config.aspect_ratio,
                "temperature": config.temperature,
                "max_tokens": config.max_tokens,
                "seed": config.seed
            },
            "timestamp": datetime.now().isoformat(),
            "model": NanoBananaClient.MODEL,
            "api_usage": response.get("usage", {})
        }

        img_path = self.extractor.save_image(
            base64_data=base64_data,
            output_dir=output_dir,
            task_type=task_type,
            metadata=metadata
        )

        print(f"✅ 图像已保存到: {img_path}")
        print(f"📊 元数据: {img_path.parent / f'{img_path.stem}_metadata.json'}")

        return {
            "success": True,
            "image_path": str(img_path),
            "task_type": task_type,
            "optimized_prompt": optimized_prompt,
            "metadata": metadata
        }


# ============================================
# 命令行接口 (供测试使用)
# ============================================

def main():
    """命令行测试接口"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Nano-Banana AIGC 核心引擎 v2.0 - 9种图片处理工作流"
    )
    parser.add_argument("prompt", help="图像生成提示词")
    parser.add_argument(
        "--type",
        default="text-to-image",
        choices=[
            "text-to-image", "style-reference", "subject-reference",
            "background-replace", "subject-replace", "local-edit",
            "pose-angle-space", "style-transfer"
        ],
        help="任务类型"
    )
    parser.add_argument("--context", default="", help="业务场景上下文")
    parser.add_argument("--style", help="目标风格")
    parser.add_argument("--image", action="append", help="输入图像路径 (可多次指定)")
    parser.add_argument("--output", help="输出目录")
    parser.add_argument("--project", default="测试项目", help="项目名称")

    args = parser.parse_args()

    # 准备输入图像
    images = None
    if args.image:
        images = [ImageInput(path=img_path) for img_path in args.image]

    executor = NanoBananaExecutor()
    result = executor.execute(
        user_prompt=args.prompt,
        task_type=args.type,
        context=args.context,
        target_style=args.style,
        images=images,
        output_dir=Path(args.output) if args.output else None,
        project_name=args.project
    )

    if result["success"]:
        print(f"\n✨ 成功生成图像!")
        print(f"📁 文件位置: {result['image_path']}")
        print(f"🎯 任务类型: {result['task_type']}")
    else:
        print(f"\n❌ 生成失败: {result.get('error')}")


if __name__ == "__main__":
    main()
