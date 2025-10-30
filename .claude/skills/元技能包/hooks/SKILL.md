---
name: hooks
description: Design, create, and debug Claude Code hooks for event-driven automation. Covers 8 lifecycle events, script development, testing strategies, and real-world best practices. Use when building hooks or troubleshooting hook systems.
---

# Claude Code Hooks Creation

Build high-performance, event-driven hooks that automate workflows through Claude Code's lifecycle events with deterministic behavior independent of AI decisions.

## What Are Hooks?

Hooks are mechanisms in Claude Code for executing custom logic when specific events occur. Each hook:

- ✅ Triggers automatically at specific **lifecycle events**
- ✅ Receives **JSON-formatted input** containing event context
- ✅ Can **validate, modify, or block** operations
- ✅ Supports **shell commands** or **executable scripts**

**Key Advantages**:
1. **Deterministic Behavior**: Provides deterministic automation not dependent on AI decisions
2. **Event-Driven**: Based on Claude Code lifecycle events for loose coupling
3. **Flexible Control**: Can intercept operations, enhance inputs, or log behavior

## When to Use This Skill

Use this skill to:

- Create event-driven automation for Claude Code workflows
- Block dangerous operations before execution
- Auto-format code after file edits
- Enhance user prompts with context
- Log agent execution for audit trails
- Build complex multi-hook automation systems
- Debug hook execution issues

## Hook Event Types

Claude Code supports 8 lifecycle events:

### 1. PreToolUse (Before Tool Call)

```yaml
Trigger Timing: Before tool execution
Input Data:
  - tool_name: Tool name (e.g., "Edit", "Bash")
  - tool_input: Tool parameter object
Capability: Can return {"action": "block"} to prevent tool execution
Typical Scenarios:
  - Block dangerous bash commands (rm -rf *, delete sensitive files)
  - Validate file path legality
  - Check required environment variables
  - Implement security policies and permission control
```

### 2. PostToolUse (After Tool Call)

```yaml
Trigger Timing: After successful tool execution
Input Data:
  - tool_name: Tool name
  - tool_input: Tool parameters
  - tool_output: Tool execution result
Capability: Cannot block (operation already completed), but can trigger follow-up actions
Typical Scenarios:
  - Auto-format code after editing
  - Log file edit history
  - Trigger test or build processes
  - Update documentation or metadata
```

### 3. UserPromptSubmit (User Submits Prompt)

```yaml
Trigger Timing: When user submits prompt
Input Data:
  - prompt: User's complete prompt
  - session_id: Session ID
  - cwd: Current working directory
Capability: Can display additional information or reminders to user
Typical Scenarios:
  - Remind user to use specific agents or tools
  - Detect keywords and inject relevant context
  - Log user intent history
  - Provide intelligent suggestions
```

### 4. SubagentStop (Subagent Completes)

```yaml
Trigger Timing: When subagent completes task
Input Data:
  - subagent_name: Subagent name
  - subagent_output: Subagent output
Capability: Process subagent results, trigger follow-up workflows
Typical Scenarios:
  - Validate subagent output quality
  - Trigger dependent follow-up tasks
  - Log agent execution statistics
  - Implement inter-agent collaboration
```

### 5. Stop (Main Agent Completes)

```yaml
Trigger Timing: When main agent completes response
Input Data:
  - response: Main agent's complete response
  - session_id: Session ID
Capability: Session-level post-processing
Typical Scenarios:
  - Generate session summary
  - Clean up temporary files
  - Update statistics
  - Trigger CI/CD processes
```

### 6. Notification (System Notification)

```yaml
Trigger Timing: When system sends notification
Input Data:
  - notification_type: Notification type
  - notification_message: Notification message
Capability: Can modify notification content or forward
Typical Scenarios:
  - Forward important notifications to external systems (Slack, email)
  - Filter noise notifications
  - Add notification context
  - Implement notification routing
```

### 7. PreCompact (Before Context Compression)

