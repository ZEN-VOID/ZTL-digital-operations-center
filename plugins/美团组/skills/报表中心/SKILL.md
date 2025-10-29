---
name: meituan-report-center-knowledge
description: 美团管家报表中心完整知识库，包含10个核心报表模块（经营分析、财务报表、销售报表、库存报表、会员分析、营销报表、商圈选址、员工报表、自定义报表）的详细功能说明、导航结构、数据实体、业务场景和分析指南
---

# 美团管家报表中心知识库

## 📋 概述

本知识库为美团管家SaaS系统的**报表中心**模块提供完整的功能知识、导航结构、数据分析方法和业务场景指南。

### 适用场景

- 🎯 **智能体决策参考**: 为M3-美团管家报表管理员提供专业领域知识
- 🤖 **网页自动化**: 支持M4智能体进行精确的页面定位和操作
- 📊 **数据分析流程**: 掌握10个核心报表模块的完整分析逻辑
- 🔍 **数据结构分析**: 理解报表字段、数据实体和业务关系

### 核心价值

- ✅ **完整性**: 覆盖报表中心所有10个一级菜单、35+二级功能
- ✅ **结构化**: JSON导航树 + Markdown知识库双重结构
- ✅ **可操作性**: 提供CSS选择器、URL路由、报表字段等技术细节
- ✅ **分析深度**: 包含经营分析、财务管理、数据洞察完整体系

---

## 🚀 Quick Start

### 基础查询

**查询导航结构**:
```markdown
请参考 knowledge/navigation-tree.json 获取完整的导航树结构
- 包含所有菜单的ID、名称、URL、层级关系
- 支持通过menucode快速定位功能模块
```

**查询功能详情**:
```markdown
请参考 knowledge/knowledge-base-report.md 获取详细功能说明
- 第2节: 侧边导航架构（10大核心模块）
- 第3节: 核心报表模块详解
- 第4节: 数据可视化体系
- 第5节: 关键数据实体
- 第6节: 业务场景与决策树
```

**快速索引**:
```markdown
请参考 knowledge/index.md 获取快速导航索引
- 按功能模块分类的报表清单
- 常用分析场景的快速链接
- 关键数据实体速查
```

### 使用示例

**示例1: 查询经营分析功能**
```
需求: "生成日报表分析门店经营数据"
→ 查询 navigation-tree.json → operating-analysis 模块
→ 查询 knowledge-base-report.md → 第3.2节 (经营分析详解)
→ 获取:
  - 页面URL: #/rms-report/operating-analysis
  - 子功能: 日报表、月报表、趋势分析、同行对比
  - 关键指标: 营业额、订单量、客单价、毛利率
  - 数据实体: Order, Revenue, Performance
```

**示例2: 网页自动化定位**
```
需求: "自动化导出财务报表"
→ 查询 navigation-tree.json → financial-report 模块
→ 获取URL: #/rms-report/financial
→ 查询子菜单:
  - 收入报表 (#/rms-report/financial/revenue)
  - 成本报表 (#/rms-report/financial/cost)
  - 利润报表 (#/rms-report/financial/profit)
→ 查询导出格式: Excel, PDF, CSV, PNG
```

**示例3: 业务场景理解**
```
需求: "如何基于会员RFM分析设计营销活动"
→ 查询 knowledge-base-report.md → 第6.4节
→ 获取完整流程:
  1. 会员分析 → RFM分析
  2. 导出重要挽留客户名单（R低、F低、M高）
  3. 设计专属挽留方案
  4. 执行营销活动
  5. 查看营销报表评估效果
```

---

## 📚 知识库结构

### 1. 导航结构 (navigation-tree.json)

**文件位置**: `knowledge/navigation-tree.json`

**数据结构**:
```json
{
  "metadata": {
    "platform": "美团管家",
    "module": "报表中心",
    "base_url": "https://pos.meituan.com/web/report/main",
    "collected_at": "2025-10-23",
    "routing_mode": "hash"
  },
  "side_navigation": {
    "section": "报表中心",
    "description": "提供经营分析、财务管理、数据洞察等全方位报表服务",
    "menus": [
      {
        "id": "report-home",
        "name": "报表首页",
        "url": "#/rms-report/home",
        "description": "总览展示核心经营指标",
        "expected_features": [
          "核心经营指标卡片",
          "趋势图表",
          "快捷报表入口"
        ]
      }
    ]
  },
  "data_visualization": {
    "chart_types": [
      {"type": "line_chart", "name": "折线图"},
      {"type": "bar_chart", "name": "柱状图"},
      {"type": "pie_chart", "name": "饼图"},
      {"type": "table", "name": "数据表格"},
      {"type": "kpi_card", "name": "指标卡片"},
      {"type": "heatmap", "name": "热力图"}
    ]
  },
  "filter_dimensions": {
    "time_filters": ["今日", "昨日", "近7天", "近30天", "本周", "本月", "上月", "自定义"],
    "store_filters": ["单门店", "多门店", "门店组", "全部门店"],
    "channel_filters": ["堂食", "外卖", "自提", "全渠道"]
  }
}
```

