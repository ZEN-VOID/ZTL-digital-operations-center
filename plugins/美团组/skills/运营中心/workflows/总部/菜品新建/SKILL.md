---
name: dish-creator
description: SOP型技能包,用于根据指定信息按照美团管家标准模板创建或批量创建菜品。自动分析自然语言或结构化数据,智能填写菜品导入模板的32个字段,生成符合美团管家菜品导入标准的Excel文件。
version: 1.0.0
category: 运营中心/workflows
author: ZTL数智化作战中心
tags: [菜品管理, 运营中心, SOP, Excel, 批量处理]
---

# 菜品创建技能包 (Dish Creator)

## 概述

这是一个**标准操作流程(SOP)型技能包**,用于自动化创建符合美团管家标准的菜品导入文件。遵循**三层架构模式**,支持单个和批量创建,能够智能解析自然语言描述或结构化数据,自动填写32个字段,生成标准化的Excel菜品导入文件。

## 核心能力

### 1. 多源信息解析

**支持输入格式**:
- ✅ 自然语言描述 (中文/英文)
- ✅ 结构化数据 (JSON/CSV/Excel)
- ✅ 混合格式
- ✅ 批量数据文件

**智能提取能力**:
- 菜品基本信息 (名称、分类、规格)
- 价格信息 (售卖价、会员价、预估成本)
- 销售设置 (计价方式、单位、售卖状态)
- 扩展信息 (菜品角标、描述标签、辣度)
- 其他可选字段 (保质期、自定义字段、点餐标签)

### 2. 智能字段填写

#### 必填字段自动识别

**必填字段** (标记 * 的字段):
1. **菜品名称** - 从输入数据中提取
2. **所属品牌** - 从品牌库匹配或使用默认值
3. **分类** - 支持两级分类,采用"/"分隔 (如"招牌菜/川菜")
4. **售卖价** - 必须提供,数值类型
5. **计价方式** - 按份销售或称重销售

#### 非必填字段智能推断

**价格相关**:
- 会员价: 默认等于售卖价,可智能分析调整 (如"会员价9折" → 售卖价 * 0.9)
- 预估成本: 可根据历史数据或品类平均值智能推断

**销售设置**:
- 计价方式: 根据单位智能推断 (如"斤"/"两" → 称重销售, "份" → 按份销售)
- 单位: 根据品类智能推断 (如"饮料" → "杯", "主食" → "份")
- 售卖状态: 默认"在售"

**点餐设置**:
- 是否打印: 默认"是"
- 点餐端展示: 默认"是"
- 收银端临时改价: 默认"不允许"
- 收银端手动打折: 默认"允许"
- 起售份数: 默认1
- 增量售卖数: 默认1
- 仅套餐售卖: 默认"否"

**标签和描述**:
- 菜品角标: 根据分析推断 (如"新品" → "新菜", "爆款" → "招牌菜")
- 描述标签: 根据菜品特性智能添加 (如含乳制品、可做热饮等)
- 点餐标签: 根据营销策略添加 (如店长推荐、活动菜等)
- 菜品辣度: 根据菜品名称或描述推断 (如"麻辣" → "重辣", "微辣" → "微辣")

### 3. 菜品导入文件生成

**基于标准模板**:
- `plugins/美团组/templates/菜品导入模板.xlsx`

**核心处理逻辑**:
1. **字段验证**: 验证必填字段完整性
2. **格式规范化**: 确保字段格式符合美团管家要求
3. **智能填充**: 非必填字段智能推断
4. **批量扩展**: 批量创建时自动扩展行

**模板字段映射** (32个字段):

