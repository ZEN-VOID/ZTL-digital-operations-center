---
name: product-exchange-coupon
description: SOP型技能包,用于在美团管家后台创建商品兑换券活动。自动化配置兑换规则、商品库存、使用限制等,生成符合美团平台标准的商品兑换券活动方案。
version: 1.0.0
category: 营销中心/workflows/优惠券
author: ZTL数智化作战中心
tags: [商品兑换券, 营销中心, SOP, 优惠券, 美团管家]
---

# 商品兑换券创建技能包 (Product Exchange Coupon Creator)

## 概述

这是一个**标准操作流程(SOP)型技能包**,用于自动化创建符合美团平台标准的商品兑换券活动。遵循**三层架构模式**,支持单个和批量创建,能够智能解析业务需求,生成完整的商品兑换券配置方案,并输出标准化的活动配置文件。

**业务目标**:
- 提升用户粘性:通过商品兑换激励用户领取和使用优惠券
- 促进商品销售:引导用户兑换特定商品,提升销量
- 库存管理:通过兑换券控制商品供应和库存消耗
- 营销灵活性:支持多种兑换规则(直接兑换、满额兑换、积分兑换等)

**适用场景**:
- ✅ 新品推广:用兑换券吸引用户尝试新品
- ✅ 库存清理:通过兑换券加速滞销商品出货
- ✅ 会员福利:为会员提供专属商品兑换权益
- ✅ 满赠活动:满足消费条件后赠送商品兑换券
- ✅ 积分商城:用户积分兑换实物商品

## 核心能力

### 1. 活动基本信息配置

**支持字段**:
- ✅ 活动名称 (必填)
- ✅ 活动时间 (开始时间、结束时间)
- ✅ 适用门店 (全部门店/指定门店)
- ✅ 适用商品 (全部商品/指定商品/指定分类)
- ✅ 活动说明 (对用户的活动描述)

**智能配置能力**:
- 自动生成活动名称模板 (如:"[品牌名]新品尝鲜券", "[商品名]专属兑换券")
- 智能推荐活动时间 (如:周末、节假日、特定营销节点)
- 适用门店自动匹配 (基于商品库存分布)

### 2. 兑换规则配置

#### 兑换类型

**支持类型**:
1. **直接兑换**: 用户直接领取后可兑换指定商品
2. **满额兑换**: 满足消费金额后可兑换
3. **积分兑换**: 使用积分兑换商品
4. **消费次数兑换**: 累计消费N次后可兑换
5. **组合兑换**: 多种条件组合 (如:满100元+消费2次)

#### 兑换商品配置

**配置项**:
- ✅ 兑换商品名称 (必填)
- ✅ 兑换商品规格 (如:标准、1人份、大份)
- ✅ 兑换数量 (单次可兑换数量)
- ✅ 兑换价格 (0元/优惠价/市场价)
- ✅ 商品库存 (总库存、单店库存)
- ✅ 商品图片 (商品展示图)

**智能匹配能力**:
- 从菜品库自动匹配商品编码和名称
- 从物品清单匹配库存信息
- 自动关联商品图片资源

#### 兑换条件配置

**条件类型**:
- **消费金额**: 单笔满XX元可兑换
- **消费次数**: 累计消费N次可兑换
- **积分数量**: 使用XX积分兑换
- **会员等级**: 指定会员等级可兑换 (如:金卡会员、钻石会员)
- **时间段**: 特定时间段内可兑换 (如:工作日午餐、周末晚餐)

### 3. 库存与限制管理

#### 库存配置

**配置项**:
- ✅ 总库存数量 (活动总共可兑换次数)
- ✅ 单店库存 (每个门店可兑换次数)
- ✅ 库存预警阈值 (库存低于X时预警)
- ✅ 库存补充策略 (自动补充/手动补充)

**库存分配策略**:
- 平均分配:总库存平均分配到各门店
- 按销量分配:根据历史销量加权分配
- 按需分配:各门店按需申请库存
- 智能预测:根据历史数据预测各门店需求

#### 使用限制

**限制类型**:
- ✅ 领取限制:每人限领X张
- ✅ 使用限制:每人限用X张/每日限用X张
- ✅ 时间限制:券有效期 (领取后N天内有效/固定日期到期)
- ✅ 门店限制:指定门店可用/排除指定门店
- ✅ 商品限制:指定商品可用/排除指定商品
- ✅ 渠道限制:线上/线下/全渠道

