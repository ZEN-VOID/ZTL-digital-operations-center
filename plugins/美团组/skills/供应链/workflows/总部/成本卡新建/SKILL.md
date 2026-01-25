---
name: cost-card-creator
description: SOP型技能包,用于根据指定信息按照模板创建或批量创建成本卡。自动分析自然语言或结构化数据,匹配菜品和物品编码,生成符合总部成本卡导入模板格式的Excel文件。
version: 1.0.0
category: 供应链/workflows
author: ZTL数智化作战中心
tags: [成本卡, 供应链, SOP, Excel, 批量处理]
---

# 成本卡创建技能包 (Cost Card Creator)

## 概述

这是一个**标准操作流程(SOP)型技能包**,用于自动化创建符合吼巷总部标准的成本卡文件。遵循**三层架构模式**,支持单个和批量创建,能够智能解析自然语言描述或结构化数据,自动匹配菜品SPU编码和物品编码,生成标准化的Excel成本卡文件。

## 核心能力

### 1. 多源信息解析

**支持输入格式**:
- ✅ 自然语言描述 (中文/英文)
- ✅ 结构化数据 (JSON/CSV/Excel)
- ✅ 混合格式
- ✅ 批量数据文件

**智能提取能力**:
- 菜品名称和规格
- 物品名称和用量
- 单位和净料率
- 其他可选字段 (目标毛利率、配方名称等)

### 2. 智能编码匹配

#### 菜品SPU编码匹配

**数据源**:
- `plugins/美团组/templates/吼巷_菜品库_总部.xlsx`
- `plugins/美团组/templates/吼巷_菜品库_总部_做法及加料.xlsx`

**匹配策略**:
1. **精确匹配**: 菜品名称完全一致 → 自动采用
2. **模糊匹配**: 使用Levenshtein距离算法
   - 相似度 ≥ 70% → 自动采用
   - 相似度 < 70% → 暂停执行,请求人工确认
3. **规格匹配**: 同时匹配菜品名称和规格 (标准、1人份等)

**输出字段**:
- 菜品SPU编码 (必填)
- 菜品名称 (必填)
- 菜品规格 (可选)
- 加工份数 (可选)

#### 物品编码匹配

**数据源**:
- `plugins/美团组/templates/物品导出清单-总部.xlsx`

**匹配策略**:
- 精确匹配: 物品名称完全一致
- 若无法匹配: 报告错误,请求人工确认

**输出字段**:
- 物品编码 (必填)
- 物品名称 (必填)
- 成本单位 (必填)

### 3. 成本卡生成

**基于标准模板**:
- `plugins/美团组/templates/总部成本卡导入模版.xlsx`

**核心处理逻辑**:
1. **一对多关系扩展**: 一个菜品多个物品时,自动扩展行
2. **必填字段验证**: 菜品SPU编码、菜品名称、物品编码、物品名称、成本单位、净料量、净料率
3. **智能字段推断**: 根据解析信息智能填充可选字段
4. **格式规范化**: 百分比字段使用文本格式 + 手动输入%符号

**模板字段映射** (22个字段):

| 字段编号 | 字段名称 | 必填 | 说明 |
|---------|---------|------|------|
| 1 | 菜品SPU编码 | ✅ | 从菜品库匹配 |
| 2 | 菜品名称 | ✅ | 从菜品库匹配 |
| 3 | 加工份数 | ❌ | 默认1 |
| 4 | 菜品规格 | ❌ | 标准、1人份等 |
| 5 | 其他成本 | ❌ | - |
| 6 | 目标毛利率 | ❌ | 文本格式+% |
| 7 | 配方名称 | ✅ | 默认"标准成本配方" |
| 8 | 物品编码 | ✅ | 从物品清单匹配 |
| 9 | 物品名称 | ✅ | 从物品清单匹配 |
| 10 | 成本单位 | ✅ | 从物品清单获取 |
| 11 | 净料量 | ✅ | 用户输入 |
| 12 | 净料率 | ✅ | 文本格式+% |
| 13 | 是否主料 | ❌ | 是/否 |
| 14-15 | 替代关系 | ❌ | - |
| 16 | 是否半成品 | ❌ | 是/否 |
| 17 | 是否辅助单位扣减料 | ❌ | 是/否 |
| 18 | 是否同时适用堂食和外卖 | ❌ | 是/否 |
| 19 | 门店是否可修改 | ❌ | 是/否 |
| 20 | 备注 | ❌ | - |
| 21 | 适用门店商户号 | ❌ | 例外配方时二选一 |
| 22 | 适用门店分组 | ❌ | 例外配方时二选一 |

