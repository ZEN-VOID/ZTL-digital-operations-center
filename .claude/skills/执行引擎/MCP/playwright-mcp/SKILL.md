# Playwright MCP 技能包

---
name: playwright-mcp
description: 基于Playwright的企业级网页爬虫和测试框架，提供真实浏览器环境操作、复杂交互自动化、表单填写、文件上传、网络请求捕获、控制台日志监控等30+核心能力，适用于深度爬虫、端到端测试和复杂自动化场景
---

## 快速开始

Playwright MCP是基于Playwright的企业级网页爬虫和自动化测试框架，提供真实浏览器环境的完整控制能力。

### 基础用法

```python
# 1. 导航到网页
await mcp__playwright_mcp__browser_navigate(
    url="https://example.com"
)

# 2. 获取页面快照
snapshot = await mcp__playwright_mcp__browser_snapshot()

# 3. 点击元素
await mcp__playwright_mcp__browser_click(
    element="登录按钮",
    ref="button[data-testid='login-btn']"
)

# 4. 填写表单
await mcp__playwright_mcp__browser_type(
    element="用户名输入框",
    ref="input[name='username']",
    text="user@example.com"
)

# 5. 截图
await mcp__playwright_mcp__browser_take_screenshot(
    filename="page-screenshot.png",
    fullPage=True
)
```

### 高级用法

```python
# 网络请求监控
await mcp__playwright_mcp__browser_network_debugger_start()
# ... 执行操作
requests = await mcp__playwright_mcp__browser_network_debugger_stop()

# 控制台日志捕获
logs = await mcp__playwright_mcp__browser_console_messages(
    onlyErrors=False
)

# JavaScript执行
result = await mcp__playwright_mcp__browser_evaluate(
    function="() => document.title"
)
```

---

## 核心能力

### 1. 浏览器生命周期管理

#### 导航控制
```python
# 导航到URL
await mcp__playwright_mcp__browser_navigate(
    url="https://example.com"
)

# 后退
await mcp__playwright_mcp__browser_navigate_back()

# 刷新页面
await mcp__playwright_mcp__browser_navigate(
    url="",  # 空URL表示刷新当前页面
    refresh=True
)
```

#### 窗口管理
```python
# 调整窗口大小
await mcp__playwright_mcp__browser_resize(
    width=1920,
    height=1080
)

# 关闭浏览器
await mcp__playwright_mcp__browser_close()
```

#### 标签页管理
```python
# 列出所有标签页
tabs = await mcp__playwright_mcp__browser_tabs(
    action="list"
)

# 新建标签页
await mcp__playwright_mcp__browser_tabs(
    action="new"
)

# 切换标签页
await mcp__playwright_mcp__browser_tabs(
    action="select",
    index=1
)

# 关闭标签页
await mcp__playwright_mcp__browser_tabs(
    action="close",
    index=2  # 可选，不指定则关闭当前标签页
)
```

### 2. 页面内容获取

#### 页面快照
```python
# 获取可访问性快照（推荐用于操作）
snapshot = await mcp__playwright_mcp__browser_snapshot()

# 返回结构化的页面元素树
# 包含所有可交互元素的层级关系和属性
```

#### 内容抓取
```python
# 获取文本内容
text_content = await mcp__playwright_mcp__chrome_get_web_content(
    textContent=True
)

# 获取HTML内容
html_content = await mcp__playwright_mcp__chrome_get_web_content(
    htmlContent=True
)

# 获取特定元素内容
element_content = await mcp__playwright_mcp__chrome_get_web_content(
    selector="#main-content",
    textContent=True
)
```

#### 截图
```python
# 截取当前视口
await mcp__playwright_mcp__browser_take_screenshot(
    filename="viewport.png",
    fullPage=False,
    type="png"
)

# 截取整页
await mcp__playwright_mcp__browser_take_screenshot(
    filename="full-page.png",
    fullPage=True
)

# 截取指定元素
await mcp__playwright_mcp__browser_take_screenshot(
    element="产品卡片",
    ref=".product-card",
    filename="product.png"
)

# JPEG格式（更小的文件）
await mcp__playwright_mcp__browser_take_screenshot(
    filename="page.jpeg",
    type="jpeg"
)
```

### 3. 元素交互

#### 点击操作
```python
# 基础点击
await mcp__playwright_mcp__browser_click(
    element="提交按钮",
    ref="button[type='submit']"
)

# 右键点击
await mcp__playwright_mcp__browser_click(
    element="上下文菜单",
    ref=".menu-trigger",
    button="right"
)

# 双击
await mcp__playwright_mcp__browser_click(
    element="文件项",
    ref=".file-item",
    doubleClick=True
)

# 带修饰键的点击
await mcp__playwright_mcp__browser_click(
    element="链接",
    ref="a[href='/page']",
    modifiers=["Control"]  # Ctrl+Click 在新标签页打开
)
```

