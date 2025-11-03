---
name: html-to-ppt
description: Complete HTML-to-PPT workflow including content analysis, HTML slide design (1920x1080), screenshot capture, PPT assembly, and quality verification. Use for presentation generation, marketing proposals, design mockups, and visual reports.
---

# HTML-to-PPT Skill

完整的HTML到PPT转换流程型技能包,从内容分析、HTML设计、截图到PPT组装的端到端解决方案。

## Quick Start

### 基础使用

```python
# 1. 分析内容需求
content = """
需要制作一份云南过桥米线营销方案PPT,包含:
- 封面页
- 目录页
- 品牌分析
- 创意策略
- 执行方案
- 预算ROI
- 风险控制
"""

# 2. 生成HTML幻灯片
slides_data = [
    {
        "title": "云南过桥米线<br>品牌营销策划方案",
        "content": '<p style="font-size:48px;">"一碗过桥,三餐云南"</p>',
        "bg_type": "gradient"  # 封面使用渐变背景
    },
    {
        "title": "目录",
        "content": """
            <ul>
                <li>01. 项目概览</li>
                <li>02. 品牌分析</li>
                <li>03. 创意策略</li>
                ...
            </ul>
        """,
        "bg_type": "card"  # 内容页使用卡片背景
    }
]

# 3. 生成HTML文件
for i, slide in enumerate(slides_data, 1):
    html = create_html_slide(i, slide['title'], slide['content'], slide['bg_type'])
    Path(f"html_slides/slide_{i:02d}.html").write_text(html, encoding='utf-8')

# 4. 使用screenshots skill截图
await page.set_viewport_size(width=1920, height=1080)
for i in range(1, len(slides_data) + 1):
    file_url = f"file:///{Path(f'html_slides/slide_{i:02d}.html').absolute()}"
    await page.navigate(url=file_url, wait_until="load")
    await page.wait_for_timeout(1500)
    await page.screenshot(path=f"screenshots/slide_{i:02d}.png", fullPage=True)

# 5. 组装PPT
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(5.625)

for i in range(1, len(slides_data) + 1):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.shapes.add_picture(
        f"screenshots/slide_{i:02d}.png",
        0, 0, Inches(10), Inches(5.625)
    )

prs.save("output.pptx")
```

## Workflow Overview

```
Phase 1: 内容分析
  ↓
Phase 2: HTML设计
  ↓
Phase 3: 截图捕获
  ↓
Phase 4: PPT组装
  ↓
Phase 5: 质量验证
  ↓
Phase 6: 返工优化 (如需要)
```

## Phase 1: 内容分析 (Content Analysis)

### 目标
理解用户需求,提取关键信息,规划幻灯片结构。

### 分析维度

```python
def analyze_content_requirements(user_input: str) -> Dict:
    """
    分析内容需求

    Returns:
        {
            "theme": str,           # 主题
            "purpose": str,         # 目的
            "target_audience": str, # 目标受众
            "key_messages": list,   # 核心信息
            "slide_count": int,     # 预计页数
            "design_style": str,    # 设计风格
            "color_scheme": dict    # 配色方案
        }
    """
```

### 示例分析

**用户输入**:
```
制作云南过桥米线营销方案PPT
```

**分析结果**:
```python
{
    "theme": "云南过桥米线品牌营销策划",
    "purpose": "营销策划提案",
    "target_audience": "客户决策层、营销团队",
    "key_messages": [
        "项目概览与核心理念",
        "品牌分析与市场洞察",
        "创意策略与视觉展示",
        "执行方案与传播渠道",
        "预算投入与ROI预期",
        "风险控制与应对策略"
    ],
    "slide_count": 7,
    "design_style": "现代简约,专业商务",
    "color_scheme": {
        "primary": "#FF6B35",    # 橙色 (热情,食欲)
        "secondary": "#004E89",  # 深蓝 (专业,信任)
        "accent": "#FFD23F",     # 金黄 (高端,品质)
        "background": "#F7F7F7"  # 浅灰 (简洁,现代)
    }
}
```

### 幻灯片结构规划

```python
slide_structure = [
    {"type": "cover", "title": "封面页", "content": "标题+副标题+日期"},
    {"type": "toc", "title": "目录", "content": "6个章节导航"},
    {"type": "content", "title": "01. 项目概览", "content": "主题+核心理念"},
    {"type": "content", "title": "02. 品牌分析", "content": "目标客群+市场洞察"},
    {"type": "content", "title": "03. 创意策略", "content": "核心创意+视觉展示"},
    {"type": "content", "title": "04. 执行方案", "content": "线上线下渠道"},
    {"type": "content", "title": "05. 预算与ROI", "content": "投入产出预期"},
    {"type": "content", "title": "06. 风险控制", "content": "保障措施"},
]
```

