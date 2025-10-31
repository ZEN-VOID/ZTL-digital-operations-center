---
name: nano-banana
description: Comprehensive AIGC image multi-workflow toolkit powered by Google Gemini 2.5 Flash Image. Supports 9 image processing types including text-to-image, style-reference generation, subject-reference generation, background replacement, subject replacement, local editing, pose/angle/space adjustment, style transfer, and intelligent prompt optimization for each workflow. Specialized for restaurant industry visual content creation.
---

# Nano-Banana AIGC 图片多工作流技能包

> 基于 Google Gemini 2.5 Flash Image (OpenRouter)
> 集成9种图片处理工作流,专为餐饮行业AIGC内容创作优化

## 🎯 核心能力矩阵

| 工作流类型 | 能力描述 | 典型场景 | 关键参数 |
|-----------|---------|---------|---------|
| **1-文生图** | 从文本描述直接生成图片 | 创意海报、产品概念图 | `task_type="text-to-image"` |
| **2-风格参考生图** | 参考图片风格+文本描述→新图片 | 品牌风格统一、系列设计 | `task_type="style-reference"` |
| **3-主体参考生图** | 保持主体一致+新场景描述 | 角色一致性、产品多场景展示 | `task_type="subject-reference"` |
| **4-背景替换** | 主体抠出+新背景合成 | 产品换背景、场景变换 | `task_type="background-replace"` |
| **5-主体替换** | 保持背景+替换新主体 | 菜品替换、人物更换 | `task_type="subject-replace"` |
| **6-局部修改** | 精确修改图片指定区域 | 去水印、局部优化、细节调整 | `task_type="local-edit"` |
| **7-调整动作/角度/空间** | 同主体不同姿态/视角/空间关系 | 产品多角度、人物动作调整 | `task_type="pose-angle-space"` |
| **8-风格转绘** | 保持内容,转换艺术风格 | 照片转手绘、风格化处理 | `task_type="style-transfer"` |
| **9-提示词优化器** | 智能解析任务→高质量提示词 | 所有工作流的前置优化 | 自动集成到每种工作流 |

## 🚀 快速开始

### ⚡ 并发执行模式 (推荐)

**v2.0 升级**: 迁移至通用并发执行器,支持所有技能包,自动依赖分析,智能调度,4-5倍提速!

```python
from .claude.skills.幻影之舞.universal_concurrent_executor.scripts.core import execute_plan
from .claude.skills.幻影之舞.universal_concurrent_executor.adapters import NanoBananaAdapter

# 创建适配器
adapter = NanoBananaAdapter()

# 一行代码执行计划
report = execute_plan(
    plan_path="output/项目名/nano-banana/plans/execution_plan.json",
    adapter=adapter,
    max_workers=4,
    enable_dependency_analysis=True
)

print(f"✅ 成功: {report.successful_tasks}/{report.total_tasks}")
print(f"⏱️  总耗时: {report.total_duration_seconds:.2f}s")
print(f"📊 成功率: {report.success_rate:.1f}%")
```

**智能特性**:
- ✅ **自动依赖分析**: 检测任务间依赖关系(如style-transfer依赖source image生成)
- ✅ **分层并发执行**: 同层任务并发,层间串行,最大化并发效率
- ✅ **进度追踪**: 实时日志 + 详细执行报告 (JSON)
- ✅ **错误处理**: 单任务失败不影响其他任务
- ✅ **通用架构**: 图片/音乐/视频/语音/数据处理/网页爬虫统一框架

**详细文档**: `.claude/skills/幻影之舞/universal-concurrent-executor/SKILL.md`

**执行计划JSON示例**:
```json
{
  "plan_id": "plan_20251031_001",
  "project_name": "中餐菜品Icon设计",
  "created_at": "2025-10-31T10:00:00",
  "total_tasks": 20,
  "total_batches": 10,
  "batches": [
    {
      "batch_id": "B01",
      "batch_name": "特色包子-非点击态+点击态",
      "tasks": [
        {
          "task_id": "01-A-非点击态",
          "task_type": "text-to-image",
          "user_prompt": "Chinese restaurant app menu icon, baozi...",
          "context": "餐饮App菜品分类icon",
          "target_style": "Chinese anime style",
          "config": {
            "aspect_ratio": "1:1",
            "temperature": 0.8,
            "max_tokens": 8192
          },
          "output_filename": "baozi_non_active.png"
        },
        {
          "task_id": "01-B-点击态",
          "task_type": "style-transfer",
          "user_prompt": "Add blue-orange gradient glow effect...",
          "context": "点击态视觉反馈",
          "depends_on": ["01-A-非点击态"],  # 依赖关系
          "images": [
            {"path": "output/.../01-A-非点击态.png"}
          ],
          "config": {"aspect_ratio": "1:1"}
        }
      ]
    }
  ]
}
```

