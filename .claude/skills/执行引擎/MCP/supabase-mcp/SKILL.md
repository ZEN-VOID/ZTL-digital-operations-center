---
name: Supabase Cloud Database
description: Supabase云数据库管理，基于PostgreSQL提供数据库操作、实时订阅、认证管理、存储服务等全栈后端能力，支持双向数据流转和实时协作
---

# Supabase MCP Skill

基于supabase-mcp的云数据库管理能力包，提供PostgreSQL数据库的完整操作能力、实时数据订阅、用户认证和文件存储等后端服务。

## Quick Start

### 示例1: 数据库基础操作

```python
# 1. 查询数据
users = await supabase.table('users') \
    .select('*') \
    .eq('status', 'active') \
    .order('created_at', desc=True) \
    .limit(10) \
    .execute()

# 2. 插入数据
new_user = await supabase.table('users').insert({
    'email': 'user@example.com',
    'name': 'John Doe',
    'status': 'active'
}).execute()

# 3. 更新数据
updated = await supabase.table('users') \
    .update({'status': 'inactive'}) \
    .eq('id', user_id) \
    .execute()

# 4. 删除数据
deleted = await supabase.table('users') \
    .delete() \
    .eq('id', user_id) \
    .execute()
```

### 示例2: 高级查询

```python
# 1. 关联查询(JOIN)
posts_with_authors = await supabase.table('posts') \
    .select('*, author:users(name, email)') \
    .execute()

# 2. 条件组合
results = await supabase.table('products') \
    .select('*') \
    .gte('price', 100) \
    .lte('price', 1000) \
    .in_('category', ['electronics', 'books']) \
    .ilike('name', '%laptop%') \
    .execute()

# 3. 分页查询
page_size = 20
page = 2
offset = (page - 1) * page_size

paginated = await supabase.table('articles') \
    .select('*', count='exact') \
    .range(offset, offset + page_size - 1) \
    .execute()

total_count = paginated.count
items = paginated.data

# 4. 聚合查询
stats = await supabase.rpc('get_product_stats', {
    'category': 'electronics'
}).execute()
```

### 示例3: 实时订阅

```python
# 1. 订阅表的所有变更
def handle_change(payload):
    event_type = payload['eventType']  # INSERT, UPDATE, DELETE
    new_record = payload.get('new')
    old_record = payload.get('old')

    print(f"Change detected: {event_type}")
    print(f"New data: {new_record}")

# 订阅users表
subscription = supabase.table('users') \
    .on('*', handle_change) \
    .subscribe()

# 2. 订阅特定事件
insert_subscription = supabase.table('orders') \
    .on('INSERT', handle_new_order) \
    .subscribe()

# 3. 订阅过滤条件
high_value_orders = supabase.table('orders') \
    .on('INSERT', handle_high_value_order) \
    .filter('amount', 'gt', 1000) \
    .subscribe()

# 4. 取消订阅
subscription.unsubscribe()
```

### 示例4: 用户认证

```python
# 1. 用户注册
signup_result = await supabase.auth.sign_up({
    'email': 'user@example.com',
    'password': 'secure_password'
})

user = signup_result.user
session = signup_result.session

# 2. 用户登录
login_result = await supabase.auth.sign_in_with_password({
    'email': 'user@example.com',
    'password': 'secure_password'
})

# 3. 获取当前用户
current_user = await supabase.auth.get_user()

# 4. 更新用户信息
updated_user = await supabase.auth.update_user({
    'data': {
        'display_name': 'John Doe',
        'avatar_url': 'https://...'
    }
})

# 5. 登出
await supabase.auth.sign_out()
```

### 示例5: 文件存储

```python
# 1. 上传文件
with open('photo.jpg', 'rb') as f:
    upload_result = await supabase.storage \
        .from_('avatars') \
        .upload('user123/avatar.jpg', f)

# 2. 获取公开URL
public_url = supabase.storage \
    .from_('avatars') \
    .get_public_url('user123/avatar.jpg')

# 3. 下载文件
file_data = await supabase.storage \
    .from_('avatars') \
    .download('user123/avatar.jpg')

# 4. 删除文件
await supabase.storage \
    .from_('avatars') \
    .remove(['user123/avatar.jpg'])

# 5. 列出文件
files = await supabase.storage \
    .from_('documents') \
    .list('user123/', {
        'limit': 100,
        'offset': 0,
        'sortBy': {'column': 'name', 'order': 'asc'}
    })
```

