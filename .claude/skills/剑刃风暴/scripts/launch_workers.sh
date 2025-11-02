#!/bin/bash
# ========================================================================
# Worker启动器 - 并行任务执行引擎
# ========================================================================
# 功能: 扫描任务队列,启动多个Worker实例并行执行任务
# 版本: 1.0.0
# 创建时间: 2025-11-01
# ========================================================================

# ========== Configuration ==========
SCRIPT_NAME="launch-workers"
LOG_DIR=".claude/logs"
LOG_FILE="${LOG_DIR}/${SCRIPT_NAME}.log"
ABYSS_GAZE_SCRIPT=".claude/skills/深渊凝视/scripts/abyss_gaze.py"
MAX_WORKERS=${MAX_WORKERS:-3}  # 最大并发Worker数
WORKER_STARTUP_DELAY=${WORKER_STARTUP_DELAY:-5}  # Worker启动间隔(秒)
CLAUDE_INIT_DELAY=${CLAUDE_INIT_DELAY:-20}  # Claude初始化等待时间(秒)
DEBUG=${DEBUG:-false}

# 创建日志目录
mkdir -p "$LOG_DIR"

# ========== Function Definitions ==========

log() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $*" | tee -a "$LOG_FILE"
}

error_exit() {
    log "ERROR: $1"
    exit 1
}

check_dependencies() {
    """检查依赖工具是否存在"""

    if [[ ! -f "$ABYSS_GAZE_SCRIPT" ]]; then
        error_exit "深渊凝视脚本不存在: $ABYSS_GAZE_SCRIPT"
    fi

    if ! command -v python3 &> /dev/null; then
        error_exit "Python3未安装"
    fi

    if ! command -v jq &> /dev/null; then
        log "WARNING: jq未安装,部分功能可能受限"
    fi
}

scan_pending_tasks() {
    """扫描待执行任务"""
    local task_queue_dir="$1"

    if [[ ! -d "$task_queue_dir" ]]; then
        log "任务队列目录不存在: $task_queue_dir"
        echo ""
        return
    fi

    # 查找状态为pending的任务
    local pending_tasks=""

    for task_file in "$task_queue_dir"/task-*.json; do
        if [[ -f "$task_file" ]]; then
            local status=$(jq -r '.status' "$task_file" 2>/dev/null || echo "unknown")
            if [[ "$status" == "pending" ]]; then
                local task_id=$(jq -r '.task_id' "$task_file" 2>/dev/null)
                pending_tasks="${pending_tasks}${task_id} "
            fi
        fi
    done

    echo "$pending_tasks"
}

check_task_dependencies() {
    """检查任务依赖是否已完成"""
    local task_file="$1"
    local task_queue_dir=$(dirname "$task_file")

    # 获取任务依赖列表
    local dependencies=$(jq -r '.dependencies[]' "$task_file" 2>/dev/null)

    if [[ -z "$dependencies" ]]; then
        # 无依赖,可以执行
        return 0
    fi

    # 检查每个依赖任务的状态
    for dep_id in $dependencies; do
        local dep_file="$task_queue_dir/task-${dep_id}.json"

        if [[ ! -f "$dep_file" ]]; then
            log "依赖任务文件不存在: $dep_file"
            return 1
        fi

        local dep_status=$(jq -r '.status' "$dep_file" 2>/dev/null)

        if [[ "$dep_status" != "completed" ]]; then
            log "依赖任务未完成: $dep_id (状态: $dep_status)"
            return 1
        fi
    done

    # 所有依赖已完成
    return 0
}

get_current_worker_count() {
    """获取当前运行的Worker数量"""
    local windows=$(python3 "$ABYSS_GAZE_SCRIPT" list_windows 2>/dev/null)
    local total=$(echo "$windows" | jq -r '.total' 2>/dev/null || echo "0")

    # 减去主窗口
    local worker_count=$((total - 1))

    if [[ $worker_count -lt 0 ]]; then
        worker_count=0
    fi

    echo "$worker_count"
}

