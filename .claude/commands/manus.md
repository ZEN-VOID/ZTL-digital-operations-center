---
description: "基于MANUS上下文工程的统一上下文管理系统，整合注意力管理、错误学习和知识沉淀，支持智能类型识别和全局/项目双层级分类机制"
allowed-tools: ["Read", "Write", "Edit", "Grep"]
version: "2.1.0"
argument-hint: "[type] [multi-line parameters] 或 [content] (智能识别)"
last-updated: "2025-10-23"
---
# manus - 统一上下文管理系统

> **M**istake **A**cknowledgment **N**ew Understanding **U**pdated Approach **S**ystematic Prevention
> 基于生产级AI系统的上下文工程原则，实现高效的注意力管理、错误学习和知识积累

---

## 🎯 核心原则

本命令整合了三个原命令(C/X/Z)的功能，实现统一的上下文管理：

```yaml
MANUS上下文工程原则:
  KV缓存优化: 稳定前缀 + 仅追加结构 → 10倍成本优势
  注意力管理: 任务重述机制 → 解决"中间丢失"问题
  错误保存: 完整上下文保存 → 最清晰的智能体行为指标
  文件系统上下文: 无限持久化外部记忆
  可恢复压缩: 保留恢复路径(URL/文件路径)而非完整内容

双层级识别机制:
  全局级别: ~/.claude/CLAUDE.md (跨所有项目/框架)
  项目级别: CLAUDE.md (当前项目特定)
```

---

## 📋 使用方法

### 基本语法

```bash
# 显式指定类型
/manus [TYPE] [PARAMETERS]

# 智能类型识别（推荐）
/manus [CONTENT]

类型 (Types):
  focus    - 🎯 记录当前注意力焦点
  todo     - 📋 任务管理和注意力锚点
  process  - ⚙️ 流程执行记录
  error    - ❌ 错误保存和恢复学习
  success  - ✅ 成功经验和解决方案
  insights - 🧠 技术洞察和实践技巧
  patterns - 🔍 模式识别和最佳实践
```

### 🤖 智能类型识别

**当用户执行 `/manus` 而未显式指定类型时，系统将智能分析输入内容，自动判断应该使用哪种类型。**

```yaml
识别逻辑:

  ERROR类型识别:
    关键词:
      - "错误" "失败" "报错" "bug" "issue"
      - "异常" "崩溃" "crash" "exception"
      - "不工作" "无法" "无效"
    结构特征:
      - 包含堆栈追踪
      - 包含错误代码
      - 包含"预期 vs 实际"对比
      - 提及恢复/修复过程
    判断: → error

  FOCUS类型识别:
    关键词:
      - "专注" "集中" "当前任务" "正在做"
      - "注意力" "焦点" "优先级"
      - "接下来" "计划做"
    结构特征:
      - 包含时间估计
      - 包含成功标准
      - 包含优先级标识
    判断: → focus

  TODO类型识别:
    关键词:
      - "待办" "任务" "需要" "要做"
      - "TODO" "清单" "checklist"
      - "依赖" "blocked" "阻塞"
    结构特征:
      - 列表形式
      - 包含状态标识（待处理/进行中/完成）
      - 包含依赖关系
    判断: → todo

  SUCCESS类型识别:
    关键词:
      - "成功" "解决了" "实现了" "完成"
      - "突破" "优化" "改进"
      - "效果" "收益" "提升"
    结构特征:
      - 包含问题→解决方案结构
      - 包含可衡量的改进数据
      - 包含可复用的方法
    判断: → success

  INSIGHTS类型识别:
    关键词:
      - "洞察" "发现" "理解"
      - "原理" "机制" "为什么"
      - "深度" "本质" "根本"
    结构特征:
      - 包含理论解释
      - 包含实践应用
      - 跨领域适用性
    判断: → insights

  PATTERNS类型识别:
    关键词:
      - "模式" "pattern" "重复"
      - "最佳实践" "反模式" "anti-pattern"
      - "设计模式" "工作流模式"
    结构特征:
      - 包含应用时机
      - 包含正确做法 vs 错误做法
      - 包含多个示例
    判断: → patterns

  PROCESS类型识别:
    关键词:
      - "流程" "步骤" "过程"
      - "工作流" "workflow" "pipeline"
      - "执行" "操作"
    结构特征:
      - 包含步骤序列（Step1 → Step2）
      - 包含用时记录
      - 包含结果状态
    判断: → process

默认策略:
  如果无法明确判断类型:
    - 检查内容长度和复杂度
    - 简短描述 → focus
    - 列表形式 → todo
    - 详细叙述 → insights
    - 默认兜底 → process
```

**识别示例**:

```bash
# 示例1: 自动识别为 ERROR
/manus
遇到了分类逻辑错误，条目同时包含"本项目"和"通用"关键词时产生歧义。
预期应该默认为项目级别，但实际抛出了分类异常。
已通过添加tie-breaker逻辑修复。

→ 系统识别: ❌ ERROR (包含"错误"、"异常"、"修复"等关键词)

# 示例2: 自动识别为 SUCCESS
/manus
成功实现了KV-cache优化，通过稳定前缀模式将token成本从$3.00降低到$0.30，
实现了10倍成本节约。方法可以应用到所有上下文管理场景。

→ 系统识别: ✅ SUCCESS (包含"成功"、"优化"、可衡量改进数据)

# 示例3: 自动识别为 TODO
/manus
需要完成以下任务:
- 实现MANUS命令
- 更新文档
- 运行测试

→ 系统识别: 📋 TODO (列表形式，包含"需要"、"任务"等关键词)

# 示例4: 自动识别为 FOCUS
/manus
接下来3小时专注实现MANUS统一上下文管理命令，
成功标准是命令文件创建并通过所有测试。

→ 系统识别: 🎯 FOCUS (包含时间估计、成功标准、"专注"等关键词)
```

