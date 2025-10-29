# Screenshots Skill

专业的网页截图能力包，基于playwright-mcp提供完整的页面截图、视口配置和加载等待功能。

## 功能特性

- ✅ **fullPage全页截图**: 捕获完整页面高度,不限于视口
- ✅ **视口配置**: 支持1920x1080、4K等标准尺寸
- ✅ **加载等待**: 智能等待页面完全加载和渲染
- ✅ **批量处理**: 高效处理多个HTML文件截图
- ✅ **质量验证**: 自动验证截图尺寸和完整性
- ✅ **格式支持**: PNG(无损)、JPEG(压缩)
- ✅ **文件管理**: 标准化路径组织和命名规范

## 快速开始

### 单页截图

```python
# 1. 设置视口
await page.set_viewport_size(width=1920, height=1080)

# 2. 导航到页面
file_url = f"file:///{Path('slide_01.html').absolute()}"
await page.navigate(url=file_url, wait_until="load")

# 3. 等待渲染
await page.wait_for_timeout(1500)

# 4. 全页截图
await page.screenshot(
    path="screenshot_01.png",
    fullPage=True
)
```

### 批量截图

```python
from pathlib import Path

html_dir = Path("html_slides")
output_dir = Path("screenshots")
output_dir.mkdir(exist_ok=True)

# 获取所有HTML文件
html_files = sorted(html_dir.glob("slide_*.html"))

# 设置视口
await page.set_viewport_size(width=1920, height=1080)

# 批量处理
for html_file in html_files:
    file_url = f"file:///{html_file.absolute()}"
    await page.navigate(url=file_url, wait_until="load")
    await page.wait_for_timeout(1500)

    output_file = output_dir / f"{html_file.stem}.png"
    await page.screenshot(
        path=str(output_file),
        fullPage=True
    )
```

## 核心能力

### 1. 页面加载控制

```python
# 等待load事件 (适用于本地HTML)
await page.navigate(url=file_url, wait_until="load")
await page.wait_for_timeout(1000)

# 等待网络空闲 (适用于远程网页)
await page.navigate(url=remote_url, wait_until="networkidle")
await page.wait_for_timeout(2000)
```

### 2. 截图模式

```python
# fullPage模式 - 捕获完整页面高度
await page.screenshot(path="full.png", fullPage=True)

# viewport模式 - 仅捕获视口区域
await page.screenshot(path="viewport.png", fullPage=False)
```

### 3. 视口配置

```python
# 全高清 (1920x1080)
await page.set_viewport_size(width=1920, height=1080)

# 4K (3840x2160)
await page.set_viewport_size(width=3840, height=2160)

# 移动端 (375x667)
await page.set_viewport_size(width=375, height=667)
```

### 4. 质量验证

```python
from PIL import Image

img = Image.open("screenshot.png")
width, height = img.size

# 验证尺寸
assert width == 1920, f"Width {width} != 1920"
assert height >= 800, f"Height {height} too small"
```

## 辅助脚本

### batch_screenshot.py

提供批量处理和验证功能:

```python
from scripts.batch_screenshot import (
    validate_screenshot,
    batch_validate_screenshots,
    split_screenshot_by_height,
    generate_screenshot_report
)

# 验证单个截图
result = validate_screenshot(
    screenshot_path=Path("screenshot.png"),
    expected_width=1920,
    min_height=800
)

# 批量验证
results = batch_validate_screenshots(
    screenshot_dir=Path("screenshots"),
    pattern="slide_*.png"
)

# 生成报告
report = generate_screenshot_report(results)
print(report)

# 按高度分割
split_files = split_screenshot_by_height(
    screenshot_path=Path("fullpage.png"),
    output_dir=Path("paginated"),
    page_height=1080
)
```

## 最佳实践

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
# ✓ 推荐: fullPage=True
await page.screenshot(path="output.png", fullPage=True)

# ✗ 不推荐: fullPage=False (可能内容不完整)
await page.screenshot(path="output.png", fullPage=False)
```

### 3. 标准化视口尺寸

```python
# ✓ 推荐: 显式设置
await page.set_viewport_size(width=1920, height=1080)

