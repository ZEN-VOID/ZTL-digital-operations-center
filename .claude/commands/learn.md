---
name: Plugins研究迭代系统
description: 从"组件学习"转向"生态研究"：Plugin健康度分析、协作关系图、演进计划生成。整合What/Why/How/Wield四步研究流程，输出PLUGIN-REPORT和PLUGIN-EVOLUTION
allowed-tools: ["Read", "Write", "Glob", "Grep", "Bash", "WebSearch", "WebFetch", "Task"]
argument-hint: "[step=what|why|how|wield] | continue | review | history"
version: 3.0.0
last_updated: 2025-10-28
---

> ⚠️ **重要提示**: v3.0重大更新 - 从"组件学习"转向"Plugins生态研究"

# Plugins研究迭代系统 (learn)

> **PERIS**: Plugin Ecosystem Research & Iteration System
>
> **新定位**: 以Plugins作为First-Class Citizens，研究8个业务组、65个智能体的生态健康度、协作关系和演进路径

## 执行策略

根据参数执行不同模式:
- **无参数**: 完整学习循环 (What → Why → How → Wield)
- **step=what/why/how/wield**: 单步执行指定步骤
- **continue**: 断点续传,从中断处继续
- **review**: 审阅今日学习成果
- **history**: 查看历史学习记录

## Step 0: 环境准备

1. 获取今日日期: `!date +%Y-%m-%d`
2. 创建研究目录: `context/research/{YYYY-MM-DD}/`
3. 检查历史研究记录(最近7天)
4. 如果是continue模式,检测中断点
5. **扫描 plugins/ 目录结构**（v3.0新增）
   - `!find plugins -name "plugin.json" | wc -l` 统计plugin数量
   - `!find plugins -name "*.md" -path "*/agents/*" | wc -l` 统计agents数量

## Step 1: What模块 (现状考察) - v3.0重构 🔥

**目标**: 建立完整的 **Plugins 生态认知**

**执行步骤（保持原有功能）**:
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

**执行步骤（v3.0新增：Plugins视角）** 🔥:

8. **Plugin配置扫描**:
   ```bash
   # 扫描所有 plugin.json
   !find plugins -name "plugin.json" -type f

   # 对每个plugin.json:
   - 读取配置（name, version, description, keywords）
   - 验证必需字段完整性（name, version, description必需）
   - 提取元数据（author, homepage, repository）
   - 统计agents数量：!find plugins/[组名]/agents -name "*.md" | wc -l
   - 检查commands目录：!ls plugins/[组名]/commands/*.md 2>/dev/null | wc -l
   - 检查skills目录：!find plugins/[组名]/skills -name "SKILL.md" | wc -l
   - 检查hooks配置：!test -f plugins/[组名]/hooks/hooks.json && echo "configured"
   ```

9. **Plugin健康度分析**:
   ```yaml
   对每个Plugin计算健康度评分（0-10分）:
     配置完整性（0-3分）:
       - plugin.json存在且格式正确: +1
       - 包含description和keywords: +1
       - 包含author和homepage: +1

     Agents分布（0-3分）:
       - 有agents: +1
       - agents数量均衡（不过多也不过少）: +1
       - agents有详细文档: +1

     扩展能力（0-2分）:
       - 配置了commands: +1
       - 配置了skills: +1

     维护状态（0-2分）:
       - 有README.md: +1
       - 有CHANGELOG.md: +1

   健康度分级:
     9-10分: 优秀（Excellent）
     7-8分: 良好（Good）
     5-6分: 及格（Fair）
     0-4分: 需改进（Needs Improvement）
   ```

10. **Plugin协作关系图**:
    ```yaml
    分析跨plugin的典型工作流:
      方法1 - 从agents文档分析:
        - 读取所有agents/*.md
        - 提取"调用"、"协作"、"依赖"等关键词
        - 识别跨plugin的agent引用

      方法2 - 从业务流程推断:
        - 战略组 → 创意组 → 美团组（营销活动流程）
        - 情报组 → 开发组（数据分析→系统开发）
        - 筹建组 → 供应组（门店筹建→物资采购）

      输出格式:
        Plugin A → Plugin B (工作流描述)
        示例: strategy-team → creative-team (战略分析后需要创意制作)
    ```

11. **识别学习目标**:
    ```yaml
    Plugin级别目标:
      - 哪些plugin健康度低？
      - 哪些plugin缺少扩展功能（commands/skills）？
      - 哪些plugin agents使用频率失衡？

    生态级别目标:
      - 是否存在功能重复的plugins？
      - 是否有能力空白区域？
      - 跨plugin协作是否流畅？
    ```

**输出**: `context/research/{YYYY-MM-DD}/WHAT-plugins.md`

**文档结构（v3.0扩展）**:
```markdown
# 项目现状考察

## 1. 项目概览
- 项目定位
- 技术栈
- 业务矩阵

## 2. Plugins生态概览（v3.0新增）🔥
- 总计: 8个plugins, 65个agents
- 各plugin基本信息（name, version, agents数）
- 整体健康度分布

## 3. Plugin详细扫描（v3.0新增）🔥
### 3.1 战略组 (strategy-team)
- 配置完整性: ✓/✗
- Agents数: 9个
- Commands配置: ✓/✗
- Skills配置: ✓/✗
- 健康度评分: X/10
- 主要发现: [...]

[... 其他7个plugins类似结构 ...]

## 4. Plugin协作关系图（v3.0新增）🔥
- 已识别工作流: N条
- 工作流详情:
  - strategy-team → creative-team (战略分析→创意制作)
  - intelligence-team → development-team (数据分析→系统开发)
  [...]

## 5. 传统组件统计（保持）
### 5.1 智能体系统
- 总计: {数量}
- 分组统计

### 5.2 命令系统
- 总计: {数量}

### 5.3 Skills系统
- 总计: {数量}

### 5.4 Hooks系统
- 配置状态

### 5.5 工具生态
- MCP服务器
- 插件状态

## 6. 学习目标识别（v3.0扩展）
### Plugin级别目标:
- 健康度<7的plugins: [列表]
- 缺少commands的plugins: [列表]
- agents使用失衡的plugins: [列表]

### 生态级别目标:
- 功能重复问题: [...]
- 能力空白区域: [...]
- 协作瓶颈: [...]
```

