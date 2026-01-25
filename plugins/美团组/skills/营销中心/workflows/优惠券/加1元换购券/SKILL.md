---
name: add-one-yuan-coupon
description: SOP型技能包,用于在美团管家后台创建"加1元换购券"优惠券活动。自动解析活动需求,生成标准化配置,支持换购商品设置、价格策略、库存控制和使用限制的智能配置。
version: 1.0.0
category: 营销中心/workflows/优惠券
author: ZTL数智化作战中心
tags: [优惠券, 加1元换购券, 营销活动, SOP, 美团管家]
---

# 加1元换购券创建技能包 (Add One Yuan Exchange Coupon)

## 概述

这是一个**标准操作流程(SOP)型技能包**,用于自动化创建美团管家后台的"加1元换购券"优惠券活动。遵循**三层架构模式**,支持单个和批量创建,能够智能解析活动需求并生成完整的配置方案。

**业务目标**:
- 🎯 提升客单价: 通过低价换购引导用户增加订单金额
- 🎯 促进新品推广: 以换购形式推广新上市菜品/饮品
- 🎯 提高用户粘性: 创造超值感,增强用户复购意愿
- 🎯 精准营销: 定向门店、时段、人群的差异化促销

**适用场景**:
- ✅ 新品推广: 新上市饮品/菜品的试吃推广
- ✅ 客单价提升: 满XX元加1元换购指定商品
- ✅ 库存消耗: 临期商品、滞销商品的清仓处理
- ✅ 节日促销: 节假日期间的特殊优惠活动
- ✅ 会员专享: 特定会员等级的增值福利

## 核心能力

### 1. 活动配置智能生成

**支持输入格式**:
- ✅ 自然语言描述 (中文/英文)
- ✅ 结构化数据 (JSON/CSV)
- ✅ Excel批量配置
- ✅ 现有活动复制修改

**智能提取能力**:
- 活动基本信息 (名称、时间、门店范围)
- 换购规则 (消费条件、换购商品、加价金额)
- 使用限制 (领取限制、使用限制、时段限制)
- 库存管理 (总库存、每日库存)

### 2. 换购商品配置

#### 换购商品设置

**支持配置项**:
- 换购商品选择 (菜品/饮品/套餐)
- 加价金额设定 (通常为1元,可调整)
- 换购库存控制 (总量/每日限量)
- 商品排除规则 (不可换购商品)

**配置策略**:
1. **单品换购**: 指定1个商品可加1元换购
2. **多选一换购**: 从N个商品中任选1个加1元换购
3. **多选多换购**: 可换购多个商品,每个加1元
4. **阶梯换购**: 消费金额越高,可换购商品越多

### 3. 活动规则配置

#### 消费条件设置

**门槛类型**:
- 消费金额门槛 (如满50元可换购)
- 订单菜品数量 (如购买3个菜品可换购)
- 特定商品购买 (如购买指定套餐可换购)
- 无门槛换购 (所有订单均可)

#### 使用限制配置

**限制维度**:
- 每人限领: 1张/N张/不限
- 每日限用: 1次/N次/不限
- 每单限用: 1张/N张
- 使用时段: 全天/午市/晚市/自定义时段

### 4. 门店与渠道配置

**适用门店**:
- 全部门店
- 指定门店 (按商户号)
- 门店分组 (按区域/类型)

**适用渠道**:
- 美团外卖
- 美团团购
- 堂食点餐 (小程序)
- 全渠道通用

## 快速开始

### 基础用法

