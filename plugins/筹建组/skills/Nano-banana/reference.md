# 建筑空间设计提示词模板库 (Architectural Photography Prompt Template Library)

> 本文档为Nano Banana建筑空间设计图生成提供完整的提示词工程参考资料,包括专业术语库、场景模板和优化检查清单。

---

## 📐 8元素标准提示词结构

**核心理念**: 模拟专业建筑摄影师的观察与描述方式,将空间设计需求转化为SDXL能理解的高质量提示词。

### 8元素构成

```yaml
1. 空间类型 (Space Type):
   作用: 明确场景定位,建立基础语境
   示例: "entrance reception area", "dining space", "private VIP room"

2. 风格关键词 (Style Keywords):
   作用: 定义整体设计风格
   示例: "新中式风格", "现代简约", "日式侘寂", "工业风"

3. 空间描述 (Space Description):
   作用: 核心设计需求的自然语言描述
   示例: "米白色墙面配胡桃木色木饰面,古典格栅屏风作为隔断"

4. 色彩方案 (Color Scheme):
   作用: 遵循60-30-10配色法则
   结构: "主色调 as primary color, 次色调 as secondary color, 点缀色 as accent color"
   示例: "米白色 as primary, 胡桃木色 as secondary, 中国红 as accent"

5. 材质纹理 (Materials & Textures):
   作用: 强调空间质感和触感
   示例: "木饰面墙板, 仿古地砖, 实木格栅, 丝绸灯罩"

6. 光照氛围 (Lighting Atmosphere):
   作用: 定义空间情绪和时间感
   示例: "warm ambient lighting, golden hour glow, soft shadows"

7. 相机构图 (Camera Composition):
   作用: 专业摄影视角和构图术语
   示例: "eye level front shot, symmetrical composition"

8. 质量标签 (Quality Tags):
   作用: 强化输出质量
   固定项: "architectural photography, photorealistic, 8K resolution,
            ultra high detail, professional rendering, sharp focus"
```

### 字数控制原则

- **推荐范围**: 300-400字符 (SDXL最优甜点区)
- **最大限制**: ≤400字符
- **截断策略**: 在逗号处智能截断,保持句子完整性
- **优先级**: 质量标签 > 空间类型 > 风格 > 其他

---

## 🎨 专业术语库

### 1. 空间类型关键词 (Space Type Keywords)

#### 1.1 餐饮空间

```yaml
入口迎宾区:
  英文: "entrance reception area, welcoming lobby, grand foyer"
  适用: 品牌LOGO墙、接待台、等候区

正餐区:
  英文: "dining space, restaurant interior, main seating area"
  适用: 大厅就餐区、卡座区、圆桌区

包间/VIP房:
  英文: "private dining room, VIP space, intimate setting"
  适用: 独立包间、宴会厅、贵宾室

明档厨房:
  英文: "open kitchen, culinary workspace, chef station"
  适用: 开放式操作台、档口、后厨展示区

洗手间前厅:
  英文: "restroom foyer, washroom entrance, powder room approach"
  适用: 洗手间入口走廊、洗手台区域

收银区:
  英文: "cashier counter, payment area, service desk"
  适用: 前台收银、结账区、服务台

等位区:
  英文: "waiting lounge, seating area, comfortable waiting space"
  适用: 候位沙发区、休息区
```

#### 1.2 其他建筑空间

```yaml
办公空间:
  - "open office layout, cubicle area, collaborative workspace"
  - "executive office, private meeting room, conference hall"

商业空间:
  - "retail storefront, boutique interior, showroom display"
  - "shopping mall atrium, commercial corridor"

居住空间:
  - "living room, family lounge, residential interior"
  - "master bedroom, bedroom suite, sleeping quarters"
  - "modern kitchen, culinary space, cooking area"
```

### 2. 风格关键词库 (Style Keywords Library)

#### 2.1 新中式风格 (New Chinese Style)

```yaml
核心关键词:
  - "新中式风格" / "Modern Chinese style"
  - "对称布局" / "symmetrical composition"
  - "现代雅致" / "contemporary elegance"
  - "东方美学" / "Eastern aesthetics"

特征元素:
  - "木格栅屏风" / "wooden lattice partition"
  - "宫灯吊灯" / "palace lantern chandelier"
  - "山水壁画" / "landscape mural"
  - "青花瓷装饰" / "blue and white porcelain accents"
  - "茶桌摆件" / "tea table ornaments"

色彩倾向:
  - 主色调: 米白色 (#F5F5DC), 象牙白 (#FFFFF0)
  - 次色调: 胡桃木色 (#8B4513), 乌木色 (#3C2F2F)
  - 点缀色: 中国红 (#DC143C), 青花蓝 (#1E90FF)

材质组合:
  - 木饰面墙板, 仿古地砖, 实木格栅
  - 丝绸灯罩, 大理石台面, 青铜摆件

参考提示词:
  "Modern Chinese style entrance, symmetrical layout, beige walls with
   walnut wood paneling, classic wooden lattice partition, palace
   lantern chandeliers, warm ambient lighting, eye level front shot"
```