```yaml
Trigger Timing: Before context compression
Input Data:
  - context_to_compact: Context about to be compressed
  - reason: Compression reason
Capability: Protect important information, log compressed content
Typical Scenarios:
  - Extract and save key information
  - Log complete context snapshot
  - Update external knowledge base
  - Implement context persistence
```

### 8. SessionStart (Session Starts)

```yaml
Trigger Timing: When session initializes
Input Data:
  - session_id: New session ID
  - cwd: Working directory
Capability: Environment check, initialize configuration
Typical Scenarios:
  - Check required tools and dependencies
  - Load project-specific configuration
  - Set environment variables
  - Display welcome message
```

## Quick Start

### 1. Analyze Requirements

Answer these core questions:

```yaml
Automation Goal: What operation to automate?
Trigger Timing: When to execute? (Choose appropriate event type)
Input Data: What context information needed?
Expected Output: What results or side effects?

Event Type Selection:
  - Need to block operation → PreToolUse
  - Post-operation processing → PostToolUse
  - Prompt enhancement → UserPromptSubmit
  - Agent collaboration → SubagentStop
  - Session-level processing → Stop/SessionStart
  - Context management → PreCompact
  - Notification routing → Notification
```

### 2. Develop Script

#### Standard Script Template

```bash
#!/bin/bash
# Hook Script Template - Following Best Practices

# ========== Configuration ==========
SCRIPT_NAME="your-hook-name"
LOG_DIR=".claude/logs"
LOG_FILE="${LOG_DIR}/${SCRIPT_NAME}.log"
DEBUG=${DEBUG:-false}

# Create log directory
mkdir -p "$LOG_DIR"

# ========== Function Definitions ==========

# Logging function
log() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $*" >> "$LOG_FILE"
    if [[ "$DEBUG" == "true" ]]; then
        echo "$*" >&2
    fi
}

# JSON field extraction (cross-platform compatible, no jq dependency)
extract_field() {
    local input="$1"
    local field="$2"
    echo "$input" | tr -d '\n' | \
        grep -o "\"${field}\"[[:space:]]*:[[:space:]]*\"[^\"]*\"" | \
        sed 's/.*"\([^"]*\)"$/\1/'
}

# Error handling function
handle_error() {
    local error_msg="$1"
    log "ERROR: $error_msg"
    echo "{\"action\": \"block\", \"message\": \"$error_msg\"}"
    exit 1
}

# ========== Main Logic ==========
main() {
    # Read JSON input from stdin
    input=$(cat)

    # Log original input (for debugging)
    log "Hook triggered"
    log "Input length: ${#input} characters"

    # Extract necessary fields
    tool_name=$(extract_field "$input" "tool_name")

    # Validate input
    if [[ -z "$tool_name" ]]; then
        log "WARNING: No tool_name found in input"
    fi

    # ===== Core Business Logic =====
    # Implement your hook functionality here

    # Example: Check for dangerous operations
    # if [[ "$tool_name" == "Bash" ]]; then
    #     command=$(extract_field "$input" "command")
    #     if [[ "$command" =~ rm.*-rf ]]; then
    #         handle_error "Dangerous rm -rf command blocked"
    #     fi
    # fi

    # ===== Return Result =====
    # Success: Return empty JSON
    echo "{}"
    log "Hook executed successfully"
}

# Execute main function
main
```

#### Cross-Platform Compatibility

```yaml
Windows Git Bash Notes:
  - jq usually unavailable, use pure bash JSON parsing
  - Use forward slashes / or double backslashes \\ for paths
  - Avoid complex pipes and subshells
  - Test scripts in Windows environment

JSON Parsing Strategy:
  - Preferred: Use jq (if available)
  - Fallback: tr + grep + sed combination
  - Handle multi-line JSON: Use tr -d '\n' to remove newlines first
  - Handle spaces: Use [[:space:]]* regex
  - Extract example:
    extract_field "$input" "field_name"

Path Handling:
  - Use absolute paths to avoid ambiguity
  - Check file existence: [[ -f "$path" ]]
  - Create directories: mkdir -p "$dir"
  - Log paths: Relative to project root

Error Handling:
  - Use set -e to auto-exit on error
  - Or manually check each command's exit code: $?
  - Use trap to catch exceptions
  - Comprehensive logging
```

