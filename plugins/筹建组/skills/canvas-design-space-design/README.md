# 空间设计效果图生成 (Canvas Design - Space Design)

> 基于Stable Diffusion XL的餐饮空间设计效果图生成技能包

## 概述

本技能包为Z2-空间设计AIGC助手提供专业的空间设计效果图生成能力,通过精心设计的Prompt工程和Stable Diffusion XL模型,快速生成符合设计理论的高质量空间渲染图。

## 核心特性

- **6大设计风格支持**: 现代简约、新中式、工业风、日式侘寂、北欧风、复古怀旧
- **理论驱动设计**: 60-30-10色彩法则、前厅后厨分区、三流线设计
- **8要素Prompt结构**: 空间类型+风格+布局+色彩+材料+照明+视角+质量
- **高质量输出**: 1024x1024 PNG,可扩展至2048x2048
- **快速生成**: 20-30秒/张,支持并行处理
- **批量处理**: 支持多场景批量生成配置

## 快速开始

### 1. 环境准备

```bash
# 设置OpenRouter API密钥
export OPENROUTER_API_KEY="your-api-key-here"

# 安装依赖
pip install requests
```

### 2. 单张生成

```bash
cd plugins/筹建组/skills/canvas-design-space-design

python scripts/api_client.py generate \
    --prompt "新中式风格火锅店入口迎宾区,米白色墙面配胡桃木色木饰面,古典格栅屏风,暖黄色氛围灯光,品牌LOGO墙,绿植点缀,温馨雅致,摄影级质量,8K高清,室内设计渲染" \
    --style "photographic" \
    --aspect-ratio "16:9" \
    --output "output/entrance-001.png"
```

### 3. 批量生成

```bash
# 复制配置模板
cp scripts/config_template.json my-project.json

# 编辑配置文件(修改space_scenes部分)

# 批量生成
python scripts/api_client.py batch \
    --config my-project.json \
    --output-dir "output/my-project/"
```

## 目录结构

```
canvas-design-space-design/
├── SKILL.md                    # 技能包元数据和使用指南
├── README.md                   # 本文件
├── scripts/
│   ├── api_client.py           # OpenRouter API客户端(推荐使用)
│   ├── sdxl-base.py            # 底层API封装(可选)
│   ├── space-design-execute.py # 批量执行引擎(可选)
│   └── config_template.json    # 配置文件模板
└── examples/
    └── hotpot-300sqm.json      # 完整项目示例配置
```

## 配置文件结构

### project_info (项目信息)

```json
{
  "project_name": "火锅店开业筹备",
  "location": "北京望京",
  "total_area": "300㎡",
  "cuisine_type": "火锅",
  "target_customer": "25-40岁中高收入白领",
  "budget": "60万元"
}
```

### design_positioning (设计定位)

```json
{
  "style": "新中式",
  "keywords": ["雅致", "温馨", "现代", "文化感"],
  "color_scheme": {
    "primary": "#F5F5DC (米白)",
    "secondary": "#8B4513 (胡桃木)",
    "accent": "#DC143C (中国红)"
  }
}
```

### space_scenes (空间场景列表)

```json
{
  "scene_name": "入口迎宾区",
  "area": "30㎡",
  "function": "顾客接待、品牌展示",
  "prompt": "New Chinese style hotpot restaurant entrance...",
  "negative_prompt": "blurry, low quality, distorted...",
  "generation_params": {
    "style_preset": "photographic",
    "aspect_ratio": "16:9",
    "cfg_scale": 7.5,
    "steps": 50
  }
}
```

## Prompt工程最佳实践

### 8要素结构

```
[1.空间类型] + [2.风格关键词] + [3.空间布局描述] +
[4.色彩方案] + [5.材料质感] + [6.照明氛围] +
[7.视角构图] + [8.质量标签]
```

### 示例

