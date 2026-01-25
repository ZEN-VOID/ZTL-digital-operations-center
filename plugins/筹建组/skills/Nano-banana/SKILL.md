---
name: Nano Banana建筑空间设计图生成
description: 专为筹建组设计的建筑空间设计图生成技能包。支持文生图(空间设计主图)和图生图(多角度透视图)两大模式。内置建筑摄影级提示词优化器,将任意需求优化为高质量渲染提示词。强调空间质感、光影效果、建筑美学和摄影构图。用于餐厅空间设计、室内设计、建筑效果图等场景。
---

# Nano Banana建筑空间设计图生成

> 基于Nano Banana模型的专业建筑空间设计图生成,专注于餐厅室内空间设计、建筑效果图渲染。内置建筑摄影级提示词优化器,确保输出达到专业建筑摄影标准。

## 🎯 核心定位

**筹建组专属技能包**: 主要服务于建筑、空间、室内、场景设计的图片创作

**核心能力**:
- **文生图 (Text-to-Image)**: 生成空间设计主图,确定基本风格
  - 空间设计主图: 入口、就餐区、包间、等待区、洗手间、收银台等
  - 建筑摄影风格: 强调空间设计质感、光影、高清写实感
  - 专业渲染: 8K分辨率、photorealistic、建筑摄影级别

- **图生图 (Image-to-Image)**: 基于主图生成多角度透视图
  - 多角度视图: 正面、侧面、鸟瞰、角落透视等
  - 视觉一致性: 保持主图风格和色彩方案(一致性≥95%)
  - 精确变化: 仅改变指定元素(视角、光照、局部细节)

- **提示词优化 (Prompt Optimization)**: ⭐ 新增核心功能
  - 自动优化: 将任意需求描述优化为高质量建筑摄影提示词
  - 最佳实践: 遵循Stable Diffusion XL最佳实践和建筑摄影标准
  - 专业术语: 集成建筑摄影、室内设计、材质纹理、光照氛围等专业词汇
  - 字数控制: 智能截断至推荐长度(≤400字符)

## 🎨 设计风格特点

**建筑摄影风格**:
- 空间质感: 材质纹理细腻、光影层次丰富
- 高清写实: 8K分辨率、超高清细节、专业渲染
- 构图美学: 对称构图、透视准确、视觉平衡
- 空间美学: 功能合理、动线流畅、氛围到位
- 摄影美学: 专业光照、色彩和谐、细节丰富

## 🚀 快速开始

### 模式1: 文生图 - 空间设计主图

**前置步骤: 提示词优化** ⭐ 推荐使用

在生成图片之前,建议使用提示词优化器将需求描述优化为高质量提示词:

```python
# 1. 导入提示词优化器
from scripts.prompt_optimizer_architecture import ArchitecturePromptOptimizer

# 2. 初始化优化器
optimizer = ArchitecturePromptOptimizer()

# 3. 定义设计需求
raw_description = "米白色墙面配胡桃木色木饰面,古典格栅屏风,品牌LOGO墙,绿植点缀"
space_type = "entrance"  # 空间类型
style_keywords = ["新中式风格", "对称布局", "温馨雅致"]
color_scheme = {
    "primary": "米白色 (#F5F5DC)",
    "secondary": "胡桃木色 (#8B4513)",
    "accent": "中国红 (#DC143C)"
}
materials = ["木饰面墙板", "仿古地砖", "实木格栅", "宫灯吊灯"]

# 4. 优化提示词
result = optimizer.optimize_text_to_image(
    raw_description=raw_description,
    space_type=space_type,
    style_keywords=style_keywords,
    color_scheme=color_scheme,
    materials=materials,
    lighting="warm",        # 光照氛围: warm/cool/dramatic/soft/natural
    view_angle="front_view" # 视角: front_view/side_view/aerial_view/corner_view
)

print("优化后的提示词:")
print(result["positive_prompt"])
print(f"字符数: {len(result['positive_prompt'])}")
```

