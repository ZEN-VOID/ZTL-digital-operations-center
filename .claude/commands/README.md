# Claude Code斜杠命令目录

> Slash Commands for Claude Code Workflow Automation

本目录包含ZTL数智化情报组的13个专业斜杠命令,覆盖配置管理、文档生成、GitHub集成、知识管理、上下文分析等核心工作流。

---

## 📋 命令清单

### 配置管理类 (Configuration Management)

#### /claude
**用途**: 智能识别并更新全局级(~/.claude/CLAUDE.md)和项目级(./CLAUDE.md)的CLAUDE配置文档
**核心功能**:
- 自动扫描项目配置(agents, commands, skills, hooks, plugins)
- 同步智能体、命令、技能包和目录结构信息
- 智能识别配置文件位置(全局级 vs 项目级)
- 更新CLAUDE.md的特定章节而不覆盖其他内容

**使用场景**:
- 新增或修改智能体后同步文档
- 新增或修改命令后更新配置
- 项目配置变更后刷新文档

**调用方式**:
```bash
/claude
```

**输出**: 更新后的CLAUDE.md文档,包含最新配置信息

---

#### /context-aware
**用途**: 全面分析项目8大维度的上下文
**核心功能**:
- 分析智能体定义(.claude/agents/)
- 分析斜杠命令(.claude/commands/)
- 分析钩子配置(.claude/hooks/)
- 分析技能包(.claude/skills/)
- 分析项目结构(目录树)
- 分析知识积累(learning/)
- 分析配置文件(CLAUDE.md)
- 分析文档说明(README.md)

**使用场景**:
- 项目初始化时全面了解项目结构
- 新成员加入团队快速上手
- 项目架构梳理和文档化
- 深度理解项目上下文

**调用方式**:
```bash
/context-aware
```

**输出**: 全面的项目上下文分析报告

---

### 文档生成类 (Documentation Generation)

#### /readme-generator
**用途**: 自动化README和OVERVIEW文档生成系统
**核心功能**:
- 五阶段文档生成工作流:
  - Stage 0: 前置比对检查(git-based change detection)
  - Stage 1: 更新trees/快照(目录结构和树形可视化)
  - Stage 2: 深度项目分析(基于CLAUDE.md)
  - Stage 3: 生成README.md和OVERVIEW.md
  - Stage 4: 子目录README生成(可选)
  - Stage 5: 验证与输出
- 智能目录结构变更检测
- 自动引用同步和路径修正

**使用场景**:
- 项目初始化时生成完整文档
- 项目结构变更后刷新文档
- 定期更新项目文档
- 确保文档与代码同步

**调用方式**:
```bash
/readme-generator
```

**输出**:
- README.md (项目主文档)
- OVERVIEW.md (技术深度解析)
- trees/目录快照
- 子目录README(可选)

---

#### /project-instructions
**用途**: 全面管理project/instructions目录下的完整文档体系
**核心功能**:
- 管理多个HTML页面(index.html, instructions.html等)
- 管理支持脚本(page-processor.js, nav-generator.js等)
- 管理样式文件(styles.css)
- 智能同步项目最新状态
- 保持设计风格一致性

**使用场景**:
- 生成项目指引网站
- 创建交互式文档系统
- 维护项目知识库
- 团队协作文档管理

**调用方式**:
```bash
/project-instructions
```

**输出**: project/instructions/目录下的完整HTML文档体系

---

### GitHub集成类 (GitHub Integration)

#### /github-start
**用途**: 自动化GitHub仓库创建、初始化和首次推送流程
**核心功能**:
- 创建新的GitHub仓库(公开/私有可选)
- 初始化本地git仓库
- 配置remote origin
- 首次推送所有文件
- 自动生成初始README(如不存在)

**使用场景**:
- 新项目初始化并推送到GitHub
- 快速建立项目远程仓库
- 标准化项目启动流程

**调用方式**:
```bash
/github-start
```

**交互流程**:
1. 询问仓库名称
2. 询问仓库可见性(公开/私有)
3. 确认是否创建README
4. 执行创建和推送

---

#### /github-pull
**用途**: 将本地项目完整同步推送到GitHub仓库
**核心功能**:
- 检测目录结构变更
- 自动更新文档引用路径
- 完整推送所有变更
- 确保远程与本地完全一致