#### 文本输入
```python
# 基础输入
await mcp__playwright_mcp__browser_type(
    element="邮箱输入框",
    ref="input[type='email']",
    text="user@example.com"
)

# 逐字符输入（触发键盘事件）
await mcp__playwright_mcp__browser_type(
    element="搜索框",
    ref="input[name='q']",
    text="playwright automation",
    slowly=True  # 触发每个字符的键盘事件
)

# 输入后提交
await mcp__playwright_mcp__browser_type(
    element="搜索框",
    ref="input[name='search']",
    text="查询内容",
    submit=True  # 输入后按Enter
)
```

#### 键盘操作
```python
# 按单个键
await mcp__playwright_mcp__browser_press_key(
    key="Enter"
)

# 组合键
await mcp__playwright_mcp__browser_press_key(
    key="Control+A"  # 全选
)

# 特殊键
await mcp__playwright_mcp__browser_press_key(
    key="ArrowDown"  # 方向键
)

# 向特定元素发送键盘事件
await mcp__playwright_mcp__browser_keyboard(
    selector="input[name='username']",
    keys="Enter"
)

# 键盘序列
await mcp__playwright_mcp__browser_keyboard(
    keys="A,B,C",  # 依次输入A、B、C
    delay=100  # 每个键之间延迟100ms
)
```

#### 鼠标操作
```python
# 悬停
await mcp__playwright_mcp__browser_hover(
    element="下拉菜单",
    ref=".dropdown-trigger"
)

# 拖拽
await mcp__playwright_mcp__browser_drag(
    startElement="拖拽源",
    startRef="#drag-source",
    endElement="放置目标",
    endRef="#drop-target"
)
```

#### 下拉选择
```python
# 选择单个选项
await mcp__playwright_mcp__browser_select_option(
    element="国家选择器",
    ref="select[name='country']",
    values=["CN"]
)

# 选择多个选项
await mcp__playwright_mcp__browser_select_option(
    element="兴趣选择",
    ref="select[name='interests']",
    values=["sports", "music", "reading"]
)
```

### 4. 表单处理

#### 表单填写
```python
# 批量填写表单
await mcp__playwright_mcp__browser_fill_form(
    fields=[
        {
            "name": "用户名",
            "type": "textbox",
            "ref": "input[name='username']",
            "value": "john_doe"
        },
        {
            "name": "邮箱",
            "type": "textbox",
            "ref": "input[name='email']",
            "value": "john@example.com"
        },
        {
            "name": "同意条款",
            "type": "checkbox",
            "ref": "input[name='terms']",
            "value": "true"
        },
        {
            "name": "性别",
            "type": "radio",
            "ref": "input[name='gender'][value='male']",
            "value": "male"
        },
        {
            "name": "城市",
            "type": "combobox",
            "ref": "select[name='city']",
            "value": "北京"
        }
    ]
)
```

#### 文件上传
```python
# 上传单个文件
await mcp__playwright_mcp__browser_file_upload(
    paths=["/path/to/document.pdf"]
)

# 上传多个文件
await mcp__playwright_mcp__browser_file_upload(
    paths=[
        "/path/to/image1.jpg",
        "/path/to/image2.png",
        "/path/to/document.pdf"
    ]
)

# 取消文件选择（不传paths）
await mcp__playwright_mcp__browser_file_upload()
```

### 5. 对话框处理

```python
# 接受对话框
await mcp__playwright_mcp__browser_handle_dialog(
    accept=True
)

# 拒绝对话框
await mcp__playwright_mcp__browser_handle_dialog(
    accept=False
)

# 处理prompt对话框并输入文本
await mcp__playwright_mcp__browser_handle_dialog(
    accept=True,
    promptText="用户输入内容"
)
```

### 6. JavaScript执行

```python
# 执行简单表达式
title = await mcp__playwright_mcp__browser_evaluate(
    function="() => document.title"
)

# 执行复杂脚本
result = await mcp__playwright_mcp__browser_evaluate(
    function="""() => {
        const links = document.querySelectorAll('a');
        return Array.from(links).map(a => ({
            text: a.textContent,
            href: a.href
        }));
    }"""
)

# 在特定元素上执行
element_text = await mcp__playwright_mcp__browser_evaluate(
    element="文章内容",
    ref="article.content",
    function="(element) => element.innerText"
)
```

### 7. 网络监控