**手动覆盖**:

如果自动识别不准确，始终可以显式指定类型：

```bash
/manus error [CONTENT]    # 强制作为ERROR类型
/manus focus [CONTENT]    # 强制作为FOCUS类型
# ... 以此类推
```

---

## 🔍 分类逻辑

```yaml
双层级分类决策:

  问题1: "这是否仅限于当前项目?"
    YES → 项目级别 (CLAUDE.md)
      示例:
        - 项目特定配置错误
        - 本地开发工作流
        - 项目业务逻辑洞察
        - 当前项目任务清单

    NO → 继续问题2

  问题2: "这是否可跨项目/框架复用?"
    YES → 全局级别 (~/.claude/CLAUDE.md)
      示例:
        - 通用编程模式
        - 工具使用技巧
        - 跨项目工作流
        - 可复用错误解决方案

    NO → 不确定,默认项目级别

分类关键词:
  全局级别指标:
    - "跨项目" "通用" "框架"
    - "最佳实践" "可复用"
    - "技术洞察" "工具使用"

  项目级别指标:
    - "本项目" "当前业务"
    - "项目配置" "本地开发"
    - 提及项目名称
    - 当前项目特定文件路径
```

---

## 📝 参数模板

根据不同类型，使用以下多行参数模板：

### 🎯 FOCUS (注意力焦点)

```
/manus focus
📊 Priority: HIGH/MEDIUM/LOW
⏱️ Duration: [预计时长]
🎯 Success: [具体可衡量的成功标准]
💭 Rationale: [为什么这是当前焦点]

[当前焦点的详细描述]
```

**示例**:

```
/manus focus
📊 Priority: HIGH
⏱️ Duration: 4h
🎯 Success: MANUS命令实现并通过所有测试
💭 Rationale: 上下文管理系统整合是v2.0关键功能

实现MANUS统一上下文管理命令，整合C/X/Z三个命令的功能
```

---

### 📋 TODO (任务管理)

```
/manus todo
🏷️ Type: DEV/DOC/CONFIG/TEST/REVIEW/DEPLOY/RESEARCH
📊 Priority: HIGH/MEDIUM/LOW
🎯 Completion: [具体完成标准]
🔗 Dependencies: [任务ID或文件路径]

[任务详细描述]
```

**状态标识**:

- ⭕ Pending (待处理)
- 🔄 InProgress (进行中)
- ✅ Done (已完成)
- ❌ Cancelled (已取消)
- 🚫 Blocked (被阻塞)
- ⏸️ Paused (已暂停)

**示例**:

```
/manus todo
🏷️ Type: DEV
📊 Priority: HIGH
🎯 Completion: 命令文件创建并可正常执行
🔗 Dependencies: 设计文档已完成

创建MANUS.md命令文件，实现7个核心功能模块
```

---

### ⚙️ PROCESS (流程记录)

```
/manus process
🏷️ Type: DEVELOP/DEBUG/OPTIMIZE/LEARN/REVIEW/REFACTOR
📝 Key Steps: [步骤1] → [步骤2] → [步骤3]
⏱️ Duration: [实际用时]
💡 Learnings: [关键收获]
🔗 Related Files: [相关文件路径]
📊 Outcome: SUCCESS/PARTIAL/FAILED

[流程详细描述]
```

**示例**:

```
/manus process
🏷️ Type: DEVELOP
📝 Key Steps: 设计 → 实现 → 测试 → 部署
⏱️ Duration: 6h
💡 Learnings: 双层级分类比三层级更清晰高效
🔗 Related Files: .claude/commands/MANUS.md
📊 Outcome: SUCCESS

完成MANUS命令从设计到实现的完整流程
```

---

### ❌ ERROR (错误记录)

> **MANUS技巧**: M-istake, A-cknowledgment, N-ew Understanding, U-pdated Approach, S-ystematic Prevention
> **存储**: 记录到 `learning/errors/ERRORS.jsonl` (结构化JSON)
> **闭环**: /manus error写入 → /learn读取 → 系统优化

```
/manus error
🏷️ Type: LOGIC/SYNTAX/PERMISSION/TOOL_USE/FILE_OP/INTEGRATION/PERFORMANCE
📊 Severity: CRITICAL/HIGH/MEDIUM/LOW
🎯 Failed Action: [具体失败的操作]
💡 Learning Value: [为什么这个错误重要]

错误完整上下文:
[完整错误信息、堆栈追踪、相关状态]

恢复策略:
🏷️ Strategy: ROLLBACK/REPAIR/REBUILD/WORKAROUND
📝 Steps: [详细恢复步骤]
⏱️ Recovery Time: [实际恢复用时]

根因分析 (MANUS - Acknowledgment & New Understanding):
📝 Root Cause: [深度根因分析]
💡 Wrong Understanding: [错误的理解]
✅ Correct Understanding: [正确的理解]
🔑 Key Insights: [关键洞察，支持列表]

更新方法 (MANUS - Updated Approach):
📋 Correct Workflow: [正确的工作流程，支持列表]
✓ Verification Checklist: [验证检查清单，支持列表]

系统性预防 (MANUS - Systematic Prevention):
🔧 Prevention Rules: [预防规则，支持列表]
📈 System Updates: [配置/代码变更]
🔍 Patterns Identified: [识别的错误模式，可选]
```

