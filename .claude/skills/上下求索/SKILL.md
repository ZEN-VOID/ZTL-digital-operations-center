---
name: 上下求索
description: "基于MANUS上下文工程的智能上下文管理能力包,支持注意力管理、错误学习、知识沉淀和长期记忆。自动识别10种类型(focus/todo/process/error/success/insights/patterns/context/memory/snapshot),双层级分类(全局/项目),KV缓存优化。Use when: 上下文管理、错误记录、知识积累、记忆管理、快照管理"
version: "3.0.0"
allowed-tools: ["Read", "Write", "Edit", "Bash"]
---

# 上下求索 - 智能上下文管理技能包

> **M**istake **A**cknowledgment **N**ew Understanding **U**pdated Approach **S**ystematic Prevention
>
> 基于生产级AI系统的上下文工程原则,提供自动化的注意力管理、错误学习和知识积累能力

## 快速开始

### 自动调用场景

当Claude识别到以下场景时,会自动调用本技能包:

```yaml
场景识别:
  错误记录: "遇到XX错误", "失败", "异常", "崩溃"
  焦点管理: "当前任务", "专注", "接下来", "优先级"
  任务管理: "待办", "需要完成", "任务清单"
  成功经验: "成功解决", "优化", "改进", "突破"
  技术洞察: "发现", "理解", "原理", "本质"
  模式识别: "重复出现", "最佳实践", "设计模式"
  上下文监控: "token使用", "上下文优化", "容量监控"
  长期记忆: "需要记住", "关键决策", "架构决策"
  快照管理: "创建快照", "版本备份", "恢复版本"
```

### 核心能力

**1. 智能类型识别** (10种类型)

```python
# 原有7种类型
- 🎯 FOCUS    # 注意力焦点管理
- 📋 TODO     # 任务清单和依赖管理
- ⚙️ PROCESS  # 流程执行记录
- ❌ ERROR    # 错误保存和恢复学习(MANUS五步法)
- ✅ SUCCESS  # 成功经验和解决方案
- 🧠 INSIGHTS # 技术洞察和实践技巧
- 🔍 PATTERNS # 模式识别和最佳实践

# v3.0新增3种类型
- 📊 CONTEXT  # 上下文监控和优化
- 🧠 MEMORY   # 长期记忆管理
- 📸 SNAPSHOT # 快照版本管理
```

**2. 双层级分类系统**

```yaml
全局级别 (~/.claude/CLAUDE.md):
  - 跨项目可复用的知识
  - 通用技术/工具/模式
  - 框架无关的经验

项目级别 (CLAUDE.md):
  - 项目特定配置/代码
  - 当前项目业务逻辑
  - 本地开发环境设置
```

**3. KV缓存优化**

```yaml
稳定前缀模式:
  格式: 🕐 [ISO 8601 Timestamp] [Icon] [Type]:
  优势:
    - 共享稳定前缀 → 10倍成本降低
    - 仅追加更新 → 保持上下文确定性
    - 最大化缓存复用 → $0.30 vs $3.00 per MTok
```

## API Reference

### 主函数签名

```python
def execute_manus(
    content: str,
    explicit_type: Optional[str] = None
) -> ManusResult:
    """
    执行MANUS上下文管理操作

    Args:
        content: 用户输入的内容
        explicit_type: 显式指定的类型(可选)
                      取值: focus/todo/process/error/success/
                           insights/patterns/context/memory/snapshot

    Returns:
        ManusResult: 包含操作结果、存储位置、统计信息

    智能识别逻辑:
        1. 如果explicit_type存在,直接使用
        2. 否则基于关键词和结构特征自动识别
        3. 输出识别依据供用户验证

    分类逻辑:
        1. 检查"本项目"/"当前业务"关键词 → 项目级别
        2. 检查"跨项目"/"通用"关键词 → 全局级别
        3. 默认: 项目级别

    存储策略:
        - ERROR类型 → context/errors/ERRORS.jsonl
        - 其他类型 → CLAUDE.md相应section
        - 使用稳定前缀格式优化缓存
    """
```

### 类型识别算法

```python
def auto_detect_type(content: str) -> tuple[str, str]:
    """
    智能识别内容类型

    Args:
        content: 用户输入内容

    Returns:
        (type, reason): 类型和识别依据

    识别优先级:
        1. ERROR (最高) - 错误关键词/预期vs实际结构
        2. SUCCESS - 成功关键词+可衡量改进
        3. INSIGHTS - 深度理解关键词
        4. PATTERNS - 模式/最佳实践关键词
        5. CONTEXT - 上下文监控关键词
        6. MEMORY - 记忆/持久化关键词
        7. SNAPSHOT - 快照/版本关键词
        8. TODO - 列表结构/任务关键词
        9. FOCUS - 时间估计/成功标准
        10. PROCESS - 流程/步骤关键词
        11. 默认策略 - 基于长度和结构
    """
```

### 输出格式

```python
@dataclass
class ManusResult:
    """MANUS执行结果"""

    type: str              # 识别的类型
    level: str             # 分类级别(全局/项目)
    target_file: str       # 目标文件路径
    timestamp: str         # ISO 8601时间戳
    detection_method: str  # 识别方式(智能识别/显式指定)
    detection_reason: str  # 识别依据

    # ERROR类型特殊字段
    error_id: Optional[str] = None
    error_stats: Optional[dict] = None

    # 通用统计
    section_stats: Optional[dict] = None
```

## 使用示例

### 示例1: 自动识别ERROR类型

