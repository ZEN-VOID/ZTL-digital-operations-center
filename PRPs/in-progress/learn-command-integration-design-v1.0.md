# learn命令整合设计文档

> **版本**: v1.0.0
> **创建日期**: 2025-10-23
> **设计目标**: 整合ASDW四步学习系统为统一的learn命令,实现自动化学习循环和系统优化建议

---

## 📋 目录

1. [设计背景](#1-设计背景)
2. [核心原则](#2-核心原则)
3. [命令架构](#3-命令架构)
4. [执行流程](#4-执行流程)
5. [智能分析系统](#5-智能分析系统)
6. [日志系统设计](#6-日志系统设计)
7. [输出格式规范](#7-输出格式规范)
8. [迁移策略](#8-迁移策略)
9. [实施计划](#9-实施计划)
10. [验证标准](#10-验证标准)

---

## 1. 设计背景

### 1.1 当前ASDW系统分析

**现有命令结构**:

```yaml
/A - ASDW学习系统第一步 (What - 是什么):
  功能: 项目现状考察、目标识别
  输出: learning/{YYYY-MM-DD}/A_WHAT.md
  依赖: 无前置依赖
  版本: v2.1.0

/S - ASDW学习系统第二步 (Why - 为什么):
  功能: 内外因深度分析、问题根源定位
  输出: learning/{YYYY-MM-DD}/S_WHY.md
  依赖: 需要A_WHAT.md完成
  版本: v2.0.1

/D - ASDW学习系统第三步 (How - 怎么做):
  功能: 方法论研究、实践策略制定
  输出: learning/{YYYY-MM-DD}/D_HOW.md
  依赖: 需要A_WHAT.md和S_WHY.md完成
  版本: v2.1.0
  特性: 集成CONTEXT7 MCP实时文档检索

/W - ASDW学习系统第四步 (Wield - 整合执行):
  功能: 知识整合、优化实施
  输出: learning/{YYYY-MM-DD}/W_WIELD.md
  依赖: 需要A/S/D三步完成
  版本: v2.0.1
```

**核心特性**:
- ✅ 渐进式依赖链: A → S → D → W
- ✅ 日期驱动的文件夹管理
- ✅ 历史学习检测 (7天窗口)
- ✅ 结构化输出 (Markdown格式)
- ✅ 与项目配置深度集成

### 1.2 整合目标

**用户明确需求**:

```yaml
统一命令: /learn

执行模式:
  - 按顺序完整执行A→S→D→W全流程
  - 自动化依赖检查和流程编排

智能增强:
  - 智能分析是否需要优化或拓展学习目标
  - 思考是否需要更完善的日志系统

输出管理:
  - 阶段性产出物料保存于learning/
  - 保留历史学习记录和迭代轨迹

最终交付:
  - 针对agents/commands/hooks/skills的优化建议
  - 明确的行动清单: 增加、减少、优化
```

**设计挑战**:

1. **流程自动化**: 如何优雅地串联四个独立步骤?
2. **中断恢复**: 如何支持部分完成后的断点续传?
3. **智能分析**: 如何判断学习目标是否需要拓展?
4. **日志增强**: 如何设计更好的迭代追踪系统?
5. **建议生成**: 如何结构化输出系统优化建议?

---

## 2. 核心原则

### 2.1 ASDW学习模型保留

**核心哲学**: 保持ASDW四步学习模型的完整性

```yaml
What (是什么) - 观察现状:
  核心价值: 建立清晰的项目认知基线
  不可省略: 所有学习的基础

Why (为什么) - 分析原因:
  核心价值: 理解问题的本质和根源
  不可省略: 避免盲目优化

How (怎么做) - 研究方法:
  核心价值: 基于理论指导实践
  不可省略: 确保方案科学性

Wield (整合执行) - 知识转化:
  核心价值: 将学习成果转化为实际改进
  不可省略: 学习的最终目的
```

### 2.2 自动化优先原则

```yaml
默认行为:
  - 一键触发完整A→S→D→W流程
  - 自动依赖检查和前置条件验证
  - 自动创建日期目录和文件结构

可选中断:
  - 支持用户在任意阶段暂停审阅
  - 支持从中断点继续执行
  - 支持单步执行模式(调试用)
```

### 2.3 智能增强原则

```yaml
目标自适应:
  - 分析当前学习目标是否覆盖全面
  - 基于项目变化动态调整学习范围
  - 主动发现被忽略的优化机会

日志驱动迭代:
  - 完整记录每次学习循环的元数据
  - 追踪学习目标的演进历史
  - 建立学习效果的度量体系
```

### 2.4 可追溯性原则

```yaml
文件命名规范:
  learning/{YYYY-MM-DD}/
    ├── A_WHAT.md           # 现状分析
    ├── S_WHY.md            # 问题根因
    ├── D_HOW.md            # 方法论
    ├── W_WIELD.md          # 整合执行
    ├── OPTIMIZATION.md     # 系统优化建议
    └── METADATA.json       # 学习元数据

历史保留:
  - 所有历史学习记录永久保留
  - 支持跨时间段的学习轨迹分析
  - 支持知识演进的可视化
```

---

## 3. 命令架构

### 3.1 统一命令结构

```yaml
命令名称: /learn

命令类型:
  - 无参数: 完整执行A→S→D→W全流程
  - 带参数: 执行特定阶段或配置选项

参数设计:
  /learn              # 默认: 完整流程
  /learn step=what    # 单步执行: 仅执行What步骤
  /learn step=why     # 单步执行: 仅执行Why步骤
  /learn step=how     # 单步执行: 仅执行How步骤
  /learn step=wield   # 单步执行: 仅执行Wield步骤
  /learn continue     # 从上次中断点继续
  /learn review       # 审阅当天学习成果
  /learn history      # 查看历史学习记录
```

### 3.2 内部模块化

**设计思路**: learn命令内部保留ASDW四个功能模块,但作为统一流程的子模块

```yaml
learn.md结构:

  Section 1: 命令元数据
    - 版本号: v2.0.0
    - 描述: 统一学习系统
    - 参数说明

  Section 2: 执行流程控制
    - 参数解析逻辑
    - 依赖检查机制
    - 流程编排引擎

  Section 3: What模块 (现状考察)
    - 原A.md的核心功能
    - 四大功能保持不变

  Section 4: Why模块 (问题分析)
    - 原S.md的核心功能
    - 内外因分析框架

  Section 5: How模块 (方法论)
    - 原D.md的核心功能
    - CONTEXT7 MCP集成

  Section 6: Wield模块 (整合执行)
    - 原W.md的核心功能
    - 系统优化建议生成

  Section 7: 智能分析系统
    - 学习目标自适应分析
    - 日志系统改进建议

  Section 8: 日志与追踪系统
    - 元数据记录规范
    - 学习历史管理
```

### 3.3 文件输出结构

```yaml
learning/{YYYY-MM-DD}/

  WHAT.md:              # 现状分析 (原A_WHAT.md)
    内容: 项目概览、配置分析、工具评估、目标识别

  WHY.md:               # 问题根因 (原S_WHY.md)
    内容: 内外因分析、问题定位、根源诊断

  HOW.md:               # 方法论 (原D_HOW.md)
    内容: 方法论研究、策略制定、资源整合、实践指导

  WIELD.md:             # 整合执行 (原W_WIELD.md)
    内容: 知识整合、优化策略、实施方案、持续改进

  OPTIMIZATION.md:      # 新增: 系统优化建议
    内容:
      - Agents优化建议 (增加/减少/优化)
      - Commands优化建议
      - Hooks优化建议
      - Skills优化建议
      - 优先级排序和实施路线图

  METADATA.json:        # 新增: 学习元数据
    内容:
      - 学习日期和时长
      - 学习目标和范围
      - 完成度追踪
      - 智能分析结果
      - 上次学习的关联
```

---

## 4. 执行流程

### 4.1 完整流程模式 (默认)

```yaml
触发: /learn (无参数)

执行序列:

  Step 0: 前置检查
    □ 检查learning/目录是否存在
    □ 创建今日日期目录: learning/{YYYY-MM-DD}/
    □ 检查历史学习记录 (7天窗口)
    □ 如存在历史记录,加载上次学习的目标和发现

  Step 1: What模块 (现状考察)
    ├─ 读取CLAUDE.md (项目级)
    ├─ 读取~/.claude/CLAUDE.md (全局级)
    ├─ 扫描.claude/agents/目录
    ├─ 扫描.claude/commands/目录
    ├─ 扫描.claude/hooks/目录
    ├─ 扫描.claude/skills/目录
    ├─ 评估当前工具和配置状态
    ├─ 识别学习目标和改进机会
    └─ 输出: WHAT.md

    ⏸ 阶段暂停点: 询问用户是否继续到Why步骤

  Step 2: Why模块 (问题分析)
    ├─ 读取WHAT.md识别的问题
    ├─ 内因分析:
    │   ├─ 知识局限性
    │   ├─ 使用模式问题
    │   ├─ 思维方式限制
    │   └─ 资源管理不足
    ├─ 外因分析:
    │   ├─ 系统架构问题
    │   ├─ 工具功能限制
    │   ├─ 配置不合理
    │   └─ 协作流程缺陷
    └─ 输出: WHY.md

    ⏸ 阶段暂停点: 询问用户是否继续到How步骤

  Step 3: How模块 (方法论)
    ├─ 读取WHAT.md和WHY.md
    ├─ 针对每个问题研究解决方法:
    │   ├─ CONTEXT7 MCP检索相关文档
    │   ├─ 分析官方最佳实践
    │   ├─ 研究社区解决方案
    │   └─ 制定适配策略
    ├─ 输出四大功能:
    │   ├─ 方法论研究
    │   ├─ 策略制定
    │   ├─ 资源整合
    │   └─ 实践指导
    └─ 输出: HOW.md

    ⏸ 阶段暂停点: 询问用户是否继续到Wield步骤

  Step 4: Wield模块 (整合执行)
    ├─ 综合What/Why/How三步学习成果
    ├─ 知识整合:
    │   ├─ 关键洞察提炼
    │   ├─ 行动清单生成
    │   └─ 优先级排序
    ├─ 优化策略制定:
    │   ├─ Agents优化建议
    │   ├─ Commands优化建议
    │   ├─ Hooks优化建议
    │   └─ Skills优化建议
    ├─ 实施方案:
    │   ├─ 阶段1: 快速见效(1-2周)
    │   ├─ 阶段2: 核心改进(1-2月)
    │   └─ 阶段3: 长期优化
    └─ 输出: WIELD.md

  Step 5: 智能分析与增强
    ├─ 学习目标覆盖度分析
    ├─ 识别遗漏的优化机会
    ├─ 评估日志系统完善度
    └─ 生成改进建议

  Step 6: 生成系统优化建议
    ├─ 基于WIELD.md的优化策略
    ├─ 结构化为四大类别:
    │   ├─ Agents: 新增/删除/优化
    │   ├─ Commands: 新增/删除/优化
    │   ├─ Hooks: 新增/删除/优化
    │   └─ Skills: 新增/删除/优化
    ├─ 每项建议包含:
    │   ├─ 建议类型 (ADD/REMOVE/OPTIMIZE)
    │   ├─ 优先级 (HIGH/MEDIUM/LOW)
    │   ├─ 预期收益
    │   ├─ 实施难度
    │   └─ 具体步骤
    └─ 输出: OPTIMIZATION.md

  Step 7: 记录学习元数据
    ├─ 学习日期和时长
    ├─ 学习目标清单
    ├─ 完成的步骤
    ├─ 发现的问题数量
    ├─ 生成的建议数量
    ├─ 智能分析结果
    └─ 输出: METADATA.json

完成提示:
  "✅ 学习循环完成!

   📁 输出位置: learning/{YYYY-MM-DD}/
   📄 生成文件:
      - WHAT.md (现状分析)
      - WHY.md (问题根因)
      - HOW.md (方法论)
      - WIELD.md (整合执行)
      - OPTIMIZATION.md (系统优化建议)
      - METADATA.json (学习元数据)

   🎯 下一步建议:
      - 执行 /learn review 审阅学习成果
      - 根据OPTIMIZATION.md实施系统改进"
```

### 4.2 单步执行模式

```yaml
触发: /learn step=A|S|D|W

用途: 调试、单步审阅、逐步学习

执行逻辑:

  /learn step=what:
    - 执行What模块
    - 输出WHAT.md
    - 不自动进入Why步骤

  /learn step=why:
    - 前置检查: 验证WHAT.md存在
    - 执行Why模块
    - 输出WHY.md

  /learn step=how:
    - 前置检查: 验证WHAT.md和WHY.md存在
    - 执行How模块 (含CONTEXT7 MCP调用)
    - 输出HOW.md

  /learn step=wield:
    - 前置检查: 验证What/Why/How三个文件存在
    - 执行Wield模块
    - 输出WIELD.md + OPTIMIZATION.md + METADATA.json
```

### 4.3 断点续传模式

```yaml
触发: /learn continue

场景:
  - 完整流程在某个阶段中断
  - 用户审阅后希望继续执行

检测逻辑:

  检查今日目录: learning/{YYYY-MM-DD}/

  如果存在WHAT.md但不存在WHY.md:
    → 从Why步骤开始执行

  如果存在WHAT.md和WHY.md但不存在HOW.md:
    → 从How步骤开始执行

  如果存在What/Why/How但不存在WIELD.md:
    → 从Wield步骤开始执行

  如果所有文件都存在:
    → 提示: "今日学习已完成,执行 /learn review 查看成果"
```

### 4.4 审阅模式

```yaml
触发: /learn review

功能: 展示今日学习成果的结构化摘要

输出格式:

  📚 学习成果摘要 - {YYYY-MM-DD}

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  📊 学习元数据:
  ├─ 学习时长: {XX}分钟
  ├─ 完成步骤: A → S → D → W ✅
  ├─ 发现问题: {N}个
  └─ 生成建议: {M}条

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  🎯 核心发现 (WHAT.md):
  {提取3-5个关键发现}

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  🔍 问题根源 (WHY.md):
  {提取2-3个核心问题}

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  💡 方法论 (HOW.md):
  {提取2-3个关键策略}

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ✨ 系统优化建议 (OPTIMIZATION.md):

  Agents优化:
  ├─ 新增: {N}项
  ├─ 优化: {M}项
  └─ 删除: {K}项

  Commands优化:
  ├─ 新增: {N}项
  ├─ 优化: {M}项
  └─ 删除: {K}项

  Hooks优化:
  ├─ 新增: {N}项
  └─ 优化: {M}项

  Skills优化:
  ├─ 新增: {N}项
  ├─ 优化: {M}项
  └─ 删除: {K}项

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  📁 完整文件:
  - learning/{YYYY-MM-DD}/WHAT.md
  - learning/{YYYY-MM-DD}/WHY.md
  - learning/{YYYY-MM-DD}/HOW.md
  - learning/{YYYY-MM-DD}/WIELD.md
  - learning/{YYYY-MM-DD}/OPTIMIZATION.md
  - learning/{YYYY-MM-DD}/METADATA.json
```

### 4.5 历史查看模式

```yaml
触发: /learn history

功能: 展示历史学习记录和演进轨迹

输出格式:

  📖 学习历史记录

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  {最近7天记录}

  📅 2025-10-23 (今日)
  ├─ 学习目标: {简述}
  ├─ 核心发现: {1-2句总结}
  └─ 状态: ✅ 已完成

  📅 2025-10-20
  ├─ 学习目标: {简述}
  ├─ 核心发现: {1-2句总结}
  └─ 状态: ✅ 已完成

  📅 2025-10-18
  ├─ 学习目标: {简述}
  ├─ 核心发现: {1-2句总结}
  └─ 状态: ✅ 已完成

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  📊 学习统计:
  ├─ 总学习次数: {N}
  ├─ 发现问题总数: {M}
  ├─ 实施建议数: {K}
  └─ 平均学习间隔: {X}天

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  🔄 演进趋势:
  {分析学习目标的演进方向}

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  💡 下一步建议:
  - 基于历史趋势,建议下次学习聚焦: {领域}
  - 上次未实施的建议: {列出未完成的优化建议}
```

---

## 5. 智能分析系统

### 5.1 学习目标自适应分析

**触发时机**: 在W步骤完成后,生成OPTIMIZATION.md之前

**分析维度**:

```yaml
1. 目标覆盖度分析:

   检查项:
     □ 是否覆盖了所有四大主体 (agents/commands/hooks/skills)?
     □ 是否只关注了某一类问题而忽略其他?
     □ 是否遗漏了最近项目变化带来的新需求?

   输出:
     - 覆盖度百分比
     - 遗漏领域清单
     - 建议拓展的方向

2. 历史对比分析:

   检查项:
     □ 与上次学习相比,关注点是否有演进?
     □ 是否重复发现相同问题而未解决?
     □ 是否出现新的优化机会?

   输出:
     - 重复问题清单 (需要提高优先级)
     - 新兴问题清单
     - 学习目标演进趋势

3. 项目变化感知:

   检查项:
     □ 自上次学习后,agents/commands/hooks/skills是否有新增?
     □ 是否有被删除的组件?
     □ 是否有重大配置变更?

   方法:
     - 读取上次学习的METADATA.json
     - 对比当前文件结构
     - 识别delta变化

   输出:
     - 新增组件清单
     - 删除组件清单
     - 变更组件清单
     - 这些变化引发的新学习目标

4. 学习深度评估:

   检查项:
     □ 问题分析是否深入到根源?
     □ 方法论研究是否充分?
     □ 实施方案是否具体可行?

   输出:
     - 深度评分 (1-5分)
     - 浅层分析的领域
     - 建议深化的方向
```

**输出格式** (追加到OPTIMIZATION.md末尾):

```markdown
## 智能分析结果

### 📊 学习目标覆盖度

✅ 已覆盖领域:
- Agents优化 (覆盖度: 80%)
- Commands优化 (覆盖度: 90%)
- Skills优化 (覆盖度: 60%)

⚠️ 遗漏领域:
- Hooks优化 (未覆盖)
- Output-styles配置 (未覆盖)

💡 建议拓展目标:
1. 【高优先级】增加Hooks系统的学习和优化
2. 【中优先级】研究Output-styles的配置潜力
3. 【低优先级】探索与MCP服务器的深度集成

---

### 🔄 历史对比分析

📅 上次学习: 2025-10-20

🔁 重复问题 (需重点关注):
- 智能体协作效率低 (连续3次出现)
- Commands命名不规范 (连续2次出现)

🆕 新兴问题:
- Skills自动发现机制不够智能
- 日志系统缺乏结构化

📈 学习目标演进趋势:
从"功能完善"逐步转向"协作效率"和"智能化"

---

### 🔔 项目变化感知

自上次学习(2025-10-20)以来的变化:

➕ 新增组件:
- .claude/commands/MANUS.md (统一上下文管理)
- .claude/skills/执行引擎/MCP/playwright-mcp/html-to-ppt/

➖ 删除组件:
- .claude/commands/C.md
- .claude/commands/X.md
- .claude/commands/Z.md

🔧 变更组件:
- CLAUDE.md (命令数量: 26 → 24)
- B.md/G.md/M.md/N.md (交叉引用更新)

💡 变化引发的新学习目标:
1. 评估MANUS命令的实际效果
2. 研究是否有其他命令可以整合
3. 探索html-to-ppt技能包的应用场景

---

### 🎯 学习深度评估

综合深度评分: ⭐⭐⭐⭐ (4/5)

✅ 分析充分的领域:
- 命令系统架构 (深度: 5/5)
- Agents协作模式 (深度: 4/5)

⚠️ 分析浅层的领域:
- Hooks系统潜力 (深度: 2/5)
- Skills自动发现机制 (深度: 3/5)

💡 建议深化方向:
1. 深入研究Hooks的事件驱动自动化潜力
2. 探索Skills description字段的智能匹配算法
3. 分析MCP服务器的高级用法
```

### 5.2 日志系统完善度分析

**分析目标**: 评估当前日志系统是否足以支撑有效的学习迭代

**评估维度**:

```yaml
1. 元数据完整性:

   检查项:
     □ METADATA.json是否记录了足够的元信息?
     □ 是否缺少关键的追踪指标?

   当前METADATA.json字段:
     ✅ 学习日期
     ✅ 学习时长
     ✅ 学习目标
     ✅ 完成步骤
     ✅ 发现问题数量
     ✅ 生成建议数量
     ✅ 智能分析结果

   潜在增强字段:
     ⭐ 学习触发原因 (主动/被动)
     ⭐ 实施状态追踪 (建议是否被执行)
     ⭐ 学习效果评分 (1-5分)
     ⭐ 关联的PR/Commit (如有实施)

2. 可追溯性:

   检查项:
     □ 能否清晰追溯某个优化建议的来源学习?
     □ 能否追踪建议的实施状态?
     □ 能否分析哪些建议被采纳,哪些被忽略?

   当前机制:
     ✅ 日期目录清晰
     ✅ 文件命名规范
     ❌ 缺少建议实施追踪
     ❌ 缺少建议与实际变更的关联

3. 迭代支持:

   检查项:
     □ 能否基于历史日志优化下次学习?
     □ 能否识别学习盲区和重复问题?
     □ 能否度量学习效果?

   当前能力:
     ✅ 7天历史检测
     ✅ 历史目录保留
     ⚠️ 缺少结构化的历史分析工具
     ⚠️ 缺少学习效果的量化指标

4. 可视化潜力:

   检查项:
     □ 日志格式是否便于可视化?
     □ 是否支持生成学习趋势图表?

   当前格式:
     ✅ JSON元数据 (易于解析)
     ✅ Markdown内容 (人类可读)
     ❌ 缺少可视化脚本
     ❌ 缺少趋势分析工具
```

**改进建议输出** (追加到OPTIMIZATION.md):

```markdown
## 日志系统改进建议

### 📋 当前日志系统评估

✅ 优点:
- 文件结构清晰,易于查找
- JSON元数据便于程序化处理
- Markdown内容人类可读性好

⚠️ 不足:
- 缺少建议实施状态追踪
- 缺少学习效果量化指标
- 缺少可视化工具

---

### 🔧 改进方案

#### 方案1: 增强METADATA.json字段

```json
{
  "date": "2025-10-23",
  "duration_minutes": 45,
  "trigger_reason": "scheduled|manual|project_change",
  "learning_objectives": [...],
  "completed_steps": ["A", "S", "D", "W"],
  "problems_found": 12,
  "suggestions_generated": 15,
  "intelligent_analysis": {...},

  // 新增字段
  "effectiveness_score": 4.5,        // 学习效果自评分 (1-5)
  "implementation_tracking": {       // 建议实施追踪
    "implemented": 8,                // 已实施建议数
    "pending": 5,                    // 待实施建议数
    "rejected": 2                    // 已放弃建议数
  },
  "related_commits": [               // 关联的Git提交
    "abc123: 实施MANUS命令整合",
    "def456: 优化智能体协作流程"
  ],
  "previous_learning": "2025-10-20", // 上次学习日期
  "delta_analysis": {                // 与上次对比
    "new_problems": 3,
    "resolved_problems": 5,
    "recurring_problems": 2
  }
}
```

#### 方案2: 建议追踪系统

在OPTIMIZATION.md中,为每条建议增加追踪ID:

```markdown
### Agents优化建议

#### A-001 [HIGH] 新增M系列智能体协作模式优化

**建议类型**: OPTIMIZE
**优先级**: HIGH
**追踪ID**: A-001
**状态**: ⏳ PENDING
**预期收益**: 提升30%协作效率
**实施难度**: MEDIUM
**实施步骤**: [...]

---

#### A-002 [MEDIUM] 删除冗余的G5智能体

**建议类型**: REMOVE
**优先级**: MEDIUM
**追踪ID**: A-002
**状态**: ❌ REJECTED
**拒绝原因**: 经评估仍有使用场景
```

#### 方案3: 学习历史数据库

创建 `learning/HISTORY.jsonl` (JSON Lines格式):

```jsonl
{"date":"2025-10-23","objectives":[...],"problems":12,"suggestions":15,"score":4.5}
{"date":"2025-10-20","objectives":[...],"problems":10,"suggestions":12,"score":4.0}
{"date":"2025-10-18","objectives":[...],"problems":8,"suggestions":10,"score":3.5}
```

便于脚本化分析和可视化。

#### 方案4: 可视化脚本

创建 `scripts/learning-analytics.py`:

功能:
- 解析learning/目录下所有METADATA.json
- 生成学习趋势图表 (问题数、建议数、评分)
- 生成实施率统计 (建议采纳率)
- 生成热点领域分析 (哪类问题最频繁)

输出:
- `learning/ANALYTICS.md` (Markdown报告)
- `learning/charts/` (可选的图表PNG)

---

### 🎯 推荐实施顺序

1. **立即实施** (本次learn命令更新):
   - 增强METADATA.json字段
   - 为OPTIMIZATION.md建议添加追踪ID

2. **短期实施** (1周内):
   - 创建learning/HISTORY.jsonl
   - 开发learning-analytics.py脚本

3. **长期优化** (1个月内):
   - 建立建议实施状态的更新机制
   - 开发可视化Dashboard (可选)
```

---

## 6. 日志系统设计

### 6.1 METADATA.json规范 (增强版)

```json
{
  "version": "2.0.0",
  "date": "2025-10-23",
  "timestamp_start": "2025-10-23T14:30:00+08:00",
  "timestamp_end": "2025-10-23T15:15:00+08:00",
  "duration_minutes": 45,

  "trigger": {
    "type": "manual|scheduled|project_change|error_driven",
    "reason": "用户主动执行 /learn 命令"
  },

  "learning_scope": {
    "objectives": [
      "评估MANUS命令整合效果",
      "发现智能体协作瓶颈",
      "探索Skills自动发现优化"
    ],
    "focus_areas": ["commands", "agents", "skills"],
    "excluded_areas": []
  },

  "execution": {
    "completed_steps": ["A", "S", "D", "W"],
    "interrupted_at": null,
    "errors_encountered": []
  },

  "findings": {
    "problems_found": 12,
    "problems_by_category": {
      "agents": 4,
      "commands": 3,
      "hooks": 2,
      "skills": 3
    },
    "root_causes_identified": 8,
    "methodologies_researched": 5
  },

  "outputs": {
    "suggestions_generated": 15,
    "suggestions_by_type": {
      "ADD": 6,
      "REMOVE": 2,
      "OPTIMIZE": 7
    },
    "suggestions_by_priority": {
      "HIGH": 5,
      "MEDIUM": 7,
      "LOW": 3
    },
    "files_created": [
      "A_WHAT.md",
      "S_WHY.md",
      "D_HOW.md",
      "W_WIELD.md",
      "OPTIMIZATION.md",
      "METADATA.json"
    ]
  },

  "intelligent_analysis": {
    "coverage_score": 0.85,
    "depth_score": 4.0,
    "missing_areas": ["hooks", "output-styles"],
    "suggested_expansions": [
      "深入研究Hooks事件驱动自动化",
      "探索Output-styles配置潜力"
    ]
  },

  "historical_context": {
    "previous_learning_date": "2025-10-20",
    "days_since_last_learning": 3,
    "recurring_problems": [
      "智能体协作效率低",
      "Commands命名不规范"
    ],
    "new_problems": [
      "Skills自动发现不够智能",
      "日志系统结构化不足"
    ],
    "resolved_problems_count": 5
  },

  "implementation_tracking": {
    "total_suggestions": 15,
    "implemented": 0,
    "pending": 15,
    "rejected": 0,
    "implementation_rate": 0.0,
    "related_commits": [],
    "related_prs": []
  },

  "quality_metrics": {
    "self_assessment_score": 4.5,
    "completeness": 0.90,
    "actionability": 0.85,
    "estimated_impact": "HIGH"
  },

  "project_context": {
    "total_agents": 60,
    "total_commands": 24,
    "total_hooks": 3,
    "total_skills": 33,
    "project_version": "v2.0.0",
    "claude_code_version": "1.0+",
    "sonnet_version": "4.5"
  }
}
```

### 6.2 HISTORY.jsonl设计

**位置**: `learning/HISTORY.jsonl`

**格式**: JSON Lines (每行一个JSON对象)

**字段** (精简版METADATA):

```jsonl
{"date":"2025-10-23","duration":45,"problems":12,"suggestions":15,"coverage":0.85,"depth":4.0,"score":4.5,"implemented":0,"rate":0.0}
{"date":"2025-10-20","duration":38,"problems":10,"suggestions":12,"coverage":0.75,"depth":3.5,"score":4.0,"implemented":8,"rate":0.67}
{"date":"2025-10-18","duration":42,"problems":8,"suggestions":10,"coverage":0.80,"depth":4.0,"score":3.5,"implemented":7,"rate":0.70}
```

**用途**:
- 快速加载历史记录(无需解析多个JSON文件)
- 支持流式追加写入
- 便于数据分析和可视化脚本

### 6.3 建议追踪ID规范

**格式**: `[类别]-[序号]`

```yaml
类别代码:
  A - Agents建议
  C - Commands建议
  H - Hooks建议
  S - Skills建议

序号: 三位数字,从001开始

示例:
  A-001: 第1条Agents建议
  C-012: 第12条Commands建议
  H-003: 第3条Hooks建议
  S-025: 第25条Skills建议
```

**追踪状态标识**:

```yaml
⏳ PENDING:   待实施
🔄 IN_PROGRESS: 实施中
✅ IMPLEMENTED: 已实施
❌ REJECTED:    已拒绝
🔁 RECURRING:   重复出现(需提高优先级)
```

**OPTIMIZATION.md中的使用**:

```markdown
### Agents优化建议

#### A-001 [HIGH] ⏳ 新增M系列智能体协作模式优化

**追踪ID**: A-001
**状态**: ⏳ PENDING
**创建日期**: 2025-10-23
**建议类型**: OPTIMIZE
**优先级**: HIGH

**预期收益**:
- 提升30%协作效率
- 减少20%重复工作

**实施难度**: MEDIUM

**具体步骤**:
1. 分析M1-M4协作瓶颈
2. 设计统一协作接口
3. 更新智能体配置

**关联问题**: S_WHY.md第3节

---

#### A-002 [MEDIUM] ✅ 删除冗余的G5智能体

**追踪ID**: A-002
**状态**: ✅ IMPLEMENTED
**创建日期**: 2025-10-20
**实施日期**: 2025-10-22
**建议类型**: REMOVE
**优先级**: MEDIUM

**实施记录**:
- Commit: abc123def456
- PR: #42
- 实际收益: 简化系统结构,减少维护成本
```

---

## 7. 输出格式规范

### 7.1 OPTIMIZATION.md完整模板

```markdown
# 系统优化建议

> **生成日期**: {YYYY-MM-DD}
> **学习循环**: ASDW完整流程
> **分析深度**: ⭐⭐⭐⭐ (4/5)
> **覆盖范围**: agents, commands, hooks, skills

---

## 📋 目录

1. [优化建议总览](#优化建议总览)
2. [Agents优化建议](#agents优化建议)
3. [Commands优化建议](#commands优化建议)
4. [Hooks优化建议](#hooks优化建议)
5. [Skills优化建议](#skills优化建议)
6. [实施路线图](#实施路线图)
7. [智能分析结果](#智能分析结果)
8. [日志系统改进建议](#日志系统改进建议)

---

## 优化建议总览

### 📊 统计概览

| 类别     | 新增 (ADD) | 优化 (OPTIMIZE) | 删除 (REMOVE) | 总计 |
|----------|------------|-----------------|---------------|------|
| Agents   | 3          | 5               | 1             | 9    |
| Commands | 2          | 3               | 0             | 5    |
| Hooks    | 1          | 1               | 0             | 2    |
| Skills   | 4          | 2               | 1             | 7    |
| **总计** | **10**     | **11**          | **2**         | **23** |

### 🎯 优先级分布

- 🔴 HIGH: 8条 (35%)
- 🟡 MEDIUM: 10条 (43%)
- 🟢 LOW: 5条 (22%)

### ⏱️ 预估实施时长

- 快速见效 (1-2周): 10条
- 核心改进 (1-2月): 8条
- 长期优化 (3月+): 5条

---

## Agents优化建议

### 🆕 新增建议 (ADD)

#### A-001 [HIGH] ⏳ 新增M系列协作优化智能体

**建议类型**: ADD
**优先级**: HIGH
**追踪ID**: A-001
**状态**: ⏳ PENDING
**预估工作量**: 3-5天

**背景**:
M1-M4智能体在协作时存在信息传递效率低、重复工作多的问题。

**建议内容**:
新增一个专门的"M系列协作优化智能体",负责:
- 分析M1-M4的协作模式
- 设计统一的数据接口
- 优化任务编排逻辑

**预期收益**:
- 协作效率提升30%
- 重复工作减少20%
- 用户体验改善

**实施难度**: MEDIUM

**具体步骤**:
1. 研究M1-M4当前协作模式
2. 设计协作接口规范
3. 创建新智能体配置文件
4. 更新M1-M4引用新协作模式
5. 测试验证

**关联分析**:
- 问题来源: WHY.md 第3节
- 方法论参考: HOW.md 第2节

---

#### A-002 [MEDIUM] ⏳ 新增E系列并行调度智能体

{类似结构...}

---

### ⚡ 优化建议 (OPTIMIZE)

#### A-010 [HIGH] 🔄 优化GG战略规划总监的任务分解能力

**建议类型**: OPTIMIZE
**优先级**: HIGH
**追踪ID**: A-010
**状态**: 🔄 IN_PROGRESS
**预估工作量**: 2-3天

**当前问题**:
GG在分解复杂战略任务时,颗粒度不够细,导致G1-G7执行困难。

**优化方案**:
1. 增强GG的任务分解算法
2. 引入SMART原则验证
3. 添加任务依赖关系图

**预期收益**:
- 任务执行成功率提升40%
- 返工率降低30%

**实施难度**: MEDIUM

**具体步骤**:
1. 分析GG当前任务分解逻辑
2. 设计新的分解算法
3. 更新GG配置文件
4. 编写验证测试用例
5. 回归测试

**关联分析**:
- 问题来源: WHAT.md 第2节
- 方法论参考: HOW.md 第4节

---

### 🗑️ 删除建议 (REMOVE)

#### A-020 [LOW] ❌ 删除G5加盟政策设计师

**建议类型**: REMOVE
**优先级**: LOW
**追踪ID**: A-020
**状态**: ❌ REJECTED
**拒绝原因**: 经评估仍有加盟业务需求

{或者如果确实要删除:}

**建议类型**: REMOVE
**优先级**: LOW
**追踪ID**: A-020
**状态**: ⏳ PENDING
**预估工作量**: 1天

**删除理由**:
- 使用频率极低 (过去3个月0次调用)
- 功能可被G0+外部咨询替代
- 维护成本不值得

**影响分析**:
- 无直接依赖的其他智能体
- 可安全删除

**具体步骤**:
1. 确认无依赖引用
2. 删除 .claude/agents/战略组/G5-加盟政策设计师.md
3. 更新CLAUDE.md中的agents列表
4. 更新GG的调度逻辑

---

## Commands优化建议

{类似结构,包含C-001, C-002等建议}

---

## Hooks优化建议

### 🆕 新增建议 (ADD)

#### H-001 [MEDIUM] ⏳ 新增ToolUse Hook进行工具使用审计

**建议类型**: ADD
**优先级**: MEDIUM
**追踪ID**: H-001
**状态**: ⏳ PENDING

**背景**:
当前缺少对工具使用的审计机制,难以分析工具调用模式和优化机会。

**建议内容**:
新增ToolUse Hook,在每次工具调用前记录:
- 调用时间戳
- 工具名称和参数
- 调用上下文

输出到: `logs/tool-usage.jsonl`

**预期收益**:
- 建立工具使用数据库
- 发现工具使用模式
- 识别优化机会

**实施难度**: LOW

**具体步骤**:
1. 创建 .claude/hooks/tool_use_audit.py
2. 实现日志记录逻辑
3. 配置 settings.json 的 hooks.ToolUse
4. 测试验证

**关联分析**:
- 问题来源: WHY.md 第5节
- 方法论参考: HOW.md 第6节

---

## Skills优化建议

{类似结构,包含S-001, S-002等建议}

---

## 实施路线图

### 🏃 阶段1: 快速见效 (1-2周)

**目标**: 解决明显的痛点,快速提升体验

**任务清单**:

| ID    | 类别     | 建议描述                     | 优先级 | 预估工作量 |
|-------|----------|------------------------------|--------|-----------|
| C-003 | Commands | 优化/M命令的扫描速度         | HIGH   | 1天       |
| A-015 | Agents   | 修复E2网站采集的超时问题     | HIGH   | 2天       |
| S-008 | Skills   | 优化AIGC text-to-image缓存   | MEDIUM | 1天       |
| H-002 | Hooks    | 优化Stop Hook的响应速度      | MEDIUM | 1天       |
| ...   | ...      | ...                          | ...    | ...       |

**预期收益**:
- 明显减少等待时间
- 提升用户体验满意度

---

### 🚀 阶段2: 核心改进 (1-2月)

**目标**: 提升系统能力,解决结构性问题

**任务清单**:

| ID    | 类别     | 建议描述                     | 优先级 | 预估工作量 |
|-------|----------|------------------------------|--------|-----------|
| A-001 | Agents   | 新增M系列协作优化智能体      | HIGH   | 5天       |
| A-010 | Agents   | 优化GG的任务分解能力         | HIGH   | 3天       |
| C-001 | Commands | 新增/learn统一学习命令       | HIGH   | 7天       |
| S-005 | Skills   | 开发learning-analytics工具   | MEDIUM | 4天       |
| ...   | ...      | ...                          | ...    | ...       |

**预期收益**:
- 协作效率提升30%+
- 学习迭代能力提升50%+

---

### 🎯 阶段3: 长期优化 (3月+)

**目标**: 探索性优化,提升系统智能化水平

**任务清单**:

| ID    | 类别     | 建议描述                         | 优先级 | 预估工作量 |
|-------|----------|----------------------------------|--------|-----------|
| A-018 | Agents   | 研究智能体自适应学习机制         | LOW    | 2周       |
| S-012 | Skills   | 开发Skills自动发现优化算法       | LOW    | 2周       |
| H-003 | Hooks    | 探索多Hook协同编排               | LOW    | 1周       |
| ...   | ...      | ...                              | ...    | ...       |

**预期收益**:
- 系统自适应能力提升
- 减少人工干预需求

---

## 智能分析结果

{此部分内容在第5.1节已详细设计}

---

## 日志系统改进建议

{此部分内容在第5.2节已详细设计}

---

## 📎 附录

### 文件清单

- `A_WHAT.md` - 现状分析
- `S_WHY.md` - 问题根因
- `D_HOW.md` - 方法论研究
- `W_WIELD.md` - 整合执行
- `OPTIMIZATION.md` - 本文件
- `METADATA.json` - 学习元数据

### 下一步行动

1. 审阅本优化建议文档
2. 选择优先实施的建议
3. 使用 /E 或 /F 命令创建PRP
4. 按路线图分阶段实施
5. 更新METADATA.json的implementation_tracking

### 反馈与迭代

- 如需调整优先级,请更新对应建议的状态
- 如需补充新建议,请使用追踪ID格式添加
- 下次 /learn 执行时,将自动对比实施进展
```

### 7.2 WHAT.md输出格式 (保留原格式)

保持原有结构,无需变更:

```markdown
# 学习系统 - What (现状考察)

> **日期**: {YYYY-MM-DD}
> **版本**: v2.0.0

---

## 1. 项目概览

{项目基本信息、技术栈、业务定位}

---

## 2. 核心配置分析

### 2.1 CLAUDE.md (项目级)

{分析项目级配置}

### 2.2 ~/.claude/CLAUDE.md (全局级)

{分析全局级配置}

---

## 3. 智能体系统现状

{agents/目录分析}

---

## 4. 命令系统现状

{commands/目录分析}

---

## 5. Hooks系统现状

{hooks/配置分析}

---

## 6. Skills系统现状

{skills/目录分析}

---

## 7. 工具与资源评估

{MCP服务器、插件、工具评估}

---

## 8. 学习目标识别

{基于上述分析,识别需要深入学习和优化的目标}
```

### 7.3 其他文件格式

- **WHY.md**: 保留原格式
- **HOW.md**: 保留原格式
- **WIELD.md**: 保留原格式

---

## 8. 迁移策略

### 8.1 迁移步骤

```yaml
Phase 1: 创建learn.md (预计3-5天)

  任务:
    1. 基于本设计文档编写完整的learn.md
    2. 整合A/S/D/W四个命令的核心功能
    3. 实现流程控制和参数解析逻辑
    4. 实现智能分析系统
    5. 实现日志系统增强
    6. 实现OPTIMIZATION.md生成逻辑

  输出:
    - .claude/commands/learn.md (v2.0.0)

Phase 2: 测试验证 (预计1-2天)

  测试用例:
    □ /learn (完整流程)
    □ /learn step=A (单步执行)
    □ /learn step=S (依赖检查)
    □ /learn step=D (CONTEXT7 MCP调用)
    □ /learn step=W (优化建议生成)
    □ /learn continue (断点续传)
    □ /learn review (审阅模式)
    □ /learn history (历史查看)

  验证:
    □ 所有文件正确生成
    □ METADATA.json字段完整
    □ OPTIMIZATION.md格式正确
    □ 智能分析结果合理
    □ 历史检测正常工作

Phase 3: 迁移通知 (预计1天)

  任务:
    1. 在A/S/D/W四个命令文件顶部添加弃用通知
    2. 引导用户使用新的/learn命令

  弃用通知格式:
    ```markdown
    ---
    description: ⚠️ 本命令已整合到 /learn 统一学习系统
    ---

    # ⚠️ 弃用通知

    本命令 (`/A`) 已整合到 `/learn` 统一学习系统。

    **新用法**:
    - 完整学习流程: `/learn` (自动执行A→S→D→W)
    - 仅执行A步骤: `/learn step=A`

    **迁移时间**: 2025-10-25

    **保留期**: 本命令将在1个月后(2025-11-25)删除

    ---

    {原命令内容保留,作为过渡期兼容}
    ```

Phase 4: 更新交叉引用 (预计半天)

  需要更新的文件:
    - CLAUDE.md (项目级)
      - 更新命令数量: 24 → 21 (删除A/S/D/W, 新增learn)
      - 更新"上下文与学习管理类"命令清单

    - ~/.claude/CLAUDE.md (全局级)
      - 如有引用ASDW,同步更新

    - 其他commands/*.md (如B/M/N等)
      - 更新"相关指令"章节的引用

Phase 5: 观察期 (1个月)

  任务:
    - 保留A/S/D/W命令文件(标记为弃用)
    - 监控/learn命令的使用情况
    - 收集用户反馈
    - 修复发现的问题

  观察指标:
    - /learn命令调用次数
    - 完整流程完成率
    - 用户满意度
    - 发现的bug数量

Phase 6: 正式删除 (1个月后)

  任务:
    1. 删除A.md, S.md, D.md, W.md
    2. 更新所有引用
    3. 发布正式版本公告

  命令:
    ```bash
    git rm .claude/commands/A.md
    git rm .claude/commands/S.md
    git rm .claude/commands/D.md
    git rm .claude/commands/W.md
    git commit -m "chore: 移除已弃用的ASDW命令,统一使用/learn"
    ```
```

### 8.2 兼容性保障

**过渡期策略** (1个月):

```yaml
用户体验:
  - A/S/D/W命令保持可用
  - 顶部显示弃用警告和迁移指引
  - 不影响现有工作流

文档更新:
  - CLAUDE.md明确标注新旧命令
  - README.md添加迁移指南
  - 发布更新公告

数据兼容:
  - learning/目录结构不变
  - 历史学习记录格式兼容
  - METADATA.json向后兼容
```

---

## 9. 实施计划

### 9.1 时间表

```yaml
Week 1 (2025-10-23 ~ 2025-10-29):
  Day 1-3: 编写learn.md核心功能
    - 流程控制逻辑
    - A/S/D/W模块整合
    - 参数解析

  Day 4-5: 实现智能分析和日志系统
    - 学习目标自适应分析
    - METADATA.json增强
    - HISTORY.jsonl实现

  Day 6-7: 实现OPTIMIZATION.md生成
    - 建议分类和格式化
    - 追踪ID生成
    - 实施路线图生成

Week 2 (2025-10-30 ~ 2025-11-05):
  Day 1-2: 测试验证
    - 8个测试用例全覆盖
    - bug修复

  Day 3: 更新交叉引用
    - CLAUDE.md更新
    - 其他commands更新

  Day 4-5: 添加弃用通知
    - 更新A/S/D/W四个文件
    - 编写迁移指南

  Day 6-7: 文档和公告
    - 更新README.md
    - 发布更新公告

Week 3-6 (观察期):
  - 监控使用情况
  - 收集用户反馈
  - 迭代优化

Week 7 (正式删除):
  - 删除A/S/D/W命令
  - 清理所有弃用标记
  - 发布v2.1.0版本
```

### 9.2 人力资源

```yaml
角色分工:
  - Claude (AI助手): 主要开发者
    - 编写learn.md
    - 实现所有功能
    - 测试验证

  - 用户 (项目所有者): 审阅者
    - 审阅设计文档
    - 测试新命令
    - 提供反馈

预估工作量:
  - 开发: 5-7天
  - 测试: 1-2天
  - 文档: 1天
  - 观察期: 1个月 (后台)
  - 总计: 约2个月 (包含观察期)
```

---

## 10. 验证标准

### 10.1 功能验证

```yaml
核心功能:
  □ /learn 完整执行A→S→D→W流程
  □ 自动创建learning/{YYYY-MM-DD}/目录
  □ 生成所有6个文件 (A/S/D/W/OPTIMIZATION/METADATA)
  □ METADATA.json包含所有增强字段
  □ HISTORY.jsonl正确追加记录

参数功能:
  □ /learn step=A/S/D/W 单步执行正常
  □ /learn continue 断点续传正确
  □ /learn review 审阅输出格式正确
  □ /learn history 历史展示完整

智能分析:
  □ 学习目标覆盖度分析准确
  □ 历史对比分析有效
  □ 项目变化感知准确
  □ 学习深度评估合理

优化建议:
  □ OPTIMIZATION.md格式规范
  □ 建议追踪ID唯一且连续
  □ 优先级分类合理
  □ 实施路线图清晰

依赖检查:
  □ S步骤检查A_WHAT.md存在
  □ D步骤检查A和S存在
  □ W步骤检查A/S/D存在
  □ continue模式检测当前进度准确
```

### 10.2 质量验证

```yaml
代码质量:
  □ 符合Markdown语法规范
  □ YAML frontmatter格式正确
  □ 无拼写和语法错误
  □ 代码块语言标识完整

用户体验:
  □ 命令响应时间 < 3秒 (除D步骤的MCP调用)
  □ 错误提示清晰友好
  □ 进度反馈及时
  □ 输出格式美观易读

文档完整性:
  □ learn.md包含完整使用说明
  □ 每个参数都有示例
  □ 常见问题有FAQ
  □ 与A/S/D/W的差异说明清楚

向后兼容:
  □ 历史learning/目录可正常访问
  □ 旧METADATA.json格式兼容
  □ 不影响现有工作流
```

### 10.3 性能验证

```yaml
执行时间:
  □ A步骤 (现状考察) < 30秒
  □ S步骤 (问题分析) < 20秒
  □ D步骤 (方法论) < 60秒 (含MCP调用)
  □ W步骤 (整合执行) < 40秒
  □ 完整流程 < 3分钟

资源消耗:
  □ 生成文件总大小 < 500KB
  □ METADATA.json < 10KB
  □ HISTORY.jsonl单行 < 1KB

缓存效率:
  □ 历史检测使用文件缓存
  □ CONTEXT7调用结果缓存
  □ 减少重复读取
```

---

## 附录

### A. 参考文档

- MANUS命令整合设计: `PRPs/completed/MANUS-command-restructuring-design-v1.0.md`
- 当前A命令: `.claude/commands/A.md`
- 当前S命令: `.claude/commands/S.md`
- 当前D命令: `.claude/commands/D.md`
- 当前W命令: `.claude/commands/W.md`
- 项目配置: `CLAUDE.md`
- 全局配置: `~/.claude/CLAUDE.md`

### B. 相关链接

- Claude Code官方文档: https://docs.claude.com/en/docs/claude-code/
- CONTEXT7 MCP文档: {项目内部文档}
- ASDW学习模型: {原创设计}

### C. 更新历史

- v1.0.0 (2025-10-23): 初始设计文档
  - 完整架构设计
  - 智能分析系统设计
  - 日志系统增强设计
  - 迁移策略制定

---

**设计负责人**: Claude (AI助手)
**审阅负责人**: 用户 (项目所有者)
**预计完成时间**: 2025-11-25 (包含1个月观察期)
