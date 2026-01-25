# Context - 上下文工程中心

> **基于 Claude Code 官方最佳实践的统一上下文管理系统**
>
> **版本**: v3.0.0
> **状态**: 🚧 Implementation
> **创建日期**: 2025-10-28

---

## 📖 快速导航

| 文档 | 描述 | 状态 |
|------|------|------|
| [优化方案](./context-engineering-optimization-plan.md) | 完整的优化方案和实施计划 | ✅ 已完成 |
| [manus.md](../.claude/commands/manus.md) | 统一上下文管理命令 | 🔄 待优化 |
| [learn.md](../.claude/commands/learn.md) | Plugins研究迭代系统 | 🔄 待重构 |

---

## 🎯 核心功能

### 1. 上下文管理 (manus.md v3.0.0)

**核心类型**:
- `focus` - 注意力焦点管理
- `todo` - 任务管理和追踪
- `process` - 流程执行记录
- `error` - 结构化错误记录（MANUS五步法）
- `success` - 成功经验沉淀
- `insights` - 技术洞察积累
- `patterns` - 模式识别和最佳实践

**新增类型**（整合官方特性）:
- `context` - 上下文监控和优化
- `memory` - 长期记忆管理
- `snapshot` - 快照和版本管理

**快速使用**:
```bash
# 记录错误（智能识别）
/manus
遇到了分类逻辑错误，通过添加tie-breaker修复。

# 检查上下文健康度
/manus context

# 创建快照
/manus snapshot
```

---

### 2. Plugins研究迭代 (learn.md v3.0.0)

**重新定位**: 从"组件学习"转向"生态研究"

**核心功能**:
- ✅ Plugin健康度分析（配置完整性、agents分布、使用频率）
- ✅ Plugin协作关系图（跨业务组工作流、数据流转）
- ✅ 错误归因到Plugin（高错误率plugin识别）
- ✅ Plugin演进计划生成（PLUGIN-EVOLUTION.json）
- ✅ 生态级改进建议（跨plugin协作优化）

**快速使用**:
```bash
# 执行完整研究循环
/learn

# 查看Plugin研究报告
cat context/research/{YYYY-MM-DD}/PLUGIN-REPORT.md

# 查看Plugin演进计划
cat context/research/{YYYY-MM-DD}/PLUGIN-EVOLUTION.json
```

---

## 📁 目录结构

```
context/
├── README.md                    # 📘 本文件
├── context-engineering-optimization-plan.md  # 📋 完整优化方案
│
├── errors/                      # ❌ 错误记录系统
│   ├── ERRORS.jsonl            # 结构化错误日志（MANUS五步法）
│   ├── PATTERNS.json           # 错误模式库
│   └── STATS.json              # 统计元数据
│
├── memory/                      # 🧠 长期记忆系统（即将推出）
│   ├── project-memory.json     # 项目特定长期记忆
│   └── cross-session.json      # 跨会话上下文
│
├── snapshots/                   # 📸 快照版本管理（即将推出）
│   ├── CLAUDE-{timestamp}.md   # CLAUDE.md历史快照
│   └── metadata.json           # 快照索引
│
├── analytics/                   # 📊 上下文分析报告（即将推出）
│   ├── token-usage.json        # Token使用统计
│   └── context-health.json     # 上下文健康报告
│
└── research/                    # 🔬 Plugins研究系统
    └── {YYYY-MM-DD}/           # 按日期组织
        ├── WHAT-plugins.md
        ├── WHY-plugins.md
        ├── HOW-plugins.md
        ├── WIELD-plugins.md
        ├── PLUGIN-REPORT.md        # ⭐ 核心输出
        ├── PLUGIN-EVOLUTION.json   # ⭐ 演进计划
        └── METADATA.json
```

---

## 🚀 快速开始

### 1. 错误记录（当前可用）

```bash
# 方式1: 智能识别
/manus
遇到了配置解析错误，未处理null值。
根因是缺少JSON schema验证。
已添加验证步骤和默认值填充。

# 方式2: 显式指定
/manus error
🏷️ Type: LOGIC
📊 Severity: HIGH
[... 完整MANUS五步法 ...]
```

