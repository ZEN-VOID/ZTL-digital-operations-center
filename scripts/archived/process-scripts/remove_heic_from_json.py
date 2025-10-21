#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从JSON文件中移除所有HEIC格式的图片URL
"""

import json
from pathlib import Path

def remove_heic_from_json(json_file_path: str) -> dict:
    """
    从JSON文件中移除所有HEIC格式的图片条目
    
    Args:
        json_file_path: JSON文件路径
        
    Returns:
        包含移除统计信息的字典
    """
    file_path = Path(json_file_path)
    
    if not file_path.exists():
        return {
            'status': 'error',
            'message': f'文件不存在: {json_file_path}'
        }
    
    # 读取JSON文件
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 统计信息
    original_count = len(data.get('images', []))
    
    # 过滤掉HEIC格式的图片
    filtered_images = [
        img for img in data.get('images', [])
        if not img.get('filename', '').upper().endswith('.HEIC')
    ]
    
    removed_count = original_count - len(filtered_images)
    
    # 更新数据
    data['images'] = filtered_images
    
    # 更新metadata中的total_images
    if 'metadata' in data:
        data['metadata']['total_images'] = len(filtered_images)
    
    # 保存回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return {
        'status': 'success',
        'file': json_file_path,
        'original_count': original_count,
        'removed_count': removed_count,
        'remaining_count': len(filtered_images)
    }

def main():
    """主函数 - 处理所有指定的JSON文件"""
    
    # 要处理的文件列表
    files = [
        'input/明红/图片URL/模板1/1.IFS/cos-index.json',
        'input/明红/图片URL/模板1/2.太古里/cos-index.json',
        'input/明红/图片URL/模板1/3.大慈寺/cos-index.json',
        'input/明红/图片URL/模板1/4.望平街/cos-index.json',
        'input/明红/图片URL/模板1/5.人民公园/cos-index.json',
        'input/明红/图片URL/模板1/6.宽窄巷子/cos-index.json',
    ]
    
    print('=' * 70)
    print('🧹 开始移除HEIC格式图片URL')
    print('=' * 70)
    
    results = []
    total_removed = 0
    
    for file_path in files:
        print(f'\n📄 处理: {file_path}')
        result = remove_heic_from_json(file_path)
        results.append(result)
        
        if result['status'] == 'success':
            print(f'  ✅ 原始数量: {result["original_count"]}')
            print(f'  ❌ 移除HEIC: {result["removed_count"]}')
            print(f'  ✅ 剩余数量: {result["remaining_count"]}')
            total_removed += result['removed_count']
        else:
            print(f'  ❌ 错误: {result["message"]}')
    
    # 输出总结
    print('\n' + '=' * 70)
    print('📊 处理总结')
    print('=' * 70)
    
    success_count = sum(1 for r in results if r['status'] == 'success')
    
    print(f'\n✅ 成功处理: {success_count}/{len(files)} 个文件')
    print(f'🗑️  总共移除: {total_removed} 个HEIC格式图片')
    
    print('\n' + '=' * 70)
    print('🎉 全部完成!')
    print('=' * 70)

if __name__ == '__main__':
    main()