---

### 1. 文生图 (Text-to-Image)

最基础的工作流,从文本描述直接生成图片:

```python
from pathlib import Path
from scripts.core_engine import NanoBananaExecutor

executor = NanoBananaExecutor()

# 基础文生图
result = executor.execute(
    user_prompt="火锅店开业庆典海报,红色主色调,喜庆氛围",
    task_type="text-to-image",
    context="餐饮行业海报设计",
    project_name="火锅店开业筹备"
)

print(f"生成图片: {result['image_path']}")
```

**自动提示词优化**:
- 原始: "火锅店开业庆典海报,红色主色调,喜庆氛围"
- 优化后: "Professional restaurant promotional poster design, 火锅店开业庆典海报, 喜庆red色主色调, celebration氛围, ultra-realistic, photographic quality, 8K resolution, golden hour light, 85mm portrait lens, attention-grabbing composition..."

### 2. 风格参考生图 (Style-Reference Generation)

输入参考风格图片,生成保持相同风格的新内容:

```python
from scripts.core_engine import ImageInput

# 准备风格参考图
style_ref = ImageInput(
    path="references/brand_style_guide.jpg",
    description="品牌视觉风格参考"
)

# 风格参考生图
result = executor.execute(
    user_prompt="火锅店新品上市海报",
    task_type="style-reference",
    images=[style_ref],
    context="保持品牌视觉风格统一",
    project_name="新品推广物料"
)
```

**提示词优化策略** (自动):
- 提取参考图风格特征(色调、构图、质感)
- 将风格特征编码到提示词
- 强调风格一致性指令

### 3. 主体参考生图 (Subject-Reference Generation)

保持主体角色/产品一致,生成不同场景:

```python
# 准备主体参考图
subject_ref = ImageInput(
    path="assets/mascot_character.png",
    description="品牌吉祥物角色"
)

# 主体参考生图
result = executor.execute(
    user_prompt="吉祥物在火锅店内迎宾的场景",
    task_type="subject-reference",
    images=[subject_ref],
    context="品牌角色一致性",
    project_name="吉祥物系列图"
)
```

**提示词优化策略** (自动):
- 提取主体特征(外观、服饰、特征细节)
- 场景与主体融合指令
- 强调角色一致性约束

### 4. 背景替换 (Background Replacement)

保持主体,替换背景环境:

```python
# 准备原图
original = ImageInput(
    path="products/dish_white_bg.jpg",
    description="白底菜品图"
)

# 背景替换
result = executor.execute(
    user_prompt="将背景替换为温馨的火锅店用餐氛围",
    task_type="background-replace",
    images=[original],
    context="产品场景化",
    project_name="菜品场景图"
)
```

**提示词优化策略** (自动):
- 主体保护指令(保持原主体完整)
- 新背景详细描述
- 主体与背景融合光照一致性

### 5. 主体替换 (Subject Replacement)

保持背景,替换主体对象:

```python
# 准备原图
original = ImageInput(
    path="scenes/dining_room.jpg",
    description="餐厅用餐场景,桌上是毛肚"
)

# 主体替换
result = executor.execute(
    user_prompt="将桌上的毛肚替换为鲜虾滑",
    task_type="subject-replace",
    images=[original],
    context="菜品变体展示",
    project_name="菜单摄影"
)
```

**提示词优化策略** (自动):
- 背景保护指令
- 新主体详细描述
- 光照与透视一致性约束

### 6. 局部修改 (Local Editing)

精确修改图片特定区域:

```python
# 准备原图
original = ImageInput(
    path="posters/with_watermark.jpg",
    description="带水印的海报"
)

# 局部修改
result = executor.execute(
    user_prompt="删除左上角的水印,保持其他元素不变",
    task_type="local-edit",
    images=[original],
    context="图片修复",
    project_name="海报优化"
)
```

**提示词优化策略** (自动):
- 精确区域定位指令
- 保护非修改区域
- 自然过渡与修复指令

### 7. 调整动作/角度/空间 (Pose/Angle/Space Adjustment)

保持主体,调整姿态、视角或空间关系:

