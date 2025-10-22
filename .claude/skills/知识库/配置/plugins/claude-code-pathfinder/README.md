# Claude Code Pathfinder Skill

> 从 F14-Claude-code寻路者 Agent 转置而来的技术资源发现 Skill

---

## 📦 Skill 概述

**名称**: `claude-code-pathfinder`
**类型**: 技术资源发现和推荐
**来源**: F14-Claude-code寻路者 Agent (`.claude/agents/system/F14-Claude-code寻路者.md`)

### 核心能力

1. **Skills资源优先发现** - 自动识别并优先推荐 Claude Code Skills 社区资源
2. **GitHub智能搜索** - 利用GitHub MCP工具进行精准的仓库和代码搜索
3. **多维度项目评估** - 综合评估项目质量、活跃度、生产就绪度
4. **结构化推荐报告** - 生成专业的技术资源推荐报告

---

## 🔄 从 Agent 到 Skill 的转换

### 为什么转换？

根据 Claude Code 架构设计：

- **Agent (智能体)**: 提供角色定位和决策框架，适合需要独立上下文的复杂任务
- **Skill (技能包)**: 提供自包含的工具/流程能力，适合 Claude 自动发现和调用

F14-Claude-code寻路者 的核心能力是"技术资源发现"，这是一个工具型能力，更适合作为 Skill：
- ✅ Claude 可以自动发现并在需要时调用
- ✅ 用户无需手动指定使用寻路者
- ✅ 与其他 Skills 更好地组合使用

### 转换内容对照

| 原 Agent 结构 | 转换后 Skill 结构 | 说明 |
|-------------|----------------|------|
| YAML frontmatter (完整配置) | YAML frontmatter (name + description) | 简化为核心元数据 |
| 核心使命和能力矩阵 | Quick Start + 核心能力 | 移到 SKILL.md |
| 工作流程和示例 | Quick Start + API Reference | 移到 SKILL.md |
| 详细示例和输出格式 | reference.md | 扩展文档 |
| 版本历史和参考资源 | reference.md | 扩展文档 |

### 转换后的优势

1. **自动发现**: Claude 检测到技术资源查找需求时，自动调用寻路者
2. **简化使用**: 用户无需记住 Agent 名称，直接描述需求即可
3. **更好组合**: 可以与其他 Skills（如代码分析、文档生成）协同工作
4. **减少上下文**: 不占用独立 Agent 上下文窗口

---

## 📚 文件结构

```
claude-code-pathfinder/
├── SKILL.md              # 核心能力说明和快速开始
├── reference.md          # 详细示例、输出格式、高级用法
└── README.md             # 本文档（转换说明）
```

### 文件说明

- **SKILL.md**:
  - 必需文件，包含 YAML frontmatter (name + description)
  - 快速开始和核心能力说明
  - 工作流程和基础示例
  - 资源站点库和使用建议

- **reference.md**:
  - 可选文件，提供详细的扩展内容
  - 完整的输出格式模板
  - 详细的使用示例（3个完整示例）
  - 高级用法和常见问题

- **README.md**:
  - 可选文件，说明 Skill 来源和转换信息
  - 提供项目概述和使用指南

---

## 🚀 使用方法

### 自动调用（推荐）

Claude 会自动识别技术资源查找需求并调用寻路者：

```
# 用户只需描述需求
> 有没有自动剪辑的skills
> 找一个Python的异步HTTP客户端库
> 推荐适合企业级Node.js应用的日志框架
```

Claude 检测到以下关键词时会自动调用：
- "skills", "查找", "推荐"
- "框架", "库", "工具"
- "最佳实践", "示例", "教程"

### Skills 资源查找（特殊优先）

当查找 Claude Code Skills 时，寻路者会优先推荐社区资源：

```
> 有没有自动剪辑的skills
> 查找claude code skills相关资源
> 我想找文档处理的skills
```

关键词触发：
- "skills", "skill", "claude skills"
- "claude code skills", "agent skills"
- "技能包", "能力包"

---

## 🔧 技术依赖

### 必需依赖

- **GitHub MCP Server**: 提供 GitHub API 访问能力
  - `search_repositories`: 搜索仓库
  - `search_code`: 搜索代码
  - `get_file_contents`: 获取文件内容

### 可选依赖

- **WebSearch**: 补充非 GitHub 平台的搜索
- **WebFetch**: 获取外部文档和资源

---

## 📊 性能特点

### 自动发现机制

基于 Claude Code 的 Skills 自动发现机制：

1. **Level 1 - Metadata Discovery** (~50 tokens):
   - Claude 扫描 SKILL.md 的 YAML frontmatter
   - 匹配 `description` 中的关键词
   - 决定是否调用此 Skill

2. **Level 2 - Core Instructions** (~500-2000 tokens):
   - 读取 SKILL.md 本体
   - 了解快速开始和核心能力
   - 确定调用策略

