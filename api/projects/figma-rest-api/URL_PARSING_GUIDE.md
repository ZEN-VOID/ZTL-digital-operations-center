# Figma URL 自动解析功能指南

> 🎉 现在您只需要提供Figma URL，系统会自动提取所有必要的参数！

## 🎯 新功能概述

我们已经为您的Figma REST API服务添加了**智能URL解析功能**，现在您可以：

- ✅ **直接使用Figma URL** 而不需要手动提取file_key
- ✅ **自动提取node_id** 从URL中的node-id参数
- ✅ **支持多种URL格式** (file、proto、design等)
- ✅ **批量URL处理** 一次解析多个URL
- ✅ **参数验证** 自动验证URL格式和参数

## 🚀 使用方式对比

### **之前的方式** (仍然支持)
```json
{
  "file_key": "ABC123DEF456",
  "replacements": [
    {
      "node_id": "1:23",
      "image_url": "https://example.com/image1.jpg"
    }
  ]
}
```

### **现在的方式** (新增)
```json
{
  "figma_url": "https://www.figma.com/file/ABC123DEF456/Restaurant-Menu?node-id=1%3A23",
  "replacements": [
    {
      "figma_url": "https://www.figma.com/file/ABC123DEF456/Restaurant-Menu?node-id=1%3A23",
      "image_url": "https://example.com/image1.jpg"
    }
  ]
}
```

## 📋 支持的URL格式

### 1. **基本文件URL**
```
https://www.figma.com/file/ABC123DEF456/Restaurant-Menu-Design
```
**提取结果**:
- `file_key`: ABC123DEF456
- `file_name`: Restaurant-Menu-Design

### 2. **包含节点ID的URL**
```
https://www.figma.com/file/ABC123DEF456/Restaurant-Menu-Design?node-id=1%3A23
```
**提取结果**:
- `file_key`: ABC123DEF456
- `node_id`: 1:23

### 3. **原型URL**
```
https://www.figma.com/proto/ABC123DEF456/Restaurant-Menu-Design?node-id=1%3A23
```
**提取结果**:
- `file_key`: ABC123DEF456
- `node_id`: 1:23
- `url_type`: prototype

### 4. **设计URL**
```
https://www.figma.com/design/ABC123DEF456/Restaurant-Menu-Design?node-id=1%3A23
```

### 5. **多个节点ID**
```
https://www.figma.com/file/ABC123DEF456/Restaurant-Menu?node-ids=1%3A23,1%3A24,1%3A25
```
**提取结果**:
- `node_ids`: ["1:23", "1:24", "1:25"]

## 🔧 新增的API端点

### 1. **URL解析工具**

#### 解析单个URL
```http
POST /api/v1/url-parser/parse
Content-Type: application/json

{
  "url": "https://www.figma.com/file/ABC123DEF456/Restaurant-Menu?node-id=1%3A23"
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "file_key": "ABC123DEF456",
    "file_name": "Restaurant-Menu",
    "node_id": "1:23",
    "url_type": "file",
    "original_url": "https://www.figma.com/file/ABC123DEF456/Restaurant-Menu?node-id=1%3A23"
  },
  "api_params": {
    "file_key": "ABC123DEF456",
    "node_id": "1:23",
    "ids": "1:23"
  }
}
```

#### 快速提取File Key
```http
GET /api/v1/url-parser/extract-file-key?url=https://www.figma.com/file/ABC123DEF456/Restaurant-Menu
```

**响应**:
```json
{
  "url": "https://www.figma.com/file/ABC123DEF456/Restaurant-Menu",
  "file_key": "ABC123DEF456"
}
```

#### 验证URL格式
```http
GET /api/v1/url-parser/validate?url=https://www.figma.com/file/ABC123DEF456/Restaurant-Menu
```

#### 获取URL示例
```http
GET /api/v1/url-parser/examples
```

### 2. **更新的批量替换API**

现在支持两种方式：

