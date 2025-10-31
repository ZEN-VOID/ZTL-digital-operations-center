# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ZTL数智化作战中心 (ZTL Digital Intelligence Operations Center) is a multi-agent orchestration platform for the restaurant industry's digital transformation. Built on Claude Code + Sonnet 4.5, it coordinates **60+ specialized agents** across **8 business groups** to handle everything from strategic planning to store construction.

**Core Philosophy**: This is not a traditional monolithic application. It's an **agent orchestration framework** where Claude dynamically composes solutions by coordinating specialized agents, each with domain expertise encoded in their Markdown definitions.

## Architecture

### Three-Layer Agent Architecture

```
Layer 1: Knowledge Layer (.claude/agents/ + .claude/skills/)
  ├── Agents: Role-based decision frameworks and domain knowledge
  └── Skills: Self-contained capability packages with execution engines

Layer 2: Orchestration Layer (Claude Reasoning)
  ├── Runtime reasoning and dynamic capability composition
  └── Intelligent routing and task scheduling

Layer 3: Execution Layer (Tools + Output)
  ├── Tool execution (Bash, Python, API, MCP)
  └── Results persisted to output/[项目名]/[agent-name]/
```

### Agent Organization

Agents are organized into **8 business groups** under `plugins/`:

- **战略组** (Strategy): 9 agents - Business strategy, operations analysis, product positioning
- **创意组** (Creative): 9 agents - Advertising, copywriting, design, video production
- **情报组** (Intelligence): 8 agents - Research, web scraping, data analysis
- **筹建组** (Construction): 6 agents - Floor plans, BIM modeling, space design
- **开发组** (Development): 11 agents - Full-stack development, testing, deployment
- **美团组** (Meituan Ops): 6 agents - Platform operations, marketing, reporting
- **供应组** (Supply Chain): 7 agents - Procurement, inventory, cost management
- **行政组** (Admin): 9 agents - Finance, HR, legal, document management

Each plugin directory follows this structure:
```
plugins/[业务组]/
├── plugin.json           # Plugin metadata
├── agents/               # Agent definitions (Markdown)
├── commands/             # Business-specific commands
├── skills/               # Business-specific skills
└── README.md            # Group documentation
```

### Output Path Convention

**Critical**: All agent outputs follow a standardized path structure defined in the global CLAUDE.md:

```
output/[项目名]/[agent-name]/
├── plans/      # Execution plan configs (JSON/YAML)
├── results/    # Actual outputs (images, docs, data)
├── logs/       # Execution logs
└── metadata/   # Traceability metadata
```

**Project naming** is dynamic and user-driven:
- Good: "火锅店开业筹备", "美团营业额提升", "2025Q1数据分析"
- Avoid: "20250127任务", "task_001"

## Development Commands

### Core Workflow Commands

The command system (`/command`) provides one-shot workflows. Key commands:

**PRP Workflow** (Plan-Research-Plan):
- `/prp <feature-description>` - Generate PRP documentation (research + planning only)
- `/test` - Run full test suite with iterative fixing until all pass

**Context Management**:
- `/context-aware` - Comprehensive 8-dimension project analysis
- `/manus` - Unified context management system with attention, error learning, knowledge accumulation

**Project Management**:
- `/github-pull` - Sync project to GitHub with structure change detection
- `/github-issue <issue-url>` - Systematic issue analysis, fix, and closure
- `/readme-generator` - Auto-update README.md with structure sync
- `/claude` - Update CLAUDE.md configs (both global ~/.claude/ and project ./)

**Agent Orchestration**:
- `/trees <feature> <parallel-count> <description>` - Parallel execution workflow for multi-solution exploration
- `/trees-clean` - Thoroughly clean all worktrees, branches, and directory remnants created by /trees command

### Common Development Tasks

**Running Tests**:
```bash
# Python projects
ruff check .              # Linting
mypy .                    # Type checking
pytest                    # Unit tests
pytest --cov=.           # Coverage

# Or use the integrated command
/test                     # Runs everything with auto-fix iteration
```

**Creating a New Agent**:
Agents are Markdown files in `.claude/agents/[业务组]/`. Key sections:
- YAML frontmatter: `name`, `description`, `model`, `tools`
- Role definition and expertise
- Workflow steps
- Output specifications

After creating, run `/claude` to sync documentation.

**Creating a New Skill**:
Skills live in `.claude/skills/[category]/[skill-name]/`:
```
skill-name/
├── SKILL.md              # Metadata (YAML) + usage guide
├── scripts/              # Execution engine (Python)
│   └── core_engine.py
└── reference.md          # Extended documentation (optional)
```