#### 2.2 现代简约 (Modern Minimalist)

```yaml
核心关键词:
  - "现代简约风格" / "Modern minimalist style"
  - "简洁线条" / "clean lines"
  - "开放空间" / "open space layout"
  - "功能主义" / "functionalism"

特征元素:
  - "落地玻璃窗" / "floor-to-ceiling windows"
  - "隐藏式收纳" / "concealed storage"
  - "几何吊灯" / "geometric pendant lights"
  - "简约家具" / "minimalist furniture"

色彩倾向:
  - 主色调: 纯白 (#FFFFFF), 浅灰 (#D3D3D3)
  - 次色调: 深灰 (#696969), 黑色 (#000000)
  - 点缀色: 金属银 (#C0C0C0), 极简木色 (#D2B48C)

材质组合:
  - 抛光水泥地面, 玻璃隔断, 不锈钢装饰
  - 皮革沙发, 极简木饰面

参考提示词:
  "Modern minimalist dining room, clean lines, pure white walls,
   floor-to-ceiling glass windows, polished concrete floor, geometric
   pendant lights, natural daylight, 45-degree angle view"
```

#### 2.3 工业风 (Industrial Style)

```yaml
核心关键词:
  - "工业风格" / "Industrial style"
  - "裸露结构" / "exposed structure"
  - "原始质感" / "raw textures"
  - "复古机械感" / "vintage mechanical aesthetics"

特征元素:
  - "裸露砖墙" / "exposed brick wall"
  - "金属管道" / "metal piping"
  - "爱迪生灯泡" / "Edison bulb lighting"
  - "皮革座椅" / "leather seating"
  - "铁艺装饰" / "wrought iron accents"

色彩倾向:
  - 主色调: 水泥灰 (#808080), 砖红 (#B22222)
  - 次色调: 黑色 (#000000), 锈铁色 (#A0522D)
  - 点缀色: 铜色 (#B87333), 黄铜色 (#B5A642)

材质组合:
  - 裸露混凝土, 红砖墙, 金属管道
  - 皮革, 铁艺, 回收木材

参考提示词:
  "Industrial style restaurant, exposed brick walls, metal piping ceiling,
   Edison bulb string lights, polished concrete floor, leather booth
   seating, dramatic lighting, corner perspective"
```

#### 2.4 日式侘寂 (Japanese Wabi-Sabi)

```yaml
核心关键词:
  - "日式侘寂风格" / "Japanese Wabi-Sabi style"
  - "自然朴素" / "natural simplicity"
  - "禅意空间" / "zen atmosphere"
  - "不完美之美" / "beauty of imperfection"

特征元素:
  - "榻榻米" / "tatami flooring"
  - "障子门" / "shoji sliding doors"
  - "枯山水" / "dry landscape garden"
  - "陶瓷器具" / "ceramic tableware"
  - "竹制装饰" / "bamboo accents"

色彩倾向:
  - 主色调: 米色 (#F5F5DC), 和纸白 (#FAF0E6)
  - 次色调: 茶褐色 (#8B4513), 墨绿色 (#2F4F4F)
  - 点缀色: 朱红色 (#C41E3A), 竹青色 (#7CB342)

材质组合:
  - 实木地板, 和纸墙面, 竹制屏风
  - 陶瓷, 藤编, 手工纺织物

参考提示词:
  "Japanese Wabi-Sabi tea room, tatami flooring, shoji sliding doors,
   natural wood grain, ceramic tea set, soft diffused light, zen
   atmosphere, eye level front shot, calm and serene"
```

#### 2.5 北欧风 (Scandinavian/Nordic Style)

```yaml
核心关键词:
  - "北欧风格" / "Scandinavian style"
  - "温馨舒适" / "hygge coziness"
  - "功能美学" / "functional beauty"
  - "自然采光" / "natural lighting"

特征元素:
  - "原木家具" / "natural wood furniture"
  - "羊毛地毯" / "wool rug"
  - "几何图案" / "geometric patterns"
  - "绿植装饰" / "indoor plants"
  - "简约吊灯" / "minimalist pendant lamp"

色彩倾向:
  - 主色调: 奶白色 (#FAFAFA), 浅木色 (#D2B48C)
  - 次色调: 浅灰 (#D3D3D3), 浅蓝 (#ADD8E6)
  - 点缀色: 芥末黄 (#DAA520), 森林绿 (#228B22)

材质组合:
  - 浅色木地板, 白色墙面, 亚麻窗帘
  - 羊毛织物, 陶瓷, 玻璃

参考提示词:
  "Scandinavian style cafe, light oak flooring, white walls,
   floor-to-ceiling windows, natural daylight, cozy wool rug,
   indoor plants, minimalist pendant lamps, hygge atmosphere,
   bright and airy, eye level shot"
```

