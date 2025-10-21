"""
增强版批量替换API使用示例

演示如何使用批量替换和导出API的各种功能
"""

import asyncio
import httpx
from typing import Dict, Any


API_BASE_URL = "http://localhost:8000/api/v1/batch"


async def example_1_basic_replace():
    """示例1：基本批量替换"""
    print("\n=== 示例1：基本批量替换 ===")

    payload = {
        "figma_file_id": "your_figma_file_id_here",
        "replacement_rules": [
            {
                "target_node_path": "dish-001",
                "image_url": "https://example.com/images/dish-001.jpg",
            },
            {
                "target_node_path": "dish-002",
                "image_url": "https://example.com/images/dish-002.jpg",
            },
        ],
        "export_config": {"format": "png", "scale": 1.0},
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE_URL}/replace-and-export", json=payload, timeout=60.0
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✓ 任务ID: {result['task_id']}")
            print(f"✓ 状态: {result['status']}")
            print(f"✓ 成功替换: {result['successful_replacements']}/{result['total_replacements']}")
            print(f"✓ 导出文件数: {len(result['exported_files'])}")
        else:
            print(f"✗ 请求失败: {response.status_code}")
            print(response.text)


async def example_2_pattern_matching():
    """示例2：使用模式匹配"""
    print("\n=== 示例2：使用模式匹配 ===")

    payload = {
        "figma_file_id": "your_figma_file_id_here",
        "replacement_rules": [
            {
                "target_node_path": "dish-*",  # 匹配所有以dish-开头的节点
                "image_url": "https://example.com/images/dish-default.jpg",
            },
            {
                "target_node_path": "drink-*",  # 匹配所有以drink-开头的节点
                "image_url": "https://example.com/images/drink-default.jpg",
            },
        ],
        "export_config": {"format": "png", "scale": 2.0},
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE_URL}/replace-and-export", json=payload, timeout=60.0
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✓ 匹配到 {result['total_replacements']} 个节点")
            print(f"✓ 处理时间: {result['processing_time']:.2f}秒")
        else:
            print(f"✗ 请求失败: {response.status_code}")


async def example_3_multi_resolution():
    """示例3：多分辨率导出"""
    print("\n=== 示例3：多分辨率导出 ===")

    payload = {
        "figma_file_id": "your_figma_file_id_here",
        "replacement_rules": [
            {
                "target_node_path": "dish-001",
                "image_url": "https://example.com/images/dish-001.jpg",
            }
        ],
        "export_config": {
            "format": "png",
            "scales": [1.0, 2.0, 3.0],  # 导出三种分辨率
        },
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE_URL}/replace-and-export", json=payload, timeout=60.0
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✓ 导出了 {len(result['exported_files'])} 个文件:")

            for file in result["exported_files"]:
                print(
                    f"  - {file['filename']} ({file['scale']}x, {file['size_bytes']} bytes)"
                )
        else:
            print(f"✗ 请求失败: {response.status_code}")


async def example_4_cloud_upload():
    """示例4：云盘上传"""
    print("\n=== 示例4：云盘上传 ===")

    payload = {
        "figma_file_id": "your_figma_file_id_here",
        "replacement_rules": [
            {
                "target_node_path": "dish-*",
                "image_url": "https://example.com/images/dish.jpg",
            }
        ],
        "export_config": {
            "format": "png",
            "scale": 2.0,
            "save_to_cloud": True,
            "cloud_dir": "/projects/restaurant-menu/2025-09",
        },
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE_URL}/replace-and-export", json=payload, timeout=60.0
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✓ 上传到云盘:")

            for file in result["exported_files"]:
                if file.get("cloud_url"):
                    print(f"  - {file['filename']}: {file['cloud_url']}")
        else:
            print(f"✗ 请求失败: {response.status_code}")


async def example_5_validate_rules():
    """示例5：验证替换规则"""
    print("\n=== 示例5：验证替换规则 ===")

    payload = {
        "figma_file_id": "your_figma_file_id_here",
        "target_patterns": ["dish-*", "drink-*", "dessert-*"],
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE_URL}/validate-rules", json=payload, timeout=30.0
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✓ 文件中共有 {result['total_nodes']} 个节点")
            print(f"✓ 匹配结果:")

            for match in result["match_results"]:
                print(f"\n  模式: {match['pattern']}")
                print(f"  匹配数量: {match['count']}")
                if match["matched_nodes"]:
                    print(f"  匹配节点: {', '.join(match['matched_nodes'][:5])}")
                    if len(match["matched_nodes"]) > 5:
                        print(f"            ... 还有 {len(match['matched_nodes']) - 5} 个")
        else:
            print(f"✗ 请求失败: {response.status_code}")


async def example_6_query_task_status():
    """示例6：查询任务状态"""
    print("\n=== 示例6：查询任务状态 ===")

    # 首先创建一个任务
    create_payload = {
        "figma_file_id": "your_figma_file_id_here",
        "replacement_rules": [
            {
                "target_node_path": "dish-001",
                "image_url": "https://example.com/images/dish-001.jpg",
            }
        ],
        "export_config": {"format": "png", "scale": 1.0},
    }

    async with httpx.AsyncClient() as client:
        # 创建任务
        create_response = await client.post(
            f"{API_BASE_URL}/replace-and-export", json=create_payload, timeout=60.0
        )

        if create_response.status_code == 200:
            task_id = create_response.json()["task_id"]
            print(f"✓ 创建任务: {task_id}")

            # 查询任务状态
            status_response = await client.get(f"{API_BASE_URL}/task/{task_id}")

            if status_response.status_code == 200:
                status = status_response.json()
                print(f"✓ 状态: {status['status']}")
                print(f"✓ 进度: {status['progress']:.1f}%")
                print(f"✓ 当前步骤: {status['current_step']}")
            else:
                print(f"✗ 查询失败: {status_response.status_code}")
        else:
            print(f"✗ 创建任务失败: {create_response.status_code}")


async def example_7_list_tasks():
    """示例7：列出所有任务"""
    print("\n=== 示例7：列出所有任务 ===")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_BASE_URL}/tasks", params={"limit": 5, "offset": 0}
        )

        if response.status_code == 200:
            tasks = response.json()
            print(f"✓ 找到 {len(tasks)} 个任务:")

            for task in tasks:
                print(f"\n  任务ID: {task['task_id']}")
                print(f"  状态: {task['status']}")
                print(f"  成功: {task['successful_replacements']}/{task['total_replacements']}")
                print(f"  处理时间: {task['processing_time']:.2f}秒")
        else:
            print(f"✗ 请求失败: {response.status_code}")


async def main():
    """运行所有示例"""
    print("=" * 60)
    print("增强版批量替换API使用示例")
    print("=" * 60)

    try:
        # 运行各个示例
        # 注意：需要替换实际的Figma文件ID和图片URL
        print("\n提示：请在代码中替换实际的Figma文件ID和图片URL")
        print("\n以下是各个示例的功能演示：")

        # await example_1_basic_replace()
        # await example_2_pattern_matching()
        # await example_3_multi_resolution()
        # await example_4_cloud_upload()
        await example_5_validate_rules()
        # await example_6_query_task_status()
        # await example_7_list_tasks()

    except httpx.ConnectError:
        print("\n✗ 无法连接到API服务器")
        print("  请确保API服务器已启动: python -m uvicorn app.main:app --reload --port 8000")
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")


if __name__ == "__main__":
    asyncio.run(main())