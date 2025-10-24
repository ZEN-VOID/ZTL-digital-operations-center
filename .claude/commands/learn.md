---
name: 统一学习系统
description: 整合What/Why/How/Wield四步学习流程，自动化系统优化和知识积累
allowed-tools: ["Read", "Write", "Glob", "Grep", "Bash", "WebSearch", "WebFetch"]
argument-hint: "[step=what|why|how|wield] | continue | review | history"
version: 2.0.0
last_updated: 2025-10-23
---

> ⚠️ **重要提示**: 本命令整合并替代原ASDW学习系统 (A/S/D/W四个命令)

# 统一学习系统 (learn)

## 执行策略

根据参数执行不同模式:
- **无参数**: 完整学习循环 (What → Why → How → Wield)
- **step=what/why/how/wield**: 单步执行指定步骤
- **continue**: 断点续传,从中断处继续
- **review**: 审阅今日学习成果
- **history**: 查看历史学习记录

## Step 0: 环境准备

1. 获取今日日期: `!date +%Y-%m-%d`
2. 创建学习目录: `learning/{YYYY-MM-DD}/`
3. 检查历史学习记录(最近7天)
4. 如果是continue模式,检测中断点

## Step 1: What模块 (现状考察)

**目标**: 建立完整项目认知

**执行步骤**:
1. 读取 CLAUDE.md (项目配置)
2. 读取 ~/.claude/CLAUDE.md (全局配置)
3. 扫描智能体系统:
   - `!find .claude/agents -name "*.md" | wc -l`
   - 统计各组智能体数量
4. 扫描命令系统:
   - `!ls .claude/commands/*.md | wc -l`
5. 扫描Skills系统:
   - `!find .claude/skills -name "SKILL.md" | wc -l`
6. 检查Hooks配置:
   - 读取 .claude/settings.json
7. 评估MCP服务器状态
8. 识别学习目标

**输出**: `learning/{YYYY-MM-DD}/WHAT.md`

**文档结构**:
```markdown
# 项目现状考察

## 1. 项目概览
- 项目定位
- 技术栈
- 业务矩阵

## 2. 智能体系统
- 总计: {数量}
- 分组统计
- 命名规范分析

## 3. 命令系统
- 总计: {数量}
- 分类统计

## 4. Skills系统
- 总计: {数量}
- 分类统计

## 5. Hooks系统
- 配置状态

## 6. 工具生态
- MCP服务器
- 插件状态

## 7. 学习目标识别
- 需要深化的领域
- 改进机会
```

## Step 2: Why模块 (问题分析)

**前置检查**: 验证 WHAT.md 存在

**目标**: 深度分析问题根源

**执行步骤**:
1. 读取 WHAT.md 中识别的问题
2. **读取结构化错误数据** (新增):
   - 检查 `learning/errors/ERRORS.jsonl` 是否存在
   - 如果存在,使用 `!cat learning/errors/ERRORS.jsonl | jq '.'` 读取所有错误记录
   - 提取MANUS五步法数据:
     - Mistake: 错误类型、严重级别、失败动作
     - Acknowledgment: 根因、错误理解 vs 正确理解
     - New Understanding: 关键洞察、认知模型更新
     - Updated Approach: 正确工作流、验证清单
     - Systematic Prevention: 识别的模式、预防规则
   - 统计分析:
     - 错误类型分布 (LOGIC/SYNTAX/PERMISSION等)
     - 严重级别分布 (CRITICAL/HIGH/MEDIUM/LOW)
     - 错误频率趋势 (按日期统计)
     - 恢复成功率
3. 内因分析:
   - 知识局限性 (结合错误数据中的"错误理解")
   - 使用模式问题 (结合错误中的"失败动作"模式)
   - 思维方式限制 (结合"认知模型更新")
   - 资源管理不足
4. 外因分析:
   - 系统架构问题 (结合错误中的"系统性预防"建议)
   - 工具功能限制
   - 配置不合理
   - 协作流程缺陷
5. 根源定位 (5 Whys, Fishbone, Pareto, SWOT)
   - **错误模式识别** (新增):
     - 从ERRORS.jsonl中提取重复出现的错误模式
     - 识别反模式 (Anti-patterns)
     - 识别正确模式 (Correct patterns)