**输出位置**: `context/errors/ERRORS.jsonl`

---

### 2. Plugins研究（当前可用）

```bash
# 执行完整研究
/learn

# 查看研究摘要
/learn review

# 查看历史趋势
/learn history
```

**核心输出**:
- `context/research/{DATE}/PLUGIN-REPORT.md` - 详细分析报告
- `context/research/{DATE}/PLUGIN-EVOLUTION.json` - 可执行的演进计划
- `OPTIMIZATION.md` - 系统优化建议（项目根目录）

---

### 3. 上下文监控（即将推出）

```bash
# 检查上下文健康度
/manus context

# 输出示例
✅ 上下文健康度报告
📊 Token统计:
   - 当前使用: 45,230 tokens
   - 剩余容量: 154,770 tokens
   - 使用率: 23%

📈 Section占用:
   - 🎯 FOCUS: 2,340 tokens (5%)
   - 📋 TODO: 5,678 tokens (13%)
   - ❌ ERROR: 12,456 tokens (28%) ⚠️ 建议压缩
   - 🧠 INSIGHTS: 8,900 tokens (20%)

💡 优化建议:
   1. ERROR section超过20%阈值，建议归档旧数据
   2. 已识别3个可压缩的长描述
   3. 预计优化后节省: 8,000 tokens
```

---

### 4. 长期记忆（即将推出）

```bash
# 标记重要信息为长期记忆
/manus memory
这是项目的核心架构决策：
- 使用Plugins作为业务单元
- 8个业务组，65个智能体
- 基于Claude Code v1.0.124+
```

**输出位置**: `context/memory/project-memory.json`

**检索方式**:
```bash
# 查询记忆
/manus memory query "架构决策"

# 输出
✅ 找到2条相关记忆:
1. [2025-10-28] 核心架构决策
   - Plugins作为业务单元...
2. [2025-10-15] 技术选型决策
   - Claude Code v1.0.124+...
```

---

### 5. 快照管理（即将推出）

```bash
# 创建当前快照
/manus snapshot

# 输出
✅ 快照已创建
📸 快照ID: CLAUDE-20251028-120000
📁 位置: context/snapshots/
💾 大小: 125 KB

# 恢复快照
/manus restore CLAUDE-20251028-120000

# 输出
✅ 已恢复快照 CLAUDE-20251028-120000
📝 已备份当前版本到: context/snapshots/CLAUDE-20251028-125000-backup.md
```

---

## 📊 核心输出文件

### 1. ERRORS.jsonl

**格式**: 行分隔JSON（每行一个完整错误记录）

**包含字段**:
- `error_id`: ERR-YYYYMMDD-NNN
- `timestamp`: ISO 8601格式
- `manus`: MANUS五步法完整数据
- `impact`: 影响评估
- `recovery`: 恢复策略
- `metadata`: 关联的plugin/agent信息

**查询示例**:
```bash
# 查看最新错误
tail -1 context/errors/ERRORS.jsonl | jq '.'

# 按类型筛选
grep '"type":"LOGIC"' context/errors/ERRORS.jsonl | jq '.'

# 统计错误数
wc -l < context/errors/ERRORS.jsonl
```

---

### 2. PLUGIN-REPORT.md

**生成**: `/learn` 命令执行后

**包含内容**:
- 总体评估（健康度评分、生态协作成熟度）
- 各Plugin详细分析（优势、问题诊断、改进建议）
- 跨Plugin协作优化（工作流优化方案）
- 生态演进路线图（短期/中期/长期规划）

**示例结构**:
```markdown
## 📊 总体评估

### 健康度评分
| Plugin | 健康度 | Agents数 | 使用频率 | 主要问题 |
|--------|--------|---------|---------|---------|
| strategy-team | 8.5/10 | 9 | 中 | G7使用率低 |

## 🔍 各Plugin详细分析

### 1. 战略组 (strategy-team)
**健康度**: 8.5/10
[...]
```

---

### 3. PLUGIN-EVOLUTION.json

**生成**: `/learn` 命令执行后

**包含内容**:
- 各Plugin的演进项目（优化、新增功能）
- 生态级改进建议（跨plugin协作）
- 统计数据（总工作量估算、优先级分布）

