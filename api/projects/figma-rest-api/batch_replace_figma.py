"""
执行Figma批量替换任务
"""
import json
import requests
import time
import os

# 禁用代理以访问本地API
os.environ['NO_PROXY'] = 'localhost,127.0.0.1'

# API基础URL
API_BASE_URL = "http://localhost:8001/api/v1"

# Figma文件信息
FIGMA_FILE_KEY = "1u2yKbDBwJfmFagH6ym9p8"

# 读取选择的URL
with open('selected_urls.json', 'r', encoding='utf-8') as f:
    selected_urls = json.load(f)

print("=" * 80)
print("Figma批量替换任务")
print("=" * 80)
print(f"\nFigma文件: {FIGMA_FILE_KEY}")
print(f"选择的图片数量: {len(selected_urls)}")

# 步骤1: 获取Figma文件信息
print("\n[步骤1] 获取Figma文件信息...")
try:
    response = requests.get(f"{API_BASE_URL}/files/{FIGMA_FILE_KEY}")
    if response.status_code == 200:
        file_data = response.json()
        print(f"✓ 文件名称: {file_data.get('name', 'Unknown')}")
        print(f"✓ 最后修改: {file_data.get('lastModified', 'Unknown')}")

        # 遍历找到所有图片节点
        def find_image_nodes(node, path=""):
            nodes = []
            current_path = f"{path}/{node.get('name', 'unnamed')}"

            # 检查是否是图片节点（RECTANGLE with fills）
            if node.get('type') == 'RECTANGLE':
                fills = node.get('fills', [])
                for fill in fills:
                    if fill.get('type') == 'IMAGE':
                        nodes.append({
                            'id': node.get('id'),
                            'name': node.get('name'),
                            'path': current_path
                        })
                        break

            # 递归搜索子节点
            children = node.get('children', [])
            for child in children:
                nodes.extend(find_image_nodes(child, current_path))

            return nodes

        # 从document开始搜索
        image_nodes = []
        document = file_data.get('document', {})
        image_nodes = find_image_nodes(document)

        print(f"✓ 找到 {len(image_nodes)} 个图片节点:")
        for i, node in enumerate(image_nodes[:10], 1):  # 只显示前10个
            print(f"  {i}. [{node['id']}] {node['name']}")
            print(f"     路径: {node['path']}")

        if len(image_nodes) > 10:
            print(f"  ... 还有 {len(image_nodes) - 10} 个节点")

    else:
        print(f"✗ 获取文件信息失败: {response.status_code}")
        print(f"  错误: {response.text}")
        exit(1)

except Exception as e:
    print(f"✗ 请求失败: {e}")
    exit(1)

# 步骤2: 准备替换配置
print("\n[步骤2] 准备批量替换配置...")

# 如果图片节点数量少于6个，使用所有节点；否则选择前6个
nodes_to_replace = image_nodes[:min(len(image_nodes), len(selected_urls))]

replacement_rules = []
for i, (node, url_info) in enumerate(zip(nodes_to_replace, selected_urls)):
    replacement_rules.append({
        "target_node_path": node['id'],  # 使用节点ID
        "image_url": url_info['url']
    })
    print(f"  {i+1}. 节点 [{node['name']}] <- {url_info['source_file']}/{url_info['filename']}")

# 步骤3: 执行批量替换和导出
print("\n[步骤3] 执行批量替换和导出...")

batch_request = {
    "figma_file_id": FIGMA_FILE_KEY,
    "replacement_rules": replacement_rules,
    "export_config": {
        "format": "png",
        "scales": [1.0, 2.0],
        "save_to_cloud": True,
        "cloud_dir": "/output/figma-batch-replace/" + time.strftime("%Y%m%d_%H%M%S")
    }
}

print(f"\n请求配置:")
print(json.dumps(batch_request, ensure_ascii=False, indent=2))

# 发送批量替换请求
try:
    response = requests.post(
        f"{API_BASE_URL}/batch/replace-and-export",
        json=batch_request,
        timeout=300  # 5分钟超时
    )

    if response.status_code == 200:
        result = response.json()
        print("\n✓ 批量替换任务已创建!")
        print(f"  任务ID: {result.get('task_id', 'unknown')}")
        print(f"  状态: {result.get('status', 'unknown')}")

        if 'export_urls' in result:
            print(f"\n导出的文件 ({len(result['export_urls'])}):")
            for i, url in enumerate(result['export_urls'], 1):
                print(f"  {i}. {url}")

        # 保存结果
        with open('batch_replace_result.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n结果已保存到: batch_replace_result.json")

    else:
        print(f"\n✗ 批量替换失败: {response.status_code}")
        print(f"  错误: {response.text}")

except requests.exceptions.Timeout:
    print("\n✗ 请求超时（5分钟）")
except Exception as e:
    print(f"\n✗ 请求失败: {e}")

print("\n" + "=" * 80)