#### 基础网络捕获
```python
# 开始捕获（不含响应体）
await mcp__playwright_mcp__browser_network_capture_start(
    url="https://example.com"  # 可选，指定要监控的URL
)

# 执行操作...

# 停止并获取网络请求
requests = await mcp__playwright_mcp__browser_network_capture_stop()

# 返回结构:
# [
#   {
#     "url": "https://api.example.com/data",
#     "method": "GET",
#     "status": 200,
#     "headers": {...}
#   },
#   ...
# ]
```

#### 高级网络调试（含响应体）
```python
# 开始调试模式（使用Chrome Debugger API）
await mcp__playwright_mcp__browser_network_debugger_start(
    url="https://example.com"
)

# 执行操作...

# 停止并获取完整网络数据
network_data = await mcp__playwright_mcp__browser_network_debugger_stop()

# 返回结构包含:
# [
#   {
#     "url": "https://api.example.com/data",
#     "method": "POST",
#     "status": 200,
#     "requestHeaders": {...},
#     "responseHeaders": {...},
#     "requestBody": "{...}",
#     "responseBody": "{...}"  # 完整响应体
#   },
#   ...
# ]
```

#### 获取历史网络请求
```python
# 获取页面加载后的所有网络请求
requests = await mcp__playwright_mcp__browser_network_requests()
```

### 8. 控制台监控

```python
# 获取所有控制台消息
all_logs = await mcp__playwright_mcp__browser_console_messages(
    includeExceptions=True,
    maxMessages=100
)

# 仅获取错误消息
errors = await mcp__playwright_mcp__browser_console_messages(
    onlyErrors=True
)

# 从指定URL获取控制台
logs = await mcp__playwright_mcp__browser_console_messages(
    url="https://example.com"
)

# 返回结构:
# [
#   {
#     "type": "error",
#     "text": "Uncaught TypeError: ...",
#     "location": {
#       "url": "https://example.com/script.js",
#       "lineNumber": 42
#     }
#   },
#   ...
# ]
```

### 9. 等待机制

```python
# 等待文本出现
await mcp__playwright_mcp__browser_wait_for(
    text="加载完成"
)

# 等待文本消失
await mcp__playwright_mcp__browser_wait_for(
    textGone="正在加载..."
)

# 等待指定时间
await mcp__playwright_mcp__browser_wait_for(
    time=3  # 等待3秒
)
```

### 10. 浏览器安装

```python
# 安装配置的浏览器（首次使用时）
await mcp__playwright_mcp__browser_install()
```

---

## 使用模式

### 模式1: 深度网页爬虫

**场景**: 爬取需要JavaScript渲染的动态网站

```python
async def deep_crawl_website(url: str, max_pages: int = 10):
    """深度爬取网站内容"""

    visited = set()
    to_visit = [url]
    results = []

    while to_visit and len(visited) < max_pages:
        current_url = to_visit.pop(0)

        if current_url in visited:
            continue

        # 1. 导航到页面
        await mcp__playwright_mcp__browser_navigate(url=current_url)

        # 2. 等待页面加载
        await mcp__playwright_mcp__browser_wait_for(time=2)

        # 3. 获取页面内容
        content = await mcp__playwright_mcp__chrome_get_web_content(
            textContent=True
        )

        # 4. 截图存档
        await mcp__playwright_mcp__browser_take_screenshot(
            filename=f"crawl_{len(visited)}.png",
            fullPage=True
        )

        # 5. 提取链接
        links = await mcp__playwright_mcp__browser_evaluate(
            function="""() => {
                return Array.from(document.querySelectorAll('a'))
                    .map(a => a.href)
                    .filter(href => href.startsWith(window.location.origin));
            }"""
        )

        # 6. 保存结果
        results.append({
            "url": current_url,
            "content": content,
            "links_count": len(links)
        })

        # 7. 添加新链接到待访问列表
        to_visit.extend([link for link in links if link not in visited])
        visited.add(current_url)

        print(f"已爬取: {current_url} ({len(visited)}/{max_pages})")

    return results

# 使用示例
crawled_data = await deep_crawl_website(
    url="https://example.com",
    max_pages=50
)
```

### 模式2: 表单自动化提交

**场景**: 自动填写并提交在线表单

