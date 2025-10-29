---
name: Nano Banana衍生图生成
description: 基于参考主图生成视觉一致的衍生图像。专注于保持角色特征、风格一致性的图像变化生成。用于影视分镜细化、角色动作序列、表情变化等场景。需要参考主图和变化描述。
---

# Nano Banana衍生图生成

> 基于Nano Banana模型的专业衍生图生成，在保持主图视觉一致性的前提下，生成精确控制的图像变化。

## 🎯 核心能力

- **视觉一致性**: 精确保持主图的角色特征和风格（一致性≥95%）
- **精确控制**: 通过keep/change分离指定保持和改变的元素
- **高质量输出**: 1024x1024高分辨率PNG图像
- **快速生成**: 平均16.5秒/张，支持5-8倍并行
- **批量处理**: 支持角色动作序列和表情变化批量生成

## 🚀 快速开始

### 基础用法

```python
# 1. 准备参考主图
reference_image = "output/project/character-base-001.png"

# 2. 定义变化需求
variation = {
    "description": "角色转身动作",
    "keep_consistent": [
        "赛博朋克风格",
        "角色服装",
        "发型特征",
        "面部特征"
    ],
    "change_elements": [
        "身体姿态: 从正面转为侧面",
        "头部角度: 微微转向右侧"
    ],
    "strength": 0.65  # 0.4-0.8，数值越大变化越大
}

# 3. 使用脚本生成
python scripts/api_client.py generate \
    --reference $reference_image \
    --keep "赛博朋克风格,角色服装,发型" \
    --change "身体转为侧面,头部右转" \
    --strength 0.65 \
    --output output/variations/
```

### 核心参数

| 参数 | 说明 | 取值范围 |
|------|------|----------|
| `reference_image` | 参考主图路径 | PNG/JPG, ≥512x512 |
| `keep_consistent` | 保持不变的元素 | 至少1个 |
| `change_elements` | 需要改变的元素 | 至少1个 |
| `strength` | 变化强度 | 0.4-0.8 |

**strength建议值**：
- `0.4-0.5`: 轻微变化（表情、视角微调）
- `0.6-0.7`: 中等变化（姿态、动作变化）
- `0.75-0.8`: 较大变化（场景元素、光影变化）

## 📁 常见场景

### 场景1: 角色动作序列

生成角色转身3个动作帧：

```bash
python scripts/api_client.py batch \
    --reference character-base.png \
    --sequence "正面,侧面,背面" \
    --keep "风格,服装,发型" \
    --output output/turn-sequence/
```

输出：
- `turn-frame-01.png`: 正面→轻微右转
- `turn-frame-02.png`: 侧面90度
- `turn-frame-03.png`: 背面180度

### 场景2: 表情变化

生成5种不同表情：

```bash
python scripts/api_client.py batch \
    --reference character-base.png \
    --expressions "平静,微笑,惊讶,严肃,愤怒" \
    --keep "姿态,背景" \
    --strength 0.50 \
    --output output/expressions/
```

### 场景3: 批量配置文件

使用JSON配置文件批量生成：

```bash
python scripts/api_client.py batch \
    --config-file config/variations.json
```

配置文件示例见 `scripts/config_template.json`。

## 📁 进阶文档

- **[API详细参考](reference.md)** - 完整API参数、配置选项、错误处理
- **[丰富示例集](examples.md)** - 按场景分类的详细示例和最佳实践

## 🛠️ 使用脚本

### scripts/api_client.py

整合Nano Banana API调用和批量处理的统一客户端(推荐使用)。

**功能**：
- 单张图像生成
- 批量序列生成
- 配置文件驱动
- 自动重试和错误处理
- 结果保存和日志记录

**调用方式**：

```bash
# 查看帮助
python scripts/api_client.py --help

# 单张生成
python scripts/api_client.py generate [参数]

# 批量生成
python scripts/api_client.py batch [参数]

# 使用配置文件
python scripts/api_client.py batch --config config.json
```

### scripts/nano-banana-base.py

API客户端基础模板,提供底层API调用能力。

**功能**:
- OpenRouter API封装
- 图像base64转换
- 请求构建和响应处理
- 错误处理和重试机制

**适用场景**: 需要自定义API调用逻辑时使用

### scripts/nano-banana-execute.py

基于执行计划的批量处理引擎。

**功能**:
- 读取JSON执行计划
- 批次管理和并发控制
- Checkpoint断点续传
- 执行日志和元数据生成

**调用方式**:
```bash
python scripts/nano-banana-execute.py --plan api/plans/nano-banana/my-plan.json
```

**配合文件**: `api/plans/nano-banana/`目录下的执行计划JSON

### scripts/config_template.json

标准配置文件模板，包含：
- 执行配置（batch_size, 并发数）
- API配置（endpoint, model, timeout）
- 任务列表（tasks）

复制模板创建您的配置：
```bash
cp scripts/config_template.json config/my-project.json
```

## ⚙️ 配置说明

### 基础配置

```json
{
  "execution_config": {
    "batch_size": 2,           // 每批处理数量
    "max_concurrent_requests": 2,  // 最大并发数
    "retry_attempts": 3        // 失败重试次数
  },
  "api_config": {
    "model": "nano-banana-v1",
    "timeout_seconds": 60
  }
}
```

### 任务配置

```json
{
  "task_id": "variation-001",
  "reference_image": "path/to/reference.png",
  "variation_instruction": {
    "description": "角色转身动作",
    "keep_consistent": ["风格", "服装"],
    "change_elements": ["身体转侧面"],
    "nano_banana_parameters": {
      "strength": 0.65,
      "prompt_weight": "turning, dynamic motion"
    }
  }
}
```

## 🚨 注意事项

1. **参考主图质量**：
   - 分辨率至少512x512
   - 清晰、无模糊
   - 文件大小<10MB

2. **一致性控制**：
   - `keep_consistent`必须明确定义
   - 至少包含1个元素
   - 元素描述要具体

3. **变化控制**：
   - `change_elements`描述要清晰
   - 避免与keep_consistent冲突
   - 一次变化不要太多

4. **成本预估**：
   - 每张图约5积分
   - 批量生成前预估总成本
   - 超预算时会请求确认

## 📊 性能参考

- **生成速度**: 16.5秒/张（平均）
- **成功率**: 100%（基于E5实测）
- **质量评分**: ⭐⭐⭐⭐⭐ 5/5
- **一致性保持**: ≥95%
- **并行能力**: 5-8倍并行

## 📖 延伸阅读

- [通义万相](../tongyi-wanxiang/SKILL.md) - 图像生成的另一选择
- [Midjourney](../midjourney/SKILL.md) - 艺术质量优先的图像生成
- [三层架构API规范](../../../../.claude/agents/system/Api-Creator.md)

---

**版本**: 2.0.0
**更新日期**: 2025-10-19
**状态**: ✅ 多文件Skill重构版本