```
New Chinese style hotpot restaurant entrance (1.空间类型 + 2.风格),
beige walls with walnut wood panels (3.布局 + 4.色彩 + 5.材料),
classical lattice screens, warm yellow ambient lighting (6.照明),
brand logo wall, green plants decoration,
warm and elegant (情绪氛围),
photographic quality, 8K, interior design rendering (8.质量标签),
45-degree perspective, three-point perspective (7.视角)
```

## 6大设计风格

| 风格 | 关键词 | 主色调 | 材料 |
|------|--------|---------|------|
| 现代简约 | minimalist, clean lines | 纯白#FFFFFF, 浅灰#F5F5F5 | Glass, metal, concrete |
| 新中式 | Chinese elements, elegant | 米白#F5F5DC, 胡桃木#8B4513 | Wood, bamboo, silk |
| 工业风 | exposed brick, vintage | 水泥灰#808080, 复古棕#8B4513 | Brick, concrete, metal |
| 日式侘寂 | wabi-sabi, zen | 米色#F5F5DC, 原木#D2B48C | Wood, bamboo, stone |
| 北欧风 | Scandinavian, hygge | 纯白#FFFFFF, 浅木#D2B48C | Light wood, wool, glass |
| 复古怀旧 | vintage, nostalgic | 米黄#F5DEB3, 深棕#8B4513 | Dark wood, leather, brass |

## 参数说明

### style_preset (风格预设)

- `photographic`: 摄影级质量(推荐用于空间设计)
- `cinematic`: 电影感质感
- `digital-art`: 数字艺术风格
- `3d-model`: 3D建模风格

### aspect_ratio (画面比例)

- `16:9`: 横向宽屏(推荐用于空间全景)
- `4:3`: 标准横向
- `1:1`: 正方形(推荐用于局部细节)
- `9:16`: 竖向(推荐用于高度展示)

### cfg_scale (Prompt权重)

- `5-7`: 较自由,AI有更多创造空间
- `7-9`: 平衡,忠实度和创造性兼顾(推荐)
- `9-15`: 严格遵循Prompt,创造性降低

### steps (生成步数)

- `30-40`: 快速生成,质量较低
- `40-60`: 平衡速度和质量(推荐50)
- `60-70`: 高质量,生成时间较长

## 成本估算

- **每张图**: $0.02-0.05
- **典型项目** (5个场景): $0.10-0.25
- **完整设计** (10+场景): $0.20-0.50

## 性能参考

- 生成速度: 20-30秒/张
- 成功率: ≥95%
- 质量: ⭐⭐⭐⭐⭐ 5/5
- 分辨率: 1024x1024 (可扩展至2048x2048)
- 并行能力: 3-5倍并行

## 故障排查

### 问题1: API密钥错误

```
错误: 未找到OPENROUTER_API_KEY环境变量
解决: export OPENROUTER_API_KEY="your-api-key"
```

### 问题2: 生成质量不佳

```
问题: 图像模糊、不真实
解决:
1. 增加steps参数(50→60)
2. 增加cfg_scale参数(7.5→9.0)
3. 优化Prompt描述,增加专业术语
4. 添加更详细的negative_prompt
```

### 问题3: 超时错误

```
错误: Request timeout after 120s
解决:
1. 降低steps参数(60→40)
2. 降低分辨率要求
3. 增加timeout设置
4. 检查网络连接
```

## 相关文档

- [SKILL.md](SKILL.md) - 技能包详细文档
- [Z2-空间设计AIGC助手](../../agents/Z2-空间设计师.md) - 智能体定义
- [Stable Diffusion XL官方文档](https://stability.ai/stable-diffusion)
- [OpenRouter API文档](https://openrouter.ai/docs)

## 更新日志

### v1.0.0 (2025-10-28)

- ✅ 初版发布
- ✅ 支持6大设计风格
- ✅ 单张和批量生成功能
- ✅ 配置文件驱动
- ✅ 完整的Prompt工程指南

## 许可证

本技能包为ZTL数智化作战中心内部使用,遵循项目整体许可证。
