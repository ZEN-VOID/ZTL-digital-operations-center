---
name: lark-mcp
description: Feishu/Lark collaboration integration with 15+ tools for messaging, group chat, bitable (multidimensional tables), documents, user management, and permissions. Use for enterprise collaboration, data management, and workflow automation.
---

# Lark-MCP Skill

基于lark-mcp的飞书/Lark完整协同能力包，提供消息推送、群聊管理、多维表格、云文档、用户管理等15+核心功能。

## Quick Start

### 消息推送

```python
# 发送文本消息到群聊
await im_v1_message_create(
    data={
        "receive_id": "oc_xxx",  # 群聊ID
        "msg_type": "text",
        "content": '{"text": "Hello from Claude!"}'
    },
    params={"receive_id_type": "chat_id"}
)
```

### 多维表格操作

```python
# 1. 搜索记录
records = await bitable_v1_appTableRecord_search(
    path={"app_token": "bascxxx", "table_id": "tblxxx"},
    data={"filter": {...}, "sort": [...]}
)

# 2. 创建记录
await bitable_v1_appTableRecord_create(
    path={"app_token": "bascxxx", "table_id": "tblxxx"},
    data={"fields": {"Name": "新记录", "Status": "进行中"}}
)
```

### 创建群聊

```python
# 创建群聊并邀请成员
await im_v1_chat_create(
    data={
        "name": "项目讨论组",
        "description": "ZTL项目开发讨论",
        "user_id_list": ["ou_xxx", "ou_yyy"],
        "chat_type": "private"
    },
    params={"user_id_type": "open_id"}
)
```

## Core Capabilities

### 1. 消息管理 (Messaging)

#### 发送消息

**支持的消息类型**:
- `text`: 文本消息
- `post`: 富文本消息
- `image`: 图片
- `file`: 文件
- `audio`: 音频
- `media`: 视频
- `sticker`: 表情
- `interactive`: 卡片消息
- `share_chat`: 群名片
- `share_user`: 个人名片

```python
# 文本消息
await im_v1_message_create(
    data={
        "receive_id": "ou_xxx",
        "msg_type": "text",
        "content": '{"text": "你好!"}'
    },
    params={"receive_id_type": "open_id"}
)

# 富文本消息
await im_v1_message_create(
    data={
        "receive_id": "oc_xxx",
        "msg_type": "post",
        "content": '''{
            "zh_cn": {
                "title": "项目更新",
                "content": [
                    [{"tag": "text", "text": "本周完成: "}],
                    [{"tag": "text", "text": "✓ 功能A开发"}],
                    [{"tag": "a", "text": "查看详情", "href": "https://..."}]
                ]
            }
        }'''
    },
    params={"receive_id_type": "chat_id"}
)

# 卡片消息
card_content = {
    "config": {"wide_screen_mode": True},
    "header": {"title": {"tag": "plain_text", "content": "任务提醒"}},
    "elements": [
        {"tag": "div", "text": {"tag": "plain_text", "content": "您有新任务待处理"}}
    ]
}

await im_v1_message_create(
    data={
        "receive_id": "ou_xxx",
        "msg_type": "interactive",
        "content": json.dumps(card_content)
    },
    params={"receive_id_type": "open_id"}
)
```

#### 获取消息历史

```python
# 获取群聊历史消息
messages = await im_v1_message_list(
    params={
        "container_id_type": "chat",  # 或 "thread" (话题)
        "container_id": "oc_xxx",
        "start_time": "1640000000",  # Unix时间戳（秒）
        "end_time": "1650000000",
        "page_size": 50,
        "sort_type": "ByCreateTimeDesc"  # 或 "ByCreateTimeAsc"
    }
)

# 获取话题消息
thread_messages = await im_v1_message_list(
    params={
        "container_id_type": "thread",
        "container_id": "omt_xxx",
        "page_size": 100
    }
)
```

### 2. 群聊管理 (Group Chat)

#### 创建群聊

