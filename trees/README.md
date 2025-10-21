# Trees 目录说明

## 📁 目录用途

这个目录是**并行开发工作空间**的专用存放位置,用于存储通过 Git Worktree 创建的独立工作环境。

## 🎯 主要功能

### 与 `/R` 命令配合使用

当执行 `/R` (并行任务准备与执行)命令时,系统会:

1. **自动创建多个 worktree** - 每个独立的开发分支
2. **存放在此目录** - 所有 worktree 统一管理
3. **并行开发** - 多个 AI Agent 同时在不同方案上工作
4. **结果对比** - 完成后对比选择最佳实现

### 典型目录结构

```
trees/
├── feature-name-1/          # Agent-1 的工作空间
│   ├── src/
│   ├── RESULTS.md          # 实现报告
│   └── ...
├── feature-name-2/          # Agent-2 的工作空间
│   ├── src/
│   ├── RESULTS.md
│   └── ...
└── feature-name-3/          # Agent-3 的工作空间
    ├── src/
    ├── RESULTS.md
    └── ...
```

## 🔧 使用示例

### 创建并行工作空间
```bash
# 方式1: 指定参数
/R "new-feature" 3 "实现新功能的详细描述..."

# 方式2: 使用默认PRP
/R
```

### 查看工作空间
```bash
# 列出所有 worktree
git worktree list

# 进入特定工作空间
cd trees/new-feature-1
```

### 清理工作空间
```bash
# 删除指定 worktree
git worktree remove trees/new-feature-1

# 或强制删除(包含未提交更改)
git worktree remove --force trees/new-feature-1

# 删除对应分支
git branch -D new-feature-1
```

## ⚠️ 注意事项

### 不要手动创建子目录
- ❌ 不要手动在 `trees/` 下创建文件夹
- ✅ 始终通过 `/R` 命令或 Git Worktree 命令创建

### Git 状态独立
- 每个 worktree 有独立的 Git 工作区
- 可以在不同 worktree 中切换到不同分支
- 修改互不影响,完全隔离

### 磁盘空间考虑
- 每个 worktree 会占用完整项目大小的空间
- 建议并行数量控制在 2-5 个
- 及时清理不需要的 worktree

## 🚀 工作流示例

### 标准并行开发流程

```bash
# 1. 创建并行工作空间
/R "user-auth" 3 "实现用户认证功能..."

# 2. 等待 Agent 完成(自动并行执行)
# Agent-1、Agent-2、Agent-3 同时工作

# 3. 查看结果
cat trees/user-auth-1/RESULTS.md
cat trees/user-auth-2/RESULTS.md
cat trees/user-auth-3/RESULTS.md

# 4. 对比选择最佳方案
cd trees/user-auth-2  # 假设选择方案2

# 5. 合并到主分支
git checkout main
git merge user-auth-2

# 6. 清理其他方案
git worktree remove --force trees/user-auth-1
git worktree remove --force trees/user-auth-3
git branch -D user-auth-1 user-auth-3
```

## 🎭 Git Worktree 工作机制详解

### 核心概念:"项目分身"

当执行 `/R` 命令创建并行工作空间时,实际上是创建了**多个完整的项目副本**:

```
主项目 (main branch)
    ↓
Git Worktree 机制
    ↓
创建多个"分身"副本
    ↓
├── trees/todo-manager-1/  ← 完整的项目副本(分支: todo-manager-1)
├── trees/todo-manager-2/  ← 完整的项目副本(分支: todo-manager-2)
└── trees/todo-manager-3/  ← 完整的项目副本(分支: todo-manager-3)
```

### 每个"分身"包含什么?

执行 `git worktree add -b feature-1 ./trees/feature-1` 时会创建:

```
trees/feature-1/
├── .claude/              ← 完整复制
├── src/                  ← 完整复制
├── README.md             ← 完整复制
├── package.json          ← 完整复制
└── ... (所有项目文件)   ← 完整复制
```

**关键特性**:
- ✅ 每个 worktree 是**完整的项目副本**
- ✅ 拥有**独立的 Git 分支**
- ✅ 文件修改**互不影响**
- ✅ 共享**同一个 .git 仓库**(节省空间)

### 完整流程图

```
1. 创建阶段
   主项目 → git worktree add → trees/feature-1/ (完整副本)
                             → trees/feature-2/ (完整副本)
                             → trees/feature-3/ (完整副本)

2. 执行阶段
   Agent-1 在 trees/feature-1/ 独立工作 → 修改文件 → feature-1 分支
   Agent-2 在 trees/feature-2/ 独立工作 → 修改文件 → feature-2 分支
   Agent-3 在 trees/feature-3/ 独立工作 → 修改文件 → feature-3 分支

3. 对比阶段
   对比 3 个分支的实现 → 选择最佳方案 → 合并到主分支

4. 清理阶段
   删除 worktree → 删除分支 → 保留最佳实现
```

