#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将合并的随机组合JSON拆分为独立文件

功能：
1. 读取合并的JSON文件（包含50组合并的组合）
2. 将每个组合拆分为独立的JSON文件
3. 转换为/3脚本兼容的扁平格式
4. 保存到相应的输出目录
"""

import json
from pathlib import Path
from datetime import datetime

def convert_to_flat_format(combination_data):
    """
    将新格式转换为/3脚本兼容的扁平格式

    输入格式:
    {
        "combination_id": 1,
        "images": [
            {"source": "cos-index-1.自然博物馆", "url": "https://...", "key": ""}
        ]
    }

    输出格式:
    {
        "1.自然博物馆": ["https://..."],
        "2.东郊记忆": ["https://..."]
    }

    Args:
        combination_data: 单个组合的数据

    Returns:
        dict: 扁平格式的字典
    """
    flat_data = {}

    for i, image_data in enumerate(combination_data.get("images", []), 1):
        # 提取景点名称（去掉"cos-index-"前缀）
        source = image_data.get("source", "")
        # 处理source名称
        # 格式1: "cos-index-1.自然博物馆" -> "1.自然博物馆"
        # 格式2: "cos-index-DAY1.1太古里" -> "DAY1.1太古里"
        # 格式3: "cos-index-普通经典-1-1太古里" -> "普通经典-1-1太古里"
        if source.startswith("cos-index-"):
            key = source.replace("cos-index-", "")
        else:
            key = f"{i}.{source}"

        url = image_data.get("url", "")

        # 使用扁平格式：键 -> [URL列表]
        flat_data[key] = [url]

    return flat_data

def split_combined_json(input_file, output_dir, template_name):
    """
    拆分合并的JSON文件为独立文件

    Args:
        input_file: 输入的合并JSON文件路径
        output_dir: 输出目录路径
        template_name: 模板名称（用于生成文件名）
    """
    print(f"\n{'='*60}")
    print(f"处理 {template_name}")
    print(f"{'='*60}")
    print(f"📂 输入文件: {input_file}")

    # 加载合并的JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    metadata = data.get("metadata", {})
    combinations = data.get("combinations", [])

    print(f"📊 找到 {len(combinations)} 个组合")
    print(f"📁 输出目录: {output_dir}")

    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)

    # 拆分每个组合
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    for combination in combinations:
        combination_id = combination.get("combination_id", 0)

        # 转换为扁平格式
        flat_data = convert_to_flat_format(combination)

        # 生成文件名（与模板1的命名规则一致）
        # 格式: random_{id:02d}_{timestamp}.json
        output_filename = f"random_{combination_id:02d}_{timestamp}.json"
        output_path = output_dir / output_filename

        # 保存为独立JSON文件
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(flat_data, f, ensure_ascii=False, indent=2)

        if combination_id <= 3 or combination_id == len(combinations):
            print(f"  ✅ 生成: {output_filename} ({len(flat_data)} 个景点)")
        elif combination_id == 4:
            print(f"  ... 处理中 ...")

    print(f"\n✅ 成功拆分 {len(combinations)} 个组合")
    print(f"📁 保存到: {output_dir.relative_to(base_dir)}")

    # 显示第一个文件的内容示例
    if combinations:
        first_file = output_dir / f"random_01_{timestamp}.json"
        if first_file.exists():
            print(f"\n📄 示例文件内容 (random_01_{timestamp}.json):")
            with open(first_file, 'r', encoding='utf-8') as f:
                sample_data = json.load(f)
            for key in list(sample_data.keys())[:3]:
                url_short = sample_data[key][0][:80] + "..." if len(sample_data[key][0]) > 80 else sample_data[key][0]
                print(f'  "{key}": ["{url_short}"]')
            if len(sample_data) > 3:
                print(f"  ... 还有 {len(sample_data) - 3} 个景点")

def main():
    """主函数 - 处理所有模板"""
    global base_dir
    base_dir = Path(r"d:\@ZEN-VOID\ZTL\ZTL-AI-Powered-Digital-Design")

    # 定义要处理的模板
    templates = [
        {
            "name": "模板4",
            "input_file": base_dir / "input" / "明红" / "图片URL" / "随机组合" / "模板4" / "random-combinations-20251005-160158.json",
            "output_dir": base_dir / "input" / "明红" / "图片URL" / "随机组合" / "模板4"
        },
        {
            "name": "模板5",
            "input_file": base_dir / "input" / "明红" / "图片URL" / "随机组合" / "模板5" / "random-combinations-20251005-160513.json",
            "output_dir": base_dir / "input" / "明红" / "图片URL" / "随机组合" / "模板5"
        },
        {
            "name": "模板6",
            "input_file": base_dir / "input" / "明红" / "图片URL" / "随机组合" / "模板6" / "random-combinations-20251005-160514.json",
            "output_dir": base_dir / "input" / "明红" / "图片URL" / "随机组合" / "模板6"
        },
        {
            "name": "模板7",
            "input_file": base_dir / "input" / "明红" / "图片URL" / "随机组合" / "模板7" / "random-combinations-20251005-160514.json",
            "output_dir": base_dir / "input" / "明红" / "图片URL" / "随机组合" / "模板7"
        }
    ]

    print("=" * 60)
    print("拆分合并JSON为独立文件")
    print("=" * 60)

    success_count = 0
    fail_count = 0

    for template in templates:
        try:
            if not template["input_file"].exists():
                print(f"\n❌ 输入文件不存在: {template['input_file']}")
                fail_count += 1
                continue

            split_combined_json(
                template["input_file"],
                template["output_dir"],
                template["name"]
            )
            success_count += 1
        except Exception as e:
            print(f"\n❌ 处理 {template['name']} 时出错: {e}")
            import traceback
            traceback.print_exc()
            fail_count += 1

    # 总结
    print(f"\n{'='*60}")
    print(f"处理完成")
    print(f"{'='*60}")
    print(f"✅ 成功: {success_count} 个模板")
    print(f"❌ 失败: {fail_count} 个模板")
    print(f"\n💡 提示: 拆分后的JSON文件可直接用于/3指令进行批量替换")

if __name__ == "__main__":
    main()