## Step 2: Why模块 (问题分析) - v3.0重构 🔥

**前置检查**: 验证 WHAT-plugins.md 存在

**目标**: 深度分析 **Plugin生态问题根源**，实现错误归因到Plugin

**执行步骤**:

1. **读取 WHAT-plugins.md 识别的问题**:
   - Plugin级别问题（健康度低、配置不完整）
   - 生态级别问题（功能重复、能力空白）

2. **读取结构化错误数据** (保持):
   - 检查 `context/errors/ERRORS.jsonl` 是否存在
   - 如果存在,使用 `!cat context/errors/ERRORS.jsonl | jq '.'` 读取所有错误记录
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

3. **错误归因到Plugin** (v3.0新增🔥):
   ```bash
   # 分析每个错误记录，推断关联的plugin
   # 方法1 - 从metadata.plugin字段直接获取（如果有）
   !cat context/errors/ERRORS.jsonl | jq -r '.metadata.plugin // "unknown"' | sort | uniq -c

   # 方法2 - 从错误描述推断（关键词匹配）
   # 例如: "战略组" → strategy-team, "AIGC" → creative-team

   # 方法3 - 从文件路径推断
   # 例如: "plugins/创意组/agents/X3-..." → creative-team
   ```

   **错误归因规则**:
   ```yaml
   关键词映射:
     战略组/strategy: strategy-team
     创意组/creative/AIGC: creative-team
     情报组/intelligence/采集: intelligence-team
     行政组/admin: admin-team
     美团组/meituan: meituan-ops-team
     供应组/supply: supply-chain-team
     开发组/development: development-team
     筹建组/construction/BIM: construction-team

   路径映射:
     plugins/战略组/ → strategy-team
     plugins/创意组/ → creative-team
     plugins/情报组/ → intelligence-team
     [其他7个plugins类似]

   Agent映射:
     G系列 → strategy-team
     X系列 → creative-team
     E系列 → intelligence-team
     R系列 → admin-team
     M系列 → meituan-ops-team
     S系列 → supply-chain-team
     F系列 → development-team
     Z系列 → construction-team
   ```

4. **Plugin级别问题分析** (v3.0新增🔥):
   对每个Plugin分析:

   **内因分析**:
   - 配置问题: plugin.json不完整、agents数量不合理
   - 文档问题: 缺少README、描述不清晰
   - 使用问题: 调用频率低、错误率高
   - 维护问题: 长期未更新、deprecated agents未清理

   **外因分析**:
   - 依赖问题: 依赖其他plugin但未声明
   - 集成问题: 与系统集成不良
   - 资源问题: 缺少必要的MCP/API支持

   **错误归因分析**:
   - 该Plugin相关的错误数量和类型
   - 高频错误模式（从ERRORS.jsonl中提取）
   - 错误严重性分布
   - 恢复成功率

5. **生态级别问题分析** (v3.0新增🔥):

   **功能重复问题**:
   - 识别多个plugin提供相似功能的情况
   - 分析是否可以合并或建立统一接口

   **能力空白问题**:
   - 识别业务流程中缺失的能力
   - 分析哪些plugin应该扩展功能

   **协作流程问题**:
   - 分析跨plugin工作流的瓶颈
   - 识别数据流转不畅的环节
   - 分析plugin间的依赖关系是否合理

6. **根源定位** (保持原方法论，应用到Plugin):
   使用经典分析方法:
   - **5 Whys**: 对每个Plugin问题深挖根因
   - **Fishbone Diagram**: 绘制Plugin问题的因果关系
   - **Pareto Analysis**: 识别20%的问题Plugin导致80%的错误
   - **SWOT**: 分析Plugin的优势、劣势、机会、威胁

**输出**: `context/research/{YYYY-MM-DD}/WHY-plugins.md`

