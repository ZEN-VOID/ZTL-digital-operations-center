"""
批量处理three-day-tour模板 - 图片替换和截图
模板6批量处理脚本
"""

import json
import time
import os
from pathlib import Path

# 配置
TEMPLATE_PAGE = Path("project/src/app/three-day-tour/page.tsx")
INPUT_DIR = Path("input/明红/图片URL/随机组合/模板6")
OUTPUT_DIR = Path("output/screenshots/three-day-tour")
BACKUP_FILE = TEMPLATE_PAGE.with_suffix('.tsx.backup')

# 创建输出目录
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 图片URL到占位符的映射
IMAGE_MAPPING = {
    "DAY1.1太古里": "179:32",      # day1-1
    "DAY1.2IFS": "179:33",          # day1-2
    "DAY1.3大慈寺": "179:34",       # day1-3
    "DAY1.4望平街": "179:35",       # day1-4
    "DAY2.1大熊猫基地": "164:61",   # day2-1 (实际是自然博物馆位置)
    "DAY2.2武侯祠": "165:21",       # day2-2
    "DAY2.3锦里": "165:28",         # day2-3
    "DAY2.4杜甫草堂": "165:35",     # day2-4
    "DAY3.1自然博物馆": "179:51",   # day3-1
    "DAY3.2东郊记忆": "179:52",     # day3-2
    "DAY3.3建设路": "179:53",       # day3-3
    "DAY3.4玉林路": "179:54"        # day3-4
}

def backup_template():
    """备份原始模板"""
    if not BACKUP_FILE.exists():
        content = TEMPLATE_PAGE.read_text(encoding='utf-8')
        BACKUP_FILE.write_text(content, encoding='utf-8')
        print(f"✅ 备份原始模板: {BACKUP_FILE}")

def restore_template():
    """恢复原始模板"""
    if BACKUP_FILE.exists():
        content = BACKUP_FILE.read_text(encoding='utf-8')
        TEMPLATE_PAGE.write_text(content, encoding='utf-8')
        print(f"✅ 恢复原始模板")

def replace_images(json_file):
    """替换图片URL到模板"""
    # 读取JSON配置
    with open(json_file, 'r', encoding='utf-8') as f:
        image_data = json.load(f)

    # 读取模板内容
    content = TEMPLATE_PAGE.read_text(encoding='utf-8')

    # 替换每个图片URL
    replacements = 0
    for key, figma_id in IMAGE_MAPPING.items():
        if key in image_data and image_data[key]:
            url = image_data[key][0]  # 取第一个URL

            # 查找并替换对应的占位符
            # 灰色占位框格式: background: 'rgba(217, 217, 217, 1)'
            search_pattern = f'data-figma-id="{figma_id}"'

            if search_pattern in content:
                # 找到该元素,替换background为backgroundImage
                start_pos = content.find(search_pattern)
                # 找到该元素的style开始和结束位置
                style_start = content.rfind('style={{', 0, start_pos)
                style_end = content.find('}}', start_pos)

                if style_start != -1 and style_end != -1:
                    # 提取原始style
                    old_style = content[style_start:style_end+2]

                    # 构建新style - 用backgroundImage替换background
                    new_style = old_style.replace(
                        "background: 'rgba(217, 217, 217, 1)'",
                        f"backgroundImage: 'url({url})', backgroundSize: 'cover', backgroundPosition: 'center'"
                    )

                    content = content[:style_start] + new_style + content[style_end+2:]
                    replacements += 1

    # 写回文件
    TEMPLATE_PAGE.write_text(content, encoding='utf-8')
    print(f"✅ 替换完成: {replacements} 张图片")
    return replacements

def process_batch():
    """批量处理所有JSON文件"""
    # 备份原始模板
    backup_template()

    # 获取所有JSON文件
    json_files = sorted(INPUT_DIR.glob("random_*.json"))
    total = len(json_files)

    print(f"\n📊 开始批量处理: {total} 个配置文件\n")

    for idx, json_file in enumerate(json_files, 1):
        print(f"\n{'='*60}")
        print(f"[{idx}/{total}] 处理: {json_file.name}")
        print(f"{'='*60}")

        try:
            # 1. 替换图片
            replace_images(json_file)

            # 2. 等待热更新
            print("⏳ 等待页面热更新...")
            time.sleep(3)

            # 3. 截图指令
            screenshot_name = f"three-day-tour-{json_file.stem}"
            print(f"\n📸 请在浏览器中截图: {screenshot_name}")
            print(f"   访问: http://localhost:3005/three-day-tour")
            print(f"   保存到: {OUTPUT_DIR / screenshot_name}.png")

            # 4. 等待用户确认
            input("\n按Enter继续下一个...")

        except Exception as e:
            print(f"❌ 处理失败: {e}")
            continue

    # 恢复原始模板
    restore_template()
    print(f"\n\n✅ 批量处理完成!")
    print(f"📊 总计: {total} 个配置文件")
    print(f"📁 输出目录: {OUTPUT_DIR}")

if __name__ == "__main__":
    process_batch()
