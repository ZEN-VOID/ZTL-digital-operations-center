#!/usr/bin/env python3
"""
并发可行性分析示例
==================

演示如何使用 analyze_concurrency_feasibility() 函数
分析任务的并发潜力并获取优化建议
"""

import sys
from pathlib import Path

# 添加脚本路径到sys.path
script_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(script_dir))

from core import analyze_concurrency_feasibility

# ============================================
# 示例1: 高度独立的任务 (并行化比率高)
# ============================================
print("=" * 60)
print("示例1: 高度独立的图片生成任务")
print("=" * 60)

independent_tasks = [
    {"id": "task1", "type": "text-to-image", "params": {"prompt": "海报1"}},
    {"id": "task2", "type": "text-to-image", "params": {"prompt": "海报2"}},
    {"id": "task3", "type": "text-to-image", "params": {"prompt": "海报3"}},
    {"id": "task4", "type": "text-to-image", "params": {"prompt": "海报4"}},
    {"id": "task5", "type": "text-to-image", "params": {"prompt": "海报5"}},
]

analysis1 = analyze_concurrency_feasibility(independent_tasks)

print(f"\n📊 分析结果:")
print(f"  总任务数: {analysis1.total_tasks}")
print(f"  独立任务: {analysis1.independent_tasks}")
print(f"  依赖任务: {analysis1.dependent_tasks}")
print(f"  推荐并发度: {analysis1.recommended_workers}")
print(f"  并行化比率: {analysis1.parallelization_ratio:.1%}")
print(f"  预估耗时: {analysis1.estimated_duration:.1f}秒")
print(f"  预估内存: {analysis1.estimated_memory_gb:.1f}GB")

print(f"\n💡 优化建议:")
for rec in analysis1.recommendations:
    print(f"  {rec}")

print(f"\n🔄 执行层次:")
for layer in analysis1.execution_layers:
    print(f"  第{layer.layer}层: {len(layer.tasks)}个任务, "
          f"可并行={layer.can_parallel}, "
          f"预估耗时={layer.estimated_duration:.1f}秒")


# ============================================
# 示例2: 存在依赖关系的任务
# ============================================
print("\n" + "=" * 60)
print("示例2: 图片生成 + 视频合成 (有依赖)")
print("=" * 60)

dependent_tasks = [
    {"id": "img1", "type": "text-to-image", "params": {"prompt": "帧1"}},
    {"id": "img2", "type": "text-to-image", "params": {"prompt": "帧2"}},
    {"id": "img3", "type": "text-to-image", "params": {"prompt": "帧3"}},
    {
        "id": "video1",
        "type": "image-to-video",
        "params": {"first_frame": "output/img1/result.png"},
        "depends_on": ["img1"]
    },
]

analysis2 = analyze_concurrency_feasibility(dependent_tasks)

print(f"\n📊 分析结果:")
print(f"  总任务数: {analysis2.total_tasks}")
print(f"  独立任务: {analysis2.independent_tasks}")
print(f"  依赖任务: {analysis2.dependent_tasks}")
print(f"  推荐并发度: {analysis2.recommended_workers}")
print(f"  并行化比率: {analysis2.parallelization_ratio:.1%}")

print(f"\n💡 优化建议:")
for rec in analysis2.recommendations:
    print(f"  {rec}")

print(f"\n🔄 执行层次:")
for layer in analysis2.execution_layers:
    tasks_str = ", ".join(layer.tasks)
    print(f"  第{layer.layer}层: [{tasks_str}]")
    print(f"    可并行={layer.can_parallel}, 预估耗时={layer.estimated_duration:.1f}秒")


# ============================================
# 示例3: 复杂依赖链
# ============================================
print("\n" + "=" * 60)
print("示例3: 复杂依赖链 (多层依赖)")
print("=" * 60)

complex_tasks = [
    # 第0层: 3个独立任务
    {"id": "A1", "params": {}},
    {"id": "A2", "params": {}},
    {"id": "A3", "params": {}},

    # 第1层: 依赖第0层
    {"id": "B1", "params": {}, "depends_on": ["A1"]},
    {"id": "B2", "params": {}, "depends_on": ["A2"]},

    # 第2层: 依赖第1层
    {"id": "C1", "params": {}, "depends_on": ["B1", "B2"]},
]

analysis3 = analyze_concurrency_feasibility(complex_tasks)

print(f"\n📊 分析结果:")
print(f"  总任务数: {analysis3.total_tasks}")
print(f"  独立任务: {analysis3.independent_tasks}")
print(f"  依赖任务: {analysis3.dependent_tasks}")
print(f"  推荐并发度: {analysis3.recommended_workers}")
print(f"  并行化比率: {analysis3.parallelization_ratio:.1%}")

print(f"\n💡 优化建议:")
for rec in analysis3.recommendations:
    print(f"  {rec}")

print(f"\n🔄 执行层次:")
for layer in analysis3.execution_layers:
    tasks_str = ", ".join(layer.tasks)
    print(f"  第{layer.layer}层: [{tasks_str}]")
    print(f"    可并行={layer.can_parallel}")


print("\n" + "=" * 60)
print("✅ 示例运行完成!")
print("=" * 60)
