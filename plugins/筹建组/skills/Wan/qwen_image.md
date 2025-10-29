# Qwen-Image 文本渲染深度指南

> 中英文文本渲染行业领先(准确率≥98%),专为海报、标语、品牌设计等场景优化。

---

## 🎯 核心概念

### 什么是Qwen-Image?

Qwen-Image是通义万相推出的专业文本渲染模型,专注于在生成的图像中嵌入高质量的文字内容。

**核心优势**:
- **中英文渲染准确率≥98%**: 行业领先的文本识别和渲染能力
- **复杂中文字符精准识别**: 包含笔画复杂的繁体字、生僻字
- **英文文本高质量嵌入**: 支持多种字体和排版风格
- **原生多语言支持**: 中英文混合排版无缝集成

**适用场景**:
- 电影海报标题设计
- 品牌标语和口号生成
- 社交媒体营销图文
- 书籍封面文字设计
- 产品包装文字渲染

**与通用模型的差异**:

| 指标 | Qwen-Image | wanx2.2-t2i-flash |
|------|-----------|-------------------|
| **文本渲染准确率** | ≥98% | ~60-70% |
| **中文字符支持** | 完整支持 | 有限支持 |
| **英文文本质量** | 高质量 | 中等 |
| **复杂排版** | 支持 | 基础 |
| **成本** | ¥0.10/张 | ¥0.08/张 |
| **生成速度** | ~60-120秒 | ~60-120秒 |

**关键参数差异**:
```json
{
  "model": "qwen-image",  // 指定Qwen-Image模型
  "prompt_extend": false,  // 禁用自动优化,确保文本精确
  "style": "cinematic_poster"  // 可选预设风格
}
```

---

## 📋 参数详解

### 核心参数

#### model
**值**: `qwen-image`

**说明**: 必须指定为`qwen-image`才能启用文本渲染能力。

**示例**:
```json
{
  "model": "qwen-image"
}
```

---

#### prompt_extend
**值**: `true` | `false` (推荐: `false`)

**说明**:
- `false`: 严格按照提示词生成,确保文本内容精确
- `true`: 允许模型优化提示词,可能导致文本内容偏差

**最佳实践**: 文本渲染场景下**强烈推荐设置为`false`**,确保标题、标语完全按照指定内容生成。

**示例**:
```json
{
  "prompt_extend": false,
  "prompt": "Movie poster with title '未来都市2077' in bold futuristic font"
}
```

---

#### style
**值**: 17种预设风格(可选)

**说明**: 虽然Qwen-Image主要用于文本渲染,但仍可应用预设风格确保画面与文字风格统一。

**推荐风格**:
- `cinematic_poster`: 电影海报
- `realistic`: 写实风格品牌设计
- `flat_illustration`: 扁平插画风格
- `minimalism`: 极简主义设计

**示例**:
```json
{
  "style": "cinematic_poster",
  "prompt": "Sci-fi movie poster with title 'CYBERPUNK 2077' in neon glow font"
}
```

---

## 🎨 文本嵌入技巧

### 技巧1: 中文文本渲染

**挑战**: 中文字符笔画复杂,容易出现识别错误或模糊。

**解决方案**: 在提示词中明确指定文字内容、字体风格和排版位置。

**提示词结构**:
```
[场景描述] with title '[中文标题]' in [字体风格] font at [位置]
```

**示例1: 电影海报标题**
```json
{
  "model": "qwen-image",
  "prompt": "Cyberpunk movie poster with title '未来都市2077' in bold futuristic font at the top, dark cityscape background with neon lights",
  "size": "768*1024",
  "style": "cinematic_poster",
  "prompt_extend": false
}
```

**示例2: 品牌标语**
```json
{
  "model": "qwen-image",
  "prompt": "Minimalist brand poster with slogan '创新引领未来' in modern sans-serif font, centered on clean white background",
  "size": "1024*768",
  "style": "minimalism",
  "prompt_extend": false
}
```