## Phase 2: HTML设计 (HTML Design)

### 标准尺寸规范

```python
# 固定尺寸标准
SLIDE_WIDTH = 1920  # px
SLIDE_HEIGHT = 1080  # px

# PPT尺寸 (16:9)
PPT_WIDTH = Inches(10)      # 10英寸
PPT_HEIGHT = Inches(5.625)  # 5.625英寸
```

### HTML模板结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1920, height=1080">
    <title>Slide {slide_num}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            width: 1920px;
            height: 1080px;
            font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            background: {background};
        }

        .slide-container {
            width: 100%;
            height: 100%;
            padding: 80px;
            display: flex;
            flex-direction: column;
        }

        h1 {
            font-size: 64px;
            font-weight: 700;
            color: #FFFFFF;
            text-align: center;
            margin-bottom: 50px;
            text-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }

        .content {
            background: #FFFFFF;
            border-radius: 24px;
            padding: 50px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            flex: 1;
            overflow-y: auto;
        }
    </style>
</head>
<body>
    <div class="slide-container">
        <h1>{title}</h1>
        <div class="content">
            {content}
        </div>
    </div>
</body>
</html>
```

### 背景类型

#### 1. Gradient渐变背景 (封面页)

```python
bg_gradient = "linear-gradient(135deg, #FF6B35 0%, #004E89 100%)"
```

**适用场景**: 封面页、章节分隔页

**特点**:
- 视觉冲击力强
- 现代感强
- 适合放置标题和口号

#### 2. Card卡片背景 (内容页)

```python
bg_card = "#F7F7F7"  # 浅灰背景
# 内容放在白色卡片中: .content { background: #FFFFFF; }
```

**适用场景**: 内容展示页、详细说明页

**特点**:
- 层次分明
- 阅读性好
- 适合放置大段文字和列表

#### 3. Image图片背景 (特殊页)

```python
bg_image = f"url('images/background.jpg')"
```

**适用场景**: 产品展示页、场景演示页

**特点**:
- 沉浸感强
- 视觉丰富
- 需要注意文字可读性

### 内容排版规范

```python
# 标题层级
h1: 64px   # 页面主标题
h2: 40px   # 章节标题
h3: 32px   # 小节标题

# 正文内容
p: 28px    # 段落文字
li: 28px   # 列表项

# 行高
line-height: 1.6

# 间距
margin-bottom: 20px (段落间距)
margin-bottom: 30px (章节间距)
```

### 设计最佳实践

```python
# ✓ 推荐: 内容控制在可视高度内
.content {
    max-height: 850px;  # 确保内容不溢出1080px
    overflow-y: auto;   # 如果超出显示滚动条
}

# ✓ 推荐: 使用足够的padding
.slide-container {
    padding: 80px;  # 上下左右留白
}

# ✓ 推荐: 渐进式信息呈现
- 封面页: 极简,仅标题+副标题
- 目录页: 清晰列表
- 内容页: 分层次展示

# ✗ 避免: 内容过多导致溢出
# ✗ 避免: 字号过小难以阅读
# ✗ 避免: 颜色对比度不足
```

## Phase 3: 截图捕获 (Screenshot Capture)

### 使用screenshots skill

```python
from pathlib import Path

# 1. 准备输出目录
screenshot_dir = Path("screenshots")
screenshot_dir.mkdir(exist_ok=True)

# 2. 获取HTML文件列表
html_files = sorted(Path("html_slides").glob("slide_*.html"))

# 3. 设置浏览器视口
await page.set_viewport_size(width=1920, height=1080)

# 4. 批量截图
for html_file in html_files:
    slide_num = html_file.stem.split('_')[1]

    # 导航到HTML文件
    file_url = f"file:///{html_file.absolute()}"
    await page.navigate(url=file_url, wait_until="load")

    # 等待页面完全渲染
    await page.wait_for_timeout(1500)

    # 全页截图
    output_file = screenshot_dir / f"slide_{slide_num}.png"
    await page.screenshot(
        path=str(output_file),
        fullPage=True
    )

    print(f"✓ {output_file.name}")
