---
name: meituan-operations-center-knowledge
description: 美团管家运营中心完整知识库，包含12个核心运营模块（餐厅管理、菜品管理、手机点餐、二维码管理、外卖管理、财务管理、分账管理、数智督导、效期管理、组织机构、系统设置）的详细功能说明、导航结构、表单定义、业务流程和自动化指南
---

# 美团管家运营中心知识库

## 📋 概述

本知识库为美团管家SaaS系统的**运营中心**模块提供完整的功能知识、导航结构、业务流程和自动化操作指南。

### 适用场景

- 🎯 **智能体决策参考**: 为M1-美团管家运营管理员提供专业领域知识
- 🤖 **网页自动化**: 支持M4智能体进行精确的页面定位和操作
- 📊 **业务流程理解**: 掌握11个核心模块的完整业务逻辑
- 🔍 **数据结构分析**: 理解表单字段、数据实体和业务关系

### 核心价值

- ✅ **完整性**: 覆盖运营中心所有12个一级菜单、56+二级功能
- ✅ **结构化**: JSON导航树 + Markdown知识库双重结构
- ✅ **可操作性**: 提供CSS选择器、URL路由、表单字段等技术细节
- ✅ **业务深度**: 包含业务流程、数据模型、自动化策略

---

## 🚀 Quick Start

### 基础查询

**查询导航结构**:
```markdown
请参考 knowledge/navigation-tree.json 获取完整的导航树结构
- 包含所有菜单的ID、名称、URL、CSS选择器
- 支持通过menucode快速定位功能模块
```

**查询功能详情**:
```markdown
请参考 knowledge/knowledge-base-report.md 获取详细功能说明
- 第3节: 12个核心模块的深度解析
- 第5节: 表单系统分析
- 第6节: 业务流程文档
- 第8节: 自动化操作指南
```

**快速索引**:
```markdown
请参考 knowledge/index.md 获取快速导航索引
- 按模块分类的功能清单
- 常用操作的快速链接
- 关键数据实体速查
```

### 使用示例

**示例1: 查询菜品管理功能**
```
需求: "帮我配置菜品库"
→ 查询 navigation-tree.json → menucode_119 (菜品管理)
→ 查询 knowledge-base-report.md → 第3.3节 (菜品管理详解)
→ 获取:
  - 页面URL: #/dish/list
  - 表单字段: 菜品名称、分类、价格、规格等
  - 业务规则: 批量导入、多规格设置、价格管理
```

**示例2: 网页自动化定位**
```
需求: "自动化配置外卖菜品同步"
→ 查询 navigation-tree.json → menucode_164 (外卖管理)
→ 获取选择器: #menucode_164
→ 查询子菜单: "菜品同步" → #/takeout/dish-sync
→ 查询表单定义 → 同步规则、价格策略字段
```

**示例3: 业务流程理解**
```
需求: "外卖订单处理流程"
→ 查询 knowledge-base-report.md → 第6.2节
→ 获取完整流程:
  1. 订单接收 (实时推送)
  2. 订单确认 (自动/手动)
  3. 备餐制作
  4. 配送安排
  5. 订单完成
```

---

## 📚 知识库结构

### 1. 导航结构 (navigation-tree.json)

**文件位置**: `knowledge/navigation-tree.json`

**数据结构**:
```json
{
  "metadata": {
    "task_id": "唯一任务标识",
    "platform": "美团管家",
    "module": "运营中心",
    "base_url": "https://pos.meituan.com/web/operation/main",
    "routing_mode": "hash"
  },
  "top_navigation": [
    {
      "id": "顶层导航ID",
      "name": "导航名称",
      "url": "路由地址",
      "active": true/false,
      "description": "功能描述"
    }
  ],
  "side_navigation": {
    "section": "运营中心",
    "total_menus": 12,
    "menus": [
      {
        "id": "menucode_XXX",
        "name": "菜单名称",
        "level": 1,
        "type": "page/submenu",
        "url": "#/path",
        "selector": "#menucode_XXX",
        "icon": "图标类型",
        "description": "功能描述",
        "children": [
          {
            "name": "子菜单名称",
            "url": "#/path/subpath",
            "description": "子功能描述"
          }
        ]
      }
    ]
  },
  "statistics": {
    "total_level1_menus": 12,
    "total_level2_menus": 56,
    "estimated_total_pages": 60
  }
}
```

**用途**:
- ✅ 精确的CSS选择器定位
- ✅ 完整的URL路由映射
- ✅ 菜单层级关系理解
- ✅ 自动化脚本导航支持

### 2. 综合知识库 (knowledge-base-report.md)

**文件位置**: `knowledge/knowledge-base-report.md`

**章节结构**:

1. **运营中心概览** (第1节)
   - 平台定位与价值
   - 核心功能矩阵
   - 业务流程架构

2. **顶层导航架构** (第2节)
   - 4大顶层导航模块
   - 运营中心、营销中心、供应链、报表中心

