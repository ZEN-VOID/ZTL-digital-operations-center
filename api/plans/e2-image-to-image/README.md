# E2图生图执行计划目录

> E2智能体(餐饮图生图AIGC)的JSON执行计划存储目录，支持图片优化、风格迁移、局部编辑等多种图片处理任务。

## 📋 目录概述

存储E2智能体的执行计划文件，通过标准化的JSON格式定义图生图任务，支持基于原图的专业级图片处理和创意编辑。

## 🎯 E2智能体能力

**核心功能**: 图片生成图片(Image-to-Image)
**专业领域**: 餐饮图片优化、风格转换、局部编辑
**输出质量**: 保持原图分辨率或更高，PNG格式

**三大操作类型**:
1. **optimization** - 图片优化增强
2. **style_transfer** - 风格迁移转换
3. **local_edit** - 局部元素编辑

## 📁 文件类型

### template.json - 标准模板
**作用**: 提供E2执行计划的标准格式
**包含**: operation_type、image_url、text_prompt等字段示例

### task-*.json - 用户任务
**命名格式**: `task-[序号]-[操作类型]-[描述].json`
**示例**: `task-001-dish-style-transfer.json`

### [项目名]-*.json - 专项任务
**命名格式**: `[项目]-[操作]-[日期].json`
**示例**: `houxiang-baozi-poster-redesign-20251011.json`

## 📝 JSON执行计划标准格式

```json
{
  "agent_id": "E2",
  "task_description": "任务描述",
  "input_data": {
    "image_url": "原始图片路径",
    "operation_type": "optimization|style_transfer|local_edit",
    "text_prompt": "指导文字",
    "edit_config": {
      "edit_areas": [
        {
          "target": "编辑目标",
          "modification": "修改内容",
          "requirement": "要求说明"
        }
      ]
    }
  },
  "output_settings": {
    "save_path": "output/images/2-image-processing/[子目录]/",
    "format": "png",
    "quality": 95
  },
  "metadata": {
    "created_at": "2025-10-11T15:00:00",
    "created_by": "创建者",
    "version": "1.0"
  }
}
```

## 🔧 input_data字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| image_url | string | ✅ | 原始图片路径(相对项目根目录) |
| operation_type | string | ✅ | 操作类型(optimization/style_transfer/local_edit) |
| text_prompt | string | ❌ | 文字指导(可从edit_config自动生成) |
| edit_config | object | ❌ | 局部编辑配置(local_edit时使用) |
| operation_params | object | ❌ | 操作特定参数 |

## 🎨 操作类型详解

### 1. optimization - 图片优化

**适用场景**:
- 提升图片清晰度和细节
- 增强色彩饱和度
- 修复图片瑕疵
- 优化光线和对比度

**配置示例**:
```json
{
  "operation_type": "optimization",
  "text_prompt": "增强图片清晰度，优化色彩，提升整体质量"
}
```

**输出目录**: `output/images/2-image-processing/optimization/`

### 2. style_transfer - 风格迁移

**适用场景**:
- 将照片转为艺术风格
- 应用特定视觉风格
- 改变图片整体氛围
- 品牌风格统一

**配置示例**:
```json
{
  "operation_type": "style_transfer",
  "text_prompt": "将这张菜品图转换为水彩画风格，保持食物的主体特征"
}
```

**输出目录**: `output/images/2-image-processing/style_transfer/`

### 3. local_edit - 局部编辑

**适用场景**:
- Logo替换和修改
- 文字内容更新
- 配色调整
- 元素添加或删除

**配置示例**:
```json
{
  "operation_type": "local_edit",
  "text_prompt": "修改Logo为新品牌名称，调整背景色为蓝色",
  "edit_config": {
    "edit_areas": [
      {
        "target": "Logo文字",
        "modification": "替换为'NEW BRAND'",
        "requirement": "保持Logo位置和大小不变"
      },
      {
        "target": "背景色",
        "modification": "改为深蓝色",
        "requirement": "保持视觉层次和对比度"
      }
    ]
  }
}
```

**输出目录**: `output/images/2-image-processing/local_edit/`

## 🚀 使用流程

### 创建新任务

**步骤1**: 准备原始图片
```bash
# 确保图片存在于项目中
ls -la input/项目名/图片.jpg
```

**步骤2**: 复制模板并编辑
```bash
cp api/plans/e2-image-to-image/template.json \
   api/plans/e2-image-to-image/task-002-my-edit.json

# 编辑JSON文件，填写:
# - image_url: 原图路径
# - operation_type: 操作类型
# - text_prompt: 编辑指导
```

