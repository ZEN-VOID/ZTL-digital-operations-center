# AIGC Skills Collection

> 餐饮AIGC图像处理技能集合，整合NanoBanana API的完整能力，为Claude提供专业的图像生成、处理、识别和高级操作功能。

## 📚 Skills概览

本目录包含4个核心Skills，对应4个主要智能体：

### 1. Text-to-Image (文生图)
**目录**: `text-to-image/`
**对应智能体**: V3-AIGC文生图设计师
**核心能力**: 从文字描述生成专业餐饮设计图像

**支持的设计类型**:
- 海报设计 (1-poster)
- 菜单设计 (2-menu)
- 门头设计 (3-storefront)
- 菜单面板 (4-panel)
- 画册宣传册 (5-magazine)
- 图标设计 (6-icon)
- 字体设计 (7-typography)
- 主图摄影 (8-main-image)
- 详情页设计 (9-detail)

**快速开始**:
```python
from banana_api_core import NanoBananaAPI
api = NanoBananaAPI()
result = api.generate_text_to_image(
    prompt="Modern hotpot restaurant poster",
    design_type="1-poster"
)
```

---

### 2. Image-to-Image (图生图)
**目录**: `image-to-image/`
**对应智能体**: V4-AIGC图生图设计师
**核心能力**: 基于现有图片进行优化、修改和风格转换

**支持的处理类型**:
- Local Modification (局部修改)
- Local Optimization (局部优化)
- Multi-Image Processing (多图处理)
- Style Transfer (风格迁移)
- Scene Analysis (场景分析)

**快速开始**:
```python
result = api.generate_image_to_image(
    prompt="Enhance food colors and lighting",
    image_urls=["path/to/photo.jpg"],
    processing_type="local_optimization"
)
```

---

### 3. Image Recognition (图片识别)
**目录**: `image-recognition/`
**对应智能体**: V5-AIGC图片识别分析师
**核心能力**: 智能分析餐饮图片，提供多维度洞察

**支持的分析类型**:
- Comprehensive Analysis (综合分析) - 6大类、24子类、120+维度
- Quality Assessment (质量评估)
- Content Analysis (内容分析)
- Scene Recognition (场景识别)
- Brand Detection (品牌检测)

**快速开始**:
```python
result = api.generate_image_recognition(
    image_url="path/to/photo.jpg",
    analysis_type="comprehensive_analysis"
)
```

---

### 4. Advanced Processing (高级图片处理)
**目录**: `advanced-processing/`
**对应智能体**: V6-AIGC高级图片处理师
**核心能力**: 整合6大高级处理能力的完整解决方案

**6大核心能力**:
- **E4 Smart Repair**: 智能修复与扩展（水印移除、物体移除、画面扩展）
- **E5 Structure Control**: 结构控制生成（姿态、深度、边缘、布局控制）
- **E6 Multi-Image Fusion**: 多图创意融合（元素提取、智能融合、风格统一）
- **E7 Character Consistency**: 角色一致性生成（品牌IP、吉祥物、多场景适配）
- **E8 Design Iteration**: 设计稿迭代精炼（反馈响应、渐进改进、版本管理）
- **E9 Super-Resolution**: 超分细节增强（分辨率提升、质感优化、印刷级输出）

**快速开始**:
```python
# E4: 移除水印
result = api.generate_smart_repair(
    image_url="photo.jpg",
    repair_prompt="Remove watermark",
    repair_type="watermark_removal"
)

# E9: 超分增强
result = api.generate_super_resolution(
    source_image="photo.jpg",
    target_resolution="4K"
)
```

---

## 🎯 Skills架构设计

### 渐进式披露模式

所有Skills采用统一的三层结构，实现渐进式信息披露：

```
skill-name/
├── SKILL.md              # Level 1: 快速开始 (~500 tokens)
│   ├── Quick Start       # 核心使用示例
│   ├── Common Tasks      # 常见任务
│   ├── Requirements      # 依赖说明
│   └── Related Skills    # 相关Skills引用
│
├── reference.md          # Level 2: API参考 (~2000 tokens)
│   ├── API Methods       # 完整方法文档
│   ├── Parameters        # 参数详解
│   ├── Return Values     # 返回值说明
│   ├── Error Handling    # 错误处理
│   └── Best Practices    # 最佳实践
│
└── scripts/              # Level 3: 可执行代码
    ├── banana_api_core.py → 主API脚本（指向_shared/）
    └── plan_executor.py   → 执行器脚本（指向_shared/）
```

### 触发机制

Skills通过description中的关键词自动触发：

**Text-to-Image关键词**:
- `text-to-image`, `generate`, `design`, `create`
- `poster`, `menu`, `logo`, `restaurant design`

**Image-to-Image关键词**:
- `image-to-image`, `edit`, `modify`, `enhance`
- `optimize`, `improve`, `style transfer`

**Image Recognition关键词**:
- `image recognition`, `analyze`, `identify`, `detect`
- `quality assessment`, `scene recognition`

**Advanced Processing关键词**:
- `remove watermark`, `upscale`, `super-resolution`
- `character consistency`, `multi-image fusion`
- `design iteration`, `repair`, `extend image`

---

