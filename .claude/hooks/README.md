# Claude Code Hooks System

> Automated workflows triggered by Claude Code lifecycle events

## 📋 Overview

**Hooks** are executable scripts that automatically run in response to specific Claude Code events, enabling powerful automation workflows like parallel collaboration, context preservation, and task orchestration.

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Hook Event** | Lifecycle event that triggers a hook (e.g., PreCompact, SessionEnd) |
| **Hook Script** | Executable bash/python script in `.claude/hooks/` |
| **Hook Input** | JSON payload with event context passed via stdin |
| **Hook Output** | JSON response returned via stdout |

## 🎯 Available Hooks

### PreCompact Hook

**Event**: Triggered BEFORE Claude compacts conversation context

**Purpose**: Save context snapshot and launch parallel Claude instance to continue work

**Implementation**: `parallel-claude-after-compact.sh`

**Workflow**:
```
1. Compact triggered (context too large)
   ↓
2. PreCompact hook intercepts
   ↓
3. Save context snapshot to context/snapshots/
   ↓
4. Launch new iTerm window with Claude
   ↓
5. Inject context summary to new instance
   ↓
6. Original compact continues
   ↓
7. Two Claude instances work in parallel
```

**Benefits**:
- ✅ Zero context loss during compact
- ✅ Automatic task continuity
- ✅ Parallel processing capability
- ✅ No manual intervention needed

### SessionEnd Hook (Future)

**Event**: Triggered when Claude Code session ends

**Purpose**: Save session summary, cleanup resources, trigger notifications

**Status**: Not yet implemented

### TaskSubmit Hook (Future)

**Event**: Triggered when user submits a task

**Purpose**: Task routing, validation, or preprocessing

**Status**: Not yet implemented

## 📁 Directory Structure

```
.claude/hooks/
├── README.md                           # This file
├── parallel-claude-after-compact.sh   # PreCompact hook implementation
├── SessionEnd.sh                       # (Future) Session cleanup hook
└── TaskSubmit.sh                       # (Future) Task preprocessing hook

Related directories:
├── context/snapshots/                  # Context snapshots saved by hooks
├── .claude/logs/                       # Hook execution logs
└── .claude/locks/                      # Hook coordination locks
```

## 🚀 Quick Start

### Enabling a Hook

Hooks are automatically enabled when present in `.claude/hooks/` with executable permissions.

```bash
# Ensure hook is executable
chmod +x .claude/hooks/parallel-claude-after-compact.sh

# Verify hook is detected
ls -la .claude/hooks/
```

### Testing a Hook

```bash
# Test PreCompact hook with mock input
echo '{"context_to_compact": "Test context", "reason": "test"}' | \
  .claude/hooks/parallel-claude-after-compact.sh

# Check execution log
cat .claude/logs/parallel-claude-after-compact.log
```

### Viewing Hook Logs

```bash
# Tail hook logs in real-time
tail -f .claude/logs/parallel-claude-after-compact.log

# View full log history
cat .claude/logs/parallel-claude-after-compact.log
```

## 🎨 Hook Implementation Guide

### Hook Input Format

Hooks receive JSON input via stdin:

```json
{
  "event": "PreCompact",
  "timestamp": "2025-10-30T08:30:00Z",
  "context_to_compact": "Full conversation context...",
  "reason": "context_limit_reached",
  "metadata": {
    "total_tokens": 150000,
    "compact_threshold": 140000
  }
}
```

### Hook Output Format

Hooks must return JSON via stdout:

```json
{
  "success": true,
  "message": "Hook executed successfully",
  "data": {
    "context_saved": "/path/to/snapshot.txt",
    "parallel_instance_launched": true,
    "window_index": 4
  }
}
```

### Hook Template

```bash
#!/bin/bash

# ========================================================================
# Hook Name: My Custom Hook
# Event: PreCompact / SessionEnd / TaskSubmit
# Version: 1.0.0
# ========================================================================

# Configuration
LOG_FILE=".claude/logs/my-hook.log"

# Function: Log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"
}

# Function: Extract JSON field
extract_field() {
    local input="$1"
    local field="$2"
    echo "$input" | grep -o "\"${field}\"[[:space:]]*:[[:space:]]*\"[^\"]*\"" | \
        sed 's/.*"\([^"]*\)"$/\1/'
}

# Main logic
main() {
    log "=== Hook Triggered ==="

    # Read input
    input=$(cat)
    log "Input received: ${#input} characters"

    # Extract fields
    context=$(extract_field "$input" "context_to_compact")
    reason=$(extract_field "$input" "reason")

    # Your hook logic here
    # ...

    # Return success
    echo '{"success": true, "message": "Hook executed"}'
}

main
```

## ⚙️ Configuration

### Global Hook Settings

Hook behavior is controlled by Claude Code settings:

```json
{
  "hooks": {
    "enabled": true,
    "timeout": 30000,
    "parallel": false
  }
}
```

### Hook-Specific Configuration

Each hook can have its own configuration:

```bash
# In parallel-claude-after-compact.sh
DEBUG=${DEBUG:-false}                # Enable debug logging
CONTEXT_DIR="context/snapshots"
LOCK_FILE=".claude/locks/parallel-claude.lock"
```

### Environment Variables

```bash
# Enable debug mode
export DEBUG=true

# Customize timeout
export HOOK_TIMEOUT=60

# Disable specific hook
export SKIP_PARALLEL_CLAUDE=true
```

## 🔧 Advanced Features

### Lock Mechanism

Prevents duplicate hook executions:

```bash
# Acquire lock
acquire_lock() {
    local lock_dir=".claude/locks/my-hook.lock.d"
    if mkdir "$lock_dir" 2>/dev/null; then
        echo $$ > "$lock_dir/pid"
        return 0
    else
        return 1  # Lock already held
    fi
}

# Release lock
release_lock() {
    local lock_dir=".claude/locks/my-hook.lock.d"
    rm -f "$lock_dir/pid"
    rmdir "$lock_dir" 2>/dev/null
}
```

### Async Execution

Launch background tasks without blocking:

```bash
# Launch parallel task asynchronously
(launch_parallel_claude "$context" >> "$LOG_FILE" 2>&1) &
log "Background task launched (PID: $!)"

# Hook returns immediately, compact proceeds
echo '{"success": true}'
```

### Context Preservation

Save conversation snapshots:

```bash
# Save full context
{
    echo "=== Context Snapshot ==="
    echo "Time: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "Reason: $reason"
    echo "=== Context Content ==="
    echo "$context"
} > "context/snapshots/compact-$(date +%s).txt"
```

### Integration with Skills

Hooks can invoke skills directly:

```bash
# Use 深渊凝视 skill to launch parallel Claude
ABYSS_GAZE_SCRIPT=".claude/skills/深渊凝视/scripts/abyss_gaze.py"

# Create new window and send command
python3 "$ABYSS_GAZE_SCRIPT" execute_in_new_window \
    "cd '$PWD' && claude --dangerously-skip-permissions"

# Type context into new window
python3 "$ABYSS_GAZE_SCRIPT" type_text_in_window \
    "$context_summary" "$new_window_index" true
```

## 📊 Monitoring & Debugging

### Log Analysis

```bash
# Count hook executions
grep "Hook Triggered" .claude/logs/*.log | wc -l

# Find errors
grep "ERROR" .claude/logs/*.log

# Monitor in real-time
tail -f .claude/logs/*.log
```

### Performance Metrics

```bash
# Measure hook execution time
start_time=$(date +%s)
# ... hook logic ...
end_time=$(date +%s)
execution_time=$((end_time - start_time))
log "Execution time: ${execution_time}s"
```

### Debugging Tips

```bash
# Enable verbose logging
DEBUG=true .claude/hooks/parallel-claude-after-compact.sh

# Test with mock data
echo '{"context": "test", "reason": "debug"}' | \
    bash -x .claude/hooks/parallel-claude-after-compact.sh

# Check lock status
ls -la .claude/locks/

# Verify permissions
ls -la .claude/hooks/
```

## ⚠️ Important Notes

### Best Practices

✅ **Do**:
- Always return valid JSON
- Use lock files to prevent duplicates
- Log all important events
- Clean up temporary files
- Test hooks before deployment
- Use reasonable timeouts

❌ **Don't**:
- Block hook execution indefinitely
- Modify Claude Code internal state
- Depend on specific directory structure
- Hardcode absolute paths
- Ignore error handling

### Performance Considerations

| Aspect | Recommendation |
|--------|----------------|
| **Execution Time** | < 5 seconds (use async for long tasks) |
| **Log File Size** | Rotate logs > 10MB |
| **Lock Timeout** | Clean stale locks > 5 minutes old |
| **Context Size** | Truncate summaries > 1000 chars |

### Security Notes

- Hooks run with same permissions as Claude Code
- Never execute untrusted code in hooks
- Sanitize all user inputs
- Validate JSON before processing
- Use temporary files securely

## 🔗 Related Resources

### Internal Documentation
- [深渊凝视 Skill](../skills/深渊凝视/SKILL.md) - iTerm control integration
- [iTerm Integration Summary](../../scripts/iTerm-integration-summary.md)
- [Project CLAUDE.md](../../CLAUDE.md) - Global configuration

### Claude Code Documentation
- [Hooks Documentation](https://docs.claude.com/en/docs/claude-code/hooks)
- [Settings Reference](https://docs.claude.com/en/docs/claude-code/settings)

## 📝 Changelog

### v1.0.0 (2025-10-30)
- ✅ Initial hook system documentation
- ✅ PreCompact hook implementation
- ✅ 深渊凝视 skill integration
- ✅ Lock mechanism and async execution
- ✅ Comprehensive testing and debugging guide

---

**Status**: Production Ready ✅
**Maintainer**: ZTL Team
**Last Updated**: 2025-10-30