## 快速开始

### 基础用法

```python
from scripts.cost_card_generator import CostCardGenerator

# 初始化生成器
generator = CostCardGenerator()

# 方式1: 自然语言输入
result = generator.create_from_text(
    text="""
    请为"麻辣牛肉"创建成本卡:
    - 使用牛肉500g
    - 使用辣椒油50ml
    - 使用花椒10g
    """,
    project_name="火锅店成本管理"  # 项目名称(必填)
)

# 方式2: 结构化数据输入
data = {
    "dish_name": "麻辣牛肉",
    "dish_spec": "标准",
    "ingredients": [
        {"item_name": "牛肉", "quantity": 500, "unit": "g", "yield_rate": "100%"},
        {"item_name": "辣椒油", "quantity": 50, "unit": "ml", "yield_rate": "100%"},
        {"item_name": "花椒", "quantity": 10, "unit": "g", "yield_rate": "100%"}
    ]
}
result = generator.create_from_dict(
    data=data,
    project_name="火锅店成本管理"
)

# 方式3: 批量创建
batch_data = [
    {"dish_name": "麻辣牛肉", "ingredients": [...]},
    {"dish_name": "酸菜鱼", "ingredients": [...]},
    {"dish_name": "水煮肉片", "ingredients": [...]}
]
results = generator.create_batch(
    batch_data=batch_data,
    project_name="火锅店成本管理"
)
```

### 输出路径规范

所有生成的成本卡文件按照**标准路径规范**输出:

```
output/[项目名]/cost-card-creator/
├── 成本卡_麻辣牛肉_20250103_143000.xlsx
├── 成本卡_酸菜鱼_20250103_143001.xlsx
├── 批量成本卡_20250103_143002.xlsx
├── plan_成本卡生成_20250103_143000.json
├── log_execution_20250103_143000.txt
└── metadata_20250103_143000.json
```

**⚠️ 简化版路径结构**:
- 不再使用 `plans/results/logs/metadata/` 子目录
- 所有文件直接存放在 `output/[项目名]/cost-card-creator/` 目录下
- 通过文件名前缀区分类型 (如: `plan_xxx.json`, `成本卡_xxx.xlsx`, `log_xxx.txt`)

## 核心工作流程 (三层架构)

### Layer 1: 规范层 (本文档)

**定义内容**:
- ✅ 业务目标: 自动化创建符合总部标准的成本卡
- ✅ 领域知识: 吼巷总部成本卡导入规范和字段说明
- ✅ 工作流程: 5个步骤的标准化流程
- ✅ 质量标准: 字段必填验证、编码匹配准确率、格式规范化

### Layer 2: 计划层 (JSON配置)

**执行计划示例**:

```json
{
  "plan_id": "plan_成本卡生成_20250103_143000",
  "project_name": "火锅店成本管理",
  "skill_name": "cost-card-creator",
  "task_type": "single",
  "execution_config": {
    "match_threshold": 0.7,
    "auto_confirm_above": 0.9,
    "require_manual_confirm": true
  },
  "tasks": [
    {
      "task_id": "T001",
      "dish_name": "麻辣牛肉",
      "dish_spec": "标准",
      "processing_servings": 1,
      "recipe_name": "标准成本配方",
      "ingredients": [
        {
          "item_name": "牛肉",
          "quantity": 500,
          "unit": "g",
          "yield_rate": "100%",
          "is_main_ingredient": "是"
        },
        {
          "item_name": "辣椒油",
          "quantity": 50,
          "unit": "ml",
          "yield_rate": "100%"
        }
      ]
    }
  ],
  "output_path": "output/火锅店成本管理/cost-card-creator/成本卡_麻辣牛肉_20250103_143000.xlsx"
}
```

**计划配置文件位置**:
- `output/[项目名]/cost-card-creator/plan_*.json`

### Layer 3: 执行层 (Python脚本)

**核心执行引擎**:
- `scripts/cost_card_generator.py` - 主生成器
- `scripts/parsers/text_parser.py` - 自然语言解析
- `scripts/matchers/dish_matcher.py` - 菜品编码匹配
- `scripts/matchers/item_matcher.py` - 物品编码匹配
- `scripts/generators/excel_generator.py` - Excel生成器

**执行步骤**:

1. **Step 1: 信息解析与结构化**
   - 调用 `text_parser.py` 或直接接收结构化数据
   - 提取菜品名称、物品名称、用量、单位等信息