| 字段编号 | 字段名称 | 必填 | 说明 | 智能推断逻辑 |
|---------|---------|------|------|------------|
| 1 | * 菜品名称 | ✅ | 用户输入 | 直接提取 |
| 2 | * 所属品牌 | ✅ | 从品牌库匹配 | 默认使用第一个品牌 |
| 3 | * 分类 | ✅ | 两级分类,用"/"分隔 | 根据菜品名称和类型推断 |
| 4 | 规格 | ❌ | 如"大份"、"中份"、"小份" | 用户输入或留空 |
| 5 | * 售卖价 | ✅ | 必须提供数值 | 直接提取 |
| 6 | 会员价 | ❌ | 小于等于售卖价 | 默认等于售卖价 |
| 7 | 预估成本 | ❌ | 数字 | 根据品类平均值推断 |
| 8 | 条形码 | ❌ | 5-30位数字或字母 | 用户输入或留空 |
| 9 | * 计价方式 | ✅ | 按份销售或称重销售 | 根据单位推断 |
| 10 | 单位 | ❌ | 如份、斤、两 | 根据计价方式推断 |
| 11 | 数字助记码 | ❌ | 点菜宝中使用,数字 | 用户输入或留空 |
| 12 | 拼音助记码 | ❌ | 点菜宝中使用,字母 | 自动生成拼音首字母 |
| 13 | 保质期 | ❌ | 1-999整数 | 用户输入或留空 |
| 14 | 保质期单位 | ❌ | 年、天、自然日、小时、分钟 | 若有保质期则必填 |
| 15-18 | 自定义字段1-4 | ❌ | 最多200字 | 用户输入或留空 |
| 19 | 是否打印 | ❌ | 是或否 | 默认"是" |
| 20 | 售卖状态 | ❌ | 在售或停售 | 默认"在售" |
| 21 | 点餐端展示-统一设置 | ❌ | 是或否 | 默认"是" |
| 22 | 收银端临时改价 | ❌ | 允许或不允许 | 默认"不允许" |
| 23 | 收银端手动打折 | ❌ | 允许或不允许 | 默认"允许" |
| 24 | 起售份数 | ❌ | 数字 | 默认1 |
| 25 | 增量售卖数 | ❌ | 数字 | 默认1 |
| 26 | 仅套餐售卖 | ❌ | 是或否 | 默认"否" |
| 27 | 菜品角标 | ❌ | 如新菜、招牌菜 | 根据营销策略推断 |
| 28 | 描述标签 | ❌ | 多个用//分隔 | 根据菜品特性推断 |
| 29 | 点餐标签 | ❌ | 多个用//分隔 | 根据营销策略推断 |
| 30 | 菜品辣度 | ❌ | 不辣到爆辣6级 | 根据菜品名称推断 |
| 31 | 菜品描述 | ❌ | 最多50字 | 自动生成或用户输入 |
| 32 | 菜品详细描述 | ❌ | 最多200字 | 自动生成或用户输入 |

## 快速开始

### 基础用法

```python
from scripts.dish_creator import DishCreator

# 初始化创建器
creator = DishCreator()

# 方式1: 自然语言输入
result = creator.create_from_text(
    text="""
    请创建一个新菜品"麻辣小龙虾":
    - 所属品牌: 吼巷
    - 分类: 招牌菜/海鲜
    - 售卖价: 88元
    - 会员价: 78元
    - 辣度: 重辣
    - 描述: 精选优质小龙虾,秘制麻辣调料,鲜香麻辣
    """,
    project_name="新菜品上架"  # 项目名称(必填)
)

# 方式2: 结构化数据输入
data = {
    "dish_name": "麻辣小龙虾",
    "brand": "吼巷",
    "category": "招牌菜/海鲜",
    "selling_price": 88,
    "member_price": 78,
    "spicy_level": "重辣",
    "description": "精选优质小龙虾,秘制麻辣调料,鲜香麻辣"
}
result = creator.create_from_dict(
    data=data,
    project_name="新菜品上架"
)

# 方式3: 批量创建
batch_data = [
    {"dish_name": "麻辣小龙虾", "selling_price": 88, ...},
    {"dish_name": "蒜蓉小龙虾", "selling_price": 88, ...},
    {"dish_name": "十三香小龙虾", "selling_price": 88, ...}
]
results = creator.create_batch(
    batch_data=batch_data,
    project_name="夏季新品上架"
)
```

### 输出路径规范

所有生成的菜品导入文件按照**标准路径规范**输出:

```
output/[项目名]/dish-creator/
├── 菜品导入_麻辣小龙虾_20250103_143000.xlsx
├── 菜品导入_蒜蓉小龙虾_20250103_143001.xlsx
├── 批量菜品导入_20250103_143002.xlsx
├── plan_菜品创建_20250103_143000.json
├── log_execution_20250103_143000.txt
└── metadata_20250103_143000.json
```

