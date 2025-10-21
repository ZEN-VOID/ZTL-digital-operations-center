"""
全自动批量处理three-day-tour模板
使用Claude Code直接调用,无需手动操作
"""

import json
from pathlib import Path

# 配置
TEMPLATE_PAGE = Path("project/src/app/three-day-tour/page.tsx")
INPUT_DIR = Path("input/明红/图片URL/随机组合/模板6")
BACKUP_FILE = TEMPLATE_PAGE.with_suffix('.tsx.backup')

# 图片URL到data-figma-id的映射(按页面实际显示顺序)
# DAY1列(left:56px) → DAY2列(left:511px) → DAY3列(left:978px)
IMAGE_MAPPING = {
    # DAY1列 (从上到下)
    "DAY1.1太古里": "164:61",      # top: 469px
    "DAY1.2IFS": "165:21",          # top: 851px
    "DAY1.3大慈寺": "165:28",       # top: 1233px
    "DAY1.4望平街": "165:35",       # top: 1615px

    # DAY2列 (从上到下)
    "DAY2.1大熊猫基地": "179:32",   # top: 469px
    "DAY2.2武侯祠": "179:33",       # top: 851px
    "DAY2.3锦里": "179:34",         # top: 1233px
    "DAY2.4杜甫草堂": "179:35",     # top: 1615px

    # DAY3列 (从上到下)
    "DAY3.1自然博物馆": "179:51",   # top: 469px
    "DAY3.2东郊记忆": "179:52",     # top: 851px
    "DAY3.3建设路": "179:53",       # top: 1233px
    "DAY3.4玉林路": "179:54"        # top: 1615px
}

def get_json_files():
    """获取所有JSON文件列表"""
    return sorted(INPUT_DIR.glob("random_*.json"))

def backup_template():
    """备份原始模板"""
    if not BACKUP_FILE.exists():
        content = TEMPLATE_PAGE.read_text(encoding='utf-8')
        BACKUP_FILE.write_text(content, encoding='utf-8')
        return True
    return False

def restore_template():
    """恢复原始模板"""
    if BACKUP_FILE.exists():
        content = BACKUP_FILE.read_text(encoding='utf-8')
        TEMPLATE_PAGE.write_text(content, encoding='utf-8')
        return True
    return False

def replace_images_in_template(json_file_path):
    """
    替换模板中的图片URL

    返回: (success: bool, replaced_count: int, json_filename: str)
    """
    # 读取JSON配置
    with open(json_file_path, 'r', encoding='utf-8') as f:
        image_data = json.load(f)

    # 读取模板内容
    content = TEMPLATE_PAGE.read_text(encoding='utf-8')

    # 逐个替换图片
    replacements = 0
    for location_key, figma_id in IMAGE_MAPPING.items():
        if location_key in image_data and image_data[location_key]:
            image_url = image_data[location_key][0]  # 取第一个URL

            # 查找对应的占位符div
            search_str = f'data-figma-id="{figma_id}"'

            if search_str in content:
                # 定位到这个元素的style属性
                elem_start = content.find(search_str)
                # 向前找style={{
                style_start = content.rfind('style={{', 0, elem_start)
                # 向后找}}
                style_end = content.find('}}', elem_start) + 2

                if style_start != -1 and style_end != -1:
                    old_style_block = content[style_start:style_end]

                    # 替换background为backgroundImage并添加backgroundSize和backgroundPosition
                    new_style_block = old_style_block.replace(
                        "background: 'rgba(217, 217, 217, 1)'",
                        f"backgroundImage: 'url({image_url})', backgroundSize: 'cover', backgroundPosition: 'center'"
                    )

                    content = content[:style_start] + new_style_block + content[style_end:]
                    replacements += 1

    # 写回文件
    TEMPLATE_PAGE.write_text(content, encoding='utf-8')

    return True, replacements, json_file_path.name

def get_next_json_file(current_index=0):
    """获取下一个要处理的JSON文件"""
    json_files = get_json_files()
    if current_index < len(json_files):
        return json_files[current_index], current_index + 1, len(json_files)
    return None, current_index, len(json_files)

# 主函数供Claude Code调用
def process_next_batch(batch_index=0):
    """
    处理指定索引的批次

    参数:
        batch_index: 要处理的批次索引(0-49)

    返回:
        dict: {
            'success': bool,
            'current_index': int,
            'total': int,
            'json_file': str,
            'replaced_count': int,
            'screenshot_name': str,
            'has_more': bool
        }
    """
    # 首次运行时备份
    if batch_index == 0:
        backup_template()

    json_file, next_index, total = get_next_json_file(batch_index)

    if json_file is None:
        # 处理完成,恢复模板
        restore_template()
        return {
            'success': True,
            'message': '所有批次处理完成',
            'total': total,
            'has_more': False
        }

    # 替换图片
    success, count, filename = replace_images_in_template(json_file)

    screenshot_name = f"three-day-tour-{json_file.stem}"

    return {
        'success': success,
        'current_index': batch_index + 1,
        'total': total,
        'json_file': filename,
        'replaced_count': count,
        'screenshot_name': screenshot_name,
        'has_more': next_index < total,
        'next_index': next_index
    }

if __name__ == "__main__":
    # 测试第一个文件
    result = process_next_batch(0)
    print(json.dumps(result, indent=2, ensure_ascii=False))
