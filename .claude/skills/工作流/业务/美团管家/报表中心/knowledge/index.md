# 美团管家报表中心 - 快速索引

> 快速定位报表中心功能模块、常用操作和关键数据实体

---

## 📑 功能模块快速导航

### 1️⃣ 报表首页 (report-home)
- **URL**: `#/rms-report/home`
- **功能**: 报表中心总览、核心经营指标、快捷报表入口
- **常用操作**: 查看实时数据、快速访问高频报表

---

### 2️⃣ 经营分析 (operating-analysis)

| 功能 | URL | 用途 |
|-----|-----|---------|
| 日报表 | `#/rms-report/operating-analysis/daily` | 每日经营数据汇总 |
| 月报表 | `#/rms-report/operating-analysis/monthly` | 月度经营数据分析 |
| 趋势分析 | `#/rms-report/operating-analysis/trend` | 时间序列数据趋势 |
| 同行对比 | `#/rms-report/operating-analysis/peer` | 与同商圈/品类对比 |

**关键指标**: 营业额、订单量、客单价、毛利率、同比环比

**数据实体**: Order (订单ID、金额、时间、渠道、支付方式)

---

### 3️⃣ 财务报表 (financial-report)

| 功能 | URL | 用途 |
|-----|-----|---------|
| 收入报表 | `#/rms-report/financial/revenue` | 营业收入明细、支付方式占比 |
| 成本报表 | `#/rms-report/financial/cost` | 原材料、人工、其他成本 |
| 利润报表 | `#/rms-report/financial/profit` | 毛利、净利润分析 |
| 资金流水 | `#/rms-report/financial/cashflow` | 现金流入流出记录 |

**关键指标**: 营业收入、食材成本率、人工成本率、毛利、净利润

**行业基准**:
- 食材成本率: 30%-40%
- 人工成本率: 18%-25%
- 房租成本率: 8%-15%
- 综合成本率: 65%-75%

**常用操作**:
- 生成财务月报 → 财务报表 → 选择时间范围 → 导出Excel
- 成本分析 → 成本报表 → 查看各项成本占比 → 对标行业基准

---

### 4️⃣ 销售报表 (sales-report)

| 功能 | URL | 用途 |
|-----|-----|---------|
| 菜品销售 | `#/rms-report/sales/dish` | 单品销量、销售额排行 |
| 品类销售 | `#/rms-report/sales/category` | 菜品分类销售统计 |
| 时段分析 | `#/rms-report/sales/time-slot` | 不同时段营业数据 |
| 渠道分析 | `#/rms-report/sales/channel` | 堂食、外卖、自提占比 |

**关键指标**: 销量排行、销售额、销售占比、增长率

**数据实体**:
```json
{
  "dish_id": "D001",
  "dish_name": "招牌毛血旺",
  "sales_volume": 856,
  "sales_revenue": 42800.00,
  "avg_price": 50.00,
  "cost": 15.00,
  "gross_margin": 35.00,
  "margin_rate": 70.00%
}
```

**常用操作**:
- 查看畅销菜品 → 菜品销售 → 按销量排序 → Top 10
- 分析时段客流 → 时段分析 → 查看早中晚时段数据

---

### 5️⃣ 库存报表 (inventory-report)

| 功能 | URL | 用途 |
|-----|-----|---------|
| 库存现状 | `#/rms-report/inventory/status` | 当前库存量、库存金额 |
| 出入库记录 | `#/rms-report/inventory/inout` | 采购入库、销售出库明细 |
| 库存预警 | `#/rms-report/inventory/warning` | 低库存、积压库存告警 |
| 损耗报表 | `#/rms-report/inventory/loss` | 原材料损耗、报废统计 |

**关键指标**: 库存量、库存金额、周转率、损耗率

**行业基准**:
- 正常损耗率: 3%-5%
- 库存周转天数: 7-10天

**常用操作**:
- 查看库存预警 → 库存预警 → 处理低库存/积压
- 分析损耗原因 → 损耗报表 → 查看损耗明细 → 制定改进措施

---

### 6️⃣ 会员分析 (member-report)

