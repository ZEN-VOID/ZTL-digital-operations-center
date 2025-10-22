---
name: screenshots
description: Playwright-MCP screenshot capability for capturing web pages with full page support, viewport configuration, and load waiting. Use for web page screenshots, HTML rendering capture, full-page captures, and quality verification.
---

# Screenshots Skill

专业的网页截图能力包，基于playwright-mcp提供完整的页面截图、视口配置和加载等待功能。

## Quick Start

### 基础截图

```python
# 1. 导航到目标URL并截图
await page.navigate(url="file:///path/to/file.html")
await page.wait_for_timeout(1000)  # 等待页面加载
await page.screenshot(
    path="output.png",
    fullPage=True
)
```

### 配置视口尺寸

```python
# 2. 指定视口大小进行截图
await page.set_viewport_size(width=1920, height=1080)
await page.navigate(url="https://example.com")
await page.wait_for_timeout(2000)
await page.screenshot(
    path="screenshot.png",
    fullPage=True  # 捕获整个页面高度
)
```

### 批量截图HTML文件

```python
# 3. 批量处理多个HTML文件
html_files = ["slide_01.html", "slide_02.html", "slide_03.html"]

for i, html_file in enumerate(html_files):
    file_url = f"file:///{Path(html_file).absolute()}"
    await page.navigate(url=file_url)
    await page.wait_for_timeout(1500)

    await page.screenshot(
        path=f"screenshot_{i+1:02d}.png",
        fullPage=True
    )
```

## Core Capabilities

### 1. 页面加载控制

**等待策略**:
- `wait_for_timeout(ms)`: 固定等待时间
- `wait_until="networkidle"`: 等待网络空闲
- `wait_until="load"`: 等待load事件

**最佳实践**:
```python
# 对于本地HTML文件
await page.navigate(url=file_url, wait_until="load")
await page.wait_for_timeout(1000)  # 额外等待1秒确保渲染完成

# 对于远程网页
await page.navigate(url=remote_url, wait_until="networkidle")
await page.wait_for_timeout(2000)  # 等待动态内容加载
```

### 2. 截图配置

**fullPage模式** (推荐用于长页面):
```python
await page.screenshot(
    path="fullpage.png",
    fullPage=True  # 捕获完整页面高度,不限于视口
)
```

**viewport模式** (仅视口可见区域):
```python
await page.screenshot(
    path="viewport.png",
    fullPage=False  # 仅捕获1920x1080视口区域
)
```

**图片格式**:
```python
# PNG格式 (默认,无损)
await page.screenshot(path="output.png")

# JPEG格式 (有损压缩,文件更小)
await page.screenshot(path="output.jpg", type="jpeg", quality=90)
```

### 3. 视口配置

**标准尺寸**:
```python
# 全高清 (1920x1080)
await page.set_viewport_size(width=1920, height=1080)

# 4K (3840x2160)
await page.set_viewport_size(width=3840, height=2160)

# 移动端 (375x667)
await page.set_viewport_size(width=375, height=667)
```

### 4. 文件路径管理

**本地HTML文件**:
```python
from pathlib import Path

html_path = Path("output/创意组/营销策划/html_slides/slide_01.html")
file_url = f"file:///{html_path.absolute()}"
await page.navigate(url=file_url)
```

**输出路径组织**:
```python
output_dir = Path("output/创意组/营销策划/screenshots")
output_dir.mkdir(parents=True, exist_ok=True)

screenshot_path = output_dir / f"slide_{i+1:02d}.png"
await page.screenshot(path=str(screenshot_path), fullPage=True)
```

## Usage Patterns

### Pattern 1: 单页面截图工作流

```python
# Step 1: 设置视口
await page.set_viewport_size(width=1920, height=1080)

# Step 2: 导航并等待
await page.navigate(url=target_url, wait_until="load")
await page.wait_for_timeout(1500)

# Step 3: 全页截图
await page.screenshot(
    path="output.png",
    fullPage=True
)

# Step 4: 验证截图尺寸
from PIL import Image
img = Image.open("output.png")
print(f"Screenshot size: {img.size}")  # (1920, actual_height)
```

### Pattern 2: HTML演示稿批量截图

```python
from pathlib import Path

html_dir = Path("html_slides")
output_dir = Path("screenshots")
output_dir.mkdir(exist_ok=True)

# 获取所有HTML文件
html_files = sorted(html_dir.glob("slide_*.html"))

# 设置视口
await page.set_viewport_size(width=1920, height=1080)

# 批量截图
for html_file in html_files:
    slide_num = html_file.stem.split('_')[1]

    file_url = f"file:///{html_file.absolute()}"
    await page.navigate(url=file_url, wait_until="load")
    await page.wait_for_timeout(1500)

    output_file = output_dir / f"slide_{slide_num}.png"
    await page.screenshot(
        path=str(output_file),
        fullPage=True
    )

    print(f"✓ {output_file.name}")
```

### Pattern 3: 带质量验证的截图

```python
from PIL import Image

async def screenshot_with_validation(page, url, output_path, expected_width=1920):
    """截图并验证质量"""

    # 截图
    await page.navigate(url=url, wait_until="load")
    await page.wait_for_timeout(1500)
    await page.screenshot(path=output_path, fullPage=True)

    # 验证
    img = Image.open(output_path)
    width, height = img.size

    if width != expected_width:
        raise ValueError(f"Screenshot width {width} != expected {expected_width}")

    if height < 800:
        raise ValueError(f"Screenshot height {height} too small, may be incomplete")

    return {"width": width, "height": height, "path": output_path}
```

