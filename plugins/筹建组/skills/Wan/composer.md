# Composer组合式生成框架深度指南

> 通义万相独创的设计元素分解/重组系统,精确控制色彩、布局、材质、语义,确保视觉设计的专业性和一致性。

---

## 🎯 核心概念

### 什么是Composer框架?

Composer是通义万相**行业独创**的组合式生成框架,将图像生成过程分解为可独立控制的设计元素:

1. **color_palette (色彩方案)**: 精确指定RGB颜色,控制整体色调
2. **layout (构图布局)**: 选择专业构图法则(三分法、黄金比例等)
3. **material (材质纹理)**: 定义物体表面质感(霓虹玻璃、金属、木质等)
4. **semantic (语义主题)**: 高层次场景类型(未来都市、自然景观等)

**核心优势**:
- **精确控制**: 相比纯文本prompt,设计元素可独立调整
- **一致性保证**: 固定Composer元素,确保系列作品风格统一
- **专业设计**: 基于设计理论(构图法则、色彩理论),输出质量更专业
- **减少重复**: 精确控制减少30-50%无效生成

---

## 📋 Composer参数详解

### color_palette (色彩方案)

**格式**: RGB hex code数组 `["#RRGGBB", "#RRGGBB", ...]`

**参数说明**:
- 最少1个颜色,最多10个颜色
- 第一个颜色通常为主色调
- 后续颜色为辅助色和点缀色
- 按重要性排序(出现频率从高到低)

**色彩理论参考**:

| 色彩搭配 | 数量 | 示例 | 适用场景 |
|---------|------|------|----------|
| **单色调** | 1 | ["#FF6B6B"] | 极简设计、强调主体 |
| **互补色** | 2 | ["#FF6B6B", "#4ECDC4"] | 对比强烈、视觉冲击 |
| **类比色** | 3 | ["#FF6B6B", "#FFA07A", "#FF1493"] | 和谐过渡、柔和氛围 |
| **三角色** | 3 | ["#FF6B6B", "#4ECDC4", "#FFD93D"] | 平衡协调、丰富层次 |
| **完整方案** | 5-7 | ["#00F5FF", "#FF1493", "#9400D3", "#FFD700", "#32CD32"] | 复杂场景、多元素设计 |

**赛博朋克色彩方案**:
```json
{
  "color_palette": ["#00F5FF", "#FF1493", "#9400D3", "#FFD700", "#32CD32"],
  "description": "深蓝(霓虹蓝) + 粉红(霓虹粉) + 紫色(深紫) + 金色(点缀) + 绿色(数据流)"
}
```

**自然风光色彩方案**:
```json
{
  "color_palette": ["#87CEEB", "#228B22", "#F4A460", "#FFD700"],
  "description": "天空蓝 + 草绿 + 沙棕 + 阳光金"
}
```

**电影海报色彩方案**:
```json
{
  "color_palette": ["#1C1C1C", "#FF4500", "#FFD700"],
  "description": "深黑(背景) + 橙红(主体) + 金色(高光)"
}
```

---

### layout (构图布局)

**可选值**: `rule_of_thirds`, `center`, `golden_ratio`, `diagonal`, `symmetry`

#### rule_of_thirds (三分法构图)

**原理**: 将画面横竖各分为三等分,形成4个交叉点,视觉重心分布在交叉点或分割线上。

**适用场景**:
- 风景摄影(地平线放在上/下三分线)
- 人物特写(眼睛放在交叉点)
- 建筑摄影(垂直线放在左/右三分线)

**示例**:
```json
{
  "layout": "rule_of_thirds",
  "prompt": "Futuristic city skyline at sunset, main building on right third, horizon on upper third"
}
```

#### center (中心构图)

**原理**: 主体位于画面正中心,形成对称稳定的视觉效果。

**适用场景**:
- 对称建筑(寺庙、宫殿)
- 正面人像
- 产品展示
- 标志性物体

**示例**:
```json
{
  "layout": "center",
  "prompt": "Symmetrical ancient temple with reflection in water, centered composition"
}
```

#### golden_ratio (黄金比例构图)

**原理**: 基于1.618黄金比例分割画面,符合人类审美本能。

