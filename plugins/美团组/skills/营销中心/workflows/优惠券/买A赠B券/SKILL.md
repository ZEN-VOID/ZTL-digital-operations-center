---
name: buy-a-get-b-coupon
description: SOP型技能包,用于在美团管家后台创建"买A赠B券"营销活动。自动化配置活动规则、购买条件、赠品设置、库存管理等,生成符合美团平台规范的优惠券配置方案。
version: 1.0.0
category: 营销中心/workflows/优惠券
author: ZTL数智化作战中心
tags: [买A赠B券, 优惠券, 营销活动, SOP, 美团管家]
---

# 买A赠B券创建技能包 (Buy A Get B Coupon Creator)

## 概述

这是一个**标准操作流程(SOP)型技能包**,用于自动化创建符合美团平台规范的"买A赠B券"营销活动。遵循**三层架构模式**,支持单个和批量创建,能够智能解析活动需求,生成标准化的优惠券配置方案,并提供完整的后台操作指引。

**业务目标**:
- 🎁 促进店铺销量增长,提升客单价
- 🎯 精准引导顾客购买指定商品(商品A)
- 💰 通过赠品(商品B)提升顾客体验和复购率
- 📊 支持库存管理和活动效果追踪

**适用场景**:
- ✅ 新品推广 (买新品送畅销品)
- ✅ 库存消化 (买滞销品送热销品)
- ✅ 套餐组合 (买主食送饮料/小吃)
- ✅ 会员福利 (买指定金额送会员礼品)
- ✅ 节日营销 (买节日套餐送限定礼品)

## 核心能力

### 1. 活动类型特点

**"买A赠B券"核心机制**:
```
顾客购买指定商品A(或满足购买条件)
    → 系统自动发放优惠券
    → 顾客使用券可兑换赠品B
    → 赠品库存实时扣减
```

**与其他券种的区别**:
- **vs 满减券**: 不是直接减免金额,而是赠送实物商品
- **vs 折扣券**: 不是打折,而是赠送指定赠品
- **vs 代金券**: 不是现金抵扣,而是商品兑换

### 2. 功能特性

#### 2.1 购买规则配置

**支持的触发条件**:
- ✅ 购买指定商品A (单个或多个)
- ✅ 购买数量要求 (≥N份)
- ✅ 购买金额要求 (≥X元)
- ✅ 购买商品分类 (如"主食类"、"饮品类")
- ✅ 购买套餐组合

**灵活配置**:
- 支持"任意N个商品"或"特定商品"
- 支持"满N件"或"满X元"
- 支持分类级触发 (如购买任意主食即可触发)

#### 2.2 赠送规则配置

**赠品设置**:
- 🎁 赠送商品B (单个或多个可选)
- 🎁 赠送数量 (固定或阶梯式)
- 🎁 赠品价值上限 (防止套利)
- 🎁 赠品库存管理 (自动扣减)

**赠送方式**:
- **立即赠送**: 下单后自动添加到订单
- **发券赠送**: 下单后发放优惠券,顾客后续兑换

#### 2.3 库存管理

**赠品库存控制**:
- 📦 实时库存扣减 (防止超发)
- 📦 库存预警 (低于阈值时提醒)
- 📦 库存不足时自动停止活动
- 📦 多门店库存独立管理

**库存分配策略**:
- **总量控制**: 全门店共享库存池
- **门店分配**: 每个门店独立库存
- **先到先得**: 库存耗尽后自动关闭

#### 2.4 使用限制

**时间限制**:
- ⏰ 活动生效时间 (开始-结束)
- ⏰ 券有效期 (领取后N天内有效)
- ⏰ 可用时段 (如仅周末可用)

**使用限制**:
- 🚫 每人限领次数 (如每人最多领3张)
- 🚫 每单限用张数 (如每单最多用1张)
- 🚫 与其他券叠加规则 (是否可叠加使用)
- 🚫 适用门店范围 (全门店或指定门店)

#### 2.5 数据追踪

**效果监控**:
- 📈 券发放量 (已发放/剩余)
- 📈 券核销量 (使用率)
- 📈 带动销量 (商品A销售增长)
- 📈 赠品消耗 (库存变化)
- 📈 ROI分析 (活动成本vs收益)

## 快速开始