**步骤3**: 执行任务
```bash
python api/projects/nano-banana-api/execute_plan.py \
  --plan api/plans/e2-image-to-image/task-002-my-edit.json
```

**步骤4**: 查看结果
- 根据operation_type查找对应输出目录
- 文件名格式: `[operation_type]_YYYYMMDDHHmmss_1.png`

## 💡 text_prompt编写技巧

### local_edit的prompt构建

**方法1: 手动编写**
```json
"text_prompt": "修改Logo为HOUXIANG BAOZI，背景改为蓝色，包子改为白色粉笔质感"
```

**方法2: 从edit_config自动生成**
```json
"edit_config": {
  "edit_areas": [
    {"target": "Logo", "modification": "HOUXIANG BAOZI"},
    {"target": "背景", "modification": "蓝色"},
    {"target": "包子", "modification": "白色粉笔质感"}
  ]
}
// execute_plan.py会自动生成: "Logo: HOUXIANG BAOZI; 背景: 蓝色; 包子: 白色粉笔质感"
```

### optimization的prompt建议

```
增强这张[菜品/海报]图片的整体质量：
- 提升清晰度和细节表现
- 优化色彩饱和度和对比度
- 增强光线效果
- 保持原图构图和主体特征
```

### style_transfer的prompt建议

```
将这张图片转换为[风格名称]风格：
- 保持主体元素不变
- 应用[风格]的视觉特征
- 保证转换后的可识别性
- 适合[用途]使用
```

## 🔍 任务示例分析

### 示例1: 吼巷包子海报重设计

**文件**: `houxiang-baozi-poster-redesign-20251011.json`

**任务描述**: 修改吼巷海报 - 更换Logo + 蓝底配色 + 白色粉笔质感

**关键配置**:
```json
{
  "operation_type": "local_edit",
  "text_prompt": "修改这张海报设计，保持整体构图和版式不变，进行以下调整：
1. 将Logo文字替换为'HOUXIANG BAOZI'
2. 将背景色改为深蓝色调
3. 将包子部分改为白色粉笔手绘质感效果
4. 保持海报的整体风格和设计感
5. 确保文字清晰可读，视觉层次分明",
  "edit_config": {
    "edit_areas": [
      {
        "target": "Logo文字",
        "modification": "替换为'HOUXIANG BAOZI'",
        "requirement": "保持Logo的位置、大小和风格"
      },
      // ... 其他编辑区域
    ]
  }
}
```

**设计要点**:
- 使用详细的text_prompt指导编辑
- edit_config提供结构化的编辑要求
- 多个编辑区域协同处理

### 示例2: 菜品风格迁移

**文件**: `task-001-dish-style-transfer.json`

**任务描述**: 将菜品图转换为艺术风格

**操作类型**: style_transfer

## ⚠️ 常见问题

### Q1: image_url路径错误
**错误**: `FileNotFoundError: image not found`
**解决**: 使用项目相对路径，如`input/吼巷/设计/海报/1.jpg`

### Q2: operation_type不正确
**错误**: `ValueError: invalid operation_type`
**解决**: 只能使用optimization/style_transfer/local_edit三种

### Q3: text_prompt为空但edit_config也为空
**解决**: local_edit必须提供text_prompt或edit_config之一

### Q4: 输出质量不理想
**解决**:
- 增强text_prompt的详细程度
- 使用edit_config提供结构化要求
- 尝试调整operation_params参数

## 🔗 相关文档

- [E2智能体文档](../../../.claude/agents/E2.md)
- [统一执行器文档](../../projects/nano-banana-api/README.md)
- [execute_plan.py参数映射](../../projects/nano-banana-api/execute_plan.py#L59-L79)
- [输出目录说明](../../../output/images/README.md#2-e2图生图输出-2-image-processing)

## 📊 最佳实践

**任务规划**:
- 明确操作类型(optimization/style_transfer/local_edit)
- 准备高质量原图(分辨率越高效果越好)
- 详细描述编辑需求

**配置编写**:
- local_edit优先使用edit_config结构化配置
- text_prompt应具体、可执行
- 保持JSON格式正确性

**质量控制**:
- 对比原图和生成结果
- 记录成功的prompt模板
- 迭代优化配置参数

**版本管理**:
- 重要任务使用项目名-日期命名
- 保留编辑历史JSON文件
- 记录参数调整过程

---

**目录版本**: v1.0.0
**创建日期**: 2025-10-11
**智能体**: E2 - 餐饮图生图AIGC智能体
**执行器**: api/projects/nano-banana-api/execute_plan.py
**参数映射**: Lines 59-79 (E2专用逻辑)
