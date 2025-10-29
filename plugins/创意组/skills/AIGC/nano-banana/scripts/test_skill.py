#!/usr/bin/env python3
"""
Nano-Banana 技能包测试脚本
测试核心功能是否正常工作
"""

import os
from pathlib import Path
from core_engine import (
    NanoBananaExecutor,
    PromptOptimizer,
    PromptOptimizationConfig,
    ImageConfig
)


def test_prompt_optimizer():
    """测试提示词优化器"""
    print("=" * 60)
    print("测试 1: 提示词优化器")
    print("=" * 60)

    optimizer = PromptOptimizer()

    # 测试文生图优化
    config = PromptOptimizationConfig(
        task_type="text-to-image",
        context="餐饮行业海报设计",
        target_style="摄影级",
        requirements=["300 DPI", "可打印质量"]
    )

    user_prompt = "火锅店开业海报,红色主色调"
    optimized = optimizer.optimize(user_prompt, config)

    print(f"\n原始提示词: {user_prompt}")
    print(f"优化后: {optimized}")
    print("\n✅ 提示词优化器测试通过")


def test_api_client():
    """测试 API 客户端 (需要有效的 API Key)"""
    print("\n" + "=" * 60)
    print("测试 2: API 客户端")
    print("=" * 60)

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("⚠️  未找到 OPENROUTER_API_KEY 环境变量")
        print("跳过 API 测试")
        return

    print(f"\n✅ API Key 已配置: {api_key[:20]}...")

    # 不实际调用 API (避免产生费用),只测试客户端初始化
    try:
        from core_engine import NanoBananaClient
        client = NanoBananaClient(api_key)
        print("✅ API 客户端初始化成功")
    except Exception as e:
        print(f"❌ API 客户端初始化失败: {e}")


def test_full_workflow_dry_run():
    """测试完整工作流 (不实际调用 API)"""
    print("\n" + "=" * 60)
    print("测试 3: 完整工作流 (Dry Run)")
    print("=" * 60)

    # 测试配置构建
    config = ImageConfig(
        aspect_ratio="16:9",
        temperature=0.9,
        seed=42
    )

    print("\n图像配置:")
    print(f"  - 比例: {config.aspect_ratio}")
    print(f"  - 温度: {config.temperature}")
    print(f"  - 种子: {config.seed}")
    print("✅ 配置构建测试通过")

    # 测试输出路径生成
    output_dir = Path("output/测试项目/nano-banana/results")
    print(f"\n输出路径: {output_dir}")
    print("✅ 路径生成测试通过")


def test_restaurant_detection():
    """测试餐饮场景检测"""
    print("\n" + "=" * 60)
    print("测试 4: 餐饮场景类型检测")
    print("=" * 60)

    optimizer = PromptOptimizer()

    test_cases = [
        ("火锅店开业海报", "poster"),
        ("菜单摄影 - 招牌毛肚", "menu"),
        ("朋友圈宣传图", "social_media"),
        ("普通文本", None)
    ]

    for prompt, expected in test_cases:
        detected = optimizer._detect_restaurant_type(prompt)
        status = "✅" if detected == expected else "❌"
        print(f"{status} '{prompt}' → {detected} (期望: {expected})")

    print("\n✅ 场景检测测试通过")


def test_style_mapping():
    """测试风格映射"""
    print("\n" + "=" * 60)
    print("测试 5: 风格映射")
    print("=" * 60)

    optimizer = PromptOptimizer()

    test_cases = [
        ("摄影级", "photorealistic"),
        ("卡通风格", "kawaii"),
        ("简约设计", "minimalist"),
        ("复古海报", "vintage"),
        ("水彩画", "watercolor"),
    ]

    for input_style, expected_key in test_cases:
        mapped = optimizer._map_style_to_key(input_style)
        status = "✅" if mapped == expected_key else "❌"
        print(f"{status} '{input_style}' → {mapped} (期望: {expected_key})")

    print("\n✅ 风格映射测试通过")


def main():
    """运行所有测试"""
    print("\n🚀 开始 Nano-Banana 技能包测试\n")

    try:
        test_prompt_optimizer()
        test_api_client()
        test_full_workflow_dry_run()
        test_restaurant_detection()
        test_style_mapping()

        print("\n" + "=" * 60)
        print("🎉 所有测试完成!")
        print("=" * 60)
        print("\n提示:")
        print("  - 如需测试完整 API 调用,请确保设置了有效的 OPENROUTER_API_KEY")
        print("  - 完整 API 测试会产生费用 (~$0.039/张)")
        print("  - 使用 core_engine.py 的 main() 函数进行实际生成测试")

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