| 功能 | URL | 用途 |
|-----|-----|---------|
| 会员增长 | `#/rms-report/member/growth` | 新增会员、活跃会员趋势 |
| 会员消费 | `#/rms-report/member/consumption` | 会员消费金额、频次分析 |
| 会员画像 | `#/rms-report/member/portrait` | 年龄、性别、地域分布 |
| RFM分析 | `#/rms-report/member/rfm` | 最近消费、消费频率、消费金额 |

**RFM阈值标准**:
- **重要价值客户**: R≥60天, F≥8次, M≥500元
- **重要挽留客户**: R<60天, F≥5次, M≥300元

**常用操作**:
- 识别流失会员 → RFM分析 → 导出"重要挽留客户"名单
- 设计会员活动 → 会员画像 → 了解会员特征 → 精准营销

---

### 7️⃣ 营销报表 (marketing-report)

| 功能 | URL | 用途 |
|-----|-----|---------|
| 活动效果 | `#/rms-report/marketing/campaign` | 营销活动数据汇总 |
| 优惠券分析 | `#/rms-report/marketing/coupon` | 券发放、核销、成本分析 |
| 折扣分析 | `#/rms-report/marketing/discount` | 折扣使用情况统计 |
| 营销ROI | `#/rms-report/marketing/roi` | 营销投入产出比分析 |

**关键指标**: 参与人数、活动GMV、优惠券核销率、ROI

**常用操作**:
- 评估活动效果 → 活动效果 → 查看参与人数、GMV → 计算ROI
- 优惠券复盘 → 优惠券分析 → 查看核销率 → 优化发放策略

---

### 8️⃣ 商圈选址 (location-analysis)

| 功能 | URL | 用途 |
|-----|-----|---------|
| 商圈分析 | `#/rms-report/location/trade-area` | 商圈人口、消费力、竞争态势 |
| 客流分析 | `#/rms-report/location/customer-flow` | 进店客流、转化率分析 |
| 竞品对比 | `#/rms-report/location/competitor` | 与竞争对手的对比分析 |

**关键指标**: 人口密度、消费水平、竞品数量、客流量

**常用操作**:
- 新店选址 → 商圈分析 → 评估商圈潜力
- 竞品研究 → 竞品对比 → 分析竞争优势

---

### 9️⃣ 员工报表 (employee-report)

| 功能 | URL | 用途 |
|-----|-----|---------|
| 员工绩效 | `#/rms-report/employee/performance` | 销售业绩、服务评分 |
| 考勤报表 | `#/rms-report/employee/attendance` | 出勤、请假、加班统计 |
| 人效分析 | `#/rms-report/employee/labor-efficiency` | 人均产值、人工成本占比 |

**关键指标**: 人均产值、人工成本率、出勤率

**常用操作**:
- 绩效考核 → 员工绩效 → 查看销售业绩排名
- 人效优化 → 人效分析 → 分析人均产值 → 优化排班

---

### 🔟 自定义报表 (custom-report)
- **URL**: `#/rms-report/custom`
- **功能**: 用户自定义报表配置和生成
- **特性**: 报表模板库、自定义字段选择、自定义时间维度、报表保存和分享

---

## 🔥 高频分析场景快速指南

### 场景1: 经营数据异常诊断

```
步骤:
1. 查看日报表 → 经营分析 > 日报表
2. 识别异常指标（营业额下降/成本上升）
3. 分析具体原因:
   - 营业额 ↓ → 销售报表 > 查看菜品销量
   - 成本 ↑ → 财务报表 > 查看成本明细
   - 会员 ↓ → 会员分析 > 查看流失情况
4. 制定改进措施并跟踪效果
```

### 场景2: 新品定价策略分析

```
步骤:
1. 成本核算 → 财务报表 > 成本报表 → 计算食材+人工成本
2. 市场调研 → 商圈选址 > 竞品对比 → 了解同类产品定价
3. 销售预测 → 销售报表 > 品类销售 → 参考同品类销量
4. 定价测试 → 设置价格 → 跟踪销售数据
5. 优化调整 → 根据销售反馈调整定价
```

### 场景3: 库存预警与补货决策

```
步骤:
1. 查看预警 → 库存报表 > 库存预警
2. 分析原因:
   - 低库存 → 出入库记录 → 查看消耗速度
   - 积压 → 销售报表 → 查看销售趋势
3. 制定策略:
   - 低库存 → 立即补货
   - 积压 → 促销/停进货
4. 执行操作 → 通知采购/发起促销
5. 持续监控 → 定期查看库存状态
```

