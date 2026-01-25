---
name: minimax-image-prompt-optimizer
description: Optimizes user input prompts for MiniMax Image Generation API (image-01) to produce high-quality professional images. Transforms creative briefs into structured prompts with subject descriptions, composition details, artistic style, and aspect ratio optimization. Specializes in restaurant industry visual content (menu designs, posters, social media graphics, store signage).
version: 1.0.0
author: ZTL Digital Intelligence Operations Center - 创意组
allowed-tools: ["Read", "Write"]
---

# MiniMax Image Prompt Optimizer

## 📋 Overview

This skill optimizes prompts for MiniMax Image Generation API (`mcp__minimax-mcp__text_to_image`), transforming user creative intentions into technically precise image generation requests that produce professional-quality visual content.

**Supported Model**:
- **image-01**: High-quality text-to-image generation with 8 aspect ratios

**Core Value**: Bridge the gap between creative vision ("I need a hotpot grand opening poster") and technical API requirements (structured prompts with subject + composition + style + lighting + colors).

## 🎯 Quick Start

### ⚡ 并发执行模式 (推荐)

**v2.0 升级**: 迁移至通用并发执行器,支持所有技能包,自动依赖分析,智能调度,3-5倍提速!

```python
from .claude.skills.幻影之舞.universal_concurrent_executor.scripts.core import execute_plan
from .claude.skills.幻影之舞.universal_concurrent_executor.adapters import MinimaxAdapter

# 创建适配器
adapter = MinimaxAdapter()

# 一行代码执行计划
report = execute_plan(
    plan_path="output/项目名/minimax/plans/execution_plan.json",
    adapter=adapter,
    max_workers=4,
    enable_dependency_analysis=True
)

print(f"✅ 成功: {report.successful_tasks}/{report.total_tasks}")
print(f"⏱️  总耗时: {report.total_duration_seconds:.2f}s")
```

**智能特性**:
- ✅ **自动依赖分析**: 检测任务间依赖关系 (显式 + 隐式)
- ✅ **分层并发执行**: 同层任务并发,层间串行
- ✅ **Prompt Optimizer 集成**: 自动优化图片生成提示词
- ✅ **进度追踪**: 实时日志 + 详细执行报告 (JSON)
- ✅ **错误处理**: 单任务失败不影响其他任务
- ✅ **通用架构**: 图片/音乐/视频/语音/数据处理/网页爬虫统一框架

**详细文档**: `.claude/skills/幻影之舞/universal-concurrent-executor/SKILL.md`

---

### 单任务模式 (传统方式)

```python
# Basic T2I usage - Poster
input = "火锅店开业海报"
optimized = optimize_image_prompt(input, design_type="poster")
# Output: {
#   "model": "image-01",
#   "prompt": "Grand opening poster for hotpot restaurant, vibrant red and gold colors, steaming hotpot center stage, lucky Chinese lanterns, bold '开业大吉' text, festive celebratory atmosphere, professional graphic design, 300 DPI quality",
#   "aspect_ratio": "2:3",
#   "n": 1,
#   "prompt_optimizer": true
# }

# Menu Design
input = "火锅菜单设计,展示牛肉、羊肉、蔬菜拼盘"
optimized = optimize_image_prompt(input, design_type="menu")
# Output: {
#   "prompt": "Professional hotpot menu design, beautifully plated beef slices, lamb rolls, vegetable platter, clean white background, elegant typography, appetizing food photography lighting, high-end restaurant style",
#   "aspect_ratio": "3:4"
# }

# Social Media Graphics
input = "抖音短视频封面图,限时优惠火锅套餐"
optimized = optimize_image_prompt(input, design_type="social-media")
# Output: {
#   "prompt": "Eye-catching social media graphic, limited-time hotpot deal, bold discount text '限时8.8折', appetizing hotpot close-up, vibrant colors, mobile-optimized design, attention-grabbing composition",
#   "aspect_ratio": "9:16"
# }
```

## 🎬 Core Capabilities

### 1. Design Type System (9 Categories)

**1-Poster (海报)**:
- **Aspect Ratio**: 2:3 (portrait) or 3:2 (landscape)
- **Use Case**: Grand openings, special events, seasonal promotions
- **Key Elements**: Bold headline, hero image, CTA, brand logo
- **Style**: Vibrant, festive, high-impact visual

