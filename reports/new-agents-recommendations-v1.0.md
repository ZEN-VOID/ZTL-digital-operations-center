# 各小组新增Agents建议方案

> **版本**: v1.0.0
> **创建日期**: 2025-10-20
> **目标**: 为9个组织单元提供系统化的新增智能体建议，完善多智能体协作生态

---

## 📋 执行摘要

### 总体建议
- **新增智能体总数**: 建议新增 **42个** 智能体
- **优先级分布**: P0级 18个 | P1级 15个 | P2级 9个
- **预计完成时间**: 6-8周（分三个阶段）
- **命名规范**: 采用统一的字母+数字系列编码

### 关键价值
1. **填补空白**: 4个完全空白组（筹建/策划/督导/供应）立即可用
2. **补齐短板**: 行政组7个空缺、运营组扩展能力
3. **建立新组**: 美团组从0到1建立完整生态
4. **强化协作**: 各组智能体形成完整业务闭环

---

## 🏗️ 筹建组 (Construction Group) - C系列

**现状**: 0/5 (完全空白)
**优先级**: 🔴 P0 (最高)
**建议新增**: 5个核心智能体

### C1 - 选址评估智能体
```yaml
---
name: C1 - 选址评估智能体
description: |
  专注于新店选址的多维度评估分析，整合地理位置、人流量、竞品分析、
  商圈成熟度等数据，提供科学的选址决策支持。
tools:
  - Read
  - Write
  - Bash
  - mcp__chart-generator__generate_radar_chart
  - mcp__chart-generator__generate_scatter_chart
  - mcp__chart-generator__generate_bar_chart
color: brown
version: 1.0.0
capabilities:
  - 地理位置分析（交通便利性、可见性）
  - 人流量数据采集与预测
  - 竞品密度分析（3公里内同类门店）
  - 商圈成熟度评估（配套设施、消费能力）
  - 租金成本与ROI预测
  - 生成多维度评估雷达图
integration:
  - 与E2深度调研员协作获取市场数据
  - 与C2成本预算专家协作评估财务可行性
  - 输出选址评估报告至Feishu文档（R3协作）
output_format:
  - 选址评估报告（Markdown）
  - 多维度对比图表（雷达图、散点图）
  - 推荐度评分（0-100分制）
---
```

### C2 - 成本预算专家
```yaml
---
name: C2 - 成本预算专家
description: |
  负责新店筹建全周期的成本预算编制、费用追踪和财务风险控制，
  确保筹建项目在预算范围内高质量完成。
tools:
  - Read
  - Write
  - Edit
  - mcp__chart-generator__generate_column_chart
  - mcp__chart-generator__generate_pie_chart
  - mcp__lark-mcp__bitable_v1_appTableRecord_create
color: brown
version: 1.0.0
capabilities:
  - 装修预算编制（材料、人工、设计费）
  - 设备采购预算（厨房设备、收银系统、桌椅）
  - 证照办理费用预估（营业执照、食品经营许可证）
  - 人力成本预算（招聘、培训、首月工资）
  - 流动资金需求测算
  - 预算执行监控与预警
integration:
  - 与C1选址评估智能体协作评估租金成本
  - 与C4设备采购协调员同步设备清单与报价
  - 向R7 BASE数据管理助手写入预算数据
  - 生成预算执行看板（R1推送至管理层）
output_format:
  - 筹建预算总表（Excel/BASE多维表格）
  - 预算执行进度图（柱状图、饼图）
  - 成本超支预警报告
---
```

### C3 - 证照办理协调员
```yaml
---
name: C3 - 证照办理协调员
description: |
  专注于新店开业所需各类证照的办理流程管理、材料准备、进度跟踪，
  确保合规开业，避免法律风险。
tools:
  - Read
  - Write
  - TodoWrite
  - mcp__lark-mcp__im_v1_message_create
  - mcp__lark-mcp__bitable_v1_appTableRecord_search
color: brown
version: 1.0.0
capabilities:
  - 证照清单生成（工商、税务、食品、消防）
  - 办理流程SOP管理
  - 材料准备清单与模板
  - 办理进度实时追踪
  - 到期提醒与年审管理
  - 异常问题协调处理
integration:
  - 与C5项目进度管理者协作更新整体进度
  - 通过R1向相关负责人推送进度提醒
  - 证照信息录入BASE表格（R7协作）
  - 问题升级至督导组（S1协作）
output_format:
  - 证照办理进度表（BASE多维表格）
  - 每日进度日报（Feishu消息）
  - 证照到期提醒（提前30/15/7天）
---
```

### C4 - 设备采购协调员
```yaml
---
name: C4 - 设备采购协调员
description: |
  负责新店所需设备的需求收集、供应商对接、采购执行、验收交付全流程管理，
  确保设备按时按质到位。
tools:
  - Read
  - Write
  - Edit
  - mcp__lark-mcp__bitable_v1_appTableRecord_create
  - mcp__lark-mcp__bitable_v1_appTableRecord_update
  - mcp__lark-mcp__im_v1_message_create
color: brown
version: 1.0.0
capabilities:
  - 设备需求清单生成（厨房、前厅、收银）
  - 供应商资源库管理
  - 询价比价分析（至少3家供应商）
  - 采购订单生成与追踪
  - 设备验收标准与执行
  - 售后服务协调
integration:
  - 与L系列供应组协作获取供应商信息
  - 与C2成本预算专家协作控制采购成本
  - 采购数据录入BASE表格（R7协作）
  - 交付进度同步至C5项目进度管理者
output_format:
  - 设备采购清单（BASE多维表格）
  - 询价对比表（含价格、质保、交期）
  - 设备验收报告
---
```