**关键词选择**:
- **字体风格**: bold (粗体), modern (现代), futuristic (未来感), elegant (优雅), handwritten (手写)
- **位置**: at the top (顶部), centered (居中), at the bottom (底部), on the left (左侧)
- **效果**: neon glow (霓虹发光), metallic (金属感), 3D effect (立体效果)

---

### 技巧2: 英文文本渲染

**优势**: Qwen-Image对英文文本的渲染质量极高,支持多种字体和排版。

**提示词结构**:
```
[场景描述] with title '[英文标题]' in [字体风格] font, subtitle '[副标题]' below
```

**示例1: 科幻电影海报**
```json
{
  "model": "qwen-image",
  "prompt": "Epic sci-fi movie poster with title 'THE LAST FRONTIER' in bold metallic font at the top, subtitle 'A Journey Beyond Stars' in sleek modern font below, space background with planets and stars",
  "size": "768*1024",
  "style": "cinematic_poster",
  "prompt_extend": false
}
```

**示例2: 品牌广告**
```json
{
  "model": "qwen-image",
  "prompt": "Modern tech brand advertisement with title 'INNOVATE TODAY' in futuristic font, tagline 'Shape Tomorrow' below, minimalist blue gradient background",
  "size": "1024*768",
  "style": "realistic",
  "prompt_extend": false
}
```

---

### 技巧3: 中英文混合排版

**场景**: 双语海报、国际品牌设计、影视作品国际版。

**提示词结构**:
```
[场景描述] with Chinese title '[中文标题]' and English title '[英文标题]' in [排版方式]
```

**示例1: 双语电影海报**
```json
{
  "model": "qwen-image",
  "prompt": "Cyberpunk movie poster with Chinese title '未来都市' at the top in bold futuristic font, English title 'FUTURE CITY' below in metallic font, dark urban background with neon lights",
  "size": "768*1024",
  "style": "cyberpunk",
  "prompt_extend": false
}
```

**示例2: 双语品牌海报**
```json
{
  "model": "qwen-image",
  "prompt": "Luxury brand poster with Chinese slogan '品质生活' in elegant font at the center, English tagline 'Quality Life' below in refined serif font, minimalist beige background",
  "size": "1024*768",
  "style": "realistic",
  "prompt_extend": false
}
```

**排版方式**:
- **上下排列**: Chinese title at the top, English title below
- **左右排列**: Chinese on the left, English on the right
- **主副关系**: Chinese as main title, English as subtitle
- **对称布局**: Chinese and English mirrored on both sides

---

### 技巧4: 多行文本和长段落

**挑战**: 长文本容易导致排版混乱或文字模糊。

**解决方案**: 分段指定,明确行数和对齐方式。

**提示词结构**:
```
[场景描述] with first line '[第一行]', second line '[第二行]', third line '[第三行]' in [对齐方式]
```

**示例: 三行标语**
```json
{
  "model": "qwen-image",
  "prompt": "Motivational poster with first line 'DREAM BIG', second line 'WORK HARD', third line 'STAY FOCUSED' in bold uppercase font, centered alignment, gradient blue background",
  "size": "768*1024",
  "style": "minimalism",
  "prompt_extend": false
}
```

**对齐方式**:
- centered alignment (居中对齐)
- left alignment (左对齐)
- right alignment (右对齐)
- justified (两端对齐)

---

## 🚀 工作流程

### 工作流1: 电影海报标题设计

**目标**: 为科幻短片生成带有中文标题的电影海报

**场景**: 赛博朋克短片 - 未来都市2077

**步骤1: 确定文本内容和风格**
- **主标题**: 未来都市2077
- **副标题**: 在霓虹深处寻找真实
- **字体风格**: 粗体未来感字体
- **排版**: 主标题顶部,副标题居中

