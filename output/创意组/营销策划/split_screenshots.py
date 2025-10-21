#!/usr/bin/env python3
"""
将fullPage截图按1080px高度自动分页
"""

from pathlib import Path
from PIL import Image

# 路径配置
input_dir = Path(__file__).parent / "screenshots_fullpage"
output_dir = Path(__file__).parent / "screenshots_paginated"
output_dir.mkdir(exist_ok=True)

PAGE_HEIGHT = 1080  # 每页高度

def split_image(image_path, output_prefix):
    """
    将图片按高度分割

    Args:
        image_path: 输入图片路径
        output_prefix: 输出文件前缀(如 "slide_01")

    Returns:
        生成的截图文件列表
    """
    print(f"📄 处理 {image_path.name}:")

    img = Image.open(image_path)
    img_width, img_height = img.size

    print(f"  📐 原始尺寸: {img_width}x{img_height}px")

    # 计算需要分成几页
    num_pages = (img_height + PAGE_HEIGHT - 1) // PAGE_HEIGHT

    print(f"  📄 将分割成 {num_pages} 页")

    output_files = []

    for page_num in range(num_pages):
        # 计算裁剪区域
        top = page_num * PAGE_HEIGHT
        bottom = min((page_num + 1) * PAGE_HEIGHT, img_height)

        # 裁剪
        cropped = img.crop((0, top, img_width, bottom))

        # 如果最后一页高度不足1080px,创建一个1080px高的白色背景
        if bottom - top < PAGE_HEIGHT:
            # 创建白色背景
            background = Image.new('RGB', (img_width, PAGE_HEIGHT), (250, 250, 250))
            # 将裁剪的图片粘贴到顶部
            background.paste(cropped, (0, 0))
            cropped = background

        # 保存
        if num_pages == 1:
            output_file = output_dir / f"{output_prefix}.png"
        else:
            output_file = output_dir / f"{output_prefix}_page{page_num + 1}.png"

        cropped.save(output_file)
        output_files.append(output_file)
        print(f"    ✓ {output_file.name}")

    print()
    return output_files

def main():
    """处理所有截图"""
    # 获取所有PNG文件
    image_files = sorted(input_dir.glob("slide_*.png"))

    if not image_files:
        print("❌ 未找到截图文件")
        print(f"请先将fullPage截图放到: {input_dir}")
        return

    print(f"📸 开始处理 {len(image_files)} 个截图...\n")

    all_screenshots = []

    for image_file in image_files:
        # 提取slide编号
        slide_num = image_file.stem.split('_')[1] if '_' in image_file.stem else image_file.stem
        output_prefix = f"slide_{slide_num}"

        screenshots = split_image(image_file, output_prefix)
        all_screenshots.extend(screenshots)

    print(f"✅ 所有截图已保存到: {output_dir}")
    print(f"📊 共生成 {len(all_screenshots)} 张截图")
    print(f"\n截图列表:")
    for screenshot in all_screenshots:
        print(f"  - {screenshot.name}")

if __name__ == "__main__":
    main()