```python
# 创建私有群聊
chat = await im_v1_chat_create(
    data={
        "name": "技术讨论组",
        "description": "后端技术讨论",
        "avatar": "img_xxx",  # 群头像key
        "chat_type": "private",  # 或 "public"
        "user_id_list": ["ou_a", "ou_b", "ou_c"],
        "bot_id_list": ["cli_xxx"],  # 邀请机器人
        "owner_id": "ou_a",  # 群主
        "join_message_visibility": "all_members",
        "leave_message_visibility": "only_owner",
        "membership_approval": "no_approval_required"
    },
    params={
        "user_id_type": "open_id",
        "uuid": "unique-request-id"  # 用于去重
    }
)
```

#### 获取群聊列表

```python
# 获取机器人/用户所在的群聊
chats = await im_v1_chat_list(
    params={
        "user_id_type": "open_id",
        "page_size": 50,
        "page_token": "",
        "sort_type": "ByCreateTimeAsc"  # 或 "ByActiveTimeDesc"
    },
    useUAT=True  # 使用用户访问令牌
)

# 遍历所有群聊
all_chats = []
page_token = ""

while True:
    response = await im_v1_chat_list(
        params={
            "page_size": 100,
            "page_token": page_token
        }
    )
    all_chats.extend(response['items'])

    if not response.get('has_more'):
        break
    page_token = response['page_token']
```

#### 获取群成员

```python
# 获取群聊成员列表
members = await im_v1_chatMembers_get(
    path={"chat_id": "oc_xxx"},
    params={
        "member_id_type": "open_id",
        "page_size": 100,
        "page_token": ""
    }
)
```

### 3. 多维表格 (Bitable)

#### 表格与字段管理

```python
# 创建Base App
app = await bitable_v1_app_create(
    data={
        "name": "项目管理系统",
        "folder_token": "fldcnxxx",  # 文件夹token
        "time_zone": "Asia/Shanghai"
    },
    useUAT=True
)

# 创建数据表
table = await bitable_v1_appTable_create(
    path={"app_token": "bascxxx"},
    data={
        "table": {
            "name": "任务列表",
            "default_view_name": "所有任务",
            "fields": [
                {
                    "field_name": "任务名称",
                    "type": 1,  # 文本类型
                    "ui_type": "Text"
                },
                {
                    "field_name": "状态",
                    "type": 3,  # 单选
                    "ui_type": "SingleSelect",
                    "property": {
                        "options": [
                            {"name": "待处理", "color": 1},
                            {"name": "进行中", "color": 2},
                            {"name": "已完成", "color": 3}
                        ]
                    }
                },
                {
                    "field_name": "负责人",
                    "type": 11,  # 人员
                    "ui_type": "User",
                    "property": {"multiple": False}
                },
                {
                    "field_name": "截止日期",
                    "type": 5,  # 日期
                    "ui_type": "DateTime"
                }
            ]
        }
    }
)

# 列出所有表
tables = await bitable_v1_appTable_list(
    path={"app_token": "bascxxx"},
    params={"page_size": 100}
)

# 列出字段
fields = await bitable_v1_appTableField_list(
    path={
        "app_token": "bascxxx",
        "table_id": "tblxxx"
    },
    params={"page_size": 100}
)
```

#### 记录操作

```python
# 创建记录
record = await bitable_v1_appTableRecord_create(
    path={
        "app_token": "bascxxx",
        "table_id": "tblxxx"
    },
    data={
        "fields": {
            "任务名称": "开发登录功能",
            "状态": "进行中",
            "负责人": [{"id": "ou_xxx"}],
            "截止日期": 1698422400000  # 毫秒时间戳
        }
    },
    params={"user_id_type": "open_id"}
)

# 更新记录
await bitable_v1_appTableRecord_update(
    path={
        "app_token": "bascxxx",
        "table_id": "tblxxx",
        "record_id": "recxxx"
    },
    data={
        "fields": {
            "状态": "已完成"
        }
    }
)

# 搜索记录
results = await bitable_v1_appTableRecord_search(
    path={
        "app_token": "bascxxx",
        "table_id": "tblxxx"
    },
    data={
        "filter": {
            "conjunction": "and",
            "conditions": [
                {
                    "field_name": "状态",
                    "operator": "is",
                    "value": ["进行中"]
                },
                {
                    "field_name": "负责人",
                    "operator": "contains",
                    "value": ["ou_xxx"]
                }
            ]
        },
        "sort": [
            {"field_name": "截止日期", "desc": False}
        ],
        "field_names": ["任务名称", "状态", "负责人", "截止日期"],
        "page_size": 50
    },
    params={"user_id_type": "open_id"}
)
```