**用途**:
- ✅ 精确的URL路由映射
- ✅ 完整的菜单层级关系理解
- ✅ 图表类型和筛选维度参考
- ✅ 自动化脚本导航支持

### 2. 综合知识库 (knowledge-base-report.md)

**文件位置**: `knowledge/knowledge-base-report.md`

**章节结构**:

1. **报表中心概览** (第1节)
   - 平台定位与价值
   - 核心功能矩阵
   - 数据架构体系

2. **侧边导航架构** (第2节)
   - 10大核心报表模块
   - 35个子功能菜单

3. **核心报表模块详解** (第3节) ⭐
   - 3.1 报表首页 (report-home)
   - 3.2 经营分析 (operating-analysis) - 4个子模块
   - 3.3 财务报表 (financial-report) - 4个子模块
   - 3.4 销售报表 (sales-report) - 4个子模块
   - 3.5 库存报表 (inventory-report) - 4个子模块
   - 3.6 会员分析 (member-report) - 4个子模块
   - 3.7 营销报表 (marketing-report) - 4个子模块
   - 3.8 商圈选址 (location-analysis) - 3个子模块
   - 3.9 员工报表 (employee-report) - 3个子模块
   - 3.10 自定义报表 (custom-report)

4. **数据可视化体系** (第4节)
   - 6种图表类型及使用场景
   - 图表组合最佳实践

5. **关键数据实体** (第5节) ⭐
   - Order实体（订单数据）
   - Revenue实体（收入数据）
   - Cost实体（成本数据）
   - Member实体（会员数据）
   - Inventory实体（库存数据）
   - Campaign实体（活动数据）
   - 实体关系图

6. **业务场景与决策树** (第6节) ⭐
   - 6.1 经营数据异常诊断
   - 6.2 新品定价策略分析
   - 6.3 库存预警与补货决策
   - 6.4 会员营销活动设计
   - 6.5 商圈选址评估
   - 6.6 人效分析与排班优化

7. **筛选与导出规范** (第7节)
   - 时间筛选器使用
   - 门店筛选器使用
   - 渠道筛选器使用
   - 导出格式说明

8. **行业基准数据** (第8节)
   - 成本率标准
   - 损耗率标准
   - 人效标准
   - RFM阈值

9. **技术实施细节** (第9节)
   - Hash路由机制
   - 数据加载模式
   - 实时/小时/天级刷新策略

10. **角色快速索引** (第10节)
    - 老板视角
    - 店长视角
    - 财务视角
    - 运营视角

11. **按问题类型索引** (第11节)
    - 营收下降
    - 成本上升
    - 会员流失
    - 库存积压

12. **按访问频率索引** (第12节)
    - 高频报表（日报表、收入报表）
    - 中频报表（会员分析、活动分析）
    - 低频报表（选址分析）

13. **常见问题FAQ** (第13节)

**用途**:
- ✅ 深度报表业务理解
- ✅ 数据实体参考
- ✅ 分析场景指导
- ✅ 决策树逻辑

### 3. 快速索引 (index.md)

**文件位置**: `knowledge/index.md`

**内容**:
- 按模块分类的报表清单
- 常用分析操作的快速链接
- 关键数据实体速查
- 高频分析场景索引
- CSS选择器速查

**用途**:
- ✅ 快速查找报表入口
- ✅ 常用操作快捷访问
- ✅ 减少知识检索时间

---

## 🎯 核心模块速查

### 模块1: 经营分析 (operating-analysis)

