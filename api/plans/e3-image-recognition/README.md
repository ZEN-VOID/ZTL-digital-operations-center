# E3智能体 - 餐饮图片识别 使用指南

> 遵循"规范·计划·执行"三层架构的标准化图片识别工作流

---

## 📋 快速开始

### 1️⃣ 创建执行计划（基于template.json）

```bash
# 复制模板创建新任务
cp api/plans/e3-image-recognition/template.json \
   api/plans/e3-image-recognition/my-dish-analysis.json

# 编辑JSON文件，填写：
# - task_description: 任务描述
# - image_url: 图片路径
# - analysis_type: 分析类型（content/quality/scene/comprehensive）
# - analysis_dimensions: 分析维度列表
```

### 2️⃣ 执行分析（使用统一执行器）

```bash
# 单图片分析
python api/projects/nano-banana-api/execute_plan.py \
  --plan api/plans/e3-image-recognition/my-dish-analysis.json

# 批量分析（多张图片）
bash api/plans/e3-image-recognition/batch-analyze-4-images.sh
```

### 3️⃣ 查看结果

```bash
# 结果保存在output_settings.save_path指定的目录
ls -lh output/analysis/e3-image-recognition/
```

---

## 🏗️ 三层架构说明

### 第1层 - 规范层（智能体文档）
- **文档位置**: `.claude/agents/E3.md`
- **作用**: 定义E3智能体的业务目标、工作流程、质量标准
- **核心能力**: 理解用户需求、分析识别场景、生成执行计划

### 第2层 - 计划层（JSON配置）
- **目录位置**: `api/plans/e3-image-recognition/`
- **标准模板**: `template.json`（必须遵循的标准格式）
- **实际任务**: `*.json`（基于模板创建的具体任务）

### 第3层 - 执行层（统一执行器）
- **执行器位置**: `api/projects/nano-banana-api/execute_plan.py`
- **特点**: 固定脚本，支持E1-E9所有智能体，通过JSON驱动任务执行
- **底层API**: `banana-all-in-one.py` (NanoBananaAPI核心实现)

---

## 📐 JSON执行计划标准格式

```json
{
  "agent_id": "E3",
  "task_description": "图片识别任务描述",
  "input_data": {
    "image_url": "图片路径（单张图片）",
    "analysis_type": "分析类型：content|quality|scene|comprehensive",
    "analysis_dimensions": [
      "分析维度1：例如：食材识别",
      "分析维度2：例如：色彩分析"
    ]
  },
  "output_settings": {
    "save_path": "output/analysis/e3-image-recognition/",
    "format": "json"
  },
  "metadata": {
    "created_at": "YYYY-MM-DDTHH:MM:SS",
    "created_by": "智能体名称或用户名",
    "version": "1.0"
  }
}
```

### ⚠️ 重要说明

1. **单图片处理**: E3智能体处理**单张图片**（`image_url`字段），而不是多图数组
2. **多图片场景**:
   - 需要分析多张图片时，有两种方案：
     - 方案A：创建多个JSON任务文件，分别执行
     - 方案B：使用批处理脚本（参考`batch-analyze-4-images.sh`）
3. **多图融合**: 如果需要**融合多张图片**生成新图，应使用**E6智能体**（餐饮多图融合AIGC智能体）

---

## 🔧 analysis_type 分析类型说明

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| `content` | 内容分析 | 全面了解图片内容（菜品、环境、元素） |
| `quality` | 质量评估 | 评估图片商业价值和技术质量 |
| `scene` | 场景识别 | 判断餐厅类型和用餐环境 |
| `comprehensive` | 综合分析 | 完整的六大分类、24子分类深度分析（推荐） |

---

## 📊 输出结果格式

- **格式**: JSON结构化数据
- **路径**: 由`output_settings.save_path`指定
- **命名**: `analysis_[description]_[timestamp].json`
- **内容**: 包含完整的分析维度和商业洞察

---

## 🚫 常见错误与解决方案

### 错误1: `KeyError: 'image_url'`
**原因**: JSON中使用了`"images"`数组而不是`"image_url"`单个字符串
**解决**: 修改JSON，使用标准格式的`"image_url"`字段

### 错误2: `图片文件不存在`
**原因**: `image_url`路径不正确
**解决**: 确保路径相对于项目根目录，或使用绝对路径

### 错误3: `无效的图片URL`
**原因**: 图片格式不支持或文件损坏
**解决**: 确保图片为常见格式（PNG/JPG/JPEG），且文件完整

---

## 📚 示例任务

### 示例1: 菜品内容分析
```json
{
  "agent_id": "E3",
  "task_description": "分析火锅菜品的食材和摆盘",
  "input_data": {
    "image_url": "input/dishes/hotpot-01.jpg",
    "analysis_type": "content",
    "analysis_dimensions": ["食材识别", "摆盘风格", "色彩搭配"]
  },
  "output_settings": {
    "save_path": "output/analysis/e3-image-recognition/dishes/",
    "format": "json"
  },
  "metadata": {
    "created_at": "2025-10-11T18:00:00",
    "created_by": "E3示例",
    "version": "1.0"
  }
}
```

### 示例2: 品牌IP形象分析
```json
{
  "agent_id": "E3",
  "task_description": "吼巷品牌IP形象专业分析",
  "input_data": {
    "image_url": "input/吼巷/设计/IP/微信图片_20250923171141_52_171.png",
    "analysis_type": "comprehensive",
    "analysis_dimensions": [
      "视觉特征识别",
      "整体设计分析",
      "商业价值洞察"
    ]
  },
  "output_settings": {
    "save_path": "output/analysis/e3-image-recognition/houthang-ip/",
    "format": "json"
  },
  "metadata": {
    "created_at": "2025-10-11T18:00:00",
    "created_by": "E3品牌分析",
    "version": "1.0"
  }
}
```

---

## 🔗 相关资源

- **E3智能体文档**: `.claude/agents/E3.md`
- **统一执行器**: `api/projects/nano-banana-api/execute_plan.py`
- **NanoBananaAPI**: `api/projects/nano-banana-api/banana-all-in-one.py`
- **三层架构说明**: `.claude/CLAUDE.md` (第3节)

---

**版本**: v1.0.0
**最后更新**: 2025-10-11
**维护标准**: 遵循E系列智能体三层架构标准化流程