## Playwright-MCP Tools Reference

### mcp__playwright-mcp__browser_navigate
导航到指定URL

**Parameters**:
- `url` (string, required): 目标URL或file://路径
- `width` (number, optional): 视口宽度,默认1280
- `height` (number, optional): 视口高度,默认720

**Example**:
```python
await page.navigate(
    url="file:///Users/path/to/file.html",
    width=1920,
    height=1080
)
```

### mcp__playwright-mcp__browser_take_screenshot
截取当前页面

**Parameters**:
- `fullPage` (boolean, optional): 是否全页截图,默认true
- `filename` (string, optional): 输出文件名
- `type` (string, optional): 图片格式 "png"|"jpeg"

**Example**:
```python
await page.screenshot(
    fullPage=True,
    filename="output.png",
    type="png"
)
```

### mcp__playwright-mcp__browser_wait_for
等待页面状态

**Parameters**:
- `time` (number, optional): 等待时间(秒)
- `text` (string, optional): 等待文本出现
- `textGone` (string, optional): 等待文本消失

**Example**:
```python
# 等待1.5秒
await page.wait_for_timeout(1500)

# 等待特定文本出现
await page.wait_for(text="加载完成")
```

## Best Practices

### 1. 确保页面完全加载

```python
# ✓ 推荐: 组合使用wait_until和固定等待
await page.navigate(url=target_url, wait_until="load")
await page.wait_for_timeout(1500)

# ✗ 不推荐: 仅依赖wait_until
await page.navigate(url=target_url, wait_until="load")
```

### 2. 使用fullPage捕获完整内容

```python
# ✓ 推荐: 使用fullPage=True捕获所有内容
await page.screenshot(path="output.png", fullPage=True)

# ✗ 不推荐: 仅截取视口(可能内容不完整)
await page.screenshot(path="output.png", fullPage=False)
```

### 3. 标准化视口尺寸

```python
# ✓ 推荐: 显式设置视口尺寸
await page.set_viewport_size(width=1920, height=1080)
await page.navigate(url=target_url)

# ✗ 不推荐: 依赖默认视口(可能不一致)
await page.navigate(url=target_url)
```

### 4. 验证截图质量

```python
# ✓ 推荐: 验证尺寸和文件大小
from PIL import Image
img = Image.open("output.png")
if img.size[0] != 1920:
    raise ValueError("Screenshot width incorrect")
if img.size[1] < 800:
    raise ValueError("Screenshot may be incomplete")

# ✗ 不推荐: 直接假设截图成功
await page.screenshot(path="output.png")
```

## Common Issues

### Issue 1: 截图内容不完整

**原因**: 页面未完全加载或视口高度不足

**解决方案**:
```python
# 1. 增加等待时间
await page.wait_for_timeout(2000)  # 从1000ms增加到2000ms

# 2. 确保使用fullPage
await page.screenshot(fullPage=True)

# 3. 减少HTML内容高度
# 在HTML中添加: max-height: 850px; overflow-y: auto;
```

### Issue 2: 截图尺寸不符合预期

**原因**: 视口未正确设置或HTML内容超出尺寸

**解决方案**:
```python
# 1. 显式设置视口
await page.set_viewport_size(width=1920, height=1080)

# 2. 验证HTML body尺寸
# body { width: 1920px; height: 1080px; }

# 3. 验证截图实际尺寸
img = Image.open("output.png")
print(f"Actual size: {img.size}")
```

### Issue 3: 本地文件路径错误

**原因**: file:// URL格式不正确

**解决方案**:
```python
# ✓ 正确: 使用绝对路径
from pathlib import Path
html_path = Path("file.html").absolute()
file_url = f"file:///{html_path}"  # 注意三个斜杠

# ✗ 错误: 使用相对路径
file_url = "file://file.html"  # 缺少绝对路径
```

## Integration Examples

### Example 1: 与PPT生成集成

```python
from pptx import Presentation
from pptx.util import Inches

# 1. 截图HTML幻灯片
screenshots = []
for i in range(1, 8):
    await page.navigate(url=f"file:///{html_dir}/slide_{i:02d}.html")
    await page.wait_for_timeout(1500)

    screenshot_path = f"screenshots/slide_{i:02d}.png"
    await page.screenshot(path=screenshot_path, fullPage=True)
    screenshots.append(screenshot_path)

# 2. 组装PPT
prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(5.625)

for screenshot in screenshots:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.shapes.add_picture(
        screenshot,
        left=0,
        top=0,
        width=Inches(10),
        height=Inches(5.625)
    )

prs.save("output.pptx")
```

### Example 2: 与图片处理集成

```python
from PIL import Image

# 1. 截图
await page.screenshot(path="fullpage.png", fullPage=True)

# 2. 按高度分页
img = Image.open("fullpage.png")
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

    cropped.save(f"page_{page_num+1}.png")
```

## Tips & Tricks

1. **HTML设计优化**: 将HTML内容控制在1080px高度内,避免需要分页
2. **等待时间调优**: 本地HTML文件1000-1500ms,远程网页2000-3000ms
3. **文件命名规范**: 使用`slide_01.png`而非`slide_1.png`,便于排序
4. **批量处理效率**: 重用同一个browser实例,避免重复启动
5. **内存管理**: 处理大量截图时及时关闭不用的page对象
