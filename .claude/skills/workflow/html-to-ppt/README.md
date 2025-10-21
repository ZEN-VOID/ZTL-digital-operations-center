# HTML-to-PPT Skill

完整的HTML到PPT转换流程型技能包,从内容分析、HTML设计、截图到PPT组装的端到端解决方案。

## 功能特性

- ✅ **6阶段工作流**: 内容分析 → HTML设计 → 截图捕获 → PPT组装 → 质量验证 → 返工优化
- ✅ **标准尺寸**: 固定1920x1080 HTML设计,16:9 PPT输出
- ✅ **配色方案**: 4种预定义配色(商务/科技/自然/优雅)
- ✅ **模板系统**: 封面页/目录页/内容页标准化模板
- ✅ **质量保证**: 自动验证截图和PPT质量
- ✅ **迭代优化**: 支持返工重新生成
- ✅ **元数据支持**: 嵌入PPT标题、作者等元数据

## 快速开始

### 完整工作流

```python
from pathlib import Path
from scripts.html_generator import (
    generate_cover_slide,
    generate_toc_slide,
    generate_content_slide
)
from scripts.ppt_assembler import (
    create_ppt_from_screenshots,
    validate_screenshots,
    validate_ppt,
    generate_quality_report
)

# Phase 1: 内容分析 (手动规划)
slides_data = [
    {"type": "cover", "title": "营销方案", "subtitle": "口号"},
    {"type": "toc", "chapters": ["章节1", "章节2"]},
    {"type": "content", "title": "章节1", "sections": [...]}
]

# Phase 2: 生成HTML
html_dir = Path("html_slides")
html_dir.mkdir(exist_ok=True)

cover = generate_cover_slide(
    title="云南过桥米线<br>品牌营销策划方案",
    subtitle='"一碗过桥,三餐云南"',
    date="2025年10月"
)
(html_dir / "slide_01.html").write_text(cover, encoding='utf-8')

# Phase 3: 截图 (使用screenshots skill)
await page.set_viewport_size(width=1920, height=1080)
for html_file in html_dir.glob("slide_*.html"):
    file_url = f"file:///{html_file.absolute()}"
    await page.navigate(url=file_url, wait_until="load")
    await page.wait_for_timeout(1500)
    await page.screenshot(
        path=f"screenshots/{html_file.stem}.png",
        fullPage=True
    )

# Phase 4: 组装PPT
create_ppt_from_screenshots(
    screenshot_dir=Path("screenshots"),
    output_ppt=Path("output.pptx"),
    title="云南过桥米线营销方案"
)

# Phase 5: 质量验证
screenshot_validation = validate_screenshots(Path("screenshots"))
ppt_validation = validate_ppt(Path("output.pptx"), expected_slide_count=7)
report = generate_quality_report(screenshot_validation, ppt_validation)
print(report)
```

## 工作流详解

### Phase 1: 内容分析

理解用户需求,提取关键信息,规划幻灯片结构。

**分析维度**:
- 主题与目的
- 目标受众
- 核心信息
- 预计页数
- 设计风格
- 配色方案

**输出**: 幻灯片结构规划

### Phase 2: HTML设计

根据规划生成标准化HTML幻灯片。

**标准尺寸**:
- HTML: 1920x1080px
- PPT: 10x5.625英寸 (16:9)

**模板类型**:

#### 1. 封面页 (Gradient背景)

```python
from scripts.html_generator import generate_cover_slide

html = generate_cover_slide(
    title="云南过桥米线<br>品牌营销策划方案",
    subtitle='"一碗过桥,三餐云南"',
    date="2025年10月",
    color_scheme="business"
)
```

**特点**:
- 渐变背景,视觉冲击力强
- 标题+副标题+日期
- 无内容卡片,简洁大气

#### 2. 目录页 (Card背景)

```python
from scripts.html_generator import generate_toc_slide

html = generate_toc_slide(
    chapters=[
        "01. 项目概览 – 营销主题与核心理念",
        "02. 品牌分析 – 目标客群与市场洞察",
        "03. 创意策略 – 三大核心创意与视觉展示"
    ],
    color_scheme="business"
)
```

**特点**:
- 白色卡片背景,阅读性好
- 清晰的列表结构
- 层次分明

#### 3. 内容页 (Card背景)

```python
from scripts.html_generator import generate_content_slide

html = generate_content_slide(
    slide_num=3,
    title="01. 项目概览",
    sections=[
        {
            "subtitle": "营销主题",
            "content": '<p>"一碗过桥,三餐云南"</p>'
        },
        {
            "subtitle": "核心理念",
            "content": '<ul><li>传承云南味道</li></ul>'
        }
    ],
    color_scheme="business"
)
```