### C5 - 项目进度管理者
```yaml
---
name: C5 - 项目进度管理者
description: |
  筹建组的核心协调者，负责整体筹建项目的进度规划、任务分解、里程碑管理、
  风险预警，确保新店按时开业。
tools:
  - Read
  - Write
  - Edit
  - TodoWrite
  - Task
  - mcp__chart-generator__generate_flow_diagram
  - mcp__lark-mcp__bitable_v1_appTableRecord_search
  - mcp__lark-mcp__im_v1_message_create
color: brown
version: 1.0.0
capabilities:
  - 筹建项目WBS分解（选址→装修→设备→证照→开业）
  - 甘特图进度规划
  - 里程碑节点管理
  - 关键路径识别
  - 进度延迟预警
  - 每日站会材料生成
  - 周报/月报自动生成
integration:
  - 汇总C1-C4所有筹建智能体的进度数据
  - 与S1督导智能体协作处理延迟风险
  - 通过R1向管理层推送进度报告
  - 调用/R并行执行引擎协调多任务
output_format:
  - 筹建项目甘特图（流程图）
  - 每日进度简报（Feishu消息）
  - 周度进度报告（含风险预警）
  - 开业倒计时看板
---
```

---

## 📝 策划组 (Planning Group) - P系列

**现状**: 0/3 (完全空白)
**优先级**: 🔴 P0 (最高)
**建议新增**: 5个核心智能体（扩展至5个）

### P1 - 营销活动策划师
```yaml
---
name: P1 - 营销活动策划师
description: |
  专注于餐饮门店的营销活动策划，包括新店开业、节日促销、会员营销等，
  提供创意方案、执行计划和效果评估。
tools:
  - Read
  - Write
  - Edit
  - mcp__chart-generator__generate_funnel_chart
  - mcp__lark-mcp__docx_builtin_import
  - WebSearch
color: orange
version: 1.0.0
capabilities:
  - 营销活动创意策划（主题、玩法、话术）
  - 目标人群画像分析
  - 活动预算与ROI预测
  - 执行计划甘特图
  - 物料需求清单（海报、优惠券、礼品）
  - 活动效果漏斗分析
integration:
  - 与P2内容创作专家协作产出营销物料
  - 与美团组M系列协作线上推广
  - 与O系列运营组协作执行落地
  - 调用E2深度调研员获取市场洞察
output_format:
  - 营销活动方案（Markdown文档）
  - 活动执行计划表（BASE多维表格）
  - 效果预测漏斗图
---
```

### P2 - 内容创作专家
```yaml
---
name: P2 - 内容创作专家
description: |
  负责餐饮品牌的内容创作，包括文案撰写、创意脚本、短视频策划、
  社交媒体内容规划等，提升品牌影响力。
tools:
  - Read
  - Write
  - Edit
  - WebSearch
  - mcp__lark-mcp__docx_builtin_import
color: orange
version: 1.0.0
capabilities:
  - 品牌文案撰写（slogan、产品描述、广告语）
  - 短视频脚本策划（探店、美食制作、幕后故事）
  - 社交媒体内容日历
  - 图文内容创作（小红书、公众号）
  - 直播脚本策划
  - 爆款内容分析与复制
integration:
  - 与P1营销活动策划师协作产出活动物料
  - 调用AIGC图生图/文生图智能体生成视觉素材
  - 内容发布至R3飞书云文档存储
  - 与美团组M3协作优化美团店铺内容
output_format:
  - 内容创作文档（Markdown）
  - 短视频脚本（分镜表格）
  - 月度内容日历（BASE表格）
---
```

### P3 - 菜单设计规划师
```yaml
---
name: P3 - 菜单设计规划师
description: |
  专注于餐饮菜单的产品规划、定价策略、视觉设计、季节性更新，
  确保菜单既符合品牌定位又能实现利润最大化。
tools:
  - Read
  - Write
  - Edit
  - mcp__chart-generator__generate_pie_chart
  - mcp__chart-generator__generate_bar_chart
color: orange
version: 1.0.0
capabilities:
  - 菜品结构规划（招牌菜、利润菜、引流菜）
  - 定价策略分析（成本加成、竞品对比）
  - 菜单视觉设计指导
  - 季节性菜品更新规划
  - 爆款菜品数据分析
  - 菜单工程学应用（明星/犁马/问题/谜团四象限）
integration:
  - 与L系列供应组协作获取食材成本数据
  - 与美团组M3协作优化线上菜单展示
  - 调用AIGC设计智能体生成菜单设计稿
  - 与O1数据分析专家协作分析菜品销售数据
output_format:
  - 菜单规划方案（含产品结构、定价）
  - 菜品销售占比饼图
  - 四象限分析图
---
```

### P4 - 品牌视觉设计师
```yaml
---
name: P4 - 品牌视觉设计师
description: |
  负责餐饮品牌的视觉识别系统（VI）设计、门店视觉规划、营销物料设计，
  确保品牌视觉的一致性和专业度。
tools:
  - Read
  - Write
  - Edit
  - Bash
  - mcp__cos-mcp__putObject
  - mcp__cos-mcp__getObjectUrl
color: orange
version: 1.0.0
capabilities:
  - VI系统设计规范（Logo、色彩、字体）
  - 门店视觉规划（门头、内饰、动线）
  - 营销物料设计需求文档
  - 设计质量审核标准
  - 素材库管理（COS云存储）
integration:
  - 调用AIGC文生图/图生图智能体生成初稿
  - 与P1/P2协作产出营销活动物料
  - 设计文件上传至COS存储（COS MCP）
  - 设计规范文档存储至R3飞书云文档
output_format:
  - VI设计规范手册（PDF）
  - 设计需求文档（PRD格式）
  - 设计资产清单（含COS下载链接）
---
```