### 4. 用户可见性配置

**配置项**:
- ✅ 券面信息:券名称、券描述、券面图片
- ✅ 使用说明:兑换流程、注意事项
- ✅ 展示位置:首页banner、个人中心、商品详情页
- ✅ 推送策略:自动推送/手动领取

## 快速开始

### 基础用法

```python
from scripts.product_exchange_coupon_generator import ProductExchangeCouponGenerator

# 初始化生成器
generator = ProductExchangeCouponGenerator()

# 方式1: 自然语言输入
result = generator.create_from_text(
    text="""
    创建一个新品尝鲜兑换券活动:
    - 活动名称: 冬季新品鸳鸯锅底兑换券
    - 活动时间: 2025-01-10 至 2025-01-31
    - 兑换商品: 鸳鸯锅底 (标准)
    - 兑换条件: 满200元可免费兑换
    - 总库存: 1000份
    - 每人限领: 1张
    - 适用门店: 全部门店
    """,
    project_name="冬季新品推广"  # 项目名称(必填)
)

# 方式2: 结构化数据输入
data = {
    "activity_name": "冬季新品鸳鸯锅底兑换券",
    "activity_time": {
        "start_time": "2025-01-10 00:00:00",
        "end_time": "2025-01-31 23:59:59"
    },
    "exchange_rules": {
        "exchange_type": "满额兑换",
        "condition": {
            "min_amount": 200,
            "exchange_price": 0
        },
        "product": {
            "product_name": "鸳鸯锅底",
            "product_spec": "标准",
            "exchange_quantity": 1
        }
    },
    "inventory": {
        "total_stock": 1000,
        "allocation_strategy": "平均分配"
    },
    "limitations": {
        "receive_limit": 1,
        "use_limit": 1,
        "validity_days": 21
    },
    "applicable_stores": "全部门店"
}
result = generator.create_from_dict(
    data=data,
    project_name="冬季新品推广"
)

# 方式3: 批量创建
batch_data = [
    {
        "activity_name": "鸳鸯锅底兑换券",
        "exchange_product": "鸳鸯锅底",
        "exchange_condition": "满200元"
    },
    {
        "activity_name": "特色小菜兑换券",
        "exchange_product": "招牌毛肚",
        "exchange_condition": "满150元"
    },
    {
        "activity_name": "饮品兑换券",
        "exchange_product": "酸梅汤",
        "exchange_condition": "满100元"
    }
]
results = generator.create_batch(
    batch_data=batch_data,
    project_name="冬季满赠活动"
)
```

### 输出路径规范

所有生成的商品兑换券配置文件按照**标准路径规范**输出:

```
output/[项目名]/product-exchange-coupon/
├── 商品兑换券_鸳鸯锅底_20250103_143000.json
├── 商品兑换券_招牌毛肚_20250103_143001.json
├── 批量商品兑换券_20250103_143002.json
├── plan_商品兑换券生成_20250103_143000.json
├── log_execution_20250103_143000.txt
└── metadata_20250103_143000.json
```

**⚠️ 简化版路径结构**:
- 不再使用 `plans/results/logs/metadata/` 子目录
- 所有文件直接存放在 `output/[项目名]/product-exchange-coupon/` 目录下
- 通过文件名前缀区分类型 (如: `plan_xxx.json`, `商品兑换券_xxx.json`, `log_xxx.txt`)

## 核心工作流程 (三层架构)

### Layer 1: 规范层 (本文档)

**定义内容**:
- ✅ 业务目标: 自动化创建符合美团平台标准的商品兑换券
- ✅ 领域知识: 美团管家后台商品兑换券创建规范和字段说明
- ✅ 工作流程: 5个步骤的标准化流程
- ✅ 质量标准: 字段必填验证、兑换规则合规性、库存配置合理性

### Layer 2: 计划层 (JSON配置)

**执行计划示例**:

