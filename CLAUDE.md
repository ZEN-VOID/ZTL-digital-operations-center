
# ZTL Digital Intelligence Operations Center (ZTL数智化作战中心)

## 1. Project Overview

**ZTL Digital Intelligence Operations Center** is a comprehensive **Multi-Agent Orchestration Platform** designed for the digital transformation of the restaurant industry. It leverages **Claude Code** and **Sonnet 4.5** to coordinate over **70 specialized AI agents** across 6 business groups, handling everything from strategic planning and creative design to construction management and software development.

### Core Technologies

* **AI Core**: Claude Code, Sonnet 4.5, MCP (Model Context Protocol).
* **Frontend**: Next.js 16+, React 19, TypeScript, Tailwind CSS, Radix UI.
* **Backend/Scripting**: Python 3.12+, Node.js.
* **Integration**: Supabase, Tencent COS, Feishu (Lark), GitHub.

### Architectural Principles

The project follows a **Three-Layer Architecture**:

1. **Knowledge Layer**: Agents (Roles/Expertise) + Skills (Capabilities/Engines).
2. **Orchestration Layer**: Claude's runtime reasoning and dynamic capability composition.
3. **Execution Layer**: Tools (Bash, Python, MCP) and standardized Output generation.

---

## 2. Directory Structure

### Core Configuration (`.claude/`)

The "Brain" of the system.

* **`agents/`**: Definitions for 70+ agents (Markdown).
* **`commands/`**: Custom slash commands (e.g., `/prp`, `/context-aware`).
* **`skills/`**: Reusable capabilities (e.g., `OFFICE自动化`, `ITERM多终端调用`).
* **`hooks/`**: Lifecycle automation (e.g., `parallel-claude-after-compact.sh`).

### Business Plugins (`plugins/`)

Organized by business function:

* **`战略组` (Strategy)**: Business planning, analysis (Agents: T-series).
* **`创意组` (Creative)**: Design, AIGC, video/audio (Agents: X-series).
* **`情报组` (Intelligence)**: Research, scraping (Agents: E-series).
* **`筹建组` (Construction)**: BIM, floor plans (Agents: Z-series).
* **`开发组` (Development)**: Software engineering (Agents: F-series).
* **`美团组` (Meituan Ops)**: Platform operations (Agents: R-series).

### Application Source (`project/`)

* **`web-ui/`**: The visual dashboard for the platform.
  * **Stack**: Next.js 16 (App Router), TypeScript, Tailwind.
  * **Key Scripts**: `npm run dev`, `npm run build`, `npm run parse:agents`.
  * **Path**: `project/web-ui/`.

### Workflow Directories

* **`PRPs/`**: Plan-Research-Plan documents for feature planning.
* **`output/`**: Standardized artifact storage: `output/[ProjectName]/[AgentName]/`.
* **`reports/`**: System and execution reports.
* **`learning/`**: Knowledge base for system self-improvement.

---

## 3. Key Workflows & Commands

### Feature Planning (PRP System)

**Command**: `/prp <feature-description>`

* Generates a comprehensive **Plan-Research-Plan** document in `PRPs/`.
* **Required** for any complex feature implementation.
* Includes validation gates and implementation blueprints.

### Project Context

**Command**: `/context-aware`

* Performs a deep 8-dimensional scan of the project (Agents, Commands, Hooks, Skills, etc.).
* Use this to "refresh" your understanding of the system state.

### Agent Execution Modes

1. **Three-Layer Architecture** (Default): Specification -> Plan (JSON) -> Execution. Used by Strategy, Creative, etc.
2. **Direct Execution**: Specification -> Execution. **Exclusive to Development Group (F-series)** for fast iteration on the codebase.
3. **Hybrid Coordination**: Orchestrated by `QQ-总指挥官` for multi-group initiatives.

### Web UI Development

Working directory: `project/web-ui/`

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Update agent data for UI
npm run parse:agents
```

---

## 4. Development Conventions

### Coding Standards

* **Frontend**: Strict TypeScript usage. Use `lucide-react` for icons, `shadcn/ui` (via Radix) for components.
* **Styling**: Tailwind CSS with `tailwind-merge` and `clsx` for class management.
* **State**: React Hooks.

### Output Management

* **Agents**: Must output to `output/[ProjectName]/[AgentName]/` with subfolders `plans/`, `results/`, `logs/`.
* **Developers**: Direct code modifications in `project/web-ui/` (no `output` folder needed for code changes).

### Testing

* **Command**: `/test`
* Runs the full test suite (linting, type-checking, unit tests) and iteratively fixes issues.

---

## 5. Quick Start for Agents

1. **Understand the Task**: Is it a code change (Dev Group) or a business output (Strategy/Creative)?
2. **Select the Mode**: Direct Execution for code, Three-Layer for business artifacts.
3. **Plan**: Use `/prp` if the task is complex.
4. **Execute**: Use the appropriate tools (MCP, Python scripts, or File Ops).
5. **Verify**: Run `/test` or validate the `output/` artifacts.