```

### 截图参数配置

```python
screenshot_config = {
    "fullPage": True,           # 捕获完整页面高度
    "wait_time": 1500,          # 等待渲染时间(ms)
    "wait_until": "load",       # 等待策略
    "viewport": {
        "width": 1920,
        "height": 1080
    }
}
```

### 质量检查

```python
from PIL import Image

def verify_screenshot(screenshot_path: Path) -> Dict:
    """验证截图质量"""
    img = Image.open(screenshot_path)
    width, height = img.size

    errors = []

    # 检查宽度
    if width != 1920:
        errors.append(f"Width {width} != 1920")

    # 检查高度 (应该>=1080或等于1080)
    if height < 1080:
        errors.append(f"Height {height} < 1080, may be incomplete")

    return {
        "path": str(screenshot_path),
        "width": width,
        "height": height,
        "valid": len(errors) == 0,
        "errors": errors
    }

# 验证所有截图
for screenshot in screenshot_dir.glob("slide_*.png"):
    result = verify_screenshot(screenshot)
    if not result['valid']:
        print(f"✗ {screenshot.name}: {result['errors']}")
    else:
        print(f"✓ {screenshot.name}: {result['width']}x{result['height']}")
```

## Phase 4: PPT组装 (PPT Assembly)

### 使用python-pptx

```python
from pptx import Presentation
from pptx.util import Inches

def create_ppt_from_screenshots(
    screenshot_dir: Path,
    output_ppt: Path,
    pattern: str = "slide_*.png"
) -> None:
    """
    将截图组装成PPT

    Args:
        screenshot_dir: 截图目录
        output_ppt: 输出PPT路径
        pattern: 文件匹配模式
    """
    # 获取所有截图
    screenshots = sorted(screenshot_dir.glob(pattern))

    if not screenshots:
        raise ValueError(f"No screenshots found in {screenshot_dir}")

    print(f"📸 找到 {len(screenshots)} 张截图\n")

    # 创建PPT
    prs = Presentation()

    # 设置幻灯片尺寸 (16:9)
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)

    # 获取空白版式
    blank_slide_layout = prs.slide_layouts[6]

    # 添加每张截图为一页幻灯片
    for screenshot in screenshots:
        print(f"  ➕ 添加: {screenshot.name}")

        # 创建新幻灯片
        slide = prs.slides.add_slide(blank_slide_layout)

        # 添加图片,填满整个幻灯片
        slide.shapes.add_picture(
            str(screenshot),
            left=0,
            top=0,
            width=Inches(10),
            height=Inches(5.625)
        )

    # 保存PPT
    prs.save(str(output_ppt))

    print(f"\n✅ PPT已生成: {output_ppt}")
    print(f"📊 共 {len(screenshots)} 页\n")

# 使用示例
create_ppt_from_screenshots(
    screenshot_dir=Path("screenshots"),
    output_ppt=Path("云南过桥米线营销方案_截图版.pptx")
)
```

### PPT尺寸标准

```python
# 16:9 宽屏 (推荐)
prs.slide_width = Inches(10)
prs.slide_height = Inches(5.625)

# 4:3 传统
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)

# A4 纵向
prs.slide_width = Inches(8.27)
prs.slide_height = Inches(11.69)
```

### 图片适配策略

```python
# 策略1: 填满整个幻灯片 (推荐,无黑边)
slide.shapes.add_picture(
    str(screenshot),
    left=0,
    top=0,
    width=prs.slide_width,
    height=prs.slide_height
)

# 策略2: 保持宽高比 (可能有黑边)
from pptx.util import Inches
from PIL import Image

img = Image.open(screenshot)
img_width, img_height = img.size
aspect_ratio = img_width / img_height

slide_aspect = prs.slide_width / prs.slide_height

if aspect_ratio > slide_aspect:
    # 图片更宽,按宽度适配
    width = prs.slide_width
    height = width / aspect_ratio
    top = (prs.slide_height - height) / 2
    left = 0
else:
    # 图片更高,按高度适配
    height = prs.slide_height
    width = height * aspect_ratio
    left = (prs.slide_width - width) / 2
    top = 0

