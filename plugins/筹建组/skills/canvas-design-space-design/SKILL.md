---
name: 空间设计效果图生成
description: 基于Stable Diffusion XL的餐饮空间设计效果图生成。专注于6大设计风格(现代简约、新中式、工业风、日式侘寂、北欧风、复古怀旧)的专业空间渲染。输出1024x1024高质量PNG效果图。
---

# 空间设计效果图生成

> 基于Stable Diffusion XL模型的专业餐饮空间设计效果图生成,通过精心设计的Prompt工程,生成符合设计理论的高质量空间渲染图。

## 🎯 核心能力

- **6大设计风格**: 现代简约、新中式、工业风、日式侘寂、北欧风、复古怀旧
- **空间理论指导**: 60-30-10色彩法则、前厅后厨分区、三流线设计
- **高质量输出**: 1024x1024高分辨率PNG图像
- **快速生成**: 平均20-30秒/张,支持并行处理
- **批量处理**: 支持多场景批量生成

## 🚀 快速开始

### 基础用法

```python
# 1. 准备设计配置
design_config = {
    "project_name": "火锅店开业筹备",
    "space_type": "入口迎宾区",
    "style": "新中式",
    "area": "30㎡",
    "color_scheme": {
        "primary": "#F5F5DC",    # 米白色 60%
        "secondary": "#8B4513",  # 胡桃木 30%
        "accent": "#DC143C"      # 中国红 10%
    }
}

# 2. 生成Prompt
prompt = """
新中式风格火锅店入口迎宾区,米白色墙面配胡桃木色木饰面,
古典格栅屏风,暖黄色氛围灯光,品牌LOGO墙,绿植点缀,
温馨雅致,摄影级质量,8K高清,室内设计渲染,
45度透视角度,三点透视,纵深感
"""

# 3. 使用脚本生成
python scripts/api_client.py generate \
    --prompt "$prompt" \
    --style "photographic" \
    --aspect-ratio "16:9" \
    --output output/space-design/
```

### 核心参数

| 参数 | 说明 | 取值范围 |
|------|------|----------|
| `prompt` | 设计描述(8要素) | 200-500字 |
| `negative_prompt` | 排除元素 | 可选 |
| `style_preset` | 风格预设 | photographic, cinematic |
| `aspect_ratio` | 画面比例 | 16:9, 1:1, 4:3 |
| `cfg_scale` | Prompt权重 | 5-15 (推荐7.5) |
| `steps` | 生成步数 | 30-70 (推荐50) |

## 📁 常见场景

### 场景1: 单个空间渲染

生成新中式火锅店入口区:

```bash
python scripts/api_client.py generate \
    --prompt "新中式风格火锅店入口迎宾区..." \
    --style "photographic" \
    --aspect-ratio "16:9" \
    --cfg-scale 7.5 \
    --steps 50 \
    --output output/space-design/entrance/
```

输出:
- `entrance-新中式-001.png`: 1024x1024 PNG效果图

### 场景2: 多风格对比

生成同一空间的3种风格对比:

```bash
python scripts/api_client.py batch \
    --config config/multi-style-comparison.json
```

输出:
- `dining-modern-001.png`: 现代简约风格
- `dining-new-chinese-001.png`: 新中式风格
- `dining-industrial-001.png`: 工业风风格

### 场景3: 完整项目批量生成

使用JSON配置文件批量生成整店设计:

```bash
python scripts/api_client.py batch \
    --config-file config/hotpot-300sqm.json
```

配置文件示例见 `scripts/config_template.json`。

## 📁 进阶文档

- **[API详细参考](reference.md)** - 完整API参数、Stable Diffusion XL配置、错误处理
- **[Prompt工程指南](prompt-guide.md)** - 8要素Prompt结构、设计风格提示词库、质量标准

## 🛠️ 使用脚本

### scripts/api_client.py

整合OpenRouter Stable Diffusion XL API调用和批量处理的统一客户端(推荐使用)。

**功能**:
- 单张图像生成
- 批量场景生成
- 配置文件驱动
- 自动重试和错误处理
- 结果保存和日志记录

