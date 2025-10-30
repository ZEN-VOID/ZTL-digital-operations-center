#!/bin/bash
# ========================================================================
# PreCompact Hook: 并行 Claude 实例协作 v2.0
# ========================================================================
# 功能: 在 compact 执行前保存上下文，启动新 iTerm 窗口运行并行 Claude
# 触发时机: PreCompact (compact 执行前)
# 改进: 确保命令发送到正确窗口，自动提交输入
# 版本: 2.0.0
# ========================================================================

# ========== Configuration ==========
SCRIPT_NAME="parallel-claude-after-compact"
LOG_DIR=".claude/logs"
LOG_FILE="${LOG_DIR}/${SCRIPT_NAME}.log"
CONTEXT_DIR="context/snapshots"
CONTEXT_FILE="${CONTEXT_DIR}/last-compact-context.txt"
LOCK_FILE=".claude/locks/parallel-claude.lock"
ABYSS_GAZE_SCRIPT=".claude/skills/深渊凝视/scripts/abyss_gaze.py"
DEBUG=${DEBUG:-false}

# 创建必需的目录
mkdir -p "$LOG_DIR"
mkdir -p "$CONTEXT_DIR"
mkdir -p ".claude/locks"

# ========== Function Definitions ==========

log() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $*" >> "$LOG_FILE"
    if [[ "$DEBUG" == "true" ]]; then
        echo "$*" >&2
    fi
}

extract_field() {
    local input="$1"
    local field="$2"
    echo "$input" | tr -d '\n' | \
        grep -o "\"${field}\"[[:space:]]*:[[:space:]]*\"[^\"]*\"" | \
        sed 's/.*"\([^"]*\)"$/\1/' | \
        sed 's/\\n/\n/g'
}

handle_error() {
    local error_msg="$1"
    log "ERROR: $error_msg"
    echo "{}"
    exit 0
}

acquire_lock() {
    # 使用 mkdir 实现原子锁（macOS 兼容）
    local lock_dir=".claude/locks/parallel-claude.lock.d"
    local max_age=300  # 锁文件最大存活时间(秒)

    # 检查是否有过期的锁
    if [[ -d "$lock_dir" ]]; then
        local lock_age=$(( $(date +%s) - $(stat -f %m "$lock_dir" 2>/dev/null || echo 0) ))
        if [[ $lock_age -gt $max_age ]]; then
            log "Cleaning up stale lock (age: ${lock_age}s)"
            rmdir "$lock_dir" 2>/dev/null || true
        fi
    fi

    # 尝试创建锁目录（原子操作）
    if mkdir "$lock_dir" 2>/dev/null; then
        echo $$ > "$lock_dir/pid"
        log "Lock acquired (PID: $$)"
        return 0
    else
        local lock_pid=$(cat "$lock_dir/pid" 2>/dev/null || echo "unknown")
        # 检查锁的进程是否还在运行
        if [[ "$lock_pid" != "unknown" ]] && ! ps -p "$lock_pid" > /dev/null 2>&1; then
            log "Cleaning up stale lock (PID: $lock_pid no longer exists)"
            rmdir "$lock_dir" 2>/dev/null || true
            # 再次尝试获取锁
            if mkdir "$lock_dir" 2>/dev/null; then
                echo $$ > "$lock_dir/pid"
                log "Lock acquired (PID: $$)"
                return 0
            fi
        fi
        log "SKIP: Another parallel Claude instance is already running (PID: $lock_pid)"
        return 1
    fi
}

release_lock() {
    local lock_dir=".claude/locks/parallel-claude.lock.d"
    local lock_pid=$(cat "$lock_dir/pid" 2>/dev/null || echo "unknown")

    # 只释放自己创建的锁
    if [[ "$lock_pid" == "$$" ]]; then
        rm -f "$lock_dir/pid"
        rmdir "$lock_dir" 2>/dev/null || true
        log "Lock released (PID: $$)"
    fi
}