## Core Capabilities

### 1. 数据库操作 (Database Operations)

#### 1.1 查询数据 (SELECT)
```python
# 基础查询
data = await supabase.table('table_name').select('*').execute()

# 指定字段
data = await supabase.table('users').select('id, name, email').execute()

# 关联查询
data = await supabase.table('posts') \
    .select('title, content, author:users(name, avatar)') \
    .execute()

# 嵌套关联
data = await supabase.table('comments') \
    .select('*, post:posts(*, author:users(*))') \
    .execute()
```

#### 1.2 插入数据 (INSERT)
```python
# 插入单条
result = await supabase.table('users').insert({
    'name': 'Alice',
    'email': 'alice@example.com'
}).execute()

# 批量插入
result = await supabase.table('users').insert([
    {'name': 'Bob', 'email': 'bob@example.com'},
    {'name': 'Carol', 'email': 'carol@example.com'}
]).execute()

# 插入并返回数据
result = await supabase.table('users') \
    .insert({'name': 'David'}) \
    .select() \
    .execute()

# Upsert(存在则更新)
result = await supabase.table('users') \
    .upsert({'id': 1, 'name': 'Updated Name'}) \
    .execute()
```

#### 1.3 更新数据 (UPDATE)
```python
# 基础更新
result = await supabase.table('users') \
    .update({'status': 'inactive'}) \
    .eq('id', 123) \
    .execute()

# 条件更新
result = await supabase.table('products') \
    .update({'in_stock': False}) \
    .lt('quantity', 10) \
    .execute()

# 更新并返回
result = await supabase.table('users') \
    .update({'last_login': 'now()'}) \
    .eq('id', user_id) \
    .select() \
    .execute()
```

#### 1.4 删除数据 (DELETE)
```python
# 基础删除
result = await supabase.table('users') \
    .delete() \
    .eq('id', 123) \
    .execute()

# 条件删除
result = await supabase.table('sessions') \
    .delete() \
    .lt('expires_at', 'now()') \
    .execute()

# 删除并返回
result = await supabase.table('users') \
    .delete() \
    .eq('id', user_id) \
    .select() \
    .execute()
```

### 2. 查询条件 (Query Filters)

#### 2.1 比较运算符
```python
# 等于
.eq('column', 'value')

# 不等于
.neq('column', 'value')

# 大于
.gt('age', 18)

# 大于等于
.gte('price', 100)

# 小于
.lt('quantity', 10)

# 小于等于
.lte('score', 100)

# 模糊匹配(LIKE)
.like('name', '%John%')

# 不区分大小写模糊匹配(ILIKE)
.ilike('email', '%@gmail.com')

# 在列表中(IN)
.in_('status', ['active', 'pending'])

# 为空
.is_('deleted_at', None)

# 不为空
.not_.is_('email', None)
```

#### 2.2 逻辑组合
```python
# AND(默认)
result = await supabase.table('users') \
    .select('*') \
    .eq('status', 'active') \
    .gt('age', 18) \
    .execute()

# OR
result = await supabase.table('users') \
    .select('*') \
    .or_('status.eq.active,status.eq.pending') \
    .execute()

# NOT
result = await supabase.table('users') \
    .select('*') \
    .not_.eq('role', 'admin') \
    .execute()
```

#### 2.3 排序与限制
```python
# 排序
.order('created_at', desc=True)
.order('name', desc=False)

# 多字段排序
.order('category').order('price', desc=True)

# 限制数量
.limit(10)

# 分页(OFFSET)
.range(0, 9)    # 第1-10条
.range(10, 19)  # 第11-20条

# 单条记录
.single()  # 确保只返回一条,否则报错
.maybe_single()  # 返回一条或None
```

### 3. 高级功能 (Advanced Features)

#### 3.1 全文搜索
```python
# 文本搜索
result = await supabase.table('articles') \
    .select('*') \
    .text_search('title', 'postgres database') \
    .execute()

# 配置搜索
result = await supabase.table('articles') \
    .select('*') \
    .text_search('content', 'python programming', {
        'config': 'english',
        'type': 'websearch'
    }) \
    .execute()
```

#### 3.2 JSON操作
```python
# 查询JSON字段
result = await supabase.table('users') \
    .select('*') \
    .eq('metadata->city', 'Beijing') \
    .execute()

# JSON包含
result = await supabase.table('products') \
    .select('*') \
    .contains('tags', ['electronics', 'sale']) \
    .execute()
```