```python
async def auto_fill_registration_form(user_data: dict):
    """自动填写注册表单"""

    # 1. 导航到注册页面
    await mcp__playwright_mcp__browser_navigate(
        url="https://example.com/register"
    )

    # 2. 批量填写表单字段
    await mcp__playwright_mcp__browser_fill_form(
        fields=[
            {
                "name": "用户名",
                "type": "textbox",
                "ref": "input[name='username']",
                "value": user_data["username"]
            },
            {
                "name": "邮箱",
                "type": "textbox",
                "ref": "input[name='email']",
                "value": user_data["email"]
            },
            {
                "name": "密码",
                "type": "textbox",
                "ref": "input[name='password']",
                "value": user_data["password"]
            },
            {
                "name": "国家",
                "type": "combobox",
                "ref": "select[name='country']",
                "value": user_data["country"]
            },
            {
                "name": "同意条款",
                "type": "checkbox",
                "ref": "input[name='terms']",
                "value": "true"
            }
        ]
    )

    # 3. 上传头像（如果需要）
    if "avatar_path" in user_data:
        await mcp__playwright_mcp__browser_click(
            element="上传按钮",
            ref="button#upload-avatar"
        )
        await mcp__playwright_mcp__browser_file_upload(
            paths=[user_data["avatar_path"]]
        )

    # 4. 提交表单
    await mcp__playwright_mcp__browser_click(
        element="提交按钮",
        ref="button[type='submit']"
    )

    # 5. 等待成功消息
    await mcp__playwright_mcp__browser_wait_for(
        text="注册成功"
    )

    # 6. 截图确认
    await mcp__playwright_mcp__browser_take_screenshot(
        filename="registration_success.png"
    )

    print("✅ 注册表单提交成功")

# 使用示例
await auto_fill_registration_form({
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "country": "CN",
    "avatar_path": "/path/to/avatar.jpg"
})
```

### 模式3: API接口逆向分析

**场景**: 监控网页的API调用，分析接口参数

```python
async def reverse_engineer_api(url: str, action_description: str):
    """逆向分析网页API调用"""

    # 1. 启动网络调试模式
    await mcp__playwright_mcp__browser_network_debugger_start(
        url=url
    )

    # 2. 导航到页面
    await mcp__playwright_mcp__browser_navigate(url=url)

    # 3. 执行触发API调用的操作
    print(f"执行操作: {action_description}")
    # 例如: 点击加载更多按钮
    await mcp__playwright_mcp__browser_click(
        element="加载更多",
        ref="button.load-more"
    )

    # 4. 等待请求完成
    await mcp__playwright_mcp__browser_wait_for(time=3)

    # 5. 停止监控并获取网络数据
    network_data = await mcp__playwright_mcp__browser_network_debugger_stop()

    # 6. 分析API调用
    api_calls = []
    for request in network_data:
        if "/api/" in request["url"]:
            api_calls.append({
                "url": request["url"],
                "method": request["method"],
                "request_headers": request.get("requestHeaders", {}),
                "request_body": request.get("requestBody", ""),
                "response_status": request["status"],
                "response_body": request.get("responseBody", "")
            })

    # 7. 保存分析结果
    with open("api_analysis.json", 'w') as f:
        json.dump(api_calls, f, indent=2, ensure_ascii=False)

    print(f"✅ 捕获到 {len(api_calls)} 个API调用")
    return api_calls

# 使用示例
api_data = await reverse_engineer_api(
    url="https://example.com/products",
    action_description="点击加载更多商品"
)
```

### 模式4: 端到端测试

**场景**: 自动化测试Web应用流程

```python
async def e2e_test_login_flow():
    """端到端测试登录流程"""

    test_results = []

    try:
        # 1. 导航到登录页面
        await mcp__playwright_mcp__browser_navigate(
            url="https://example.com/login"
        )
        test_results.append({"step": "导航", "status": "✅"})

        # 2. 填写登录表单
        await mcp__playwright_mcp__browser_type(
            element="邮箱输入框",
            ref="input[name='email']",
            text="test@example.com"
        )

        await mcp__playwright_mcp__browser_type(
            element="密码输入框",
            ref="input[name='password']",
            text="TestPassword123!"
        )
        test_results.append({"step": "填写表单", "status": "✅"})

        # 3. 提交登录
        await mcp__playwright_mcp__browser_click(
            element="登录按钮",
            ref="button[type='submit']"
        )

        # 4. 等待跳转
        await mcp__playwright_mcp__browser_wait_for(
            text="欢迎回来"
        )
        test_results.append({"step": "登录成功", "status": "✅"})

        # 5. 验证用户信息
        user_name = await mcp__playwright_mcp__browser_evaluate(
            function="() => document.querySelector('.user-name').textContent"
        )

        if user_name:
            test_results.append({"step": "验证用户名", "status": "✅"})
        else:
            test_results.append({"step": "验证用户名", "status": "❌"})

        # 6. 截图验证
        await mcp__playwright_mcp__browser_take_screenshot(
            filename="login_success.png"
        )

        # 7. 测试登出
        await mcp__playwright_mcp__browser_click(
            element="登出按钮",
            ref="button#logout"
        )

        await mcp__playwright_mcp__browser_wait_for(
            text="您已成功登出"
        )
        test_results.append({"step": "登出", "status": "✅"})

    except Exception as e:
        test_results.append({"step": "测试失败", "status": "❌", "error": str(e)})

    # 输出测试报告
    print("\n=== 测试报告 ===")
    for result in test_results:
        print(f"{result['step']}: {result['status']}")

    return test_results

# 运行测试
test_report = await e2e_test_login_flow()
```

