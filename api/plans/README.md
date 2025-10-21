# E系列智能体JSON执行计划

> **规范·计划·执行三层架构的第2层**: 存储所有E系列智能体(E1-E9)的标准化JSON执行计划，将用户意图转化为可执行的、版本可控的配置文件。

## 📋 目录说明

本目录包含E1-E9共9个智能体的JSON执行计划，每个智能体对应一个子目录，用于存储该智能体的任务模板(template.json)和用户自定义任务配置。

## 🎯 核心理念

**配置与代码完全分离**
- ✅ 配置驱动: 任务差异化通过JSON计划实现，无需修改代码
- ✅ 版本可控: 执行计划可纳入Git版本控制、可复用、可追溯
- ✅ 标准统一: 所有E系列智能体使用统一的5字段JSON格式
- ✅ 模板先行: 每个智能体提供template.json作为标准参考
- ✅ 单一执行器: 所有计划通过`api/projects/nano-banana-api/execute_plan.py`统一执行

## 📂 目录结构

```
api/plans/
├── e1-text-to-image/          # E1 餐饮文生图AIGC智能体
│   ├── template.json          # 标准模板
│   └── [用户任务].json        # 用户自定义任务
│
├── e2-image-to-image/         # E2 餐饮图生图AIGC智能体
│   ├── template.json
│   └── [用户任务].json
│
├── e3-image-recognition/      # E3 餐饮图片识别AIGC智能体
│   ├── template.json
│   └── [用户任务].json
│
├── e4-smart-repair/           # E4 餐饮智能修复AIGC智能体
│   ├── template.json
│   └── [用户任务].json
│
├── e5-structure-control/      # E5 餐饮结构控制AIGC智能体
│   ├── template.json
│   └── [用户任务].json
│
├── e6-creative-combination/   # E6 餐饮多图融合AIGC智能体
│   ├── template.json
│   └── [用户任务].json
│
├── e7-character-consistency/  # E7 餐饮角色一致性AIGC智能体
│   ├── template.json
│   └── [用户任务].json
│
├── e8-design-iteration/       # E8 餐饮设计迭代AIGC智能体
│   ├── template.json
│   └── [用户任务].json
│
├── e9-super-resolution/       # E9 餐饮超分增强AIGC智能体
│   ├── template.json
│   └── [用户任务].json
│
└── README.md                  # 本文档
```

## 📋 标准化JSON格式

> 所有E1-E9智能体使用统一的5个顶层字段，确保执行计划的一致性和互操作性。

### 5个顶层字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| agent_id | string | ✅ | 智能体标识(E1-E9) |
| task_description | string | ✅ | 任务的自然语言描述 |
| input_data | object | ✅ | 智能体特定的输入参数(各智能体不同) |
| output_settings | object | ✅ | 输出配置(路径、格式) |
| metadata | object | ✅ | 元数据(时间、创建者、版本) |

### 完整JSON模板

```json
{
  "agent_id": "E[X]",
  "task_description": "任务的自然语言描述",

  "input_data": {
    // 智能体特定的输入参数
    // E1-E9各不相同，详见下方"各智能体input_data规范"
  },

  "output_settings": {
    "save_path": "output/images/e[x]-*/",
    "format": "png",
    "quality": 95
  },

  "metadata": {
    "created_at": "2025-10-11T10:30:00",
    "created_by": "用户名或智能体名",
    "version": "1.0",
    "notes": "可选的备注信息"
  }
}
```

## 🔄 使用流程

### 第1步: 基于模板创建任务

```bash
# 复制模板创建新任务
cp api/plans/e1-text-to-image/template.json \
   api/plans/e1-text-to-image/my-hotpot-poster.json

# 编辑任务配置(修改 input_data 和 output_settings)
# 示例: 生成一张火锅店开业海报
```

### 第2步: 编辑任务配置

```yaml
必须修改的字段:
  - task_description: 清晰描述任务目标
  - input_data: 根据智能体类型填写具体参数
  - output_settings.save_path: 指定输出路径

可选修改的字段:
  - output_settings.format: png/jpg/webp
  - output_settings.quality: 图片质量(仅jpg/webp)
  - metadata.notes: 添加备注信息
```

### 第3步: 执行任务计划