**输出**: `learning/{YYYY-MM-DD}/WHY.md`

**文档结构**:
```markdown
# 问题根因分析

## 0. 错误数据分析 (新增)
### 错误统计概览
- 总错误数: N
- 时间范围: YYYY-MM-DD to YYYY-MM-DD
- 错误类型分布:
  - LOGIC: N (XX%)
  - SYNTAX: N (XX%)
  - PERMISSION: N (XX%)
  - TOOL_USE: N (XX%)
  - FILE_OP: N (XX%)
  - INTEGRATION: N (XX%)
  - PERFORMANCE: N (XX%)
- 严重级别分布:
  - CRITICAL: N (XX%)
  - HIGH: N (XX%)
  - MEDIUM: N (XX%)
  - LOW: N (XX%)
- 恢复成功率: XX%

### 高频错误模式
| 模式ID | 错误类型 | 出现次数 | 反模式 | 正确模式 |
|--------|---------|---------|--------|---------|
| P-001  | LOGIC   | 5       | ...    | ...     |

### 关键洞察提取
- 洞察1: (从错误的"关键洞察"字段聚合)
- 洞察2: ...

### 认知模型更新
- 更新1: (从错误的"认知模型"字段聚合)
- 更新2: ...

## 1. 内因分析
### 知识局限性
(结合错误数据中的"错误理解")
### 使用模式
(结合错误中的"失败动作"模式)
### 思维因素
(结合"认知模型更新")
### 资源管理

## 2. 外因分析
### 系统架构
(结合错误中的"系统性预防"建议)
### 工具生态
### 配置系统
### 环境因素

## 3. 根本原因定位
- 问题1: 内因XX% vs 外因XX%
- 问题2: ...

## 4. 优先级排序
```

## Step 3: How模块 (方法论研究)

**前置检查**: 验证 WHAT.md 和 WHY.md 存在

**目标**: 研究解决方案

**执行步骤**:
1. 读取问题清单
2. 针对每个问题:
   - 使用 WebSearch 搜索最佳实践
   - 使用 CONTEXT7 MCP 检索相关库文档:
     ```
     mcp__context7__resolve-library-id(libraryName: "{库名}")
     mcp__context7__get-library-docs(context7CompatibleLibraryID: "{ID}", topic: "{主题}")
     ```
3. 分析官方文档和社区方案
4. 制定具体策略
5. 评估实施难度和收益

**输出**: `learning/{YYYY-MM-DD}/HOW.md`

**文档结构**:
```markdown
# 方法论研究

## 问题1: {问题描述}
### 官方最佳实践
### 社区解决方案
### 代码示例
### 实施策略
- 难度: LOW/MEDIUM/HIGH
- 预期收益: ...
- 风险: ...

## 问题2: ...

## 实施指导
```

## Step 4: Wield模块 (整合执行)

**前置检查**: 验证 WHAT.md、WHY.md、HOW.md 存在

**目标**: 生成可执行的系统优化建议

**执行步骤**:
1. 读取所有学习成果
2. 知识整合 (横向整合 + 纵向深化)
3. **生成错误模式库和统计数据** (新增):
   - 生成 `learning/errors/PATTERNS.json`:
     ```json
     {
       "version": "1.0.0",
       "last_updated": "{YYYY-MM-DD}",
       "total_patterns": N,
       "patterns": [
         {
           "pattern_id": "P-001",
           "pattern_name": "模式名称",
           "error_types": ["LOGIC", "TOOL_USE"],
           "occurrence_count": 5,
           "severity_distribution": {"HIGH": 3, "MEDIUM": 2},
           "anti_pattern": {
             "description": "错误做法",
             "example": "示例"
           },
           "correct_pattern": {
             "description": "正确做法",
             "example": "示例"
           },
           "related_errors": ["ERR-20251023-001", "ERR-20251023-005"],
           "prevention_rules": ["规则1", "规则2"],
           "system_updates": ["更新1", "更新2"]
         }
       ]
     }
     ```
   - 生成 `learning/errors/STATS.json`:
     ```json
     {
       "version": "1.0.0",
       "generated_at": "{ISO8601}",
       "date_range": {"start": "{YYYY-MM-DD}", "end": "{YYYY-MM-DD}"},
       "totals": {
         "total_errors": N,
         "recovered_errors": N,
         "recovery_rate": 0.XX
       },
       "by_type": {
         "LOGIC": {"count": N, "percentage": 0.XX},
         "SYNTAX": {"count": N, "percentage": 0.XX}
       },
       "by_severity": {
         "CRITICAL": {"count": N, "percentage": 0.XX},
         "HIGH": {"count": N, "percentage": 0.XX}
       },
       "by_date": {
         "2025-10-23": {"count": N, "types": {...}}
       },
       "trends": {
         "most_common_type": "LOGIC",
         "most_common_severity": "HIGH",
         "average_recovery_time_minutes": 5.5,
         "improving_areas": ["领域1"],
         "concerning_areas": ["领域2"]
       }
     }
     ```