### 基础用法

```python
from scripts.buy_a_get_b_generator import BuyAGetBGenerator

# 初始化生成器
generator = BuyAGetBGenerator()

# 方式1: 自然语言输入
result = generator.create_from_text(
    text="""
    创建"买火锅套餐送饮料"活动:
    - 购买条件: 购买"豪华火锅套餐"1份
    - 赠品: 可口可乐1瓶(价值5元)
    - 活动时间: 2025年1月1日-1月31日
    - 每人限领3次
    - 赠品总库存: 500份
    """,
    project_name="春节促销活动"  # 项目名称(必填)
)

# 方式2: 结构化数据输入
data = {
    "activity_name": "买火锅套餐送饮料",
    "purchase_rules": {
        "trigger_type": "specific_product",
        "product_a": "豪华火锅套餐",
        "quantity_required": 1
    },
    "gift_rules": {
        "product_b": "可口可乐",
        "gift_quantity": 1,
        "gift_value": 5,
        "total_stock": 500
    },
    "time_settings": {
        "start_time": "2025-01-01 00:00:00",
        "end_time": "2025-01-31 23:59:59"
    },
    "usage_limits": {
        "per_user_limit": 3,
        "per_order_limit": 1
    }
}
result = generator.create_from_dict(
    data=data,
    project_name="春节促销活动"
)

# 方式3: 批量创建
batch_data = [
    {"activity_name": "买火锅送饮料", "purchase_rules": {...}},
    {"activity_name": "买主食送甜品", "purchase_rules": {...}},
    {"activity_name": "买套餐送小吃", "purchase_rules": {...}}
]
results = generator.create_batch(
    batch_data=batch_data,
    project_name="春节促销活动批量创建"
)
```

### 输出路径规范

所有生成的配置方案和操作指引按照**标准路径规范**输出:

```
output/[项目名]/buy-a-get-b-coupon/
├── 买A赠B券配置_买火锅送饮料_20250103_143000.xlsx
├── 操作指引_买火锅送饮料_20250103_143000.pdf
├── 批量配置方案_20250103_143002.xlsx
├── plan_买A赠B券创建_20250103_143000.json
├── log_execution_20250103_143000.txt
└── metadata_20250103_143000.json
```

**⚠️ 简化版路径结构**:
- 不再使用 `plans/results/logs/metadata/` 子目录
- 所有文件直接存放在 `output/[项目名]/buy-a-get-b-coupon/` 目录下
- 通过文件名前缀区分类型 (如: `plan_xxx.json`, `买A赠B券配置_xxx.xlsx`, `log_xxx.txt`)

## 创建流程详解

### 美团管家后台操作路径

**导航路径**:
```
美团管家后台
  → 营销中心
  → 优惠券管理
  → 创建优惠券
  → 选择券种类型: "买A赠B券"
```

### 必填表单字段清单

#### 第一部分: 活动基本信息

| 字段编号 | 字段名称 | 必填 | 说明 | 示例 |
|---------|---------|------|------|------|
| 1 | 活动名称 | ✅ | 内部管理名称,顾客不可见 | "春节买火锅送饮料活动" |
| 2 | 活动宣传语 | ✅ | 展示给顾客的文案 | "买豪华火锅套餐,免费送可口可乐!" |
| 3 | 活动生效时间 | ✅ | 开始时间-结束时间 | 2025-01-01 00:00 ~ 2025-01-31 23:59 |
| 4 | 券有效期 | ✅ | 顾客领取后的有效天数 | 7天 (领取后7天内有效) |
| 5 | 活动说明 | ❌ | 活动规则详细说明 | "仅限堂食使用,不可与其他活动叠加" |

#### 第二部分: 购买规则配置

| 字段编号 | 字段名称 | 必填 | 说明 | 示例 |
|---------|---------|------|------|------|
| 6 | 触发条件类型 | ✅ | 购买何种商品触发 | 选项: 指定商品/商品分类/满金额 |
| 7 | 指定商品A | ✅ | 触发活动的商品 | "豪华火锅套餐" (从商品库选择) |
| 8 | 购买数量要求 | ✅ | 至少购买几份 | ≥1份 |
| 9 | 购买金额要求 | ❌ | 订单金额要求 (可选) | ≥100元 (与商品条件二选一) |
| 10 | 商品分类范围 | ❌ | 按分类触发 (可选) | "主食类"/"饮品类"等 |