**2-Menu (菜单)**:
- **Aspect Ratio**: 3:4 (portrait) or 4:3 (landscape)
- **Use Case**: Dish presentations, menu boards, digital menus
- **Key Elements**: Food photography, clean background, elegant typography
- **Style**: Appetizing, professional, high-end

**3-Social Media (社交媒体图)**:
- **Aspect Ratio**: 1:1 (Instagram), 9:16 (Stories/Reels/TikTok), 16:9 (YouTube)
- **Use Case**: Posts, Stories, video thumbnails
- **Key Elements**: Attention-grabbing, mobile-optimized, text overlay
- **Style**: Trendy, eye-catching, shareable

**4-Store Signage (店铺标识)**:
- **Aspect Ratio**: 16:9 (wide) or 21:9 (ultra-wide)
- **Use Case**: Outdoor signs, storefront banners, LED displays
- **Key Elements**: Brand logo, store name, tagline, visibility
- **Style**: Bold, readable from distance, weather-resistant look

**5-Coupon/Voucher (优惠券)**:
- **Aspect Ratio**: 3:2 or 4:3
- **Use Case**: Discount coupons, gift vouchers, loyalty rewards
- **Key Elements**: Offer details, QR code, expiry date, T&C
- **Style**: Professional, trustworthy, clear hierarchy

**6-Infographic (信息图表)**:
- **Aspect Ratio**: 3:4 (portrait) or 9:16 (vertical)
- **Use Case**: Nutritional info, cooking steps, brand story
- **Key Elements**: Data visualization, icons, clean layout
- **Style**: Informative, modern, easy to digest

**7-Product Showcase (产品展示)**:
- **Aspect Ratio**: 1:1 or 4:3
- **Use Case**: Dish highlights, ingredient spotlights, new items
- **Key Elements**: Hero product, clean background, studio lighting
- **Style**: Professional photography, appetizing, premium

**8-Event Invitation (活动邀请)**:
- **Aspect Ratio**: 2:3 or 3:4
- **Use Case**: Private events, VIP nights, chef's table
- **Key Elements**: Event details, RSVP info, elegant design
- **Style**: Sophisticated, invitation-worthy, formal

**9-Branding Material (品牌物料)**:
- **Aspect Ratio**: 1:1 or 3:2
- **Use Case**: Business cards, letterheads, packaging
- **Key Elements**: Logo, color palette, brand identity
- **Style**: Consistent, professional, brand-aligned

### 2. Aspect Ratio Optimization

**Supported Ratios (8 total)**:

| Ratio | Dimensions | Use Case |
|-------|------------|----------|
| **1:1** | Square | Instagram posts, profile pics, product photos |
| **16:9** | Landscape | YouTube thumbnails, presentation slides, website banners |
| **4:3** | Standard | Traditional menus, print materials, flyers |
| **3:2** | Photo | Professional photography, posters, coupons |
| **2:3** | Portrait | Posters, door hangers, vertical banners |
| **3:4** | Vertical | Mobile-first designs, Stories, infographics |
| **9:16** | Vertical | TikTok, Instagram Reels, mobile Stories |
| **21:9** | Ultra-wide | LED displays, storefront signage, panoramic views |

**Auto-Selection Logic**:
```yaml
Design Type → Aspect Ratio Mapping:
  poster: 2:3 (portrait poster)
  menu: 3:4 (vertical menu)
  social-media: 1:1 (Instagram default) or 9:16 (Stories/Reels)
  store-signage: 16:9 (wide banner) or 21:9 (ultra-wide LED)
  coupon: 3:2 (standard coupon)
  infographic: 9:16 (vertical infographic)
  product-showcase: 1:1 (square product photo)
  event-invitation: 2:3 (portrait invitation)
  branding: 1:1 (logo/icon) or 3:2 (business card)
```

### 3. Precise Prompt Formula

#### Restaurant Image Structure:
```
Subject + Composition + Artistic Style + Lighting + Colors + Quality Keywords
```

**Example (Poster)**:
```
Subject: "Grand opening celebration for Sichuan hotpot restaurant"
Composition: "Center-stage steaming hotpot, red lanterns framing, bold Chinese calligraphy"
Style: "Professional graphic design, festive celebratory mood"
Lighting: "Warm golden hour lighting, glowing lanterns"
Colors: "Vibrant red and gold, auspicious color scheme"
Quality: "300 DPI print quality, high-resolution photography"

Final Prompt:
"Grand opening celebration poster for Sichuan hotpot restaurant, center-stage steaming hotpot with rising steam, red Chinese lanterns framing the composition, bold calligraphy '开业大吉', warm golden hour lighting with glowing lanterns, vibrant red and gold auspicious color scheme, professional graphic design, festive celebratory atmosphere, 300 DPI print quality, high-resolution commercial photography"
```