```json
{
  "plan_id": "plan_商品兑换券生成_20250103_143000",
  "project_name": "冬季新品推广",
  "skill_name": "product-exchange-coupon",
  "task_type": "single",
  "execution_config": {
    "auto_match_products": true,
    "validate_inventory": true,
    "require_manual_confirm": true
  },
  "tasks": [
    {
      "task_id": "T001",
      "activity_basic_info": {
        "activity_name": "冬季新品鸳鸯锅底兑换券",
        "activity_description": "满200元即可免费兑换新品鸳鸯锅底一份",
        "activity_time": {
          "start_time": "2025-01-10 00:00:00",
          "end_time": "2025-01-31 23:59:59"
        },
        "applicable_stores": {
          "type": "all",
          "store_ids": []
        }
      },
      "exchange_rules": {
        "exchange_type": "满额兑换",
        "condition": {
          "min_amount": 200,
          "exchange_price": 0,
          "currency": "CNY"
        },
        "product": {
          "product_name": "鸳鸯锅底",
          "product_code": "SPU_YUANYANG_001",
          "product_spec": "标准",
          "exchange_quantity": 1,
          "product_image_url": "https://example.com/product.jpg"
        }
      },
      "inventory_config": {
        "total_stock": 1000,
        "allocation_strategy": "平均分配",
        "per_store_stock": 50,
        "low_stock_threshold": 10,
        "replenishment_strategy": "手动补充"
      },
      "usage_limitations": {
        "receive_limit": {
          "enabled": true,
          "limit_per_user": 1
        },
        "use_limit": {
          "enabled": true,
          "limit_per_user": 1,
          "limit_per_day": 1
        },
        "validity": {
          "type": "relative",
          "days_after_receive": 21
        },
        "channel_restriction": {
          "online": true,
          "offline": true
        }
      },
      "visibility_config": {
        "coupon_display": {
          "coupon_name": "新品鸳鸯锅底兑换券",
          "coupon_description": "满200元免费兑换",
          "coupon_image_url": "https://example.com/coupon.jpg"
        },
        "usage_instructions": "1. 消费满200元自动获得兑换资格\n2. 在结算时选择兑换商品\n3. 每人限领限用1张\n4. 有效期21天",
        "display_positions": ["首页banner", "个人中心"],
        "push_strategy": "自动推送"
      }
    }
  ],
  "output_path": "output/冬季新品推广/product-exchange-coupon/商品兑换券_鸳鸯锅底_20250103_143000.json"
}
```

**计划配置文件位置**:
- `output/[项目名]/product-exchange-coupon/plan_*.json`

### Layer 3: 执行层 (Python脚本)

**核心执行引擎**:
- `scripts/product_exchange_coupon_generator.py` - 主生成器
- `scripts/parsers/activity_parser.py` - 活动信息解析
- `scripts/matchers/product_matcher.py` - 商品编码匹配
- `scripts/validators/rule_validator.py` - 兑换规则验证
- `scripts/generators/config_generator.py` - 配置文件生成器

**执行步骤**:

1. **Step 1: 活动信息解析与结构化**
   - 调用 `activity_parser.py` 解析自然语言或结构化数据
   - 提取活动名称、时间、适用门店、兑换商品等信息
   - 标准化数据格式

2. **Step 2: 兑换商品匹配**
   - 调用 `product_matcher.py`
   - 从菜品库匹配商品编码和名称
   - 验证商品是否存在、是否可售
   - 获取商品规格、价格、图片等信息

3. **Step 3: 兑换规则验证**
   - 调用 `rule_validator.py`
   - 验证兑换条件合理性 (如:满额金额、积分数量)
   - 验证库存配置合理性 (总库存、单店库存)
   - 验证使用限制合规性 (领取限制、使用限制)
   - 检查与平台规则的兼容性

4. **Step 4: 库存分配计算**
   - 根据分配策略计算各门店库存
   - 平均分配:总库存 / 门店数量
   - 按销量分配:根据历史数据加权
   - 生成库存分配表

5. **Step 5: 配置文件生成**
   - 调用 `config_generator.py`
   - 生成符合美团平台标准的配置JSON
   - 包含活动基本信息、兑换规则、库存配置、使用限制、可见性配置
   - 保存到标准输出路径

## 创建流程 - 美团管家后台表单字段

### 1. 活动基本信息