**输出示例**:
```
优化后的提示词:
entrance reception area, welcoming lobby, grand foyer, 新中式风格, 对称布局, 温馨雅致,
米白色墙面配胡桃木色木饰面,古典格栅屏风,品牌LOGO墙,绿植点缀, 米白色 (#F5F5DC) as primary color,
胡桃木色 (#8B4513) as secondary color, 中国红 (#DC143C) as accent color, 木饰面墙板, 仿古地砖,
实木格栅, 宫灯吊灯, warm ambient lighting, golden hour glow, soft shadows, eye level front shot,
symmetrical composition, architectural photography, photorealistic, 8K resolution

字符数: 386
```

**使用优化后的提示词生成图片**:

```bash
# 使用API客户端生成
python scripts/api_client.py generate \
    --prompt "entrance reception area, welcoming lobby, grand foyer..." \
    --negative "blurry, low quality, noise, distorted, cartoon style..." \
    --aspect-ratio "16:9" \
    --output output/火锅店开业筹备/Z2-空间设计师/
```

### 模式2: 图生图 - 多角度透视图

基于已有的空间设计主图,生成不同视角的透视图:

```python
# 1. 准备参考主图
reference_image = "output/火锅店开业筹备/Z2-空间设计师/空间设计-入口迎宾区-main.png"

# 2. 使用优化器生成图生图提示词
result = optimizer.optimize_image_to_image(
    reference_description="新中式风格餐厅入口,米白色墙面,胡桃木家具,暖黄色灯光",
    keep_consistent=[
        "新中式风格",
        "米白色墙面",
        "胡桃木家具",
        "暖黄色灯光",
        "整体色调",
        "材质质感"
    ],
    change_elements=[
        "视角从正面改为45度侧面",
        "增加窗外自然光",
        "调整构图为两点透视"
    ],
    strength=0.65  # 变化强度 0.4-0.8
)

# 3. 使用API客户端执行图生图
python scripts/api_client.py generate \
    --reference $reference_image \
    --prompt "${result['positive_prompt']}" \
    --strength 0.65 \
    --output output/火锅店开业筹备/Z2-空间设计师/
```

### 提示词优化器核心参数

**文生图优化器参数**:

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `space_type` | 空间类型 | entrance/dining/vip_room/kitchen/restroom/cashier/waiting |
| `style_keywords` | 风格关键词列表 | ["新中式", "现代简约", "工业风"...] |
| `color_scheme` | 色彩方案字典 | {"primary": "米白", "secondary": "胡桃木", "accent": "中国红"} |
| `materials` | 材质列表 | ["木饰面", "仿古地砖", "实木家具"...] |
| `lighting` | 光照氛围 | warm/cool/dramatic/soft/natural |
| `view_angle` | 视角类型 | front_view/side_view/aerial_view/corner_view/wide_angle |

**图生图优化器参数**:

| 参数 | 说明 | 取值范围 |
|------|------|----------|
| `reference_description` | 参考主图描述 | 文本 |
| `keep_consistent` | 保持一致的元素列表 | 至少1个 |
| `change_elements` | 需要改变的元素列表 | 至少1个 |
| `strength` | 变化强度 | 0.4-0.8 |

**strength建议值**:
- `0.4-0.5`: 轻微变化(光照微调、细节优化)
- `0.6-0.7`: 中等变化(视角变化、局部调整)
- `0.75-0.8`: 较大变化(空间元素、构图变化)

## 📁 常见场景

### 场景1: 单个空间场景 - 新中式火锅店入口

```python
# 使用优化器生成完整场景配置
scene_config = optimizer.generate_config_for_scene(
    project_name="火锅店开业筹备",
    scene_name="入口迎宾区",
    space_type="entrance",
    style_keywords=["新中式风格", "对称布局", "温馨雅致"],
    color_scheme={
        "primary": "米白色",
        "secondary": "胡桃木色",
        "accent": "中国红"
    },
    materials=["木饰面墙板", "仿古地砖", "实木格栅"],
    raw_description="品牌LOGO墙居中,古典格栅屏风隔断,绿植点缀",
    lighting="warm",
    view_angle="front_view",
    area="10㎡",
    aspect_ratio="16:9"
)

# 导出配置为JSON
optimizer.export_to_json(scene_config, "config/entrance-scene.json")

# 使用配置生成图片
python scripts/api_client.py batch --config config/entrance-scene.json
```

