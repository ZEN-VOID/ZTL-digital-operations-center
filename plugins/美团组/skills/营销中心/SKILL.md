---
name: meituan-marketing-center-knowledge
description: 美团管家营销中心完整知识库，包含12个核心营销模块（渠道管理、会员运营、卡券管理、大促活动、储值管理、评价管理、群发短信、团购管理、数据报表、优惠同享、素材管理）的详细功能说明、导航结构、表单定义、业务流程和自动化指南
---

# 美团管家营销中心知识库

## 📋 概述

本知识库为美团管家SaaS系统的**营销中心**模块提供完整的功能知识、导航结构、业务流程和自动化操作指南。

### 适用场景

- 🎯 **智能体决策参考**: 为M2-美团管家营销管理员提供专业领域知识
- 🤖 **网页自动化**: 支持M4智能体进行精确的页面定位和操作
- 📊 **营销流程理解**: 掌握12个核心模块的完整营销逻辑
- 🔍 **数据结构分析**: 理解表单字段、数据实体和业务关系

### 核心价值

- ✅ **完整性**: 覆盖营销中心所有12个一级菜单、52+二级功能
- ✅ **结构化**: JSON导航树 + Markdown知识库双重结构
- ✅ **可操作性**: 提供CSS选择器、URL路由、表单字段等技术细节
- ✅ **营销深度**: 包含会员运营、活动促销、数据分析完整体系

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

**示例1: 查询会员管理功能**
```
需求: "配置会员等级体系"
→ 查询 navigation-tree.json → menucode_2220 (用户模块)
→ 查询 knowledge-base-report.md → 第3.3节 (会员管理详解)
→ 获取:
  - 页面URL: #/marketing/member/level
  - 表单字段: 等级名称、升级条件、会员权益
  - 业务规则: 积分累计、等级晋升、权益配置
```

**示例2: 网页自动化定位**
```
需求: "自动化创建优惠券"
→ 查询 navigation-tree.json → menucode_2221 (卡券模块)
→ 获取选择器: #menucode_2221
→ 查询子菜单: "创建卡券" → #/marketing/coupon/create
→ 查询表单定义 → 券类型、面额、使用门槛等字段
```