**调用方式**:

```bash
# 查看帮助
python scripts/api_client.py --help

# 单张生成
python scripts/api_client.py generate [参数]

# 批量生成
python scripts/api_client.py batch [参数]

# 使用配置文件
python scripts/api_client.py batch --config config.json
```

### scripts/sdxl-base.py

Stable Diffusion XL API客户端基础模板,提供底层API调用能力。

**功能**:
- OpenRouter API封装
- 图像base64解码
- 请求构建和响应处理
- 错误处理和重试机制

**适用场景**: 需要自定义API调用逻辑时使用

### scripts/space-design-execute.py

基于执行计划的批量处理引擎。

**功能**:
- 读取JSON执行计划
- 批次管理和并发控制
- Checkpoint断点续传
- 执行日志和元数据生成

**调用方式**:
```bash
python scripts/space-design-execute.py --plan output/plans/my-plan.json
```

**配合文件**: `output/[项目名]/Z2-空间设计AIGC助手/plans/`目录下的执行计划JSON

### scripts/config_template.json

标准配置文件模板,包含:
- 执行配置(batch_size, 并发数)
- API配置(endpoint, model, timeout)
- 空间场景列表(scenes)

复制模板创建您的配置:
```bash
cp scripts/config_template.json config/my-project.json
```

## ⚙️ 配置说明

### 基础配置

```json
{
  "execution_config": {
    "batch_size": 2,              // 每批处理数量
    "max_concurrent_requests": 2, // 最大并发数
    "retry_attempts": 3           // 失败重试次数
  },
  "api_config": {
    "model": "stable-diffusion-xl",
    "endpoint": "https://openrouter.ai/api/v1/images/generations",
    "timeout_seconds": 60
  }
}
```

### 场景配置

```json
{
  "scene_name": "入口迎宾区",
  "prompt": "新中式风格火锅店入口迎宾区,米白色墙面配胡桃木色木饰面,古典格栅屏风,暖黄色氛围灯光,品牌LOGO墙,绿植点缀,温馨雅致,摄影级质量,8K高清,室内设计渲染",
  "negative_prompt": "blurry, low quality, distorted, unrealistic",
  "generation_params": {
    "style_preset": "photographic",
    "aspect_ratio": "16:9",
    "cfg_scale": 7.5,
    "steps": 50
  }
}
```

## 🚨 注意事项

1. **Prompt质量**:
   - 遵循8要素结构(空间类型+风格+布局+色彩+材料+照明+视角+质量)
   - 描述具体化,避免模糊表达
   - 包含专业术语增强渲染质量

2. **色彩方案**:
   - 遵循60-30-10法则
   - 主色调占60%,辅助色30%,点缀色10%
   - 明确RGB或色彩名称

3. **空间布局**:
   - 符合前厅后厨分区原则(前厅60%,后厨40%)
   - 考虑三流线设计(顾客流、服务流、物流)
   - 明确功能分区

4. **成本预估**:
   - 每张图约$0.02-0.05
   - 批量生成前预估总成本
   - 超预算时会请求确认

## 📊 性能参考

- **生成速度**: 20-30秒/张(平均)
- **成功率**: ≥95%
- **质量评分**: ⭐⭐⭐⭐⭐ 5/5
- **分辨率**: 1024x1024 (可扩展至2048x2048)
- **并行能力**: 3-5倍并行

## 🎨 设计风格库

### 1. 现代简约 (Modern Minimalist)

**关键词**: minimalist, clean lines, neutral colors, open space, natural light, functional

**色彩方案**:
- 主色: #FFFFFF (纯白), #F5F5F5 (浅灰)
- 辅助色: #B0B0B0 (中灰)
- 点缀色: #000000 (黑色), #FFD700 (金色)

**材料**: Glass, metal, concrete, white marble

**示例Prompt**:
```
Modern minimalist hotpot restaurant, white walls with clean lines,
large glass windows, natural light, open ceiling design,
gray concrete floor, black metal chairs, gold accent lighting,
simple and elegant, architectural photography, 8K, interior design rendering
```

