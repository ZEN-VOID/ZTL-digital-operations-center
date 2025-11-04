"""
Example: Markdown to PDF Conversion

Demonstrates creating technical documentation using Markdown.
Best for simple, clean documentation with code highlighting.
"""

import sys
from pathlib import Path

# Add skill to path
skill_path = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(skill_path))

from pdf_generator import create_pdf_from_markdown


def create_technical_doc():
    """Create a technical documentation using Markdown."""

    markdown_content = """
# API接口文档

> 火锅江湖 - 外卖订单管理系统 v2.0
>
> 最后更新: 2025-10-21

---

## 概述

本文档描述了火锅江湖外卖订单管理系统的API接口规范。系统提供RESTful API，
支持订单创建、查询、更新和取消等核心功能。

### 基础信息

- **Base URL**: `https://api.hotpotjianghu.com/v2`
- **认证方式**: Bearer Token
- **数据格式**: JSON
- **字符编码**: UTF-8

---

## 认证

所有API请求需要在Header中包含认证令牌：

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### 获取Access Token

```bash
curl -X POST https://api.hotpotjianghu.com/v2/auth/token \\
  -H "Content-Type: application/json" \\
  -d '{
    "app_id": "your_app_id",
    "app_secret": "your_app_secret"
  }'
```

**响应示例:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 7200
}
```

---

## 订单管理

### 1. 创建订单

创建新的外卖订单。

**接口地址**: `POST /orders`

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| user_id | string | 是 | 用户ID |
| restaurant_id | string | 是 | 餐厅ID |
| items | array | 是 | 订单商品列表 |
| delivery_address | object | 是 | 配送地址 |
| payment_method | string | 是 | 支付方式 (wechat/alipay) |

**请求示例**:

```json
{
  "user_id": "user_12345",
  "restaurant_id": "rest_001",
  "items": [
    {
      "dish_id": "dish_101",
      "dish_name": "麻辣牛油锅底",
      "quantity": 1,
      "price": 68.00
    },
    {
      "dish_id": "dish_203",
      "dish_name": "精品肥牛",
      "quantity": 2,
      "price": 58.00
    }
  ],
  "delivery_address": {
    "name": "张三",
    "phone": "13800138000",
    "address": "成都市武侯区天府大道999号A座1001",
    "latitude": 30.5728,
    "longitude": 104.0668
  },
  "payment_method": "wechat"
}
```

**响应示例**:

```json
{
  "code": 200,
  "message": "订单创建成功",
  "data": {
    "order_id": "ORD20251021001",
    "order_no": "20251021145630001",
    "total_amount": 184.00,
    "delivery_fee": 6.00,
    "status": "pending_payment",
    "estimated_delivery_time": "2025-10-21 16:30:00"
  }
}
```

### 2. 查询订单

根据订单ID查询订单详情。

**接口地址**: `GET /orders/{order_id}`

**路径参数**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| order_id | string | 订单ID |

**响应示例**:

```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "order_id": "ORD20251021001",
    "order_no": "20251021145630001",
    "status": "delivering",
    "created_at": "2025-10-21 14:56:30",
    "paid_at": "2025-10-21 14:57:15",
    "items": [...],
    "delivery_info": {
      "rider_name": "李师傅",
      "rider_phone": "13900139000",
      "current_location": {
        "latitude": 30.5720,
        "longitude": 104.0670
      }
    }
  }
}
```

### 3. 取消订单

取消未完成的订单。

**接口地址**: `DELETE /orders/{order_id}`

**注意事项**:

- 只能取消状态为 `pending_payment` 或 `paid` 的订单
- 已配送的订单无法取消
- 取消后会自动退款

---

## 错误码

| 错误码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 401 | 认证失败 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 联系我们

如有技术问题，请联系:

- **技术支持邮箱**: tech@hotpotjianghu.com
- **开发者社群**: https://dev.hotpotjianghu.com
- **工单系统**: https://support.hotpotjianghu.com

---

© 2025 火锅江湖. All rights reserved.
"""

    result = create_pdf_from_markdown(
        markdown_content=markdown_content,
        output_path="output/行政组/技术文档/api-documentation.pdf",
        toc=True,
        number_sections=True,
        highlight_style="pygments"
    )

    if result["success"]:
        print(f"✅ API documentation generated successfully")
        print(f"   File: {result['file_path']}")
        print(f"   Size: {result['size_bytes']:,} bytes")
        print(f"   Method: {result['method']}")
        print(f"   TOC: {result.get('toc', False)}")
        print(f"   Numbered: {result.get('numbered', False)}")
    else:
        print(f"❌ Generation failed: {result['error']}")
        if 'install_instructions' in result:
            print(f"\n📦 Installation required:")
            for os, cmd in result['install_instructions'].items():
                print(f"   {os}: {cmd}")


if __name__ == "__main__":
    create_technical_doc()