### 4. Restaurant Industry Specialization

#### Hotpot Restaurant Templates

**Grand Opening Poster**:
```yaml
Prompt Template:
  "Grand opening [celebration/promotion] for [Sichuan/Mongolian/seafood] hotpot restaurant,
  [hero element: steaming hotpot/chef/signature dish],
  [decorative elements: red lanterns/gold coins/Chinese knots],
  [text: 开业大吉/grand opening],
  [lighting: warm golden hour/festive bright],
  [colors: vibrant red and gold/auspicious],
  [style: professional graphic design/festive celebratory],
  [quality: 300 DPI/high-resolution],
  [mood: inviting/exciting/lucky]"

Examples:
  - Sichuan Style: "Grand opening celebration for authentic Sichuan hotpot, bubbling red spicy broth center stage, vibrant chili peppers and Sichuan peppercorns, red lanterns and gold ingots, bold '开业大吉' calligraphy, warm ambient lighting, fiery red and gold color palette, professional poster design, appetizing and inviting atmosphere, 300 DPI print ready"

  - Mongolian Style: "Grand opening promotion for Mongolian copper hotpot restaurant, traditional copper pot with clear lamb broth, fresh lamb slices arrangement, Mongolian yurt pattern decorations, '盛大开业' text, warm cozy lighting, earthy brown and copper tones, rustic elegant style, high-quality photography, welcoming family atmosphere"
```

**Menu Design**:
```yaml
Prompt Template:
  "Professional [hotpot/Chinese cuisine] menu design,
  [dishes: beef slices/lamb rolls/vegetable platter],
  [background: clean white/dark moody/wooden texture],
  [typography: elegant serif/modern sans-serif],
  [lighting: appetizing food photography/studio soft box],
  [style: high-end restaurant/casual dining],
  [quality: commercial photography/300 DPI]"

Examples:
  - Premium Menu: "Luxury hotpot menu design, premium wagyu beef slices beautifully arranged, fresh seafood platter, organic vegetable selection, pristine white marble background, elegant gold serif typography, soft diffused studio lighting, high-end fine dining aesthetic, commercial food photography quality, mouth-watering presentation"

  - Casual Menu: "Friendly hotpot menu board, assorted meat platters (beef, lamb, pork), colorful vegetable trays, wooden table background, modern sans-serif font, natural daylight photography, casual family dining vibe, appetizing vibrant colors, clean menu design, print-ready 300 DPI"
```

**Social Media Graphics**:
```yaml
Prompt Template:
  "Eye-catching [social media platform] graphic for [promotion/announcement],
  [focal point: dish close-up/discount badge/event highlight],
  [text overlay: bold offer/catchy headline],
  [composition: mobile-optimized/attention-grabbing],
  [colors: vibrant/trendy/on-brand],
  [style: modern social media design/shareable content]"

Examples:
  - TikTok/Reels: "Vertical 9:16 TikTok video thumbnail, extreme close-up of bubbling Sichuan hotpot, bold text overlay '限时8.8折', vibrant red and orange color palette, dynamic steam effects, modern trendy design, mobile-first composition, attention-grabbing visual hook, shareable food content style"

  - Instagram Post: "Square Instagram post for hotpot special offer, top-down flat lay of colorful hotpot ingredients, circular hotpot arrangement, pastel pink and mint green trendy colors, '周末特惠' text in modern Chinese typography, Instagram-worthy aesthetic, foodie influencer style, high engagement visual"
```

#### Fine Dining Templates

**Tasting Menu Booklet**:
```yaml
Prompt: "Elegant tasting menu booklet cover, artistic plating of French cuisine, black matte background, minimalist gold typography, soft rim lighting, sophisticated luxury aesthetic, high-end restaurant branding, editorial photography quality, Michelin-star presentation"
```

**Wine Pairing Guide**:
```yaml
Prompt: "Wine pairing infographic poster, premium wine bottles with French labels, gourmet dish pairings, vertical 3:4 layout, classic serif fonts, dark moody photography, rich burgundy and gold tones, sommelier-approved design, educational yet elegant style"
```

#### Fast Food Templates

