#!/usr/bin/env python3
"""
MiniMax Image Prompt Optimizer
Transforms creative briefs into optimized MiniMax Image Generation API prompts.

Author: ZTL Digital Intelligence Operations Center - 创意组
Version: 1.0.0
"""

import re
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict


@dataclass
class ImagePromptInput:
    """Input schema for image prompt optimization."""
    creative_brief: str
    model: Optional[str] = "image-01"
    design_type: Optional[str] = None  # poster, menu, social-media, store-signage, coupon, infographic, product-showcase, event-invitation, branding
    restaurant_type: Optional[str] = None  # hotpot, fine-dining, fast-food, cafe
    aspect_ratio: Optional[str] = None  # 1:1, 16:9, 4:3, 3:2, 2:3, 3:4, 9:16, 21:9
    n: int = 1  # Number of images (1-9)
    artistic_style: Optional[str] = None  # professional, festive, trendy, elegant, rustic
    color_palette: Optional[str] = None  # red-gold, earth-tones, pastel, monochrome
    prompt_optimizer: bool = True


@dataclass
class OptimizedImageOutput:
    """Output schema for optimized image prompt."""
    model: str
    prompt: str
    aspect_ratio: str
    n: int
    prompt_optimizer: bool
    analysis: Dict[str, Union[str, List]]
    api_params: Dict
    optimization_notes: List[str]


