#!/bin/bash
# ========================================================================
# PreCompact Hook: 智能任务分割 + 并行Worker执行 v3.0
# ========================================================================
# 功能:
#   1. 在compact执行前保存上下文
#   2. 智能分析任务并分割为子任务
#   3. 启动多个Worker实例并行执行
#   4. 启动结果汇总器自动整合输出
# 触发时机: PreCompact (compact执行前)
# 版本: 3.0.0 (剑刃风暴)
# 创建时间: 2025-11-01
# ========================================================================

# ========== Configuration ==========
SCRIPT_NAME="parallel-claude-after-compact-v3"
LOG_DIR=".claude/logs"
LOG_FILE="${LOG_DIR}/${SCRIPT_NAME}.log"
CONTEXT_DIR="context/snapshots"
CONTEXT_FILE="${CONTEXT_DIR}/last-compact-context.txt"
LOCK_FILE=".claude/locks/parallel-claude.lock"

# 剑刃风暴组件路径
SKILL_BASE=".claude/skills/剑刃风暴/multi-threading-executor"
TASK_SPLITTER_SCRIPT="${SKILL_BASE}/scripts/task_splitter.py"
RESULT_AGGREGATOR_SCRIPT="${SKILL_BASE}/scripts/result_aggregator.py"
WORKER_LAUNCHER_SCRIPT="${SKILL_BASE}/scripts/launch_workers.sh"

# 深渊凝视脚本
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

check_dependencies() {
    """检查依赖组件是否存在"""

    if [[ ! -f "$TASK_SPLITTER_SCRIPT" ]]; then
        log "WARNING: TaskSplitter未找到: $TASK_SPLITTER_SCRIPT"
        return 1
    fi

    if [[ ! -f "$RESULT_AGGREGATOR_SCRIPT" ]]; then
        log "WARNING: ResultAggregator未找到: $RESULT_AGGREGATOR_SCRIPT"
        return 1
    fi

    if [[ ! -f "$WORKER_LAUNCHER_SCRIPT" ]]; then
        log "WARNING: Worker启动器未找到: $WORKER_LAUNCHER_SCRIPT"
        return 1
    fi

    if [[ ! -f "$ABYSS_GAZE_SCRIPT" ]]; then
        log "WARNING: 深渊凝视未找到: $ABYSS_GAZE_SCRIPT"
        return 1
    fi

    return 0
}

acquire_lock() {
    local lock_dir=".claude/locks/parallel-claude.lock.d"
    local max_age=300

    if [[ -d "$lock_dir" ]]; then
        local lock_age=$(( $(date +%s) - $(stat -f %m "$lock_dir" 2>/dev/null || echo 0) ))
        if [[ $lock_age -gt $max_age ]]; then
            log "Cleaning up stale lock (age: ${lock_age}s)"
            rmdir "$lock_dir" 2>/dev/null || true
        fi
    fi

    if mkdir "$lock_dir" 2>/dev/null; then
        echo $$ > "$lock_dir/pid"
        log "Lock acquired (PID: $$)"
        return 0
    else
        local lock_pid=$(cat "$lock_dir/pid" 2>/dev/null || echo "unknown")
        if [[ "$lock_pid" != "unknown" ]] && ! ps -p "$lock_pid" > /dev/null 2>&1; then
            log "Cleaning up stale lock (PID: $lock_pid no longer exists)"
            rmdir "$lock_dir" 2>/dev/null || true
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

    if [[ "$lock_pid" == "$$" ]]; then
        rm -f "$lock_dir/pid"
        rmdir "$lock_dir" 2>/dev/null || true
        log "Lock released (PID: $$)"
    fi
}

analyze_task_from_context() {
    """从上下文中分析当前任务"""
    local context="$1"

    # 提取任务相关信息
    # 简单策略: 查找"任务"、"目标"、"需要"等关键词
    local task_description=""

    # 尝试从上下文中提取任务描述
    if echo "$context" | grep -q "任务:"; then
        task_description=$(echo "$context" | grep "任务:" | head -1 | sed 's/任务://g')
    elif echo "$context" | grep -q "目标:"; then
        task_description=$(echo "$context" | grep "目标:" | head -1 | sed 's/目标://g')
    else
        # 使用上下文前200字符作为任务描述
        task_description=$(echo "$context" | head -c 200)
    fi

    echo "$task_description"
}