3. **核心模块详解** (第3节) ⭐
   - 3.1 首页 (menucode_927)
   - 3.2 餐厅管理 (menucode_347) - 5个子模块
   - 3.3 菜品管理 (menucode_119) - 6个子模块
   - 3.4 手机点餐 (menucode_1571) - 4个子模块
   - 3.5 二维码管理 (menucode_1816) - 4个子模块
   - 3.6 外卖管理 (menucode_164) - 4个子模块
   - 3.7 财务管理 (menucode_157) - 6个子模块
   - 3.8 分账管理 (menucode_2509) - 3个子模块
   - 3.9 数智督导 (menucode_2782) - 4个子模块
   - 3.10 效期管理 (menucode_2730) - 4个子模块
   - 3.11 组织机构及账号 (menucode_1758) - 4个子模块
   - 3.12 系统设置 (menucode_348) - 5个子模块

4. **导航结构图** (第4节)
   - ASCII树状结构
   - 可视化导航关系

5. **表单系统分析** (第5节) ⭐
   - 通用字段定义
   - 字段验证规则
   - 数据关联关系
   - 表单样式规范

6. **业务流程文档** (第6节) ⭐
   - 6.1 堂食点餐流程
   - 6.2 外卖订单处理流程
   - 6.3 菜品管理流程
   - 6.4 财务对账流程

7. **数据实体模型** (第7节)
   - 餐厅实体、桌台实体
   - 菜品实体、订单实体
   - 支付实体、财务实体
   - 实体关系图

8. **自动化操作指南** (第8节) ⭐
   - 页面导航策略
   - 表单填写规范
   - 数据采集方法
   - 错误处理机制

9. **技术实施细节** (第9节)
   - Hash路由机制
   - CSS选择器策略
   - 数据加载模式
   - API交互模式

10. **附录** (第10节)
    - 术语表
    - 常见问题
    - 版本历史

**用途**:
- ✅ 深度业务理解
- ✅ 表单字段参考
- ✅ 流程逻辑掌握
- ✅ 自动化策略指导

### 3. 快速索引 (index.md)

**文件位置**: `knowledge/index.md`

**内容**:
- 按模块分类的功能清单
- 常用操作的快速链接
- 关键数据实体速查
- 高频业务场景索引

**用途**:
- ✅ 快速查找功能入口
- ✅ 常用操作快捷访问
- ✅ 减少知识检索时间

---

## 🎯 核心模块速查

### 模块1: 餐厅管理 (menucode_347)