**示例**:

```
/manus error
🏷️ Type: LOGIC
📊 Severity: HIGH
🎯 Failed Action: 分类同时包含全局和项目指标的条目
💡 Learning Value: 需要明确的tie-breaker逻辑处理模糊情况

错误完整上下文:
Entry: "本项目使用通用的React最佳实践"
包含: "本项目" (项目指标) 和 "通用" (全局指标)
分类: 失败，产生歧义错误
预期: 按设计规范默认为项目级别

恢复策略:
🏷️ Strategy: REPAIR
📝 Steps:
  1. 添加tie-breaker: 两种指标同时存在时默认项目级别
  2. 添加模糊情况日志记录
  3. 更新分类测试用例
⏱️ Recovery Time: 15分钟

根因分析:
📝 Root Cause: 设计规范未覆盖模糊情况
🔧 Prevention: 添加明确的tie-breaker逻辑和边界情况测试
📈 System Updates: 分类逻辑更新、测试套件扩展
```

---

### ✅ SUCCESS (成功经验)

```
/manus success
🏷️ Type: IMPLEMENTATION/OPTIMIZATION/INTEGRATION/DEBUGGING
📊 Value Level: HIGH/MEDIUM/LOW
🎯 Problem Solved: [解决的原始问题]
📈 Impact: [可衡量的改进]
💡 Reusability: [如何应用到其他场景]
🔗 Related Files: [实现文件路径]

解决方案详细描述:
[详细解决方案，包含代码/配置示例]

解决方案模板 (如适用):
[可复用的模板]
```

**示例**:

```
/manus success
🏷️ Type: OPTIMIZATION
📊 Value Level: HIGH
🎯 Problem Solved: KV缓存利用率低，token成本高
📈 Impact: 10倍成本降低 ($3.00/MTok → $0.30/MTok)
💡 Reusability: 稳定前缀模式适用于所有上下文管理
🔗 Related Files: .claude/commands/MANUS.md

解决方案详细描述:
使用稳定的时间戳前缀格式:
🕐 [ISO 8601 Timestamp] [Icon] [Type]:

优势:
1. 时间戳在前 → 所有条目共享稳定前缀
2. 仅追加更新 → 保持上下文确定性
3. 最大化缓存复用 → 显著降低成本

解决方案模板:
所有上下文条目使用格式: 🕐 YYYY-MM-DDTHH:mm:ss [Emoji] [Type]: [Content]
```

---

### 🧠 INSIGHTS (技术洞察)

```
/manus insights
📊 Depth Level: SURFACE/MODERATE/DEEP/BREAKTHROUGH
🏷️ Domain: [技术领域]
💡 Innovation: INCREMENTAL/SIGNIFICANT/BREAKTHROUGH

核心洞察:
[详细解释洞察]

理论基础:
[为什么这样有效]

实践技巧:
[如何应用]

参考资料:
[文档、文章、文件路径]
```

**示例**:

```
/manus insights
📊 Depth Level: DEEP
🏷️ Domain: 上下文工程
💡 Innovation: SIGNIFICANT

核心洞察:
错误保存是真实智能体行为的最清晰指标。完整保存错误上下文(堆栈追踪、状态)提供了不可替代的学习信号。

理论基础:
1. 成功路径是确定的,错误路径揭示边界情况
2. 错误恢复展示适应性学习能力
3. 完整上下文支持根因分析和系统性预防

实践技巧:
1. 保存完整堆栈追踪,不要截断
2. 记录失败时的完整状态
3. 文档化恢复过程和根因分析
4. 将错误转化为系统改进

参考资料:
- MANUS上下文工程技术 (dev.to)
- .claude/commands/MANUS.md
- PRPs/in-progress/MANUS-command-restructuring-design-v1.0.md
```

---

### 🔍 PATTERNS (模式识别)

```
/manus patterns
🏷️ Category: ERROR_PATTERN/DESIGN_PATTERN/WORKFLOW_PATTERN
📊 Frequency: [遇到频率]

模式描述:
[详细模式描述]

应用时机:
[触发条件]

反模式:
[要避免的做法]

最佳实践:
[推荐方法]

示例:
[文件路径指向示例]
```

**示例**:

```
/manus patterns
🏷️ Category: DESIGN_PATTERN
📊 Frequency: 常见

模式描述:
三层级配置系统 (机器/系统/项目) 导致分类混淆和维护复杂度

应用时机:
当配置层级超过2层时，考虑是否真的需要中间层

反模式:
- 创建不清晰的中间层级 (如"系统级")
- 三层或更多层的配置层级
- 层级边界模糊不清

最佳实践:
- 使用双层级: 全局 vs 特定
- 清晰的分类标准: "可复用" vs "特定场景"
- 默认策略处理模糊情况

示例:
- PRPs/in-progress/MANUS-command-restructuring-design-v1.0.md
- ~/.claude/CLAUDE.md (全局级别)
- CLAUDE.md (项目级别)
```