**Combo Meal Poster**:
```yaml
Prompt: "Energetic fast food combo meal poster, burger and fries hero shot, bright primary colors (red, yellow, blue), bold sans-serif text '超值套餐¥39.9', dynamic diagonal composition, high-energy young vibe, commercial product photography, appetite appeal focus"
```

**Mobile App Banner**:
```yaml
Prompt: "Mobile app promotion banner 16:9, smartphone mockup showing food ordering app, '下载APP享首单优惠' text, modern UI/UX design, tech-savvy aesthetic, clean minimal layout, app store ready graphics, digital-first composition"
```

#### Cafe Templates

**Seasonal Drink Menu**:
```yaml
Prompt: "Autumn seasonal drink menu board, cozy latte art coffee cups, falling maple leaves decoration, warm earth tones (brown, orange, cream), handwritten chalk-style typography, rustic wooden background, Instagram-worthy cafe aesthetic, inviting comfort feel"
```

**Loyalty Card Design**:
```yaml
Prompt: "Minimalist coffee loyalty card design 3:2, simple coffee bean icon, clean white background, elegant sans-serif font, stamp collection layout, premium card stock appearance, Scandinavian minimalist style, professional print design"
```

## 🔧 API Integration Points

### Input Schema
```python
{
  "creative_brief": str,         # Required: Raw user request
  "model": str,                  # Optional: "image-01" (default)
  "design_type": str,            # Optional: poster, menu, social-media, etc. (9 types)
  "restaurant_type": str,        # Optional: hotpot, fine-dining, fast-food, cafe
  "aspect_ratio": str,           # Optional: 1:1, 16:9, 4:3, 3:2, 2:3, 3:4, 9:16, 21:9
  "n": int,                      # Optional: Number of images (1-9, default 1)
  "artistic_style": str,         # Optional: professional, festive, trendy, elegant, rustic
  "color_palette": str,          # Optional: red-gold, earth-tones, pastel, monochrome
  "prompt_optimizer": bool       # Optional: Enable AI prompt enhancement (default true)
}
```

### Output Schema
```python
{
  "model": str,                  # "image-01"
  "prompt": str,                 # Optimized detailed prompt
  "aspect_ratio": str,           # Selected aspect ratio
  "n": int,                      # Number of images to generate
  "prompt_optimizer": bool,      # Whether prompt optimizer is enabled
  "analysis": {
    "detected_design_type": str, # poster / menu / social-media / etc.
    "detected_style": str,       # professional / festive / trendy / etc.
    "restaurant_context": str,   # hotpot / fine-dining / fast-food / cafe
    "composition_elements": list,# [subject, background, lighting, colors]
    "quality_keywords": list     # [300 DPI, high-resolution, commercial photography]
  },
  "api_params": {
    "model": "image-01",
    "prompt": str,
    "aspect_ratio": str,
    "n": int,
    "prompt_optimizer": bool,
    "output_directory": str
  },
  "optimization_notes": list[str]
}
```

## 📚 Best Practices

### Prompt Engineering Principles

#### 1. Subject Clarity
- ❌ Vague: "火锅海报"
- ✅ Clear: "Grand opening celebration poster for authentic Sichuan hotpot restaurant, steaming spicy red broth, fresh ingredients, festive atmosphere"

#### 2. Composition Details
- ❌ Missing: "菜单设计"
- ✅ Detailed: "Premium hotpot menu design, top-down flat lay of meat platters, clean white background, elegant gold typography, studio lighting"

#### 3. Artistic Style Specification
- ❌ Generic: "海报设计"
- ✅ Specific: "Professional graphic design poster, festive celebratory mood, modern Chinese aesthetics, commercial print quality"

#### 4. Color Palette Guidance
- ❌ No colors: "开业活动"
- ✅ Specified: "Grand opening event, vibrant red and gold auspicious color scheme, lucky festive palette, Chinese New Year vibes"

### Design Type Selection Strategy

```yaml
Decision Tree:

Need to attract attention? → poster or social-media
  Event/Promotion → poster (2:3 or 3:2)
  Social sharing → social-media (1:1 or 9:16)

Need to display products? → menu or product-showcase
  Multiple dishes → menu (3:4 or 4:3)
  Single hero dish → product-showcase (1:1)

Need information/data? → infographic or coupon
  Educational content → infographic (9:16)
  Discount offer → coupon (3:2)

Need brand identity? → branding or store-signage
  Logo/Icon → branding (1:1)
  Storefront → store-signage (16:9 or 21:9)

Need invitation? → event-invitation (2:3 or 3:4)
```