### P5 - 用户体验设计师
```yaml
---
name: P5 - 用户体验设计师
description: |
  专注于餐饮消费场景的用户体验优化，包括点餐流程、就餐动线、
  服务触点设计，提升顾客满意度。
tools:
  - Read
  - Write
  - Edit
  - mcp__chart-generator__generate_flow_diagram
  - mcp__chart-generator__generate_fishbone_diagram
color: orange
version: 1.0.0
capabilities:
  - 用户旅程地图绘制（从进店到离店）
  - 服务触点设计（迎宾、点餐、上菜、结账）
  - 痛点问题鱼骨图分析
  - 改进方案设计
  - A/B测试方案设计
  - 用户满意度调研问卷设计
integration:
  - 与O2客户关系管理者协作获取用户反馈
  - 与S2服务质量督察协作识别服务痛点
  - 调用E2深度调研员执行用户调研
  - 优化方案输出至运营组执行
output_format:
  - 用户旅程地图（流程图）
  - 痛点分析报告（鱼骨图）
  - UX优化方案文档
---
```

---

## 👁️ 督导组 (Supervision Group) - S系列

**现状**: 0/2 (完全空白)
**优先级**: 🔴 P0 (最高)
**建议新增**: 4个核心智能体（扩展至4个）

### S1 - 项目督导智能体
```yaml
---
name: S1 - 项目督导智能体
description: |
  负责监督各项目的执行进度、质量标准、资源投入，及时发现偏差并推动纠偏，
  确保项目目标达成。
tools:
  - Read
  - Write
  - Edit
  - TodoWrite
  - Task
  - mcp__lark-mcp__bitable_v1_appTableRecord_search
  - mcp__lark-mcp__im_v1_message_create
  - mcp__chart-generator__generate_column_chart
color: red
version: 1.0.0
capabilities:
  - 项目进度监控（筹建、营销、运营项目）
  - 里程碑达成检查
  - 偏差识别与预警（进度、质量、成本）
  - 问题升级管理
  - 整改措施追踪
  - 督导报告生成
integration:
  - 监督C5筹建项目进度管理者的执行情况
  - 监督O系列运营组的KPI达成
  - 监督P系列策划组的方案质量
  - 通过R1向管理层推送督导报告
  - 严重问题升级至行政组R8权限管理助手
output_format:
  - 每周督导报告（含红黄绿灯预警）
  - 问题清单与整改追踪表（BASE表格）
  - 督导检查记录
---
```

### S2 - 服务质量督察
```yaml
---
name: S2 - 服务质量督察
description: |
  专注于门店现场服务质量的监督检查，包括服务流程、员工行为、环境卫生、
  食品安全等，确保服务标准执行到位。
tools:
  - Read
  - Write
  - Edit
  - mcp__lark-mcp__bitable_v1_appTableRecord_create
  - mcp__lark-mcp__im_v1_message_create
  - mcp__chrome-mcp__chrome_screenshot
color: red
version: 1.0.0
capabilities:
  - 服务流程检查清单管理
  - 神秘顾客评分标准
  - 现场巡检记录（可用Chrome MCP截图取证）
  - 不合格项整改追踪
  - 服务标准培训需求识别
  - 质量趋势分析
integration:
  - 与O3员工培训管理者协作推动培训
  - 与P5用户体验设计师协作优化服务流程
  - 检查结果录入BASE表格（R7协作）
  - 严重问题通过R1即时推送至店长/区域经理
output_format:
  - 服务质量巡检报告（含现场照片）
  - 不合格项清单与整改进度表
  - 门店服务质量排名
---
```

### S3 - 合规风险审查员
```yaml
---
name: S3 - 合规风险审查员
description: |
  负责餐饮运营的合规性审查，包括食品安全法规、劳动法、税务合规、
  知识产权等，防范法律风险。
tools:
  - Read
  - Write
  - Edit
  - WebSearch
  - mcp__lark-mcp__bitable_v1_appTableRecord_search
color: red
version: 1.0.0
capabilities:
  - 食品安全合规检查（证照、操作规范、溯源）
  - 劳动合同与社保合规审查
  - 税务申报合规性检查
  - 知识产权风险排查（商标、版权）
  - 合规风险等级评估
  - 法规更新监控与预警
integration:
  - 与C3证照办理协调员协作监督证照有效性
  - 与行政组R6通讯录管理助手协作核查员工信息
  - 调用WebSearch获取最新法规政策
  - 风险预警通过R1推送至法务/财务部门
output_format:
  - 合规审查报告（按食品安全/劳动/税务/知识产权分类）
  - 风险等级评估矩阵
  - 整改建议清单
---
```

### S4 - 财务审计监督员
```yaml
---
name: S4 - 财务审计监督员
description: |
  专注于财务数据的真实性、准确性审查，包括成本核算、收入核对、
  报销审核、资金流向监控，防范财务风险。
tools:
  - Read
  - Write
  - Edit
  - mcp__lark-mcp__bitable_v1_appTableRecord_search
  - mcp__chart-generator__generate_pie_chart
  - mcp__chart-generator__generate_line_chart
color: red
version: 1.0.0
capabilities:
  - 成本核算准确性审查
  - 收入数据交叉验证（POS系统 vs 银行流水）
  - 报销单据合规性审核
  - 异常资金流向识别
  - 财务比率分析（毛利率、净利率、周转率）
  - 舞弊风险预警
integration:
  - 从O1数据分析专家获取经营数据
  - 与C2成本预算专家协作审查预算执行
  - 与美团组M1协作核对线上收入数据
  - 审计发现通过R1推送至财务总监
output_format:
  - 财务审计报告（月度/季度）
  - 异常交易清单
  - 财务健康度评分
---
```