**文档结构** (v3.0重构):
```markdown
# Plugin生态问题根因分析

## 1. 错误数据统计概览（保持）
### 错误统计
- 总错误数: N
- 时间范围: YYYY-MM-DD to YYYY-MM-DD
- 错误类型分布: ...
- 严重级别分布: ...
- 恢复成功率: XX%

## 2. 错误归因到Plugin（v3.0新增）🔥
### Plugin错误统计
| Plugin ID | 错误数 | 占比 | 高频错误类型 | 平均严重性 |
|-----------|-------|------|------------|----------|
| strategy-team | 5 | 15% | LOGIC | HIGH |
| creative-team | 12 | 35% | TOOL_USE | MEDIUM |
| intelligence-team | 8 | 23% | INTEGRATION | HIGH |
| ... | ... | ... | ... | ... |

### 高错误率Plugin Top 3
1. **[Plugin名称]**: X个错误，主要原因...
2. **[Plugin名称]**: X个错误，主要原因...
3. **[Plugin名称]**: X个错误，主要原因...

### 错误模式归因
| 模式ID | 错误类型 | 关联Plugin | 出现次数 | 反模式 | 正确模式 |
|--------|---------|-----------|---------|--------|---------|
| P-001  | LOGIC   | creative-team | 5 | ... | ... |

## 3. Plugin级别问题分析（v3.0新增）🔥
### 3.1 战略组 (strategy-team)
#### 内因分析
- 配置问题: ...
- 文档问题: ...
- 使用问题: ...
- 维护问题: ...

#### 外因分析
- 依赖问题: ...
- 集成问题: ...
- 资源问题: ...

#### 错误归因
- 关联错误数: N
- 高频错误: [错误类型列表]
- 根本原因: ...

[... 其他7个plugins类似结构 ...]

## 4. 生态级别问题分析（v3.0新增）🔥
### 功能重复问题
- 重复功能1: [Plugin A] 和 [Plugin B] 都提供...
- 重复功能2: ...

### 能力空白问题
- 空白领域1: 业务流程X缺少Plugin支持
- 空白领域2: ...

### 协作流程问题
- 瓶颈1: [Plugin A] → [Plugin B] 数据流转不畅
- 瓶颈2: ...

## 5. 根本原因定位（应用到Plugin）
### Pareto分析
- 20%问题Plugin: [列表]
- 导致80%错误: [分析]

### 5 Whys示例
问题: Plugin X错误率高
- Why 1: 因为...
- Why 2: 因为...
- [...]

### SWOT分析
#### 战略组 (strategy-team)
- Strengths: ...
- Weaknesses: ...
- Opportunities: ...
- Threats: ...

[... 其他plugins类似 ...]

## 6. 优先级排序
### 高优先级问题（需立即解决）
1. Plugin X: [问题描述] - 影响: CRITICAL
2. Plugin Y: [问题描述] - 影响: HIGH

### 中优先级问题（近期解决）
...

### 低优先级问题（长期改进）
...
```

## Step 3: How模块 (方法论研究) - v3.0重构 🔥

**前置检查**: 验证 WHAT-plugins.md 和 WHY-plugins.md 存在

**目标**: 研究 **Plugin生态优化解决方案**，结合Claude Code官方最佳实践

**执行步骤**:

1. **读取Plugin问题清单** (从WHY-plugins.md):
   - Plugin级别问题列表
   - 生态级别问题列表
   - 高错误率Plugin Top 3

2. **研究Plugin管理最佳实践** (v3.0新增🔥):

   **使用WebSearch搜索**:
   ```
   WebSearch(query="Claude Code plugin system best practices")
   WebSearch(query="multi-agent orchestration patterns")
   WebSearch(query="plugin architecture design patterns")
   ```

   **使用CONTEXT7 MCP检索**:
   ```
   # 检索Claude Code官方文档
   mcp__context7__resolve-library-id(libraryName: "Claude Code")
   mcp__context7__get-library-docs(
     context7CompatibleLibraryID: "/anthropic/claude-code",
     topic: "plugins management"
   )

   # 检索插件系统设计
   mcp__context7__resolve-library-id(libraryName: "plugin architecture")
   mcp__context7__get-library-docs(
     context7CompatibleLibraryID: "{ID}",
     topic: "plugin lifecycle, dependency management"
   )
   ```

   **重点研究内容**:
   - Plugin生命周期管理（创建、启用、禁用、删除）
   - Plugin依赖关系管理（显式声明、版本兼容性）
   - Plugin配置标准化（plugin.json schema验证）
   - Plugin健康度监控（指标定义、阈值设置）
   - Plugin协作模式（事件总线、数据共享）

3. **针对每个Plugin级别问题研究解决方案** (v3.0新增🔥):

   对于每个识别的Plugin问题:

   **Step 3.1 - 官方最佳实践查询**:
   - 查询Claude Code官方文档关于该问题的建议
   - 查询Anthropic Agent Skills类似场景的处理方式
   - 查询MCP服务器集成的标准模式

   **Step 3.2 - 社区解决方案研究**:
   - WebSearch搜索开源项目的类似实现
   - 分析GitHub上高星plugin项目的设计
   - 查找Stack Overflow相关问题的解决方案

   **Step 3.3 - 制定Plugin改进策略**:
   ```yaml
   改进策略模板:
     plugin_id: [Plugin ID]
     问题描述: [简短描述]

     解决方案:
       方案1: [描述]
         - 实施步骤: [...]
         - 难度: LOW/MEDIUM/HIGH
         - 预期收益: [...]
         - 风险: [...]
         - 参考案例: [链接或项目名]

       方案2 (备选): [描述]
         - [...]

     推荐方案: 方案X
     原因: [...]
   ```

4. **针对生态级别问题研究解决方案** (v3.0新增🔥):

   **功能重复问题**:
   - 研究接口抽象和统一门面模式
   - 查询微服务架构中的服务合并策略
   - 制定Plugin重构和合并方案

   **能力空白问题**:
   - 研究如何扩展现有Plugin功能
   - 查询是否有成熟的第三方解决方案
   - 评估创建新Plugin vs 扩展现有Plugin

   **协作流程问题**:
   - 研究Plugin间通信机制（事件、消息队列）
   - 查询工作流编排引擎（Temporal, Airflow）
   - 制定标准化的Plugin协作协议

