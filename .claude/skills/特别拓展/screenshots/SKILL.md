---
name: screenshots
description: Chrome DevTools screenshot capability for capturing web pages with full page support, viewport configuration, and load waiting. Use for web page screenshots, HTML rendering capture, full-page captures, and quality verification.
---

# Screenshots Skill

专业的网页截图能力包,基于 chrome-devtools-mcp 提供完整的页面截图、视口配置和加载等待功能。

## Quick Start

### 基础截图 (⚠️ 必须 fullPage=True)

```python
# 1. 导航到目标URL并截图
from pathlib import Path

# 导航并等待加载完成
mcp__chrome-devtools__navigate_page(
    url="file:///path/to/file.html",
    timeout=3000  # 3秒超时,确保加载完全
)

# ⚠️ 必须使用 fullPage=True 捕获完整页面
output_path = Path("output/项目名/screenshots/output.png")
output_path.parent.mkdir(parents=True, exist_ok=True)

mcp__chrome-devtools__take_screenshot(
    filePath=str(output_path),
    fullPage=True  # ⚠️ 必须设置为 True
)
```

### 配置视口尺寸 (⚠️ 必须 fullPage=True)

```python
# 2. 指定视口大小进行截图
from pathlib import Path

# 设置视口
mcp__chrome-devtools__resize_page(width=1920, height=1080)

# 导航并等待
mcp__chrome-devtools__navigate_page(
    url="https://example.com",
    timeout=3000  # 确保页面加载完全
)

# ⚠️ 必须使用 fullPage=True
output_path = Path("output/项目名/screenshots/screenshot.png")
output_path.parent.mkdir(parents=True, exist_ok=True)

mcp__chrome-devtools__take_screenshot(
    filePath=str(output_path),
    fullPage=True  # ⚠️ 必须设置为 True,捕获完整高度
)
```

### 批量截图HTML文件 (⚠️ 必须 fullPage=True)

```python
# 3. 批量处理多个HTML文件
from pathlib import Path

html_files = ["slide_01.html", "slide_02.html", "slide_03.html"]
output_dir = Path("output/项目名/screenshots")
output_dir.mkdir(parents=True, exist_ok=True)

for i, html_file in enumerate(html_files):
    file_url = f"file:///{Path(html_file).absolute()}"

    # 导航并等待加载完成
    mcp__chrome-devtools__navigate_page(
        url=file_url,
        timeout=3000  # 3秒超时,确保HTML渲染完全
    )

    output_path = output_dir / f"screenshot_{i+1:02d}.png"

    # ⚠️ 必须使用 fullPage=True
    mcp__chrome-devtools__take_screenshot(
        filePath=str(output_path),
        fullPage=True  # ⚠️ 必须设置为 True
    )
```

## Core Capabilities

### 1. 页面加载控制 (⚠️ 关键:确保加载完全)

**等待策略**:
- `navigate_page(timeout=ms)`: 设置导航超时时间
- Chrome会自动等待DOM加载完成
- **⚠️ 强制要求**: timeout必须≥3000ms,确保动态内容完全渲染

**最佳实践**:
```python
# ⚠️ 对于本地HTML文件 - 最低3秒超时
mcp__chrome-devtools__navigate_page(
    url=file_url,
    timeout=3000  # ⚠️ 最低3秒,确保CSS/JS加载完全
)

# ⚠️ 对于远程网页 - 建议5秒超时
mcp__chrome-devtools__navigate_page(
    url=remote_url,
    timeout=5000  # ⚠️ 5秒超时,确保动态内容渲染
)

# ⚠️ 对于复杂页面 - 可增加到10秒
mcp__chrome-devtools__navigate_page(
    url=complex_url,
    timeout=10000  # 复杂页面需要更长加载时间
)
```

**⚠️ 加载验证检查清单**:
1. ✅ timeout ≥ 3000ms (本地HTML)
2. ✅ timeout ≥ 5000ms (远程网页)
3. ✅ 等待navigate_page完成后再截图
4. ✅ 必须使用fullPage=True

### 2. 截图配置 (⚠️ 强制要求 fullPage=True)

**⚠️ fullPage模式 (强制要求)**:
```python
# ✅ 正确: 必须使用 fullPage=True
mcp__chrome-devtools__take_screenshot(
    filePath="output/项目名/screenshots/fullpage.png",
    fullPage=True  # ⚠️ 强制要求 True,捕获完整页面高度
)
```