**配置说明**:
- **指定商品**: 必须购买特定商品A才能触发 (如"豪华火锅套餐")
- **商品分类**: 购买该分类下任意商品即可触发 (如购买任意"主食类"商品)
- **满金额**: 订单总金额达到阈值即可触发 (如满100元)

#### 第三部分: 赠送规则配置

| 字段编号 | 字段名称 | 必填 | 说明 | 示例 |
|---------|---------|------|------|------|
| 11 | 赠品类型 | ✅ | 赠送方式 | 选项: 立即赠送/发券兑换 |
| 12 | 赠送商品B | ✅ | 赠送的商品 | "可口可乐" (从商品库选择) |
| 13 | 赠送数量 | ✅ | 每次赠送几个 | 1瓶 |
| 14 | 赠品价值上限 | ❌ | 防止套利 | ≤10元 (可选) |
| 15 | 赠品总库存 | ✅ | 活动总库存量 | 500份 |
| 16 | 库存分配模式 | ✅ | 库存管理方式 | 选项: 总量控制/按门店分配 |
| 17 | 库存预警阈值 | ❌ | 低于此值时提醒 | 50份 (剩余10%时预警) |

**配置说明**:
- **立即赠送**: 下单时自动添加赠品到订单 (适合堂食/自提)
- **发券兑换**: 下单后发放优惠券,顾客后续使用券兑换 (适合外卖/打包)
- **总量控制**: 全门店共享库存池 (先到先得)
- **按门店分配**: 每个门店独立库存 (避免单店耗尽)

#### 第四部分: 使用限制配置

| 字段编号 | 字段名称 | 必填 | 说明 | 示例 |
|---------|---------|------|------|------|
| 18 | 每人限领次数 | ✅ | 单用户可领取次数 | 3次 (每人最多领3张) |
| 19 | 每单限用张数 | ✅ | 单笔订单可用张数 | 1张 (每单最多用1张) |
| 20 | 适用门店范围 | ✅ | 可用门店 | 选项: 全门店/指定门店 |
| 21 | 可用时段 | ❌ | 限制使用时间 | 如: 仅周末 11:00-22:00可用 |
| 22 | 适用订单类型 | ✅ | 堂食/外卖/自提 | 选项: 全部/仅堂食/仅外卖 |
| 23 | 与其他券叠加 | ❌ | 是否可与其他券同用 | 选项: 可叠加/不可叠加 |

#### 第五部分: 展示配置

| 字段编号 | 字段名称 | 必填 | 说明 | 示例 |
|---------|---------|------|------|------|
| 24 | 券面设计 | ✅ | 优惠券展示样式 | 选择模板或自定义 |
| 25 | 活动封面图 | ❌ | 券列表展示图 | 750x400px, ≤500KB |
| 26 | 活动详情图 | ❌ | 券详情页展示图 | 750x1200px, ≤1MB |
| 27 | 按钮文案 | ❌ | 领取按钮文字 | "立即领取"/"马上抢" |

#### 第六部分: 高级配置

| 字段编号 | 字段名称 | 必填 | 说明 | 示例 |
|---------|---------|------|------|------|
| 28 | 用户分群 | ❌ | 限定发放人群 | 如: 新用户/会员/特定标签用户 |
| 29 | 发放方式 | ✅ | 券的发放渠道 | 选项: 自动发放/手动领取/活动页领取 |
| 30 | 发放总量上限 | ❌ | 最多发放张数 | 1000张 (发完即止) |
| 31 | 核销提醒 | ❌ | 使用时提醒商家 | 开启/关闭 |
| 32 | 数据统计维度 | ❌ | 自定义统计字段 | 如: 按门店/按时段统计 |

### 完整配置示例

**场景**: 春节促销 - 买火锅套餐送饮料