### 模式5: 批量数据采集

**场景**: 批量采集电商商品数据

```python
async def batch_collect_products(category_url: str, max_products: int = 50):
    """批量采集商品数据"""

    products = []

    # 1. 导航到分类页面
    await mcp__playwright_mcp__browser_navigate(url=category_url)

    # 2. 滚动加载更多商品
    for _ in range(5):  # 滚动5次
        await mcp__playwright_mcp__browser_evaluate(
            function="() => window.scrollTo(0, document.body.scrollHeight)"
        )
        await mcp__playwright_mcp__browser_wait_for(time=2)

    # 3. 提取商品列表
    product_elements = await mcp__playwright_mcp__browser_snapshot()

    # 4. 获取商品详细信息
    product_data = await mcp__playwright_mcp__browser_evaluate(
        function="""() => {
            const items = document.querySelectorAll('.product-item');
            return Array.from(items).slice(0, 50).map(item => ({
                title: item.querySelector('.title')?.textContent,
                price: item.querySelector('.price')?.textContent,
                image: item.querySelector('img')?.src,
                url: item.querySelector('a')?.href
            }));
        }"""
    )

    # 5. 访问每个商品详情页
    for i, product in enumerate(product_data[:max_products]):
        try:
            # 导航到详情页
            await mcp__playwright_mcp__browser_navigate(url=product["url"])
            await mcp__playwright_mcp__browser_wait_for(time=1)

            # 获取详细描述
            description = await mcp__playwright_mcp__browser_evaluate(
                function="() => document.querySelector('.description')?.textContent"
            )

            # 截图
            await mcp__playwright_mcp__browser_take_screenshot(
                filename=f"product_{i}.png"
            )

            # 保存完整数据
            products.append({
                **product,
                "description": description,
                "screenshot": f"product_{i}.png"
            })

            print(f"已采集: {product['title']} ({i+1}/{max_products})")

            # 返回列表页
            await mcp__playwright_mcp__browser_navigate_back()
            await mcp__playwright_mcp__browser_wait_for(time=1)

        except Exception as e:
            print(f"采集失败: {product['title']} - {e}")

    # 6. 保存数据
    with open("products_data.json", 'w') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    print(f"\n✅ 共采集 {len(products)} 个商品")
    return products

# 使用示例
products = await batch_collect_products(
    category_url="https://example.com/category/electronics",
    max_products=100
)
```

---

## 最佳实践

### 1. 等待策略

```python
# ✅ 推荐: 等待特定文本出现
await mcp__playwright_mcp__browser_wait_for(
    text="加载完成"
)

# ⚠️ 谨慎使用: 固定时间等待
await mcp__playwright_mcp__browser_wait_for(time=3)

# ✅ 推荐: 等待元素可见后再操作
await mcp__playwright_mcp__browser_wait_for(text="提交")
await mcp__playwright_mcp__browser_click(
    element="提交按钮",
    ref="button[type='submit']"
)
```

### 2. 错误处理

```python
# ✅ 推荐: 使用try-except处理异常
try:
    await mcp__playwright_mcp__browser_click(
        element="可能不存在的按钮",
        ref=".optional-button"
    )
except Exception as e:
    print(f"按钮不存在，跳过: {e}")
    # 继续执行其他操作

# ✅ 推荐: 截图记录错误现场
try:
    await mcp__playwright_mcp__browser_fill_form(fields=form_data)
except Exception as e:
    await mcp__playwright_mcp__browser_take_screenshot(
        filename="error_screenshot.png"
    )
    raise
```

### 3. 性能优化

```python
# ✅ 推荐: 禁用不必要的资源加载
# 注: Playwright MCP默认配置已优化

# ✅ 推荐: 复用浏览器实例
# 连续操作时不要频繁关闭/重新打开浏览器

# ✅ 推荐: 合理使用快照vs截图
# - 操作前: 使用snapshot获取元素信息
# - 验证时: 使用screenshot保存视觉证据
```

### 4. 选择器策略

```python
# ✅ 推荐: 使用稳定的选择器
ref="button[data-testid='submit-btn']"  # data-testid属性
ref="button#login-button"  # ID选择器

# ⚠️ 避免: 使用易变的选择器
ref="body > div:nth-child(3) > button"  # 位置选择器
ref=".btn-primary.btn-lg.mt-3"  # 过多class组合
```

### 5. 网络监控