#### 3.3 RPC调用(存储过程)
```python
# 调用数据库函数
result = await supabase.rpc('function_name', {
    'param1': 'value1',
    'param2': 'value2'
}).execute()

# 示例: 复杂业务逻辑
stats = await supabase.rpc('calculate_user_stats', {
    'user_id': 123,
    'start_date': '2024-01-01',
    'end_date': '2024-12-31'
}).execute()
```

### 4. 实时功能 (Realtime)

#### 4.1 表级订阅
```python
# 订阅所有事件
def handle_all_events(payload):
    print(f"Event: {payload['eventType']}")
    print(f"Table: {payload['table']}")
    print(f"New: {payload.get('new')}")
    print(f"Old: {payload.get('old')}")

subscription = supabase.table('messages') \
    .on('*', handle_all_events) \
    .subscribe()

# 订阅INSERT事件
insert_sub = supabase.table('orders') \
    .on('INSERT', handle_new_order) \
    .subscribe()

# 订阅UPDATE事件
update_sub = supabase.table('products') \
    .on('UPDATE', handle_product_update) \
    .subscribe()

# 订阅DELETE事件
delete_sub = supabase.table('sessions') \
    .on('DELETE', handle_session_end) \
    .subscribe()
```

#### 4.2 条件订阅
```python
# 仅订阅特定条件的变更
high_priority_sub = supabase.table('tasks') \
    .on('INSERT', handle_high_priority) \
    .filter('priority', 'eq', 'high') \
    .subscribe()

# 多条件过滤
filtered_sub = supabase.table('events') \
    .on('*', handle_event) \
    .filter('type', 'eq', 'alert') \
    .filter('severity', 'gt', 5) \
    .subscribe()
```

#### 4.3 Presence(在线状态)
```python
# 加入Presence频道
channel = supabase.channel('room:123')

# 追踪用户在线状态
await channel.track({
    'user_id': 'user123',
    'online_at': datetime.now().isoformat()
})

# 监听状态变化
def on_presence_sync():
    state = channel.presenceState()
    print(f"Online users: {len(state)}")

channel.on('presence', {'event': 'sync'}, on_presence_sync)

# 订阅频道
await channel.subscribe()

# 离开频道
await channel.untrack()
await channel.unsubscribe()
```

#### 4.4 Broadcast(广播消息)
```python
# 发送广播消息
channel = supabase.channel('chat:room1')

await channel.send({
    'type': 'broadcast',
    'event': 'message',
    'payload': {
        'user': 'Alice',
        'text': 'Hello everyone!'
    }
})

# 接收广播消息
def on_broadcast(payload):
    print(f"Message from {payload['user']}: {payload['text']}")

channel.on('broadcast', {'event': 'message'}, on_broadcast)
await channel.subscribe()
```

### 5. 认证管理 (Authentication)

#### 5.1 邮箱密码认证
```python
# 注册
signup = await supabase.auth.sign_up({
    'email': 'user@example.com',
    'password': 'password123',
    'options': {
        'data': {
            'first_name': 'John',
            'last_name': 'Doe'
        }
    }
})

# 登录
login = await supabase.auth.sign_in_with_password({
    'email': 'user@example.com',
    'password': 'password123'
})

# 登出
await supabase.auth.sign_out()

# 重置密码
await supabase.auth.reset_password_for_email('user@example.com')
```

#### 5.2 第三方OAuth
```python
# Google登录
await supabase.auth.sign_in_with_oauth({
    'provider': 'google',
    'options': {
        'redirectTo': 'https://example.com/callback'
    }
})

# GitHub登录
await supabase.auth.sign_in_with_oauth({
    'provider': 'github'
})

# 其他提供商: apple, azure, facebook, twitter等
```

#### 5.3 用户管理
```python
# 获取当前用户
user = await supabase.auth.get_user()

# 更新用户数据
await supabase.auth.update_user({
    'data': {
        'avatar_url': 'https://...',
        'bio': 'Developer'
    }
})

# 更新密码
await supabase.auth.update_user({
    'password': 'new_password'
})

# 刷新会话
session = await supabase.auth.refresh_session()

# 获取会话
session = await supabase.auth.get_session()
```

### 6. 存储服务 (Storage)