## 🔗 与智能体集成

### 智能体引用方式

每个智能体文档中添加了Skills引用：

```markdown
### 工具集 (Tools) - 规范·计划·执行三层架构 + Skills集成

> **Skills集成**: 本智能体使用 `.claude/skills/aigc/[skill-name]/` Skill，
> 该Skill提供完整的API封装、参数指南和示例文档。
> Claude会在需要时自动发现并加载此Skill。
```

### 工作流程

```
用户请求
    ↓
智能体分析需求
    ↓
Claude自动发现相关Skill（基于description关键词）
    ↓
加载SKILL.md（快速开始）
    ↓
如需详细信息，加载reference.md
    ↓
调用scripts/中的API
    ↓
返回结果
```

---

## 📝 统一执行方式

所有Skills共享统一的执行入口：

### 方式1: 直接API调用

```python
import sys
sys.path.append('./.claude/skills/aigc/_shared')
from banana_api_core import NanoBananaAPI

api = NanoBananaAPI()

# 文生图
result = api.generate_text_to_image(prompt="...", design_type="1-poster")

# 图生图
result = api.generate_image_to_image(prompt="...", image_urls=["..."])

# 图片识别
result = api.generate_image_recognition(image_url="...")

# 高级处理
result = api.generate_smart_repair(image_url="...", repair_prompt="...")
```

### 方式2: JSON执行计划

```bash
# 创建执行计划 (JSON格式)
# 然后执行
python .claude/skills/aigc/_shared/plan_executor.py \
  --plan api/plans/e1-text-to-image/task.json
```

---

## 🛠️ 技术栈

- **API网关**: OpenRouter (https://openrouter.ai)
- **模型**: google/gemini-2.5-flash-image-preview
- **主API**: `.claude/skills/aigc/_shared/banana_api_core.py`
- **执行器**: `.claude/skills/aigc/_shared/plan_executor.py`
- **语言**: Python 3.10+
- **依赖**: requests, pydantic, python-dotenv, pillow

---

## 📊 质量标准

所有Skills遵循统一的质量标准：

### 技术质量
- **分辨率**: 300 DPI起（印刷级）
- **格式**: PNG/JPG/WebP
- **色彩**: 专业色彩管理
- **清晰度**: 高分辨率输出

### 餐饮专业标准
- **美学**: 符合餐饮行业美学规范
- **品牌**: 保持品牌一致性
- **商业**: 满足商业应用需求
- **创意**: 融合专业设计理论

### 处理标准
- **精准性**: 准确完成任务目标
- **自然性**: 处理结果自然融合
- **一致性**: 整体风格协调统一
- **可靠性**: 稳定可复现的结果

---

## 🚀 快速入门示例

### 完整工作流示例

```python
from banana_api_core import NanoBananaAPI

api = NanoBananaAPI()

# 1. 生成初始设计
design = api.generate_text_to_image(
    prompt="Modern Chinese restaurant poster",
    design_type="1-poster"
)

# 2. 分析生成质量
analysis = api.generate_image_recognition(
    image_url=design["image_paths"][0],
    analysis_type="quality_assessment"
)

# 3. 根据分析优化
if analysis["scores"]["overall_quality"] < 8.0:
    improved = api.generate_image_to_image(
        prompt="Enhance colors and composition",
        image_urls=[design["image_paths"][0]],
        processing_type="local_optimization"
    )

# 4. 超分到印刷级
final = api.generate_super_resolution(
    source_image=improved["image_paths"][0],
    target_resolution="4K"
)

print(f"Final output: {final['image_paths'][0]}")
```

---

## 📞 支持与文档

### 核心文档
- **主API文档**: `.claude/skills/aigc/_shared/README.md`
- **执行器说明**: `.claude/skills/aigc/_shared/plan_executor.py`
- **智能体文档**: `.claude/agents/创意组/V3-V6.md`

### Skills文档
- **Text-to-Image**: `.claude/skills/aigc/text-to-image/SKILL.md`
- **Image-to-Image**: `.claude/skills/aigc/image-to-image/SKILL.md`
- **Image Recognition**: `.claude/skills/aigc/image-recognition/SKILL.md`
- **Advanced Processing**: `.claude/skills/aigc/advanced-processing/SKILL.md`

### 执行计划模板
- `api/plans/e1-text-to-image/template.json`
- `api/plans/e2-image-to-image/template.json`
- `api/plans/e3-image-recognition/template.json`
- `api/plans/e4-e9-*/template.json`

---

## 🎓 最佳实践

1. **Skills发现**: 让Claude自然发现Skills，避免手动加载
2. **渐进披露**: 先读SKILL.md，需要时再读reference.md
3. **错误处理**: 利用Skills内置的错误处理和重试机制
4. **参数优化**: 参考reference.md中的参数说明调优
5. **多能力协同**: 组合使用多个Skills完成复杂任务
6. **质量验证**: 使用Image Recognition验证处理结果
7. **版本管理**: 保留中间结果便于追溯和迭代

---

**版本**: v1.0.0
**最后更新**: 2025-10-20
**维护标准**: 遵循Anthropic Agent Skills设计规范
**兼容性**: Claude Code v1.0+, Sonnet 4.5
