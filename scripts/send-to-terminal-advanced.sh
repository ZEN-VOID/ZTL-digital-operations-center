#!/bin/bash
# 增强版终端命令发送脚本
# 支持: 多窗口管理、输出捕获、窗口查询
# 用法: ./send-to-terminal-advanced.sh [选项] "命令"

set -e

# 显示帮助
show_help() {
    cat << 'HELP'
用法: ./send-to-terminal-advanced.sh [选项] "命令"

选项:
  -w, --window N     向指定窗口发送命令 (N=1,2,3...)
  -c, --capture      捕获命令输出到文件
  -l, --list         列出所有 iTerm 窗口
  -n, --new          创建新窗口并执行命令
  -h, --help         显示此帮助信息

示例:
  # 向当前窗口发送命令
  ./send-to-terminal-advanced.sh "echo hello"

  # 向窗口2发送命令
  ./send-to-terminal-advanced.sh -w 2 "npm test"

  # 列出所有窗口
  ./send-to-terminal-advanced.sh -l

  # 创建新窗口并执行
  ./send-to-terminal-advanced.sh -n "tail -f /var/log/system.log"

  # 捕获输出
  ./send-to-terminal-advanced.sh -c "ls -la"

HELP
}

# 列出所有窗口
list_windows() {
    osascript <<'EOF'
tell application "iTerm"
    set windowCount to count of windows

    if windowCount = 0 then
        return "❌ 没有打开的窗口"
    end if

    set output to "📊 iTerm 窗口列表 (" & windowCount & " 个窗口)" & return & return

    repeat with i from 1 to windowCount
        set output to output & "窗口 " & i & ":" & return
        set tabCount to count of tabs of window i
        set output to output & "  标签页: " & tabCount & return

        try
            set sessionName to name of current session of window i
            set output to output & "  会话名: " & sessionName & return
        end try

        set output to output & return
    end repeat

    return output
end tell
EOF
}

# 向指定窗口发送命令
send_to_window() {
    local window_num=$1
    local command=$2

    osascript <<EOF
tell application "iTerm"
    activate

    set windowCount to count of windows

    if windowCount < $window_num then
        error "窗口 $window_num 不存在（共有 " & windowCount & " 个窗口）"
    end if

    tell current session of window $window_num
        write text "$command"
    end tell
end tell
EOF

    if [ $? -eq 0 ]; then
        echo "✅ [iTerm 窗口$window_num] 已发送: $command"
    else
        echo "❌ 发送失败"
        exit 1
    fi
}

# 创建新窗口并执行命令
create_and_execute() {
    local command=$1

    osascript <<EOF
tell application "iTerm"
    activate
    create window with default profile
    tell current session of current window
        write text "$command"
    end tell
    return "新窗口已创建"
end tell
EOF

    echo "✅ [iTerm 新窗口] 已发送: $command"
}

# 捕获输出
capture_output() {
    local command=$1
    local output_file="/tmp/iterm-output-$(date +%s).txt"

    # 发送带重定向的命令
    send_command "$command > $output_file 2>&1"

    # 等待执行
    sleep 2

    # 读取输出
    if [ -f "$output_file" ]; then
        echo "📄 捕获的输出:"
        cat "$output_file"
        rm "$output_file"
    else
        echo "⚠️ 未能捕获输出（可能需要更长等待时间）"
    fi
}

# 发送到当前窗口（默认行为）
send_command() {
    local command=$1

    osascript <<EOF
tell application "iTerm"
    activate

    -- 如果没有窗口，创建新窗口
    if (count of windows) = 0 then
        create window with default profile
    end if

    tell current session of current window
        write text "$command"
    end tell
end tell
EOF

    if [ $? -eq 0 ]; then
        echo "✅ [iTerm] 已发送: $command"
    else
        echo "❌ 发送失败"
        exit 1
    fi
}

# 解析参数
WINDOW_NUM=""
CAPTURE=false
LIST=false
NEW_WINDOW=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -w|--window)
            WINDOW_NUM="$2"
            shift 2
            ;;
        -c|--capture)
            CAPTURE=true
            shift
            ;;
        -l|--list)
            LIST=true
            shift
            ;;
        -n|--new)
            NEW_WINDOW=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            COMMAND="$1"
            shift
            ;;
    esac
done

# 执行操作
if [ "$LIST" = true ]; then
    list_windows
    exit 0
fi

if [ -z "$COMMAND" ]; then
    echo "❌ 错误: 请提供命令"
    echo "使用 -h 查看帮助"
    exit 1
fi

if [ -n "$WINDOW_NUM" ]; then
    send_to_window "$WINDOW_NUM" "$COMMAND"
elif [ "$NEW_WINDOW" = true ]; then
    create_and_execute "$COMMAND"
elif [ "$CAPTURE" = true ]; then
    capture_output "$COMMAND"
else
    send_command "$COMMAND"
fi