**特点**:
- 支持多个章节
- h2/h3标题层级
- 段落/列表/引用等丰富格式

### Phase 3: 截图捕获

使用screenshots skill对HTML进行全页截图。

**关键配置**:

```python
# 1. 设置视口
await page.set_viewport_size(width=1920, height=1080)

# 2. 导航并等待
file_url = f"file:///{html_file.absolute()}"
await page.navigate(url=file_url, wait_until="load")
await page.wait_for_timeout(1500)

# 3. 全页截图
await page.screenshot(
    path="screenshot.png",
    fullPage=True
)
```

**质量检查**:

```python
from scripts.ppt_assembler import validate_screenshots

result = validate_screenshots(
    screenshot_dir=Path("screenshots"),
    expected_width=1920,
    min_height=800
)

if not result['valid']:
    print("截图质量问题:")
    for error in result['errors']:
        print(f"  - {error}")
```

### Phase 4: PPT组装

将截图组装成PPT文件。

```python
from scripts.ppt_assembler import create_ppt_from_screenshots

result = create_ppt_from_screenshots(
    screenshot_dir=Path("screenshots"),
    output_ppt=Path("output.pptx"),
    pattern="slide_*.png",
    slide_width=10.0,
    slide_height=5.625,
    title="云南过桥米线营销方案",
    author="ZTL数智化作战中心"
)

print(f"✅ 生成 {result['slide_count']} 页PPT")
print(f"📦 文件大小: {result['file_size_mb']}MB")
```

### Phase 5: 质量验证

全面验证截图和PPT质量。

```python
from scripts.ppt_assembler import (
    validate_screenshots,
    validate_ppt,
    generate_quality_report
)

# 验证截图
screenshot_result = validate_screenshots(
    screenshot_dir=Path("screenshots")
)

# 验证PPT
ppt_result = validate_ppt(
    ppt_path=Path("output.pptx"),
    expected_slide_count=7,
    max_file_size_mb=50.0
)

# 生成报告
report = generate_quality_report(
    screenshot_validation=screenshot_result,
    ppt_validation=ppt_result,
    output_file=Path("quality_report.md")
)
```

**验证清单**:

```yaml
截图质量:
  - ✓ 尺寸1920xN (N>=1080)
  - ✓ 内容完整无截断
  - ✓ 文字清晰可读

PPT质量:
  - ✓ 页数与截图一致
  - ✓ 16:9宽屏格式
  - ✓ 图片无失真
  - ✓ 文件大小<50MB

内容质量:
  - ✓ 字号足够大
  - ✓ 颜色对比度足够
  - ✓ 版式平衡美观
  - ✓ 品牌元素一致
```

### Phase 6: 返工优化

发现问题后的迭代优化。

**常见问题**:

#### 问题1: 截图内容不完整

**解决**:
```python
# 1. 增加等待时间
await page.wait_for_timeout(2000)

# 2. 优化HTML内容高度
.content {
    max-height: 850px;
    overflow-y: auto;
}

# 3. 减少字号
h2 { font-size: 36px; }  # 从40px减小
```

#### 问题2: 文字模糊

**解决**:
```python
# 1. 确保PNG格式
await page.screenshot(path="output.png", type="png")

# 2. 增大字号
h1 { font-size: 72px; }

# 3. 增强文字阴影
h1 { text-shadow: 0 4px 12px rgba(0,0,0,0.3); }
```

#### 问题3: PPT文件过大

**解决**:
```python
# 1. 压缩截图
from PIL import Image
img = Image.open("slide.png")
img.save("slide_compressed.jpg", 'JPEG', quality=85)

# 2. 使用JPEG格式
await page.screenshot(path="output.jpg", type="jpeg", quality=90)
```

## 配色方案

### 1. Business (商务)

```python
color_scheme="business"

# 颜色值:
primary: #FF6B35    # 橙色 (热情)
secondary: #004E89  # 深蓝 (专业)
accent: #FFD23F     # 金黄 (高端)
background: #F7F7F7 # 浅灰 (简洁)
```

**适用**: 营销方案、商业提案、年度总结

### 2. Tech (科技)

```python
color_scheme="tech"

# 颜色值:
primary: #00D9FF    # 青色 (创新)
secondary: #6366F1  # 紫色 (科技)
accent: #F43F5E     # 玫红 (活力)
background: #0F172A # 深灰 (现代)
```

**适用**: 产品发布、技术分享、创新方案

### 3. Nature (自然)

```python
color_scheme="nature"

# 颜色值:
primary: #10B981    # 绿色 (自然)
secondary: #059669  # 深绿 (健康)
accent: #FCD34D     # 黄色 (活力)
background: #F0FDF4 # 浅绿 (清新)
```