Skills use **progressive disclosure**: Claude loads SKILL.md first (~500-2000 tokens), then scripts/reference as needed.

## Hooks System

**Hooks** are executable scripts that automatically run in response to Claude Code lifecycle events, enabling automated workflows.

### Available Hooks

**PreCompact Hook**: `.claude/hooks/parallel-claude-after-compact.sh`
- **Event**: Triggered before context compact
- **Purpose**: Launch parallel Claude instance to continue work
- **Features**:
  - Saves context snapshot to `context/snapshots/`
  - Creates new iTerm window with Claude
  - Injects context summary to new instance
  - Uses lock mechanism to prevent duplicates
  - Integrates with 深渊凝视 skill for terminal control

**Workflow**:
```
Context → PreCompact → Save Snapshot → Launch Parallel Claude → Continue Original Compact
  |                                            |
  └─────────── Two Claude instances work in parallel ────────────┘
```

### Using Hooks

Hooks are automatically enabled when present in `.claude/hooks/` with executable permissions:

```bash
# Verify hook is enabled
ls -la .claude/hooks/

# View hook logs
tail -f .claude/logs/parallel-claude-after-compact.log

# Test hook manually
echo '{"context": "test", "reason": "debug"}' | \
  .claude/hooks/parallel-claude-after-compact.sh
```

**Benefits**:
- ✅ Zero context loss during compact
- ✅ Automatic task continuity
- ✅ Parallel processing capability
- ✅ No manual intervention needed

**Documentation**: See `.claude/hooks/README.md` for full guide

## PRP (Plan-Research-Plan) System

**Critical for complex features**: Before implementing non-trivial features, generate a PRP document.

### PRP Workflow

```bash
/prp <feature-description>
```

This command:
1. **Codebase Analysis**: Searches for similar patterns and reusable code
2. **External Research**: Fetches official docs, best practices, Stack Overflow solutions
3. **User Clarification**: Asks questions if requirements are ambiguous
4. **Deep Thinking**: Thinks through architecture before template-filling
5. **Blueprint Generation**: Creates executable implementation plan
6. **Validation Gates**: Defines automated quality checks (must be AI-executable)

**PRP Output**: `PRPs/{feature-name}.md`

**Quality Standard**: PRP must score ≥8/10 (confidence of one-shot implementation success)

### PRP Template Structure

```markdown
## 🔍 Context & References
- Documentation links with specific chapters
- Code examples from codebase (file:line)
- Technical gotchas and workarounds
- Implementation patterns to follow

## 🎯 Implementation Blueprint
- High-level pseudocode
- File structure (create/modify)
- Error handling strategy
- Task checklist (by completion order)

## ✅ Validation Gates
```bash
# Must be AI-executable, no manual steps
ruff check --fix && mypy . && pytest
```
```

**Why PRPs Matter**: AI agents executing features only have access to the PRP and training data. PRPs must contain ALL necessary context.

## Agent Coordination Patterns

### QQ-总指挥官 (Supreme Commander)

For **complex multi-agent coordination**, invoke the commander agent:

```python
Task(subagent_type="QQ-总指挥官",
     prompt="我需要为新开的火锅店做一个完整的开业筹备方案")
```

