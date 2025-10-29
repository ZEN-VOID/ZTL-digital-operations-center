# 美团管家营销中心 - 快速索引

> 快速定位营销中心功能模块、常用操作和关键数据实体

---

## 📑 功能模块快速导航

### 1️⃣ 首页 (menucode_928)
- **URL**: `#/rms-discount/marketing`
- **功能**: 营销数据概览、快捷功能入口、活动效果展示
- **常用操作**: 查看营销数据、快速创建活动

---

### 2️⃣ 渠道管理 (menucode_2227)

| 功能 | URL | 用途 |
|-----|-----|------|
| 渠道列表 | `#/marketing/channel/list` | 查看和管理所有营销渠道 |
| 渠道配置 | `#/marketing/channel/config` | 配置渠道参数和规则 |
| 渠道效果 | `#/marketing/channel/effect` | 查看各渠道营销效果数据 |

**关键实体**: Channel (渠道名称、渠道类型、流量配置、转化率、ROI)

---

### 3️⃣ 用户管理 (menucode_2220)

| 功能 | URL | 用途 |
|-----|-----|------|
| 会员列表 | `#/marketing/member/list` | 会员信息查询和管理 |
| 会员等级 | `#/marketing/member/level` | 会员等级体系设置 |
| 积分管理 | `#/marketing/member/points` | 积分规则和积分明细 |
| 会员权益 | `#/marketing/member/rights` | 会员专属权益配置 |
| 会员标签 | `#/marketing/member/tags` | 用户画像和标签管理 |

**关键实体**: Member (会员ID、手机号、等级、积分、储值余额、消费金额、标签)

**常用操作**:
- 新增会员 → 会员列表 → 点击"新增会员"按钮
- 配置等级体系 → 会员等级 → 设置升级条件和权益
- 管理积分规则 → 积分管理 → 配置积分获取和消耗规则

---

### 4️⃣ 卡券管理 (menucode_2221)

| 功能 | URL | 用途 |
|-----|-----|------|
| 卡券列表 | `#/marketing/coupon/list` | 查看所有卡券和使用情况 |
| 创建卡券 | `#/marketing/coupon/create` | 创建优惠券、代金券、折扣券 |
| 卡券核销 | `#/marketing/coupon/verify` | 卡券核销记录和统计 |
| 卡券模板 | `#/marketing/coupon/template` | 卡券模板管理 |
| 发放记录 | `#/marketing/coupon/grant` | 卡券发放历史和明细 |
| 使用规则 | `#/marketing/coupon/rules` | 卡券使用条件和限制 |

**关键实体**: Coupon (券名称、券类型、面额、使用门槛、有效期、发行量、核销状态)

**常用操作**:
- 创建优惠券 → 创建卡券 → 填写券信息 → 发布
- 查看核销情况 → 卡券核销 → 筛选时间范围
- 批量发放 → 卡券列表 → 选择卡券 → 发放

---

### 5️⃣ 大促活动 (menucode_2222)

| 功能 | URL | 用途 |
|-----|-----|------|
| 活动列表 | `#/marketing/campaign/list` | 查看所有营销活动 |
| 创建活动 | `#/marketing/campaign/create` | 新建营销活动 |
| 活动数据 | `#/marketing/campaign/data` | 活动效果数据分析 |
| 满减活动 | `#/marketing/campaign/discount` | 满减促销活动配置 |
| 限时折扣 | `#/marketing/campaign/flash` | 限时折扣活动设置 |

**关键实体**: Campaign (活动名称、活动类型、优惠规则、活动周期、预算、目标人群)

**关键指标**: 参与人数、活动GMV、客单价提升、ROI

**常用操作**:
- 创建满减活动 → 创建活动 → 选择"满减" → 配置阶梯规则
- 查看活动效果 → 活动数据 → 选择活动 → 查看转化数据

---

### 6️⃣ 储值管理 (menucode_3071)

