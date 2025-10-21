#!/usr/bin/env python3
"""
Nano Banana API - 餐饮AIGC全系列智能体统一执行引擎
===================================================

版本: 2.1 (2025-10-21)

核心功能:
--------
支持E1-E9全系列9个餐饮AIGC智能体的统一执行,实现从创意生成到印刷级成品的完整生产链路。

支持的智能体:
- E1: 餐饮文生图 (9种设计类型)
- E2: 餐饮图生图 (5种处理类型)
- E3: 餐饮图片识别 (5种分析类型)
- E4: 餐饮智能修复 (5种修复类型)
- E5: 餐饮结构控制 (4种控制类型)
- E6: 餐饮多图融合 (4种融合类型)
- E7: 餐饮角色一致性 (4种角色类型)
- E8: 餐饮设计迭代 (4种迭代类型)
- E9: 餐饮超分增强 (4种增强类型)

三层架构设计:
-----------
Layer 1 - 规则层 (Rules):
    由.claude/agents/E1.md~E9.md定义,包含智能体的专业知识、工作流程和输出规范

Layer 2 - 计划层 (Plans):
    JSON执行计划文件,位于api/plans/e{1-9}-{operation-name}/目录
    定义任务配置、参数和执行目标
    核心方法: execute_from_plan(plan_file_path)

Layer 3 - 执行层 (Execution):
    本文件 (banana_api_core.py) 提供统一的API执行引擎
    位于 .claude/skills/aigc/_shared/ 目录
    基于成功验证的OpenRouter配置 (google/gemini-2.5-flash-image-preview)
    所有E1-E9智能体共用同一个执行路径

执行方式:
-------
方式1 - 直接调用方法:
    api = NanoBananaAPI()
    result = api.generate_text_to_image(prompt="...", design_type="1-poster")

方式2 - 通过JSON执行计划:
    api = NanoBananaAPI()
    result = api.execute_from_plan("api/plans/e1-text-to-image/task-001.json")

输出路径结构:
-----------
output/创意组/[项目名]/images/{agent_id}-{operation_type}/     # 生成的图片
output/创意组/[项目名]/prompts/{agent_id}-{operation_type}/    # 提示词和元数据

技术栈:
------
- API网关: OpenRouter (https://openrouter.ai)
- 模型: google/gemini-2.5-flash-image-preview
- 图像格式: PNG (base64编码传输)
- 质量标准: 300 DPI 印刷级
- 行业专注: 餐饮设计和食品摄影

文档位置:
--------
- 智能体文档: .claude/agents/E{1-9}.md
- Skills文档: .claude/skills/aigc/{skill-name}/
- 执行计划示例: api/plans/e{1-9}-{operation-name}/*.json
- 数据模型定义: .claude/skills/aigc/_shared/models/execution_plan.py
- 测试脚本: .claude/skills/aigc/_shared/tests/test_plan_executor.py

更新日志:
--------
v2.1 (2025-10-21):
    - 重构为自包含架构,位于 .claude/skills/aigc/_shared/
    - 移除对 api/projects/nano-banana-api/ 的依赖
    - 统一输出路径为 output/创意组/[项目名]/
    - 更新所有文档引用路径

v2.0 (2025-10-11):
    - 新增E3-E9智能体支持
    - 实现execute_from_plan()计划层方法
    - 支持多种JSON格式灵活解析
    - 完善三层架构体系
    - 通过完整测试验证

v1.0 (2024-12):
    - 初始版本,支持E1文生图和E2图生图
    - 基于OpenRouter API封装
    - 实现餐饮行业提示词增强
"""

import requests
import json
import base64
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Union, Dict, Any
import os

from config import AIGCConfig

