# 美团管家运营中心 - 快速索引

> 快速查找功能入口、常用操作和关键数据实体

---

## 🚀 按模块快速导航

### 模块1: 首页 (menucode_927)
**路由**: `#/`
**功能**:
- 常用功能快捷入口
- 经营推荐卡片
- App下载引导

---

### 模块2: 餐厅管理 (menucode_347)
**选择器**: `#menucode_347`

| 子功能 | 路由 | 关键字段 |
|--------|------|---------|
| 餐厅信息 | `#/restaurant/info` | 门店名称、地址、营业时间 |
| 桌台管理 | `#/restaurant/table` | 桌台号、区域、容纳人数 |
| 打印设置 | `#/restaurant/printer` | 打印机IP、打印类型 |
| 支付配置 | `#/restaurant/payment` | 支付方式、商户号 |
| 设备管理 | `#/restaurant/device` | 设备类型、设备状态 |

**常用操作**:
- ✅ 配置门店基本信息
- ✅ 添加桌台并设置二维码
- ✅ 配置小票打印机和厨房打印机
- ✅ 开通聚合支付

---

### 模块3: 菜品管理 (menucode_119)
**选择器**: `#menucode_119`

| 子功能 | 路由 | 关键字段 |
|--------|------|---------|
| 菜品库 | `#/dish/list` | 菜品名称、分类、价格、图片 |
| 菜品分类 | `#/dish/category` | 分类名称、排序、图标 |
| 菜品规格 | `#/dish/spec` | 规格名称、规格选项 |
| 价格管理 | `#/dish/price` | 堂食价、外卖价、会员价 |
| 菜品组合 | `#/dish/combo` | 套餐名称、组合菜品、优惠 |
| 菜品部门 | `#/dish/department` | 部门名称、出品顺序 |

**常用操作**:
- ✅ 批量导入菜品
- ✅ 设置多规格 (大/中/小杯)
- ✅ 配置不同价格体系
- ✅ 创建套餐组合

---

### 模块4: 手机点餐 (menucode_1571)
**选择器**: `#menucode_1571`

| 子功能 | 路由 | 关键字段 |
|--------|------|---------|
| 小程序设置 | `#/mobile-order/settings` | 界面配置、轮播图、底部导航 |
| 菜品上架 | `#/mobile-order/dish` | 菜品同步、上架状态 |
| 订单管理 | `#/mobile-order/orders` | 订单列表、订单状态 |
| 桌台绑定 | `#/mobile-order/table` | 二维码生成、桌台关联 |

**常用操作**:
- ✅ 配置小程序界面
- ✅ 同步菜品到小程序
- ✅ 生成桌台点餐二维码

---

### 模块5: 二维码管理 (menucode_1816)
**选择器**: `#menucode_1816`

| 子功能 | 路由 | 关键字段 |
|--------|------|---------|
| 桌台二维码 | `#/qrcode/table` | 桌台号、二维码类型 |
| 收款二维码 | `#/qrcode/payment` | 支付方式、收款码 |
| 二维码打印 | `#/qrcode/print` | 打印模板、打印数量 |
| 扫码记录 | `#/qrcode/log` | 扫码时间、扫码用户 |

**常用操作**:
- ✅ 批量生成桌台点餐码
- ✅ 生成美团/微信/支付宝收款码
- ✅ 打印二维码标签

---

### 模块6: 外卖管理 (menucode_164)
**选择器**: `#menucode_164`

| 子功能 | 路由 | 关键字段 |
|--------|------|---------|
| 外卖订单 | `#/takeout/orders` | 订单号、配送地址、订单状态 |
| 菜品同步 | `#/takeout/dish-sync` | 同步规则、价格策略 |
| 营业设置 | `#/takeout/business` | 营业时间、配送范围 |
| 外卖活动 | `#/takeout/activity` | 活动类型、优惠规则 |

**常用操作**:
- ✅ 接收美团/饿了么订单
- ✅ 同步堂食菜品到外卖平台
- ✅ 设置外卖营业时间
- ✅ 配置满减活动

---

### 模块7: 财务管理 (menucode_157)
**选择器**: `#menucode_157`

| 子功能 | 路由 | 关键字段 |
|--------|------|---------|
| 支付明细 | `#/finance/payment-detail` | 交易流水号、支付方式、支付金额 |
| 支付结算 | `#/finance/settlement` | 结算日期、结算金额、结算状态 |
| 营业概览 | `#/finance/overview` | 营业额、营业收入、营业天数 |
| 菜品销售统计 | `#/finance/dish-sales` | 菜品名称、销量、收入、优惠 |
| 综合营业统计 | `#/finance/comprehensive` | 日期、营业额、优惠金额、收入 |
| 对账管理 | `#/finance/reconciliation` | 对账状态、异常订单 |

**关键指标**:
- 月度营业额: ¥87,217.21
- 月度营业天数: 23天
- 月度异常订单: 0笔