### 3. Configure Integration

#### Configuration File Syntax

```json
{
  "hooks": {
    "EventType": [
      {
        "matcher": "tool-name-regex",
        "hooks": [
          {
            "type": "command",
            "command": "hook-script-path-or-inline-command",
            "description": "optional description"
          }
        ]
      }
    ]
  }
}
```

#### Complete Configuration Example

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/format-after-edit.sh",
            "description": "Auto-format code after edit"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/block-dangerous-commands.sh",
            "description": "Block dangerous bash commands"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/prompt-enhancement.sh",
            "description": "Intelligent prompt enhancement"
          }
        ]
      }
    ]
  }
}
```

### 4. Test and Debug

#### Debug Mode

```bash
# Enable debug mode
claude --debug

# Debug mode displays:
# - Which hooks were triggered
# - Hook input data
# - Hook output results
# - Execution time and error messages
```

#### Manual Testing

```bash
# Prepare test input
cat > test_input.json <<'EOF'
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/path/to/file.py",
    "old_string": "old",
    "new_string": "new"
  }
}
EOF

# Test hook script
cat test_input.json | .claude/hooks/your-hook.sh

# Check output and exit code
echo "Exit code: $?"

# Validate JSON format
cat test_input.json | .claude/hooks/your-hook.sh | jq .
```

#### Log Analysis

```bash
# View hook logs
tail -f .claude/logs/your-hook.log

# Analyze log patterns
grep "ERROR" .claude/logs/*.log
grep "executed successfully" .claude/logs/*.log | wc -l

# Clean old logs (keep 7 days)
find .claude/logs -name "*.log" -mtime +7 -delete
```

### 5. Deploy

#### Deployment Checklist

```yaml
Pre-deployment checks:
  - [ ] All scripts tested and passing
  - [ ] settings.json configured correctly
  - [ ] Log directory created: .claude/logs/
  - [ ] Scripts have execute permission: chmod +x .claude/hooks/*.sh
  - [ ] Line endings correct: LF not CRLF
  - [ ] Documentation updated (README or CLAUDE.md)
  - [ ] Team members notified (if team project)

File Organization:
  .claude/
    ├── settings.json              # Hooks config (project-level, in Git)
    ├── settings.local.json        # Hooks config (local-level, personal)
    ├── hooks/
    │   ├── README.md              # Hooks usage documentation
    │   ├── *.sh                   # Hook scripts
    │   └── templates/             # Script templates
    └── logs/
        ├── .gitkeep
        └── *.log                  # Log files

Version Control:
  Include in Git:
    - settings.json (if team sharing needed)
    - hooks/*.sh
    - hooks/README.md
    - hooks/templates/

  Add to .gitignore:
    - settings.local.json
    - logs/*.log
    - hooks/**/*.backup
```

## Hook Configuration Layers

Following three-tier architecture consistent with Claude Code settings system:

| Layer | Location | Scope | Priority |
|-------|----------|-------|----------|
| **Project (Shared)** | `.claude/settings.json` | Current project (team) | Highest ⭐⭐⭐ |
| **Project (Personal)** | `.claude/settings.local.json` | Current project (personal) | Medium ⭐⭐ |
| **User** | `~/.claude/settings.json` | All projects | Lower ⭐ |

**Configuration Merge Rules**:
- `settings.local.json` > `settings.json` > `~/.claude/settings.json`
- Same config keys: local overrides project overrides global
- Different config keys: All configs merged and effective

## Hook Examples

### Example 1: Auto-Format After File Edit

**Scenario**: After editing code files with Edit/Write tools, automatically run formatting tools

```bash
#!/bin/bash
# .claude/hooks/format-after-edit.sh

input=$(cat)

# Extract file path
file_path=$(echo "$input" | tr -d '\n' | \
    grep -o '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | \
    sed 's/.*"\([^"]*\)"$/\1/')