| 字段名称 | 必填 | 类型 | 说明 | 示例 |
|---------|------|------|------|------|
| 活动名称 | ✅ | 文本 | 活动的唯一标识名称 | "冬季新品鸳鸯锅底兑换券" |
| 活动说明 | ✅ | 长文本 | 对用户的活动描述 | "满200元即可免费兑换新品鸳鸯锅底一份" |
| 活动开始时间 | ✅ | 日期时间 | 活动开始时间 | "2025-01-10 00:00:00" |
| 活动结束时间 | ✅ | 日期时间 | 活动结束时间 | "2025-01-31 23:59:59" |
| 适用门店 | ✅ | 多选 | 全部门店/指定门店 | "全部门店" 或 ["门店A", "门店B"] |
| 活动状态 | ✅ | 单选 | 启用/停用 | "启用" |

### 2. 兑换规则配置

#### 2.1 兑换类型

| 字段名称 | 必填 | 类型 | 说明 | 可选值 |
|---------|------|------|------|--------|
| 兑换类型 | ✅ | 单选 | 兑换方式 | 直接兑换/满额兑换/积分兑换/消费次数兑换 |

#### 2.2 兑换条件 (根据兑换类型显示不同字段)

**满额兑换**:

| 字段名称 | 必填 | 类型 | 说明 | 示例 |
|---------|------|------|------|------|
| 最低消费金额 | ✅ | 数值 | 满足此金额可兑换 | 200 |
| 兑换价格 | ✅ | 数值 | 0元免费/优惠价 | 0 或 10 |

**积分兑换**:

| 字段名称 | 必填 | 类型 | 说明 | 示例 |
|---------|------|------|------|------|
| 所需积分 | ✅ | 数值 | 兑换所需积分数 | 500 |
| 兑换价格 | ❌ | 数值 | 积分+现金组合 | 10 |

**消费次数兑换**:

| 字段名称 | 必填 | 类型 | 说明 | 示例 |
|---------|------|------|------|------|
| 累计消费次数 | ✅ | 数值 | 满足此次数可兑换 | 5 |
| 统计周期 | ✅ | 单选 | 近7天/近30天/全部 | "近30天" |

#### 2.3 兑换商品配置

| 字段名称 | 必填 | 类型 | 说明 | 示例 |
|---------|------|------|------|------|
| 兑换商品 | ✅ | 下拉选择 | 从菜品库选择 | "鸳鸯锅底" |
| 商品规格 | ✅ | 下拉选择 | 标准/1人份/大份等 | "标准" |
| 兑换数量 | ✅ | 数值 | 单次可兑换数量 | 1 |
| 商品图片 | ❌ | 图片上传 | 券面展示图 | "product.jpg" |

### 3. 库存配置

| 字段名称 | 必填 | 类型 | 说明 | 示例 |
|---------|------|------|------|------|
| 总库存数量 | ✅ | 数值 | 活动总可兑换次数 | 1000 |
| 库存分配策略 | ✅ | 单选 | 平均分配/按销量分配/按需分配 | "平均分配" |
| 单店库存 | ❌ | 数值 | 每个门店可兑换次数 | 50 |
| 库存预警阈值 | ❌ | 数值 | 库存低于此值预警 | 10 |
| 库存补充策略 | ❌ | 单选 | 自动补充/手动补充 | "手动补充" |

### 4. 使用限制

#### 4.1 领取限制

| 字段名称 | 必填 | 类型 | 说明 | 示例 |
|---------|------|------|------|------|
| 是否限制领取 | ✅ | 开关 | 是/否 | "是" |
| 每人限领数量 | ✅* | 数值 | 开启限制时必填 | 1 |

#### 4.2 使用限制

| 字段名称 | 必填 | 类型 | 说明 | 示例 |
|---------|------|------|------|------|
| 是否限制使用 | ✅ | 开关 | 是/否 | "是" |
| 每人限用数量 | ✅* | 数值 | 总共限用次数 | 1 |
| 每日限用数量 | ❌ | 数值 | 每日限用次数 | 1 |

#### 4.3 有效期配置

| 字段名称 | 必填 | 类型 | 说明 | 示例 |
|---------|------|------|------|------|
| 有效期类型 | ✅ | 单选 | 相对时间/固定时间 | "相对时间" |
| 领取后有效天数 | ✅* | 数值 | 相对时间时必填 | 21 |
| 固定到期日期 | ✅* | 日期 | 固定时间时必填 | "2025-01-31" |