**❌ viewport模式 (禁止使用)**:
```python
# ❌ 错误: 禁止使用 fullPage=False
# 这会导致内容被截断,只捕获视口区域
mcp__chrome-devtools__take_screenshot(
    filePath="output/项目名/screenshots/viewport.png",
    fullPage=False  # ❌ 禁止!会导致内容不完整
)
```

**⚠️ 截图配置检查清单**:
1. ✅ fullPage=True (强制要求)
2. ✅ 输出路径: output/[项目名]/screenshots/
3. ✅ 格式: PNG (默认) 或 JPEG/WebP (压缩)
4. ✅ 先navigate_page再take_screenshot

**图片格式**:
```python
# PNG格式 (默认,无损) - ⚠️ 记住 fullPage=True
mcp__chrome-devtools__take_screenshot(
    filePath="output/项目名/screenshots/output.png",
    format="png",
    fullPage=True  # ⚠️ 必须
)

# JPEG格式 (有损压缩,文件更小) - ⚠️ 记住 fullPage=True
mcp__chrome-devtools__take_screenshot(
    filePath="output/项目名/screenshots/output.jpg",
    format="jpeg",
    quality=90,  # 0-100
    fullPage=True  # ⚠️ 必须
)

# WebP格式 (现代格式,高压缩率) - ⚠️ 记住 fullPage=True
mcp__chrome-devtools__take_screenshot(
    filePath="output/项目名/screenshots/output.webp",
    format="webp",
    quality=85,
    fullPage=True  # ⚠️ 必须
)
```

### 3. 视口配置

**标准尺寸**:
```python
# 全高清 (1920x1080)
mcp__chrome-devtools__resize_page(width=1920, height=1080)

# 4K (3840x2160)
mcp__chrome-devtools__resize_page(width=3840, height=2160)

# 移动端 (375x667)
mcp__chrome-devtools__resize_page(width=375, height=667)
```

### 4. 输出路径规范 (简化版)

**⚠️ 标准化路径**: `output/[项目名]/screenshots/`

```python
from pathlib import Path

# ✅ 简化的路径结构(不使用子目录)
project_name = "火锅店开业筹备"
output_dir = Path("output") / project_name / "screenshots"
output_dir.mkdir(parents=True, exist_ok=True)

# 直接保存到screenshots目录
screenshot_path = output_dir / "海报设计_20250130_103000.png"

mcp__chrome-devtools__take_screenshot(
    filePath=str(screenshot_path),
    fullPage=True  # ⚠️ 必须
)
```

**本地HTML文件路径**:
```python
from pathlib import Path

html_path = Path("output/创意组/营销策划/html_slides/slide_01.html")
file_url = f"file:///{html_path.absolute()}"

# 导航并等待加载
mcp__chrome-devtools__navigate_page(
    url=file_url,
    timeout=3000  # ⚠️ 最低3秒
)

# 截图
output_path = Path("output/项目名/screenshots/slide_01.png")
output_path.parent.mkdir(parents=True, exist_ok=True)

mcp__chrome-devtools__take_screenshot(
    filePath=str(output_path),
    fullPage=True  # ⚠️ 必须
)
```

## Usage Patterns

### Pattern 1: 单页面截图工作流 (⚠️ 完整检查清单)

```python
from pathlib import Path

# Step 1: 准备输出路径 (简化版,不使用子目录)
project_name = "火锅店开业筹备"
output_dir = Path("output") / project_name / "screenshots"
output_dir.mkdir(parents=True, exist_ok=True)

# Step 2: 设置视口
mcp__chrome-devtools__resize_page(width=1920, height=1080)

# Step 3: 导航并等待 (⚠️ timeout≥3000ms)
mcp__chrome-devtools__navigate_page(
    url=target_url,
    timeout=3000  # ⚠️ 最低3秒,确保加载完全
)

# Step 4: 全页截图 (⚠️ fullPage=True)
screenshot_path = output_dir / "output.png"
mcp__chrome-devtools__take_screenshot(
    filePath=str(screenshot_path),
    fullPage=True  # ⚠️ 必须True,捕获完整页面
)

# Step 5: 验证截图尺寸
from PIL import Image
img = Image.open(screenshot_path)
print(f"Screenshot size: {img.size}")  # (1920, actual_height)

# ⚠️ 检查清单:
# ✅ timeout ≥ 3000ms
# ✅ fullPage = True
# ✅ 输出路径: output/[项目名]/screenshots/
```

### Pattern 2: HTML演示稿批量截图 (⚠️ 简化版+完整检查)