launch_worker_instance() {
    """启动单个Worker实例"""
    local task_id="$1"
    local task_queue_dir="$2"
    local task_file="$task_queue_dir/task-${task_id}.json"

    log "=== 启动Worker: 任务 $task_id ==="

    # 检查任务文件是否存在
    if [[ ! -f "$task_file" ]]; then
        log "ERROR: 任务文件不存在: $task_file"
        return 1
    fi

    # 检查依赖
    if ! check_task_dependencies "$task_file"; then
        log "任务 $task_id 依赖未满足,跳过"
        return 1
    fi

    # 读取任务配置
    local task_description=$(jq -r '.description' "$task_file")
    local execution_plan=$(jq -r '.execution_plan' "$task_file")
    local output_path=$(jq -r '.output_path' "$task_file")
    local input_data=$(jq -r '.input_data' "$task_file")

    log "任务描述: $task_description"

    # Step 1: 获取当前窗口数
    local before_windows=$(python3 "$ABYSS_GAZE_SCRIPT" list_windows 2>/dev/null)
    local before_count=$(echo "$before_windows" | jq -r '.total' 2>/dev/null || echo "0")
    log "当前窗口数: $before_count"

    # Step 2: 创建新窗口并启动Claude
    local current_dir=$(pwd)
    local startup_cmd="cd '$current_dir' && claude --dangerously-skip-permissions"

    log "执行启动命令: $startup_cmd"

    local window_result=$(python3 "$ABYSS_GAZE_SCRIPT" execute_in_new_window "$startup_cmd" 2>&1)
    log "窗口创建结果: $window_result"

    # Step 3: 计算新窗口索引
    local new_window_index=$((before_count + 1))
    log "新窗口索引: $new_window_index"

    # Step 4: 等待Claude初始化
    log "等待Claude初始化 ($CLAUDE_INIT_DELAY 秒)..."
    sleep "$CLAUDE_INIT_DELAY"

    # Step 5: 更新任务状态为running
    local temp_file=$(mktemp)
    jq ".status = \"running\" | .started_at = \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\" | .worker_window_index = $new_window_index" \
        "$task_file" > "$temp_file" && mv "$temp_file" "$task_file"

    log "✅ 任务状态已更新: $task_id → running"

    # Step 6: 构造任务提示
    local task_prompt="请执行以下任务:

**任务ID**: $task_id
**任务描述**: $task_description

**输入数据**:
\`\`\`json
$input_data
\`\`\`

**执行计划**:
$execution_plan

**输出要求**:
1. 按照执行计划完成任务
2. 将结果保存到以下路径: \`$output_path\`
3. 结果格式为JSON,包含以下字段:
   - task_id: 任务ID
   - status: completed 或 failed
   - execution_time: 执行时间戳
   - duration_seconds: 执行耗时(秒)
   - output_data: 任务输出数据(字典)
   - summary: 执行摘要(字符串)
   - errors: 错误信息列表
   - warnings: 警告信息列表
   - next_steps: 后续建议列表

4. 完成后,更新任务状态文件: \`$task_file\`
   使用以下命令:
   \`\`\`bash
   jq '.status = \"completed\" | .completed_at = \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"' \\
       $task_file > /tmp/task-update.json && \\
       mv /tmp/task-update.json $task_file
   \`\`\`

**重要**: 请严格按照上述要求完成任务并保存结果。"

    # Step 7: 保存提示到临时文件
    local prompt_file="/tmp/worker-task-${task_id}-$$.txt"
    echo "$task_prompt" > "$prompt_file"
    log "任务提示已保存: $prompt_file"

    # Step 8: 发送任务提示到Worker窗口
    log "发送任务提示到窗口 $new_window_index..."

    python3 "$ABYSS_GAZE_SCRIPT" type_text_in_window \
        "$task_prompt" \
        "$new_window_index" \
        true \
        > /tmp/send-task-result-${task_id}.json 2>&1

    local send_result=$(cat "/tmp/send-task-result-${task_id}.json" 2>/dev/null)
    log "发送结果: $send_result"

    # Step 9: 清理临时文件
    rm -f "$prompt_file"
    rm -f "/tmp/send-task-result-${task_id}.json"

    log "✅ Worker $task_id 启动完成 (窗口 $new_window_index)"
    return 0
}

launch_workers() {
    """启动Worker实例(主入口)"""
    local project_name="$1"
    local task_queue_dir="output/${project_name}/task-queue"

    log "=== Worker启动器开始运行 ==="
    log "项目名称: $project_name"
    log "任务队列: $task_queue_dir"
    log "最大Worker数: $MAX_WORKERS"

    # 检查依赖
    check_dependencies

    # 扫描待执行任务
    local pending_tasks=$(scan_pending_tasks "$task_queue_dir")

    if [[ -z "$pending_tasks" ]]; then
        log "没有待执行任务"
        return 0
    fi

    log "待执行任务: $pending_tasks"

    # 启动Worker
    local launched_count=0

    for task_id in $pending_tasks; do
        # 检查当前Worker数量
        local current_workers=$(get_current_worker_count)

        if [[ $current_workers -ge $MAX_WORKERS ]]; then
            log "已达到最大Worker数($MAX_WORKERS),等待Worker完成..."
            break
        fi

        # 启动Worker实例
        if launch_worker_instance "$task_id" "$task_queue_dir"; then
            launched_count=$((launched_count + 1))
            log "✅ Worker $launched_count/$MAX_WORKERS 已启动"

            # 启动间隔
            if [[ $launched_count -lt $MAX_WORKERS ]]; then
                log "等待 $WORKER_STARTUP_DELAY 秒后启动下一个Worker..."
                sleep "$WORKER_STARTUP_DELAY"
            fi
        fi
    done

    log "=== Worker启动完成 ==="
    log "已启动Worker数: $launched_count"
    log "剩余待执行任务: $(echo $pending_tasks | wc -w)"
}

# ========== Main Logic ==========
main() {
    if [[ $# -lt 1 ]]; then
        echo "Usage: $0 <project_name>"
        echo "Example: $0 数据分析项目"
        exit 1
    fi

    local project_name="$1"

    launch_workers "$project_name"
}

# 执行主函数
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
