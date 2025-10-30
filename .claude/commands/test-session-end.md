---
description: 测试SessionEnd hook的行为(不真正退出)
---

模拟SessionEnd hook的执行逻辑,测试是否能触发活动终端通知。

执行脚本:
!.claude/hooks/SessionEnd.sh '{"reason":"test"}'
