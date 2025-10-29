# 通义万相完整示例集

> 涵盖Text-to-Image、Composer控制、Qwen-Image文本渲染、图像编辑、混合工作流等6大类实战案例。

---

## 📋 目录

1. [Text-to-Image 基础生成](#example-1-text-to-image-基础生成)
2. [Composer 精细控制](#example-2-composer-精细控制)
3. [Qwen-Image 文本渲染](#example-3-qwen-image-文本渲染)
4. [图像编辑工作流](#example-4-图像编辑工作流)
5. [Composer + Qwen-Image 混合工作流](#example-5-composer--qwen-image-混合工作流)
6. [系列作品风格统一](#example-6-系列作品风格统一)

---

## Example 1: Text-to-Image 基础生成

### 场景: 赛博朋克都市夜景

**需求**: 生成赛博朋克风格的未来都市夜景概念图,用于影视项目前期设计。

**JSON完整配置**:
```json
{
  "plan_id": "tongyi-wanxiang-cyberpunk-city-20251019",
  "agent_id": "tongyi-wanxiang",
  "api_version": "v1",
  "execution_config": {
    "api_endpoint": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis",
    "timeout": 120000,
    "retry_limit": 3
  },
  "batches": [
    {
      "batch_id": "batch-001",
      "task_count": 1,
      "prompt_config": {
        "prompt": "Futuristic cyberpunk city at night, neon lights, flying cars, rain-soaked streets, towering skyscrapers with holographic advertisements, dark atmosphere with vibrant colors, cinematic composition",
        "negative_prompt": "blurry, low quality, bad anatomy, distorted, cartoon"
      },
      "parameters": {
        "model": "wanx2.2-t2i-flash",
        "size": "1024*768",
        "n": 4,
        "style": "cyberpunk",
        "prompt_extend": true,
        "watermark": false
      }
    }
  ]
}
```

**关键参数解析**:
- `model: wanx2.2-t2i-flash`: 使用通用模型,快速生成
- `size: 1024*768`: 横向构图,适合影视概念图
- `n: 4`: 生成4张变体,用于风格探索
- `style: cyberpunk`: 应用赛博朋克预设风格
- `prompt_extend: true`: 允许模型优化提示词,增强画面细节

**预期效果**:
- 赛博朋克风格的未来都市夜景
- 霓虹灯光、飞行汽车、全息广告等元素
- 4张不同构图和色调的变体
- 生成时间: ~60-120秒

**成本估算**: ¥0.08 × 4 = ¥0.32

---

## Example 2: Composer 精细控制

### 场景: 品牌视觉设计 - 科技感产品海报

**需求**: 为科技产品生成极简风格的海报,精确控制色彩、布局和材质。

**JSON完整配置**:
```json
{
  "plan_id": "tongyi-wanxiang-composer-product-20251019",
  "agent_id": "tongyi-wanxiang",
  "api_version": "v1",
  "execution_config": {
    "api_endpoint": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis",
    "timeout": 120000,
    "retry_limit": 3
  },
  "batches": [
    {
      "batch_id": "batch-001",
      "task_count": 1,
      "prompt_config": {
        "prompt": "Modern tech product on minimalist podium, sleek design, professional photography, clean background",
        "negative_prompt": "cluttered, messy, low quality, distorted"
      },
      "parameters": {
        "model": "wanx2.2-t2i-flash",
        "size": "768*1024",
        "n": 1,
        "style": "realistic",
        "prompt_extend": false,
        "watermark": false
      },
      "composer_config": {
        "color_palette": ["#0A84FF", "#FFFFFF", "#E5E5EA"],
        "layout": "center",
        "material": "metal",
        "semantic": "interior_design"
      }
    }
  ]
}
```

**关键参数解析**:
- `prompt_extend: false`: 严格按照提示词生成,确保Composer控制精确
- `composer_config`:
  - `color_palette: ["#0A84FF", "#FFFFFF", "#E5E5EA"]`: 蓝白灰配色,科技感强
  - `layout: center`: 居中构图,聚焦产品
  - `material: metal`: 金属质感,增强科技感
  - `semantic: interior_design`: 室内设计场景,专业感

**预期效果**:
- 极简风格的科技产品海报
- 蓝白灰色调,金属质感
- 居中构图,产品突出
- 专业摄影级画面

**成本估算**: ¥0.08 × 1 = ¥0.08

**Composer优势**: 相比纯提示词生成,Composer确保色彩、布局、材质完全符合品牌视觉规范。

---

## Example 3: Qwen-Image 文本渲染

### 场景: 电影海报 - 中文标题精准渲染

**需求**: 为科幻短片生成带有中文标题的电影海报,确保文字清晰准确。

**JSON完整配置**:
```json
{
  "plan_id": "tongyi-wanxiang-qwen-poster-20251019",
  "agent_id": "tongyi-wanxiang",
  "api_version": "v1",
  "execution_config": {
    "api_endpoint": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis",
    "timeout": 120000,
    "retry_limit": 3
  },
  "batches": [
    {
      "batch_id": "batch-001",
      "task_count": 1,
      "prompt_config": {
        "prompt": "Cyberpunk movie poster with main title '未来都市2077' in bold futuristic font at the top, subtitle '在霓虹深处寻找真实' in sleek modern font at the center, dark cityscape background with neon lights and rain, cinematic composition",
        "negative_prompt": "blurry text, unreadable text, low quality, distorted"
      },
      "parameters": {
        "model": "qwen-image",
        "size": "768*1024",
        "n": 1,
        "style": "cyberpunk",
        "prompt_extend": false,
        "watermark": false
      }
    }
  ]
}
```

**关键参数解析**:
- `model: qwen-image`: 使用Qwen-Image模型,确保中文文本准确率≥98%
- `prompt_extend: false`: 必须禁用,确保标题内容精确
- `prompt`: 使用引号明确标题内容,指定字体风格和位置

**预期效果**:
- 赛博朋克风格的电影海报
- 主标题"未来都市2077"清晰准确,粗体未来感字体
- 副标题"在霓虹深处寻找真实"居中,现代字体
- 画面与文字风格统一

**成本估算**: ¥0.10 × 1 = ¥0.10

**Qwen-Image优势**: 中文文本渲染准确率≥98%,远超通用模型的60-70%。

---

## Example 4: 图像编辑工作流

### 场景: 图像扩展 - 16:9转21:9超宽构图

**需求**: 将现有的16:9概念图扩展为21:9超宽屏构图,用于影视分镜设计。

**JSON完整配置**:
```json
{
  "plan_id": "tongyi-wanxiang-extend-20251019",
  "agent_id": "tongyi-wanxiang",
  "api_version": "v1",
  "execution_config": {
    "api_endpoint": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis",
    "timeout": 120000,
    "retry_limit": 3
  },
  "batches": [
    {
      "batch_id": "batch-001",
      "task_count": 1,
      "prompt_config": {
        "prompt": "Extend the image to the left and right, maintaining the cyberpunk city atmosphere and neon lighting style"
      },
      "parameters": {
        "model": "wanx2.5-image-edit",
        "task_type": "extend",
        "input_image_url": "https://cdn.example.com/original-image.jpg",
        "extend_config": {
          "direction": "horizontal",
          "extend_ratio_left": 0.3,
          "extend_ratio_right": 0.3
        }
      }
    }
  ]
}
```

**关键参数解析**:
- `model: wanx2.5-image-edit`: 使用图像编辑模型
- `task_type: extend`: 图像扩展任务
- `input_image_url`: 原图URL(必须公开可访问)
- `extend_config`:
  - `direction: horizontal`: 水平方向扩展
  - `extend_ratio_left: 0.3`: 左侧扩展30%
  - `extend_ratio_right: 0.3`: 右侧扩展30%

**预期效果**:
- 原16:9图像扩展为21:9超宽屏
- 左右两侧自然延伸,保持风格一致
- 适合电影分镜设计的超宽构图

**成本估算**: ¥0.10 × 1 = ¥0.10

**应用场景**: 16:9 → 21:9, 4:3 → 16:9, 1:1 → 16:9等构图转换。

---

## Example 5: Composer + Qwen-Image 混合工作流

### 场景: 品牌海报 - 精确色彩 + 中文标语

**需求**: 为品牌生成带有中文标语的海报,同时精确控制色彩和布局。

**JSON完整配置**:
```json
{
  "plan_id": "tongyi-wanxiang-hybrid-20251019",
  "agent_id": "tongyi-wanxiang",
  "api_version": "v1",
  "execution_config": {
    "api_endpoint": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis",
    "timeout": 120000,
    "retry_limit": 3
  },
  "batches": [
    {
      "batch_id": "batch-001",
      "task_count": 1,
      "prompt_config": {
        "prompt": "Modern tech brand poster with Chinese slogan '创新引领未来' in bold modern font at the top, English tagline 'INNOVATION LEADS THE FUTURE' in sleek font below, minimalist design with abstract tech elements",
        "negative_prompt": "blurry text, unreadable text, cluttered, messy"
      },
      "parameters": {
        "model": "qwen-image",
        "size": "1024*768",
        "n": 1,
        "style": "minimalism",
        "prompt_extend": false,
        "watermark": false
      },
      "composer_config": {
        "color_palette": ["#0A84FF", "#FFFFFF", "#F5F5F7"],
        "layout": "rule_of_thirds",
        "material": "plastic",
        "semantic": "futuristic_city"
      }
    }
  ]
}
```

**关键参数解析**:
- `model: qwen-image`: 确保中英文标语准确渲染
- `composer_config`: 精确控制色彩、布局、材质
  - `color_palette: ["#0A84FF", "#FFFFFF", "#F5F5F7"]`: 蓝白灰品牌色
  - `layout: rule_of_thirds`: 三分法构图,专业感强
  - `material: plastic`: 塑料质感,现代科技感
- `prompt_extend: false`: 确保文字内容精确

**预期效果**:
- 极简风格的品牌海报
- 中文标语"创新引领未来"清晰准确
- 英文标语"INNOVATION LEADS THE FUTURE"排版精美
- 蓝白灰品牌色精确还原
- 三分法构图,视觉平衡

**成本估算**: ¥0.10 × 1 = ¥0.10

**混合工作流优势**: 结合Composer的精确色彩控制和Qwen-Image的文本渲染能力,实现设计的完全可控。

---

## Example 6: 系列作品风格统一

### 场景: 科幻短片分镜系列 - 24小时时间序列

**需求**: 为科幻短片生成4个时间段的场景概念图,保持统一的美术风格。

**策略**: 使用固定的Composer配置,仅更改时间和光线描述。

**场景1: 清晨5:00**
```json
{
  "batch_id": "scene-01-dawn",
  "prompt_config": {
    "prompt": "Futuristic city at dawn, soft morning light, fog rolling over buildings, empty streets, quiet atmosphere, first light breaking through skyscrapers",
    "negative_prompt": "people, crowds, busy, bright neon lights"
  },
  "parameters": {
    "model": "wanx2.2-t2i-flash",
    "size": "1024*768",
    "n": 1,
    "style": "cyberpunk",
    "prompt_extend": true
  },
  "composer_config": {
    "color_palette": ["#FFB84D", "#4A4A4A", "#E8E8E8"],
    "layout": "rule_of_thirds",
    "material": "metal",
    "semantic": "futuristic_city"
  }
}
```

**场景2: 正午12:00**
```json
{
  "batch_id": "scene-02-noon",
  "prompt_config": {
    "prompt": "Futuristic city at noon, bright sunlight, clear sky, busy streets with flying cars, crowds of people, bustling atmosphere, vibrant city life",
    "negative_prompt": "dark, night, fog, empty"
  },
  "parameters": {
    "model": "wanx2.2-t2i-flash",
    "size": "1024*768",
    "n": 1,
    "style": "cyberpunk",
    "prompt_extend": true
  },
  "composer_config": {
    "color_palette": ["#FFB84D", "#4A4A4A", "#E8E8E8"],
    "layout": "rule_of_thirds",
    "material": "metal",
    "semantic": "futuristic_city"
  }
}
```

**场景3: 黄昏18:00**
```json
{
  "batch_id": "scene-03-dusk",
  "prompt_config": {
    "prompt": "Futuristic city at dusk, golden hour lighting, warm glow over buildings, neon lights starting to illuminate, rush hour traffic with flying cars, transition from day to night",
    "negative_prompt": "completely dark, completely bright, midday sun"
  },
  "parameters": {
    "model": "wanx2.2-t2i-flash",
    "size": "1024*768",
    "n": 1,
    "style": "cyberpunk",
    "prompt_extend": true
  },
  "composer_config": {
    "color_palette": ["#FFB84D", "#4A4A4A", "#E8E8E8"],
    "layout": "rule_of_thirds",
    "material": "metal",
    "semantic": "futuristic_city"
  }
}
```

**场景4: 深夜00:00**
```json
{
  "batch_id": "scene-04-midnight",
  "prompt_config": {
    "prompt": "Futuristic city at midnight, full neon illumination, rain-soaked streets reflecting colorful lights, vibrant nightlife, holographic advertisements everywhere, cyberpunk atmosphere at its peak",
    "negative_prompt": "daylight, sunshine, bright sky"
  },
  "parameters": {
    "model": "wanx2.2-t2i-flash",
    "size": "1024*768",
    "n": 1,
    "style": "cyberpunk",
    "prompt_extend": true
  },
  "composer_config": {
    "color_palette": ["#FFB84D", "#4A4A4A", "#E8E8E8"],
    "layout": "rule_of_thirds",
    "material": "metal",
    "semantic": "futuristic_city"
  }
}
```

**完整JSON配置** (包含所有4个场景):
```json
{
  "plan_id": "tongyi-wanxiang-series-24h-20251019",
  "agent_id": "tongyi-wanxiang",
  "api_version": "v1",
  "execution_config": {
    "api_endpoint": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis",
    "timeout": 120000,
    "retry_limit": 3
  },
  "batches": [
    {
      "batch_id": "scene-01-dawn",
      "task_count": 1,
      "prompt_config": {
        "prompt": "Futuristic city at dawn, soft morning light, fog rolling over buildings, empty streets, quiet atmosphere, first light breaking through skyscrapers",
        "negative_prompt": "people, crowds, busy, bright neon lights"
      },
      "parameters": {
        "model": "wanx2.2-t2i-flash",
        "size": "1024*768",
        "n": 1,
        "style": "cyberpunk",
        "prompt_extend": true,
        "watermark": false
      },
      "composer_config": {
        "color_palette": ["#FFB84D", "#4A4A4A", "#E8E8E8"],
        "layout": "rule_of_thirds",
        "material": "metal",
        "semantic": "futuristic_city"
      }
    },
    {
      "batch_id": "scene-02-noon",
      "task_count": 1,
      "prompt_config": {
        "prompt": "Futuristic city at noon, bright sunlight, clear sky, busy streets with flying cars, crowds of people, bustling atmosphere, vibrant city life",
        "negative_prompt": "dark, night, fog, empty"
      },
      "parameters": {
        "model": "wanx2.2-t2i-flash",
        "size": "1024*768",
        "n": 1,
        "style": "cyberpunk",
        "prompt_extend": true,
        "watermark": false
      },
      "composer_config": {
        "color_palette": ["#FFB84D", "#4A4A4A", "#E8E8E8"],
        "layout": "rule_of_thirds",
        "material": "metal",
        "semantic": "futuristic_city"
      }
    },
    {
      "batch_id": "scene-03-dusk",
      "task_count": 1,
      "prompt_config": {
        "prompt": "Futuristic city at dusk, golden hour lighting, warm glow over buildings, neon lights starting to illuminate, rush hour traffic with flying cars, transition from day to night",
        "negative_prompt": "completely dark, completely bright, midday sun"
      },
      "parameters": {
        "model": "wanx2.2-t2i-flash",
        "size": "1024*768",
        "n": 1,
        "style": "cyberpunk",
        "prompt_extend": true,
        "watermark": false
      },
      "composer_config": {
        "color_palette": ["#FFB84D", "#4A4A4A", "#E8E8E8"],
        "layout": "rule_of_thirds",
        "material": "metal",
        "semantic": "futuristic_city"
      }
    },
    {
      "batch_id": "scene-04-midnight",
      "task_count": 1,
      "prompt_config": {
        "prompt": "Futuristic city at midnight, full neon illumination, rain-soaked streets reflecting colorful lights, vibrant nightlife, holographic advertisements everywhere, cyberpunk atmosphere at its peak",
        "negative_prompt": "daylight, sunshine, bright sky"
      },
      "parameters": {
        "model": "wanx2.2-t2i-flash",
        "size": "1024*768",
        "n": 1,
        "style": "cyberpunk",
        "prompt_extend": true,
        "watermark": false
      },
      "composer_config": {
        "color_palette": ["#FFB84D", "#4A4A4A", "#E8E8E8"],
        "layout": "rule_of_thirds",
        "material": "metal",
        "semantic": "futuristic_city"
      }
    }
  ]
}
```

**关键参数解析**:
- **固定Composer配置**:
  - `color_palette: ["#FFB84D", "#4A4A4A", "#E8E8E8"]`: 金色、灰色、浅灰色,形成统一色调
  - `layout: rule_of_thirds`: 三分法构图,确保视觉平衡
  - `material: metal`: 金属质感,强化科幻氛围
  - `semantic: futuristic_city`: 未来都市场景
- **变化的Prompt**: 仅更改时间、光线、氛围描述
- **统一的尺寸和风格**: `size: 1024*768`, `style: cyberpunk`

**预期效果**:
- 4个时间段的场景保持统一的美术风格
- 色彩、布局、材质一致,仅光线和氛围变化
- 形成完整的24小时时间序列视觉叙事
- 适合影视分镜设计和场景规划

**成本估算**: ¥0.08 × 4 = ¥0.32

**系列化优势**: Composer确保了不同场景之间的风格统一性,是影视项目场景序列设计的理想选择。

---

## 💡 关键要点总结

### Composer vs. 纯Prompt

| 场景 | 推荐方式 | 原因 |
|------|---------|------|
| **风格探索** | 纯Prompt | 灵活性高,快速迭代 |
| **精确控制** | Composer | 色彩、布局、材质完全可控 |
| **系列作品** | Composer | 风格统一性强 |
| **品牌设计** | Composer | 符合品牌规范 |

### Qwen-Image vs. 通用模型

| 场景 | 推荐模型 | 原因 |
|------|---------|------|
| **中文文本渲染** | Qwen-Image | 准确率≥98% |
| **英文文本渲染** | Qwen-Image | 高质量字体和排版 |
| **无文本场景** | wanx2.2 | 更快速、成本更低 |
| **海报设计** | Qwen-Image | 确保标题准确 |

### 混合工作流最佳实践

1. **Composer + Qwen-Image**: 品牌海报、影视海报
2. **Text-to-Image + Extend**: 概念图扩展为宽屏
3. **Qwen-Image + Style Transfer**: 文本渲染后风格化
4. **Composer系列生成**: 影视分镜序列设计

---

## 🔗 延伸阅读

- [通义万相SKILL.md](SKILL.md) - 快速入门和核心能力
- [API详细参考](reference.md) - 完整参数说明和代码示例
- [Composer框架指南](composer.md) - 深度掌握Composer控制
- [Qwen-Image文本渲染指南](qwen_image.md) - 文本渲染技巧和最佳实践

---

**最后更新**: 2025-10-19
**版本**: 1.0.0
