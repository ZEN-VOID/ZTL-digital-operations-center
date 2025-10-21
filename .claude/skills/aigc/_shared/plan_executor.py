#!/usr/bin/env python3
"""
通用执行计划执行器 - 支持E1-E9所有智能体
基于JSON执行计划动态调用NanoBananaAPI

使用方法:
  python execute_plan.py --plan api/plans/e8-design-iteration/task.json
  python execute_plan.py --plan api/plans/e1-text-to-image/poster.json
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# 导入共享核心库
from banana_api_core import NanoBananaAPI


# E1-E9智能体方法映射表
AGENT_METHOD_MAP = {
    "E1": "generate_text_to_image",
    "E2": "generate_image_to_image",
    "E3": "generate_image_recognition",
    "E4": "generate_smart_repair",
    "E5": "generate_structure_control",
    "E6": "generate_image_fusion",
    "E7": "generate_character_consistency",
    "E8": "generate_design_iteration",
    "E9": "generate_super_resolution"
}


def load_execution_plan(plan_path: str) -> dict:
    """加载JSON执行计划"""
    with open(plan_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_api_params(plan: dict) -> dict:
    """从执行计划中提取API调用参数"""
    agent_id = plan.get("agent_id", "").upper()

    # E1: 文生图
    if agent_id == "E1":
        return {
            "prompt": plan["input_data"]["text_prompt"],
            "design_type": plan["input_data"].get("design_type"),
            "design_requirements": plan["input_data"].get("design_requirements", [])
        }

    # E2: 图生图
    elif agent_id == "E2":
        # 构建prompt
        prompt = plan["input_data"].get("text_prompt", "")
        if not prompt and "operation_params" in plan["input_data"]:
            # 从operation_params构建prompt
            params = plan["input_data"]["operation_params"]
            prompt = params.get("additional_prompt", "优化这张图片")
        elif not prompt and "edit_config" in plan["input_data"]:
            # 从edit_config构建prompt
            edit_config = plan["input_data"]["edit_config"]
            prompt_parts = []
            for area in edit_config.get("edit_areas", []):
                prompt_parts.append(f"{area.get('target')}: {area.get('modification')}")
            prompt = "; ".join(prompt_parts) if prompt_parts else "优化这张图片"

        return {
            "prompt": prompt,
            "image_urls": [plan["input_data"]["image_url"]],  # 转为列表
            "processing_type": plan["input_data"].get("operation_type")
        }

    # E3: 图片识别
    elif agent_id == "E3":
        return {
            "image_url": plan["input_data"]["image_url"],
            "analysis_type": plan["input_data"]["analysis_type"],
            "analysis_dimensions": plan["input_data"].get("analysis_dimensions", [])
        }

    # E4: 智能修复
    elif agent_id == "E4":
        repair_config = plan["input_data"].get("repair_config", {})
        # 从repair_config提取repair_prompt
        repair_prompt = repair_config.get("description", "")
        if not repair_prompt:
            repair_prompt = f"{repair_config.get('repair_method', '')} {repair_config.get('target_area', '')}"

        return {
            "image_url": plan["input_data"]["image_url"],
            "repair_prompt": repair_prompt,
            "repair_type": plan["input_data"]["repair_type"]
        }

    # E5: 结构控制
    elif agent_id == "E5":
        return {
            "reference_image": plan["input_data"]["reference_image"],
            "control_type": plan["input_data"]["control_type"],
            "target_prompt": plan["input_data"]["generation_prompt"],
            "control_strength": plan["input_data"].get("control_strength", 0.8)
        }

    # E6: 多图融合
    elif agent_id == "E6":
        fusion_config = plan["input_data"].get("fusion_config", {})
        return {
            "source_images": plan["input_data"]["source_images"],
            "fusion_prompt": fusion_config.get("fusion_prompt", ""),
            "fusion_type": plan["input_data"]["fusion_type"]
        }

    # E7: 角色一致性
    elif agent_id == "E7":
        return {
            "character_reference": plan["input_data"]["character_reference"],
            "scene_description": plan["input_data"]["scene_description"],
            "consistency_level": plan["input_data"].get("consistency_level", "high")
        }

    # E8: 设计迭代
    elif agent_id == "E8":
        return {
            "current_version": plan["input_data"]["current_version"],
            "feedback": plan["input_data"]["feedback"],
            "iteration_type": plan["input_data"].get("iteration_type", "feedback_response"),
            "iteration_goals": plan["input_data"].get("iteration_goals", [])
        }

    # E9: 超分增强
    elif agent_id == "E9":
        return {
            "image_url": plan["input_data"]["image_url"],
            "target_resolution": plan["input_data"].get("target_resolution"),
            "enhancement_level": plan["input_data"].get("enhancement_level", "medium")
        }

    else:
        raise ValueError(f"不支持的智能体ID: {agent_id}")


def execute_plan(plan_path: str):
    """执行JSON执行计划"""

    # 1. 加载执行计划
    print("=" * 80)
    print("📋 通用执行计划执行器")
    print("=" * 80)
    print(f"\n📄 执行计划: {plan_path}")

    plan = load_execution_plan(plan_path)
    agent_id = plan.get("agent_id", "").upper()
    task_description = plan.get("task_description", "未提供描述")

    print(f"🤖 智能体: {agent_id}")
    print(f"📝 任务描述: {task_description}")
    print()

    # 2. 验证智能体ID
    if agent_id not in AGENT_METHOD_MAP:
        print(f"❌ 错误: 不支持的智能体ID '{agent_id}'")
        print(f"支持的智能体: {', '.join(AGENT_METHOD_MAP.keys())}")
        return

    # 3. 初始化API
    print(f"🚀 初始化 {agent_id} 智能体...")
    api = NanoBananaAPI()
    method_name = AGENT_METHOD_MAP[agent_id]
    method = getattr(api, method_name)

    # 4. 提取参数并执行
    print(f"⚙️  提取API参数...")
    api_params = extract_api_params(plan)

    print(f"🎯 开始执行 {agent_id}.{method_name}()...")
    print()

    start_time = datetime.now()
    result = method(**api_params)
    end_time = datetime.now()

    # 5. 输出结果
    print("\n" + "=" * 80)
    print(f"📊 {agent_id} 执行报告")
    print("=" * 80)

    if result.get("success"):
        print(f"✅ 状态: 成功")
        print(f"🆔 任务ID: {result.get('task_id')}")
        print(f"⏱️  处理时间: {(end_time - start_time).total_seconds():.2f}秒")

        if "image_paths" in result:
            print(f"📁 生成图片数量: {len(result.get('image_paths', []))}")
            print("\n生成的图片:")
            for i, path in enumerate(result.get('image_paths', []), 1):
                print(f"  {i}. {path}")

        if "analysis_content" in result:
            print(f"\n📊 分析结果:")
            print(result.get("analysis_content", "")[:500] + "..." if len(result.get("analysis_content", "")) > 500 else result.get("analysis_content", ""))

        print(f"\n✅ {agent_id} 任务执行完成!")
    else:
        print(f"❌ 状态: 失败")
        print(f"错误信息: {result.get('error', '未知错误')}")

    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description='执行JSON执行计划')
    parser.add_argument('--plan', required=True, help='执行计划JSON文件路径')

    args = parser.parse_args()

    # 验证文件存在
    plan_path = Path(args.plan)
    if not plan_path.exists():
        print(f"❌ 错误: 执行计划文件不存在 - {args.plan}")
        sys.exit(1)

    # 执行计划
    execute_plan(args.plan)


if __name__ == "__main__":
    main()
