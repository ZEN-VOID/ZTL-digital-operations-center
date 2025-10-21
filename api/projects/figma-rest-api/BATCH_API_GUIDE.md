# 增强版批量处理API指南

## 📋 概述

增强版批量处理API提供了强大的图片替换和导出功能，支持节点模式匹配、多分辨率导出和云盘集成。

## 🎯 核心功能

### 1. 节点模式匹配

支持使用通配符匹配多个节点，无需手动指定每个节点ID。

**支持的模式**：
- `*` - 匹配任意多个字符
- `?` - 匹配单个字符

**示例**：
- `dish-*` - 匹配所有以"dish-"开头的节点
- `*-photo` - 匹配所有以"-photo"结尾的节点
- `dish-?-small` - 匹配"dish-1-small"、"dish-a-small"等

### 2. 多分辨率导出

一次性导出多种分辨率的图片，满足不同显示设备的需求。

**支持的缩放比例**：1.0 - 4.0

**常用配置**：
- Web显示：`[1.0, 2.0]`
- 移动端：`[1.0, 2.0, 3.0]`
- 印刷品：`[2.0, 3.0, 4.0]`

### 3. 云盘集成

自动上传导出的文件到云存储，方便团队协作和资源管理。

**支持的操作**：
- 自动上传到指定目录
- 保留本地副本
- 返回云盘URL

## 🚀 API端点

### POST /api/v1/batch/replace-and-export

批量替换图片并导出处理后的设计稿。

**请求体**：

```json
{
  "figma_file_id": "string",
  "replacement_rules": [
    {
      "target_node_path": "string",
      "image_url": "string"
    }
  ],
  "export_config": {
    "format": "png",
    "scale": 1.0,
    "scales": [1.0, 2.0, 3.0],
    "save_to_cloud": false,
    "cloud_dir": null,
    "svg_outline_text": true,
    "svg_include_id": false,
    "svg_include_node_id": false,
    "svg_simplify_stroke": true,
    "contents_only": true,
    "use_absolute_bounds": false
  }
}
```

**响应**：

```json
{
  "success": true,
  "message": "Completed successfully",
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "total_replacements": 12,
  "successful_replacements": 12,
  "failed_replacements": 0,
  "exported_files": [
    {
      "filename": "dish-001_1.0x.png",
      "local_path": "./exports/file123/20250930_120000/dish-001_1.0x.png",
      "cloud_url": "https://cloud.example.com/path/to/dish-001_1.0x.png",
      "format": "png",
      "scale": 1.0,
      "size_bytes": 524288,
      "node_id": "dish-001"
    }
  ],
  "processing_time": 15.32,
  "created_at": "2025-09-30T12:00:00Z",
  "updated_at": "2025-09-30T12:00:15Z",
  "completed_at": "2025-09-30T12:00:15Z",
  "error_message": null,
  "failed_nodes": []
}
```

### GET /api/v1/batch/task/{task_id}

查询批量处理任务的状态和进度。

**响应**：

```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "exporting",
  "progress": 75.0,
  "current_step": "导出设计稿",
  "estimated_time_remaining": 5.2,
  "result": null
}
```

### GET /api/v1/batch/tasks

列出所有批量处理任务。

**查询参数**：
- `status` (optional): 按状态过滤
- `limit` (optional): 每页数量，默认20
- `offset` (optional): 偏移量，默认0

**响应**：

```json
[
  {
    "success": true,
    "message": "Completed successfully",
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "completed",
    "total_replacements": 12,
    "successful_replacements": 12,
    "failed_replacements": 0,
    "exported_files": [],
    "processing_time": 15.32
  }
]
```

### DELETE /api/v1/batch/task/{task_id}

取消正在处理的批量替换任务。

**响应**：

```json
{
  "message": "Task cancelled successfully",
  "task_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### POST /api/v1/batch/validate-rules

验证替换规则并预览匹配的节点。

**请求体**：

```json
{
  "figma_file_id": "your_figma_file_key",
  "target_patterns": ["dish-*", "drink-*", "dessert-*"]
}
```

**响应**：

```json
{
  "file_id": "your_figma_file_key",
  "total_nodes": 50,
  "match_results": [
    {
      "pattern": "dish-*",
      "matched_nodes": ["dish-001", "dish-002", "dish-003"],
      "count": 3
    },
    {
      "pattern": "drink-*",
      "matched_nodes": ["drink-001", "drink-002"],
      "count": 2
    }
  ]
}
```

## 📝 使用示例

### 示例1：基本批量替换

替换所有以"dish-"开头的节点，并导出为PNG格式。

```python
import httpx