#### 4.4 渠道限制

| 字段名称 | 必填 | 类型 | 说明 | 可选值 |
|---------|------|------|------|--------|
| 适用渠道 | ✅ | 多选 | 线上/线下 | ["线上", "线下"] |

### 5. 可见性配置

#### 5.1 券面信息

| 字段名称 | 必填 | 类型 | 说明 | 示例 |
|---------|------|------|------|------|
| 券名称 | ✅ | 文本 | 用户看到的券名称 | "新品鸳鸯锅底兑换券" |
| 券描述 | ✅ | 长文本 | 简短描述 | "满200元免费兑换" |
| 券面图片 | ❌ | 图片上传 | 券面展示图 | "coupon.jpg" |

#### 5.2 使用说明

| 字段名称 | 必填 | 类型 | 说明 | 示例 |
|---------|------|------|------|------|
| 使用说明 | ✅ | 长文本 | 使用流程和注意事项 | "1. 消费满200元自动获得兑换资格\n2. 在结算时选择兑换商品..." |

#### 5.3 展示位置

| 字段名称 | 必填 | 类型 | 说明 | 可选值 |
|---------|------|------|------|--------|
| 展示位置 | ✅ | 多选 | 券的展示位置 | ["首页banner", "个人中心", "商品详情页"] |

#### 5.4 推送策略

| 字段名称 | 必填 | 类型 | 说明 | 可选值 |
|---------|------|------|------|--------|
| 推送方式 | ✅ | 单选 | 自动推送/手动领取 | "自动推送" |
| 推送条件 | ✅* | 多选 | 自动推送时必填 | ["满足消费条件", "会员等级"] |

### 6. 高级配置 (可选)

| 字段名称 | 必填 | 类型 | 说明 | 示例 |
|---------|------|------|------|------|
| 会员等级限制 | ❌ | 多选 | 指定会员等级可用 | ["金卡", "钻石"] |
| 时间段限制 | ❌ | 时间范围 | 特定时间段可用 | "周一至周五 11:00-14:00" |
| 排除商品 | ❌ | 多选 | 不可与哪些商品同时使用 | ["特价商品", "促销套餐"] |
| 优先级 | ❌ | 数值 | 多张券叠加时的优先级 | 1 (数字越小优先级越高) |

## 执行流程图

```
用户输入 (自然语言/结构化数据)
    ↓
[Step 1] 活动信息解析与结构化
    ├─ 提取活动名称、时间、门店
    ├─ 提取兑换规则、兑换商品
    ├─ 提取库存配置、使用限制
    └─ 提取可见性配置
    ↓
[Step 2] 兑换商品匹配
    ├─ 读取菜品库
    ├─ 匹配商品编码和名称
    ├─ 验证商品是否存在、是否可售
    └─ 获取商品规格、价格、图片
    ↓
[Step 3] 兑换规则验证
    ├─ 验证兑换条件合理性
    ├─ 验证库存配置合理性
    ├─ 验证使用限制合规性
    └─ 检查与平台规则的兼容性
    ↓
[Step 4] 库存分配计算
    ├─ 根据分配策略计算各门店库存
    ├─ 平均分配/按销量分配/按需分配
    └─ 生成库存分配表
    ↓
[Step 5] 配置文件生成
    ├─ 生成符合美团平台标准的配置JSON
    ├─ 包含所有必填和可选字段
    ├─ 格式化数据和验证完整性
    └─ 保存到 output/[项目名]/product-exchange-coupon/
    ↓
输出配置文件 + 执行日志 + 元数据
```

## 使用场景

### 场景1: 新品推广兑换券

**需求**: 新上市"麻辣小龙虾",通过兑换券吸引用户尝鲜

**输入**:
```python
generator.create_from_text(
    text="""
    为新品"麻辣小龙虾"创建兑换券:
    - 活动时间: 2025-01-15 至 2025-02-15
    - 兑换条件: 满300元免费兑换
    - 总库存: 500份
    - 每人限领限用: 1张
    - 有效期: 领取后15天内有效
    - 适用门店: 全部门店
    - 展示位置: 首页banner、个人中心
    """,
    project_name="春节新品推广"
)
```

