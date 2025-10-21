import json

# 读取原始JSON
with open('../library/figma-informations/1u2yKbDBwJfmFagH6ym9p8_three-day-tour_raw.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def find_node_178_7(node):
    """递归查找node 178:7"""
    if node.get('id') == '178:7':
        return node
    if 'children' in node:
        for child in node['children']:
            result = find_node_178_7(child)
            if result:
                return result
    return None

def search_in_document(doc):
    """在document中搜索"""
    if 'children' in doc:
        for child in doc['children']:
            result = find_node_178_7(child)
            if result:
                return result
    return None

def extract_text_styles(node, results=None):
    """递归提取所有TEXT节点的样式"""
    if results is None:
        results = []

    if node.get('type') == 'TEXT' and 'style' in node:
        style = node['style']
        results.append({
            'id': node.get('id'),
            'name': node.get('name', node.get('characters', ''))[:30],
            'fontSize': style.get('fontSize'),
            'fontWeight': style.get('fontWeight'),
            'fontFamily': style.get('fontFamily'),
            'letterSpacing': style.get('letterSpacing'),
            'lineHeightPx': style.get('lineHeightPx'),
        })

    if 'children' in node:
        for child in node['children']:
            extract_text_styles(child, results)

    return results

# 查找Node 178:7
frame_178_7 = search_in_document(data.get('document', {}))

if frame_178_7:
    styles = extract_text_styles(frame_178_7)
    print(f"找到 {len(styles)} 个TEXT节点:\n")
    for s in styles:
        print(f"ID: {s['id']:10s} | {s['name']:30s} | "
              f"Font: {s['fontSize']:3.0f}px {s['fontFamily']:20s} | "
              f"Weight: {s['fontWeight']:3.0f} | "
              f"Spacing: {s['letterSpacing']:5.1f} | "
              f"LineH: {s['lineHeightPx']:5.1f}")
else:
    print("未找到Node 178:7")