**⚠️ 简化版路径结构**:
- 所有文件直接存放在 `output/[项目名]/dish-creator/` 目录下
- 通过文件名前缀区分类型 (如: `plan_xxx.json`, `菜品导入_xxx.xlsx`, `log_xxx.txt`)

## 核心工作流程 (三层架构)

### Layer 1: 规范层 (本文档)

**定义内容**:
- ✅ 业务目标: 自动化创建符合美团管家标准的菜品导入文件
- ✅ 领域知识: 美团管家菜品导入模板的32个字段规范
- ✅ 工作流程: 5个步骤的标准化流程
- ✅ 质量标准: 字段必填验证、格式规范化、智能推断准确率

### Layer 2: 计划层 (JSON配置)

**执行计划示例**:

```json
{
  "plan_id": "plan_菜品创建_20250103_143000",
  "project_name": "新菜品上架",
  "skill_name": "dish-creator",
  "task_type": "single",
  "execution_config": {
    "auto_fill_optional": true,
    "validate_before_save": true,
    "use_intelligent_inference": true
  },
  "tasks": [
    {
      "task_id": "T001",
      "dish_name": "麻辣小龙虾",
      "brand": "吼巷",
      "category": "招牌菜/海鲜",
      "spec": null,
      "selling_price": 88,
      "member_price": 78,
      "estimated_cost": null,
      "barcode": null,
      "pricing_method": "按份销售",
      "unit": "份",
      "numeric_memo": null,
      "pinyin_memo": "MLXLX",
      "shelf_life": null,
      "shelf_life_unit": null,
      "custom_field_1": null,
      "custom_field_2": null,
      "custom_field_3": null,
      "custom_field_4": null,
      "is_print": "是",
      "selling_status": "在售",
      "display_unified": "是",
      "allow_temp_price": "不允许",
      "allow_manual_discount": "允许",
      "min_order_qty": 1,
      "increment_qty": 1,
      "combo_only": "否",
      "dish_badge": "招牌菜",
      "description_tags": "海鲜//麻辣",
      "order_tags": "店长推荐",
      "spicy_level": "重辣",
      "description": "精选优质小龙虾,秘制麻辣调料,鲜香麻辣",
      "detailed_description": "精选优质小龙虾,采用秘制麻辣调料,经过多道工序精心烹制,鲜香麻辣,回味无穷"
    }
  ],
  "output_path": "output/新菜品上架/dish-creator/菜品导入_麻辣小龙虾_20250103_143000.xlsx"
}
```

**计划配置文件位置**:
- `output/[项目名]/dish-creator/plan_*.json`

### Layer 3: 执行层 (Python脚本)

**核心执行引擎**:
- `scripts/dish_creator.py` - 主创建器
- `scripts/parsers/text_parser.py` - 自然语言解析
- `scripts/validators/field_validator.py` - 字段验证器
- `scripts/generators/excel_generator.py` - Excel生成器

**执行步骤**:

1. **Step 1: 信息解析与结构化**
   - 调用 `text_parser.py` 或直接接收结构化数据
   - 提取菜品名称、分类、价格、辣度等信息
   - 识别必填字段和可选字段

2. **Step 2: 智能字段推断**
   - 必填字段: 验证完整性
   - 非必填字段: 根据业务规则智能推断
   - 计价方式: 根据单位自动推断
   - 拼音助记码: 自动生成拼音首字母
   - 菜品辣度: 根据菜品名称或描述推断

3. **Step 3: 字段验证**
   - 调用 `field_validator.py`
   - 验证必填字段完整性
   - 验证字段格式 (如会员价 ≤ 售卖价)
   - 验证字段长度限制 (如菜品描述 ≤ 50字)
   - 验证枚举值 (如计价方式只能是"按份销售"或"称重销售")