**使用场景**:
- 定期同步本地变更到远程
- 项目结构调整后推送
- 文档更新后同步
- 确保团队协作一致性

**调用方式**:
```bash
/github-pull
```

**特色功能**:
- 智能检测目录结构变更
- 自动修正文档中的引用路径
- 生成详细的变更日志

---

#### /github-issue <Issue的URL或号码>
**用途**: 系统化的Issue分析、修复和关闭流程
**核心功能**:
- 获取Issue详细信息
- 分析问题根因
- 生成修复方案
- 实施修复并测试
- 更新Issue状态
- 自动关闭Issue(可选)

**使用场景**:
- 处理GitHub Issue
- 标准化问题修复流程
- 确保问题解决的完整性和可追溯性

**调用方式**:
```bash
/github-issue https://github.com/owner/repo/issues/123
# 或
/github-issue 123
```

**工作流程**:
1. 获取Issue详情
2. 分析问题和复现步骤
3. 定位代码问题
4. 实施修复
5. 运行测试验证
6. 更新Issue并关闭

---

### 并行执行类 (Parallel Execution)

#### /trees <功能名称> <并行数量> <执行计划的详细描述>
**用途**: 完整的并行执行工作流
**核心功能**:
- 环境准备(创建工作区、备份配置)
- 并行执行多个方案探索
- 自动结果对比和分析
- 方案推荐和选择

**使用场景**:
- 探索多种技术方案
- A/B测试不同实现
- 并行尝试多种策略
- 性能对比分析

**调用方式**:
```bash
/trees 爬虫策略优化 3 "尝试不同的反爬虫策略: 1)延迟+User-Agent轮换 2)代理池 3)浏览器指纹伪装"
```

**参数说明**:
- `<功能名称>`: 本次并行任务的名称
- `<并行数量>`: 并行探索的方案数量(2-5)
- `<执行计划>`: 详细描述每个方案的具体内容

**输出**:
- trees/目录下的方案对比报告
- 推荐的最优方案
- 详细的性能和质量分析

---

### 知识管理类 (Knowledge Management)

#### /manus [type] [content]
**用途**: 基于MANUS上下文工程的统一上下文管理系统
**核心功能**:
- 支持6种上下文类型:
  - `decision`: 决策记录
  - `error`: 错误教训
  - `pattern`: 代码模式
  - `knowledge`: 领域知识
  - `context`: 项目上下文
  - `insight`: 重要洞察
- 智能类型识别(可省略type参数)
- 全局/项目双层级分类机制
- 自动化记忆提取和注入

**使用场景**:
- 记录重要决策和理由
- 保存错误教训避免重犯
- 沉淀代码模式和最佳实践
- 积累领域知识和经验

**调用方式**:
```bash
# 显式指定类型
/manus decision "采用PostgreSQL而非MongoDB,因为需要复杂关联查询"

# 智能识别类型(推荐)
/manus "采用PostgreSQL而非MongoDB,因为需要复杂关联查询"
```

**存储位置**:
- 全局级: ~/.claude/learning/
- 项目级: ./learning/

---

#### /learn [step=what|why|how|wield] | continue | review | history
**用途**: 整合What/Why/How/Wield四步学习流程,自动化系统优化和知识积累
**核心功能**:
- 四步学习框架:
  - `what`: 理解问题本质和现状
  - `why`: 分析根本原因
  - `how`: 设计解决方案
  - `wield`: 实施和验证
- 支持学习流程续接(`continue`)
- 支持学习回顾(`review`)
- 支持历史记录查询(`history`)

**使用场景**:
- 系统性学习新技术
- 分析和解决复杂问题
- 优化系统架构
- 积累经验和最佳实践

**调用方式**:
```bash
# 开始新的学习流程
/learn step=what

# 继续上次学习
/learn continue

# 回顾学习内容
/learn review

# 查看历史记录
/learn history
```

---

### 任务规划类 (Task Planning)

#### /prp <功能需求描述或功能文件路径>
**用途**: 快速生成功能规划文档(Plan-Research-Plan)
**核心功能**:
- 专注研究和规划阶段
- 不执行实际实现
- 生成结构化PRP文档:
  - 问题分析
  - 研究发现
  - 实施计划
  - 验证门控

