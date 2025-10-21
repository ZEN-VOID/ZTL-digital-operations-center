#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证拆分后的JSON格式是否与/3脚本兼容

测试逻辑：模拟batch_replace_images.py中的JSON解析代码
"""

import json
from pathlib import Path

def test_json_parsing(json_file):
    """
    模拟batch_replace_images.py的JSON解析逻辑

    原代码:
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    urls = [list(urls)[0] for urls in data.values()]
    """
    print(f"\n{'='*60}")
    print(f"测试文件: {json_file.name}")
    print(f"{'='*60}")

    try:
        # 读取JSON文件
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"✅ JSON加载成功")
        print(f"📊 数据结构: {type(data)}")
        print(f"📊 键数量: {len(data)}")

        # 模拟/3脚本的解析逻辑
        urls = [list(urls)[0] for urls in data.values()]

        print(f"✅ URL提取成功")
        print(f"📊 提取到 {len(urls)} 个URL")

        # 显示前3个URL的简化版本
        print(f"\n📄 提取的URL示例:")
        for i, url in enumerate(urls[:3], 1):
            url_short = url[:80] + "..." if len(url) > 80 else url
            print(f"  {i}. {url_short}")

        if len(urls) > 3:
            print(f"  ... 还有 {len(urls) - 3} 个URL")

        # 验证URL格式
        print(f"\n✅ 格式验证:")
        all_valid = True
        for i, url in enumerate(urls, 1):
            if not url.startswith("https://"):
                print(f"  ❌ URL {i} 格式错误: 不是https://开头")
                all_valid = False
            elif "cos.ap-chengdu.myqcloud.com" not in url:
                print(f"  ⚠️  URL {i} 警告: 不包含预期的COS域名")

        if all_valid:
            print(f"  ✅ 所有URL格式正确")

        return True

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数 - 测试所有模板的第一个JSON文件"""
    base_dir = Path(r"d:\@ZEN-VOID\ZTL\ZTL-AI-Powered-Digital-Design")

    # 定义要测试的文件
    test_files = [
        base_dir / "input" / "明红" / "图片URL" / "随机组合" / "模板4" / "random_01_20251005_162425.json",
        base_dir / "input" / "明红" / "图片URL" / "随机组合" / "模板5" / "random_01_20251005_162425.json",
        base_dir / "input" / "明红" / "图片URL" / "随机组合" / "模板6" / "random_01_20251005_162426.json",
        base_dir / "input" / "明红" / "图片URL" / "随机组合" / "模板7" / "random_01_20251005_162426.json",
    ]

    print("=" * 60)
    print("验证JSON格式兼容性")
    print("=" * 60)
    print("模拟/3脚本的JSON解析逻辑")

    success_count = 0
    fail_count = 0

    for test_file in test_files:
        if not test_file.exists():
            print(f"\n❌ 文件不存在: {test_file.name}")
            fail_count += 1
            continue

        if test_json_parsing(test_file):
            success_count += 1
        else:
            fail_count += 1

    # 总结
    print(f"\n{'='*60}")
    print(f"验证结果")
    print(f"{'='*60}")
    print(f"✅ 成功: {success_count}/{len(test_files)} 个文件")
    print(f"❌ 失败: {fail_count}/{len(test_files)} 个文件")

    if fail_count == 0:
        print(f"\n🎉 所有JSON文件格式完全兼容/3脚本!")
        print(f"💡 可以直接使用/3指令进行批量替换操作")
    else:
        print(f"\n⚠️  存在格式问题，需要修复")

if __name__ == "__main__":
    main()