```python
# ✅ 推荐: 需要响应体时使用debugger模式
await mcp__playwright_mcp__browser_network_debugger_start()
# ... 执行操作
data = await mcp__playwright_mcp__browser_network_debugger_stop()

# ✅ 推荐: 只需请求头时使用capture模式（更轻量）
await mcp__playwright_mcp__browser_network_capture_start()
# ... 执行操作
requests = await mcp__playwright_mcp__browser_network_capture_stop()
```

---

## 常见问题

### 1. 浏览器未安装

**问题**: 首次使用时提示浏览器未安装

```python
# ✅ 解决方案: 运行安装命令
await mcp__playwright_mcp__browser_install()
```

### 2. 元素选择失败

**问题**: 无法找到元素或点击失败

```python
# ❌ 错误示例
await mcp__playwright_mcp__browser_click(
    element="按钮",
    ref=".button"  # 选择器可能不准确
)

# ✅ 解决方案1: 先获取快照确认选择器
snapshot = await mcp__playwright_mcp__browser_snapshot()
# 检查snapshot中的元素结构

# ✅ 解决方案2: 等待元素出现
await mcp__playwright_mcp__browser_wait_for(text="按钮文本")
await mcp__playwright_mcp__browser_click(...)

# ✅ 解决方案3: 使用更精确的选择器
await mcp__playwright_mcp__browser_click(
    element="提交按钮",
    ref="button[type='submit'][data-testid='submit']"
)
```

### 3. 页面加载超时

**问题**: 页面加载时间过长导致超时

```python
# ❌ 问题场景
await mcp__playwright_mcp__browser_navigate(
    url="https://slow-website.com"
)  # 可能超时

# ✅ 解决方案: 增加等待时间
await mcp__playwright_mcp__browser_navigate(
    url="https://slow-website.com"
)
await mcp__playwright_mcp__browser_wait_for(time=10)  # 额外等待
```

### 4. 对话框阻塞

**问题**: alert/confirm对话框阻塞操作

```python
# ✅ 解决方案: 提前设置对话框处理
# 在可能出现对话框的操作前设置处理器

await mcp__playwright_mcp__browser_click(
    element="删除按钮",
    ref="button.delete"
)

# 立即处理确认对话框
await mcp__playwright_mcp__browser_handle_dialog(
    accept=True
)
```

### 5. 动态内容加载

**问题**: 内容是JavaScript动态加载的

```python
# ❌ 错误: 立即获取内容
await mcp__playwright_mcp__browser_navigate(url="...")
content = await mcp__playwright_mcp__chrome_get_web_content()  # 内容可能未加载

# ✅ 正确: 等待内容加载完成
await mcp__playwright_mcp__browser_navigate(url="...")
await mcp__playwright_mcp__browser_wait_for(text="加载完成标志")
content = await mcp__playwright_mcp__chrome_get_web_content()
```

---

## 集成示例

### 示例1: 完整的登录->操作->登出流程

```python
async def complete_user_workflow():
    """完整的用户操作流程示例"""

    try:
        # === 阶段1: 登录 ===
        print(">>> 阶段1: 用户登录")
        await mcp__playwright_mcp__browser_navigate(
            url="https://app.example.com/login"
        )

        await mcp__playwright_mcp__browser_fill_form(
            fields=[
                {
                    "name": "邮箱",
                    "type": "textbox",
                    "ref": "input[name='email']",
                    "value": "user@example.com"
                },
                {
                    "name": "密码",
                    "type": "textbox",
                    "ref": "input[name='password']",
                    "value": "SecurePass123!"
                }
            ]
        )

        await mcp__playwright_mcp__browser_click(
            element="登录按钮",
            ref="button[type='submit']"
        )

        await mcp__playwright_mcp__browser_wait_for(text="仪表板")
        print("✅ 登录成功")

        # === 阶段2: 执行业务操作 ===
        print("\n>>> 阶段2: 执行业务操作")

        # 导航到设置页面
        await mcp__playwright_mcp__browser_click(
            element="设置菜单",
            ref="a[href='/settings']"
        )

        await mcp__playwright_mcp__browser_wait_for(text="账户设置")

        # 修改用户资料
        await mcp__playwright_mcp__browser_type(
            element="昵称输入框",
            ref="input[name='nickname']",
            text="新昵称"
        )

        # 上传头像
        await mcp__playwright_mcp__browser_click(
            element="上传头像",
            ref="button#upload-avatar"
        )

        await mcp__playwright_mcp__browser_file_upload(
            paths=["/path/to/avatar.jpg"]
        )

        # 保存更改
        await mcp__playwright_mcp__browser_click(
            element="保存按钮",
            ref="button.save-changes"
        )

        await mcp__playwright_mcp__browser_wait_for(text="保存成功")
        print("✅ 资料更新成功")

        # === 阶段3: 数据导出 ===
        print("\n>>> 阶段3: 导出数据")

        await mcp__playwright_mcp__browser_click(
            element="导出数据",
            ref="button.export-data"
        )

        # 处理下载确认对话框
        await mcp__playwright_mcp__browser_handle_dialog(accept=True)

        await mcp__playwright_mcp__browser_wait_for(time=3)
        print("✅ 数据导出完成")

        # === 阶段4: 登出 ===
        print("\n>>> 阶段4: 用户登出")

        await mcp__playwright_mcp__browser_click(
            element="登出按钮",
            ref="button#logout"
        )

        await mcp__playwright_mcp__browser_wait_for(text="您已成功登出")
        print("✅ 登出成功")

        # === 最终验证截图 ===
        await mcp__playwright_mcp__browser_take_screenshot(
            filename="workflow_complete.png",
            fullPage=True
        )

        return {"status": "success", "message": "工作流执行完成"}

    except Exception as e:
        # 错误处理
        await mcp__playwright_mcp__browser_take_screenshot(
            filename="workflow_error.png"
        )
        return {"status": "failed", "error": str(e)}

# 执行完整流程
result = await complete_user_workflow()
print(f"\n最终结果: {result}")
```