**适用**: 环保主题、健康食品、生态项目

### 4. Elegant (优雅)

```python
color_scheme="elegant"

# 颜色值:
primary: #8B5CF6    # 紫色 (优雅)
secondary: #EC4899  # 粉色 (浪漫)
accent: #F59E0B     # 橙色 (温暖)
background: #FAF5FF # 浅紫 (柔和)
```

**适用**: 品牌发布、时尚设计、文化活动

## 辅助工具

### html_generator.py

HTML生成和格式化工具:

```python
from scripts.html_generator import (
    create_html_slide,
    format_list_content,
    format_two_column_content,
    format_quote_content,
    generate_cover_slide,
    generate_toc_slide,
    generate_content_slide
)

# 生成列表内容
list_html = format_list_content([
    "项目1",
    "项目2",
    "项目3"
], ordered=False)

# 生成双栏内容
two_col_html = format_two_column_content(
    left="<h3>优势</h3><p>内容</p>",
    right="<h3>挑战</h3><p>内容</p>"
)

# 生成引用
quote_html = format_quote_content(
    quote="一碗过桥,三餐云南",
    author="品牌口号"
)
```

### ppt_assembler.py

PPT组装和验证工具:

```python
from scripts.ppt_assembler import (
    create_ppt_from_screenshots,
    validate_screenshots,
    validate_ppt,
    generate_quality_report
)

# 组装PPT
result = create_ppt_from_screenshots(
    screenshot_dir=Path("screenshots"),
    output_ppt=Path("output.pptx")
)

# 验证质量
screenshot_val = validate_screenshots(Path("screenshots"))
ppt_val = validate_ppt(Path("output.pptx"), expected_slide_count=7)

# 生成报告
report = generate_quality_report(screenshot_val, ppt_val)
```

## 最佳实践

### 1. 内容规划优先

```python
# ✓ 推荐: 先规划结构
slides_structure = [
    {"type": "cover", ...},
    {"type": "toc", ...},
    {"type": "content", ...}
]

# ✗ 不推荐: 直接生成HTML
```

### 2. 控制内容高度

```python
# ✓ 推荐: 使用max-height限制
.content {
    max-height: 850px;
    overflow-y: auto;
}

# ✗ 不推荐: 无高度限制
```

### 3. 统一设计系统

```python
# ✓ 推荐: 所有页面使用同一配色方案
color_scheme="business"

# ✗ 不推荐: 每页不同配色
```

### 4. 测试优先

```python
# ✓ 推荐: 先生成1-2页测试
generate_and_test_slides([1, 2])

# ✗ 不推荐: 一次生成所有页面
```

### 5. 质量验证

```python
# ✓ 推荐: 每个阶段都验证
validate_html()
validate_screenshots()
validate_ppt()

# ✗ 不推荐: 只在最后验证
```

## 完整示例

查看`scripts/`目录下的示例代码:

- `html_generator.py`: HTML生成示例
- `ppt_assembler.py`: PPT组装示例

## 应用场景

### 场景1: 营销方案PPT

```python
# 适用配色: business
# 页面类型: 封面+目录+6-8个内容页
# 特点: 专业商务,数据可视化

generate_marketing_proposal(
    title="云南过桥米线营销方案",
    chapters=["项目概览", "品牌分析", "创意策略", ...],
    color_scheme="business"
)
```

### 场景2: 产品发布PPT

```python
# 适用配色: tech
# 页面类型: 封面+产品特性+技术优势
# 特点: 现代科技,视觉冲击

generate_product_launch(
    product_name="智能餐饮系统",
    features=[...],
    color_scheme="tech"
)
```

### 场景3: 培训课程PPT

```python
# 适用配色: elegant
# 页面类型: 封面+目录+知识点+案例
# 特点: 清晰易读,层次分明

generate_training_course(
    course_name="餐饮运营管理",
    modules=[...],
    color_scheme="elegant"
)
```

## 技术栈

- **HTML/CSS**: 标准化幻灯片设计
- **playwright-mcp**: 浏览器自动化和截图
- **python-pptx**: PPT文件生成
- **PIL/Pillow**: 图像处理和验证
- **pathlib**: 文件路径管理

## 版本历史

- **v1.0.0** (2025-10-21): 初始版本
  - 6阶段完整工作流
  - 4种配色方案
  - HTML生成器和PPT组装器
  - 质量验证系统
  - 返工优化机制

## License

MIT License

## 相关资源

- [screenshots skill](../screenshots/) - 截图能力包
- [playwright-mcp](https://github.com/microsoft/playwright-python) - 浏览器自动化
- [python-pptx](https://python-pptx.readthedocs.io/) - PPT生成库