slide.shapes.add_picture(str(screenshot), left, top, width, height)
```

## Phase 5: 质量验证 (Quality Verification)

### 验证清单

```python
quality_checklist = {
    "screenshots": {
        "count": "所有幻灯片都已截图",
        "size": "尺寸为1920xN (N>=1080)",
        "completeness": "内容无截断或溢出",
        "clarity": "文字清晰可读"
    },
    "ppt": {
        "page_count": "页数与截图数量一致",
        "aspect_ratio": "16:9宽屏格式",
        "image_quality": "图片无失真或模糊",
        "file_size": "文件大小合理 (<50MB)"
    },
    "content": {
        "text_readable": "字号足够大,易读",
        "color_contrast": "颜色对比度足够",
        "layout_balanced": "版式平衡,美观",
        "branding_consistent": "品牌元素一致"
    }
}
```

### 自动化验证脚本

```python
def verify_ppt_quality(
    screenshot_dir: Path,
    ppt_path: Path
) -> Dict[str, any]:
    """
    验证PPT质量

    Returns:
        {
            "valid": bool,
            "errors": list,
            "warnings": list,
            "stats": dict
        }
    """
    errors = []
    warnings = []
    stats = {}

    # 1. 验证截图
    screenshots = list(screenshot_dir.glob("slide_*.png"))
    stats['screenshot_count'] = len(screenshots)

    if len(screenshots) == 0:
        errors.append("No screenshots found")

    for screenshot in screenshots:
        img = Image.open(screenshot)
        width, height = img.size

        if width != 1920:
            errors.append(f"{screenshot.name}: Width {width} != 1920")

        if height < 1080:
            warnings.append(f"{screenshot.name}: Height {height} < 1080")

    # 2. 验证PPT
    if not ppt_path.exists():
        errors.append("PPT file not found")
    else:
        prs = Presentation(str(ppt_path))
        stats['ppt_slide_count'] = len(prs.slides)

        if len(prs.slides) != len(screenshots):
            errors.append(
                f"PPT slides ({len(prs.slides)}) != "
                f"screenshots ({len(screenshots)})"
            )

        # 验证幻灯片尺寸
        expected_width = Inches(10)
        expected_height = Inches(5.625)

        if prs.slide_width != expected_width:
            warnings.append(f"Slide width {prs.slide_width} != {expected_width}")

        if prs.slide_height != expected_height:
            warnings.append(f"Slide height {prs.slide_height} != {expected_height}")

        # 验证文件大小
        file_size_mb = ppt_path.stat().st_size / (1024 * 1024)
        stats['file_size_mb'] = round(file_size_mb, 2)

        if file_size_mb > 50:
            warnings.append(f"File size {file_size_mb:.2f}MB > 50MB")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "stats": stats
    }

# 使用示例
result = verify_ppt_quality(
    screenshot_dir=Path("screenshots"),
    ppt_path=Path("output.pptx")
)

if result['valid']:
    print("✅ 质量验证通过")
else:
    print("✗ 质量验证失败")
    for error in result['errors']:
        print(f"  - {error}")
```

## Phase 6: 返工优化 (Rework & Optimization)

### 常见问题与解决方案

#### 问题1: 截图内容不完整

**症状**: 截图高度<1080px或内容被截断

**诊断**:
```python
img = Image.open("slide_01.png")
if img.size[1] < 1080:
    print("Screenshot height insufficient")
```

**解决方案**:
```python
# 1. 增加等待时间
await page.wait_for_timeout(2000)  # 从1500增加到2000

# 2. 检查HTML内容高度
# 在HTML中添加:
.content {
    max-height: 850px;
    overflow-y: auto;
}

# 3. 减少内容量
# 拆分为多页或简化内容

# 4. 使用更小字号
h2 { font-size: 36px; }  # 从40px减小到36px
```

#### 问题2: 文字模糊或不清晰

**症状**: PPT中文字难以阅读

**诊断**:
```python
# 检查截图DPI
from PIL import Image
img = Image.open("slide_01.png")
dpi = img.info.get('dpi', (72, 72))
print(f"DPI: {dpi}")
```

**解决方案**:
```python
# 1. 确保截图为PNG格式 (无损)
await page.screenshot(path="output.png", type="png")

# 2. 使用更大字号
h1 { font-size: 72px; }  # 从64px增大到72px