**步骤2: 编写提示词**
```json
{
  "model": "qwen-image",
  "prompt": "Cyberpunk movie poster with main title '未来都市2077' in bold futuristic font at the top, subtitle '在霓虹深处寻找真实' in sleek modern font at the center, dark cityscape background with neon lights and rain, cinematic composition",
  "size": "768*1024",
  "style": "cyberpunk",
  "prompt_extend": false,
  "n": 1
}
```

**步骤3: 验证和优化**
- 检查文本渲染准确性(是否所有字符正确)
- 评估字体风格与画面的协调性
- 如需调整,修改字体描述或排版位置

**预期效果**: 赛博朋克风格的电影海报,中文标题清晰准确,画面与文字风格统一。

---

### 工作流2: 品牌标语生成

**目标**: 为品牌设计带有标语的宣传海报

**场景**: 科技品牌 - 创新引领未来

**步骤1: 确定标语内容**
- **主标语**: 创新引领未来
- **副标语**: INNOVATION LEADS THE FUTURE
- **风格**: 现代极简

**步骤2: 编写提示词**
```json
{
  "model": "qwen-image",
  "prompt": "Modern tech brand poster with Chinese slogan '创新引领未来' in bold modern font at the top, English tagline 'INNOVATION LEADS THE FUTURE' in sleek font below, minimalist blue gradient background with subtle tech elements",
  "size": "1024*768",
  "style": "minimalism",
  "prompt_extend": false,
  "n": 1
}
```

**步骤3: 系列化设计**
- 保持相同的字体风格和排版
- 更换不同的背景色或元素
- 生成系列宣传物料

**预期效果**: 现代极简风格的品牌海报,中英文标语清晰,视觉冲击力强。

---

### 工作流3: 社交媒体营销图文

**目标**: 为社交媒体平台生成带有文字的营销图片

**场景**: 节日促销活动

**步骤1: 确定营销文案**
- **主标题**: 双11狂欢节
- **促销信息**: 全场5折起
- **行动号召**: 立即购买

**步骤2: 编写提示词**
```json
{
  "model": "qwen-image",
  "prompt": "E-commerce promotional banner with main title '双11狂欢节' in bold red font at the top, discount text '全场5折起' in large font at the center, call-to-action '立即购买' button at the bottom, vibrant red and gold background with festive elements",
  "size": "1024*768",
  "style": "flat_illustration",
  "prompt_extend": false,
  "n": 1
}
```

**步骤3: 多平台适配**
- 根据不同平台调整尺寸(微信公众号、微博、小红书)
- 保持文字内容和风格一致
- 快速批量生成

**预期效果**: 符合节日氛围的促销图片,文字信息清晰,吸引用户点击。

---

### 工作流4: 书籍封面文字设计

**目标**: 为小说设计带有书名和作者名的封面

**场景**: 科幻小说 - 《星际迷航》

**步骤1: 确定封面元素**
- **书名**: 星际迷航
- **作者**: 张三
- **风格**: 科幻写实

**步骤2: 编写提示词**
```json
{
  "model": "qwen-image",
  "prompt": "Sci-fi novel cover with book title '星际迷航' in bold futuristic font at the top, author name '张三 著' in elegant font at the bottom, space background with distant stars and planets, cinematic lighting",
  "size": "768*1024",
  "style": "realistic",
  "prompt_extend": false,
  "n": 1
}
```

**步骤3: 系列丛书设计**
- 保持统一的字体和排版风格
- 更换不同的背景和色调
- 形成视觉识别系统

**预期效果**: 专业的科幻小说封面,书名和作者名清晰,画面具有强烈的科幻氛围。

---

### 工作流5: 产品包装文字渲染

**目标**: 为产品包装设计带有品牌名和产品信息的图案

**场景**: 高端茶叶包装

**步骤1: 确定包装信息**
- **品牌名**: 云雾山茶
- **产品名**: 特级龙井
- **风格**: 中国风极简