```python
# 用户输入(无需指定类型)
content = """
遇到了分类逻辑错误,条目同时包含"本项目"和"通用"关键词时产生歧义。
预期应该默认为项目级别,但实际抛出了分类异常。
已通过添加tie-breaker逻辑修复。
"""

# Claude自动识别并调用
result = execute_manus(content)

# 输出
→ 🤖 类型识别: ❌ ERROR (智能识别)
→ 💡 识别依据: 包含关键词'错误'、'异常',提及修复过程
→ ✅ 错误已记录到结构化日志系统
→ 📊 错误ID: ERR-20251031-001
→ 📁 存储位置: context/errors/ERRORS.jsonl
```

### 示例2: 自动识别SUCCESS类型

```python
content = """
成功实现了KV-cache优化,通过稳定前缀模式将token成本从$3.00降低到$0.30,
实现了10倍成本节约。方法可以应用到所有上下文管理场景。
"""

result = execute_manus(content)

→ 🤖 类型识别: ✅ SUCCESS (智能识别)
→ 💡 识别依据: 包含关键词'成功'、'优化',包含可衡量改进数据
→ ✅ 条目已添加到 全局级别 (~/.claude/CLAUDE.md)
→ 📝 Section: ✅ SUCCESS
```

### 示例3: 上下文监控(v3.0)

```python
content = """
检查当前CLAUDE.md的整体健康度,
分析token使用情况和各section占用比例
"""

result = execute_manus(content)

→ 🤖 类型识别: 📊 CONTEXT (智能识别)
→ 💡 识别依据: 包含关键词'token'、'健康度'、'分析'
→ ✅ 分析报告已生成
→ 📁 位置: context/analytics/context-health-20251031.json
```

### 示例4: 长期记忆管理(v3.0)

```python
content = """
项目采用 Plugins 作为核心架构单元,
包含8个业务组、65个专业智能体,
这是影响所有后续开发的关键架构决策
"""

result = execute_manus(content)

→ 🤖 类型识别: 🧠 MEMORY (智能识别)
→ 💡 识别依据: 包含关键词'架构决策'、'关键'
→ ✅ 记忆已存储
→ 📁 位置: context/memory/project-memory.json
```

## 高级特性

### 1. MANUS五步法(ERROR类型)

```yaml
M - Mistake Acknowledgment:
  - Type, Severity, Failed Action
  - 完整错误上下文保存

A - Acknowledgment:
  - Root Cause分析
  - Wrong vs Correct Understanding

N - New Understanding:
  - Key Insights提炼
  - Mental Model更新

U - Updated Approach:
  - Correct Workflow定义
  - Verification Checklist

S - Systematic Prevention:
  - Prevention Rules
  - System Updates
  - Pattern Identification
```

### 2. 渐进披露原则

```yaml
Level 1 - 本文件YAML (50 tokens):
  - 能力发现: Claude扫描description匹配场景

Level 2 - 本文件核心指令 (2000 tokens):
  - 快速开始 + API Reference

Level 3 - reference.md (5000 tokens):
  - 详细参数模板
  - 完整识别逻辑
  - 所有示例

Level 4 - scripts/执行引擎:
  - Python实现
  - 实际文件操作
```

### 3. 缓存优化策略

```yaml
稳定前缀:
  🕐 2025-10-31T22:00:00 🎯 FOCUS: ...
  🕐 2025-10-31T22:15:00 📋 TODO: ...
  🕐 2025-10-31T22:30:00 ❌ ERROR: ...

仅追加:
  - 永不修改已有条目
  - 状态变更通过新条目记录
  - 保持完整历史

可恢复压缩:
  - 使用文件路径而非完整内容
  - 使用URL引用而非网页全文
  - 保留核心学习信号(错误堆栈)
```

## 与其他系统集成

### 与 context-manager agent 的协作

```yaml
context-manager职责:
  - 跨多agent协调时的上下文萃取
  - 为每个agent准备最小化相关上下文
  - 维护context索引快速检索

上下求索skill职责:
  - 单次上下文操作的执行引擎
  - 智能类型识别和分类
  - 数据持久化和缓存优化

协作模式:
  context-manager → 调用 → 上下求索 skill
  分析需求          执行操作      返回结果
```

### 与 PreCompact Hook 的集成

```yaml
PreCompact触发 → 保存快照:
  /manus snapshot
  🎯 Action: CREATE
  📝 Description: Compact前自动快照
  🏷️ Tags: [auto-compact, pre-compact]
```

## 技术规范

**遵循Claude Code Skills标准**:

```yaml
目录结构:
  .claude/skills/上下求索/
  ├── SKILL.md              # 本文件
  ├── reference.md          # 扩展文档(详细参数模板)
  ├── scripts/
  │   ├── core_engine.py    # 核心执行引擎
  │   ├── type_detector.py  # 智能类型识别
  │   ├── classifier.py     # 双层级分类器
  │   └── error_recorder.py # ERROR类型JSONL记录器
  └── templates/
      ├── error.template    # ERROR类型模板
      └── general.template  # 通用类型模板
```

**数据存储规范**:

```yaml
ERROR类型:
  - context/errors/ERRORS.jsonl
  - 行分隔JSON格式
  - 完整MANUS五步法

其他类型:
  - CLAUDE.md (项目级别)
  - ~/.claude/CLAUDE.md (全局级别)
  - 按类型section组织

快照和分析:
  - context/snapshots/
  - context/memory/
  - context/analytics/
```

## 参考资源

- **设计文档**: PRPs/in-progress/MANUS-command-restructuring-design-v1.0.md
- **MANUS原理**: Production AI Agents - Context Engineering (dev.to)
- **优化方案**: context/context-engineering-optimization-plan.md
- **原命令**: .claude/commands/manus.md

---

**版本**: v3.0.0 | **更新**: 2025-10-31
**兼容**: Claude Code v1.0.124+ | **依赖**: Python 3.8+