```json
{
  "activity_basic_info": {
    "activity_name": "春节买火锅送饮料活动",
    "promotion_text": "买豪华火锅套餐,免费送可口可乐!",
    "start_time": "2025-01-01 00:00:00",
    "end_time": "2025-01-31 23:59:59",
    "coupon_validity_days": 7,
    "activity_description": "春节特惠,买火锅套餐即送饮料,仅限堂食,不可与其他活动叠加。"
  },
  "purchase_rules": {
    "trigger_type": "specific_product",
    "product_a": {
      "product_id": "SKU001",
      "product_name": "豪华火锅套餐",
      "quantity_required": 1
    },
    "amount_required": null
  },
  "gift_rules": {
    "gift_type": "immediate_gift",
    "product_b": {
      "product_id": "SKU099",
      "product_name": "可口可乐",
      "gift_quantity": 1,
      "gift_value_limit": 10
    },
    "stock_settings": {
      "total_stock": 500,
      "allocation_mode": "total_pool",
      "warning_threshold": 50
    }
  },
  "usage_limits": {
    "per_user_limit": 3,
    "per_order_limit": 1,
    "applicable_stores": "all",
    "available_time_slots": null,
    "order_types": ["dine_in"],
    "stackable_with_others": false
  },
  "display_config": {
    "coupon_template": "template_001",
    "cover_image": "url_to_cover_image.jpg",
    "detail_image": "url_to_detail_image.jpg",
    "button_text": "立即领取"
  },
  "advanced_config": {
    "user_segmentation": null,
    "distribution_method": "auto_issue",
    "max_distribution": 1000,
    "redemption_alert": true,
    "custom_stats_dimensions": ["store", "time_slot"]
  }
}
```

## 核心工作流程 (三层架构)

### Layer 1: 规范层 (本文档)

**定义内容**:
- ✅ 业务目标: 通过"买A赠B"机制促进销量和客单价
- ✅ 领域知识: 美团优惠券平台规则和"买A赠B券"机制
- ✅ 工作流程: 从需求分析到后台配置的完整流程
- ✅ 质量标准: 字段完整性验证、库存管理规范、活动效果追踪

### Layer 2: 计划层 (JSON配置)

**执行计划示例**:

```json
{
  "plan_id": "plan_买A赠B券创建_20250103_143000",
  "project_name": "春节促销活动",
  "skill_name": "buy-a-get-b-coupon",
  "task_type": "single",
  "execution_config": {
    "validate_stock": true,
    "auto_alert_low_stock": true,
    "generate_operation_guide": true
  },
  "tasks": [
    {
      "task_id": "T001",
      "activity_name": "春节买火锅送饮料活动",
      "activity_basic_info": {
        "promotion_text": "买豪华火锅套餐,免费送可口可乐!",
        "start_time": "2025-01-01 00:00:00",
        "end_time": "2025-01-31 23:59:59",
        "coupon_validity_days": 7
      },
      "purchase_rules": {
        "trigger_type": "specific_product",
        "product_a": "豪华火锅套餐",
        "quantity_required": 1
      },
      "gift_rules": {
        "product_b": "可口可乐",
        "gift_quantity": 1,
        "total_stock": 500
      },
      "usage_limits": {
        "per_user_limit": 3,
        "per_order_limit": 1,
        "order_types": ["dine_in"]
      }
    }
  ],
  "output_paths": {
    "config_file": "output/春节促销活动/buy-a-get-b-coupon/买A赠B券配置_春节买火锅送饮料_20250103_143000.xlsx",
    "operation_guide": "output/春节促销活动/buy-a-get-b-coupon/操作指引_春节买火锅送饮料_20250103_143000.pdf"
  }
}
```

**计划配置文件位置**:
- `output/[项目名]/buy-a-get-b-coupon/plan_*.json`

### Layer 3: 执行层 (Python脚本)

**核心执行引擎**:
- `scripts/buy_a_get_b_generator.py` - 主生成器
- `scripts/parsers/activity_parser.py` - 活动需求解析
- `scripts/validators/field_validator.py` - 字段完整性验证
- `scripts/validators/stock_validator.py` - 库存合理性验证
- `scripts/generators/config_generator.py` - 配置方案生成器
- `scripts/generators/guide_generator.py` - 操作指引生成器

**执行步骤**:

1. **Step 1: 需求解析与结构化**
   - 调用 `activity_parser.py`
   - 提取活动信息、购买规则、赠送规则、使用限制等
   - 标准化字段格式

2. **Step 2: 字段完整性验证**
   - 调用 `field_validator.py`
   - 验证32个字段的必填性和格式
   - 报告缺失或格式错误的字段

