#!/usr/bin/env python3
"""
测试Wan技能包提示词优化功能
验证2025最佳实践是否正确集成
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from prompt_optimizer import PromptOptimizer


def test_character_count_validation():
    """测试1: 字符数验证（使用Bash工具）"""
    print("\n" + "="*60)
    print("测试1: 字符数验证（Bash工具）")
    print("="*60)

    optimizer = PromptOptimizer()

    # 测试用例1: 短提示词（需要扩展）
    short_prompt = "一个厨师在厨房烹饪美食"
    print(f"\n测试用例1: 短提示词")
    print(f"原始提示词: {short_prompt}")
    print(f"字符数: {len(short_prompt)}")

    char_count_bash = optimizer.validate_char_count_bash(short_prompt)
    print(f"Bash验证字符数: {char_count_bash}")
    print(f"需要扩展: {char_count_bash < 1500}")

    # 测试用例2: 标准提示词
    standard_prompt = "水彩风格，一位专业厨师在现代化厨房中精心烹饪美食，镜头缓慢推进，展现精致的烹饪细节。" * 20
    print(f"\n测试用例2: 标准提示词")
    print(f"字符数: {len(standard_prompt)}")

    char_count_bash = optimizer.validate_char_count_bash(standard_prompt)
    print(f"Bash验证字符数: {char_count_bash}")
    print(f"是否在1500-2000范围: {1500 <= char_count_bash <= 2000}")


def test_style_keyword_positioning():
    """测试2: 风格关键词位置检查"""
    print("\n" + "="*60)
    print("测试2: 风格关键词位置检查")
    print("="*60)

    optimizer = PromptOptimizer()

    # 测试用例1: 风格关键词在前20字符内（正确）
    good_prompt = "水彩风格，一位专业厨师在现代化厨房中精心烹饪美食，镜头缓慢推进，展现精致的烹饪细节。"
    is_valid, position = optimizer.check_style_keyword_position(good_prompt, "watercolor")
    print(f"\n测试用例1: 风格关键词前置")
    print(f"提示词: {good_prompt[:50]}...")
    print(f"风格关键词位置: {position}")
    print(f"是否在前20字符: {is_valid}")

    # 测试用例2: 风格关键词位置靠后（需要优化）
    bad_prompt = "一位专业厨师在现代化厨房中精心烹饪美食，镜头缓慢推进，展现精致的烹饪细节，整体采用水彩风格。"
    is_valid, position = optimizer.check_style_keyword_position(bad_prompt, "watercolor")
    print(f"\n测试用例2: 风格关键词靠后")
    print(f"提示词: {bad_prompt[:50]}...")
    print(f"风格关键词位置: {position}")
    print(f"是否在前20字符: {is_valid}")


def test_composer_validation():
    """测试3: Composer框架配置验证"""
    print("\n" + "="*60)
    print("测试3: Composer框架配置验证")
    print("="*60)

    optimizer = PromptOptimizer()

    # 测试用例1: 完整配置（正确）
    complete_config = {
        "color_palette": ["#FF5733", "#C70039"],
        "layout": "center",
        "material": "smooth",
        "semantic": "professional"
    }
    is_complete, missing = optimizer.validate_composer_config(complete_config)
    print(f"\n测试用例1: 完整Composer配置")
    print(f"配置: {complete_config}")
    print(f"是否完整: {is_complete}")
    print(f"缺失字段: {missing}")

    # 测试用例2: 不完整配置（需要补充）
    incomplete_config = {
        "color_palette": ["#FF5733"],
        "layout": "center"
    }
    is_complete, missing = optimizer.validate_composer_config(incomplete_config)
    print(f"\n测试用例2: 不完整Composer配置")
    print(f"配置: {incomplete_config}")
    print(f"是否完整: {is_complete}")
    print(f"缺失字段: {missing}")


def test_full_optimization():
    """测试4: 完整优化流程"""
    print("\n" + "="*60)
    print("测试4: 完整优化流程")
    print("="*60)

    optimizer = PromptOptimizer()

    # 测试用例: 短提示词 + 风格 + Composer
    raw_prompt = "一个厨师在厨房烹饪美食"
    style = "watercolor"
    composer_config = {
        "color_palette": ["#FF5733", "#C70039", "#900C3F"],
        "layout": "golden_ratio",
        "material": "watercolor_paper",
        "semantic": "culinary_art"
    }

    print(f"\n原始提示词: {raw_prompt}")
    print(f"风格: {style}")
    print(f"Composer配置: {composer_config}")

    result = optimizer.optimize_prompt(
        raw_prompt=raw_prompt,
        style=style,
        use_composer=True,
        composer_config=composer_config,
        use_qwen_image=False
    )

    print(f"\n优化结果:")
    print(f"优化后提示词长度: {result['char_count_bash']}字符 (Bash验证)")
    print(f"质量检查:")
    print(f"  - 字符范围 (1500-2000): {result['checks']['char_range_valid']}")
    print(f"  - 风格关键词前置: {result['checks']['style_keyword_positioned']}")
    print(f"  - Composer配置完整: {result['checks']['composer_complete']}")

    if result['warnings']:
        print(f"\n警告:")
        for warning in result['warnings']:
            print(f"  - {warning}")

    print(f"\n优化后提示词（前300字符）:")
    print(result['optimized_prompt'][:300] + "...")


def test_qwen_image_optimization():
    """测试5: Qwen-Image文字渲染优化"""
    print("\n" + "="*60)
    print("测试5: Qwen-Image文字渲染优化")
    print("="*60)

    optimizer = PromptOptimizer()

    raw_prompt = "一个带有'开业大吉'文字的火锅店海报"

    print(f"\n原始提示词: {raw_prompt}")

    result = optimizer.optimize_prompt(
        raw_prompt=raw_prompt,
        style="realistic",
        use_composer=False,
        use_qwen_image=True
    )

    print(f"\n优化结果:")
    print(f"优化后提示词长度: {result['char_count_bash']}字符")
    print(f"Qwen-Image优化已应用: {result['checks']['qwen_image_optimized']}")

    print(f"\n优化后提示词（前300字符）:")
    print(result['optimized_prompt'][:300] + "...")


def main():
    """运行所有测试"""
    print("\n" + "🎬"*30)
    print("Wan技能包 - 提示词优化功能测试")
    print("2025最佳实践验证")
    print("🎬"*30)

    try:
        test_character_count_validation()
        test_style_keyword_positioning()
        test_composer_validation()
        test_full_optimization()
        test_qwen_image_optimization()

        print("\n" + "="*60)
        print("✅ 所有测试完成")
        print("="*60)

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        print(traceback.format_exc())


if __name__ == "__main__":
    main()
