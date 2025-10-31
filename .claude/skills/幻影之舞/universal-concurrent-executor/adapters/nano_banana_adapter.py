"""Nano-Banana Skill 适配器 - OpenRouter API (图片工作流)"""

import sys
from pathlib import Path
from typing import Dict, Any
import time

# 添加nano-banana到Python路径
nano_banana_path = Path(__file__).parent.parent.parent.parent.parent.parent / "plugins/创意组/skills/AIGC/nano-banana"
sys.path.insert(0, str(nano_banana_path))

from scripts.core_engine import NanoBananaEngine
from ..scripts.core import SkillAdapter, TaskDefinition, TaskResult


class NanoBananaAdapter(SkillAdapter):
    """Nano-Banana技能包适配器"""

    def __init__(self):
        """初始化适配器"""
        self.engine = NanoBananaEngine()

    def execute_task(self, task: TaskDefinition) -> TaskResult:
        """
        执行单个Nano-Banana任务

        Args:
            task: 任务定义

        Returns:
            TaskResult: 执行结果
        """
        start_time = time.time()

        try:
            # 解析任务参数
            params = task.params
            task_type = params.get("task_type")
            user_prompt = params.get("user_prompt")
            context = params.get("context", "")
            target_style = params.get("target_style", "")
            config = params.get("config", {})

            # 调用Nano-Banana核心引擎
            result = self.engine.execute_task(
                task_type=task_type,
                user_prompt=user_prompt,
                context=context,
                target_style=target_style,
                config=config
            )

            end_time = time.time()

            # 检查执行状态
            if result.get("status") == "success":
                return TaskResult(
                    task_id=task.task_id,
                    status="success",
                    start_time=start_time,
                    end_time=end_time,
                    duration=end_time - start_time,
                    output_files=[result.get("output_path")],
                    api_response=result
                )
            else:
                return TaskResult(
                    task_id=task.task_id,
                    status="failed",
                    start_time=start_time,
                    end_time=end_time,
                    duration=end_time - start_time,
                    error_message=result.get("error", "Unknown error"),
                    api_response=result
                )

        except Exception as e:
            end_time = time.time()
            return TaskResult(
                task_id=task.task_id,
                status="failed",
                start_time=start_time,
                end_time=end_time,
                duration=end_time - start_time,
                error_message=str(e)
            )

    def validate_params(self, params: Dict[str, Any]) -> bool:
        """
        验证Nano-Banana任务参数

        Args:
            params: 任务参数

        Returns:
            bool: 是否有效
        """
        required = ["task_type", "user_prompt"]

        # 检查必需参数
        for key in required:
            if key not in params:
                return False

        # 验证task_type
        valid_task_types = [
            "text-to-image",
            "image-to-image",
            "image-variation",
            "background-replacement",
            "upscale",
            "local-edit",
            "pose-angle-space",
            "style-transfer"
        ]

        if params["task_type"] not in valid_task_types:
            return False

        return True

    def pre_execute_hook(self, task: TaskDefinition) -> None:
        """执行前钩子"""
        print(f"[Nano-Banana] 准备执行任务: {task.task_id}")
        print(f"[任务类型] {task.params.get('task_type')}")
        print(f"[原始提示词] {task.params.get('user_prompt')[:100]}...")

    def post_execute_hook(self, task: TaskDefinition, result: TaskResult) -> None:
        """执行后钩子"""
        if result.status == "success":
            print(f"[Nano-Banana] ✅ 任务完成: {task.task_id}")
            print(f"[输出路径] {result.output_files[0] if result.output_files else 'N/A'}")
        else:
            print(f"[Nano-Banana] ❌ 任务失败: {task.task_id}")
            print(f"[错误信息] {result.error_message}")