```python
from pathlib import Path
from datetime import datetime

# 配置 (简化路径,不使用子目录)
project_name = "批量生成餐饮海报"
html_dir = Path("html_slides")
output_dir = Path("output") / project_name / "screenshots"
output_dir.mkdir(parents=True, exist_ok=True)

# 获取所有HTML文件
html_files = sorted(html_dir.glob("slide_*.html"))

# 设置视口
mcp__chrome-devtools__resize_page(width=1920, height=1080)

# 批量截图
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
for i, html_file in enumerate(html_files):
    slide_num = html_file.stem.split('_')[1]

    file_url = f"file:///{html_file.absolute()}"

    # ⚠️ 导航并等待(最低3秒)
    mcp__chrome-devtools__navigate_page(
        url=file_url,
        timeout=3000  # ⚠️ 改为3000ms,确保加载完全
    )

    output_file = output_dir / f"slide_{slide_num}_{timestamp}.png"

    # ⚠️ 全页截图
    mcp__chrome-devtools__take_screenshot(
        filePath=str(output_file),
        fullPage=True  # ⚠️ 必须True
    )

    print(f"✓ {output_file.name}")

print(f"\n✅ 批量截图完成: {len(html_files)} 张")
print(f"📁 输出目录: {output_dir}")

# ⚠️ 检查清单:
# ✅ timeout = 3000ms (本地HTML)
# ✅ fullPage = True (所有截图)
# ✅ 输出路径: output/[项目名]/screenshots/
```

### Pattern 3: 带质量验证的截图 (⚠️ 简化版)

```python
from PIL import Image
from pathlib import Path
from datetime import datetime

def screenshot_with_validation(
    url: str,
    project_name: str,
    output_filename: str,
    expected_width: int = 1920,
    timeout: int = 3000  # ⚠️ 默认3秒
) -> dict:
    """
    截图并验证质量

    ⚠️ 强制要求:
    - timeout ≥ 3000ms
    - fullPage = True
    """

    # 准备输出路径 (简化版,不使用子目录)
    output_dir = Path("output") / project_name / "screenshots"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / output_filename

    # ⚠️ 导航并等待(确保加载完全)
    mcp__chrome-devtools__navigate_page(
        url=url,
        timeout=max(timeout, 3000)  # ⚠️ 最低3秒
    )

    # ⚠️ 全页截图
    mcp__chrome-devtools__take_screenshot(
        filePath=str(output_path),
        fullPage=True  # ⚠️ 必须True
    )

    # 验证截图质量
    img = Image.open(output_path)
    width, height = img.size

    if width != expected_width:
        raise ValueError(f"Screenshot width {width} != expected {expected_width}")

    if height < 800:
        raise ValueError(f"Screenshot height {height} too small, may be incomplete")

    # 打印验证结果
    print(f"✅ {output_filename}: {width}x{height} - SUCCESS")

    return {
        "width": width,
        "height": height,
        "path": str(output_path),
        "size_mb": round(output_path.stat().st_size / (1024 * 1024), 2)
    }
```

## Chrome DevTools MCP Tools Reference

### mcp__chrome-devtools__navigate_page
导航到指定URL

**Parameters**:
- `url` (string, required): 目标URL或file://路径
- `timeout` (number, optional): 导航超时时间(毫秒),默认30000

**Example**:
```python
mcp__chrome-devtools__navigate_page(
    url="file:///Users/path/to/file.html",
    timeout=3000
)
```

### mcp__chrome-devtools__take_screenshot
截取当前页面

**Parameters**:
- `filePath` (string, optional): 输出文件路径(绝对或相对)
- `fullPage` (boolean, optional): 是否全页截图,默认false
- `format` (string, optional): 图片格式 "png"|"jpeg"|"webp",默认"png"
- `quality` (number, optional): 压缩质量0-100(仅JPEG/WebP),默认80

**Example**:
```python
mcp__chrome-devtools__take_screenshot(
    filePath="output/项目名/screenshots/output.png",
    fullPage=True,
    format="png"
)
```

### mcp__chrome-devtools__resize_page
调整页面视口尺寸

**Parameters**:
- `width` (number, required): 视口宽度(像素)
- `height` (number, required): 视口高度(像素)

**Example**:
```python
mcp__chrome-devtools__resize_page(width=1920, height=1080)
```

## Best Practices (⚠️ 强制规范)

### ⚠️ 核心原则 (必须遵守)

1. **fullPage=True**: 所有截图必须使用 fullPage=True
2. **timeout≥3000ms**: 本地HTML最低3秒,远程网页5秒
3. **简化路径**: output/[项目名]/screenshots/ (不使用子目录)
4. **等待加载**: 先navigate_page,等待完成后再take_screenshot

