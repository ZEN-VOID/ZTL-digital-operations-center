#!/usr/bin/env python3
"""
Nano Banana API Client
基于Nano Banana模型的专业衍生图生成客户端
提供单张生成和批量处理功能
"""

import requests
import json
import base64
import uuid
import argparse
import asyncio
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any
import mimetypes


class NanoBananaClient:
    """Nano Banana API客户端 - 统一API调用和批量执行"""

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化客户端

        Args:
            api_key: OpenRouter API密钥,如果不提供则从环境变量读取
        """
        # API配置
        self.api_key = api_key or self._get_api_key()
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "google/gemini-2.5-flash-image-preview"

        # 站点信息
        self.site_url = "https://ztl-aigc-film-producer.com"
        self.site_name = "ZTL-AIGC-Film-Producer"

        # 路径配置
        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent.parent.parent
        self.output_base = project_root / "output"

        # 默认参数
        self.default_strength = 0.6
        self.timeout = 120

    def _get_api_key(self) -> str:
        """从环境变量获取API密钥"""
        import os
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError(
                "未找到API密钥。请设置环境变量OPENROUTER_API_KEY或在初始化时传入api_key参数"
            )
        return api_key

    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": self.site_url,
            "X-Title": self.site_name
        }

    def _convert_local_image_to_base64(self, image_path: str) -> Optional[str]:
        """
        将本地图片转换为base64格式

        Args:
            image_path: 本地图片路径

        Returns:
            base64格式的图片数据URL,失败返回None
        """
        try:
            # 处理file://协议
            if image_path.startswith("file://"):
                image_path = image_path[7:]

            # 转换为绝对路径
            path = Path(image_path)
            if not path.is_absolute():
                path = path.resolve()

            if not path.exists():
                print(f"图片文件不存在: {path}")
                return None

            # 读取图片并转换为base64
            with open(path, 'rb') as f:
                image_bytes = f.read()

            # 获取MIME类型
            mime_type, _ = mimetypes.guess_type(str(path))
            if not mime_type:
                mime_type = "image/png"

            # 转换为base64
            base64_data = base64.b64encode(image_bytes).decode('utf-8')
            return f"data:{mime_type};base64,{base64_data}"

        except Exception as e:
            print(f"转换图片为base64时出错: {e}")
            return None

    def _build_variation_prompt(
        self,
        keep_consistent: List[str],
        change_elements: List[str],
        prompt_weight: str
    ) -> str:
        """
        构建变体生成提示词

        Args:
            keep_consistent: 需要保持一致的元素列表
            change_elements: 需要改变的元素列表
            prompt_weight: 主要变化描述

        Returns:
            增强后的提示词
        """
        prompt_parts = []

        # 主要变化指令
        prompt_parts.append(f"Main Variation: {prompt_weight}")
        prompt_parts.append("")

        # 保持一致的元素
        if keep_consistent:
            prompt_parts.append("Keep Consistent:")
            for element in keep_consistent:
                prompt_parts.append(f"- {element}")
            prompt_parts.append("")

        # 需要改变的元素
        if change_elements:
            prompt_parts.append("Change Elements:")
            for element in change_elements:
                prompt_parts.append(f"- {element}")
            prompt_parts.append("")

        # 质量要求
        prompt_parts.extend([
            "Quality Requirements:",
            "- Maintain visual consistency with reference image",
            "- Keep scene, lighting, and color tone consistent",
            "- Professional photography quality",
            "- Natural and seamless variations",
            "- Commercial production standard"
        ])

        return "\n".join(prompt_parts)

    def _save_base64_image(self, base64_data: str, output_path: Path) -> bool:
        """
        保存base64图像到文件

        Args:
            base64_data: base64编码的图像数据
            output_path: 输出文件路径

        Returns:
            保存是否成功
        """
        try:
            # 解析base64数据
            if base64_data.startswith('data:image/'):
                _, base64_content = base64_data.split(',', 1)
            else:
                base64_content = base64_data

            # 解码并保存
            image_bytes = base64.b64decode(base64_content)

            # 确保目录存在
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # 保存文件
            with open(output_path, 'wb') as f:
                f.write(image_bytes)

            return True

        except Exception as e:
            print(f"保存图像时出错: {e}")
            return False

    def _extract_images_from_response(self, response_data: Dict[str, Any]) -> List[str]:
        """
        从响应中提取图像数据

        Args:
            response_data: API响应数据

        Returns:
            图像base64数据列表
        """
        images = []

        try:
            choices = response_data.get("choices", [])
            if choices:
                message = choices[0].get("message", {})

                # 检查message中的images字段
                message_images = message.get("images", [])
                if message_images:
                    for img in message_images:
                        if isinstance(img, dict) and "image_url" in img:
                            image_url = img["image_url"]
                            if isinstance(image_url, dict) and "url" in image_url:
                                images.append(image_url["url"])

                # 也检查content中的图像数据
                content = message.get("content", "")
                if "data:image/" in content:
                    import re
                    pattern = r'data:image/[^;]+;base64,[A-Za-z0-9+/=]+'
                    matches = re.findall(pattern, content)
                    images.extend(matches)

        except Exception as e:
            print(f"提取图像时出错: {e}")

        return images

    def generate(
        self,
        reference_image: str,
        variation_instruction: Dict[str, Any],
        output_path: Optional[Path] = None
    ) -> Dict[str, Any]:
        """
        生成单张衍生图像

        Args:
            reference_image: 参考主图路径
            variation_instruction: 变体指令字典,包含:
                - keep_consistent: 保持一致的元素列表
                - change_elements: 需要改变的元素列表
                - nano_banana_parameters: API参数
                    - strength: 变体强度 (0.4-0.8)
                    - prompt_weight: 主要变化描述
            output_path: 输出路径(可选,默认自动生成)

        Returns:
            生成结果字典
        """
        task_id = str(uuid.uuid4())
        start_time = datetime.now()

        try:
            # 解析变体指令
            keep_consistent = variation_instruction.get("keep_consistent", [])
            change_elements = variation_instruction.get("change_elements", [])
            nano_params = variation_instruction.get("nano_banana_parameters", {})

            # 提取参数
            strength = nano_params.get("strength", self.default_strength)
            prompt_weight = nano_params.get("prompt_weight", "Generate variation")

            # 构建增强提示词
            enhanced_prompt = self._build_variation_prompt(
                keep_consistent, change_elements, prompt_weight
            )

            # 转换参考图为base64
            reference_base64 = self._convert_local_image_to_base64(reference_image)
            if not reference_base64:
                return {
                    "success": False,
                    "task_id": task_id,
                    "error": "无法读取参考图像",
                    "details": f"参考图路径: {reference_image}"
                }

            # 构建请求
            headers = self._get_headers()
            messages = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": enhanced_prompt},
                    {"type": "image_url", "image_url": {"url": reference_base64}}
                ]
            }]

            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 4000,
                "temperature": 0.7
            }

            # 发送请求
            response = requests.post(
                self.base_url,
                headers=headers,
                json=data,
                timeout=self.timeout
            )

            if response.status_code == 200:
                result = response.json()

                # 提取图像
                images = self._extract_images_from_response(result)

                # 确定输出路径
                if not output_path:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"derivative_{timestamp}_{task_id[:8]}.png"
                    output_path = self.output_base / "temp" / filename

                # 保存图像
                image_paths = []
                for i, image_data in enumerate(images):
                    if len(images) > 1:
                        img_path = output_path.parent / f"{output_path.stem}_{i+1}{output_path.suffix}"
                    else:
                        img_path = output_path

                    if self._save_base64_image(image_data, img_path):
                        image_paths.append(str(img_path))

                # 保存元数据
                metadata = {
                    "task_id": task_id,
                    "reference_image": reference_image,
                    "variation_instruction": variation_instruction,
                    "enhanced_prompt": enhanced_prompt,
                    "timestamp": datetime.now().isoformat(),
                    "api_response": result
                }

                metadata_path = output_path.parent / f"{output_path.stem}_metadata.json"
                with open(metadata_path, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, ensure_ascii=False, indent=2)

                end_time = datetime.now()
                processing_time = (end_time - start_time).total_seconds()

                return {
                    "success": True,
                    "task_id": task_id,
                    "message": "衍生图生成成功",
                    "image_paths": image_paths,
                    "metadata_path": str(metadata_path),
                    "processing_time": processing_time
                }
            else:
                return {
                    "success": False,
                    "task_id": task_id,
                    "error": f"API调用失败: {response.status_code}",
                    "details": response.text
                }

        except Exception as e:
            return {
                "success": False,
                "task_id": task_id,
                "error": "生成异常",
                "details": str(e)
            }

    async def execute_batch(
        self,
        config_file: str,
        max_concurrent: int = 2,
        retry_attempts: int = 3
    ) -> Dict[str, Any]:
        """
        批量执行生成任务

        Args:
            config_file: 配置文件路径
            max_concurrent: 最大并发数
            retry_attempts: 失败重试次数

        Returns:
            批量执行结果
        """
        # 加载配置
        config_path = Path(config_file)
        if not config_path.exists():
            return {"success": False, "error": f"配置文件不存在: {config_file}"}

        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # 提取配置
        plan_id = config.get("plan_id", "unknown")
        batches = config.get("batches", [])

        # 统计
        total_tasks = sum(len(batch.get("tasks", [])) for batch in batches)
        completed = 0
        failed = 0
        results = []

        print(f"\n开始批量生成: {plan_id}")
        print(f"总任务数: {total_tasks}")

        # 执行所有批次
        for batch in batches:
            tasks = batch.get("tasks", [])

            # 并发执行任务
            for i in range(0, len(tasks), max_concurrent):
                batch_tasks = tasks[i:i + max_concurrent]
                task_coroutines = [
                    self._execute_task_with_retry(task, retry_attempts)
                    for task in batch_tasks
                ]
                batch_results = await asyncio.gather(*task_coroutines)

                for result in batch_results:
                    results.append(result)
                    if result["success"]:
                        completed += 1
                    else:
                        failed += 1

                print(f"进度: {completed + failed}/{total_tasks}")

        # 生成报告
        report = {
            "plan_id": plan_id,
            "total_tasks": total_tasks,
            "completed": completed,
            "failed": failed,
            "success_rate": f"{(completed / total_tasks * 100):.2f}%" if total_tasks > 0 else "0%",
            "results": results
        }

        # 保存报告
        report_path = Path(config.get("output_config", {}).get("base_path", "output")) / "batch_report.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"\n批量生成完成!")
        print(f"成功: {completed}, 失败: {failed}")
        print(f"报告保存至: {report_path}")

        return report

    async def _execute_task_with_retry(
        self,
        task: Dict[str, Any],
        retry_attempts: int
    ) -> Dict[str, Any]:
        """执行单个任务(带重试)"""
        task_id = task.get("task_id")
        reference_image = task.get("reference_image")
        variation_instruction = task.get("variation_instruction")

        for attempt in range(retry_attempts):
            try:
                result = self.generate(reference_image, variation_instruction)
                if result["success"]:
                    result["task_id"] = task_id
                    result["attempts"] = attempt + 1
                    return result
                else:
                    if attempt < retry_attempts - 1:
                        await asyncio.sleep(2 ** attempt)  # 指数退避
            except Exception as e:
                if attempt == retry_attempts - 1:
                    return {
                        "success": False,
                        "task_id": task_id,
                        "error": str(e),
                        "attempts": retry_attempts
                    }
                await asyncio.sleep(2 ** attempt)

        return {
            "success": False,
            "task_id": task_id,
            "error": "达到最大重试次数",
            "attempts": retry_attempts
        }


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='Nano Banana API客户端')
    subparsers = parser.add_subparsers(dest='command', help='命令')

    # 单张生成命令
    gen_parser = subparsers.add_parser('generate', help='生成单张衍生图')
    gen_parser.add_argument('--reference', required=True, help='参考主图路径')
    gen_parser.add_argument('--keep', required=True, help='保持一致的元素(逗号分隔)')
    gen_parser.add_argument('--change', required=True, help='需要改变的元素(逗号分隔)')
    gen_parser.add_argument('--strength', type=float, default=0.6, help='变化强度(0.4-0.8)')
    gen_parser.add_argument('--output', help='输出路径')

    # 批量生成命令
    batch_parser = subparsers.add_parser('batch', help='批量生成')
    batch_parser.add_argument('--config', required=True, help='配置文件路径')
    batch_parser.add_argument('--parallel', type=int, default=2, help='最大并发数')

    args = parser.parse_args()

    client = NanoBananaClient()

    if args.command == 'generate':
        # 单张生成
        variation = {
            "keep_consistent": [x.strip() for x in args.keep.split(',')],
            "change_elements": [x.strip() for x in args.change.split(',')],
            "nano_banana_parameters": {
                "strength": args.strength,
                "prompt_weight": args.change
            }
        }

        output_path = Path(args.output) if args.output else None
        result = client.generate(args.reference, variation, output_path)

        if result["success"]:
            print(f"✅ 生成成功: {result['image_paths']}")
        else:
            print(f"❌ 生成失败: {result['error']}")
            sys.exit(1)

    elif args.command == 'batch':
        # 批量生成
        result = asyncio.run(client.execute_batch(args.config, args.parallel))

        if result.get("failed", 0) > 0:
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
