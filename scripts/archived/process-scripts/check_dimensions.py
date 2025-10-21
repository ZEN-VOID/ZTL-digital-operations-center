import json

# 读取原始JSON
with open('../library/figma-informations/1u2yKbDBwJfmFagH6ym9p8_three-day-tour_raw.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def find_node_by_id(node, target_id):
    """递归查找指定ID的节点"""
    if node.get('id') == target_id:
        return node
    if 'children' in node:
        for child in node['children']:
            result = find_node_by_id(child, target_id)
            if result:
                return result
    return None

def search_in_document(doc, target_id):
    """在document中搜索"""
    if 'children' in doc:
        for child in doc['children']:
            result = find_node_by_id(child, target_id)
            if result:
                return result
    return None

# 查找Frame 178:7
frame = search_in_document(data.get('document', {}), '178:7')

if frame:
    bbox = frame.get('absoluteBoundingBox', {})
    print(f"Frame 178:7 尺寸: {bbox.get('width')}×{bbox.get('height')}px")
    print(f"Frame 178:7 位置: ({bbox.get('x')}, {bbox.get('y')})")
    print()

    # 提取所有RECTANGLE节点(图片)的尺寸
    def extract_rectangles(node, results=None):
        if results is None:
            results = []
        if node.get('type') == 'RECTANGLE' and 'Rectangle' in node.get('name', ''):
            bbox = node.get('absoluteBoundingBox', {})
            results.append({
                'id': node.get('id'),
                'name': node.get('name', ''),
                'width': bbox.get('width'),
                'height': bbox.get('height'),
                'x': bbox.get('x'),
                'y': bbox.get('y')
            })
        if 'children' in node:
            for child in node['children']:
                extract_rectangles(child, results)
        return results

    rectangles = extract_rectangles(frame)
    print(f"找到 {len(rectangles)} 个图片矩形:")
    for r in rectangles:
        print(f"  {r['id']:10s} | {r['name']:20s} | {r['width']}×{r['height']}px | 位置({r['x']}, {r['y']})")
else:
    print("未找到Frame 178:7")
