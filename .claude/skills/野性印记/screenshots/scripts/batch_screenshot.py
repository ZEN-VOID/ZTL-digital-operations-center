#!/usr/bin/env python3
"""
批量截图辅助脚本

提供批量处理HTML文件截图的便捷函数,配合playwright-mcp使用。
"""

from pathlib import Path
from typing import List, Dict, Optional
from PIL import Image


def validate_screenshot(
    screenshot_path: Path,
    expected_width: int = 1920,
    min_height: int = 800
) -> Dict[str, any]:
    """
    验证截图质量

    Args:
        screenshot_path: 截图文件路径
        expected_width: 预期宽度
        min_height: 最小高度

    Returns:
        验证结果字典,包含width, height, valid, errors

    Raises:
        FileNotFoundError: 截图文件不存在
    """
    if not screenshot_path.exists():
        raise FileNotFoundError(f"Screenshot not found: {screenshot_path}")

    img = Image.open(screenshot_path)
    width, height = img.size

    errors = []

    if width != expected_width:
        errors.append(f"Width {width} != expected {expected_width}")

    if height < min_height:
        errors.append(f"Height {height} < minimum {min_height}, may be incomplete")

    return {
        "width": width,
        "height": height,
        "valid": len(errors) == 0,
        "errors": errors,
        "path": str(screenshot_path)
    }


def get_html_files(
    html_dir: Path,
    pattern: str = "slide_*.html"
) -> List[Path]:
    """
    获取HTML文件列表

    Args:
        html_dir: HTML文件目录
        pattern: glob匹配模式

    Returns:
        排序后的HTML文件路径列表
    """
    html_files = sorted(html_dir.glob(pattern))

    if not html_files:
        raise ValueError(f"No HTML files found in {html_dir} with pattern {pattern}")

    return html_files


def prepare_output_dir(output_dir: Path) -> Path:
    """
    准备输出目录

    Args:
        output_dir: 输出目录路径

    Returns:
        创建后的输出目录路径
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def split_screenshot_by_height(
    screenshot_path: Path,
    output_dir: Path,
    page_height: int = 1080,
    background_color: tuple = (250, 250, 250)
) -> List[Path]:
    """
    按高度分割截图

    Args:
        screenshot_path: 原始截图路径
        output_dir: 输出目录
        page_height: 每页高度
        background_color: 背景填充颜色(R,G,B)

    Returns:
        分割后的截图路径列表
    """
    img = Image.open(screenshot_path)
    img_width, img_height = img.size

    # 计算需要分成几页
    num_pages = (img_height + page_height - 1) // page_height

    if num_pages == 1:
        # 无需分割,直接返回原图
        return [screenshot_path]

    output_files = []
    base_name = screenshot_path.stem

    for page_num in range(num_pages):
        # 计算裁剪区域
        top = page_num * page_height
        bottom = min((page_num + 1) * page_height, img_height)

        # 裁剪
        cropped = img.crop((0, top, img_width, bottom))

        # 如果最后一页高度不足,创建背景填充
        if bottom - top < page_height:
            background = Image.new('RGB', (img_width, page_height), background_color)
            background.paste(cropped, (0, 0))
            cropped = background

        # 保存
        output_file = output_dir / f"{base_name}_page{page_num + 1}.png"
        cropped.save(output_file)
        output_files.append(output_file)

    return output_files


def batch_validate_screenshots(
    screenshot_dir: Path,
    pattern: str = "slide_*.png",
    expected_width: int = 1920,
    min_height: int = 800
) -> Dict[str, any]:
    """
    批量验证截图

    Args:
        screenshot_dir: 截图目录
        pattern: glob匹配模式
        expected_width: 预期宽度
        min_height: 最小高度

    Returns:
        验证结果汇总字典
    """
    screenshots = sorted(screenshot_dir.glob(pattern))

    if not screenshots:
        return {
            "total": 0,
            "valid": 0,
            "invalid": 0,
            "results": [],
            "summary": "No screenshots found"
        }

    results = []
    valid_count = 0

    for screenshot in screenshots:
        result = validate_screenshot(screenshot, expected_width, min_height)
        results.append(result)

        if result["valid"]:
            valid_count += 1

    return {
        "total": len(screenshots),
        "valid": valid_count,
        "invalid": len(screenshots) - valid_count,
        "results": results,
        "summary": f"{valid_count}/{len(screenshots)} screenshots valid"
    }


def get_file_url(file_path: Path) -> str:
    """
    将文件路径转换为file:// URL

    Args:
        file_path: 文件路径

    Returns:
        file:// URL字符串
    """
    absolute_path = file_path.absolute()
    return f"file:///{absolute_path}"


def generate_screenshot_report(
    validation_results: Dict[str, any],
    output_file: Optional[Path] = None
) -> str:
    """
    生成截图验证报告

    Args:
        validation_results: 验证结果字典
        output_file: 输出报告文件路径(可选)

    Returns:
        报告文本内容
    """
    report_lines = [
        "# 截图质量验证报告",
        "",
        f"总计: {validation_results['total']} 张",
        f"有效: {validation_results['valid']} 张",
        f"无效: {validation_results['invalid']} 张",
        "",
        "## 详细结果",
        ""
    ]

    for i, result in enumerate(validation_results['results'], 1):
        status = "✓" if result['valid'] else "✗"
        report_lines.append(f"{i}. {status} {Path(result['path']).name}")
        report_lines.append(f"   尺寸: {result['width']}x{result['height']}")

        if result['errors']:
            for error in result['errors']:
                report_lines.append(f"   错误: {error}")

        report_lines.append("")

    report_text = "\n".join(report_lines)

    if output_file:
        output_file.write_text(report_text, encoding='utf-8')

    return report_text


# 使用示例
if __name__ == "__main__":
    # 示例1: 验证截图
    screenshot_dir = Path("screenshots")
    results = batch_validate_screenshots(screenshot_dir)
    print(generate_screenshot_report(results))

    # 示例2: 分割截图
    screenshot = Path("screenshots/slide_01.png")
    output_dir = Path("screenshots_paginated")
    split_files = split_screenshot_by_height(screenshot, output_dir)
    print(f"Split into {len(split_files)} pages")

    # 示例3: 准备HTML文件列表
    html_dir = Path("html_slides")
    html_files = get_html_files(html_dir)
    for html_file in html_files:
        file_url = get_file_url(html_file)
        print(f"{html_file.name} -> {file_url}")