### 1. 输出路径组织 (⚠️ 简化版)

```python
# ✅ 推荐: 简化路径结构
output_path = Path("output/项目名/screenshots/文件名.png")
output_path.parent.mkdir(parents=True, exist_ok=True)

mcp__chrome-devtools__take_screenshot(
    filePath=str(output_path),
    fullPage=True  # ⚠️ 必须
)

# ✗ 错误: 直接输出到当前目录
mcp__chrome-devtools__take_screenshot(filePath="output.png")

# ✗ 错误: 使用子目录(过度复杂)
output_path = Path("output/项目名/screenshots/文件名.png")
```

### 2. 项目名称规范

```python
# ✓ 推荐: 使用语义化项目名
project_name = "火锅店开业筹备"
project_name = "美团餐饮行业调研"
project_name = "批量生成餐饮海报"

# ✗ 不推荐: 使用日期或编号作为项目名
project_name = "20250127任务"
project_name = "task_001"
```

### 3. ⚠️ fullPage=True (强制要求)

```python
# ✅ 正确: 必须使用fullPage=True
mcp__chrome-devtools__take_screenshot(
    filePath="output/项目名/screenshots/output.png",
    fullPage=True  # ⚠️ 强制要求
)

# ❌ 错误: 禁止使用fullPage=False
mcp__chrome-devtools__take_screenshot(
    filePath="output.png",
    fullPage=False  # ❌ 会截断内容!
)

# ❌ 错误: 省略fullPage参数(默认False)
mcp__chrome-devtools__take_screenshot(
    filePath="output.png"  # ❌ 缺少fullPage=True
)
```

### 4. ⚠️ timeout≥3000ms (强制要求)

```python
# ✅ 正确: 本地HTML - 最低3秒
mcp__chrome-devtools__navigate_page(
    url="file:///slide.html",
    timeout=3000  # ⚠️ 最低3000ms
)

# ✅ 正确: 远程网页 - 建议5秒
mcp__chrome-devtools__navigate_page(
    url="https://example.com",
    timeout=5000  # ⚠️ 建议5000ms
)

# ❌ 错误: timeout太短(加载不完全)
mcp__chrome-devtools__navigate_page(
    url="file:///slide.html",
    timeout=1000  # ❌ 太短!至少3000ms
)
```

### 5. 验证截图质量

```python
# ✅ 推荐: 验证尺寸和文件大小
from PIL import Image
img = Image.open("output/项目名/screenshots/output.png")

if img.size[0] != 1920:
    raise ValueError(f"Width {img.size[0]} != 1920")
if img.size[1] < 800:
    raise ValueError(f"Height {img.size[1]} < 800 (可能不完整)")

print(f"✅ {img.size[0]}x{img.size[1]} - 验证通过")
```

## Common Issues (⚠️ 常见错误)

### Issue 1: 截图内容不完整 ⚠️

**原因**: fullPage=False 或 timeout太短

**解决方案**:
```python
# ✅ 解决方案1: 确保fullPage=True
mcp__chrome-devtools__take_screenshot(
    filePath="output/项目名/screenshots/output.png",
    fullPage=True  # ⚠️ 必须True
)

# ✅ 解决方案2: 增加timeout
mcp__chrome-devtools__navigate_page(
    url=target_url,
    timeout=5000  # 从3000ms增加到5000ms
)

# ✅ 解决方案3: 验证截图高度
from PIL import Image
img = Image.open("output/项目名/screenshots/output.png")
if img.size[1] < 800:
    print("⚠️ 警告: 截图高度不足,可能内容不完整")
```

### Issue 2: timeout太短导致加载不完全 ⚠️

**原因**: timeout < 3000ms

**解决方案**:
```python
# ❌ 错误: timeout太短
mcp__chrome-devtools__navigate_page(url=url, timeout=1000)

# ✅ 正确: timeout≥3000ms
mcp__chrome-devtools__navigate_page(
    url=url,
    timeout=3000  # 本地HTML最低3秒
)

# ✅ 更好: 远程网页5秒
mcp__chrome-devtools__navigate_page(
    url=remote_url,
    timeout=5000  # 远程网页建议5秒
)
```

### Issue 3: 本地文件路径错误

**原因**: file:// URL格式不正确