4. **Step 4: 数据组织**
   - 按照模板结构组织数据
   - 处理多标签字段 (用//分隔)
   - 处理两级分类 (用/分隔)
   - 填充默认值

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
    ├─ 提取菜品名称、分类、价格
    ├─ 提取销售设置、标签信息
    └─ 识别必填和可选字段
    ↓
[Step 2] 智能字段推断
    ├─ 必填字段: 验证完整性
    ├─ 非必填字段: 智能推断
    ├─ 计价方式: 根据单位推断
    ├─ 拼音助记码: 自动生成
    └─ 菜品辣度: 根据名称/描述推断
    ↓
[Step 3] 字段验证
    ├─ 必填字段完整性验证
    ├─ 字段格式验证 (会员价 ≤ 售卖价)
    ├─ 字段长度验证 (描述 ≤ 50字)
    └─ 枚举值验证 (计价方式、辣度等)
    ↓
[Step 4] 数据组织
    ├─ 按模板结构组织数据
    ├─ 处理多标签字段 (//分隔)
    ├─ 处理两级分类 (/分隔)
    └─ 填充默认值
    ↓
[Step 5] Excel文件生成
    ├─ 复制模板文件
    ├─ 填充数据到对应单元格
    ├─ 应用单元格格式
    └─ 保存到 output/[项目名]/dish-creator/
    ↓
输出菜品导入文件 + 执行日志 + 元数据
```

## 使用场景

### 场景1: 新品上架

**需求**: 新上架"麻辣小龙虾",需要快速创建菜品档案

**输入**:
```python
creator.create_from_text(
    text="""
    创建新菜品"麻辣小龙虾":
    - 品牌: 吼巷
    - 分类: 招牌菜/海鲜
    - 售价: 88元
    - 会员价: 78元
    - 辣度: 重辣
    - 角标: 新菜
    """,
    project_name="夏季新品上架"
)
```

**输出**:
- `output/夏季新品上架/dish-creator/菜品导入_麻辣小龙虾_YYYYMMDD_HHMMSS.xlsx`

### 场景2: 批量导入菜品

**需求**: 一次性导入50个新菜品

**输入**:
```python
# 从Excel批量读取
import pandas as pd
df = pd.read_excel("新菜品清单.xlsx")

batch_data = []
for _, row in df.iterrows():
    batch_data.append({
        "dish_name": row["菜品名称"],
        "brand": row["品牌"],
        "category": row["分类"],
        "selling_price": row["售卖价"],
        "member_price": row["会员价"],
        "spicy_level": row["辣度"]
    })

creator.create_batch(
    batch_data=batch_data,
    project_name="2025Q1新品批量导入"
)
```

**输出**:
- `output/2025Q1新品批量导入/dish-creator/批量菜品导入_YYYYMMDD_HHMMSS.xlsx`

### 场景3: 菜品信息更新

**需求**: 更新"麻辣小龙虾"的价格和描述

**输入**:
```python
creator.create_from_dict(
    data={
        "dish_name": "麻辣小龙虾",
        "brand": "吼巷",
        "selling_price": 98,  # 原88元 → 98元
        "member_price": 88,   # 原78元 → 88元
        "description": "升级版秘制麻辣调料,更加鲜香"
    },
    project_name="价格调整2025Q1"
)
```

**输出**:
- `output/价格调整2025Q1/dish-creator/菜品导入_麻辣小龙虾_YYYYMMDD_HHMMSS.xlsx`

## 高级特性

### 1. 智能辣度推断

**问题**: 用户输入菜品名称时,如何自动推断辣度

**解决方案**:
- 分析菜品名称中的关键词
- "麻辣"/"重辣" → 重辣
- "微辣" → 微辣
- "酸辣" → 中辣
- 无辣度关键词 → 不辣

```python
# 示例代码
from scripts.validators.field_validator import FieldValidator

validator = FieldValidator()
spicy_level = validator.infer_spicy_level("麻辣小龙虾")
# spicy_level = "重辣"
```

### 2. 拼音助记码自动生成

**问题**: 点菜宝需要拼音助记码,如何自动生成

**解决方案**:
- 使用 `pypinyin` 库自动生成拼音首字母
- "麻辣小龙虾" → "MLXLX"

```python
from scripts.parsers.text_parser import TextParser

parser = TextParser()
pinyin_memo = parser.generate_pinyin_memo("麻辣小龙虾")
# pinyin_memo = "MLXLX"
```

### 3. 批量处理进度追踪

**问题**: 批量处理50个菜品时,需要实时查看进度

**解决方案**:
- 使用 `TodoWrite` 工具实时更新任务列表
- 日志文件记录每个任务的执行状态

```python
# 批量处理会自动生成进度日志
results = creator.create_batch(batch_data, project_name="批量导入")
# 查看日志: output/批量导入/dish-creator/log_*.txt
```

### 4. 字段验证和错误处理

**问题**: 如何确保生成的文件符合美团管家导入规范

**解决方案**:
- 必填字段缺失: 抛出错误,提示补充
- 字段格式错误: 自动修正或提示用户
- 枚举值错误: 自动修正为最接近的合法值

```python
# 执行时遇到验证错误
result = creator.create_from_text("创建新菜品xxx")
if result["status"] == "validation_error":
    print("字段验证错误:")
    for error in result["errors"]:
        print(f"- {error['field']}: {error['message']}")
```

### 5. 集成奥术光辉/excel技能包

**技术实现**:
- 调用 `.claude/skills/奥术光辉/excel/scripts/excel_processor.py`
- 利用其高级Excel处理能力 (样式、数据验证)

```python
from scripts.excel_generator import ExcelGenerator

generator = ExcelGenerator(use_excel_skill=True)
# 自动调用奥术光辉/excel的高级特性
```

## 质量保障

### 必填字段验证

**验证规则**:
```python
REQUIRED_FIELDS = [
    "菜品名称",
    "所属品牌",
    "分类",
    "售卖价",
    "计价方式"
]
```

### 字段格式验证

**格式规则**:
- 会员价 ≤ 售卖价
- 保质期: 1-999整数
- 条形码: 5-30位数字或字母
- 计价方式: "按份销售" 或 "称重销售"
- 辣度: "不辣"、"微微辣"、"微辣"、"中辣"、"重辣"、"爆辣"

### 智能推断准确率

**目标准确率**:
- 计价方式推断: ≥ 95%
- 拼音助记码生成: 100%
- 辣度推断: ≥ 85%
- 单位推断: ≥ 90%

## 依赖资源

### 数据源文件

1. **菜品导入模板**:
   - `plugins/美团组/templates/菜品导入模板.xlsx`

2. **品牌库** (可选):
   - 用于验证品牌名称的合法性

### 技能包依赖

- **奥术光辉/excel**: 高级Excel处理能力
  - 位置: `.claude/skills/奥术光辉/excel/`
  - 功能: 数据验证、样式设置

### Python库依赖

```
pandas >= 2.0.0
openpyxl >= 3.1.0
pypinyin >= 0.49.0  # 拼音转换
```

## 注意事项

### 1. 品牌名称验证

**问题**: 所属品牌必须是系统中已存在的品牌

**建议**:
- 维护品牌白名单
- 提供品牌选择建议

### 2. 分类层级限制

**问题**: 美团管家支持两级分类,用"/"分隔

**建议**:
- 一级分类: 大类 (如"招牌菜"、"凉菜")
- 二级分类: 细分 (如"川菜"、"海鲜")
- 示例: "招牌菜/海鲜"

### 3. 标签字段格式

**问题**: 描述标签和点餐标签支持多个,用"//"分隔

**建议**:
- 描述标签: "含乳制品//可做热饮"
- 点餐标签: "团购//活动菜//店长推荐"

### 4. 批量处理性能

**问题**: 批量处理100+菜品时性能较慢

**建议**:
- 使用分批处理 (每批50个)
- 启用缓存机制

## 相关文档

- [三层架构规范](~/.claude/CLAUDE.md#5-复杂系统三层架构规范)
- [输出路径规范](~/.claude/CLAUDE.md#45-输出路径规范)
- [奥术光辉/excel技能包](.claude/skills/奥术光辉/excel/SKILL.md)
- [菜品导入模板](plugins/美团组/templates/菜品导入模板.xlsx)
- [成本卡创建技能包](plugins/美团组/skills/供应链/workflows/成本卡新建/SKILL.md)

## 版本历史

- **v1.0.0** (2025-01-03): 初始版本
  - 支持单个和批量菜品创建
  - 智能字段推断和验证
  - 标准化Excel输出
  - 集成三层架构模式
