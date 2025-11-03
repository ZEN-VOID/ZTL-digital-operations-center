#!/usr/bin/env python3
"""
README文档生成器
基于/readme-generator命令的实现
"""

import os
import json
import glob
from pathlib import Path
from datetime import datetime
from typing import Dict, List

class READMEGenerator:
    def __init__(self, project_root: Path):
        self.root = project_root
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def analyze_project(self) -> Dict:
        """8维度项目分析"""
        return {
            "project_name": "ZTL数智化作战中心",
            "description": "Multi-agent orchestration platform for restaurant industry digital transformation",
            "agents": self._count_agents(),
            "commands": self._count_commands(),
            "skills": self._count_skills(),
            "plugins": self._count_plugins(),
            "directory_count": self._count_directories(),
        }

    def _count_agents(self) -> Dict:
        """统计智能体数量"""
        agents = {}
        plugins_dir = self.root / "plugins"
        if plugins_dir.exists():
            for group_dir in plugins_dir.iterdir():
                if group_dir.is_dir():
                    agents_dir = group_dir / "agents"
                    if agents_dir.exists():
                        count = len(list(agents_dir.glob("*.md")))
                        agents[group_dir.name] = count
        return agents

    def _count_commands(self) -> int:
        """统计命令数量"""
        commands_dir = self.root / ".claude" / "commands"
        if commands_dir.exists():
            return len(list(commands_dir.glob("*.md")))
        return 0

    def _count_skills(self) -> int:
        """统计技能包数量"""
        skills_dir = self.root / ".claude" / "skills"
        if skills_dir.exists():
            return len([d for d in skills_dir.iterdir() if d.is_dir()])
        return 0

    def _count_plugins(self) -> int:
        """统计插件数量"""
        plugins_dir = self.root / "plugins"
        if plugins_dir.exists():
            return len([d for d in plugins_dir.iterdir() if d.is_dir()])
        return 0

    def _count_directories(self) -> int:
        """统计目录数量"""
        dirs_file = self.root / "trees" / "dirs_*.txt"
        files = list(self.root.glob("trees/dirs_*.txt"))
        if files:
            latest = max(files, key=os.path.getmtime)
            with open(latest) as f:
                return len(f.readlines())
        return 0

    def generate_readme(self, profile: Dict) -> str:
        """生成README.md内容"""
        total_agents = sum(profile["agents"].values())

        content = f"""# {profile["project_name"]}

> Multi-Agent Orchestration Platform for Restaurant Industry Digital Transformation

[![Claude Code](https://img.shields.io/badge/Claude-Code-8B5CF6)](https://claude.ai/code)
[![Agents](https://img.shields.io/badge/Agents-{total_agents}-blue)](.claude/agents/)
[![Commands](https://img.shields.io/badge/Commands-{profile["commands"]}-green)](.claude/commands/)
[![Skills](https://img.shields.io/badge/Skills-{profile["skills"]}-orange)](.claude/skills/)

## 📖 项目简介

ZTL数智化作战中心是基于Claude Code + Sonnet 4.5构建的**多智能体编排平台**,专为餐饮行业数字化转型设计。通过协调**{total_agents}个专业智能体**分布在**{profile["plugins"]}个业务组**,实现从战略规划到门店筹建的全流程智能化。

### 核心理念

这不是传统的单体应用,而是一个**智能体编排框架**。Claude通过动态组合专业智能体,每个智能体都拥有领域专业知识编码在其Markdown定义中。

## ✨ 核心特性

- 🤖 **60+专业智能体** - 覆盖战略、创意、情报、筹建、开发、美团、供应、行政8大业务组
- 🎯 **三层架构** - 知识层(Agents+Skills) → 编排层(Claude推理) → 执行层(Tools+Output)
- 🔄 **多模式执行** - 支持三层架构、直接执行、混合协调三种模式
- 📊 **智能调度** - QQ-总指挥官统筹多智能体协作
- 🛠️ **工具生态** - 集成7+ MCP服务器(chrome, playwright, github, context7, lark, cos, supabase)
- 📁 **标准化输出** - output/[项目名]/[agent-name]/ 结构化输出路径

## 🏗️ 技术架构

### 架构层次

```
Layer 1: 知识层 (.claude/agents/ + .claude/skills/)
  ├── Agents: 角色决策框架和领域知识
  └── Skills: 自包含能力包和执行引擎

Layer 2: 编排层 (Claude推理)
  ├── 运行时推理和动态能力组合
  └── 智能路由和任务调度

Layer 3: 执行层 (Tools + Output)
  ├── 工具执行(Bash, Python, API, MCP)
  └── 结果持久化到 output/[项目名]/[agent-name]/
```

### 技术栈

| 类别 | 技术 |
|------|------|
| AI核心 | Claude Code, Sonnet 4.5 |
| 智能体架构 | Multi-Agent System, Task-based Delegation |
| 协议标准 | Model Context Protocol (MCP) |
| 开发语言 | Python, TypeScript, Markdown |
| 浏览器自动化 | chrome-mcp, playwright-mcp |
| 版本控制 | Git, GitHub API (github-mcp) |
| 云服务 | Tencent COS (cos-mcp), Supabase (supabase-mcp) |
| 企业协作 | Feishu/Lark (lark-mcp) |

## 📁 项目结构

基于最新快照生成时间: {self.timestamp}

```
.
├── .claude/              # Claude Code配置
│   ├── agents/          # 智能体定义({total_agents}个)
│   ├── commands/        # 斜杠命令({profile["commands"]}个)
│   ├── hooks/           # 生命周期钩子
│   └── skills/          # 技能包({profile["skills"]}个)
├── plugins/             # 业务组插件({profile["plugins"]}个)
│   ├── 战略组/
│   ├── 创意组/
│   ├── 情报组/
│   ├── 筹建组/
│   ├── 开发组/
│   ├── 美团组/
│   ├── 供应组/
│   └── 行政组/
├── output/              # 智能体输出目录
├── reports/             # 执行报告
├── trees/               # 目录快照
├── PRPs/                # PRP文档
└── project/             # 项目代码
```

详细目录树参见: [trees/tree_structure_*.md](trees/)

## 🚀 快速开始

### 环境要求

- Claude Code CLI
- Python 3.12+
- Node.js 18+ (可选,用于MCP服务器)
- Git

### 使用指南

1. **调用智能体**:
```python
# 通过Task工具调用专业智能体
Task(subagent_type="G1-经营分析优化师",
     prompt="分析本月门店经营数据")
```

2. **使用命令**:
```bash
/prp <feature-description>     # 生成PRP文档
/test                           # 运行测试套件
/context-aware                  # 8维度项目分析
/github-pull                    # 同步到GitHub
```

3. **协调多智能体**:
```python
# 复杂任务调用总指挥官
Task(subagent_type="QQ-总指挥官",
     prompt="为新开的火锅店做完整的开业筹备方案")
```

## 🤖 智能体系统

### 业务组概览

| 业务组 | 智能体数量 | 核心职能 |
|--------|-----------|----------|
"""

        for group, count in profile["agents"].items():
            content += f"| {group} | {count}个 | 专业领域智能体 |\n"

        content += f"""

详细信息请参阅: [OVERVIEW.md](OVERVIEW.md#智能体系统)

## 📜 命令系统

项目包含**{profile["commands"]}个斜杠命令**,分为以下类别:

- **PRP工作流**: `/prp`, `/test`
- **上下文管理**: `/context-aware`, `/manus`
- **项目管理**: `/github-pull`, `/github-issue`, `/readme-generator`, `/claude`
- **智能体编排**: `/trees`, `/trees-clean`

完整命令列表参见: [.claude/commands/](.claude/commands/)

## 📊 项目统计

- **总目录数**: {profile["directory_count"]}
- **智能体数**: {total_agents}个({profile["plugins"]}个业务组)
- **命令数**: {profile["commands"]}个
- **技能包数**: {profile["skills"]}个
- **MCP服务器**: 7+个

## 🛣️ 开发指南

### 创建新智能体

智能体是`.claude/agents/[业务组]/`下的Markdown文件:

```markdown
---
name: 智能体名称
description: 简短描述
model: claude-sonnet-4.5
tools: ["*"]
---

# 角色定位

[智能体的专业领域和职责]

# 工作流程

1. 分析需求
2. 执行任务
3. 输出结果

# 输出规范

[输出格式和质量标准]
```

创建后运行 `/claude` 同步文档。

### 创建新技能包

技能包位于 `.claude/skills/[category]/[skill-name]/`:

```
skill-name/
├── SKILL.md              # 元数据(YAML) + 使用指南
├── scripts/              # 执行引擎(Python)
│   └── core_engine.py
└── reference.md          # 扩展文档(可选)
```

技能包使用**渐进披露原则**:Claude先加载SKILL.md(~500-2000 tokens),然后按需加载scripts/reference。

### 最佳实践

- ✅ 复杂功能先使用 `/prp` 生成PRP文档
- ✅ 所有改动通过 `/test` 验证
- ✅ 提交前使用 `/github-pull` 同步
- ✅ 定期执行 `/context-aware` 刷新上下文
- ✅ 手动修改配置后运行 `/claude` 更新文档

## 📄 相关文档

- [OVERVIEW.md](OVERVIEW.md) - 技术深度文档
- [CLAUDE.md](CLAUDE.md) - 项目配置指南
- [~/.claude/CLAUDE.md](~/.claude/CLAUDE.md) - 全局配置文档

## 📄 许可证

本项目为私有项目,未经授权不得复制、修改或分发。

---

**⭐ 最后更新**: {self.timestamp}
**🔧 生成工具**: `/readme-generator` 命令

*这是一个活文档。运行 `/readme-generator` 在重大配置更改后保持其与实际项目状态同步。*
"""

        return content

    def generate_overview(self, profile: Dict) -> str:
        """生成OVERVIEW.md内容"""
        total_agents = sum(profile["agents"].values())

        content = f"""# {profile["project_name"]} - 技术概览

> Deep Technical Documentation

**最后更新**: {self.timestamp}

## 📋 项目概要

- **项目类型**: Multi-Agent Orchestration Platform
- **核心定位**: Restaurant Industry Digital Transformation
- **技术栈**: Claude Code + Sonnet 4.5
- **智能体规模**: {total_agents}个专业智能体 × {profile["plugins"]}个业务组

### 价值主张

1. **智能化决策**: 60+专业智能体提供领域专业知识
2. **动态编排**: Claude运行时推理实现智能任务路由
3. **标准化执行**: 三层架构确保质量可追溯
4. **开放生态**: 7+ MCP服务器无缝集成外部系统

## 🏗️ 架构设计

### 整体架构

```mermaid
graph TD
    A[用户请求] --> B[Claude Code]
    B --> C{{智能体选择}}
    C --> D[QQ-总指挥官]
    C --> E[业务组智能体]
    D --> F[多智能体协作]
    E --> G[任务执行]
    F --> G
    G --> H[输出结果]
    H --> I[output/[项目名]/[agent-name]/]
```

### 三层架构模式

**Layer 1: 知识层**
- 位置: `.claude/agents/` + `.claude/skills/`
- 内容: Markdown格式的智能体定义和技能包
- 特点: 声明式知识,易于维护和版本控制

**Layer 2: 编排层**
- 执行者: Claude Code运行时推理
- 能力: 动态能力组合,智能路由调度
- 机制: 基于任务特征选择最佳智能体

**Layer 3: 执行层**
- 工具: Bash, Python, MCP服务器
- 输出: `output/[项目名]/[agent-name]/`
- 追溯: plans/, results/, logs/, metadata/

### 目录结构

基于最新快照: {self.timestamp}

```
ZTL数智化作战中心/
├── .claude/                  # Claude Code核心配置
│   ├── agents/              # {total_agents}个智能体定义
│   ├── commands/            # {profile["commands"]}个斜杠命令
│   ├── hooks/               # 生命周期钩子
│   │   ├── parallel-claude-after-compact.sh
│   │   └── README.md
│   ├── skills/              # {profile["skills"]}个技能包
│   └── logs/                # 执行日志
│
├── plugins/                 # {profile["plugins"]}个业务组插件
"""

        for group, count in profile["agents"].items():
            content += f"│   ├── {group}/          # {count}个智能体\n"

        content += f"""│
├── output/                  # 智能体输出目录
│   ├── [项目名]/
│   │   └── [agent-name]/
│   │       ├── plans/       # 执行计划
│   │       ├── results/     # 最终输出
│   │       ├── logs/        # 执行日志
│   │       └── metadata/    # 追溯元数据
│
├── reports/                 # 执行报告
├── trees/                   # 目录快照
├── PRPs/                    # PRP文档
├── project/                 # 项目代码
│   └── web-ui/             # Web前端项目
└── context/                 # 上下文管理
    └── snapshots/          # 上下文快照

总目录数: {profile["directory_count"]}
```

## 🤖 智能体系统

### 组织架构

本项目采用**多智能体协作架构**,共有**{total_agents}个专业智能体**。

### 各业务组智能体清单

"""

        for group, count in profile["agents"].items():
            content += f"#### {group}\n\n"
            content += f"智能体数量: {count}个\n\n"
            content += "详细列表请查看: `.claude/agents/{group}/`\n\n"

        content += f"""### 协作机制

- **Task工具**: 调用子智能体执行专业任务
- **组长智能体**: 负责任务分解和调度(如GG-战略组组长)
- **专业智能体**: 执行具体的业务任务
- **QQ-总指挥官**: 统筹多业务组协作,生成JSON作战指令

### 执行模式

项目支持三种智能体执行模式:

1. **三层架构模式** (适用于AIGC、调研、战略等)
   - 规范层(.md) → 计划层(JSON) → 执行层(Scripts)
   - 特点: 批量处理能力强,质量可追溯

2. **直接执行模式** (适用于开发组12个智能体)
   - 规范层(.md) → 执行层(Tools直接调用)
   - 特点: 快速迭代,实时反馈

3. **混合协调模式** (适用于复杂业务协作)
   - 战略阶段用三层架构,执行阶段用直接执行
   - 特点: 灵活性强,兼顾质量和效率

## 📜 命令系统

### 命令清单

项目包含**{profile["commands"]}个斜杠命令**:

| 命令 | 功能 | 类别 |
|------|------|------|
| /prp | 生成PRP文档 | PRP工作流 |
| /test | 运行测试套件 | PRP工作流 |
| /context-aware | 8维度项目分析 | 上下文管理 |
| /manus | 统一上下文管理系统 | 上下文管理 |
| /github-pull | 同步到GitHub | 项目管理 |
| /github-issue | 系统化Issue处理 | 项目管理 |
| /readme-generator | 自动更新README | 项目管理 |
| /claude | 更新CLAUDE.md配置 | 项目管理 |
| /trees | 并行执行工作流 | 智能体编排 |
| /trees-clean | 清理并行工作空间 | 智能体编排 |

### 命令分类

**PRP工作流类**:
- `/prp` - 复杂功能开发前必须执行
- `/test` - 迭代修复直到所有测试通过

**上下文管理类**:
- `/context-aware` - 项目概览分析
- `/manus` - 注意力管理、错误学习、知识沉淀

**项目管理类**:
- `/github-pull` - 包含目录结构变更检测和引用同步
- `/github-issue` - Issue分析、修复、关闭全流程
- `/readme-generator` - 双层文档生成(README + OVERVIEW)
- `/claude` - 配置文档更新

**智能体编排类**:
- `/trees` - 多方案并行探索
- `/trees-clean` - 清理工作树残留

### 使用示例

```bash
# 复杂功能开发工作流
/prp "为美团平台添加自动化报表生成功能"
# → 生成PRP文档,包含研究、蓝图、验证门控

/test
# → 运行测试套件,自动修复失败直到全部通过

# 项目同步工作流
/github-pull
# → 检测目录变更 → 同步引用 → 更新README → 提交推送

# 上下文管理工作流
/context-aware
# → 8维度分析: 智能体、命令、钩子、技能包、结构、学习、配置、文档
```

## 🛠️ 技术栈

### 核心技术

- **Claude Code**: AI-native开发框架
- **Sonnet 4.5**: 最新Claude模型
- **Multi-Agent System**: 多智能体协作架构
- **Model Context Protocol (MCP)**: 标准化工具协议

### MCP服务器集成

项目集成**7+ MCP服务器**:

1. **chrome-mcp**: 浏览器自动化(20+工具)
   - 页面导航、元素交互、网页抓取

2. **playwright-mcp**: 深度网页爬取(30+工具)
   - 复杂交互、网络捕获、截图

3. **github-mcp**: GitHub操作(25+工具)
   - 仓库、Issue、PR、代码搜索

4. **context7**: 实时库文档(2工具)
   - 解析库ID、获取最新文档

5. **lark-mcp**: 飞书/Lark集成(15+工具)
   - 消息、多维表格、文档

6. **cos-mcp**: 腾讯云COS(10+工具)
   - 文件管理、图片处理

7. **supabase-mcp**: Supabase PostgreSQL
   - 数据库操作、表管理

## 💻 开发指南

### 环境要求

- Claude Code CLI
- Python 3.12+
- Node.js 18+ (MCP服务器)
- Git

### 项目结构说明

```yaml
配置层:
  - .claude/: Claude Code核心配置
  - plugins/: 业务组插件(隔离)

知识层:
  - .claude/agents/: 智能体定义(Markdown)
  - .claude/skills/: 技能包(Scripts + 文档)

执行层:
  - output/: 智能体输出目录
  - reports/: 执行报告
  - trees/: 目录快照

开发层:
  - project/web-ui/: Web前端项目
  - PRPs/: PRP文档

上下文层:
  - context/snapshots/: 上下文快照
  - .claude/logs/: 执行日志
```

### 开发流程

1. **需求分析**: 使用`/context-aware`了解项目全貌
2. **规划设计**: 复杂功能使用`/prp`生成PRP文档
3. **实现开发**: 调用相应智能体执行任务
4. **测试验证**: 使用`/test`运行测试套件
5. **文档更新**: 使用`/readme-generator`和`/claude`同步文档
6. **版本控制**: 使用`/github-pull`推送到GitHub

### 最佳实践

**智能体开发**:
- ✅ 使用Markdown格式定义智能体
- ✅ YAML frontmatter包含name, description, model, tools
- ✅ 明确定义角色、工作流程、输出规范
- ✅ 创建后运行`/claude`同步文档

**技能包开发**:
- ✅ 遵循渐进披露原则(SKILL.md → scripts → reference)
- ✅ 核心逻辑封装在scripts/目录
- ✅ 使用allowed-tools限制工具访问(如需要)

**PRP工作流**:
- ✅ 复杂功能(非平凡)必须先生成PRP
- ✅ PRP包含:代码库分析、外部研究、实现蓝图、验证门控
- ✅ PRP质量标准:≥8/10(一次性实现成功的信心度)

**测试驱动**:
- ✅ 所有改动通过`/test`验证
- ✅ 修复失败测试而非禁用它们
- ✅ 保持测试覆盖率≥80%

## 📊 项目统计

### 代码规模

- **总目录数**: {profile["directory_count"]}
- **Python文件**: (动态统计)
- **TypeScript文件**: (动态统计)
- **Markdown文件**: (动态统计)

### 系统规模

- **智能体数**: {total_agents}个
- **业务组数**: {profile["plugins"]}个
- **命令数**: {profile["commands"]}个
- **技能包数**: {profile["skills"]}个
- **MCP服务器**: 7+个

## 🔗 相关资源

- **项目文档**: [CLAUDE.md](CLAUDE.md)
- **全局配置**: [~/.claude/CLAUDE.md](~/.claude/CLAUDE.md)
- **智能体目录**: [.claude/agents/](.claude/agents/)
- **命令目录**: [.claude/commands/](.claude/commands/)
- **技能包目录**: [.claude/skills/](.claude/skills/)
- **目录快照**: [trees/](trees/)

---

**配置版本**: v1.0.0
**更新时间**: {self.timestamp}
**维护原则**: 深度分析、智能生成、标准化、可追溯

*这是一个活文档。运行 `/readme-generator` 在重大配置更改后保持其与实际项目状态同步。*
"""

        return content

    def save_documents(self, readme_content: str, overview_content: str):
        """保存文档"""
        # 备份现有文件
        readme_path = self.root / "README.md"
        overview_path = self.root / "OVERVIEW.md"

        if readme_path.exists():
            backup_time = datetime.now().strftime('%Y%m%d_%H%M%S')
            readme_path.rename(self.root / f"README.md.backup.{backup_time}")
            print(f"✅ 备份README.md → README.md.backup.{backup_time}")

        if overview_path.exists():
            backup_time = datetime.now().strftime('%Y%m%d_%H%M%S')
            overview_path.rename(self.root / f"OVERVIEW.md.backup.{backup_time}")
            print(f"✅ 备份OVERVIEW.md → OVERVIEW.md.backup.{backup_time}")

        # 写入新文件
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"✅ 生成README.md ({len(readme_content)} 字符)")

        with open(overview_path, 'w', encoding='utf-8') as f:
            f.write(overview_content)
        print(f"✅ 生成OVERVIEW.md ({len(overview_content)} 字符)")

def main():
    project_root = Path(__file__).parent
    generator = READMEGenerator(project_root)

    print("=" * 60)
    print("📋 README文档生成器")
    print("=" * 60)
    print()

    print("Step 2: 深度项目分析...")
    profile = generator.analyze_project()
    print(f"✅ 分析完成")
    print(f"   - 智能体: {sum(profile['agents'].values())}个")
    print(f"   - 命令: {profile['commands']}个")
    print(f"   - 技能包: {profile['skills']}个")
    print(f"   - 插件: {profile['plugins']}个")
    print()

    print("Step 3: 生成双层文档...")
    readme_content = generator.generate_readme(profile)
    overview_content = generator.generate_overview(profile)
    print("✅ 内容生成完成")
    print()

    print("Step 5: 保存文档...")
    generator.save_documents(readme_content, overview_content)
    print()

    print("=" * 60)
    print("✅ README文档生成完成")
    print("=" * 60)
    print()
    print("生成的文件:")
    print("  - README.md (入门文档)")
    print("  - OVERVIEW.md (技术文档)")
    print()

if __name__ == "__main__":
    main()