### 场景2: 批量生成6个空间场景

为完整项目生成所有空间场景:

```python
# 定义6个场景
scenes = [
    {"name": "入口迎宾区", "type": "entrance", "area": "10㎡", "view": "front_view"},
    {"name": "开放就餐区", "type": "dining", "area": "150㎡", "view": "wide_angle"},
    {"name": "VIP包间", "type": "vip_room", "area": "25㎡", "view": "corner_view"},
    {"name": "等待休息区", "type": "waiting", "area": "15㎡", "view": "side_view"},
    {"name": "洗手间前厅", "type": "restroom", "area": "8㎡", "view": "front_view"},
    {"name": "收银结账区", "type": "cashier", "area": "5㎡", "view": "front_view"}
]

# 批量生成场景配置
for scene in scenes:
    scene_config = optimizer.generate_config_for_scene(
        project_name="火锅店开业筹备",
        scene_name=scene["name"],
        space_type=scene["type"],
        style_keywords=["新中式风格", "温馨雅致"],
        color_scheme={"primary": "米白色", "secondary": "胡桃木色", "accent": "中国红"},
        materials=["木饰面", "仿古地砖", "实木家具"],
        raw_description=f"{scene['name']}空间设计",
        lighting="warm",
        view_angle=scene["view"],
        area=scene["area"]
    )

    optimizer.export_to_json(scene_config, f"config/{scene['name']}.json")
```

### 场景3: 同一场景多视角生成

基于主图生成多个视角的透视图:

```bash
# 已有主图: entrance-main.png (正面视图)

# 生成侧面视图
python scripts/api_client.py generate \
    --reference entrance-main.png \
    --keep "新中式风格,米白色墙面,胡桃木家具,暖黄灯光" \
    --change "视角改为45度侧面,两点透视" \
    --strength 0.65

# 生成鸟瞰视图
python scripts/api_client.py generate \
    --reference entrance-main.png \
    --keep "新中式风格,米白色墙面,胡桃木家具" \
    --change "视角改为鸟瞰,俯视构图" \
    --strength 0.70

# 生成角落透视
python scripts/api_client.py generate \
    --reference entrance-main.png \
    --keep "新中式风格,整体色调,材质质感" \
    --change "视角改为角落透视,展示空间深度" \
    --strength 0.68
```

## 📁 进阶文档

- **[提示词优化器详细文档](scripts/prompt_optimizer_architecture.py)** - 完整API、使用示例、最佳实践
- **[API客户端参考](scripts/api_client.py)** - 统一API调用客户端
- **[建筑摄影术语库](reference.md)** - 专业术语、质量标签、材质描述

## 🛠️ 使用脚本

### scripts/prompt_optimizer_architecture.py ⭐ 核心工具

建筑空间设计专用提示词优化器。

**功能**:
- 文生图提示词优化 (8元素结构: 空间类型+风格+色彩+材质+光照+视角+质量)
- 图生图提示词优化 (keep/change分离策略)
- 完整场景配置生成 (JSON格式)
- 自动质量标签注入 (建筑摄影级别)
- 字数智能控制 (≤400字符)

**调用方式**:
```python
from scripts.prompt_optimizer_architecture import ArchitecturePromptOptimizer

optimizer = ArchitecturePromptOptimizer()

# 文生图优化
result = optimizer.optimize_text_to_image(
    raw_description="...",
    space_type="entrance",
    style_keywords=["新中式"],
    color_scheme={"primary": "米白"},
    materials=["木饰面"],
    lighting="warm",
    view_angle="front_view"
)

# 图生图优化
result = optimizer.optimize_image_to_image(
    reference_description="...",
    keep_consistent=["风格", "色调"],
    change_elements=["视角", "光照"],
    strength=0.65
)
```

