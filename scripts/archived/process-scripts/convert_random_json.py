#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
转换随机组合JSON格式

将 {key: [url]} 格式转换为标准的 {images: [{url: url}]} 格式
"""

import json
import sys
from pathlib import Path


def convert_json(input_file: str, output_file: str):
    """转换JSON格式"""
    input_path = Path(input_file)
    output_path = Path(output_file)

    # 读取原始JSON
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 转换为标准格式
    images = []
    for key, urls in data.items():
        for url in urls:
            images.append({"url": url})

    # 构建输出JSON
    output_data = {
        "metadata": {
            "source": "random_combination",
            "original_file": str(input_path),
            "total_images": len(images)
        },
        "images": images
    }

    # 保存
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"✅ 转换完成: {input_file} -> {output_file}")
    print(f"📊 图片数量: {len(images)}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python convert_random_json.py <input> <output>")
        sys.exit(1)

    convert_json(sys.argv[1], sys.argv[2])