#### 2.6 复古怀旧 (Retro Nostalgia)

```yaml
核心关键词:
  - "复古怀旧风格" / "Retro nostalgia style"
  - "时代印记" / "vintage charm"
  - "岁月质感" / "aged textures"
  - "老物件" / "antique items"

特征元素:
  - "马赛克瓷砖" / "mosaic tiles"
  - "搪瓷灯罩" / "enamel lampshade"
  - "老式海报" / "vintage posters"
  - "铜质水龙头" / "brass faucets"
  - "皮质卡座" / "leather booth seating"

色彩倾向:
  - 主色调: 奶油黄 (#FFF8DC), 复古绿 (#8FBC8F)
  - 次色调: 咖啡色 (#8B4513), 砖红色 (#B22222)
  - 点缀色: 橙色 (#FF8C00), 薄荷绿 (#98FF98)

材质组合:
  - 马赛克瓷砖, 老木地板, 搪瓷装饰
  - 铜质五金, 皮革, 花纹壁纸

参考提示词:
  "Retro nostalgia diner, mosaic tile floor, vintage enamel lamps,
   leather booth seating, old movie posters, warm yellow lighting,
   aged wood paneling, brass fixtures, nostalgic atmosphere,
   eye level front shot"
```

### 3. 色彩方案库 (Color Scheme Library)

#### 3.1 60-30-10配色法则

```yaml
原则: 60%主色调 + 30%次色调 + 10%点缀色

示例1 - 新中式温暖配色:
  primary (60%): 米白色墙面、天花板
  secondary (30%): 胡桃木色家具、地板
  accent (10%): 中国红装饰画、抱枕

示例2 - 现代简约冷色调:
  primary (60%): 纯白墙面、天花板
  secondary (30%): 浅灰色地面、家具
  accent (10%): 黑色边框、金属装饰

示例3 - 工业风粗犷配色:
  primary (60%): 水泥灰墙面、地面
  secondary (30%): 红砖墙、深色木材
  accent (10%): 铜色管道、灯具
```

#### 3.2 常用色彩术语

```yaml
白色系:
  - 纯白 Pure White (#FFFFFF)
  - 象牙白 Ivory (#FFFFF0)
  - 米白 Beige (#F5F5DC)
  - 奶白 Off-white (#FAF0E6)

灰色系:
  - 浅灰 Light Gray (#D3D3D3)
  - 中灰 Medium Gray (#808080)
  - 深灰 Dark Gray (#696969)
  - 炭灰 Charcoal (#36454F)

木色系:
  - 浅木色 Light Wood (#D2B48C)
  - 胡桃木色 Walnut (#8B4513)
  - 乌木色 Ebony (#3C2F2F)
  - 橡木色 Oak (#CD853F)

其他常用色:
  - 中国红 Chinese Red (#DC143C)
  - 青花蓝 Blue and White Porcelain Blue (#1E90FF)
  - 芥末黄 Mustard Yellow (#DAA520)
  - 森林绿 Forest Green (#228B22)
```

### 4. 材质纹理库 (Materials & Textures Library)

```yaml
木材类 (Wood):
  - oak flooring (橡木地板)
  - walnut wood panel (胡桃木饰面)
  - natural wood grain texture (天然木纹理)
  - solid wood furniture (实木家具)
  - bamboo accents (竹制装饰)
  - reclaimed wood (回收木材)

石材类 (Stone):
  - marble countertop (大理石台面)
  - granite flooring (花岗岩地板)
  - travertine wall (洞石墙面)
  - polished stone surface (抛光石材表面)
  - terrazzo flooring (水磨石地面)

金属类 (Metal):
  - brushed steel (拉丝钢)
  - polished brass (抛光黄铜)
  - industrial iron (工业铁艺)
  - chrome fixtures (镀铬装置)
  - copper piping (铜质管道)

玻璃类 (Glass):
  - floor-to-ceiling glass (落地玻璃)
  - transparent glass partition (透明玻璃隔断)
  - frosted glass (磨砂玻璃)
  - reflective glass (反光玻璃)

混凝土类 (Concrete):
  - polished concrete floor (抛光混凝土地面)
  - exposed concrete wall (裸露混凝土墙)
  - industrial concrete finish (工业混凝土饰面)

纺织物类 (Fabric):
  - linen curtains (亚麻窗帘)
  - velvet upholstery (天鹅绒软包)
  - wool rug (羊毛地毯)
  - silk cushions (丝绸抱枕)
  - leather seating (皮革座椅)

瓷砖类 (Tiles):
  - mosaic tiles (马赛克瓷砖)
  - ceramic tiles (陶瓷砖)
  - vintage tiles (仿古砖)
  - subway tiles (地铁瓷砖)
```

