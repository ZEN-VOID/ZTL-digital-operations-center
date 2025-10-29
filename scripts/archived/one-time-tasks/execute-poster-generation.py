#!/usr/bin/env python3
"""
冰川鲜毛肚海报生成执行脚本
调用nano-banana技能包的text-to-image能力
"""

import sys
import os

# 添加技能包路径到Python路径
sys.path.insert(0, '/Users/vincentlee/Desktop/ZTL数智化作战中心/.claude/skills/aigc/_shared')

from plan_executor import execute_plan

def main():
    """执行海报生成任务"""
    plan_path = '/Users/vincentlee/Desktop/ZTL数智化作战中心/api/plans/e1-text-to-image/glacier-tripe-poster.json'

    print("=" * 60)
    print("开始生成冰川鲜毛肚海报")
    print("=" * 60)

    try:
        result = execute_plan(plan_path)

        if result['status'] == 'success':
            print("\n✅ 海报生成成功!")
            print(f"📁 保存路径: {result['output_path']}")
            print(f"🎨 图片尺寸: {result.get('dimensions', 'N/A')}")
            print(f"⏱️  生成耗时: {result.get('duration', 'N/A')}秒")
        else:
            print(f"\n❌ 生成失败: {result.get('error', '未知错误')}")
            return 1

    except Exception as e:
        print(f"\n❌ 执行出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

    print("\n" + "=" * 60)
    return 0

if __name__ == '__main__':
    exit(main())