**输出**:
- `output/春节新品推广/product-exchange-coupon/商品兑换券_麻辣小龙虾_YYYYMMDD_HHMMSS.json`

### 场景2: 库存清理兑换活动

**需求**: 清理即将过季的饮品库存

**输入**:
```python
batch_data = [
    {
        "activity_name": "夏日饮品清仓",
        "exchange_product": "冰镇酸梅汤",
        "exchange_condition": "满100元",
        "total_stock": 300
    },
    {
        "activity_name": "夏日饮品清仓",
        "exchange_product": "冰糖雪梨",
        "exchange_condition": "满100元",
        "total_stock": 200
    }
]

generator.create_batch(
    batch_data=batch_data,
    project_name="夏季库存清理"
)
```

**输出**:
- `output/夏季库存清理/product-exchange-coupon/批量商品兑换券_YYYYMMDD_HHMMSS.json`

### 场景3: 会员专属兑换福利

**需求**: 为金卡会员提供专属兑换权益

**输入**:
```python
data = {
    "activity_name": "金卡会员专属兑换",
    "exchange_product": "招牌毛肚",
    "exchange_type": "直接兑换",
    "exchange_price": 0,
    "total_stock": 1000,
    "member_level_restriction": ["金卡", "钻石"],
    "receive_limit": 1,
    "use_limit": 1,
    "validity_days": 30
}

generator.create_from_dict(
    data=data,
    project_name="会员权益升级"
)
```

**输出**:
- `output/会员权益升级/product-exchange-coupon/商品兑换券_招牌毛肚_YYYYMMDD_HHMMSS.json`

### 场景4: 满赠活动兑换券

**需求**: 周末满赠活动,满500元送小吃兑换券

**输入**:
```python
data = {
    "activity_name": "周末满500送小吃",
    "activity_time": {
        "start_time": "2025-01-18 00:00:00",
        "end_time": "2025-01-19 23:59:59"
    },
    "exchange_type": "满额兑换",
    "min_amount": 500,
    "exchange_product": "特色小吃拼盘",
    "exchange_price": 0,
    "total_stock": 200,
    "time_restriction": "周六周日全天"
}

generator.create_from_dict(
    data=data,
    project_name="周末满赠活动"
)
```

**输出**:
- `output/周末满赠活动/product-exchange-coupon/商品兑换券_特色小吃拼盘_YYYYMMDD_HHMMSS.json`

## 高级特性

### 1. 智能商品匹配

**问题**: 用户输入商品名称可能与菜品库不完全一致

**解决方案**:
- 使用模糊匹配算法
- 相似度 ≥ 80%: 自动匹配
- 相似度 < 80%: 提供候选列表供人工确认

```python
from scripts.matchers.product_matcher import ProductMatcher

matcher = ProductMatcher()
result = matcher.match("鸳鸯火锅底")
# result = {"product_code": "SPU_YUANYANG_001", "product_name": "鸳鸯锅底", "similarity": 0.9}
```

### 2. 库存智能分配

**问题**: 如何合理分配库存到各门店

**解决方案**:
- **平均分配**: 简单快速,适合新品推广
- **按销量分配**: 根据历史数据加权,适合成熟商品
- **智能预测**: 基于机器学习预测各门店需求

```python
from scripts.allocators.inventory_allocator import InventoryAllocator

allocator = InventoryAllocator(strategy="按销量分配")
allocation = allocator.allocate(
    total_stock=1000,
    stores=["门店A", "门店B", "门店C"],
    historical_sales={
        "门店A": 500,
        "门店B": 300,
        "门店C": 200
    }
)
# allocation = {"门店A": 500, "门店B": 300, "门店C": 200}
```

### 3. 兑换规则验证

**问题**: 用户配置的兑换规则可能不合理

**解决方案**:
- 自动验证兑换条件合理性
- 检查与平台规则的兼容性
- 提供优化建议

```python
from scripts.validators.rule_validator import RuleValidator

validator = RuleValidator()
validation_result = validator.validate({
    "exchange_type": "满额兑换",
    "min_amount": 50,  # 金额过低
    "exchange_price": 0,
    "total_stock": 10000  # 库存过高
})

if validation_result["warnings"]:
    print("警告:")
    for warning in validation_result["warnings"]:
        print(f"- {warning}")
# 警告:
# - 最低消费金额50元过低,建议设置为100元以上
# - 总库存10000份过高,建议根据历史数据合理设置
```