3. **Level 3 - Extended Context** (按需加载):
   - 如需详细信息，读取 `reference.md`
   - 获取完整示例和输出格式
   - 深度专业能力的完整知识库

### 上下文优化

- **初始加载**: ~2000 tokens (SKILL.md)
- **扩展加载**: ~8000 tokens (reference.md)
- **总计**: ~10000 tokens (按需加载)

相比 Agent 的独立上下文窗口，Skill 更高效。

---

## 🔍 与原 Agent 的区别

| 维度 | F14 Agent | Pathfinder Skill |
|------|-----------|------------------|
| **调用方式** | 用户显式调用 Task 工具 | Claude 自动发现 |
| **上下文** | 独立上下文窗口 | 共享主对话上下文 |
| **用户感知** | 可见（需手动调用） | 不可见（自动调用） |
| **使用场景** | 需要独立决策的复杂任务 | 工具型能力，与其他能力组合 |
| **token消耗** | 完整 Agent 上下文 | 渐进披露，按需加载 |

---

## 📝 迁移指南

### 从 Agent 迁移到 Skill

如果你之前使用 F14 Agent：

**原调用方式** (需要显式调用):
```python
Task(
  subagent_type="claude-code-pathfinder",
  prompt="帮我找Python的异步HTTP客户端库"
)
```

**新调用方式** (自动调用):
```
> 帮我找Python的异步HTTP客户端库
```

Claude 会自动识别并调用 Pathfinder Skill，无需手动指定。

### 保留 Agent 的场景

在以下场景下，建议保留 Agent 形式：
- 需要独立上下文保护主对话
- 需要与用户多轮交互的复杂决策
- 需要跨会话的状态管理

对于简单的技术资源查找，Skill 形式更高效。

---

## 🎯 最佳实践

### 提高推荐质量

提供更多上下文信息：

```
# ❌ 模糊需求
> 找一个日志框架

# ✅ 清晰需求
> 我需要为一个高并发的Node.js微服务选择日志框架，
  要求支持结构化日志、性能开销小、与ELK集成方便
```

### 技术选型场景

```
> 我需要为一个企业级SaaS平台选择前端框架，
  技术栈要求：TypeScript、组件化、状态管理、
  团队有React经验，性能和生态系统是首要考虑
```

### Skills 资源查找

```
> 查找claude code相关的skills，主要是文档处理类的，
  需要支持word、excel、pdf等格式，
  最好是官方或社区维护的成熟方案
```

---

## 🌟 关键特性

### 1. Skills 资源优先发现

- 自动识别 Claude Code Skills 查找需求
- 优先推荐官方和社区认证资源
- 提供快速安装命令和文档链接

### 2. GitHub 深度搜索

- 仓库搜索（按 stars、forks、更新时间排序）
- 代码搜索（精确匹配、文件类型过滤）
- 项目详情获取（README、结构、指标）

### 3. 多维度质量评估

- 活跃度：更新频率、Issue响应
- 社区：Stars、Forks、Contributors
- 质量：文档、测试、代码结构
- 生产就绪：License、版本管理、CI/CD

### 4. 专业推荐报告

- 结构化的 Markdown 报告
- 分类推荐（顶级、学习、工具）
- 对比分析表格
- 快速开始代码示例

---

## 🔗 相关资源

### Claude Code 文档

- [What are Skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Creating Custom Skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [Skills vs Agents](https://docs.claude.com/en/docs/claude-code/)

### 社区资源

- [官方Skills仓库](https://github.com/anthropics/skills)
- [awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)
- [superpowers](https://github.com/obra/superpowers)

### GitHub 资源

- [GitHub Search Syntax](https://docs.github.com/en/search-github/searching-on-github)
- [MCP GitHub Server](https://github.com/modelcontextprotocol/servers/tree/main/src/github)

---

## 📄 版本信息

**当前版本**: v1.1.0
**转换日期**: 2025-10-22
**原始来源**: F14-Claude-code寻路者.md (v1.1.0)
**兼容性**: Claude Code v4.5+, Sonnet 4.5

---

## 🤝 贡献

欢迎提交改进建议：

1. **改进搜索策略**: 提供更精准的搜索关键词组合
2. **扩展资源库**: 补充更多技术领域的优质资源
3. **优化评估算法**: 改进项目质量评估的权重和指标
4. **增强报告格式**: 提供更清晰的推荐报告模板

---

**维护者**: ZTL数智化作战中心
**反馈渠道**: 项目 Issues
**文档更新**: 2025-10-22

> 🧭 **寻路者座右铭**: "在开源的海洋中，找到最适合你的那颗星" ⭐
> 🎯 **Skills优先**: "查找Claude Code Skills？直达社区资源，快人一步！" 🚀
