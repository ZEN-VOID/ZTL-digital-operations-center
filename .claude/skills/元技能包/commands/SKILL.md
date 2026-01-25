---
name: commands
description: Design, create, and optimize Claude Code slash commands based on official specifications and best practices. Use when building reusable command workflows or optimizing command configurations.
---

# Claude Code Slash Command Creation

Create efficient, reusable slash commands that transform frequent prompts into one-command workflows with parameter support, Bash execution, and file references.

## What Are Slash Commands?

Slash commands are a powerful Claude Code feature that allows you to:

- ✅ Define frequently used prompts as reusable Markdown files
- ✅ Trigger complex workflows through short commands
- ✅ Support parameterization, Bash execution, and file references
- ✅ Share commands at project or user level

**Key Benefits**:
- **Efficiency Boost**: Transform repetitive prompts into one-command actions
- **Team Collaboration**: Project-level commands shared with codebase
- **Flexible Extension**: Support dynamic parameters, Bash integration, file references
- **Auto-Discovery**: Intelligent invocation via SlashCommand tool

## When to Use This Skill

Use this skill to:

- Create new slash commands for frequent workflows
- Optimize existing command configurations
- Understand command architecture and parameter design
- Configure tool permissions and Bash execution
- Integrate commands with SlashCommand tool for auto-discovery

## Command Types and Scope

| Type | Location | Scope | Identifier |
|------|----------|-------|------------|
| **Project Command** | `.claude/commands/` | Current project, team-shared | (project) |
| **Personal Command** | `~/.claude/commands/` | All projects, personal use | (user) |
| **Plugin Command** | Plugin's `commands/` directory | Auto-available after plugin install | (plugin) |
| **MCP Command** | Dynamically exposed by MCP server | Available when server connected | (mcp) |

**Naming Conflict Rules**:
- No same-name conflicts between user-level and project-level commands
- Multiple commands can have same base filename if in different subdirectories

## Quick Start

### 1. Analyze Requirements

Answer these core questions:

```yaml
Command Goal: What problem does this command solve?
Usage Frequency: One-time task or frequent operation?
Scope: Project-level (team-shared) or personal-level?
Complexity: Simple prompt or complex workflow?
```

### 2. Design Parameters

Choose parameter type based on needs:

```yaml
No Parameters:
  - Use Case: Fixed prompt, no dynamic input
  - Example: /review → "Review this code for errors"

$ARGUMENTS (All arguments):
  - Use Case: Arguments passed as a whole
  - Example: /fix-issue $ARGUMENTS → "Fix issue #123 high-priority"

Positional Parameters ($1, $2, ...):
  - Use Case: Structured parameters with clear roles
  - Example: /review-pr $1 $2 $3 → "Review PR #456, priority high, assign to alice"

Design Template:
  argument-hint: [clear parameter format]
  Examples:
    - "[message]" - Single optional parameter
    - "[pr-number] [priority] [assignee]" - Multiple positional parameters
    - "add [tagId] | remove [tagId] | list" - Multiple subcommand pattern
```

### 3. Configure Tool Permissions

Follow minimum privilege principle:

```yaml
Tool Configuration Principles:
  - Minimum Privilege: Only grant necessary tools
  - Explicit Scope: Specify allowed bash commands
  - Security First: Avoid dangerous operations

Common Tool Configuration Patterns:

1. File Operations:
   allowed-tools: Read, Write, Edit

2. Git Operations:
   allowed-tools: Bash(git status:*), Bash(git add:*), Bash(git commit:*)

3. Code Analysis:
   allowed-tools: Read, Grep, Bash(eslint:*), Bash(npm test:*)

4. Inherit All Tools:
   allowed-tools: # Omit field to inherit from conversation
```

### 4. Build Command Content

Structure based on analysis:

```markdown
---
allowed-tools: [tool list]
argument-hint: [parameter hint]
description: [one-sentence description]
model: [optional: specify model]
---

# [Command Title]

## Context (Optional)
[Use Bash execution to get dynamic context]
- Current state: !`command`
- Related info: !`command`

## Your Task
[Clear task description]

## Requirements (Optional)
- [Specific requirement 1]
- [Specific requirement 2]

## Examples (Optional)
[Provide examples to guide Claude]
```

### 5. Create and Activate

#### Determine Storage Path