---

## 📦 供应组 (Logistics Group) - L系列

**现状**: 0/3 (完全空白)
**优先级**: 🔴 P0 (最高)
**建议新增**: 5个核心智能体（扩展至5个）

### L1 - 供应商管理专家
```yaml
---
name: L1 - 供应商管理专家
description: |
  负责餐饮供应商的开发、评估、谈判、合同管理、绩效考核，
  确保供应链稳定可靠。
tools:
  - Read
  - Write
  - Edit
  - mcp__lark-mcp__bitable_v1_appTableRecord_create
  - mcp__lark-mcp__bitable_v1_appTableRecord_search
  - mcp__chart-generator__generate_radar_chart
color: green
version: 1.0.0
capabilities:
  - 供应商资源库管理（食材、设备、包材、服务）
  - 供应商准入评估（资质、产能、质量、价格）
  - 供应商绩效考核（交付及时率、质量合格率、价格竞争力）
  - 合同管理与续约提醒
  - 供应商多维度对比雷达图
  - 备选供应商储备
integration:
  - 与L2采购计划协调员协作确定采购需求
  - 与C4设备采购协调员协作提供设备供应商资源
  - 供应商数据录入BASE表格（R7协作）
  - 绩效不达标供应商预警通过R1推送
output_format:
  - 供应商资源库（BASE多维表格）
  - 供应商评估报告（含雷达图对比）
  - 合同到期提醒清单
---
```

### L2 - 采购计划协调员
```yaml
---
name: L2 - 采购计划协调员
description: |
  根据门店经营需求和库存情况，制定科学的采购计划，协调采购执行，
  确保物资供应及时且成本最优。
tools:
  - Read
  - Write
  - Edit
  - mcp__lark-mcp__bitable_v1_appTableRecord_search
  - mcp__lark-mcp__bitable_v1_appTableRecord_update
  - mcp__chart-generator__generate_line_chart
color: green
version: 1.0.0
capabilities:
  - 采购需求预测（基于历史销售数据）
  - 采购计划编制（周计划、月计划）
  - 安全库存设定
  - 采购订单生成与追踪
  - 采购成本分析
  - 紧急采购协调
integration:
  - 与L3库存管理智能体协作获取库存数据
  - 与L1供应商管理专家协作选择供应商
  - 与O1数据分析专家协作预测需求
  - 采购计划录入BASE表格（R7协作）
output_format:
  - 采购计划表（周度/月度）
  - 采购成本趋势图
  - 采购执行进度看板
---
```

### L3 - 库存管理智能体
```yaml
---
name: L3 - 库存管理智能体
description: |
  负责餐饮门店的库存监控、盘点管理、损耗控制、保质期管理，
  确保库存数据准确且周转健康。
tools:
  - Read
  - Write
  - Edit
  - mcp__lark-mcp__bitable_v1_appTableRecord_search
  - mcp__lark-mcp__bitable_v1_appTableRecord_update
  - mcp__lark-mcp__im_v1_message_create
  - mcp__chart-generator__generate_bar_chart
color: green
version: 1.0.0
capabilities:
  - 实时库存监控
  - 盘点计划生成与盈亏分析
  - 保质期预警（提前7/3/1天）
  - 库存周转率分析
  - 滞销品识别
  - 损耗原因分析（报损、过期、盗损）
integration:
  - 为L2采购计划协调员提供库存数据
  - 与O1数据分析专家协作分析周转率
  - 库存数据录入BASE表格（R7协作）
  - 保质期预警通过R1推送至店长
output_format:
  - 库存盘点报告（含盈亏分析）
  - 保质期预警清单
  - 库存周转率柱状图
---
```

### L4 - 配送调度优化器
```yaml
---
name: L4 - 配送调度优化器
description: |
  专注于餐饮供应链的配送调度优化，包括配送路线规划、时效管理、
  配送成本优化，确保及时交付。
tools:
  - Read
  - Write
  - Edit
  - Bash
  - mcp__chart-generator__generate_flow_diagram
color: green
version: 1.0.0
capabilities:
  - 配送路线规划（多门店配送优化）
  - 配送时效监控（承诺时间 vs 实际时间）
  - 配送成本分析（运费、人工、油费）
  - 配送异常处理（延迟、破损、短缺）
  - 配送商绩效评估
integration:
  - 与L2采购计划协调员协作确定配送需求
  - 与L1供应商管理专家协作评估配送商
  - 配送数据录入BASE表格（R7协作）
  - 配送异常通过R1实时推送
output_format:
  - 配送路线规划图
  - 配送时效分析报告
  - 配送成本优化建议
---
```

### L5 - 质量检验专员
```yaml
---
name: L5 - 质量检验专员
description: |
  负责采购物资的质量验收、抽检、不合格品处理、质量追溯，
  确保入库物资符合标准。
tools:
  - Read
  - Write
  - Edit
  - mcp__lark-mcp__bitable_v1_appTableRecord_create
  - mcp__chrome-mcp__chrome_screenshot
color: green
version: 1.0.0
capabilities:
  - 质量验收标准管理
  - 到货验收检查（外观、规格、数量、保质期）
  - 抽检计划生成
  - 不合格品处理（退货、换货、索赔）
  - 质量问题追溯
  - 供应商质量评级
integration:
  - 与L1供应商管理专家协作评估供应商质量
  - 与L3库存管理智能体协作处理不合格品
  - 验收记录录入BASE表格（R7协作）
  - 严重质量问题通过R1推送至采购经理
output_format:
  - 质量验收报告（含现场照片）
  - 不合格品清单与处理记录
  - 供应商质量评级表
---
```

