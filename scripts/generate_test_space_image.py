#!/usr/bin/env python3
"""
快速生成测试空间设计图 - 用于Z4视频生成测试
"""

import requests
import json
import base64
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

def generate_space_image():
    """生成测试空间设计图"""

    # 加载环境变量
    load_dotenv()

    # OpenRouter配置
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("   ❌ 错误: 未找到 OPENROUTER_API_KEY 环境变量")
        return None

    api_url = "https://openrouter.ai/api/v1/chat/completions"

    # 测试提示词 - 现代简约餐厅就餐区
    prompt = """现代简约风格餐厅开放就餐区,原木色实木餐桌整齐排列,白色墙面,浅色木地板,简洁吊灯照明,绿植点缀,明亮通透氛围,45度透视角度,摄影级质量,8K高清,室内设计渲染"""

    print("🎨 生成测试空间设计图...")
    print(f"   提示词: {prompt}")

    # 构建请求
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/dall-e-3",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 1000
    }

    try:
        # 发送请求
        print("   发送API请求...")
        response = requests.post(api_url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()

        result = response.json()

        # 提取图片URL
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"]

            # 查找图片URL
            import re
            url_pattern = r'https://[^\s)]+'
            urls = re.findall(url_pattern, content)

            if urls:
                image_url = urls[0]
                print(f"   ✅ 图片生成成功: {image_url}")

                # 下载图片
                print("   下载图片...")
                img_response = requests.get(image_url)
                img_response.raise_for_status()

                # 保存图片
                output_dir = Path("output/视频生成测试/Z2-空间设计师/results")
                output_dir.mkdir(parents=True, exist_ok=True)

                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                output_path = output_dir / f"空间设计-测试餐厅-{timestamp}.png"

                with open(output_path, 'wb') as f:
                    f.write(img_response.content)

                print(f"   ✅ 图片已保存: {output_path}")
                return str(output_path)
            else:
                print("   ❌ 未找到图片URL")
                print(f"   响应内容: {content}")
                return None
        else:
            print("   ❌ 响应格式错误")
            print(f"   响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return None

    except Exception as e:
        print(f"   ❌ 生成失败: {e}")
        return None

if __name__ == "__main__":
    image_path = generate_space_image()
    if image_path:
        print(f"\n🎉 测试图片生成成功!")
        print(f"📁 路径: {image_path}")
        print("\n下一步可以使用此图片进行Z4视频生成测试")
    else:
        print("\n❌ 测试图片生成失败")