# Check if file exists
if [[ ! -f "$file_path" ]]; then
    echo "{}"
    exit 0
fi

# Choose formatting tool based on file type
case "$file_path" in
    *.py)
        if command -v black &> /dev/null; then
            black "$file_path" 2>&1 | logger -t format-hook
        fi
        ;;
    *.js|*.ts|*.jsx|*.tsx)
        if command -v prettier &> /dev/null; then
            prettier --write "$file_path" 2>&1 | logger -t format-hook
        fi
        ;;
    *.go)
        if command -v gofmt &> /dev/null; then
            gofmt -w "$file_path" 2>&1 | logger -t format-hook
        fi
        ;;
esac

echo "{}"
```

### Example 2: Block Dangerous Bash Commands

**Scenario**: Block bash commands that could cause data loss

```bash
#!/bin/bash
# .claude/hooks/block-dangerous-commands.sh

input=$(cat)

# Extract command
command=$(echo "$input" | tr -d '\n' | \
    grep -o '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | \
    sed 's/.*"\([^"]*\)"$/\1/')

# Dangerous pattern list
dangerous_patterns=(
    'rm.*-rf.*\*'
    'rm.*-rf.*/'
    'delete.*\*'
    ':(){:|:&};:'
    'dd.*if=.*of=/dev'
    'mkfs'
    'format'
)

# Check command
for pattern in "${dangerous_patterns[@]}"; do
    if [[ "$command" =~ $pattern ]]; then
        echo "{\"action\": \"block\", \"message\": \"Dangerous command blocked: $command\"}"
        exit 0
    fi
done

# Check sensitive files
if [[ "$command" =~ (rm|delete).*(\.env|credentials|secret|password) ]]; then
    echo "{\"action\": \"block\", \"message\": \"Attempt to delete sensitive file blocked\"}"
    exit 0
fi

echo "{}"
```

### Example 3: Intelligent Prompt Enhancement

**Scenario**: Detect keywords in user prompts and automatically remind about relevant agents

```bash
#!/bin/bash
# .claude/hooks/prompt-enhancement.sh

LOG_FILE=".claude/logs/prompt-enhancement.log"
mkdir -p "$(dirname "$LOG_FILE")"

input=$(cat)

# Extract prompt
prompt=$(echo "$input" | tr -d '\n' | \
    grep -o '"prompt"[[:space:]]*:[[:space:]]*"[^"]*"' | \
    sed 's/.*"\([^"]*\)"$/\1/')

