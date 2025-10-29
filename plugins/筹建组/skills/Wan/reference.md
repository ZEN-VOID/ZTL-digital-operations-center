# 通义万相API详细参考

> 通义万相完整API参考文档,包含所有参数说明、模型对比、执行方式详解和成本优化策略。

---

## 📋 目录

1. [完整参数表](#完整参数表)
2. [模型版本对比](#模型版本对比)
3. [Prompt工程指南](#prompt工程指南)
4. [API端点详解](#api端点详解)
5. [JSON配置结构](#json配置结构)
6. [完整代码示例](#完整代码示例)
7. [错误处理](#错误处理)
8. [成本详细说明](#成本详细说明)

---

## 完整参数表

### 基础参数

| 参数 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|------|------|------|--------|------|------|
| **model** | string | ✅ | - | 模型版本 | wanx2.2-t2i-flash, qwen-image, wanx2.5-image-edit |
| **prompt** | string | ✅ | - | 文本描述 | "Futuristic city at night, cyberpunk style, neon lights" |
| **negative_prompt** | string | ❌ | "" | 反向提示词 | "low quality, blurry, distorted, ugly" |
| **size** | string | ❌ | 1024*1024 | 图像尺寸 | 768*1024, 1024*1024, 1024*768, {width}*{height} (768-1440px) |
| **n** | integer | ❌ | 1 | 生成数量 | 1-4 |
| **style** | string | ❌ | auto | 预设风格 | watercolor, anime, cyberpunk, realistic, oil_painting |
| **prompt_extend** | boolean | ❌ | true | 自动优化prompt | true, false |
| **watermark** | boolean | ❌ | false | 添加水印 | true, false |
| **ref_img** | string | ❌ | - | 参考图URL | 公开可访问的图像URL |
| **ref_strength** | float | ❌ | 0.5 | 参考图影响强度 | 0.0-1.0 |
| **ref_mode** | string | ❌ | refonly | 参考图模式 | repaint(重绘), refonly(参考) |

### Composer参数

**使用方式**: 在请求参数中添加 `parameters` 字段

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| **color_palette** | array | ❌ | RGB色彩方案 | ["#00F5FF", "#FF1493", "#9400D3"] |
| **layout** | string | ❌ | 构图布局 | rule_of_thirds, center, golden_ratio, diagonal, symmetry |
| **material** | string | ❌ | 材质纹理 | neon_glass, metal, wood, fabric, stone, plastic, ceramic |
| **semantic** | string | ❌ | 语义主题 | futuristic_city, natural_landscape, interior_design, character_portrait |

**Composer布局选项**:
- **rule_of_thirds**: 三分法构图,视觉重心分布在画面交叉点
- **center**: 中心构图,主体居中对称
- **golden_ratio**: 黄金比例构图,1.618比例分割
- **diagonal**: 对角线构图,动态视觉引导
- **symmetry**: 对称构图,稳定平衡

**Composer材质选项**:
- **neon_glass**: 霓虹玻璃质感,透明发光
- **metal**: 金属质感,高反光
- **wood**: 木质纹理,自然温暖
- **fabric**: 布料质感,柔软褶皱
- **stone**: 石质纹理,粗糙坚硬
- **plastic**: 塑料质感,光滑现代
- **ceramic**: 陶瓷质感,温润细腻

### Qwen-Image参数

**使用方式**: 设置 `model = "qwen-image"`

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| **prompt** | string | ✅ | 包含文本内容的描述 | "Cyberpunk poster with title '未来都市2077' and subtitle 'Welcome to the future'" |
| **text_position** | string | ❌ | 文本位置 | top, center, bottom, custom |
| **font_style** | string | ❌ | 字体风格 | bold, elegant, handwritten, modern |

**Qwen-Image最佳实践**:
- 中文字符准确率≥98%
- 英文文本高质量嵌入
- 支持复杂排版(多行、多段)
- 适用场景:海报标题、品牌标语、电影字幕、书籍封面

### 图像编辑参数

**使用方式**: 设置 `model = "wanx2.5-image-edit"` 并指定 `task_type`

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| **task_type** | string | ✅ | 编辑类型 | extend, remove_watermark, style_transfer, repair, beautify |
| **input_image_url** | string | ✅ | 原图URL | https://example.com/image.jpg |
| **extend_config** | object | ❌ | 扩展配置 | {"direction": "right", "ratio": 1.5} |
| **style_reference_url** | string | ❌ | 风格参考图URL | https://example.com/style.jpg |

**task_type选项**:

| 类型 | 说明 | 使用场景 | 额外参数 |
|------|------|----------|----------|
| **extend** | 图像扩展 | 扩展画布,保持主体 | extend_config: {"direction": "right/left/top/bottom", "ratio": 1.0-2.0} |
| **remove_watermark** | 去除水印 | 智能识别并去除水印 | - |
| **style_transfer** | 风格迁移 | 应用参考图风格 | style_reference_url |
| **repair** | 图像修复 | 修复破损、划痕 | - |
| **beautify** | 智能美化 | 色彩增强、细节优化 | - |

---

## 模型版本对比

| 模型 | 版本 | 速度 | 质量 | 成本 | 适用场景 |
|------|------|------|------|------|----------|
| **wanx2.2-t2i-flash** | 2.2 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ¥0.08/张 | 通用文生图,快速迭代,成本敏感项目 |
| **wanx2.1-t2i-plus** | 2.1 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ¥0.10/张 | 高质量生成,细节丰富,最终成品 |
| **qwen-image** | 专用 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ¥0.10/张 | 复杂文本渲染(中英文),海报标题,品牌标语 |
| **wanx2.5-image-edit** | 2.5 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ¥0.08/张 | 图像编辑(扩展、去水印、风格迁移、修复、美化) |
| **wan2.5-multimodal** | 2.5 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ¥0.20/张 | 音画同步视频生成(开发中) |
| **万相2.1开源** | 2.1 | ⭐⭐ | ⭐⭐⭐ | 免费 | 本地部署,FLF2V-14B开源模型 |

**选择策略**:

- **快速探索**: wanx2.2-t2i-flash (速度最快+成本最低)
- **高质量输出**: wanx2.1-t2i-plus (细节最丰富)
- **文本渲染**: qwen-image (中英文准确率≥98%)
- **图像编辑**: wanx2.5-image-edit (扩展、去水印、风格迁移)
- **本地部署**: 万相2.1开源 (FLF2V-14B,免费)

---

## Prompt工程指南

### Prompt结构模板

**基础结构**:
```
[主体] + [详细描述] + [环境/背景] + [光线/氛围] + [风格] + [质量关键词]
```

**示例**:
```
Prompt: A cyberpunk female hacker, wearing futuristic VR goggles and black leather jacket with neon circuit patterns, sitting in front of multiple holographic screens in a dark underground room, dramatic blue and purple neon lighting from monitors, cyberpunk aesthetic, highly detailed, 8K, cinematic composition

主体: A cyberpunk female hacker
详细描述: wearing futuristic VR goggles and black leather jacket with neon circuit patterns
环境: sitting in front of multiple holographic screens in a dark underground room
光线: dramatic blue and purple neon lighting from monitors
风格: cyberpunk aesthetic
质量关键词: highly detailed, 8K, cinematic composition
```

### 17种预设风格

| 风格 | 英文名 | 适用场景 | Prompt建议 |
|------|--------|----------|-----------|
| **水彩** | watercolor | 柔和艺术风格,自然场景 | 强调"soft colors, flowing brushstrokes" |
| **扁平插画** | flat_illustration | 现代设计,UI图标,简约风格 | 强调"simple shapes, bold colors, minimalist" |
| **动漫** | anime | 动漫角色,二次元风格 | 强调"anime style, manga art, cel shading" |
| **油画** | oil_painting | 经典艺术,质感丰富 | 强调"textured brushwork, rich colors, canvas" |
| **国画** | chinese_painting | 中国传统艺术,水墨风格 | 强调"ink wash, traditional Chinese art" |
| **3D卡通** | 3d_cartoon | 三维角色,游戏美术 | 强调"3D render, Pixar style, smooth lighting" |
| **素描** | sketch | 草图风格,线条艺术 | 强调"pencil sketch, line art, hand drawn" |
| **赛博朋克** | cyberpunk | 未来都市,霓虹美学 | 强调"neon lights, high-tech, dystopian" |
| **电影海报** | cinematic_poster | 电影视觉,戏剧化光影 | 强调"dramatic lighting, cinematic composition" |
| **写实** | realistic | 照片级真实感 | 强调"photorealistic, lifelike, detailed" |
| **抽象** | abstract | 抽象艺术,概念表达 | 强调"abstract shapes, conceptual, artistic" |
| **水墨** | ink_wash | 中国水墨画 | 强调"ink wash painting, traditional" |
| **波普艺术** | pop_art | 波普风格,鲜艳色彩 | 强调"pop art, bold colors, graphic design" |
| **印象派** | impressionism | 印象派绘画 | 强调"impressionist style, soft focus, light" |
| **超现实** | surrealism | 超现实主义,梦幻奇异 | 强调"surrealist, dreamlike, fantasy" |
| **极简** | minimalism | 极简主义,简洁优雅 | 强调"minimalist, simple, clean design" |
| **巴洛克** | baroque | 巴洛克艺术,华丽复杂 | 强调"baroque style, ornate, dramatic" |

### Negative Prompt建议

**通用反向提示词**:
```
low quality, blurry, distorted, ugly, deformed, disfigured, bad anatomy, bad proportions, extra limbs, cloned face, malformed limbs, missing arms, missing legs, fused fingers, too many fingers, long neck, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, ugly, blurry, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck
```

**针对性反向提示词**:

- **人物**: bad hands, extra fingers, deformed face, asymmetrical eyes
- **场景**: messy background, chaotic composition, unbalanced layout
- **风格**: inconsistent style, mixed styles, conflicting aesthetics

---

## API端点详解

### DashScope API

**Base URL**: `https://dashscope.aliyuncs.com`

**端点**:

| 功能 | 端点 | 方法 | 说明 |
|------|------|------|------|
| **文生图** | `/api/v1/services/aigc/text2image/image-synthesis` | POST | 文本生成图像 |
| **图像编辑** | `/api/v1/services/aigc/text2image/image-synthesis` | POST | 图像扩展、去水印等(指定task_type) |
| **任务查询** | `/api/v1/tasks/{task_id}` | GET | 查询异步任务状态 |

**认证方式**:

```bash
# 方式1: 环境变量
export DASHSCOPE_API_KEY="your-api-key"

# 方式2: HTTP Header
Authorization: Bearer {DASHSCOPE_API_KEY}
```

**请求头**:

```
Content-Type: application/json
Authorization: Bearer {DASHSCOPE_API_KEY}
X-DashScope-Async: enable  # 可选,启用异步模式
```

---

## JSON配置结构

### 完整JSON示例

```json
{
  "plan_id": "tongyi-wanxiang-cyberpunk-20251019",
  "agent_id": "TongyiWanxiang",
  "api_version": "2024-11-15",
  "execution_config": {
    "api_endpoint": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis",
    "api_key_env": "DASHSCOPE_API_KEY",
    "timeout": 120,
    "async_mode": false
  },
  "batches": [
    {
      "batch_id": 1,
      "generation_type": "text-to-image",
      "tasks": [
        {
          "task_id": "scene-001-base",
          "generation_mode": "text_to_image",
          "prompt_config": {
            "prompt": "Futuristic city at night, cyberpunk style, neon lights reflecting on wet streets, flying cars in the sky, towering skyscrapers with holographic advertisements, dramatic purple and blue lighting, highly detailed, 8K, cinematic composition",
            "negative_prompt": "low quality, blurry, distorted, ugly, deformed, bad anatomy, messy background"
          },
          "parameters": {
            "model": "wanx2.2-t2i-flash",
            "size": "1024*1024",
            "n": 4,
            "style": "cyberpunk",
            "prompt_extend": true,
            "watermark": false
          },
          "composer_config": {
            "enabled": false
          },
          "qwen_image_config": {
            "enabled": false
          }
        },
        {
          "task_id": "scene-001-composer",
          "generation_mode": "composer",
          "prompt_config": {
            "prompt": "Futuristic city at night, cyberpunk style",
            "negative_prompt": "low quality, blurry, messy background"
          },
          "parameters": {
            "model": "wanx2.2-t2i-flash",
            "size": "1024*1024",
            "n": 1,
            "style": "cyberpunk",
            "prompt_extend": false,
            "watermark": false,
            "color_palette": ["#00F5FF", "#FF1493", "#9400D3"],
            "layout": "rule_of_thirds",
            "material": "neon_glass",
            "semantic": "futuristic_city"
          },
          "composer_config": {
            "enabled": true,
            "color_palette": ["#00F5FF", "#FF1493", "#9400D3"],
            "layout": "rule_of_thirds",
            "material": "neon_glass",
            "semantic": "futuristic_city"
          },
          "qwen_image_config": {
            "enabled": false
          }
        },
        {
          "task_id": "scene-001-poster",
          "generation_mode": "qwen_image",
          "prompt_config": {
            "prompt": "Cyberpunk movie poster with title '未来都市2077' in bold futuristic font at the top, subtitle 'Welcome to the future' below the title, dark cityscape background with neon lights, cinematic composition",
            "negative_prompt": "low quality, blurry, text errors, misspelled words"
          },
          "parameters": {
            "model": "qwen-image",
            "size": "768*1024",
            "n": 1,
            "style": "cinematic_poster",
            "prompt_extend": false,
            "watermark": false
          },
          "composer_config": {
            "enabled": false
          },
          "qwen_image_config": {
            "enabled": true,
            "text_content": {
              "title": "未来都市2077",
              "subtitle": "Welcome to the future",
              "text_position": "top",
              "font_style": "bold"
            }
          }
        }
      ]
    }
  ],
  "output_config": {
    "save_directory": "output/tongyi-wanxiang/cyberpunk-20251019/",
    "filename_pattern": "{task_id}_{timestamp}.png",
    "download_immediately": true,
    "url_expiry_note": "URLs expire in 24 hours, download immediately"
  }
}
```

---

## 完整代码示例

### Python SDK (推荐)

**安装**:
```bash
pip install dashscope
```

**示例1: 基础文生图**

```python
import dashscope
from http import HTTPStatus

def generate_image_basic(prompt: str, style: str = "cyberpunk"):
    """基础文生图"""
    response = dashscope.ImageSynthesis.call(
        model='wanx2.2-t2i-flash',
        prompt=prompt,
        negative_prompt='low quality, blurry, distorted',
        size='1024*1024',
        n=1,
        style=style,
        prompt_extend=True,
        watermark=False
    )

    if response.status_code == HTTPStatus.OK:
        result = response.output.results[0]
        print(f"Image URL: {result.url}")
        return result.url
    else:
        print(f"Error: {response.code} - {response.message}")
        return None

# 使用
image_url = generate_image_basic(
    prompt="Futuristic city at night, cyberpunk style, neon lights",
    style="cyberpunk"
)
```

**示例2: Composer精细控制**

```python
def generate_image_composer(prompt: str):
    """使用Composer框架精细控制"""
    response = dashscope.ImageSynthesis.call(
        model='wanx2.2-t2i-flash',
        prompt=prompt,
        size='1024*1024',
        n=1,
        style='cyberpunk',
        parameters={
            'color_palette': ["#00F5FF", "#FF1493", "#9400D3"],
            'layout': 'rule_of_thirds',
            'material': 'neon_glass',
            'semantic': 'futuristic_city'
        }
    )

    if response.status_code == HTTPStatus.OK:
        return response.output.results[0].url
    else:
        print(f"Error: {response.code} - {response.message}")
        return None

# 使用
image_url = generate_image_composer(
    prompt="Futuristic city at night"
)
```

**示例3: Qwen-Image文本渲染**

```python
def generate_poster_with_text(title: str, subtitle: str):
    """使用Qwen-Image生成包含文本的海报"""
    prompt = f"Cyberpunk movie poster with title '{title}' in bold futuristic font at the top, subtitle '{subtitle}' below the title, dark cityscape background with neon lights"

    response = dashscope.ImageSynthesis.call(
        model='qwen-image',
        prompt=prompt,
        size='768*1024',
        n=1,
        style='cinematic_poster',
        prompt_extend=False
    )

    if response.status_code == HTTPStatus.OK:
        return response.output.results[0].url
    else:
        print(f"Error: {response.code} - {response.message}")
        return None

# 使用
poster_url = generate_poster_with_text(
    title="未来都市2077",
    subtitle="Welcome to the future"
)
```

**示例4: 图像编辑 - 图像扩展**

```python
def extend_image(input_image_url: str, direction: str = "right", ratio: float = 1.5):
    """扩展图像"""
    response = dashscope.ImageSynthesis.call(
        model='wanx2.5-image-edit',
        task_type='extend',
        input_image_url=input_image_url,
        extend_config={
            'direction': direction,
            'ratio': ratio
        }
    )

    if response.status_code == HTTPStatus.OK:
        return response.output.results[0].url
    else:
        print(f"Error: {response.code} - {response.message}")
        return None

# 使用
extended_url = extend_image(
    input_image_url="https://example.com/original.jpg",
    direction="right",
    ratio=1.5
)
```

### HTTP请求示例

```bash
curl -X POST \
  https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis \
  -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "wanx2.2-t2i-flash",
    "input": {
      "prompt": "Futuristic city at night, cyberpunk style, neon lights",
      "negative_prompt": "low quality, blurry, distorted"
    },
    "parameters": {
      "size": "1024*1024",
      "n": 1,
      "style": "cyberpunk"
    }
  }'
```

---

## 错误处理

### 常见错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| **400** | 请求参数错误 | 检查prompt、size、model等参数格式 |
| **401** | 认证失败 | 检查API Key是否正确设置 |
| **403** | 权限不足 | 确认账户是否已开通通义万相服务 |
| **429** | 请求频率超限 | 降低请求频率或升级配额 |
| **500** | 服务器内部错误 | 稍后重试或联系客服 |
| **504** | 请求超时 | 增加timeout或简化prompt |

### 错误处理最佳实践

```python
import dashscope
from http import HTTPStatus
import time

def generate_image_with_retry(prompt: str, max_retries: int = 3):
    """带重试机制的图像生成"""
    for attempt in range(max_retries):
        try:
            response = dashscope.ImageSynthesis.call(
                model='wanx2.2-t2i-flash',
                prompt=prompt,
                size='1024*1024',
                n=1
            )

            if response.status_code == HTTPStatus.OK:
                return response.output.results[0].url
            elif response.status_code == 429:
                # 频率限制,等待后重试
                wait_time = 2 ** attempt  # 指数退避
                print(f"Rate limit hit, waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"Error: {response.code} - {response.message}")
                if attempt < max_retries - 1:
                    time.sleep(1)

        except Exception as e:
            print(f"Exception: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(1)

    return None
```

---

## 成本详细说明

### 详细定价表

| 模型 | 基础价格 | 包月套餐 | 按量计费 | 成本优势 |
|------|---------|---------|---------|----------|
| **wanx2.2-t2i-flash** | ¥0.08/张 | 500张/¥30 (¥0.06/张) | ¥0.08/张 | 速度最快+成本最低 |
| **wanx2.1-t2i-plus** | ¥0.10/张 | 500张/¥40 (¥0.08/张) | ¥0.10/张 | 高质量输出 |
| **qwen-image** | ¥0.10/张 | - | ¥0.10/张 | 文本渲染专用 |
| **wanx2.5-image-edit** | ¥0.08/张 | - | ¥0.08/张 | 图像编辑 |

**计费说明**:
- 生成数量n=1-4时,按实际生成数量计费
- 失败的请求不计费
- URL有效期24小时,不下载会失效但已扣费

### 成本优化策略

**1. 选择合适的模型**:
- 探索阶段: wanx2.2-t2i-flash (¥0.08/张)
- 最终输出: wanx2.1-t2i-plus (¥0.10/张)
- 文本渲染: qwen-image (¥0.10/张)

**2. 使用Composer减少重复生成**:
- 固定color_palette、layout、material (减少30-50%重复生成)
- 精确控制设计元素 (提升首次成功率)

**3. 批量处理**:
- 一次请求n=4张 (相同prompt生成4个变体)
- 减少API调用次数 (节省网络开销)

**4. prompt_extend优化**:
- 简单场景: 关闭prompt_extend (节省token)
- 复杂场景: 开启prompt_extend (提升生成质量,减少重试)

**5. 下载策略**:
- URL有效期24小时,立即下载保存
- 使用OSS对象存储 (避免重复生成)

### 成本对比

**项目案例**: 生成100张赛博朋克风格概念图

| 方案 | 模型 | 策略 | 成本 | 时长 |
|------|------|------|------|------|
| **方案A** | wanx2.2-t2i-flash | 直接生成,n=1 | ¥8 | ~100分钟 |
| **方案B** | wanx2.2-t2i-flash | Composer精细控制,n=1 | ¥8 | ~100分钟 |
| **方案C** | wanx2.2-t2i-flash | 批量生成,n=4,筛选最佳 | ¥32 | ~25分钟 |
| **方案D** | wanx2.1-t2i-plus | 高质量生成,n=1 | ¥10 | ~120分钟 |

**推荐策略**: 方案B (Composer精细控制) - 成本低+质量稳定+可控性强

---

**最后更新**: 2025-10-19
**版本**: 1.0.0
