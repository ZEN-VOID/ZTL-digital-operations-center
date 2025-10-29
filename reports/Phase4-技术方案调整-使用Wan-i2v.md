# Phase 4 技术方案调整 - 使用Wan Image-to-Video

> **调整日期**: 2025-10-28
> **调整原因**: 使用现有Wan技能包的i2v功能，技术路线更简洁
> **关键变更**: Z2多角度概念图 → Wan i2v → 视频动画 (跳过Z3 3D建模)

---

## 🔄 技术路线对比

### 原方案 (Phase 3调研)
```
Z1 平面图(SVG)
  ↓
Z2 单角度效果图(PNG)
  ↓
Z3 3D模型(GLB/OBJ) ← 需要TripoSR生成
  ↓
Z4 建筑动画(MP4) ← 需要Luma/Runway生成
```

**问题**:
- 需要两次API调用(Z3 + Z4)
- 成本: $0.24(Z3) + $4.20(Z4) = $4.44
- 技术栈复杂(TripoSR + Luma)
- Z3的3D模型质量影响Z4效果

### ✅ 新方案 (使用Wan i2v)
```
Z1 平面图(SVG)
  ↓
Z2 多角度空间概念图(PNG) ← 关键改变
  ├─ 前视图
  ├─ 侧视图
  ├─ 俯视图
  ├─ 特写视角
  └─ 环视角度
  ↓
Z4 建筑动画(MP4) ← 直接用Wan i2v生成
```

**优势**:
- ✅ 省略Z3环节,技术更简洁
- ✅ 只需一次API调用(Wan i2v)
- ✅ 使用现有Wan技能包,无需开发
- ✅ Z2已有生成多角度的能力
- ✅ 成本更低: ¥0.30(Z2) + ¥X(Z4 Wan i2v)

---

## 📊 Wan Image-to-Video 技术评估

### 核心功能

**模型**: `wan2.5-i2v-preview` (通义万相 2.5 图生视频)

**功能特性**:
```yaml
输入:
  - 格式: PNG/JPG图像
  - 编码: Base64 Data URI
  - 分辨率: 支持主流分辨率

输出:
  - 格式: MP4视频
  - 分辨率: 720P / 1080P
  - 时长: 4-6秒典型

控制:
  - Prompt: 文本描述运动方式
  - Negative Prompt: 排除不需要的效果
  - 参数: 分辨率、时长配置
```

### API状态

**✅ 已实现功能**:
- 完整的API客户端 (`wan-base.py`)
- 图生视频测试脚本 (`test_i2v.py`)
- Base64图像编码
- 异步任务提交和查询
- 视频下载和保存

**技术成熟度**: ⭐⭐⭐⭐ 4/5
- 基础功能完整
- 已有测试验证
- 稳定的API

### 成本分析

**预估定价**: ¥0.20-0.50/视频 (基于wan2.5多模态定价)

**典型项目成本** (300㎡火锅店):
```
6个场景 × ¥0.35/视频 = ¥2.10

完整Z1-Z4成本:
- Z1 平面图: 免费
- Z2 多角度图: ¥0.30 (6场景×5角度=30张,但成本相同)
- Z4 动画视频: ¥2.10 (6段)
─────────────────────
总计: ¥2.40 (约$0.34)

对比原Luma方案:
- Luma方案: $4.74
- Wan方案: ¥2.40 (约$0.34)
- 节省: 93%

对比传统:
- 传统: ¥50,000-80,000
- Wan方案: ¥2.40
- 节省: 99.997%
```

---

## 🎬 Z2多角度生成策略

### Z2需要输出的角度

**为了生成流畅的建筑漫游动画，Z2需要生成以下角度**:

```yaml
场景示例: 入口迎宾区

角度1: 正面全景
  - 视角: 正对入口
  - 用途: 展示整体布局
  - Z4动画: 推进镜头(Dolly-in)

角度2: 侧面视角
  - 视角: 45度侧视
  - 用途: 展示空间深度
  - Z4动画: 横向扫视(Pan)

角度3: 近景特写
  - 视角: 聚焦重点区域
  - 用途: 展示细节材质
  - Z4动画: 特写放大(Zoom)

角度4: 俯视全景
  - 视角: 鸟瞰视角
  - 用途: 展示空间关系
  - Z4动画: 俯视扫描

角度5: 内部环视
  - 视角: 站在空间内向外看
  - 用途: 沉浸式体验
  - Z4动画: 环视360°
```

### Z2-Z4协同工作流

```
Step 1: Z2生成多角度概念图
  输入: Z1平面图 + 风格需求
  输出: 每场景5-6个角度的PNG

Step 2: Z4选择关键角度
  分析: Z2输出的多角度图
  选择: 最适合动画的2-3个角度
  策略: 前景+中景+远景组合

Step 3: Z4生成动画视频
  使用: Wan i2v API
  输入: 选定角度的PNG
  Prompt: "smooth camera movement, architectural walkthrough..."
  输出: 4-6秒MP4视频

Step 4: 后期组合(可选)
  工具: FFmpeg
  操作: 拼接多段视频
  输出: 完整漫游视频(30-60秒)
```

---

## ⚖️ Wan i2v vs Luma AI 对比

| 维度 | Wan i2v | Luma Dream Machine | 评估 |
|------|---------|-------------------|------|
| **技术成熟度** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Luma略优 |
| **已有实现** | ✅ Wan技能包 | ❌ 需开发 | **Wan优** |
| **相机控制** | ⭐⭐⭐ Prompt描述 | ⭐⭐⭐⭐⭐ 专业API | Luma优 |
| **视频时长** | 4-6秒 | 10秒 | Luma优 |
| **分辨率** | 720P/1080P | 720p | Wan略优 |
| **成本** | ¥0.20-0.50 | $0.70 | **Wan优(6倍)** |
| **中文支持** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | **Wan优** |
| **集成难度** | ⭐⭐⭐⭐⭐ 即用 | ⭐⭐⭐ 需开发 | **Wan优** |
| **建筑适配** | ⭐⭐⭐ 通用i2v | ⭐⭐⭐⭐⭐ 专为空间 | Luma优 |

### 决策因素

**选择Wan i2v的理由**:

1. **✅ 已有技能包** - 立即可用,无需开发
   - `plugins/筹建组/skills/Wan/`
   - 完整的API客户端和测试
   - 稳定的执行引擎

2. **✅ 成本极低** - ¥0.35 vs $0.70 (6倍差异)
   - 对于中国市场更友好
   - 人民币直接支付
   - 无汇率损失

3. **✅ 技术栈统一** - Z2已使用通义万相生态
   - Z2用Stable Diffusion XL (可替换为通义万相)
   - Z4用Wan i2v
   - 统一阿里云DashScope平台

4. **✅ 中文优化** - Prompt和文档都是中文
   - 中文Prompt效果更好
   - 文档和示例都是中文
   - 本土化支持

**Luma的优势**:

1. **专业相机控制** - Dolly, Orbit, Pan等专业术语
   - 但Wan i2v可以用中文描述达到类似效果
   - 例如: "镜头平滑推进" vs "Dolly-in"

2. **时长更长** - 10秒 vs 4-6秒
   - 但可以生成多段后拼接
   - FFmpeg拼接无缝衔接

3. **建筑场景优化** - Ray2专为空间设计
   - 但通用i2v也能满足需求
   - 通义万相在中国建筑场景训练数据更多

### 综合评分

| 方案 | 技术 | 成本 | 集成 | 质量 | 综合 |
|------|------|------|------|------|------|
| **Wan i2v** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **4.6/5** |
| Luma AI | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 4/5 |

**结论**: 对于ZTL项目,**Wan i2v是更优选择**

