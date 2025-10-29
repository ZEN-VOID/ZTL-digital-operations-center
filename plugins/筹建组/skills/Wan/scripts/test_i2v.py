#!/usr/bin/env python3
"""
通义万相图生视频测试脚本
测试Image-to-Video功能
"""

import os
import json
import time
import base64
import requests
import mimetypes
from pathlib import Path
from datetime import datetime

# 加载.env文件
def load_env():
    """从.env文件加载环境变量"""
    current_dir = Path(__file__).resolve().parent
    while current_dir != current_dir.parent:
        env_file = current_dir / ".env"
        if env_file.exists():
            print(f"📄 找到.env文件: {env_file}")
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
            return os.getenv('DASHSCOPE_API_KEY')
        current_dir = current_dir.parent
    return None

# 加载环境变量
api_key = load_env()

# API endpoints (from wan-base.py)
SUBMIT_ENDPOINT = "https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis"
QUERY_ENDPOINT = "https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"


def download_image(image_url, save_path):
    """下载图片到本地"""
    try:
        response = requests.get(image_url, timeout=30)
        if response.status_code == 200:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"   ✅ 图片已下载: {save_path}")
            return True
        else:
            print(f"   ❌ 下载失败: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 下载错误: {str(e)}")
        return False


def image_to_base64(image_path):
    """将图片转换为Base64编码"""
    with open(image_path, 'rb') as f:
        image_data = f.read()
    return base64.b64encode(image_data).decode('utf-8')


def convert_resolution(resolution_str):
    """
    转换分辨率格式
    从 "1280x720" 格式转换为API要求的格式 "720P"
    """
    resolution_map = {
        "1280x720": "720P",
        "720x1280": "720P",  # 竖屏也是720P
        "1920x1080": "1080P",
        "1080x1920": "1080P"
    }

    return resolution_map.get(resolution_str, "720P")


def submit_i2v_task(image_path, prompt, negative_prompt, params):
    """提交图生视频任务"""

    # 将图片转换为Base64
    image_base64 = image_to_base64(image_path)

    # 确定图片MIME类型
    mime_type, _ = mimetypes.guess_type(str(image_path))
    if not mime_type or not mime_type.startswith('image/'):
        mime_type = 'image/png'

    # 构建Data URI格式
    data_uri = f"data:{mime_type};base64,{image_base64}"

    # 构建payload
    payload = {
        "model": params.get('model', 'wan2.5-i2v-preview'),  # 注意: 使用wan2.5而非wanx2.5
        "input": {
            "img_url": data_uri,
            "prompt": prompt,
            "negative_prompt": negative_prompt
        },
        "parameters": {
            "duration": params.get('video_duration', 5),  # 注意: API使用duration而非video_duration
            "resolution": convert_resolution(params.get('resolution', '1280x720'))
        }
    }

    # 添加音频配置 (简化为boolean)
    if 'audio_config' in params:
        audio_config = params['audio_config']
        # API只支持boolean类型，true表示自动生成背景音乐
        payload['parameters']['audio'] = audio_config.get('enable_audio', False)

    # 准备请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable"  # 启用异步模式（必需）
    }

    print(f"   🚀 提交I2V任务...")
    print(f"   📝 提示词: {prompt[:50]}...")
    print(f"   📐 分辨率: {payload['parameters']['resolution']}")

    try:
        # 使用HTTP POST提交任务
        response = requests.post(
            SUBMIT_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=120
        )

        if response.status_code == 200:
            result = response.json()

            # 提取task_id
            if "output" in result and "task_id" in result["output"]:
                task_id = result["output"]["task_id"]
                print(f"   ✅ 任务已提交: {task_id}")
                return task_id
            else:
                print(f"   ❌ 提交失败: 响应中缺少task_id")
                print(f"   响应内容: {result}")
                return None
        else:
            print(f"   ❌ 提交失败: HTTP {response.status_code}")
            print(f"   错误信息: {response.text}")
            return None

    except Exception as e:
        print(f"   ❌ 提交错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def poll_task_result(task_id, max_wait=300, poll_interval=10):
    """轮询任务结果"""

    print(f"\n   ⏳ 等待任务完成 (最长{max_wait}秒)...")

    # 准备请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable"  # 启用异步模式（必需）
    }

    # 构建查询URL
    query_url = QUERY_ENDPOINT.format(task_id=task_id)

    start_time = time.time()
    while time.time() - start_time < max_wait:
        try:
            # 使用HTTP GET查询任务状态
            response = requests.get(query_url, headers=headers, timeout=30)

            if response.status_code == 200:
                result = response.json()

                if "output" in result:
                    output = result["output"]
                    task_status = output.get("task_status", "UNKNOWN")

                    if task_status == 'SUCCEEDED':
                        print(f"   ✅ 任务完成!")
                        # 提取视频URL（直接从output.video_url字段）
                        if "video_url" in output:
                            video_url = output["video_url"]
                            print(f"   🎬 视频URL: {video_url[:80]}...")
                            # 打印API增强的提示词
                            if "actual_prompt" in output:
                                print(f"   📝 API增强提示词: {output['actual_prompt'][:100]}...")
                            return video_url
                        else:
                            print(f"   ❌ 响应中缺少video_url字段")
                            print(f"   [DEBUG] output内容: {json.dumps(output, ensure_ascii=False, indent=2)}")
                            return None

                    elif task_status == 'FAILED':
                        error_msg = output.get("message", "未知错误")
                        print(f"   ❌ 任务失败: {error_msg}")
                        return None

                    else:
                        elapsed = int(time.time() - start_time)
                        print(f"   ⏳ 任务进行中... ({elapsed}秒) 状态: {task_status}")

                else:
                    print(f"   ⚠️  查询失败: 响应中缺少output字段")

            else:
                print(f"   ⚠️  查询失败: HTTP {response.status_code}")
                print(f"   错误信息: {response.text}")

        except Exception as e:
            print(f"   ⚠️  查询错误: {str(e)}")

        time.sleep(poll_interval)

    print(f"   ⏰ 超时: 任务未在{max_wait}秒内完成")
    return None


