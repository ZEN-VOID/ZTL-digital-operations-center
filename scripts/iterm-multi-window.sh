#!/bin/bash
# iTerm 多窗口管理脚本
# 用法示例在脚本底部

# 列出所有窗口
list_windows() {
    osascript <<'EOF'
tell application "iTerm"
    set windowCount to count of windows
    if windowCount = 0 then
        return "❌ 没有打开的窗口"
    end if

    set output to "📊 窗口总数: " & windowCount & return

    repeat with i from 1 to windowCount
        set output to output & "窗口 " & i & ": "
        try
            set sessionName to name of current session of window i
            set output to output & sessionName
        end try
        set output to output & return
    end repeat

    return output
end tell
EOF
}

# 向指定窗口发送命令
# 用法: send_to_window 窗口号 "命令"
send_to_window() {
    local window_num=$1
    local command=$2

    osascript <<EOF
tell application "iTerm"
    tell current session of window $window_num
        write text "$command"
    end tell
end tell
EOF
    echo "✅ [窗口$window_num] $command"
}

# 创建新窗口
create_window() {
    local command=$1

    osascript <<EOF
tell application "iTerm"
    create window with default profile
    if "$command" is not "" then
        tell current session of current window
            write text "$command"
        end tell
    end if
    return count of windows
end tell
EOF
}

# 向所有窗口广播命令
broadcast_to_all() {
    local command=$1

    osascript <<EOF
tell application "iTerm"
    set windowCount to count of windows
    repeat with i from 1 to windowCount
        tell current session of window i
            write text "$command"
        end tell
    end repeat
    return "✅ 已向 " & windowCount & " 个窗口发送命令"
end tell
EOF
}

# 使用示例
case "${1:-help}" in
    list)
        list_windows
        ;;
    send)
        if [ $# -lt 3 ]; then
            echo "用法: $0 send <窗口号> \"命令\""
            exit 1
        fi
        send_to_window "$2" "$3"
        ;;
    new)
        create_window "${2:-}"
        echo "✅ 新窗口已创建"
        ;;
    broadcast)
        if [ -z "$2" ]; then
            echo "用法: $0 broadcast \"命令\""
            exit 1
        fi
        broadcast_to_all "$2"
        ;;
    *)
        cat << 'HELP'
iTerm 多窗口管理脚本

用法:
  ./iterm-multi-window.sh list                    # 列出所有窗口
  ./iterm-multi-window.sh send 1 "命令"           # 向窗口1发送命令
  ./iterm-multi-window.sh new "初始命令"          # 创建新窗口
  ./iterm-multi-window.sh broadcast "命令"        # 向所有窗口发送命令

示例:
  # 列出窗口
  ./iterm-multi-window.sh list

  # 向窗口2发送命令
  ./iterm-multi-window.sh send 2 "git status"

  # 创建新窗口并启动服务器
  ./iterm-multi-window.sh new "npm run dev"

  # 向所有窗口发送清屏命令
  ./iterm-multi-window.sh broadcast "clear"

HELP
        ;;
esac