#### 6.1 文件上传
```python
# 上传文件
with open('document.pdf', 'rb') as f:
    result = await supabase.storage \
        .from_('documents') \
        .upload('folder/document.pdf', f)

# 上传并覆盖
with open('image.jpg', 'rb') as f:
    result = await supabase.storage \
        .from_('images') \
        .upload('photo.jpg', f, {'upsert': True})

# 上传字节数据
data = b'file content'
result = await supabase.storage \
    .from_('files') \
    .upload('data.bin', data)
```

#### 6.2 文件下载
```python
# 下载文件
file_bytes = await supabase.storage \
    .from_('documents') \
    .download('folder/document.pdf')

# 保存到本地
with open('local_file.pdf', 'wb') as f:
    f.write(file_bytes)
```

#### 6.3 文件URL
```python
# 获取公开URL
public_url = supabase.storage \
    .from_('avatars') \
    .get_public_url('user123/avatar.jpg')

# 创建签名URL(带过期时间)
signed_url = await supabase.storage \
    .from_('private-files') \
    .create_signed_url('confidential.pdf', 3600)  # 1小时有效
```

#### 6.4 文件管理
```python
# 列出文件
files = await supabase.storage \
    .from_('documents') \
    .list('folder/', {
        'limit': 100,
        'offset': 0,
        'sortBy': {'column': 'name', 'order': 'asc'}
    })

# 删除文件
await supabase.storage \
    .from_('images') \
    .remove(['old_photo1.jpg', 'old_photo2.jpg'])

# 移动文件
await supabase.storage \
    .from_('files') \
    .move('old_path/file.txt', 'new_path/file.txt')

# 复制文件
await supabase.storage \
    .from_('files') \
    .copy('source.txt', 'backup.txt')
```

## Usage Patterns

### Pattern 1: CRUD完整流程

```python
class UserRepository:
    """用户数据仓库"""

    def __init__(self, supabase):
        self.supabase = supabase
        self.table = 'users'

    async def create(self, user_data):
        """创建用户"""
        result = await self.supabase.table(self.table) \
            .insert(user_data) \
            .select() \
            .single() \
            .execute()
        return result.data

    async def get_by_id(self, user_id):
        """根据ID获取用户"""
        result = await self.supabase.table(self.table) \
            .select('*') \
            .eq('id', user_id) \
            .maybe_single() \
            .execute()
        return result.data

    async def get_by_email(self, email):
        """根据邮箱获取用户"""
        result = await self.supabase.table(self.table) \
            .select('*') \
            .eq('email', email) \
            .maybe_single() \
            .execute()
        return result.data

    async def list(self, page=1, page_size=20, filters=None):
        """分页列表"""
        offset = (page - 1) * page_size

        query = self.supabase.table(self.table).select('*', count='exact')

        # 应用过滤条件
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)

        result = await query \
            .order('created_at', desc=True) \
            .range(offset, offset + page_size - 1) \
            .execute()

        return {
            'data': result.data,
            'total': result.count,
            'page': page,
            'page_size': page_size
        }

    async def update(self, user_id, updates):
        """更新用户"""
        result = await self.supabase.table(self.table) \
            .update(updates) \
            .eq('id', user_id) \
            .select() \
            .single() \
            .execute()
        return result.data

    async def delete(self, user_id):
        """删除用户"""
        await self.supabase.table(self.table) \
            .delete() \
            .eq('id', user_id) \
            .execute()
        return True
```

### Pattern 2: 实时协作系统

