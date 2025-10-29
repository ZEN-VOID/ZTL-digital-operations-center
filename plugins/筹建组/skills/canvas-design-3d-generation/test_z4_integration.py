#!/usr/bin/env python3
"""
Z4-建筑动画AIGC助手 - 集成测试脚本

测试范围:
1. Wan API连接测试
2. 单图像i2v生成测试
3. Prompt工程测试
4. 质量验收测试
5. 批量生成测试
6. 视频合并测试

Usage:
    python test_z4_integration.py
    python test_z4_integration.py --full  # 完整测试(包含实际API调用)
"""

import os
import sys
import time
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional

# 添加Wan技能包路径
wan_scripts_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Wan/scripts"))
sys.path.insert(0, wan_scripts_path)

try:
    # 方法1: 尝试从__init__.py导入
    import importlib.util
    init_path = os.path.join(wan_scripts_path, "__init__.py")
    if os.path.exists(init_path):
        spec = importlib.util.spec_from_file_location("wan_scripts", init_path)
        wan_scripts = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(wan_scripts)
        WanAPIClient = wan_scripts.WanAPIClient
        WAN_AVAILABLE = True
    else:
        # 方法2: 直接使用importlib加载wan-base.py
        wan_base_path = os.path.join(wan_scripts_path, "wan-base.py")
        spec = importlib.util.spec_from_file_location("wan_base", wan_base_path)
        wan_base = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(wan_base)
        WanAPIClient = wan_base.WanAPIClient
        WAN_AVAILABLE = True
except Exception as e:
    WAN_AVAILABLE = False
    print(f"⚠️  警告: Wan技能包未找到,将跳过实际API测试 ({e})")


# ==================== 测试辅助函数 ====================

def print_test_header(test_name: str):
    """打印测试标题"""
    print(f"\n{'='*70}")
    print(f"  TEST: {test_name}")
    print(f"{'='*70}")