### 5. 光照氛围库 (Lighting Atmosphere Library)

```yaml
温暖光照 (Warm Lighting):
  英文: "warm ambient lighting, golden hour glow, soft shadows"
  适用: 新中式、日式侘寂、复古怀旧
  特点: 营造温馨、舒适、亲切的氛围
  色温: 2700K-3000K

冷色光照 (Cool Lighting):
  英文: "cool daylight, bright natural light, clean shadows"
  适用: 现代简约、北欧风
  特点: 清爽、明亮、理性的氛围
  色温: 5000K-6500K

戏剧性光照 (Dramatic Lighting):
  英文: "dramatic lighting, high contrast, cinematic mood"
  适用: 工业风、高端餐厅
  特点: 强烈对比、电影感、艺术氛围
  技术: 聚光灯、侧光、背光

柔和散射光 (Soft Diffused Light):
  英文: "soft diffused light, gentle shadows, cozy atmosphere"
  适用: 日式侘寂、温馨家庭餐厅
  特点: 柔和、均匀、舒缓的氛围
  技术: 漫反射、柔光箱、纱帘过滤

自然日光 (Natural Daylight):
  英文: "natural daylight, floor-to-ceiling windows, bright and airy"
  适用: 北欧风、现代简约
  特点: 通透、健康、自然的氛围
  技术: 大窗户、天窗、玻璃幕墙
```

### 6. 相机构图术语库 (Camera Composition Terms)

#### 6.1 视角类型 (View Angles)

```yaml
正面平视 (Front View):
  英文: "eye level front shot, symmetrical composition"
  适用: 入口迎宾区、品牌展示墙、对称空间
  特点: 端庄、正式、强调对称美

侧面45度 (Side View):
  英文: "45-degree angle view, dynamic perspective"
  适用: 就餐区、包间、展示空间深度
  特点: 动态、有层次感、展示空间纵深

俯视鸟瞰 (Aerial View):
  英文: "bird's eye view, overhead perspective"
  适用: 整体空间布局、平面图风格、餐桌摆台
  特点: 全局视野、展示布局关系

转角透视 (Corner View):
  英文: "corner perspective, two-point perspective"
  适用: 室内整体空间、展示多个墙面
  特点: 立体感强、展示两个面的设计

广角镜头 (Wide Angle):
  英文: "ultra wide angle lens, 16mm, expansive view"
  适用: 小空间显大、展示完整场景
  特点: 视野宽广、空间感强
```

#### 6.2 构图技巧 (Composition Techniques)

```yaml
对称构图 (Symmetrical Composition):
  英文: "symmetrical composition, centered framing"
  适用: 新中式、现代简约
  特点: 平衡、稳定、正式感

三分法构图 (Rule of Thirds):
  英文: "rule of thirds composition, balanced layout"
  适用: 自然、舒适的空间
  特点: 视觉平衡、动态感

引导线构图 (Leading Lines):
  英文: "leading lines, perspective depth"
  适用: 长廊、通道、纵深空间
  特点: 引导视线、强调深度

框架构图 (Framing):
  英文: "natural framing, layered composition"
  适用: 通过门窗看室内
  特点: 层次感、聚焦主体
```

### 7. 质量标签库 (Quality Tags Library)

```yaml
建筑摄影标准 (Architectural Photography Standards):
  - architectural photography
  - photorealistic
  - professional rendering

分辨率与细节 (Resolution & Detail):
  - 8K resolution
  - ultra high detail
  - sharp focus
  - hyper realistic

摄影技术 (Photography Techniques):
  - professional camera work
  - high dynamic range (HDR)
  - color grading
  - lens correction

渲染质量 (Rendering Quality):
  - physically based rendering (PBR)
  - ray tracing
  - global illumination
  - realistic materials

负面提示词 (Negative Prompts):
  - blurry (模糊)
  - low quality (低质量)
  - noise (噪点)
  - distorted (扭曲)
  - warped (变形)
  - cartoon style (卡通风格)
  - anime style (动漫风格)
  - sketch (草图)
  - watercolor (水彩)
  - text (文字)
  - watermark (水印)
  - signature (签名)
  - over-decorated (过度装饰)
  - cluttered (杂乱)
  - crowded (拥挤)
  - 人物 (默认不包含人物)
```