# Log
{
    echo "=== Hook Triggered ==="
    echo "Time: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "Prompt length: ${#prompt} characters"
} >> "$LOG_FILE"

# High priority detection - explicit task management intent
if echo "$prompt" | grep -qiE "TodoWrite|task.*list|task.*status"; then
    echo "💡 Reminder: Task management need detected, suggest using /T TodoWrite command" >&2
    log "Trigger: High priority - task management" >> "$LOG_FILE"

# Medium priority detection - may need reminder
elif echo "$prompt" | grep -qiE "continue|next step|progress"; then
    # Smart filter: only trigger on short text
    if [ ${#prompt} -lt 100 ]; then
        echo "Tip: Can use /T to view current task status" >&2
        log "Trigger: Medium priority - task query" >> "$LOG_FILE"
    fi
fi

echo "{}"
```

## Real-World Experience & Pitfall Guide

Based on practical project experience successfully deploying hooks, revealing key details not explicitly stated in official documentation.

### Key Findings

#### 1. Session Restart is Mandatory

**Important Discovery**: Hooks configuration only loads at Claude Code session startup, runtime changes won't take effect.

```yaml
Problem Manifestation:
  - Hooks don't trigger after modifying .claude/settings.json
  - No error messages
  - Configuration appears completely ineffective

Root Cause:
  - Hooks config loads at session startup
  - Runtime changes not reloaded
  - Official docs don't emphasize this clearly

Solution:
  1. Completely exit Claude Code
  2. Restart Claude Code
  3. Enter project directory
  4. Test hooks functionality

Verification Method:
  - Enter trigger keywords
  - Check if log file has new records
  - Confirm reminder messages appear
```

#### 2. Script Permissions and Line Endings

```yaml
Permission Issue:
  Wrong: -rw-r--r-- (644, not executable)
  Correct: -rwxr-xr-x (755, executable)
  Solution: chmod +x .claude/hooks/*.sh

Line Endings Issue (Windows):
  Wrong: CRLF (Windows style)
  Correct: LF (Unix style)
  Check: file .claude/hooks/script.sh
  Solution: dos2unix .claude/hooks/*.sh
           or git config core.autocrlf input
```

#### 3. Silent Failure Diagnosis Strategy

```yaml
Diagnostic Checklist:
  1. Manual test script:
     echo '{"prompt":"test"}' | .claude/hooks/script.sh

  2. Check script syntax:
     bash -n .claude/hooks/script.sh

  3. Enable debug mode:
     bash -x .claude/hooks/script.sh <<< '{"prompt":"test"}'

  4. Check log files:
     tail -f .claude/logs/hook-name.log

  5. Validate config syntax:
     cat .claude/settings.json | jq .

  6. Check permissions:
     ls -la .claude/hooks/*.sh

  7. Check line endings:
     file .claude/hooks/*.sh

Common Failure Causes:
  - Script lacks execute permission → chmod +x
  - Line endings wrong → dos2unix
  - JSON parsing failed → check extraction logic
  - Config file syntax error → jq validate
  - Session not restarted → restart Claude Code
```

#### 4. Cross-Platform JSON Parsing

**Discovery**: Cannot rely on jq, must use pure bash solution.

```bash
# Reliable field extraction function
extract_field() {
    local input="$1"
    local field="$2"
    echo "$input" | tr -d '\n' | \
        grep -o "\"${field}\"[[:space:]]*:[[:space:]]*\"[^\"]*\"" | \
        sed 's/.*"\([^"]*\)"$/\1/'
}

# Usage example
input=$(cat)
prompt=$(extract_field "$input" "prompt")
session_id=$(extract_field "$input" "session_id")

# Handle complex JSON - remove newlines first, then extract fields
input=$(cat | tr -d '\n')
```

## Quality Checklist

Verify quality after creating hooks using this checklist:

```yaml
□ Goal Clarity
  - [ ] Automation goal clear and measurable
  - [ ] Trigger conditions clearly defined
  - [ ] Expected behavior specifically described

□ Event Selection
  - [ ] Event type matches requirements
  - [ ] Matcher rules precise
  - [ ] Won't over-trigger

□ Script Quality
  - [ ] Uses standard template
  - [ ] Comprehensive error handling
  - [ ] Detailed logging
  - [ ] Cross-platform compatible

□ JSON Processing
  - [ ] Uses reliable field extraction function
  - [ ] No jq dependency
  - [ ] Handles multi-line JSON
  - [ ] Validates output format

□ Configuration Correctness
  - [ ] settings.json syntax correct
  - [ ] command path correct
  - [ ] description clearly describes
  - [ ] Configuration layer selection correct

□ Testing Completeness
  - [ ] Manual tests pass
  - [ ] Boundary condition tests
  - [ ] Error scenario tests
  - [ ] Performance tests

□ Deployment Ready
  - [ ] Scripts have execute permission
  - [ ] Line endings correct
  - [ ] Log directory created
  - [ ] Documentation updated
```

## Reference Resources

### Official Documentation

- **[Claude Code Hooks Official Docs](https://docs.claude.com/zh-CN/docs/claude-code/hooks)** ⭐ Must-read
- **[Claude Code Hooks Guide](https://docs.claude.com/zh-CN/docs/claude-code/hooks-guide)** ⭐ Practical guide

---

**Version**: 1.0.0
**Last Updated**: 2025-10-18
**Compatibility**: Claude Code v4.5+
**Based On**: Claude Code Official Documentation (2025-10-18)
