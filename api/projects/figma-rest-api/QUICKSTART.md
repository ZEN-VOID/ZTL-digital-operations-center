# 快速开始指南

## 🚀 5分钟快速上手增强版批量替换API

### 前置要求

1. Python 3.11+
2. 有效的Figma API Token
3. 一个Figma文件用于测试

### 步骤1: 启动API服务

```bash
# 进入项目目录
cd api/projects/figma-rest-api

# 安装依赖（如果还没安装）
pip install -r requirements.txt

# 启动服务
python -m uvicorn app.main:app --reload --port 8000
```

服务启动后，访问 http://localhost:8000/docs 查看API文档。

### 步骤2: 验证服务运行

打开浏览器访问：http://localhost:8000/docs

你应该能看到Swagger UI界面，其中包含 `/api/v1/batch` 下的所有端点。

### 步骤3: 准备测试数据

你需要：
1. **Figma文件ID**: 从Figma文件URL中获取
   - URL格式: `https://www.figma.com/file/{FILE_ID}/...`
2. **节点ID或匹配模式**: 要替换的节点标识
3. **图片URL**: 用于替换的图片地址

### 步骤4: 第一次API调用

#### 使用cURL

```bash
curl -X POST "http://localhost:8000/api/v1/batch/replace-and-export" \
  -H "Content-Type: application/json" \
  -d '{
    "figma_file_id": "YOUR_FILE_ID",
    "replacement_rules": [
      {
        "target_node_path": "dish-001",
        "image_url": "https://example.com/images/dish.jpg"
      }
    ],
    "export_config": {
      "format": "png",
      "scale": 1.0
    }
  }'
```

#### 使用Python

```python
import httpx
import asyncio

async def test_api():
    url = "http://localhost:8000/api/v1/batch/replace-and-export"

    payload = {
        "figma_file_id": "YOUR_FILE_ID",
        "replacement_rules": [
            {
                "target_node_path": "dish-001",
                "image_url": "https://example.com/images/dish.jpg"
            }
        ],
        "export_config": {
            "format": "png",
            "scale": 1.0
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, timeout=60.0)
        result = response.json()
        print(f"任务ID: {result['task_id']}")
        print(f"状态: {result['status']}")

asyncio.run(test_api())
```

#### 使用Swagger UI

1. 访问 http://localhost:8000/docs
2. 找到 `POST /api/v1/batch/replace-and-export` 端点
3. 点击 "Try it out"
4. 填写请求体
5. 点击 "Execute"

### 步骤5: 验证替换规则（推荐）

在实际替换之前，先验证你的匹配规则：

```bash
curl -X POST "http://localhost:8000/api/v1/batch/validate-rules" \
  -H "Content-Type: application/json" \
  -d '{
    "figma_file_id": "YOUR_FILE_ID",
    "target_patterns": ["dish-*", "drink-*"]
  }'
```

这会返回匹配到的节点列表，确保你的规则正确。

## 🎯 常用场景示例

### 场景1: 替换单个节点

```json
{
  "figma_file_id": "abc123",
  "replacement_rules": [
    {
      "target_node_path": "dish-001",
      "image_url": "https://example.com/dish-001.jpg"
    }
  ],
  "export_config": {
    "format": "png",
    "scale": 1.0
  }
}
```

### 场景2: 批量替换（模式匹配）

```json
{
  "figma_file_id": "abc123",
  "replacement_rules": [
    {
      "target_node_path": "dish-*",
      "image_url": "https://example.com/default-dish.jpg"
    }
  ],
  "export_config": {
    "format": "png",
    "scale": 2.0
  }
}
```

### 场景3: 多分辨率导出

```json
{
  "figma_file_id": "abc123",
  "replacement_rules": [
    {
      "target_node_path": "dish-001",
      "image_url": "https://example.com/dish.jpg"
    }
  ],
  "export_config": {
    "format": "png",
    "scales": [1.0, 2.0, 3.0]
  }
}
```

### 场景4: 云盘上传

```json
{
  "figma_file_id": "abc123",
  "replacement_rules": [
    {
      "target_node_path": "dish-*",
      "image_url": "https://example.com/dish.jpg"
    }
  ],
  "export_config": {
    "format": "png",
    "scale": 2.0,
    "save_to_cloud": true,
    "cloud_dir": "/projects/menu/2025-09"
  }
}
```

## 📖 理解响应

成功的响应示例：

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
      "local_path": "./exports/abc123/20250930_120000/dish-001_1.0x.png",
      "cloud_url": null,
      "format": "png",
      "scale": 1.0,
      "size_bytes": 524288,
      "node_id": "dish-001"
    }
  ],
  "processing_time": 15.32
}
```

## 🔧 常见问题

### Q1: 启动失败，提示"Figma API token is required"

**解决**: 确保`.env`文件中配置了`FIGMA_API_TOKEN`

```env
FIGMA_API_TOKEN=your_token_here
```

### Q2: 请求返回404 "File not found"

**原因**:
1. Figma文件ID错误
2. API Token没有访问该文件的权限

**解决**:
1. 检查文件ID是否正确
2. 确保你的Token有该文件的访问权限

### Q3: 模式没有匹配到任何节点

**解决**: 使用`/validate-rules`端点验证：

```bash
curl -X POST "http://localhost:8000/api/v1/batch/validate-rules" \
  -H "Content-Type: application/json" \
  -d '{
    "figma_file_id": "YOUR_FILE_ID",
    "target_patterns": ["your-pattern"]
  }'
```

### Q4: 导出的文件在哪里？

**位置**: `./exports/{file_id}/{timestamp}/`

例如: `./exports/abc123/20250930_120000/dish-001_1.0x.png`

### Q5: 如何查看任务进度？

使用任务ID查询：

```bash
curl "http://localhost:8000/api/v1/batch/task/{task_id}"
```

## 📚 下一步

1. 查看[完整API指南](./BATCH_API_GUIDE.md)了解所有功能
2. 查看[实现总结](./IMPLEMENTATION_SUMMARY.md)了解技术细节
3. 运行[使用示例](./examples/batch_replace_example.py)学习更多用法
4. 浏览[Swagger文档](http://localhost:8000/docs)查看所有端点

## 💡 提示

- 在生产环境中使用前，先在测试文件上验证功能
- 使用`validate-rules`端点预览匹配结果
- 大批量操作时注意API速率限制
- 定期清理导出目录避免占用过多磁盘空间

## 🆘 获取帮助

- 查看Swagger文档: http://localhost:8000/docs
- 查看ReDoc文档: http://localhost:8000/redoc
- 提交Issue: [GitHub Issues](https://github.com/ZEN-VOID/ZTL-Restaurant-Digital-Design/issues)

---

祝使用愉快！ 🎉