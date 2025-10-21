"""
验证三日游攻略页面坐标精度
对比Figma原始数据和CSS实现,输出差异报告
"""
import json
import re

# Figma Frame偏移量
FRAME_X = 17.0
FRAME_Y = 12971.0

# 读取Figma原始数据
with open('library/figma-informations/1u2yKbDBwJfmFagH6ym9p8_three-day-tour_raw.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def find_node(obj, target_id):
    """递归查找节点"""
    if isinstance(obj, dict):
        if obj.get('id') == target_id:
            return obj
        for value in obj.values():
            result = find_node(value, target_id)
            if result:
                return result
    elif isinstance(obj, list):
        for item in obj:
            result = find_node(item, target_id)
            if result:
                return result
    return None

# 读取CSS文件
with open('project/src/app/three-day-tour/three-day-tour.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

def extract_css_position(selector):
    """从CSS中提取位置信息"""
    pattern = rf'\.{re.escape(selector)}\s*\{{[^}}]*left:\s*(\d+)px;[^}}]*top:\s*(\d+)px;'
    match = re.search(pattern, css_content)
    if match:
        return float(match.group(1)), float(match.group(2))
    return None, None

# 验证元素
elements = [
    # 标题元素
    ('164:45', 'city-title', '成都'),
    ('164:46', 'main-title', '三日游攻略'),
    ('164:51', 'subtitle-container', '副标题容器'),
    ('164:54', 'day-label.day1', 'DAY1'),
    ('164:56', 'day-label.day2', 'DAY2'),
    ('164:58', 'day-label.day3', 'DAY3'),

    # DAY1卡片
    ('164:61', 'card-day1-1', '太古里'),
    ('165:21', 'card-day1-2', 'IFS'),
    ('165:28', 'card-day1-3', '大慈寺'),
    ('165:35', 'card-day1-4', '望平街'),

    # DAY2卡片
    ('179:32', 'card-day2-1', '自然博物馆'),
    ('179:33', 'card-day2-2', '东郊记忆'),
    ('179:34', 'card-day2-3', '建设路'),
    ('179:35', 'card-day2-4', '玉林路'),

    # DAY3卡片
    ('179:51', 'card-day3-1', '大熊猫基地'),
    ('179:52', 'card-day3-2', '武侯祠'),
    ('179:53', 'card-day3-3', '锦里'),
    ('179:54', 'card-day3-4', '杜甫草堂'),
]

print('='*80)
print('三日游攻略页面坐标验证报告')
print('='*80)
print()

total_errors = 0
max_error_x = 0
max_error_y = 0

for node_id, css_class, name in elements:
    node = find_node(data, node_id)
    if not node:
        print(f'❌ {name} (节点{node_id}未找到)')
        total_errors += 1
        continue

    bbox = node.get('absoluteBoundingBox', {})
    figma_abs_x = bbox.get('x', 0)
    figma_abs_y = bbox.get('y', 0)
    figma_rel_x = figma_abs_x - FRAME_X
    figma_rel_y = figma_abs_y - FRAME_Y

    # 提取CSS位置
    css_x, css_y = extract_css_position(css_class)

    if css_x is None:
        print(f'⚠️  {name} - CSS类名未找到: {css_class}')
        total_errors += 1
        continue

    # 计算误差
    error_x = abs(css_x - figma_rel_x)
    error_y = abs(css_y - figma_rel_y)
    max_error_x = max(max_error_x, error_x)
    max_error_y = max(max_error_y, error_y)

    if error_x > 0.5 or error_y > 0.5:
        print(f'❌ {name} ({node_id})')
        print(f'   Figma相对: ({figma_rel_x}, {figma_rel_y})')
        print(f'   CSS实际:   ({css_x}, {css_y})')
        print(f'   误差:      X={error_x}px, Y={error_y}px')
        print()
        total_errors += 1
    else:
        print(f'✅ {name} - 精确匹配 (误差<0.5px)')

print()
print('='*80)
print('验证总结:')
print(f'总元素数: {len(elements)}')
print(f'错误数量: {total_errors}')
print(f'最大X误差: {max_error_x}px')
print(f'最大Y误差: {max_error_y}px')

if total_errors == 0:
    print('✅ 坐标100%精确匹配Figma设计!')
else:
    print(f'⚠️  发现{total_errors}个坐标误差')
print('='*80)