| 功能 | URL | 用途 |
|-----|-----|------|
| 储值卡列表 | `#/marketing/prepaid/list` | 储值卡查询和管理 |
| 储值规则 | `#/marketing/prepaid/rules` | 储值赠送规则设置 |
| 充值记录 | `#/marketing/prepaid/recharge` | 会员充值历史记录 |
| 消费记录 | `#/marketing/prepaid/consumption` | 储值卡消费明细 |

**关键实体**: PrepaidCard (卡号、会员ID、余额、充值总额、消费总额、状态)

---

### 7️⃣ 评价管理 (menucode_1407)

| 功能 | URL | 用途 |
|-----|-----|------|
| 评价列表 | `#/marketing/review/list` | 查看所有用户评价 |
| 评价回复 | `#/marketing/review/reply` | 商家回复管理 |
| 评价统计 | `#/marketing/review/stats` | 评价数据分析 |
| 激励设置 | `#/marketing/review/incentive` | 评价激励机制配置 |

**关键实体**: Review (订单号、会员ID、评分、评价内容、回复内容、时间)

---

### 8️⃣ 群发短信 (menucode_438)

| 功能 | URL | 用途 |
|-----|-----|------|
| 短信列表 | `#/marketing/sms/list` | 查看短信发送记录 |
| 发送短信 | `#/marketing/sms/send` | 创建短信营销任务 |
| 短信模板 | `#/marketing/sms/template` | 短信模板管理 |
| 发送统计 | `#/marketing/sms/stats` | 短信发送效果分析 |

**关键实体**: SMS (任务ID、模板ID、目标人群、发送数量、成功数、失败数、发送时间)

---

### 9️⃣ 团购管理 (menucode_1564)

| 功能 | URL | 用途 |
|-----|-----|------|
| 团购列表 | `#/marketing/group/list` | 查看团购活动 |
| 创建团购 | `#/marketing/group/create` | 新建团购活动 |
| 订单管理 | `#/marketing/group/orders` | 团购订单查询 |
| 核销管理 | `#/marketing/group/verify` | 团购券核销 |

**关键实体**: GroupBuy (团购ID、活动名称、商品、团购价、原价、库存、已售)

---

### 🔟 数据报表 (menucode_2226)

| 功能 | URL | 用途 |
|-----|-----|------|
| 营销概览 | `#/marketing/report/overview` | 营销数据总览 |
| 会员分析 | `#/marketing/report/member` | 会员增长和活跃度分析 |
| 卡券分析 | `#/marketing/report/coupon` | 卡券使用效果分析 |
| 活动分析 | `#/marketing/report/campaign` | 活动ROI和转化分析 |
| 渠道分析 | `#/marketing/report/channel` | 各渠道营销效果对比 |

**关键指标**: 会员增长率、活动转化率、卡券核销率、营销ROI

---

### 1️⃣1️⃣ 优惠同享管理 (menucode_2286)

| 功能 | URL | 用途 |
|-----|-----|------|
| 同享活动 | `#/marketing/share/list` | 优惠同享活动列表 |
| 创建活动 | `#/marketing/share/create` | 新建同享活动 |
| 分享记录 | `#/marketing/share/records` | 用户分享行为记录 |
| 裂变数据 | `#/marketing/share/stats` | 裂变效果数据分析 |

**关键实体**: ShareCampaign (活动ID、分享奖励、被分享奖励、分享次数、转化人数)

---

### 1️⃣2️⃣ 素材管理 (menucode_2956)

| 功能 | URL | 用途 |
|-----|-----|------|
| 图片素材 | `#/marketing/material/image` | 营销图片库 |
| 文案模板 | `#/marketing/material/text` | 营销文案模板库 |
| 海报模板 | `#/marketing/material/poster` | 营销海报模板 |
| 素材分类 | `#/marketing/material/category` | 素材分类管理 |

**关键实体**: Material (素材ID、名称、类型、分类、URL、创建时间)

---

## 🔥 高频营销场景快速指南

### 场景1: 新会员注册送券

```
步骤:
1. 创建优惠券 → 卡券管理 > 创建卡券
2. 设置发放规则 → 卡券管理 > 使用规则 → 新用户注册自动发放
3. 监控发放情况 → 卡券管理 > 发放记录
```