# ✗ 不推荐: 依赖默认值
```

### 4. 验证截图质量

```python
# ✓ 推荐: 验证尺寸和质量
from PIL import Image
img = Image.open("output.png")
if img.size[0] != 1920:
    raise ValueError("Screenshot width incorrect")

# ✗ 不推荐: 假设截图成功
```

## 常见问题

### Q1: 截图内容不完整

**原因**: 页面未完全加载或视口高度不足

**解决**:
- 增加等待时间: `wait_for_timeout(2000)`
- 确保使用fullPage: `fullPage=True`
- 优化HTML内容高度

### Q2: 截图尺寸不符合预期

**原因**: 视口未正确设置或HTML内容超出尺寸

**解决**:
- 显式设置视口: `set_viewport_size(width=1920, height=1080)`
- 验证HTML body尺寸
- 检查截图实际尺寸

### Q3: 本地文件路径错误

**原因**: file:// URL格式不正确

**解决**:
```python
# ✓ 正确: 使用绝对路径
file_url = f"file:///{Path('file.html').absolute()}"

# ✗ 错误: 使用相对路径
file_url = "file://file.html"
```

## 典型应用场景

### 场景1: HTML演示稿截图

用于将HTML幻灯片转换为图片,再组装成PPT:

```python
# 截图7页HTML演示稿
for i in range(1, 8):
    html_file = f"slide_{i:02d}.html"
    file_url = f"file:///{Path(html_file).absolute()}"

    await page.navigate(url=file_url)
    await page.wait_for_timeout(1500)

    await page.screenshot(
        path=f"screenshot_{i:02d}.png",
        fullPage=True
    )
```

### 场景2: 网页存档

用于保存网页完整视觉效果:

```python
await page.set_viewport_size(width=1920, height=1080)
await page.navigate(url="https://example.com", wait_until="networkidle")
await page.wait_for_timeout(2000)

await page.screenshot(
    path="webpage_archive.png",
    fullPage=True
)
```

### 场景3: 自动化测试验证

用于UI自动化测试的视觉回归:

```python
# 截图前状态
await page.screenshot(path="before.png")

# 执行操作
await page.click(selector="#button")

# 截图后状态
await page.screenshot(path="after.png")

# 对比差异
from PIL import Image, ImageChops
img1 = Image.open("before.png")
img2 = Image.open("after.png")
diff = ImageChops.difference(img1, img2)
```

## 与其他Skills集成

### 与html-to-ppt集成

```python
# 1. screenshots skill: 截图HTML幻灯片
await page.screenshot(path="slide_01.png", fullPage=True)

# 2. html-to-ppt skill: 组装PPT
from pptx import Presentation
prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[6])
slide.shapes.add_picture("slide_01.png", 0, 0, Inches(10), Inches(5.625))
```

### 与图片处理集成

```python
# 1. screenshots skill: 全页截图
await page.screenshot(path="fullpage.png", fullPage=True)

# 2. 图片处理: 按高度分页
from scripts.batch_screenshot import split_screenshot_by_height
split_files = split_screenshot_by_height(
    screenshot_path=Path("fullpage.png"),
    output_dir=Path("paginated"),
    page_height=1080
)
```

## 技术栈

- **playwright-mcp**: 浏览器自动化MCP工具
- **PIL/Pillow**: Python图像处理库
- **pathlib**: 现代文件路径操作
- **asyncio**: 异步I/O支持

## 版本历史

- **v1.0.0** (2025-10-21): 初始版本
  - 基础截图功能
  - fullPage全页支持
  - 批量处理脚本
  - 质量验证工具

## License

MIT License

## 相关资源

- [playwright-mcp官方文档](https://github.com/microsoft/playwright-python)
- [PIL/Pillow文档](https://pillow.readthedocs.io/)
- [Skills创建规范](.claude/agents/system/F5-Skills技能包创建工程师.md)