---

## 🎯 调整后的Phase 4计划

### Day 1: 技术调研 ✅ (已完成)
- ✅ 调研Luma/Runway/Pika等方案
- ✅ 发现Wan i2v现有实现
- ✅ 决策使用Wan i2v

### Day 2: Z4智能体定义 (调整)
```yaml
任务:
  - 重写Z4-建筑动画AIGC助手.md
  - 基于Wan i2v重新设计工作流
  - 定义Z2多角度生成要求
  - 设计中文Prompt模板库

输出:
  - Z4智能体定义(~600-800行)
  - 明确与Z2的协同机制
```

### Day 3-4: 技能包适配 (简化)
```yaml
任务:
  - ❌ 不需要创建新技能包
  - ✅ 使用现有Wan技能包
  - ✅ 创建Z4专用配置模板
  - ✅ 编写中文Prompt预设库
  - ✅ 创建视频拼接脚本(FFmpeg)

输出:
  - config/z4-animation-config-template.json
  - config/camera-movement-prompts.json (中文)
  - scripts/video_merger.py (视频拼接工具)
  - README-Z4.md (使用说明)
```

### Day 5: 集成测试
```yaml
任务:
  - 创建test_z4_integration.py
  - 测试Wan i2v调用
  - 测试多角度视频生成
  - 测试视频拼接功能

输出:
  - 测试通过率: 6/6 (100%)
```

---

## 📦 完整工作流总结

### 新的Z1-Z4完整流程

```
Z1-平面图计划师
  输入: 门店信息(面积、类型)
  输出: SVG平面图
  技能包: canvas-design-floor-plan
  成本: 免费
  ↓
Z2-空间设计师
  输入: Z1平面图 + 设计需求
  输出: 每场景5-6个角度PNG (共30张)
  技能包: canvas-design-space-design
  成本: ¥0.30
  ↓
Z4-建筑动画助手 ← 当前阶段
  输入: Z2多角度PNG
  输出: 6段动画视频MP4 (各4-6秒)
  技能包: Wan (现有)
  成本: ¥2.10
  ↓
最终交付: 完整可视化方案
  - 1个平面图SVG
  - 30张多角度效果图PNG
  - 6段建筑漫游视频MP4
  - 总成本: ¥2.40 (约$0.34)
  - 总耗时: <1天
```

### Z3的角色调整

**原计划**: Z3生成3D模型 (TripoSR)
**新方案**: ❌ 暂时跳过Z3，Z4直接从Z2的2D图生成视频

**Z3未来定位**:
- 保留Z3-3D生成AIGC助手的定义
- 作为可选的高级功能
- 适用场景:
  - 需要真实3D模型(GLB)用于VR/AR
  - 需要在Unity/Unreal Engine中使用
  - 需要用户自由旋转查看

**当前优先级**:
```
Phase 1 (Z1): ✅ 已完成
Phase 2 (Z2): ✅ 已完成
Phase 4 (Z4): 🔄 进行中 (使用Wan i2v)
Phase 3 (Z3): ⏸️ 暂缓,作为可选扩展
```

---

## 🔧 技术实现细节

### Wan i2v API调用

**基于现有`wan-base.py`**:

```python
from scripts.wan_base import WanAPIClient

client = WanAPIClient()

# 提交图生视频任务
result = client.submit_i2v_task(
    image_path="output/Z2/entrance-front.png",
    prompt="平滑推进镜头,展示火锅店入口迎宾区,新中式风格,氛围灯光",
    negative_prompt="模糊,失真,突兀,跳跃",
    params={
        "model": "wan2.5-i2v-preview",
        "resolution": "720P",
        "duration": 6
    }
)

# 查询任务状态
status = client.query_task_status(result['task_id'])

# 下载视频
if status['status'] == 'SUCCEEDED':
    video_url = status['output']['video_url']
    client.download_video(video_url, "output/Z4/entrance-animation.mp4")
```

