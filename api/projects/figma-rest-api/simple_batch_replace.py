"""
简化版Figma批量替换 - 直接调用批量替换API
"""
import json
import requests
import os

# 禁用代理
os.environ['NO_PROXY'] = 'localhost,127.0.0.1'

# 读取选择的URL
with open('selected_urls.json', 'r', encoding='utf-8') as f:
    selected_urls = json.load(f)

print("=" * 80)
print("Figma批量替换任务 (简化版)")
print("=" * 80)
print(f"\n选择的图片数量: {len(selected_urls)}")
for i, url_info in enumerate(selected_urls, 1):
    print(f"  {i}. [{url_info['source_file']}] {url_info['filename']}")

# 构建替换规则 - 使用通配符模式
# 假设Figma文件中的图片节点命名为 image-1, image-2, image-3...
replacement_rules = []
for i, url_info in enumerate(selected_urls, 1):
    replacement_rules.append({
        "target_node_path": f"image-{i}",  # 或使用通配符 "image-*"
        "image_url": url_info['url']
    })

# 批量替换请求
batch_request = {
    "figma_file_id": "1u2yKbDBwJfmFagH6ym9p8",
    "replacement_rules": replacement_rules,
    "export_config": {
        "format": "png",
        "scales": [1.0, 2.0],
        "save_to_cloud": False,  # 先不上传到云盘，本地测试
        "cloud_dir": None
    }
}

print("\n" + "=" * 80)
print("替换配置:")
print("=" * 80)
print(json.dumps(batch_request, ensure_ascii=False, indent=2))

print("\n" + "=" * 80)
print("发送批量替换请求...")
print("=" * 80)

try:
    response = requests.post(
        "http://localhost:8001/api/v1/batch/replace-and-export",
        json=batch_request,
        timeout=300
    )

    print(f"\nHTTP状态码: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print("\n✓ 批量替换任务已创建!")
        print(json.dumps(result, ensure_ascii=False, indent=2))

        # 保存结果
        with open('batch_replace_result.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n结果已保存到: batch_replace_result.json")

    else:
        print(f"\n✗ 批量替换失败")
        print(f"响应内容: {response.text}")

except Exception as e:
    print(f"\n✗ 请求失败: {e}")

print("\n" + "=" * 80)
