#!/usr/bin/env python3
"""
冰川鲜毛肚海报生成脚本
使用 Gemini 2.5 Flash Image (Nano-Banana) API
"""

import os
import json
import base64
from datetime import datetime
from pathlib import Path

def generate_poster():
    """生成冰川鲜毛肚海报"""

    # 1. 读取执行计划
    plan_path = Path('/Users/vincentlee/Desktop/ZTL数智化作战中心/api/plans/e1-text-to-image/glacier-tripe-poster.json')
    with open(plan_path, 'r', encoding='utf-8') as f:
        plan = json.load(f)

    # 2. 提取提示词和配置
    prompt = plan['input_data']['text_prompt']
    output_dir = Path('/Users/vincentlee/Desktop/ZTL数智化作战中心') / plan['output_settings']['save_path']
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / plan['output_settings']['filename']

    print("=" * 80)
    print("🎨 冰川鲜毛肚海报生成任务")
    print("=" * 80)
    print(f"\n📋 任务ID: {plan['plan_id']}")
    print(f"🎯 设计类型: {plan['input_data']['design_type']}")
    print(f"📐 尺寸比例: {plan['input_data']['aspect_ratio']}")
    print(f"\n💬 提示词预览:")
    print(f"   {prompt[:150]}...")
    print(f"\n📁 输出路径: {output_file}")

    # 3. 调用 Gemini 2.5 Flash Image API
    print("\n⏳ 正在调用 Gemini 2.5 Flash Image API...")

    try:
        from google import genai
        from PIL import Image
        from io import BytesIO

        client = genai.Client(
            api_key=os.environ.get('GEMINI_API_KEY')
        )

        # 生成图像
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=prompt
        )

        # 4. 处理响应并保存图像
        image_saved = False
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image = Image.open(BytesIO(part.inline_data.data))

                # 保存主图像
                image.save(output_file, format='PNG', dpi=(300, 300))
                image_saved = True

                # 保存元数据
                metadata = {
                    **plan['metadata'],
                    'generation_timestamp': datetime.now().isoformat(),
                    'image_size': image.size,
                    'model': 'gemini-2.5-flash-image',
                    'prompt': prompt,
                    'output_file': str(output_file)
                }

                metadata_file = output_dir / f"{output_file.stem}_metadata.json"
                with open(metadata_file, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, ensure_ascii=False, indent=2)

                print(f"\n✅ 海报生成成功!")
                print(f"   📷 图像尺寸: {image.size[0]} x {image.size[1]} 像素")
                print(f"   💾 文件大小: {output_file.stat().st_size / 1024:.2f} KB")
                print(f"   📝 元数据: {metadata_file.name}")

                break

        if not image_saved:
            print("\n❌ 未能从响应中提取图像数据")
            return False

        # 5. 生成缩略图预览
        thumbnail_file = output_dir / f"{output_file.stem}_thumbnail.png"
        image.thumbnail((400, 600))
        image.save(thumbnail_file, format='PNG')
        print(f"   🖼️  缩略图: {thumbnail_file.name}")

        print("\n" + "=" * 80)
        print("🎉 任务完成!")
        print("=" * 80)

        return True

    except ImportError:
        print("\n⚠️  警告: 未安装 google-genai 库")
        print("   请运行: pip install google-genai pillow")
        return False

    except Exception as e:
        print(f"\n❌ 生成失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = generate_poster()
    exit(0 if success else 1)