The commander:
1. **Scouts** the plugin system (Glob plugins/*/agents/*.md)
2. **Analyzes** requirements using first-principles thinking
3. **Generates** JSON battle plan with task dependencies
4. **Coordinates** execution across multiple business groups
5. **Integrates** outputs into final deliverables

**Output**: `output/[项目名]/QQ-总指挥官/作战指令-[项目名]-YYYYMMDD-HHMMSS.json`

### Direct Agent Invocation

For single-domain tasks, invoke agents directly:

```python
# Strategic analysis
Task(subagent_type="G1-经营分析优化师",
     prompt="分析本月门店经营数据")

# Creative design
Task(subagent_type="X3-平面设计师",
     prompt="设计新品海报")

# Intelligence gathering
Task(subagent_type="E2-Chrome网页采集",
     prompt="采集竞品网站数据")
```

## MCP Server Integration

The project integrates **7+ MCP servers** for external system access:

- **chrome-mcp**: Browser automation (20+ tools) - page navigation, element interaction, scraping
- **playwright-mcp**: Deep web crawling (30+ tools) - complex interactions, network capture
- **github-mcp**: GitHub operations (25+ tools) - repos, issues, PRs, code search
- **context7**: Real-time library docs (2 tools) - resolve library IDs, fetch latest docs
- **lark-mcp**: Feishu/Lark integration (15+ tools) - messages, multidimensional tables, docs
- **cos-mcp**: Tencent Cloud COS (10+ tools) - file management, image processing
- **supabase-mcp**: Supabase PostgreSQL - database operations, table management

**Tool Priority**: Prefer specialized tools over bash:
- File ops: `Read/Write/Edit` > `cat/echo`
- Search: `Glob/Grep` > `find/grep`
- Browser: `chrome-mcp/playwright-mcp` > manual scripting

## Key Conventions

### Code Quality Standards

- **Test Coverage**: New code must have ≥80% coverage
- **Validation Gates**: All PRPs must define automated validation
- **Error Handling**: Always include error handling in implementation blueprints
- **Type Safety**: Use mypy for Python, TypeScript for JS/TS

### File Organization

```
PRPs/                    # Plan-Research-Plan documents
├── templates/           # PRP templates
├── in-progress/         # Active PRPs
└── {feature}.md         # Completed PRPs

output/                  # Agent execution outputs
├── [项目名]/           # Grouped by project
│   ├── [agent-name]/   # Each agent has own directory
│   │   ├── plans/      # JSON execution configs
│   │   ├── results/    # Final outputs
│   │   ├── logs/       # Execution logs
│   │   └── metadata/   # Traceability data

reports/                 # Execution reports and analyses
learning/                # Knowledge accumulation (ASDW system)
trees/                   # Parallel execution workspaces
```

### Naming Conventions

**Agents**: `[字母][数字]-名称.md`
- Examples: `G1-经营分析优化师.md`, `X3-平面设计师.md`, `GG-战略组组长.md`

**Commands**: Short verbs or abbreviations
- Examples: `prp.md`, `test.md`, `github-pull.md`

**Skills**: kebab-case (lowercase + hyphens)
- Examples: `text-to-image/`, `excel-data-analyzer/`, `web-scraping/`

### Version Control

**Track**:
- ✅ `.claude/agents/`, `.claude/commands/`, `.claude/skills/`
- ✅ `PRPs/`, `scripts/`, `plugins/`
- ✅ `CLAUDE.md`, `README.md`

**Ignore**:
- ❌ `output/**/results/`, `output/**/logs/`, `output/**/metadata/`
- ❌ Individual `settings.json` (personal configs)
- ✅ `output/**/plans/` (track execution plans for traceability)

## Important Notes

### Don't Reinvent the Wheel

- **Before creating new agents**: Check if existing agents can handle the task
- **Before writing new code**: Search codebase for similar patterns (PRPs do this automatically)
- **Before implementing features**: Generate PRP first for complex tasks

### Progressive Disclosure Principle

Skills use progressive disclosure to optimize token usage:
1. **Level 1**: YAML frontmatter (~50 tokens) - for capability discovery
2. **Level 2**: SKILL.md core instructions (~500-2000 tokens) - usage guide
3. **Level 3**: reference.md (~1000-5000 tokens) - deep expertise
4. **Level 4**: scripts/ - executable code

Only load what's needed for the current task.

### Test-Driven Quality

**Never skip validation**. Use `/test` command which:
1. Runs linting, type checking, unit tests, coverage
2. **Iteratively fixes failures** until all pass
3. Updates TodoWrite task list in real-time
4. Provides comprehensive test report

**Principle**: Fix failing tests, don't disable them.

## Getting Started

1. **Understand the agent system**: Browse `plugins/[业务组]/agents/` to see what capabilities exist
2. **Use slash commands**: Start with `/context-aware` to get project overview
3. **Follow PRP workflow**: For new features, always `/prp` first
4. **Test rigorously**: Every change must pass `/test`
5. **Sync documentation**: After changes, run `/claude` to update this file

## Common Patterns

### Multi-Agent Workflow
```
1. Commander analyzes requirements → generates JSON battle plan
2. Intelligence group → gathers data
3. Strategy group → analyzes data, creates recommendations
4. Creative group → produces marketing materials
5. Commander → integrates all outputs
```

### Single-Agent Workflow
```
1. User invokes agent directly with Task()
2. Agent executes with domain expertise
3. Results saved to output/[项目名]/[agent-name]/
4. Metadata logged for traceability
```

### PRP-Driven Development
```
1. /prp <feature> → generates research-backed plan
2. Review PRP, ensure ≥8/10 score
3. Implement following PRP blueprint
4. /test → validate with automated gates
5. Iterate until all tests pass
```

---

**Note**: This is a living document. Run `/claude` after significant configuration changes to keep it synchronized with actual project state.
