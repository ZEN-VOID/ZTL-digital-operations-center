#!/bin/bash
# 发送命令到 iTerm 并捕获输出
# 用法: ./send-and-capture.sh "命令" [超时秒数]

COMMAND="$1"
TIMEOUT="${2:-3}"  # 默认等待3秒

if [ -z "$COMMAND" ]; then
    echo "❌ 用法: $0 \"命令\" [超时秒数]"
    exit 1
fi

# 生成唯一的输出文件
OUTPUT_FILE="/tmp/iterm-capture-$(date +%s)-$RANDOM.txt"

# 发送命令到 iTerm（带重定向）
osascript <<EOF
tell application "iTerm"
    tell current session of current window
        write text "$COMMAND > $OUTPUT_FILE 2>&1"
    end tell
end tell
EOF

echo "✅ 命令已发送到 iTerm: $COMMAND"
echo "⏳ 等待 ${TIMEOUT} 秒..."

# 等待执行
sleep "$TIMEOUT"

# 读取输出
if [ -f "$OUTPUT_FILE" ]; then
    echo ""
    echo "📄 命令输出:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    cat "$OUTPUT_FILE"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # 清理临时文件
    rm "$OUTPUT_FILE"
else
    echo "❌ 未能捕获输出（文件不存在）"
    echo "   可能原因："
    echo "   1. 命令执行时间超过 $TIMEOUT 秒"
    echo "   2. 命令本身有错误"
    echo "   3. iTerm 窗口不存在"
fi