**示例3: 业务流程理解**
```
需求: "卡券发放流程"
→ 查询 knowledge-base-report.md → 第6.2节
→ 获取完整流程:
  1. 创建卡券 (设置规则)
  2. 发布卡券 (激活状态)
  3. 发放卡券 (手动/自动)
  4. 用户领取
  5. 核销使用
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
    "module": "营销中心",
    "base_url": "https://pos.meituan.com/web/marketing/home",
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
    "section": "营销中心",
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
    "total_level2_menus": 52,
    "estimated_total_pages": 65
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

1. **营销中心概览** (第1节)
   - 平台定位与价值
   - 核心功能矩阵
   - 业务流程架构

2. **顶层导航架构** (第2节)
   - 4大顶层导航模块
   - 运营中心、营销中心、供应链、报表中心

3. **核心模块详解** (第3节) ⭐
   - 3.1 首页 (menucode_928)
   - 3.2 渠道管理 (menucode_2227) - 3个子模块
   - 3.3 用户管理 (menucode_2220) - 5个子模块
   - 3.4 卡券管理 (menucode_2221) - 6个子模块
   - 3.5 大促活动 (menucode_2222) - 5个子模块
   - 3.6 储值管理 (menucode_3071) - 4个子模块
   - 3.7 评价管理 (menucode_1407) - 4个子模块
   - 3.8 群发短信 (menucode_438) - 4个子模块
   - 3.9 团购管理 (menucode_1564) - 4个子模块
   - 3.10 数据报表 (menucode_2226) - 5个子模块
   - 3.11 优惠同享管理 (menucode_2286) - 4个子模块
   - 3.12 素材管理 (menucode_2956) - 4个子模块

4. **导航结构图** (第4节)
   - ASCII树状结构
   - 可视化导航关系

5. **表单系统分析** (第5节) ⭐
   - 通用字段定义
   - 字段验证规则
   - 数据关联关系
   - 表单样式规范

6. **业务流程文档** (第6节) ⭐
   - 6.1 会员注册流程
   - 6.2 卡券创建与发放流程
   - 6.3 营销活动执行流程
   - 6.4 储值充值流程

7. **数据实体模型** (第7节)
   - 会员实体、卡券实体
   - 活动实体、订单实体
   - 储值实体、评价实体
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
- ✅ 深度营销业务理解
- ✅ 表单字段参考
- ✅ 流程逻辑掌握
- ✅ 自动化策略指导

### 3. 快速索引 (index.md)

**文件位置**: `knowledge/index.md`

**内容**:
- 按模块分类的功能清单
- 常用营销操作的快速链接
- 关键数据实体速查
- 高频营销场景索引

**用途**:
- ✅ 快速查找功能入口
- ✅ 常用操作快捷访问
- ✅ 减少知识检索时间

---

## 🎯 核心模块速查

### 模块1: 渠道管理 (menucode_2227)

**核心功能**:
- 渠道列表 (#/marketing/channel/list)
- 渠道配置 (#/marketing/channel/config)
- 渠道效果 (#/marketing/channel/effect)

**关键字段**: 渠道名称、渠道类型、流量配置、转化率、ROI

### 模块2: 用户管理 (menucode_2220)

**核心功能**:
- 会员列表 (#/marketing/member/list)
- 会员等级 (#/marketing/member/level)
- 积分管理 (#/marketing/member/points)
- 会员权益 (#/marketing/member/rights)
- 会员标签 (#/marketing/member/tags)

**关键字段**: 会员ID、手机号、等级、积分、储值余额、消费金额、标签

### 模块3: 卡券管理 (menucode_2221)

**核心功能**:
- 卡券列表 (#/marketing/coupon/list)
- 创建卡券 (#/marketing/coupon/create)
- 卡券核销 (#/marketing/coupon/verify)
- 卡券模板 (#/marketing/coupon/template)
- 发放记录 (#/marketing/coupon/grant)
- 使用规则 (#/marketing/coupon/rules)

**关键字段**: 券名称、券类型、面额、使用门槛、有效期、发行量、核销状态

### 模块4: 大促活动 (menucode_2222)

**核心功能**:
- 活动列表 (#/marketing/campaign/list)
- 创建活动 (#/marketing/campaign/create)
- 活动数据 (#/marketing/campaign/data)
- 满减活动 (#/marketing/campaign/discount)
- 限时折扣 (#/marketing/campaign/flash)

**关键指标**:
- 活动参与人数
- 活动GMV
- 客单价提升
- ROI分析

**关键字段**: 活动名称、活动类型、优惠规则、活动周期、预算、目标人群

### 模块5: 数据报表 (menucode_2226)

**核心功能**:
- 营销概览 (#/marketing/report/overview)
- 会员分析 (#/marketing/report/member)
- 卡券分析 (#/marketing/report/coupon)
- 活动分析 (#/marketing/report/campaign)
- 渠道分析 (#/marketing/report/channel)

**关键指标**:
- 会员增长率
- 活动转化率
- 卡券核销率
- 营销ROI

---

## 🤖 与M2智能体集成

### M2核心任务类别映射

本知识库直接支持M2智能体的11个核心任务类别:

| M2任务类别 | 对应知识模块 | 导航定位 |
|-----------|------------|---------|
| 1. 会员管理 | 用户管理 (3.3节) | menucode_2220 |
| 2. 会员等级体系 | 用户管理 > 会员等级 | menucode_2220 |
| 3. 积分管理 | 用户管理 > 积分管理 | menucode_2220 |
| 4. 卡券管理 | 卡券管理 (3.4节) | menucode_2221 |
| 5. 营销活动 | 大促活动 (3.5节) | menucode_2222 |
| 6. 储值管理 | 储值管理 (3.6节) | menucode_3071 |
| 7. 评价管理 | 评价管理 (3.7节) | menucode_1407 |
| 8. 短信营销 | 群发短信 (3.8节) | menucode_438 |
| 9. 团购管理 | 团购管理 (3.9节) | menucode_1564 |
| 10. 营销数据分析 | 数据报表 (3.10节) | menucode_2226 |
| 11. 裂变营销 | 优惠同享管理 (3.11节) | menucode_2286 |

### 使用建议

**决策阶段**:
- 查询业务流程 (第6节) 理解完整营销逻辑
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

**基础URL**: `https://pos.meituan.com/web/marketing/home`

**路由格式**: `#/[module]/[function]`

**示例**:
- 首页: `#/rms-discount/marketing`
- 会员列表: `#/marketing/member/list`
- 创建卡券: `#/marketing/coupon/create`
- 活动数据: `#/marketing/campaign/data`

### CSS选择器策略

**一级菜单定位**:
```css
#menucode_928   /* 首页 */
#menucode_2220  /* 用户管理 */
#menucode_2221  /* 卡券管理 */
#menucode_2222  /* 大促活动 */
#menucode_2226  /* 数据报表 */
```

**辅助功能定位**:
```css
input[placeholder='请输入想搜索的功能']  /* 功能搜索 */
#marketing-navigator  /* 营销中心顶部导航 */
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
- **一级菜单**: 12个核心营销功能
- **二级菜单**: 52+子功能
- **预估页面**: 65+页面

### 数据来源

- **采集时间**: 2025-10-23
- **采集智能体**: E2-网站情报采集员
- **数据版本**: v1.0
- **完整度**: 营销中心模块100%覆盖

### 更新记录

- **v1.0** (2025-10-23): 初始版本，完整覆盖营销中心12个核心模块

---

## 🎓 最佳实践

### DO ✅

1. **查询前明确目标**: 明确是查询导航、功能、流程还是数据结构
2. **分层渐进**: 先查索引 → 再查导航 → 最后查详细文档
3. **结合使用**: navigation-tree.json (技术定位) + knowledge-base-report.md (业务理解)
4. **验证数据**: 参考业务规则验证配置正确性

### DON'T ❌

1. **避免盲目操作**: 未理解营销流程前不要直接自动化
2. **避免忽略验证**: 不要跳过字段验证规则检查
3. **避免硬编码**: 使用menucode而非硬编码CSS选择器
4. **避免忽略错误**: 参考错误处理机制确保操作可靠

---

## 📞 支持与反馈

### 关联智能体

- **M2**: 美团管家营销管理员 (主要使用者)
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
**适用智能体**: M2-美团管家营销管理员
**知识库类型**: 静态知识库 (Static Knowledge Base)