---

## ⚙️ 执行逻辑

当你执行 `/manus [type] [parameters]` 或 `/manus [content]` 时，本命令将:

### 第1步: 解析参数与智能类型识别

```python
# 步骤1.1: 检查是否显式指定类型
if first_word in ["focus", "todo", "process", "error", "success", "insights", "patterns"]:
    type = first_word
    content = remaining_arguments
    source = "显式指定"
else:
    # 步骤1.2: 智能类型识别
    content = full_arguments
    type = auto_detect_type(content)
    source = "智能识别"

# 步骤1.3: 类型识别算法
def auto_detect_type(content):
    """
    基于关键词和结构特征智能识别类型
    """
    content_lower = content.lower()

    # ERROR类型识别 (优先级最高)
    error_keywords = ["错误", "失败", "报错", "bug", "issue", "异常",
                      "崩溃", "crash", "exception", "不工作", "无法", "无效"]
    error_structures = ["预期", "实际", "堆栈", "stack", "恢复", "修复"]

    if (any(kw in content_lower for kw in error_keywords) or
        any(kw in content_lower for kw in error_structures)):
        return "error"

    # SUCCESS类型识别
    success_keywords = ["成功", "解决了", "实现了", "完成", "突破",
                        "优化", "改进", "效果", "收益", "提升"]
    if (any(kw in content_lower for kw in success_keywords) and
        ("→" in content or "从" in content and "到" in content)):
        return "success"

    # INSIGHTS类型识别
    insights_keywords = ["洞察", "发现", "理解", "原理", "机制",
                         "为什么", "深度", "本质", "根本"]
    if any(kw in content_lower for kw in insights_keywords):
        return "insights"

    # PATTERNS类型识别
    patterns_keywords = ["模式", "pattern", "重复", "最佳实践",
                         "反模式", "anti-pattern", "设计模式"]
    if any(kw in content_lower for kw in patterns_keywords):
        return "patterns"

    # TODO类型识别
    todo_keywords = ["待办", "任务", "需要", "要做", "todo", "清单", "checklist"]
    todo_structures = content.count("-") >= 2 or content.count("•") >= 2

    if any(kw in content_lower for kw in todo_keywords) or todo_structures:
        return "todo"

    # FOCUS类型识别
    focus_keywords = ["专注", "集中", "当前任务", "正在做", "注意力",
                      "焦点", "优先级", "接下来", "计划做"]
    focus_structures = ("小时" in content or "h" in content or
                        "成功标准" in content)

    if (any(kw in content_lower for kw in focus_keywords) or
        focus_structures):
        return "focus"

    # PROCESS类型识别
    process_keywords = ["流程", "步骤", "过程", "工作流", "workflow",
                        "pipeline", "执行", "操作"]
    process_structures = "→" in content or ("step" in content_lower)

    if (any(kw in content_lower for kw in process_keywords) or
        process_structures):
        return "process"

    # 默认策略
    if len(content) < 100:
        return "focus"  # 简短描述默认为焦点
    elif content.count("\n") >= 3:
        return "todo"   # 多行列表默认为任务
    else:
        return "insights"  # 详细叙述默认为洞察

# 步骤1.4: 解析多行参数
parsed_params = parse_multiline_parameters(content)
# - 提取emoji标记的字段
# - 保留完整文本内容
# - 处理MANUS五步法特殊字段(对于error类型)

# 步骤1.5: 验证必需字段完整性
validate_required_fields(type, parsed_params)

# 步骤1.6: 输出识别结果
print(f"🤖 类型识别: {type_icon[type]} {type.upper()}")
print(f"📊 识别方式: {source}")
if source == "智能识别":
    print(f"💡 识别依据: {get_detection_reason(type, content)}")
```

**识别依据说明**:

```python
def get_detection_reason(type, content):
    """
    返回类型识别的具体依据，帮助用户理解识别逻辑
    """
    reasons = []

    if type == "error":
        if "错误" in content:
            reasons.append("包含关键词'错误'")
        if "预期" in content and "实际" in content:
            reasons.append("包含预期vs实际对比结构")
        if "恢复" in content or "修复" in content:
            reasons.append("提及恢复/修复过程")

    elif type == "success":
        if "成功" in content:
            reasons.append("包含关键词'成功'")
        if "→" in content or ("从" in content and "到" in content):
            reasons.append("包含问题→解决方案结构")

    # ... 其他类型类似

    return ", ".join(reasons) if reasons else "基于内容综合判断"
```


### 第2步: 分类判断

```python
分类决策树:
  if "本项目" in content or project_specific_keywords:
      level = "项目级别"
      target_file = "CLAUDE.md"
  elif "跨项目" in content or "通用" in content or reusable_keywords:
      level = "全局级别"
      target_file = "~/.claude/CLAUDE.md"
  else:
      # 默认策略
      level = "项目级别"
      target_file = "CLAUDE.md"
      log_classification_uncertainty()
```

### 第3步: 生成条目

**对于ERROR类型** (特殊处理):