```python
# 准备原图
original = ImageInput(
    path="products/dish_front_view.jpg",
    description="菜品正面图"
)

# 调整视角
result = executor.execute(
    user_prompt="调整为45度俯拍视角,展示菜品层次感",
    task_type="pose-angle-space",
    images=[original],
    context="多角度产品展示",
    project_name="菜单摄影"
)
```

**提示词优化策略** (自动):
- 视角/姿态变换指令
- 保持主体特征一致性
- 空间关系物理合理性

### 8. 风格转绘 (Style Transfer)

保持内容,转换为特定艺术风格:

```python
# 准备原图
original = ImageInput(
    path="photos/restaurant_photo.jpg",
    description="餐厅实拍照片"
)

# 风格转绘
result = executor.execute(
    user_prompt="转换为水彩画风格,保持场景内容",
    task_type="style-transfer",
    images=[original],
    target_style="水彩",
    context="艺术化处理",
    project_name="宣传物料"
)
```

**提示词优化策略** (自动):
- 目标风格详细描述(艺术流派、技法)
- 内容保留指令
- 风格化程度控制

## 📐 配置选项

### ImageConfig - 图像生成技术参数

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
    task_type="text-to-image",
    config=config
)
```

### TaskTypeConfig - 工作流类型配置

```python
# 每种工作流类型的推荐配置
TASK_TYPE_CONFIGS = {
    "text-to-image": {
        "temperature": 1.0,
        "aspect_ratio": "16:9"
    },
    "style-reference": {
        "temperature": 0.8,  # 风格一致性需要更低温度
        "aspect_ratio": None  # 继承参考图比例
    },
    "subject-reference": {
        "temperature": 0.7,  # 角色一致性优先
        "aspect_ratio": None
    },
    "background-replace": {
        "temperature": 0.8,
        "aspect_ratio": None
    },
    "subject-replace": {
        "temperature": 0.8,
        "aspect_ratio": None
    },
    "local-edit": {
        "temperature": 0.6,  # 精确编辑需要低温度
        "aspect_ratio": None
    },
    "pose-angle-space": {
        "temperature": 0.7,
        "aspect_ratio": None
    },
    "style-transfer": {
        "temperature": 1.0,  # 风格转换允许更高创意度
        "aspect_ratio": None
    }
}
```

## 🎨 自动提示词优化系统

每种工作流类型都有专属的提示词优化策略,自动在任务执行前优化:

### 优化策略矩阵

```yaml
1-文生图:
  核心: Subject + Composition + Style + Lighting + Colors + Quality
  餐饮优化: 美食摄影术语、诱人造型、工作室光照

2-风格参考:
  核心: 风格特征提取 + 风格一致性指令
  餐饮优化: 品牌调性匹配、色调统一

3-主体参考:
  核心: 主体特征锁定 + 场景融合
  餐饮优化: 角色/产品一致性、品牌IP保护

4-背景替换:
  核心: 主体保护 + 新背景描述 + 光照一致性
  餐饮优化: 场景氛围营造、环境真实感

5-主体替换:
  核心: 背景保护 + 新主体描述 + 透视一致性
  餐饮优化: 菜品变体、同场景多产品展示

6-局部修改:
  核心: 精确区域定位 + 保护非修改区 + 自然过渡
  餐饮优化: 去水印、局部优化、细节修复

7-动作/角度/空间:
  核心: 视角变换 + 主体一致性 + 物理合理性
  餐饮优化: 多角度产品展示、立体感增强

8-风格转绘:
  核心: 风格详细描述 + 内容保留 + 风格化程度
  餐饮优化: 艺术化宣传、创意海报
```

### 餐饮行业场景自动识别

```python
# 系统自动识别餐饮场景类型并应用专属优化
RESTAURANT_SCENARIOS = {
    "海报设计": {
        "keywords": ["海报", "poster", "宣传"],
        "optimization": "专业海报设计前缀 + 高质量印刷 + 吸睛构图"
    },
    "菜单摄影": {
        "keywords": ["菜单", "menu", "菜品"],
        "optimization": "美食摄影术语 + 诱人造型 + 工作室光照"
    },
    "社交媒体": {
        "keywords": ["朋友圈", "社交", "social", "抖音"],
        "optimization": "移动端构图 + 鲜艳配色 + 可分享美学"
    },
    "产品图": {
        "keywords": ["产品", "商品", "展示"],
        "optimization": "干净背景 + 专业灯光 + 突出质感"
    }
}
```

## 📊 输出路径规范

遵循项目标准化输出路径:

```
output/[项目名]/nano-banana/
├── results/            # 生成的图像
│   ├── nano_banana_[task_type]_20250130_103000.png
│   └── nano_banana_[task_type]_20250130_103000_metadata.json
├── plans/             # 执行计划 (如使用JSON配置)
│   └── execution_plan_20250130.json
└── logs/              # 执行日志
    └── execution_20250130_103000.log