3. **Step 3: 库存合理性验证**
   - 调用 `stock_validator.py`
   - 验证赠品库存是否充足
   - 计算预期活动周期内的库存消耗
   - 提供库存预警建议

4. **Step 4: 商品库匹配**
   - 从美团商品库匹配商品A和商品B
   - 验证商品ID的有效性
   - 获取商品价格、库存等信息

5. **Step 5: 配置方案生成**
   - 调用 `config_generator.py`
   - 生成Excel配置表 (所有字段填充完整)
   - 生成JSON配置文件 (供API调用)

6. **Step 6: 操作指引生成**
   - 调用 `guide_generator.py`
   - 生成PDF操作指引 (含截图和步骤说明)
   - 包含后台操作路径、字段填写说明、注意事项

## 执行流程图

```
用户输入 (活动需求)
    ↓
[Step 1] 需求解析与结构化
    ├─ 提取活动基本信息
    ├─ 提取购买规则
    ├─ 提取赠送规则
    └─ 提取使用限制
    ↓
[Step 2] 字段完整性验证
    ├─ 验证32个表单字段
    ├─ 必填字段检查
    └─ 格式规范验证
    ↓
[Step 3] 库存合理性验证
    ├─ 验证赠品库存充足性
    ├─ 计算预期消耗量
    └─ 生成库存预警建议
    ↓
[Step 4] 商品库匹配
    ├─ 匹配商品A (购买商品)
    ├─ 匹配商品B (赠品)
    └─ 验证商品ID有效性
    ↓
[Step 5] 配置方案生成
    ├─ 生成Excel配置表
    ├─ 生成JSON配置文件
    └─ 填充所有字段数据
    ↓
[Step 6] 操作指引生成
    ├─ 生成PDF操作指引
    ├─ 包含后台操作截图
    └─ 详细步骤说明
    ↓
输出配置方案 + 操作指引 + 执行日志 + 元数据
```

## 使用场景

### 场景1: 新品推广活动

**需求**: 推广新上线的"冬日暖心套餐",提升首单转化率

**输入**:
```python
generator.create_from_text(
    text="""
    创建"买冬日暖心套餐送热饮"活动:
    - 购买条件: 购买"冬日暖心套餐"1份
    - 赠品: 招牌奶茶1杯(价值12元)
    - 活动时间: 2025年1月1日-1月31日
    - 每人限领5次
    - 赠品总库存: 1000份
    - 仅限堂食使用
    """,
    project_name="冬季新品推广"
)
```

**输出**:
- `output/冬季新品推广/buy-a-get-b-coupon/买A赠B券配置_买冬日暖心套餐送热饮_YYYYMMDD_HHMMSS.xlsx`
- `output/冬季新品推广/buy-a-get-b-coupon/操作指引_买冬日暖心套餐送热饮_YYYYMMDD_HHMMSS.pdf`

### 场景2: 库存消化活动

**需求**: 快速消化临期库存"麻辣鸭脖",通过赠送热销品引流

**输入**:
```python
data = {
    "activity_name": "买鸭脖送啤酒活动",
    "purchase_rules": {
        "trigger_type": "specific_product",
        "product_a": "麻辣鸭脖(临期)",
        "quantity_required": 2
    },
    "gift_rules": {
        "product_b": "雪花啤酒",
        "gift_quantity": 1,
        "total_stock": 300
    },
    "time_settings": {
        "start_time": "2025-01-10 00:00:00",
        "end_time": "2025-01-20 23:59:59"
    },
    "usage_limits": {
        "per_user_limit": 2,
        "per_order_limit": 1,
        "order_types": ["dine_in", "takeout"]
    }
}
generator.create_from_dict(
    data=data,
    project_name="临期库存清仓"
)
```

**输出**:
- `output/临期库存清仓/buy-a-get-b-coupon/买A赠B券配置_买鸭脖送啤酒_YYYYMMDD_HHMMSS.xlsx`

### 场景3: 会员福利活动

**需求**: 会员日专属福利,提升会员活跃度