### 4. 云文档 (Documents)

#### 文档搜索

```python
# 搜索Wiki文档
wiki_docs = await wiki_v1_node_search(
    data={
        "query": "API文档",
        "space_id": "wikixxx",  # 可选，限定知识空间
        "node_id": "nodexxx"    # 可选，限定节点
    },
    params={
        "page_size": 20,
        "page_token": ""
    },
    useUAT=True
)

# 搜索云文档（新版文档）
docs = await docx_builtin_search(
    data={
        "search_key": "项目规划",
        "docs_types": ["docx", "sheet", "bitable"],
        "owner_ids": ["ou_xxx"],  # 可选，按所有者筛选
        "chat_ids": ["oc_yyy"],   # 可选，按所在群聊筛选
        "count": 20,
        "offset": 0
    },
    useUAT=True
)
```

#### 获取文档内容

```python
# 获取新版文档纯文本内容
content = await docx_v1_document_rawContent(
    path={"document_id": "doxcnxxx"},
    params={"lang": 0},  # 0=中文, 1=英文
    useUAT=True
)

# 获取Wiki节点信息
wiki_node = await wiki_v2_space_getNode(
    params={
        "token": "wikixxx",  # Wiki节点token
        "obj_type": "docx"   # 或 "sheet", "bitable"
    },
    useUAT=True
)
```

#### 导入文档

```python
# 导入Markdown为云文档
doc = await docx_builtin_import(
    data={
        "markdown": """
# 项目计划

## 第一阶段
- 需求分析
- 技术选型

## 第二阶段
- 开发实现
- 测试验证
        """,
        "file_name": "项目计划"
    },
    useUAT=True
)
```

### 5. 权限管理 (Permissions)

```python
# 添加文档协作者
await drive_v1_permissionMember_create(
    path={"token": "doxcnxxx"},
    params={
        "type": "docx",  # 文档类型
        "need_notification": True  # 是否通知用户
    },
    data={
        "member_type": "openid",  # 或 "userid", "email", "openchat"
        "member_id": "ou_xxx",
        "perm": "edit",  # "view"(可读), "edit"(可编辑), "full_access"(可管理)
        "type": "user"   # "user", "chat", "department", "group"
    },
    useUAT=True
)
```

### 6. 用户管理 (User Management)

```python
# 通过邮箱/手机号批量获取用户ID
users = await contact_v3_user_batchGetId(
    data={
        "emails": ["user1@company.com", "user2@company.com"],
        "mobiles": ["+8613800138000"],
        "include_resigned": False  # 是否包含离职员工
    },
    params={"user_id_type": "open_id"}
)

# 返回格式
# {
#   "user_list": [
#     {
#       "user_id": "ou_xxx",
#       "mobile": "+8613800138000",
#       "email": "user@company.com",
#       "status": 1  # 1=在职, 2=离职
#     }
#   ]
# }
```

## Usage Patterns

### Pattern 1: 项目任务管理

```python
async def create_project_task(
    app_token: str,
    table_id: str,
    task_data: dict
):
    """创建项目任务"""

    # 1. 创建任务记录
    record = await bitable_v1_appTableRecord_create(
        path={"app_token": app_token, "table_id": table_id},
        data={"fields": task_data}
    )

    # 2. 发送任务通知
    assignee_id = task_data.get('负责人', [{}])[0].get('id')
    if assignee_id:
        await im_v1_message_create(
            data={
                "receive_id": assignee_id,
                "msg_type": "interactive",
                "content": json.dumps({
                    "config": {"wide_screen_mode": True},
                    "header": {
                        "title": {"tag": "plain_text", "content": "新任务分配"}
                    },
                    "elements": [
                        {
                            "tag": "div",
                            "text": {
                                "tag": "lark_md",
                                "content": f"**任务**: {task_data['任务名称']}\n**截止**: {task_data.get('截止日期', '未设置')}"
                            }
                        }
                    ]
                })
            },
            params={"receive_id_type": "open_id"}
        )

    return record
```