launch_parallel_claude() {
    local context_summary="$1"
    local current_dir="$2"

    log "=== Starting parallel Claude instance ==="

    # 尝试获取锁
    if ! acquire_lock; then
        log "Cannot launch: lock acquisition failed"
        return 1
    fi

    # 确保退出时释放锁
    trap release_lock EXIT

    if [[ ! -f "$ABYSS_GAZE_SCRIPT" ]]; then
        log "ERROR: 深渊凝视 script not found at $ABYSS_GAZE_SCRIPT"
        release_lock
        return 1
    fi

    # Step 1: 记录当前窗口数
    local before_windows=$(python3 "$ABYSS_GAZE_SCRIPT" list_windows 2>/dev/null)
    local before_count=$(echo "$before_windows" | grep -o '"total"[[:space:]]*:[[:space:]]*[0-9]*' | grep -o '[0-9]*')
    log "Current window count: $before_count"

    # Step 2: 创建新窗口并启动 Claude
    local startup_cmd="cd '$current_dir' && claude --dangerously-skip-permissions"
    log "Executing: $startup_cmd"

    local window_result=$(python3 "$ABYSS_GAZE_SCRIPT" execute_in_new_window "$startup_cmd" 2>&1)
    log "Window creation result: $window_result"

    # Step 3: 获取新窗口的索引
    local new_window_index=$((before_count + 1))
    log "New window index should be: $new_window_index"

    # Step 4: 验证新窗口已创建
    sleep 2
    local after_windows=$(python3 "$ABYSS_GAZE_SCRIPT" list_windows 2>/dev/null)
    local after_count=$(echo "$after_windows" | grep -o '"total"[[:space:]]*:[[:space:]]*[0-9]*' | grep -o '[0-9]*')
    log "After creation window count: $after_count"

    if [[ "$after_count" -le "$before_count" ]]; then
        log "ERROR: New window was not created"
        return 1
    fi

    log "✓ New window created successfully at index $new_window_index"

    # Step 5: 等待 Claude Code 完全启动
    log "Waiting for Claude Code to initialize (20 seconds)..."
    sleep 20

    # Step 6: 构造任务提示（简洁版，避免特殊字符问题）
    local task_prompt="请帮我继续执行任务。上下文状态：

$context_summary"

    log "Preparing to send task context (${#task_prompt} chars)"

    # Step 7: 将任务写入临时文件
    local prompt_file="/tmp/claude-compact-context-$$.txt"
    echo "$task_prompt" > "$prompt_file"
    log "Context saved to temp file: $prompt_file"

    # Step 8: 使用 type_text_in_window 命令发送并提交
    log "Sending context to window $new_window_index using type_text_in_window..."

    # 直接使用 type_text_in_window (submit=true 自动按回车)
    python3 "$ABYSS_GAZE_SCRIPT" type_text_in_window "$task_prompt" "$new_window_index" true > /tmp/send-context-result.json 2>&1

    local send_result=$(cat /tmp/send-context-result.json 2>/dev/null)
    log "Send result: $send_result"

    # Step 9: 清理临时文件
    rm -f "$prompt_file"
    rm -f /tmp/send-context-result.json

    # Step 10: 验证发送状态
    sleep 3
    log "Task context sent to window $new_window_index"
    log "✓ Parallel Claude instance is now processing the task"

    # Step 11: 启动监控（可选）
    monitor_parallel_claude "$new_window_index" &

    return 0
}

monitor_parallel_claude() {
    local window_index="$1"
    local monitor_interval=30
    local max_checks=10

    for ((i=1; i<=max_checks; i++)); do
        sleep "$monitor_interval"

        local window_check=$(python3 "$ABYSS_GAZE_SCRIPT" list_windows 2>&1)

        if echo "$window_check" | grep -q "\"index\": $window_index"; then
            log "Monitor [$i/$max_checks]: Window $window_index is active"
        else
            log "Monitor [$i/$max_checks]: Window $window_index closed"
            break
        fi
    done

    log "Monitoring completed for window $window_index"
}

# ========== Main Logic ==========
main() {
    log "=== PreCompact Hook Triggered ==="

    input=$(cat)
    log "Input length: ${#input} characters"

    context=$(extract_field "$input" "context_to_compact")
    reason=$(extract_field "$input" "reason")

    if [[ -z "$context" ]]; then
        log "WARNING: No context field, using full input"
        context="$input"
    fi

    log "Context length: ${#context} characters"
    log "Reason: $reason"

    # 保存完整上下文
    {
        echo "=== Context Snapshot ==="
        echo "Time: $(date '+%Y-%m-%d %H:%M:%S')"
        echo "Reason: $reason"
        echo "=== Context Content ==="
        echo "$context"
    } > "$CONTEXT_FILE"

    log "Context saved to $CONTEXT_FILE"

    # 创建摘要（前800字符）
    local context_summary
    if [[ ${#context} -gt 800 ]]; then
        context_summary="${context:0:800}

... (上下文已截断，完整内容共 ${#context} 字符)

请根据以上信息继续执行任务。"
    else
        context_summary="$context"
    fi

    local current_dir=$(pwd)
    log "Current directory: $current_dir"

    # 异步启动并行实例（不阻塞 compact）
    (launch_parallel_claude "$context_summary" "$current_dir" >> "$LOG_FILE" 2>&1) &

    log "Parallel Claude launch initiated (PID: $!)"
    log "Hook completed, compact will proceed"

    echo "{}"
}

main