5. **评估实施优先级** (保持原逻辑):
   对每个解决方案评估:
   ```yaml
   评估维度:
     难度: LOW (1-3天) / MEDIUM (1-2周) / HIGH (1月+)
     预期收益:
       - 错误率降低: XX%
       - 使用效率提升: XX%
       - 维护成本降低: XX%

     风险:
       - 技术风险: [描述]
       - 兼容性风险: [描述]
       - 时间风险: [描述]

     依赖:
       - 需要先完成: [其他任务]
       - 依赖外部资源: [...]

     优先级: P0 (立即) / P1 (本周) / P2 (本月) / P3 (季度)
   ```

**输出**: `context/research/{YYYY-MM-DD}/HOW-plugins.md`

**文档结构** (v3.0重构):
```markdown
# Plugin生态优化方法论研究

## 1. 研究综述
### Claude Code官方最佳实践
- Plugin管理: [要点总结]
- 依赖管理: [要点总结]
- 健康度监控: [要点总结]

### 社区解决方案概览
- 开源项目案例: [列表]
- 成熟模式: [列表]

## 2. Plugin级别解决方案（v3.0新增）🔥
### 2.1 战略组 (strategy-team)
#### 问题1: [问题描述]
**官方最佳实践**:
- [Claude Code官方建议]

**社区解决方案**:
- 方案A: [开源项目X的实现]
- 方案B: [GitHub高星项目Y的设计]

**代码示例**:
```python
# 示例代码
```

**实施策略**:
- **推荐方案**: 方案A
- **实施步骤**:
  1. [步骤1]
  2. [步骤2]
- **难度**: MEDIUM (1周)
- **预期收益**: 错误率降低30%
- **风险**: 需要重构agents配置
- **优先级**: P1

#### 问题2: [问题描述]
[... 类似结构 ...]

[... 其他7个plugins类似 ...]

## 3. 生态级别解决方案（v3.0新增）🔥
### 3.1 功能重复问题
#### 问题: [Plugin A] 和 [Plugin B] 功能重复

**解决方案**:
- 方案1: 统一接口抽象
  - 实施步骤: [...]
  - 参考: [微服务架构案例]

- 方案2: Plugin合并
  - 实施步骤: [...]
  - 参考: [开源项目合并案例]

**推荐方案**: 方案1
**原因**: [...]
**难度**: HIGH (2周)
**优先级**: P2

### 3.2 能力空白问题
[... 类似结构 ...]

### 3.3 协作流程问题
[... 类似结构 ...]

## 4. Plugin健康度监控方案（v3.0新增）🔥
### 监控指标定义
```yaml
健康度评分 (0-10分):
  配置完整性 (0-3分):
    - plugin.json必需字段: +1
    - README.md存在: +1
    - 文档完整性: +1

  Agents分布 (0-3分):
    - Agents数量合理 (3-15个): +3
    - Agents数量过少 (<3): +1
    - Agents数量过多 (>15): +2

  扩展能力 (0-2分):
    - 提供commands: +1
    - 提供skills: +1

  维护状态 (0-2分):
    - 最近3个月有更新: +2
    - 最近6个月有更新: +1
    - 6个月无更新: +0
```

### 监控实施方案
- 工具: 自动化脚本 (Python)
- 频率: 每周执行
- 告警阈值: 健康度 < 6分
- 输出: `context/analytics/plugin-health-{date}.json`

## 5. 实施指导
### 短期行动项 (1-2周)
1. [P0任务列表]

### 中期行动项 (1个月)
1. [P1任务列表]

### 长期改进项 (1季度)
1. [P2/P3任务列表]

### 资源需求
- 人力: [估算]
- 工具: [所需工具列表]
- 外部依赖: [列表]
```

## Step 4: Wield模块 (整合执行) - v3.0重构 🔥

**前置检查**: 验证 WHAT-plugins.md、WHY-plugins.md、HOW-plugins.md 存在

**目标**: 生成 **Plugin生态研究报告** 和 **可执行的演进计划**

**执行步骤**:

1. **读取所有Plugin研究成果**:
   - WHAT-plugins.md: Plugin配置、健康度、协作关系
   - WHY-plugins.md: 问题根因、错误归因
   - HOW-plugins.md: 解决方案、最佳实践

2. **知识整合** (横向整合 + 纵向深化):

   **横向整合**:
   - 跨8个plugins的共性问题
   - 生态级别的协作模式
   - 全局优化机会

   **纵向深化**:
   - 每个plugin的完整诊断（What → Why → How）
   - 优先级排序（基于错误率、影响范围、实施难度）
   - 可执行的改进项目（项目ID、工作量估算、依赖关系）

3. **生成错误模式库和统计数据** (保持):
   - 生成 `context/errors/PATTERNS.json`:
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
           "related_plugin": "creative-team",
           "anti_pattern": {
             "description": "错误做法",
             "example": "示例"
           },
           "correct_pattern": {
             "description": "正确做法",
             "example": "示例"
           },
           "related_errors": ["ERR-20251023-001"],
           "prevention_rules": ["规则1", "规则2"],
           "system_updates": ["更新1", "更新2"]
         }
       ]
     }
     ```
   - 生成 `context/errors/STATS.json`:
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
       "by_plugin": {
         "creative-team": {"count": 12, "percentage": 0.35},
         "strategy-team": {"count": 5, "percentage": 0.15}
       },
       "by_type": {"LOGIC": {"count": N, "percentage": 0.XX}},
       "by_severity": {"HIGH": {"count": N, "percentage": 0.XX}},
       "trends": {
         "most_problematic_plugin": "creative-team",
         "most_common_type": "LOGIC",
         "improving_plugins": ["strategy-team"],
         "concerning_plugins": ["creative-team"]
       }
     }
     ```

