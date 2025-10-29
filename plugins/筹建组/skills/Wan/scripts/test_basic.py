#!/usr/bin/env python3
"""
通义万相基础测试 - 验证wanx-v1模型
"""

import os
import sys
from pathlib import Path

# 加载.env文件
def load_env():
    """从.env文件加载环境变量"""
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
if not api_key:
    print("❌ 错误: 未找到DASHSCOPE_API_KEY")
    sys.exit(1)

import dashscope
from http import HTTPStatus

dashscope.api_key = api_key

print("\n" + "="*60)
print("🧪 通义万相基础API测试")
print("="*60)
print(f"\n✅ API Key: {api_key[:20]}...")

# 测试1: 最基础的调用
print("\n📝 测试1: 最基础的文生图（无可选参数）")
print("-"*60)

try:
    response = dashscope.ImageSynthesis.call(
        model='wanx-v1',
        prompt='未来都市夜景',
        n=1
    )

    print(f"✅ API调用成功")
    print(f"📊 状态码: {response.status_code}")
    print(f"📋 响应内容:")
    print(f"   - output: {response.output}")

    if response.status_code == HTTPStatus.OK:
        results = response.output.results
        print(f"\n✅ 生成成功!")
        print(f"   - 图片数量: {len(results)}")
        if len(results) > 0:
            print(f"   - 图片URL: {results[0].url}")
        else:
            print(f"   ⚠️  警告: results列表为空")
    else:
        print(f"❌ 生成失败")
        print(f"   - code: {response.code}")
        print(f"   - message: {response.message}")

except Exception as e:
    print(f"❌ 异常: {str(e)}")
    import traceback
    traceback.print_exc()

# 测试2: 添加size和style参数
print("\n\n📝 测试2: 添加size和style参数")
print("-"*60)

try:
    response = dashscope.ImageSynthesis.call(
        model='wanx-v1',
        prompt='赛博朋克风格的未来都市',
        n=1,
        size='1024*768'
    )

    print(f"✅ API调用成功")
    print(f"📊 状态码: {response.status_code}")

    if response.status_code == HTTPStatus.OK:
        results = response.output.results
        print(f"\n✅ 生成成功!")
        print(f"   - 图片数量: {len(results)}")
        if len(results) > 0:
            print(f"   - 图片URL: {results[0].url}")
        else:
            print(f"   ⚠️  警告: results列表为空")
    else:
        print(f"❌ 生成失败")
        print(f"   - code: {response.code}")
        print(f"   - message: {response.message}")

except Exception as e:
    print(f"❌ 异常: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("测试完成")
print("="*60 + "\n")