```yaml
Project-level command (recommended for team sharing):
  Path: .claude/commands/[name].md
  Example: .claude/commands/commit.md
  Usage: /commit
  Identifier: (project)

Personal-level command (personal use):
  Path: ~/.claude/commands/[name].md
  Example: ~/.claude/commands/my-review.md
  Usage: /my-review
  Identifier: (user)

Namespace organization:
  Path: .claude/commands/[subdirectory]/[name].md
  Example: .claude/commands/git/commit.md
  Usage: /commit
  Identifier: (project:git)
```

#### Create File

**Method 1: Use Write tool (Recommended)**

```bash
# Create project command
Write tool create: .claude/commands/commit.md
Content: [Complete command file content]

# Create personal command
Write tool create: ~/.claude/commands/my-commit.md
Content: [Complete command file content]
```

**Method 2: Use Bash command**

```bash
# Create project command
mkdir -p .claude/commands
cat > .claude/commands/commit.md << 'EOF'
---
description: Create git commit
---
Create a descriptive git commit message
EOF
```

## Core Features

### 1. Namespaces

Organize commands through subdirectories for logical grouping:

```yaml
Namespace Rules:
  - Subdirectories for organization, don't affect command name itself
  - Namespace path shown in description

Example:
  .claude/commands/frontend/component.md
  → Command: /component
  → Description: "(project:frontend)"

  ~/.claude/commands/component.md
  → Command: /component
  → Description: "(user)"
```

### 2. Parameter Support

#### All Arguments ($ARGUMENTS)

Capture all arguments passed to command:

```bash
# Command definition
echo 'Fix issue #$ARGUMENTS per our coding standards' > .claude/commands/fix-issue.md

# Usage
> /fix-issue 123 high-priority
# $ARGUMENTS → "123 high-priority"
```

#### Positional Parameters ($1, $2, ...)

Access specific arguments individually (like shell scripts):

```bash
# Command definition
echo 'Review PR #$1, priority $2, assign to $3' > .claude/commands/review-pr.md

# Usage
> /review-pr 456 high alice
# $1 → "456", $2 → "high", $3 → "alice"
```

**Use Cases**:
- ✅ Need to access arguments separately in different parts of command
- ✅ Provide default values for missing parameters
- ✅ Build more structured commands with specific parameter roles

### 3. Bash Command Execution

Use `!` prefix to execute bash commands before command runs, with output included in context:

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create git commit
---

## Context
- Current git status: !`git status`
- Current git diff: !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your Task
Based on the above changes, create a git commit.
```

**Note**:
- Must include Bash tool in `allowed-tools`
- Can specify specific allowed bash commands

### 4. File References

Use `@` prefix to include file contents in commands:

```markdown
# Reference specific file
Review the implementation in @src/utils/helpers.js

# Reference multiple files
Compare @src/old-version.js with @src/new-version.js
```

### 5. Extended Thinking Mode

Commands can trigger extended thinking mode by including extended thinking keywords.

## Front Matter Configuration

Command files support YAML front matter for metadata:

```yaml
---
allowed-tools: Tool list (inherit from conversation)
argument-hint: Argument hint string (none)
description: Brief command description (uses first line of prompt)
model: Specific model string (inherit from conversation)
disable-model-invocation: Prevent SlashCommand tool invocation (false)
---
```

### Configuration Fields

| Field | Purpose | Default | Example |
|-------|---------|---------|---------|
| `allowed-tools` | Tools command can use | Inherit from conversation | `Bash(git *), Read, Write` |
| `argument-hint` | Parameter hint (shown in auto-complete) | None | `[message]` or `add [id] \| remove [id]` |
| `description` | Brief command description (Important!) | First line of prompt | `Create git commit` |
| `model` | Specify model | Inherit from conversation | `claude-3-5-haiku-20241022` |
| `disable-model-invocation` | Disable tool invocation | `false` | `true` |

**Key Tips**:
- ✅ `description` field crucial for SlashCommand tool auto-discovery
- ✅ `argument-hint` improves UX, shown in auto-complete
- ✅ `allowed-tools` implements principle of least privilege

## Complete Examples

### Example 1: Simple Code Review Command

**Requirements Analysis**:
```yaml
Goal: Quick trigger code review
Frequency: High frequency use
Scope: Project-level (team-shared)
Complexity: Simple prompt
Parameters: No parameters needed
```

**Command File**:
```markdown
---
description: Review code for errors, performance, and style issues
---

# Code Review

