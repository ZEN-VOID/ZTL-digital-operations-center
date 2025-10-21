#!/usr/bin/env python3
"""
使用Playwright对HTML幻灯片进行全页截图,并按1080px高度自动分页
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image

# 路径配置
html_dir = Path(__file__).parent / "html_slides"
screenshot_dir = Path(__file__).parent / "screenshots_paginated"
screenshot_dir.mkdir(exist_ok=True)

PAGE_HEIGHT = 1080  # 每页高度

async def screenshot_and_paginate(page, html_file, output_prefix):
    """
    对单个HTML文件全页截图,然后按高度分页

    Args:
        page: Playwright page对象
        html_file: HTML文件路径
        output_prefix: 输出文件前缀(如 "slide_01")

    Returns:
        生成的截图文件列表
    """
    # 打开HTML文件
    file_url = f"file://{html_file.absolute()}"
    await page.goto(file_url, wait_until="networkidle")
    await page.wait_for_timeout(1000)

    # 全页截图
    temp_screenshot = screenshot_dir / f"{output_prefix}_fullpage_temp.png"
    await page.screenshot(
        path=str(temp_screenshot),
        full_page=True
    )

    # 使用PIL分割图片
    img = Image.open(temp_screenshot)
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
            output_file = screenshot_dir / f"{output_prefix}.png"
        else:
            output_file = screenshot_dir / f"{output_prefix}_page{page_num + 1}.png"

        cropped.save(output_file)
        output_files.append(output_file)
        print(f"    ✓ {output_file.name}")

    # 删除临时文件
    temp_screenshot.unlink()

    return output_files

async def main():
    """批量截图所有HTML幻灯片"""
    # 获取所有HTML文件
    html_files = sorted(html_dir.glob("slide_*.html"))

    if not html_files:
        print("❌ 未找到HTML文件")
        return

    print(f"📸 开始处理 {len(html_files)} 个HTML幻灯片...\n")

    all_screenshots = []

    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=True)

        # 创建页面 (1920px宽度,高度自适应)
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})

        # 批量截图并分页
        for html_file in html_files:
            slide_num = html_file.stem.split('_')[1]  # 提取编号 "01", "02" 等
            output_prefix = f"slide_{slide_num}"

            print(f"📄 处理 {html_file.name}:")
            screenshots = await screenshot_and_paginate(page, html_file, output_prefix)
            all_screenshots.extend(screenshots)
            print()

        # 关闭浏览器
        await browser.close()

    print(f"✅ 所有截图已保存到: {screenshot_dir}")
    print(f"📊 共生成 {len(all_screenshots)} 张截图")
    print(f"\n截图列表:")
    for screenshot in all_screenshots:
        print(f"  - {screenshot.name}")

if __name__ == "__main__":
    asyncio.run(main())
