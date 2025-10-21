#!/usr/bin/env python3
"""
HTML幻灯片生成器

提供HTML模板生成、配色方案管理和内容格式化功能。
"""

from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ColorScheme:
    """配色方案"""
    primary: str  # 主色
    secondary: str  # 辅助色
    accent: str  # 强调色
    background: str  # 背景色


# 预定义配色方案
COLOR_SCHEMES = {
    "business": ColorScheme(
        primary="#FF6B35",  # 橙色
        secondary="#004E89",  # 深蓝
        accent="#FFD23F",  # 金黄
        background="#F7F7F7"  # 浅灰
    ),
    "tech": ColorScheme(
        primary="#00D9FF",  # 青色
        secondary="#6366F1",  # 紫色
        accent="#F43F5E",  # 玫红
        background="#0F172A"  # 深灰
    ),
    "nature": ColorScheme(
        primary="#10B981",  # 绿色
        secondary="#059669",  # 深绿
        accent="#FCD34D",  # 黄色
        background="#F0FDF4"  # 浅绿
    ),
    "elegant": ColorScheme(
        primary="#8B5CF6",  # 紫色
        secondary="#EC4899",  # 粉色
        accent="#F59E0B",  # 橙色
        background="#FAF5FF"  # 浅紫
    )
}


def create_html_slide(
    slide_num: int,
    title: str,
    content: str,
    bg_type: str = "card",
    color_scheme: str = "business"
) -> str:
    """
    生成HTML幻灯片

    Args:
        slide_num: 幻灯片编号
        title: 标题
        content: 内容HTML
        bg_type: 背景类型 "gradient"|"card"|"image"
        color_scheme: 配色方案名称

    Returns:
        完整的HTML字符串
    """
    colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["business"])

    # 根据背景类型设置背景样式
    if bg_type == "gradient":
        background = f"linear-gradient(135deg, {colors.primary} 0%, {colors.secondary} 100%)"
        content_wrapper = content  # 渐变背景不需要卡片
    elif bg_type == "image":
        background = f"url('images/bg_{slide_num:02d}.jpg')"
        content_wrapper = f'<div class="content with-image-bg">{content}</div>'
    else:  # card
        background = colors.background
        content_wrapper = f'<div class="content">{content}</div>'

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1920, height=1080">
    <title>Slide {slide_num}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            width: 1920px;
            height: 1080px;
            font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            background: {background};
            background-size: cover;
            background-position: center;
        }}

        .slide-container {{
            width: 100%;
            height: 100%;
            padding: 80px;
            display: flex;
            flex-direction: column;
        }}

        h1 {{
            font-size: 64px;
            font-weight: 700;
            color: #FFFFFF;
            text-align: center;
            margin-bottom: 50px;
            text-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}

        .content {{
            background: #FFFFFF;
            border-radius: 24px;
            padding: 50px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            flex: 1;
            max-height: 850px;
            overflow-y: auto;
        }}

        .content.with-image-bg {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
        }}

        .content h2 {{
            font-size: 40px;
            color: {colors.primary};
            margin-bottom: 30px;
            border-left: 6px solid {colors.primary};
            padding-left: 20px;
        }}

        .content h3 {{
            font-size: 32px;
            color: {colors.secondary};
            margin-bottom: 20px;
            margin-top: 30px;
        }}

        .content p {{
            font-size: 28px;
            line-height: 1.6;
            color: #333333;
            margin-bottom: 20px;
        }}

        .content ul, .content ol {{
            padding-left: 40px;
            margin-bottom: 20px;
        }}

        .content li {{
            font-size: 28px;
            line-height: 1.8;
            color: #333333;
            margin-bottom: 15px;
        }}

        .content li::marker {{
            color: {colors.primary};
            font-weight: bold;
        }}

        .content .highlight {{
            background: {colors.accent};
            color: #FFFFFF;
            padding: 2px 8px;
            border-radius: 4px;
        }}

        .content .quote {{
            border-left: 4px solid {colors.accent};
            padding-left: 20px;
            margin: 30px 0;
            font-style: italic;
            color: #666666;
        }}

        .content .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-top: 30px;
        }}

        .content .card {{
            background: {colors.background};
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid {colors.primary};
        }}
    </style>
</head>
<body>
    <div class="slide-container">
        <h1>{title}</h1>
        {content_wrapper}
    </div>