```python
from scripts.add_one_yuan_coupon_generator import AddOneYuanCouponGenerator

# 初始化生成器
generator = AddOneYuanCouponGenerator()

# 方式1: 自然语言输入
result = generator.create_from_text(
    text="""
    创建一个"加1元换购可乐"活动:
    - 活动时间: 2025-01-10到2025-01-20
    - 消费条件: 满50元
    - 换购商品: 可口可乐500ml
    - 加价金额: 1元
    - 每人限领1张,每日限用1次
    - 适用门店: 全部门店
    - 总库存: 1000张
    """,
    project_name="春节促销活动"  # 项目名称(必填)
)

# 方式2: 结构化数据输入
config = {
    "activity_name": "加1元换购可乐",
    "activity_time": {
        "start_date": "2025-01-10",
        "end_date": "2025-01-20",
        "valid_hours": "全天"  # 或 "11:00-14:00,17:00-21:00"
    },
    "consumption_condition": {
        "type": "amount",  # amount/quantity/specific_product/none
        "threshold": 50,  # 消费金额门槛
        "unit": "元"
    },
    "exchange_items": [
        {
            "item_name": "可口可乐500ml",
            "item_type": "饮品",
            "add_price": 1,  # 加价金额
            "stock": 1000,  # 该商品换购库存
            "daily_stock": 50  # 每日库存(可选)
        }
    ],
    "usage_limits": {
        "receive_limit": 1,  # 每人限领
        "daily_usage_limit": 1,  # 每日限用
        "per_order_limit": 1  # 每单限用
    },
    "store_scope": {
        "type": "all",  # all/specific/group
        "store_ids": []  # 指定门店商户号(可选)
    }
}

result = generator.create_from_dict(
    config=config,
    project_name="春节促销活动"
)

# 方式3: 批量创建
batch_configs = [
    {"activity_name": "加1元换购可乐", ...},
    {"activity_name": "加1元换购雪碧", ...},
    {"activity_name": "加1元换购奶茶", ...}
]

results = generator.create_batch(
    batch_configs=batch_configs,
    project_name="春节促销活动"
)
```

### 输出路径规范

所有生成的配置文件按照**标准路径规范**输出:

```
output/[项目名]/add-one-yuan-coupon/
├── 加1元换购可乐_20250103_143000.json
├── 加1元换购雪碧_20250103_143001.json
├── 批量换购券配置_20250103_143002.xlsx
├── plan_换购券创建_20250103_143000.json
├── log_execution_20250103_143000.txt
└── metadata_20250103_143000.json
```

**⚠️ 简化版路径结构**:
- 不再使用 `plans/results/logs/metadata/` 子目录
- 所有文件直接存放在 `output/[项目名]/add-one-yuan-coupon/` 目录下
- 通过文件名前缀区分类型 (如: `plan_xxx.json`, `加1元换购xxx.json`, `log_xxx.txt`)

## 核心工作流程 (三层架构)

### Layer 1: 规范层 (本文档)

**定义内容**:
- ✅ 业务目标: 创建加1元换购券活动,提升客单价和新品推广
- ✅ 领域知识: 美团管家优惠券配置规范和字段说明
- ✅ 工作流程: 5个步骤的标准化流程
- ✅ 质量标准: 字段必填验证、规则合规性检查、配置完整性

### Layer 2: 计划层 (JSON配置)

**执行计划示例**:

```json
{
  "plan_id": "plan_换购券创建_20250103_143000",
  "project_name": "春节促销活动",
  "skill_name": "add-one-yuan-coupon",
  "task_type": "single",
  "execution_config": {
    "platform": "meituan_manager",
    "validate_rules": true,
    "auto_calculate_stock": true
  },
  "tasks": [
    {
      "task_id": "T001",
      "activity_basic": {
        "activity_name": "加1元换购可乐",
        "activity_description": "满50元加1元换购可口可乐500ml",
        "start_time": "2025-01-10 00:00:00",
        "end_time": "2025-01-20 23:59:59",
        "valid_hours": "全天"
      },
      "consumption_condition": {
        "type": "amount",
        "threshold": 50,
        "description": "订单金额满50元"
      },
      "exchange_items": [
        {
          "item_name": "可口可乐500ml",
          "item_code": "DRINK_001",
          "item_type": "饮品",
          "add_price": 1,
          "original_price": 6,
          "stock": 1000,
          "daily_stock": 50
        }
      ],
      "usage_limits": {
        "receive_limit_per_user": 1,
        "daily_usage_limit": 1,
        "per_order_limit": 1,
        "combine_with_other_coupons": false
      },
      "store_scope": {
        "type": "all",
        "store_count": 10,
        "store_list": []
      },
      "channel_scope": ["外卖", "团购", "堂食"]
    }
  ],
  "output_path": "output/春节促销活动/add-one-yuan-coupon/加1元换购可乐_20250103_143000.json"
}
```

