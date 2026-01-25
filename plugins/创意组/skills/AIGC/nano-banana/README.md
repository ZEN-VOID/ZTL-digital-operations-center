# Nano-Banana AIGC 技能包

> 专业的 AIGC 图像生成和编辑能力,基于 Google Gemini 2.5 Flash Image (OpenRouter)
> 为餐饮行业设计场景深度优化

## 📦 快速概览

**技能包名称**: `nano-banana`
**版本**: v1.0.0
**所属组**: 创意组
**位置**: `plugins/创意组/skills/AIGC/nano-banana/`

### 核心能力

- ✅ **文生图** (Text-to-Image) - 从文本描述生成高质量图像
- ✅ **图生图** (Image-to-Image) - 基于输入图像生成新图像
- ✅ **图像编辑** (Editing) - 添加、删除或修改图像元素
- ✅ **风格迁移** (Style Transfer) - 将照片转换为特定艺术风格
- ✅ **多图合成** (Multi-Composition) - 合成多张图像创建复合场景
- ✅ **角色一致性** (Character Consistency) - 保持同一角色在不同场景的一致性
- ✅ **背景替换** (Background Replacement) - 替换图像背景
- ✅ **局部优化** (Local Enhancement) - 精确优化图像特定区域

### 特色功能

- 🎯 **智能提示词优化**: 自动将用户输入优化为专业级提示词
- 🍲 **餐饮行业专用模板**: 内置海报、菜单、社交媒体三大场景模板
- 📐 **标准化输出路径**: 遵循项目三层架构规范
- 🔄 **批量处理支持**: 基于 JSON 计划的批量生成能力
- 💰 **成本透明**: 清晰的定价和 token 消耗跟踪

## 🚀 快速开始

### 1. 环境配置

```bash
# 设置 OpenRouter API Key
export OPENROUTER_API_KEY="sk-or-v1-YOUR_API_KEY"

# 或创建 .env 文件
echo "OPENROUTER_API_KEY=sk-or-v1-YOUR_API_KEY" > .env

# 安装依赖
pip install requests
```

### 2. 基础使用

```python
from pathlib import Path
from scripts.core_engine import NanoBananaExecutor

# 初始化执行器
executor = NanoBananaExecutor()

# 生成图像
result = executor.execute(
    user_prompt="火锅店开业庆典海报,红色主色调,喜庆氛围",
    task_type="text-to-image",
    context="餐饮行业海报设计",
    target_style="摄影级",
    project_name="火锅店开业筹备"
)

print(f"✅ 图像已生成: {result['image_path']}")
```

### 3. 运行测试

```bash
cd plugins/创意组/skills/AIGC/nano-banana/scripts
python3 test_skill.py
```

## 📁 目录结构

```
nano-banana/
├── SKILL.md              # 元数据和快速开始指南 (~500-2000 tokens)
├── reference.md          # 深度技术文档 (~5000 tokens)
├── README.md            # 本文件 (项目说明)
│
├── scripts/             # 执行引擎
│   ├── core_engine.py   # 核心执行引擎 (Layer 3)
│   ├── test_skill.py    # 测试脚本
│   └── batch_processor.py  # 批处理器 (可选,参考 reference.md)
│
└── templates/           # 提示词模板库 (预留)
```

## 🎨 使用场景

### 场景 1: 海报设计

```python
result = executor.execute(
    user_prompt="火锅店盛大开业,红色喜庆,金色点缀",
    task_type="text-to-image",
    context="餐饮行业海报设计",
    target_style="摄影级",
    requirements=["300 DPI", "2:3竖版"],
    config=ImageConfig(aspect_ratio="2:3", temperature=0.9)
)
```

### 场景 2: 菜品摄影

```python
result = executor.execute(
    user_prompt="新鲜毛肚特写,工作室光照,诱人食欲",
    task_type="text-to-image",
    context="餐饮行业菜单摄影",
    target_style="摄影级",
    config=ImageConfig(aspect_ratio="4:3", temperature=0.7)
)
```

### 场景 3: 社交媒体内容

```python
result = executor.execute(
    user_prompt="朋友圈推广图,突出优惠信息,吸睛配色",
    task_type="text-to-image",
    context="餐饮行业社交媒体",
    config=ImageConfig(aspect_ratio="1:1", temperature=0.8)
)
```