**适用场景**:
- 艺术摄影
- 高端设计
- 自然景观(螺旋构图)
- 追求极致美感

**示例**:
```json
{
  "layout": "golden_ratio",
  "prompt": "Spiral galaxy with golden ratio composition, cosmic beauty"
}
```

#### diagonal (对角线构图)

**原理**: 主要元素沿对角线排列,创造动感和视觉引导。

**适用场景**:
- 动作场景
- 道路/河流/阶梯
- 运动摄影
- 追求动态感

**示例**:
```json
{
  "layout": "diagonal",
  "prompt": "Winding mountain road stretching from bottom left to top right, dynamic perspective"
}
```

#### symmetry (对称构图)

**原理**: 画面左右或上下完全对称,营造稳定、庄重的氛围。

**适用场景**:
- 建筑摄影
- 镜像反射
- 正式场合
- 追求平衡感

**示例**:
```json
{
  "layout": "symmetry",
  "prompt": "Modern glass building with perfect reflection in lake, symmetrical composition"
}
```

---

### material (材质纹理)

**可选值**: `neon_glass`, `metal`, `wood`, `fabric`, `stone`, `plastic`, `ceramic`

| 材质 | 视觉特征 | 适用场景 | 示例 |
|------|---------|----------|------|
| **neon_glass** | 透明发光、霓虹效果、高反射 | 赛博朋克、未来都市、科技感 | 霓虹广告牌、玻璃幕墙 |
| **metal** | 高反光、冷硬质感、金属光泽 | 工业风、机械设计、科幻 | 钢铁建筑、机器人 |
| **wood** | 自然纹理、温暖质感、有机感 | 自然场景、室内设计、古朴风格 | 木屋、家具、森林 |
| **fabric** | 柔软褶皱、布料质感、轻盈感 | 服装设计、室内装饰、柔和氛围 | 窗帘、衣物、旗帜 |
| **stone** | 粗糙纹理、坚硬质感、历史感 | 建筑、雕塑、古代场景 | 石墙、石雕、山岩 |
| **plastic** | 光滑表面、现代感、人工质感 | 产品设计、现代艺术、简洁风格 | 塑料制品、玩具 |
| **ceramic** | 温润质感、细腻表面、光泽柔和 | 工艺品、陶瓷设计、东方美学 | 瓷器、陶罐、茶具 |

**材质组合策略**:
- **单一材质**: 强调统一质感 `{"material": "metal"}`
- **对比材质**: 通过prompt描述不同部分的材质 `{"material": "metal", "prompt": "metal structure with glass panels"}`

---

### semantic (语义主题)

**可选值**: `futuristic_city`, `natural_landscape`, `interior_design`, `character_portrait`

| 语义主题 | 场景特征 | 适用场景 | 关键元素 |
|---------|---------|----------|----------|
| **futuristic_city** | 未来都市、高楼大厦、科技感 | 赛博朋克、科幻场景 | 摩天大楼、飞行器、霓虹灯 |
| **natural_landscape** | 自然风光、山川河流、有机形态 | 风景摄影、自然题材 | 山脉、湖泊、森林、天空 |
| **interior_design** | 室内空间、家具陈设、空间感 | 室内设计、建筑可视化 | 家具、灯具、装饰、空间布局 |
| **character_portrait** | 人物特写、肖像画、表情细节 | 角色设计、人物摄影 | 面部特征、表情、服装、背景虚化 |

---

## 🚀 工作流程

### 工作流1: 色彩方案探索

**目标**: 发现最适合项目的色彩组合

**步骤1: 单色调测试**
```json
{
  "prompt": "Futuristic city at night",
  "color_palette": ["#00F5FF"],
  "layout": "rule_of_thirds",
  "material": "neon_glass",
  "semantic": "futuristic_city"
}
```
→ 评估单一主色调效果

**步骤2: 互补色对比**
```json
{
  "color_palette": ["#00F5FF", "#FF1493"],
  ...
}
```
→ 评估对比强度

**步骤3: 完整色彩方案**
```json
{
  "color_palette": ["#00F5FF", "#FF1493", "#9400D3", "#FFD700", "#32CD32"],
  ...
}
```
→ 确定最终色彩方案

**步骤4: 固定色彩,批量生成**
- 固定最佳color_palette
- 生成系列作品,确保色彩一致性