**计划配置文件位置**:
- `output/[项目名]/add-one-yuan-coupon/plan_*.json`

### Layer 3: 执行层 (Python脚本)

**核心执行引擎**:
- `scripts/add_one_yuan_coupon_generator.py` - 主生成器
- `scripts/parsers/coupon_text_parser.py` - 自然语言解析
- `scripts/validators/coupon_rule_validator.py` - 规则验证器
- `scripts/matchers/item_matcher.py` - 商品匹配器
- `scripts/generators/coupon_config_generator.py` - 配置生成器

**执行步骤**:

1. **Step 1: 活动需求解析**
   - 调用 `coupon_text_parser.py` 或接收结构化数据
   - 提取活动名称、时间、消费条件、换购商品等信息
   - 智能识别业务意图 (新品推广/客单价提升/库存消耗)

2. **Step 2: 商品信息匹配**
   - 调用 `item_matcher.py`
   - 匹配换购商品的编码、价格、库存信息
   - 验证商品是否可用于换购活动

3. **Step 3: 规则合规性验证**
   - 调用 `coupon_rule_validator.py`
   - 验证活动时间合理性 (开始时间<结束时间)
   - 验证使用限制合理性 (领取限制≤库存)
   - 验证门店范围有效性

4. **Step 4: 配置方案生成**
   - 按照美团管家后台表单结构组织数据
   - 生成完整的JSON配置文件
   - 生成人工操作指引文档

5. **Step 5: 输出与追溯**
   - 保存配置到标准输出路径
   - 生成执行日志和元数据
   - 记录配置版本和变更历史

## 创建流程: 美团管家后台配置

### 第一步: 活动基本信息

**必填字段**:

| 字段名称 | 必填 | 字段说明 | 示例 |
|---------|------|---------|------|
| 活动名称 | ✅ | 优惠券活动名称,建议包含换购商品 | 加1元换购可乐 |
| 活动描述 | ❌ | 活动详细说明,向用户展示 | 满50元加1元换购可口可乐500ml |
| 开始时间 | ✅ | 活动开始日期和时间 | 2025-01-10 00:00:00 |
| 结束时间 | ✅ | 活动结束日期和时间 | 2025-01-20 23:59:59 |
| 有效时段 | ❌ | 每日可用时段,不填则全天有效 | 11:00-14:00,17:00-21:00 |

**配置说明**:
- 活动名称建议格式: "加N元换购XXX"
- 开始时间必须晚于当前时间
- 结束时间必须晚于开始时间
- 有效时段支持多个时间段,用逗号分隔

### 第二步: 消费条件设置

**条件类型**:

| 条件类型 | 配置说明 | 示例 |
|---------|---------|------|
| 消费金额 | 订单金额满XX元可换购 | 满50元 |
| 菜品数量 | 订单菜品数量达到N个可换购 | 购买3个菜品 |
| 指定商品 | 购买指定商品后可换购 | 购买套餐A |
| 无门槛 | 所有订单均可换购 | 无条件 |

**配置字段**:

| 字段名称 | 必填 | 字段说明 | 示例 |
|---------|------|---------|------|
| 条件类型 | ✅ | 从上述4种类型中选择 | 消费金额 |
| 门槛值 | ✅ | 具体的金额/数量/商品编码 | 50(元) |
| 是否包含配送费 | ❌ | 消费金额是否包含配送费 | 否 |
| 是否包含包装费 | ❌ | 消费金额是否包含包装费 | 否 |

### 第三步: 换购商品配置

**商品选择**:

| 字段名称 | 必填 | 字段说明 | 示例 |
|---------|------|---------|------|
| 换购商品 | ✅ | 从菜品库选择可换购的商品 | 可口可乐500ml |
| 商品编码 | ✅ | 系统自动填充,唯一标识 | DRINK_001 |
| 原价 | ✅ | 商品正常售价 | 6元 |
| 加价金额 | ✅ | 用户需额外支付的金额 | 1元 |
| 换购库存 | ✅ | 该商品总换购数量 | 1000 |
| 每日库存 | ❌ | 每日最多可换购数量 | 50 |

**换购模式**:

| 模式 | 说明 | 配置方式 |
|------|------|---------|
| 单品换购 | 只能选择1个商品换购 | 添加1个商品 |
| 多选一换购 | 从N个商品中选1个换购 | 添加N个商品,设置"任选1个" |
| 多选多换购 | 可同时换购多个商品 | 添加N个商品,设置"可选多个" |

### 第四步: 使用限制设置

**领取限制**:

| 字段名称 | 必填 | 字段说明 | 示例 |
|---------|------|---------|------|
| 每人限领 | ✅ | 每个用户最多领取张数 | 1张 |
| 自动发放 | ❌ | 满足条件自动发放到用户卡包 | 是 |
| 领取后生效时间 | ❌ | 领取后多久可使用 | 立即生效 |
| 券有效期 | ❌ | 领取后多少天内有效 | 7天 |

**使用限制**:

| 字段名称 | 必填 | 字段说明 | 示例 |
|---------|------|---------|------|
| 每日限用 | ✅ | 每个用户每天最多使用次数 | 1次 |
| 每单限用 | ✅ | 每个订单最多使用张数 | 1张 |
| 是否可叠加使用 | ✅ | 是否可与其他优惠券同时使用 | 否 |
| 适用支付方式 | ❌ | 限制特定支付方式,不填则不限 | 不限 |

**时段限制**:

| 字段名称 | 必填 | 字段说明 | 示例 |
|---------|------|---------|------|
| 可用时段 | ❌ | 每日可使用时间段,不填则全天 | 11:00-14:00,17:00-21:00 |
| 排除日期 | ❌ | 特殊日期不可使用(如节假日) | 2025-02-01,2025-02-02 |

### 第五步: 适用门店设置

**门店范围**:

| 字段名称 | 必填 | 字段说明 | 示例 |
|---------|------|---------|------|
| 适用门店 | ✅ | 选择活动适用的门店范围 | 全部门店 |
| 门店商户号 | ❌ | 指定门店时填写商户号列表 | [12345, 67890] |
| 门店分组 | ❌ | 按区域/类型分组选择 | 华北区/旗舰店 |

**适用渠道**:

| 字段名称 | 必填 | 字段说明 | 示例 |
|---------|------|---------|------|
| 外卖渠道 | ❌ | 是否适用于外卖订单 | 是 |
| 团购渠道 | ❌ | 是否适用于团购订单 | 是 |
| 堂食渠道 | ❌ | 是否适用于堂食扫码点餐 | 否 |

### 第六步: 库存与预算设置

**库存管理**:

| 字段名称 | 必填 | 字段说明 | 示例 |
|---------|------|---------|------|
| 总库存 | ✅ | 活动总发券数量 | 1000张 |
| 每日库存 | ❌ | 每日最多发券数量 | 50张 |
| 库存预警阈值 | ❌ | 库存低于此值时预警 | 100张 |
| 库存耗尽后操作 | ✅ | 自动下架/显示"已抢光" | 自动下架 |

**成本预算**:

| 字段名称 | 必填 | 字段说明 | 示例 |
|---------|------|---------|------|
| 单张券成本 | ❌ | 商品原价-加价金额 | 5元(6-1) |
| 活动总预算 | ❌ | 总库存×单张券成本 | 5000元 |
| 预算预警阈值 | ❌ | 消耗预算超过此比例时预警 | 80% |

### 第七步: 其他配置

**展示设置**:

| 字段名称 | 必填 | 字段说明 | 示例 |
|---------|------|---------|------|
| 活动图片 | ❌ | 在用户端展示的活动横幅图片 | banner.jpg |
| 活动标签 | ❌ | 活动标签(如"新品推荐"/"超值换购") | 超值换购 |
| 展示顺序 | ❌ | 多个活动时的展示优先级 | 1 |

