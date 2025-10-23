---
name: chrome-mcp
description: Chrome browser automation with 20+ tools for navigation, interaction, screenshot, network capture, history, bookmarks, and script injection. Use for web scraping, testing, automation, and data collection tasks.
---

# Chrome-MCP Skill

基于chrome-mcp的完整浏览器自动化能力包，提供页面导航、元素交互、内容抓取、网络监控、历史管理等20+核心功能。

## Quick Start

### 基础导航与截图

```python
# 1. 导航到网页
await chrome_navigate(url="https://example.com", width=1920, height=1080)

# 2. 获取页面内容
content = await chrome_get_web_content(textContent=True)

# 3. 截图
await chrome_screenshot(
    fullPage=True,
    savePng=True,
    name="example_screenshot"
)
```

### 元素交互

```python
# 1. 获取可交互元素
elements = await chrome_get_interactive_elements(
    selector="button.submit"
)

# 2. 点击元素
await chrome_click_element(
    selector="button.submit",
    waitForNavigation=True
)

# 3. 填写表单
await chrome_fill_or_select(
    selector="input#username",
    value="user@example.com"
)
```

### 网络请求监控

```python
# 1. 开始捕获网络请求
await chrome_network_debugger_start(url="https://api.example.com")

# 2. 执行操作（触发API调用）
await chrome_click_element(selector="button.load-data")

# 3. 停止捕获并获取请求
requests = await chrome_network_debugger_stop()
```

## Core Capabilities

### 1. 页面导航与窗口管理

#### 导航控制

```python
# 导航到URL
await chrome_navigate(
    url="https://example.com",
    width=1920,
    height=1080,
    newWindow=False  # 在当前窗口打开
)

# 刷新页面
await chrome_navigate(refresh=True)

# 前进/后退
await chrome_go_back_or_forward(isForward=False)  # 后退
await chrome_go_back_or_forward(isForward=True)   # 前进
```

#### 窗口与标签管理

```python
# 获取所有窗口和标签
windows_tabs = await get_windows_and_tabs()

# 关闭标签
await chrome_close_tabs(tabIds=[123, 456])  # 关闭指定标签
await chrome_close_tabs(url="https://example.com")  # 关闭匹配URL的标签
await chrome_close_tabs()  # 关闭当前标签
```

### 2. 内容获取与截图

#### 获取页面内容

```python
# 获取文本内容（推荐）
text_content = await chrome_get_web_content(textContent=True)

# 获取HTML内容
html_content = await chrome_get_web_content(htmlContent=True)

# 获取特定元素内容
element_content = await chrome_get_web_content(
    selector="div.content",
    textContent=True
)

# 从URL获取内容
content = await chrome_get_web_content(
    url="https://example.com",
    textContent=True
)
```

#### 页面截图

```python
# 全页截图（PNG）
await chrome_screenshot(
    fullPage=True,
    savePng=True,
    name="fullpage_screenshot"
)

# 视口截图（Base64）
screenshot_data = await chrome_screenshot(
    fullPage=False,
    storeBase64=True,
    width=1280,
    height=720
)

# 元素截图
await chrome_screenshot(
    selector="div.product-card",
    savePng=True,
    name="product_screenshot"
)
```

### 3. 元素交互

#### 查找元素

```python
# 获取所有可交互元素
all_elements = await chrome_get_interactive_elements()

# 通过选择器过滤
buttons = await chrome_get_interactive_elements(
    selector="button.action"
)

# 通过文本搜索（模糊匹配）
submit_buttons = await chrome_get_interactive_elements(
    textQuery="Submit"
)

# 包含坐标信息
elements_with_coords = await chrome_get_interactive_elements(
    includeCoordinates=True
)
```

#### 点击操作

```python
# 基础点击
await chrome_click_element(
    selector="button#submit",
    element="Submit Button"
)

# 等待导航完成
await chrome_click_element(
    selector="a.next-page",
    element="Next Page Link",
    waitForNavigation=True,
    timeout=10000
)

# 通过坐标点击
await chrome_click_element(
    coordinates={"x": 100, "y": 200}
)
```

#### 表单填写

```python
# 填写文本输入框
await chrome_fill_or_select(
    selector="input#username",
    value="user@example.com"
)

# 选择下拉选项
await chrome_fill_or_select(
    selector="select#country",
    value="China"
)
```

### 4. 键盘操作