```python
class RealtimeCollaboration:
    """实时协作系统"""

    def __init__(self, supabase, document_id):
        self.supabase = supabase
        self.document_id = document_id
        self.channel = None
        self.subscriptions = []

    async def start(self):
        """启动实时协作"""

        # 1. 订阅文档变更
        doc_subscription = self.supabase.table('documents') \
            .on('UPDATE', self.on_document_update) \
            .filter('id', 'eq', self.document_id) \
            .subscribe()

        self.subscriptions.append(doc_subscription)

        # 2. 创建Presence频道
        self.channel = self.supabase.channel(f'doc:{self.document_id}')

        # 追踪当前用户
        await self.channel.track({
            'user_id': self.current_user_id,
            'joined_at': datetime.now().isoformat()
        })

        # 监听其他用户
        self.channel.on('presence', {'event': 'sync'}, self.on_presence_sync)
        self.channel.on('presence', {'event': 'join'}, self.on_user_join)
        self.channel.on('presence', {'event': 'leave'}, self.on_user_leave)

        # 监听广播消息
        self.channel.on('broadcast', {'event': 'cursor'}, self.on_cursor_move)
        self.channel.on('broadcast', {'event': 'selection'}, self.on_selection_change)

        await self.channel.subscribe()

    async def update_cursor(self, position):
        """更新光标位置"""
        await self.channel.send({
            'type': 'broadcast',
            'event': 'cursor',
            'payload': {
                'user_id': self.current_user_id,
                'position': position
            }
        })

    async def save_changes(self, content):
        """保存文档变更"""
        await self.supabase.table('documents') \
            .update({
                'content': content,
                'updated_at': 'now()',
                'updated_by': self.current_user_id
            }) \
            .eq('id', self.document_id) \
            .execute()

    def on_document_update(self, payload):
        """文档更新回调"""
        new_content = payload['new']['content']
        self.handle_remote_changes(new_content)

    def on_presence_sync(self):
        """在线用户同步"""
        users = self.channel.presenceState()
        self.update_online_users(users)

    def on_user_join(self, payload):
        """用户加入"""
        print(f"User joined: {payload}")

    def on_user_leave(self, payload):
        """用户离开"""
        print(f"User left: {payload}")

    def on_cursor_move(self, payload):
        """远程光标移动"""
        self.update_remote_cursor(payload)

    async def stop(self):
        """停止协作"""
        for sub in self.subscriptions:
            sub.unsubscribe()

        if self.channel:
            await self.channel.untrack()
            await self.channel.unsubscribe()
```

### Pattern 3: 认证与授权

```python
class AuthService:
    """认证服务"""

    def __init__(self, supabase):
        self.supabase = supabase

    async def signup(self, email, password, user_data=None):
        """用户注册"""
        result = await self.supabase.auth.sign_up({
            'email': email,
            'password': password,
            'options': {
                'data': user_data or {}
            }
        })

        if result.user:
            # 创建用户资料
            await self.supabase.table('profiles').insert({
                'user_id': result.user.id,
                'email': email,
                **(user_data or {})
            }).execute()

        return result

    async def login(self, email, password):
        """用户登录"""
        result = await self.supabase.auth.sign_in_with_password({
            'email': email,
            'password': password
        })

        # 更新最后登录时间
        if result.user:
            await self.supabase.table('profiles') \
                .update({'last_login': 'now()'}) \
                .eq('user_id', result.user.id) \
                .execute()

        return result

    async def logout(self):
        """用户登出"""
        await self.supabase.auth.sign_out()

    async def get_current_user(self):
        """获取当前用户"""
        user = await self.supabase.auth.get_user()

        if user:
            # 获取完整资料
            profile = await self.supabase.table('profiles') \
                .select('*') \
                .eq('user_id', user.id) \
                .single() \
                .execute()

            return {**user.dict(), 'profile': profile.data}

        return None

    async def update_profile(self, user_id, updates):
        """更新用户资料"""
        result = await self.supabase.table('profiles') \
            .update(updates) \
            .eq('user_id', user_id) \
            .select() \
            .single() \
            .execute()

        return result.data

    async def change_password(self, new_password):
        """修改密码"""
        await self.supabase.auth.update_user({
            'password': new_password
        })

    async def reset_password(self, email):
        """重置密码"""
        await self.supabase.auth.reset_password_for_email(email)
```

### Pattern 4: 文件管理服务