Review this code, focusing on:
- Potential errors and bugs
- Performance issues and optimization opportunities
- Code style and best practice violations
- Security vulnerabilities

Provide specific, actionable improvement suggestions.
```

**Storage Path**: `.claude/commands/review.md`
**Usage**: `/review`

---

### Example 2: PR Review Command with Parameters

**Requirements Analysis**:
```yaml
Goal: Review GitHub Pull Request
Frequency: Daily multiple times
Scope: Project-level
Complexity: Medium
Parameters: PR number, priority, assignee
```

**Command File**:
```markdown
---
argument-hint: [pr-number] [priority] [assignee]
description: Review GitHub Pull Request
allowed-tools: Read, Grep, Bash(gh:*)
---

# Pull Request Review

Review PR #$1, priority $2, assign to $3.

## Review Focus
1. Code quality and style
2. Security and performance
3. Test coverage
4. Documentation completeness

## Output Format
Provide structured review report including:
- Overall assessment
- Issues found (by severity)
- Improvement suggestions
- Final recommendation (approve/request changes/needs discussion)
```

**Storage Path**: `.claude/commands/review-pr.md`
**Usage**: `/review-pr 456 high alice`

---

### Example 3: Git Commit Command (with Bash Execution)

**Requirements Analysis**:
```yaml
Goal: Auto-create descriptive git commit
Frequency: Very high frequency
Scope: Project-level
Complexity: High (needs git context)
Parameters: Optional commit message
```

**Command File**:
```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git diff:*), Bash(git log:*), Bash(git branch:*)
argument-hint: [message]
description: Create git commit
---

# Git Commit

## Current Context
- Git status: !`git status`
- Staged and unstaged changes: !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent 10 commits: !`git log --oneline -10`

## Your Task
Based on the above changes, create a clear, descriptive git commit message.

## Requirements
1. Follow Conventional Commits specification (feat/fix/docs/style/refactor/test/chore)
2. First line no more than 50 characters (title)
3. Add detailed description if necessary (blank line after title)
4. Explain "why" not "what" (code already explains what)

## Commit Message Template
```
<type>(<scope>): <subject>

<body>

<footer>
```

$ARGUMENTS
```

**Storage Path**: `.claude/commands/commit.md`
**Usage**:
- `/commit` - Auto-generate
- `/commit "feat: add user authentication"` - Specify message

---

### Example 4: File Comparison Command (with File References)

**Requirements Analysis**:
```yaml
Goal: Compare two file differences
Frequency: Medium frequency
Scope: Personal-level
Complexity: Simple
Parameters: Two file paths (via @ references)
```

**Command File**:
```markdown
---
description: Compare two file differences
argument-hint: @file1 @file2
---

# File Comparison

Analyze differences between the following two files:

**File 1**: $1
**File 2**: $2

## Analysis Focus
1. Structural differences
2. Logical differences
3. Performance impact
4. Potential issues

Provide clear comparison summary and recommendations.
```

**Storage Path**: `~/.claude/commands/diff.md`
**Usage**: `/diff @src/old.js @src/new.js`

## SlashCommand Tool Integration

### What is SlashCommand Tool?

SlashCommand tool allows Claude to **programmatically** execute custom slash commands during conversation. This enables Claude to invoke commands on your behalf when appropriate.

### Enable Auto-Discovery

To let Claude auto-discover and invoke commands:

1. **Fill description field** (Required)
```yaml
---
description: Create git commit  # ← Required!
---
```

2. **Reference command in CLAUDE.md or prompt**
```markdown
# CLAUDE.md
Run /write-unit-test when about to start writing tests.
Run /commit to create commit when code changes complete.
```

### Character Budget Limit

SlashCommand tool includes character budget (default 15,000 characters) to limit size of command descriptions shown to Claude.

**Management Strategies**:
- Use `/context` to monitor token usage
- Keep description concise (one sentence)
- Consider disabling rarely used commands

### Disable Specific Commands

```markdown
---
description: Rarely used command
disable-model-invocation: true  # ← Disable tool invocation
---
```

### Permission Rules

```bash
# Exact match
SlashCommand:/commit  # Only allow /commit without parameters