**示例结构**:
```json
{
  "plugins": {
    "strategy-team": {
      "current_version": "1.0.0",
      "target_version": "1.1.0",
      "evolution_items": [
        {
          "item_id": "A-001",
          "type": "agent_optimization",
          "priority": "HIGH",
          "estimated_effort_days": 2
        }
      ]
    }
  },
  "ecosystem_improvements": [...]
}
```

**查询示例**:
```bash
# 查看整体统计
jq '.statistics' context/research/*/PLUGIN-EVOLUTION.json

# 查看高优先级项目
jq '.plugins[].evolution_items[] | select(.priority=="HIGH")' context/research/*/PLUGIN-EVOLUTION.json
```

---

## 🛠️ 工具和脚本

### 迁移脚本（即将推出）

```bash
# 从learning/迁移到context/
./scripts/context-migrate.sh

# 输出
✅ 正在迁移数据...
📁 源目录: learning/errors/
📁 目标目录: context/errors/
✅ 已迁移 15 条错误记录
✅ 已生成新的 PATTERNS.json
✅ 已生成新的 STATS.json
✅ 迁移完成！
```

### 初始化脚本（即将推出）

```bash
# 初始化context目录结构
./scripts/context-init.sh

# 输出
✅ 正在创建目录结构...
📁 context/errors/
📁 context/memory/
📁 context/snapshots/
📁 context/analytics/
📁 context/research/
📁 context/archives/
✅ 目录结构创建完成！
✅ 已创建 .gitignore
✅ 已创建 README.md
```

### 快照恢复脚本（即将推出）

```bash
# 快速恢复快照
./context/snapshots/restore.sh CLAUDE-20251028-120000

# 输出
✅ 正在恢复快照...
📸 快照: CLAUDE-20251028-120000
📝 备份当前版本...
✅ 已恢复快照！
```

---

## 📚 参考文档

### 命令文档

- [manus.md](../.claude/commands/manus.md) - 统一上下文管理命令
- [learn.md](../.claude/commands/learn.md) - Plugins研究迭代系统

### 优化方案

- [优化方案](./context-engineering-optimization-plan.md) - 完整的优化方案和实施计划

### 官方文档

- [Claude Code Context Management](https://docs.claude.com/zh-CN/docs/claude-code/context)
- [Claude Code Plugins Reference](https://docs.claude.com/zh-CN/docs/claude-code/plugins-reference)

### 最佳实践

- [Context Engineering Techniques](https://dev.to/olimdzhon/context-engineering-techniques-in-production-ai-agents-1hk9)
- [MANUS上下文工程](https://dev.to/olimdzhon/production-ai-agents-context-engineering)

---

## 🔄 版本历史

### v3.0.0 (2025-10-28) - 重大更新

**新增功能**:
- ✅ 整合 Claude Code 官方上下文管理特性
- ✅ 从"组件学习"转向"Plugins生态研究"
- ✅ 统一输出路径为 `context/` 目录
- ✅ 新增 context/memory/snapshot/analytics 功能

**优化改进**:
- ✅ manus.md 新增 context/memory/snapshot 类型
- ✅ learn.md 重构为 Plugins 研究迭代系统
- ✅ 标准化文件格式和命名规范
- ✅ 完整的文档和工具脚本

**向后兼容**:
- ✅ 保持原有 manus 类型不变
- ✅ 保持原有 learn 流程兼容
- ✅ 提供 learning/ → context/ 迁移脚本

---

## 🤝 贡献指南

### 报告问题

如果发现问题，请提供以下信息：
- 问题描述
- 复现步骤
- 预期行为
- 实际行为
- 相关日志（如 context/errors/ERRORS.jsonl）

### 建议改进

欢迎提出改进建议：
- 新功能需求
- 用户体验优化
- 文档改进
- 工具脚本增强

---

## 📞 支持

**文档问题**: 查看 [优化方案](./context-engineering-optimization-plan.md)
**使用问题**: 参考各命令的内置文档
**技术支持**: 提交 Issue 或联系项目维护者

---

**版本**: v3.0.0
**状态**: 🚧 Implementation
**下一步**: 完成 Phase 1（manus.md 优化）