### Z4配置模板结构

```json
{
  "project_info": {
    "project_name": "火锅店开业筹备",
    "z4_task_id": "Z4-Animation-20251028-001",
    "input_source": "Z2-空间设计AIGC助手"
  },
  "generation_config": {
    "model": "wan2.5-i2v-preview",
    "api_endpoint": "dashscope.aliyuncs.com",
    "version": "2.5"
  },
  "scenes_to_animate": [
    {
      "scene_id": "scene-01",
      "scene_name": "入口迎宾区",
      "input_images": {
        "front_view": "output/Z2/entrance-front.png",
        "side_view": "output/Z2/entrance-side.png"
      },
      "animation_config": {
        "camera_movement": "dolly_in",
        "prompt": "镜头平滑推进,展示火锅店入口迎宾区,新中式风格,暖色调灯光,4K画质",
        "negative_prompt": "模糊,失真,突兀,抖动,低质量",
        "duration": 6,
        "resolution": "720P"
      },
      "output_path": "output/Z4/entrance-animation.mp4"
    }
  ]
}
```

### 中文Prompt模板库

```json
{
  "camera_movements": {
    "dolly_in": "镜头平滑推进,由远及近展示空间",
    "dolly_out": "镜头平滑拉远,展示整体布局",
    "pan_left": "镜头水平向左扫视,展示空间宽度",
    "pan_right": "镜头水平向右扫视,全景展示",
    "tilt_up": "镜头向上仰视,展示空间高度",
    "tilt_down": "镜头向下俯视,展示空间布局",
    "orbit": "镜头环绕主体旋转,360度展示",
    "zoom_in": "镜头变焦推进,特写重点区域",
    "static": "静止镜头,微小动态元素"
  },
  "atmosphere": {
    "warm": "暖色调,温馨氛围,柔和光线",
    "bright": "明亮通透,自然光充足,清新感",
    "dramatic": "戏剧化光影,对比强烈,高级感",
    "cozy": "温馨舒适,氛围灯光,居家感"
  },
  "quality": {
    "standard": "高清画质,细节清晰,色彩准确",
    "premium": "4K超清,极致细节,专业级画质,电影感"
  }
}
```

---

## ✅ 决策总结

### 关键决策

1. **✅ 使用现有Wan技能包** - 立即可用,无需开发新技能包
2. **✅ 采用Wan i2v (wan2.5-i2v-preview)** - 成本低、中文友好
3. **✅ Z2生成多角度概念图** - 每场景5-6个角度
4. **✅ 跳过Z3 3D建模环节** - 简化技术路线,Z3作为可选扩展
5. **✅ 使用中文Prompt** - 更符合中国场景,效果更好

### 优势汇总

```yaml
技术优势:
  - 使用现有技能包,立即可用
  - 技术栈统一(阿里云生态)
  - 中文Prompt效果更好
  - 简化技术路线(Z2直接到Z4)

成本优势:
  - 总成本: ¥2.40 (vs Luma $4.74)
  - 节省: 93%
  - 支付方式: 人民币,无汇率损失

集成优势:
  - Wan技能包已验证
  - API文档完整
  - 测试脚本齐全
  - 无需额外开发
```

---

## 📅 下一步行动

**立即开始**: Day 2 - 重写Z4-建筑动画AIGC助手.md

**重点内容**:
1. 明确Z4基于Wan i2v
2. 定义与Z2的协同机制(多角度生成要求)
3. 设计中文Prompt模板库
4. 建立6-Step AIGC工作流
5. 定义质量标准和验收规范

---

**报告编制**: Z4-建筑动画AIGC助手(筹备阶段)
**审核**: QQ-总指挥官
**版本**: v2.0.0 (重大调整)
**日期**: 2025-10-28
**状态**: ✅ 技术方案调整完成,准备进入Day 2
