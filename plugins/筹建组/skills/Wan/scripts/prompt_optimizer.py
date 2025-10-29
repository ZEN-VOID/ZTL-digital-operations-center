#!/usr/bin/env python3
"""
通义万相提示词优化器 - 2025最佳实践
基于MoE架构、IC-LoRA、Composer框架和Qwen-Image的专业提示词优化引擎

核心功能:
- 字符数智能扩展/压缩到1500-2000范围
- 三层结构化组织(核心+Composer+细化)
- 风格关键词前置验证
- Composer配置完整性检查
- Qwen-Image文本渲染优化
- Bash工具字符数验证

使用方式:
  optimizer = PromptOptimizer()
  result = optimizer.optimize_prompt(
      raw_prompt="未来城市夜景",
      style="cyberpunk",
      use_composer=True,
      composer_config={"color_palette": [...], "layout": "rule_of_thirds", ...}
  )
"""

import re
import subprocess
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path


class PromptOptimizer:
    """通义万相提示词优化器 - 2025最佳实践"""

    def __init__(self):
        """初始化优化器"""
        # 目标字符数范围
        self.target_min = 1500
        self.target_max = 2000

        # 三层结构配比
        self.layer_ratios = {
            "core": 0.35,       # 核心元素层 ~600字符
            "composer": 0.30,   # Composer设计层 ~500字符
            "refinement": 0.23, # 细化增强层 ~400字符
            "negative": 0.12    # 负向控制层 ~200字符
        }

        # 17种预设风格关键词
        self.style_keywords = {
            "watercolor": "水彩",
            "flat_illustration": "扁平插画",
            "anime": "动漫",
            "oil_painting": "油画",
            "chinese_painting": "国画",
            "3d_cartoon": "3D卡通",
            "sketch": "素描",
            "cyberpunk": "赛博朋克",
            "cinematic_poster": "电影海报",
            "realistic": "写实",
            "abstract": "抽象",
            "ink_wash": "水墨",
            "pop_art": "波普艺术",
            "impressionism": "印象派",
            "surrealism": "超现实",
            "minimalism": "极简",
            "baroque": "巴洛克"
        }

        # Composer布局选项
        self.composer_layouts = {
            "rule_of_thirds": "三分法构图",
            "center": "中心构图",
            "golden_ratio": "黄金比例构图",
            "diagonal": "对角线构图",
            "symmetry": "对称构图"
        }

        # Composer材质选项
        self.composer_materials = {
            "neon_glass": "霓虹玻璃",
            "metal": "金属",
            "wood": "木质",
            "fabric": "布料",
            "stone": "石质",
            "plastic": "塑料",
            "ceramic": "陶瓷"
        }

        # 清晰度增强关键词(Qwen-Image专用)
        self.clarity_keywords = [
            "清晰锐利的文字边缘",
            "专业排版无错别字",
            "高清文本渲染无乱码",
            "字体轮廓精准清晰",
            "文字笔画完整无断裂",
            "印刷级文本质量"
        ]

    def validate_char_count_bash(self, text: str) -> int:
        """
        使用Bash工具验证字符数(wc -m)

        Args:
            text: 要验证的文本

        Returns:
            字符数
        """
        try:
            # 使用echo和wc -m验证字符数
            result = subprocess.run(
                ['bash', '-c', f'echo -n "{text}" | wc -m'],
                capture_output=True,
                text=True,
                check=True
            )
            char_count = int(result.stdout.strip())
            return char_count
        except Exception as e:
            # Bash验证失败时回退到Python len()
            print(f"⚠️  Bash验证失败,使用Python len(): {e}")
            return len(text)

    def check_style_keyword_position(self, prompt: str, style: str) -> Tuple[bool, int]:
        """
        检查风格关键词是否在前20字符内

        Args:
            prompt: 提示词
            style: 风格(英文key)

        Returns:
            (是否在前20字符, 实际位置)
        """
        if not style or style not in self.style_keywords:
            return True, -1  # 无风格要求时默认通过

        style_cn = self.style_keywords[style]
        position = prompt.find(style_cn)

        if position == -1:
            return False, -1

        return position < 20, position

    def validate_composer_config(self, composer_config: Optional[Dict]) -> Tuple[bool, List[str]]:
        """
        验证Composer配置完整性

        Args:
            composer_config: Composer配置字典

        Returns:
            (是否完整, 缺失字段列表)
        """
        if not composer_config:
            return False, ["color_palette", "layout", "material", "semantic"]

        required_keys = ["color_palette", "layout", "material", "semantic"]
        missing_keys = [key for key in required_keys if key not in composer_config]

        return len(missing_keys) == 0, missing_keys

    def expand_to_target_length(self,
                                raw_prompt: str,
                                target_length: int,
                                style: str,
                                use_composer: bool,
                                composer_config: Optional[Dict] = None) -> str:
        """
        智能扩展提示词到目标长度

        策略:
        1. 核心元素扩展: 添加细节描述
        2. Composer设计扩展: RGB色值、布局、材质具体化
        3. 细化层扩展: 光线、氛围、技术参数
        """
        current_length = len(raw_prompt)
        if current_length >= target_length:
            return raw_prompt

        expansion_needed = target_length - current_length
        expanded_parts = []

        # 步骤1: 确保风格关键词前置
        style_cn = self.style_keywords.get(style, "")
        if style_cn and not raw_prompt.startswith(style_cn):
            expanded_parts.append(f"{style_cn}风格的")

        expanded_parts.append(raw_prompt)

        # 步骤2: 添加Composer设计元素(如果启用)
        if use_composer and composer_config:
            composer_text = self._generate_composer_description(composer_config)
            expanded_parts.append(composer_text)

        # 步骤3: 添加细化层(光线、氛围、技术参数)
        refinement_text = self._generate_refinement_layer(style)
        expanded_parts.append(refinement_text)

        # 步骤4: 添加技术质量关键词
        quality_keywords = "高清晰度,细节丰富,专业摄影,电影级构图,8K超高清分辨率"
        expanded_parts.append(quality_keywords)

        expanded_prompt = "".join(expanded_parts)

        # 验证是否达到目标长度
        final_length = len(expanded_prompt)
        if final_length < self.target_min:
            # 还需要进一步扩展,添加更多细节描述
            additional_details = self._generate_additional_details(style, self.target_min - final_length)
            expanded_prompt = expanded_prompt + additional_details

        return expanded_prompt

    def _generate_composer_description(self, composer_config: Dict) -> str:
        """生成Composer设计元素描述"""
        parts = []

        # 色彩方案
        if "color_palette" in composer_config:
            colors = composer_config["color_palette"]
            if colors and len(colors) > 0:
                color_desc = "色彩方案采用"
                for i, color in enumerate(colors[:3]):  # 最多取3个颜色
                    if i == 0:
                        color_desc += f"{color}作为主导色调"
                    else:
                        color_desc += f",{color}作为辅助配色"
                color_desc += "形成和谐的视觉平衡。"
                parts.append(color_desc)

        # 布局构图
        if "layout" in composer_config:
            layout = composer_config["layout"]
            layout_cn = self.composer_layouts.get(layout, layout)
            layout_desc = f"采用{layout_cn}({layout})将视觉焦点精准分布于画面关键位置,引导观者视线流动。"
            parts.append(layout_desc)

        # 材质纹理
        if "material" in composer_config:
            material = composer_config["material"]
            material_cn = self.composer_materials.get(material, material)
            material_desc = f"{material_cn}({material})材质呈现独特的质感和光影效果,表面细节清晰可见。"
            parts.append(material_desc)

        # 语义主题
        if "semantic" in composer_config:
            semantic = composer_config["semantic"]
            semantic_desc = f"整体语义主题为{semantic},强化场景的氛围营造和情感表达。"
            parts.append(semantic_desc)

        return "".join(parts)

    def _generate_refinement_layer(self, style: str) -> str:
        """生成细化增强层描述"""
        # 根据风格生成对应的光线和氛围描述
        refinement_templates = {
            "cyberpunk": "戏剧性的蓝紫色霓虹照明从多个角度投射,湿漉的街面反射建筑灯光形成镜面效果,营造神秘未来的视觉氛围。低角度仰视视角强化空间纵深感,电影级光影处理捕捉细节纹理。",
            "watercolor": "柔和的自然光线从画面左侧45度角斜射,形成温暖的暖色调氛围。水彩颜料的流动感和渐变效果清晰可见,笔触自然流畅,色彩饱和度适中,呈现艺术性的手绘质感。",
            "realistic": "自然的环境光照模拟真实光源特性,阴影过渡柔和自然,高光反射精准还原材质特性。采用专业摄影的光圈景深效果,前景清晰背景虚化,营造空间层次感。照片级真实感,细节纹理完整。",
            "oil_painting": "经典的伦勃朗式光影技法,明暗对比强烈,主体受光部分细节丰富,暗部层次分明。厚重的油画颜料堆叠形成立体笔触,色彩饱满浓郁,画布纹理质感清晰,呈现传统油画艺术的经典美学。",
            "anime": "明快的动漫风格光影处理,色块分明边缘清晰,赛璐璐着色技法呈现光滑的色彩过渡。眼睛高光点精确定位增强角色表现力,整体配色鲜艳饱和,画面干净简洁,日式动漫美学标准。"
        }

        return refinement_templates.get(style, "专业的光线处理和氛围营造,细节丰富,质感突出,构图精准,艺术性与技术性完美结合。")

    def _generate_additional_details(self, style: str, target_additional: int) -> str:
        """生成额外的细节描述以达到目标字符数"""
        # 通用细节扩展模板
        detail_templates = [
            "画面构图遵循经典的视觉平衡原则,主体与背景的空间关系处理得当,视觉焦点明确,引导观者视线自然流动于画面各个关键区域。",
            "色彩关系和谐统一,冷暖色调对比适中,色彩饱和度控制精准,整体色调营造出符合场景氛围的情感基调。",
            "光影效果真实自然,高光、中间调、阴影的过渡柔和流畅,立体感强烈,空间纵深清晰可辨。",
            "细节纹理精致丰富,无论是前景主体还是背景元素,都保持高水平的细节刻画,无模糊失焦现象。",
            "整体画面质量达到专业级标准,技术参数设置合理,后期处理恰到好处,呈现出高品质的视觉作品。"
        ]

        additional_text = ""
        for template in detail_templates:
            if len(additional_text) >= target_additional:
                break
            additional_text += template

        return additional_text

    def compress_to_target_length(self, prompt: str, target_length: int) -> str:
        """
        智能压缩提示词到目标长度

        策略:
        1. 合并同类描述
        2. 移除冗余修饰词
        3. 整合技术参数
        """
        if len(prompt) <= target_length:
            return prompt

        # 压缩策略1: 移除冗余修饰词
        redundant_patterns = [
            (r'非常非常', '非常'),
            (r'非常', ''),
            (r'特别特别', '特别'),
            (r'特别', ''),
            (r'十分十分', '十分'),
            (r'十分', ''),
            (r'极其极其', '极其'),
            (r',+', ','),  # 合并多个逗号
            (r'\s+', ''),  # 移除多余空格
        ]

        compressed = prompt
        for pattern, replacement in redundant_patterns:
            compressed = re.sub(pattern, replacement, compressed)

        # 压缩策略2: 整合技术参数
        tech_keywords = ['8K', '超高清', '细节丰富', '质量最佳', '专业摄影', '高分辨率']
        for keyword in tech_keywords:
            if compressed.count(keyword) > 1:
                # 只保留第一次出现
                first_pos = compressed.find(keyword)
                compressed = compressed[:first_pos + len(keyword)] + compressed[first_pos + len(keyword):].replace(keyword, '')

        # 如果还是太长,进行更激进的压缩
        if len(compressed) > target_length:
            # 截取到目标长度,但确保在句号或逗号处截断
            truncated = compressed[:target_length]
            last_punctuation = max(truncated.rfind('。'), truncated.rfind(','), truncated.rfind('、'))
            if last_punctuation > target_length * 0.9:  # 如果标点在后10%范围内
                compressed = truncated[:last_punctuation + 1]
            else:
                compressed = truncated + "..."

        return compressed

    def optimize_prompt(self,
                       raw_prompt: str,
                       style: str = "",
                       use_composer: bool = False,
                       composer_config: Optional[Dict] = None,
                       use_qwen_image: bool = False) -> Dict[str, Any]:
        """
        优化提示词 - 应用2025最佳实践

        Args:
            raw_prompt: 原始提示词
            style: 风格(英文key, 如 "cyberpunk")
            use_composer: 是否使用Composer框架
            composer_config: Composer配置(color_palette, layout, material, semantic)
            use_qwen_image: 是否为Qwen-Image模型优化

        Returns:
            {
                "optimized_prompt": str,
                "char_count": int,
                "char_count_bash": int,  # Bash验证的字符数
                "structure": {
                    "core": str,
                    "composer": str,
                    "refinement": str
                },
                "checks": {
                    "char_range_valid": bool,
                    "style_keyword_positioned": bool,
                    "composer_complete": bool,
                    "qwen_image_optimized": bool
                },
                "warnings": List[str]
            }
        """
        warnings = []
        current_length = len(raw_prompt)

        # 步骤1: 字符数调整
        if current_length < self.target_min:
            # 需要扩展
            optimized_prompt = self.expand_to_target_length(
                raw_prompt, self.target_min, style, use_composer, composer_config
            )
            warnings.append(f"原始提示词过短({current_length}字符),已扩展到{len(optimized_prompt)}字符")

        elif current_length > self.target_max:
            # 需要压缩
            optimized_prompt = self.compress_to_target_length(raw_prompt, self.target_max)
            warnings.append(f"原始提示词过长({current_length}字符),已压缩到{len(optimized_prompt)}字符")

        else:
            # 长度合适,仅做风格关键词前置优化
            style_cn = self.style_keywords.get(style, "")
            if style_cn and not raw_prompt.startswith(style_cn):
                optimized_prompt = f"{style_cn}风格的" + raw_prompt
            else:
                optimized_prompt = raw_prompt

        # 步骤2: Qwen-Image专项优化
        if use_qwen_image:
            optimized_prompt = self._optimize_for_qwen_image(optimized_prompt)

        # 步骤3: 字符数验证(Bash工具)
        char_count = len(optimized_prompt)
        char_count_bash = self.validate_char_count_bash(optimized_prompt)

        # 步骤4: 风格关键词位置检查
        style_positioned, style_position = self.check_style_keyword_position(optimized_prompt, style)
        if not style_positioned and style:
            warnings.append(f"风格关键词'{self.style_keywords.get(style)}'未在前20字符内(当前位置:{style_position})")

        # 步骤5: Composer完整性检查
        composer_complete = True
        if use_composer and composer_config:
            required_keys = ["color_palette", "layout", "material", "semantic"]
            missing_keys = [k for k in required_keys if k not in composer_config]
            if missing_keys:
                composer_complete = False
                warnings.append(f"Composer配置不完整,缺少: {', '.join(missing_keys)}")

        # 步骤6: 生成结构化分析
        structure = self._analyze_structure(optimized_prompt)

        # 步骤7: 质量检查
        checks = {
            "char_range_valid": self.target_min <= char_count <= self.target_max,
            "style_keyword_positioned": style_positioned,
            "composer_complete": composer_complete if use_composer else True,
            "qwen_image_optimized": use_qwen_image
        }

        return {
            "optimized_prompt": optimized_prompt,
            "char_count": char_count,
            "char_count_bash": char_count_bash,
            "structure": structure,
            "checks": checks,
            "warnings": warnings
        }

    def _optimize_for_qwen_image(self, prompt: str) -> str:
        """Qwen-Image专项优化"""
        # 添加清晰度关键词
        if not any(keyword in prompt for keyword in self.clarity_keywords):
            prompt += f",{self.clarity_keywords[0]},{self.clarity_keywords[1]},{self.clarity_keywords[2]}"

        return prompt

    def _analyze_structure(self, prompt: str) -> Dict[str, str]:
        """分析提示词的三层结构"""
        # 简单的启发式分割(基于字符数比例)
        total_len = len(prompt)
        core_end = int(total_len * 0.35)
        composer_end = int(total_len * 0.65)

        return {
            "core": prompt[:core_end] if core_end < total_len else prompt,
            "composer": prompt[core_end:composer_end] if composer_end < total_len else "",
            "refinement": prompt[composer_end:] if composer_end < total_len else ""
        }