```python
# 按单个键
await chrome_keyboard(keys="Enter")

# 组合键
await chrome_keyboard(keys="Ctrl+C")

# 按键序列
await chrome_keyboard(keys="A,B,C", delay=100)

# 在特定元素上输入
await chrome_keyboard(
    selector="input#search",
    keys="search term"
)
```

### 5. 网络请求监控

#### 使用Debugger API（带响应体）

```python
# 开始捕获
await chrome_network_debugger_start(
    url="https://example.com"  # 可选，指定要监控的页面
)

# 执行操作...
await chrome_click_element(selector="button.load-data")

# 停止并获取请求
network_data = await chrome_network_debugger_stop()
# network_data包含请求和响应的完整信息，包括响应体
```

#### 使用WebRequest API（无响应体）

```python
# 开始捕获
await chrome_network_capture_start(url="https://example.com")

# 执行操作...

# 停止并获取请求
requests = await chrome_network_capture_stop()
# requests包含请求头、状态码等信息，但不包含响应体
```

### 6. 浏览器历史管理

```python
# 搜索历史记录
history = await chrome_history(
    text="example",           # 搜索关键词
    startTime="1 week ago",   # 开始时间
    endTime="now",            # 结束时间
    maxResults=50             # 最大结果数
)

# 排除当前打开的标签
history = await chrome_history(
    text="github",
    excludeCurrentTabs=True
)

# 使用ISO时间格式
history = await chrome_history(
    startTime="2025-01-01",
    endTime="2025-10-23",
    maxResults=100
)
```

### 7. 书签管理

#### 搜索书签

```python
# 搜索所有书签
bookmarks = await chrome_bookmark_search(query="python")

# 限制结果数量
bookmarks = await chrome_bookmark_search(
    query="documentation",
    maxResults=20
)

# 在特定文件夹搜索
bookmarks = await chrome_bookmark_search(
    query="tutorial",
    folderPath="Programming/Python"
)
```

#### 添加书签

```python
# 添加当前页面
await chrome_bookmark_add(
    title="Example Page",
    parentId="Bookmarks Bar"
)

# 添加指定URL
await chrome_bookmark_add(
    url="https://example.com",
    title="Example Site",
    parentId="Work/Resources"
)

# 创建文件夹（如果不存在）
await chrome_bookmark_add(
    url="https://docs.python.org",
    title="Python Docs",
    parentId="Programming/Python",
    createFolder=True
)
```

#### 删除书签

```python
# 通过ID删除
await chrome_bookmark_delete(bookmarkId="123")

# 通过URL删除
await chrome_bookmark_delete(
    url="https://example.com",
    title="Example"  # 可选，帮助匹配
)
```

### 8. JavaScript执行

#### 注入脚本

```python
# 在ISOLATED世界执行（推荐）
await chrome_inject_script(
    type="ISOLATED",
    jsScript="""
        document.querySelector('h1').textContent = 'Modified Title';
    """
)

# 在MAIN世界执行（可访问页面全局变量）
await chrome_inject_script(
    type="MAIN",
    jsScript="""
        console.log(window.myApp);
    """,
    url="https://example.com"  # 可选，指定页面
)
```

#### 发送命令到注入脚本

```python
# 1. 先注入监听脚本
await chrome_inject_script(
    type="ISOLATED",
    jsScript="""
        window.addEventListener('customEvent', (event) => {
            console.log('Received:', event.detail);
            // 处理命令
        });
    """
)

# 2. 发送命令
await chrome_send_command_to_inject_script(
    eventName="customEvent",
    payload='{"action": "update", "data": "test"}',
    tabId=123  # 可选，默认当前标签
)
```

### 9. 控制台监控

```python
# 获取控制台消息
console_logs = await chrome_console(
    url="https://example.com",  # 可选，导航到指定页面
    includeExceptions=True,     # 包含异常
    maxMessages=100             # 最大消息数
)

# 仅获取当前页面的控制台
logs = await chrome_console(
    includeExceptions=False,
    maxMessages=50
)
```

### 10. 标签内容搜索

```python
# 在所有打开的标签中搜索内容
results = await search_tabs_content(query="API documentation")
```

### 11. 网络请求（带浏览器上下文）

```python
# 发送请求（使用浏览器的cookies和session）
response = await chrome_network_request(
    url="https://api.example.com/data",
    method="GET",
    headers={"Authorization": "Bearer token"},
    timeout=30000
)

# POST请求
response = await chrome_network_request(
    url="https://api.example.com/submit",
    method="POST",
    headers={"Content-Type": "application/json"},
    body='{"key": "value"}'
)
```

