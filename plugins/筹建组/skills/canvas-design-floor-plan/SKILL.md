---
name: canvas-design-floor-plan
description: 专为筹建组Z1-平面图计划师定制的建筑平面图生成技能包。基于自然语言描述和结构化配置文档生成专业建筑平面图PNG/PDF。支持功能分区可视化、动线设计、家具布置标准化表达。适用于餐饮空间规划、新店筹建的平面图创作。
---

# Canvas-Design Floor Plan Generator

> 专为建筑平面图设计的AI可视化工具，将结构化配置文档转化为专业制图标准的PNG/PDF平面图。

---

## 🎯 核心能力

- **建筑制图标准**: 符合GB建筑制图规范（线型、标注、图例）
- **智能布局**: 自动计算家具布置、动线流畅性、空间效率
- **多格式输出**: PNG (4K屏幕展示) + PDF (A3矢量打印)
- **快速生成**: 平均2分钟完成300㎡平面图
- **高度可定制**: 支持6种餐饮类型的预设模板

---

## 🚀 快速开始

### 基础用法

```python
from scripts.floor_plan_generator import generate_floor_plan

# 输入: Z1生成的平面图配置.md
config_path = "output/火锅店开业筹备/Z1-平面图计划师/平面图配置-20251028.md"

# 输出目录
output_dir = "output/火锅店开业筹备/Z1-平面图计划师/"

# 执行生成
result = generate_floor_plan(
    config_md_path=config_path,
    output_dir=output_dir,
    output_formats=["png", "pdf"],  # 可选: "png", "pdf", "svg"
    resolution="4K"  # 可选: "1080p", "4K", "8K"
)

print(f"✅ 平面图生成成功!")
print(f"PNG: {result['png_path']}")
print(f"PDF: {result['pdf_path']}")
```

### Claude Code使用方式

在Z1 Agent中直接调用：

```markdown
我现在将调用canvas-design-floor-plan技能包生成专业平面图。

输入: output/火锅店开业筹备/Z1-平面图计划师/平面图配置-20251028.md
输出: PNG (4K) + PDF (A3矢量)

执行命令:
```

使用 `Skill` tool 调用 `canvas-design-floor-plan`。

---

## 📁 配置文档格式

### 必需字段

平面图配置.md必须包含以下结构：

```markdown
# [项目名称] 平面图设计配置

## 基础信息
- **项目名称**: 火锅店开业筹备
- **空间尺寸**: 300㎡ (长20m × 宽15m)
- **层高**: 3.6m
- **风格**: 现代简约 + 工业风

## 功能分区布局

### 入口区域 (10㎡)
- 位置: 建筑左侧主入口
- 元素: 接待台、等候区、品牌展示
- 设计要点: 开阔视野、品牌形象强化

### 开放就餐区 (150㎡)
- 位置: 中央主区域
- 座位数: 60人（2人桌×10，4人桌×10）
- 桌椅规格: 2人桌 600×700mm，4人桌 800×800mm
- 间距要求: 主通道≥1400mm，桌间≥600mm

[其他区域同理...]

## 动线设计

### 顾客动线
入口 → 等候区 → 就餐区 → 卫生间 → 收银 → 出口

### 服务动线
厨房 → 传菜通道 → 就餐区 → 回收通道 → 洗碗区

[其他动线...]

## 视觉风格要求

### 线条风格
- 墙体: 粗实线 (3px黑色)
- 门窗: 中等线 (1.5px黑色)
- 家具: 细线 (0.8px灰色)
- 尺寸标注: 细线 (0.5px蓝色)

### 配色方案
- 背景: 浅灰 (#F5F5F5)
- 墙体: 深灰 (#333333)
- 功能区: 不同色块区分（就餐区浅蓝、厨房浅绿、卫生间浅黄）

### 图例要求
- 比例尺: 1:100
- 指北针: 右上角
- 图例: 左下角（包含所有符号说明）

## canvas-design调用参数

**创作风格**: architectural_floor_plan
**输出格式**: PNG (4K分辨率) + PDF (矢量格式)
**画布尺寸**: 1920×1440 (适合A3打印)
```

---

## 🎨 支持的餐饮类型预设

### 1. 快餐型 (Fast-Casual)
- 特点: 高密度开放座位、快速动线、小厨房
- 空间效率: 1.8-2.2㎡/座
- 典型: 快餐店、面馆、轻餐

### 2. 火锅型 (Hot Pot)
- 特点: 卡座为主、通风要求高、大厨房
- 空间效率: 2.5-3.0㎡/座
- 典型: 火锅店、烧烤店、韩式烤肉

### 3. 中餐型 (Chinese Fine Dining)
- 特点: 包间为主、走廊系统、展示厨房
- 空间效率: 3.5-4.5㎡/座
- 典型: 中餐厅、酒楼、宴会厅