# Prefix match
SlashCommand:/review-pr:*  # Allow /review-pr with any parameters
```

## Commands vs Skills: Selection Guide

According to official documentation, slash commands and agent skills serve different purposes:

### Use Slash Commands When

✅ **Quick, frequently used prompts**:
- Simple prompt snippets you use often
- Quick reminders or templates
- Frequently used instructions that fit in one file

**Examples**:
- `/review` → "Review this code for errors and suggest improvements"
- `/explain` → "Explain this code in simple terms"
- `/optimize` → "Analyze this code for performance issues"

### Use Skills When

✅ **Comprehensive capabilities with structure**:
- Complex workflows with multiple steps
- Capabilities requiring scripts or utilities
- Knowledge organized across multiple files
- Team workflows you want to standardize

**Examples**:
- PDF processing skill with form-filling scripts and validation
- Data analysis skill with reference docs for different data types
- Documentation skill with style guides and templates

### Key Differences

| Aspect | Slash Commands | Agent Skills |
|--------|----------------|--------------|
| **Complexity** | Simple prompts | Complex capabilities |
| **Structure** | Single .md file | Directory+SKILL.md+resources |
| **Discovery** | Explicit invocation (/command) | Auto (context-based) |
| **Files** | Only one file | Multiple files, scripts, templates |
| **Scope** | Project or personal | Project or personal |
| **Sharing** | Via git | Via git |

### Decision Flowchart

```yaml
Does your need fit in a single file?
  Yes → Use slash command
  No ↓

Does it need complex multi-step workflow?
  Yes → Use skill
  No ↓

Does it need scripts, validation, or external tools?
  Yes → Use skill
  No ↓

Should Claude auto-discover this capability?
  Yes → Use skill
  No → Use slash command (explicit invocation)
```

## Quality Checklist

Verify quality after creating command using this checklist:

```yaml
□ Requirements Clarity
  - [ ] Command goal clear and specific
  - [ ] Use cases clearly defined
  - [ ] Target users and frequency confirmed

□ File Specifications
  - [ ] YAML front matter format correct
  - [ ] description field exists and clear (SlashCommand tool required)
  - [ ] argument-hint consistent with actual parameters
  - [ ] Filename follows naming conventions (lowercase, hyphens)
  - [ ] Stored in correct path

□ Parameter Design
  - [ ] Parameter type selection reasonable ($ARGUMENTS vs $1,$2,...)
  - [ ] argument-hint clearly describes parameter format
  - [ ] Parameter placeholders correctly used

□ Tool Permissions
  - [ ] allowed-tools list minimized
  - [ ] Bash commands explicitly specify allowed scope
  - [ ] No unnecessary permissions granted
  - [ ] Dangerous operations have safeguards

□ Functionality Completeness
  - [ ] Bash execution (if used) syntax correct
  - [ ] File references (if used) paths correct
  - [ ] Command content clear and structured
  - [ ] Provides sufficient context and guidance

□ Testing Verification
  - [ ] Verify command appears via /help
  - [ ] Test basic invocation works normally
  - [ ] Test parameter replacement correct
  - [ ] Test Bash execution normal (if applicable)
  - [ ] Test file references normal (if applicable)
  - [ ] Verify SlashCommand tool can discover (if needed)

□ Documentation and Maintenance
  - [ ] Command purpose clearly stated in description
  - [ ] Complex commands include inline comments
  - [ ] Project commands committed to version control
  - [ ] Team members aware of new command (if project-level)
```

## Best Practices

1. **Start Simple**: Create basic command first, gradually add complexity
2. **Use Claude Generation**: Let Claude generate initial command, then iterate
3. **Stay Focused**: Each command does one thing and does it well
4. **Detailed Description**: Clearly state command purpose in description (SlashCommand tool relies on this field)
5. **Minimum Privilege**: Only grant necessary tools and bash commands
6. **Version Control**: Check project commands into git, share with team
7. **Continuous Optimization**: Continuously improve commands based on usage feedback
8. **Documentation**: Add comments and usage examples for complex commands

## Reference Resources

### Official Documentation

- **[Claude Code Slash Commands Official Docs](https://docs.claude.com/zh-CN/docs/claude-code/slash-commands)** ⭐ Must-read
- [Claude Code Plugin Development](https://docs.claude.com/docs/claude-code/plugins)
- [Claude Code Skills Development](https://docs.claude.com/docs/claude-code/skills)

---

**Version**: 1.0.0
**Last Updated**: 2025-10-19
**Compatibility**: Claude Code v1.0.124+
**Based On**: Claude Code Official Documentation (2025-10-19)