4. **生成 PLUGIN-REPORT.md** (v3.0核心输出🔥):

   **核心内容**:
   - 总体评估（健康度评分、生态协作成熟度）
   - 各Plugin详细分析（8个plugins逐一分析）
   - 跨Plugin协作优化（工作流优化方案）
   - 生态演进路线图（短期/中期/长期规划）

   **评分体系**:
   ```yaml
   Plugin健康度 (0-10分):
     配置完整性 (0-3分)
     Agents分布 (0-3分)
     扩展能力 (0-2分)
     维护状态 (0-2分)

   生态协作成熟度 (0-10分):
     依赖声明清晰度 (0-3分)
     接口标准化程度 (0-3分)
     文档完整性 (0-2分)
     工作流流畅度 (0-2分)
   ```

5. **生成 PLUGIN-EVOLUTION.json** (v3.0核心输出🔥):

   **核心内容**:
   - 各Plugin的演进项目（优化、新增功能）
   - 生态级改进建议（跨plugin协作）
   - 统计数据（总工作量估算、优先级分布）

   **项目分类**:
   ```yaml
   项目类型:
     agent_optimization: Agent优化（修改现有agent）
     agent_addition: Agent新增
     command_optimization: Command优化
     skill_addition: Skill新增
     plugin_refactoring: Plugin重构
     ecosystem_improvement: 生态改进（跨plugin）
     documentation: 文档完善
     health_monitoring: 健康度监控实施

   优先级定义:
     CRITICAL: 阻塞性问题，影响核心功能
     HIGH: 高频错误、显著影响用户体验
     MEDIUM: 重要改进，非紧急
     LOW: 优化建议，可延后

   工作量估算:
     estimated_effort_days: 0.5 (半天) ~ 10 (2周)
   ```

**输出**:
- `context/research/{YYYY-MM-DD}/WIELD-plugins.md` (执行总结)
- `context/research/{YYYY-MM-DD}/PLUGIN-REPORT.md` (详细报告) ⭐
- `context/research/{YYYY-MM-DD}/PLUGIN-EVOLUTION.json` (演进计划) ⭐

**PLUGIN-REPORT.md结构** (v3.0新增🔥):
```markdown
# Plugin生态研究报告

## 📊 总体评估

### 健康度评分
| Plugin | 健康度 | Agents数 | 使用频率 | 主要问题 |
|--------|--------|---------|---------|---------|
| strategy-team | 8.5/10 | 9 | 中 | G7使用率低 |
| creative-team | 6.0/10 | 9 | 高 | 错误率高 |
| intelligence-team | 7.5/10 | 8 | 中 | 文档不完整 |
| admin-team | 8.0/10 | 9 | 低 | 功能重叠 |
| meituan-ops-team | 7.0/10 | 6 | 高 | 缺少监控 |
| supply-chain-team | 6.5/10 | 7 | 低 | 集成问题 |
| development-team | 9.0/10 | 11 | 高 | 配置完善 |
| construction-team | 7.0/10 | 6 | 低 | agents不足 |

**平均健康度**: 7.4/10
**生态协作成熟度**: 6.5/10

### 关键发现
1. **高频问题**: 创意组错误率高（35%错误来自该plugin）
2. **能力空白**: 缺少供应链与筹建组的深度集成
3. **协作瓶颈**: Plugin间数据流转需要手动操作

## 🔍 各Plugin详细分析

### 1. 战略组 (strategy-team)
**健康度**: 8.5/10 ⭐ 优秀

**配置状态**:
- ✅ plugin.json完整
- ✅ README.md详细
- ✅ 9个agents配置良好

**优势**:
- Agents功能明确，分工清晰
- 文档完善，使用方便
- 错误率低（仅5个错误，占15%）

**问题诊断**:
- G7智能体使用率低（<10%）
- 缺少commands快捷方式
- 与情报组的协作流程不够顺畅

**改进建议**:
1. [高优] G7功能优化或合并到其他agent
2. [中优] 添加/strategy命令集
3. [低优] 建立与情报组的标准化工作流

**关联错误**: ERR-20251023-001 (LOGIC, MEDIUM)

[... 其他7个plugins类似结构 ...]

## 🌐 跨Plugin协作优化

### 协作模式1: 情报 → 战略 → 创意
**当前流程**:
1. 情报组采集数据 (E系列)
2. 手动整理数据
3. 战略组分析 (G系列)
4. 手动转交需求
5. 创意组生产 (X系列)

**优化方案**:
- 建立标准化数据格式
- 创建workflow编排命令
- 自动化数据流转

**预期收益**: 减少50%的手动操作时间

[... 其他协作模式 ...]

## 📈 生态演进路线图

### 短期优化 (1-2周)
**P0 - 立即执行**:
- [ ] 修复创意组高频错误 (creative-team错误率降低)
- [ ] 完善文档缺失的plugins

**P1 - 本周完成**:
- [ ] 实施Plugin健康度监控
- [ ] 建立错误预防机制

### 中期改进 (1个月)
**P1 - 功能增强**:
- [ ] 新增跨plugin工作流命令
- [ ] 优化低使用率agents

**P2 - 架构优化**:
- [ ] 建立Plugin间通信协议
- [ ] 实施依赖管理机制

### 长期规划 (1季度)
**P2 - 生态完善**:
- [ ] 补齐能力空白（新plugin或扩展）
- [ ] 建立Plugin市场机制

**P3 - 持续优化**:
- [ ] 自动化测试覆盖所有plugins
- [ ] 建立Plugin版本管理

## 📊 统计数据

**总工作量估算**: 约25人天
**优先级分布**:
- CRITICAL: 2项
- HIGH: 8项
- MEDIUM: 12项
- LOW: 5项

**预期收益**:
- 错误率降低: 40%
- 使用效率提升: 30%
- 维护成本降低: 25%
```

