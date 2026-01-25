#!/usr/bin/env python3
"""
建筑空间设计提示词优化器 (Architecture Space Design Prompt Optimizer)

专为筹建组Nano-banana技能包设计,将任意用户需求优化为高质量建筑空间设计提示词。

核心功能:
1. 文生图 (Text-to-Image): 优化为建筑摄影级别提示词
2. 图生图 (Image-to-Image): 在保持主图风格基础上精准变化

设计原则:
- 建筑摄影风格: 强调空间质感、光影、高质量渲染
- 高清写实感: 8K、photorealistic、architectural photography
- 构图美学: 专业摄影术语 (camera angles, composition)
- 空间美学: 室内设计术语 (materials, textures, lighting)

参考标准:
- Stable Diffusion XL Best Practices
- 建筑摄影行业标准
- 室内设计专业术语
"""

from typing import Dict, List, Optional
import json
import re


class ArchitecturePromptOptimizer:
    """建筑空间设计提示词优化器"""

    # 建筑摄影质量标签 (Photography Quality Tags)
    QUALITY_TAGS = [
        "architectural photography",
        "photorealistic",
        "8K resolution",
        "ultra high detail",
        "professional rendering",
        "sharp focus",
        "hyper realistic"
    ]

    # 相机术语 (Camera Technical Terms)
    CAMERA_TERMS = {
        "front_view": "eye level front shot, symmetrical composition",
        "side_view": "45-degree angle view, dynamic perspective",
        "aerial_view": "bird's eye view, overhead perspective",
        "corner_view": "corner perspective, two-point perspective",
        "wide_angle": "ultra wide angle lens, 16mm, expansive view"
    }

    # 光照氛围 (Lighting Atmosphere)
    LIGHTING_ATMOSPHERE = {
        "warm": "warm ambient lighting, golden hour glow, soft shadows",
        "cool": "cool daylight, bright natural light, clean shadows",
        "dramatic": "dramatic lighting, high contrast, cinematic mood",
        "soft": "soft diffused light, gentle shadows, cozy atmosphere",
        "natural": "natural daylight, floor-to-ceiling windows, bright and airy"
    }

    # 材质描述库 (Materials Library)
    MATERIALS_LIBRARY = {
        "wood": ["oak flooring", "walnut wood panel", "natural wood grain texture", "solid wood furniture"],
        "stone": ["marble countertop", "granite flooring", "travertine wall", "polished stone surface"],
        "metal": ["brushed steel", "polished brass", "industrial iron", "chrome fixtures"],
        "glass": ["floor-to-ceiling glass", "transparent glass partition", "frosted glass", "reflective glass"],
        "concrete": ["polished concrete floor", "exposed concrete wall", "industrial concrete finish"],
        "fabric": ["linen curtains", "velvet upholstery", "wool rug", "silk cushions"]
    }

    # 空间类型关键词 (Space Type Keywords)
    SPACE_TYPE_KEYWORDS = {
        "entrance": "entrance reception area, welcoming lobby, grand foyer",
        "dining": "dining space, restaurant interior, seating area",
        "vip_room": "private dining room, VIP space, intimate setting",
        "kitchen": "professional kitchen, culinary workspace, cooking area",
        "restroom": "restroom foyer, washroom entrance, powder room",
        "cashier": "cashier counter, payment area, service desk",
        "waiting": "waiting lounge, seating area, comfortable waiting space"
    }

    # 负面提示词 (Negative Prompts)
    NEGATIVE_PROMPTS = [
        "blurry",
        "low quality",
        "noise",
        "distorted",
        "warped",
        "cartoon style",
        "anime style",
        "sketch",
        "watercolor",
        "text",
        "watermark",
        "signature",
        "over-decorated",
        "cluttered",
        "crowded",
        "人物" # 默认不包含人物
    ]

    def __init__(self):
        """初始化优化器"""
        self.prompt_max_length = 400  # SDXL推荐最大字符数

    def optimize_text_to_image(
        self,
        raw_description: str,
        space_type: str,
        style_keywords: List[str],
        color_scheme: Dict[str, str],
        materials: List[str],
        lighting: str = "natural",
        view_angle: str = "front_view",
        include_people: bool = False
    ) -> Dict[str, str]:
        """
        优化文生图提示词 (Optimize Text-to-Image Prompt)

        Args:
            raw_description: 用户原始需求描述
            space_type: 空间类型 (entrance/dining/vip_room/kitchen/restroom/cashier/waiting)
            style_keywords: 风格关键词列表 (如 ["新中式", "雅致", "温馨"])
            color_scheme: 色彩方案字典 (如 {"primary": "米白", "secondary": "胡桃木", "accent": "中国红"})
            materials: 材质列表 (如 ["木饰面", "仿古地砖", "实木家具"])
            lighting: 光照氛围类型 (warm/cool/dramatic/soft/natural)
            view_angle: 视角类型 (front_view/side_view/aerial_view/corner_view/wide_angle)
            include_people: 是否包含人物

        Returns:
            包含positive_prompt和negative_prompt的字典
        """

        # 1. 空间类型描述
        space_desc = self.SPACE_TYPE_KEYWORDS.get(space_type, space_type)

        # 2. 风格关键词整合
        style_str = ", ".join(style_keywords)

        # 3. 色彩方案描述
        color_desc = self._format_color_scheme(color_scheme)

        # 4. 材质描述
        materials_str = ", ".join(materials)

        # 5. 光照氛围
        lighting_desc = self.LIGHTING_ATMOSPHERE.get(lighting, lighting)

        # 6. 视角构图
        camera_desc = self.CAMERA_TERMS.get(view_angle, view_angle)

        # 7. 质量标签
        quality_str = ", ".join(self.QUALITY_TAGS)

        # 8. 组装完整提示词 (8-Element Structure)
        positive_prompt = f"{space_desc}, {style_str}, {raw_description}, " \
                         f"{color_desc}, {materials_str}, {lighting_desc}, " \
                         f"{camera_desc}, {quality_str}"

        # 9. 截断至最大长度
        positive_prompt = self._truncate_prompt(positive_prompt, self.prompt_max_length)

        # 10. 生成负面提示词
        negative_prompt = ", ".join(self.NEGATIVE_PROMPTS)
        if include_people:
            # 如果需要人物,移除"人物"负面提示
            negative_prompt = negative_prompt.replace(", 人物", "")

        return {
            "positive_prompt": positive_prompt,
            "negative_prompt": negative_prompt
        }

    def optimize_image_to_image(
        self,
        reference_description: str,
        keep_consistent: List[str],
        change_elements: List[str],
        strength: float = 0.65
    ) -> Dict[str, str]:
        """
        优化图生图提示词 (Optimize Image-to-Image Prompt)

        Args:
            reference_description: 参考主图描述
            keep_consistent: 保持一致的元素列表
            change_elements: 需要改变的元素列表
            strength: 变化强度 (0.4-0.8)

        Returns:
            包含positive_prompt, keep_prompt, change_prompt, strength的字典
        """

        # 1. 保持一致元素
        keep_prompt = ", ".join(keep_consistent)

        # 2. 变化元素
        change_prompt = ", ".join(change_elements)

        # 3. 完整提示词: 参考描述 + 保持一致 + 变化描述
        positive_prompt = f"{reference_description}, maintaining: {keep_prompt}, changing: {change_prompt}"

        # 4. 截断至最大长度
        positive_prompt = self._truncate_prompt(positive_prompt, self.prompt_max_length)

        # 5. 负面提示词
        negative_prompt = ", ".join(self.NEGATIVE_PROMPTS)

        return {
            "positive_prompt": positive_prompt,
            "keep_prompt": keep_prompt,
            "change_prompt": change_prompt,
            "negative_prompt": negative_prompt,
            "strength": strength
        }

    def _format_color_scheme(self, color_scheme: Dict[str, str]) -> str:
        """格式化色彩方案描述"""
        colors = []
        if "primary" in color_scheme:
            colors.append(f"{color_scheme['primary']} as primary color")
        if "secondary" in color_scheme:
            colors.append(f"{color_scheme['secondary']} as secondary color")
        if "accent" in color_scheme:
            colors.append(f"{color_scheme['accent']} as accent color")
        return ", ".join(colors)

    def _truncate_prompt(self, prompt: str, max_length: int) -> str:
        """截断提示词至最大长度,保持句子完整性"""
        if len(prompt) <= max_length:
            return prompt

        # 在最大长度附近找最后一个逗号
        truncated = prompt[:max_length]
        last_comma = truncated.rfind(",")
        if last_comma > max_length * 0.8:  # 如果逗号在80%位置之后
            return truncated[:last_comma].strip()
        else:
            return truncated.strip()

    def generate_config_for_scene(
        self,
        project_name: str,
        scene_name: str,
        space_type: str,
        style_keywords: List[str],
        color_scheme: Dict[str, str],
        materials: List[str],
        raw_description: str,
        lighting: str = "natural",
        view_angle: str = "front_view",
        area: str = "N/A",
        aspect_ratio: str = "16:9"
    ) -> Dict:
        """
        为单个场景生成完整配置 (Generate Full Config for Single Scene)

        Args:
            project_name: 项目名称
            scene_name: 场景名称 (如"入口迎宾区")
            space_type: 空间类型
            style_keywords: 风格关键词
            color_scheme: 色彩方案
            materials: 材质列表
            raw_description: 原始场景描述
            lighting: 光照氛围
            view_angle: 视角
            area: 面积
            aspect_ratio: 宽高比

        Returns:
            场景配置字典
        """

        # 优化提示词
        prompts = self.optimize_text_to_image(
            raw_description=raw_description,
            space_type=space_type,
            style_keywords=style_keywords,
            color_scheme=color_scheme,
            materials=materials,
            lighting=lighting,
            view_angle=view_angle
        )

        # 生成场景配置
        scene_config = {
            "scene_name": scene_name,
            "space_type": space_type,
            "view_angle": view_angle,
            "area": area,
            "prompt": prompts["positive_prompt"],
            "negative_prompt": prompts["negative_prompt"],
            "generation_params": {
                "model": "stable-diffusion-xl",
                "aspect_ratio": aspect_ratio,
                "style_preset": "photographic",
                "cfg_scale": 7.5,
                "steps": 50
            }
        }

        return scene_config

    def export_to_json(self, config: Dict, output_path: str):
        """导出配置为JSON文件"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print(f"✅ 配置已导出: {output_path}")


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 初始化优化器
    optimizer = ArchitecturePromptOptimizer()

    # ========== 示例1: 文生图 - 新中式火锅店入口 ==========
    print("=" * 60)
    print("示例1: 文生图 - 新中式火锅店入口迎宾区")
    print("=" * 60)

    result1 = optimizer.optimize_text_to_image(
        raw_description="米白色墙面配胡桃木色木饰面,古典格栅屏风作为隔断,品牌LOGO墙居中,绿植点缀,温馨雅致",
        space_type="entrance",
        style_keywords=["新中式风格", "对称布局", "现代雅致"],
        color_scheme={
            "primary": "米白色 (#F5F5DC)",
            "secondary": "胡桃木色 (#8B4513)",
            "accent": "中国红 (#DC143C)"
        },
        materials=["木饰面墙板", "仿古地砖", "实木格栅", "宫灯吊灯"],
        lighting="warm",
        view_angle="front_view"
    )

    print("\n✅ 优化后的正向提示词:")
    print(result1["positive_prompt"])
    print(f"\n字符数: {len(result1['positive_prompt'])}")
    print("\n✅ 负面提示词:")
    print(result1["negative_prompt"])

    # ========== 示例2: 图生图 - 角色转身动作 ==========
    print("\n" + "=" * 60)
    print("示例2: 图生图 - 从正面视角变为侧面视角")
    print("=" * 60)

    result2 = optimizer.optimize_image_to_image(
        reference_description="新中式风格餐厅空间,米白色墙面,胡桃木家具,暖黄色灯光",
        keep_consistent=[
            "新中式风格",
            "米白色墙面",
            "胡桃木家具",
            "暖黄色灯光",
            "整体色调"
        ],
        change_elements=[
            "视角从正面改为45度侧面",
            "增加窗外自然光",
            "调整构图为两点透视"
        ],
        strength=0.65
    )

    print("\n✅ 优化后的正向提示词:")
    print(result2["positive_prompt"])
    print(f"\n字符数: {len(result2['positive_prompt'])}")
    print(f"\n变化强度: {result2['strength']}")
    print("\n✅ 保持一致元素:")
    print(result2["keep_prompt"])
    print("\n✅ 变化元素:")
    print(result2["change_prompt"])

    # ========== 示例3: 生成完整场景配置 ==========
    print("\n" + "=" * 60)
    print("示例3: 生成完整场景配置JSON")
    print("=" * 60)

    scene_config = optimizer.generate_config_for_scene(
        project_name="火锅店开业筹备",
        scene_name="入口迎宾区",
        space_type="entrance",
        style_keywords=["新中式风格", "对称布局", "温馨雅致"],
        color_scheme={
            "primary": "米白色",
            "secondary": "胡桃木色",
            "accent": "中国红"
        },
        materials=["木饰面墙板", "仿古地砖", "实木格栅"],
        raw_description="品牌LOGO墙居中,古典格栅屏风隔断,绿植点缀",
        lighting="warm",
        view_angle="front_view",
        area="10㎡",
        aspect_ratio="16:9"
    )

    print("\n✅ 场景配置:")
    print(json.dumps(scene_config, ensure_ascii=False, indent=2))

    print("\n" + "=" * 60)
    print("✅ 所有示例执行完成")
    print("=" * 60)