**步骤2: 编写提示词**
```json
{
  "model": "qwen-image",
  "prompt": "Luxury tea packaging design with brand name '云雾山茶' in elegant Chinese calligraphy font at the top, product name '特级龙井' in refined font at the center, minimalist background with subtle tea leaves and mountain silhouette, traditional Chinese aesthetic",
  "size": "1024*1024",
  "style": "chinese_painting",
  "prompt_extend": false,
  "n": 1
}
```

**步骤3: 产品线扩展**
- 保持品牌名风格不变
- 更换产品名和配色
- 形成统一的品牌视觉

**预期效果**: 高端中国风茶叶包装,品牌名和产品名清晰,画面优雅大气。

---

## 💡 最佳实践

### 1. 文本准确性优化

**原则**: 确保生成的文字与指定内容完全一致。

**技巧**:

1. **禁用prompt_extend**:
   ```json
   {
     "prompt_extend": false
   }
   ```
   确保模型严格按照提示词生成,不会自行优化或添加内容。

2. **使用引号明确文本内容**:
   ```
   with title 'EXACT TEXT HERE' in bold font
   ```
   引号内的内容会被模型识别为精确文本。

3. **避免模糊描述**:
   - ❌ "with some Chinese text"
   - ✅ "with title '未来都市' in bold font"

4. **多次验证**:
   - 生成后仔细检查每个字符
   - 如有错误,重新生成或调整提示词

---

### 2. 字体选择策略

**不同场景的字体推荐**:

| 场景 | 推荐字体风格 | 英文描述 |
|------|------------|---------|
| **电影海报** | 粗体未来感字体 | bold futuristic font |
| **品牌标语** | 现代无衬线字体 | modern sans-serif font |
| **书籍封面** | 优雅衬线字体 | elegant serif font |
| **产品包装** | 精致书法字体 | refined calligraphy font |
| **社交媒体** | 活泼手写字体 | playful handwritten font |

**字体效果增强**:
- **霓虹发光**: neon glow font
- **金属质感**: metallic font
- **立体效果**: 3D embossed font
- **渐变色**: gradient color font

---

### 3. 排版布局优化

**布局原则**: 文字与画面协调,视觉层次清晰。

**黄金三分法**:
```
with title at the top third, subtitle at the center, tagline at the bottom third
```

**居中对称布局**:
```
with title centered on the canvas, symmetrical design
```

**左右分栏布局**:
```
with Chinese text on the left, English text on the right, divided layout
```

**多行文本间距**:
```
with first line at the top, second line at the center with proper spacing, third line at the bottom
```

---

### 4. 风格协调技巧

**原则**: 文字风格与画面风格保持一致。

**赛博朋克场景**:
```json
{
  "style": "cyberpunk",
  "prompt": "... with title in neon glow futuristic font, metallic effects ..."
}
```

**极简主义场景**:
```json
{
  "style": "minimalism",
  "prompt": "... with title in clean modern font, simple and elegant ..."
}
```

**中国风场景**:
```json
{
  "style": "chinese_painting",
  "prompt": "... with title in traditional calligraphy font, classical aesthetic ..."
}
```

**写实风格场景**:
```json
{
  "style": "realistic",
  "prompt": "... with title in bold serif font, professional and sophisticated ..."
}
```

---

### 5. 常见问题与解决方案

**问题1: 文本内容不准确**

**原因**:
- prompt_extend开启,模型自行优化了提示词
- 文本描述不够明确

**解决方案**:
- 设置`prompt_extend: false`
- 使用引号明确文本内容
- 重新生成并验证

---

**问题2: 文字模糊或难以辨认**

**原因**:
- 字体风格与画面背景对比度不足
- 文字尺寸过小

**解决方案**:
- 调整字体描述,增加粗体或发光效果
- 明确指定文字位置和尺寸
- 选择对比度更高的配色