**使用场景**:
- 新功能开发前的规划
- 复杂问题的系统性分析
- 技术方案的研究和设计
- 团队协作的需求澄清

**调用方式**:
```bash
# 从描述生成
/prp "实现一个支持断点续传的大文件上传功能"

# 从文件生成
/prp path/to/feature-request.md
```

**输出**: PRPs/目录下的结构化规划文档

---

### 工具类 (Utilities)

#### /cross-workspace-sync <路径1> [路径2] [...] [--参数]
**用途**: 实现多工作区项目间的文件/文件夹智能同步
**核心功能**:
- 基于配置文件进行目标识别
- 支持批量操作
- 智能冲突处理
- 双向同步支持

**使用场景**:
- 多项目共享配置文件
- 跨项目同步代码模块
- 团队配置统一管理

**调用方式**:
```bash
# 同步单个文件
/cross-workspace-sync .claude/agents/E1-深度调研员.md

# 同步多个文件
/cross-workspace-sync .claude/agents/ .claude/commands/

# 使用参数
/cross-workspace-sync .claude/ --dry-run
```

**配置文件**: .claude/configs/cross-workspace-sync.yaml

---

#### /test
**用途**: 测试与质量验证工程师
**核心功能**:
- 全面的自动化测试执行
- 测试覆盖率管理
- 迭代修复工作流
- 确保所有代码变更经过严格验证

**使用场景**:
- 代码变更后的质量验证
- 持续集成的测试环节
- 发布前的质量把关

**调用方式**:
```bash
/test
```

**工作流程**:
1. 识别测试目标
2. 运行相关测试套件
3. 分析测试结果
4. 如有失败,迭代修复
5. 重新运行直到全部通过
6. 生成测试报告

---

## 🏗️ 命令分类架构

### 按功能分类

```
配置管理 (2个)
├── /claude              # 配置文档同步
└── /context-aware       # 8维上下文分析

文档生成 (3个)
├── /readme-generator    # README/OVERVIEW生成
└── /project-instructions # HTML文档体系管理

GitHub集成 (3个)
├── /github-start        # 仓库初始化
├── /github-pull         # 完整同步推送
└── /github-issue        # Issue处理流程

并行执行 (1个)
└── /trees               # 并行方案探索

知识管理 (2个)
├── /manus               # MANUS上下文管理
└── /learn               # 四步学习流程

任务规划 (1个)
└── /prp                 # 功能规划文档

工具类 (2个)
├── /cross-workspace-sync # 跨工作区同步
└── /test                # 测试验证
```

### 按使用频率分类

**高频使用** (日常工作流):
- /claude - 配置更新
- /github-pull - 代码推送
- /test - 质量验证
- /manus - 知识记录

**中频使用** (定期维护):
- /readme-generator - 文档更新
- /context-aware - 项目分析
- /learn - 系统学习

**低频使用** (特定场景):
- /github-start - 项目初始化
- /github-issue - Issue处理
- /trees - 并行探索
- /prp - 功能规划
- /cross-workspace-sync - 跨项目同步
- /project-instructions - 文档体系管理

---

## 📝 使用规范

### 1. 命令调用格式

**无参数命令**:
```bash
/claude
/context-aware
/readme-generator
/test
```

**带参数命令**:
```bash
/github-issue 123
/prp "功能描述"
/trees 功能名 3 "执行计划"
/cross-workspace-sync path/to/file
/manus decision "决策内容"
/learn step=what
```

### 2. 参数说明

**位置参数**:
- `$1`, `$2`, `$3`: 按顺序传递的参数
- `$ARGUMENTS`: 所有参数的组合

**可选参数**:
- `--dry-run`: 模拟执行,不实际操作
- `--verbose`: 详细输出
- `--force`: 强制执行

### 3. 命令组合使用

**典型工作流1: 项目初始化**
```bash
1. /github-start          # 创建GitHub仓库
2. /readme-generator      # 生成项目文档
3. /claude                # 更新配置文档
4. /github-pull           # 推送到远程
```

**典型工作流2: 功能开发**
```bash
1. /prp "功能需求"        # 生成规划文档
2. (实施开发)
3. /test                  # 运行测试
4. /claude                # 更新配置
5. /github-pull           # 推送变更
```