### Pattern 2: 自动化报告推送

```python
async def push_daily_report(chat_id: str, report_data: dict):
    """推送日报到群聊"""

    # 1. 构建富文本消息
    content = {
        "zh_cn": {
            "title": f"{report_data['date']} 日报",
            "content": [
                [{"tag": "text", "text": f"📊 总完成任务: {report_data['completed_tasks']}"}],
                [{"tag": "text", "text": f"🔄 进行中任务: {report_data['in_progress_tasks']}"}],
                [{"tag": "text", "text": f"⚠️ 待处理任务: {report_data['pending_tasks']}"}],
                [{"tag": "a", "text": "查看详情", "href": report_data['detail_link']}]
            ]
        }
    }

    # 2. 发送消息
    await im_v1_message_create(
        data={
            "receive_id": chat_id,
            "msg_type": "post",
            "content": json.dumps(content)
        },
        params={"receive_id_type": "chat_id"}
    )

    # 3. 记录到多维表格
    await bitable_v1_appTableRecord_create(
        path={
            "app_token": "bascxxx",
            "table_id": "tblxxx"
        },
        data={
            "fields": {
                "日期": report_data['date'],
                "完成任务数": report_data['completed_tasks'],
                "进行中任务数": report_data['in_progress_tasks']
            }
        }
    )
```

### Pattern 3: 批量用户邀请

```python
async def batch_invite_users(
    chat_id: str,
    user_emails: list
):
    """批量邀请用户加入群聊"""

    # 1. 通过邮箱获取用户ID
    users = await contact_v3_user_batchGetId(
        data={"emails": user_emails},
        params={"user_id_type": "open_id"}
    )

    # 2. 提取在职用户的open_id
    active_users = [
        user['user_id']
        for user in users['user_list']
        if user['status'] == 1
    ]

    # 3. 创建群聊（或添加成员到现有群聊）
    # 这里假设是创建新群聊
    chat = await im_v1_chat_create(
        data={
            "name": "项目协作群",
            "user_id_list": active_users,
            "chat_type": "private"
        },
        params={"user_id_type": "open_id"}
    )

    return chat
```

### Pattern 4: 文档权限批量管理

```python
async def share_document_with_team(
    doc_token: str,
    team_members: list,
    permission: str = "view"
):
    """批量分享文档给团队成员"""

    results = []

    for member in team_members:
        try:
            # 添加协作者
            result = await drive_v1_permissionMember_create(
                path={"token": doc_token},
                params={
                    "type": "docx",
                    "need_notification": True
                },
                data={
                    "member_type": "openid",
                    "member_id": member['open_id'],
                    "perm": permission,
                    "type": "user"
                },
                useUAT=True
            )
            results.append({
                "user": member['name'],
                "status": "success"
            })
        except Exception as e:
            results.append({
                "user": member['name'],
                "status": "failed",
                "error": str(e)
            })

    return results
```

### Pattern 5: 智能数据同步

