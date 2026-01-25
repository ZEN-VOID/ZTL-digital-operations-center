#!/usr/bin/env python3
"""
Nano Banana API - E5 Derivative Image Generation Template
专为E5智能体（Nano Banana衍生图生成专家）设计的API模板
基于参考主图生成视觉一致的衍生图像，保持场景/光照/色调一致性

核心功能：
- 图生图：基于参考主图生成衍生图
- 变体控制：精确控制保持一致vs改变的元素
- 批量支持：配合execute引擎实现批量处理
"""

import requests
import json
import base64
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
import os


class NanoBananaAPI:
    """Nano Banana API 客户端 - E5专用版本"""

    def __init__(self):
        # OpenRouter配置
        self.api_key = "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"
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "google/gemini-2.5-flash-image-preview"

        # 站点信息
        self.site_url = "https://ztl-aigc-film-producer.com"
        self.site_name = "ZTL-AIGC-Film-Producer"

        # 路径配置（相对于项目根目录）
        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent.parent
        self.output_base = project_root / "output"

        # E5默认参数
        self.default_strength = 0.6  # 默认变体强度
        self.default_guidance_scale = 7.5
        self.default_num_inference_steps = 50

    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": self.site_url,
            "X-Title": self.site_name
        }

    def _build_messages(self, prompt: str, image_urls: List[str]) -> List[Dict[str, Any]]:
        """
        构建消息内容

        Args:
            prompt: 文本提示词
            image_urls: 图像URL列表（至少包含1张参考主图）

        Returns:
            消息列表
        """
        content = []

        # 添加文本内容
        content.append({
            "type": "text",
            "text": prompt
        })

        # 添加图像内容（参考主图）
        for image_url in image_urls:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": image_url
                }
            })

        return [{
            "role": "user",
            "content": content
        }]

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
                header, base64_content = base64_data.split(',', 1)
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

                # 也检查content中的图像数据（备用方法）
                content = message.get("content", "")
                if "data:image/" in content:
                    import re
                    pattern = r'data:image/[^;]+;base64,[A-Za-z0-9+/=]+'
                    matches = re.findall(pattern, content)
                    images.extend(matches)

        except Exception as e:
            print(f"提取图像时出错: {e}")

        return images

    def _convert_local_image_to_base64(self, image_path: str) -> Optional[str]:
        """
        将本地图片转换为base64格式

        Args:
            image_path: 本地图片路径

        Returns:
            base64格式的图片数据URL，失败返回None
        """
        try:
            import mimetypes

            # 处理file://协议
            if image_path.startswith("file://"):
                image_path = image_path[7:]

            # 转换为绝对路径
            if not Path(image_path).is_absolute():
                image_path = Path(image_path).resolve()
            else:
                image_path = Path(image_path)

            if not image_path.exists():
                print(f"图片文件不存在: {image_path}")
                return None

            # 读取图片并转换为base64
            with open(image_path, 'rb') as f:
                image_bytes = f.read()

            # 获取MIME类型
            mime_type, _ = mimetypes.guess_type(str(image_path))
            if not mime_type:
                mime_type = "image/png"  # 默认PNG

            # 转换为base64
            base64_data = base64.b64encode(image_bytes).decode('utf-8')
            return f"data:{mime_type};base64,{base64_data}"

        except Exception as e:
            print(f"转换图片为base64时出错: {e}")
            return None

    def _build_variation_prompt(self,
                               keep_consistent: List[str],
                               change_elements: List[str],
                               prompt_weight: str) -> str:
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

    def generate_derivative_image(self,
                                 reference_image_path: str,
                                 variation_instruction: Dict[str, Any],
                                 output_path: Optional[Path] = None,
                                 **kwargs) -> Dict[str, Any]:
        """
        生成衍生图像 - E5核心方法

        Args:
            reference_image_path: 参考主图路径
            variation_instruction: 变体指令字典，包含：
                - keep_consistent: 保持一致的元素列表
                - change_elements: 需要改变的元素列表
                - nano_banana_parameters: API参数
                    - strength: 变体强度 (0.1-1.0)
                    - prompt_weight: 主要变化描述
                    - negative_prompt: 负面提示词（可选）
                    - guidance_scale: 引导比例（可选）
                    - num_inference_steps: 推理步数（可选）
            output_path: 输出路径（可选，默认自动生成）
            **kwargs: 其他参数

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
            negative_prompt = nano_params.get("negative_prompt", "low quality, blurry, noise, distortion")
            guidance_scale = nano_params.get("guidance_scale", self.default_guidance_scale)
            num_inference_steps = nano_params.get("num_inference_steps", self.default_num_inference_steps)

            # 构建增强提示词
            enhanced_prompt = self._build_variation_prompt(
                keep_consistent, change_elements, prompt_weight
            )

            # 转换参考图为base64
            reference_base64 = self._convert_local_image_to_base64(reference_image_path)
            if not reference_base64:
                return {
                    "success": False,
                    "task_id": task_id,
                    "error": "无法读取参考图像",
                    "details": f"参考图路径: {reference_image_path}"
                }

            # 构建请求
            headers = self._get_headers()
            messages = self._build_messages(enhanced_prompt, [reference_base64])

            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 4000,
                "temperature": kwargs.get("temperature", 0.7),
                # 注意：以下参数为示意，实际API可能不支持
                # "strength": strength,
                # "guidance_scale": guidance_scale,
                # "num_inference_steps": num_inference_steps
            }

            # 发送请求
            response = requests.post(
                self.base_url,
                headers=headers,
                json=data,
                timeout=120
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
                    "reference_image": reference_image_path,
                    "variation_instruction": variation_instruction,
                    "parameters": {
                        "strength": strength,
                        "guidance_scale": guidance_scale,
                        "num_inference_steps": num_inference_steps
                    },
                    "enhanced_prompt": enhanced_prompt,
                    "timestamp": datetime.now().isoformat(),
                    "api_response": result
                }

                metadata_path = output_path.parent / f"{output_path.stem}_metadata.json"
                metadata_path.parent.mkdir(parents=True, exist_ok=True)

                with open(metadata_path, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, ensure_ascii=False, indent=2)

                end_time = datetime.now()
                processing_time = (end_time - start_time).total_seconds()

                return {
                    "success": True,
                    "task_id": task_id,
                    "message": "E5衍生图生成成功",
                    "images": images,
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


# 便捷函数
def generate_derivative(reference_image: str, variation_instruction: Dict[str, Any], **kwargs):
    """E5衍生图生成便捷函数"""
    api = NanoBananaAPI()
    return api.generate_derivative_image(reference_image, variation_instruction, **kwargs)


# 测试代码
def test_derivative_generation():
    """测试衍生图生成功能"""
    print("🎨 测试E5衍生图生成功能...")

    # 测试案例（需要实际的参考图路径）
    test_case = {
        "reference_image_path": "path/to/reference/shot_001.png",
        "variation_instruction": {
            "keep_consistent": [
                "办公室环境",
                "金色阳光窗户",
                "暖色调整体氛围"
            ],
            "change_elements": [
                "角色从背影改为正面",
                "景别从Wide Shot改为Medium Shot"
            ],
            "nano_banana_parameters": {
                "strength": 0.6,
                "prompt_weight": "保持办公室环境和金色阳光，角色改为正面中景"
            }
        }
    }

    result = generate_derivative(**test_case)

    if result["success"]:
        print(f"✅ 生成成功: {len(result['image_paths'])} 张图片")
        for path in result["image_paths"]:
            print(f"   📁 {path}")
        print(f"   📄 元数据: {result['metadata_path']}")
    else:
        print(f"❌ 生成失败: {result['error']}")


def main():
    """主函数 - 演示用法"""
    print("🍌 Nano Banana API - E5衍生图生成模板")
    print("=" * 60)
    print("\n⚠️  此模板需配合execute引擎和执行计划使用")
    print("   执行计划路径: api/plans/nano-banana/")
    print("   执行引擎: api/projects/nano-banana-api/nano-banana-execute.py")
    print("\n" + "=" * 60)

    # 测试衍生图生成（需要实际参考图）
    # test_derivative_generation()

    print("\n✅ E5专用API模板已加载")
    print("📋 支持的核心方法: generate_derivative_image()")


if __name__ == "__main__":
    main()