### Common Pitfalls to Avoid

1. **❌ Too Vague Prompts**
   - "Make a hotpot image"
   - **Fix**: Specify design type, purpose, style, colors

2. **❌ Wrong Aspect Ratio**
   - Using 1:1 for TikTok vertical video (should be 9:16)
   - **Fix**: Match ratio to platform/use case

3. **❌ Missing Quality Keywords**
   - Not mentioning "300 DPI" or "high-resolution" for print
   - **Fix**: Always add quality keywords for professional use

4. **❌ Ignoring Brand Colors**
   - Using random colors instead of brand palette
   - **Fix**: Specify brand colors or match restaurant type

5. **❌ Overcomplicating Composition**
   - Too many elements in one image
   - **Fix**: Keep it simple, focus on 1-2 hero elements

## 🚀 Workflow Integration

### Step 1: Receive Input
```python
# From X9-AIGC文生图 agent
raw_input = {
  "creative_brief": "火锅店开业海报,要喜庆的红色配色",
  "restaurant_type": "hotpot",
  "design_type": "poster"
}
```

### Step 2: Analyze & Select Parameters
```python
from scripts.optimizer import ImagePromptOptimizer

optimizer = ImagePromptOptimizer()

# Optimizer decides:
# - Design type: poster → aspect_ratio=2:3
# - Style: 开业 + 喜庆 → festive, celebratory
# - Colors: 红色 → vibrant red and gold
```

### Step 3: Optimize Prompt
```python
optimized = optimizer.optimize(raw_input)

# Output:
# {
#   "model": "image-01",
#   "prompt": "Grand opening celebration poster for Sichuan hotpot restaurant, center-stage steaming hotpot with rising steam, red Chinese lanterns framing, bold '开业大吉' calligraphy, warm golden lighting, vibrant red and gold auspicious colors, professional graphic design, festive atmosphere, 300 DPI print quality",
#   "aspect_ratio": "2:3",
#   "n": 1,
#   "prompt_optimizer": true
# }
```

### Step 4: Validate & Call API
```python
validated = optimizer.validate_for_api(optimized)

result = mcp__minimax-mcp__text_to_image(
  model=validated["model"],
  prompt=validated["prompt"],
  aspect_ratio=validated["aspect_ratio"],
  n=validated["n"],
  prompt_optimizer=validated["prompt_optimizer"],
  output_directory=f"output/{project_name}/X9-AIGC文生图/"
)
```

### Step 5: Return Results
```python
# X9 agent receives image file(s)
return {
  "status": "success",
  "image_files": result["file_paths"],
  "optimization_details": optimized["optimization_notes"],
  "design_type": optimized["analysis"]["detected_design_type"],
  "aspect_ratio": optimized["aspect_ratio"]
}
```

## 🧪 Testing & Quality Assurance

### Validation Checklist
```yaml
Prompt Quality:
  - [ ] Subject clearly described
  - [ ] Composition details specified
  - [ ] Artistic style included
  - [ ] Lighting described
  - [ ] Color palette specified
  - [ ] Quality keywords added (300 DPI, high-resolution)

Design Type:
  - [ ] Correct design type selected (9 types)
  - [ ] Aspect ratio matches use case
  - [ ] Style appropriate for type

Restaurant Fit:
  - [ ] Content matches restaurant type
  - [ ] Colors align with brand/type
  - [ ] Tone appropriate (festive/elegant/casual)

Technical Params:
  - [ ] aspect_ratio is valid (8 supported ratios)
  - [ ] n is between 1-9
  - [ ] prompt_optimizer enabled for best results
```

## 📖 Extended Documentation

See `reference.md` for:
- Complete MiniMax Image-01 API specification
- All 9 design type detailed templates
- 8 aspect ratio use case guide
- Advanced prompt engineering techniques
- Restaurant industry complete template library
- Edge case handling
- Batch generation strategies
- Troubleshooting guide

## 🔗 Related Components

- **X9-AIGC文生图 Agent**: Primary consumer of this skill
- **minimax-mcp**: MCP server providing `text_to_image` tool
- **Output Convention**: `output/[项目名]/X9-AIGC文生图/`

## 📝 Version History

- **v1.0.0** (2025-10-30): Initial release
  - Support for image-01 model
  - 9 design type system
  - 8 aspect ratio optimization
  - Restaurant industry templates
  - Precise prompt formula
  - API parameter validation
