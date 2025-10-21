#!/usr/bin/env python3
"""
Stop Hook Handler - 使用fish895623/claude-hook库
功能: 智能检测任务状态，自动决定是否继续
"""

import sys
import json
from pathlib import Path

# 添加claude_hooks库到路径
sys.path.insert(0, str(Path(__file__).parent / "claude-hook-system"))

from claude_hooks.core.parser import parse_hook_event
from claude_hooks.core.events import HookResponse, StopEvent

def has_pending_tasks(transcript_path) -> tuple:
    """检测是否有未完成的任务"""
    try:
        if not Path(transcript_path).exists():
            return False, ""

        # 读取最近的transcript内容
        with open(transcript_path, 'r', encoding='utf-8') as f:
            # 只读取最后5000行以提高性能
            lines = f.readlines()
            recent_content = ''.join(lines[-5000:])

        # 检测TodoList中的未完成任务
        pending_count = recent_content.count('[pending]')
        in_progress_count = recent_content.count('[in_progress]')

        if pending_count > 0 or in_progress_count > 0:
            return True, f"检测到TodoList中还有 {pending_count} 个待办任务和 {in_progress_count} 个进行中任务"

        # 检测其他未完成标志
        unfinished_markers = [
            "接下来",
            "下一步",
            "然后",
            "继续",
        ]

        # 只检查最后100行以减少误触发
        last_100_lines = ''.join(lines[-100:])
        for marker in unfinished_markers:
            if marker in last_100_lines:
                return True, f"检测到未完成标识: '{marker}'"

        return False, ""

    except Exception as e:
        # 出错时不阻止停止
        print(f"Error checking tasks: {e}", file=sys.stderr)
        return False, ""

def main():
    try:
        # 读取stdin中的JSON事件
        event_json = sys.stdin.read()

        # 使用Pydantic解析事件（类型安全）
        event = parse_hook_event(event_json)

        # 确认是Stop事件
        if not isinstance(event, StopEvent):
            response = HookResponse.continue_response("Not a Stop event")
            print(response.to_json())
            return

        # 防止无限循环：如果已经是通过Stop hook继续的，不再继续
        if event.stop_hook_active:
            response = HookResponse.continue_response("Stop hook already active, allowing stop")
            print(response.to_json())
            return

        # 检查是否有未完成的任务
        has_tasks, reason = has_pending_tasks(event.transcript_path)

        if has_tasks:
            # 阻止停止，继续执行
            response = HookResponse.block_response(
                f"🔄 任务未完成，自动继续执行\n\n原因: {reason}\n\n请继续完成所有任务，逐个标记为completed。"
            )
            print(response.to_json())
        else:
            # 允许停止
            response = HookResponse.continue_response("✅ 所有任务已完成，允许停止")
            print(response.to_json())

    except Exception as e:
        # 出错时允许停止，避免阻塞
        print(f"Error in stop handler: {e}", file=sys.stderr)
        response = HookResponse.continue_response("Error occurred, allowing stop")
        print(response.to_json())

if __name__ == "__main__":
    main()
