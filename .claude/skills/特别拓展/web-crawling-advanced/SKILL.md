---
name: web-crawling-advanced
description: 基于Crawlee-Python的企业级网页爬虫框架，支持静态和动态网页采集、反反爬机制、代理轮换、数据持久化，适用于竞品监控、市场调研、数据采集等场景
---

# Web Crawling Advanced Skill

> 企业级Python爬虫框架，基于Crawlee v1.0.3
> 适用智能体：E2-网站情报采集员、E3-网站深度爬虫员、G4-竞争情报分析师

---

## 🚀 Quick Start

### 基础用法 - 静态网页采集

```python
from skills.web_crawling_advanced.scripts.crawlee_engine import ZTLCrawler
import asyncio

async def quick_crawl():
    """快速采集静态网页"""

    # 创建爬虫实例
    crawler = ZTLCrawler(crawler_type='beautifulsoup')

    # 定义数据提取逻辑
    async def handler(context):
        return {
            'url': context.request.url,
            'title': context.soup.find('title').get_text() if context.soup.find('title') else '',
            'text': context.soup.get_text()[:500]  # 前500字符
        }

    # 执行爬取
    results = await crawler.crawl(['https://example.com'], handler)

    # 导出结果
    await crawler.export_data('output/情报组/crawl-results.json')

    return results

# 运行
asyncio.run(quick_crawl())
```

### 进阶用法 - 动态网页采集

```python
async def dynamic_crawl():
    """采集需要JavaScript渲染的动态网页"""

    # 使用Playwright引擎
    crawler = ZTLCrawler(
        crawler_type='playwright',
        headless=True,
        max_requests=50
    )

    async def handler(context):
        page = context.page

        # 等待内容加载
        await page.wait_for_selector('.content')

        # 提取数据
        return {
            'url': context.request.url,
            'title': await page.title(),
            'content': await page.inner_text('.content')
        }

    results = await crawler.crawl(['https://dynamic-site.com'], handler)
    return results
```

---

## 📋 核心功能

### ✅ 支持的爬虫类型

| 爬虫类型 | 适用场景 | 性能 | 功能 |
|---------|---------|------|------|
| **BeautifulSoupCrawler** | 静态HTML网页 | ⚡⚡⚡ 极快 | 基础 |
| **PlaywrightCrawler** | 动态JavaScript渲染 | ⚡⚡ 中等 | 完整 |
| **AdaptivePlaywrightCrawler** | 智能自适应 | ⚡⚡ 中等 | 智能 |

### ✅ 核心特性

- 🛡️ **反反爬保护**: 真实浏览器指纹、User-Agent轮换
- 🔄 **自动重试**: 请求失败自动重试，支持自定义策略
- 💾 **数据持久化**: 支持暂停/恢复，状态自动保存
- 📊 **多格式导出**: JSON、CSV、Excel
- 🚀 **自动并发**: 根据系统资源自动调整并发数
- 🔗 **智能链接发现**: 自动发现和爬取关联链接

---

## 🎯 典型应用场景

### 场景1: 竞品菜单监控

```python
from skills.web_crawling_advanced.scripts.crawlee_engine import crawl_competitor_menu

# 一行代码监控竞品菜单
results = await crawl_competitor_menu('https://www.meituan.com/meishi/123456')
```

### 场景2: 批量采集餐厅评价

```python
from skills.web_crawling_advanced.scripts.crawlee_engine import crawl_reviews

# 批量采集多家餐厅评价
restaurant_urls = [
    'https://www.dianping.com/shop/1',
    'https://www.dianping.com/shop/2',
    # ... 更多URL
]

reviews = await crawl_reviews(restaurant_urls, max_reviews_per_restaurant=100)
```

### 场景3: 行业数据定期采集

```python
from skills.web_crawling_advanced.scripts.crawlee_engine import schedule_crawl

# 每天自动采集行业新闻
await schedule_crawl(
    urls=['https://industry-news.com'],
    handler=news_handler,
    schedule='0 9 * * *',  # 每天9点
    output_path='output/情报组/daily-news/'
)
```

---

## 🛠️ API Reference

### ZTLCrawler类

**初始化参数**:
```python
crawler = ZTLCrawler(
    crawler_type='beautifulsoup',  # 'beautifulsoup' | 'playwright' | 'adaptive'
    headless=True,                 # 无头模式（仅Playwright）
    max_requests=100,              # 最大请求数
    proxy_config=None,             # 代理配置
    retry_config=None              # 重试配置
)
```

**核心方法**:
- `crawl(urls, handler)`: 执行爬取任务
- `export_data(output_path, format='json')`: 导出数据
- `get_stats()`: 获取爬取统计信息

详细API文档请参考 [reference.md](./reference.md)

---

## 📦 依赖安装

```bash
# 安装Crawlee和所有依赖
pip install 'crawlee[all]'

# 安装Playwright浏览器驱动
playwright install chromium
```

---

## 🔗 相关资源

- **官方文档**: https://crawlee.dev/python/
- **GitHub仓库**: https://github.com/apify/crawlee-python
- **示例代码**: [examples/](./examples/)
- **扩展文档**: [reference.md](./reference.md)

---

## ⚠️ 注意事项

1. **合规使用**: 请遵守网站robots.txt和服务条款
2. **速率限制**: 建议设置合理的请求间隔，避免对目标服务器造成压力
3. **数据隐私**: 采集的数据仅用于业务分析，不得用于非法用途
4. **资源占用**: Playwright爬虫占用较多内存，建议单次爬取不超过1000页

---

**版本**: v1.0.0
**最后更新**: 2025-10-21
**维护者**: ZTL数智化作战中心-情报组