**数据追踪**:

| 字段名称 | 必填 | 字段说明 | 示例 |
|---------|------|---------|------|
| 活动编号 | ✅ | 系统自动生成,唯一标识 | ACT20250103001 |
| 创建人 | ✅ | 创建活动的管理员账号 | admin@houx.com |
| 备注 | ❌ | 内部备注信息,用户不可见 | 春节促销活动第一期 |

## 执行流程图

```
用户输入 (自然语言/结构化数据)
    ↓
[Step 1] 活动需求解析
    ├─ 提取活动名称、时间
    ├─ 提取消费条件、换购规则
    └─ 识别业务意图
    ↓
[Step 2] 商品信息匹配
    ├─ 读取菜品库
    ├─ 匹配换购商品编码和价格
    └─ 验证商品可用性
    ↓
[Step 3] 规则合规性验证
    ├─ 验证活动时间合理性
    ├─ 验证使用限制合理性
    ├─ 验证库存与领取限制一致性
    └─ 验证门店范围有效性
    ↓
[Step 4] 配置方案生成
    ├─ 按美团管家表单结构组织数据
    ├─ 生成JSON配置文件
    └─ 生成操作指引文档
    ↓
[Step 5] 输出与追溯
    ├─ 保存配置到标准路径
    ├─ 生成执行日志
    └─ 记录元数据和版本
    ↓
输出配置文件 + 操作指引 + 执行日志
```

## 使用场景

### 场景1: 新品推广活动

**需求**: 新上市奶茶"黑糖珍珠奶茶",通过加1元换购推广

**输入**:
```python
generator.create_from_text(
    text="""
    创建"加1元换购黑糖珍珠奶茶"活动:
    - 活动时间: 2025-01-15到2025-01-25 (10天)
    - 消费条件: 满40元
    - 换购商品: 黑糖珍珠奶茶(中杯)
    - 原价: 18元, 加价1元
    - 每人限领1张,每日限用1次
    - 总库存: 2000张
    - 适用门店: 全部门店
    - 适用渠道: 外卖+团购
    """,
    project_name="新品推广-黑糖珍珠奶茶"
)
```

**输出**:
- `output/新品推广-黑糖珍珠奶茶/add-one-yuan-coupon/加1元换购黑糖珍珠奶茶_YYYYMMDD_HHMMSS.json`
- `output/新品推广-黑糖珍珠奶茶/add-one-yuan-coupon/操作指引_加1元换购黑糖珍珠奶茶.md`

### 场景2: 多商品换购活动

**需求**: 用户可从3款饮品中任选1款加1元换购

**输入**:
```python
config = {
    "activity_name": "加1元任选饮品",
    "activity_time": {
        "start_date": "2025-02-01",
        "end_date": "2025-02-14"
    },
    "consumption_condition": {
        "type": "amount",
        "threshold": 60
    },
    "exchange_items": [
        {"item_name": "可口可乐500ml", "add_price": 1, "stock": 500},
        {"item_name": "雪碧500ml", "add_price": 1, "stock": 500},
        {"item_name": "冰红茶500ml", "add_price": 1, "stock": 500}
    ],
    "exchange_mode": "choose_one",  # 任选1个
    "usage_limits": {
        "receive_limit": 2,  # 可领2张
        "daily_usage_limit": 1
    }
}

generator.create_from_dict(
    config=config,
    project_name="春节促销活动"
)
```

**输出**:
- `output/春节促销活动/add-one-yuan-coupon/加1元任选饮品_YYYYMMDD_HHMMSS.json`

### 场景3: 批量创建多个换购活动

**需求**: 为10个门店分别创建定制化换购活动