class ImagePromptOptimizer:
    """Core optimizer for MiniMax Image Generation API prompts."""

    # Design type to aspect ratio mapping
    DESIGN_ASPECT_RATIOS = {
        "poster": "2:3",
        "menu": "3:4",
        "social-media": "1:1",  # Default, can be 9:16 for Stories/Reels
        "store-signage": "16:9",
        "coupon": "3:2",
        "infographic": "9:16",
        "product-showcase": "1:1",
        "event-invitation": "2:3",
        "branding": "1:1"
    }

    # Restaurant type style mapping
    RESTAURANT_STYLES = {
        "hotpot": {
            "keywords": ["steaming", "spicy", "fresh ingredients", "bubbling broth"],
            "colors": "vibrant red and gold, auspicious festive palette",
            "mood": "warm, inviting, appetizing, lively"
        },
        "fine-dining": {
            "keywords": ["elegant plating", "gourmet", "artistic presentation", "luxury"],
            "colors": "sophisticated black and gold, minimalist tones",
            "mood": "refined, exclusive, high-end, Michelin-star quality"
        },
        "fast-food": {
            "keywords": ["energetic", "bold", "quick service", "value"],
            "colors": "bright primary colors (red, yellow, blue)",
            "mood": "fun, young, dynamic, appetite appeal"
        },
        "cafe": {
            "keywords": ["cozy", "artisan", "latte art", "relaxing"],
            "colors": "warm earth tones, rustic browns and creams",
            "mood": "comfortable, Instagram-worthy, indie aesthetic"
        }
    }

    # Style keywords
    STYLE_KEYWORDS = {
        "professional": "professional graphic design, commercial quality, high-resolution",
        "festive": "festive celebratory atmosphere, joyful vibrant mood, auspicious",
        "trendy": "modern trendy design, social media style, shareable content",
        "elegant": "sophisticated elegant aesthetic, refined luxury, timeless",
        "rustic": "rustic handcrafted style, natural organic feel, artisanal"
    }

    # Quality keywords (always add)
    QUALITY_KEYWORDS = [
        "300 DPI print quality",
        "high-resolution photography",
        "commercial photography standard"
    ]

    def __init__(self):
        self.notes = []

    def optimize(self, input_data: Union[Dict, ImagePromptInput, str]) -> OptimizedImageOutput:
        """Main optimization entry point."""
        self.notes = []

        # Normalize input
        if isinstance(input_data, str):
            input_obj = ImagePromptInput(creative_brief=input_data)
        elif isinstance(input_data, dict):
            input_obj = ImagePromptInput(**input_data)
        else:
            input_obj = input_data

        # Step 1: Analyze intent
        analysis = self._analyze_intent(input_obj)

        # Step 2: Select aspect ratio
        aspect_ratio = self._select_aspect_ratio(input_obj, analysis)

        # Step 3: Build optimized prompt
        prompt = self._build_prompt(input_obj, analysis)

        # Step 4: Build API parameters
        api_params = self._build_api_params(input_obj, prompt, aspect_ratio)

        return OptimizedImageOutput(
            model=input_obj.model,
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            n=input_obj.n,
            prompt_optimizer=input_obj.prompt_optimizer,
            analysis=analysis,
            api_params=api_params,
            optimization_notes=self.notes.copy()
        )

    def _analyze_intent(self, input_obj: ImagePromptInput) -> Dict:
        """Analyze creative brief to extract key elements."""
        brief = input_obj.creative_brief.lower()

        # Detect design type
        detected_design_type = input_obj.design_type or "poster"
        if "海报" in brief or "poster" in brief:
            detected_design_type = "poster"
        elif "菜单" in brief or "menu" in brief:
            detected_design_type = "menu"
        elif "社交" in brief or "抖音" in brief or "instagram" in brief or "tiktok" in brief:
            detected_design_type = "social-media"
        elif "标识" in brief or "signage" in brief or "招牌" in brief:
            detected_design_type = "store-signage"
        elif "优惠券" in brief or "coupon" in brief:
            detected_design_type = "coupon"
        elif "信息图" in brief or "infographic" in brief:
            detected_design_type = "infographic"
        elif "产品" in brief or "product" in brief or "展示" in brief:
            detected_design_type = "product-showcase"
        elif "邀请" in brief or "invitation" in brief:
            detected_design_type = "event-invitation"
        elif "品牌" in brief or "logo" in brief or "标志" in brief:
            detected_design_type = "branding"

        # Detect style
        detected_style = input_obj.artistic_style or "professional"
        if "开业" in brief or "庆祝" in brief or "festive" in brief:
            detected_style = "festive"
        elif "潮流" in brief or "时尚" in brief or "trendy" in brief:
            detected_style = "trendy"
        elif "高端" in brief or "奢华" in brief or "elegant" in brief:
            detected_style = "elegant"
        elif "乡村" in brief or "手工" in brief or "rustic" in brief:
            detected_style = "rustic"

        # Extract composition elements
        composition_elements = []
        if "蒸汽" in brief or "steam" in brief:
            composition_elements.append("rising steam effects")
        if "灯笼" in brief or "lantern" in brief:
            composition_elements.append("Chinese lanterns decoration")
        if "食材" in brief or "ingredient" in brief:
            composition_elements.append("fresh ingredients arrangement")
        if "文字" in brief or "text" in brief or "标题" in brief:
            composition_elements.append("bold headline text")

        return {
            "detected_design_type": detected_design_type,
            "detected_style": detected_style,
            "restaurant_context": input_obj.restaurant_type or "general",
            "composition_elements": composition_elements,
            "quality_keywords": self.QUALITY_KEYWORDS
        }

    def _select_aspect_ratio(self, input_obj: ImagePromptInput, analysis: Dict) -> str:
        """Select optimal aspect ratio."""
        # Priority 1: User specified
        if input_obj.aspect_ratio:
            self.notes.append(f"Using user-specified aspect ratio: {input_obj.aspect_ratio}")
            return input_obj.aspect_ratio

        # Priority 2: Design type default
        design_type = analysis["detected_design_type"]
        default_ratio = self.DESIGN_ASPECT_RATIOS.get(design_type, "1:1")

        # Special handling for social-media
        if design_type == "social-media":
            brief = input_obj.creative_brief.lower()
            if "story" in brief or "reel" in brief or "tiktok" in brief or "抖音" in brief:
                default_ratio = "9:16"
            elif "youtube" in brief or "横版" in brief:
                default_ratio = "16:9"

        self.notes.append(f"Auto-selected aspect ratio {default_ratio} for {design_type}")
        return default_ratio

    def _build_prompt(self, input_obj: ImagePromptInput, analysis: Dict) -> str:
        """Build optimized prompt using formula: Subject + Composition + Style + Lighting + Colors + Quality."""
        brief = input_obj.creative_brief
        design_type = analysis["detected_design_type"]
        style = analysis["detected_style"]
        restaurant_context = analysis["restaurant_context"]

        # Start with base subject
        prompt_parts = [brief]

        # Add restaurant context keywords
        if restaurant_context in self.RESTAURANT_STYLES:
            restaurant_style = self.RESTAURANT_STYLES[restaurant_context]
            prompt_parts.extend(restaurant_style["keywords"][:2])  # Top 2 keywords

        # Add composition elements from analysis
        if analysis["composition_elements"]:
            prompt_parts.extend(analysis["composition_elements"])

        # Add style keywords
        if style in self.STYLE_KEYWORDS:
            prompt_parts.append(self.STYLE_KEYWORDS[style])

        # Add lighting (based on style)
        lighting_map = {
            "professional": "studio soft box lighting, professional photography setup",
            "festive": "warm golden hour lighting, glowing festive lights",
            "trendy": "natural daylight, bright vibrant lighting",
            "elegant": "soft rim lighting, dramatic chiaroscuro",
            "rustic": "natural window light, cozy ambient lighting"
        }
        prompt_parts.append(lighting_map.get(style, "natural lighting"))

        # Add color palette
        if input_obj.color_palette:
            prompt_parts.append(f"{input_obj.color_palette} color palette")
        elif restaurant_context in self.RESTAURANT_STYLES:
            prompt_parts.append(self.RESTAURANT_STYLES[restaurant_context]["colors"])

        # Add mood
        if restaurant_context in self.RESTAURANT_STYLES:
            prompt_parts.append(self.RESTAURANT_STYLES[restaurant_context]["mood"])

        # Add quality keywords
        prompt_parts.extend(analysis["quality_keywords"][:2])  # Top 2 quality keywords

        # Join all parts
        optimized_prompt = ", ".join(prompt_parts)

        # Clean up
        optimized_prompt = re.sub(r',\s*,', ',', optimized_prompt)  # Remove double commas
        optimized_prompt = optimized_prompt.strip()

        return optimized_prompt

    def _build_api_params(self, input_obj: ImagePromptInput, prompt: str, aspect_ratio: str) -> Dict:
        """Build API parameters."""
        params = {
            "model": input_obj.model,
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "n": max(1, min(input_obj.n, 9)),  # Clamp to 1-9
            "prompt_optimizer": input_obj.prompt_optimizer,
            "output_directory": None  # Will be set by caller
        }

        return params

    def validate_for_api(self, optimized: OptimizedImageOutput) -> Dict:
        """Final validation for API call."""
        return {
            "model": optimized.model,
            "prompt": optimized.prompt,
            "aspect_ratio": optimized.aspect_ratio,
            "n": optimized.n,
            "prompt_optimizer": optimized.prompt_optimizer
        }


# CLI testing
if __name__ == "__main__":
    import json

    optimizer = ImagePromptOptimizer()

    # Test 1: Poster
    print("=== Test 1: Hotpot Grand Opening Poster ===")
    result1 = optimizer.optimize({
        "creative_brief": "火锅店开业海报,喜庆的红色配色",
        "restaurant_type": "hotpot",
        "design_type": "poster"
    })
    print(json.dumps(asdict(result1), ensure_ascii=False, indent=2))

    # Test 2: Menu
    print("\n=== Test 2: Fine Dining Menu ===")
    result2 = optimizer.optimize({
        "creative_brief": "高端西餐厅菜单设计,展示法式烩海鲜",
        "restaurant_type": "fine-dining",
        "design_type": "menu"
    })
    print(json.dumps(asdict(result2), ensure_ascii=False, indent=2))

    # Test 3: Social Media
    print("\n=== Test 3: TikTok Promotional Graphic ===")
    result3 = optimizer.optimize({
        "creative_brief": "抖音短视频封面,限时8.8折火锅套餐",
        "restaurant_type": "hotpot",
        "design_type": "social-media"
    })
    print(json.dumps(asdict(result3), ensure_ascii=False, indent=2))