2. **Step 2: 菜品SPU编码匹配**
   - 调用 `dish_matcher.py`
   - 读取菜品库,执行模糊匹配
   - 相似度 ≥ 70%: 自动采用
   - 相似度 < 70%: 暂停执行,请求人工确认

3. **Step 3: 物品编码匹配**
   - 调用 `item_matcher.py`
   - 读取物品清单,执行精确匹配
   - 若无法匹配: 报告错误,请求人工确认

4. **Step 4: 数据重构**
   - 按照模板结构组织数据
   - 处理一对多关系 (一个菜品对应多个物品)
   - 填充必填字段,推断可选字段

5. **Step 5: Excel文件生成**
   - 调用 `excel_generator.py`
   - 使用 `openpyxl` 复制模板
   - 填充数据到对应单元格
   - 保存到标准输出路径

## 执行流程图

```
用户输入 (自然语言/结构化数据)
    ↓
[Step 1] 信息解析与结构化
    ├─ 提取菜品名称、规格
    ├─ 提取物品名称、用量、单位
    └─ 提取其他可选字段
    ↓
[Step 2] 菜品SPU编码匹配
    ├─ 读取菜品库 (2个Excel文件)
    ├─ 精确匹配: 菜品名称 + 规格
    ├─ 模糊匹配: Levenshtein距离
    ├─ 相似度 ≥ 70% → 自动采用
    └─ 相似度 < 70% → 请求人工确认
    ↓
[Step 3] 物品编码匹配
    ├─ 读取物品清单
    ├─ 精确匹配: 物品名称
    └─ 无法匹配 → 报告错误,请求确认
    ↓
[Step 4] 数据重构
    ├─ 按模板结构组织数据
    ├─ 处理一对多关系 (菜品字段重复填写)
    ├─ 填充必填字段
    └─ 智能推断可选字段
    ↓
[Step 5] Excel文件生成
    ├─ 复制模板文件
    ├─ 填充数据到对应单元格
    ├─ 格式化百分比字段 (文本格式 + %)
    └─ 保存到 output/[项目名]/cost-card-creator/
    ↓
输出成本卡文件 + 执行日志 + 元数据
```

## 使用场景

### 场景1: 新菜品成本卡创建

**需求**: 新上架菜品"香辣蛙锅",需要创建成本卡

**输入**:
```python
generator.create_from_text(
    text="""
    为"香辣蛙锅"创建成本卡:
    - 牛蛙 800g (净料率85%)
    - 青椒 100g
    - 辣椒酱 80g
    - 蒜末 20g
    - 目标毛利率: 65%
    """,
    project_name="新菜品上架"
)
```

**输出**:
- `output/新菜品上架/cost-card-creator/成本卡_香辣蛙锅_YYYYMMDD_HHMMSS.xlsx`

### 场景2: 批量成本卡导入

**需求**: 一次性导入50个菜品的成本卡

**输入**:
```python
# 从Excel批量读取
import pandas as pd
df = pd.read_excel("菜品配方清单.xlsx")

batch_data = []
for _, row in df.iterrows():
    batch_data.append({
        "dish_name": row["菜品名称"],
        "dish_spec": row["规格"],
        "ingredients": [
            {
                "item_name": row["物品1"],
                "quantity": row["用量1"],
                "unit": row["单位1"]
            },
            # ... 更多物品
        ]
    })

generator.create_batch(
    batch_data=batch_data,
    project_name="2025Q1成本卡批量导入"
)
```

**输出**:
- `output/2025Q1成本卡批量导入/cost-card-creator/批量成本卡_YYYYMMDD_HHMMSS.xlsx`

### 场景3: 成本卡更新

**需求**: 更新"麻辣牛肉"的成本配方 (调整用量)

**输入**:
```python
generator.create_from_dict(
    data={
        "dish_name": "麻辣牛肉",
        "dish_spec": "标准",
        "ingredients": [
            {"item_name": "牛肉", "quantity": 600, "unit": "g"},  # 原500g → 600g
            {"item_name": "辣椒油", "quantity": 60, "unit": "ml"}  # 原50ml → 60ml
        ]
    },
    project_name="成本卡更新2025Q1"
)
```

**输出**:
- `output/成本卡更新2025Q1/cost-card-creator/成本卡_麻辣牛肉_YYYYMMDD_HHMMSS.xlsx`

## 高级特性

### 1. 智能模糊匹配

**问题**: 用户输入"麻辣牛肉" vs 菜品库中是"麻辣牛肉片"

**解决方案**:
- 使用Levenshtein距离算法计算相似度
- 相似度 ≥ 70%: 自动匹配
- 相似度 < 70%: 请求人工确认

