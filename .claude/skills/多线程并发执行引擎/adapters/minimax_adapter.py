"""MiniMax Skill 适配器 - MiniMax MCP工具 (图片/音乐/视频/语音)"""

import time
from typing import Dict, Any

from ..scripts.core import SkillAdapter, TaskDefinition, TaskResult


class MinimaxAdapter(SkillAdapter):
    """MiniMax技能包适配器 - 调用MiniMax MCP工具"""

    def execute_task(self, task: TaskDefinition) -> TaskResult:
        """
        执行单个MiniMax任务

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
            api_params = params.get("api_params", {})
            use_prompt_optimizer = params.get("use_prompt_optimizer", False)

            # 根据任务类型调用不同的MCP工具
            if task_type == "text_to_image":
                result = self._execute_text_to_image(api_params, use_prompt_optimizer)
            elif task_type == "text_to_audio":
                result = self._execute_text_to_audio(api_params)
            elif task_type == "generate_video":
                result = self._execute_generate_video(api_params)
            elif task_type == "music_generation":
                result = self._execute_music_generation(api_params)
            else:
                raise ValueError(f"Unsupported task type: {task_type}")

            end_time = time.time()

            return TaskResult(
                task_id=task.task_id,
                status="success" if result.get("status") == "success" else "failed",
                start_time=start_time,
                end_time=end_time,
                duration=end_time - start_time,
                output_files=result.get("output_files", []),
                error_message=result.get("error"),
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

    def _execute_text_to_image(
        self,
        api_params: Dict[str, Any],
        use_optimizer: bool
    ) -> Dict[str, Any]:
        """执行图片生成任务 (需要通过Claude调用MCP工具)"""
        # 注意: 实际执行需要Claude调用 mcp__minimax-mcp__text_to_image
        # 这里返回模拟结果,实际使用时需要集成真实的MCP调用
        return {
            "status": "success",
            "output_files": [f"output/images/{api_params.get('model', 'image-01')}_result.png"],
            "message": "Image generated successfully (simulated)"
        }

    def _execute_text_to_audio(self, api_params: Dict[str, Any]) -> Dict[str, Any]:
        """执行语音生成任务"""
        return {
            "status": "success",
            "output_files": [f"output/audio/speech_result.mp3"],
            "message": "Audio generated successfully (simulated)"
        }

    def _execute_generate_video(self, api_params: Dict[str, Any]) -> Dict[str, Any]:
        """执行视频生成任务"""
        return {
            "status": "success",
            "output_files": [f"output/video/video_result.mp4"],
            "message": "Video generated successfully (simulated)"
        }

    def _execute_music_generation(self, api_params: Dict[str, Any]) -> Dict[str, Any]:
        """执行音乐生成任务"""
        return {
            "status": "success",
            "output_files": [f"output/music/music_result.mp3"],
            "message": "Music generated successfully (simulated)"
        }

    def validate_params(self, params: Dict[str, Any]) -> bool:
        """
        验证MiniMax任务参数

        Args:
            params: 任务参数

        Returns:
            bool: 是否有效
        """
        required = ["task_type", "api_params"]

        # 检查必需参数
        for key in required:
            if key not in params:
                return False

        # 验证task_type
        valid_task_types = [
            "text_to_image",
            "text_to_audio",
            "generate_video",
            "music_generation",
            "voice_clone",
            "voice_design"
        ]

        if params["task_type"] not in valid_task_types:
            return False

        return True

    def pre_execute_hook(self, task: TaskDefinition) -> None:
        """执行前钩子"""
        print(f"[MiniMax] 准备执行任务: {task.task_id}")
        print(f"[任务类型] {task.params.get('task_type')}")
        if task.params.get("use_prompt_optimizer"):
            print(f"[提示词优化] 已启用")

    def post_execute_hook(self, task: TaskDefinition, result: TaskResult) -> None:
        """执行后钩子"""
        if result.status == "success":
            print(f"[MiniMax] ✅ 任务完成: {task.task_id}")
            print(f"[输出路径] {result.output_files[0] if result.output_files else 'N/A'}")
        else:
            print(f"[MiniMax] ❌ 任务失败: {task.task_id}")
            print(f"[错误信息] {result.error_message}")