**输入**:
```python
data = {
    "activity_name": "会员日买套餐送甜品",
    "purchase_rules": {
        "trigger_type": "amount_threshold",
        "amount_required": 88
    },
    "gift_rules": {
        "product_b": "提拉米苏",
        "gift_quantity": 1,
        "total_stock": 200
    },
    "time_settings": {
        "start_time": "2025-01-15 00:00:00",
        "end_time": "2025-01-15 23:59:59"
    },
    "usage_limits": {
        "per_user_limit": 1,
        "per_order_limit": 1
    },
    "advanced_config": {
        "user_segmentation": "members_only"
    }
}
generator.create_from_dict(
    data=data,
    project_name="会员日专属活动"
)
```

### 场景4: 批量创建多活动

**需求**: 春节期间同时推出5个"买A赠B"活动

**输入**:
```python
batch_data = [
    {"activity_name": "买火锅送饮料", "purchase_rules": {...}},
    {"activity_name": "买主食送甜品", "purchase_rules": {...}},
    {"activity_name": "买套餐送小吃", "purchase_rules": {...}},
    {"activity_name": "买酒水送下酒菜", "purchase_rules": {...}},
    {"activity_name": "买早餐送豆浆", "purchase_rules": {...}}
]
results = generator.create_batch(
    batch_data=batch_data,
    project_name="春节促销活动批量创建"
)
```

**输出**:
- `output/春节促销活动批量创建/buy-a-get-b-coupon/批量配置方案_YYYYMMDD_HHMMSS.xlsx`
- 包含5个活动的完整配置

## 高级特性

### 1. 智能库存预警

**问题**: 活动上线后赠品库存快速耗尽

**解决方案**:
- 根据历史数据预测活动期间的库存消耗
- 库存低于阈值时自动提醒补货
- 库存耗尽时自动暂停活动

```python
from scripts.validators.stock_validator import StockValidator

validator = StockValidator()
result = validator.predict_stock_consumption(
    activity_duration_days=30,
    expected_daily_orders=50,
    gift_per_order=1
)
# result = {"predicted_consumption": 1500, "current_stock": 500, "status": "insufficient"}
```

### 2. 活动效果模拟

**问题**: 不知道活动能带来多少销量增长

**解决方案**:
- 基于历史数据模拟活动效果
- 预测券发放量、核销率、带动销量
- 计算ROI (投入产出比)

```python
from scripts.simulators.activity_simulator import ActivitySimulator

simulator = ActivitySimulator()
result = simulator.simulate(
    purchase_product="豪华火锅套餐",
    gift_product="可口可乐",
    activity_duration_days=30,
    historical_avg_daily_orders=20
)
# result = {
#     "predicted_orders": 600,
#     "predicted_coupon_usage": 450,
#     "predicted_revenue_increase": 12000,
#     "roi": 3.5
# }
```

### 3. A/B测试支持

**问题**: 不确定哪个赠品更吸引顾客

**解决方案**:
- 同时创建两个活动 (赠品A vs 赠品B)
- 分配到不同门店或时段
- 对比活动效果数据

```python
# 创建A/B测试活动
activities = [
    {"activity_name": "买火锅送可乐", "gift_rules": {"product_b": "可口可乐"}},
    {"activity_name": "买火锅送雪碧", "gift_rules": {"product_b": "雪碧"}}
]
results = generator.create_ab_test(
    activities=activities,
    test_duration_days=7,
    project_name="赠品A/B测试"
)
```

### 4. 自动数据追踪

**问题**: 活动上线后需要手动统计效果数据

**解决方案**:
- 自动生成数据追踪配置
- 每日定时抓取美团后台数据
- 生成可视化报表

```python
from scripts.trackers.activity_tracker import ActivityTracker

tracker = ActivityTracker()
tracker.setup_auto_tracking(
    activity_id="ACT001",
    tracking_interval_hours=24,
    alert_thresholds={
        "low_usage_rate": 0.3,  # 核销率<30%时预警
        "low_stock": 50  # 库存<50时预警
    }
)
```

## 质量保障

### 1. 字段完整性验证

**验证规则**:
```python
REQUIRED_FIELDS = {
    "activity_basic_info": ["activity_name", "promotion_text", "start_time", "end_time", "coupon_validity_days"],
    "purchase_rules": ["trigger_type", "product_a", "quantity_required"],
    "gift_rules": ["product_b", "gift_quantity", "total_stock"],
    "usage_limits": ["per_user_limit", "per_order_limit", "order_types"]
}
```