**PLUGIN-EVOLUTION.json结构** (v3.0新增🔥):
```json
{
  "version": "1.0.0",
  "generated_at": "2025-10-28T10:30:00Z",
  "research_date": "2025-10-28",

  "plugins": {
    "strategy-team": {
      "current_version": "1.0.0",
      "target_version": "1.1.0",
      "current_health_score": 8.5,
      "target_health_score": 9.0,

      "evolution_items": [
        {
          "item_id": "A-001",
          "type": "agent_optimization",
          "title": "优化G7智能体功能",
          "description": "将G7部分功能合并到G1，提升使用率",
          "priority": "HIGH",
          "estimated_effort_days": 2,
          "dependencies": [],
          "related_errors": ["ERR-20251023-001"],
          "expected_benefits": "提升使用率从10%到50%"
        },
        {
          "item_id": "C-001",
          "type": "command_addition",
          "title": "添加/strategy命令集",
          "description": "创建战略分析快捷命令",
          "priority": "MEDIUM",
          "estimated_effort_days": 1,
          "dependencies": [],
          "expected_benefits": "减少30%的调用时间"
        }
      ]
    },

    "creative-team": {
      "current_version": "1.0.0",
      "target_version": "1.2.0",
      "current_health_score": 6.0,
      "target_health_score": 8.0,

      "evolution_items": [
        {
          "item_id": "B-001",
          "type": "plugin_refactoring",
          "title": "修复AIGC错误率高问题",
          "description": "重构X3-AIGC设计师的prompt和验证逻辑",
          "priority": "CRITICAL",
          "estimated_effort_days": 3,
          "dependencies": [],
          "related_errors": ["ERR-20251023-005", "ERR-20251023-012"],
          "expected_benefits": "错误率从35%降低到15%"
        }
      ]
    }

    [... 其他6个plugins类似结构 ...]
  },

  "ecosystem_improvements": [
    {
      "item_id": "E-001",
      "type": "ecosystem_improvement",
      "title": "建立情报→战略→创意工作流",
      "description": "创建标准化的跨plugin数据流转协议",
      "priority": "HIGH",
      "estimated_effort_days": 5,
      "involved_plugins": ["intelligence-team", "strategy-team", "creative-team"],
      "expected_benefits": "减少50%的手动操作时间"
    },
    {
      "item_id": "E-002",
      "type": "health_monitoring",
      "title": "实施Plugin健康度监控",
      "description": "创建自动化脚本，每周生成健康度报告",
      "priority": "HIGH",
      "estimated_effort_days": 2,
      "involved_plugins": ["all"],
      "expected_benefits": "提前发现80%的潜在问题"
    }
  ],

  "statistics": {
    "total_plugins": 8,
    "total_evolution_items": 27,
    "total_estimated_days": 25,

    "by_priority": {
      "CRITICAL": 2,
      "HIGH": 8,
      "MEDIUM": 12,
      "LOW": 5
    },

    "by_type": {
      "agent_optimization": 8,
      "agent_addition": 3,
      "command_optimization": 4,
      "skill_addition": 2,
      "plugin_refactoring": 3,
      "ecosystem_improvement": 4,
      "documentation": 2,
      "health_monitoring": 1
    },

    "health_score_improvement": {
      "current_average": 7.4,
      "target_average": 8.5,
      "improvement": "+1.1"
    }
  }
}
```

## Step 5: 生成元数据 - v3.0更新