**常用操作**:
- ✅ 查询每日营业额
- ✅ 查看支付结算明细
- ✅ 导出财务报表
- ✅ 处理对账异常

---

### 模块8: 分账管理 (menucode_2509)
**选择器**: `#menucode_2509`

| 子功能 | 路由 | 关键字段 |
|--------|------|---------|
| 分账规则 | `#/split/rules` | 分账比例、分账对象 |
| 分账记录 | `#/split/records` | 分账时间、分账金额 |
| 分账对象 | `#/split/partners` | 股东姓名、联系方式 |

**常用操作**:
- ✅ 设置多股东分账比例
- ✅ 查询分账明细
- ✅ 管理股东信息

---

### 模块9: 数智督导 (menucode_2782)
**选择器**: `#menucode_2782`

| 子功能 | 路由 | 关键字段 |
|--------|------|---------|
| 异常监控 | `#/supervision/monitor` | 异常类型、异常时间 |
| 数据大屏 | `#/supervision/dashboard` | 实时数据、可视化图表 |
| 督导报告 | `#/supervision/report` | 报告周期、报告内容 |
| 预警提醒 | `#/supervision/alert` | 提醒方式、提醒内容 |

**常用操作**:
- ✅ 监控退菜/折扣/库存异常
- ✅ 查看实时运营数据大屏
- ✅ 接收短信/微信预警

---

### 模块10: 效期管理 (menucode_2730)
**选择器**: `#menucode_2730`

| 子功能 | 路由 | 关键字段 |
|--------|------|---------|
| 效期设置 | `#/expiration/settings` | 食材名称、保质期天数 |
| 效期预警 | `#/expiration/alert` | 预警时间、预警级别 |
| 效期记录 | `#/expiration/records` | 处理时间、处理方式 |
| 库存周转 | `#/expiration/turnover` | 周转策略、出库顺序 |

**常用操作**:
- ✅ 设置食材保质期
- ✅ 接收临期预警
- ✅ 记录过期处理
- ✅ 启用先进先出

---

### 模块11: 组织机构及账号 (menucode_1758)
**选择器**: `#menucode_1758`

| 子功能 | 路由 | 关键字段 |
|--------|------|---------|
| 账号管理 | `#/org/accounts` | 账号名称、角色、状态 |
| 角色管理 | `#/org/roles` | 角色名称、权限配置 |
| 组织架构 | `#/org/structure` | 部门名称、岗位设置 |
| 操作日志 | `#/org/logs` | 操作时间、操作内容 |

**常用操作**:
- ✅ 新增员工账号
- ✅ 配置角色权限
- ✅ 设置组织架构
- ✅ 查询操作审计日志

---

### 模块12: 系统设置 (menucode_348)
**选择器**: `#menucode_348`

| 子功能 | 路由 | 关键字段 |
|--------|------|---------|
| 基础设置 | `#/settings/basic` | 系统参数、业务规则 |
| 业务设置 | `#/settings/business` | 结账规则、优惠规则 |
| 打印设置 | `#/settings/print` | 小票模板、打印规则 |
| 消息设置 | `#/settings/message` | 通知开关、提醒方式 |
| 数据同步 | `#/settings/sync` | 同步频率、同步状态 |

**常用操作**:
- ✅ 配置系统参数
- ✅ 设置业务规则
- ✅ 自定义小票模板
- ✅ 开启/关闭消息通知

---

## 🔥 高频操作快捷访问

### 日常运营

1. **查看营业数据**
   - 路由: `#/finance/overview`
   - 选择器: `#menucode_157` → 营业概览

2. **接收外卖订单**
   - 路由: `#/takeout/orders`
   - 选择器: `#menucode_164` → 外卖订单

3. **查询支付明细**
   - 路由: `#/finance/payment-detail`
   - 选择器: `#menucode_157` → 支付明细

4. **管理菜品库存**
   - 路由: `#/dish/list`
   - 选择器: `#menucode_119` → 菜品库

### 初始化配置

1. **配置餐厅信息**
   - 路由: `#/restaurant/info`
   - 选择器: `#menucode_347` → 餐厅信息

2. **批量导入菜品**
   - 路由: `#/dish/list`
   - 选择器: `#menucode_119` → 菜品库

3. **生成桌台二维码**
   - 路由: `#/qrcode/table`
   - 选择器: `#menucode_1816` → 桌台二维码

4. **配置支付方式**
   - 路由: `#/restaurant/payment`
   - 选择器: `#menucode_347` → 支付配置

### 营销活动

1. **设置外卖活动**
   - 路由: `#/takeout/activity`
   - 选择器: `#menucode_164` → 外卖活动

2. **配置菜品套餐**
   - 路由: `#/dish/combo`
   - 选择器: `#menucode_119` → 菜品组合

### 权限管理

1. **新增员工账号**
   - 路由: `#/org/accounts`
   - 选择器: `#menucode_1758` → 账号管理