---

## 🏗️ 完整场景模板 (Complete Scene Templates)

### 模板1: 新中式火锅店入口迎宾区

```yaml
项目名称: 火锅店开业筹备
场景名称: 入口迎宾区
空间类型: entrance
面积: 10㎡

用户原始需求:
  "需要一个新中式风格的入口,要有品牌LOGO墙,用格栅屏风做隔断,
   整体温馨雅致,米白色配胡桃木色"

优化后提示词 (386字符):
  entrance reception area, welcoming lobby, grand foyer, 新中式风格,
  对称布局, 现代雅致, 米白色墙面配胡桃木色木饰面,古典格栅屏风作为隔断,
  品牌LOGO墙居中,绿植点缀,温馨雅致, 米白色 (#F5F5DC) as primary color,
  胡桃木色 (#8B4513) as secondary color, 中国红 (#DC143C) as accent color,
  木饰面墙板, 仿古地砖, 实木格栅, 宫灯吊灯, warm ambient lighting,
  golden hour glow, soft shadows, eye level front shot, symmetrical
  composition, architectural photography, photorealistic, 8K resolution

负面提示词:
  blurry, low quality, noise, distorted, cartoon style, watermark,
  over-decorated, cluttered, 人物

生成参数:
  model: stable-diffusion-xl
  aspect_ratio: 16:9
  style_preset: photographic
  cfg_scale: 7.5
  steps: 50
```

### 模板2: 现代简约咖啡厅正餐区

```yaml
项目名称: 精品咖啡厅设计
场景名称: 正餐区
空间类型: dining
面积: 80㎡

用户原始需求:
  "现代简约风格的咖啡厅,要有落地窗,自然采光好,白色墙面,
   木色家具,整体明亮通透"

优化后提示词 (372字符):
  dining space, restaurant interior, seating area, 现代简约风格,
  简洁线条, 开放空间, 纯白墙面, floor-to-ceiling glass windows,
  natural daylight flooding in, 浅木色家具, 极简吊灯, 绿植装饰,
  纯白 (#FFFFFF) as primary color, 浅木色 (#D2B48C) as secondary color,
  黑色 (#000000) as accent color, polished concrete floor, glass partition,
  minimalist wood furniture, geometric pendant lights, natural daylight,
  bright and airy, 45-degree angle view, dynamic perspective,
  architectural photography, photorealistic, 8K resolution, sharp focus

负面提示词:
  blurry, low quality, cartoon style, cluttered, over-decorated, 人物

生成参数:
  model: stable-diffusion-xl
  aspect_ratio: 3:2
  style_preset: photographic
  cfg_scale: 7.0
  steps: 50
```

### 模板3: 工业风烧烤店VIP包间

```yaml
项目名称: 烧烤店室内设计
场景名称: VIP包间
空间类型: vip_room
面积: 25㎡

用户原始需求:
  "工业风的包间,要有裸露砖墙和金属管道,皮质卡座,
   爱迪生灯泡照明,营造粗犷但精致的氛围"

优化后提示词 (378字符):
  private dining room, VIP space, intimate setting, 工业风格, 裸露结构,
  原始质感, exposed red brick wall, metal piping ceiling, Edison bulb
  string lights, leather booth seating, 铁艺装饰, 水泥灰 (#808080) as
  primary color, 砖红 (#B22222) as secondary color, 铜色 (#B87333) as
  accent color, polished concrete floor, industrial metal fixtures,
  reclaimed wood table, wrought iron accents, dramatic lighting,
  high contrast, cinematic mood, corner perspective, two-point perspective,
  architectural photography, photorealistic, 8K resolution

负面提示词:
  blurry, low quality, cartoon style, over-decorated, clean and sterile, 人物

生成参数:
  model: stable-diffusion-xl
  aspect_ratio: 4:3
  style_preset: photographic
  cfg_scale: 8.0
  steps: 50
```

### 模板4: 日式侘寂茶室

```yaml
项目名称: 日式茶室设计
场景名称: 茶室主空间
空间类型: dining
面积: 15㎡

用户原始需求:
  "日式侘寂风格的茶室,榻榻米,障子门,自然光线,
   简朴宁静的氛围,陶瓷茶具"

优化后提示词 (365字符):
  dining space, tea room, intimate setting, 日式侘寂风格, 自然朴素,
  禅意空间, tatami flooring, shoji sliding doors, natural wood grain,
  ceramic tea set, bamboo accents, 米色 (#F5F5DC) as primary color,
  茶褐色 (#8B4513) as secondary color, 竹青色 (#7CB342) as accent color,
  natural wood flooring, washi paper walls, bamboo partition, ceramic ware,
  handwoven textiles, soft diffused light, gentle shadows, cozy atmosphere,
  zen and serene, eye level front shot, symmetrical composition,
  architectural photography, photorealistic, 8K resolution

负面提示词:
  blurry, low quality, bright colors, modern furniture, cluttered, 人物

生成参数:
  model: stable-diffusion-xl
  aspect_ratio: 1:1
  style_preset: photographic
  cfg_scale: 7.0
  steps: 50
```