**输入**:
```python
batch_configs = [
    {
        "activity_name": "北京朝阳店-加1元换购可乐",
        "store_scope": {"type": "specific", "store_ids": ["12345"]},
        "exchange_items": [{"item_name": "可口可乐500ml", "add_price": 1}]
    },
    {
        "activity_name": "上海浦东店-加1元换购雪碧",
        "store_scope": {"type": "specific", "store_ids": ["67890"]},
        "exchange_items": [{"item_name": "雪碧500ml", "add_price": 1}]
    },
    # ... 更多门店配置
]

generator.create_batch(
    batch_configs=batch_configs,
    project_name="2025Q1门店专属活动"
)
```

**输出**:
- `output/2025Q1门店专属活动/add-one-yuan-coupon/批量换购券配置_YYYYMMDD_HHMMSS.xlsx`

### 场景4: 午市/晚市差异化活动

**需求**: 午市和晚市使用不同的换购规则

**输入**:
```python
# 午市活动
lunch_config = {
    "activity_name": "午市专享-加1元换购套餐",
    "activity_time": {"valid_hours": "11:00-14:00"},
    "consumption_condition": {"type": "amount", "threshold": 30},
    "exchange_items": [{"item_name": "商务套餐A", "add_price": 1}]
}

# 晚市活动
dinner_config = {
    "activity_name": "晚市专享-加1元换购酒水",
    "activity_time": {"valid_hours": "17:00-21:00"},
    "consumption_condition": {"type": "amount", "threshold": 80},
    "exchange_items": [{"item_name": "啤酒500ml", "add_price": 1}]
}

generator.create_batch(
    batch_configs=[lunch_config, dinner_config],
    project_name="时段差异化营销"
)
```

## 高级特性

### 1. 智能库存预测

**功能**: 基于历史数据预测活动所需库存

```python
from scripts.predictors.stock_predictor import StockPredictor

predictor = StockPredictor()
predicted_stock = predictor.predict(
    activity_duration_days=10,
    target_stores=10,
    avg_daily_orders_per_store=200,
    estimated_conversion_rate=0.3  # 30%的订单会使用换购券
)
# predicted_stock = 6000 (10天 × 10门店 × 200单 × 30%)
```

### 2. 动态定价策略

**功能**: 根据商品成本和目标毛利率智能推荐加价金额

```python
from scripts.pricing.dynamic_pricer import DynamicPricer

pricer = DynamicPricer()
recommended_add_price = pricer.calculate(
    item_original_price=18,  # 原价18元
    item_cost=5,  # 成本5元
    target_profit_margin=0.5,  # 目标保留50%毛利
    min_add_price=1,  # 最低加价1元
    max_add_price=5  # 最高加价5元
)
# recommended_add_price = 2 (保证毛利率≥50%)
```

### 3. A/B测试配置

**功能**: 同时创建多个版本进行效果对比

```python
ab_test_configs = [
    {
        "version": "A",
        "activity_name": "加1元换购可乐",
        "consumption_condition": {"threshold": 50},
        "target_stores": ["12345", "12346"]  # 测试组门店
    },
    {
        "version": "B",
        "activity_name": "加1元换购雪碧",
        "consumption_condition": {"threshold": 50},
        "target_stores": ["12347", "12348"]  # 对照组门店
    }
]

generator.create_ab_test(
    ab_configs=ab_test_configs,
    project_name="换购商品AB测试"
)
```

### 4. 活动效果监控

**功能**: 自动生成活动数据看板配置

```python
from scripts.monitors.activity_monitor import ActivityMonitor

monitor = ActivityMonitor()
dashboard_config = monitor.create_dashboard(
    activity_id="ACT20250103001",
    metrics=[
        "领取率",  # 领取人数/活动曝光人数
        "使用率",  # 使用人数/领取人数
        "客单价提升",  # 使用券订单客单价 vs 未使用订单
        "ROI",  # (客单价提升×使用订单数) / 活动成本
        "库存消耗速度"  # 每日消耗量
    ]
)
```

## 质量保障

### 必填字段验证

**验证规则**:
```python
REQUIRED_FIELDS = {
    "activity_basic": ["activity_name", "start_time", "end_time"],
    "consumption_condition": ["type", "threshold"],
    "exchange_items": ["item_name", "add_price", "stock"],
    "usage_limits": ["receive_limit", "daily_usage_limit", "per_order_limit"],
    "store_scope": ["type"]
}
```

