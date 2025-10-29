# Nano Banana 使用示例集

> 本文档提供按场景分类的详细示例，包括配置代码、预期输出和最佳实践。

## 📁 示例索引

1. [角色动作序列](#1-角色动作序列)
2. [表情变化序列](#2-表情变化序列)
3. [场景光影调整](#3-场景光影调整)
4. [视角变化](#4-视角变化)
5. [服装变化](#5-服装变化)
6. [批量处理工作流](#6-批量处理工作流)

---

## 1. 角色动作序列

### 场景：角色转身3帧动画

**需求描述**：
基于正面角色主图，生成转身动作的3个关键帧：正面→侧面→背面

**参考主图**：`character-base-front.png`

#### 配置文件

```json
{
  "plan_id": "nano-turn-sequence-001",
  "execution_config": {
    "batch_size": 3,
    "max_concurrent_requests": 2
  },
  "batches": [
    {
      "batch_id": 1,
      "tasks": [
        {
          "task_id": "turn-frame-01",
          "reference_image": "character-base-front.png",
          "variation_instruction": {
            "description": "轻微右转15度",
            "keep_consistent": [
              "赛博朋克风格",
              "角色服装-黑色皮夹克",
              "霓虹蓝发型",
              "面部特征"
            ],
            "change_elements": [
              "身体姿态: 轻微右转15度",
              "头部角度: 保持正面但眼神右移",
              "双臂: 开始摆动准备转身"
            ],
            "nano_banana_parameters": {
              "strength": 0.60,
              "prompt_weight": "slight turn, beginning rotation"
            }
          }
        },
        {
          "task_id": "turn-frame-02",
          "reference_image": "character-base-front.png",
          "variation_instruction": {
            "description": "侧面90度",
            "keep_consistent": [
              "赛博朋克风格",
              "角色服装-黑色皮夹克",
              "霓虹蓝发型",
              "面部特征"
            ],
            "change_elements": [
              "身体姿态: 完全侧面90度",
              "头部角度: 侧面轮廓",
              "双臂: 自然摆动中"
            ],
            "nano_banana_parameters": {
              "strength": 0.70,
              "prompt_weight": "side view, 90 degree turn, profile"
            }
          }
        },
        {
          "task_id": "turn-frame-03",
          "reference_image": "character-base-front.png",
          "variation_instruction": {
            "description": "背面180度",
            "keep_consistent": [
              "赛博朋克风格",
              "角色服装-黑色皮夹克",
              "霓虹蓝发型"
            ],
            "change_elements": [
              "身体姿态: 完全背面180度",
              "头部角度: 后脑勺可见",
              "双臂: 完成摆动动作"
            ],
            "nano_banana_parameters": {
              "strength": 0.75,
              "prompt_weight": "back view, 180 degree turn, rear view"
            }
          }
        }
      ]
    }
  ]
}
```

#### 命令行调用

```bash
python scripts/api_client.py batch \
    --config examples/turn-sequence.json \
    --output output/turn-sequence/
```

#### 预期输出

```
output/turn-sequence/
  ├── turn-frame-01.png  # 轻微右转15度
  ├── turn-frame-02.png  # 侧面90度
  └── turn-frame-03.png  # 背面180度
```

#### 关键参数说明

- **strength递增策略**: 0.60 → 0.70 → 0.75
  - 变化越大，strength越高
  - 保证渐进式转变自然流畅

- **keep_consistent精细化**:
  - 第1-2帧保持"面部特征"
  - 第3帧（背面）移除面部要求

---

## 2. 表情变化序列

### 场景：情绪光谱5表情

**需求描述**：
基于平静表情主图，生成5种情绪状态：平静→喜悦→惊讶→严肃→愤怒

**参考主图**：`character-neutral.png`

#### 配置文件（精简版）

```json
{
  "batches": [{
    "tasks": [
      {
        "task_id": "expr-joy",
        "variation_instruction": {
          "description": "喜悦-灿烂笑容",
          "keep_consistent": ["姿态", "背景", "光线", "服装"],
          "change_elements": [
            "面部表情: 灿烂笑容",
            "眼睛: 眯成月牙形",
            "嘴角: 大幅上扬",
            "眉毛: 舒展上扬"
          ],
          "nano_banana_parameters": {
            "strength": 0.50,
            "prompt_weight": "bright smile, joyful, happy expression"
          }
        }
      },
      {
        "task_id": "expr-surprise",
        "variation_instruction": {
          "description": "惊讶-瞪大双眼",
          "keep_consistent": ["姿态", "背景", "光线", "服装"],
          "change_elements": [
            "面部表情: 惊讶",
            "眼睛: 瞪大圆睁",
            "嘴巴: 微微张开O形",
            "眉毛: 高挑上扬"
          ],
          "nano_banana_parameters": {
            "strength": 0.55,
            "prompt_weight": "surprised, shocked, wide eyes"
          }
        }
      },
      {
        "task_id": "expr-serious",
        "variation_instruction": {
          "description": "严肃-凝重表情",
          "keep_consistent": ["姿态", "背景", "光线", "服装"],
          "change_elements": [
            "面部表情: 严肃凝重",
            "眼神: 锐利直视",
            "嘴唇: 紧抿成线",
            "眉毛: 微蹙集中"
          ],
          "nano_banana_parameters": {
            "strength": 0.50,
            "prompt_weight": "serious, stern, focused gaze"
          }
        }
      },
      {
        "task_id": "expr-anger",
        "variation_instruction": {
          "description": "愤怒-怒容",
          "keep_consistent": ["姿态", "背景", "光线", "服装"],
          "change_elements": [
            "面部表情: 愤怒",
            "眼神: 怒目而视",
            "眉毛: 紧皱下压",
            "嘴角: 下沉或咬牙"
          ],
          "nano_banana_parameters": {
            "strength": 0.55,
            "prompt_weight": "angry, furious, intense glare"
          }
        }
      }
    ]
  }]
}
```

#### 最佳实践

1. **表情强度控制**：
   - 微表情（微笑、沉思）：strength = 0.45-0.50
   - 中等表情（喜悦、惊讶）：strength = 0.50-0.55
   - 强烈表情（愤怒、恐惧）：strength = 0.55-0.60

2. **多维度描述**：
   - 不仅描述整体表情
   - 细化到眼睛、嘴、眉毛
   - 提升生成准确性

---

## 3. 场景光影调整

### 场景：同一场景的不同光线氛围

**需求描述**：
基于白天场景，生成黄昏和夜晚版本

**参考主图**：`scene-daytime.png`

#### 任务1: 黄昏氛围

```json
{
  "task_id": "lighting-dusk",
  "variation_instruction": {
    "description": "黄昏暖光氛围",
    "keep_consistent": [
      "场景布局",
      "建筑元素",
      "角色位置",
      "构图"
    ],
    "change_elements": [
      "光线方向: 从侧面低角度照射",
      "色温: 温暖的橙黄色调",
      "环境亮度: 整体调暗20%",
      "阴影: 拉长的斜影",
      "天空: 黄昏渐变色"
    ],
    "nano_banana_parameters": {
      "strength": 0.70,
      "prompt_weight": "dusk lighting, warm golden hour, sunset atmosphere"
    }
  }
}
```

#### 任务2: 夜晚氛围

```json
{
  "task_id": "lighting-night",
  "variation_instruction": {
    "description": "夜晚霓虹光氛围",
    "keep_consistent": [
      "场景布局",
      "建筑元素",
      "角色位置",
      "构图"
    ],
    "change_elements": [
      "光线来源: 霓虹灯、路灯人工光源",
      "色温: 冷色调蓝紫色",
      "环境亮度: 整体暗调,局部高光",
      "阴影: 深邃的黑色阴影",
      "天空: 深蓝夜空"
    ],
    "nano_banana_parameters": {
      "strength": 0.75,
      "prompt_weight": "night scene, neon lights, dark atmosphere, cyberpunk lighting"
    }
  }
}
```

#### 注意事项

- 光影变化需要较高strength（0.70-0.80）
- keep_consistent要强调场景布局和构图
- 色温变化会影响整体氛围，需详细描述

---

## 4. 视角变化

### 场景：多角度产品展示

**需求描述**：
基于正面产品图，生成45度和侧面视角

**参考主图**：`product-front.png`

#### 配置示例

```json
{
  "tasks": [
    {
      "task_id": "view-45deg",
      "variation_instruction": {
        "description": "45度斜视角",
        "keep_consistent": [
          "产品外观",
          "材质质感",
          "颜色",
          "细节特征"
        ],
        "change_elements": [
          "视角: 从正面改为45度斜角",
          "可见面: 同时看到正面和侧面",
          "景深: 轻微透视效果"
        ],
        "nano_banana_parameters": {
          "strength": 0.65
        }
      }
    },
    {
      "task_id": "view-side",
      "variation_instruction": {
        "description": "完整侧面视角",
        "keep_consistent": [
          "产品外观",
          "材质质感",
          "颜色",
          "细节特征"
        ],
        "change_elements": [
          "视角: 完全侧面90度",
          "可见面: 只看侧面轮廓",
          "厚度展示: 产品厚度清晰可见"
        ],
        "nano_banana_parameters": {
          "strength": 0.70
        }
      }
    }
  ]
}
```

---

## 5. 服装变化

### 场景：同一角色不同服装

**参考主图**：`character-casual.png`（休闲装）

#### 任务：生成正装版本

```json
{
  "task_id": "outfit-formal",
  "variation_instruction": {
    "description": "商务正装",
    "keep_consistent": [
      "角色面部特征",
      "发型",
      "体型",
      "姿态",
      "背景"
    ],
    "change_elements": [
      "服装: 从休闲装改为深色西装",
      "领带: 添加深蓝色领带",
      "整体风格: 更正式商务"
    ],
    "nano_banana_parameters": {
      "strength": 0.70,
      "prompt_weight": "formal business suit, professional attire"
    }
  }
}
```

#### ⚠️ 注意

- 服装大幅变化需要strength=0.70-0.75
- 必须明确保持面部特征和姿态
- 可能需要多次迭代才能达到理想效果

---

## 6. 批量处理工作流

### 场景：完整的角色表情库生成

**目标**：
从1张主图生成10种表情的完整表情库

#### 工作流程

**Step 1**: 准备配置文件

```bash
# 复制模板
cp scripts/config_template.json config/expression-library.json

# 编辑配置，添加10个表情任务
```

**Step 2**: 批量执行

```bash
python scripts/api_client.py batch \
    --config config/expression-library.json \
    --output output/expression-library/ \
    --parallel 4
```

**Step 3**: 质量检查

```bash
# 查看生成日志
cat output/expression-library/generation.log

# 检查失败任务
grep "FAILED" output/expression-library/generation.log
```

**Step 4**: 重试失败任务

```bash
# 如果有失败任务，单独重试
python scripts/api_client.py retry \
    --log output/expression-library/generation.log \
    --failed-only
```

#### 预期输出结构

```
output/expression-library/
  ├── expr-neutral.png
  ├── expr-happy.png
  ├── expr-sad.png
  ├── expr-angry.png
  ├── expr-surprised.png
  ├── expr-fearful.png
  ├── expr-disgusted.png
  ├── expr-confused.png
  ├── expr-excited.png
  ├── expr-thoughtful.png
  ├── generation.log
  └── config.json （备份）
```

---

## 💡 通用最佳实践

### 1. 参考图像准备

```bash
# 确保参考图像质量
- 分辨率: ≥1024x1024 （最佳）
- 格式: PNG（无损）
- 清晰度: 无模糊、无伪影
- 构图: 主体清晰、背景简洁
```

### 2. 配置参数调优

```python
# 保守策略（推荐）
strength_start = 0.55  # 从中等值开始
# 观察结果后调整
if 变化不够: strength += 0.05
if 一致性差: strength -= 0.05

# 激进策略（不推荐）
strength = 0.75  # 可能丢失一致性
```

### 3. 批量任务优化

```json
{
  "execution_config": {
    // 小批次，避免全部失败
    "batch_size": 2-4,

    // 适度并发，避免API限流
    "max_concurrent_requests": 2-4,

    // 足够的重试次数
    "retry_attempts": 3
  }
}
```

### 4. 成本控制

```python
# 预估成本
num_tasks = 10
cost_per_task = 5  # 积分
total_cost = num_tasks * cost_per_task
print(f"预估总成本: {total_cost}积分")

# 分批执行（测试+生产）
batch1 = tasks[:2]  # 先测试2个
if batch1_success:
    batch2 = tasks[2:]  # 再执行剩余
```

---

## 📚 延伸示例

更多复杂场景示例请参考：

- [角色设计工作流](../../../project/赛博朋克短片测试/角色设计工作流.md)
- [分镜细化流程](../../../project/赛博朋克短片测试/分镜细化流程.md)
- [E5成功案例](../../../../api/projects/nano-banana-api/SUCCESS_CASES.md)

---

**版本**: 2.0.0
**更新日期**: 2025-10-19
