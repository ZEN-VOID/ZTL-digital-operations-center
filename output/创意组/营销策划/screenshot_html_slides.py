#!/usr/bin/env python3
"""
使用Playwright对HTML幻灯片进行截图
生成高质量PNG图片用于组合成PPT
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

# 路径配置
html_dir = Path(__file__).parent / "html_slides"
screenshot_dir = Path(__file__).parent / "screenshots"
screenshot_dir.mkdir(exist_ok=True)

async def screenshot_slide(page, html_file, output_file):
    """对单个HTML文件截图"""
    # 打开HTML文件
    file_url = f"file://{html_file.absolute()}"
    await page.goto(file_url, wait_until="networkidle")

    # 等待页面完全渲染
    await page.wait_for_timeout(1000)

    # 截图 (1920x1080分辨率)
    await page.screenshot(
        path=str(output_file),
        full_page=False,
        clip={'x': 0, 'y': 0, 'width': 1920, 'height': 1080}
    )

    print(f"✓ 截图完成: {output_file.name}")

async def main():
    """批量截图所有HTML幻灯片"""
    # 获取所有HTML文件
    html_files = sorted(html_dir.glob("slide_*.html"))

    if not html_files:
        print("❌ 未找到HTML文件")
        return

    print(f"📸 开始截图 {len(html_files)} 页HTML幻灯片...\n")

    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=True)

        # 创建页面 (1920x1080分辨率)
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})

        # 批量截图
        for html_file in html_files:
            slide_num = html_file.stem.split('_')[1]  # 提取编号 "01", "02" 等
            output_file = screenshot_dir / f"slide_{slide_num}.png"

            await screenshot_slide(page, html_file, output_file)

        # 关闭浏览器
        await browser.close()

    print(f"\n✅ 所有截图已保存到: {screenshot_dir}")
    print(f"📊 共生成 {len(html_files)} 张截图")

if __name__ == "__main__":
    asyncio.run(main())
