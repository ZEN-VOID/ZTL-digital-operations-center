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

## Agent Execution Modes

**Critical**: Not all agents follow the same execution pattern. The project uses **multiple execution modes** based on task characteristics.

### Mode 1: Three-Layer Architecture (Default for AIGC, Research, Strategy)

**Pattern**: Specification Layer → Plan Layer → Execution Layer

**Applies to**:
- **战略组** (Strategy): Strategic analysis, business planning, operations optimization
- **创意组** (Creative): AIGC generation, batch design tasks, video production
- **情报组** (Intelligence): Data collection, web scraping, competitive research
- **筹建组** (Construction): BIM modeling, floor plans, space design
- **美团组** (Meituan Ops): Batch operations, reporting, campaign management
- **供应组** (Supply Chain): Inventory analysis, procurement planning
- **行政组** (Admin): Document generation, financial reports

**Execution Flow**:
```
1. Specification (.md) → Defines business logic and quality standards
2. Plan (JSON/YAML) → Generates parameterized execution config
3. Execution (Scripts) → Runs tasks and saves to output/[项目名]/[agent-name]/
```

**Output Structure**:
```
output/[项目名]/[agent-name]/
├── plans/      # JSON execution configs
├── results/    # Final outputs
├── logs/       # Execution logs
└── metadata/   # Traceability data
```

### Mode 2: Direct Execution (Development Group Only)

**⭐ Special Rule for Development Group**: The following agents **skip the plan layer** and execute directly:

**Affected Agents** (12 total):
- F1-前端开发 (Frontend Developer)
- F2-UI设计师 (UI Designer)
- F3-全栈开发 (Full-Stack Developer)
- F5-后端架构师 (Backend Architect)
- F6-数据库架构师 (Database Architect)
- F8-云架构师 (Cloud Architect)
- F10-Python专家 (Python Expert)
- F11-TypeScript专家 (TypeScript Expert)
- F12-JavaScript专家 (JavaScript Expert)
- F14-测试工程师 (Test Engineer)
- F15-性能优化专家 (Performance Optimizer)
- F16-调试专家 (Debugging Expert)

**Pattern**: Specification Layer → Execution Layer (No Plan)

**Why Direct Execution?**
- Fast iteration cycles required for development tasks
- Real-time feedback more valuable than batch processing
- Code changes need immediate testing and validation
- Plan layer adds unnecessary overhead for one-shot operations

**Default Working Path**: `project/web-ui/`

**Execution Flow**:
```
1. Specification (.md) → Defines role and workflow
2. Direct Execution → Immediately uses:
   - Tools: Read/Write/Edit for file operations
   - MCP: chrome-mcp, github-mcp, playwright-mcp
   - Skills: Relevant development skills
   - Results: Directly modify files in project/web-ui/
```

**No Output Directory**: Development agents don't create output/[项目名] structure. They work directly on the codebase.

**Example Workflows**:

```python
# F1-前端开发: Modify a React component
Task(subagent_type="F1-前端开发",
     prompt="在project/web-ui/src/components/Button.tsx中添加loading状态")
# → Directly edits the file, no plan JSON

# F14-测试工程师: Run tests
Task(subagent_type="F14-测试工程师",
     prompt="在project/web-ui/运行所有单元测试")
# → Directly runs pytest, reports results

# F6-数据库架构师: Design schema
Task(subagent_type="F6-数据库架构师",
     prompt="在project/web-ui/设计用户表schema")
# → Directly creates migration files
```

### Mode 3: Hybrid Coordination (QQ-总指挥官)

**Pattern**: Strategic coordination using three-layer + Direct execution for implementation

**When to Use**:
- Complex multi-group projects (e.g., restaurant launch campaign)
- Strategic phase requires quality gates (three-layer)
- Implementation phase requires speed (direct execution)

**Coordination Flow**:
```
1. QQ-总指挥官 → Creates battle plan (JSON)
2. 战略组/情报组 → Uses three-layer for analysis
3. 开发组 → Uses direct execution for implementation
4. 创意组 → Uses three-layer for batch design
5. QQ-总指挥官 → Integrates all outputs
```

### Mode Selection Decision Tree

```
What kind of task?
│
├─ Batch processing / Quality tracking needed?
│  └─ YES → Three-Layer Architecture
│     Examples: Generate 100 posters, analyze 50 stores
│
├─ Fast iteration / Real-time feedback needed?
│  └─ YES → Direct Execution
│     Examples: Fix bug, update UI, optimize query
│
└─ Multi-group coordination?
   └─ YES → Hybrid Coordination
      Examples: Restaurant launch, platform migration
```

### Best Practices

**For Development Group Agents**:
- ✅ Work directly in `project/web-ui/`
- ✅ Use Read/Write/Edit for file operations
- ✅ Leverage MCP servers for browser/API testing
- ✅ Run tests immediately after changes
- ❌ Don't create plan JSONs
- ❌ Don't create output/[项目名] directories

**For Other Groups**:
- ✅ Follow three-layer architecture
- ✅ Generate plan JSONs for traceability
- ✅ Use output/[项目名]/[agent-name]/ structure
- ✅ Include metadata for quality tracking

**Mixed Scenarios**:
- Development prototyping → Direct execution
- Production batch deployment → Upgrade to three-layer
- One-time design → Direct execution
- Campaign with 100+ assets → Three-layer architecture

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
