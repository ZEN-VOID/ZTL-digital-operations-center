#!/usr/bin/env python3
"""
提取Figma Frame 20中的背景板(RECTANGLE)和照片(IMAGE)元素
"""
import json

def extract_visual_elements(node, parent_x=0, parent_y=0, results=None):
    """递归提取RECTANGLE和IMAGE元素"""
    if results is None:
        results = {'rectangles': [], 'images': []}

    node_type = node.get('type')
    node_id = node.get('id')
    node_name = node.get('name', '')

    # 获取绝对位置
    bounds = node.get('absoluteBoundingBox', {})
    x = bounds.get('x', 0)
    y = bounds.get('y', 0)
    width = bounds.get('width', 0)
    height = bounds.get('height', 0)

    # 提取RECTANGLE元素(背景板)
    if node_type == 'RECTANGLE':
        # 获取填充颜色
        fills = node.get('fills', [])
        fill_info = None
        if fills and len(fills) > 0:
            fill = fills[0]
            if fill.get('type') == 'SOLID':
                color = fill.get('color', {})
                fill_info = {
                    'r': int(color.get('r', 0) * 255),
                    'g': int(color.get('g', 0) * 255),
                    'b': int(color.get('b', 0) * 255),
                    'a': color.get('a', 1)
                }

        # 获取圆角
        corner_radius = node.get('cornerRadius', 0)

        results['rectangles'].append({
            'id': node_id,
            'name': node_name,
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'fill': fill_info,
            'cornerRadius': corner_radius
        })

    # 提取IMAGE元素(照片)
    elif node_type == 'RECTANGLE' and node.get('fills', []):
        # 检查是否包含图片填充
        fills = node.get('fills', [])
        for fill in fills:
            if fill.get('type') == 'IMAGE':
                image_ref = fill.get('imageRef')
                results['images'].append({
                    'id': node_id,
                    'name': node_name,
                    'x': x,
                    'y': y,
                    'width': width,
                    'height': height,
                    'imageRef': image_ref,
                    'scaleMode': fill.get('scaleMode', 'FILL')
                })

    # 递归处理子节点
    if 'children' in node:
        for child in node['children']:
            extract_visual_elements(child, x, y, results)

    return results

# 读取数据
with open('temp_figma_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 提取Frame 20 (node id: 178:7)
frame20 = data.get('document', {}).get('children', [{}])[0].get('children', [{}])[0].get('children', [])
target_frame = None
for frame in frame20:
    if frame.get('id') == '178:7':
        target_frame = frame
        break

if target_frame:
    results = extract_visual_elements(target_frame)

    print(f"\n找到 {len(results['rectangles'])} 个RECTANGLE元素(背景板)")
    print(f"找到 {len(results['images'])} 个IMAGE元素(照片)\n")

    # 输出详细信息
    print("=" * 80)
    print("RECTANGLE元素 (背景板)")
    print("=" * 80)
    for i, rect in enumerate(results['rectangles'], 1):
        print(f"\n{i}. {rect['name']} (ID: {rect['id']})")
        print(f"   位置: ({rect['x']}, {rect['y']})")
        print(f"   尺寸: {rect['width']}×{rect['height']}")
        if rect['fill']:
            print(f"   颜色: rgba({rect['fill']['r']}, {rect['fill']['g']}, {rect['fill']['b']}, {rect['fill']['a']})")
        if rect['cornerRadius'] > 0:
            print(f"   圆角: {rect['cornerRadius']}px")

    print("\n" + "=" * 80)
    print("IMAGE元素 (照片)")
    print("=" * 80)
    for i, img in enumerate(results['images'], 1):
        print(f"\n{i}. {img['name']} (ID: {img['id']})")
        print(f"   位置: ({img['x']}, {img['y']})")
        print(f"   尺寸: {img['width']}×{img['height']}")
        print(f"   图片引用: {img['imageRef']}")
        print(f"   缩放模式: {img['scaleMode']}")

    # 保存为JSON
    with open('output/analysis/frame20_visual_elements.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n详细数据已保存到: output/analysis/frame20_visual_elements.json")
else:
    print("未找到Frame 20 (ID: 178:7)")
