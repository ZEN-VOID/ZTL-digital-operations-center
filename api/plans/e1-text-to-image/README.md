# E1文生图执行计划目录

> E1智能体(餐饮文生图AIGC)的JSON执行计划存储目录，基于三层架构的标准化任务配置文件。

## 📋 目录概述

存储E1智能体的执行计划文件，通过标准化的JSON格式定义文生图任务，支持从文字描述到高质量餐饮设计图片的自动化生成。

## 🎯 E1智能体能力

**核心功能**: 文字生成图片(Text-to-Image)
**专业领域**: 餐饮行业设计内容生成
**输出质量**: 1024x1024或更高分辨率的PNG图片

**典型应用场景**:
- 餐饮海报设计(开业、促销、节日)
- 菜品展示图生成
- 营销物料图片创作
- 品牌视觉素材生成

## 📁 文件类型

### template.json - 标准模板
**作用**: 提供标准的JSON执行计划格式参考
**用途**: 用户创建新任务时的基础模板
**内容**: 包含所有必填和可选字段的示例

### task-*.json - 用户任务
**命名格式**: `task-[序号]-[描述].json`
**作用**: 具体的文生图任务配置
**示例**: `task-001-hotpot-poster.json`

### test-*.json - 测试任务
**命名格式**: `test-[描述].json`
**作用**: 用于功能测试和效果验证
**示例**: `test-poster-sichuan-hotpot.json`

## 📝 JSON执行计划标准格式

```json
{
  "agent_id": "E1",
  "task_description": "任务的自然语言描述",
  "input_data": {
    "text_prompt": "详细的文字描述",
    "style": "设计风格标签",
    "negative_prompt": "负面提示词(可选)"
  },
  "output_settings": {
    "save_path": "output/images/1-poster/",
    "format": "png",
    "quality": 95
  },
  "metadata": {
    "created_at": "2025-10-11T10:30:00",
    "created_by": "创建者名称",
    "version": "1.0"
  }
}
```

## 🔧 input_data字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| text_prompt | string | ✅ | 文字描述，越详细效果越好 |
| style | string | ❌ | 风格标签(如"商业摄影"、"手绘风格") |
| negative_prompt | string | ❌ | 不希望出现的元素(如"模糊"、"低质量") |
| design_type | string | ❌ | 设计类型(如"poster"、"menu") |
| design_requirements | array | ❌ | 设计要求列表 |

## 🚀 使用流程

### 创建新任务

**步骤1**: 复制模板文件
```bash
cp api/plans/e1-text-to-image/template.json \
   api/plans/e1-text-to-image/task-002-my-poster.json
```

**步骤2**: 编辑任务配置
- 修改`task_description`描述任务目标
- 填写`text_prompt`提供详细的设计描述
- 设置`output_settings`指定输出路径
- 更新`metadata`记录创建信息

**步骤3**: 执行任务
```bash
python api/projects/nano-banana-api/execute_plan.py \
  --plan api/plans/e1-text-to-image/task-002-my-poster.json
```

**步骤4**: 查看结果
- 生成的图片保存在`output/images/1-poster/`
- 文件名格式: `text_to_image_YYYYMMDDHHmmss_1.png`

### 批量执行

```bash
# 执行目录下所有任务
for plan in api/plans/e1-text-to-image/task-*.json; do
  python api/projects/nano-banana-api/execute_plan.py --plan "$plan"
  sleep 5  # 避免API限流
done
```

## 💡 text_prompt编写技巧

### 基本结构
```
[主题] + [风格] + [元素描述] + [质量要求]
```

### 优质示例
```
中国成都火锅店盛大开业海报设计。商业摄影风格，
展示沸腾的红油火锅，新鲜食材整齐摆放，
暖色调灯光营造温馨氛围，4K高清品质，
专业级餐饮摄影，适合印刷使用。
```

### 关键要素
- **主题明确**: 说明是什么类型的设计
- **风格定义**: 商业摄影、手绘、水彩等
- **元素细节**: 具体包含哪些视觉元素
- **氛围描述**: 色调、灯光、情绪感受
- **质量标准**: 4K、高清、印刷级等

## 🔍 任务示例分析

### 示例1: 火锅店开业海报

**文件**: `task-001-hotpot-poster.json`

**text_prompt**:
```
中国成都火锅店盛大开业，红色喜庆背景，
展示麻辣火锅底料和新鲜食材，包括毛肚、
鸭肠、牛肉等特色菜品，暖色调灯光，
商业摄影风格，4K高清。
```

**设计要点**:
- 主题: 火锅店开业
- 风格: 商业摄影 + 喜庆
- 元素: 火锅、食材
- 质量: 4K高清

### 示例2: 川菜餐厅测试海报

**文件**: `test-poster-sichuan-hotpot.json`

**text_prompt**:
```
川菜餐厅的专业美食摄影海报，展示经典川菜火锅...
```

**特点**:
- 用于测试E1智能体功能
- 包含完整的metadata信息
- 验证输出质量和格式

## ⚠️ 常见问题

### Q1: text_prompt过于简单导致效果不佳
**解决**: 增加细节描述，包含风格、元素、氛围等信息

### Q2: 生成的图片不符合预期
**解决**: 使用negative_prompt排除不想要的元素

### Q3: 输出路径不存在
**解决**: 执行器会自动创建目录，无需手动创建

### Q4: JSON格式错误
**解决**: 使用`python -m json.tool`验证JSON格式

## 🔗 相关文档

- [E1智能体文档](../../../.claude/agents/E1.md)
- [统一执行器文档](../../projects/nano-banana-api/README.md)
- [三层架构标准化流程](../../../.claude/CLAUDE.md#3-e系列智能体三层架构标准化流程)
- [输出目录说明](../../../output/images/README.md)

## 📊 最佳实践

**任务命名**:
- 使用描述性名称，便于识别
- 包含序号方便管理(task-001, task-002)
- 测试任务使用test-前缀

**版本管理**:
- JSON计划文件纳入Git管理
- 记录任务创建时间和创建者
- 重要任务保留多个版本

**质量控制**:
- 复用成功的text_prompt模板
- 记录优质prompt到library/prompts/
- 定期总结有效的描述技巧

---

**目录版本**: v1.0.0
**创建日期**: 2025-10-11
**智能体**: E1 - 餐饮文生图AIGC智能体
**执行器**: api/projects/nano-banana-api/execute_plan.py