```python
async def sync_tasks_to_lark(tasks: list, app_token: str, table_id: str):
    """同步任务数据到飞书多维表格"""

    # 1. 获取现有记录
    existing_records = await bitable_v1_appTableRecord_search(
        path={"app_token": app_token, "table_id": table_id},
        data={"page_size": 500}
    )

    existing_map = {
        record['fields'].get('任务ID'): record['record_id']
        for record in existing_records.get('items', [])
    }

    # 2. 同步任务
    for task in tasks:
        task_id = task['id']

        if task_id in existing_map:
            # 更新现有记录
            await bitable_v1_appTableRecord_update(
                path={
                    "app_token": app_token,
                    "table_id": table_id,
                    "record_id": existing_map[task_id]
                },
                data={
                    "fields": {
                        "任务名称": task['title'],
                        "状态": task['status'],
                        "进度": task['progress']
                    }
                }
            )
        else:
            # 创建新记录
            await bitable_v1_appTableRecord_create(
                path={"app_token": app_token, "table_id": table_id},
                data={
                    "fields": {
                        "任务ID": task_id,
                        "任务名称": task['title'],
                        "状态": task['status'],
                        "进度": task['progress']
                    }
                }
            )
```

## Best Practices

### 1. 使用正确的ID类型

```python
# ✓ 推荐：使用open_id（跨应用唯一）
await im_v1_message_create(
    data={"receive_id": "ou_xxx", ...},
    params={"receive_id_type": "open_id"}
)

# ✓ 可接受：使用user_id（租户内唯一）
await im_v1_message_create(
    data={"receive_id": "123abc", ...},
    params={"receive_id_type": "user_id"}
)

# ✗ 避免：混用ID类型
await im_v1_message_create(
    data={"receive_id": "ou_xxx", ...},
    params={"receive_id_type": "user_id"}  # ID类型不匹配
)
```

### 2. 消息内容格式化

```python
# ✓ 推荐：使用json.dumps序列化复杂内容
content = {"text": "Hello"}
await im_v1_message_create(
    data={
        "receive_id": "ou_xxx",
        "msg_type": "text",
        "content": json.dumps(content)  # 正确序列化
    },
    params={"receive_id_type": "open_id"}
)

# ✗ 错误：传递dict对象
await im_v1_message_create(
    data={
        "content": content  # 应该是字符串
    }
)
```

### 3. 分页查询完整数据

```python
# ✓ 推荐：使用while循环获取所有数据
all_records = []
page_token = ""

while True:
    response = await bitable_v1_appTableRecord_search(
        path={"app_token": "bascxxx", "table_id": "tblxxx"},
        data={"page_size": 500, "page_token": page_token}
    )

    all_records.extend(response['items'])

    if not response.get('has_more'):
        break
    page_token = response['page_token']

# ✗ 不推荐：只获取第一页
records = await bitable_v1_appTableRecord_search(
    path={"app_token": "bascxxx", "table_id": "tblxxx"},
    data={"page_size": 100}
)
```

### 4. 错误处理与重试

```python
# ✓ 推荐：添加错误处理
async def send_message_with_retry(receive_id: str, content: str, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            return await im_v1_message_create(
                data={
                    "receive_id": receive_id,
                    "msg_type": "text",
                    "content": json.dumps({"text": content})
                },
                params={"receive_id_type": "open_id"}
            )
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"重试 {attempt + 1}/{max_retries}: {e}")
            await asyncio.sleep(2 ** attempt)  # 指数退避
```

### 5. 使用UAT vs Tenant Token

```python
# ✓ 用户操作：使用useUAT=True
docs = await docx_builtin_search(
    data={"search_key": "项目"},
    useUAT=True  # 搜索用户可见的文档
)

# ✓ 机器人操作：不使用UAT（默认租户令牌）
await im_v1_message_create(
    data={
        "receive_id": "ou_xxx",
        "msg_type": "text",
        "content": '{"text": "机器人消息"}'
    }
)
```

## Common Issues

### Issue 1: 消息发送失败

**原因**:
- 机器人未添加到群聊
- 权限不足
- receive_id类型错误

**解决方案**:
```python
# 1. 确认机器人在群聊中
chats = await im_v1_chat_list(params={"page_size": 100})
chat_ids = [chat['chat_id'] for chat in chats['items']]

if target_chat_id in chat_ids:
    await im_v1_message_create(...)
else:
    print("机器人不在目标群聊中")

# 2. 检查ID类型
# receive_id_type必须与receive_id格式匹配
# open_id: ou_xxx
# chat_id: oc_xxx
# user_id: 自定义格式
```