```bash
# ERROR类型写入结构化JSON而非CLAUDE.md

1. 确保目录存在:
   !mkdir -p learning/errors/

2. 生成错误ID:
   error_count=$(grep -c "^{" learning/errors/ERRORS.jsonl 2>/dev/null || echo "0")
   error_id="ERR-$(date +%Y%m%d)-$(printf "%03d" $((error_count + 1)))"

3. 解析MANUS五步法参数:
   - Mistake: Type, Severity, Failed Action, Description, Context
   - Acknowledgment: Root Cause, Wrong Understanding, Correct Understanding
   - New Understanding: Key Insights, Mental Model
   - Updated Approach: Correct Workflow, Verification Checklist
   - Systematic Prevention: Prevention Rules, System Updates, Patterns

4. 生成完整JSON结构:
   {
     "error_id": "ERR-20251023-001",
     "timestamp": "2025-10-23T14:30:45.123Z",
     "date": "2025-10-23",
     "manus": {
       "mistake": {...},
       "acknowledgment": {...},
       "new_understanding": {...},
       "updated_approach": {...},
       "systematic_prevention": {...}
     },
     "impact": {...},
     "recovery": {...},
     "metadata": {...},
     "learning_integration": {...}
   }

5. 追加到ERRORS.jsonl:
   echo '{json}' >> learning/errors/ERRORS.jsonl

6. 更新CLAUDE.md第10章统计:
   - 错误总计 +1
   - 最新记录日期
   - 错误类型统计
   - 严重级别统计
```

**对于其他类型** (FOCUS/TODO/PROCESS/SUCCESS/INSIGHTS/PATTERNS):

```python
生成格式:
  timestamp = datetime.now().isoformat()  # ISO 8601
  icon = type_to_icon_map[type]

  entry_prefix = f"🕐 {timestamp} {icon} {Type}: "

  # 稳定前缀优化KV缓存
  entry = f"""
  #### {entry_prefix}[Title]
  - 📊 [Field1]: [Value1]
  - 🏷️ [Field2]: [Value2]
  ...

  [Content]
  """
```

### 第4步: 追加到文件

**对于ERROR类型**:

```bash
操作步骤:
  1. 写入 learning/errors/ERRORS.jsonl (行分隔JSON)
  2. 更新 CLAUDE.md 第10章统计摘要
  3. 不在 CLAUDE.md 中存储完整错误详情

注意事项:
  ✅ JSONL格式 (每行一个完整JSON对象)
  ✅ 包含完整MANUS五步法数据
  ✅ 支持 /learn 命令读取和分析
  ✅ CLAUDE.md 仅保留统计摘要和引用
```

**对于其他类型**:

```python
操作步骤:
  1. 读取目标CLAUDE.md文件
  2. 定位对应section (# 🎯 FOCUS / # 📋 TODO 等)
  3. 追加新条目 (append-only, 永不修改已有条目)
  4. 添加缓存断点注释
  5. 保存文件

注意事项:
  ✅ 仅追加,永不修改
  ✅ 保持完整历史
  ✅ 状态变更通过新条目记录
  ✅ 稳定前缀最大化缓存复用
```

### 第5步: 输出确认

**智能识别信息输出** (如适用):

```bash
🤖 智能类型识别
  - 📊 识别类型: {type_icon} {TYPE}
  - 💡 识别依据: {detection_reason}
  - 🔄 手动覆盖: 如需修改，请使用 /manus {correct_type} [content]
```

**对于ERROR类型**:

```bash
输出信息:
  - 🤖 类型识别: ❌ ERROR (智能识别/显式指定)
  - 💡 识别依据: 包含关键词'错误', 提及恢复过程 (仅智能识别时显示)
  - ✅ 错误已记录到结构化日志系统
  - 📊 错误信息:
      - 错误ID: ERR-20251023-001
      - 类型: LOGIC
      - 严重级别: HIGH
      - 时间戳: 2025-10-23T14:30:45Z
  - 📁 存储位置:
      - 主日志: learning/errors/ERRORS.jsonl
      - 行号: #N
  - 🔗 查看方式:
      - 查看最新: !tail -1 learning/errors/ERRORS.jsonl | jq '.'
      - 查看全部: !cat learning/errors/ERRORS.jsonl | jq '.'
      - 分析建议: 执行 /learn 进行深度分析
  - 📈 当前统计:
      - 总错误数: N
      - 本日错误: N
      - 恢复成功率: X%
```

**对于其他类型**:

```python
输出信息:
  - 🤖 类型识别: {icon} {TYPE} (智能识别/显式指定)
  - 💡 识别依据: {detection_reason} (仅智能识别时显示)
  - ✅ 条目已添加到 [level] ([file_path])
  - 📝 Section: [section_name]
  - 🕐 Timestamp: [timestamp]
  - 🔗 File Reference: [file_path]:#L[line_number]
```

**识别依据示例**:

```bash
示例1 - ERROR类型:
  💡 识别依据: 包含关键词'错误'、'异常'，包含预期vs实际对比结构

示例2 - SUCCESS类型:
  💡 识别依据: 包含关键词'成功'、'优化'，包含可衡量改进数据

示例3 - TODO类型:
  💡 识别依据: 列表结构(3个以上项目符号)，包含关键词'任务'

示例4 - FOCUS类型:
  💡 识别依据: 包含时间估计('3小时')，包含成功标准描述

示例5 - 默认策略:
  💡 识别依据: 基于内容综合判断(内容长度200字符，包含详细解释)
```

---

## 🔄 缓存优化策略

### 稳定前缀模式