### 场景2: 会员日大促活动

```
步骤:
1. 创建活动 → 大促活动 > 创建活动
2. 设置目标人群 → 选择会员等级或标签
3. 配置优惠规则 → 满减阶梯或折扣
4. 发送通知 → 群发短信 > 发送短信
5. 监控效果 → 大促活动 > 活动数据
```

### 场景3: 储值卡充值送活动

```
步骤:
1. 配置储值规则 → 储值管理 > 储值规则
2. 设置充值阶梯 → 充100送20、充300送80等
3. 推广活动 → 群发短信 + 优惠同享
4. 查看充值情况 → 储值管理 > 充值记录
```

### 场景4: 老客户召回活动

```
步骤:
1. 筛选目标用户 → 用户管理 > 会员列表 → 按"最后消费时间"筛选
2. 打标签 → 用户管理 > 会员标签 → 创建"沉睡用户"标签
3. 创建专属券 → 卡券管理 > 创建卡券 → 针对标签发放
4. 发送召回短信 → 群发短信 > 发送短信 → 选择标签人群
5. 监控回流效果 → 数据报表 > 会员分析
```

---

## 📋 关键数据实体速查

### Member (会员实体)

```typescript
interface Member {
  member_id: string;          // 会员ID（主键）
  phone: string;              // 手机号（唯一索引）
  name: string;               // 会员姓名
  level_id: string;           // 会员等级ID（外键）
  points: number;             // 当前积分
  balance: number;            // 储值余额
  total_consumption: number;  // 累计消费
  order_count: number;        // 订单总数
  tags: string[];             // 会员标签
  status: 'active' | 'inactive' | 'blacklist';
  created_at: Date;
  updated_at: Date;
}
```

### Coupon (卡券实体)

```typescript
interface Coupon {
  coupon_id: string;
  coupon_name: string;
  coupon_type: 'voucher' | 'discount' | 'exchange';
  face_value: number;         // 面额
  min_amount?: number;        // 使用门槛
  valid_start: Date;
  valid_end: Date;
  total_quantity: number;     // 发行总量
  issued_quantity: number;    // 已发放数量
  used_quantity: number;      // 已使用数量
  status: 'draft' | 'active' | 'paused' | 'expired';
  campaign_id?: string;
  created_by: string;
  created_at: Date;
  updated_at: Date;
}
```

### Campaign (营销活动实体)

```typescript
interface Campaign {
  campaign_id: string;
  campaign_name: string;
  campaign_type: 'discount' | 'giveaway' | 'lottery' | 'combo';
  start_time: Date;
  end_time: Date;
  target_audience: 'all' | 'level' | 'tag';
  discount_rule: JSON;        // 优惠规则配置
  budget: number;
  daily_limit: number;
  status: 'draft' | 'active' | 'paused' | 'completed';
  created_by: string;
  created_at: Date;
}
```

---

## 🎯 常用CSS选择器速查

```css
/* 一级菜单选择器 */
#menucode_928   /* 首页 */
#menucode_2227  /* 渠道 */
#menucode_2220  /* 用户 */
#menucode_2221  /* 卡券 */
#menucode_2222  /* 大促活动 */
#menucode_3071  /* 储值管理 */
#menucode_1407  /* 评价管理 */
#menucode_438   /* 群发短信 */
#menucode_1564  /* 团购管理 */
#menucode_2226  /* 数据报表 */
#menucode_2286  /* 优惠同享 */
#menucode_2956  /* 素材管理 */

/* 辅助功能选择器 */
input[placeholder='请输入想搜索的功能']  /* 全局搜索 */
#marketing-navigator                    /* 营销中心导航 */
```

---

## 📄 相关文档

- **完整导航结构**: `navigation-tree.json`
- **详细知识库**: `knowledge-base-report.md`
- **技能包主文件**: `../SKILL.md`

---

**更新时间**: 2025-10-23
**适用智能体**: M2-美团管家营销管理员、M4-美团管家网页自动化操作助手