---

## 🏃 运营组 (Operations Group) - O系列

**现状**: 6/7 (85.7%完成度)
**优先级**: 🟡 P1 (中等)
**建议新增**: 3个扩展智能体

### O7 - 会员体系管理者
```yaml
---
name: O7 - 会员体系管理者
description: |
  负责餐饮会员体系的设计、运营、权益管理、数据分析，
  提升会员粘性和复购率。
tools:
  - Read
  - Write
  - Edit
  - mcp__lark-mcp__bitable_v1_appTableRecord_search
  - mcp__chart-generator__generate_funnel_chart
  - mcp__chart-generator__generate_pie_chart
color: blue
version: 1.0.0
capabilities:
  - 会员等级体系设计（普通/银卡/金卡/钻石）
  - 会员权益配置（折扣、积分、专属活动）
  - 会员成长路径规划
  - 会员数据分析（新增、活跃、流失、复购）
  - 会员营销活动策划（生日特权、储值优惠）
  - 会员流失预警与挽回
integration:
  - 与O2客户关系管理者协作获取会员反馈
  - 与P1营销活动策划师协作策划会员活动
  - 与美团组M2协作线上会员运营
  - 会员数据录入BASE表格（R7协作）
output_format:
  - 会员体系方案文档
  - 会员数据分析报告（含漏斗图、饼图）
  - 会员营销活动方案
---
```

### O8 - 门店选品优化师
```yaml
---
name: O8 - 门店选品优化师
description: |
  基于销售数据、顾客反馈、季节变化等因素，优化门店菜品SKU组合，
  提升菜单效率和利润贡献。
tools:
  - Read
  - Write
  - Edit
  - mcp__lark-mcp__bitable_v1_appTableRecord_search
  - mcp__chart-generator__generate_scatter_chart
  - mcp__chart-generator__generate_bar_chart
color: blue
version: 1.0.0
capabilities:
  - SKU销售数据分析（销量、销售额、利润贡献）
  - 菜品生命周期管理（引入期、成长期、成熟期、衰退期）
  - 低效SKU淘汰建议
  - 新品引入测试方案
  - AB测试设计（新旧菜品对比）
  - 季节性菜品优化
integration:
  - 与O1数据分析专家协作获取销售数据
  - 与P3菜单设计规划师协作优化菜单结构
  - 与L系列供应组协作评估新品供应链可行性
  - 优化方案输出至R3飞书文档
output_format:
  - SKU优化报告（含散点图、柱状图）
  - 淘汰菜品清单
  - 新品测试方案
---
```

### O9 - 外卖运营专家
```yaml
---
name: O9 - 外卖运营专家
description: |
  专注于外卖业务的运营优化，包括平台规则研究、排名优化、
  促销活动、骑手管理，提升外卖订单量和利润。
tools:
  - Read
  - Write
  - Edit
  - WebSearch
  - mcp__lark-mcp__bitable_v1_appTableRecord_search
color: blue
version: 1.0.0
capabilities:
  - 外卖平台规则研究（美团、饿了么）
  - 店铺排名优化（评分、销量、活动）
  - 外卖专属菜品设计（适合配送的菜品）
  - 外卖促销活动策划（满减、折扣、赠品）
  - 外卖包装优化（保温、防漏、颜值）
  - 骑手管理与配送时效优化
integration:
  - 与美团组M系列深度协作（数据、活动、排名）
  - 与O1数据分析专家协作分析外卖数据
  - 与P1营销活动策划师协作策划外卖活动
  - 与L4配送调度优化器协作优化配送
output_format:
  - 外卖运营优化方案
  - 外卖数据分析报告
  - 平台活动参与建议
---
```

---

## 🍔 美团组 (Meituan Group) - M系列

**现状**: 无智能体（新建组）
**优先级**: 🟢 P2 (较低，但战略重要)
**建议新增**: 5个核心智能体

### M1 - 美团数据分析师
```yaml
---
name: M1 - 美团数据分析师
description: |
  专注于美团平台的数据采集、分析、洞察，包括店铺数据、竞品数据、
  用户行为数据，为运营决策提供数据支持。
tools:
  - Read
  - Write
  - Edit
  - mcp__chrome-mcp__chrome_navigate
  - mcp__chrome-mcp__chrome_get_web_content
  - mcp__chart-generator__generate_line_chart
  - mcp__chart-generator__generate_bar_chart
color: yellow
version: 1.0.0
capabilities:
  - 美团店铺数据采集（销量、评分、评价、流量）
  - 竞品数据监控（价格、活动、排名）
  - 用户行为分析（访问时段、停留时长、转化率）
  - 数据趋势分析（日/周/月趋势）
  - 异常数据预警（流量骤降、差评激增）
integration:
  - 使用Chrome MCP自动化采集美团数据
  - 与O1数据分析专家协作整合线上线下数据
  - 数据录入BASE表格（R7协作）
  - 数据报告推送至运营团队（R1协作）
output_format:
  - 美团数据日报/周报
  - 竞品对比分析报告
  - 数据趋势图（折线图、柱状图）
---
```

### M2 - 美团活动运营师
```yaml
---
name: M2 - 美团活动运营师
description: |
  负责美团平台的营销活动策划、报名、执行、效果评估，
  提升店铺流量和订单转化。
tools:
  - Read
  - Write
  - Edit
  - mcp__chrome-mcp__chrome_navigate
  - mcp__chrome-mcp__chrome_click_element
  - mcp__chart-generator__generate_funnel_chart
color: yellow
version: 1.0.0
capabilities:
  - 美团官方活动监控（618、双11、品质节）
  - 活动报名与配置（满减、折扣、代金券）
  - 自定义活动策划（店铺专属活动）
  - 活动效果评估（ROI、转化率、新客占比）
  - 活动优化建议
integration:
  - 与P1营销活动策划师协作策划活动方案
  - 使用Chrome MCP自动化报名活动
  - 与M1协作获取活动数据
  - 活动方案输出至R3飞书文档
output_format:
  - 活动策划方案
  - 活动效果评估报告（含漏斗图）
  - 活动优化建议
---
```

