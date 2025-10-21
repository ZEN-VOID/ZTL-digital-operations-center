"""
主控脚本 - 自动化批量截图流程
由Claude Code调用,自动完成50个批次的图片替换和截图
"""

import sys
import time
import subprocess
from pathlib import Path

# 导入批量处理模块
sys.path.insert(0, str(Path(__file__).parent))
from auto_batch_three_day_tour import process_next_batch

def run_full_batch():
    """
    运行完整的50个批次
    每个批次:
    1. 替换图片
    2. 等待热更新(3秒)
    3. 触发截图(通过输出指令让Claude Code执行)
    """
    print("="*60)
    print("开始批量处理 - 共50个批次")
    print("="*60)

    for batch_index in range(50):
        print(f"\n{'='*60}")
        print(f"批次 {batch_index + 1}/50")
        print(f"{'='*60}")

        # 1. 处理当前批次(替换图片)
        result = process_next_batch(batch_index)

        if not result['success']:
            print(f"❌ 批次 {batch_index + 1} 处理失败")
            continue

        print(f"✅ 图片替换完成: {result['replaced_count']} 张")
        print(f"📄 JSON文件: {result['json_file']}")
        print(f"📸 截图名称: {result['screenshot_name']}")

        # 2. 等待热更新
        print("⏳ 等待页面热更新(3秒)...")
        time.sleep(3)

        # 3. 输出截图指令(让Claude Code执行)
        print(f"\n🎯 截图指令:")
        print(f"SCREENSHOT_CMD::{result['screenshot_name']}")

        # 4. 等待截图完成(给Claude Code一些时间)
        time.sleep(2)

        print(f"\n✅ 批次 {batch_index + 1} 完成")

    print(f"\n\n{'='*60}")
    print("✅ 所有50个批次处理完成!")
    print(f"{'='*60}")

if __name__ == "__main__":
    run_full_batch()