class NanoBananaAPI:
    """Nano Banana API 客户端"""

    def __init__(self):
        # 使用统一配置
        self.config = AIGCConfig()
        self.api_key = self.config.API_KEY
        self.base_url = self.config.BASE_URL
        self.model = self.config.MODEL

        # 站点信息
        self.site_url = "https://ztl-restaurant-design.com"
        self.site_name = "ZTL-Restaurant-Design-Platform"

        # 路径配置（使用AIGCConfig）
        self.output_base = self.config.OUTPUT_BASE
        self.library_base = self.config.PROJECT_ROOT / "library"

        # 项目名称(可在调用时指定)
        self.project_name = None

        # 初始化创意组输出目录
        self.config.CREATIVE_TEAM_DIR.mkdir(parents=True, exist_ok=True)

        # E1设计类型映射
        self.design_types = {
            "1-poster": {"name": "海报设计", "ratio": "2:3", "dpi": 300},
            "2-menu": {"name": "菜单设计", "ratio": "3:4", "dpi": 300},
            "3-storefront": {"name": "门头设计", "ratio": "16:9", "dpi": 300},
            "4-panel": {"name": "菜单面板", "ratio": "4:3", "dpi": 300},
            "5-magazine": {"name": "画册宣传册", "ratio": "A4", "dpi": 300},
            "6-icon": {"name": "图标设计", "ratio": "1:1", "dpi": 300},
            "7-typography": {"name": "字体设计", "ratio": "16:9", "dpi": 300},
            "8-main-image": {"name": "主图摄影", "ratio": "1:1", "dpi": 300},
            "9-detail": {"name": "详情页设计", "ratio": "9:16", "dpi": 300}
        }

        # E2处理类型映射
        self.processing_types = {
            "local_modification": "局部修改",
            "local_optimization": "局部优化",
            "multi_image_processing": "多图处理",
            "style_transfer": "风格迁移",
            "scene_analysis": "场景分析"
        }

        # E3分析类型映射
        self.analysis_types = {
            "comprehensive_analysis": "综合分析",
            "quality_assessment": "质量评估",
            "content_analysis": "内容分析",
            "scene_recognition": "场景识别",
            "brand_detection": "品牌检测"
        }

        # E4修复类型映射
        self.repair_types = {
            "watermark_removal": "水印去除",
            "object_removal": "物体移除",
            "background_repair": "背景修复",
            "inpainting": "内补修复",
            "outpainting": "外扩延伸"
        }

        # E5控制类型映射
        self.control_types = {
            "pose_control": "姿态控制",
            "depth_control": "深度控制",
            "edge_control": "边缘控制",
            "layout_control": "布局控制"
        }

        # E6融合类型映射
        self.fusion_types = {
            "creative_combination": "创意组合",
            "brand_integration": "品牌融合",
            "scene_composition": "场景合成",
            "element_collage": "元素拼贴"
        }

        # E7角色类型映射
        self.character_types = {
            "brand_mascot": "品牌吉祥物",
            "chef_character": "厨师角色",
            "spokesperson": "代言人",
            "product_ip": "产品IP"
        }

        # E8迭代类型映射
        self.iteration_types = {
            "local_optimization": "局部优化",
            "progressive_improvement": "渐进改进",
            "feedback_response": "反馈响应",
            "aesthetic_enhancement": "美学增强"
        }

        # E9增强类型映射
        self.enhancement_types = {
            "intelligent_upscaling": "智能超分",
            "detail_enhancement": "细节增强",
            "texture_optimization": "质感优化",
            "noise_reduction": "降噪处理"
        }

    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": self.site_url,
            "X-Title": self.site_name
        }

    def _build_messages(self, prompt: str, image_urls: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """构建消息内容"""
        content = []

        # 添加文本内容
        content.append({
            "type": "text",
            "text": prompt
        })

        # 添加图像内容（如果有）
        if image_urls:
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

    def _enhance_prompt_for_design(self, prompt: str, design_type: Optional[str] = None) -> str:
        """为E1文生图增强提示词"""
        if not design_type or design_type not in self.design_types:
            design_type = "8-main-image"  # 默认主图摄影

        design_info = self.design_types[design_type]

        enhanced_prompt = f"""
        Restaurant Design Task: {prompt}

        Design Type: {design_info['name']} ({design_type})
        Aspect Ratio: {design_info['ratio']}
        Quality: {design_info['dpi']}DPI professional print quality

        Requirements:
        - Professional restaurant industry design
        - High visual impact and appetite appeal
        - Commercial use quality
        - Brand consistency
        - Food photography standards
        - Suitable for {design_info['name']} application

        Please create a detailed, professional restaurant design that meets these specifications.
        """

        return enhanced_prompt.strip()

    def _enhance_prompt_for_processing(self, prompt: str, processing_type: Optional[str] = None) -> str:
        """为E2图生图增强提示词"""
        if not processing_type or processing_type not in self.processing_types:
            processing_type = "local_optimization"  # 默认局部优化

        processing_name = self.processing_types[processing_type]

        enhanced_prompt = f"""
        Restaurant Image Processing Task: {prompt}

        Processing Type: {processing_name} ({processing_type})

        Requirements:
        - Maintain food authenticity and appeal
        - Professional restaurant industry standards
        - High-resolution output quality
        - Natural and seamless processing
        - Commercial use compatibility
        - Preserve food texture and color accuracy

        Please process the image according to these restaurant industry specifications.
        """

        return enhanced_prompt.strip()

    def _get_output_paths(self, agent_id: Optional[str] = None,
                         operation_type: Optional[str] = None,
                         design_type: Optional[str] = None,
                         processing_type: Optional[str] = None,
                         project_name: Optional[str] = None) -> Dict[str, Path]:
        """
        获取输出路径 - 新架构: output/创意组/[项目名]/

        Args:
            agent_id: 智能体ID (E1-E9)
            operation_type: 操作类型
            design_type: 设计类型 (E1专用)
            processing_type: 处理类型 (E2专用)
            project_name: 项目名称,默认使用self.project_name或配置的默认值

        Returns:
            包含image_dir, prompt_dir, filename_prefix, timestamp的字典
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 使用项目名称
        proj_name = project_name or self.project_name or self.config.DEFAULT_PROJECT_NAME

        # 新的统一路径结构：output/创意组/[项目名]/images|prompts/
        image_dir = self.config.get_images_dir(proj_name)
        prompt_dir = self.config.get_prompts_dir(proj_name)

        # 根据不同类型设置文件名前缀
        if agent_id and operation_type:
            filename_prefix = f"{agent_id.lower()}_{operation_type}_{timestamp}"
            # 按操作类型创建子目录
            image_dir = image_dir / f"{agent_id.lower()}-{operation_type}"
            prompt_dir = prompt_dir / f"{agent_id.lower()}-{operation_type}"
        elif design_type:
            filename_prefix = f"{design_type}_{timestamp}"
            image_dir = image_dir / design_type
            prompt_dir = prompt_dir / design_type
        elif processing_type:
            filename_prefix = f"{processing_type}_{timestamp}"
            image_dir = image_dir / processing_type
            prompt_dir = prompt_dir / processing_type
        else:
            filename_prefix = f"generated_{timestamp}"
            image_dir = image_dir / "generated"
            prompt_dir = prompt_dir / "generated"

        return {
            "image_dir": image_dir,
            "prompt_dir": prompt_dir,
            "filename_prefix": filename_prefix,
            "timestamp": timestamp
        }

    def _save_base64_image(self, base64_data: str, output_path: Path) -> bool:
        """保存base64图像到文件"""
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
        """从响应中提取图像数据"""
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

    def generate_text_to_image(self, prompt: str, design_type: Optional[str] = None,
                              style: str = "professional", **kwargs) -> Dict[str, Any]:
        """E1智能体文生图功能"""
        task_id = str(uuid.uuid4())
        start_time = datetime.now()

        try:
            # 增强提示词
            enhanced_prompt = self._enhance_prompt_for_design(prompt, design_type)

            # 构建请求
            headers = self._get_headers()
            messages = self._build_messages(enhanced_prompt)

            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 4000,
                "temperature": kwargs.get("temperature", 0.7)
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

                # 保存图像和提示词
                paths = self._get_output_paths(design_type=design_type)
                image_paths = []

                for i, image_data in enumerate(images):
                    filename = f"{paths['filename_prefix']}_{i+1}.png"
                    image_path = paths["image_dir"] / filename

                    if self._save_base64_image(image_data, image_path):
                        image_paths.append(str(image_path))

                # 保存提示词
                prompt_data = {
                    "task_id": task_id,
                    "original_prompt": prompt,
                    "enhanced_prompt": enhanced_prompt,
                    "design_type": design_type,
                    "style": style,
                    "timestamp": paths["timestamp"],
                    "api_response": result
                }

                prompt_file = paths["prompt_dir"] / f"{paths['filename_prefix']}_prompt.json"
                prompt_file.parent.mkdir(parents=True, exist_ok=True)

                with open(prompt_file, 'w', encoding='utf-8') as f:
                    json.dump(prompt_data, f, ensure_ascii=False, indent=2)

                end_time = datetime.now()
                processing_time = (end_time - start_time).total_seconds()

                return {
                    "success": True,
                    "task_id": task_id,
                    "message": "E1文生图生成成功",
                    "images": images,
                    "image_paths": image_paths,
                    "prompt_file": str(prompt_file),
                    "processing_time": processing_time,
                    "design_type": design_type
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

    def _convert_local_image_to_base64(self, image_path: str) -> Optional[str]:
        """将本地图片转换为base64格式"""
        try:
            from pathlib import Path
            import base64
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

    def generate_image_to_image(self, prompt: str, image_urls: List[str],
                               processing_type: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """E2智能体图生图功能"""
        task_id = str(uuid.uuid4())
        start_time = datetime.now()

        try:
            # 增强提示词
            enhanced_prompt = self._enhance_prompt_for_processing(prompt, processing_type)

            # 处理图像URL，转换本地文件为base64
            processed_image_urls = []
            for url in image_urls:
                if url.startswith("file://") or not url.startswith("http"):
                    # 本地文件，转换为base64
                    base64_url = self._convert_local_image_to_base64(url)
                    if base64_url:
                        processed_image_urls.append(base64_url)
                    else:
                        print(f"跳过无效的图片: {url}")
                else:
                    # 网络URL，直接使用
                    processed_image_urls.append(url)

            if not processed_image_urls:
                return {
                    "success": False,
                    "task_id": task_id,
                    "error": "没有有效的输入图片",
                    "details": "所有提供的图片URL都无法处理"
                }

            # 构建请求
            headers = self._get_headers()
            messages = self._build_messages(enhanced_prompt, processed_image_urls)

            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 4000,
                "temperature": kwargs.get("temperature", 0.7)
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

                # 保存图像和提示词
                paths = self._get_output_paths(processing_type=processing_type)
                image_paths = []

                for i, image_data in enumerate(images):
                    filename = f"{paths['filename_prefix']}_{i+1}.png"
                    image_path = paths["image_dir"] / filename

                    if self._save_base64_image(image_data, image_path):
                        image_paths.append(str(image_path))

                # 保存提示词
                prompt_data = {
                    "task_id": task_id,
                    "original_prompt": prompt,
                    "enhanced_prompt": enhanced_prompt,
                    "processing_type": processing_type,
                    "input_images": image_urls,
                    "timestamp": paths["timestamp"],
                    "api_response": result
                }

                prompt_file = paths["prompt_dir"] / f"{paths['filename_prefix']}_prompt.json"
                prompt_file.parent.mkdir(parents=True, exist_ok=True)

                with open(prompt_file, 'w', encoding='utf-8') as f:
                    json.dump(prompt_data, f, ensure_ascii=False, indent=2)

                end_time = datetime.now()
                processing_time = (end_time - start_time).total_seconds()

                return {
                    "success": True,
                    "task_id": task_id,
                    "message": "E2图生图处理成功",
                    "images": images,
                    "image_paths": image_paths,
                    "prompt_file": str(prompt_file),
                    "processing_time": processing_time,
                    "processing_type": processing_type
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
                "error": "处理异常",
                "details": str(e)
            }

    def generate_image_recognition(self, image_url: str, analysis_type: str = "comprehensive_analysis",
                                   analysis_dimensions: Optional[List[str]] = None, **kwargs) -> Dict[str, Any]:
        """E3智能体图片识别功能"""
        task_id = str(uuid.uuid4())
        start_time = datetime.now()

        try:
            # 构建分析prompt
            analysis_name = self.analysis_types.get(analysis_type, "综合分析")
            dimensions_text = ", ".join(analysis_dimensions) if analysis_dimensions else "全面分析"

            prompt = f"""
            Restaurant Image Recognition Task:
            Analysis Type: {analysis_name} ({analysis_type})
            Analysis Dimensions: {dimensions_text}

            Please analyze this restaurant/food image and provide:
            1. Food Content Analysis: Identify all dishes, ingredients, presentation style
            2. Visual Quality Assessment: Evaluate lighting, composition, color, clarity
            3. Scene Recognition: Identify setting, ambiance, style, target audience
            4. Brand Elements: Detect any logos, text, branding elements
            5. Commercial Value: Assess marketing potential and usage recommendations

            Provide detailed analysis in JSON format with structured categories.
            """

            # 处理图像URL
            if image_url.startswith("file://") or not image_url.startswith("http"):
                image_url = self._convert_local_image_to_base64(image_url)

            if not image_url:
                return {
                    "success": False,
                    "task_id": task_id,
                    "error": "无效的图片URL",
                    "details": "无法读取或转换图片"
                }

            # 构建请求
            headers = self._get_headers()
            messages = self._build_messages(prompt, [image_url])

            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 4000,
                "temperature": kwargs.get("temperature", 0.3)  # 识别任务使用较低温度
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

                # 提取分析内容
                choices = result.get("choices", [])
                analysis_content = ""
                if choices:
                    message = choices[0].get("message", {})
                    analysis_content = message.get("content", "")

                # 保存分析结果
                paths = self._get_output_paths(agent_id="E3", operation_type=analysis_type)
                analysis_file = paths["prompt_dir"] / f"{paths['filename_prefix']}_analysis.json"
                analysis_file.parent.mkdir(parents=True, exist_ok=True)

                analysis_data = {
                    "task_id": task_id,
                    "analysis_type": analysis_type,
                    "image_url": image_url[:100] + "..." if len(image_url) > 100 else image_url,
                    "analysis_content": analysis_content,
                    "timestamp": paths["timestamp"],
                    "api_response": result
                }

                with open(analysis_file, 'w', encoding='utf-8') as f:
                    json.dump(analysis_data, f, ensure_ascii=False, indent=2)

                end_time = datetime.now()
                processing_time = (end_time - start_time).total_seconds()

                return {
                    "success": True,
                    "task_id": task_id,
                    "message": "E3图片识别完成",
                    "analysis_content": analysis_content,
                    "analysis_file": str(analysis_file),
                    "processing_time": processing_time,
                    "analysis_type": analysis_type
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
                "error": "识别异常",
                "details": str(e)
            }

    def generate_smart_repair(self, image_url: str, repair_prompt: str,
                             repair_type: str = "watermark_removal", **kwargs) -> Dict[str, Any]:
        """E4智能体智能修复功能"""
        task_id = str(uuid.uuid4())
        start_time = datetime.now()

        try:
            repair_name = self.repair_types.get(repair_type, "智能修复")

            enhanced_prompt = f"""
            Restaurant Image Repair Task: {repair_prompt}
            Repair Type: {repair_name} ({repair_type})

            Requirements:
            - Remove unwanted elements seamlessly
            - Maintain natural food appearance
            - Preserve image quality and resolution
            - Fill repaired areas naturally
            - Commercial use quality standards

            Please repair the image professionally maintaining restaurant industry standards.
            """

            # 处理图像
            if image_url.startswith("file://") or not image_url.startswith("http"):
                image_url = self._convert_local_image_to_base64(image_url)

            if not image_url:
                return {"success": False, "task_id": task_id, "error": "无效的图片URL"}

            # 构建请求
            headers = self._get_headers()
            messages = self._build_messages(enhanced_prompt, [image_url])

            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 4000,
                "temperature": kwargs.get("temperature", 0.7)
            }

            response = requests.post(self.base_url, headers=headers, json=data, timeout=120)

            if response.status_code == 200:
                result = response.json()
                images = self._extract_images_from_response(result)

                paths = self._get_output_paths(agent_id="E4", operation_type=repair_type)
                image_paths = []

                for i, image_data in enumerate(images):
                    filename = f"{paths['filename_prefix']}_{i+1}.png"
                    image_path = paths["image_dir"] / filename
                    if self._save_base64_image(image_data, image_path):
                        image_paths.append(str(image_path))

                return {
                    "success": True,
                    "task_id": task_id,
                    "message": "E4智能修复完成",
                    "images": images,
                    "image_paths": image_paths,
                    "processing_time": (datetime.now() - start_time).total_seconds(),
                    "repair_type": repair_type
                }
            else:
                return {"success": False, "task_id": task_id, "error": f"API调用失败: {response.status_code}"}

        except Exception as e:
            return {"success": False, "task_id": task_id, "error": "修复异常", "details": str(e)}

    def generate_structure_control(self, reference_image: str, target_prompt: str,
                                   control_type: str = "pose_control",
                                   control_strength: float = 0.8, **kwargs) -> Dict[str, Any]:
        """E5智能体结构控制功能"""
        task_id = str(uuid.uuid4())
        start_time = datetime.now()

        try:
            control_name = self.control_types.get(control_type, "结构控制")

            enhanced_prompt = f"""
            Restaurant Image Structure Control Task: {target_prompt}
            Control Type: {control_name} ({control_type})
            Control Strength: {control_strength}

            Requirements:
            - Maintain structural elements from reference image
            - Generate new content following the control guidance
            - Professional restaurant industry quality
            - Natural and realistic result
            - {control_name} consistency with reference

            Please generate a new image following the structural control.
            """

            # 处理参考图像
            if reference_image.startswith("file://") or not reference_image.startswith("http"):
                reference_image = self._convert_local_image_to_base64(reference_image)

            if not reference_image:
                return {"success": False, "task_id": task_id, "error": "无效的参考图片"}

            # 构建请求
            headers = self._get_headers()
            messages = self._build_messages(enhanced_prompt, [reference_image])

            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 4000,
                "temperature": kwargs.get("temperature", 0.7)
            }

            response = requests.post(self.base_url, headers=headers, json=data, timeout=120)

            if response.status_code == 200:
                result = response.json()
                images = self._extract_images_from_response(result)

                paths = self._get_output_paths(agent_id="E5", operation_type=control_type)
                image_paths = []

                for i, image_data in enumerate(images):
                    filename = f"{paths['filename_prefix']}_{i+1}.png"
                    image_path = paths["image_dir"] / filename
                    if self._save_base64_image(image_data, image_path):
                        image_paths.append(str(image_path))

                return {
                    "success": True,
                    "task_id": task_id,
                    "message": "E5结构控制完成",
                    "images": images,
                    "image_paths": image_paths,
                    "processing_time": (datetime.now() - start_time).total_seconds(),
                    "control_type": control_type
                }
            else:
                return {"success": False, "task_id": task_id, "error": f"API调用失败: {response.status_code}"}

        except Exception as e:
            return {"success": False, "task_id": task_id, "error": "控制异常", "details": str(e)}

    def generate_image_fusion(self, source_images: List[str], fusion_prompt: str,
                             fusion_type: str = "creative_combination", **kwargs) -> Dict[str, Any]:
        """E6智能体多图融合功能"""
        task_id = str(uuid.uuid4())
        start_time = datetime.now()

        try:
            fusion_name = self.fusion_types.get(fusion_type, "多图融合")

            enhanced_prompt = f"""
            Restaurant Image Fusion Task: {fusion_prompt}
            Fusion Type: {fusion_name} ({fusion_type})

            Requirements:
            - Seamlessly combine multiple images
            - Maintain visual harmony and coherence
            - Professional restaurant industry standards
            - Natural lighting and color consistency
            - Creative and appealing composition

            Please create a fused image combining all input images creatively.
            """

            # 处理所有源图像
            processed_images = []
            for img_url in source_images:
                if img_url.startswith("file://") or not img_url.startswith("http"):
                    img_url = self._convert_local_image_to_base64(img_url)
                if img_url:
                    processed_images.append(img_url)

            if not processed_images:
                return {"success": False, "task_id": task_id, "error": "没有有效的源图片"}

            # 构建请求
            headers = self._get_headers()
            messages = self._build_messages(enhanced_prompt, processed_images)

            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 4000,
                "temperature": kwargs.get("temperature", 0.7)
            }

            response = requests.post(self.base_url, headers=headers, json=data, timeout=120)

            if response.status_code == 200:
                result = response.json()
                images = self._extract_images_from_response(result)

                paths = self._get_output_paths(agent_id="E6", operation_type=fusion_type)
                image_paths = []

                for i, image_data in enumerate(images):
                    filename = f"{paths['filename_prefix']}_{i+1}.png"
                    image_path = paths["image_dir"] / filename
                    if self._save_base64_image(image_data, image_path):
                        image_paths.append(str(image_path))

                return {
                    "success": True,
                    "task_id": task_id,
                    "message": "E6多图融合完成",
                    "images": images,
                    "image_paths": image_paths,
                    "processing_time": (datetime.now() - start_time).total_seconds(),
                    "fusion_type": fusion_type
                }
            else:
                return {"success": False, "task_id": task_id, "error": f"API调用失败: {response.status_code}"}

        except Exception as e:
            return {"success": False, "task_id": task_id, "error": "融合异常", "details": str(e)}

    def generate_character_consistency(self, character_reference: str, scene_prompt: str,
                                      character_type: str = "brand_mascot",
                                      consistency_level: int = 5, **kwargs) -> Dict[str, Any]:
        """E7智能体角色一致性功能"""
        task_id = str(uuid.uuid4())
        start_time = datetime.now()

        try:
            character_name = self.character_types.get(character_type, "角色一致性")

            enhanced_prompt = f"""
            Restaurant Character Consistency Task: {scene_prompt}
            Character Type: {character_name} ({character_type})
            Consistency Level: {consistency_level}/5

            Requirements:
            - Maintain character appearance and features exactly
            - Preserve character personality and style
            - Integrate character naturally into new scene
            - Professional restaurant industry context
            - Brand consistency and recognition
            - High consistency level ({consistency_level}/5)

            Please generate the character in the new scene maintaining perfect consistency.
            """

            # 处理角色参考图
            if character_reference.startswith("file://") or not character_reference.startswith("http"):
                character_reference = self._convert_local_image_to_base64(character_reference)

            if not character_reference:
                return {"success": False, "task_id": task_id, "error": "无效的角色参考图"}

            # 构建请求
            headers = self._get_headers()
            messages = self._build_messages(enhanced_prompt, [character_reference])

            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 4000,
                "temperature": kwargs.get("temperature", 0.5)  # 较低温度保证一致性
            }

            response = requests.post(self.base_url, headers=headers, json=data, timeout=120)

            if response.status_code == 200:
                result = response.json()
                images = self._extract_images_from_response(result)

                paths = self._get_output_paths(agent_id="E7", operation_type=character_type)
                image_paths = []

                for i, image_data in enumerate(images):
                    filename = f"{paths['filename_prefix']}_{i+1}.png"
                    image_path = paths["image_dir"] / filename
                    if self._save_base64_image(image_data, image_path):
                        image_paths.append(str(image_path))

                return {
                    "success": True,
                    "task_id": task_id,
                    "message": "E7角色一致性完成",
                    "images": images,
                    "image_paths": image_paths,
                    "processing_time": (datetime.now() - start_time).total_seconds(),
                    "character_type": character_type
                }
            else:
                return {"success": False, "task_id": task_id, "error": f"API调用失败: {response.status_code}"}

        except Exception as e:
            return {"success": False, "task_id": task_id, "error": "一致性异常", "details": str(e)}

    def generate_design_iteration(self, current_version: str, feedback: str,
                                  iteration_type: str = "feedback_response",
                                  iteration_goals: Optional[List[str]] = None, **kwargs) -> Dict[str, Any]:
        """E8智能体设计迭代功能"""
        task_id = str(uuid.uuid4())
        start_time = datetime.now()

        try:
            iteration_name = self.iteration_types.get(iteration_type, "设计迭代")
            goals_text = "\n".join(f"- {goal}" for goal in iteration_goals) if iteration_goals else "- General improvement"

            enhanced_prompt = f"""
            Restaurant Design Iteration Task:
            Iteration Type: {iteration_name} ({iteration_type})
            Feedback: {feedback}

            Iteration Goals:
            {goals_text}

            Requirements:
            - Address all feedback points specifically
            - Improve design while maintaining core elements
            - Professional restaurant industry standards
            - Progressive improvement approach
            - Commercial use quality

            Please generate an improved version addressing the feedback.
            """

            # 处理当前版本图片
            if current_version.startswith("file://") or not current_version.startswith("http"):
                current_version = self._convert_local_image_to_base64(current_version)

            if not current_version:
                return {"success": False, "task_id": task_id, "error": "无效的当前版本图片"}

            # 构建请求
            headers = self._get_headers()
            messages = self._build_messages(enhanced_prompt, [current_version])

            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 4000,
                "temperature": kwargs.get("temperature", 0.7)
            }

            response = requests.post(self.base_url, headers=headers, json=data, timeout=120)

            if response.status_code == 200:
                result = response.json()
                images = self._extract_images_from_response(result)

                paths = self._get_output_paths(agent_id="E8", operation_type=iteration_type)
                image_paths = []

                for i, image_data in enumerate(images):
                    filename = f"{paths['filename_prefix']}_{i+1}.png"
                    image_path = paths["image_dir"] / filename
                    if self._save_base64_image(image_data, image_path):
                        image_paths.append(str(image_path))

                return {
                    "success": True,
                    "task_id": task_id,
                    "message": "E8设计迭代完成",
                    "images": images,
                    "image_paths": image_paths,
                    "processing_time": (datetime.now() - start_time).total_seconds(),
                    "iteration_type": iteration_type
                }
            else:
                return {"success": False, "task_id": task_id, "error": f"API调用失败: {response.status_code}"}

        except Exception as e:
            return {"success": False, "task_id": task_id, "error": "迭代异常", "details": str(e)}

    def generate_super_resolution(self, source_image: str, target_resolution: str = "4K",
                                  enhancement_type: str = "intelligent_upscaling",
                                  enhancement_strength: float = 0.8, **kwargs) -> Dict[str, Any]:
        """E9智能体超分增强功能"""
        task_id = str(uuid.uuid4())
        start_time = datetime.now()

        try:
            enhancement_name = self.enhancement_types.get(enhancement_type, "超分增强")

            enhanced_prompt = f"""
            Restaurant Image Super Resolution Task:
            Enhancement Type: {enhancement_name} ({enhancement_type})
            Target Resolution: {target_resolution}
            Enhancement Strength: {enhancement_strength}

            Requirements:
            - Intelligently upscale to {target_resolution} resolution
            - Enhance details and textures naturally
            - Preserve food authenticity and colors
            - Commercial print quality (300+ DPI)
            - Reduce noise while maintaining sharpness
            - Professional restaurant industry standards

            Please enhance the image to print-ready commercial quality.
            """

            # 处理源图像
            if source_image.startswith("file://") or not source_image.startswith("http"):
                source_image = self._convert_local_image_to_base64(source_image)

            if not source_image:
                return {"success": False, "task_id": task_id, "error": "无效的源图片"}

            # 构建请求
            headers = self._get_headers()
            messages = self._build_messages(enhanced_prompt, [source_image])

            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 4000,
                "temperature": kwargs.get("temperature", 0.5)  # 较低温度保证质量
            }

            response = requests.post(self.base_url, headers=headers, json=data, timeout=120)

            if response.status_code == 200:
                result = response.json()
                images = self._extract_images_from_response(result)

                paths = self._get_output_paths(agent_id="E9", operation_type=enhancement_type)
                image_paths = []

                for i, image_data in enumerate(images):
                    filename = f"{paths['filename_prefix']}_{i+1}.png"
                    image_path = paths["image_dir"] / filename
                    if self._save_base64_image(image_data, image_path):
                        image_paths.append(str(image_path))

                return {
                    "success": True,
                    "task_id": task_id,
                    "message": "E9超分增强完成",
                    "images": images,
                    "image_paths": image_paths,
                    "processing_time": (datetime.now() - start_time).total_seconds(),
                    "enhancement_type": enhancement_type,
                    "target_resolution": target_resolution
                }
            else:
                return {"success": False, "task_id": task_id, "error": f"API调用失败: {response.status_code}"}

        except Exception as e:
            return {"success": False, "task_id": task_id, "error": "增强异常", "details": str(e)}

    def execute_from_plan(self, plan_file_path: str) -> Dict[str, Any]:
        """
        执行JSON计划文件 - Layer 2: 计划层

        三层架构的核心方法,实现从JSON配置到API执行的自动化路由。
        支持E1-E9全系列智能体,自动识别智能体类型并调用相应方法。

        功能特性:
        --------
        - 智能路由: 根据agent_id自动路由到对应的E1-E9方法
        - 灵活解析: 支持多种JSON字段命名约定 (向后兼容)
        - 错误处理: 完整的文件检查、JSON解析和执行错误处理
        - 类型安全: 支持多种数据类型格式 (字符串/数组/对象)

        支持的字段命名约定:
        ----------------
        E1 (文生图):
            - text_prompt 或 design_goals (数组/对象)
            - design_type

        E2 (图生图):
            - source_image 或 base_image
            - processing_type 或 operation_type
            - processing_requirements 或 style_requirements

        E3 (图片识别):
            - image_url 或 image_path
            - analysis_type 或 recognition_type
            - analysis_dimensions (数组) 或 analysis_requirements (对象)

        E4-E9: 参照api/plans目录下的JSON示例

        JSON计划文件结构:
        ---------------
        {
            "plan_version": "1.0",
            "agent_id": "E1",                    // 必需: E1~E9
            "operation_type": "text_to_image",   // 必需: 操作类型
            "input_data": {                      // 必需: 输入数据
                // ... 智能体特定的字段
            },
            "model_config": {},                  // 可选: 模型配置
            "output_settings": {},               // 可选: 输出设置
            "metadata": {}                       // 可选: 元数据
        }

        Args:
        ----
            plan_file_path (str): JSON执行计划文件的路径 (相对或绝对路径)

        Returns:
        -------
            Dict[str, Any]: 执行结果字典,包含以下字段:
                - success (bool): 执行是否成功
                - task_id (str): 任务唯一标识符
                - message (str): 执行消息 (成功时)
                - error (str): 错误信息 (失败时)
                - details (str): 详细信息 (失败时)
                - agent_id (str): 执行的智能体ID
                - operation_type (str): 操作类型
                - image_paths (List[str]): 生成的图片路径 (适用于E1/E2/E4-E9)
                - analysis_content (str): 分析内容 (适用于E3)
                - processing_time (float): 处理时间 (秒)

        Raises:
        ------
            不抛出异常,所有错误通过返回值的success字段标识

        Examples:
        --------
            # 示例1: 执行E1文生图计划
            >>> api = NanoBananaAPI()
            >>> result = api.execute_from_plan("api/plans/e1-text-to-image/task-001.json")
            >>> if result["success"]:
            ...     print(f"生成图片: {result['image_paths']}")

            # 示例2: 执行E3图片识别计划
            >>> result = api.execute_from_plan("api/plans/e3-image-recognition/task-001.json")
            >>> if result["success"]:
            ...     print(f"分析结果: {result['analysis_content']}")

        使用场景:
        --------
        1. 智能体调用: .claude/agents/E{1-9}.md中的智能体通过此方法执行任务
        2. 批量任务: 预定义多个JSON计划文件,批量执行生成任务
        3. 任务模板: 创建可复用的JSON模板,快速生成类似内容
        4. 自动化流程: 集成到CI/CD或定时任务中自动执行

        相关文档:
        --------
        - 智能体定义: .claude/agents/E{1-9}.md
        - 计划示例: api/plans/e{1-9}-{operation-name}/*.json
        - 数据模型: api/projects/nano-banana-api/models/execution_plan.py
        - 测试脚本: test_execute_plan.py
        """
        task_id = str(uuid.uuid4())

        try:
            # 读取JSON计划文件
            plan_path = Path(plan_file_path)
            if not plan_path.exists():
                return {
                    "success": False,
                    "task_id": task_id,
                    "error": "计划文件不存在",
                    "details": f"文件路径: {plan_file_path}"
                }

            with open(plan_path, 'r', encoding='utf-8') as f:
                plan_data = json.load(f)

            # 提取核心信息
            agent_id = plan_data.get("agent_id", "").upper()
            operation_type = plan_data.get("operation_type", "")
            input_data = plan_data.get("input_data", {})

            if not agent_id or not operation_type:
                return {
                    "success": False,
                    "task_id": task_id,
                    "error": "计划文件格式错误",
                    "details": "缺少必需字段: agent_id 或 operation_type"
                }

            # 根据agent_id路由到相应的方法
            if agent_id == "E1":
                # E1文生图 - 支持多种JSON格式
                design_type = input_data.get("design_type", "8-main-image")

                # 提取prompt - 支持多种字段名
                prompt = ""
                if "text_prompt" in input_data:
                    # 直接文本提示词格式
                    prompt = input_data.get("text_prompt", "")
                elif "design_goals" in input_data:
                    # design_goals数组格式
                    design_goals = input_data.get("design_goals", [])
                    if isinstance(design_goals, list) and design_goals:
                        # 支持字符串数组或对象数组
                        if isinstance(design_goals[0], dict):
                            prompt = design_goals[0].get("description", "")
                        elif isinstance(design_goals[0], str):
                            prompt = design_goals[0]

                return self.generate_text_to_image(prompt=prompt, design_type=design_type)

            elif agent_id == "E2":
                # E2图生图 - 支持多种JSON格式
                # 支持operation_type或processing_type
                processing_type = input_data.get("processing_type") or input_data.get("operation_type", "local_optimization")

                # 支持source_image或base_image
                source_image = input_data.get("source_image") or input_data.get("base_image", "")

                # 从多种可能的字段提取prompt
                prompt = ""
                if "processing_requirements" in input_data:
                    if isinstance(input_data["processing_requirements"], str):
                        prompt = input_data["processing_requirements"]
                    elif isinstance(input_data["processing_requirements"], dict):
                        # 如果是对象,尝试提取描述
                        prompt = str(input_data["processing_requirements"])
                elif "style_requirements" in input_data:
                    style_req = input_data["style_requirements"]
                    if isinstance(style_req, dict):
                        # 拼接风格要求
                        prompt = f"Target style: {style_req.get('target_style', '')}, {style_req.get('lighting', '')}"
                    else:
                        prompt = str(style_req)

                return self.generate_image_to_image(
                    prompt=prompt,
                    image_urls=[source_image],
                    processing_type=processing_type
                )

            elif agent_id == "E3":
                # E3图片识别 - 支持多种JSON格式
                # 支持analysis_type或recognition_type
                analysis_type = input_data.get("analysis_type") or input_data.get("recognition_type", "comprehensive_analysis")

                # 支持image_url或image_path
                image_url = input_data.get("image_url") or input_data.get("image_path", "")

                # 提取分析维度
                analysis_dimensions = []
                if "analysis_dimensions" in input_data:
                    analysis_dimensions = input_data.get("analysis_dimensions", [])
                elif "analysis_requirements" in input_data:
                    # 从analysis_requirements对象提取维度
                    req = input_data["analysis_requirements"]
                    if isinstance(req, dict):
                        analysis_dimensions = [k for k, v in req.items() if v is True]

                return self.generate_image_recognition(
                    image_url=image_url,
                    analysis_type=analysis_type,
                    analysis_dimensions=analysis_dimensions
                )

            elif agent_id == "E4":
                # E4智能修复
                repair_type = input_data.get("repair_type", "watermark_removal")
                source_image = input_data.get("source_image", "")
                # 从repair_areas提取修复描述
                repair_areas = input_data.get("repair_areas", [])
                repair_prompt = repair_areas[0].get("description", "智能修复") if repair_areas else "智能修复"
                return self.generate_smart_repair(
                    image_url=source_image,
                    repair_prompt=repair_prompt,
                    repair_type=repair_type
                )

            elif agent_id == "E5":
                # E5结构控制
                control_type = input_data.get("control_type", "pose_control")
                reference_image = input_data.get("reference_image", "")
                target_prompt = input_data.get("target_prompt", "")
                control_strength = input_data.get("control_strength", 0.8)
                return self.generate_structure_control(
                    reference_image=reference_image,
                    target_prompt=target_prompt,
                    control_type=control_type,
                    control_strength=control_strength
                )

            elif agent_id == "E6":
                # E6多图融合
                fusion_type = input_data.get("fusion_type", "creative_combination")
                source_images = input_data.get("source_images", [])
                fusion_prompt = input_data.get("fusion_prompt", "")
                return self.generate_image_fusion(
                    source_images=source_images,
                    fusion_prompt=fusion_prompt,
                    fusion_type=fusion_type
                )

            elif agent_id == "E7":
                # E7角色一致性
                character_type = input_data.get("character_type", "brand_mascot")
                character_reference = input_data.get("character_reference", "")
                scene_prompt = input_data.get("scene_prompt", "")
                consistency_level = input_data.get("consistency_level", 5)
                return self.generate_character_consistency(
                    character_reference=character_reference,
                    scene_prompt=scene_prompt,
                    character_type=character_type,
                    consistency_level=consistency_level
                )

            elif agent_id == "E8":
                # E8设计迭代
                iteration_type = input_data.get("iteration_type", "feedback_response")
                current_version = input_data.get("current_version", "")
                feedback = input_data.get("feedback", "")
                iteration_goals = input_data.get("iteration_goals", [])
                return self.generate_design_iteration(
                    current_version=current_version,
                    feedback=feedback,
                    iteration_type=iteration_type,
                    iteration_goals=iteration_goals
                )

            elif agent_id == "E9":
                # E9超分增强
                enhancement_type = input_data.get("enhancement_type", "intelligent_upscaling")
                source_image = input_data.get("source_image", "")
                target_resolution = input_data.get("target_resolution", "4K")
                enhancement_strength = input_data.get("enhancement_strength", 0.8)
                return self.generate_super_resolution(
                    source_image=source_image,
                    target_resolution=target_resolution,
                    enhancement_type=enhancement_type,
                    enhancement_strength=enhancement_strength
                )

            else:
                return {
                    "success": False,
                    "task_id": task_id,
                    "error": "不支持的智能体",
                    "details": f"agent_id={agent_id} 不在支持范围内 (E1-E9)"
                }

        except json.JSONDecodeError as e:
            return {
                "success": False,
                "task_id": task_id,
                "error": "JSON解析失败",
                "details": str(e)
            }

        except Exception as e:
            return {
                "success": False,
                "task_id": task_id,
                "error": "执行计划失败",
                "details": str(e)
            }

    def unified_generate(self, prompt: str, image_urls: Optional[List[str]] = None,
                        design_type: Optional[str] = None, processing_type: Optional[str] = None,
                        **kwargs) -> Dict[str, Any]:
        """统一生成接口 - 自动判断E1或E2模式"""
        if image_urls:
            # 有图像输入，使用E2图生图
            return self.generate_image_to_image(prompt, image_urls, processing_type, **kwargs)
        else:
            # 无图像输入，使用E1文生图
            return self.generate_text_to_image(prompt, design_type, **kwargs)


# 便捷函数
def create_restaurant_design(prompt: str, design_type: str = "8-main-image", **kwargs):
    """E1文生图便捷函数"""
    api = NanoBananaAPI()
    return api.generate_text_to_image(prompt, design_type, **kwargs)

def process_restaurant_image(prompt: str, image_urls: List[str],
                           processing_type: str = "local_optimization", **kwargs):
    """E2图生图便捷函数"""
    api = NanoBananaAPI()
    return api.generate_image_to_image(prompt, image_urls, processing_type, **kwargs)

def generate_restaurant_content(prompt: str, image_urls: Optional[List[str]] = None, **kwargs):
    """统一生成便捷函数"""
    api = NanoBananaAPI()
    return api.unified_generate(prompt, image_urls, **kwargs)


# 测试和演示代码
def test_e1_text_to_image():
    """测试E1文生图功能"""
    print("🎨 测试E1文生图功能...")

    test_cases = [
        {
            "prompt": "Create a modern Chinese hotpot restaurant poster with festive red colors",
            "design_type": "1-poster"
        },
        {
            "prompt": "Design an elegant Japanese sushi restaurant menu with zen aesthetics",
            "design_type": "2-menu"
        },
        {
            "prompt": "Generate a cozy coffee shop logo with artisanal elements",
            "design_type": "6-icon"
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📸 测试案例 {i}: {test_case['design_type']}")
        result = create_restaurant_design(**test_case)

        if result["success"]:
            print(f"✅ 生成成功: {len(result['image_paths'])} 张图片")
            for path in result["image_paths"]:
                print(f"   📁 {path}")
        else:
            print(f"❌ 生成失败: {result['error']}")

def test_e2_image_to_image():
    """测试E2图生图功能"""
    print("🖼️ 测试E2图生图功能...")

    # 注意：这里需要实际的图像URL
    test_image_url = "https://example.com/restaurant-image.jpg"

    test_cases = [
        {
            "prompt": "Enhance the food presentation and lighting in this restaurant image",
            "image_urls": [test_image_url],
            "processing_type": "local_optimization"
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔄 测试案例 {i}: {test_case['processing_type']}")
        result = process_restaurant_image(**test_case)

        if result["success"]:
            print(f"✅ 处理成功: {len(result['image_paths'])} 张图片")
            for path in result["image_paths"]:
                print(f"   📁 {path}")
        else:
            print(f"❌ 处理失败: {result['error']}")

def main():
    """主函数 - 演示用法"""
    print("🍌 Nano Banana API - 餐饮AIGC图像生成工具")
    print("=" * 60)

    # 测试E1文生图
    test_e1_text_to_image()

    print("\n" + "=" * 60)

    # 测试E2图生图（需要实际图像URL）
    # test_e2_image_to_image()

    print("\n🎉 测试完成！")
    print("📁 生成的文件保存在 output/images/ 和 output/prompts/ 目录下")


if __name__ == "__main__":
    main()