### 业务规则校验

**校验项目**:

1. **时间合理性**:
   - 开始时间 > 当前时间
   - 结束时间 > 开始时间
   - 活动时长 ≥ 1天

2. **库存一致性**:
   - 总库存 ≥ 每人限领 × 预估参与人数
   - 每日库存 × 活动天数 ≥ 总库存

3. **价格合理性**:
   - 加价金额 < 原价
   - 加价金额 ≥ 0.01元

4. **限制合理性**:
   - 每人限领 ≥ 每日限用
   - 每单限用 ≤ 每日限用

### 配置完整性检查

**检查项目**:
- ✅ 所有必填字段已填写
- ✅ 换购商品在菜品库中存在
- ✅ 适用门店商户号有效
- ✅ 活动时段配置正确
- ✅ 库存与使用限制匹配

## 依赖资源

### 数据源文件

1. **菜品库**:
   - `plugins/美团组/templates/吼巷_菜品库_总部.xlsx`
   - `plugins/美团组/templates/吼巷_菜品库_总部_做法及加料.xlsx`

2. **门店档案**:
   - `plugins/美团组/templates/门店信息清单.xlsx`

3. **优惠券模板**:
   - `plugins/美团组/templates/优惠券配置模板.json`

### 技能包依赖

- **奥术光辉/excel**: Excel数据处理
  - 位置: `.claude/skills/奥术光辉/excel/`
  - 功能: 批量配置导入/导出

- **美团组/数据分析**: 历史活动数据分析
  - 位置: `.claude/skills/美团组/数据分析/`
  - 功能: 库存预测、效果评估

### Python库依赖

```
pandas >= 2.0.0
openpyxl >= 3.1.0
pydantic >= 2.0.0  # 数据验证
```

## 注意事项

### 1. 活动时间冲突检查

**问题**: 同一门店同时存在多个换购活动可能导致冲突

**建议**:
- 创建前检查门店现有活动
- 避免同一时段多个换购活动重叠
- 使用互斥规则(不可与XX活动同时参与)

### 2. 库存预留策略

**问题**: 库存设置不合理导致活动提前结束或库存积压

**建议**:
- 总库存 = 预估参与人数 × 预估使用率 × 1.2 (20%冗余)
- 每日库存均衡分配,避免前期消耗过快
- 设置库存预警,及时调整

### 3. 加价金额设定

**问题**: 加价金额过高影响用户参与意愿

**建议**:
- 通常设置为1元(用户感知最佳)
- 高价值商品可设置2-5元
- 确保加价金额 < 原价的30%

### 4. 门店差异化配置

**问题**: 不同门店的经营情况差异大,统一配置效果不佳

**建议**:
- 根据门店客单价差异化设置消费门槛
- 根据门店客流量差异化设置库存
- 核心商圈门店可设置更有吸引力的换购商品

### 5. 防刷单机制

**问题**: 恶意用户利用换购券多次下单后取消,占用库存

**建议**:
- 设置"领取后N分钟内不可取消订单"
- 限制单用户每日领取次数
- 监控异常领取行为(多账号/同IP)

### 6. 活动效果追踪

**问题**: 活动效果无法量化评估

**建议**:
- 设置明确的KPI指标(客单价提升、新品试用率等)
- 对比活动期和非活动期数据
- A/B测试不同配置方案

## 相关文档

- [三层架构规范](~/.claude/CLAUDE.md#5-复杂系统三层架构规范)
- [输出路径规范](~/.claude/CLAUDE.md#45-输出路径规范)
- [美团管家操作手册](plugins/美团组/docs/美团管家操作手册.md)
- [优惠券营销最佳实践](plugins/美团组/docs/优惠券营销最佳实践.md)

## 版本历史

- **v1.0.0** (2025-01-03): 初始版本
  - 支持单个和批量换购券创建
  - 智能商品匹配和规则验证
  - 标准化JSON配置输出
  - 集成三层架构模式