```python
class FileService:
    """文件管理服务"""

    def __init__(self, supabase, bucket='files'):
        self.supabase = supabase
        self.bucket = bucket

    async def upload(self, file_path, content, metadata=None):
        """上传文件"""

        # 1. 上传到Storage
        result = await self.supabase.storage \
            .from_(self.bucket) \
            .upload(file_path, content)

        # 2. 记录元数据到数据库
        file_record = {
            'path': file_path,
            'bucket': self.bucket,
            'size': len(content) if isinstance(content, bytes) else 0,
            'content_type': metadata.get('contentType') if metadata else None,
            'uploaded_by': await self.get_current_user_id()
        }

        await self.supabase.table('files').insert(file_record).execute()

        # 3. 获取公开URL
        url = self.supabase.storage \
            .from_(self.bucket) \
            .get_public_url(file_path)

        return {
            'path': file_path,
            'url': url
        }

    async def download(self, file_path):
        """下载文件"""
        content = await self.supabase.storage \
            .from_(self.bucket) \
            .download(file_path)

        # 记录下载日志
        await self.supabase.table('file_downloads').insert({
            'file_path': file_path,
            'downloaded_by': await self.get_current_user_id(),
            'downloaded_at': 'now()'
        }).execute()

        return content

    async def list_files(self, folder='', user_id=None):
        """列出文件"""

        # 从数据库查询(支持权限过滤)
        query = self.supabase.table('files') \
            .select('*') \
            .like('path', f'{folder}%')

        if user_id:
            query = query.eq('uploaded_by', user_id)

        result = await query.execute()

        return result.data

    async def delete(self, file_path):
        """删除文件"""

        # 1. 从Storage删除
        await self.supabase.storage \
            .from_(self.bucket) \
            .remove([file_path])

        # 2. 从数据库删除记录
        await self.supabase.table('files') \
            .delete() \
            .eq('path', file_path) \
            .execute()

    async def create_share_link(self, file_path, expires_in=3600):
        """创建分享链接"""

        # 创建签名URL
        signed_url = await self.supabase.storage \
            .from_(self.bucket) \
            .create_signed_url(file_path, expires_in)

        # 记录分享
        await self.supabase.table('file_shares').insert({
            'file_path': file_path,
            'shared_by': await self.get_current_user_id(),
            'expires_at': f"now() + interval '{expires_in} seconds'"
        }).execute()

        return signed_url

    async def get_current_user_id(self):
        """获取当前用户ID"""
        user = await self.supabase.auth.get_user()
        return user.id if user else None
```

## Best Practices

### 1. 连接管理
```python
# ✅ 推荐: 使用单例模式
class SupabaseClient:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = create_client(
                supabase_url=os.getenv('SUPABASE_URL'),
                supabase_key=os.getenv('SUPABASE_KEY')
            )
        return cls._instance

# 使用
supabase = SupabaseClient.get_instance()
```

### 2. 错误处理
```python
from supabase.lib.client_options import ClientOptions
from postgrest.exceptions import APIError

async def safe_query():
    try:
        result = await supabase.table('users') \
            .select('*') \
            .eq('id', user_id) \
            .single() \
            .execute()

        return result.data

    except APIError as e:
        if e.code == 'PGRST116':  # 未找到记录
            return None
        else:
            raise
```

### 3. 性能优化
```python
# ✅ 仅选择需要的字段
.select('id, name, email')  # 好
.select('*')  # 避免

# ✅ 使用索引字段作为查询条件
.eq('id', value)  # 好(主键)
.like('description', '%keyword%')  # 慢(全表扫描)

# ✅ 批量操作而非循环单条
.insert([item1, item2, item3])  # 好
# 避免: for item in items: .insert(item)
```

### 4. 安全最佳实践
```python
# ✅ 使用Row Level Security(RLS)
"""
CREATE POLICY "Users can only see their own data"
ON users
FOR SELECT
USING (auth.uid() = user_id);
"""

# ✅ 验证用户输入
def sanitize_input(text):
    # 防止SQL注入(Supabase已自动处理)
    # 但仍需验证业务逻辑
    return text.strip()

# ✅ 使用服务端密钥处理敏感操作
admin_supabase = create_client(
    url=SUPABASE_URL,
    key=SERVICE_ROLE_KEY  # 服务端密钥
)
```

### 5. 数据库设计
```python
# ✅ 推荐的表结构
"""
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 自动更新updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
"""
```

## Common Issues

### Issue 1: 跨域错误(CORS)
**问题**: 前端请求被CORS策略阻止
**解决**:
- 在Supabase Dashboard配置允许的域名
- 或使用服务端代理请求

### Issue 2: RLS策略导致查询失败
**问题**: 查询返回空结果或权限错误
**解决**:
```python
# 检查RLS策略
# 暂时禁用RLS测试(仅开发环境)
ALTER TABLE table_name DISABLE ROW LEVEL SECURITY;

# 查看当前用户
user = await supabase.auth.get_user()
print(f"Current user: {user.id}")

# 确保RLS策略正确
"""
CREATE POLICY "policy_name"
ON table_name
FOR SELECT
TO authenticated
USING (user_id = auth.uid());
"""
```

### Issue 3: 实时订阅未触发
**问题**: 数据变更但回调未执行
**解决**:
```python
# 1. 确保表启用了Realtime
# Dashboard > Database > Replication > 启用表

# 2. 检查订阅状态
subscription = channel.subscribe(
    callback=lambda status: print(f"Status: {status}")
)

# 3. 正确的事件类型
.on('postgres_changes', {
    'event': '*',  # INSERT, UPDATE, DELETE, *
    'schema': 'public',
    'table': 'table_name'
}, callback)
```

