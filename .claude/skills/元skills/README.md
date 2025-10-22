# 元Skills (Meta Skills)

> 元Skills包含两类:
> 1. **Anthropic官方Skills**: skill-creator, template-skill (来自官方仓库)
> 2. **F系列元Skills**: agents, commands, hooks, output-styles (基于F系列智能体转化)
>
> 更新时间: 2025-10-21

---

## 📋 目录

- [F系列元Skills](#f系列元skills) (新增)
  - [agents](#1-agents) - 智能体创建
  - [commands](#2-commands) - 斜杠命令创建
  - [hooks](#3-hooks) - 钩子函数创建
  - [output-styles](#4-output-styles) - 输出样式设计
- [Anthropic官方Skills](#anthropic官方skills)
  - [skill-creator](#5-skill-creator) - Skill创建指导
  - [template-skill](#6-template-skill) - Skill模板起点

---

## F系列元Skills

> 基于F系列系统智能体(F1-F4)转化而成的元技能包,提供Claude Code框架的核心开发能力。

### 1. agents

**功能定位**: Claude Code subagent创建专家

**使用场景**: 当需要创建新的智能体或优化现有智能体配置时使用

**核心能力**:
- 基于2025最新prompt engineering规范和context engineering原则
- 提供完整的subagent创建工作流:
  1. 定义智能体价值 (目标、领域、价值生成方式)
  2. 设计交互架构 (交互模式、自主程度)
  3. 规划组件能力 (工具配置、记忆系统、护栏机制)
  4. 构建系统提示 (10元素提示系统)
  5. 创建subagent文件 (YAML格式、命名规范)
  6. 激活与管理 (/agents命令)

**关键特性**:
- 上下文工程 > 提示词工程的范式转变
- 10元素提示系统 (用户角色、任务上下文、语气上下文等)
- Chain-of-Thought推理引导
- 三层架构 (项目级/CLI级/用户级)
- 独立上下文窗口保护主对话

**文件位置**: `agents/SKILL.md`

---

### 2. commands

**功能定位**: Claude Code slash command创建专家

**使用场景**: 当需要创建可复用的斜杠命令工作流时使用

**核心能力**:
- 基于官方specifications和best practices
- 提供完整的command创建工作流:
  1. 需求分析 (目标、频率、范围、复杂度)
  2. 参数设计 ($ARGUMENTS vs $1,$2,...)
  3. 工具权限配置 (最小权限原则)
  4. 命令内容构建 (结构化Markdown)
  5. 创建与激活 (项目级/用户级)

**关键特性**:
- 支持参数化 ($ARGUMENTS, 位置参数)
- Bash命令执行 (!`command`)
- 文件引用 (@filename)
- 命名空间组织 (子目录)
- SlashCommand工具集成 (自动发现)
- 字符预算限制管理

**文件位置**: `commands/SKILL.md`

---

### 3. hooks

**功能定位**: Claude Code hooks系统创建专家

**使用场景**: 当需要事件驱动的自动化工作流时使用

**核心能力**:
- 基于Claude Code钩子系统的8个生命周期事件
- 提供完整的hook创建工作流:
  1. 识别触发时机 (8种事件类型)
  2. 设计执行逻辑 (脚本开发)
  3. 实现匹配器 (正则表达式模式)
  4. 配置环境变量 (敏感信息管理)
  5. 测试与调试 (日志输出、错误处理)

**关键特性**:
- 8种Hook事件类型:
  - PreToolUse / PostToolUse (工具调用前后)
  - UserPromptSubmit (提示词提交)
  - SubagentStop (子智能体结束)
  - Stop (对话结束)
  - Notification (通知事件)
  - PreCompact (上下文压缩前)
  - SessionStart (会话开始)
- 跨平台兼容 (纯bash JSON解析,无jq依赖)
- 真实世界经验与陷阱指南
- 三层配置架构 (项目/项目本地/用户)

**文件位置**: `hooks/SKILL.md`

**重要提醒**:
- ⚠️ 配置更改后需重启会话才能生效
- ⚠️ 注意跨平台JSON解析兼容性
- ⚠️ 静默失败诊断技巧

---

### 4. output-styles

**功能定位**: Claude Code output style设计专家

**使用场景**: 当需要自定义输出格式或优化输出体验时使用

**核心能力**:
- 基于2025最新output styles规范
- 提供完整的style创建工作流:
  1. 需求分析 (场景、格式、详细程度、语气、受众)
  2. 格式结构设计 (分层结构、视觉元素)
  3. System Prompt编写 (结构要求、格式规则)
  4. 配置文件生成 (YAML front matter)
  5. 测试与优化 (质量检查清单)

**关键特性**:
- 多种输出格式类型 (Markdown, JSON, XML, Table)
- 三种详细程度级别 (简洁/标准/详细)
- 四种语气风格 (专业/友好/教学/技术)
- 三层架构 (项目级/CLI级/用户级)
- 完整示例 (代码审查报告、API响应)

**文件位置**: `output-styles/SKILL.md`

---

## Anthropic官方Skills

> 来源: Anthropic官方Skills仓库 (https://github.com/anthropics/skills)

### 5. skill-creator

**功能定位**: Skill创建指导工具

**使用场景**: 当需要创建新的Skill或更新现有Skill时使用

**核心能力**:
- 提供完整的Skill创建流程指导
- 包含6个关键步骤:
  1. 通过具体示例理解Skill需求
  2. 规划可复用的Skill内容
  3. 初始化Skill结构
  4. 编辑和完善Skill
  5. 打包Skill为可分发的zip文件
  6. 迭代优化Skill

**文件位置**: `skill-creator/SKILL.md`

**关键特性**:
- 详细的Skill解剖学说明 (SKILL.md + scripts/ + references/ + assets/)
- 渐进披露设计原则 (三级加载系统)
- 脚本、参考文档、资源文件的最佳实践
- 完整的打包和验证流程

---

### 6. template-skill

**功能定位**: Skill模板起点

**使用场景**: 作为创建新Skill的基础模板使用

**核心能力**:
- 提供最小化的Skill结构
- 包含必需的YAML frontmatter
- 预留指令编写区域

**文件位置**: `template-skill/SKILL.md`

**使用方法**:
1. 复制`template-skill`目录
2. 重命名为新的skill名称
3. 更新YAML frontmatter中的`name`和`description`
4. 在`# Insert instructions below`下方添加具体指令

---

## 🎯 使用指南

### 使用F系列元Skills

**场景1: 创建新的智能体**
```
> I need help creating a new subagent for [specific domain]
```
Claude会自动发现并使用`agents` skill来指导完整的创建流程。

**场景2: 创建新的斜杠命令**
```
> Help me create a slash command for [specific workflow]
```
Claude会自动发现并使用`commands` skill来指导命令创建。

**场景3: 创建自动化钩子**
```
> I need to set up a hook that [specific automation]
```
Claude会自动发现并使用`hooks` skill来指导钩子开发。

**场景4: 自定义输出格式**
```
> Help me design an output style for [specific scenario]
```
Claude会自动发现并使用`output-styles` skill来指导样式设计。

### 创建新Skill的标准流程

```bash
# 1. 使用skill-creator获取创建指导
Use the skill-creator to help me build a skill for [你的需求]

# 2. (可选) 基于template-skill创建基础结构
cp -r .claude/skills/元skills/template-skill .claude/skills/my-new-skill

# 3. 编辑SKILL.md
# - 更新name和description
# - 添加详细指令
# - (可选) 添加scripts/、references/、assets/目录

# 4. 测试Skill
# 在Claude Code中直接使用Skill进行测试

# 5. 迭代优化
# 根据使用反馈改进Skill
```

---

## 📚 关键概念

### Skill的三层结构

1. **SKILL.md (必需)**
   - YAML frontmatter: name + description
   - Markdown指令内容

2. **Bundled Resources (可选)**
   - `scripts/`: 可执行代码 (Python/Bash等)
   - `references/`: 参考文档 (按需加载到上下文)
   - `assets/`: 输出资源 (模板、图标、字体等)

### 渐进披露原则

Skills使用三级加载系统来高效管理上下文:

1. **元数据** (name + description) - 始终在上下文 (~100词)
2. **SKILL.md主体** - 当Skill触发时加载 (<5k词)
3. **捆绑资源** - 按需加载 (无限制*)

*无限制是因为scripts可以在不读入上下文窗口的情况下执行

---

## 🔗 相关资源

### 官方文档
- [What are Skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Creating Custom Skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [Skills API](https://docs.claude.com/en/api/skills)

### 学习教程
- [Skill创建教程](https://skywork.ai/blog/ai-agent/how-to-create-claude-skill-step-by-step-guide/)
- [Anthropic工程博客](https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

### 社区资源
- [Anthropic官方Skills库](https://github.com/anthropics/skills)
- [Awesome Claude Skills](https://github.com/travisvn/awesome-claude-skills)
- [Superpowers技能库](https://github.com/obra/superpowers)

---

## 📖 最佳实践

### SKILL.md编写规范

1. **使用祈使语气**: 使用动词开头的指令式语言
   - ✅ "To accomplish X, do Y"
   - ❌ "You should do X"

2. **明确的元数据**:
   - `name`: 小写、连字符分隔 (如`my-skill-name`)
   - `description`: 清晰说明Skill的功能和使用场景 (使用第三人称)

3. **避免重复**: 信息应存在于SKILL.md或references文件中,不要两者都有
   - 核心流程指导 → SKILL.md
   - 详细参考资料 → references/

4. **保持简洁**: SKILL.md主体控制在5k词以内,详细信息放入references/

---

## 🚀 快速开始

### 示例1: 使用skill-creator创建新Skill

```
> Use the skill-creator to help me build a skill for [功能描述]
```

Claude会引导你完成完整的Skill创建流程。

### 示例2: 基于template-skill快速创建

```bash
# 1. 复制模板
cp -r .claude/skills/元skills/template-skill .claude/skills/pdf-processor

# 2. 编辑SKILL.md
---
name: pdf-processor
description: This skill should be used when users want to extract text, rotate, merge, or split PDF files.
---

# PDF Processor

This skill provides tools for common PDF operations.

## Core Functions
- Extract text from PDFs
- Rotate PDF pages
- Merge multiple PDFs
- Split PDF into separate pages

## Usage
When a user requests PDF operations, use the appropriate script from `scripts/` directory...
```

---

**最后更新**: 2025-10-21
**维护者**: ZTL数智化作战中心
**来源**: Anthropic Official Skills Repository