生成 `context/research/{YYYY-MM-DD}/METADATA.json` v3.0:
```json
{
  "version": "3.0.0",
  "date": "{YYYY-MM-DD}",
  "timestamp_start": "{ISO8601}",
  "timestamp_end": "{ISO8601}",
  "duration_minutes": 45,

  "trigger": {"type": "manual", "reason": "..."},

  "research_scope": {
    "focus": "Plugin生态研究",
    "total_plugins": 8,
    "objectives": ["Plugin健康度评估", "错误归因分析", "生态协作优化"],
    "focus_areas": ["配置完整性", "错误率", "协作流程"]
  },

  "execution": {
    "completed_steps": ["what-plugins", "why-plugins", "how-plugins", "wield-plugins"],
    "step_status": {
      "what": "completed",
      "why": "completed",
      "how": "completed",
      "wield": "completed"
    }
  },

  "plugin_analysis": {
    "plugins_analyzed": 8,
    "avg_health_score": 7.4,
    "target_avg_health_score": 8.5,

    "health_distribution": {
      "excellent (9-10)": 1,
      "good (7-8.9)": 5,
      "fair (5-6.9)": 2,
      "poor (<5)": 0
    },

    "problems_by_plugin": {
      "creative-team": 3,
      "strategy-team": 2,
      "intelligence-team": 2,
      "admin-team": 1,
      "meituan-ops-team": 2,
      "supply-chain-team": 3,
      "development-team": 0,
      "construction-team": 2
    },

    "total_problems_found": 15
  },

  "evolution_plan": {
    "total_evolution_items": 27,
    "total_estimated_days": 25,

    "by_priority": {
      "CRITICAL": 2,
      "HIGH": 8,
      "MEDIUM": 12,
      "LOW": 5
    },

    "by_type": {
      "agent_optimization": 8,
      "agent_addition": 3,
      "command_optimization": 4,
      "skill_addition": 2,
      "plugin_refactoring": 3,
      "ecosystem_improvement": 4,
      "documentation": 2,
      "health_monitoring": 1
    }
  },

  "error_analysis": {
    "errors_analyzed": 10,
    "date_range": {"start": "{YYYY-MM-DD}", "end": "{YYYY-MM-DD}"},
    "patterns_identified": 3,
    "prevention_measures_generated": 5,

    "by_plugin": {
      "creative-team": {"count": 12, "percentage": 0.35},
      "strategy-team": {"count": 5, "percentage": 0.15},
      "intelligence-team": {"count": 8, "percentage": 0.23}
    },

    "most_problematic_plugin": "creative-team",
    "most_common_error_type": "LOGIC",
    "recovery_rate": 0.90,

    "integrated_into_evolution": true,
    "patterns_file": "context/errors/PATTERNS.json",
    "stats_file": "context/errors/STATS.json"
  },

  "outputs": {
    "what_file": "context/research/{YYYY-MM-DD}/WHAT-plugins.md",
    "why_file": "context/research/{YYYY-MM-DD}/WHY-plugins.md",
    "how_file": "context/research/{YYYY-MM-DD}/HOW-plugins.md",
    "wield_file": "context/research/{YYYY-MM-DD}/WIELD-plugins.md",
    "plugin_report": "context/research/{YYYY-MM-DD}/PLUGIN-REPORT.md",
    "evolution_plan": "context/research/{YYYY-MM-DD}/PLUGIN-EVOLUTION.json",
    "metadata": "context/research/{YYYY-MM-DD}/METADATA.json"
  },

  "intelligent_analysis": {
    "coverage_score": 0.85,
    "depth_score": 4.0,
    "plugin_ecosystem_maturity": 6.5
  },

  "implementation_tracking": {
    "total_evolution_items": 27,
    "implemented": 0,
    "in_progress": 0,
    "blocked": 0
  }
}
```

## Step 6: 智能分析

1. **覆盖度分析**: 检查是否遗漏某类主体
2. **历史对比**: 与上次学习比较,识别重复/新兴问题
3. **项目变化感知**: 对比文件变化,提出新学习目标
4. **深度评估**: 评分1-5,识别浅层分析领域

结果追加到 OPTIMIZATION.md 的"智能分析结果"章节

## Step 7: 完成提示 - v3.0更新

```
✅ Plugin生态研究完成! 🔥

📁 输出位置: context/research/{YYYY-MM-DD}/
📄 生成文件:
   ⭐ 核心输出:
   - PLUGIN-REPORT.md (Plugin生态研究报告)
   - PLUGIN-EVOLUTION.json (可执行演进计划)

   📋 研究过程:
   - WHAT-plugins.md (Plugin配置扫描)
   - WHY-plugins.md (Plugin问题根因)
   - HOW-plugins.md (Plugin方法论研究)
   - WIELD-plugins.md (整合执行总结)
   - METADATA.json (研究元数据)

📊 错误分析文件 (如适用):
   - context/errors/PATTERNS.json (错误模式库 + Plugin归因)
   - context/errors/STATS.json (统计元数据 + Plugin分布)

🎯 下一步建议:
   - 执行 /learn review 审阅Plugin研究成果
   - 查看 PLUGIN-REPORT.md 了解各Plugin健康度
   - 查看 PLUGIN-EVOLUTION.json 了解演进计划
   - 按优先级实施改进项目 (CRITICAL → HIGH → MEDIUM → LOW)
   - 查看Plugin错误分布: !cat context/errors/STATS.json | jq '.by_plugin'
   - 查看最problematic的plugin: !cat context/errors/STATS.json | jq '.trends.most_problematic_plugin'
```

## Review模式 - v3.0更新

执行 `/learn review` 时:
1. 读取今日 `context/research/{TODAY}/METADATA.json`
2. 显示Plugin研究统计摘要
3. 列出核心发现 (Plugin级别 + 生态级别)
4. 显示Plugin健康度概览
5. 显示演进计划统计
6. **显示错误分析摘要** (保持 + Plugin归因):
   - 错误总数和分析日期范围
   - 错误按Plugin分布 (Top 3)
   - 识别的错误模式数量
   - 生成的预防措施数量
   - 恢复成功率
   - 最problematic的plugin
   - 关键趋势 (改进/关注的plugins)
7. **显示演进项目概览** (v3.0新增):
   - 总演进项目数
   - 按优先级分布 (CRITICAL/HIGH/MEDIUM/LOW)
   - 按类型分布 (agent_optimization/plugin_refactoring等)
   - 总工作量估算
   - 预期健康度提升

**输出格式**:
```
📊 Plugin生态研究摘要 - {YYYY-MM-DD}

⏱️ 研究耗时: 45分钟
🔍 分析范围: 8个Plugins, 65个Agents

📈 Plugin健康度:
   平均分: 7.4/10
   目标分: 8.5/10
   提升幅度: +1.1

🏆 健康度分布:
   优秀 (9-10): 1个 (development-team)
   良好 (7-8.9): 5个
   一般 (5-6.9): 2个
   较差 (<5): 0个

🔴 主要问题:
   1. creative-team错误率高 (35%)
   2. 跨plugin协作需要手动操作
   3. 供应链与筹建组集成不足

📋 演进计划:
   总项目数: 27个
   总工作量: 约25人天

   优先级分布:
   - CRITICAL: 2个 (立即处理)
   - HIGH: 8个 (本周完成)
   - MEDIUM: 12个 (本月完成)
   - LOW: 5个 (长期优化)

❌ 错误分析:
   总错误数: 10个
   恢复成功率: 90%

   按Plugin分布:
   1. creative-team: 12个 (35%)
   2. intelligence-team: 8个 (23%)
   3. strategy-team: 5个 (15%)

   最problematic plugin: creative-team

🎯 关键洞察:
   - [洞察1]
   - [洞察2]
   - [洞察3]

📂 详细报告:
   - context/research/{YYYY-MM-DD}/PLUGIN-REPORT.md
   - context/research/{YYYY-MM-DD}/PLUGIN-EVOLUTION.json
```