```yaml
所有条目使用格式:
  🕐 [ISO 8601 Timestamp] [Type Icon] [Type]:

优势:
  - 时间戳在前 → 共享稳定前缀
  - 图标居中 → 视觉扫描
  - 类型居后 → 语义分组

示例:
  🕐 2025-10-23T14:30:00 🎯 Focus: Implementing MANUS
  🕐 2025-10-23T14:45:00 📋 TODO: Create command file
  🕐 2025-10-23T15:00:00 ❌ ERROR: Classification logic failed
```

### 仅追加更新

```yaml
原则:
  - 永不修改已有条目
  - 状态变更通过新条目记录
  - 使用时间戳引用前一条目

示例:
  🕐 2025-10-23T14:30:00 ⭕ TODO: Implement feature X
  - Status: Pending

  🕐 2025-10-23T15:00:00 🔄 TODO: Implement feature X
  - Status: Pending → InProgress
  - Reference: 2025-10-23T14:30:00

  🕐 2025-10-23T17:00:00 ✅ TODO: Implement feature X
  - Status: InProgress → Done
  - Reference: 2025-10-23T15:00:00
```

### 可恢复压缩

```yaml
文件路径引用:
  Instead of: [完整文件内容]
  Use: 🔗 Related Files: /path/to/file.ts:123

URL引用:
  Instead of: [完整网页内容]
  Use: 🔗 References: https://docs.example.com/article

代码片段:
  保留: 错误堆栈追踪 (学习信号)
  保留: 解决方案代码 (可复用性)
  压缩: 大文件内容 → 文件路径
```

---

## 📊 完整Section结构

### Section 1: 🎯 FOCUS

```markdown
## 🎯 FOCUS

### Active Attention Anchors

#### 🕐 [Timestamp] 🎯 Current Focus: [Description]
- 📊 Priority: HIGH/MEDIUM/LOW
- ⏱️ Expected Duration: [Time]
- 🎯 Success Criteria: [Criteria]
- 🔗 Related Context: [Links]
- 💭 Rationale: [Why]

<!-- Cache Breakpoint: Focus section updated -->
```

### Section 2: 📋 TODO

```markdown
## 📋 TODO

### Task List (Attention Management)

#### 🕐 [Timestamp] ⭕ Task: [Description]
- 🏷️ Type: DEV/DOC/CONFIG/TEST/REVIEW/DEPLOY/RESEARCH
- 📊 Priority: HIGH/MEDIUM/LOW
- 🎯 Completion Criteria: [Criteria]
- 🔗 Dependencies: [Task IDs or file paths]
- 📝 Notes: [Additional context]
- **Status**: ⭕Pending / 🔄InProgress / ✅Done / ❌Cancelled / 🚫Blocked / ⏸️Paused

<!-- Cache Breakpoint: TODO section updated -->
```

### Section 3: ⚙️ PROCESS

```markdown
## ⚙️ PROCESS

### Process Execution History

#### 🕐 [Timestamp] ⚙️ Process: [Name]
- 🏷️ Type: DEVELOP/DEBUG/OPTIMIZE/LEARN/REVIEW/REFACTOR
- 📝 Key Steps: [Step1] → [Step2] → [Step3]
- ⏱️ Duration: [Actual time]
- 💡 Learnings: [Key takeaways]
- 🔗 Related Files: [File paths]
- 📊 Outcome: SUCCESS/PARTIAL/FAILED

<!-- Cache Breakpoint: Process section updated -->
```

### Section 4: ❌ ERROR

> **重要**: ERROR类型不再写入CLAUDE.md，而是记录到 `learning/errors/ERRORS.jsonl`

```markdown
## ❌ ERROR

### 结构化错误数据系统

**数据存储位置**: `learning/errors/`

```yaml
核心文件:
  ERRORS.jsonl:
    格式: 行分隔JSON（每行一个完整错误记录）
    写入: /manus error (MANUS五步法)
    读取: /learn (分析和优化)
    特点: 完整的MANUS五步法记录

  PATTERNS.json:
    格式: 结构化JSON
    内容: 提炼的错误模式库
    更新: /learn自动分析生成

  STATS.json:
    格式: 结构化JSON
    内容: 错误统计和趋势分析
    更新: /learn自动计算
```

**闭环工作流**:
```
错误发生
  → /manus error记录到ERRORS.jsonl
  → /learn读取和分析
  → 更新PATTERNS.json (模式提炼)
  → 更新STATS.json (统计趋势)
  → 生成OPTIMIZATION.md (优化建议)
  → 系统改进和能力提升
```

**查询方法**:

```bash
# 查看最新错误
!tail -1 learning/errors/ERRORS.jsonl | jq '.'

# 查看所有错误
!cat learning/errors/ERRORS.jsonl | jq '.'

# 按类型筛选
!grep '"type":\["LOGIC"' learning/errors/ERRORS.jsonl | jq '.'

# 统计错误数量
!wc -l < learning/errors/ERRORS.jsonl

# 深度分析
执行 /learn 命令进行趋势分析和优化建议生成
```

**当前统计** (示例):
- 总错误数: 0
- 本月新增: 0
- 恢复成功率: N/A

**识别的错误模式** (示例):
| 模式ID | 模式名称 | 类别 | 发生频率 |
|--------|---------|------|---------|
| 暂无识别模式 | - | - | - |

**预防机制** (示例):
- 暂无预防机制

<!-- Cache Breakpoint: Error section references updated -->
```

