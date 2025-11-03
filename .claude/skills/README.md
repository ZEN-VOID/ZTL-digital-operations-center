# Skills - 技能包目录

> Self-contained capability packages with execution engines
> **总计**: 11个专业技能包

## 📋 技能包清单

### 1. 上下求索 (Context Management)
**位置**: `上下求索/`
**用途**: 基于MANUS上下文工程的智能上下文管理能力包
**核心功能**:
- 注意力管理
- 错误学习
- 知识沉淀
- 长期记忆
- 10种类型分类(focus/todo/process/error/success/insights/patterns/context/memory/snapshot)

**使用场景**: 上下文管理、错误记录、知识积累、记忆管理、快照管理

---

### 2. 元神出窍 (Agent Spawning)
**位置**: `元神出窍/`
**用途**: 创建和管理Claude Code智能体副本
**核心功能**: 并行智能体实例管理

---

### 3. 剑刃风暴 (Task Parallelization)
**位置**: `剑刃风暴/`
**用途**: 智能任务分割 + 并行Worker执行 + 自动结果汇总
**核心功能**:
- 突破200K token限制
- 实现超长任务无限制执行
- 并行处理提高效率

---

### 4. 奥术光辉 (Magic Enhancement)
**位置**: `奥术光辉/`
**用途**: 增强Claude能力的魔法技能
**核心功能**: 扩展Claude原生能力

---

### 5. 幻影之舞 (Universal Concurrency)
**位置**: `幻影之舞/`
**用途**: Universal concurrent execution engine for ALL skills
**核心功能**:
- AIGC并发生成
- 数据批处理
- 网页爬取
- 自动化任务
- 智能依赖分析
- 分层并发调度
- 进度追踪
- 健壮错误处理

**使用场景**: 批量AIGC生成、数据处理、网页爬取、自动化工作流

---

### 6. 深渊凝视 (iTerm Control)
**位置**: `深渊凝视/`
**用途**: iTerm终端控制与输出捕获
**核心功能**:
- 向iTerm发送任意命令并捕获执行结果
- 支持新建窗口、指定窗口、多窗口管理

**使用场景**: 终端自动化、命令执行追踪

---

### 7. 状态检查 (Status Check)
**位置**: `状态检查/`
**用途**: 系统状态检查和诊断
**核心功能**: 健康检查、性能监控

---

### 8. 真视之眼 (Global Plugin Visibility)
**位置**: `真视之眼/`
**用途**: 全局插件可视化查询系统
**核心功能**:
- 自动扫描和索引全局Claude Code插件(~/.claude/plugins/)
- 提供快速查询和变更检测
- 当用户询问"有哪些全局插件"、"全局技能包"、"可用的skills"时自动调用

---

### 9. 致命一击 (Critical Strike)
**位置**: `致命一击/`
**用途**: 端到端影视制作自动化工作流
**核心功能**:
- 一键完成从剧本到完整分镜脚本CSV的全流程处理
- 整合30个专业智能体
- 覆盖8个制作组
- 支持自由创作模式和批量生产模式

**使用场景**: 影视制作、脚本生成、分镜规划

---

### 10. 野性印记 (Wild Mark)
**位置**: `野性印记/`
**用途**: 标记和追踪系统
**核心功能**: 数据标注、状态追踪

---

### 11. 齐头并进 (Parallel Progress)
**位置**: `齐头并进/`
**用途**: 并行任务进度管理
**核心功能**: 多任务协同、进度同步

---

## 🎯 Skills vs Commands vs Agents

### Skills (技能包)
- **特点**: 自动发现、多文件结构、渐进披露
- **调用**: Claude自动识别并调用(无需用户干预)
- **用途**: 复杂工作流、批量处理、自动化能力

### Commands (斜杠命令)
- **特点**: 手动触发、单文件结构、支持参数
- **调用**: 用户显式输入 `/command-name`
- **用途**: 频繁使用的快捷操作

### Agents (智能体)
- **特点**: 独立上下文窗口、专业AI助手
- **调用**: 委派或显式调用
- **用途**: 专业领域深度分析

## 📖 使用指南

### 自动调用机制

Skills会被Claude自动发现并调用:

```yaml
用户输入: "生成一张海报"
↓
Claude扫描Skills目录
↓
匹配description: "text-to-image", "图片生成"
↓
读取SKILL.md核心指令
↓
按需加载scripts/执行引擎
↓
调用API生成图片
↓
返回结果到主对话
```

### 渐进披露原则

Skills使用渐进披露优化token使用:

1. **Level 1**: YAML frontmatter (~50 tokens) - 能力发现
2. **Level 2**: SKILL.md (~500-2000 tokens) - 使用说明
3. **Level 3**: reference.md (~1000-5000 tokens) - 深度知识
4. **Level 4**: scripts/ - 可执行代码

### 目录结构规范

```
skill-name/
├── SKILL.md              # 必需: 元数据 + 使用说明
│   ├── YAML frontmatter  # name + description
│   ├── Quick Start       # 快速开始示例
│   └── API Reference     # 详细参数(可选)
│
├── scripts/              # 推荐: 执行引擎
│   ├── core_engine.py    # 核心逻辑
│   ├── helpers.py        # 辅助函数
│   └── __init__.py       # Python模块
│
├── templates/            # 可选: 模板文件
├── reference.md          # 可选: 扩展文档
└── README.md             # 可选: 项目说明
```

## 🔗 相关资源

- [全局CLAUDE.md](~/.claude/CLAUDE.md) - 机器级配置
- [项目CLAUDE.md](../../CLAUDE.md) - 项目级配置
- [Commands目录](../commands/) - 斜杠命令
- [Agents目录](../agents/) - 系统级智能体

---

**最后更新**: 2025-11-03
**维护方式**: 随技能包自动更新
**状态**: ✅ Active
