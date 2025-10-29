---
name: nano-banana
description: Professional AIGC image generation and editing powered by Google Gemini 2.5 Flash Image. Supports text-to-image, image-to-image, editing, style transfer, multi-image composition, character consistency, and more. Includes intelligent prompt optimization for restaurant industry design scenarios.
---

# Nano-Banana AIGC 技能包

> 基于 Google Gemini 2.5 Flash Image (OpenRouter)
> 专业的 AIGC 图像生成和编辑能力,专为餐饮行业设计场景优化

## 🎯 核心能力矩阵

| 能力类型 | 能力描述 | 典型场景 |
|---------|---------|---------|
| **文生图** (Text-to-Image) | 从文本描述生成高质量图像 | 海报设计、产品图、宣传素材 |
| **图生图** (Image-to-Image) | 基于输入图像生成新图像 | 风格化处理、重新构图 |
| **图像编辑** (Editing) | 添加、删除或修改图像元素 | 去除水印、添加装饰、修改细节 |
| **风格迁移** (Style Transfer) | 将照片转换为特定艺术风格 | 照片转手绘、水彩化、卡通化 |
| **多图合成** (Multi-Composition) | 合成多张图像创建复合场景 | 产品多角度展示、场景融合 |
| **角色一致性** (Character Consistency) | 保持同一角色在不同场景的一致性 | 品牌吉祥物、IP角色设计 |
| **背景替换** (Background Replacement) | 替换图像背景 | 产品抠图、场景变换 |
| **局部优化** (Local Enhancement) | 精确优化图像特定区域 | 细节增强、局部修复 |

## 🚀 快速开始

### 基础文生图

```python
from pathlib import Path
from scripts.core_engine import NanoBananaExecutor

# 初始化执行器
executor = NanoBananaExecutor()

# 生成海报
result = executor.execute(
    user_prompt="火锅店开业庆典海报,红色主色调,喜庆氛围",
    task_type="text-to-image",
    context="餐饮行业海报设计",
    target_style="摄影级",
    project_name="火锅店开业筹备"
)

print(f"图像路径: {result['image_path']}")
```

**自动优化效果**:
- 原始: "火锅店开业庆典海报,红色主色调,喜庆氛围"
- 优化后: "Professional restaurant promotional poster design, 火锅店开业庆典海报, 喜庆red色主色调, 欢celebration氛围, ultra-realistic, photographic quality, 8K resolution, golden hour light, 85mm portrait lens, close-up, high-quality print resolution, attention-grabbing composition, clear hierarchy"

### 图像编辑

```python
from scripts.core_engine import ImageInput

# 准备输入图像
input_image = ImageInput(
    path="input/original_poster.jpg",
    description="原始火锅店海报"
)

# 执行编辑任务
result = executor.execute(
    user_prompt="删除左上角的水印,保持其他元素不变",
    task_type="editing",
    images=[input_image],
    project_name="海报优化"
)
```

### 风格迁移

```python
result = executor.execute(
    user_prompt="将这张照片转换为水彩画风格",
    task_type="style-transfer",
    target_style="水彩",
    images=[input_image],
    project_name="风格迁移实验"
)
```

### 多图合成

```python
# 准备多张输入图像
image1 = ImageInput(path="input/dish1.jpg", description="招牌毛肚")
image2 = ImageInput(path="input/dish2.jpg", description="特色鸭血")
image3 = ImageInput(path="input/store.jpg", description="门店外观")

result = executor.execute(
    user_prompt="将三张图片合成为一张宣传海报,展示菜品和门店",
    task_type="multi-composition",
    images=[image1, image2, image3],
    project_name="综合宣传海报"
)
```

## 📐 配置选项

### ImageConfig

控制图像生成的技术参数:

```python
from scripts.core_engine import ImageConfig

config = ImageConfig(
    aspect_ratio="16:9",  # 可选: 1:1, 16:9, 4:3, 3:2, 2:3, 3:4, 9:16, 21:9
    max_tokens=8192,      # 最大生成 token 数
    temperature=1.0,      # 创意度 (0.0-2.0)
    top_p=0.95,          # 采样策略
    seed=42              # 可复现性 (可选)
)

result = executor.execute(
    user_prompt="...",
    config=config
)
```

### PromptOptimizationConfig

控制提示词优化策略:

```python
from scripts.core_engine import PromptOptimizationConfig

opt_config = PromptOptimizationConfig(
    task_type="text-to-image",
    context="餐饮行业海报设计",          # 业务场景上下文
    target_style="摄影级",              # 目标风格
    requirements=[                      # 特殊要求列表
        "300 DPI高清",
        "可打印质量",
        "符合品牌调性"
    ]
)
```

## 🎨 餐饮行业专用优化

技能包内置餐饮行业设计模板,自动识别场景类型并优化提示词:

| 场景类型 | 自动识别关键词 | 优化策略 |
|---------|---------------|---------|
| **海报设计** | 海报、poster、宣传 | 添加专业海报设计前缀,强调高质量印刷和吸睛构图 |
| **菜单摄影** | 菜单、menu、菜品 | 添加美食摄影术语,强调诱人的食物造型和工作室光照 |
| **社交媒体** | 朋友圈、社交、social | 优化移动端构图,强调鲜艳配色和可分享的美学 |

