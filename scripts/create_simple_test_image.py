#!/usr/bin/env python3
"""
创建简单测试图片 - 用于Z4视频生成测试
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from datetime import datetime

def create_test_image():
    """创建简单的测试图片"""

    print("🎨 创建测试图片...")

    # 创建1280x720的图片(Z4标准分辨率)
    width, height = 1280, 720
    image = Image.new('RGB', (width, height), color=(240, 240, 240))

    # 绘制一些基本元素
    draw = ImageDraw.Draw(image)

    # 绘制背景渐变效果(模拟餐厅空间)
    for y in range(height):
        gray_value = int(240 - (y / height) * 60)
        draw.line([(0, y), (width, y)], fill=(gray_value, gray_value, gray_value + 10))

    # 绘制"桌子"(矩形)
    table_color = (139, 115, 85)  # 原木色
    draw.rectangle([200, 400, 500, 600], fill=table_color, outline=(100, 80, 60), width=3)
    draw.rectangle([600, 400, 900, 600], fill=table_color, outline=(100, 80, 60), width=3)

    # 绘制"灯光"效果(圆形)
    light_color = (255, 248, 220)
    draw.ellipse([400, 100, 500, 200], fill=light_color, outline=(200, 200, 150), width=2)
    draw.ellipse([700, 100, 800, 200], fill=light_color, outline=(200, 200, 150), width=2)

    # 添加文字说明
    try:
        # 尝试使用系统字体
        font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 40)
    except:
        font = None

    text = "现代简约餐厅测试场景"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (width - text_width) // 2
    draw.text((text_x, 30), text, fill=(80, 80, 80), font=font)

    # 保存图片
    output_dir = Path("output/视频生成测试/Z2-空间设计师/results")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_path = output_dir / f"测试餐厅场景-{timestamp}.png"

    image.save(output_path, 'PNG', quality=95)

    print(f"   ✅ 测试图片已创建: {output_path}")
    return str(output_path)

if __name__ == "__main__":
    image_path = create_test_image()
    print(f"\n🎉 测试图片创建成功!")
    print(f"📁 路径: {image_path}")
    print(f"📏 尺寸: 1280x720 (Z4标准输入尺寸)")
    print("\n下一步: 使用此图片进行Z4视频生成")