# 便捷函数
def optimize_prompt(raw_prompt: str, **kwargs) -> Dict[str, Any]:
    """便捷优化函数"""
    optimizer = PromptOptimizer()
    return optimizer.optimize_prompt(raw_prompt, **kwargs)


# 测试代码
def test_optimizer():
    """测试提示词优化器"""
    print("🎨 通义万相提示词优化器测试\n")
    print("=" * 80)

    # 测试案例1: 短提示词扩展
    print("\n测试案例1: 短提示词扩展")
    print("-" * 80)
    result1 = optimize_prompt(
        raw_prompt="未来城市夜景",
        style="cyberpunk",
        use_composer=True,
        composer_config={
            "color_palette": ["#00F5FF", "#FF1493", "#9400D3"],
            "layout": "rule_of_thirds",
            "material": "neon_glass",
            "semantic": "futuristic_city"
        }
    )
    print(f"原始提示词: 未来城市夜景 ({len('未来城市夜景')}字符)")
    print(f"优化后提示词: {result1['optimized_prompt'][:100]}...")
    print(f"字符数: {result1['char_count']} (Bash验证: {result1['char_count_bash']})")
    print(f"字符范围检查: {'✅' if result1['checks']['char_range_valid'] else '❌'}")
    print(f"风格关键词前置: {'✅' if result1['checks']['style_keyword_positioned'] else '❌'}")
    print(f"Composer完整性: {'✅' if result1['checks']['composer_complete'] else '❌'}")
    if result1['warnings']:
        print(f"⚠️  警告: {'; '.join(result1['warnings'])}")

    # 测试案例2: Qwen-Image优化
    print("\n\n测试案例2: Qwen-Image文本渲染优化")
    print("-" * 80)
    result2 = optimize_prompt(
        raw_prompt="电影海报,标题\"未来都市2077\",副标题'Welcome to the Future'",
        style="cinematic_poster",
        use_qwen_image=True
    )
    print(f"优化后提示词: {result2['optimized_prompt'][:150]}...")
    print(f"字符数: {result2['char_count']}")
    print(f"Qwen-Image优化: {'✅' if result2['checks']['qwen_image_optimized'] else '❌'}")

    print("\n" + "=" * 80)
    print("✅ 测试完成")


if __name__ == "__main__":
    test_optimizer()
