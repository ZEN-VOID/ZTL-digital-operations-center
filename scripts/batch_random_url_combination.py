#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量生成多个模板的随机URL组合

功能：
1. 自动扫描指定模板目录下的所有JSON索引文件
2. 从每个JSON文件中随机抽取1个图片URL
3. 生成指定数量的随机组合
4. 支持批量处理多个模板
"""

import json
import random
import os
from pathlib import Path
from datetime import datetime
import glob

def load_json_file(file_path):
    """加载JSON文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_json_files(template_dir):
    """
    查找模板目录下所有的JSON索引文件（排除root文件）

    Args:
        template_dir: 模板目录路径

    Returns:
        list: JSON文件路径列表
    """
    json_files = []

    # 使用glob查找所有cos-index-*.json文件
    pattern = os.path.join(template_dir, "**/cos-index-*.json")
    all_files = glob.glob(pattern, recursive=True)

    # 排除root文件
    for file_path in all_files:
        if "cos-index-root" not in file_path:
            json_files.append(Path(file_path))

    # 按文件名排序
    json_files.sort(key=lambda x: x.stem)

    return json_files

def random_select_from_files(file_paths, num_combinations=50):
    """
    从多个JSON文件中随机抽取URL生成组合

    Args:
        file_paths: JSON文件路径列表
        num_combinations: 生成的组合数量

    Returns:
        list: 包含随机组合的列表
    """
    # 加载所有JSON文件
    all_data = {}
    for file_path in file_paths:
        file_name = file_path.stem
        data = load_json_file(file_path)
        # 提取图片URL列表
        if 'images' in data:
            all_data[file_name] = data['images']
            print(f"  ✓ {file_name}: {len(data['images'])} 张图片")
        else:
            print(f"  ⚠ {file_name}: 没有 'images' 字段")
            continue

    if not all_data:
        print("  ❌ 错误: 没有找到有效的图片数据")
        return []

    # 生成随机组合
    combinations = []
    for i in range(num_combinations):
        combination = {
            "combination_id": i + 1,
            "created_at": datetime.now().isoformat(),
            "images": []
        }

        # 从每个文件中随机抽取一个URL
        for file_name, images in all_data.items():
            if images:
                random_image = random.choice(images)
                combination["images"].append({
                    "source": file_name,
                    "url": random_image.get("url", ""),
                    "key": random_image.get("key", "")
                })

        combinations.append(combination)

    return combinations

def process_template(template_name, input_dir, output_base_dir, num_combinations=50):
    """
    处理单个模板的随机组合生成

    Args:
        template_name: 模板名称（如"模板5"）
        input_dir: 输入目录路径
        output_base_dir: 输出基础目录路径
        num_combinations: 生成的组合数量
    """
    print(f"\n{'='*60}")
    print(f"处理 {template_name}")
    print(f"{'='*60}")

    # 查找JSON文件
    print(f"📂 扫描目录: {input_dir}")
    file_paths = find_json_files(input_dir)

    if not file_paths:
        print(f"❌ 错误: 在 {input_dir} 中没有找到JSON文件")
        return False

    print(f"📋 找到 {len(file_paths)} 个JSON文件:")

    # 生成随机组合
    combinations = random_select_from_files(file_paths, num_combinations)

    if not combinations:
        print(f"❌ 错误: 生成组合失败")
        return False

    # 创建输出目录
    output_dir = output_base_dir / template_name
    output_dir.mkdir(parents=True, exist_ok=True)

    # 保存结果
    output_file = output_dir / f"random-combinations-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"

    base_dir = Path(r"d:\@ZEN-VOID\ZTL\ZTL-AI-Powered-Digital-Design")
    output_data = {
        "metadata": {
            "template": template_name,
            "total_combinations": len(combinations),
            "sources": [str(p.relative_to(base_dir)) for p in file_paths],
            "generated_at": datetime.now().isoformat()
        },
        "combinations": combinations
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 成功生成 {len(combinations)} 组随机组合")
    print(f"📁 保存位置: {output_file.relative_to(base_dir)}")

    # 显示第一组示例
    if combinations:
        print(f"\n📸 示例组合 #1 (共 {len(combinations[0]['images'])} 个来源):")
        for img in combinations[0]["images"][:3]:  # 只显示前3个
            source_short = img['source'].replace('cos-index-', '')
            print(f"  - {source_short}")
        if len(combinations[0]['images']) > 3:
            print(f"  ... 还有 {len(combinations[0]['images']) - 3} 个来源")

    return True

def main():
    # 定义基础目录
    base_dir = Path(r"d:\@ZEN-VOID\ZTL\ZTL-AI-Powered-Digital-Design")
    url_base_dir = base_dir / "input" / "明红" / "图片URL"
    output_base_dir = url_base_dir / "随机组合"

    # 定义要处理的模板
    templates = [
        {
            "name": "模板5",
            "input_dir": url_base_dir / "模板5",
            "num_combinations": 50
        },
        {
            "name": "模板6",
            "input_dir": url_base_dir / "模板6",
            "num_combinations": 50
        },
        {
            "name": "模板7",
            "input_dir": url_base_dir / "模板7",
            "num_combinations": 50
        }
    ]

    print("=" * 60)
    print("批量生成随机URL组合")
    print("=" * 60)

    success_count = 0
    fail_count = 0

    # 处理每个模板
    for template in templates:
        try:
            if process_template(
                template["name"],
                template["input_dir"],
                output_base_dir,
                template["num_combinations"]
            ):
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            print(f"❌ 处理 {template['name']} 时出错: {e}")
            fail_count += 1

    # 总结
    print(f"\n{'='*60}")
    print(f"处理完成")
    print(f"{'='*60}")
    print(f"✅ 成功: {success_count} 个模板")
    print(f"❌ 失败: {fail_count} 个模板")

if __name__ == "__main__":
    main()