</body>
</html>"""

    return html


def format_list_content(items: List[str], ordered: bool = False) -> str:
    """
    格式化列表内容

    Args:
        items: 列表项
        ordered: 是否有序列表

    Returns:
        HTML列表字符串
    """
    tag = "ol" if ordered else "ul"
    items_html = "\n".join([f"<li>{item}</li>" for item in items])
    return f"<{tag}>\n{items_html}\n</{tag}>"


def format_two_column_content(left: str, right: str) -> str:
    """
    格式化双栏内容

    Args:
        left: 左栏内容
        right: 右栏内容

    Returns:
        HTML双栏布局字符串
    """
    return f"""
    <div class="grid-2">
        <div class="card">
            {left}
        </div>
        <div class="card">
            {right}
        </div>
    </div>
    """


def format_quote_content(quote: str, author: Optional[str] = None) -> str:
    """
    格式化引用内容

    Args:
        quote: 引用文本
        author: 作者(可选)

    Returns:
        HTML引用字符串
    """
    author_html = f"<br><strong>— {author}</strong>" if author else ""
    return f'<div class="quote">{quote}{author_html}</div>'


def generate_cover_slide(
    title: str,
    subtitle: str,
    date: Optional[str] = None,
    color_scheme: str = "business"
) -> str:
    """
    生成封面页

    Args:
        title: 主标题
        subtitle: 副标题/口号
        date: 日期(可选)
        color_scheme: 配色方案

    Returns:
        封面页HTML
    """
    date_html = f'<p style="font-size:32px; color:#FFFFFF; opacity:0.9; margin-top:30px;">{date}</p>' if date else ""

    content = f"""
    <div style="text-align:center;">
        <p style="font-size:48px; color:#FFFFFF; text-shadow:0 4px 8px rgba(0,0,0,0.3); margin-top: 60px;">
            {subtitle}
        </p>
        {date_html}
    </div>
    """

    return create_html_slide(
        slide_num=1,
        title=title,
        content=content,
        bg_type="gradient",
        color_scheme=color_scheme
    )


def generate_toc_slide(
    chapters: List[str],
    color_scheme: str = "business"
) -> str:
    """
    生成目录页

    Args:
        chapters: 章节列表
        color_scheme: 配色方案

    Returns:
        目录页HTML
    """
    content = format_list_content(chapters, ordered=False)

    return create_html_slide(
        slide_num=2,
        title="目录",
        content=content,
        bg_type="card",
        color_scheme=color_scheme
    )


def generate_content_slide(
    slide_num: int,
    title: str,
    sections: List[Dict[str, str]],
    color_scheme: str = "business"
) -> str:
    """
    生成内容页

    Args:
        slide_num: 幻灯片编号
        title: 标题
        sections: 章节列表,每项包含 {"subtitle": "...", "content": "..."}
        color_scheme: 配色方案

    Returns:
        内容页HTML
    """
    content_html = ""

    for section in sections:
        subtitle = section.get("subtitle", "")
        content = section.get("content", "")

        if subtitle:
            content_html += f"<h2>{subtitle}</h2>\n"

        content_html += f"{content}\n"

    return create_html_slide(
        slide_num=slide_num,
        title=title,
        content=content_html,
        bg_type="card",
        color_scheme=color_scheme
    )


# 使用示例
if __name__ == "__main__":
    output_dir = Path("html_slides")
    output_dir.mkdir(exist_ok=True)

    # 示例1: 封面页
    cover = generate_cover_slide(
        title="云南过桥米线<br>品牌营销策划方案",
        subtitle='"一碗过桥,三餐云南"',
        date="2025年10月",
        color_scheme="business"
    )
    (output_dir / "slide_01.html").write_text(cover, encoding='utf-8')

    # 示例2: 目录页
    toc = generate_toc_slide(
        chapters=[
            "01. 项目概览 – 营销主题与核心理念",
            "02. 品牌分析 – 目标客群与市场洞察",
            "03. 创意策略 – 三大核心创意与视觉展示",
            "04. 执行方案 – 线上线下整合传播",
            "05. 预算与ROI – 投入产出预期",
            "06. 风险控制 – 保障措施与应对策略"
        ],
        color_scheme="business"
    )
    (output_dir / "slide_02.html").write_text(toc, encoding='utf-8')

    # 示例3: 内容页
    content = generate_content_slide(
        slide_num=3,
        title="01. 项目概览",
        sections=[
            {
                "subtitle": "营销主题",
                "content": '<p>"一碗过桥,三餐云南"——让云南味道走进千家万户</p>'
            },
            {
                "subtitle": "核心理念",
                "content": format_list_content([
                    "<strong>传承:</strong> 百年云南味道,世代相传",
                    "<strong>创新:</strong> 现代化呈现,年轻化表达",
                    "<strong>品质:</strong> 精选食材,匠心制作"
                ])
            }
        ],
        color_scheme="business"
    )
    (output_dir / "slide_03.html").write_text(content, encoding='utf-8')

    print(f"✅ 生成3个HTML示例文件到 {output_dir}")