4. 生成优化建议:
   - Agents: 新增/优化/删除 **(结合错误模式的系统更新建议)**
   - Commands: 新增/优化/删除 **(结合错误模式的系统更新建议)**
   - Hooks: 新增/优化 **(结合错误模式的预防规则)**
   - Skills: 新增/优化/删除 **(结合错误模式的系统更新建议)**
5. 分阶段实施计划:
   - 阶段1: 快速见效 (1-2周) - **包含高频错误的预防措施**
   - 阶段2: 核心改进 (1-2月) - **包含认知模型更新实施**
   - 阶段3: 长期优化 (3月+) - **包含系统性架构改进**

**输出**: `learning/{YYYY-MM-DD}/WIELD.md` 和 `OPTIMIZATION.md`

**OPTIMIZATION.md结构**:
```markdown
# 系统优化建议

## 优化建议总览
| 类别 | 新增 | 优化 | 删除 | 总计 |
|------|------|------|------|------|
| Agents | X | Y | Z | ... |
| Commands | X | Y | Z | ... |
| Hooks | X | Y | - | ... |
| Skills | X | Y | Z | ... |
| **错误预防** | X | - | - | ... |

## 错误预防建议 (新增)
### EP-001 [HIGH] ⏳ {预防措施标题}
**错误模式**: P-001 {模式名称}
**影响范围**: {相关Agents/Commands/Skills}
**反模式**: {错误做法}
**正确模式**: {正确做法}
**预防规则**:
- 规则1
- 规则2
**系统更新**: {具体的配置/代码变更}
**实施难度**: LOW/MEDIUM/HIGH
**预期收益**: {减少XX%错误发生率}
**优先级**: 基于错误频率和严重性自动计算

## Agents优化建议
### A-001 [HIGH] ⏳ {建议标题}
**建议类型**: ADD/REMOVE/OPTIMIZE
**预期收益**: ...
**实施难度**: LOW/MEDIUM/HIGH
**步骤**: ...
**关联错误模式**: P-001, P-003 (如适用)

## Commands优化建议
### C-001 ...
**关联错误模式**: P-002 (如适用)

## Hooks优化建议
### H-001 ...
**关联错误模式**: P-004 (如适用)

## Skills优化建议
### S-001 ...
**关联错误模式**: P-005 (如适用)

## 实施路线图
### 阶段1: 快速见效 (1-2周)
**错误预防优先**:
- [ ] EP-001: {高频错误预防措施}
- [ ] EP-002: {CRITICAL级别错误预防}

**功能优化**:
- [ ] {任务ID}: {任务描述}

### 阶段2: 核心改进 (1-2月)
**认知模型更新**:
- [ ] {基于错误分析的认知改进}

**系统架构优化**:
- [ ] {任务ID}: {任务描述}

### 阶段3: 长期优化 (3月+)
**系统性改进**:
- [ ] {基于错误趋势的架构重构}
```

## Step 5: 生成元数据