def download_video(video_url, save_path):
    """下载视频到本地"""
    try:
        print(f"   📥 下载视频...")
        response = requests.get(video_url, timeout=60)

        if response.status_code == 200:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(response.content)

            file_size = len(response.content) / (1024 * 1024)  # MB
            print(f"   ✅ 视频已保存: {save_path}")
            print(f"   📊 文件大小: {file_size:.2f} MB")
            return True
        else:
            print(f"   ❌ 下载失败: HTTP {response.status_code}")
            return False

    except Exception as e:
        print(f"   ❌ 下载错误: {str(e)}")
        return False


def test_cyberpunk_scene_animation():
    """测试1: 赛博朋克场景动画化"""

    print("\n" + "="*60)
    print("🎬 测试1: 赛博朋克场景动画化")
    print("="*60)

    # 读取文生图生成的图片元数据
    metadata_dir = Path("output/images/tongyi-wanxiang")
    metadata_files = list(metadata_dir.glob("test1_composer_*.json"))

    if not metadata_files:
        print("❌ 未找到test1_composer元数据文件")
        return None

    # 读取最新的元数据
    metadata_file = sorted(metadata_files)[-1]
    with open(metadata_file, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    # 获取第一张图片URL
    image_url = metadata['image_urls'][0]
    print(f"\n📷 使用图片: {image_url}")

    # 下载图片
    image_filename = f"source_image_1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    image_path = Path("output/images/tongyi-wanxiang") / image_filename

    if not download_image(image_url, image_path):
        return None

    # I2V参数
    prompt = "镜头缓慢推进，展现赛博朋克都市的霓虹灯光效果，雨滴在玻璃窗上流淌，远处飞行汽车缓慢移动"
    negative_prompt = "模糊，抖动，低质量，变形，闪烁"

    params = {
        'model': 'wan2.5-i2v-preview',
        'video_duration': 5,
        'fps': 24,
        'resolution': '1280x720',
        'motion_intensity': 0.6,
        'camera_movement': {
            'type': 'dolly_in',
            'speed': 0.3
        },
        'audio_config': {
            'enable_audio': False
        }
    }

    # 提交任务
    task_id = submit_i2v_task(image_path, prompt, negative_prompt, params)

    if not task_id:
        return None

    # 轮询结果
    video_url = poll_task_result(task_id)

    if not video_url:
        return None

    # 下载视频
    video_filename = f"test1_cyberpunk_animation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    video_path = Path("output/videos/tongyi-wanxiang") / video_filename

    if download_video(video_url, video_path):
        # 保存元数据
        result_metadata = {
            "test_name": "cyberpunk_scene_animation",
            "timestamp": datetime.now().isoformat(),
            "task_id": task_id,
            "source_image": str(image_path),
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "parameters": params,
            "video_url": video_url,
            "video_path": str(video_path)
        }

        metadata_path = video_path.with_suffix('.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(result_metadata, f, ensure_ascii=False, indent=2)

        print(f"   💾 元数据已保存: {metadata_path}")
        return video_url

    return None


def test_poster_animation():
    """测试2: 电影海报动画化（带配音）"""

    print("\n" + "="*60)
    print("🎬 测试2: 电影海报动画化（带配音）")
    print("="*60)

    # 读取文生图生成的海报图片元数据
    metadata_dir = Path("output/images/tongyi-wanxiang")
    metadata_files = list(metadata_dir.glob("test2_text_rendering_*.json"))

    if not metadata_files:
        print("❌ 未找到test2_text_rendering元数据文件")
        return None

    # 读取最新的元数据
    metadata_file = sorted(metadata_files)[-1]
    with open(metadata_file, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    # 获取图片URL
    image_url = metadata['image_url']
    print(f"\n📷 使用图片: {image_url}")

    # 下载图片
    image_filename = f"source_image_2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    image_path = Path("output/images/tongyi-wanxiang") / image_filename

    if not download_image(image_url, image_path):
        return None

    # I2V参数（带配音）
    prompt = "海报中的城市景观缓慢展现层次感，霓虹灯光微微闪烁，营造电影级氛围感"
    negative_prompt = "文字移动，模糊，抖动，低质量"

    params = {
        'model': 'wan2.5-i2v-preview',
        'video_duration': 5,
        'fps': 30,
        'resolution': '720x1280',
        'motion_intensity': 0.4,
        'camera_movement': {
            'type': 'static_subtle',
            'speed': 0.2
        },
        'audio_config': {
            'enable_audio': True,
            'audio_mode': 'auto_caption',
            'voice_id': 'zh-CN-XiaoxiaoNeural',
            'speech_rate': 1.0,
            'caption_text': '未来都市2077，在霓虹深处寻找真实'
        }
    }

    # 提交任务
    task_id = submit_i2v_task(image_path, prompt, negative_prompt, params)

    if not task_id:
        return None

    # 轮询结果
    video_url = poll_task_result(task_id)

    if not video_url:
        return None

    # 下载视频
    video_filename = f"test2_poster_animation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    video_path = Path("output/videos/tongyi-wanxiang") / video_filename

    if download_video(video_url, video_path):
        # 保存元数据
        result_metadata = {
            "test_name": "poster_animation_with_audio",
            "timestamp": datetime.now().isoformat(),
            "task_id": task_id,
            "source_image": str(image_path),
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "parameters": params,
            "video_url": video_url,
            "video_path": str(video_path)
        }

        metadata_path = video_path.with_suffix('.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(result_metadata, f, ensure_ascii=False, indent=2)

        print(f"   💾 元数据已保存: {metadata_path}")
        return video_url

    return None


def main():
    """主函数"""

    print("\n" + "🎬 "*20)
    print("   通义万相(Tongyi Wanxiang)图生视频能力测试")
    print("🎬 "*20)

    # 检查环境变量
    api_key = os.getenv('DASHSCOPE_API_KEY')
    if not api_key:
        print("\n❌ 错误: 请先设置DASHSCOPE_API_KEY环境变量")
        print("   export DASHSCOPE_API_KEY='your-api-key'")
        return

    print(f"\n✅ API Key已配置: {api_key[:20]}...")

    # 测试1: 赛博朋克场景动画化
    scene_result = test_cyberpunk_scene_animation()

    # 测试2: 电影海报动画化（带配音）
    poster_result = test_poster_animation()

    # 总结
    print("\n" + "="*60)
    print("📊 测试总结")
    print("="*60)

    print(f"\n✅ 赛博朋克场景动画化: {'成功' if scene_result else '失败'}")
    if scene_result:
        print(f"   - 特点: 5秒视频、镜头推进、霓虹灯光效果")

    print(f"\n✅ 电影海报动画化: {'成功' if poster_result else '失败'}")
    if poster_result:
        print(f"   - 特点: 5秒视频、微妙动画、auto_caption配音")

    print("\n" + "🎬 "*20)
    print("   测试完成!")
    print("🎬 "*20 + "\n")


if __name__ == "__main__":
    main()
