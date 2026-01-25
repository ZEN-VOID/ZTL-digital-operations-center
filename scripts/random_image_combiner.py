"""
图片随机选择组合器
从指定目录的cos-index.json文件中随机选择指定数量的图片URL,并保存为极简JSON格式
"""
import json
import random
from pathlib import Path
from datetime import datetime
from typing import List, Dict


def load_cos_index(cos_index_path: Path) -> List[Dict]:
    """加载cos-index.json文件"""
    with open(cos_index_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get('images', [])


def random_select(images: List[Dict], count: int = 1) -> List[str]:
    """随机选择指定数量的图片URL"""
    if count > len(images):
        count = len(images)
    selected = random.sample(images, count)
    return [img['url'] for img in selected]


def combine_random_images(
    source_dirs: List[str],
    counts: List[int],
    output_path: Path
):
    """
    从多个源目录随机选择图片并组合

    Args:
        source_dirs: 源目录路径列表(相对于input/明红/图片URL/)
        counts: 每个目录选择的数量
        output_path: 输出文件路径
    """
    base_dir = Path(__file__).parent.parent / 'input' / '明红' / '图片URL'

    result = {}

    for source_dir, count in zip(source_dirs, counts):
        # 构建cos-index.json路径 (优先查找带景点名的文件)
        dir_name = Path(source_dir).name  # 例如: DAY1.1太古里
        cos_index_with_name = base_dir / source_dir / f'cos-index-{dir_name}.json'
        cos_index_standard = base_dir / source_dir / 'cos-index.json'

        # 优先使用带景点名的文件
        if cos_index_with_name.exists():
            cos_index_path = cos_index_with_name
        elif cos_index_standard.exists():
            cos_index_path = cos_index_standard
        else:
            print(f"警告: 未找到cos-index文件,跳过 {source_dir}")
            continue

        # 加载并随机选择
        images = load_cos_index(cos_index_path)
        selected_urls = random_select(images, count)

        # 使用目录名作为key
        key = Path(source_dir).name
        result[key] = selected_urls

    # 保存为极简JSON
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✓ 已保存随机组合到: {output_path}")
    print(f"  共选择 {sum(len(v) for v in result.values())} 张图片")


def main():
    """主函数"""
    # 配置: 从模板6 (three-day-tour) 的12个景点各随机选择1张图片
    source_dirs = [
        '模板6/DAY1.1太古里',
        '模板6/DAY1.2IFS',
        '模板6/DAY1.3大慈寺',
        '模板6/DAY1.4望平街',
        '模板6/DAY2.1大熊猫基地',
        '模板6/DAY2.2武侯祠',
        '模板6/DAY2.3锦里',
        '模板6/DAY2.4杜甫草堂',
        '模板6/DAY3.1自然博物馆',
        '模板6/DAY3.2东郊记忆',
        '模板6/DAY3.3建设路',
        '模板6/DAY3.4玉林路'
    ]

    # 每个目录选择的数量(默认都为1)
    counts = [1] * len(source_dirs)

    # 批量生成20组随机组合(仅生成缺失的序号)
    missing_indices = [10, 15, 16, 18, 20, 22, 24, 25, 26, 27, 30, 35, 36, 37, 38, 44, 45, 46, 49, 50]
    batch_count = len(missing_indices)
    print(f"开始生成 {batch_count} 组缺失的随机图片组合...")
    print(f"缺失序号: {missing_indices}")
    print(f"每组从12个景点各选择1张图片\n")

    for idx, num in enumerate(missing_indices):
        # 输出路径（每组使用独立的编号和时间戳）
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = Path(__file__).parent.parent / 'input' / '明红' / '图片URL' / '随机组合' / '模板6' / f'random_{num:02d}_{timestamp}.json'

        # 执行组合
        print(f"[{idx+1}/{batch_count}] 序号 {num:02d}: ", end='')
        combine_random_images(source_dirs, counts, output_path)

    print(f"\n✓ 成功生成 {batch_count} 组随机图片组合!")
    print(f"  保存位置: input/明红/图片URL/随机组合/模板6/")


if __name__ == '__main__':
    main()
