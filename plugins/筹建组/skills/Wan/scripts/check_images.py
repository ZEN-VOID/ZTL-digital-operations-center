#!/usr/bin/env python3
"""检查图片是否有透明通道和尺寸"""

from PIL import Image
import os
from pathlib import Path

# 图片目录
img_dir = Path("output/花间集美妆店双11活动/4-Midjourney主图")

# 获取所有PNG文件
png_files = sorted([f for f in os.listdir(img_dir) if f.endswith('.png')])

print(f"检查 {len(png_files)} 张图片...")
print("=" * 80)

for filename in png_files:
    img_path = img_dir / filename
    img = Image.open(img_path)

    has_alpha = img.mode in ['RGBA', 'LA', 'PA']
    file_size = img_path.stat().st_size / (1024 * 1024)  # MB

    status = "❌ 有透明通道" if has_alpha else "✅ 无透明通道"
    size_status = "✅" if 360 <= img.size[0] <= 2000 and 360 <= img.size[1] <= 2000 else "❌"
    file_size_status = "✅" if file_size <= 10 else "❌"

    print(f"{filename}:")
    print(f"  模式: {img.mode} {status}")
    print(f"  尺寸: {img.size[0]}x{img.size[1]} {size_status}")
    print(f"  大小: {file_size:.2f}MB {file_size_status}")
    print()