**核心功能**:
- 日报表 (#/rms-report/operating-analysis/daily)
- 月报表 (#/rms-report/operating-analysis/monthly)
- 趋势分析 (#/rms-report/operating-analysis/trend)
- 同行对比 (#/rms-report/operating-analysis/peer)

**关键指标**: 营业额、订单量、客单价、毛利率、同比环比

**数据实体**: Order, Revenue, Performance

### 模块2: 财务报表 (financial-report)

**核心功能**:
- 收入报表 (#/rms-report/financial/revenue)
- 成本报表 (#/rms-report/financial/cost)
- 利润报表 (#/rms-report/financial/profit)
- 资金流水 (#/rms-report/financial/cashflow)

**关键指标**: 营业收入、食材成本率、人工成本率、毛利、净利润

**数据实体**: Revenue, Cost, Profit

**行业基准**:
- 食材成本率: 30%-40%
- 人工成本率: 18%-25%
- 房租成本率: 8%-15%

### 模块3: 销售报表 (sales-report)

**核心功能**:
- 菜品销售 (#/rms-report/sales/dish)
- 品类销售 (#/rms-report/sales/category)
- 时段分析 (#/rms-report/sales/time-slot)
- 渠道分析 (#/rms-report/sales/channel)

**关键指标**: 销量排行、销售额、销售占比、增长率

**数据实体**: Order, Dish, Category

### 模块4: 库存报表 (inventory-report)

**核心功能**:
- 库存现状 (#/rms-report/inventory/status)
- 出入库记录 (#/rms-report/inventory/inout)
- 库存预警 (#/rms-report/inventory/warning)
- 损耗报表 (#/rms-report/inventory/loss)

**关键指标**: 库存量、库存金额、周转率、损耗率

**数据实体**: Inventory, Material

**行业基准**:
- 正常损耗率: 3%-5%
- 库存周转天数: 7-10天

### 模块5: 会员分析 (member-report)

**核心功能**:
- 会员增长 (#/rms-report/member/growth)
- 会员消费 (#/rms-report/member/consumption)
- 会员画像 (#/rms-report/member/portrait)
- RFM分析 (#/rms-report/member/rfm)

**关键指标**: 新增会员、活跃会员、消费频次、客单价

**数据实体**: Member, Order

**RFM阈值**:
- 重要价值客户: R≥60, F≥8, M≥500
- 重要挽留客户: R<60, F≥5, M≥300

### 模块6: 营销报表 (marketing-report)

**核心功能**:
- 活动效果 (#/rms-report/marketing/campaign)
- 优惠券分析 (#/rms-report/marketing/coupon)
- 折扣分析 (#/rms-report/marketing/discount)
- 营销ROI (#/rms-report/marketing/roi)

**关键指标**: 参与人数、活动GMV、优惠券核销率、ROI

**数据实体**: Campaign, Coupon

---

## 🤖 与M3智能体集成

### M3核心任务类别映射

本知识库直接支持M3智能体的9个核心任务类别:

| M3任务类别 | 对应知识模块 | 导航定位 |
|-----------|------------|---------|
| 1. 经营数据分析 | 经营分析 (3.2节) | operating-analysis |
| 2. 财务报表生成 | 财务报表 (3.3节) | financial-report |
| 3. 销售数据分析 | 销售报表 (3.4节) | sales-report |
| 4. 库存管理报表 | 库存报表 (3.5节) | inventory-report |
| 5. 会员数据分析 | 会员分析 (3.6节) | member-report |
| 6. 营销效果分析 | 营销报表 (3.7节) | marketing-report |
| 7. 商圈选址分析 | 商圈选址 (3.8节) | location-analysis |
| 8. 员工绩效分析 | 员工报表 (3.9节) | employee-report |
| 9. 自定义报表生成 | 自定义报表 (3.10节) | custom-report |

### 使用建议

**决策阶段**:
- 查询业务场景 (第6节) 理解完整分析逻辑
- 查询数据实体模型 (第5节) 理解数据关系
- 查询行业基准 (第8节) 获取对标标准

**执行阶段**:
- 查询导航结构 (navigation-tree.json) 精确定位页面
- 查询筛选规范 (第7节) 获取筛选器配置
- 查询导出格式 (第7节) 确定输出格式

**质量保障**:
- 参考数据实体确保字段正确性
- 参考行业基准确保分析合理性
- 参考决策树确保逻辑完整性

---

## 📖 API Reference

### 查询导航结构

```javascript
// 查询一级菜单
navigation-tree.json → side_navigation.menus
  → 筛选条件: level === 1

// 查询特定模块
navigation-tree.json → side_navigation.menus
  → 筛选条件: id === "report-home" / "operating-analysis" 等

// 查询子菜单
navigation-tree.json → side_navigation.menus[i].sub_menus
```

### 查询功能详情

```markdown
// 查询模块详解
knowledge-base-report.md → 第3节
  → 3.X 具体模块名称

// 查询数据实体
knowledge-base-report.md → 第5节
  → 5.X 具体实体类型

// 查询业务场景
knowledge-base-report.md → 第6节
  → 6.X 具体场景类型
```

### 查询图表类型

```markdown
// 查询可用图表
navigation-tree.json → data_visualization.chart_types

// 查询筛选器
navigation-tree.json → filter_dimensions
  → time_filters / store_filters / channel_filters
```

---

## 🔧 技术实施

### Hash路由机制

**基础URL**: `https://pos.meituan.com/web/report/main`

**路由格式**: `#/rms-report/[module]/[function]`

**示例**:
- 报表首页: `#/rms-report/home`
- 日报表: `#/rms-report/operating-analysis/daily`
- 收入报表: `#/rms-report/financial/revenue`
- 菜品销售: `#/rms-report/sales/dish`

### 数据刷新策略

- **实时**: 核心经营指标（营业额、订单量）
- **小时级**: 销售数据、库存数据
- **天级**: 财务报表、会员分析

### 数据权限

- **基于角色**: 不同角色看到不同数据范围
- **门店权限**: 单店/多店/区域/全国
- **时间权限**: 历史数据访问期限

---

## 📊 统计信息

### 覆盖范围

- **一级菜单**: 10个核心报表功能
- **二级菜单**: 35+子功能
- **图表类型**: 6种可视化方式
- **筛选维度**: 时间/门店/渠道

### 数据来源

- **采集时间**: 2025-10-23
- **采集智能体**: E2-网站情报采集员
- **数据版本**: v1.0
- **完整度**: 报表中心模块100%覆盖

### 质量评分

根据Phase 2验证:
- **总分**: 91.11/100 (优秀)
- **导航系统**: 10/10
- **数据实体**: 10/10
- **业务场景**: 10/10

### 更新记录

- **v1.0** (2025-10-23): 初始版本，完整覆盖报表中心10个核心模块

---

## 🎓 最佳实践

### DO ✅

1. **查询前明确目标**: 明确是查询导航、报表、场景还是数据结构
2. **分层渐进**: 先查索引 → 再查导航 → 最后查详细文档
3. **结合使用**: navigation-tree.json (技术定位) + knowledge-base-report.md (业务理解)
4. **参考基准**: 使用行业基准数据进行对标分析
5. **理解场景**: 先理解业务场景再进行数据分析

### DON'T ❌

1. **避免盲目分析**: 未理解数据实体前不要直接出报表
2. **避免忽略筛选**: 不要忘记设置时间、门店、渠道筛选
3. **避免孤立分析**: 综合多个报表模块进行交叉分析
4. **避免忽略基准**: 不要忽略行业基准数据的对标参考

---

## 📞 支持与反馈

### 关联智能体

- **M3**: 美团管家报表管理员 (主要使用者)
- **M4**: 美团管家网页自动化操作助手 (执行层)
- **M1**: 美团管家运营管理员 (数据源)
- **M2**: 美团管家营销管理员 (营销数据)

### 知识库维护

- **维护者**: E2-网站情报采集员
- **更新频率**: 根据美团管家平台更新
- **版本控制**: Git管理，保留历史版本

---

## 📚 相关资源

### 外部文档

- [美团管家官方帮助中心](https://pos.meituan.com/help)
- [美团商家中心](https://e.meituan.com)

### 内部智能体

- **M1**: 运营管理 (`.claude/agents/中台组/M1-美团管家运营管理员.md`)
- **M2**: 营销管理 (`.claude/agents/中台组/M2-美团管家营销管理员.md`)
- **M3**: 报表管理 (`.claude/agents/中台组/M3-美团管家报表管理员.md`)
- **M4**: 网页自动化 (`.claude/agents/中台组/M4-美团管家网页自动化操作助手.md`)

### 系统文档

- **框架文档**: `.claude/CLAUDE.md` (系统架构)
- **项目文档**: `CLAUDE.md` (项目配置)

---

**版本**: v1.0
**更新时间**: 2025-10-23
**适用智能体**: M3-美团管家报表管理员
**知识库类型**: 静态知识库 (Static Knowledge Base)