---

## 📝 风格完整配置模板 (Complete Style Configuration Templates)

### 配置模板1: 新中式风格全场景套装

```python
# 新中式火锅店 - 完整7场景配置

from scripts.prompt_optimizer_architecture import ArchitecturePromptOptimizer

optimizer = ArchitecturePromptOptimizer()

# 全局风格配置
project_name = "新中式火锅店开业筹备"
style_keywords = ["新中式风格", "对称布局", "现代雅致", "温馨舒适"]
color_scheme = {
    "primary": "米白色 (#F5F5DC)",
    "secondary": "胡桃木色 (#8B4513)",
    "accent": "中国红 (#DC143C)"
}
base_materials = ["木饰面墙板", "仿古地砖", "实木家具"]
lighting = "warm"  # 全场景温暖光照

# 场景1: 入口迎宾区
scene1 = optimizer.generate_config_for_scene(
    project_name=project_name,
    scene_name="入口迎宾区",
    space_type="entrance",
    style_keywords=style_keywords,
    color_scheme=color_scheme,
    materials=base_materials + ["实木格栅", "宫灯吊灯"],
    raw_description="品牌LOGO墙居中,古典格栅屏风隔断,绿植点缀",
    lighting=lighting,
    view_angle="front_view",
    area="10㎡",
    aspect_ratio="16:9"
)

# 场景2: 正餐区大厅
scene2 = optimizer.generate_config_for_scene(
    project_name=project_name,
    scene_name="正餐区大厅",
    space_type="dining",
    style_keywords=style_keywords,
    color_scheme=color_scheme,
    materials=base_materials + ["实木圆桌", "软包椅子", "中式吊灯"],
    raw_description="圆桌布局,软包座椅,中式吊灯,山水壁画装饰",
    lighting=lighting,
    view_angle="corner_view",
    area="120㎡",
    aspect_ratio="3:2"
)

# 场景3: VIP包间
scene3 = optimizer.generate_config_for_scene(
    project_name=project_name,
    scene_name="VIP包间",
    space_type="vip_room",
    style_keywords=style_keywords + ["私密雅致"],
    color_scheme=color_scheme,
    materials=base_materials + ["实木茶桌", "丝绸屏风", "青花瓷装饰"],
    raw_description="独立包间,实木茶桌,丝绸屏风,青花瓷摆件,宁静雅致",
    lighting=lighting,
    view_angle="side_view",
    area="25㎡",
    aspect_ratio="4:3"
)

# 场景4: 明档厨房
scene4 = optimizer.generate_config_for_scene(
    project_name=project_name,
    scene_name="明档厨房",
    space_type="kitchen",
    style_keywords=["新中式风格", "开放透明", "专业操作"],
    color_scheme=color_scheme,
    materials=["不锈钢操作台", "木饰面背墙", "玻璃隔断"],
    raw_description="开放式明档,不锈钢操作台,玻璃隔断,木饰面背墙",
    lighting="cool",  # 厨房使用冷色光
    view_angle="front_view",
    area="30㎡",
    aspect_ratio="16:9"
)

# 场景5: 洗手间前厅
scene5 = optimizer.generate_config_for_scene(
    project_name=project_name,
    scene_name="洗手间前厅",
    space_type="restroom",
    style_keywords=style_keywords,
    color_scheme=color_scheme,
    materials=base_materials + ["大理石洗手台", "铜质镜框"],
    raw_description="洗手间入口走廊,大理石洗手台,铜质镜框,绿植装饰",
    lighting=lighting,
    view_angle="front_view",
    area="8㎡",
    aspect_ratio="9:16"
)

# 场景6: 收银台
scene6 = optimizer.generate_config_for_scene(
    project_name=project_name,
    scene_name="收银台",
    space_type="cashier",
    style_keywords=style_keywords,
    color_scheme=color_scheme,
    materials=base_materials + ["大理石台面", "实木柜体"],
    raw_description="收银服务台,大理石台面,实木柜体,品牌标识展示",
    lighting=lighting,
    view_angle="front_view",
    area="6㎡",
    aspect_ratio="16:9"
)

# 场景7: 等位区
scene7 = optimizer.generate_config_for_scene(
    project_name=project_name,
    scene_name="等位休息区",
    space_type="waiting",
    style_keywords=style_keywords + ["舒适休闲"],
    color_scheme=color_scheme,
    materials=base_materials + ["软包沙发", "茶几", "宫灯落地灯"],
    raw_description="等位沙发区,软包座椅,茶几,绿植,宫灯落地灯",
    lighting=lighting,
    view_angle="side_view",
    area="15㎡",
    aspect_ratio="3:2"
)

# 导出完整配置
all_scenes = [scene1, scene2, scene3, scene4, scene5, scene6, scene7]
optimizer.export_to_json(
    {"scenes": all_scenes},
    "output/新中式火锅店开业筹备/complete_scenes_config.json"
)
```