**核心功能**:
- 餐厅信息配置 (#/restaurant/info)
- 桌台管理 (#/restaurant/table)
- 打印设置 (#/restaurant/printer)
- 支付配置 (#/restaurant/payment)
- 设备管理 (#/restaurant/device)

**关键字段**: 门店名称、营业时间、桌台号、区域、容纳人数、打印机IP、支付方式

### 模块2: 菜品管理 (menucode_119)

**核心功能**:
- 菜品库 (#/dish/list) - 新增、编辑、批量导入
- 菜品分类 (#/dish/category) - 分类创建、排序
- 菜品规格 (#/dish/spec) - 多规格设置
- 价格管理 (#/dish/price) - 堂食价、外卖价、会员价
- 菜品组合 (#/dish/combo) - 套餐配置
- 菜品部门 (#/dish/department) - 厨房部门分配

**关键字段**: 菜品名称、分类、规格、价格、库存、图片、描述

### 模块3: 外卖管理 (menucode_164)

**核心功能**:
- 外卖订单 (#/takeout/orders) - 实时订单接收
- 菜品同步 (#/takeout/dish-sync) - 外卖菜品关联
- 营业设置 (#/takeout/business) - 营业时间、配送范围
- 外卖活动 (#/takeout/activity) - 满减活动、折扣券

**关键字段**: 订单号、配送地址、联系电话、菜品明细、订单状态

### 模块4: 财务管理 (menucode_157)

**核心功能**:
- 支付明细 (#/finance/payment-detail)
- 支付结算 (#/finance/settlement)
- 营业概览 (#/finance/overview)
- 菜品销售统计 (#/finance/dish-sales)
- 综合营业统计 (#/finance/comprehensive)
- 对账管理 (#/finance/reconciliation)

**关键指标**:
- 月度营业额: ¥87,217.21
- 月度营业天数: 23天
- 异常订单数: 0

**关键字段**: 交易流水号、支付方式、支付金额、结算状态、对账状态

---

## 🤖 与M1智能体集成

### M1核心任务类别映射

本知识库直接支持M1智能体的11个核心任务类别:

| M1任务类别 | 对应知识模块 | 导航定位 |
|-----------|------------|---------|
| 1. 餐厅信息配置 | 餐厅管理 (3.2节) | menucode_347 |
| 2. 菜品库管理 | 菜品管理 (3.3节) | menucode_119 |
| 3. 手机点餐设置 | 手机点餐 (3.4节) | menucode_1571 |
| 4. 桌台二维码生成 | 二维码管理 (3.5节) | menucode_1816 |
| 5. 外卖平台对接 | 外卖管理 (3.6节) | menucode_164 |
| 6. 财务对账 | 财务管理 (3.7节) | menucode_157 |
| 7. 支付配置 | 餐厅管理 > 支付配置 | menucode_347 |
| 8. 打印设置 | 餐厅管理 > 打印设置 | menucode_347 |
| 9. 营业数据查询 | 财务管理 > 营业概览 | menucode_157 |
| 10. 权限管理 | 组织机构及账号 (3.11节) | menucode_1758 |
| 11. 系统参数配置 | 系统设置 (3.12节) | menucode_348 |

### 使用建议

**决策阶段**:
- 查询业务流程 (第6节) 理解完整业务逻辑
- 查询数据实体模型 (第7节) 理解数据关系

**执行阶段**:
- 查询导航结构 (navigation-tree.json) 精确定位页面
- 查询表单系统 (第5节) 获取字段定义和验证规则
- 查询自动化指南 (第8节) 获取操作策略

**质量保障**:
- 参考业务规则确保配置正确性
- 参考数据标准确保数据准确性
- 参考错误处理机制提升操作可靠性

---

## 📖 API Reference

### 查询导航结构

```javascript
// 查询一级菜单
navigation-tree.json → side_navigation.menus
  → 筛选条件: level === 1

// 查询特定模块
navigation-tree.json → side_navigation.menus
  → 筛选条件: id === "menucode_XXX"

// 查询子菜单
navigation-tree.json → side_navigation.menus[i].children
```

### 查询功能详情

```markdown
// 查询模块详解
knowledge-base-report.md → 第3节
  → 3.X 具体模块名称

// 查询表单字段
knowledge-base-report.md → 第5节
  → 5.X 具体表单类型

// 查询业务流程
knowledge-base-report.md → 第6节
  → 6.X 具体流程类型
```

### 查询数据实体

```markdown
// 查询实体定义
knowledge-base-report.md → 第7节
  → 7.X 具体实体类型

// 查询实体关系
knowledge-base-report.md → 第7节
  → 实体关系图
```

### 查询自动化策略

```markdown
// 查询操作指南
knowledge-base-report.md → 第8节
  → 8.X 具体操作类型

// 查询技术细节
knowledge-base-report.md → 第9节
  → 9.X 具体技术主题
```

---

## 🔧 技术实施

### Hash路由机制

**基础URL**: `https://pos.meituan.com/web/operation/main`

**路由格式**: `#/[module]/[function]`

**示例**:
- 首页: `#/`
- 菜品库: `#/dish/list`
- 外卖订单: `#/takeout/orders`
- 财务对账: `#/finance/reconciliation`

### CSS选择器策略

**一级菜单定位**:
```css
#menucode_927  /* 首页 */
#menucode_347  /* 餐厅管理 */
#menucode_119  /* 菜品管理 */
#menucode_164  /* 外卖管理 */
#menucode_157  /* 财务管理 */
```

**辅助功能定位**:
```css
input[placeholder='请输入想搜索的功能']  /* 功能搜索 */
/* 其他辅助功能详见 navigation-tree.json → auxiliary_functions */
```

### 数据加载模式

- **懒加载**: 菜单展开时才加载子菜单内容
- **按需加载**: 切换页面时才加载对应数据
- **缓存策略**: 常用数据缓存在浏览器

---

## 📊 统计信息

### 覆盖范围

- **顶层导航**: 4个模块
- **一级菜单**: 12个核心功能
- **二级菜单**: 56+子功能
- **预估页面**: 60+页面

### 数据来源

- **采集时间**: 2025-10-23
- **采集智能体**: E2-网站情报采集员
- **数据版本**: v1.0
- **完整度**: 运营中心模块100%覆盖

### 更新记录

- **v1.0** (2025-10-23): 初始版本，完整覆盖运营中心12个核心模块

---

## 🎓 最佳实践

### DO ✅

1. **查询前明确目标**: 明确是查询导航、功能、流程还是数据结构
2. **分层渐进**: 先查索引 → 再查导航 → 最后查详细文档
3. **结合使用**: navigation-tree.json (技术定位) + knowledge-base-report.md (业务理解)
4. **验证数据**: 参考业务规则验证配置正确性

### DON'T ❌

1. **避免盲目操作**: 未理解业务流程前不要直接自动化
2. **避免忽略验证**: 不要跳过字段验证规则检查
3. **避免硬编码**: 使用menucode而非硬编码CSS选择器
4. **避免忽略错误**: 参考错误处理机制确保操作可靠

---

## 📞 支持与反馈

### 关联智能体

- **M1**: 美团管家运营管理员 (主要使用者)
- **M4**: 美团管家网页自动化操作助手 (执行层)
- **M3**: 美团管家报表管理员 (数据分析)

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
**适用智能体**: M1-美团管家运营管理员
**知识库类型**: 静态知识库 (Static Knowledge Base)
