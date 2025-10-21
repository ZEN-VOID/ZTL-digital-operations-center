# 元Skills (Meta Skills)

> 来源: Anthropic官方Skills仓库
> 仓库: https://github.com/anthropics/skills
> 更新时间: 2025-10-21

---

## 📋 Skills列表

### 1. skill-creator

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

### 2. template-skill

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