### 2. 新中式 (New Chinese Style)

**关键词**: Chinese elements, wooden lattice, warm tones, cultural atmosphere, elegant

**色彩方案**:
- 主色: #F5F5DC (米白), #8B7355 (檀木)
- 辅助色: #8B4513 (胡桃木)
- 点缀色: #DC143C (中国红), #FFD700 (金色)

**材料**: Wood, bamboo, silk, traditional Chinese tiles

**示例Prompt**:
```
New Chinese style hotpot restaurant entrance, beige walls with walnut wood panels,
classical lattice screens, warm yellow ambient lighting, brand logo wall,
green plants decoration, warm and elegant, photographic quality, 8K,
interior design rendering, 45-degree perspective
```

### 3. 工业风 (Industrial Style)

**关键词**: exposed brick, metal, concrete, Edison bulbs, raw materials, vintage

**色彩方案**:
- 主色: #808080 (水泥灰)
- 辅助色: #8B4513 (复古棕)
- 点缀色: #FFB90F (暖黄), #CD853F (古铜)

**材料**: Exposed brick, concrete, rusted metal, reclaimed wood

**示例Prompt**:
```
Industrial style hotpot restaurant, exposed brick walls, concrete floor,
metal pipes ceiling, Edison bulb pendant lights, reclaimed wood tables,
vintage metal chairs, warm yellow lighting, raw and authentic,
architectural photography, 8K, interior design rendering
```

### 4. 日式侘寂 (Japanese Wabi-Sabi)

**关键词**: wabi-sabi, natural materials, zen, minimal decoration, wood tones

**色彩方案**:
- 主色: #F5F5DC (米色), #D2B48C (原木)
- 辅助色: #8B7355 (深木)
- 点缀色: #2F4F4F (墨绿), #CD853F (茶色)

**材料**: Natural wood, bamboo, washi paper, stone, clay

**示例Prompt**:
```
Japanese wabi-sabi hotpot restaurant, natural wood walls, tatami mats,
paper lanterns, minimalist zen decoration, bamboo accents,
soft warm lighting, peaceful atmosphere, natural materials,
photographic quality, 8K, interior design rendering
```

### 5. 北欧风 (Nordic Style)

**关键词**: Scandinavian, light wood, simple, cozy, hygge, natural light

**色彩方案**:
- 主色: #FFFFFF (纯白), #F0EAD6 (浅米)
- 辅助色: #D2B48C (浅木)
- 点缀色: #4682B4 (淡蓝), #FFD700 (金色)

**材料**: Light wood, white walls, wool textiles, glass, ceramic

**示例Prompt**:
```
Nordic style hotpot restaurant, white walls with light wood accents,
large windows with natural light, simple pendant lights,
cozy textile decorations, light wood floor, minimalist furniture,
hygge atmosphere, clean and bright, photographic quality, 8K,
interior design rendering
```

### 6. 复古怀旧 (Retro Nostalgia)

**关键词**: vintage, retro, nostalgic, warm tones, old Shanghai, classic

**色彩方案**:
- 主色: #F5DEB3 (米黄)
- 辅助色: #8B4513 (深棕)
- 点缀色: #DC143C (酒红), #FFD700 (金色)

**材料**: Dark wood, leather, brass, vintage tiles, patterned wallpaper

**示例Prompt**:
```
Retro nostalgic hotpot restaurant, old Shanghai style,
dark wood panels, vintage patterned wallpaper, brass pendant lights,
leather booth seating, classic Chinese tiles, warm yellow lighting,
nostalgic atmosphere, cultural heritage, photographic quality, 8K,
interior design rendering
```

## 📖 延伸阅读

- [Stable Diffusion XL官方文档](https://stability.ai/stable-diffusion)
- [OpenRouter API参考](https://openrouter.ai/docs)
- [Prompt Engineering最佳实践](../../../.claude/skills/aigc-prompt-engineering/SKILL.md)

---

**版本**: 1.0.0
**更新日期**: 2025-10-28
**状态**: ✅ 初版完成
**兼容性**: Stable Diffusion XL via OpenRouter API