**示例**:
```json
{
  "prompt": "... with title in bold white font with dark outline on dark background, high contrast ..."
}
```

---

**问题3: 中英文混合排版混乱**

**原因**:
- 未明确中英文的排版关系
- 字体风格冲突

**解决方案**:
- 明确指定中英文的相对位置
- 统一字体风格系列

**示例**:
```json
{
  "prompt": "... with Chinese title at the top in bold font, English title below in matching bold font, unified typographic style ..."
}
```

---

## 🎬 影视制作应用

### 案例1: 科幻短片系列海报

**项目**: 赛博朋克短片 - 未来都市三部曲

**需求**: 生成三张系列海报,每张带有不同的主标题和副标题。

**海报1: 第一部《觉醒》**
```json
{
  "model": "qwen-image",
  "prompt": "Cyberpunk movie poster with main title '未来都市·觉醒' in bold neon font at the top, subtitle '第一部：黎明前的黑暗' in sleek font below, dark cityscape with first light of dawn, character silhouette in foreground",
  "size": "768*1024",
  "style": "cyberpunk",
  "prompt_extend": false
}
```

**海报2: 第二部《抗争》**
```json
{
  "model": "qwen-image",
  "prompt": "Cyberpunk movie poster with main title '未来都市·抗争' in bold neon font at the top, subtitle '第二部:霓虹中的战斗' in sleek font below, action scene with neon lights and rain, intense atmosphere",
  "size": "768*1024",
  "style": "cyberpunk",
  "prompt_extend": false
}
```

**海报3: 第三部《新生》**
```json
{
  "model": "qwen-image",
  "prompt": "Cyberpunk movie poster with main title '未来都市·新生' in bold neon font at the top, subtitle '第三部：希望的曙光' in sleek font below, sunrise over futuristic city, hopeful mood",
  "size": "768*1024",
  "style": "cyberpunk",
  "prompt_extend": false
}
```

**优势**:
- 三张海报保持统一的字体风格和排版
- 主标题格式一致,副标题描述各部剧情
- 画面色调和氛围随剧情发展递进

---

### 案例2: 品牌视觉系统设计

**项目**: 科技品牌"星辰科技"视觉识别系统

**需求**: 生成品牌主海报、产品宣传海报、企业文化海报,统一视觉风格。

**品牌主海报**:
```json
{
  "model": "qwen-image",
  "prompt": "Modern tech brand poster with company name '星辰科技' in bold futuristic font at the top, tagline 'INNOVATE THE FUTURE' in sleek font below, minimalist blue gradient background with abstract tech elements, professional and sophisticated",
  "size": "1024*768",
  "style": "minimalism",
  "prompt_extend": false
}
```

**产品宣传海报**:
```json
{
  "model": "qwen-image",
  "prompt": "Product promotional poster with brand '星辰科技' small logo at the top, product name 'AI智能助手' in large modern font at the center, tagline '让生活更智能' below, clean white background with subtle AI visual elements",
  "size": "1024*768",
  "style": "minimalism",
  "prompt_extend": false
}
```

**企业文化海报**:
```json
{
  "model": "qwen-image",
  "prompt": "Corporate culture poster with brand '星辰科技' at the top, motto '创新·协作·卓越' in bold font at the center, minimalist design with abstract team collaboration visual, professional blue color scheme",
  "size": "1024*768",
  "style": "minimalism",
  "prompt_extend": false
}
```

**优势**:
- 统一的品牌视觉风格
- 不同海报有明确的信息层级
- 形成完整的品牌视觉识别系统

---

## 🔗 延伸阅读

- [通义万相API完整参考](reference.md) - 完整参数说明、模型对比、API端点详解
- [Composer框架指南](composer.md) - Composer深度指南、元素组合策略
- [丰富示例集](examples.md) - Qwen-Image实战案例、混合工作流

---

**最后更新**: 2025-10-19
**版本**: 1.0.0