### 空间占用说明

假设项目大小是 **100MB**:

```
传统估算:
主项目:                    100MB
trees/feature-1/:          100MB  ← 完整副本
trees/feature-2/:          100MB  ← 完整副本
trees/feature-3/:          100MB  ← 完整副本
-----------------------------------
预计总计:                  400MB

实际占用(Git 优化后):
主项目 + .git:             100MB
trees/feature-1/:           50MB  ← 只复制工作区文件
trees/feature-2/:           50MB  ← .git 数据库共享
trees/feature-3/:           50MB  ← 节省大量空间
-----------------------------------
实际总计:                  250MB
```

### 为什么需要"分身"?

#### 1. 完全隔离
```bash
# Agent-1 在 trees/todo-manager-1/ 中
# 修改了 src/auth.js
# 不会影响 Agent-2 和 Agent-3

# Agent-2 在 trees/todo-manager-2/ 中
# 可以完全重写 src/auth.js
# 采用不同的实现方案
```

#### 2. 真正并行
```
传统方式(串行):
Agent-1 实现 → 提交 → Agent-2 实现 → 提交 → Agent-3 实现
总耗时: 30分钟 + 30分钟 + 30分钟 = 90分钟

Worktree方式(并行):
Agent-1 实现 ┐
Agent-2 实现 ├→ 同时进行
Agent-3 实现 ┘
总耗时: 30分钟
```

#### 3. 独立的 Git 历史
```bash
# trees/todo-manager-1/ 的提交历史
commit abc123 (todo-manager-1)
    实现了JSON存储方案

# trees/todo-manager-2/ 的提交历史
commit def456 (todo-manager-2)
    实现了SQLite存储方案

# 两者互不干扰,各自维护独立的提交历史
```

### 与普通分支的区别

#### 传统 Git 分支切换
```bash
git checkout feature-1  # 切换到分支1
# 工作目录文件变化

git checkout feature-2  # 切换到分支2
# 工作目录文件再次变化

# 问题: 只有一个工作目录,无法同时查看两个分支
```

#### Git Worktree 方式
```bash
cd trees/feature-1/     # 查看分支1的实现
cd trees/feature-2/     # 查看分支2的实现

# 优势: 可以同时打开多个终端/编辑器
#       同时查看/对比不同方案
#       无需频繁切换分支
```

### Agent 工作时的视角

```bash
# Agent-1 的视角
当前目录: /project/trees/todo-manager-1
当前分支: todo-manager-1
可见文件: 完整的项目文件(独立副本)
修改范围: 只影响 todo-manager-1 分支

# Agent-2 的视角
当前目录: /project/trees/todo-manager-2
当前分支: todo-manager-2
可见文件: 完整的项目文件(独立副本)
修改范围: 只影响 todo-manager-2 分支

# 两个 Agent 完全感知不到对方的存在
```

### 实际操作示例

#### 创建分身
```bash
# 命令
git worktree add -b todo-manager-1 ./trees/todo-manager-1

# 发生了什么?
1. 创建新分支 todo-manager-1
2. 在 trees/todo-manager-1/ 创建完整项目副本
3. 切换到该分支
4. Agent-1 可以开始独立工作了
```

#### 完成后对比
```bash
# 查看 Agent-1 的实现
cd trees/todo-manager-1
cat src/todo.py          # 可能使用了 JSON 存储

# 查看 Agent-2 的实现
cd trees/todo-manager-2
cat src/todo.py          # 可能使用了 SQLite 存储

# 两个文件内容可能完全不同!
# 这就是并行探索的价值
```

## 📊 最佳实践

### 何时使用并行开发

✅ **适合的场景**:
- 探索多种技术方案
- A/B 测试不同实现
- 快速原型验证
- 并行开发独立模块

❌ **不适合的场景**:
- 简单的 bug 修复
- 已有明确最佳方案
- 磁盘空间严重不足
- 功能间强依赖

### 推荐的并行数量

- **简单功能**: 2 个方案
- **中等复杂度**: 3 个方案
- **高复杂度**: 4 个方案
- **最大建议**: 5 个方案

## 🔗 相关资源

- **命令文档**: `.claude/commands/R.md`
- **PRP 模板**: `.claude/PRPs/PRP.md`
- **项目快捷键**: `.claude/commands/Q.md`

## 📝 维护记录

- **创建时间**: 2025-10-20
- **最后更新**: 2025-10-20
- **更新内容**: 添加 Git Worktree 工作机制详解
- **维护原则**: 保持目录清洁,及时清理过期 worktree

---

**提示**: 这个目录通常应该保持为空或只包含活跃的 worktree。定期清理已完成的并行任务!
