#!/usr/bin/env python3
"""
测试不同的size参数格式
"""

import os
from pathlib import Path

# 加载.env
def load_env():
    current_dir = Path(__file__).resolve().parent
    while current_dir != current_dir.parent:
        env_file = current_dir / ".env"
        if env_file.exists():
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
            return os.getenv('DASHSCOPE_API_KEY')
        current_dir = current_dir.parent
    return None

api_key = load_env()
if not api_key:
    print("❌ 错误: 未找到DASHSCOPE_API_KEY")
    exit(1)

import dashscope
from http import HTTPStatus

dashscope.api_key = api_key

test_cases = [
    ("不指定size", {}),
    ("size='1024*768'", {"size": "1024*768"}),
    ("size='1024x768'", {"size": "1024x768"}),
    ("size='1024*1024'", {"size": "1024*1024"}),
    ("size='720*1280'", {"size": "720*1280"}),
    ("size='512*512'", {"size": "512*512"}),
]

print("\n" + "="*60)
print("🧪 测试不同size参数格式")
print("="*60)

for name, params in test_cases:
    print(f"\n📝 测试: {name}")
    print("-"*60)

    try:
        kwargs = {
            'model': 'wanx-v1',
            'prompt': '赛博朋克风格城市',
            'n': 1
        }
        kwargs.update(params)

        response = dashscope.ImageSynthesis.call(**kwargs)

        if response.status_code == HTTPStatus.OK:
            results = response.output.results
            if len(results) > 0:
                print(f"✅ 成功! 生成了 {len(results)} 张图片")
                print(f"   URL: {results[0].url[:80]}...")
            else:
                print(f"⚠️  API返回OK但results为空")
        else:
            print(f"❌ 失败: {response.code} - {response.message}")

    except Exception as e:
        print(f"❌ 异常: {str(e)}")

print("\n" + "="*60)
print("测试完成")
print("="*60 + "\n")