### Issue 2: 多维表格搜索无结果

**原因**:
- filter条件语法错误
- 字段名称不正确
- 数据类型不匹配

**解决方案**:
```python
# 1. 先列出字段确认名称
fields = await bitable_v1_appTableField_list(
    path={"app_token": "bascxxx", "table_id": "tblxxx"}
)
field_names = [f['field_name'] for f in fields['items']]
print(f"可用字段: {field_names}")

# 2. 使用正确的operator
# 文本字段: "is", "isNot", "contains", "doesNotContain", "isEmpty", "isNotEmpty"
# 数字字段: "is", "isGreater", "isLess"
# 日期字段: "is", "isGreater", "isLess"

# 3. 确保value格式正确
await bitable_v1_appTableRecord_search(
    data={
        "filter": {
            "conjunction": "and",
            "conditions": [
                {
                    "field_name": "状态",
                    "operator": "is",
                    "value": ["进行中"]  # 注意是数组
                }
            ]
        }
    }
)
```

### Issue 3: 权限添加失败

**原因**:
- 文档type参数错误
- 用户已有权限
- 缺少useUAT=True

**解决方案**:
```python
# 确保使用用户令牌
await drive_v1_permissionMember_create(
    path={"token": "doxcnxxx"},
    params={
        "type": "docx",  # 确保与文档类型匹配
        "need_notification": True
    },
    data={...},
    useUAT=True  # 必需
)
```

## Integration Examples

### Example 1: 与GitHub-MCP集成

```python
# GitHub PR创建后自动通知飞书
async def notify_pr_creation(pr_info: dict, chat_id: str):
    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": "🔔 新PR创建"}
        },
        "elements": [
            {
                "tag": "div",
                "fields": [
                    {"is_short": True, "text": {"tag": "lark_md", "content": f"**标题**\n{pr_info['title']}"}},
                    {"is_short": True, "text": {"tag": "lark_md", "content": f"**作者**\n{pr_info['author']}"}}
                ]
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {"tag": "plain_text", "content": "查看PR"},
                        "url": pr_info['html_url'],
                        "type": "primary"
                    }
                ]
            }
        ]
    }

    await im_v1_message_create(
        data={
            "receive_id": chat_id,
            "msg_type": "interactive",
            "content": json.dumps(card)
        },
        params={"receive_id_type": "chat_id"}
    )
```

### Example 2: 与COS-MCP集成

```python
# 上传文件到COS后分享到飞书
async def share_file_to_lark(file_url: str, chat_id: str):
    # 发送文件链接消息
    await im_v1_message_create(
        data={
            "receive_id": chat_id,
            "msg_type": "post",
            "content": json.dumps({
                "zh_cn": {
                    "title": "文件已上传",
                    "content": [
                        [{"tag": "a", "text": "点击下载", "href": file_url}]
                    ]
                }
            })
        },
        params={"receive_id_type": "chat_id"}
    )
```

## Tips & Tricks

1. **消息类型**: 富文本(post)和卡片(interactive)更适合复杂信息展示
2. **批量操作**: 使用batch API（如果可用）减少请求次数
3. **分页策略**: 设置合理的page_size（推荐100-500）平衡性能
4. **时间格式**: 多维表格日期字段使用毫秒时间戳
5. **字段类型**: 创建表时参考[字段类型对照表]
6. **去重机制**: 创建群聊时使用uuid参数防止重复创建
7. **权限管理**: 优先使用open_id保证跨应用一致性
8. **消息撤回**: 保存message_id以便后续撤回或更新
9. **卡片设计**: 使用[卡片搭建工具]快速原型设计
10. **错误日志**: 记录完整的请求参数便于调试

## Lark-MCP Tools Reference

详见[Lark-MCP工具参考](reference.md)（待补充）

## Version History

- **v1.0.0** (2025-10-23): 初始版本
  - 15+核心工具完整支持
  - 消息管理与群聊操作
  - 多维表格CRUD
  - 云文档搜索与导入
  - 权限管理
  - 用户ID批量查询