### 4. 西餐型 (Western Fine Dining)
- 特点: 宽敞开放、吧台区、酒窖
- 空间效率: 4.0-5.0㎡/座
- 典型: 西餐厅、牛排馆、法餐

### 5. 咖啡型 (Cafe)
- 特点: 混合座位、柜台区、展示区
- 空间效率: 2.0-2.5㎡/座
- 典型: 咖啡厅、烘焙店、茶饮店

### 6. 混合型 (Mixed-Use)
- 特点: 多样化座位、灵活分区、适应性强
- 空间效率: 2.5-3.0㎡/座
- 典型: 综合餐厅、多品牌餐饮

选择预设模板可加速生成，并自动应用行业最佳实践。

---

## ⚙️ 高级配置

### 自定义输出参数

```python
result = generate_floor_plan(
    config_md_path=config_path,
    output_dir=output_dir,

    # 输出格式
    output_formats=["png", "pdf", "svg"],

    # PNG分辨率
    resolution="4K",  # "1080p", "4K", "8K"

    # PDF打印规格
    pdf_size="A3",  # "A3", "A2", "A1", "A0"

    # 画布尺寸（像素）
    canvas_size=(1920, 1440),

    # 比例尺
    scale="1:100",  # "1:50", "1:100", "1:200"

    # 是否显示尺寸标注
    show_dimensions=True,

    # 是否显示家具
    show_furniture=True,

    # 线条粗细系数
    line_weight_factor=1.0,  # 0.5-2.0

    # 色彩模式
    color_mode="standard",  # "standard", "grayscale", "high_contrast"
)
```

### 批量生成

生成多个视图或方案：

```python
from scripts.floor_plan_generator import batch_generate

configs = [
    "平面图配置-方案A.md",
    "平面图配置-方案B.md",
    "平面图配置-方案C.md"
]

results = batch_generate(
    config_paths=configs,
    output_dir=output_dir,
    parallel=True,  # 并行生成
    max_workers=3
)

for result in results:
    print(f"✅ {result['config_name']}: {result['status']}")
```

---

## 📐 建筑制图规范

### 线型标准 (GB/T 18112-2000)

| 元素 | 线型 | 粗细 | 颜色 |
|------|------|------|------|
| 墙体 | 实线 | 粗线 (3px) | 黑色 #000000 |
| 柱子 | 实线 | 粗线 (3px) | 黑色 #000000 |
| 门窗 | 实线 | 中线 (1.5px) | 黑色 #000000 |
| 家具 | 细线 | 细线 (0.8px) | 灰色 #666666 |
| 尺寸标注 | 细线 | 细线 (0.5px) | 蓝色 #0000FF |
| 轴线 | 点划线 | 细线 (0.5px) | 红色 #FF0000 |
| 隐藏线 | 虚线 | 细线 (0.5px) | 灰色 #999999 |

### 标注规范

**尺寸标注**:
- 三道尺寸线：总尺寸、轴线间距、墙体/开口尺寸
- 单位：mm（毫米），标注时省略单位
- 箭头：实心箭头或斜线
- 文字：SimSun字体，3-5mm高度

**文字注释**:
- 房间名称：黑体，居中放置
- 面积标注：宋体，房间名称下方
- 门窗编号：圆圈标注，M1/C1格式

**图例**:
- 位置：左下角或右下角
- 内容：所有使用的符号说明
- 格式：符号 + 文字说明

### 比例尺标准

| 图纸类型 | 推荐比例 | 适用范围 |
|---------|---------|---------|
| 总平面图 | 1:200 | >1000㎡ |
| 平面布置图 | 1:100 | 300-1000㎡ |
| 详细平面图 | 1:50 | <300㎡ |
| 局部放大图 | 1:20 | 细节区域 |

---

## 🔧 技术实现

### 核心引擎

**floor_plan_generator.py**:
- 解析Markdown配置文档
- 提取空间尺寸、功能分区、家具布置
- 生成SVG矢量图形
- 转换为PNG/PDF输出

**config_parser.py**:
- Markdown结构化解析
- 验证必需字段完整性
- 提取数值型参数（尺寸、数量、比例）
- 构建内部数据模型

**render_engine.py**:
- SVG绘图引擎
- 线型、颜色、标注渲染
- 图例、比例尺、指北针生成
- PNG光栅化、PDF矢量化

### 依赖库

```python
# Python 3.10+
svgwrite==1.4.3       # SVG矢量绘图
cairosvg==2.7.1       # SVG转PNG
reportlab==4.0.7      # PDF生成
pillow==10.1.0        # 图像处理
markdown==3.5.1       # Markdown解析
pyyaml==6.0.1         # YAML配置
```

### 性能基准