## History模式 - v3.0更新

执行 `/learn history` 时:
1. 扫描 `context/research/` 目录最近7天
2. 读取各日期的 METADATA.json
3. 显示Plugin研究历史时间线
4. 识别Plugin演进趋势
5. 对比健康度变化

**输出格式**:
```
📅 Plugin研究历史 (最近7天)

📊 趋势分析:
   2025-10-28 (今日):
     - 平均健康度: 7.4/10
     - 总问题数: 15
     - 演进项目: 27个

   2025-10-21 (7天前):
     - 平均健康度: 7.0/10
     - 总问题数: 18
     - 演进项目: 30个

   📈 改进趋势:
     - 健康度提升: +0.4
     - 问题减少: -3个
     - 实施项目: 3个已完成

🔄 重复问题识别:
   - creative-team错误率高 (连续3次研究)
   - 跨plugin协作问题 (连续2次研究)

✅ 已解决问题:
   - strategy-team文档缺失 (已修复)
   - development-team配置问题 (已修复)

⏭️ 下一步重点:
   - 优先解决creative-team高错误率
   - 建立跨plugin工作流自动化
```
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

## 📖 版本历史

### v3.0.0 (2025-10-28) - 🔥 重大更新：Plugin生态研究系统

**核心变革**:
- ✅ 从"组件学习"转向"Plugins生态研究"
- ✅ 新增Plugin健康度评分体系（0-10分）
- ✅ 新增错误归因到Plugin机制
- ✅ 核心输出从OPTIMIZATION.md转变为PLUGIN-REPORT.md + PLUGIN-EVOLUTION.json

**What模块 (Step 1)**:
- ✅ 新增Plugin配置扫描（plugin.json、agents、commands、skills）
- ✅ 新增Plugin健康度分析（配置完整性、agents分布、扩展能力、维护状态）
- ✅ 新增Plugin协作关系图分析
- ✅ 输出路径: `learning/{DATE}/WHAT.md` → `context/research/{DATE}/WHAT-plugins.md`

**Why模块 (Step 2)**:
- ✅ 新增错误归因到Plugin（关键词映射、路径映射、Agent映射）
- ✅ 新增Plugin级别问题分析（内因、外因、错误归因）
- ✅ 新增生态级别问题分析（功能重复、能力空白、协作流程）
- ✅ 输出路径: `learning/{DATE}/WHY.md` → `context/research/{DATE}/WHY-plugins.md`

**How模块 (Step 3)**:
- ✅ 新增Plugin管理最佳实践研究（生命周期、依赖管理、健康度监控）
- ✅ 新增Plugin级别解决方案（针对8个plugins逐一制定改进策略）
- ✅ 新增生态级别解决方案（功能重复、能力空白、协作流程优化）
- ✅ 新增Plugin健康度监控方案设计
- ✅ 输出路径: `learning/{DATE}/HOW.md` → `context/research/{DATE}/HOW-plugins.md`

**Wield模块 (Step 4)**:
- ✅ 核心输出重构：OPTIMIZATION.md → **PLUGIN-REPORT.md** + **PLUGIN-EVOLUTION.json**
- ✅ PLUGIN-REPORT.md: 总体评估、各Plugin详细分析、跨Plugin协作优化、生态演进路线图
- ✅ PLUGIN-EVOLUTION.json: 27个演进项目、优先级分布、工作量估算、健康度提升目标
- ✅ 错误模式库新增`related_plugin`字段
- ✅ 统计数据新增`by_plugin`分布和`most_problematic_plugin`

**元数据 (Step 5)**:
- ✅ METADATA.json v3.0: 新增`research_scope`、`plugin_analysis`、`evolution_plan`字段
- ✅ 新增Plugin健康度分布统计
- ✅ 新增演进项目类型和优先级统计

**输出路径标准化**:
- ✅ 所有输出从`learning/`迁移到`context/research/`
- ✅ 错误文件从`learning/errors/`迁移到`context/errors/`
- ✅ 保持原有错误模式库和统计功能

**Review/History模式**:
- ✅ Review模式新增Plugin健康度概览、演进项目统计
- ✅ History模式新增Plugin演进趋势对比

---

### v2.1.0 (2025-10-23)

**更新内容**:
- ✅ 集成MANUS错误记录系统
- ✅ 实现 `/manus error` → `/learn` 闭环
- ✅ 新增错误模式库（PATTERNS.json）
- ✅ 新增错误统计数据（STATS.json）
- ✅ Why模块新增结构化错误数据分析

---

### v2.0.0 (2025-10-22)

**更新内容**:
- ✅ What/Why/How/Wield四步法完整实施
- ✅ 新增Review和History模式
- ✅ 新增智能分析功能
- ✅ 新增METADATA.json v2.0

---

**版本**: v3.0.0
**最后更新**: 2025-10-28
**重大更新**: Plugin生态研究系统 (PERIS) - 从组件学习到生态研究的范式转变
