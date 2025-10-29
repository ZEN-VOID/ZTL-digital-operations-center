#!/usr/bin/env python3
"""
通义万相文生图测试脚本
测试Text-to-Image和Qwen-Image文本渲染功能
"""

import os
import json
from pathlib import Path
from datetime import datetime
import dashscope
from http import HTTPStatus

# 加载.env文件
def load_env():
    """从.env文件加载环境变量"""
    # 从脚本所在目录向上查找.env文件
    current_dir = Path(__file__).resolve().parent
    while current_dir != current_dir.parent:
        env_file = current_dir / ".env"
        if env_file.exists():
            print(f"📄 找到.env文件: {env_file}")
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
            return os.getenv('DASHSCOPE_API_KEY')
        current_dir = current_dir.parent
    return None

# 加载环境变量
api_key = load_env()
if api_key:
    dashscope.api_key = api_key


def test_text_to_image_with_composer():
    """测试1: Composer精细控制 - 赛博朋克都市夜景"""

    print("\n" + "="*60)
    print("🎨 测试1: Composer精细控制 - 赛博朋克都市夜景")
    print("="*60)

    # 提示词
    prompt = "赛博朋克风格的未来都市夜景，霓虹灯闪烁的高楼大厦，雨后湿滑的街道，飞行汽车穿梭其间，电影级构图，专业摄影质感"
    negative_prompt = "模糊，低质量，扭曲，卡通化，白天"

    print(f"📝 提示词: {prompt}")
    print(f"🚫 负面提示词: {negative_prompt}")
    print(f"🎨 Composer配置:")
    print(f"   - 色彩: 青色(#00F5FF) + 粉红(#FF1493) + 紫色(#9400D3)")
    print(f"   - 布局: rule_of_thirds (三分法)")
    print(f"   - 材质: neon_glass (霓虹玻璃)")
    print(f"   - 语义: futuristic_city (未来都市)")

    try:
        # 调用API
        print("\n🚀 正在生成图片...")

        response = dashscope.ImageSynthesis.call(
            model='wanx-v1',
            prompt=prompt,
            negative_prompt=negative_prompt,
            n=2,
            size='1024*1024',
            style='<auto>',
            parameters={
                'color_palette': ["#00F5FF", "#FF1493", "#9400D3"],
                'layout': 'rule_of_thirds',
                'material': 'neon_glass',
                'semantic': 'futuristic_city'
            }
        )

        # 处理结果
        if response.status_code == HTTPStatus.OK:
            results = response.output.results
            print(f"\n✅ 生成成功!")
            print(f"📊 生成数量: {len(results)}")

            # 保存图片信息
            output_dir = Path("output/images/tongyi-wanxiang")
            output_dir.mkdir(parents=True, exist_ok=True)

            image_urls = []
            for idx, img_result in enumerate(results):
                url = img_result.url
                image_urls.append(url)
                print(f"   🖼️  图片 {idx+1}: {url}")

            # 保存元数据
            metadata = {
                "test_name": "composer_control",
                "timestamp": datetime.now().isoformat(),
                "model": "wanx-v1",
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "parameters": {
                    "size": "1024*1024",
                    "n": 2,
                    "style": "<auto>"
                },
                "composer_config": {
                    "color_palette": ["#00F5FF", "#FF1493", "#9400D3"],
                    "layout": "rule_of_thirds",
                    "material": "neon_glass",
                    "semantic": "futuristic_city"
                },
                "image_urls": image_urls
            }

            metadata_file = output_dir / f"test1_composer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)

            print(f"💾 元数据已保存: {metadata_file}")

            return image_urls

        else:
            print(f"❌ 生成失败: {response.code} - {response.message}")
            return None

    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def test_qwen_image_text_rendering():
    """测试2: 文本渲染测试 - 科幻电影海报"""

    print("\n" + "="*60)
    print("✍️  测试2: 文本渲染测试 - 科幻电影海报")
    print("="*60)

    # 提示词
    prompt = "科幻电影海报，主标题'未来都市2077'使用粗体未来感字体置于顶部，副标题'在霓虹深处寻找真实'使用现代字体置于中央，背景为赛博朋克都市夜景，霓虹灯和雨水营造氛围"
    negative_prompt = "文字模糊，文字不清晰，低质量，扭曲"

    print(f"📝 提示词: {prompt}")
    print(f"🚫 负面提示词: {negative_prompt}")
    print(f"🎯 使用模型: wanx-v1 (通义万相V1)")

    try:
        # 调用API
        print("\n🚀 正在生成海报...")

        response = dashscope.ImageSynthesis.call(
            model='wanx-v1',
            prompt=prompt,
            negative_prompt=negative_prompt,
            n=1,
            size='720*1280',
            style='<auto>',
            prompt_extend=False
        )

        # 处理结果
        if response.status_code == HTTPStatus.OK:
            results = response.output.results
            print(f"\n✅ 生成成功!")

            # 保存图片信息
            output_dir = Path("output/images/tongyi-wanxiang")
            output_dir.mkdir(parents=True, exist_ok=True)

            image_url = results[0].url
            print(f"   🖼️  海报图片: {image_url}")

            # 保存元数据
            metadata = {
                "test_name": "text_rendering_test",
                "timestamp": datetime.now().isoformat(),
                "model": "wanx-v1",
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "parameters": {
                    "size": "720*1280",
                    "n": 1,
                    "style": "<auto>",
                    "prompt_extend": False
                },
                "text_content": {
                    "main_title": "未来都市2077",
                    "subtitle": "在霓虹深处寻找真实"
                },
                "image_url": image_url
            }

            metadata_file = output_dir / f"test2_text_rendering_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)

            print(f"💾 元数据已保存: {metadata_file}")

            return image_url

        else:
            print(f"❌ 生成失败: {response.code} - {response.message}")
            return None

    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """主函数"""

    print("\n" + "🎬 "*20)
    print("   通义万相(Tongyi Wanxiang)文生图能力测试")
    print("🎬 "*20)

    # 检查环境变量
    api_key = os.getenv('DASHSCOPE_API_KEY')
    if not api_key:
        print("\n❌ 错误: 请先设置DASHSCOPE_API_KEY环境变量")
        print("   export DASHSCOPE_API_KEY='your-api-key'")
        return

    print(f"\n✅ API Key已配置: {api_key[:20]}...")

    # 测试1: Composer控制
    composer_result = test_text_to_image_with_composer()

    # 测试2: Qwen-Image文本渲染
    qwen_result = test_qwen_image_text_rendering()

    # 总结
    print("\n" + "="*60)
    print("📊 测试总结")
    print("="*60)

    print(f"\n✅ Composer控制测试: {'成功' if composer_result else '失败'}")
    if composer_result:
        print(f"   - 生成图片数: {len(composer_result)}")
        print(f"   - 特点: 精确色彩控制、三分法构图、霓虹玻璃材质")

    print(f"\n✅ 文本渲染测试: {'成功' if qwen_result else '失败'}")
    if qwen_result:
        print(f"   - 特点: wanx-v1模型、电影海报风格、中文标题渲染")

    print("\n" + "🎬 "*20)
    print("   测试完成!")
    print("🎬 "*20 + "\n")


if __name__ == "__main__":
    main()
