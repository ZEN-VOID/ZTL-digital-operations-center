# Z4-建筑动画AIGC助手 使用指南

> **Z4智能体**: 使用Wan Image-to-Video (i2v)技术将Z2的空间设计图像转换为动态视频
>
> **技术基础**: 阿里云通义万相 wan2.5-i2v-preview 模型
>
> **版本**: v1.0.0 | **更新日期**: 2025-10-28

---

## 📋 目录

- [1. 快速开始](#1-快速开始)
- [2. 完整工作流](#2-完整工作流)
- [3. 配置指南](#3-配置指南)
- [4. Prompt工程](#4-prompt工程)
- [5. 质量控制](#5-质量控制)
- [6. 故障排查](#6-故障排查)
- [7. 成本管理](#7-成本管理)
- [8. 最佳实践](#8-最佳实践)

---

## 1. 快速开始

### 1.1 前置条件

**✅ 必需准备:**

```yaml
环境:
  - Python 3.9+
  - DashScope API Key (已配置在环境变量)

输入:
  - Z2输出的PNG图像 (≥1024×1024推荐)
  - 存储路径: output/[项目名]/Z2-空间概念设计师/

技能包:
  - Wan技能包: plugins/筹建组/skills/Wan/
  - 包含 wan-base.py 和 test_i2v.py
```

**环境变量检查:**

```bash
# 验证DashScope API Key是否配置
echo $DASHSCOPE_API_KEY

# 如果未配置,请设置
export DASHSCOPE_API_KEY="sk-your-api-key-here"

# 永久设置 (添加到 ~/.zshrc 或 ~/.bash_profile)
echo 'export DASHSCOPE_API_KEY="sk-your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### 1.2 5分钟快速测试

**Step 1: 准备测试图像**

```bash
# 假设Z2已经生成了图像
ls output/火锅店开业筹备/Z2-空间概念设计师/

# 输出示例:
# 餐厅-主用餐区-全景.png
# 餐厅-入口月洞门.png
# ...
```

**Step 2: 创建简单测试脚本**

```python
# quick_test_z4.py

from plugins.筹建组.skills.Wan.scripts.wan_base import WanAPIClient
import os

# 1. 初始化客户端
client = WanAPIClient()

# 2. 准备输入
image_path = "output/火锅店开业筹备/Z2-空间概念设计师/餐厅-主用餐区-全景.png"
prompt = """
镜头缓慢向前推进，穿过主用餐区，两侧摆放精致圆桌和舒适座椅，
暖黄灯光从吊灯洒下，营造温馨用餐氛围，背景文化墙装饰若隐若现，
木质材料与现代设计完美融合，画面层次丰富，细节清晰自然
"""

# 3. 提交任务
print("🚀 提交视频生成任务...")
task_id = client.submit_i2v_task(
    image_path=image_path,
    prompt=prompt.strip(),
    negative_prompt="模糊不清、画面抖动、人物变形、光线过曝、色彩失真",
    params={
        "model": "wan2.5-i2v-preview",
        "size": "1280*720",
        "duration": "6s",
        "fps": 16
    }
)

print(f"✅ 任务ID: {task_id}")

# 4. 等待完成
import time
while True:
    status = client.query_task_status(task_id)
    if status == "SUCCEEDED":
        print("✅ 视频生成成功!")
        break
    elif status == "FAILED":
        print("❌ 生成失败")
        exit(1)
    else:
        print(f"⏳ 生成中... ({status})")
        time.sleep(10)

# 5. 下载视频
output_path = "output/火锅店开业筹备/Z4-建筑动画AIGC助手/test-video.mp4"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
client.download_video(task_id, output_path)

print(f"✅ 视频已保存: {output_path}")
print(f"💰 本次成本: ¥0.35")
```

**Step 3: 运行测试**

```bash
python quick_test_z4.py

# 预期输出:
# 🚀 提交视频生成任务...
# ✅ 任务ID: task-xxx-xxx-xxx
# ⏳ 生成中... (PROCESSING)
# ⏳ 生成中... (PROCESSING)
# ✅ 视频生成成功!
# ✅ 视频已保存: output/火锅店开业筹备/Z4-建筑动画AIGC助手/test-video.mp4
# 💰 本次成本: ¥0.35
```

**Step 4: 查看生成的视频**

```bash
# macOS
open "output/火锅店开业筹备/Z4-建筑动画AIGC助手/test-video.mp4"

# Linux
xdg-open "output/火锅店开业筹备/Z4-建筑动画AIGC助手/test-video.mp4"
```

✅ **如果能看到平滑的推进镜头视频,说明环境配置正确!**

---

## 2. 完整工作流

### 2.1 工作流概览

```
Z2-空间概念设计师
    ↓ 输出PNG图像
Z4-建筑动画AIGC助手 (你)
    ↓
    [Phase 1] 接收与分析 (5分钟)
      ├─ 扫描Z2输出目录
      ├─ 读取所有PNG文件
      ├─ 分析场景类型和视角
      └─ 生成执行计划JSON
    ↓
    [Phase 2] Prompt工程 (10-15分钟)
      ├─ 为每张图匹配镜头类型
      ├─ 生成中文Prompt (80-150字)
      ├─ 定义Negative Prompt
      └─ 记录到执行计划
    ↓
    [Phase 3] 批量生成 (20-30分钟)
      ├─ 并行提交5个API任务
      ├─ 轮询任务状态
      ├─ 下载生成的视频
      └─ 按场景分类存储
    ↓
    [Phase 4] 质量验收 (5-10分钟)
      ├─ 技术指标检查 (分辨率、时长、播放)
      ├─ 视觉质量检查 (清晰度、色彩、运动)
      ├─ 创意质量检查 (镜头、氛围、突出点)
      └─ 问题视频重新生成
    ↓
    [Phase 5] 交付打包 (5分钟)
      ├─ 按场景整理文件
      ├─ 生成视频清单文档
      ├─ 生成成本报告
      ├─ 可选: 合并为完整walkthrough
      └─ 通知ZZ完成
    ↓
最终交付: MP4视频 + 文档 + 元数据
```

### 2.2 Phase 1: 接收与分析

**2.2.1 扫描Z2输出**

```python
import os
import glob
from pathlib import Path

def scan_z2_output(project_name: str) -> list:
    """
    扫描Z2输出的PNG图像

    Args:
        project_name: 项目名称 (如 "火锅店开业筹备")

    Returns:
        PNG文件路径列表
    """
    z2_path = f"output/{project_name}/Z2-空间概念设计师/"

    # 查找所有PNG文件
    images = glob.glob(f"{z2_path}/*.png")

    print(f"✅ 扫描Z2输出目录: {z2_path}")
    print(f"✅ 找到{len(images)}张PNG图像:")
    for img in images:
        filename = os.path.basename(img)
        file_size = os.path.getsize(img) / (1024 * 1024)  # MB
        print(f"   - {filename} ({file_size:.2f} MB)")

    return sorted(images)

# 使用示例
images = scan_z2_output("火锅店开业筹备")
```

**2.2.2 场景类型识别**

```python
def identify_scene_type(image_filename: str) -> dict:
    """
    基于文件名识别场景类型

    Returns:
        {
            "scene_type": str,     # entrance, main_dining, private_room, detail
            "viewpoint": str,      # panoramic, close-up, aerial, eye-level
            "suggested_camera": str # push, orbit, pan, crane
        }
    """
    filename = os.path.basename(image_filename).lower()

    # 场景类型映射
    scene_keywords = {
        "entrance": ["入口", "门头", "月洞门", "exterior"],
        "waiting_area": ["等候", "等待", "前厅", "lobby"],
        "main_dining": ["主用餐", "大厅", "dining hall", "散台"],
        "private_room": ["包间", "包厢", "private", "vip"],
        "booth": ["卡座", "booth"],
        "detail": ["特写", "细节", "detail", "close"],
        "bar": ["吧台", "bar"],
        "restroom": ["洗手间", "卫生间", "restroom"]
    }

    # 视角关键词
    viewpoint_keywords = {
        "panoramic": ["全景", "panoramic", "wide"],
        "close-up": ["特写", "细节", "close-up", "detail"],
        "aerial": ["俯瞰", "俯视", "aerial", "overhead"],
        "side": ["侧面", "side view"]
    }

    # 识别场景类型
    scene_type = "unknown"
    for scene, keywords in scene_keywords.items():
        if any(kw in filename for kw in keywords):
            scene_type = scene
            break

    # 识别视角
    viewpoint = "eye-level"  # 默认平视
    for view, keywords in viewpoint_keywords.items():
        if any(kw in filename for kw in keywords):
            viewpoint = view
            break

    # 建议镜头运动
    camera_suggestions = {
        "entrance": "push",
        "waiting_area": "lateral_pan",
        "main_dining": "push" if viewpoint == "panoramic" else "lateral_pan",
        "private_room": "orbit",
        "detail": "close_up_push",
        "aerial": "crane_up"
    }

    suggested_camera = camera_suggestions.get(scene_type, "push")

    return {
        "scene_type": scene_type,
        "viewpoint": viewpoint,
        "suggested_camera": suggested_camera
    }

# 使用示例
analysis = identify_scene_type("餐厅-主用餐区-全景.png")
print(analysis)
# Output: {'scene_type': 'main_dining', 'viewpoint': 'panoramic', 'suggested_camera': 'push'}
```

### 2.3 Phase 2: Prompt工程

**2.3.1 加载Prompt模板库**

Prompt模板库已包含在 `Z4-建筑动画AIGC助手.md` 中,包括:
- 6种镜头运动类型 (推进、环绕、横移、升降、拉远、特写)
- 4类场景氛围描述 (温馨、高级、文化、活力)
- 完整的组装策略

**2.3.2 智能Prompt生成**

```python
def generate_prompt(scene_analysis: dict, design_style: str = "modern_chinese") -> str:
    """
    基于场景分析生成中文Prompt

    Args:
        scene_analysis: identify_scene_type() 返回的分析结果
        design_style: 设计风格 (modern_chinese, traditional, premium, etc.)

    Returns:
        完整的中文Prompt字符串 (80-150字)
    """
    scene_type = scene_analysis["scene_type"]
    camera_movement = scene_analysis["suggested_camera"]

    # 镜头运动描述库
    camera_phrases = {
        "push": "镜头缓慢向前推进",
        "orbit": "镜头围绕{焦点}缓慢旋转",
        "lateral_pan": "镜头从左至右平稳横移",
        "crane_up": "镜头从平视缓慢上升至俯视角度",
        "pull_out": "镜头从{起点}缓慢拉远",
        "close_up_push": "镜头聚焦{对象}，缓慢推进特写"
    }

    # 场景描述库
    scene_descriptions = {
        "entrance": "穿过精致的月洞门框架，进入典雅的等候区，暖色灯光映照古典家具",
        "waiting_area": "依次展现文化墙装饰、舒适沙发、茶水吧台，完整呈现等候区的功能布局和文化氛围",
        "main_dining": "穿过主用餐区，两侧摆放精致圆桌和舒适座椅，暖黄灯光从吊灯洒下，营造温馨用餐氛围",
        "private_room": "360度展现私密空间设计，高级灰墙面搭配暖色木饰面，精致吊灯投下柔和光影",
        "detail": "清晰展现材质肌理和质感，暖光下更显自然雅致"
    }

    # 氛围强化
    atmosphere_phrases = {
        "modern_chinese": "展现茶文化与现代设计的完美融合，空间宁静而富有韵味",
        "traditional": "传统工艺与古典审美交相辉映，讲述悠久的餐饮文化",
        "premium": "细节处处体现品质，适合重要宴请场合",
        "natural": "返璞归真的设计理念，亲近自然"
    }

    # 组装Prompt
    camera_desc = camera_phrases.get(camera_movement, "镜头缓慢移动")
    scene_desc = scene_descriptions.get(scene_type, "展现空间设计")
    atmosphere = atmosphere_phrases.get(design_style, "营造专业氛围")

    prompt = f"{camera_desc}，{scene_desc}，{atmosphere}，画面层次丰富，细节清晰自然"

    # 长度控制 (80-150字)
    if len(prompt) < 80:
        prompt += "，光影层次分明，材质质感真实"
    elif len(prompt) > 150:
        prompt = prompt[:147] + "..."

    return prompt

# 使用示例
scene = identify_scene_type("餐厅-主用餐区-全景.png")
prompt = generate_prompt(scene, design_style="modern_chinese")
print(f"生成的Prompt ({len(prompt)}字):\n{prompt}")
```

**2.3.3 Negative Prompt标准模板**

```python
NEGATIVE_PROMPTS = {
    "standard": "模糊不清、画面抖动、人物变形、光线过曝、色彩失真、物体穿模、空间比例失调、材质混乱",
    "high_quality": "模糊不清、画面抖动、人物变形、光线过曝、色彩失真、物体穿模、空间比例失调、材质混乱、低分辨率、噪点过多、帧率不稳、运动轨迹不自然、焦点模糊、细节丢失、构图失衡",
    "detail_shot": "模糊不清、画面抖动、色彩失真、焦点模糊、细节丢失、材质失真、光线不足"
}

def get_negative_prompt(scene_type: str) -> str:
    """获取适合场景类型的Negative Prompt"""
    if scene_type == "detail":
        return NEGATIVE_PROMPTS["detail_shot"]
    elif scene_type in ["entrance", "main_dining"]:
        return NEGATIVE_PROMPTS["high_quality"]
    else:
        return NEGATIVE_PROMPTS["standard"]
```

### 2.4 Phase 3: 批量生成

**2.4.1 并行任务提交**

```python
import concurrent.futures
from typing import List, Dict

def submit_batch_tasks(tasks: List[Dict]) -> List[str]:
    """
    并行提交多个视频生成任务

    Args:
        tasks: 任务列表,每个任务包含 {image_path, prompt, negative_prompt, params}

    Returns:
        任务ID列表
    """
    client = WanAPIClient()
    task_ids = []

    # 使用ThreadPoolExecutor并行提交
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for task in tasks:
            future = executor.submit(
                client.submit_i2v_task,
                image_path=task["image_path"],
                prompt=task["prompt"],
                negative_prompt=task["negative_prompt"],
                params=task["params"]
            )
            futures.append(future)

        # 收集任务ID
        for future in concurrent.futures.as_completed(futures):
            task_id = future.result()
            task_ids.append(task_id)
            print(f"✅ 提交任务: {task_id}")

    return task_ids

# 使用示例
tasks = [
    {
        "image_path": "output/.../餐厅-入口.png",
        "prompt": "镜头缓慢向前推进...",
        "negative_prompt": "模糊不清、画面抖动...",
        "params": {"model": "wan2.5-i2v-preview", "size": "1280*720", "duration": "6s"}
    },
    # ... 更多任务
]

task_ids = submit_batch_tasks(tasks)
print(f"✅ 已提交{len(task_ids)}个任务")
```

**2.4.2 智能任务监控**

```python
def monitor_tasks(task_ids: List[str], check_interval: int = 10) -> Dict[str, str]:
    """
    监控多个任务的执行状态

    Args:
        task_ids: 任务ID列表
        check_interval: 检查间隔(秒)

    Returns:
        {task_id: status} 字典
    """
    client = WanAPIClient()
    task_status = {tid: "PENDING" for tid in task_ids}

    while True:
        # 检查所有未完成任务
        pending_tasks = [
            tid for tid, status in task_status.items()
            if status not in ["SUCCEEDED", "FAILED"]
        ]

        if not pending_tasks:
            break

        # 并行查询状态
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {
                executor.submit(client.query_task_status, tid): tid
                for tid in pending_tasks
            }

            for future in concurrent.futures.as_completed(futures):
                tid = futures[future]
                status = future.result()
                task_status[tid] = status

        # 打印进度
        succeeded = sum(1 for s in task_status.values() if s == "SUCCEEDED")
        failed = sum(1 for s in task_status.values() if s == "FAILED")
        processing = len(pending_tasks)

        print(f"⏳ 进度: ✅ {succeeded}/{len(task_ids)} | ❌ {failed} | ⏳ {processing}")

        if pending_tasks:
            time.sleep(check_interval)

    return task_status

# 使用示例
final_status = monitor_tasks(task_ids, check_interval=10)
print(f"✅ 全部完成: {sum(1 for s in final_status.values() if s == 'SUCCEEDED')}/{len(task_ids)}")
```

**2.4.3 批量下载**

```python
def download_videos(task_results: Dict[str, str], output_config: Dict):
    """
    批量下载生成的视频

    Args:
        task_results: {task_id: status} 字典
        output_config: 输出配置 {task_id: output_path}
    """
    client = WanAPIClient()

    succeeded_tasks = [tid for tid, status in task_results.items() if status == "SUCCEEDED"]

    print(f"📥 开始下载{len(succeeded_tasks)}个视频...")

    for i, task_id in enumerate(succeeded_tasks, 1):
        output_path = output_config[task_id]
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        try:
            client.download_video(task_id, output_path)
            print(f"✅ [{i}/{len(succeeded_tasks)}] 已下载: {os.path.basename(output_path)}")
        except Exception as e:
            print(f"❌ [{i}/{len(succeeded_tasks)}] 下载失败: {e}")

    print(f"✅ 下载完成: {len(succeeded_tasks)}个视频")
```

### 2.5 Phase 4: 质量验收

质量验收代码已包含在 Z4 agent定义的 Step 5 中,包括:
- 自动化技术检查 (分辨率、时长、文件大小)
- 人工复核清单 (视觉质量、创意质量)
- 重新生成决策逻辑

### 2.6 Phase 5: 交付打包

**生成视频清单文档**

```python
def generate_video_list(videos: List[Dict], output_path: str):
    """
    生成视频清单Markdown文档

    Args:
        videos: [{filename, scene_type, duration, cost, prompt}, ...]
        output_path: 输出Markdown文件路径
    """
    content = """# Z4视频生成清单

**项目名称**: {project_name}
**生成日期**: {date}
**视频总数**: {total_videos}
**总成本**: ¥{total_cost}

---

## 视频列表

| 序号 | 文件名 | 场景类型 | 时长 | 分辨率 | 成本 |
|------|--------|---------|------|--------|------|
"""

    # 添加视频行
    for i, video in enumerate(videos, 1):
        content += f"| {i} | {video['filename']} | {video['scene_type']} | {video['duration']}s | {video['resolution']} | ¥{video['cost']} |\n"

    content += f"""
---

## 成本统计

- **单视频成本**: ¥0.35
- **总成本**: ¥{len(videos) * 0.35:.2f}
- **支付方式**: DashScope账户余额

## Prompt记录

详见: `metadata/prompts-used.json`

## 输出路径

```
output/{project_name}/Z4-建筑动画AIGC助手/
├── 01-entrance/
├── 02-waiting-area/
├── 03-main-dining/
├── 04-private-rooms/
└── 05-details/
```
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ 视频清单已生成: {output_path}")
```

**视频合并脚本**

```python
import subprocess

def merge_videos(video_list: List[str], output_path: str):
    """
    使用FFmpeg合并多个视频片段

    Args:
        video_list: 视频文件路径列表 (按播放顺序)
        output_path: 输出文件路径
    """
    # 创建FFmpeg输入文件列表
    concat_file = "temp_concat_list.txt"
    with open(concat_file, "w") as f:
        for video in video_list:
            # FFmpeg要求绝对路径或相对路径
            abs_path = os.path.abspath(video)
            f.write(f"file '{abs_path}'\n")

    # 执行FFmpeg合并命令
    cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        "-c", "copy",  # 直接复制编码流,不重新编码
        output_path
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ 已合并{len(video_list)}个视频: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg合并失败: {e.stderr.decode()}")
    finally:
        # 清理临时文件
        if os.path.exists(concat_file):
            os.remove(concat_file)

# 使用示例
video_sequence = [
    "results/01-entrance/火锅店-入口-推进镜头-01.mp4",
    "results/02-waiting-area/火锅店-等候区-横移镜头-03.mp4",
    "results/03-main-dining/火锅店-主用餐区-全景推进-04.mp4",
    # ... 更多视频
]

merge_videos(video_sequence, "results/合集-完整版.mp4")
```

---

## 3. 配置指南

### 3.0 架构说明（自包含设计）⭐

**Wan Skill 已完全自包含**，无需外部依赖：

```yaml
架构优化:
  原架构: ❌ 跨目录依赖
    - scripts/wan_api_manager.py (项目级工具)
    - plugins/筹建组/skills/Wan/scripts/wan-base.py
    - 问题: 违反Skills自包含原则，部署复杂

  新架构: ✅ 完全自包含
    - plugins/筹建组/skills/Wan/scripts/wan-base.py
    - 内置 WanAPIManager 类
    - 无外部依赖，开箱即用

优势:
  ✅ 符合Claude Code Skills设计原则
  ✅ 简化部署和测试流程
  ✅ 独立可复用，易于分发
  ✅ 路径管理更清晰

导入方式:
  # 标准导入（推荐）
  from plugins.筹建组.skills.Wan.scripts.wan_base import WanAPIClient

  # 内置的 WanAPIManager 会自动处理 API Key
  client = WanAPIClient()  # 自动从 .env 读取配置
```

**环境变量配置：**

在项目根目录的 `.env` 文件中配置 API Key：

```bash
# 阿里云DashScope API Key（两种方式任选其一）
DASHSCOPE_API_KEY=sk-your-api-key-here
# 或者
ALIYUN_API_KEY=sk-your-api-key-here
```

**验证配置：**

```python
from plugins.筹建组.skills.Wan.scripts.wan_base import WanAPIClient

try:
    client = WanAPIClient()
    print("✅ API Key 配置正确")
except ValueError as e:
    print(f"❌ 配置错误: {e}")
```

### 3.1 使用JSON配置模板

项目提供了标准JSON配置模板: `config-template-z4-wan-i2v.json`

**加载和使用配置:**

```python
import json

# 1. 加载配置模板
with open("plugins/筹建组/skills/canvas-design-3d-generation/config-template-z4-wan-i2v.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# 2. 修改项目信息
config["project_info"]["project_name"] = "新项目名称"
config["project_info"]["client_name"] = "客户名称"

# 3. 根据实际图像生成任务
# (参考模板中的12个示例任务)

# 4. 保存执行计划
output_plan_path = f"output/{config['project_info']['project_name']}/Z4-建筑动画AIGC助手/execution-plan.json"
os.makedirs(os.path.dirname(output_plan_path), exist_ok=True)

with open(output_plan_path, "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print(f"✅ 执行计划已保存: {output_plan_path}")
```

### 3.2 关键配置参数

**API配置:**

```json
"execution_config": {
  "model": "wan2.5-i2v-preview",
  "api_platform": "DashScope",
  "api_key_env": "DASHSCOPE_API_KEY",
  "parallel_tasks": 5,          // 并发数 (1-10,推荐5)
  "retry_attempts": 3,           // 重试次数
  "retry_delay_seconds": 10,     // 重试间隔
  "timeout_seconds": 120         // 单任务超时时间
}
```

**视频设置:**

```json
"video_settings": {
  "default_resolution": "1280*720",   // 标准清晰度
  "alternative_resolution": "1920*1080", // 高清 (文件更大,成本相同)
  "duration": "6s",                   // 时长 (4s或6s)
  "fps": 16,                          // 帧率 (固定16)
  "format": "mp4",
  "codec": "H.264"
}
```

**质量标准:**

```json
"quality_checks": {
  "technical": {
    "min_resolution": "1280*720",
    "min_duration_seconds": 3.5,
    "max_duration_seconds": 6.5,
    "max_file_size_mb": 15,
    "required_fps": 16
  },
  "regeneration_threshold": {
    "technical_fail_rate": 0.05,  // 技术失败率阈值 (5%)
    "visual_fail_rate": 0.20       // 视觉失败率阈值 (20%)
  }
}
```

---

## 4. Prompt工程

完整的Prompt模板库已包含在 `Z4-建筑动画AIGC助手.md` 中。

**核心原则:**

1. **镜头优先**: 始终以镜头运动描述开头
2. **氛围强化**: 从源图像中提取并强化氛围
3. **细节具体**: 指定材质、灯光、质感细节
4. **动作自然**: 使用自然、电影化的运动动词
5. **长度适中**: 80-150个中文字符

**快速参考:**

| 场景类型 | 推荐镜头 | Prompt起手式 |
|---------|---------|-------------|
| 入口 | 推进 | "镜头缓慢向前推进，穿过..." |
| 等候区 | 横移 | "镜头从左至右平稳横移..." |
| 主用餐区 | 推进/横移 | "镜头穿过主用餐区..." |
| 包间 | 环绕 | "镜头围绕茶几缓慢旋转..." |
| 细节 | 特写推进 | "镜头聚焦...，缓慢推进特写..." |
| 俯瞰 | 升降 | "镜头从平视缓慢上升至俯视角度..." |

---

## 5. 质量控制

### 5.1 自动化技术检查

使用 `validate_video()` 函数 (定义在 Z4 agent中):

```python
from plugins.筹建组.agents.Z4_helpers import validate_video

# 验证单个视频
result = validate_video("output/.../video.mp4")

if result["technical"]:
    print("✅ 技术指标合格")
else:
    print(f"❌ 技术问题: {result['issues']}")
```

### 5.2 人工复核清单

**技术质量 (Technical):**
- [ ] 视频播放流畅，无卡顿
- [ ] 分辨率达标 (≥720P)
- [ ] 时长符合预期 (4-6秒)
- [ ] 无明显压缩伪影
- [ ] 文件大小合理 (<15MB)

**视觉质量 (Visual):**
- [ ] 画面清晰，焦点准确
- [ ] 色彩还原准确，无偏色
- [ ] 亮度和对比度适中
- [ ] 无明显运动模糊
- [ ] 空间比例正常，无变形

**创意质量 (Creative):**
- [ ] 镜头运动自然流畅
- [ ] 突出了关键设计特征
- [ ] 氛围营造符合预期
- [ ] 过渡自然，无生硬感
- [ ] 整体观感专业

### 5.3 问题视频处理流程

```
发现问题视频
    ↓
分类问题类型
    ├─ 技术问题 (分辨率、时长)
    │   └─ 检查API参数,重新提交
    │
    ├─ 视觉问题 (模糊、偏色)
    │   └─ 优化Negative Prompt,重新生成
    │
    └─ 创意问题 (镜头不当、氛围不符)
        └─ 优化中文Prompt,重新生成
            ├─ 调整镜头运动描述
            ├─ 强化氛围关键词
            └─ 增加细节指令
```

**Prompt优化示例:**

```python
# 原始Prompt (镜头过快)
original = "镜头快速向前推进，穿过主用餐区..."

# 优化后 (强调缓慢)
optimized = "镜头缓慢平稳向前推进，节奏舒缓，穿过主用餐区..."

# 原始Prompt (细节模糊)
original = "展现用餐区..."

# 优化后 (强化细节)
optimized = "展现用餐区，特别聚焦木质桌面纹理、座椅细节、灯具造型，材质质感清晰呈现..."

# 原始Prompt (氛围不够温馨)
original = "餐厅空间..."

# 优化后 (强化氛围)
optimized = "温暖柔和的灯光洒满餐厅空间，营造家庭聚餐的温馨氛围，顾客笑语盈盈..."
```

---

## 6. 故障排查

### 6.1 常见问题与解决方案

#### 问题1: API Key未配置

**症状:**
```
❌ Error: DASHSCOPE_API_KEY environment variable not found
```

**解决方案:**
```bash
# 设置环境变量
export DASHSCOPE_API_KEY="sk-your-api-key-here"

# 验证
echo $DASHSCOPE_API_KEY

# 永久设置
echo 'export DASHSCOPE_API_KEY="sk-your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

#### 问题2: 任务生成失败

**症状:**
```
❌ 任务状态: FAILED
```

**可能原因与排查:**

1. **图像格式或分辨率问题**
   ```python
   # 检查图像
   from PIL import Image
   img = Image.open("image.png")
   print(f"尺寸: {img.size}, 格式: {img.format}")

   # 如果分辨率过低 (<512x512),需要重新生成或放大
   if img.size[0] < 512 or img.size[1] < 512:
       print("⚠️ 图像分辨率过低")
   ```

2. **Prompt包含敏感内容**
   - 检查Prompt是否有不当描述
   - 使用标准模板库的Prompt

3. **API账户余额不足**
   ```bash
   # 登录DashScope控制台检查余额
   https://dashscope.console.aliyun.com/
   ```

4. **网络连接问题**
   ```bash
   # 测试API连接
   curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/vision/image-to-video' \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY"
   ```

#### 问题3: 视频质量不佳

**症状:**
- 画面模糊或运动不自然

**解决方案:**

1. **检查输入图像质量**
   - 确保≥1024×1024分辨率
   - 使用PNG格式 (避免JPEG压缩)

2. **优化Prompt**
   - 增加细节描述
   - 强化"缓慢"、"平稳"等关键词
   - 使用更具体的氛围描述

3. **强化Negative Prompt**
   ```python
   negative_prompt = """
   模糊不清、画面抖动、人物变形、光线过曝、色彩失真、
   物体穿模、空间比例失调、材质混乱、低分辨率、噪点过多、
   帧率不稳、运动轨迹不自然、焦点模糊、细节丢失、构图失衡
   """
   ```

4. **重新生成**
   - 第一次尝试不满意时,使用优化后的Prompt重新生成
   - 成本仅¥0.35,可以承受多次尝试

#### 问题4: FFmpeg合并失败

**症状:**
```
❌ FFmpeg合并失败: concat protocol error
```

**解决方案:**

1. **检查FFmpeg安装**
   ```bash
   ffmpeg -version

   # 如果未安装
   # macOS:
   brew install ffmpeg

   # Linux:
   sudo apt-get install ffmpeg
   ```

2. **检查视频文件完整性**
   ```bash
   # 验证每个视频是否可播放
   ffmpeg -i video.mp4 -f null -

   # 检查编码格式是否一致
   ffprobe -v error -show_entries stream=codec_name video.mp4
   ```

3. **使用绝对路径**
   ```python
   # concat文件中使用绝对路径
   abs_path = os.path.abspath(video_path)
   ```

---

## 7. 成本管理

### 7.1 成本结构

**单视频固定成本:**
- Wan i2v生成: **¥0.35/video** (720P或1080P相同)
- API调用: 包含在模型费用中
- 存储: 可忽略不计 (5-10MB/video)

**典型项目成本估算:**

| 视频数量 | 总成本 (CNY) | 参考场景 |
|---------|------------|---------|
| 5个 | ¥1.75 | 单一空间,少量角度 |
| 10个 | ¥3.50 | 多空间,标准覆盖 |
| 15个 | ¥5.25 | 完整流线,多角度 |
| 20个 | ¥7.00 | 大型项目,全面展示 |
| 30个 | ¥10.50 | 特大型项目或多方案对比 |

### 7.2 与其他方案对比

| 方案 | 单视频成本 | 10视频项目 | 制作周期 | 节省率 |
|------|----------|-----------|---------|-------|
| 传统动画 (Lumion) | ¥500-1000 | ¥5000-10000 | 3周 | - |
| Luma Dream Machine | $0.70 (¥5) | $7 (¥50) | 1天 | 93% vs Luma |
| **Wan i2v (Z4)** | **¥0.35** | **¥3.50** | **1小时** | **99.96% vs 传统** |

### 7.3 成本优化策略

**1. 精准Prompt减少重试**
- 首次通过率≥80%: 减少重复生成成本
- 使用标准模板库: 避免Prompt试错

**2. 批量处理提高效率**
- 并发5个任务: 缩短总耗时,提高产能
- 按场景分批: 优先生成关键场景

**3. 质量标准平衡**
- 投资人汇报: 使用1080P + 优秀Prompt
- 社交媒体: 720P即可,成本相同但文件更小

**4. 成本追踪和报告**
```python
# 项目结束后生成成本报告
cost_report = {
    "project_name": "火锅店开业筹备",
    "total_videos": 12,
    "successful_generations": 12,
    "failed_generations": 2,  # 失败后重新生成
    "total_api_calls": 14,
    "cost_per_video": 0.35,
    "total_cost": 14 * 0.35,  # ¥4.90
    "cost_breakdown": {
        "initial_generation": 12 * 0.35,  # ¥4.20
        "regeneration": 2 * 0.35           # ¥0.70
    }
}

import json
with open("output/.../cost-report.json", "w") as f:
    json.dump(cost_report, f, indent=2)
```

---

## 8. 最佳实践

### 8.1 工作流程优化

**1. 分批次执行 (Batching)**

```
不推荐 (串行):
T1 → T2 → T3 → ... → T12  (120分钟)

推荐 (并行分批):
Batch 1: T1-T5 (5个并发, 20分钟)
Batch 2: T6-T10 (5个并发, 20分钟)
Batch 3: T11-T12 (2个并发, 10分钟)
总计: 50分钟 (节省58%)
```

**2. 优先级策略**

```python
# 按重要性排序任务
priority_order = [
    "entrance",      # 优先级1: 第一印象
    "main_dining",   # 优先级2: 核心区域
    "private_rooms", # 优先级3: 高价值场景
    "waiting_area",  # 优先级4: 辅助区域
    "details"        # 优先级5: 细节特写
]

# 先生成高优先级场景,如遇问题可及时调整
```

**3. 增量交付**

```
Day 1 Morning: 完成Batch 1 (入口+主用餐区) → 提交ZZ初审
Day 1 Afternoon: 根据反馈调整 + 完成Batch 2 (包间+细节)
Day 1 Evening: 质量验收 + 合并完整版 → 最终交付
```

### 8.2 Prompt复用与模板化

**建立项目Prompt库:**

```python
# project_prompt_library.py

ENTRANCE_PROMPTS = {
    "moon_gate": "镜头缓慢向前推进，穿过精致的月洞门框架...",
    "street_view": "镜头从街道视角缓慢推进，展现餐厅外立面...",
    "lobby": "镜头进入前厅，暖光迎接顾客..."
}

MAIN_DINING_PROMPTS = {
    "panoramic_push": "镜头缓慢向前推进，穿过主用餐区...",
    "lateral_pan": "镜头从左至右平稳横移，依次展现散台区...",
    "aerial_crane": "镜头从平视缓慢上升至俯视角度..."
}

PRIVATE_ROOM_PROMPTS = {
    "orbit": "镜头围绕包间中心茶几缓慢旋转...",
    "push_in": "镜头缓慢向前推进，进入包间内部..."
}

DETAIL_PROMPTS = {
    "tea_service": "镜头聚焦木质桌面上的精致茶具...",
    "wood_texture": "镜头聚焦实木桌面，缓慢推进特写...",
    "food_presentation": "镜头聚焦精致的火锅食材摆盘..."
}

def get_prompt(scene_type: str, sub_type: str) -> str:
    """从库中获取预设Prompt"""
    prompt_lib = {
        "entrance": ENTRANCE_PROMPTS,
        "main_dining": MAIN_DINING_PROMPTS,
        "private_room": PRIVATE_ROOM_PROMPTS,
        "detail": DETAIL_PROMPTS
    }
    return prompt_lib.get(scene_type, {}).get(sub_type, "")
```

### 8.3 质量一致性保障

**标准化输出规范:**

1. **命名规范**
   ```
   格式: [项目名]-[场景类型]-[镜头类型]-[序号].mp4

   ✅ 正确: 火锅店-主用餐区-推进镜头-04.mp4
   ❌ 错误: video_04.mp4
   ```

2. **技术参数统一**
   ```python
   STANDARD_PARAMS = {
       "resolution": "1280*720",  # 统一使用720P
       "duration": "6s",          # 统一6秒时长
       "fps": 16                  # 固定16fps
   }
   ```

3. **Prompt结构一致**
   ```
   [镜头运动] + [场景描述] + [氛围强化] + [细节补充]

   保持每个视频的Prompt遵循相同结构
   ```

### 8.4 团队协作规范

**与Z2协同:**
- ✅ 完全接受Z2的任何输出,不提要求
- ✅ 如遇图像质量问题,向ZZ报告而非直接联系Z2
- ✅ 在logs/中记录Z2图像信息以便追溯

**与ZZ沟通:**
- ✅ 开始前: 确认输入、预估成本、预计时间
- ✅ 执行中: 每完成20%更新进度
- ✅ 遇问题: 立即报告,提供解决方案选项
- ✅ 完成后: 提交完整交付清单和成本报告

**输出标准化:**
- ✅ 按场景分类存储视频
- ✅ 生成清单文档 (Markdown)
- ✅ 记录所有Prompt (JSON)
- ✅ 追踪成本 (JSON)

### 8.5 持续改进

**收集反馈:**
```python
# feedback-template.json
{
    "project_name": "火锅店开业筹备",
    "feedback_date": "2025-01-28",
    "videos_reviewed": 12,
    "zz_feedback": {
        "满意度": "4.5/5",
        "优点": ["镜头流畅", "氛围营造好", "成本低"],
        "改进点": ["部分细节镜头可以更慢", "色彩可以更暖"]
    },
    "client_feedback": {
        "满意度": "5/5",
        "最喜欢的视频": ["火锅店-主用餐区-全景推进-04.mp4"],
        "建议": ["增加音乐"]
    },
    "action_items": [
        "更新DETAIL_PROMPTS,强调'极缓慢推进'",
        "Negative Prompt中添加'色彩过冷'",
        "下次项目考虑添加BGM (需额外工具)"
    ]
}
```

**迭代Prompt库:**
- 每个项目结束后,将优秀Prompt加入库
- 标记高复用率的Prompt模板
- 淘汰效果不佳的旧模板

**性能优化:**
- 记录每次项目的实际耗时
- 优化并发数和批次大小
- 调整Prompt生成策略

---

## 9. 完整示例脚本

### 9.1 端到端自动化脚本

```python
#!/usr/bin/env python3
"""
Z4-建筑动画AIGC助手 - 完整自动化脚本

Usage:
    python z4_full_workflow.py --project "火锅店开业筹备" --style "modern_chinese"
"""

import os
import sys
import json
import time
import argparse
import glob
from pathlib import Path
from typing import List, Dict
import concurrent.futures

# 导入Wan技能包
sys.path.append("plugins/筹建组/skills/Wan/scripts")
from wan_base import WanAPIClient


def main(project_name: str, design_style: str):
    """主执行流程"""

    print(f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║  Z4-建筑动画AIGC助手 - 自动化执行系统                        ║
    ║  项目: {project_name}
    ║  风格: {design_style}
    ╚══════════════════════════════════════════════════════════════╝
    """)

    # ===== Phase 1: 接收与分析 =====
    print("\n[Phase 1] 📥 接收Z2输出...")
    z2_path = f"output/{project_name}/Z2-空间概念设计师/"
    images = glob.glob(f"{z2_path}/*.png")

    if not images:
        print(f"❌ 未找到Z2输出图像: {z2_path}")
        return

    print(f"✅ 找到{len(images)}张PNG图像")

    # ===== Phase 2: Prompt工程 =====
    print("\n[Phase 2] ✍️  生成Prompt...")
    tasks = []

    for i, image_path in enumerate(images, 1):
        filename = os.path.basename(image_path)

        # 场景分析
        scene_analysis = identify_scene_type(filename)

        # 生成Prompt
        prompt = generate_prompt(scene_analysis, design_style)
        negative_prompt = get_negative_prompt(scene_analysis["scene_type"])

        # 输出路径
        output_filename = filename.replace(".png", ".mp4")
        output_path = f"output/{project_name}/Z4-建筑动画AIGC助手/{output_filename}"

        task = {
            "task_id": f"T{i:03d}",
            "image_path": image_path,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "params": {
                "model": "wan2.5-i2v-preview",
                "size": "1280*720",
                "duration": "6s",
                "fps": 16
            },
            "output_path": output_path
        }

        tasks.append(task)
        print(f"  [{i}/{len(images)}] {filename}")
        print(f"       场景: {scene_analysis['scene_type']}, 镜头: {scene_analysis['suggested_camera']}")

    # ===== Phase 3: 批量生成 =====
    print(f"\n[Phase 3] 🚀 批量生成 ({len(tasks)}个任务)...")
    print(f"💰 预计成本: ¥{len(tasks) * 0.35:.2f}")

    client = WanAPIClient()
    task_ids = []

    # 并行提交
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for task in tasks:
            future = executor.submit(
                client.submit_i2v_task,
                image_path=task["image_path"],
                prompt=task["prompt"],
                negative_prompt=task["negative_prompt"],
                params=task["params"]
            )
            futures.append((future, task))

        for future, task in futures:
            task_id = future.result()
            task["api_task_id"] = task_id
            task_ids.append(task_id)
            print(f"✅ 提交: {task['task_id']} → {task_id}")

    # 监控进度
    print(f"\n⏳ 监控任务进度...")
    task_status = {tid: "PENDING" for tid in task_ids}

    while True:
        pending = [tid for tid, status in task_status.items()
                   if status not in ["SUCCEEDED", "FAILED"]]

        if not pending:
            break

        # 并行查询状态
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(client.query_task_status, tid): tid
                       for tid in pending}

            for future in concurrent.futures.as_completed(futures):
                tid = futures[future]
                status = future.result()
                task_status[tid] = status

        # 打印进度
        succeeded = sum(1 for s in task_status.values() if s == "SUCCEEDED")
        failed = sum(1 for s in task_status.values() if s == "FAILED")
        processing = len(pending)

        print(f"  ✅ {succeeded}/{len(task_ids)} | ❌ {failed} | ⏳ {processing}", end="\r")

        if pending:
            time.sleep(10)

    print(f"\n✅ 生成完成: {succeeded}/{len(task_ids)}")

    # 下载视频
    print(f"\n[Phase 4] 📥 下载视频...")
    for task in tasks:
        if task_status.get(task["api_task_id"]) == "SUCCEEDED":
            os.makedirs(os.path.dirname(task["output_path"]), exist_ok=True)
            client.download_video(task["api_task_id"], task["output_path"])
            print(f"✅ 已下载: {os.path.basename(task['output_path'])}")

    # ===== Phase 5: 交付打包 =====
    print(f"\n[Phase 5] 📦 交付打包...")

    # 生成清单
    generate_video_list(tasks, f"output/{project_name}/Z4-建筑动画AIGC助手/video-list.md")

    # 保存Prompt记录
    with open(f"output/{project_name}/Z4-建筑动画AIGC助手/prompts-used.json", "w", encoding="utf-8") as f:
        json.dump([{"task_id": t["task_id"], "image": os.path.basename(t["image_path"]),
                    "prompt": t["prompt"], "negative_prompt": t["negative_prompt"]}
                   for t in tasks], f, ensure_ascii=False, indent=2)

    # 成本报告
    cost_report = {
        "project_name": project_name,
        "total_videos": len(tasks),
        "successful_generations": succeeded,
        "failed_generations": failed,
        "cost_per_video": 0.35,
        "total_cost": succeeded * 0.35
    }

    with open(f"output/{project_name}/Z4-建筑动画AIGC助手/cost-report.json", "w") as f:
        json.dump(cost_report, f, indent=2)

    print(f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║  ✅ Z4任务完成!                                              ║
    ║                                                              ║
    ║  视频数量: {succeeded}/{len(tasks)}                                      ║
    ║  总成本: ¥{cost_report['total_cost']:.2f}                                         ║
    ║  输出位置: output/{project_name}/Z4-建筑动画AIGC助手/          ║
    ╚══════════════════════════════════════════════════════════════╝
    """)


# ... (其他辅助函数: identify_scene_type, generate_prompt, etc.)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Z4-建筑动画AIGC助手自动化脚本")
    parser.add_argument("--project", required=True, help="项目名称")
    parser.add_argument("--style", default="modern_chinese", help="设计风格")

    args = parser.parse_args()
    main(args.project, args.style)
```

**运行示例:**

```bash
# 完整自动化执行
python z4_full_workflow.py --project "火锅店开业筹备" --style "modern_chinese"

# 预期输出:
# ╔══════════════════════════════════════════════════════════════╗
# ║  Z4-建筑动画AIGC助手 - 自动化执行系统                        ║
# ╚══════════════════════════════════════════════════════════════╝
#
# [Phase 1] 📥 接收Z2输出...
# ✅ 找到12张PNG图像
#
# [Phase 2] ✍️  生成Prompt...
#   [1/12] 餐厅-主用餐区-全景.png
#       场景: main_dining, 镜头: push
# ...
#
# [Phase 3] 🚀 批量生成 (12个任务)...
# 💰 预计成本: ¥4.20
# ✅ 提交: T001 → task-xxx-xxx-xxx
# ...
#
# ⏳ 监控任务进度...
#   ✅ 12/12 | ❌ 0 | ⏳ 0
# ✅ 生成完成: 12/12
#
# [Phase 4] 📥 下载视频...
# ✅ 已下载: 餐厅-主用餐区-全景.mp4
# ...
#
# [Phase 5] 📦 交付打包...
#
# ╔══════════════════════════════════════════════════════════════╗
# ║  ✅ Z4任务完成!                                              ║
# ║  视频数量: 12/12                                             ║
# ║  总成本: ¥4.20                                               ║
# ╚══════════════════════════════════════════════════════════════╝
```

---

## 10. 总结

**Z4-建筑动画AIGC助手核心优势:**

✅ **速度**: 1小时 vs 传统3周 (98%时间节省)
✅ **成本**: ¥3.50/10视频 vs ¥5000-10000 (99.96%成本节省)
✅ **易用**: 无需3D软件操作,Prompt工程即可
✅ **灵活**: 接受Z2任何输出,无prescriptive要求
✅ **可扩展**: 并行处理,轻松应对大规模项目

**技术栈:**
- 阿里云通义万相 wan2.5-i2v-preview
- DashScope MaaS平台
- Python + Wan技能包
- FFmpeg (视频合并)

**典型应用场景:**
- 投资人汇报视频
- 社交媒体营销素材
- 客户预览walkthrough
- 设计方案展示

**下一步行动:**
1. 测试Wan API连接 (quick_test_z4.py)
2. 运行完整自动化脚本 (z4_full_workflow.py)
3. 收集反馈,优化Prompt库
4. 扩展到更多项目类型

---

**文档版本**: v1.0.0
**更新日期**: 2025-10-28
**维护者**: Z4-建筑动画AIGC助手
**技术支持**: plugins/筹建组/skills/Wan/