### Issue 4: 文件上传失败
**问题**: Storage上传返回403错误
**解决**:
```python
# 检查Bucket策略
"""
-- 允许认证用户上传
CREATE POLICY "Authenticated users can upload"
ON storage.objects
FOR INSERT
TO authenticated
WITH CHECK (bucket_id = 'bucket_name');
"""

# 检查文件大小限制(默认50MB)
# Dashboard > Storage > Settings
```

## Integration Examples

### 示例1: 完整的Todo应用

```python
class TodoApp:
    def __init__(self, supabase):
        self.supabase = supabase

    async def create_todo(self, title, description=None):
        """创建待办"""
        user = await self.supabase.auth.get_user()

        result = await self.supabase.table('todos').insert({
            'title': title,
            'description': description,
            'user_id': user.id,
            'completed': False
        }).select().single().execute()

        return result.data

    async def list_todos(self, completed=None):
        """列出待办"""
        user = await self.supabase.auth.get_user()

        query = self.supabase.table('todos') \
            .select('*') \
            .eq('user_id', user.id) \
            .order('created_at', desc=True)

        if completed is not None:
            query = query.eq('completed', completed)

        result = await query.execute()
        return result.data

    async def toggle_todo(self, todo_id):
        """切换完成状态"""
        # 先查询当前状态
        todo = await self.supabase.table('todos') \
            .select('completed') \
            .eq('id', todo_id) \
            .single() \
            .execute()

        # 切换状态
        new_status = not todo.data['completed']

        result = await self.supabase.table('todos') \
            .update({'completed': new_status}) \
            .eq('id', todo_id) \
            .select() \
            .single() \
            .execute()

        return result.data

    async def delete_todo(self, todo_id):
        """删除待办"""
        await self.supabase.table('todos') \
            .delete() \
            .eq('id', todo_id) \
            .execute()

    async def subscribe_to_changes(self, callback):
        """订阅变更"""
        user = await self.supabase.auth.get_user()

        return self.supabase.table('todos') \
            .on('*', callback) \
            .filter('user_id', 'eq', user.id) \
            .subscribe()
```

### 示例2: 实时聊天应用

```python
class ChatApp:
    def __init__(self, supabase, room_id):
        self.supabase = supabase
        self.room_id = room_id
        self.channel = None

    async def join_room(self):
        """加入聊天室"""
        user = await self.supabase.auth.get_user()

        # 记录用户进入
        await self.supabase.table('room_members').insert({
            'room_id': self.room_id,
            'user_id': user.id,
            'joined_at': 'now()'
        }).execute()

        # 创建Presence频道
        self.channel = self.supabase.channel(f'room:{self.room_id}')

        await self.channel.track({
            'user_id': user.id,
            'username': user.user_metadata.get('username'),
            'joined_at': datetime.now().isoformat()
        })

        # 监听在线用户
        self.channel.on('presence', {'event': 'sync'}, self.on_users_sync)

        # 监听新消息
        self.channel.on('broadcast', {'event': 'message'}, self.on_new_message)

        # 订阅历史消息变更
        self.message_subscription = self.supabase.table('messages') \
            .on('INSERT', self.on_message_inserted) \
            .filter('room_id', 'eq', self.room_id) \
            .subscribe()

        await self.channel.subscribe()

    async def send_message(self, content):
        """发送消息"""
        user = await self.supabase.auth.get_user()

        # 存储消息到数据库
        message = await self.supabase.table('messages').insert({
            'room_id': self.room_id,
            'user_id': user.id,
            'content': content,
            'created_at': 'now()'
        }).select().single().execute()

        # 广播消息(实时推送)
        await self.channel.send({
            'type': 'broadcast',
            'event': 'message',
            'payload': message.data
        })

        return message.data

    async def load_history(self, limit=50):
        """加载历史消息"""
        result = await self.supabase.table('messages') \
            .select('*, user:users(id, username, avatar)') \
            .eq('room_id', self.room_id) \
            .order('created_at', desc=True) \
            .limit(limit) \
            .execute()

        return list(reversed(result.data))

    def on_users_sync(self):
        """在线用户同步"""
        users = self.channel.presenceState()
        print(f"Online users: {len(users)}")

    def on_new_message(self, payload):
        """新消息回调"""
        print(f"New message: {payload}")

    def on_message_inserted(self, payload):
        """数据库消息插入回调"""
        print(f"Message saved: {payload['new']}")

    async def leave_room(self):
        """离开聊天室"""
        if self.channel:
            await self.channel.untrack()
            await self.channel.unsubscribe()

        if hasattr(self, 'message_subscription'):
            self.message_subscription.unsubscribe()
```