## 💡 提示词优化示例

**用户输入**:
```
"火锅店开业海报,红色"
```

**自动优化后**:
```
"Professional restaurant promotional poster design,
火锅店开业海报, 红色主色调, ultra-realistic,
photographic quality, 8K resolution, golden hour light,
85mm portrait lens, close-up, high-quality print resolution,
attention-grabbing composition, clear hierarchy"
```

**优化策略**:
1. ✅ 添加业务场景前缀 (Professional restaurant promotional poster design)
2. ✅ 增强描述具体性 (红色 → 红色主色调)
3. ✅ 注入风格术语 (ultra-realistic, photographic quality, 8K resolution)
4. ✅ 添加摄影术语 (golden hour light, 85mm portrait lens, close-up)
5. ✅ 强调质量标准 (high-quality print resolution)

## 📊 成本说明

| 任务类型 | 平均耗时 | Token 消耗 | 成本 (USD) |
|---------|---------|-----------|-----------|
| 简单文生图 | 8-12秒 | 150 input + 1290 output | $0.039 |
| 复杂文生图 | 12-18秒 | 300 input + 1290 output | $0.040 |
| 图生图 | 15-25秒 | 500 input + 1290 output | $0.041 |
| 多图合成 | 20-35秒 | 1000 input + 1290 output | $0.045 |

**定价**:
- 输入: $0.30/M tokens
- 输出: $2.50/M tokens (每张图像固定 1290 tokens)
- 输入图像: $1.238/K images

## 🔧 高级功能

### 批量处理

创建 JSON 执行计划:

```json
{
  "project_name": "火锅店开业物料",
  "tasks": [
    {
      "task_id": "task_001",
      "user_prompt": "火锅店开业海报",
      "task_type": "text-to-image",
      "context": "餐饮行业海报设计",
      "config": {"aspect_ratio": "2:3"}
    }
  ]
}
```

执行批处理 (需自行实现,参考 reference.md):
```bash
python scripts/batch_processor.py plans/batch.json
```

### 自定义优化器

```python
from scripts.core_engine import PromptOptimizer

class CustomOptimizer(PromptOptimizer):
    def _optimize_text_to_image(self, user_prompt, config):
        # 自定义优化逻辑
        return super()._optimize_text_to_image(user_prompt, config)

# 使用自定义优化器
executor = NanoBananaExecutor()
executor.optimizer = CustomOptimizer()
```

## 📚 文档索引

- **SKILL.md**: 快速开始指南和 API 参考
- **reference.md**: 深度技术文档 (架构、优化策略、批处理、高级场景)
- **README.md**: 本文件 (项目说明和快速入门)

## 🐛 故障排除

### 问题 1: API Key 无效

**错误**: `ValueError: 未找到 OPENROUTER_API_KEY`

**解决**:
```bash
# 检查环境变量
echo $OPENROUTER_API_KEY

# 重新设置
export OPENROUTER_API_KEY="sk-or-v1-YOUR_API_KEY"
```

### 问题 2: 图像提取失败

**错误**: "未能从响应中提取图像"

**解决**:
1. 检查 API 响应格式
2. 查看完整错误日志
3. 参考 reference.md 的"错误处理和调试"章节

## 🔄 更新日志

### v1.0.0 (2025-01-28)
- 🎉 初始版本发布
- ✅ 支持 8 种核心 AIGC 能力
- ✅ 内置餐饮行业提示词优化器
- ✅ 标准化输出路径
- ✅ 完整的元数据追踪

## 🤝 贡献指南

本技能包遵循 ZTL 数智化作战中心的三层架构规范:

- **Layer 1 (规范层)**: SKILL.md + reference.md
- **Layer 2 (计划层)**: JSON 执行计划 (可选)
- **Layer 3 (执行层)**: scripts/core_engine.py

如需扩展功能:
1. 在 `PromptOptimizer` 中添加新的优化策略
2. 在 `NanoBananaClient` 中集成新的 API 能力
3. 更新 SKILL.md 和 reference.md 文档

## 📞 联系方式

- **问题反馈**: 提交 GitHub Issue
- **功能建议**: 创建 PR
- **技术支持**: 联系 ZTL 数智化作战中心 - 创意组

---

**License**: MIT
**Maintained by**: ZTL 数智化作战中心 - 创意组
**Last Updated**: 2025-01-28
