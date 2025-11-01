# 上下求索 - 详细参考文档

> 扩展文档,提供完整的参数模板、识别逻辑和高级配置

## 目录

- [10种类型详细参数模板](#10种类型详细参数模板)
- [智能类型识别详细逻辑](#智能类型识别详细逻辑)
- [双层级分类决策树](#双层级分类决策树)
- [ERROR类型MANUS五步法](#error类型manus五步法)
- [缓存优化最佳实践](#缓存优化最佳实践)

---

## 10种类型详细参数模板

### 🎯 FOCUS (注意力焦点)

```yaml
必需字段:
  - 📊 Priority: HIGH/MEDIUM/LOW
  - ⏱️ Duration: [预计时长]
  - 🎯 Success: [具体可衡量的成功标准]

可选字段:
  - 💭 Rationale: [为什么这是当前焦点]
  - 🔗 Related Context: [相关链接]
```

**示例**:
```
📊 Priority: HIGH
⏱️ Duration: 4h
🎯 Success: MANUS命令实现并通过所有测试
💭 Rationale: 上下文管理系统整合是v2.0关键功能

实现MANUS统一上下文管理命令
```

---

### 📋 TODO (任务管理)

```yaml
必需字段:
  - 🏷️ Type: DEV/DOC/CONFIG/TEST/REVIEW/DEPLOY/RESEARCH
  - 📊 Priority: HIGH/MEDIUM/LOW
  - 🎯 Completion: [具体完成标准]

可选字段:
  - 🔗 Dependencies: [任务ID或文件路径]
  - **Status**: ⭕Pending/🔄InProgress/✅Done/❌Cancelled/🚫Blocked/⏸️Paused
```

**状态变更示例**:
```
# 初始状态
⭕ TODO: 实现功能X
Status: Pending

# 更新状态(新条目)
🔄 TODO: 实现功能X
Status: Pending → InProgress
Reference: [前一条目时间戳]

# 完成(新条目)
✅ TODO: 实现功能X
Status: InProgress → Done
Reference: [前一条目时间戳]
```

---

### ⚙️ PROCESS (流程执行)

```yaml
必需字段:
  - 🏷️ Type: DEVELOP/DEBUG/OPTIMIZE/LEARN/REVIEW/REFACTOR
  - 📝 Key Steps: [步骤1] → [步骤2] → [步骤3]
  - 📊 Outcome: SUCCESS/PARTIAL/FAILED

可选字段:
  - ⏱️ Duration: [实际用时]
  - 💡 Learnings: [关键收获]
  - 🔗 Related Files: [相关文件路径]
```

---

### ❌ ERROR (错误记录 - MANUS五步法)

> **特殊处理**: 记录到 `context/errors/ERRORS.jsonl`,不存储在CLAUDE.md

```yaml
M - Mistake (错误):
  🏷️ Type: LOGIC/SYNTAX/PERMISSION/TOOL_USE/FILE_OP/INTEGRATION/PERFORMANCE
  📊 Severity: CRITICAL/HIGH/MEDIUM/LOW
  🎯 Failed Action: [具体失败的操作]
  💡 Learning Value: [为什么这个错误重要]
  错误完整上下文: [完整错误信息、堆栈追踪、相关状态]

恢复策略:
  🏷️ Strategy: ROLLBACK/REPAIR/REBUILD/WORKAROUND
  📝 Steps: [详细恢复步骤]
  ⏱️ Recovery Time: [实际恢复用时]

A - Acknowledgment (承认):
  📝 Root Cause: [深度根因分析]
  💡 Wrong Understanding: [错误的理解]
  ✅ Correct Understanding: [正确的理解]

N - New Understanding (新理解):
  🔑 Key Insights: [关键洞察,支持列表]
  🧠 Mental Model: [思维模型更新]

U - Updated Approach (更新方法):
  📋 Correct Workflow: [正确的工作流程,支持列表]
  ✓ Verification Checklist: [验证检查清单,支持列表]

S - Systematic Prevention (系统性预防):
  🔧 Prevention Rules: [预防规则,支持列表]
  📈 System Updates: [配置/代码变更]
  🔍 Patterns Identified: [识别的错误模式,可选]
```

**JSON输出格式**:
```json
{
  "error_id": "ERR-20251031-001",
  "timestamp": "2025-10-31T22:00:00.000Z",
  "date": "2025-10-31",
  "manus": {
    "mistake": {
      "type": "LOGIC",
      "severity": "HIGH",
      "failed_action": "...",
      "learning_value": "...",
      "context": "..."
    },
    "acknowledgment": {
      "root_cause": "...",
      "wrong_understanding": "...",
      "correct_understanding": "..."
    },
    "new_understanding": {
      "key_insights": ["..."],
      "mental_model": "..."
    },
    "updated_approach": {
      "correct_workflow": ["..."],
      "verification_checklist": ["..."]
    },
    "systematic_prevention": {
      "prevention_rules": ["..."],
      "system_updates": "...",
      "patterns_identified": ["..."]
    }
  },
  "recovery": {
    "strategy": "REPAIR",
    "steps": ["..."],
    "recovery_time": "15min"
  },
  "metadata": {
    "project": "...",
    "file_path": "...",
    "level": "项目级别"
  }
}
```

---

### ✅ SUCCESS (成功经验)

```yaml
必需字段:
  - 🏷️ Type: IMPLEMENTATION/OPTIMIZATION/INTEGRATION/DEBUGGING
  - 📊 Value Level: HIGH/MEDIUM/LOW
  - 🎯 Problem Solved: [解决的原始问题]
  - 📈 Impact: [可衡量的改进]

可选字段:
  - 💡 Reusability: [如何应用到其他场景]
  - 🔗 Related Files: [实现文件路径]
  - **Solution Template**: [可复用的模板]
```

---

### 🧠 INSIGHTS (技术洞察)

```yaml
必需字段:
  - 📊 Depth Level: SURFACE/MODERATE/DEEP/BREAKTHROUGH
  - 🏷️ Domain: [技术领域]
  - 💡 Core Insight: [详细解释洞察]

可选字段:
  - 📚 Theoretical Basis: [为什么这样有效]
  - 🛠️ Practical Techniques: [如何应用]
  - 📈 Innovation: INCREMENTAL/SIGNIFICANT/BREAKTHROUGH
  - 🔗 References: [文档、文章、文件路径]
```

---

### 🔍 PATTERNS (模式识别)

```yaml
必需字段:
  - 🏷️ Category: ERROR_PATTERN/DESIGN_PATTERN/WORKFLOW_PATTERN
  - 📊 Frequency: [遇到频率]
  - 📝 Pattern Description: [详细模式描述]

可选字段:
  - 🎯 When to Apply: [触发条件]
  - ⚠️ Anti-Patterns: [要避免的做法]
  - 💡 Best Practices: [推荐方法]
  - 🔗 Examples: [文件路径指向示例]
```

---

### 📊 CONTEXT (上下文监控 - v3.0)

```yaml
必需字段:
  - 🎯 Action: CHECK/OPTIMIZE/ANALYZE
  - 📊 Focus: TOKEN_USAGE/SECTION_STATS/HEALTH_CHECK

输出:
  - context/analytics/context-health-{timestamp}.json

功能:
  - Token使用量统计
  - Section占用比例分析
  - 优化建议生成(压缩、归档)
```

**示例**:
```
🎯 Action: CHECK
📊 Focus: HEALTH_CHECK

检查当前CLAUDE.md的整体健康度
```

---

### 🧠 MEMORY (长期记忆 - v3.0)

```yaml
必需字段:
  - 🏷️ Type: PROJECT_DECISION/ARCHITECTURE/BUSINESS_RULE/TECHNICAL_INSIGHT
  - 📊 Priority: CRITICAL/HIGH/MEDIUM/LOW
  - 🔍 Searchable: [关键词列表,用于检索]

可选字段:
  - ⏰ Retention: PERMANENT/1Y/6M/3M
  - **为什么重要**: [记忆的价值和应用场景]
  - **相关上下文**: [关联的文件、决策、时间点]

输出:
  - context/memory/project-memory.json
```

**示例**:
```
🏷️ Type: ARCHITECTURE
📊 Priority: CRITICAL
🔍 Searchable: [Plugins, 架构决策, 业务单元]
⏰ Retention: PERMANENT

记忆内容:
项目采用 Plugins 作为核心架构单元...

为什么重要:
这是项目的核心架构决策,影响所有后续开发
```

---

### 📸 SNAPSHOT (快照管理 - v3.0)

```yaml
必需字段:
  - 🎯 Action: CREATE/RESTORE/LIST

CREATE操作:
  - 📝 Description: [快照描述]
  - 🏷️ Tags: [标签列表,用于分类]

RESTORE操作:
  - 📝 Description: [快照文件名或时间戳]

输出:
  - context/snapshots/CLAUDE-{timestamp}.md
```

**示例 - 创建**:
```
🎯 Action: CREATE
📝 Description: 完成manus.md v3.0优化前的快照
🏷️ Tags: [before-v3-upgrade, milestone]
```

**示例 - 恢复**:
```
🎯 Action: RESTORE
📝 Description: CLAUDE-20251031-220000
```

**示例 - 列表**:
```
🎯 Action: LIST
```

---

## 智能类型识别详细逻辑

### 识别优先级顺序

```python
识别顺序(优先级从高到低):

1. ERROR (最高优先级)
   关键词: "错误", "失败", "报错", "bug", "异常", "崩溃", "crash"
   结构: "预期vs实际", 堆栈追踪, "恢复"/"修复"过程

2. SUCCESS
   关键词: "成功", "解决了", "实现了", "完成", "突破", "优化"
   结构: 问题→解决方案, 可衡量改进数据("从X到Y")

3. INSIGHTS
   关键词: "洞察", "发现", "理解", "原理", "机制", "本质"
   结构: 理论解释 + 实践应用

4. PATTERNS
   关键词: "模式", "pattern", "重复", "最佳实践", "反模式"
   结构: 应用时机 + 正确做法 vs 错误做法

5. CONTEXT (v3.0)
   关键词: "上下文", "context", "token", "监控", "优化"
   结构: token统计, section分析

6. MEMORY (v3.0)
   关键词: "记忆", "memory", "记住", "长期", "持久化"
   结构: 明确表示"需要记住", 架构决策

7. SNAPSHOT (v3.0)
   关键词: "快照", "snapshot", "备份", "版本", "恢复"
   结构: 创建快照, 版本管理, 恢复操作

8. TODO
   关键词: "待办", "任务", "需要", "要做", "todo", "清单"
   结构: 列表形式(≥2个项目符号), 状态标识

9. FOCUS
   关键词: "专注", "集中", "当前任务", "注意力", "优先级"
   结构: 时间估计, 成功标准描述

10. PROCESS
    关键词: "流程", "步骤", "过程", "工作流", "workflow"
    结构: 步骤序列(Step1→Step2), 用时记录

11. 默认策略
    - 简短(<100字符) → FOCUS
    - 列表(≥3行) → TODO
    - 详细叙述 → INSIGHTS
```

### 识别依据输出示例

```yaml
ERROR类型:
  💡 识别依据: 包含关键词'错误'、'异常',包含预期vs实际对比结构,提及修复过程

SUCCESS类型:
  💡 识别依据: 包含关键词'成功'、'优化',包含可衡量改进数据,包含问题→解决方案结构

TODO类型:
  💡 识别依据: 列表结构(3个以上项目符号),包含关键词'任务'、'需要'

FOCUS类型:
  💡 识别依据: 包含时间估计('3小时'),包含成功标准描述,包含关键词'专注'

CONTEXT类型:
  💡 识别依据: 包含关键词'token'、'上下文',提及监控和分析

MEMORY类型:
  💡 识别依据: 包含关键词'架构决策'、'关键',明确表示需要记住

默认策略:
  💡 识别依据: 基于内容综合判断(内容长度200字符,包含详细解释)
```

---

## 双层级分类决策树

```python
def classify_level(content: str) -> tuple[str, str]:
    """
    双层级分类决策

    Returns:
        (level, target_file): 级别和目标文件路径
    """

    # Step 1: 强匹配项目级别
    project_keywords = [
        "本项目", "当前项目", "当前业务",
        "项目配置", "本地开发",
        # 项目名称(动态检测)
    ]
    if any(kw in content for kw in project_keywords):
        return ("项目级别", "CLAUDE.md")

    # Step 2: 强匹配全局级别
    global_keywords = [
        "跨项目", "通用", "框架",
        "最佳实践", "可复用",
        "技术洞察", "工具使用"
    ]
    if any(kw in content for kw in global_keywords):
        return ("全局级别", "~/.claude/CLAUDE.md")

    # Step 3: 特殊情况 - 文件路径检测
    if contains_project_file_path(content):
        return ("项目级别", "CLAUDE.md")

    # Step 4: 默认策略
    # 当无法明确判断时,默认项目级别(更安全)
    log_classification_uncertainty(content)
    return ("项目级别", "CLAUDE.md")


def contains_project_file_path(content: str) -> bool:
    """检测是否包含当前项目的文件路径"""
    project_paths = [
        ".claude/", "plugins/", "PRPs/",
        "context/", "output/", "reports/"
    ]
    return any(path in content for path in project_paths)
```

### Tie-Breaker规则

```yaml
当同时包含项目和全局指标时:
  示例: "本项目使用通用的React最佳实践"
  包含: "本项目"(项目指标) + "通用"(全局指标)

  Tie-Breaker逻辑:
    → 默认选择: 项目级别
    → 理由: 更安全、更具体、避免全局污染
    → 日志: 记录分类不确定性供后续审查
```

---

## ERROR类型MANUS五步法

### 完整JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["error_id", "timestamp", "date", "manus"],
  "properties": {
    "error_id": {
      "type": "string",
      "pattern": "^ERR-\\d{8}-\\d{3}$",
      "description": "格式: ERR-YYYYMMDD-NNN"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601格式"
    },
    "date": {
      "type": "string",
      "format": "date"
    },
    "manus": {
      "type": "object",
      "required": ["mistake", "acknowledgment", "new_understanding", "updated_approach", "systematic_prevention"],
      "properties": {
        "mistake": {
          "type": "object",
          "required": ["type", "severity", "failed_action", "context"],
          "properties": {
            "type": {
              "enum": ["LOGIC", "SYNTAX", "PERMISSION", "TOOL_USE", "FILE_OP", "INTEGRATION", "PERFORMANCE"]
            },
            "severity": {
              "enum": ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
            },
            "failed_action": "string",
            "learning_value": "string",
            "context": "string"
          }
        },
        "acknowledgment": {
          "type": "object",
          "required": ["root_cause", "wrong_understanding", "correct_understanding"],
          "properties": {
            "root_cause": "string",
            "wrong_understanding": "string",
            "correct_understanding": "string"
          }
        },
        "new_understanding": {
          "type": "object",
          "required": ["key_insights"],
          "properties": {
            "key_insights": {
              "type": "array",
              "items": "string"
            },
            "mental_model": "string"
          }
        },
        "updated_approach": {
          "type": "object",
          "required": ["correct_workflow"],
          "properties": {
            "correct_workflow": {
              "type": "array",
              "items": "string"
            },
            "verification_checklist": {
              "type": "array",
              "items": "string"
            }
          }
        },
        "systematic_prevention": {
          "type": "object",
          "required": ["prevention_rules"],
          "properties": {
            "prevention_rules": {
              "type": "array",
              "items": "string"
            },
            "system_updates": "string",
            "patterns_identified": {
              "type": "array",
              "items": "string"
            }
          }
        }
      }
    },
    "recovery": {
      "type": "object",
      "properties": {
        "strategy": {
          "enum": ["ROLLBACK", "REPAIR", "REBUILD", "WORKAROUND"]
        },
        "steps": {
          "type": "array",
          "items": "string"
        },
        "recovery_time": "string"
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "project": "string",
        "file_path": "string",
        "level": {
          "enum": ["全局级别", "项目级别"]
        }
      }
    },
    "learning_integration": {
      "type": "object",
      "properties": {
        "learned_analyzed": "boolean",
        "analyzed_date": "string",
        "patterns_extracted": {
          "type": "array",
          "items": "string"
        }
      }
    }
  }
}
```

---

## 缓存优化最佳实践

### 1. 稳定前缀模式

**规则**:
```yaml
格式: 🕐 [ISO 8601 Timestamp] [Type Icon] [Type]:

时间戳格式:
  ✅ 正确: 2025-10-31T22:00:00
  ❌ 错误: 2025-10-31 22:00:00 (无T分隔)
  ❌ 错误: 22:00:00 2025-10-31 (顺序错误)

完整示例:
  🕐 2025-10-31T22:00:00 🎯 FOCUS: 实现MANUS命令
  🕐 2025-10-31T22:15:00 📋 TODO: 创建skill包
  🕐 2025-10-31T22:30:00 ❌ ERROR: 分类逻辑失败
```

**缓存优势**:
```yaml
共享前缀长度:
  - "🕐 2025-10-" → 所有10月条目共享
  - "🕐 2025-10-31T" → 所有31日条目共享
  - "🕐 2025-10-31T22:" → 所有22点条目共享

成本对比:
  - 稳定前缀: $0.30/MTok (缓存命中率90%)
  - 不稳定: $3.00/MTok (缓存命中率10%)
  - 差异: 10倍成本
```

### 2. 仅追加更新原则

**禁止操作**:
```yaml
❌ 修改已有条目
❌ 删除历史记录
❌ 重新排序条目
❌ 改变时间戳
```

**正确操作**:
```yaml
✅ 追加新条目
✅ 通过新条目更新状态
✅ 引用前一条目时间戳
✅ 保持完整历史

状态更新示例:
  # 第1次记录
  🕐 2025-10-31T22:00:00 ⭕ TODO: 实现功能X
  - Status: Pending

  # 第2次记录(更新状态)
  🕐 2025-10-31T22:30:00 🔄 TODO: 实现功能X
  - Status: Pending → InProgress
  - Reference: 2025-10-31T22:00:00

  # 第3次记录(完成)
  🕐 2025-10-31T23:00:00 ✅ TODO: 实现功能X
  - Status: InProgress → Done
  - Reference: 2025-10-31T22:30:00
```

### 3. 可恢复压缩

**文件引用**:
```yaml
Instead of:
  [完整文件内容,1000行代码]

Use:
  🔗 Related Files: /path/to/file.ts:123-156
  🔗 Implementation: src/manus/core_engine.py:45
```

**URL引用**:
```yaml
Instead of:
  [完整网页内容,3000字]

Use:
  🔗 References: https://docs.example.com/article#section-3
  🔗 Documentation: https://claude.com/code/skills
```

**代码片段**:
```yaml
保留(学习信号):
  ✅ 错误堆栈追踪(完整)
  ✅ 解决方案代码(核心部分)
  ✅ 配置示例(关键配置)

压缩(可恢复引用):
  🔗 大文件内容 → 文件路径:行号
  🔗 长网页 → URL + 章节锚点
  🔗 大段代码 → 代码仓库链接
```

### 4. 缓存断点注释

**作用**:
```yaml
标记更新边界:
  - 明确指示缓存失效点
  - 帮助LLM理解section结构
  - 优化token缓存策略
```

**使用方法**:
```markdown
## 🎯 FOCUS

### Active Attention Anchors

#### 🕐 2025-10-31T22:00:00 🎯 Current Focus: 实现MANUS
- 📊 Priority: HIGH
- ⏱️ Duration: 3h
- 🎯 Success: 命令完全实现

<!-- Cache Breakpoint: Focus section updated -->
```

---

## 完整工作流示例

### 场景: 遇到错误并完整恢复

```bash
# 用户输入(无需显式指定类型)
content = """
尝试分类"本项目使用通用React模式"时出错。
预期: 默认项目级别
实际: 抛出分类异常("模糊分类")
原因: 同时包含"本项目"和"通用"关键词

恢复过程:
1. 添加tie-breaker规则
2. 更新分类逻辑
3. 扩展测试用例
用时: 15分钟

根因: 设计规范未覆盖边界情况
教训: 需要完善决策树,处理模糊输入
预防: 添加边界测试,日志记录不确定性
"""

# 执行流程
→ Step 1: 智能类型识别
   分析关键词: "出错", "预期vs实际", "恢复过程"
   识别类型: ❌ ERROR

→ Step 2: 分类判断
   检测关键词: "本项目"
   分类级别: 项目级别

→ Step 3: 生成错误ID
   当前错误数: 15
   错误ID: ERR-20251031-016

→ Step 4: 构建MANUS JSON
   {
     "error_id": "ERR-20251031-016",
     "timestamp": "2025-10-31T22:45:00.000Z",
     "manus": {
       "mistake": {...},
       "acknowledgment": {...},
       "new_understanding": {...},
       "updated_approach": {...},
       "systematic_prevention": {...}
     }
   }

→ Step 5: 写入ERRORS.jsonl
   追加到: context/errors/ERRORS.jsonl
   行号: #16

→ Step 6: 更新CLAUDE.md统计
   Section: # ❌ ERROR
   更新: 总错误数 +1

→ Step 7: 输出确认
   ✅ 错误已记录到结构化日志系统
   📊 错误ID: ERR-20251031-016
   📁 存储位置: context/errors/ERRORS.jsonl:#16
   🔗 查看: !tail -1 context/errors/ERRORS.jsonl | jq '.'
   📈 总错误数: 16
```

---

## 技术实现细节

### Python依赖

```python
# requirements.txt
pyyaml>=6.0
python-dateutil>=2.8.0

# 可选(用于JSON验证)
jsonschema>=4.0.0
```

### 关键函数实现

```python
# scripts/core_engine.py

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

def execute_manus(
    content: str,
    explicit_type: Optional[str] = None
) -> dict:
    """主执行函数"""

    # 1. 类型识别
    if explicit_type:
        manus_type = explicit_type
        detection_method = "显式指定"
        detection_reason = ""
    else:
        manus_type, detection_reason = auto_detect_type(content)
        detection_method = "智能识别"

    # 2. 分类判断
    level, target_file = classify_level(content)

    # 3. 生成条目
    if manus_type == "error":
        result = handle_error_type(content, level)
    else:
        result = handle_general_type(
            content, manus_type, level, target_file
        )

    # 4. 返回结果
    return {
        "type": manus_type,
        "level": level,
        "target_file": target_file,
        "detection_method": detection_method,
        "detection_reason": detection_reason,
        **result
    }
```

---

## 常见问题

### Q1: 如何手动覆盖智能识别?

```bash
# 智能识别可能误判时
# 方法1: 在上下文中明确指定(推荐)
context_manager调用时传入:
  execute_manus(content, explicit_type="focus")

# 方法2: 在内容开头添加类型标识
content = "[TYPE:FOCUS] 当前任务是..."
```

### Q2: ERROR类型为什么不存储在CLAUDE.md?

```yaml
原因:
  1. 结构化需求 - JSONL支持完整MANUS五步法
  2. 可分析性 - JSON格式便于 /learn 命令分析
  3. 可扩展性 - 易于添加字段(如patterns_extracted)
  4. 性能优化 - CLAUDE.md保持简洁,避免token膨胀

查询方式:
  - 最新错误: !tail -1 context/errors/ERRORS.jsonl | jq '.'
  - 所有错误: !cat context/errors/ERRORS.jsonl | jq '.'
  - 按类型: !grep '"type":"LOGIC"' context/errors/ERRORS.jsonl
  - 深度分析: /learn 命令
```

### Q3: 如何处理分类不确定的情况?

```yaml
策略:
  1. Tie-Breaker规则: 默认项目级别
  2. 日志记录: 记录不确定性供审查
  3. 后续迁移: 可通过手动或自动方式迁移

日志示例:
  log_classification_uncertainty({
    "content": "...",
    "project_indicators": ["本项目"],
    "global_indicators": ["通用"],
    "decision": "项目级别(tie-breaker)"
  })
```

---

**文档版本**: v3.0.0 | **更新**: 2025-10-31
**维护**: 与SKILL.md同步更新