generate_project_name() {
    """生成项目名称"""
    local context="$1"

    # 尝试从上下文中提取项目名称
    if echo "$context" | grep -q "项目名称:"; then
        echo "$context" | grep "项目名称:" | head -1 | sed 's/项目名称://g' | xargs
    elif echo "$context" | grep -q "项目:"; then
        echo "$context" | grep "项目:" | head -1 | sed 's/项目://g' | xargs
    else
        # 使用时间戳作为默认项目名称
        echo "任务-$(date +%Y%m%d-%H%M%S)"
    fi
}

split_task_and_launch_workers() {
    """任务分割和Worker启动"""
    local context="$1"
    local current_dir="$2"

    log "=== 开始任务分割与Worker启动 ==="

    # 分析任务
    local task_description=$(analyze_task_from_context "$context")
    log "任务描述: $task_description"

    # 生成项目名称
    local project_name=$(generate_project_name "$context")
    log "项目名称: $project_name"

    # 调用TaskSplitter分割任务
    log "调用TaskSplitter分割任务..."

    cd "$current_dir"

    python3 "$TASK_SPLITTER_SCRIPT" \
        "$project_name" \
        "$task_description" \
        >> "$LOG_FILE" 2>&1

    if [[ $? -ne 0 ]]; then
        log "ERROR: TaskSplitter执行失败"
        return 1
    fi

    log "✅ 任务分割完成"

    # 启动Worker实例
    log "启动Worker实例..."

    bash "$WORKER_LAUNCHER_SCRIPT" "$project_name" >> "$LOG_FILE" 2>&1

    if [[ $? -ne 0 ]]; then
        log "ERROR: Worker启动失败"
        return 1
    fi

    log "✅ Worker启动完成"

    # 启动结果汇总器(后台运行)
    log "启动结果汇总器..."

    (python3 "$RESULT_AGGREGATOR_SCRIPT" "$project_name" --monitor >> "$LOG_FILE" 2>&1) &

    local aggregator_pid=$!
    log "✅ 结果汇总器已启动 (PID: $aggregator_pid)"

    # 保存项目信息到文件
    local project_info_file="output/${project_name}/project-info.json"
    mkdir -p "output/${project_name}"

    cat > "$project_info_file" <<EOF
{
  "project_name": "$project_name",
  "task_description": "$task_description",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "aggregator_pid": $aggregator_pid,
  "task_queue_dir": "output/${project_name}/task-queue",
  "results_dir": "output/${project_name}/results",
  "report_path": "output/${project_name}/final-report.md"
}
EOF

    log "✅ 项目信息已保存: $project_info_file"

    return 0
}

# ========== Main Logic ==========
main() {
    log "=== PreCompact Hook Triggered (v3.0 剑刃风暴) ==="

    # 读取输入
    input=$(cat)
    log "Input length: ${#input} characters"

    # 提取字段
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

    # 检查依赖
    if ! check_dependencies; then
        log "WARNING: 剑刃风暴组件不完整,回退到传统模式"
        echo "{}"
        return 0
    fi

    # 尝试获取锁
    if ! acquire_lock; then
        log "Cannot launch: lock acquisition failed"
        echo "{}"
        return 0
    fi

    trap release_lock EXIT

    # 当前目录
    local current_dir=$(pwd)
    log "Current directory: $current_dir"

    # 异步启动任务分割和Worker(不阻塞compact)
    (split_task_and_launch_workers "$context" "$current_dir" >> "$LOG_FILE" 2>&1) &

    local worker_launcher_pid=$!
    log "Worker启动流程已启动 (PID: $worker_launcher_pid)"

    log "Hook completed, compact will proceed"
    echo "{}"
}

main