生成 `METADATA.json` v2.0:
```json
{
  "version": "2.0.0",
  "date": "{YYYY-MM-DD}",
  "timestamp_start": "{ISO8601}",
  "timestamp_end": "{ISO8601}",
  "duration_minutes": 45,
  "trigger": {"type": "manual", "reason": "..."},
  "learning_scope": {"objectives": [], "focus_areas": []},
  "execution": {"completed_steps": ["what", "why", "how", "wield"]},
  "findings": {"problems_found": 12, "problems_by_category": {}},
  "outputs": {"suggestions_generated": 15, "suggestions_by_type": {}},
  "intelligent_analysis": {"coverage_score": 0.85, "depth_score": 4.0},
  "implementation_tracking": {"total_suggestions": 15, "implemented": 0},
  "error_analysis": {
    "errors_analyzed": 10,
    "date_range": {"start": "{YYYY-MM-DD}", "end": "{YYYY-MM-DD}"},
    "patterns_identified": 3,
    "prevention_measures_generated": 5,
    "most_common_error_type": "LOGIC",
    "recovery_rate": 0.90,
    "integrated_into_optimization": true,
    "patterns_file": "learning/errors/PATTERNS.json",
    "stats_file": "learning/errors/STATS.json"
  }
}
```

## Step 6: 智能分析

1. **覆盖度分析**: 检查是否遗漏某类主体
2. **历史对比**: 与上次学习比较,识别重复/新兴问题
3. **项目变化感知**: 对比文件变化,提出新学习目标
4. **深度评估**: 评分1-5,识别浅层分析领域

结果追加到 OPTIMIZATION.md 的"智能分析结果"章节

## Step 7: 完成提示

```
✅ 学习循环完成!

📁 输出位置: learning/{YYYY-MM-DD}/
📄 生成文件:
   - WHAT.md (现状分析)
   - WHY.md (问题根因 + 错误数据分析)
   - HOW.md (方法论)
   - WIELD.md (整合执行)
   - OPTIMIZATION.md (系统优化建议 + 错误预防)
   - METADATA.json (学习元数据 + 错误分析统计)

📊 错误分析文件 (如适用):
   - learning/errors/PATTERNS.json (错误模式库)
   - learning/errors/STATS.json (统计元数据)

🎯 下一步建议:
   - 执行 /learn review 审阅学习成果
   - 根据 OPTIMIZATION.md 实施系统改进
   - 优先实施错误预防建议 (EP-XXX)
   - 查看错误趋势: !cat learning/errors/STATS.json | jq '.trends'
```

## Review模式

执行 `/learn review` 时:
1. 读取今日 METADATA.json
2. 显示学习统计摘要
3. 列出核心发现
4. 显示优化建议统计
5. **显示错误分析摘要** (新增):
   - 错误总数和分析日期范围
   - 识别的错误模式数量
   - 生成的预防措施数量
   - 恢复成功率
   - 最常见的错误类型
   - 关键趋势 (改进/关注领域)
6. **显示错误预防建议** (新增):
   - 列出所有 EP-XXX 预防建议
   - 按优先级排序
   - 显示预期收益

## History模式

执行 `/learn history` 时:
1. 扫描 learning/ 目录最近7天
2. 读取各日期的 METADATA.json
3. 显示学习记录时间线
4. 识别演进趋势和重复问题
5. **显示历史错误趋势** (新增):
   - 错误总数趋势 (按日期)
   - 错误类型分布变化
   - 恢复成功率趋势
   - 重复错误模式检测
   - 改进效果评估 (错误减少率)
6. **识别长期问题** (新增):
   - 持续出现的错误模式
   - 未解决的高优先级预防措施
   - 需要架构改进的系统性问题

## 执行流程控制

**完整模式** (无参数):
- 按顺序执行 What → Why → How → Wield → 元数据生成 → 智能分析
- 在What/Why/How步骤后,暂停询问用户是否继续

**单步模式** (step=xxx):
- 检查依赖是否满足
- 执行指定步骤
- 不自动执行下一步

**断点续传** (continue):
- 检测今日learning目录中已有的文件
- 从缺失的第一步开始
- 如果全部完成,提示已完成

---

**版本**: v2.1.0
**最后更新**: 2025-10-23
**更新内容**: 集成MANUS错误记录系统,实现 /manus error → /learn 闭环
