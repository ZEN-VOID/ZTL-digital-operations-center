#!/usr/bin/env python3
"""
批量截图HTML并组合成图片式PPT
"""

import subprocess
import time
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches

# 配置路径
html_dir = Path(__file__).parent / "html_slides"
playwright_output = Path("/Users/vincentlee/Desktop/ZTL数智化作战中心/.playwright-mcp")
final_ppt = Path(__file__).parent / "云南过桥米线营销方案_截图版.pptx"

print("=" * 60)
print("🎬 云南过桥米线营销方案 - 截图版PPT生成器")
print("=" * 60)
print()

# Step 1: 获取所有HTML文件
html_files = sorted(html_dir.glob("slide_*.html"))
print(f"📄 找到 {len(html_files)} 页HTML幻灯片")
print()

# Step 2: 使用playwright-mcp截图 (需要手动操作,这里提供命令提示)
print("⚠️  由于playwright-mcp是MCP工具,需要在Claude对话中逐个截图")
print("   请手动执行以下命令:")
print()

for html_file in html_files:
    slide_num = html_file.stem.split('_')[1]
    print(f"""
📸 Slide {slide_num}:
   1. browser_navigate: file://{html_file.absolute()}
   2. browser_take_screenshot: filename="slide_{slide_num}.png"
""")

print("=" * 60)
print("⏸️  请先完成截图,然后运行第二个脚本组合PPT")
print("=" * 60)