## Usage Patterns

### Pattern 1: 网页数据采集

```python
async def scrape_website(url: str) -> dict:
    """采集网页数据"""

    # 1. 导航到页面
    await chrome_navigate(url=url, width=1920, height=1080)

    # 2. 等待加载（通过键盘模拟等待）
    await chrome_keyboard(keys="")

    # 3. 获取页面内容
    content = await chrome_get_web_content(textContent=True)

    # 4. 截图存档
    await chrome_screenshot(
        fullPage=True,
        savePng=True,
        name=f"scrape_{int(time.time())}"
    )

    return {
        "url": url,
        "content": content,
        "timestamp": time.time()
    }
```

### Pattern 2: 自动化表单提交

```python
async def submit_form(form_data: dict):
    """自动化表单提交"""

    # 1. 导航到表单页面
    await chrome_navigate(url="https://example.com/form")

    # 2. 填写表单字段
    await chrome_fill_or_select(
        selector="input#name",
        value=form_data['name']
    )
    await chrome_fill_or_select(
        selector="input#email",
        value=form_data['email']
    )
    await chrome_fill_or_select(
        selector="select#country",
        value=form_data['country']
    )

    # 3. 提交表单
    await chrome_click_element(
        selector="button[type='submit']",
        element="Submit Button",
        waitForNavigation=True
    )

    # 4. 获取结果
    result = await chrome_get_web_content(textContent=True)
    return result
```

### Pattern 3: API请求监控

```python
async def monitor_api_calls(url: str, action_selector: str):
    """监控API调用"""

    # 1. 导航到页面
    await chrome_navigate(url=url)

    # 2. 开始网络监控
    await chrome_network_debugger_start()

    # 3. 执行触发API调用的操作
    await chrome_click_element(selector=action_selector)

    # 4. 等待请求完成
    await chrome_keyboard(keys="")  # 简单等待

    # 5. 停止监控并获取数据
    network_data = await chrome_network_debugger_stop()

    # 6. 分析API调用
    api_calls = [
        req for req in network_data
        if req['url'].startswith('https://api.')
    ]

    return api_calls
```

### Pattern 4: 批量书签管理

```python
async def organize_bookmarks(bookmarks_data: list):
    """批量整理书签"""

    # 1. 搜索现有书签
    existing = await chrome_bookmark_search(query="")

    # 2. 删除重复书签
    seen_urls = set()
    for bookmark in existing:
        if bookmark['url'] in seen_urls:
            await chrome_bookmark_delete(bookmarkId=bookmark['id'])
        else:
            seen_urls.add(bookmark['url'])

    # 3. 添加新书签
    for item in bookmarks_data:
        await chrome_bookmark_add(
            url=item['url'],
            title=item['title'],
            parentId=item['folder'],
            createFolder=True
        )
```

### Pattern 5: 浏览历史分析

```python
async def analyze_browsing_history(days: int = 7):
    """分析浏览历史"""

    # 1. 获取历史记录
    history = await chrome_history(
        startTime=f"{days} days ago",
        endTime="now",
        maxResults=1000
    )

    # 2. 按域名分组
    domains = {}
    for entry in history:
        domain = extract_domain(entry['url'])
        domains[domain] = domains.get(domain, 0) + 1

    # 3. 生成报告
    top_sites = sorted(
        domains.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    return {
        "total_visits": len(history),
        "unique_domains": len(domains),
        "top_sites": top_sites
    }
```

## Best Practices

### 1. 页面加载等待

```python
# ✓ 推荐：点击后等待导航
await chrome_click_element(
    selector="a.link",
    waitForNavigation=True,
    timeout=10000
)

# ✗ 不推荐：点击后立即操作
await chrome_click_element(selector="a.link")
await chrome_get_web_content()  # 可能获取旧页面内容
```

### 2. 元素选择器优先级

```python
# ✓ 推荐：使用ID选择器（最稳定）
await chrome_click_element(selector="button#submit")

# ✓ 可接受：使用类选择器
await chrome_click_element(selector="button.btn-primary")

# ✗ 不推荐：使用复杂的层级选择器
await chrome_click_element(
    selector="div.container > div:nth-child(2) > button"
)
```

### 3. 网络监控选择