**典型工作流3: 知识沉淀**
```bash
1. /learn step=what       # 开始学习流程
2. /learn step=why        # 分析原因
3. /learn step=how        # 设计方案
4. /learn step=wield      # 实施验证
5. /manus "总结经验"      # 记录关键知识
```

---

## 🔧 配置与集成

### 命令文件格式

每个命令文件遵循统一格式:

```markdown
---
description: 命令功能描述
allowed-tools: ["Read", "Write", "Edit"]  # 可选
model: claude-sonnet-4.5                  # 可选
---

# 命令内容

命令执行时注入的提示内容

## 支持特性

- 参数: $ARGUMENTS, $1, $2, $3
- Bash执行: !command
- 文件引用: @path/to/file
```

### Bash执行语法

```markdown
# 执行git命令并注入结果
!git status

# 执行Python脚本
!python3 scripts/analyze.py

# 执行复杂命令
!find . -name "*.md" | wc -l
```

### 文件引用语法

```markdown
# 引用文件内容
@README.md

# 引用配置文件
@.claude/CLAUDE.md

# 引用多个文件
@file1.md
@file2.md
```

---

## 📊 命令统计

| 分类 | 命令数 | 占比 |
|------|--------|------|
| 配置管理 | 2 | 15.4% |
| 文档生成 | 2 | 15.4% |
| GitHub集成 | 3 | 23.1% |
| 并行执行 | 1 | 7.7% |
| 知识管理 | 2 | 15.4% |
| 任务规划 | 1 | 7.7% |
| 工具类 | 2 | 15.4% |
| **总计** | **13** | **100%** |

---

## 🚀 快速开始

### 场景 1: 新项目初始化

```bash
# Step 1: 创建GitHub仓库并推送
/github-start

# Step 2: 生成完整项目文档
/readme-generator

# Step 3: 更新配置文档
/claude

# Step 4: 同步到远程
/github-pull
```

### 场景 2: 功能开发与测试

```bash
# Step 1: 生成功能规划
/prp "实现用户认证功能"

# Step 2: (执行开发工作)

# Step 3: 运行测试验证
/test

# Step 4: 记录关键决策
/manus decision "选择JWT而非Session,因为需要无状态API"

# Step 5: 推送变更
/github-pull
```

### 场景 3: 问题修复流程

```bash
# Step 1: 处理GitHub Issue
/github-issue 123

# Step 2: (命令会自动分析、修复、测试)

# Step 3: 更新文档
/readme-generator

# Step 4: 推送修复
/github-pull
```

### 场景 4: 知识积累

```bash
# Step 1: 开始学习流程
/learn step=what

# Step 2: 继续后续步骤
/learn continue

# Step 3: 记录关键经验
/manus pattern "使用Builder模式简化复杂对象构造"

# Step 4: 回顾学习成果
/learn review
```

---

## 📚 相关文档

- [项目主README](../../README.md) - 项目整体介绍
- [OVERVIEW.md](../../OVERVIEW.md) - 技术架构深度解析
- [CLAUDE.md](../../CLAUDE.md) - Claude Code配置文档
- [agents目录](../agents/情报组/) - 8个E系列智能体说明

---

## 🔍 命令开发指南

### 创建新命令

1. **创建命令文件**:
   ```bash
   touch .claude/commands/my-command.md
   ```

2. **编写命令内容**:
   ```markdown
   ---
   description: 我的自定义命令
   allowed-tools: ["Read", "Write"]
   ---

   # 命令逻辑

   根据用户输入执行特定操作...
   ```

3. **更新配置**:
   ```bash
   /claude
   ```

4. **测试命令**:
   ```bash
   /my-command 参数1 参数2
   ```

### 命令最佳实践

**DO ✅**:
- 使用清晰的命令描述
- 提供参数说明和示例
- 处理边界情况和错误
- 生成详细的日志
- 更新配置文档

**DON'T ❌**:
- 硬编码路径和配置
- 忽略错误处理
- 缺少使用说明
- 过度复杂的逻辑
- 缺少测试验证

---

## 📝 维护日志

- **2025-10-27**: 创建命令目录README,文档化13个斜杠命令
- **未来计划**: 添加更多自动化命令,增强工作流集成

---

**文档版本**: v1.0.0
**最后更新**: 2025-10-27
**维护者**: ZTL数智化作战中心
