# Web Crawling Advanced - 扩展参考文档

> 详细的API文档、配置选项和高级用法

---

## 目录

1. [API完整参考](#api完整参考)
2. [高级配置](#高级配置)
3. [性能优化](#性能优化)
4. [常见问题](#常见问题)
5. [最佳实践](#最佳实践)

---

## API完整参考

### ZTLCrawler 类

#### 构造函数

```python
ZTLCrawler(
    crawler_type: Literal['beautifulsoup', 'playwright', 'adaptive'] = 'beautifulsoup',
    headless: bool = True,
    max_requests: int = 100,
    proxy_config: Optional[Dict] = None,
    retry_config: Optional[Dict] = None
)
```

**参数说明**:

- `crawler_type`: 爬虫引擎类型
  - `'beautifulsoup'`: HTTP + BeautifulSoup（快速，适合静态页面）
  - `'playwright'`: 完整浏览器自动化（功能完整，适合动态页面）
  - `'adaptive'`: 智能自适应（根据页面类型自动选择）

- `headless`: 无头模式（仅Playwright）
  - `True`: 后台运行，不显示浏览器界面
  - `False`: 显示浏览器界面，便于调试

- `max_requests`: 最大请求数限制
  - 防止爬取过多页面导致资源耗尽
  - 建议根据目标网站规模设置（10-1000）

- `proxy_config`: 代理配置（可选）
  ```python
  proxy_config = {
      'server': 'http://proxy.example.com:8080',
      'username': 'user',
      'password': 'pass'
  }
  ```

- `retry_config`: 重试配置（可选）
  ```python
  retry_config = {
      'max_retries': 3,
      'retry_delay': 1000  # 毫秒
  }
  ```

#### 核心方法

##### crawl()

```python
async def crawl(
    urls: List[str],
    handler: Callable,
    enqueue_links: bool = False
) -> List[Dict[str, Any]]
```

执行爬取任务。

**参数**:
- `urls`: 起始URL列表
- `handler`: 数据处理回调函数
- `enqueue_links`: 是否自动发现和爬取页面中的链接

**返回**:
- 采集结果列表

**Handler函数签名**:

BeautifulSoup模式:
```python
async def handler(context: BeautifulSoupCrawlingContext) -> Dict:
    # context.request: 请求对象
    # context.soup: BeautifulSoup对象
    # context.http_response: HTTP响应
    return {'key': 'value'}
```

Playwright模式:
```python
async def handler(context: PlaywrightCrawlingContext) -> Dict:
    # context.request: 请求对象
    # context.page: Playwright Page对象
    # context.browser_type: 浏览器类型
    return {'key': 'value'}
```

##### export_data()

```python
async def export_data(
    output_path: str,
    format: Literal['json', 'csv'] = 'json'
) -> str
```

导出采集数据到文件。

**参数**:
- `output_path`: 输出文件路径（自动创建目录）
- `format`: 导出格式（`'json'` 或 `'csv'`）

**返回**:
- 导出文件的绝对路径

##### get_stats()

```python
def get_stats() -> Dict[str, Any]
```

获取爬取统计信息。

**返回示例**:
```python
{
    'total_requests': 50,
    'successful_requests': 48,
    'failed_requests': 2,
    'start_time': datetime(...),
    'end_time': datetime(...),
    'duration_seconds': 125.5,
    'requests_per_second': 0.398
}
```

---

### 便捷函数

#### crawl_competitor_menu()

```python
async def crawl_competitor_menu(
    restaurant_url: str,
    platform: str = 'meituan'
) -> List[Dict]
```

快速采集竞品菜单数据。

**参数**:
- `restaurant_url`: 餐厅详情页URL
- `platform`: 平台类型（`'meituan'` 或 `'dianping'`）

**返回示例**:
```python
[{
    'url': 'https://...',
    'platform': 'meituan',
    'restaurant': '海底捞火锅',
    'dishes': [
        {'name': '毛肚', 'price': '38元'},
        {'name': '鸭血', 'price': '15元'},
        ...
    ],
    'crawled_at': '2025-10-21T10:30:00'
}]
```

#### crawl_reviews()

```python
async def crawl_reviews(
    restaurant_urls: List[str],
    max_reviews_per_restaurant: int = 50
) -> List[Dict]
```

批量采集餐厅评价。

**参数**:
- `restaurant_urls`: 餐厅URL列表
- `max_reviews_per_restaurant`: 每家餐厅最多采集评价数

**返回示例**:
```python
[{
    'url': 'https://...',
    'restaurant': '西贝莜面村',
    'reviews': [
        {
            'user': '张三',
            'rating': '5星',
            'content': '味道很好...'
        },
        ...
    ],
    'crawled_at': '2025-10-21T10:30:00'
}]
```

#### quick_crawl()

```python
async def quick_crawl(
    urls: List[str],
    selector: str,
    output_path: Optional[str] = None
) -> List[Dict]
```

快速采集指定CSS选择器的内容。

**参数**:
- `urls`: URL列表
- `selector`: CSS选择器（如 `'h2'`, `'.title'`）
- `output_path`: 可选的输出路径

---

## 高级配置

### 代理配置

#### 单一代理

```python
crawler = ZTLCrawler(
    crawler_type='playwright',
    proxy_config={
        'server': 'http://proxy.example.com:8080',
        'username': 'user',
        'password': 'pass'
    }
)
```

#### 代理轮换

```python
# 需要自定义实现代理池
from itertools import cycle

proxy_pool = cycle([
    'http://proxy1.com:8080',
    'http://proxy2.com:8080',
    'http://proxy3.com:8080',
])

# 在handler中动态切换代理
async def handler_with_proxy(context):
    # 使用next(proxy_pool)获取下一个代理
    ...
```

### 请求头自定义

```python
from crawlee.playwright_crawler import PlaywrightCrawler

crawler = PlaywrightCrawler(
    browser_type='chromium',
    headless=True,
)

# 在handler中设置自定义请求头
async def handler(context):
    await context.page.set_extra_http_headers({
        'User-Agent': 'Custom User Agent',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    })
    ...
```

### Cookie管理

```python
async def handler_with_cookie(context: PlaywrightCrawlingContext):
    # 设置Cookie
    await context.page.context.add_cookies([
        {
            'name': 'session_id',
            'value': 'abc123',
            'domain': '.example.com',
            'path': '/'
        }
    ])

    # 获取Cookie
    cookies = await context.page.context.cookies()
    print(f"当前Cookie: {cookies}")
```

---

## 性能优化

### 并发控制

Crawlee会根据系统资源自动调整并发数，但可以手动配置:

```python
from crawlee.playwright_crawler import PlaywrightCrawler

crawler = PlaywrightCrawler(
    max_request_retries=3,
    max_requests_per_crawl=100,
    # 并发相关配置
)
```

### 内存优化

```python
# 1. 限制最大请求数
crawler = ZTLCrawler(max_requests=50)

# 2. 分批处理大量URL
async def batch_crawl(all_urls, batch_size=50):
    results = []
    for i in range(0, len(all_urls), batch_size):
        batch = all_urls[i:i+batch_size]
        crawler = ZTLCrawler(max_requests=batch_size)
        batch_results = await crawler.crawl(batch, handler)
        results.extend(batch_results)
    return results
```

### 请求间隔

```python
import asyncio

async def handler_with_delay(context):
    # 数据提取逻辑
    data = {...}

    # 添加延迟（礼貌爬取）
    await asyncio.sleep(1)  # 1秒延迟

    return data
```

---

## 常见问题

### Q1: 如何处理需要登录的网站？

**A**: 使用Playwright模式，先登录再爬取:

```python
async def crawl_with_login():
    from crawlee.playwright_crawler import PlaywrightCrawler

    crawler = PlaywrightCrawler(headless=False)

    first_run = True

    @crawler.router.default_handler
    async def handler(context):
        nonlocal first_run

        if first_run:
            # 首次访问，执行登录
            await context.page.fill('#username', 'your_username')
            await context.page.fill('#password', 'your_password')
            await context.page.click('#login-button')
            await context.page.wait_for_selector('.user-profile')
            first_run = False

        # 正常爬取逻辑
        ...

    await crawler.run(['https://example.com'])
```

### Q2: 如何绕过反爬虫检测？

**A**: 多种策略组合:

1. **使用真实浏览器指纹**（Crawlee默认支持）
2. **随机User-Agent**
3. **添加请求延迟**
4. **使用代理IP池**
5. **模拟人类行为**（随机滚动、移动鼠标）

```python
import random

async def anti_detection_handler(context):
    page = context.page

    # 随机滚动
    for _ in range(random.randint(2, 5)):
        await page.evaluate(f'window.scrollBy(0, {random.randint(100, 500)})')
        await asyncio.sleep(random.uniform(0.5, 1.5))

    # 数据提取
    ...
```

### Q3: 如何处理动态加载的内容？

**A**: 使用Playwright并等待元素出现:

```python
async def dynamic_handler(context: PlaywrightCrawlingContext):
    page = context.page

    # 方法1: 等待特定元素
    await page.wait_for_selector('.dynamic-content', timeout=10000)

    # 方法2: 等待网络空闲
    await page.wait_for_load_state('networkidle')

    # 方法3: 等待特定时间
    await asyncio.sleep(2)

    # 提取数据
    ...
```

### Q4: 如何导出为Excel格式？

**A**: 先导出JSON，再转换为Excel:

```python
import pandas as pd

# 1. 爬取数据
results = await crawler.crawl(urls, handler)
await crawler.export_data('data.json', format='json')

# 2. 转换为Excel
df = pd.DataFrame(results)
df.to_excel('data.xlsx', index=False)
```

---

## 最佳实践

### 1. 遵守robots.txt

```python
from urllib.robotparser import RobotFileParser

def can_fetch(url):
    rp = RobotFileParser()
    rp.set_url(f"{url.scheme}://{url.netloc}/robots.txt")
    rp.read()
    return rp.can_fetch("*", url.geturl())

# 在爬取前检查
if can_fetch(target_url):
    await crawler.crawl([target_url], handler)
```

### 2. 错误处理

```python
async def robust_handler(context):
    try:
        # 数据提取逻辑
        data = extract_data(context)
        return data

    except Exception as e:
        # 记录错误
        print(f"❌ 错误: {e}")

        # 返回错误信息
        return {
            'url': context.request.url,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }
```

### 3. 增量爬取

```python
import json
from pathlib import Path

def load_crawled_urls():
    """加载已爬取的URL"""
    cache_file = Path('crawled_urls.json')
    if cache_file.exists():
        with open(cache_file) as f:
            return set(json.load(f))
    return set()

def save_crawled_url(url):
    """保存已爬取的URL"""
    crawled = load_crawled_urls()
    crawled.add(url)
    with open('crawled_urls.json', 'w') as f:
        json.dump(list(crawled), f)

async def incremental_handler(context):
    url = context.request.url

    # 检查是否已爬取
    if url in load_crawled_urls():
        print(f"⏭️ 跳过已爬取URL: {url}")
        return None

    # 爬取数据
    data = extract_data(context)

    # 标记为已爬取
    save_crawled_url(url)

    return data
```

### 4. 数据验证

```python
from pydantic import BaseModel, HttpUrl, ValidationError

class DishData(BaseModel):
    name: str
    price: str
    url: HttpUrl

async def validated_handler(context):
    raw_data = extract_data(context)

    try:
        # 验证数据格式
        validated = DishData(**raw_data)
        return validated.dict()

    except ValidationError as e:
        print(f"❌ 数据验证失败: {e}")
        return None
```

### 5. 日志记录

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawler.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def logged_handler(context):
    url = context.request.url
    logger.info(f"🕷️ 开始爬取: {url}")

    try:
        data = extract_data(context)
        logger.info(f"✅ 爬取成功: {url}")
        return data

    except Exception as e:
        logger.error(f"❌ 爬取失败: {url} - {e}")
        raise
```

---

## 相关资源

- **Crawlee官方文档**: https://crawlee.dev/python/
- **Playwright文档**: https://playwright.dev/python/
- **BeautifulSoup文档**: https://www.crummy.com/software/BeautifulSoup/

---

**版本**: v1.0.0
**最后更新**: 2025-10-21