```bash
# 使用统一执行器执行计划
python api/projects/nano-banana-api/execute_plan.py \
  --plan api/plans/e1-text-to-image/my-hotpot-poster.json

# 批量执行
for plan in api/plans/e1-text-to-image/*.json; do
  python api/projects/nano-banana-api/execute_plan.py --plan "$plan"
  sleep 5  # 避免API限流
done
```

## 📚 各智能体input_data规范

### E1 - 餐饮文生图AIGC智能体

```json
"input_data": {
  "text_prompt": "文字描述,如'成都火锅店盛大开业，红色喜庆氛围'",
  "style": "风格标签,如'商业摄影'、'美食摄影'等",
  "negative_prompt": "负面提示词(可选),如'low quality, blurry'"
}
```

**完整示例**:
```json
{
  "agent_id": "E1",
  "task_description": "生成火锅店开业海报",
  "input_data": {
    "text_prompt": "中国成都火锅店盛大开业，红色喜庆氛围，商业摄影，高品质美食摄影",
    "style": "商业摄影",
    "negative_prompt": "low quality, blurry, distorted"
  },
  "output_settings": {
    "save_path": "output/images/e1-text-to-image/",
    "format": "png"
  },
  "metadata": {
    "created_at": "2025-10-11T10:30:00",
    "created_by": "用户名",
    "version": "1.0"
  }
}
```

### E2 - 餐饮图生图AIGC智能体

```json
"input_data": {
  "image_url": "原始图片路径",
  "operation_type": "optimization|style_transfer|local_edit",
  "text_prompt": "指导文字",
  "edit_config": {
    // 操作特定配置
  }
}
```

### E3 - 餐饮图片识别AIGC智能体

```json
"input_data": {
  "image_url": "图片路径",
  "recognition_type": "content|quality|scene|commercial",
  "detail_level": "basic|detailed|professional"
}
```

### E4 - 餐饮智能修复AIGC智能体

```json
"input_data": {
  "image_url": "待修复图片路径",
  "repair_type": "defect_removal|fill_content|expand_canvas",
  "repair_config": {
    // 修复配置
  }
}
```

### E5 - 餐饮结构控制AIGC智能体

```json
"input_data": {
  "reference_image": "结构参考图",
  "target_description": "目标内容描述",
  "control_type": "pose|depth|edge|segmentation",
  "control_strength": 0.5
}
```

### E6 - 餐饮多图融合AIGC智能体

```json
"input_data": {
  "source_images": ["图片1", "图片2", "图片3"],
  "fusion_type": "element_extraction|style_blend|creative_montage",
  "fusion_config": {
    // 融合配置
  }
}
```

### E7 - 餐饮角色一致性AIGC智能体

```json
"input_data": {
  "character_reference": "角色参考图",
  "scene_description": "新场景描述",
  "consistency_level": "high|medium|flexible"
}
```

### E8 - 餐饮设计迭代AIGC智能体

```json
"input_data": {
  "current_version": "当前版本图片",
  "feedback": "用户反馈",
  "iteration_type": "feedback_response|version_refinement|style_adjustment",
  "iteration_goals": ["目标1", "目标2"]
}
```

### E9 - 餐饮超分增强AIGC智能体

```json
"input_data": {
  "image_url": "原始图片",
  "target_resolution": "4096x4096|8K|print_quality",
  "enhancement_level": "low|medium|high|ultra"
}
```

## 最佳实践

### 命名规范

```yaml
执行计划文件命名:
  格式: task-{序号}-{简要描述}.json
  示例: task-001-hotpot-opening.json

目录命名:
  格式: {agent_id}-{operation_category}
  示例: e1-text-to-image
```

### 版本控制

```yaml
执行计划版本管理:
  - 所有执行计划纳入Git版本控制
  - 重要执行计划创建备份
  - 使用有意义的commit message
  - 标注执行计划的修改原因
```

### 文档更新

```yaml
执行计划文档维护:
  - 每个智能体目录包含README.md
  - 说明该智能体的执行计划特点
  - 列出常用的执行计划模板
  - 提供执行计划使用示例
```

---

**配置层版本**: v1.0.0
**创建日期**: 2025-01-09
**维护标准**: 遵循三层架构规范