```python
# ✓ 需要响应体：使用Debugger API
await chrome_network_debugger_start()
# ... 执行操作
data = await chrome_network_debugger_stop()

# ✓ 仅需请求信息：使用WebRequest API（更轻量）
await chrome_network_capture_start()
# ... 执行操作
requests = await chrome_network_capture_stop()
```

### 4. 截图质量控制

```python
# ✓ 推荐：全页PNG截图（高质量）
await chrome_screenshot(
    fullPage=True,
    savePng=True,
    name="screenshot"
)

# ✓ 需要嵌入：使用Base64
screenshot_data = await chrome_screenshot(
    fullPage=False,
    storeBase64=True
)

# ✗ 避免：同时保存和返回Base64（冗余）
await chrome_screenshot(
    savePng=True,
    storeBase64=True
)
```

### 5. 错误处理

```python
try:
    await chrome_click_element(
        selector="button.submit",
        timeout=5000
    )
except TimeoutError:
    # 元素未找到或不可点击
    print("Element not found or not clickable")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Common Issues

### Issue 1: 元素点击失败

**原因**: 元素被遮挡、不可见或选择器错误

**解决方案**:
```python
# 1. 先获取可交互元素验证
elements = await chrome_get_interactive_elements(
    selector="button.submit"
)
if not elements:
    print("Element not found or not interactive")

# 2. 使用坐标点击（最后手段）
await chrome_click_element(
    coordinates={"x": 500, "y": 300}
)
```

### Issue 2: 页面内容未加载完成

**原因**: 异步加载或动态内容渲染延迟

**解决方案**:
```python
# 1. 点击时等待导航
await chrome_click_element(
    selector="a.link",
    waitForNavigation=True,
    timeout=10000
)

# 2. 手动延迟
await chrome_keyboard(keys="")  # 简单延迟
# 或使用time.sleep(2)
```

### Issue 3: 网络请求未捕获

**原因**: 监控启动时机不对或请求已完成

**解决方案**:
```python
# ✓ 正确顺序：先启动监控，再触发请求
await chrome_network_debugger_start()
await chrome_click_element(selector="button.load")
data = await chrome_network_debugger_stop()

# ✗ 错误顺序
await chrome_click_element(selector="button.load")
await chrome_network_debugger_start()  # 太晚了
```

## Integration Examples

### Example 1: 与Lark-MCP集成（通知采集结果）

```python
# 采集数据
content = await chrome_get_web_content(
    url="https://competitor.com/products",
    textContent=True
)

# 发送到飞书
await lark_send_message(
    chat_id="oc_xxx",
    message=f"竞品数据采集完成:\n{content[:500]}"
)
```

### Example 2: 与COS-MCP集成（存储截图）

```python
# 截图
await chrome_screenshot(
    fullPage=True,
    savePng=True,
    name="webpage_screenshot"
)

# 上传到COS
await cos_upload_file(
    file_path="webpage_screenshot.png",
    target_dir="screenshots/competitors"
)
```

### Example 3: 与Supabase-MCP集成（存储数据）

```python
# 采集数据
data = await scrape_website("https://example.com")

# 存储到Supabase
await supabase_insert(
    table="scraped_data",
    data={
        "url": data['url'],
        "content": data['content'],
        "scraped_at": data['timestamp']
    }
)
```

## Tips & Tricks

1. **元素定位**: 优先使用ID选择器，其次是类选择器
2. **等待策略**: 对于动态内容，使用`waitForNavigation`
3. **网络监控**: 需要响应体时使用Debugger API，否则用WebRequest
4. **截图格式**: PNG用于高质量，JPEG用于文件大小
5. **历史搜索**: 使用相对时间（"1 week ago"）更灵活
6. **书签管理**: 使用`createFolder=True`自动创建文件夹层级
7. **脚本注入**: ISOLATED世界更安全，MAIN世界可访问页面变量
8. **控制台监控**: 用于调试和错误收集
9. **标签管理**: 定期清理不需要的标签释放资源
10. **错误处理**: 总是使用try-except包装操作

## Chrome-MCP Tools Reference

详见[Chrome-MCP工具参考](reference.md)（待补充）

## Version History

- **v1.0.0** (2025-10-23): 初始版本
  - 20+核心工具完整支持
  - 页面导航与窗口管理
  - 元素交互与表单填写
  - 网络请求监控
  - 历史与书签管理
  - JavaScript执行
  - 控制台监控