```

**元数据追溯**:
每张生成的图片都包含完整元数据JSON文件:

```json
{
  "task_type": "background-replace",
  "original_prompt": "将背景替换为温馨的火锅店用餐氛围",
  "optimized_prompt": "[完整的优化后提示词]",
  "input_images": ["products/dish_white_bg.jpg"],
  "config": {
    "aspect_ratio": "3:2",
    "temperature": 0.8,
    "model": "google/gemini-2.5-flash-image"
  },
  "timestamp": "2025-01-30T10:30:00",
  "cost_usd": 0.039
}
```

## 🔧 高级用法

### 批量处理 (JSON 计划)

创建 JSON 执行计划支持批量多工作流任务:

```json
{
  "project_name": "火锅店开业物料",
  "tasks": [
    {
      "id": "task_001",
      "task_type": "text-to-image",
      "user_prompt": "火锅店开业海报",
      "context": "餐饮行业海报设计",
      "config": {
        "aspect_ratio": "2:3",
        "temperature": 1.0
      }
    },
    {
      "id": "task_002",
      "task_type": "style-reference",
      "user_prompt": "朋友圈宣传图",
      "images": [
        {
          "path": "references/brand_style.jpg",
          "description": "品牌风格参考"
        }
      ],
      "context": "保持品牌视觉统一",
      "config": {
        "aspect_ratio": "1:1",
        "temperature": 0.8
      }
    },
    {
      "id": "task_003",
      "task_type": "background-replace",
      "user_prompt": "将白底菜品图换成餐厅场景背景",
      "images": [
        {
          "path": "products/dish001.jpg",
          "description": "白底菜品图"
        }
      ],
      "context": "产品场景化",
      "config": {
        "temperature": 0.8
      }
    }
  ]
}
```

使用批处理执行器:

```python
from scripts.batch_processor import BatchProcessor

processor = BatchProcessor()
results = processor.execute_plan("plans/batch_plan_001.json")

for result in results:
    print(f"{result['task_id']}: {result['status']}")
    print(f"  生成图片: {result['image_path']}")
```

### 工作流链式组合

多个工作流可以链式组合,实现复杂图像处理:

```python
# 示例: 文生图 → 风格转绘 → 局部修改
executor = NanoBananaExecutor()

# Step 1: 文生图
result1 = executor.execute(
    user_prompt="火锅店用餐场景",
    task_type="text-to-image",
    project_name="复合处理"
)

# Step 2: 风格转绘
result2 = executor.execute(
    user_prompt="转换为水彩画风格",
    task_type="style-transfer",
    images=[ImageInput(path=result1['image_path'], description="原始场景")],
    target_style="水彩",
    project_name="复合处理"
)