## Tips & Tricks

### 1. 使用TypeScript类型推导
```python
# Python类型提示
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class User:
    id: str
    email: str
    created_at: str
    updated_at: Optional[str] = None

async def get_users() -> List[User]:
    result = await supabase.table('users').select('*').execute()
    return [User(**user) for user in result.data]
```

### 2. 自动重连机制
```python
import asyncio

async def with_retry(func, max_retries=3):
    """带重试的函数包装"""
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)
                continue
            raise

# 使用
result = await with_retry(lambda: supabase.table('users').select('*').execute())
```

### 3. 批量操作优化
```python
# ✅ 批量插入
await supabase.table('logs').insert([
    {'event': 'login', 'user_id': 1},
    {'event': 'logout', 'user_id': 2},
    # ... 1000+ items
]).execute()

# ✅ 使用upsert避免重复
await supabase.table('settings') \
    .upsert([
        {'key': 'theme', 'value': 'dark'},
        {'key': 'lang', 'value': 'en'}
    ], on_conflict='key') \
    .execute()
```

### 4. 复杂查询构建
```python
# 动态构建查询
def build_query(filters):
    query = supabase.table('products').select('*')

    if 'category' in filters:
        query = query.eq('category', filters['category'])

    if 'min_price' in filters:
        query = query.gte('price', filters['min_price'])

    if 'max_price' in filters:
        query = query.lte('price', filters['max_price'])

    if 'search' in filters:
        query = query.ilike('name', f"%{filters['search']}%")

    return query

# 使用
result = await build_query({
    'category': 'electronics',
    'min_price': 100,
    'search': 'laptop'
}).execute()
```

### 5. 缓存策略
```python
from functools import lru_cache
from datetime import datetime, timedelta

cache = {}

async def cached_query(table, key, ttl_seconds=300):
    """带TTL的查询缓存"""
    cache_key = f"{table}:{key}"

    if cache_key in cache:
        data, expire_time = cache[cache_key]
        if datetime.now() < expire_time:
            return data

    # 查询数据库
    result = await supabase.table(table) \
        .select('*') \
        .eq('id', key) \
        .single() \
        .execute()

    # 缓存结果
    expire_time = datetime.now() + timedelta(seconds=ttl_seconds)
    cache[cache_key] = (result.data, expire_time)

    return result.data
```

### 6. 事务处理(通过RPC)
```python
# 创建数据库函数处理事务
"""
CREATE OR REPLACE FUNCTION transfer_funds(
    from_account_id UUID,
    to_account_id UUID,
    amount DECIMAL
)
RETURNS JSON AS $$
DECLARE
    from_balance DECIMAL;
BEGIN
    -- 检查余额
    SELECT balance INTO from_balance
    FROM accounts
    WHERE id = from_account_id
    FOR UPDATE;

    IF from_balance < amount THEN
        RAISE EXCEPTION 'Insufficient funds';
    END IF;

    -- 扣款
    UPDATE accounts
    SET balance = balance - amount
    WHERE id = from_account_id;

    -- 入账
    UPDATE accounts
    SET balance = balance + amount
    WHERE id = to_account_id;

    -- 记录交易
    INSERT INTO transactions (from_id, to_id, amount)
    VALUES (from_account_id, to_account_id, amount);

    RETURN json_build_object('success', true);
END;
$$ LANGUAGE plpgsql;
"""

# Python调用
result = await supabase.rpc('transfer_funds', {
    'from_account_id': sender_id,
    'to_account_id': receiver_id,
    'amount': 100.00
}).execute()
```

### 7. 全文搜索优化
```python
# 创建全文搜索索引
"""
CREATE INDEX articles_search_idx
ON articles
USING GIN (to_tsvector('english', title || ' ' || content));
"""

# 使用全文搜索
results = await supabase.table('articles') \
    .select('*') \
    .text_search('title', 'python programming', {
        'config': 'english',
        'type': 'websearch'
    }) \
    .execute()
```

### 8. 数据验证Hook
```python
# 创建验证触发器
"""
CREATE OR REPLACE FUNCTION validate_email()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.email !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' THEN
        RAISE EXCEPTION 'Invalid email format';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER validate_user_email
BEFORE INSERT OR UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION validate_email();
"""
```