### 配置模板2: 现代简约咖啡厅全场景套装

```python
# 现代简约咖啡厅 - 完整配置

optimizer = ArchitecturePromptOptimizer()

# 全局风格配置
project_name = "现代简约精品咖啡厅"
style_keywords = ["现代简约风格", "简洁线条", "开放空间", "明亮通透"]
color_scheme = {
    "primary": "纯白 (#FFFFFF)",
    "secondary": "浅木色 (#D2B48C)",
    "accent": "黑色 (#000000)"
}
base_materials = ["抛光水泥地面", "玻璃隔断", "极简木家具"]
lighting = "natural"  # 全场景自然日光

# 场景配置类似上方新中式,针对咖啡厅场景调整...
# (入口、吧台、座位区、包间、洗手间等)
```

---

## ✅ 提示词优化检查清单 (Prompt Optimization Checklist)

### 文生图 (Text-to-Image) 检查清单

```yaml
□ 8元素完整性检查:
  □ 空间类型明确 (entrance/dining/vip_room等)
  □ 风格关键词准确 (≥3个关键词)
  □ 空间描述详细 (核心设计需求)
  □ 色彩方案符合60-30-10法则
  □ 材质纹理具体 (≥4种材质)
  □ 光照氛围合适 (warm/cool/natural等)
  □ 相机构图专业 (eye level/corner view等)
  □ 质量标签完整 (architectural photography等)

□ 字数控制检查:
  □ 总字符数 ≤ 400字符
  □ 截断位置在逗号处
  □ 保持句子完整性

□ 专业术语检查:
  □ 使用建筑摄影术语
  □ 使用专业材质名称
  □ 使用标准光照描述
  □ 使用规范相机术语

□ 负面提示词检查:
  □ 包含所有标准负面词
  □ 根据场景调整 (如是否包含人物)
  □ 避免风格冲突词

□ 生成参数检查:
  □ aspect_ratio符合场景需求
  □ cfg_scale = 7.0-8.0
  □ steps = 50
  □ style_preset = photographic
```

### 图生图 (Image-to-Image) 检查清单

```yaml
□ 参考主图检查:
  □ 参考图路径正确
  □ 图片分辨率 ≥ 512x512
  □ 格式为PNG/JPG
  □ 文件大小 < 10MB

□ 保持一致元素检查:
  □ keep_consistent非空 (≥3个元素)
  □ 元素描述具体明确
  □ 覆盖关键设计特征
  □ 无与change_elements冲突

□ 变化元素检查:
  □ change_elements非空 (≥1个元素)
  □ 包含变化方向 ("从...到...")
  □ 一次变化不超过3个维度
  □ 描述清晰可执行

□ 变化强度检查:
  □ strength在0.4-0.8范围内
  □ 根据变化幅度选择强度:
    - 0.4-0.5: 微调 (表情、视角)
    - 0.5-0.6: 小幅变化 (姿态)
    - 0.6-0.7: 明显变化 (动作)
    - 0.7-0.8: 较大变化 (场景、光影)

□ 提示词权重检查:
  □ prompt_weight补充变化意图 (可选)
  □ 使用英文关键词
  □ 不超过15个单词
```

---

## 🎯 常见问题与解决方案 (FAQ & Troubleshooting)

### Q1: 提示词超过400字符怎么办?

