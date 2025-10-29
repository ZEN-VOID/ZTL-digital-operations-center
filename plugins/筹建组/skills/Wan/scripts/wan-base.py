#!/usr/bin/env python3
"""
通义万相2.5 I2V API - E8 Image-to-Video Generation Template
专为E8智能体（图生视频专家）设计的通义万相API模板
基于图片生成高质量动态视频，支持自动配音、音频文件导入、视频特效等高级功能

核心功能：
- 图生视频：基于单张图片生成动态视频
- 音频模式：自动配音 / 自定义音频 / 无声视频
- 视频特效：动态光效、运动模糊、色彩分级
- 反向提示词：避免不想要的效果
- 异步任务处理：提交任务 → 轮询状态 → 下载视频
- 批量支持：配合execute引擎实现批量处理
"""

import requests
import json
import time
import base64
import uuid
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
import sys
from dotenv import load_dotenv

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 导入url-end-to-end图片上传器（统一云存储接口）
try:
    from ....模块.url_end_to_end.scripts import ImageUploader
except ImportError:
    ImageUploader = None  # 可选依赖

# 导入提示词优化器（2025最佳实践）
try:
    from .prompt_optimizer import PromptOptimizer
except ImportError:
    PromptOptimizer = None  # 可选依赖


# ========== 内置 API Key 管理器 ==========
class WanAPIManager:
    """
    通义万相 API Key 管理器

    功能:
    - 从 .env 读取 API Key
    - 提供标准请求头
    - 配置验证
    """

    def __init__(self, env_path: Optional[Path] = None):
        """
        初始化 API Key 管理器

        Args:
            env_path: .env 文件路径（可选，默认为项目根目录）
        """
        if env_path is None:
            # 从当前skill目录向上查找项目根目录的.env
            current_dir = Path(__file__).parent
            env_path = current_dir.parent.parent.parent.parent / '.env'

        self.env_path = env_path
        load_dotenv(self.env_path)

        # 加载配置
        self.api_key = os.getenv('ALIYUN_API_KEY') or os.getenv('DASHSCOPE_API_KEY')

        if not self.api_key:
            raise ValueError(
                "配置错误: 请在 .env 文件中设置 ALIYUN_API_KEY 或 DASHSCOPE_API_KEY\n"
                "获取API Key: https://dashscope.console.aliyun.com/"
            )

    def get_api_key(self) -> str:
        """获取 API Key"""
        return self.api_key

    def get_headers(self) -> Dict[str, str]:
        """
        获取完整的 API 请求头

        Returns:
            包含 Authorization 的请求头字典
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-DashScope-Async": "enable"  # 启用异步模式
        }

    def is_configured(self) -> bool:
        """检查 API Key 是否已配置"""
        return self.api_key is not None and len(self.api_key) > 0

    def get_config_info(self) -> Dict[str, any]:
        """获取配置信息（隐藏敏感数据）"""
        if not self.api_key:
            return {
                "configured": False,
                "api_key": None
            }

        # 显示前8位和后4位
        masked_key = f"{self.api_key[:8]}...{self.api_key[-4:]}"

        return {
            "configured": True,
            "api_key": masked_key,
            "key_length": len(self.api_key)
        }
# ========== API Key 管理器结束 ==========


class WanAPIClient:
    """通义万相2.5 I2V API 客户端 - E8专用版本"""

    def __init__(self,
                 endpoint: str = "https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis",
                 query_endpoint: str = "https://dashscope.aliyuncs.com/api/v1/tasks",
                 model: str = "wan2.5-i2v-preview"):
        """
        初始化通义万相API客户端

        Args:
            endpoint: 图生视频API端点
            query_endpoint: 任务查询API端点
            model: 使用的模型（wanx2.5-i2v-preview）
        """
        # API配置
        self.endpoint = endpoint
        self.query_endpoint = query_endpoint
        self.model = model

        # API Key管理器
        self.api_manager = WanAPIManager()

        # 路径配置（相对于项目根目录）
        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent.parent.parent.parent.parent
        self.output_base = project_root / "output"

        # 初始化图片上传器（url-end-to-end集成）
        try:
            env_path = project_root / ".env"
            self.cos_uploader = ImageUploader(storage="cos", env_path=env_path)
        except Exception as e:
            print(f"⚠️  图片上传器初始化失败: {e}")
            print(f"   将需要手动上传图片或使用Base64模式（设置use_base64=true）")
            self.cos_uploader = None

        # 初始化提示词优化器（2025最佳实践）
        if PromptOptimizer:
            self.prompt_optimizer = PromptOptimizer()
            print(f"✅ 提示词优化器已启用（2025最佳实践）")
        else:
            self.prompt_optimizer = None
            print(f"⚠️  提示词优化器未加载，将使用原始提示词")

        # E8默认参数（通义万相）
        self.default_video_duration = 5  # 5秒或10秒
        self.default_fps = 24  # 24或30
        self.default_resolution = "1280x720"  # 1280x720, 1920x1080, 640x480
        self.default_query_interval = 5  # 查询间隔（秒）
        self.default_max_wait_time = 600  # 最大等待时间（秒）

    def _get_headers(self) -> Dict[str, str]:
        """
        获取请求头（包含API Key认证）

        Returns:
            请求头字典
        """
        return self.api_manager.get_headers()

    def _convert_image_to_base64(self, image_path: str) -> Optional[str]:
        """
        将本地图片转换为base64格式

        Args:
            image_path: 本地图片路径

        Returns:
            base64格式的图片数据，失败返回None
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

            # 转换为base64（不使用data URI格式，直接返回base64字符串）
            base64_str = base64.b64encode(image_bytes).decode('utf-8')
            return base64_str

        except Exception as e:
            print(f"转换图片为base64时出错: {e}")
            return None

    def _load_audio_file(self, audio_path: str) -> Optional[str]:
        """
        读取音频文件并转换为base64格式

        Args:
            audio_path: 音频文件路径

        Returns:
            base64格式的音频数据，失败返回None
        """
        try:
            # 转换为绝对路径
            if not Path(audio_path).is_absolute():
                audio_path = Path(audio_path).resolve()
            else:
                audio_path = Path(audio_path)

            if not audio_path.exists():
                print(f"音频文件不存在: {audio_path}")
                return None

            # 读取音频并转换为base64
            with open(audio_path, 'rb') as f:
                audio_bytes = f.read()

            base64_data = base64.b64encode(audio_bytes).decode('utf-8')
            return base64_data

        except Exception as e:
            print(f"读取音频文件时出错: {e}")
            return None

    def _prepare_audio_config(self, audio_config: Dict[str, Any]) -> Optional[bool]:
        """
        准备音频配置

        根据阿里云官方文档，parameters.audio参数只支持boolean类型：
        - true: 自动添加音频（API会自动生成背景音乐）
        - false: 不添加音频

        注意：WanX 2.5 API不支持自定义TTS配置（如voice_id、caption_text等）
        如果需要自定义音频，应该在视频生成后通过后处理添加

        Args:
            audio_config: 音频配置字典

        Returns:
            bool: True表示启用音频，False表示禁用音频
            None: 不设置audio参数（使用API默认值）
        """
        enable_audio = audio_config.get("enable_audio", False)

        if not enable_audio:
            # 禁用音频
            return False

        # 启用音频（API会自动生成背景音乐）
        return True

    def _build_request_payload(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        构建API请求载荷

        Args:
            task_data: 任务数据，包含input_data和parameters

        Returns:
            请求载荷字典
        """
        input_data = task_data.get("input_data", {})
        params = task_data.get("parameters", {})

        # ========== 2025最佳实践: 提示词优化 ==========
        original_prompt = params.get("prompt", "")

        if self.prompt_optimizer and original_prompt:
            print(f"\n🔍 应用2025最佳实践: 提示词优化")
            print(f"   原始提示词长度: {len(original_prompt)}字符")

            # 准备优化参数
            style = params.get("style", "")
            use_composer = params.get("use_composer", False)
            composer_config = params.get("composer", None) if use_composer else None
            use_qwen_image = params.get("use_qwen_image", False)

            # 执行优化
            optimization_result = self.prompt_optimizer.optimize_prompt(
                raw_prompt=original_prompt,
                style=style,
                use_composer=use_composer,
                composer_config=composer_config,
                use_qwen_image=use_qwen_image
            )

            # 使用优化后的提示词
            optimized_prompt = optimization_result["optimized_prompt"]
            char_count_bash = optimization_result["char_count_bash"]
            checks = optimization_result["checks"]
            warnings = optimization_result["warnings"]

            print(f"   优化后提示词长度: {char_count_bash}字符 (Bash验证)")

            # 显示检查结果
            print(f"   ✅ 质量检查:")
            print(f"      - 字符范围 (1500-2000): {'✓' if checks['char_range_valid'] else '✗'}")
            if style:
                print(f"      - 风格关键词前置 (前20字符): {'✓' if checks['style_keyword_positioned'] else '✗'}")
            if use_composer:
                print(f"      - Composer配置完整: {'✓' if checks['composer_complete'] else '✗'}")
            if use_qwen_image:
                print(f"      - Qwen-Image优化: {'✓' if checks['qwen_image_optimized'] else '✗'}")

            # 显示警告信息
            if warnings:
                print(f"   ⚠️  警告:")
                for warning in warnings:
                    print(f"      - {warning}")

            # 更新params中的提示词
            params["prompt"] = optimized_prompt
            print(f"   ✅ 提示词优化完成\n")

        # 基础载荷
        payload = {
            "model": params.get("model", self.model),
            "input": {},
            "parameters": {}
        }

        # 处理输入图片
        use_base64 = input_data.get("use_base64", False)

        if "image_url" in input_data and input_data["image_url"]:
            # URL模式（包括http/https URL和data URI）
            payload["input"]["img_url"] = input_data["image_url"]

        elif "image_path" in input_data and input_data["image_path"]:
            # 本地文件模式
            if use_base64:
                # Base64模式（使用img_url字段，值为data URI格式）
                base64_data = self._convert_image_to_base64(input_data["image_path"])
                if base64_data:
                    # 检测图片MIME类型
                    import mimetypes
                    mime_type, _ = mimetypes.guess_type(input_data["image_path"])
                    if not mime_type or not mime_type.startswith('image/'):
                        mime_type = 'image/png'  # 默认PNG
                    # 使用data URI格式
                    payload["input"]["img_url"] = f"data:{mime_type};base64,{base64_data}"
                else:
                    raise ValueError(f"无法加载图片: {input_data['image_path']}")
            else:
                # 自动上传模式（url-end-to-end集成）
                if not self.cos_uploader:
                    raise ValueError(
                        "图片上传器未初始化。请使用以下方式之一：\n"
                        "1. 设置use_base64=true使用Base64模式\n"
                        "2. 提供image_url（CDN URL）\n"
                        "3. 配置.env文件中的COS环境变量以启用自动上传"
                    )

                print(f"📤 检测到本地图片路径，正在上传到COS...")
                cdn_url = self.cos_uploader.upload_image(
                    input_data["image_path"],
                    prefix="wan-images"
                )
                payload["input"]["img_url"] = cdn_url
                print(f"✅ COS上传成功，使用CDN URL")

        # 添加提示词（应该在input字段下）
        if "prompt" in params:
            payload["input"]["prompt"] = params["prompt"]

        # 添加negative_prompt（应该在input字段下）
        if "negative_prompt" in params:
            payload["input"]["negative_prompt"] = params["negative_prompt"]

        # 添加视频参数（在parameters字段下）
        # duration而不是video_duration
        payload["parameters"]["duration"] = params.get("video_duration", self.default_video_duration)

        # 转换resolution格式：1280x720 -> 720P
        resolution = params.get("resolution", self.default_resolution)
        if "x" in resolution.lower():
            # 从像素分辨率转换为标准格式
            height = resolution.split('x')[1]
            resolution = f"{height}P"
        payload["parameters"]["resolution"] = resolution

        # 处理音频配置
        if "audio_config" in params:
            audio_cfg = self._prepare_audio_config(params["audio_config"])
            if audio_cfg is not None:
                payload["parameters"]["audio"] = audio_cfg

        # 处理视频特效
        if "effects" in params and params["effects"].get("enable_effects", False):
            effects = params["effects"]
            payload["parameters"]["effects"] = {
                "type": effects.get("effect_type", "dynamic_light"),
                "intensity": effects.get("effect_intensity", 0.7)
            }

        return payload

    def submit_task(self, task_data: Dict[str, Any], retry_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        提交图生视频任务

        Args:
            task_data: 任务数据，包含input_data和parameters
            retry_config: 重试配置（可选）

        Returns:
            API响应数据，包含task_id
        """
        try:
            # 构建请求
            headers = self._get_headers()
            payload = self._build_request_payload(task_data)

            # 调试：打印payload结构（不包含base64数据）
            debug_payload = payload.copy()
            if "input" in debug_payload and "img_url" in debug_payload["input"]:
                img_url = payload['input']['img_url']
                if img_url.startswith("data:"):
                    # 显示 data URI 的开头部分以验证格式
                    uri_header = img_url[:100]
                    debug_payload["input"]["img_url"] = f"<DATA_URI_{len(img_url)}_BYTES, header={uri_header}...>"
                # HTTP/HTTPS URL保持原样
            print(f"[DEBUG] 请求payload结构: {debug_payload}")

            # 发送请求（增加超时时间以支持大图片Base64传输）
            response = requests.post(
                self.endpoint,
                headers=headers,
                json=payload,
                timeout=120
            )

            # 打印完整响应以便调试
            print(f"[DEBUG] API响应状态码: {response.status_code}")
            print(f"[DEBUG] API响应内容: {response.text[:500]}...")  # 只打印前500字符

            if response.status_code == 200:
                result = response.json()

                # 提取task_id
                if "output" in result and "task_id" in result["output"]:
                    return {
                        "success": True,
                        "task_id": result["output"]["task_id"],
                        "task_status": result["output"].get("task_status", "PENDING"),
                        "message": "任务提交成功"
                    }
                else:
                    print(f"[ERROR] 响应格式错误，完整响应: {json.dumps(result, ensure_ascii=False)}")
                    return {
                        "success": False,
                        "error": "响应中缺少task_id",
                        "details": result
                    }
            else:
                print(f"[ERROR] API调用失败，状态码: {response.status_code}")
                print(f"[ERROR] 完整响应: {response.text}")
                return {
                    "success": False,
                    "error": f"API调用失败: {response.status_code}",
                    "details": response.text
                }

        except Exception as e:
            print(f"[ERROR] 提交任务异常: {str(e)}")
            import traceback
            print(f"[ERROR] 堆栈跟踪: {traceback.format_exc()}")
            return {
                "success": False,
                "error": "提交任务异常",
                "details": str(e)
            }

    def query_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        查询任务状态

        Args:
            task_id: 任务ID

        Returns:
            任务状态数据
        """
        try:
            headers = self._get_headers()
            url = f"{self.query_endpoint}/{task_id}"

            response = requests.get(url, headers=headers, timeout=30)

            if response.status_code == 200:
                result = response.json()

                if "output" in result:
                    output = result["output"]
                    return {
                        "success": True,
                        "task_id": task_id,
                        "task_status": output.get("task_status", "UNKNOWN"),
                        "task_result": output.get("task_metrics", {}),
                        "video_url": output.get("video_url"),
                        "code": result.get("request_id"),
                        "message": output.get("message", ""),
                        "full_output": output,  # 添加完整output用于调试
                        "full_response": result  # 添加完整响应用于调试
                    }
                else:
                    return {
                        "success": False,
                        "error": "响应格式错误",
                        "details": result
                    }
            else:
                return {
                    "success": False,
                    "error": f"查询失败: {response.status_code}",
                    "details": response.text
                }

        except Exception as e:
            return {
                "success": False,
                "error": "查询异常",
                "details": str(e)
            }

    def wait_for_completion(self,
                          task_id: str,
                          query_interval: int = None,
                          max_wait_time: int = None) -> Dict[str, Any]:
        """
        等待任务完成（轮询）

        Args:
            task_id: 任务ID
            query_interval: 查询间隔（秒），默认5秒
            max_wait_time: 最大等待时间（秒），默认600秒

        Returns:
            最终任务状态
        """
        query_interval = query_interval or self.default_query_interval
        max_wait_time = max_wait_time or self.default_max_wait_time

        start_time = time.time()

        while True:
            # 检查超时
            elapsed = time.time() - start_time
            if elapsed > max_wait_time:
                return {
                    "success": False,
                    "task_id": task_id,
                    "error": "等待超时",
                    "elapsed_time": elapsed
                }

            # 查询状态
            status_result = self.query_task_status(task_id)

            if not status_result["success"]:
                return status_result

            task_status = status_result["task_status"]

            # 任务成功
            if task_status == "SUCCEEDED":
                return {
                    "success": True,
                    "task_id": task_id,
                    "task_status": "SUCCEEDED",
                    "video_url": status_result.get("video_url"),
                    "task_result": status_result["task_result"],
                    "elapsed_time": elapsed
                }

            # 任务失败
            elif task_status == "FAILED":
                return {
                    "success": False,
                    "task_id": task_id,
                    "task_status": "FAILED",
                    "error": "任务生成失败",
                    "details": status_result.get("message", ""),
                    "full_output": status_result.get("full_output"),  # 添加完整output用于调试
                    "full_response": status_result.get("full_response"),  # 添加完整响应用于调试
                    "elapsed_time": elapsed
                }

            # 继续等待
            print(f"任务 {task_id[:8]}... 状态: {task_status}, 已等待 {int(elapsed)}秒")
            time.sleep(query_interval)

    def download_video(self, video_url: str, output_path: Path) -> bool:
        """
        下载生成的视频

        Args:
            video_url: 视频CDN URL
            output_path: 输出文件路径

        Returns:
            下载是否成功
        """
        try:
            # 确保目录存在
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # 下载视频
            response = requests.get(video_url, timeout=120)

            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)

                print(f"✅ 视频已保存: {output_path}")
                return True
            else:
                print(f"❌ 下载失败: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ 下载异常: {e}")
            return False

    def generate_video(self,
                      task_data: Dict[str, Any],
                      output_path: Optional[Path] = None,
                      retry_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        生成视频 - E8核心方法（整合完整流程）

        Args:
            task_data: 任务数据，包含：
                - input_data: 输入数据
                    - image_path / image_url: 图片
                    - use_base64: 是否使用Base64编码
                - parameters: 生成参数
                    - model: 模型名称
                    - prompt: 提示词
                    - negative_prompt: 反向提示词（可选）
                    - video_duration: 视频时长（5/10秒）
                    - fps: 帧率（24/30）
                    - resolution: 分辨率
                    - audio_config: 音频配置（可选）
                        - enable_audio: 是否启用音频
                        - audio_mode: auto_caption / custom_audio
                        - voice_id: 语音ID（auto_caption模式）
                        - speech_rate: 语速（auto_caption模式）
                        - caption_text: 配音文本（auto_caption模式）
                        - audio_file_path: 音频文件路径（custom_audio模式）
                    - effects: 视频特效（可选）
                        - enable_effects: 是否启用特效
                        - effect_type: 特效类型
                        - effect_intensity: 特效强度
            output_path: 输出路径（可选，默认自动生成）
            retry_config: 重试配置（可选）

        Returns:
            生成结果字典
        """
        generation_id = str(uuid.uuid4())
        start_time = datetime.now()

        try:
            # 步骤1: 提交任务
            print(f"🚀 提交图生视频任务...")
            submit_result = self.submit_task(task_data, retry_config)

            if not submit_result["success"]:
                return {
                    "success": False,
                    "generation_id": generation_id,
                    "error": "任务提交失败",
                    "details": submit_result
                }

            task_id = submit_result["task_id"]
            print(f"✅ 任务已提交: {task_id}")

            # 步骤2: 等待任务完成
            print(f"⏳ 等待视频生成...")
            wait_result = self.wait_for_completion(task_id)

            if not wait_result["success"]:
                return {
                    "success": False,
                    "generation_id": generation_id,
                    "task_id": task_id,
                    "error": "任务执行失败",
                    "details": wait_result
                }

            # 步骤3: 下载视频
            video_url = wait_result.get("video_url")

            if not video_url:
                return {
                    "success": False,
                    "generation_id": generation_id,
                    "task_id": task_id,
                    "error": "响应中缺少视频URL",
                    "details": wait_result
                }

            # 确定输出路径
            if not output_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"video_{timestamp}_{generation_id[:8]}.mp4"
                output_path = self.output_base / "temp" / filename

            # 下载视频
            print(f"⬇️ 下载视频...")
            download_success = self.download_video(video_url, output_path)

            if not download_success:
                return {
                    "success": False,
                    "generation_id": generation_id,
                    "task_id": task_id,
                    "error": "视频下载失败",
                    "video_url": video_url
                }

            # 保存元数据
            metadata = {
                "generation_id": generation_id,
                "task_id": task_id,
                "task_data": task_data,
                "video_url": video_url,
                "output_path": str(output_path),
                "elapsed_time": wait_result["elapsed_time"],
                "timestamp": datetime.now().isoformat(),
                "api_response": wait_result["task_result"]
            }

            metadata_path = output_path.parent / f"{output_path.stem}_metadata.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)

            end_time = datetime.now()
            total_time = (end_time - start_time).total_seconds()

            return {
                "success": True,
                "generation_id": generation_id,
                "task_id": task_id,
                "message": "E8图生视频生成成功（通义万相）",
                "video_url": video_url,
                "video_path": str(output_path),
                "metadata_path": str(metadata_path),
                "processing_time": total_time
            }

        except Exception as e:
            return {
                "success": False,
                "generation_id": generation_id,
                "error": "生成异常",
                "details": str(e)
            }


# 便捷函数
def generate_video(task_data: Dict[str, Any], **kwargs):
    """E8图生视频生成便捷函数（通义万相）"""
    api = WanAPIClient()
    return api.generate_video(task_data, **kwargs)


# 测试代码
def test_video_generation():
    """测试图生视频功能"""
    print("🎬 测试E8图生视频功能（通义万相2.5）...")

    # 测试案例1：自动配音
    test_case_auto_audio = {
        "input_data": {
            "image_path": "output/examples/scene-001.png",
            "use_base64": True
        },
        "parameters": {
            "model": "wanx2.5-i2v-preview",
            "prompt": "一位厨师在现代化厨房中烹饪美食，镜头缓慢推进展现细节",
            "negative_prompt": "模糊、抖动、低质量、变形",
            "video_duration": 5,
            "fps": 24,
            "resolution": "1280x720",
            "audio_config": {
                "enable_audio": True,
                "audio_mode": "auto_caption",
                "voice_id": "zh-CN-XiaoxiaoNeural",
                "speech_rate": 1.0,
                "caption_text": "美食烹饪的艺术时刻"
            }
        }
    }

    # 测试案例2：无声视频 + 特效
    test_case_silent_effects = {
        "input_data": {
            "image_path": "output/examples/scene-002.png",
            "use_base64": True
        },
        "parameters": {
            "model": "wanx2.5-i2v-preview",
            "prompt": "静谧的日式料理场景，专注的师傅手法",
            "negative_prompt": "杂乱、嘈杂",
            "video_duration": 5,
            "fps": 30,
            "resolution": "1920x1080",
            "audio_config": {
                "enable_audio": False
            },
            "effects": {
                "enable_effects": True,
                "effect_type": "dynamic_light",
                "effect_intensity": 0.7
            }
        }
    }

    # 选择测试案例
    result = generate_video(test_case_auto_audio)

    if result["success"]:
        print(f"✅ 生成成功")
        print(f"   📹 视频: {result['video_path']}")
        print(f"   📄 元数据: {result['metadata_path']}")
        print(f"   ⏱️ 耗时: {result['processing_time']:.2f}秒")
    else:
        print(f"❌ 生成失败: {result['error']}")


def main():
    """主函数 - 演示用法"""
    print("🎬 通义万相2.5 I2V API - E8图生视频模板")
    print("=" * 60)
    print("\n⚠️  此模板需配合execute引擎和执行计划使用")
    print("   执行计划路径: output/tongyi-wanxiang/plans/")
    print("   执行引擎: .claude/skills/执行引擎/API/aigc/Wan/scripts/wan-execute.py")
    print("\n" + "=" * 60)

    # 测试图生视频（需要实际图片）
    # test_video_generation()

    print("\n✅ E8专用API模板已加载（通义万相）")
    print("📋 支持的核心方法: generate_video()")
    print("📋 支持的音频模式:")
    print("   - auto_caption: 自动配音（TTS）")
    print("   - custom_audio: 自定义音频文件")
    print("   - silent: 无声视频")
    print("📋 支持的视频特效:")
    print("   - dynamic_light: 动态光效")
    print("   - motion_blur: 运动模糊")
    print("   - color_grade: 色彩分级")


if __name__ == "__main__":
    main()