**验证流程**:
1. 验证所有必填字段是否存在
2. 验证字段格式是否正确 (如时间格式、数值范围)
3. 验证业务逻辑是否合理 (如开始时间<结束时间)

### 2. 库存合理性验证

**验证规则**:
```python
# 预测活动期间的库存消耗
predicted_consumption = activity_duration_days * expected_daily_orders * gift_per_order

# 验证库存是否充足
if current_stock < predicted_consumption:
    alert("库存不足,建议补货至{}份".format(predicted_consumption))
```

### 3. 商品ID有效性验证

**验证流程**:
1. 从美团商品库查询商品A和商品B
2. 验证商品ID是否存在
3. 验证商品是否在售 (状态=上架)
4. 验证商品库存是否充足

### 4. 配置方案审核

**审核清单**:
- ✅ 活动时间是否合理 (不跨度过长)
- ✅ 赠品价值是否合理 (不过高导致亏损)
- ✅ 每人限领次数是否合理 (防止羊毛党)
- ✅ 库存是否充足 (支撑整个活动周期)
- ✅ 使用限制是否明确 (避免顾客纠纷)

## 依赖资源

### 数据源文件

1. **美团商品库**:
   - `plugins/美团组/templates/美团商品库_总部.xlsx`
   - 用于匹配商品A和商品B的商品ID

2. **历史活动数据**:
   - `plugins/美团组/data/历史活动效果数据.xlsx`
   - 用于活动效果预测和库存消耗预测

3. **操作指引模板**:
   - `plugins/美团组/templates/买A赠B券操作指引模板.docx`
   - 用于生成PDF操作指引

### 技能包依赖

- **奥术光辉/excel**: Excel处理能力
  - 位置: `.claude/skills/奥术光辉/excel/`
  - 功能: 生成配置表、数据验证

- **奥术光辉/document**: 文档生成能力
  - 位置: `.claude/skills/奥术光辉/document/`
  - 功能: 生成PDF操作指引

### Python库依赖

```
pandas >= 2.0.0
openpyxl >= 3.1.0
reportlab >= 4.0.0  # PDF生成
Pillow >= 10.0.0    # 图片处理
```

## 注意事项

### 1. 库存管理

**问题**: 赠品库存不足导致活动中断

**建议**:
- 活动上线前预留20%安全库存
- 设置库存预警阈值 (如剩余10%时提醒)
- 库存耗尽时自动暂停活动

### 2. 赠品价值控制

**问题**: 赠品价值过高导致活动亏损

**建议**:
- 赠品价值控制在商品A价格的10-20%
- 设置赠品价值上限 (如≤20元)
- 定期评估活动ROI

### 3. 防止套利行为

**问题**: 羊毛党恶意刷券

**建议**:
- 设置合理的每人限领次数 (如3-5次)
- 限制账号注册时间 (如注册满7天才能领)
- 启用风控系统识别异常订单

### 4. 活动冲突管理

**问题**: 多个活动同时进行,顾客困惑

**建议**:
- 明确活动叠加规则 (可叠加/不可叠加)
- 避免同类活动同时上线
- 提供清晰的活动说明文案

### 5. 数据追踪与优化

**问题**: 活动上线后缺乏数据支持优化决策

**建议**:
- 设置关键指标追踪 (券发放量、核销率、带动销量)
- 每周分析数据,及时调整活动参数
- A/B测试不同赠品,找到最优方案

## 相关文档

- [三层架构规范](~/.claude/CLAUDE.md#5-复杂系统三层架构规范)
- [输出路径规范](~/.claude/CLAUDE.md#45-输出路径规范)
- [奥术光辉/excel技能包](.claude/skills/奥术光辉/excel/SKILL.md)
- [美团优惠券平台规则](plugins/美团组/docs/美团优惠券平台规则.md)
- [买A赠B券操作指引模板](plugins/美团组/templates/买A赠B券操作指引模板.docx)

## 版本历史

- **v1.0.0** (2025-01-03): 初始版本
  - 支持单个和批量活动创建
  - 完整的32字段配置方案
  - 库存管理和效果预测
  - PDF操作指引生成
  - 集成三层架构模式