### 场景4: 会员营销活动设计

```
步骤:
1. 会员分析 → 会员分析 > RFM分析
2. 筛选目标客户:
   - 重要挽留客户（R低、F低、M高）
   - 一般发展客户（R中、F中、M中）
3. 设计营销方案:
   - 专属折扣券
   - 生日特惠
   - 积分翻倍
4. 执行活动 → 通过短信/飞书推送
5. 效果评估 → 营销报表 > 活动效果
```

---

## 📋 关键数据实体速查

### Order (订单实体)

```typescript
interface Order {
  order_id: string;              // 订单ID（主键）
  order_time: Date;              // 下单时间
  store_id: string;              // 门店ID
  channel: 'dine-in' | 'takeout' | 'pickup';  // 渠道
  order_amount: number;          // 订单金额
  discount_amount: number;       // 优惠金额
  actual_amount: number;         // 实收金额
  payment_method: string;        // 支付方式
  member_id?: string;            // 会员ID
  status: 'pending' | 'completed' | 'cancelled';
  items: OrderItem[];            // 订单明细
}
```

### Revenue (收入实体)

```typescript
interface Revenue {
  revenue_id: string;
  date: Date;
  store_id: string;
  total_revenue: number;         // 总收入
  dine_in_revenue: number;       // 堂食收入
  takeout_revenue: number;       // 外卖收入
  payment_breakdown: {           // 支付方式分解
    cash: number;
    wechat: number;
    alipay: number;
    card: number;
  };
  order_count: number;           // 订单数
  avg_order_value: number;       // 客单价
}
```

### Cost (成本实体)

```typescript
interface Cost {
  cost_id: string;
  date: Date;
  store_id: string;
  material_cost: number;         // 食材成本
  labor_cost: number;            // 人工成本
  rent_cost: number;             // 房租成本
  utility_cost: number;          // 水电费
  other_cost: number;            // 其他成本
  total_cost: number;            // 总成本
  cost_rate: number;             // 成本率（成本/收入）
}
```

### Member (会员实体)

```typescript
interface Member {
  member_id: string;             // 会员ID
  phone: string;                 // 手机号
  name: string;                  // 姓名
  level: string;                 // 会员等级
  points: number;                // 积分
  balance: number;               // 储值余额
  total_consumption: number;     // 累计消费
  order_count: number;           // 订单数
  last_order_time: Date;         // 最后消费时间
  rfm: {                         // RFM值
    R: number;                   // 最近消费（天数）
    F: number;                   // 消费频次
    M: number;                   // 消费金额
  };
  tags: string[];                // 会员标签
}
```

### Inventory (库存实体)

```typescript
interface Inventory {
  material_id: string;           // 物料ID
  material_name: string;         // 物料名称
  category: string;              // 分类
  unit: string;                  // 单位
  current_stock: number;         // 当前库存
  stock_value: number;           // 库存金额
  min_stock: number;             // 最低库存
  max_stock: number;             // 最高库存
  turnover_days: number;         // 周转天数
  loss_rate: number;             // 损耗率
  last_purchase_date: Date;      // 最后采购日期
  status: 'normal' | 'low' | 'overstock';  // 库存状态
}
```

---

## 🎯 常用CSS选择器速查

```css
/* 核心导航模块选择器 */
#report-home            /* 报表首页 */
#operating-analysis     /* 经营分析 */
#financial-report       /* 财务报表 */
#sales-report           /* 销售报表 */
#inventory-report       /* 库存报表 */
#member-report          /* 会员分析 */
#marketing-report       /* 营销报表 */
#location-analysis      /* 商圈选址 */
#employee-report        /* 员工报表 */
#custom-report          /* 自定义报表 */

/* 辅助功能选择器 */
.time-filter            /* 时间筛选器 */
.store-filter           /* 门店筛选器 */
.channel-filter         /* 渠道筛选器 */
.export-button          /* 导出按钮 */
```

---

## 📄 相关文档

- **完整导航结构**: `navigation-tree.json`
- **详细知识库**: `knowledge-base-report.md`
- **技能包主文件**: `../SKILL.md`

---

**更新时间**: 2025-10-23
**适用智能体**: M3-美团管家报表管理员、M4-美团管家网页自动化操作助手
