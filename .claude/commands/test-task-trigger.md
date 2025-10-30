---
description: 测试触发VS Code Task的能力
---

请执行以下步骤测试VS Code Tasks触发:

1. 使用Bash工具执行VS Code Task命令:
```bash
open -a "Visual Studio Code" && osascript -e 'tell application "Visual Studio Code" to activate' && sleep 1 && osascript -e 'tell application "System Events" to keystroke "p" using {command down, shift down}' && sleep 0.5 && osascript -e 'tell application "System Events" to keystroke "Tasks: Run Task"' && osascript -e 'tell application "System Events" to keystroke return'
```

2. 创建触发证明文件:
```bash
echo "Task触发测试 - $(date)" > .claude/test-task-triggered.txt
```

3. 报告执行结果:
   - 是否成功打开VS Code命令面板
   - 是否创建了证明文件
   - 任何错误信息