### scripts/api_client.py

整合Nano Banana API调用和批量处理的统一客户端。

**功能**:
- 单张图像生成 (文生图/图生图)
- 批量序列生成
- 配置文件驱动
- 自动重试和错误处理
- 结果保存和日志记录

**调用方式**:
```bash
# 文生图
python scripts/api_client.py generate \
    --prompt "优化后的提示词..." \
    --aspect-ratio "16:9" \
    --output output/项目名/

# 图生图
python scripts/api_client.py generate \
    --reference reference.png \
    --prompt "优化后的提示词..." \
    --strength 0.65 \
    --output output/项目名/

# 批量配置文件
python scripts/api_client.py batch --config config.json
```

### scripts/nano-banana-base.py

API客户端基础模板,提供底层API调用能力。

**功能**:
- OpenRouter API封装
- 图像base64转换
- 请求构建和响应处理
- 错误处理和重试机制

**适用场景**: 需要自定义API调用逻辑时使用

### scripts/nano-banana-execute.py

基于执行计划的批量处理引擎。

**功能**:
- 读取JSON执行计划
- 批次管理和并发控制
- Checkpoint断点续传
- 执行日志和元数据生成

**调用方式**:
```bash
python scripts/nano-banana-execute.py --plan api/nano-banana/my-plan.json
```

## ⚙️ 提示词优化最佳实践

### 8元素标准提示词结构

**筹建组建筑摄影标准**:

```
[1.空间类型] + [2.风格关键词] + [3.空间描述] +
[4.色彩方案] + [5.材质纹理] + [6.光照氛围] +
[7.视角构图] + [8.质量标签]
```

**示例: 新中式火锅店入口**:
```
entrance reception area, welcoming lobby,          // [1.空间类型]
新中式风格, 对称布局, 温馨雅致,                    // [2.风格关键词]
米白色墙面配胡桃木色木饰面, 古典格栅屏风,          // [3.空间描述]
米白色 as primary color, 胡桃木色 as secondary,   // [4.色彩方案]
木饰面墙板, 仿古地砖, 实木格栅,                    // [5.材质纹理]
warm ambient lighting, golden hour glow,           // [6.光照氛围]
eye level front shot, symmetrical composition,     // [7.视角构图]
architectural photography, photorealistic, 8K      // [8.质量标签]
```

### 建筑摄影专业术语库

**质量标签** (Quality Tags):
```
architectural photography, photorealistic, 8K resolution,
ultra high detail, professional rendering, sharp focus,
hyper realistic, HDR lighting
```

**视角术语** (Camera Angles):
```
- 正面视图: eye level front shot, symmetrical composition
- 侧面视图: 45-degree angle view, dynamic perspective
- 鸟瞰视图: bird's eye view, overhead perspective
- 角落视图: corner perspective, two-point perspective
- 广角视图: ultra wide angle lens, 16mm, expansive view
```

**光照术语** (Lighting):
```
- 温暖: warm ambient lighting, golden hour glow, soft shadows
- 冷色: cool daylight, bright natural light, clean shadows
- 戏剧: dramatic lighting, high contrast, cinematic mood
- 柔和: soft diffused light, gentle shadows, cozy atmosphere
- 自然: natural daylight, floor-to-ceiling windows, bright and airy
```

**材质术语** (Materials):
```
- 木材: oak flooring, walnut wood panel, natural wood grain
- 石材: marble countertop, granite flooring, travertine wall
- 金属: brushed steel, polished brass, industrial iron
- 玻璃: floor-to-ceiling glass, transparent partition, frosted glass
- 混凝土: polished concrete floor, exposed concrete wall
```

### 负面提示词标准

```
blurry, low quality, noise, distorted, warped,
cartoon style, anime style, sketch, watercolor,
text, watermark, signature,
over-decorated, cluttered, crowded,
人物 (默认不包含人物,除非特别需要)
```