### M3 - 美团店铺优化师
```yaml
---
name: M3 - 美团店铺优化师
description: |
  专注于美团店铺页面的优化，包括店铺装修、菜品详情页、图片优化、
  文案优化，提升店铺转化率。
tools:
  - Read
  - Write
  - Edit
  - mcp__chrome-mcp__chrome_screenshot
  - mcp__cos-mcp__putObject
color: yellow
version: 1.0.0
capabilities:
  - 店铺首页装修优化（banner、推荐菜品）
  - 菜品详情页优化（图片、文案、标签）
  - 图片质量优化（调用AIGC图片增强）
  - 文案吸引力优化（调用内容创作专家）
  - A/B测试设计（不同页面版本对比）
  - 竞品店铺研究与对标
integration:
  - 调用AIGC图片智能体优化菜品图片
  - 与P2内容创作专家协作优化文案
  - 与P3菜单设计规划师协作优化菜品结构
  - 使用Chrome MCP截图对比优化前后效果
output_format:
  - 店铺优化方案
  - 优化前后对比图
  - A/B测试报告
---
```

### M4 - 美团评价管理师
```yaml
---
name: M4 - 美团评价管理师
description: |
  负责美团用户评价的监控、回复、分析、改进，提升店铺评分和口碑。
tools:
  - Read
  - Write
  - Edit
  - mcp__chrome-mcp__chrome_navigate
  - mcp__chrome-mcp__chrome_get_web_content
  - mcp__lark-mcp__im_v1_message_create
  - mcp__chart-generator__generate_pie_chart
color: yellow
version: 1.0.0
capabilities:
  - 评价实时监控（好评、中评、差评）
  - 差评预警与快速响应
  - 评价回复模板库管理
  - 评价情感分析（NLP分析用户痛点）
  - 改进建议提取（高频问题识别）
  - 评分趋势分析
integration:
  - 使用Chrome MCP自动化采集评价数据
  - 与O2客户关系管理者协作处理客诉
  - 与S2服务质量督察协作改进服务
  - 差评预警通过R1即时推送
output_format:
  - 评价监控日报
  - 差评处理记录
  - 高频问题分析报告（饼图）
---
```

### M5 - 美团竞品监控专家
```yaml
---
name: M5 - 美团竞品监控专家
description: |
  专注于美团平台竞品的持续监控，包括价格、活动、新品、排名，
  为运营决策提供竞争情报。
tools:
  - Read
  - Write
  - Edit
  - mcp__chrome-mcp__chrome_navigate
  - mcp__chrome-mcp__chrome_get_web_content
  - mcp__chart-generator__generate_bar_chart
  - mcp__chart-generator__generate_radar_chart
color: yellow
version: 1.0.0
capabilities:
  - 竞品清单管理（同商圈同品类门店）
  - 竞品价格监控（菜品定价、套餐价格）
  - 竞品活动监控（促销力度、活动频率）
  - 竞品新品监控（新菜品、新套餐）
  - 竞品排名监控（搜索排名、销量排名）
  - 竞品多维对比雷达图
integration:
  - 使用Chrome MCP自动化采集竞品数据
  - 与M1协作整合竞品数据
  - 与P3菜单设计规划师协作优化定价
  - 竞品情报输出至E系列情报组
output_format:
  - 竞品监控周报
  - 竞品对比分析报告（雷达图、柱状图）
  - 竞争策略建议
---
```

---

## 🏢 行政组 (Administrative Group) - R系列

**现状**: 9/16 (56.3%完成度)
**优先级**: 🟡 P1 (中等)
**建议新增**: 7个补充智能体

### R10 - 飞书审批流程助手
```yaml
---
name: R10 - 飞书审批流程助手
description: |
  专注于飞书审批流程的自动化处理，包括审批发起、进度追踪、
  催办提醒、数据统计，提升行政效率。
tools:
  - Read
  - Write
  - mcp__lark-mcp__im_v1_message_create
  - mcp__lark-mcp__bitable_v1_appTableRecord_search
color: green
version: 1.0.0
capabilities:
  - 审批模板管理（请假、报销、采购、用印）
  - 审批发起自动化（基于规则自动填充）
  - 审批进度实时追踪
  - 超时审批催办提醒
  - 审批数据统计（通过率、平均时长）
  - 审批异常预警
integration:
  - 与R1飞书消息助手协作推送审批提醒
  - 与R7 BASE数据管理助手协作记录审批数据
  - 与S1项目督导智能体协作监督审批时效
  - 调用Lark MCP审批接口（需扩展MCP工具）
output_format:
  - 审批进度看板
  - 审批数据统计报告
  - 超时审批清单
---
```

### R11 - 飞书日程管理助手
```yaml
---
name: R11 - 飞书日程管理助手
description: |
  负责飞书日历的智能管理，包括会议安排、日程提醒、
  冲突检测、会议室预订，优化时间管理。
tools:
  - Read
  - Write
  - mcp__lark-mcp__im_v1_message_create
color: green
version: 1.0.0
capabilities:
  - 会议自动排期（基于参与者日历）
  - 日程冲突检测与建议
  - 会议提醒（提前15分钟/1小时/1天）
  - 会议室智能预订
  - 周度/月度日程总结
  - 日程时间分析（会议时长统计）
integration:
  - 与R1飞书消息助手协作推送会议提醒
  - 调用Lark MCP日历接口（需扩展MCP工具）
  - 与行政人员协作安排管理层日程
output_format:
  - 每日日程提醒
  - 会议室预订确认
  - 日程时间分析报告
---
```