---

### 工作流2: 构图布局对比

**目标**: 选择最适合场景的构图法则

**场景**: 未来都市夜景

**测试1: 三分法构图**
```json
{
  "prompt": "Futuristic city skyline at night, main building on right third",
  "layout": "rule_of_thirds",
  "color_palette": ["#00F5FF", "#FF1493", "#9400D3"],
  "material": "neon_glass",
  "semantic": "futuristic_city"
}
```

**测试2: 中心构图**
```json
{
  "layout": "center",
  ...
}
```

**测试3: 对角线构图**
```json
{
  "layout": "diagonal",
  ...
}
```

**对比分析**: 三分法适合风景,中心构图适合对称建筑,对角线构图适合动态场景

---

### 工作流3: 材质纹理切换

**目标**: 探索不同材质的视觉效果

**基础设定**:
```json
{
  "prompt": "Modern building with futuristic design",
  "color_palette": ["#00F5FF", "#FF1493"],
  "layout": "rule_of_thirds",
  "semantic": "futuristic_city"
}
```

**材质1: neon_glass (霓虹玻璃)**
```json
{
  "material": "neon_glass",
  ...
}
```
→ 透明发光,科技感

**材质2: metal (金属)**
```json
{
  "material": "metal",
  ...
}
```
→ 冷硬工业风

**材质3: stone (石质)**
```json
{
  "material": "stone",
  ...
}
```
→ 坚硬历史感

---

### 工作流4: 系列作品风格统一

**目标**: 生成同一项目的多个场景,保持视觉一致性

**项目**: 赛博朋克短片 - 未来都市24小时

**固定Composer元素**:
```json
{
  "color_palette": ["#00F5FF", "#FF1493", "#9400D3"],
  "layout": "rule_of_thirds",
  "material": "neon_glass",
  "semantic": "futuristic_city"
}
```

**场景1: 清晨5:00**
```json
{
  "prompt": "Futuristic city at dawn, soft morning light, fog, empty streets",
  "color_palette": ["#00F5FF", "#FF1493", "#9400D3"],
  "layout": "rule_of_thirds",
  "material": "neon_glass",
  "semantic": "futuristic_city"
}
```

**场景2: 正午12:00**
```json
{
  "prompt": "Futuristic city at noon, bright sunlight, busy streets, flying cars",
  ...
}
```

**场景3: 黄昏18:00**
```json
{
  "prompt": "Futuristic city at dusk, golden hour, neon lights starting to glow",
  ...
}
```

**场景4: 深夜00:00**
```json
{
  "prompt": "Futuristic city at midnight, full neon illumination, rain-soaked streets",
  ...
}
```

**优势**: 四个时间段保持统一的色彩、布局、材质,确保视觉风格一致性

---

### 工作流5: Composer与Prompt混合控制

**目标**: Composer控制整体风格,Prompt描述场景细节

**策略**: Composer简化(仅核心元素) + Prompt丰富化(详细描述)

**示例**:
```json
{
  "prompt": "A massive holographic billboard displaying advertisements, surrounded by flying cars and drones, rain creating reflections on the street, pedestrians with umbrellas walking below, smoke rising from street vendors, detailed cyberpunk cityscape in the background, dramatic lighting from multiple neon sources, highly detailed, 8K, cinematic composition",
  "color_palette": ["#00F5FF", "#FF1493", "#9400D3"],
  "layout": "rule_of_thirds",
  "material": "neon_glass",
  "semantic": "futuristic_city"
}
```

**优势**:
- Composer控制: 色彩、布局、材质(确保一致性)
- Prompt控制: 场景内容、细节、动作(确保多样性)

---

## 💡 最佳实践

### 1. Composer元素选择策略

**原则**: 从大到小,从整体到局部

**顺序**:
1. **semantic (语义主题)**: 确定大场景类型
2. **color_palette (色彩方案)**: 确定整体色调
3. **layout (构图布局)**: 确定视觉重心
4. **material (材质纹理)**: 确定物体质感

**推荐组合**:

| 场景类型 | semantic | color_palette | layout | material |
|---------|---------|--------------|--------|----------|
| **赛博朋克** | futuristic_city | ["#00F5FF", "#FF1493", "#9400D3"] | rule_of_thirds | neon_glass |
| **自然风光** | natural_landscape | ["#87CEEB", "#228B22", "#F4A460"] | golden_ratio | stone |
| **室内设计** | interior_design | ["#F5F5F5", "#8B4513", "#FFD700"] | center | wood |
| **人物肖像** | character_portrait | ["#FFA07A", "#4682B4", "#FFD700"] | rule_of_thirds | fabric |

### 2. 色彩方案设计技巧

**技巧1: 使用在线配色工具**
- Adobe Color: https://color.adobe.com
- Coolors: https://coolors.co
- Paletton: http://paletton.com

**技巧2: 从参考图提取色彩**
- 使用吸管工具提取主要颜色
- 保持3-5个核心色彩
- 按重要性排序

**技巧3: 色彩心理学**
- 蓝色系: 科技、冷静、专业
- 红色系: 激情、危险、活力
- 绿色系: 自然、健康、和平
- 紫色系: 神秘、高贵、创意

### 3. 固定与变化的平衡

**策略**: 固定Composer核心元素,变化prompt描述

**固定元素**:
- color_palette: 确保色彩一致性
- material: 确保材质统一
- layout: 大多数场景保持一致

**变化元素**:
- prompt: 场景内容、细节、动作
- semantic: 跨场景时可变化

**示例**:
```json
// 场景1: 室外
{
  "prompt": "Futuristic city street at night, neon lights, flying cars",
  "color_palette": ["#00F5FF", "#FF1493", "#9400D3"],
  "layout": "rule_of_thirds",
  "material": "neon_glass",
  "semantic": "futuristic_city"
}

// 场景2: 室内(semantic变化)
{
  "prompt": "Cyberpunk hacker's apartment, multiple holographic screens, dark atmosphere",
  "color_palette": ["#00F5FF", "#FF1493", "#9400D3"],
  "layout": "rule_of_thirds",
  "material": "neon_glass",
  "semantic": "interior_design"  // 变化
}
```

### 4. 常见问题与解决方案

**问题1: 色彩方案不够明显**

**原因**:
- color_palette颜色过多导致稀释
- 颜色对比度不足

**解决方案**:
- 减少颜色数量(3-5个)
- 增加对比度(使用互补色)
- 强调主色调(第一个颜色)

**问题2: 构图布局效果不明显**

**原因**:
- prompt描述与layout冲突
- 场景元素分布随机

**解决方案**:
- 在prompt中明确描述布局意图
- 使用"centered", "on the right third"等关键词配合layout

**问题3: 材质纹理不突出**

**原因**:
- 场景光线不足
- 材质与semantic不匹配

**解决方案**:
- 在prompt中强调光线效果
- 选择匹配的材质(如futuristic_city + neon_glass)

---

## 🎬 影视制作应用

### 案例1: 科幻短片概念设计

**项目**: 《赛博朋克2077》前期概念图

**Composer配置**:
```json
{
  "color_palette": ["#00F5FF", "#FF1493", "#9400D3", "#FFD700"],
  "layout": "rule_of_thirds",
  "material": "neon_glass",
  "semantic": "futuristic_city"
}
```

**场景系列**:
1. 都市全景(establishing shot)
2. 街道特写(medium shot)
3. 室内场景(interior)
4. 角色特写(character close-up)

**优势**: 固定Composer元素,确保4个场景视觉风格完全统一

---

### 案例2: 品牌视觉设计

**项目**: 环保品牌视觉方案

**Composer配置**:
```json
{
  "color_palette": ["#228B22", "#87CEEB", "#F4A460"],
  "layout": "golden_ratio",
  "material": "wood",
  "semantic": "natural_landscape"
}
```

**应用场景**:
- 品牌主视觉
- 产品包装设计
- 营销海报
- 社交媒体内容

**优势**: Composer保证品牌视觉一致性,减少30-50%重复生成成本

---

## 🔗 延伸阅读

- [通义万相API参考](reference.md) - 完整参数说明
- [Qwen-Image文本渲染指南](qwen_image.md) - 中英文文本渲染专项
- [丰富示例集](examples.md) - Composer实战案例

---

**最后更新**: 2025-10-19
**版本**: 1.0.0