### 示例2: 竞品价格监控系统

```python
async def monitor_competitor_prices(competitors: list):
    """监控竞品价格变动"""

    price_data = []

    for competitor in competitors:
        try:
            # 1. 访问竞品页面
            await mcp__playwright_mcp__browser_navigate(
                url=competitor["product_url"]
            )

            # 2. 等待价格加载
            await mcp__playwright_mcp__browser_wait_for(
                text=competitor.get("price_indicator", "¥")
            )

            # 3. 提取价格信息
            price_info = await mcp__playwright_mcp__browser_evaluate(
                function=f"""() => {{
                    const priceElement = document.querySelector('{competitor["price_selector"]}');
                    return {{
                        price: priceElement?.textContent,
                        currency: '¥',
                        timestamp: new Date().toISOString()
                    }};
                }}"""
            )

            # 4. 截图存档
            screenshot_name = f"competitor_{competitor['name']}.png"
            await mcp__playwright_mcp__browser_take_screenshot(
                element="价格区域",
                ref=competitor["price_selector"],
                filename=screenshot_name
            )

            # 5. 保存数据
            price_data.append({
                "competitor": competitor["name"],
                "url": competitor["product_url"],
                "price": price_info["price"],
                "timestamp": price_info["timestamp"],
                "screenshot": screenshot_name
            })

            print(f"✅ 已采集: {competitor['name']} - {price_info['price']}")

        except Exception as e:
            print(f"❌ 采集失败: {competitor['name']} - {e}")

    # 6. 生成报告
    with open("price_monitor_report.json", 'w') as f:
        json.dump(price_data, f, indent=2, ensure_ascii=False)

    return price_data

# 使用示例
competitors = [
    {
        "name": "竞品A",
        "product_url": "https://competitor-a.com/product/123",
        "price_selector": ".price-value"
    },
    {
        "name": "竞品B",
        "product_url": "https://competitor-b.com/item/456",
        "price_selector": "#product-price"
    }
]

price_report = await monitor_competitor_prices(competitors)
```

### 示例3: 社交媒体自动发布

```python
async def auto_post_to_social_media(post_data: dict):
    """自动发布到社交媒体"""

    # 1. 登录账户
    await mcp__playwright_mcp__browser_navigate(
        url="https://social-platform.com/login"
    )

    await mcp__playwright_mcp__browser_fill_form(
        fields=[
            {
                "name": "用户名",
                "type": "textbox",
                "ref": "input[name='username']",
                "value": post_data["credentials"]["username"]
            },
            {
                "name": "密码",
                "type": "textbox",
                "ref": "input[name='password']",
                "value": post_data["credentials"]["password"]
            }
        ]
    )

    await mcp__playwright_mcp__browser_click(
        element="登录",
        ref="button[type='submit']"
    )

    await mcp__playwright_mcp__browser_wait_for(text="首页")

    # 2. 创建新帖子
    await mcp__playwright_mcp__browser_click(
        element="创建帖子",
        ref="button.create-post"
    )

    # 3. 填写帖子内容
    await mcp__playwright_mcp__browser_type(
        element="帖子内容",
        ref="textarea[name='content']",
        text=post_data["content"]
    )

    # 4. 上传图片
    if "images" in post_data:
        await mcp__playwright_mcp__browser_click(
            element="上传图片",
            ref="button.upload-images"
        )

        await mcp__playwright_mcp__browser_file_upload(
            paths=post_data["images"]
        )

        await mcp__playwright_mcp__browser_wait_for(text="上传完成")

    # 5. 添加话题标签
    if "hashtags" in post_data:
        for tag in post_data["hashtags"]:
            await mcp__playwright_mcp__browser_type(
                element="话题标签",
                ref="input.hashtag-input",
                text=f"#{tag}",
                submit=False
            )
            await mcp__playwright_mcp__browser_press_key(key="Enter")

    # 6. 发布
    await mcp__playwright_mcp__browser_click(
        element="发布按钮",
        ref="button.publish"
    )

    await mcp__playwright_mcp__browser_wait_for(text="发布成功")

    # 7. 获取帖子链接
    post_url = await mcp__playwright_mcp__browser_evaluate(
        function="() => window.location.href"
    )

    # 8. 截图确认
    await mcp__playwright_mcp__browser_take_screenshot(
        filename="post_published.png"
    )

    print(f"✅ 帖子已发布: {post_url}")
    return {"status": "published", "url": post_url}

# 使用示例
result = await auto_post_to_social_media({
    "credentials": {
        "username": "my_account",
        "password": "secure_password"
    },
    "content": "今天分享一个有趣的发现...",
    "images": ["/path/to/image1.jpg", "/path/to/image2.jpg"],
    "hashtags": ["技术分享", "Playwright", "自动化"]
})
```