# Step 3: 局部修改
result3 = executor.execute(
    user_prompt="增强左下角的火锅细节",
    task_type="local-edit",
    images=[ImageInput(path=result2['image_path'], description="水彩风格图")],
    project_name="复合处理"
)
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
pip install requests python-dotenv pillow
```

## 💡 最佳实践

### 提示词编写技巧 (按工作流类型)

#### 1-文生图

✅ **好的提示词**:
```
一家温馨的火锅店内,柔和的金色灯光照亮餐桌,顾客正在享用热气腾腾的火锅,
展示新鲜的毛肚和虾滑,85mm镜头,浅景深,商业摄影级别
```

❌ **差的提示词**:
```
火锅店,灯光,餐桌,顾客
```

#### 2-风格参考生图

✅ **好的提示词**:
```
保持参考图的色调和构图风格,生成火锅店新品上市海报,
强调视觉一致性,品牌调性匹配
```

❌ **差的提示词**:
```
类似的海报
```

#### 3-主体参考生图

✅ **好的提示词**:
```
保持吉祥物的外观特征(红色服装、笑脸、厨师帽)完全一致,
将其放置在火锅店门口迎宾的场景,自然融入环境,光照协调
```

❌ **差的提示词**:
```
吉祥物在店门口
```

#### 4-背景替换

✅ **好的提示词**:
```
保持菜品主体完整不变(毛肚的质感、颜色、摆盘),
将白底背景替换为温馨的火锅店用餐氛围,暖色调灯光,
自然光照过渡,背景虚化突出主体
```

❌ **差的提示词**:
```
换个背景
```

#### 5-主体替换

✅ **好的提示词**:
```
保持餐桌、餐具、环境完全不变,
将桌上的毛肚替换为新鲜的鲜虾滑(粉色、饱满、有光泽),
保持相同的光照角度和摆盘风格
```

❌ **差的提示词**:
```
换成虾滑
```

#### 6-局部修改

✅ **好的提示词**:
```
精确删除图片左上角的水印区域(约100x100像素范围),
使用周围环境自然填充,保持其他所有元素完全不变,
修复区域与原图无缝衔接
```

❌ **差的提示词**:
```
去掉水印
```

#### 7-动作/角度/空间调整

✅ **好的提示词**:
```
保持菜品的外观、质感、色彩完全一致,
从正面视角调整为45度俯拍视角,展示菜品的层次感和立体感,
光照从右上方打下,保持商业摄影专业水准
```

❌ **差的提示词**:
```
换个角度
```

#### 8-风格转绘

✅ **好的提示词**:
```
将照片转换为传统水彩画风格,保留所有场景内容和构图,
水彩纸质感,颜料流动自然过渡,留白艺术,
色彩饱和度适中,保持中式美学
```

❌ **差的提示词**:
```
变成水彩画
```

### 工作流选择决策树

```
需要处理图片?
│
├─ 没有输入图片?
│  └─ 使用 1-文生图
│
├─ 有输入图片,想保持某种风格?
│  └─ 使用 2-风格参考生图
│
├─ 有输入图片,想保持主体角色?
│  └─ 使用 3-主体参考生图
│
├─ 有输入图片,想换背景?
│  └─ 使用 4-背景替换
│
├─ 有输入图片,想换主体?
│  └─ 使用 5-主体替换
│
├─ 有输入图片,只改部分区域?
│  └─ 使用 6-局部修改
│
├─ 有输入图片,想改视角/姿态?
│  └─ 使用 7-动作/角度/空间调整
│
└─ 有输入图片,想改艺术风格?
   └─ 使用 8-风格转绘
```

### 成本控制

- **每张图像约 0.039 USD** (按 1290 输出 token 计算)
- **输入图像按分辨率计费**: 尽量压缩输入图像分辨率
- **合理使用 seed**: 测试阶段固定 seed 可避免重复生成
- **批量处理优化**: 相似任务批量执行,减少初始化开销

## 🐛 故障排除

### API 调用失败

**问题**: `ValueError: 未找到 OPENROUTER_API_KEY`
**解决**: 检查环境变量是否正确设置,或创建`.env`文件

**问题**: `requests.exceptions.HTTPError: 401`
**解决**: API Key 无效或已过期,请更新

### 工作流执行失败

**问题**: "task_type not supported"
**解决**: 检查task_type参数是否为以下之一:
- `text-to-image`
- `style-reference`
- `subject-reference`
- `background-replace`
- `subject-replace`
- `local-edit`
- `pose-angle-space`
- `style-transfer`

**问题**: "输入图片路径无效"
**解决**: 确保ImageInput中的path指向实际存在的文件

### 生成质量不理想

**问题**: 生成的图像不符合预期
**解决**:
1. 增强提示词具体性(参考最佳实践)
2. 调整temperature参数(0.6-1.2)
3. 尝试不同的aspect_ratio
4. 对于需要一致性的任务(风格/主体参考),降低temperature到0.6-0.8

## 📚 相关资源

- **官方文档**: https://ai.google.dev/gemini-api/docs/image-generation
- **OpenRouter API**: https://openrouter.ai/google/gemini-2.5-flash-image/api
- **提示词最佳实践**: https://developers.googleblog.com/en/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/

## 🔄 更新日志

- **v2.0.0** (2025-01-30): 重大架构重构
  - ✅ 新增8种图片处理工作流(原1种扩展为9种)
  - ✅ 为每种工作流类型构建专属提示词优化策略
  - ✅ 智能提示词优化器集成到所有工作流
  - ✅ 餐饮行业场景自动识别优化
  - ✅ 批量处理和工作流链式组合支持
  - ✅ 完整的元数据追溯系统

- **v1.0.0** (2025-01-28): 初始版本
  - 基础文生图能力
  - 餐饮行业提示词优化器
  - 标准化输出路径

---

**注意**: 本技能包遵循 ZTL 数智化作战中心的三层架构规范:
- **Layer 1 (规范层)**: 本文档 + reference.md
- **Layer 2 (计划层)**: JSON 执行计划 (可选)
- **Layer 3 (执行层)**: scripts/core_engine.py + scripts/prompt_optimizer.py