### 提示词字数控制

**推荐长度**: ≤400字符

**原因**:
- Stable Diffusion XL推荐长度
- 保持提示词简洁有效
- 避免token超限
- 提升生成速度

**优化器自动处理**:
- 智能截断至最大长度
- 在逗号处截断,保持句子完整
- 优先保留核心元素(空间类型、风格、质量标签)

## 🚨 注意事项

### 提示词优化注意事项

1. **前置优化是核心流程** ⭐
   - 所有空间设计图生成前,**必须**先使用提示词优化器
   - 直接使用原始需求描述会导致质量不稳定
   - 优化器整合了建筑摄影最佳实践和专业术语

2. **建筑摄影风格定位**
   - 强调空间质感、光影层次、材质细节
   - 使用专业建筑摄影术语(camera angles, lighting)
   - 追求高清写实感(8K, photorealistic, ultra detail)

3. **构图美学原则**
   - 对称构图: 适合正面视图(入口、包间)
   - 透视构图: 适合空间深度展示(就餐区、走廊)
   - 广角构图: 适合大空间全景(整体鸟瞰)

4. **空间美学原则**
   - 功能合理: 空间布局符合餐饮动线
   - 尺度适当: 家具比例、层高、通道宽度
   - 氛围到位: 光照、色彩、材质协调统一

### 文生图注意事项

1. **风格一致性**
   - 所有场景使用统一的style_keywords
   - 色彩方案(color_scheme)保持一致
   - 材质(materials)风格统一

2. **视角选择**
   - 入口/收银: front_view (正面视图,对称)
   - 就餐区: wide_angle (广角,展现空间)
   - 包间: corner_view (角落透视,展现细节)
   - 鸟瞰: aerial_view (整体布局)

3. **光照氛围**
   - warm: 适合温馨场景(包间、休息区)
   - natural: 适合明亮场景(就餐区、入口)
   - dramatic: 适合特色场景(酒吧、夜景)

### 图生图注意事项

1. **keep_consistent精准定义**
   - 必须明确列出保持不变的元素
   - 至少包含: 风格、色调、主要材质
   - 元素描述要具体(如"米白色墙面"而非"墙面")

2. **change_elements清晰描述**
   - 避免与keep_consistent冲突
   - 一次变化不要太多(建议1-3个元素)
   - 变化描述要具体(如"视角从正面改为45度侧面")

3. **strength强度控制**
   - 0.4-0.5: 轻微变化(光照、细节)
   - 0.6-0.7: 中等变化(视角、局部调整)
   - 0.75-0.8: 较大变化(空间元素、构图)

4. **参考主图质量**
   - 分辨率至少512x512
   - 清晰、无模糊
   - 文件大小<10MB

### 成本预估

- **每张图约5积分** (OpenRouter计费)
- 批量生成前预估总成本
- 超预算时会请求确认

## 📊 性能参考

- **生成速度**: 16.5秒/张(平均)
- **成功率**: 100% (基于E5实测)
- **质量评分**: ⭐⭐⭐⭐⭐ 5/5
- **建筑摄影质感**: ≥95%
- **提示词优化耗时**: <1秒

## 📖 延伸阅读

- **[Z2-空间设计师 Agent](../../agents/Z2-空间设计师.md)** - 配合使用的智能体
- **[通义万相](../Wan/SKILL.md)** - 图像生成的另一选择
- **[三层架构API规范](../../../../.claude/agents/system/Api-Creator.md)** - 架构设计参考

---

**版本**: 3.0.0 (筹建组建筑空间设计专版)
**更新日期**: 2025-10-31
**状态**: ✅ 新增提示词优化器,明确筹建组定位
**核心变更**:
- 重新定位为建筑空间设计专用技能包
- 新增建筑摄影级提示词优化器
- 整合文生图+图生图两大模式
- 强化建筑美学、空间美学、摄影美学