#### 方式1: 使用URL (推荐)
```http
POST /api/v1/batch-replace/
Content-Type: application/json

{
  "figma_url": "https://www.figma.com/file/ABC123DEF456/Restaurant-Menu",
  "replacements": [
    {
      "figma_url": "https://www.figma.com/file/ABC123DEF456/Restaurant-Menu?node-id=1%3A23",
      "image_url": "https://example.com/dish1.jpg",
      "image_name": "宫保鸡丁"
    },
    {
      "figma_url": "https://www.figma.com/file/ABC123DEF456/Restaurant-Menu?node-id=1%3A24",
      "image_url": "https://example.com/dish2.jpg",
      "image_name": "麻婆豆腐"
    }
  ],
  "batch_name": "春季菜单更新",
  "auto_export": true,
  "export_format": "png"
}
```

#### 方式2: 传统方式 (仍然支持)
```http
POST /api/v1/batch-replace/
Content-Type: application/json

{
  "file_key": "ABC123DEF456",
  "replacements": [
    {
      "node_id": "1:23",
      "image_url": "https://example.com/dish1.jpg"
    }
  ]
}
```

## 🎯 实际使用场景

### **场景1: 餐厅菜单批量更新**

1. **在Figma中选择要更新的菜品图片**
2. **复制URL** (包含node-id)
3. **直接使用URL调用API**:

```javascript
const updateMenu = async () => {
  const response = await fetch('/api/v1/batch-replace/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      figma_url: "https://www.figma.com/file/ABC123DEF456/春季菜单",
      replacements: [
        {
          figma_url: "https://www.figma.com/file/ABC123DEF456/春季菜单?node-id=1%3A23",
          image_url: "https://restaurant.com/images/new-dish1.jpg",
          image_name: "春季特色菜"
        }
      ],
      batch_name: "春季菜单更新",
      auto_export: true
    })
  });
  
  const result = await response.json();
  console.log('更新任务ID:', result.task_id);
};
```

### **场景2: 量产工作流**

```javascript
const createProductionWorkflow = async () => {
  const response = await fetch('/api/v1/production/workflow', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      figma_url: "https://www.figma.com/file/ABC123DEF456/促销海报模板",
      template_frame_url: "https://www.figma.com/file/ABC123DEF456/促销海报模板?node-id=1%3A1",
      image_urls: [
        "https://example.com/product1.jpg",
        "https://example.com/product2.jpg",
        "https://example.com/product3.jpg",
        "https://example.com/product4.jpg",
        "https://example.com/product5.jpg",
        "https://example.com/product6.jpg"
      ],
      target_node_urls: [
        "https://www.figma.com/file/ABC123DEF456/促销海报模板?node-id=1%3A23",
        "https://www.figma.com/file/ABC123DEF456/促销海报模板?node-id=1%3A24",
        "https://www.figma.com/file/ABC123DEF456/促销海报模板?node-id=1%3A25",
        "https://www.figma.com/file/ABC123DEF456/促销海报模板?node-id=1%3A26",
        "https://www.figma.com/file/ABC123DEF456/促销海报模板?node-id=1%3A27",
        "https://www.figma.com/file/ABC123DEF456/促销海报模板?node-id=1%3A28"
      ],
      batch_size: 6,
      workflow_name: "春季促销海报量产"
    })
  });
};
```

## 💡 使用建议

### **最佳实践**:
1. **优先使用URL方式** - 更直观，减少错误
2. **从Figma直接复制URL** - 确保参数正确
3. **使用URL验证端点** - 在批量操作前验证URL
4. **混合使用** - 可以在同一请求中混合使用URL和传统参数

### **注意事项**:
- URL中的`%3A`会自动解码为`:`
- 支持所有Figma URL类型 (file、proto、design等)
- 如果同时提供URL和传统参数，传统参数优先
- URL解析失败会返回详细错误信息

## 🎉 总结

现在您可以：

✅ **直接粘贴Figma URL** - 无需手动提取参数  
✅ **自动参数提取** - file_key和node_id自动识别  
✅ **支持所有URL格式** - file、proto、design等  
✅ **批量URL处理** - 一次处理多个URL  
✅ **向后兼容** - 原有的参数方式仍然支持  

**这大大简化了API的使用，让您专注于业务逻辑而不是参数提取！** 🚀