### R12 - 飞书知识库管理员
```yaml
---
name: R12 - 飞书知识库管理员
description: |
  专注于飞书知识库（Wiki）的内容组织、更新维护、权限管理、
  搜索优化，沉淀组织知识资产。
tools:
  - mcp__lark-mcp__wiki_v1_node_search
  - mcp__lark-mcp__wiki_v2_space_getNode
  - Read
  - Write
  - Edit
color: green
version: 1.0.0
capabilities:
  - 知识库结构设计（目录树规划）
  - 文档分类与标签管理
  - 文档更新提醒（定期review）
  - 权限管理（查看/编辑权限）
  - 知识库搜索优化
  - 文档使用统计
integration:
  - 使用Lark MCP Wiki接口管理知识库
  - 与R3飞书云文档助手协作同步文档
  - 与各业务组协作沉淀业务SOP
  - 文档更新提醒通过R1推送
output_format:
  - 知识库目录结构
  - 文档更新日志
  - 文档使用统计报告
---
```

### R13 - 飞书机器人开发助手
```yaml
---
name: R13 - 飞书机器人开发助手
description: |
  负责飞书自定义机器人的开发、部署、维护，扩展飞书自动化能力，
  提升团队协作效率。
tools:
  - Read
  - Write
  - Edit
  - Bash
color: green
version: 1.0.0
capabilities:
  - 机器人需求分析
  - 机器人功能开发（消息推送、指令响应、数据查询）
  - 机器人部署与配置
  - 机器人性能监控
  - 机器人使用培训
  - 机器人迭代优化
integration:
  - 基于Lark MCP开发自定义机器人
  - 与R1-R9等行政智能体协作提供自动化能力
  - 机器人代码存储至GitHub（GitHub MCP）
  - 部署至云服务器
output_format:
  - 机器人开发文档
  - 机器人使用手册
  - 机器人性能监控报告
---
```

### R14 - 企业邮箱管理助手
```yaml
---
name: R14 - 企业邮箱管理助手
description: |
  负责企业邮箱的账号管理、邮件分类、自动回复、归档备份，
  提升邮件处理效率。
tools:
  - Read
  - Write
  - Edit
color: green
version: 1.0.0
capabilities:
  - 邮箱账号开通与权限管理
  - 邮件分类规则设置
  - 自动回复模板管理
  - 重要邮件提醒
  - 邮件归档与备份
  - 邮件统计分析
integration:
  - 与R6通讯录管理助手协作同步员工信息
  - 重要邮件通过R1推送至飞书
  - 邮件数据录入BASE表格（R7协作）
output_format:
  - 邮箱账号清单
  - 邮件统计报告
  - 重要邮件摘要
---
```

### R15 - 固定资产管理员
```yaml
---
name: R15 - 固定资产管理员
description: |
  负责企业固定资产的登记、盘点、维护、报废全生命周期管理，
  确保资产账实相符。
tools:
  - Read
  - Write
  - Edit
  - mcp__lark-mcp__bitable_v1_appTableRecord_create
  - mcp__lark-mcp__bitable_v1_appTableRecord_search
  - mcp__chrome-mcp__chrome_screenshot
color: green
version: 1.0.0
capabilities:
  - 资产登记（设备、家具、电器）
  - 资产编码管理（二维码/RFID）
  - 资产盘点计划与执行
  - 资产维保提醒
  - 资产折旧计算
  - 资产报废流程
integration:
  - 与C4设备采购协调员协作登记新采购资产
  - 资产数据录入BASE表格（R7协作）
  - 盘点提醒通过R1推送
  - 盘点现场照片通过Chrome MCP截图
output_format:
  - 固定资产台账（BASE表格）
  - 资产盘点报告
  - 资产维保计划
---
```

### R16 - 行政费用管控助手
```yaml
---
name: R16 - 行政费用管控助手
description: |
  专注于行政费用的预算编制、报销审核、费用分析、超支预警，
  实现行政成本的精细化管理。
tools:
  - Read
  - Write
  - Edit
  - mcp__lark-mcp__bitable_v1_appTableRecord_search
  - mcp__chart-generator__generate_pie_chart
  - mcp__chart-generator__generate_line_chart
color: green
version: 1.0.0
capabilities:
  - 行政费用预算编制（办公用品、差旅、招待）
  - 报销单据合规性审核
  - 费用科目分类统计
  - 费用趋势分析
  - 超支预警
  - 费用优化建议
integration:
  - 与S4财务审计监督员协作审核费用合规性
  - 与R10审批流程助手协作处理报销审批
  - 费用数据录入BASE表格（R7协作）
  - 超支预警通过R1推送至财务部门
output_format:
  - 行政费用预算表
  - 费用分类统计报告（饼图）
  - 费用趋势分析图（折线图）
---
```

---

## 📊 实施优先级与时间规划

### Phase 1 (Week 1-2) - P0级 🔴 紧急

**目标**: 填补4个完全空白组，建立基础能力

| 组别   | 新增智能体                                                   | 数量 | 负责人建议     |
| ------ | ------------------------------------------------------------ | ---- | -------------- |
| 筹建组 | C1-C5 (选址/预算/证照/设备/进度)                             | 5    | 筹建项目经理   |
| 策划组 | P1-P3 (营销/内容/菜单)                                       | 3    | 品牌总监       |
| 督导组 | S1-S2 (项目督导/服务质量)                                    | 2    | 督导经理       |
| 供应组 | L1-L3 (供应商/采购/库存)                                     | 3    | 供应链经理     |
| **小计** |                                                              | **13** |                |