2. **配置角色权限**
   - 路由: `#/org/roles`
   - 选择器: `#menucode_1758` → 角色管理

---

## 📊 关键数据实体速查

### 1. 餐厅实体 (Restaurant)

**关键字段**:
- restaurant_id: 餐厅唯一标识
- restaurant_name: 餐厅名称
- address: 详细地址
- business_hours: 营业时间
- contact_phone: 联系电话

**关联实体**: 桌台 (Table), 菜品 (Dish), 订单 (Order)

### 2. 桌台实体 (Table)

**关键字段**:
- table_id: 桌台唯一标识
- table_number: 桌台号
- area: 所属区域
- capacity: 容纳人数
- qrcode_url: 二维码链接

**关联实体**: 餐厅 (Restaurant), 订单 (Order)

### 3. 菜品实体 (Dish)

**关键字段**:
- dish_id: 菜品唯一标识
- dish_name: 菜品名称
- category_id: 分类ID
- price: 价格
- stock: 库存状态
- image_url: 菜品图片

**关联实体**: 分类 (Category), 订单明细 (OrderDetail), 菜品规格 (DishSpec)

### 4. 订单实体 (Order)

**关键字段**:
- order_id: 订单唯一标识
- order_number: 订单号
- table_id: 桌台ID (堂食)
- delivery_address: 配送地址 (外卖)
- order_type: 订单类型 (堂食/外卖)
- order_status: 订单状态
- total_amount: 订单总额

**关联实体**: 餐厅 (Restaurant), 桌台 (Table), 订单明细 (OrderDetail), 支付 (Payment)

### 5. 支付实体 (Payment)

**关键字段**:
- payment_id: 支付唯一标识
- transaction_no: 交易流水号
- payment_method: 支付方式
- payment_amount: 支付金额
- payment_status: 支付状态
- settlement_status: 结算状态

**关联实体**: 订单 (Order), 财务 (Finance)

### 6. 财务实体 (Finance)

**关键字段**:
- finance_id: 财务唯一标识
- date: 日期
- revenue: 营业收入
- discount_amount: 优惠金额
- actual_amount: 实收金额
- settlement_amount: 结算金额

**关联实体**: 支付 (Payment), 订单 (Order)

---

## 🎯 按业务场景索引

### 场景1: 新店开业配置

**执行顺序**:
1. 餐厅信息配置 → `#/restaurant/info`
2. 桌台管理 → `#/restaurant/table`
3. 支付配置 → `#/restaurant/payment`
4. 打印设置 → `#/restaurant/printer`
5. 菜品导入 → `#/dish/list`
6. 菜品分类 → `#/dish/category`
7. 桌台二维码生成 → `#/qrcode/table`
8. 小程序设置 → `#/mobile-order/settings`

### 场景2: 外卖平台对接

**执行顺序**:
1. 外卖菜品同步 → `#/takeout/dish-sync`
2. 外卖营业设置 → `#/takeout/business`
3. 外卖活动配置 → `#/takeout/activity`
4. 外卖订单接收 → `#/takeout/orders`

### 场景3: 每日对账流程

**执行顺序**:
1. 查询营业概览 → `#/finance/overview`
2. 查看支付明细 → `#/finance/payment-detail`
3. 查看支付结算 → `#/finance/settlement`
4. 对账管理 → `#/finance/reconciliation`
5. 处理异常订单 (如有)

### 场景4: 员工账号管理

**执行顺序**:
1. 组织架构设置 → `#/org/structure`
2. 角色权限配置 → `#/org/roles`
3. 员工账号创建 → `#/org/accounts`
4. 操作日志审计 → `#/org/logs`

---

## 🔍 搜索技巧

### 按功能名称搜索

使用系统内置搜索:
- 定位: `input[placeholder='请输入想搜索的功能']`
- 支持模糊搜索
- 返回匹配的菜单项

### 按menucode定位

```javascript
// 直接使用CSS选择器
#menucode_927   // 首页
#menucode_347   // 餐厅管理
#menucode_119   // 菜品管理
#menucode_164   // 外卖管理
#menucode_157   // 财务管理
// ... 其他menucode详见 navigation-tree.json
```

### 按URL路由跳转

```javascript
// Hash路由格式
#/                          // 首页
#/restaurant/info           // 餐厅信息
#/dish/list                 // 菜品库
#/takeout/orders            // 外卖订单
#/finance/payment-detail    // 支付明细
```

---

## 📖 详细文档索引

### 完整导航结构
📄 `navigation-tree.json`
- 包含所有菜单的ID、选择器、URL
- JSON格式，方便程序化访问

### 综合知识库
📄 `knowledge-base-report.md`
- 第3节: 12个模块的深度解析
- 第5节: 表单系统分析
- 第6节: 业务流程文档
- 第8节: 自动化操作指南

---

**索引版本**: v1.0
**更新时间**: 2025-10-23
**适用智能体**: M1, M4
**索引类型**: 快速参考索引