### Section 5: ✅ SUCCESS

```markdown
## ✅ SUCCESS

### Successful Experiences and Solutions

#### 🕐 [Timestamp] ✅ Success: [Description]
- 🏷️ Type: IMPLEMENTATION/OPTIMIZATION/INTEGRATION/DEBUGGING
- 📊 Value Level: HIGH/MEDIUM/LOW
- 🎯 Problem Solved: [Original problem]
- 📝 Solution Approach: [Detailed solution]
- 📈 Impact: [Measurable improvement]
- 🔗 Related Files: [Implementation file paths]
- 💡 Reusability: [How to apply elsewhere]

**Solution Template**: [If applicable]

<!-- Cache Breakpoint: Success section updated -->
```

### Section 6: 🧠 INSIGHTS

```markdown
## 🧠 INSIGHTS

### Technical Insights and Techniques

#### 🕐 [Timestamp] 🧠 Insight: [Title]
- 📊 Depth Level: SURFACE/MODERATE/DEEP/BREAKTHROUGH
- 🏷️ Domain: [Technical domain]
- 💡 Core Insight: [Detailed explanation]
- 📚 Theoretical Basis: [Why this works]
- 🛠️ Practical Techniques: [How to apply]
- 📈 Innovation Degree: INCREMENTAL/SIGNIFICANT/BREAKTHROUGH
- 🔗 References: [Documentation, articles, file paths]

<!-- Cache Breakpoint: Insights section updated -->
```

### Section 7: 🔍 PATTERNS

```markdown
## 🔍 PATTERNS

### Recognized Patterns (Error + Technical)

#### 🕐 [Timestamp] 🔍 Pattern: [Name]
- 🏷️ Category: ERROR_PATTERN/DESIGN_PATTERN/WORKFLOW_PATTERN
- 📊 Frequency: [How often encountered]
- 📝 Pattern Description: [Detailed description]
- 🎯 When to Apply: [Trigger conditions]
- ⚠️ Anti-Patterns: [What to avoid]
- 💡 Best Practices: [Recommended approach]
- 🔗 Examples: [File paths to examples]

<!-- Cache Breakpoint: Patterns section updated -->
```

---

## 🎓 最佳实践

### 何时使用各个类型

```yaml
🎯 FOCUS:
  - 开始新的重要任务时
  - 切换注意力焦点时
  - 需要明确成功标准时
  - 估计用时超过1小时的任务

📋 TODO:
  - 任务管理和跟踪
  - 复杂任务拆解
  - 依赖关系管理
  - 防止"中间丢失"问题

⚙️ PROCESS:
  - 记录复杂流程执行
  - 文档化可复用工作流
  - 流程优化和改进
  - 团队知识共享

❌ ERROR:
  - 任何错误都应记录 (学习信号!)
  - 特别是重复出现的错误
  - 影响用户体验的错误
  - 需要系统性预防的错误

✅ SUCCESS:
  - 突破性解决方案
  - 可复用的成功模式
  - 显著的性能改进
  - 创新性实现方法

🧠 INSIGHTS:
  - 深度技术理解
  - 理论与实践结合
  - 创新性发现
  - 可跨领域应用的洞察

🔍 PATTERNS:
  - 识别重复模式
  - 设计模式应用
  - 反模式识别
  - 最佳实践总结
```

### 分类决策指南

```yaml
选择全局级别 (~/.claude/CLAUDE.md) 当:
  ✅ 可跨多个项目复用
  ✅ 通用技术/工具/模式
  ✅ 框架无关的知识
  ✅ 可供团队共享的经验

选择项目级别 (CLAUDE.md) 当:
  ✅ 项目特定配置/代码
  ✅ 当前项目业务逻辑
  ✅ 本地开发环境
  ✅ 项目相关的决策记录

不确定时:
  ✅ 默认选择项目级别
  ✅ 记录分类不确定性
  ✅ 后续可迁移到全局
```

### 缓存优化技巧

```yaml
最大化缓存复用:
  ✅ 使用稳定的时间戳前缀
  ✅ 仅追加,永不修改
  ✅ 批量更新时保持顺序
  ✅ 添加明确的缓存断点注释

减少token使用:
  ✅ 使用文件路径引用而非完整内容
  ✅ 使用URL引用而非网页全文
  ✅ 保留核心学习信号 (错误堆栈)
  ✅ 压缩冗余内容

保持上下文质量:
  ✅ 完整保存错误上下文
  ✅ 详细记录解决方案
  ✅ 明确记录根因分析
  ✅ 提供可恢复的引用路径
```

---

## 📚 参考资源

```yaml
设计文档:
  - PRPs/in-progress/MANUS-command-restructuring-design-v1.0.md

MANUS上下文工程:
  - 来源: Production AI Agents (dev.to)
  - 核心: KV-cache优化、错误保存、注意力管理
  - 成本影响: 10倍差异 ($0.30 vs $3.00 per MTok)

原命令参考:
  - .claude/commands/C.md (注意力控制系统)
  - .claude/commands/X.md (错误纠正与学习系统)
  - .claude/commands/Z.md (知识积累系统)

配置文档:
  - ~/.claude/CLAUDE.md (机器级/全局配置)
  - CLAUDE.md (项目级配置)
```

---