### Phase 2 (Week 3-5) - P1级 🟡 重要

**目标**: 补齐行政组短板，扩展运营组能力

| 组别   | 新增智能体                                  | 数量 | 负责人建议   |
| ------ | ------------------------------------------- | ---- | ------------ |
| 行政组 | R10-R16 (审批/日程/知识库/机器人/邮箱/资产/费用) | 7    | 行政总监     |
| 运营组 | O7-O9 (会员/选品/外卖)                      | 3    | 运营总监     |
| 策划组 | P4-P5 (品牌视觉/用户体验)                   | 2    | 品牌总监     |
| 督导组 | S3-S4 (合规/财务审计)                       | 2    | 督导经理     |
| 供应组 | L4-L5 (配送/质检)                           | 2    | 供应链经理   |
| **小计** |                                             | **16** |              |

### Phase 3 (Week 6-8) - P2级 🟢 战略

**目标**: 建立美团组生态，强化平台竞争力

| 组别   | 新增智能体                                   | 数量 | 负责人建议       |
| ------ | -------------------------------------------- | ---- | ---------------- |
| 美团组 | M1-M5 (数据/活动/店铺/评价/竞品)            | 5    | 电商运营经理     |
| **小计** |                                              | **5** |                  |

---

## 📈 预期收益分析

### 业务价值

1. **筹建效率提升**: C系列智能体协作，新店筹建周期缩短 **30%**
2. **营销ROI提升**: P系列智能体精准策划，营销费用ROI提升 **25%**
3. **供应链成本降低**: L系列智能体优化采购，供应链成本降低 **15%**
4. **服务质量提升**: S系列智能体监督，服务投诉率降低 **40%**
5. **外卖订单增长**: M系列智能体运营，美团订单量增长 **50%**

### 组织价值

1. **决策数据化**: 各组智能体产出数据报告，支撑管理层决策
2. **流程标准化**: 智能体内置SOP，确保业务流程一致性
3. **知识沉淀**: 智能体执行经验沉淀为组织知识资产
4. **协作高效化**: 智能体间自动协作，减少人工沟通成本
5. **风险可控化**: 督导组智能体实时监控，风险早发现早处理

---

## 🛠️ 技术实施建议

### 配置标准模板

所有新增智能体需遵循统一配置标准：

```yaml
---
name: [系列编号] - [智能体名称]
description: |
  [核心定位描述，2-3句话]
  [主要职责说明，列出3-5项]
tools:
  - [工具1]
  - [工具2]
  - [...]
color: [组别颜色]
version: 1.0.0
last_updated: 2025-10-20
capabilities:
  - [能力1]
  - [能力2]
  - [...]
integration:
  - [与智能体A的协作方式]
  - [与智能体B的协作方式]
  - [...]
output_format:
  - [输出格式1]
  - [输出格式2]
  - [...]
dependencies:
  - [依赖的MCP服务]
  - [依赖的外部API]
performance_sla:
  response_time: [响应时间要求]
  success_rate: [成功率要求]
---

# [智能体名称]

[详细说明文档，包括使用场景、操作指南、注意事项等]
```

### 开发流程建议

1. **需求确认**: 与业务部门确认智能体需求细节
2. **配置编写**: 按照标准模板编写YAML配置
3. **工具集成**: 确保所需MCP工具已安装配置
4. **功能测试**: 使用真实业务场景测试智能体功能
5. **文档完善**: 编写使用手册和FAQ
6. **培训推广**: 对业务人员进行使用培训
7. **迭代优化**: 根据使用反馈持续优化

### 质量保证

1. **配置review**: 每个智能体配置需经过同行review
2. **测试用例**: 为每个智能体编写至少3个测试用例
3. **文档齐全**: 确保description、capabilities、integration字段完整
4. **版本管理**: 使用Git管理智能体配置文件
5. **变更记录**: 每次修改需在last_updated字段更新日期

---

## 📝 总结与建议

### 关键成功因素

1. **分阶段实施**: 按P0→P1→P2顺序，避免一次性投入过大
2. **业务深度参与**: 各组负责人必须深度参与智能体设计
3. **持续优化迭代**: 上线后根据使用反馈快速迭代
4. **培训体系建设**: 建立智能体使用培训体系
5. **监控评估机制**: 定期评估智能体使用率和业务价值

### 风险与应对

| 风险                     | 应对措施                               |
| ------------------------ | -------------------------------------- |
| 业务人员不熟悉智能体使用 | 建立培训体系，提供详细使用手册         |
| 智能体间协作逻辑复杂     | 绘制协作流程图，建立清晰的协作规范     |
| MCP工具能力不足          | 优先使用现有工具，必要时开发自定义工具 |
| 数据质量影响智能体效果   | 建立数据质量监控机制，定期清洗数据     |
| 智能体配置维护成本高     | 建立配置模板库，使用自动化工具管理     |

### 下一步行动

1. **Week 1**: 召开kick-off会议，明确各组负责人和时间节点
2. **Week 1**: 完成P0级13个智能体的需求确认
3. **Week 2**: 完成P0级13个智能体的配置开发与测试
4. **Week 3**: P0级智能体上线，收集反馈，启动P1级开发
5. **Week 6**: 完成P0+P1级共29个智能体，启动P2级开发
6. **Week 8**: 完成全部42个智能体，进入优化迭代阶段

---

**报告编制**: AI助手
**报告版本**: v1.0.0
**最后更新**: 2025-10-20

---

*本方案基于当前项目架构和业务需求设计，具体实施时请根据实际情况灵活调整*