## 📊 输出路径规范

遵循项目标准化输出路径:

```
output/[项目名]/nano-banana/
├── results/            # 生成的图像
│   ├── nano_banana_20250128_103000.png
│   └── nano_banana_20250128_103000_metadata.json
├── plans/             # 执行计划 (如使用JSON配置)
└── logs/              # 执行日志
```

## 🔧 高级用法

### 批量生成 (结合 JSON 计划)

创建 JSON 执行计划:

```json
{
  "project_name": "火锅店开业物料",
  "tasks": [
    {
      "id": "task_001",
      "user_prompt": "火锅店开业海报",
      "task_type": "text-to-image",
      "context": "餐饮行业海报设计",
      "target_style": "摄影级",
      "config": {
        "aspect_ratio": "2:3"
      }
    },
    {
      "id": "task_002",
      "user_prompt": "火锅店朋友圈宣传图",
      "task_type": "text-to-image",
      "context": "餐饮行业社交媒体",
      "config": {
        "aspect_ratio": "1:1"
      }
    }
  ]
}
```

使用批处理脚本执行 (可自行实现或参考 reference.md)

### 自定义提示词优化器

如需扩展优化器能力,可继承 `PromptOptimizer` 类:

```python
from scripts.core_engine import PromptOptimizer

class CustomOptimizer(PromptOptimizer):
    def _optimize_text_to_image(self, user_prompt, config):
        # 自定义优化逻辑
        return super()._optimize_text_to_image(user_prompt, config)
```

## ⚙️ 环境配置

### 必需环境变量

```bash
# OpenRouter API Key
export OPENROUTER_API_KEY="sk-or-v1-YOUR_API_KEY"
```

或在项目根目录创建 `.env` 文件:

```env
OPENROUTER_API_KEY=sk-or-v1-YOUR_API_KEY
```

### 依赖安装

```bash
pip install requests
```

## 💡 最佳实践

### 提示词编写技巧

1. **具体描述场景**,而非列举关键词
   - ✅ 好: "一家温馨的火锅店内,柔和的金色灯光照亮餐桌,顾客正在享用热气腾腾的火锅"
   - ❌ 差: "火锅店,灯光,餐桌,顾客"

2. **提供业务上下文**
   - 说明图像用途: "用于社交媒体推广的火锅店海报"
   - 说明品牌调性: "符合高端火锅品牌定位"

3. **使用摄影术语**控制视觉效果
   - 光照: "golden hour light", "soft diffused lighting"
   - 镜头: "85mm portrait lens", "wide-angle shot"
   - 构图: "close-up", "bird's eye view"

4. **避免SVG/网页风格 (海报设计专用)**
   - ✅ 好: "商业级海报摄影,拍摄于专业摄影棚,中画幅相机,杂志封面品质"
   - ❌ 差: "海报设计" (会被理解为矢量图/网页设计)
   - **关键**: 明确指定"摄影"、"拍摄"、"相机",避免抽象的"设计"术语

5. **参考风格引导 (强烈推荐)**
   - 使用现实世界的参考: "Nike广告牌风格", "Apple产品发布会海报", "米其林餐厅宣传照"
   - 避免: "专业设计", "高质量图片" (太模糊)

6. **迭代优化**
   - 先生成初版,再通过对话式提示微调
   - 例如: "make the lighting warmer", "add more red tones"

### 性能优化

- **复用提示词**: 相似任务使用相同的优化后提示词可节省 token
- **批量处理**: 使用 JSON 计划批量生成,减少初始化开销
- **合理设置 temperature**: 设计类任务建议 0.8-1.2,摄影类建议 0.5-0.8

### 成本控制

- **每张图像约 0.039 USD** (按 1290 输出 token 计算)
- **输入图像按分辨率计费**: 尽量压缩输入图像分辨率
- **合理使用 seed**: 测试阶段固定 seed 可避免重复生成

## 🐛 故障排除

### API 调用失败

**问题**: `ValueError: 未找到 OPENROUTER_API_KEY`
**解决**: 检查环境变量是否正确设置

**问题**: `requests.exceptions.HTTPError: 401`
**解决**: API Key 无效或已过期,请更新

### 图像提取失败

**问题**: "未能从响应中提取图像"
**解决**: 检查 API 响应格式是否变更,参考最新文档

### 生成质量不理想

**问题**: 生成的图像不符合预期
**解决**:
1. 增强提示词具体性
2. 调整 temperature 参数
3. 使用迭代优化策略

## 📚 相关资源

- **官方文档**: https://ai.google.dev/gemini-api/docs/image-generation
- **OpenRouter API**: https://openrouter.ai/google/gemini-2.5-flash-image/api
- **提示词最佳实践**: https://developers.googleblog.com/en/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/

## 🔄 更新日志

- **v1.0.0** (2025-01-28): 初始版本
  - 支持 8 种核心 AIGC 能力
  - 内置餐饮行业提示词优化器
  - 标准化输出路径
  - 完整的元数据追踪

---

**注意**: 本技能包遵循 ZTL 数智化作战中心的三层架构规范:
- **Layer 1 (规范层)**: 本文档 + reference.md
- **Layer 2 (计划层)**: JSON 执行计划 (可选)
- **Layer 3 (执行层)**: scripts/core_engine.py
