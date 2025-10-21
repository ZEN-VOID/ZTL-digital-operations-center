#!/usr/bin/env python3
"""
云南过桥米线营销方案 - HTML幻灯片生成器
生成30页独立HTML页面,用于截图转PPT
"""

import os
from pathlib import Path

# 创建输出目录
output_dir = Path(__file__).parent / "html_slides"
output_dir.mkdir(exist_ok=True)

# HTML模板
def create_html_slide(slide_num, title, content_html, bg_type="card"):
    """
    创建单页HTML幻灯片
    bg_type: "gradient" (渐变背景) 或 "card" (卡片背景)
    """

    # 渐变背景样式
    gradient_bg = """
        background: linear-gradient(135deg, #FF6B35 0%, #004E89 100%);
    """

    # 卡片背景样式
    card_bg = """
        background: #FAFAFA;
    """

    bg_style = gradient_bg if bg_type == "gradient" else card_bg

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
            font-family: 'PingFang SC', 'Microsoft YaHei', Arial, sans-serif;
            {bg_style}
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            padding: 40px;
        }}

        .slide-container {{
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}

        h1 {{
            font-size: 64px;
            font-weight: 700;
            margin-bottom: 40px;
            color: {'#FFFFFF' if bg_type == 'gradient' else '#1A1A1A'};
            text-align: center;
            text-shadow: {'0 4px 8px rgba(0,0,0,0.2)' if bg_type == 'gradient' else 'none'};
        }}

        .content {{
            background: {'rgba(255,255,255,0.95)' if bg_type == 'gradient' else '#FFFFFF'};
            border-radius: 20px;
            padding: 50px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            max-height: 850px;
            overflow-y: auto;
            width: 100%;
            max-width: 1700px;
        }}

        .content h2 {{
            font-size: 40px;
            color: #FF6B35;
            margin-bottom: 24px;
            font-weight: 600;
        }}

        .content h3 {{
            font-size: 32px;
            color: #004E89;
            margin: 24px 0 16px 0;
            font-weight: 600;
        }}

        .content p, .content li {{
            font-size: 28px;
            line-height: 1.6;
            color: #1A1A1A;
            margin-bottom: 16px;
        }}

        .content ul {{
            list-style: none;
            padding-left: 0;
        }}

        .content li {{
            padding-left: 50px;
            position: relative;
            margin-bottom: 24px;
        }}

        .content li:before {{
            content: "●";
            color: #FF6B35;
            font-size: 24px;
            position: absolute;
            left: 0;
            top: 8px;
        }}

        .two-column {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 60px;
        }}

        .column {{
            background: #FFFFFF;
            border-radius: 20px;
            padding: 50px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.1);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 30px;
        }}

        th {{
            background: linear-gradient(135deg, #FF6B35 0%, #004E89 100%);
            color: #FFFFFF;
            padding: 24px;
            font-size: 32px;
            font-weight: 600;
            text-align: center;
        }}

        td {{
            padding: 20px 24px;
            font-size: 28px;
            text-align: center;
            border-bottom: 2px solid #E0E0E0;
        }}

        tr:nth-child(even) td {{
            background: #F5F5F5;
        }}

        .highlight {{
            color: #FF6B35;
            font-weight: 600;
        }}

        .badge {{
            display: inline-block;
            background: #F7B32B;
            color: #1A1A1A;
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 28px;
            font-weight: 600;
            margin: 10px 5px;
        }}
    </style>
</head>
<body>
    <div class="slide-container">
        <h1>{title}</h1>
        {content_html}
    </div>
</body>
</html>"""

    return html


# Slide 1: 封面页 (极简风格,无卡片)
html1 = create_html_slide(
    1,
    "云南过桥米线<br>品牌营销策划方案",
    '<div style="text-align:center;"><p style="font-size:48px; color:#FFFFFF; text-shadow:0 4px 8px rgba(0,0,0,0.3); margin-top: 60px;">"一碗过桥,三餐云南"</p><p style="font-size:32px; color:#FFFFFF; opacity:0.9; margin-top:30px;">2025年10月</p></div>',
    bg_type="gradient"
)

# Slide 2: 目录
html2 = create_html_slide(
    2,
    "目 录",
    """<div class="content">
        <ul>
            <li>01. 项目概览 - 营销主题与核心理念</li>
            <li>02. 品牌分析 - 目标客群与市场洞察</li>
            <li>03. 创意策略 - 三大核心创意与视觉展示</li>
            <li>04. 执行方案 - 线上线下整合传播</li>
            <li>05. 预算与ROI - 投入产出预期</li>
            <li>06. 风险控制 - 保障措施与应对策略</li>
        </ul>
    </div>"""
)

# Slide 3: 项目概览
html3 = create_html_slide(
    3,
    "项目概览",
    """<div class="content">
        <h3>营销主题</h3>
        <p class="highlight">"一碗过桥,三餐云南"</p>

        <h3>核心理念</h3>
        <p>打破"米线=午餐"的认知枷锁，让过桥米线成为早中晚三餐的优质选择</p>

        <h3>执行周期</h3>
        <p>2025年5月-9月 (5个月)</p>

        <h3>预算规模</h3>
        <p>80万元 (线上40万 + 线下30万 + 内容10万)</p>

        <h3>ROI预期</h3>
        <p>短期ROI: 1:3.5 | 长期品牌价值: 持续增长</p>
    </div>"""
)

# Slide 4: 目标客群画像
html4 = create_html_slide(
    4,
    "目标客群画像",
    """<div class="content">
        <div class="two-column">
            <div class="column">
                <h3>核心人群 (65%)</h3>
                <ul>
                    <li><strong>年龄:</strong> 25-35岁白领</li>
                    <li><strong>收入:</strong> 月入8000-20000元</li>
                    <li><strong>特征:</strong> 追求品质生活</li>
                    <li><strong>痛点:</strong> 工作繁忙,用餐时间紧张</li>
                    <li><strong>需求:</strong> 快速+营养+有仪式感</li>
                </ul>
            </div>
            <div class="column">
                <h3>次级人群 (35%)</h3>
                <ul>
                    <li><strong>年龄:</strong> 18-25岁学生</li>
                    <li><strong>收入:</strong> 月生活费2000-5000元</li>
                    <li><strong>特征:</strong> 热爱社交分享</li>
                    <li><strong>痛点:</strong> 预算有限,追求性价比</li>
                    <li><strong>需求:</strong> 好吃+好看+可晒图</li>
                </ul>
            </div>
        </div>
    </div>"""
)

# Slide 5: 核心卖点提炼
html5 = create_html_slide(
    5,
    "核心卖点提炼",
    """<div class="content">
        <div class="two-column">
            <div class="column">
                <h3>产品层卖点</h3>
                <ul>
                    <li><strong>正宗非遗:</strong> 源自云南百年传承工艺</li>
                    <li><strong>仪式感:</strong> "过桥"动作的独特体验</li>
                    <li><strong>营养均衡:</strong> 鲜汤+蛋白+蔬菜全覆盖</li>
                    <li><strong>适配三餐:</strong> 早餐轻食/午餐正餐/晚餐滋补</li>
                </ul>
            </div>
            <div class="column">
                <h3>情感层卖点</h3>
                <ul>
                    <li><strong>文化认同:</strong> 云南美食文化的代表</li>
                    <li><strong>社交货币:</strong> 朋友圈晒图的优质素材</li>
                    <li><strong>治愈属性:</strong> 热汤温暖身心的慰藉</li>
                    <li><strong>探索欲:</strong> "隐藏吃法"的发现乐趣</li>
                </ul>
            </div>
        </div>
    </div>"""
)

# Slide 6: 市场机会洞察
html6 = create_html_slide(
    6,
    "市场机会洞察 - 2025年餐饮营销5大趋势",
    """<div class="content">
        <ul>
            <li><strong>场景化营销:</strong> 从"产品卖点"到"生活场景",打造"早餐唤醒""午餐续航""晚餐治愈"的场景IP</li>
            <li><strong>文化IP化:</strong> 云南非遗文化+过桥仪式感,构建差异化文化护城河</li>
            <li><strong>用户共创:</strong> UGC内容成本降低50%,用户创作的"隐藏吃法"成为核心传播力</li>
            <li><strong>线下体验升级:</strong> 快闪店、音乐节等沉浸式体验,提升品牌记忆点</li>
            <li><strong>全时段消费:</strong> 早午晚三餐覆盖,拓展非传统时段的消费场景</li>
        </ul>
    </div>"""
)

# Slide 7: 竞品定位对比
html7 = create_html_slide(
    7,
    "竞品定位对比分析",
    """<div class="content">
        <table>
            <tr>
                <th>品牌</th>
                <th>定位</th>
                <th>价格带</th>
                <th>核心优势</th>
                <th>核心劣势</th>
            </tr>
            <tr>
                <td>蒙自源</td>
                <td>正宗派</td>
                <td>25-35元</td>
                <td>品牌认知度高</td>
                <td>创新不足</td>
            </tr>
            <tr>
                <td>云海肴</td>
                <td>文化派</td>
                <td>30-45元</td>
                <td>云南菜品类丰富</td>
                <td>聚焦度不够</td>
            </tr>
            <tr>
                <td>四有青年</td>
                <td>年轻派</td>
                <td>20-30元</td>
                <td>社交属性强</td>
                <td>品质感偏弱</td>
            </tr>
            <tr>
                <td><strong>我们</strong></td>
                <td><strong>全时段</strong></td>
                <td><strong>22-38元</strong></td>
                <td><strong>三餐场景创新</strong></td>
                <td><strong>品牌知名度待提升</strong></td>
            </tr>
        </table>
    </div>"""
)

# 继续生成剩余幻灯片...
# 为了节省时间,我先生成前7页,确认效果后再生成剩余23页

# 保存所有HTML文件
slides = [
    (1, html1),
    (2, html2),
    (3, html3),
    (4, html4),
    (5, html5),
    (6, html6),
    (7, html7),
]

for num, html in slides:
    file_path = output_dir / f"slide_{num:02d}.html"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✓ 生成 Slide {num}: {file_path.name}")

print(f"\n✅ 已生成 {len(slides)} 页HTML幻灯片")
print(f"📁 输出目录: {output_dir}")
print(f"\n下一步: 使用chrome-mcp对每页HTML进行截图")