---

## 提示与技巧

### 1. 调试技巧

```python
# 使用快照检查页面结构
snapshot = await mcp__playwright_mcp__browser_snapshot()
print(json.dumps(snapshot, indent=2, ensure_ascii=False))

# 使用控制台日志辅助调试
logs = await mcp__playwright_mcp__browser_console_messages()
for log in logs:
    print(f"[{log['type']}] {log['text']}")

# 每步操作后截图
await mcp__playwright_mcp__browser_take_screenshot(
    filename=f"step_{step_number}.png"
)
```

### 2. 反爬虫对策

```python
# Playwright自带反检测机制
# 额外技巧:

# 1. 随机等待时间
import random
await mcp__playwright_mcp__browser_wait_for(
    time=random.uniform(1, 3)
)

# 2. 模拟人类行为
await mcp__playwright_mcp__browser_hover(
    element="链接",
    ref="a.product-link"
)
await mcp__playwright_mcp__browser_wait_for(time=0.5)
await mcp__playwright_mcp__browser_click(
    element="链接",
    ref="a.product-link"
)

# 3. 逐字符输入
await mcp__playwright_mcp__browser_type(
    element="搜索框",
    ref="input[type='search']",
    text="关键词",
    slowly=True  # 触发每个字符的键盘事件
)
```

### 3. 数据持久化

```python
# 定期保存进度
progress_data = []

for i, item in enumerate(items):
    # 处理item...
    progress_data.append(result)

    # 每10个保存一次
    if (i + 1) % 10 == 0:
        with open(f"progress_{i+1}.json", 'w') as f:
            json.dump(progress_data, f, indent=2)

    # 每50个截图一次
    if (i + 1) % 50 == 0:
        await mcp__playwright_mcp__browser_take_screenshot(
            filename=f"checkpoint_{i+1}.png"
        )
```

### 4. 并发控制

```python
# Playwright实例不适合并发
# 如需并发,使用多个独立的Playwright实例或进程

import asyncio

async def crawl_single_page(url):
    # 每个协程使用独立的浏览器会话
    await mcp__playwright_mcp__browser_navigate(url=url)
    # ... 其他操作
    return result

# 顺序执行（推荐）
results = []
for url in urls:
    result = await crawl_single_page(url)
    results.append(result)
```

### 5. 性能监控

```python
import time

# 记录操作耗时
start = time.time()

await mcp__playwright_mcp__browser_navigate(url="...")
await mcp__playwright_mcp__browser_wait_for(text="加载完成")

elapsed = time.time() - start
print(f"页面加载耗时: {elapsed:.2f}秒")

# 监控网络性能
network_data = await mcp__playwright_mcp__browser_network_requests()
total_size = sum(req.get("size", 0) for req in network_data)
print(f"总传输量: {total_size / 1024:.2f} KB")
```

---

## 相关资源

- **Playwright官方文档**: https://playwright.dev
- **Playwright Python文档**: https://playwright.dev/python/
- **选择器指南**: https://playwright.dev/docs/selectors
- **调试指南**: https://playwright.dev/docs/debug
- **最佳实践**: https://playwright.dev/docs/best-practices
- **API参考**: https://playwright.dev/docs/api/class-playwright

---

**技能包版本**: 1.0.0
**Playwright版本**: 兼容Playwright 1.40+
**更新时间**: 2025-10-23
**维护状态**: ✅ 活跃维护