**解决方案**:
```python
# ✅ 正确: 使用绝对路径
from pathlib import Path
html_path = Path("file.html").absolute()
file_url = f"file:///{html_path}"  # 注意三个斜杠

mcp__chrome-devtools__navigate_page(
    url=file_url,
    timeout=3000
)

# ❌ 错误: 使用相对路径
file_url = "file://file.html"  # 缺少绝对路径
```

## Integration Examples

### Example 1: 与PPT生成集成 (⚠️ 简化版)

```python
from pptx import Presentation
from pptx.util import Inches
from pathlib import Path

project_name = "火锅店开业筹备"
html_dir = Path("html_slides")
output_dir = Path("output") / project_name / "screenshots"  # 简化路径
output_dir.mkdir(parents=True, exist_ok=True)

# 1. 截图HTML幻灯片
mcp__chrome-devtools__resize_page(width=1920, height=1080)

screenshots = []
for i in range(1, 8):
    html_file = html_dir / f"slide_{i:02d}.html"
    file_url = f"file:///{html_file.absolute()}"

    # ⚠️ 最低3秒超时
    mcp__chrome-devtools__navigate_page(
        url=file_url,
        timeout=3000  # ⚠️ 改为3000ms
    )

    screenshot_path = output_dir / f"slide_{i:02d}.png"

    # ⚠️ 必须fullPage=True
    mcp__chrome-devtools__take_screenshot(
        filePath=str(screenshot_path),
        fullPage=True  # ⚠️ 必须
    )
    screenshots.append(screenshot_path)

# 2. 组装PPT
prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(5.625)

for screenshot in screenshots:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.shapes.add_picture(
        str(screenshot),
        left=0,
        top=0,
        width=Inches(10),
        height=Inches(5.625)
    )

ppt_path = output_dir / "presentation.pptx"
prs.save(str(ppt_path))
print(f"✅ PPT生成完成: {ppt_path}")
```

### Example 2: 与图片处理集成 (⚠️ 简化版)

```python
from PIL import Image
from pathlib import Path

project_name = "批量生成餐饮海报"
output_dir = Path("output") / project_name / "screenshots"  # 简化路径
output_dir.mkdir(parents=True, exist_ok=True)

# 1. ⚠️ 全页截图
fullpage_path = output_dir / "fullpage.png"
mcp__chrome-devtools__take_screenshot(
    filePath=str(fullpage_path),
    fullPage=True  # ⚠️ 必须
)

# 2. 按高度分页
img = Image.open(fullpage_path)
width, height = img.size
page_height = 1080

num_pages = (height + page_height - 1) // page_height

for page_num in range(num_pages):
    top = page_num * page_height
    bottom = min((page_num + 1) * page_height, height)

    cropped = img.crop((0, top, width, bottom))

    # 如果最后一页高度不足,填充白色背景
    if bottom - top < page_height:
        background = Image.new('RGB', (width, page_height), (250, 250, 250))
        background.paste(cropped, (0, 0))
        cropped = background

    page_path = output_dir / f"page_{page_num+1}.png"
    cropped.save(page_path)

print(f"✅ 图片分页完成: {num_pages} 张")
```

## Tips & Tricks (⚠️ 关键要点)

### ⚠️ 强制规范 (必须遵守)

1. **fullPage=True**: 所有截图必须使用 `fullPage=True`
2. **timeout≥3000ms**: 本地HTML最低3000ms,远程网页5000ms
3. **简化路径**: `output/[项目名]/screenshots/` (不使用子目录)
4. **等待完成**: 先 `navigate_page`,等待完成后再 `take_screenshot`

### 📋 最佳实践

5. **文件命名**: 包含时间戳 `海报_20250130_103000.png`,便于版本管理
6. **批量效率**: 重用同一个Chrome实例,避免重复导航开销
7. **格式选择**: PNG适合质量要求高的场景,WebP适合需要压缩的场景
8. **质量验证**: 使用PIL验证截图尺寸,确保内容完整

### ⚠️ 常见陷阱

- ❌ 使用 `fullPage=False` (会截断内容)
- ❌ `timeout < 3000ms` (加载不完全)
- ❌ 省略 `fullPage` 参数 (默认False)
- ❌ 使用子目录 `results/` (过度复杂)

### ✅ 完整检查清单

在每次截图前,确认:
1. ✅ `timeout` ≥ 3000ms (本地HTML) 或 ≥ 5000ms (远程网页)
2. ✅ `fullPage = True` (强制要求)
3. ✅ 输出路径: `output/[项目名]/screenshots/`
4. ✅ 等待 `navigate_page` 完成后再 `take_screenshot`
5. ✅ 验证截图尺寸 (使用PIL Image.open)
