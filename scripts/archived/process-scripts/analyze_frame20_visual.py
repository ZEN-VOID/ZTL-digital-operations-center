#!/usr/bin/env python3
"""分析Frame 20的视觉元素:RECTANGLE背景板、VECTOR箭头、FRAME图片容器"""
import json

def extract_visual_elements(node, frame_x=2540, frame_y=12730, results=None, depth=0):
    """递归提取视觉元素"""
    if results is None:
        results = {
            'rectangles': [],
            'vectors': [],
            'frames': []
        }

    node_type = node.get('type')
    node_id = node.get('id')
    node_name = node.get('name', '')

    # 获取绝对位置
    bounds = node.get('absoluteBoundingBox', {})
    abs_x = bounds.get('x', 0)
    abs_y = bounds.get('y', 0)
    width = bounds.get('width', 0)
    height = bounds.get('height', 0)

    # 转换为相对坐标
    rel_x = abs_x - frame_x
    rel_y = abs_y - frame_y

    # RECTANGLE元素(背景板)
    if node_type == 'RECTANGLE':
        fills = node.get('fills', [])
        fill_info = None

        # 检查填充类型
        if fills and len(fills) > 0:
            fill = fills[0]
            fill_type = fill.get('type')

            if fill_type == 'SOLID':
                # 纯色填充
                color = fill.get('color', {})
                fill_info = {
                    'type': 'SOLID',
                    'color': f"rgba({int(color.get('r', 0) * 255)}, {int(color.get('g', 0) * 255)}, {int(color.get('b', 0) * 255)}, {color.get('a', 1)})"
                }
            elif fill_type == 'IMAGE':
                # 图片填充
                fill_info = {
                    'type': 'IMAGE',
                    'imageRef': fill.get('imageRef'),
                    'scaleMode': fill.get('scaleMode', 'FILL')
                }

        corner_radius = node.get('cornerRadius', 0)

        results['rectangles'].append({
            'id': node_id,
            'name': node_name,
            'abs': {'x': abs_x, 'y': abs_y},
            'rel': {'x': rel_x, 'y': rel_y},
            'width': width,
            'height': height,
            'fill': fill_info,
            'cornerRadius': corner_radius,
            'depth': depth
        })

    # VECTOR元素(箭头图标)
    elif node_type == 'VECTOR':
        fills = node.get('fills', [])
        fill_color = None
        if fills and len(fills) > 0:
            color = fills[0].get('color', {})
            fill_color = f"rgba({int(color.get('r', 0) * 255)}, {int(color.get('g', 0) * 255)}, {int(color.get('b', 0) * 255)}, {color.get('a', 1)})"

        results['vectors'].append({
            'id': node_id,
            'name': node_name,
            'abs': {'x': abs_x, 'y': abs_y},
            'rel': {'x': rel_x, 'y': rel_y},
            'width': width,
            'height': height,
            'fill': fill_color,
            'depth': depth
        })

    # FRAME元素(可能是图片容器)
    elif node_type == 'FRAME' and depth > 0:  # 排除根Frame
        results['frames'].append({
            'id': node_id,
            'name': node_name,
            'abs': {'x': abs_x, 'y': abs_y},
            'rel': {'x': rel_x, 'y': rel_y},
            'width': width,
            'height': height,
            'depth': depth
        })

    # 递归处理子节点
    if 'children' in node:
        for child in node['children']:
            extract_visual_elements(child, frame_x, frame_y, results, depth + 1)

    return results

# 读取Frame 20数据
with open('library/figma-informations/1u2yKbDBwJfmFagH6ym9p8_three-day-tour_frame20.json', 'r', encoding='utf-8') as f:
    frame20 = json.load(f)

# 提取视觉元素
results = extract_visual_elements(frame20)

print(f"\n✅ Frame 20视觉元素统计:")
print(f"  - RECTANGLE(背景板): {len(results['rectangles'])}个")
print(f"  - VECTOR(箭头): {len(results['vectors'])}个")
print(f"  - FRAME(图片容器): {len(results['frames'])}个\n")

# 输出RECTANGLE详情
print("=" * 100)
print("RECTANGLE元素 (背景板)")
print("=" * 100)
for i, rect in enumerate(results['rectangles'], 1):
    print(f"\n{i}. {rect['name']} (ID: {rect['id']})")
    print(f"   相对位置: left={rect['rel']['x']}px, top={rect['rel']['y']}px")
    print(f"   尺寸: {rect['width']}×{rect['height']}px")
    if rect['fill']:
        if rect['fill']['type'] == 'SOLID':
            print(f"   背景色: {rect['fill']['color']}")
        elif rect['fill']['type'] == 'IMAGE':
            print(f"   图片填充: {rect['fill']['imageRef']}")
            print(f"   缩放模式: {rect['fill']['scaleMode']}")
    if rect['cornerRadius'] > 0:
        print(f"   圆角: {rect['cornerRadius']}px")

# 输出VECTOR详情
print("\n" + "=" * 100)
print("VECTOR元素 (箭头图标)")
print("=" * 100)
for i, vec in enumerate(results['vectors'], 1):
    print(f"\n{i}. {vec['name']} (ID: {vec['id']})")
    print(f"   相对位置: left={vec['rel']['x']}px, top={vec['rel']['y']}px")
    print(f"   尺寸: {vec['width']}×{vec['height']}px")
    print(f"   颜色: {vec['fill']}")

# 输出FRAME详情
print("\n" + "=" * 100)
print("FRAME元素 (图片容器)")
print("=" * 100)
for i, frm in enumerate(results['frames'], 1):
    print(f"\n{i}. {frm['name']} (ID: {frm['id']})")
    print(f"   相对位置: left={frm['rel']['x']}px, top={frm['rel']['y']}px")
    print(f"   尺寸: {frm['width']}×{frm['height']}px")

# 保存JSON
with open('output/analysis/frame20_visual_elements.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n\n✅ 详细数据已保存: output/analysis/frame20_visual_elements.json")