**解决方案**:
```yaml
优先级调整策略:
  1. 保留: 空间类型 + 风格 + 质量标签 (必需)
  2. 精简: 材质描述 (保留最关键3-4种)
  3. 精简: 色彩方案 (可只保留primary和secondary)
  4. 精简: 光照描述 (使用简短版本)
  5. 精简: 空间详细描述 (提炼核心关键词)

示例:
  过长 (450字符):
    "entrance reception area, 新中式风格, 对称布局, 现代雅致,
     温馨舒适, 米白色墙面配胡桃木色木饰面, 古典格栅屏风作为隔断,
     品牌LOGO墙居中, 绿植点缀, 温馨雅致, 米白色作为主色调,
     胡桃木色作为次色调, 中国红作为点缀色, 木饰面墙板, 仿古地砖,
     实木格栅, 宫灯吊灯, 丝绸灯罩, 大理石台面, warm ambient
     lighting, golden hour glow, soft shadows, gentle atmosphere,
     eye level front shot, symmetrical composition, architectural
     photography, photorealistic, 8K resolution, ultra high detail"

  优化后 (385字符):
    "entrance reception area, 新中式风格, 对称布局, 米白色墙面配
     胡桃木色木饰面, 古典格栅屏风隔断, 品牌LOGO墙, 米白色 as primary,
     胡桃木色 as secondary, 中国红 as accent, 木饰面墙板, 仿古地砖,
     实木格栅, 宫灯吊灯, warm ambient lighting, soft shadows,
     eye level front shot, symmetrical composition, architectural
     photography, photorealistic, 8K resolution"
```

### Q2: 生成结果与预期风格不符?

**排查步骤**:
```yaml
1. 检查风格关键词是否准确:
   - 是否使用了风格术语库中的标准关键词?
   - 是否包含≥3个风格描述词?

2. 检查材质是否匹配风格:
   - 新中式 → 木饰面、仿古砖、实木
   - 现代简约 → 水泥、玻璃、不锈钢
   - 工业风 → 砖墙、金属、混凝土

3. 检查色彩方案是否符合风格:
   - 新中式 → 米白+胡桃木+中国红
   - 现代简约 → 白+灰+黑
   - 工业风 → 水泥灰+砖红+铜色

4. 检查光照氛围是否合适:
   - 新中式 → warm (温暖光)
   - 现代简约 → natural/cool (自然光/冷光)
   - 工业风 → dramatic (戏剧性光)

5. 检查质量标签:
   - 是否包含 "architectural photography"?
   - 是否包含 "photorealistic"?
```

### Q3: 图生图一致性不够怎么办?

**解决方案**:
```yaml
策略1: 增加keep_consistent元素
  - 从3个增加到5-7个
  - 覆盖所有关键视觉特征
  - 使用更具体的描述

策略2: 降低strength值
  - 从0.65降至0.55或0.50
  - 逐步测试找到最佳值

策略3: 精简change_elements
  - 一次只变化1-2个维度
  - 避免多维度同时变化

策略4: 使用prompt_weight强化
  - 添加关键词强化保持一致的元素
  - 示例: "maintaining exact style, keeping character features"

示例:
  问题: 角色转身后服装颜色变了

  解决前:
    keep_consistent: ["角色服装", "风格"]
    change_elements: ["身体转向侧面"]
    strength: 0.70

  解决后:
    keep_consistent: [
      "角色的黑色皮夹克",
      "角色的蓝色牛仔裤",
      "角色的白色运动鞋",
      "赛博朋克霓虹风格",
      "背景城市夜景"
    ]
    change_elements: ["身体姿态从正面转为右侧45度"]
    strength: 0.55
    prompt_weight: "keeping exact outfit colors and style"
```

### Q4: 如何快速生成批量场景?

**解决方案**:
```python
# 使用循环批量生成配置

scenes = [
    {
        "name": "入口迎宾区",
        "type": "entrance",
        "desc": "品牌LOGO墙,格栅屏风",
        "area": "10㎡",
        "view": "front_view",
        "ratio": "16:9"
    },
    {
        "name": "正餐区大厅",
        "type": "dining",
        "desc": "圆桌布局,软包座椅",
        "area": "120㎡",
        "view": "corner_view",
        "ratio": "3:2"
    },
    # ... 更多场景
]

optimizer = ArchitecturePromptOptimizer()
configs = []

for scene in scenes:
    config = optimizer.generate_config_for_scene(
        project_name="火锅店开业筹备",
        scene_name=scene["name"],
        space_type=scene["type"],
        style_keywords=["新中式风格", "对称布局"],
        color_scheme={"primary": "米白色", "secondary": "胡桃木色"},
        materials=["木饰面", "仿古砖", "实木家具"],
        raw_description=scene["desc"],
        lighting="warm",
        view_angle=scene["view"],
        area=scene["area"],
        aspect_ratio=scene["ratio"]
    )
    configs.append(config)

# 一次性导出所有配置
optimizer.export_to_json(
    {"scenes": configs},
    "output/火锅店开业筹备/all_scenes.json"
)
```

---

**版本**: 3.0.0
**更新日期**: 2025-10-31
**适用模型**: Stable Diffusion XL (SDXL)
**配套工具**: `scripts/prompt_optimizer_architecture.py`
