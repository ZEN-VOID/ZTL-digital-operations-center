"""
爬虫模板 - 快速创建新爬虫

使用此模板快速开发自定义爬虫。
"""

import asyncio
from pathlib import Path
import sys

# 添加项目路径
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from skills.web_crawling_advanced.scripts.crawlee_engine import ZTLCrawler
from crawlee.beautifulsoup_crawler import BeautifulSoupCrawlingContext
from crawlee.playwright_crawler import PlaywrightCrawlingContext


# ============================================================================
# 模板1: BeautifulSoup静态爬虫
# ============================================================================

async def static_crawler_template():
    """静态网页爬虫模板"""

    crawler = ZTLCrawler(crawler_type='beautifulsoup', max_requests=50)

    async def my_handler(context: BeautifulSoupCrawlingContext):
        """
        自定义数据处理逻辑

        可访问属性:
        - context.request: 当前请求对象
        - context.soup: BeautifulSoup解析对象
        - context.http_response: HTTP响应
        """
        soup = context.soup

        # TODO: 添加你的选择器和数据提取逻辑
        title = soup.find('title')
        headings = soup.find_all('h2')

        return {
            'url': context.request.url,
            'title': title.get_text() if title else '',
            'headings': [h.get_text() for h in headings],
            # 添加更多字段...
        }

    # 执行爬取
    urls = [
        'https://example.com',
        # 添加更多URL...
    ]

    results = await crawler.crawl(urls, my_handler)

    # 导出结果
    await crawler.export_data('output/情报组/my-crawl-results.json')

    # 打印统计
    stats = crawler.get_stats()
    print(f"✅ 爬取完成: {stats['successful_requests']}/{stats['total_requests']} 成功")

    return results


# ============================================================================
# 模板2: Playwright动态爬虫
# ============================================================================

async def dynamic_crawler_template():
    """动态网页爬虫模板（需要JavaScript渲染）"""

    crawler = ZTLCrawler(
        crawler_type='playwright',
        headless=True,
        max_requests=30
    )

    async def my_handler(context: PlaywrightCrawlingContext):
        """
        动态网页数据处理逻辑

        可访问属性:
        - context.request: 当前请求对象
        - context.page: Playwright Page对象
        - context.browser_type: 浏览器类型
        """
        page = context.page

        # 等待特定元素加载
        await page.wait_for_selector('.content', timeout=10000)

        # TODO: 添加你的数据提取逻辑
        title = await page.title()
        content = await page.inner_text('.content')

        # 可选: 截图保存
        # await page.screenshot(path='screenshot.png')

        return {
            'url': context.request.url,
            'title': title,
            'content': content[:500],  # 前500字符
            # 添加更多字段...
        }

    # 执行爬取
    urls = [
        'https://dynamic-site.com',
        # 添加更多URL...
    ]

    results = await crawler.crawl(urls, my_handler, enqueue_links=False)

    # 导出结果
    await crawler.export_data('output/情报组/my-dynamic-crawl.json')

    return results


# ============================================================================
# 模板3: 递归链接爬取
# ============================================================================

async def recursive_crawler_template():
    """递归爬取网站链接"""

    crawler = ZTLCrawler(crawler_type='beautifulsoup', max_requests=100)

    async def my_handler(context: BeautifulSoupCrawlingContext):
        soup = context.soup

        # 提取数据
        data = {
            'url': context.request.url,
            'title': soup.find('title').get_text() if soup.find('title') else '',
        }

        return data

    # 执行爬取（自动发现和爬取链接）
    urls = ['https://example.com']
    results = await crawler.crawl(urls, my_handler, enqueue_links=True)

    return results


# ============================================================================
# 模板4: 列表详情页爬取
# ============================================================================

async def list_detail_crawler_template():
    """先爬列表页，再爬详情页"""

    # 第一步: 爬取列表页，获取详情页链接
    list_crawler = ZTLCrawler(crawler_type='beautifulsoup')

    detail_urls = []

    async def list_handler(context: BeautifulSoupCrawlingContext):
        soup = context.soup

        # 提取详情页链接
        links = soup.select('.item-link')
        for link in links:
            href = link.get('href')
            if href:
                detail_urls.append(href)

        return {'list_url': context.request.url, 'found_links': len(links)}

    await list_crawler.crawl(['https://example.com/list'], list_handler)

    print(f"✅ 找到 {len(detail_urls)} 个详情页链接")

    # 第二步: 爬取详情页
    detail_crawler = ZTLCrawler(crawler_type='playwright', max_requests=len(detail_urls))

    async def detail_handler(context: PlaywrightCrawlingContext):
        page = context.page

        # 等待内容加载
        await page.wait_for_selector('.detail-content')

        # 提取详情数据
        title = await page.inner_text('.detail-title')
        content = await page.inner_text('.detail-content')

        return {
            'url': context.request.url,
            'title': title,
            'content': content
        }

    results = await detail_crawler.crawl(detail_urls, detail_handler)

    # 导出结果
    await detail_crawler.export_data('output/情报组/detail-results.json')

    return results


# ============================================================================
# 使用示例
# ============================================================================

async def main():
    """主函数 - 选择要运行的模板"""

    print("选择模板:")
    print("1. 静态网页爬虫")
    print("2. 动态网页爬虫")
    print("3. 递归链接爬取")
    print("4. 列表详情页爬取")

    # 这里可以根据需要选择运行哪个模板
    # await static_crawler_template()
    # await dynamic_crawler_template()
    # await recursive_crawler_template()
    # await list_detail_crawler_template()

    print("✅ 请取消注释上面的函数调用来运行对应模板")


if __name__ == '__main__':
    asyncio.run(main())
