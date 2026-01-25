#!/usr/bin/env python3
"""
Nano-Banana 技能包使用示例
演示各种使用场景和最佳实践
"""

import os
from pathlib import Path

# 确保从正确的位置导入
import sys
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from core_engine import (
    NanoBananaExecutor,
    ImageConfig,
    ImageInput
)


def example_1_basic_text_to_image():
    """示例 1: 基础文生图 - 火锅店海报"""
    print("\n" + "=" * 60)
    print("示例 1: 基础文生图 - 火锅店开业海报")
    print("=" * 60)

    executor = NanoBananaExecutor()

    result = executor.execute(
        user_prompt="火锅店盛大开业,红色喜庆主色调,金色点缀,热闹氛围",
        task_type="text-to-image",
        context="餐饮行业海报设计",
        target_style="摄影级",
        requirements=["300 DPI", "2:3竖版海报", "可打印质量"],
        config=ImageConfig(
            aspect_ratio="2:3",
            temperature=0.9
        ),
        project_name="火锅店开业筹备"
    )

    if result["success"]:
        print(f"✅ 海报已生成: {result['image_path']}")
        print(f"📝 优化后提示词: {result['optimized_prompt'][:100]}...")
    else:
        print(f"❌ 生成失败: {result.get('error')}")


def example_2_food_photography():
    """示例 2: 菜品摄影 - 美食特写"""
    print("\n" + "=" * 60)
    print("示例 2: 菜品摄影 - 招牌毛肚")
    print("=" * 60)

    executor = NanoBananaExecutor()

    result = executor.execute(
        user_prompt="新鲜毛肚特写,洁白质感,配红油底料,工作室光照,诱人食欲",
        task_type="text-to-image",
        context="餐饮行业菜单摄影",
        target_style="摄影级",
        requirements=["美食摄影标准", "高光泽度", "细节清晰"],
        config=ImageConfig(
            aspect_ratio="4:3",
            temperature=0.7  # 较低温度保证一致性
        ),
        project_name="菜单摄影"
    )

    if result["success"]:
        print(f"✅ 菜品图已生成: {result['image_path']}")


def example_3_social_media():
    """示例 3: 社交媒体内容 - 朋友圈推广"""
    print("\n" + "=" * 60)
    print("示例 3: 社交媒体内容 - 朋友圈推广图")
    print("=" * 60)

    executor = NanoBananaExecutor()

    result = executor.execute(
        user_prompt="火锅店周末优惠活动,满200减50,红色背景,金色优惠文字,醒目吸睛",
        task_type="text-to-image",
        context="餐饮行业社交媒体",
        requirements=["1:1方形", "适合移动端", "优惠信息突出"],
        config=ImageConfig(
            aspect_ratio="1:1",
            temperature=0.8
        ),
        project_name="周末营销活动"
    )

    if result["success"]:
        print(f"✅ 推广图已生成: {result['image_path']}")


def example_4_style_transfer():
    """示例 4: 风格迁移 - 照片转水彩画 (需要输入图像)"""
    print("\n" + "=" * 60)
    print("示例 4: 风格迁移 - 照片转水彩画")
    print("=" * 60)

    # 检查是否有示例图像
    sample_image = Path("input/sample_restaurant.jpg")
    if not sample_image.exists():
        print("⚠️  未找到示例图像,跳过此示例")
        print(f"   请将图像放置在: {sample_image}")
        return

    executor = NanoBananaExecutor()

    input_image = ImageInput(
        path=str(sample_image),
        description="餐厅内部照片"
    )

    result = executor.execute(
        user_prompt="将这张餐厅照片转换为温暖的水彩画风格",
        task_type="style-transfer",
        target_style="水彩",
        images=[input_image],
        project_name="风格迁移实验"
    )

    if result["success"]:
        print(f"✅ 风格迁移完成: {result['image_path']}")


def example_5_consistent_seed():
    """示例 5: 使用固定种子生成一致风格的系列图像"""
    print("\n" + "=" * 60)
    print("示例 5: 固定种子生成系列海报")
    print("=" * 60)

    executor = NanoBananaExecutor()

    # 固定种子确保风格一致
    seed = 1234

    prompts = [
        "火锅店海报 - 麻辣锅底主题",
        "火锅店海报 - 清汤锅底主题",
        "火锅店海报 - 鸳鸯锅主题"
    ]

    for i, prompt in enumerate(prompts, 1):
        result = executor.execute(
            user_prompt=prompt,
            task_type="text-to-image",
            context="餐饮行业海报设计",
            target_style="摄影级",
            config=ImageConfig(
                aspect_ratio="2:3",
                temperature=0.9,
                seed=seed  # 固定种子
            ),
            project_name="系列海报设计"
        )

        if result["success"]:
            print(f"✅ [{i}/{len(prompts)}] 已生成: {Path(result['image_path']).name}")


def example_6_multi_composition():
    """示例 6: 多图合成 (需要多张输入图像)"""
    print("\n" + "=" * 60)
    print("示例 6: 多图合成 - 综合宣传海报")
    print("=" * 60)

    # 检查是否有示例图像
    image1 = Path("input/dish1.jpg")
    image2 = Path("input/dish2.jpg")
    image3 = Path("input/store.jpg")

    if not all([image1.exists(), image2.exists(), image3.exists()]):
        print("⚠️  未找到示例图像,跳过此示例")
        print("   需要以下图像:")
        print(f"   - {image1}")
        print(f"   - {image2}")
        print(f"   - {image3}")
        return

    executor = NanoBananaExecutor()

    images = [
        ImageInput(path=str(image1), description="招牌毛肚"),
        ImageInput(path=str(image2), description="特色鸭血"),
        ImageInput(path=str(image3), description="门店外观")
    ]

    result = executor.execute(
        user_prompt="将三张图片合成为一张综合宣传海报,展示菜品和门店,和谐统一",
        task_type="multi-composition",
        images=images,
        config=ImageConfig(aspect_ratio="16:9"),
        project_name="综合宣传海报"
    )

    if result["success"]:
        print(f"✅ 合成海报已生成: {result['image_path']}")


def main():
    """运行所有示例"""
    print("\n🚀 Nano-Banana 技能包使用示例")
    print("=" * 60)

    # 检查 API Key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("\n⚠️  警告: 未找到 OPENROUTER_API_KEY 环境变量")
        print("请设置 API Key 后再运行实际生成:")
        print("  export OPENROUTER_API_KEY='sk-or-v1-YOUR_API_KEY'")
        print("\n以下示例将仅演示配置和提示词优化,不会实际调用 API\n")
        return

    # 运行各个示例
    try:
        example_1_basic_text_to_image()
        example_2_food_photography()
        example_3_social_media()
        example_4_style_transfer()
        example_5_consistent_seed()
        example_6_multi_composition()

        print("\n" + "=" * 60)
        print("🎉 所有示例运行完成!")
        print("=" * 60)
        print("\n生成的图像位于:")
        print("  - output/[项目名]/nano-banana/results/")
        print("\n元数据文件位于:")
        print("  - output/[项目名]/nano-banana/results/*_metadata.json")

    except Exception as e:
        print(f"\n❌ 示例运行失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
