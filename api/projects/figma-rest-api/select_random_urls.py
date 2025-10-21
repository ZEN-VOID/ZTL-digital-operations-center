"""
从6个JSON文件中随机选择图片URL用于Figma批量替换
"""
import json
import random
from pathlib import Path

# 定义JSON文件路径
json_files = [
    r"d:\@ZEN-VOID\Round-2\ZTL餐饮数智化平面设计\input\明红\图片URL\模板1\1.IFS\cos-index.json",
    r"d:\@ZEN-VOID\Round-2\ZTL餐饮数智化平面设计\input\明红\图片URL\模板1\2.太古里\cos-index.json",
    r"d:\@ZEN-VOID\Round-2\ZTL餐饮数智化平面设计\input\明红\图片URL\模板1\3.大慈寺\cos-index.json",
    r"d:\@ZEN-VOID\Round-2\ZTL餐饮数智化平面设计\input\明红\图片URL\模板1\4.望平街\cos-index.json",
    r"d:\@ZEN-VOID\Round-2\ZTL餐饮数智化平面设计\input\明红\图片URL\模板1\5.人民公园\cos-index.json",
    r"d:\@ZEN-VOID\Round-2\ZTL餐饮数智化平面设计\input\明红\图片URL\模板1\6.宽窄巷子\cos-index.json"
]

selected_urls = []

for file_path in json_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # JSON结构: {"metadata": {...}, "images": [...]}
        if 'images' in data and isinstance(data['images'], list) and len(data['images']) > 0:
            # 随机选择一个图片
            random_image = random.choice(data['images'])
            url = random_image.get('url')

            if url:
                selected_urls.append({
                    'source_file': Path(file_path).parent.name,
                    'filename': random_image.get('filename', 'unknown'),
                    'url': url
                })
                print(f"✓ 从 {Path(file_path).parent.name} 选择: {random_image.get('filename')}")

    except Exception as e:
        print(f"✗ 读取 {file_path} 失败: {e}")

# 输出结果
print(f"\n成功选择 {len(selected_urls)} 个URL:")
for i, item in enumerate(selected_urls, 1):
    print(f"{i}. [{item['source_file']}] {item['filename']}")
    print(f"   URL: {item['url'][:100]}...")

# 保存结果到文件
output_file = "selected_urls.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(selected_urls, f, ensure_ascii=False, indent=2)

print(f"\n结果已保存到: {output_file}")