## 🔄 迁移说明

如果你之前使用过 C/X/Z 命令，请注意:

```yaml
命令映射:
  /C → /manus focus | /manus todo | /manus process
  /X → /manus error
  /Z → /manus success | /manus insights | /manus patterns

配置层级变更:
  机器级 + 系统级 → 全局级别 (~/.claude/CLAUDE.md)
  项目级 → 项目级别 (CLAUDE.md)

旧数据迁移:
  - 旧的 .claude/CLAUDE.md (系统级) 已废弃
  - 框架通用内容已迁移到全局级别
  - 框架特定内容已迁移到项目级别
  - 原始C/X/Z命令文件将被删除
```

---

## ✅ 执行示例

### 示例1: 记录当前焦点

```bash
/manus focus
📊 Priority: HIGH
⏱️ Duration: 3h
🎯 Success: MANUS命令完全实现并测试通过
💭 Rationale: 统一上下文管理是v2.0核心功能

实现MANUS统一上下文管理命令，整合注意力管理、错误学习和知识积累功能
```

**执行结果**:

```
✅ 焦点已记录到 项目级别 (CLAUDE.md)
📝 Section: 🎯 FOCUS
🕐 Timestamp: 2025-10-23T14:30:00
🔗 File Reference: CLAUDE.md:# 🎯 FOCUS
```

### 示例2: 记录错误和恢复

```bash
/manus error
🏷️ Type: LOGIC
📊 Severity: HIGH
🎯 Failed Action: 模糊分类条目处理
💡 Learning Value: 需要明确的tie-breaker逻辑

错误完整上下文:
条目同时包含"本项目"和"通用"关键词，分类逻辑产生歧义。
预期行为: 默认为项目级别

恢复策略:
🏷️ Strategy: REPAIR
📝 Steps:
  1. 添加tie-breaker: 同时存在时默认项目级别
  2. 更新测试用例
  3. 添加日志记录
⏱️ Recovery Time: 15min

根因分析:
📝 Root Cause: 设计规范未覆盖边界情况
🔧 Prevention: 完善分类决策树,添加边界测试
📈 System Updates: 分类逻辑v1.1,测试套件扩展
```

**执行结果**:

```
✅ 错误已记录到 项目级别 (CLAUDE.md)
📝 Section: ❌ ERROR
🕐 Timestamp: 2025-10-23T15:00:00
🔗 File Reference: CLAUDE.md:# ❌ ERROR
💡 Learning Signal: 完整错误上下文已保存,包含恢复过程和根因分析
```

### 示例3: 记录技术洞察

```bash
/manus insights
📊 Depth Level: DEEP
🏷️ Domain: 上下文工程
💡 Innovation: SIGNIFICANT

核心洞察:
稳定前缀格式 (🕐 Timestamp Icon Type:) 可最大化KV-cache复用,
实现10倍成本降低 ($3.00/MTok → $0.30/MTok)

理论基础:
1. KV-cache按前缀匹配
2. 即使单个token变化也会破坏下游缓存
3. 仅追加更新保持上下文确定性

实践技巧:
1. 所有条目使用统一时间戳前缀格式
2. 永不修改已有条目,仅追加
3. 状态变更通过新条目记录
4. 添加显式缓存断点注释

参考资料:
- dev.to/olimdzhon/context-engineering-techniques-in-production-ai-agents-1hk9
- PRPs/in-progress/MANUS-command-restructuring-design-v1.0.md
```

**执行结果**:

```
✅ 洞察已记录到 全局级别 (~/.claude/CLAUDE.md)
📝 Section: 🧠 INSIGHTS
🕐 Timestamp: 2025-10-23T16:00:00
🔗 File Reference: ~/.claude/CLAUDE.md:# 🧠 INSIGHTS
💡 Reusability: 跨所有项目适用的缓存优化技术
```

---

## 🎯 总结

MANUS命令提供了统一的上下文管理接口,整合了:

```yaml
核心功能:
  ✅ 注意力管理 (FOCUS/TODO/PROCESS)
  ✅ 错误学习 (ERROR完整上下文保存)
  ✅ 知识积累 (SUCCESS/INSIGHTS/PATTERNS)
  ✅ 智能类型识别 (基于关键词和结构特征)

核心价值:
  ✅ 10倍成本优化 (KV-cache优化)
  ✅ 完整学习信号 (错误保存原则)
  ✅ 无限记忆容量 (文件系统上下文)
  ✅ 简化分类 (双层级 vs 三层级)
  ✅ 智能便捷 (自动类型识别)

使用原则:
  ✅ 稳定前缀格式
  ✅ 仅追加更新
  ✅ 可恢复压缩
  ✅ 明确分类标准
  ✅ 智能类型匹配

使用方式:
  显式指定: /manus [type] [parameters]
  智能识别: /manus [content] (推荐)
```

**快速开始**:

```bash
# 方式1: 显式指定类型
/manus error [错误描述和MANUS五步法]

# 方式2: 智能识别（推荐）
/manus
遇到了XX错误，通过YY方法修复。
根因是ZZ，已添加预防措施。

→ 系统自动识别为ERROR类型并记录
```

**设计参考**: `PRPs/in-progress/MANUS-command-restructuring-design-v1.0.md`

**版本**: v2.1.0 | **日期**: 2025-10-23 | **更新**: 新增智能类型识别功能