async def basic_batch_replace():
    url = "http://localhost:8000/api/v1/batch/replace-and-export"

    payload = {
        "figma_file_id": "abc123def456",
        "replacement_rules": [
            {
                "target_node_path": "dish-*",
                "image_url": "https://example.com/images/dish-main.jpg"
            }
        ],
        "export_config": {
            "format": "png",
            "scale": 1.0
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        result = response.json()
        print(f"Task ID: {result['task_id']}")
        print(f"Status: {result['status']}")
```

### 示例2：多分辨率导出

导出1x、2x、3x三种分辨率的图片。

```python
async def multi_resolution_export():
    url = "http://localhost:8000/api/v1/batch/replace-and-export"

    payload = {
        "figma_file_id": "abc123def456",
        "replacement_rules": [
            {
                "target_node_path": "dish-001",
                "image_url": "https://example.com/images/dish-001.jpg"
            },
            {
                "target_node_path": "dish-002",
                "image_url": "https://example.com/images/dish-002.jpg"
            }
        ],
        "export_config": {
            "format": "png",
            "scales": [1.0, 2.0, 3.0]  # 导出三种分辨率
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        result = response.json()

        # 每个节点会生成3个文件（1x, 2x, 3x）
        print(f"Total files: {len(result['exported_files'])}")
```

### 示例3：云盘集成

替换并上传到云盘。

```python
async def cloud_upload_example():
    url = "http://localhost:8000/api/v1/batch/replace-and-export"

    payload = {
        "figma_file_id": "abc123def456",
        "replacement_rules": [
            {
                "target_node_path": "dish-*",
                "image_url": "https://example.com/images/dish.jpg"
            }
        ],
        "export_config": {
            "format": "png",
            "scale": 2.0,
            "save_to_cloud": True,
            "cloud_dir": "/projects/restaurant-menu/2025-09"
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        result = response.json()

        # 打印云盘URL
        for file in result['exported_files']:
            print(f"Cloud URL: {file['cloud_url']}")
```

### 示例4：验证规则

在执行替换前，先验证匹配规则。

```python
async def validate_rules_example():
    url = "http://localhost:8000/api/v1/batch/validate-rules"

    payload = {
        "figma_file_id": "abc123def456",
        "target_patterns": ["dish-*", "drink-*"]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        result = response.json()

        print(f"Total nodes in file: {result['total_nodes']}")

        for match in result['match_results']:
            print(f"\nPattern: {match['pattern']}")
            print(f"Matched nodes: {match['matched_nodes']}")
            print(f"Count: {match['count']}")
```

### 示例5：查询任务状态

轮询任务状态直到完成。

```python
import asyncio

async def poll_task_status(task_id: str):
    url = f"http://localhost:8000/api/v1/batch/task/{task_id}"

    async with httpx.AsyncClient() as client:
        while True:
            response = await client.get(url)
            status = response.json()

            print(f"Progress: {status['progress']}%")
            print(f"Current step: {status['current_step']}")

            if status['status'] in ['completed', 'failed']:
                print(f"Final status: {status['status']}")
                if status['result']:
                    print(f"Exported {len(status['result']['exported_files'])} files")
                break

            await asyncio.sleep(2)  # 每2秒查询一次
```

## ⚠️ 注意事项

### 性能考虑

1. **批量限制**：单次请求最多50个替换规则
2. **并发控制**：建议控制并发请求数，避免超过API限制
3. **文件大小**：大文件导出可能需要较长时间

### 错误处理

1. **节点不存在**：模式未匹配到任何节点时会记录警告
2. **图片URL无效**：会标记为失败并继续处理其他项
3. **导出失败**：会在`failed_nodes`中记录详细信息

### 最佳实践

1. **先验证规则**：使用`validate-rules`端点预览匹配结果
2. **合理分辨率**：根据实际需求选择分辨率，避免不必要的高分辨率导出
3. **监控任务**：对于大批量操作，建议实时监控任务进度
4. **本地缓存**：即使使用云盘，也会保留本地副本

## 🔧 配置说明

### 环境变量

```env
# Figma API配置
FIGMA_API_TOKEN=your_token_here
FIGMA_API_BASE_URL=https://api.figma.com/v1/
FIGMA_TIMEOUT=30
FIGMA_MAX_RETRIES=3

# 导出目录
APP_EXPORT_DIR=./exports

# 云存储配置（可选）
ENABLE_CLOUD_UPLOAD=true
```

### 导出格式配置

| 格式 | 描述 | 适用场景 |
|------|------|----------|
| PNG | 无损压缩，支持透明 | 图标、UI元素 |
| JPG | 有损压缩，文件小 | 照片、背景图 |
| SVG | 矢量格式 | 图标、Logo |
| PDF | 印刷级质量 | 印刷品、文档 |

## 🐛 故障排查

### 常见问题

**1. 模式未匹配到节点**

- 检查节点名称是否正确
- 确认文件结构
- 使用`validate-rules`端点预览

**2. 导出失败**

- 检查Figma API Token是否有效
- 确认文件访问权限
- 查看`error_message`字段

**3. 云盘上传失败**

- 确认云存储配置
- 检查网络连接
- 验证目录权限

## 📞 支持

如有问题或建议，请：

1. 查看完整API文档：http://localhost:8000/docs
2. 创建Issue：[GitHub Issues](https://github.com/ZEN-VOID/ZTL-Restaurant-Digital-Design/issues)
3. 联系项目维护者

---

**版本**: 1.0.0
**更新日期**: 2025-09-30
**维护者**: ZTL餐饮数智化平面设计团队