# 3. 增加文字阴影增强对比度
h1 {
    text-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

# 4. 使用更清晰的字体
font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
```

#### 问题3: PPT文件过大

**症状**: 文件大小>50MB

**诊断**:
```python
ppt_size = Path("output.pptx").stat().st_size / (1024 * 1024)
print(f"PPT size: {ppt_size:.2f}MB")
```

**解决方案**:
```python
# 1. 压缩截图
from PIL import Image

img = Image.open("slide_01.png")
img = img.convert('RGB')
img.save("slide_01_compressed.jpg", 'JPEG', quality=85)

# 2. 使用JPEG格式 (仅适用于照片类内容)
await page.screenshot(path="output.jpg", type="jpeg", quality=90)

# 3. 减少截图尺寸 (不推荐,会降低清晰度)
# 只在必要时使用
```

#### 问题4: 颜色显示不准确

**症状**: 截图颜色与HTML设计不一致

**诊断**:
```python
# 对比HTML颜色与截图颜色
# 使用取色器工具验证
```

**解决方案**:
```python
# 1. 确保使用标准颜色空间
# 在CSS中使用HEX或RGB标准格式
color: #FF6B35;  # ✓
color: rgb(255, 107, 53);  # ✓

# 2. 避免使用渐变色过渡过度
# 保持渐变简洁

# 3. 使用playwright-mcp的默认颜色配置
# 不要自定义颜色配置文件
```

### 迭代优化流程

```python
def iterative_optimization(max_iterations: int = 3):
    """迭代优化流程"""

    for iteration in range(1, max_iterations + 1):
        print(f"\n=== 第 {iteration} 轮优化 ===\n")

        # 1. 生成/重新生成HTML
        generate_html_slides()

        # 2. 截图
        capture_screenshots()

        # 3. 验证质量
        result = verify_ppt_quality(
            screenshot_dir=Path("screenshots"),
            ppt_path=Path("output.pptx")
        )

        # 4. 检查是否通过
        if result['valid'] and len(result['warnings']) == 0:
            print("✅ 质量验证通过,优化完成")
            break

        # 5. 分析问题
        print("⚠️  发现问题:")
        for error in result['errors']:
            print(f"  - {error}")
        for warning in result['warnings']:
            print(f"  - {warning}")

        # 6. 应用修复
        if "incomplete" in str(result['errors']):
            # 内容不完整 -> 增加等待时间
            config['wait_time'] += 500

        if "text_small" in str(result['warnings']):
            # 文字过小 -> 增大字号
            adjust_font_sizes(scale=1.1)

        print(f"  已应用修复,准备重新生成...\n")
    else:
        print("⚠️  已达到最大迭代次数")
```

## Complete Example

### 完整工作流示例

```python
#!/usr/bin/env python3
"""
HTML-to-PPT完整工作流示例
"""

import asyncio
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches
from PIL import Image


# ===== Phase 1: 内容分析 =====

user_request = """
制作云南过桥米线营销方案PPT,包含:
- 封面页
- 目录
- 项目概览
- 品牌分析
- 创意策略
- 执行方案
- 预算ROI
- 风险控制
"""

slides_data = [
    {
        "title": "云南过桥米线<br>品牌营销策划方案",
        "content": '<p style="font-size:48px; text-align:center; color:#FFFFFF;">"一碗过桥,三餐云南"</p><p style="font-size:32px; text-align:center; color:#FFFFFF; margin-top:30px;">2025年10月</p>',
        "bg_type": "gradient"
    },
    {
        "title": "目录",
        "content": """
            <ul style="font-size:32px; line-height:2;">
                <li>01. 项目概览 – 营销主题与核心理念</li>
                <li>02. 品牌分析 – 目标客群与市场洞察</li>
                <li>03. 创意策略 – 三大核心创意与视觉展示</li>
                <li>04. 执行方案 – 线上线下整合传播</li>
                <li>05. 预算与ROI – 投入产出预期</li>
                <li>06. 风险控制 – 保障措施与应对策略</li>
            </ul>
        """,
        "bg_type": "card"
    },
    # ... 其他幻灯片数据
]


# ===== Phase 2: HTML设计 =====

def create_html_slide(slide_num: int, title: str, content: str, bg_type: str = "card") -> str:
    """生成HTML幻灯片"""

    if bg_type == "gradient":
        background = "linear-gradient(135deg, #FF6B35 0%, #004E89 100%)"
        content_wrapper = content  # 封面不需要白色卡片
    else:
        background = "#F7F7F7"
        content_wrapper = f'<div class="content">{content}</div>'

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1920, height=1080">
    <title>Slide {slide_num}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            width: 1920px;
            height: 1080px;
            font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            background: {background};
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

        .content h2 {{ font-size: 40px; color: #FF6B35; margin-bottom: 30px; }}
        .content h3 {{ font-size: 32px; color: #004E89; margin-bottom: 20px; }}
        .content p {{ font-size: 28px; line-height: 1.6; margin-bottom: 20px; }}
        .content li {{ font-size: 28px; line-height: 1.8; margin-bottom: 15px; }}
        .content ul {{ padding-left: 40px; }}
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


# 生成HTML文件
html_dir = Path("html_slides")
html_dir.mkdir(exist_ok=True)

for i, slide in enumerate(slides_data, 1):
    html = create_html_slide(i, slide['title'], slide['content'], slide['bg_type'])
    (html_dir / f"slide_{i:02d}.html").write_text(html, encoding='utf-8')

print(f"✅ 生成 {len(slides_data)} 个HTML文件\n")


# ===== Phase 3: 截图捕获 =====

async def capture_screenshots():
    """使用playwright-mcp截图"""

    screenshot_dir = Path("screenshots")
    screenshot_dir.mkdir(exist_ok=True)

    html_files = sorted(html_dir.glob("slide_*.html"))

    # 使用playwright-mcp工具
    await page.set_viewport_size(width=1920, height=1080)

    for html_file in html_files:
        slide_num = html_file.stem.split('_')[1]

        file_url = f"file:///{html_file.absolute()}"
        await page.navigate(url=file_url, wait_until="load")
        await page.wait_for_timeout(1500)

        output_file = screenshot_dir / f"slide_{slide_num}.png"
        await page.screenshot(
            path=str(output_file),
            fullPage=True
        )

        print(f"✓ {output_file.name}")

    print(f"\n✅ 截图完成: {len(html_files)} 张\n")


# ===== Phase 4: PPT组装 =====

def create_ppt_from_screenshots():
    """将截图组装成PPT"""

    screenshot_dir = Path("screenshots")
    screenshots = sorted(screenshot_dir.glob("slide_*.png"))

    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)

    blank_layout = prs.slide_layouts[6]

    for screenshot in screenshots:
        slide = prs.slides.add_slide(blank_layout)
        slide.shapes.add_picture(
            str(screenshot),
            left=0,
            top=0,
            width=Inches(10),
            height=Inches(5.625)
        )
        print(f"➕ {screenshot.name}")

    output_ppt = Path("云南过桥米线营销方案_截图版.pptx")
    prs.save(str(output_ppt))

    print(f"\n✅ PPT已生成: {output_ppt}")
    print(f"📊 共 {len(screenshots)} 页\n")


# ===== Phase 5: 质量验证 =====

def verify_quality():
    """验证质量"""

    screenshot_dir = Path("screenshots")
    screenshots = list(screenshot_dir.glob("slide_*.png"))

    errors = []

    for screenshot in screenshots:
        img = Image.open(screenshot)
        width, height = img.size

        if width != 1920:
            errors.append(f"{screenshot.name}: Width {width} != 1920")

        if height < 1080:
            errors.append(f"{screenshot.name}: Height {height} < 1080")

    if errors:
        print("✗ 质量验证失败:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✅ 质量验证通过")
        return True


# ===== 执行完整流程 =====

async def main():
    print("🚀 开始HTML-to-PPT工作流\n")

    # Phase 3: 截图
    await capture_screenshots()

    # Phase 4: 组装PPT
    create_ppt_from_screenshots()

    # Phase 5: 验证
    if verify_quality():
        print("\n🎉 工作流完成!")
    else:
        print("\n⚠️  需要返工优化")


if __name__ == "__main__":
    asyncio.run(main())
```

## Tips & Best Practices

1. **内容规划优先**: 先分析内容结构,再设计HTML
2. **视觉一致性**: 所有幻灯片使用统一的设计系统
3. **可读性第一**: 字号足够大,颜色对比度足够
4. **测试迭代**: 先生成1-2页测试,验证通过再批量生成
5. **质量保证**: 每个阶段都进行质量验证
6. **版本管理**: 保存中间产物(HTML, 截图)便于调试
7. **性能优化**: 重用浏览器实例,避免重复启动
8. **错误处理**: 捕获异常,提供清晰的错误信息

## Integration with Other Skills

### 与screenshots skill集成

```python
# html-to-ppt使用screenshots skill进行截图
from skills.screenshots import capture_screenshot

await capture_screenshot(
    page=page,
    url=file_url,
    output_path="screenshot.png",
    fullPage=True,
    wait_time=1500
)
```

### 与AIGC skills集成

```python
# 生成封面背景图
from skills.aigc.text_to_image import generate_image

cover_image = await generate_image(
    prompt="云南过桥米线,美食摄影,专业商业海报",
    style="food-photography"
)

# 在HTML中使用
background = f"url('{cover_image}')"
```

## Version History

- **v1.0.0** (2025-10-21): 初始版本
  - 完整的6阶段工作流
  - HTML设计模板
  - screenshots skill集成
  - 质量验证系统
  - 返工优化机制
