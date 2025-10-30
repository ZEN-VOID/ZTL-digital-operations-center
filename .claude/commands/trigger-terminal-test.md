---
description: 测试向活动终端发送命令的能力
---

执行终端控制测试：

!echo "开始测试..." > .claude/test-terminal-output.txt

!osascript -e 'tell application "iTerm" to tell current session of current window to write text "echo \"🎉 测试成功！这条命令来自Claude Code斜杠命令\""' 2>/dev/null || osascript -e 'tell application "Terminal" to do script "echo \"🎉 测试成功！这条命令来自Claude Code斜杠命令\"" in front window' 2>/dev/null || echo "⚠️ 无法发送到终端,但测试命令已执行"

!echo "测试完成 - $(date)" >> .claude/test-terminal-output.txt

测试已执行！请检查:
1. 你的终端(iTerm或Terminal)是否收到了测试消息
2. 查看 `.claude/test-terminal-output.txt` 文件确认执行记录
