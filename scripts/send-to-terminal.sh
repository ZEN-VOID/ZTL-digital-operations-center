#!/bin/bash
# 通用终端命令发送脚本
# 支持: Terminal.app (系统自带) + iTerm2 (可选)

COMMAND="$1"

if [ -z "$COMMAND" ]; then
    echo "❌ 错误: 请提供要发送的命令"
    echo "用法: $0 \"命令内容\""
    exit 1
fi

# 策略1: 尝试 iTerm2 (如果已安装)
if osascript -e 'tell application "iTerm" to exists' 2>/dev/null | grep -q "true"; then
    # 确保 iTerm2 有窗口
    RESULT=$(osascript -e 'tell application "iTerm"' \
              -e '  if (count of windows) = 0 then' \
              -e '    create window with default profile' \
              -e '  end if' \
              -e '  tell current session of current window' \
              -e "    write text \"$COMMAND\"" \
              -e '  end tell' \
              -e 'end tell' 2>&1)

    if [ $? -eq 0 ]; then
        echo "✅ [iTerm2] 已发送: $COMMAND"
        exit 0
    fi
fi

# 策略2: 降级到 Terminal.app (系统自带)
RESULT=$(osascript -e "tell application \"Terminal\"" \
          -e "  if (count of windows) = 0 then" \
          -e "    do script \"$COMMAND\"" \
          -e "  else" \
          -e "    do script \"$COMMAND\" in front window" \
          -e "  end if" \
          -e "end tell" 2>&1)

if [ $? -eq 0 ]; then
    echo "✅ [Terminal] 已发送: $COMMAND"
    exit 0
fi

# 策略3: 全部失败
echo "❌ 无法发送到终端应用"
exit 1
