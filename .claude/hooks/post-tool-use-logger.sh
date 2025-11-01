#!/bin/bash
# PostToolUse hook to log file changes

TOOL_NAME="$CLAUDE_TOOL_NAME"
FILE_PATH="$CLAUDE_TOOL_FILE_PATH"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

case "$TOOL_NAME" in
  "Write")
    echo "[$TIMESTAMP] File created: $FILE_PATH" >> .claude/logs/changes.log
    ;;
  "Edit"|"MultiEdit")
    echo "[$TIMESTAMP] File modified: $FILE_PATH" >> .claude/logs/changes.log
    ;;
esac