| 场景 | 生成时间 | 输出大小 |
|------|---------|---------|
| 300㎡标准平面图 | ~90秒 | PNG 8MB, PDF 2MB |
| 500㎡复杂平面图 | ~150秒 | PNG 12MB, PDF 3MB |
| 批量生成（3个） | ~200秒 | 总计 30MB |

优化策略：
- SVG缓存：复用常见家具符号
- 并行渲染：多进程生成PNG/PDF
- 增量更新：只重绘修改部分

---

## 🧪 测试验证

### 单元测试

```bash
# 运行所有测试
pytest plugins/筹建组/skills/canvas-design-floor-plan/tests/

# 测试配置解析
pytest tests/test_config_parser.py

# 测试渲染引擎
pytest tests/test_render_engine.py

# 测试完整生成
pytest tests/test_integration.py
```

### 测试用例

**测试1: 基础平面图生成**
```python
def test_basic_floor_plan():
    result = generate_floor_plan(
        config_md_path="examples/example_floor_plan_config.md",
        output_dir="tests/output/"
    )

    assert result['status'] == 'success'
    assert os.path.exists(result['png_path'])
    assert os.path.exists(result['pdf_path'])

    # 验证PNG分辨率
    from PIL import Image
    img = Image.open(result['png_path'])
    assert img.size == (3840, 2160)  # 4K
```

**测试2: 复杂布局生成**
```python
def test_complex_layout():
    # 包含多个包间、复杂动线的配置
    result = generate_floor_plan(
        config_md_path="examples/complex_floor_plan_config.md",
        output_dir="tests/output/"
    )

    assert result['status'] == 'success'
    # 验证所有区域都已绘制
    assert result['zones_rendered'] == ['入口', '就餐区', '包间', '厨房', '卫生间']
```

**测试3: 错误处理**
```python
def test_missing_required_fields():
    with pytest.raises(ValueError) as exc_info:
        generate_floor_plan(
            config_md_path="examples/incomplete_config.md",
            output_dir="tests/output/"
        )

    assert "缺少必需字段: 空间尺寸" in str(exc_info.value)
```

---

## 📚 示例库

### 示例1: 简单火锅店（300㎡）

配置: `examples/hotpot_300sqm.md`

特点:
- 开放座位60人 + 包间3间
- 卡座为主布局
- 中央厨房

生成时间: ~90秒

### 示例2: 高端中餐厅（500㎡）

配置: `examples/chinese_fine_dining_500sqm.md`

特点:
- 包间为主（6个包间）
- 走廊系统
- 展示厨房

生成时间: ~150秒

### 示例3: 快餐店（200㎡）

配置: `examples/fast_casual_200sqm.md`

特点:
- 高密度开放座位
- 简单动线
- 小厨房

生成时间: ~60秒

---

## 🚨 常见问题

### Q1: 生成的平面图尺寸不准确？

**原因**: 配置文档中的尺寸单位不统一或缺失

**解决**:
- 确保所有尺寸使用统一单位（推荐mm）
- 在配置文档中明确标注单位
- 检查计算是否正确（如桌子数量×桌子尺寸+间距）

### Q2: Canvas-design生成失败？

**原因**: 配置文档格式不符合要求

**解决**:
- 参考 `examples/` 中的示例配置
- 使用 `validate_config()` 函数预检查
- 查看详细错误日志：`logs/execution-[timestamp].log`

### Q3: 输出的PDF无法打印？

**原因**: PDF尺寸设置不正确

**解决**:
```python
result = generate_floor_plan(
    config_md_path=config_path,
    pdf_size="A3",  # 确保与打印纸张一致
    pdf_orientation="landscape"  # 横向/纵向
)
```

### Q4: 如何添加自定义家具符号？

**解决**:
1. 在 `scripts/symbols.py` 中定义新符号
2. 使用SVG path格式
3. 在配置文档中引用符号名称

```python
# scripts/symbols.py
CUSTOM_SYMBOLS = {
    "circular_booth": {
        "path": "M 0,0 A 50,50 0 1,1 100,0 A 50,50 0 1,1 0,0",
        "width": 100,
        "height": 100
    }
}
```

---

## 📞 支持与反馈

**技能包维护**: Z1-平面图计划师团队

**问题反馈**: 在项目根目录运行
```bash
# 生成诊断报告
python plugins/筹建组/skills/canvas-design-floor-plan/scripts/diagnose.py
```

**文档更新**: 本SKILL.md会随着功能迭代持续更新

---

## 📝 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v1.0.0 | 2025-10-28 | 初始版本发布，支持基础平面图生成 |
| v1.1.0 | TBD | 计划：增加3D等轴测图生成 |
| v1.2.0 | TBD | 计划：支持动态动线动画 |

---

**License**: Internal use within ZTL Construction Group
**Compatibility**: Claude Code v2.0+, Python 3.10+