### 4. 批量处理进度追踪

**问题**: 批量创建多个兑换券时,需要实时查看进度

**解决方案**:
- 使用 `TodoWrite` 工具实时更新任务列表
- 日志文件记录每个任务的执行状态

```python
results = generator.create_batch(batch_data, project_name="批量兑换券")
# 查看日志: output/批量兑换券/product-exchange-coupon/log_*.txt
```

## 质量保障

### 必填字段验证

**验证规则**:
```python
REQUIRED_FIELDS = {
    "activity_basic_info": ["activity_name", "activity_time", "applicable_stores"],
    "exchange_rules": ["exchange_type", "product"],
    "inventory_config": ["total_stock"],
    "usage_limitations": ["receive_limit", "use_limit", "validity"],
    "visibility_config": ["coupon_display", "usage_instructions"]
}
```

### 兑换规则合规性

**验证项**:
- ✅ 兑换条件合理性 (如:满额金额不低于商品价值)
- ✅ 库存配置合理性 (总库存 ≥ 单店库存 × 门店数)
- ✅ 使用限制合规性 (领取限制 ≤ 使用限制)
- ✅ 时间配置一致性 (活动结束时间 ≥ 券有效期)

### 库存配置合理性

**验证项**:
- ✅ 总库存 > 0
- ✅ 单店库存 × 门店数 ≤ 总库存
- ✅ 库存预警阈值 < 单店库存
- ✅ 库存分配策略与实际情况匹配

## 依赖资源

### 数据源文件

1. **菜品库**:
   - `plugins/美团组/templates/吼巷_菜品库_总部.xlsx`
   - `plugins/美团组/templates/吼巷_菜品库_总部_做法及加料.xlsx`

2. **门店清单**:
   - `plugins/美团组/templates/门店清单.xlsx`

3. **会员等级配置**:
   - `plugins/美团组/templates/会员等级配置.json`

### 技能包依赖

- **营销中心/优惠券基础**: 优惠券通用能力
  - 位置: `plugins/美团组/skills/营销中心/workflows/优惠券/`
  - 功能: 优惠券基础配置、验证、生成

### Python库依赖

```
pandas >= 2.0.0
Levenshtein >= 0.21.0  # 字符串相似度计算
jsonschema >= 4.17.0   # JSON schema验证
```

## 注意事项

### 1. 商品库存同步

**问题**: 兑换商品的实际库存可能与系统不同步

**建议**:
- 创建兑换券前检查商品实际库存
- 设置合理的库存预警阈值
- 定期同步商品库存数据

### 2. 兑换条件合理性

**问题**: 兑换条件设置不合理可能影响活动效果

**建议**:
- 满额金额应高于商品价值的2-3倍
- 积分兑换数量应与商品价值匹配
- 消费次数应考虑用户消费频率

### 3. 库存分配策略

**问题**: 库存分配不当可能导致部分门店库存过剩或不足

**建议**:
- 新品推广使用平均分配
- 成熟商品使用按销量分配
- 高价值商品使用智能预测

### 4. 多券叠加规则

**问题**: 多张兑换券叠加可能影响利润

**建议**:
- 设置兑换券优先级
- 配置排除商品规则
- 限制单笔订单使用兑换券数量

### 5. 用户体验优化

**问题**: 兑换流程复杂可能影响用户使用意愿

**建议**:
- 简化兑换流程 (如:满足条件自动推送)
- 清晰的使用说明
- 显眼的展示位置
- 及时的库存提醒

## 相关文档

- [三层架构规范](~/.claude/CLAUDE.md#5-复杂系统三层架构规范)
- [输出路径规范](~/.claude/CLAUDE.md#45-输出路径规范)
- [优惠券基础配置](../README.md)
- [美团管家后台操作指南](plugins/美团组/docs/美团管家操作手册.md)

## 版本历史

- **v1.0.0** (2025-01-03): 初始版本
  - 支持单个和批量商品兑换券创建
  - 智能商品匹配和库存分配
  - 标准化JSON输出
  - 集成三层架构模式
