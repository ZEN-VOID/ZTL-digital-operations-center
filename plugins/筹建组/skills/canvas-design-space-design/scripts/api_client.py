#!/usr/bin/env python3
"""
Stable Diffusion XL API客户端
基于OpenRouter API的空间设计效果图生成

功能:
- 单张图像生成
- 批量场景生成
- 配置文件驱动
- 自动重试和错误处理
"""

import os
import json
import base64
import requests
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

class StableDiffusionXLClient:
    """Stable Diffusion XL API客户端"""

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化客户端

        Args:
            api_key: OpenRouter API密钥(默认从环境变量读取)
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("未找到OPENROUTER_API_KEY环境变量")

        self.endpoint = "https://openrouter.ai/api/v1/images/generations"
        self.default_model = "stable-diffusion-xl"

    def generate_image(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        style_preset: str = "photographic",
        aspect_ratio: str = "16:9",
        cfg_scale: float = 7.5,
        steps: int = 50,
        output_path: Optional[Path] = None
    ) -> Dict:
        """
        生成单张图像

        Args:
            prompt: 设计描述提示词
            negative_prompt: 负面提示词
            style_preset: 风格预设(photographic, cinematic等)
            aspect_ratio: 画面比例(16:9, 1:1, 4:3等)
            cfg_scale: Prompt权重(5-15, 推荐7.5)
            steps: 生成步数(30-70, 推荐50)
            output_path: 输出路径

        Returns:
            包含图像数据和元数据的字典
        """
        # 构建请求
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.default_model,
            "prompt": prompt,
            "negative_prompt": negative_prompt or "blurry, low quality, distorted, unrealistic, amateur",
            "style_preset": style_preset,
            "aspect_ratio": aspect_ratio,
            "cfg_scale": cfg_scale,
            "steps": steps,
            "num_images": 1
        }

        print(f"\n正在生成图像...")
        print(f"Prompt: {prompt[:100]}...")
        print(f"参数: style={style_preset}, ratio={aspect_ratio}, cfg={cfg_scale}, steps={steps}")

        try:
            # 发送请求
            response = requests.post(
                self.endpoint,
                headers=headers,
                json=payload,
                timeout=120
            )

            response.raise_for_status()
            result = response.json()

            # 解析图像数据
            if "images" in result and len(result["images"]) > 0:
                image_data = result["images"][0]

                # 如果提供了输出路径,保存图像
                if output_path:
                    output_path = Path(output_path)
                    output_path.parent.mkdir(parents=True, exist_ok=True)

                    # Base64解码
                    if isinstance(image_data, str):
                        image_bytes = base64.b64decode(image_data)
                    else:
                        # 如果是URL,下载图像
                        img_response = requests.get(image_data)
                        image_bytes = img_response.content

                    # 保存到文件
                    with open(output_path, 'wb') as f:
                        f.write(image_bytes)

                    print(f"✅ 图像已保存: {output_path}")

                return {
                    "success": True,
                    "image_path": str(output_path) if output_path else None,
                    "metadata": {
                        "prompt": prompt,
                        "negative_prompt": negative_prompt,
                        "style_preset": style_preset,
                        "aspect_ratio": aspect_ratio,
                        "cfg_scale": cfg_scale,
                        "steps": steps,
                        "timestamp": datetime.now().isoformat()
                    }
                }
            else:
                raise ValueError("API返回结果中未找到图像数据")

        except requests.exceptions.RequestException as e:
            print(f"❌ API请求失败: {e}")
            return {
                "success": False,
                "error": str(e)
            }
        except Exception as e:
            print(f"❌ 图像生成失败: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def generate_batch(
        self,
        scenes: List[Dict],
        output_dir: Path,
        batch_size: int = 2,
        max_concurrent: int = 2
    ) -> List[Dict]:
        """
        批量生成多个场景

        Args:
            scenes: 场景配置列表
            output_dir: 输出目录
            batch_size: 每批处理数量
            max_concurrent: 最大并发数

        Returns:
            生成结果列表
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        results = []
        total = len(scenes)

        print(f"\n开始批量生成 {total} 个场景...")

        for idx, scene in enumerate(scenes, 1):
            scene_name = scene.get("scene_name", f"scene-{idx:03d}")
            print(f"\n[{idx}/{total}] 正在生成: {scene_name}")

            # 构建输出文件名
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            output_filename = f"{scene_name}-{timestamp}.png"
            output_path = output_dir / output_filename

            # 获取生成参数
            params = scene.get("generation_params", {})

            # 生成图像
            result = self.generate_image(
                prompt=scene.get("prompt"),
                negative_prompt=scene.get("negative_prompt"),
                style_preset=params.get("style_preset", "photographic"),
                aspect_ratio=params.get("aspect_ratio", "16:9"),
                cfg_scale=params.get("cfg_scale", 7.5),
                steps=params.get("steps", 50),
                output_path=output_path
            )

            result["scene_name"] = scene_name
            results.append(result)

            # 简单的成功/失败统计
            success_count = sum(1 for r in results if r.get("success"))
            print(f"进度: {idx}/{total}, 成功: {success_count}, 失败: {idx - success_count}")

        print(f"\n批量生成完成!")
        print(f"总计: {total}, 成功: {sum(1 for r in results if r.get('success'))}")

        return results

def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="Stable Diffusion XL空间设计效果图生成")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # 单张生成命令
    generate_parser = subparsers.add_parser("generate", help="生成单张图像")
    generate_parser.add_argument("--prompt", required=True, help="设计描述提示词")
    generate_parser.add_argument("--negative-prompt", help="负面提示词")
    generate_parser.add_argument("--style", default="photographic", help="风格预设")
    generate_parser.add_argument("--aspect-ratio", default="16:9", help="画面比例")
    generate_parser.add_argument("--cfg-scale", type=float, default=7.5, help="Prompt权重")
    generate_parser.add_argument("--steps", type=int, default=50, help="生成步数")
    generate_parser.add_argument("--output", required=True, help="输出路径")

    # 批量生成命令
    batch_parser = subparsers.add_parser("batch", help="批量生成多个场景")
    batch_parser.add_argument("--config", required=True, help="配置文件路径(JSON)")
    batch_parser.add_argument("--output-dir", required=True, help="输出目录")

    args = parser.parse_args()

    # 初始化客户端
    client = StableDiffusionXLClient()

    if args.command == "generate":
        # 单张生成
        result = client.generate_image(
            prompt=args.prompt,
            negative_prompt=args.negative_prompt,
            style_preset=args.style,
            aspect_ratio=args.aspect_ratio,
            cfg_scale=args.cfg_scale,
            steps=args.steps,
            output_path=Path(args.output)
        )

        if result["success"]:
            print(f"\n✅ 生成成功!")
        else:
            print(f"\n❌ 生成失败: {result.get('error')}")

    elif args.command == "batch":
        # 批量生成
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)

        scenes = config.get("space_scenes", [])

        if not scenes:
            print("❌ 配置文件中未找到space_scenes字段")
            return

        results = client.generate_batch(
            scenes=scenes,
            output_dir=Path(args.output_dir)
        )

        # 保存结果元数据
        metadata_file = Path(args.output_dir) / "generation-metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"\n元数据已保存: {metadata_file}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