```python
# 示例代码
from scripts.matchers.dish_matcher import DishMatcher

matcher = DishMatcher()
result = matcher.match("麻辣牛肉")
# result = {"dish_code": "SPU001", "dish_name": "麻辣牛肉片", "similarity": 0.85}
```

### 2. 批量处理进度追踪

**问题**: 批量处理50个菜品时,需要实时查看进度

**解决方案**:
- 使用 `TodoWrite` 工具实时更新任务列表
- 日志文件记录每个任务的执行状态

```python
# 批量处理会自动生成进度日志
results = generator.create_batch(batch_data, project_name="批量导入")
# 查看日志: output/批量导入/cost-card-creator/log_*.txt
```

### 3. 错误处理和人工确认

**问题**: 编码匹配失败时如何处理

**解决方案**:
- 自动暂停执行,生成待确认清单
- 用户确认后继续执行

```python
# 执行时遇到匹配度<70%的情况
result = generator.create_from_text("为xxx创建成本卡")
if result["status"] == "pending_confirm":
    print("需要人工确认:")
    for item in result["pending_items"]:
        print(f"- {item['input']} → 候选: {item['candidates']}")
```

### 4. 集成奥术光辉/excel技能包

**技术实现**:
- 调用 `.claude/skills/奥术光辉/excel/scripts/excel_processor.py`
- 利用其高级Excel处理能力 (样式、图表、数据验证)

```python
from scripts.excel_generator import ExcelGenerator

generator = ExcelGenerator(use_excel_skill=True)
# 自动调用奥术光辉/excel的高级特性
```

## 质量保障

### 必填字段验证

**验证规则**:
```python
REQUIRED_FIELDS = {
    "dish": ["菜品SPU编码", "菜品名称"],
    "ingredient": ["物品编码", "物品名称", "成本单位", "净料量", "净料率"],
    "recipe": ["配方名称"]
}
```

### 编码匹配准确率

**目标准确率**:
- 菜品编码匹配: ≥ 95% (自动匹配 + 人工确认)
- 物品编码匹配: 100% (精确匹配)

### 格式规范化

**规范化处理**:
- 百分比字段: 文本格式 + 手动输入 `%` 符号
- 数量字段: 数值类型,保留2位小数
- 单位字段: 从物品档案的业务单位中选择

## 依赖资源

### 数据源文件

1. **菜品库** (2个文件):
   - `plugins/美团组/templates/吼巷_菜品库_总部.xlsx`
   - `plugins/美团组/templates/吼巷_菜品库_总部_做法及加料.xlsx`

2. **物品清单**:
   - `plugins/美团组/templates/物品导出清单-总部.xlsx`

3. **导入模板**:
   - `plugins/美团组/templates/总部成本卡导入模版.xlsx`

### 技能包依赖

- **奥术光辉/excel**: 高级Excel处理能力
  - 位置: `.claude/skills/奥术光辉/excel/`
  - 功能: 数据验证、样式设置、图表生成

### Python库依赖

```
pandas >= 2.0.0
openpyxl >= 3.1.0
Levenshtein >= 0.21.0  # 字符串相似度计算
```

## 注意事项

### 1. 数据源同步

**问题**: 菜品库和物品清单可能更新

**建议**:
- 定期同步数据源文件
- 执行前检查数据源版本号

### 2. 编码冲突处理

**问题**: 同名菜品可能有不同规格 (标准、1人份等)

**建议**:
- 匹配时同时考虑菜品名称和规格
- 规格字段必填时,强制精确匹配

### 3. 批量处理性能

**问题**: 批量处理100+菜品时性能较慢

**建议**:
- 使用分批处理 (每批50个)
- 启用缓存机制 (避免重复读取数据源)

### 4. 人工确认流程

**问题**: 自动匹配失败时需要人工确认

**建议**:
- 生成待确认清单 (JSON格式)
- 提供候选项和相似度评分
- 确认后自动继续执行

## 相关文档

- [三层架构规范](~/.claude/CLAUDE.md#5-复杂系统三层架构规范)
- [输出路径规范](~/.claude/CLAUDE.md#45-输出路径规范)
- [奥术光辉/excel技能包](.claude/skills/奥术光辉/excel/SKILL.md)
- [成本卡导入模板说明](plugins/美团组/templates/总部成本卡导入模版.xlsx)

## 版本历史

- **v1.0.0** (2025-01-03): 初始版本
  - 支持单个和批量成本卡创建
  - 智能菜品和物品编码匹配
  - 标准化Excel输出
  - 集成三层架构模式