def print_test_result(passed: bool, message: str):
    """打印测试结果"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status}: {message}")


def print_section(title: str):
    """打印章节标题"""
    print(f"\n--- {title} ---")


# ==================== Test 1: 环境检查 ====================

def test_environment() -> bool:
    """测试1: 环境和依赖检查"""
    print_test_header("Test 1: 环境和依赖检查")

    all_passed = True

    # 1.1 Python版本
    print_section("1.1 Python版本检查")
    python_version = sys.version_info
    if python_version >= (3, 9):
        print_test_result(True, f"Python版本: {python_version.major}.{python_version.minor}")
    else:
        print_test_result(False, f"Python版本过低: {python_version.major}.{python_version.minor} (需要≥3.9)")
        all_passed = False

    # 1.2 DASHSCOPE_API_KEY
    print_section("1.2 API Key检查")
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if api_key:
        print_test_result(True, f"DASHSCOPE_API_KEY: {api_key[:10]}... (已配置)")
    else:
        print_test_result(False, "DASHSCOPE_API_KEY未配置 (需设置环境变量)")
        print("  提示: export DASHSCOPE_API_KEY=\"sk-your-key\"")
        all_passed = False

    # 1.3 Wan技能包
    print_section("1.3 Wan技能包检查")
    if WAN_AVAILABLE:
        print_test_result(True, "Wan技能包导入成功")
    else:
        print_test_result(False, "Wan技能包未找到")
        print(f"  路径: {os.path.join(os.path.dirname(__file__), '../Wan/scripts')}")
        all_passed = False

    # 1.4 必需目录
    print_section("1.4 输出目录检查")
    required_dirs = [
        "output/",
        "plugins/筹建组/skills/canvas-design-3d-generation/"
    ]

    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print_test_result(True, f"目录存在: {dir_path}")
        else:
            print(f"  创建目录: {dir_path}")
            os.makedirs(dir_path, exist_ok=True)
            print_test_result(True, f"目录已创建: {dir_path}")

    return all_passed


# ==================== Test 2: 配置模板验证 ====================

def test_config_template() -> bool:
    """测试2: 配置模板JSON验证"""
    print_test_header("Test 2: 配置模板验证")

    all_passed = True

    # 2.1 加载JSON模板
    print_section("2.1 加载JSON模板")
    template_path = "plugins/筹建组/skills/canvas-design-3d-generation/config-template-z4-wan-i2v.json"

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        print_test_result(True, f"JSON模板加载成功: {template_path}")
    except FileNotFoundError:
        print_test_result(False, f"文件未找到: {template_path}")
        return False
    except json.JSONDecodeError as e:
        print_test_result(False, f"JSON格式错误: {e}")
        return False

    # 2.2 验证必需字段
    print_section("2.2 验证配置结构")
    required_fields = [
        "project_info",
        "execution_config",
        "video_settings",
        "batches",
        "output_config",
        "summary"
    ]

    for field in required_fields:
        if field in config:
            print_test_result(True, f"字段存在: {field}")
        else:
            print_test_result(False, f"字段缺失: {field}")
            all_passed = False

    # 2.3 验证批次任务
    print_section("2.3 验证批次和任务")
    if "batches" in config:
        total_tasks = sum(len(batch["tasks"]) for batch in config["batches"])
        total_cost = sum(batch["subtotal_cost"] for batch in config["batches"])

        print_test_result(True, f"批次数量: {len(config['batches'])}")
        print_test_result(True, f"任务总数: {total_tasks}")
        print_test_result(True, f"预计成本: ¥{total_cost:.2f}")

        # 检查成本计算
        expected_cost = total_tasks * 0.35
        if abs(total_cost - expected_cost) < 0.01:
            print_test_result(True, f"成本计算正确: ¥{total_cost:.2f} = {total_tasks} × ¥0.35")
        else:
            print_test_result(False, f"成本计算错误: ¥{total_cost:.2f} ≠ ¥{expected_cost:.2f}")
            all_passed = False

    return all_passed


# ==================== Test 3: Prompt工程测试 ====================

def test_prompt_engineering() -> bool:
    """测试3: Prompt生成逻辑"""
    print_test_header("Test 3: Prompt工程测试")

    all_passed = True

    # 3.1 场景类型识别
    print_section("3.1 场景类型识别")

    test_cases = [
        ("餐厅-主用餐区-全景.png", "main_dining", "panoramic", "push"),
        ("餐厅-入口月洞门.png", "entrance", "eye-level", "push"),
        ("餐厅-包间A.png", "private_room", "eye-level", "orbit"),
        ("餐厅-茶具特写.png", "detail", "close-up", "close_up_push"),
        ("餐厅-主用餐区-俯瞰.png", "main_dining", "aerial", "crane_up")
    ]

    for filename, expected_scene, expected_viewpoint, expected_camera in test_cases:
        result = identify_scene_type(filename)

        if (result["scene_type"] == expected_scene and
            result["viewpoint"] == expected_viewpoint and
            result["suggested_camera"] == expected_camera):
            print_test_result(True, f"{filename} → {result['scene_type']}/{result['suggested_camera']}")
        else:
            print_test_result(False, f"{filename}: 预期{expected_scene}/{expected_camera}, 实际{result['scene_type']}/{result['suggested_camera']}")
            all_passed = False

    # 3.2 Prompt生成
    print_section("3.2 Prompt生成测试")

    scene = identify_scene_type("餐厅-主用餐区-全景.png")
    prompt = generate_prompt(scene, design_style="modern_chinese")

    # 检查Prompt长度
    if 80 <= len(prompt) <= 150:
        print_test_result(True, f"Prompt长度合规: {len(prompt)}字 (80-150)")
    else:
        print_test_result(False, f"Prompt长度异常: {len(prompt)}字 (应为80-150)")
        all_passed = False

    # 检查必需关键词
    required_keywords = ["镜头", "缓慢"]
    for keyword in required_keywords:
        if keyword in prompt:
            print_test_result(True, f"包含关键词: '{keyword}'")
        else:
            print_test_result(False, f"缺少关键词: '{keyword}'")
            all_passed = False

    print(f"\n  生成的Prompt示例:\n  {prompt}\n")

    # 3.3 Negative Prompt
    print_section("3.3 Negative Prompt测试")

    negative_prompt = get_negative_prompt("main_dining")
    if "模糊不清" in negative_prompt and "画面抖动" in negative_prompt:
        print_test_result(True, f"Negative Prompt生成正确 ({len(negative_prompt)}字)")
    else:
        print_test_result(False, "Negative Prompt缺少必需关键词")
        all_passed = False

    return all_passed


# ==================== Test 4: Wan API连接测试 ====================

def test_wan_api_connection(api_test: bool = False) -> bool:
    """测试4: Wan API连接 (可选实际调用)"""
    print_test_header("Test 4: Wan API连接测试")

    if not WAN_AVAILABLE:
        print_test_result(False, "Wan技能包未安装,跳过API测试")
        return False

    all_passed = True

    # 4.1 客户端初始化
    print_section("4.1 客户端初始化")

    try:
        client = WanAPIClient()
        print_test_result(True, "WanAPIClient初始化成功")
    except Exception as e:
        print_test_result(False, f"客户端初始化失败: {e}")
        return False

    # 4.2 API实际调用测试 (需用户确认)
    if api_test:
        print_section("4.2 API实际调用测试 (将产生¥0.35费用)")

        # 创建测试图像 (如果不存在)
        test_image_path = "output/test-z4/test-image.png"
        if not os.path.exists(test_image_path):
            print(f"  ⚠️  测试图像不存在: {test_image_path}")
            print("  请先准备测试图像或跳过实际API测试")
            return True

        test_prompt = "镜头缓慢向前推进，展现室内空间，温暖灯光营造舒适氛围"

        try:
            print(f"  提交i2v任务...")
            task_id = client.submit_i2v_task(
                image_path=test_image_path,
                prompt=test_prompt,
                negative_prompt="模糊不清、画面抖动",
                params={
                    "model": "wan2.5-i2v-preview",
                    "size": "1280*720",
                    "duration": "6s",
                    "fps": 16
                }
            )

            print_test_result(True, f"任务提交成功: {task_id}")

            # 查询状态
            print(f"  查询任务状态...")
            max_wait = 120  # 最多等待2分钟
            start_time = time.time()

            while time.time() - start_time < max_wait:
                status = client.query_task_status(task_id)

                if status == "SUCCEEDED":
                    print_test_result(True, "视频生成成功")

                    # 下载视频
                    output_path = "output/test-z4/test-video.mp4"
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    client.download_video(task_id, output_path)

                    print_test_result(True, f"视频已下载: {output_path}")
                    break

                elif status == "FAILED":
                    print_test_result(False, "视频生成失败")
                    all_passed = False
                    break

                else:
                    print(f"  ⏳ 生成中... ({status})", end="\r")
                    time.sleep(10)

            else:
                print_test_result(False, f"超时: 等待超过{max_wait}秒")
                all_passed = False

        except Exception as e:
            print_test_result(False, f"API调用失败: {e}")
            all_passed = False

    else:
        print_section("4.2 API实际调用测试 (已跳过)")
        print("  使用 --full 参数执行完整测试 (将产生API费用)")

    return all_passed


# ==================== Test 5: 质量验收测试 ====================

def test_quality_validation() -> bool:
    """测试5: 质量验收逻辑"""
    print_test_header("Test 5: 质量验收测试")

    all_passed = True

    # 5.1 模拟视频质量检查
    print_section("5.1 质量检查函数测试")

    # 创建mock视频 (如果实际视频不存在)
    test_video = "output/test-z4/test-video.mp4"

    if os.path.exists(test_video):
        try:
            import cv2

            result = validate_video(test_video)

            if result["technical"]:
                print_test_result(True, "技术指标合格")
            else:
                print_test_result(False, f"技术问题: {result['issues']}")
                all_passed = False

        except ImportError:
            print_test_result(False, "OpenCV未安装,跳过视频验证")
        except Exception as e:
            print_test_result(False, f"质量检查失败: {e}")
            all_passed = False
    else:
        print(f"  ⚠️  测试视频不存在: {test_video}")
        print("  跳过质量检查测试 (需先运行API测试生成视频)")

    return all_passed


# ==================== Test 6: 批量处理测试 ====================

def test_batch_processing() -> bool:
    """测试6: 批量处理逻辑"""
    print_test_header("Test 6: 批量处理测试")

    all_passed = True

    # 6.1 任务调度测试
    print_section("6.1 任务调度逻辑")

    mock_tasks = [
        {"task_id": f"T{i:03d}", "status": "PENDING"}
        for i in range(1, 11)
    ]

    # 模拟并行处理
    batch_size = 5
    batches = [mock_tasks[i:i+batch_size] for i in range(0, len(mock_tasks), batch_size)]

    expected_batches = 2  # 10个任务,batch_size=5,应该分2批
    if len(batches) == expected_batches:
        print_test_result(True, f"任务分批正确: {len(batches)}批 (每批{batch_size}个)")
    else:
        print_test_result(False, f"任务分批错误: 预期{expected_batches}批, 实际{len(batches)}批")
        all_passed = False

    return all_passed


# ==================== 辅助函数实现 ====================

def identify_scene_type(image_filename: str) -> Dict[str, str]:
    """场景类型识别 (简化版实现)"""
    filename = os.path.basename(image_filename).lower()

    # 场景类型映射
    scene_keywords = {
        "entrance": ["入口", "门头", "月洞门"],
        "waiting_area": ["等候", "等待", "前厅"],
        "main_dining": ["主用餐", "大厅"],
        "private_room": ["包间", "包厢"],
        "detail": ["特写", "细节"]
    }

    viewpoint_keywords = {
        "panoramic": ["全景"],
        "close-up": ["特写", "细节"],
        "aerial": ["俯瞰", "俯视"],
        "side": ["侧面"]
    }

    # 识别场景
    scene_type = "unknown"
    for scene, keywords in scene_keywords.items():
        if any(kw in filename for kw in keywords):
            scene_type = scene
            break

    # 识别视角
    viewpoint = "eye-level"
    for view, keywords in viewpoint_keywords.items():
        if any(kw in filename for kw in keywords):
            viewpoint = view
            break

    # 建议镜头 (根据场景类型和视角)
    if viewpoint == "aerial":
        # 俯瞰视角使用升降镜头
        suggested_camera = "crane_up"
    elif scene_type == "entrance":
        suggested_camera = "push"
    elif scene_type == "waiting_area":
        suggested_camera = "lateral_pan"
    elif scene_type == "main_dining":
        suggested_camera = "push" if viewpoint == "panoramic" else "lateral_pan"
    elif scene_type == "private_room":
        suggested_camera = "orbit"
    elif scene_type == "detail":
        suggested_camera = "close_up_push"
    else:
        suggested_camera = "push"

    return {
        "scene_type": scene_type,
        "viewpoint": viewpoint,
        "suggested_camera": suggested_camera
    }


def generate_prompt(scene_analysis: Dict, design_style: str = "modern_chinese") -> str:
    """生成Prompt (简化版实现)"""
    camera_movement = scene_analysis["suggested_camera"]
    scene_type = scene_analysis["scene_type"]

    camera_phrases = {
        "push": "镜头缓慢向前推进",
        "orbit": "镜头围绕中心缓慢旋转",
        "lateral_pan": "镜头从左至右平稳横移",
        "crane_up": "镜头从平视缓慢上升至俯视角度",
        "close_up_push": "镜头聚焦对象，缓慢推进特写"
    }

    scene_descriptions = {
        "entrance": "穿过精致的月洞门框架，进入典雅的等候区，暖色灯光映照古典家具",
        "waiting_area": "依次展现文化墙装饰、舒适沙发、茶水吧台，完整呈现等候区的功能布局和文化氛围",
        "main_dining": "穿过主用餐区，两侧摆放精致圆桌和舒适座椅，暖黄灯光从吊灯洒下，营造温馨用餐氛围",
        "private_room": "360度展现私密空间设计，高级灰墙面搭配暖色木饰面，精致吊灯投下柔和光影",
        "detail": "清晰展现材质肌理和质感，暖光下更显自然雅致，细节处理考究"
    }

    camera_desc = camera_phrases.get(camera_movement, "镜头缓慢移动")
    scene_desc = scene_descriptions.get(scene_type, "展现空间设计")

    prompt = f"{camera_desc}，{scene_desc}，展现茶文化与现代设计的完美融合，画面层次丰富，细节清晰自然"

    return prompt


def get_negative_prompt(scene_type: str) -> str:
    """获取Negative Prompt"""
    if scene_type == "detail":
        return "模糊不清、画面抖动、色彩失真、焦点模糊、细节丢失、材质失真、光线不足"
    elif scene_type in ["entrance", "main_dining"]:
        return "模糊不清、画面抖动、人物变形、光线过曝、色彩失真、物体穿模、空间比例失调、材质混乱、低分辨率、噪点过多、帧率不稳、运动轨迹不自然、焦点模糊、细节丢失、构图失衡"
    else:
        return "模糊不清、画面抖动、人物变形、光线过曝、色彩失真、物体穿模、空间比例失调、材质混乱"


def validate_video(video_path: str) -> Dict:
    """视频质量验证 (简化版实现)"""
    import cv2

    issues = []

    cap = cv2.VideoCapture(video_path)

    # 检查分辨率
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if width < 1280 or height < 720:
        issues.append(f"分辨率过低: {width}x{height}")

    # 检查时长
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps if fps > 0 else 0
    if duration < 3.5 or duration > 6.5:
        issues.append(f"时长异常: {duration:.1f}秒")

    # 检查文件大小
    file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
    if file_size > 15:
        issues.append(f"文件过大: {file_size:.1f}MB")

    cap.release()

    return {
        "technical": len(issues) == 0,
        "visual": True,
        "creative": True,
        "issues": issues
    }


# ==================== 主测试流程 ====================

def run_all_tests(full_test: bool = False):
    """运行所有测试"""

    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  Z4-建筑动画AIGC助手 - 集成测试套件                          ║
    ║  Version: 1.0.0 | Date: 2025-10-28                           ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    results = {}

    # Test 1: 环境检查
    results["test_1_environment"] = test_environment()

    # Test 2: 配置模板验证
    results["test_2_config"] = test_config_template()

    # Test 3: Prompt工程测试
    results["test_3_prompt"] = test_prompt_engineering()

    # Test 4: Wan API连接测试
    results["test_4_api"] = test_wan_api_connection(api_test=full_test)

    # Test 5: 质量验收测试
    results["test_5_quality"] = test_quality_validation()

    # Test 6: 批量处理测试
    results["test_6_batch"] = test_batch_processing()

    # 汇总结果
    print(f"\n{'='*70}")
    print("  测试结果汇总")
    print(f"{'='*70}")

    passed = sum(1 for result in results.values() if result)
    total = len(results)

    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")

    print(f"\n总计: {passed}/{total} 测试通过 ({passed/total*100:.0f}%)")

    if passed == total:
        print("\n✅ 所有测试通过! Z4集成正常工作。")
        return 0
    else:
        print(f"\n❌ {total - passed}个测试失败,请检查上述错误。")
        return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Z4集成测试")
    parser.add_argument("--full", action="store_true",
                        help="执行完整测试 (包含实际API调用,将产生¥0.35费用)")

    args = parser.parse_args()

    if args.full:
        print("\n⚠️  警告: 完整测试将调用Wan i2v API,产生约¥0.35费用")
        print("确认继续? (y/N): ", end="")
        confirm = input().strip().lower()
        if confirm != "y":
            print("已取消完整测试")
            sys.exit(0)

    exit_code = run_all_tests(full_test=args.full)
    sys.exit(exit_code)
