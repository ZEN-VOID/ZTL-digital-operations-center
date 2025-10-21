"""
ZTL Web Crawling Advanced - 核心引擎
基于Crawlee-Python v1.0.3

提供企业级爬虫能力：
- BeautifulSoupCrawler: 静态HTML采集
- PlaywrightCrawler: 动态JavaScript渲染
- AdaptivePlaywrightCrawler: 智能自适应
"""

from pathlib import Path
from typing import List, Dict, Any, Callable, Optional, Literal
from datetime import datetime
import json
import asyncio

try:
    from crawlee.beautifulsoup_crawler import BeautifulSoupCrawler, BeautifulSoupCrawlingContext
    from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext
    from crawlee.storages import Dataset
    CRAWLEE_AVAILABLE = True
except ImportError:
    CRAWLEE_AVAILABLE = False
    print("⚠️ Crawlee未安装，请运行: pip install 'crawlee[all]'")


class ZTLCrawler:
    """
    ZTL智能爬虫引擎

    支持三种爬虫类型：
    - beautifulsoup: 静态HTML采集（快速）
    - playwright: 动态JavaScript渲染（功能完整）
    - adaptive: 智能自适应选择
    """

    def __init__(
        self,
        crawler_type: Literal['beautifulsoup', 'playwright', 'adaptive'] = 'beautifulsoup',
        headless: bool = True,
        max_requests: int = 100,
        proxy_config: Optional[Dict] = None,
        retry_config: Optional[Dict] = None
    ):
        """
        初始化爬虫引擎

        Args:
            crawler_type: 爬虫类型
            headless: 无头模式（仅Playwright）
            max_requests: 最大请求数
            proxy_config: 代理配置
            retry_config: 重试配置
        """
        if not CRAWLEE_AVAILABLE:
            raise ImportError("Crawlee未安装，请运行: pip install 'crawlee[all]'")

        self.crawler_type = crawler_type
        self.headless = headless
        self.max_requests = max_requests
        self.proxy_config = proxy_config
        self.retry_config = retry_config

        self.results = []
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'start_time': None,
            'end_time': None
        }

    async def crawl(
        self,
        urls: List[str],
        handler: Callable,
        enqueue_links: bool = False
    ) -> List[Dict[str, Any]]:
        """
        执行爬取任务

        Args:
            urls: 起始URL列表
            handler: 数据处理函数
            enqueue_links: 是否自动发现和爬取链接

        Returns:
            采集结果列表
        """
        self.stats['start_time'] = datetime.now()
        self.results = []

        # 创建爬虫实例
        if self.crawler_type == 'beautifulsoup':
            crawler = BeautifulSoupCrawler(
                max_requests_per_crawl=self.max_requests,
            )

            @crawler.router.default_handler
            async def request_handler(context: BeautifulSoupCrawlingContext):
                try:
                    data = await handler(context)
                    self.results.append(data)
                    await context.push_data(data)

                    if enqueue_links:
                        await context.enqueue_links()

                    self.stats['successful_requests'] += 1
                except Exception as e:
                    print(f"❌ 处理失败 {context.request.url}: {e}")
                    self.stats['failed_requests'] += 1

        elif self.crawler_type in ['playwright', 'adaptive']:
            crawler = PlaywrightCrawler(
                headless=self.headless,
                max_requests_per_crawl=self.max_requests,
            )

            @crawler.router.default_handler
            async def request_handler(context: PlaywrightCrawlingContext):
                try:
                    data = await handler(context)
                    self.results.append(data)
                    await context.push_data(data)

                    if enqueue_links:
                        await context.enqueue_links()

                    self.stats['successful_requests'] += 1
                except Exception as e:
                    print(f"❌ 处理失败 {context.request.url}: {e}")
                    self.stats['failed_requests'] += 1

        else:
            raise ValueError(f"不支持的爬虫类型: {self.crawler_type}")

        # 执行爬取
        await crawler.run(urls)

        self.stats['end_time'] = datetime.now()
        self.stats['total_requests'] = self.stats['successful_requests'] + self.stats['failed_requests']

        return self.results

    async def export_data(
        self,
        output_path: str,
        format: Literal['json', 'csv'] = 'json'
    ) -> str:
        """
        导出采集数据

        Args:
            output_path: 输出文件路径
            format: 导出格式

        Returns:
            导出文件路径
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)

        elif format == 'csv':
            import csv
            if not self.results:
                return str(output_path)

            keys = self.results[0].keys()
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(self.results)

        print(f"✅ 数据已导出: {output_path}")
        return str(output_path)

    def get_stats(self) -> Dict[str, Any]:
        """获取爬取统计信息"""
        if self.stats['start_time'] and self.stats['end_time']:
            duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
            self.stats['duration_seconds'] = duration
            self.stats['requests_per_second'] = (
                self.stats['total_requests'] / duration if duration > 0 else 0
            )

        return self.stats


# ============================================================================
# 便捷函数 - 常见爬取场景
# ============================================================================

async def crawl_competitor_menu(restaurant_url: str, platform: str = 'meituan') -> List[Dict]:
    """
    爬取竞品菜单数据

    Args:
        restaurant_url: 竞品餐厅URL
        platform: 平台类型 ('meituan' | 'dianping')

    Returns:
        菜单数据列表
    """
    crawler = ZTLCrawler(crawler_type='playwright', headless=True)

    async def menu_handler(context: PlaywrightCrawlingContext):
        page = context.page

        # 等待页面加载
        await page.wait_for_load_state('networkidle')

        # 美团平台选择器
        if platform == 'meituan':
            await page.wait_for_selector('.food-category', timeout=10000)

            # 提取菜单数据
            dishes = []
            food_items = await page.query_selector_all('.food-item')

            for item in food_items:
                name_el = await item.query_selector('.food-name')
                price_el = await item.query_selector('.food-price')

                dish = {
                    'name': await name_el.inner_text() if name_el else '',
                    'price': await price_el.inner_text() if price_el else '',
                }
                dishes.append(dish)

        # 大众点评平台选择器
        elif platform == 'dianping':
            await page.wait_for_selector('.dish-item', timeout=10000)

            dishes = []
            dish_items = await page.query_selector_all('.dish-item')

            for item in dish_items:
                name_el = await item.query_selector('.dish-name')
                price_el = await item.query_selector('.dish-price')

                dish = {
                    'name': await name_el.inner_text() if name_el else '',
                    'price': await price_el.inner_text() if price_el else '',
                }
                dishes.append(dish)

        return {
            'url': context.request.url,
            'platform': platform,
            'restaurant': await page.title(),
            'dishes': dishes,
            'crawled_at': datetime.now().isoformat()
        }

    results = await crawler.crawl([restaurant_url], menu_handler)

    # 自动导出
    output_path = f"output/情报组/competitor-menu-{platform}-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    await crawler.export_data(output_path)

    return results


async def crawl_reviews(
    restaurant_urls: List[str],
    max_reviews_per_restaurant: int = 50
) -> List[Dict]:
    """
    批量采集餐厅评价

    Args:
        restaurant_urls: 餐厅URL列表
        max_reviews_per_restaurant: 每家餐厅最多采集评价数

    Returns:
        评价数据列表
    """
    crawler = ZTLCrawler(crawler_type='playwright', max_requests=len(restaurant_urls) * 10)

    async def review_handler(context: PlaywrightCrawlingContext):
        page = context.page

        # 等待评价加载
        await page.wait_for_selector('.review-item', timeout=10000)

        # 滚动加载更多评价
        for _ in range(3):
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            await asyncio.sleep(1)

        # 提取评价
        review_items = await page.query_selector_all('.review-item')
        reviews = []

        for item in review_items[:max_reviews_per_restaurant]:
            user_el = await item.query_selector('.review-user')
            rating_el = await item.query_selector('.review-rating')
            content_el = await item.query_selector('.review-content')

            review = {
                'user': await user_el.inner_text() if user_el else '',
                'rating': await rating_el.get_attribute('data-rating') if rating_el else '',
                'content': await content_el.inner_text() if content_el else '',
            }
            reviews.append(review)

        return {
            'url': context.request.url,
            'restaurant': await page.title(),
            'reviews': reviews,
            'crawled_at': datetime.now().isoformat()
        }

    results = await crawler.crawl(restaurant_urls, review_handler)

    # 自动导出
    output_path = f"output/情报组/reviews-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    await crawler.export_data(output_path)

    return results


async def quick_crawl(
    urls: List[str],
    selector: str,
    output_path: Optional[str] = None
) -> List[Dict]:
    """
    快速采集指定元素内容

    Args:
        urls: URL列表
        selector: CSS选择器
        output_path: 输出路径（可选）

    Returns:
        采集结果
    """
    crawler = ZTLCrawler(crawler_type='beautifulsoup')

    async def quick_handler(context: BeautifulSoupCrawlingContext):
        elements = context.soup.select(selector)

        return {
            'url': context.request.url,
            'selector': selector,
            'content': [el.get_text(strip=True) for el in elements],
            'count': len(elements),
            'crawled_at': datetime.now().isoformat()
        }

    results = await crawler.crawl(urls, quick_handler)

    if output_path:
        await crawler.export_data(output_path)

    return results


# ============================================================================
# 示例用法
# ============================================================================

async def example_usage():
    """示例用法"""

    # 示例1: 快速采集
    print("=== 示例1: 快速采集 ===")
    results = await quick_crawl(
        urls=['https://example.com'],
        selector='h2',
        output_path='output/情报组/test-quick-crawl.json'
    )
    print(f"✅ 采集完成，共 {len(results)} 条结果")

    # 示例2: 竞品菜单监控
    # print("=== 示例2: 竞品菜单监控 ===")
    # menu_data = await crawl_competitor_menu('https://www.meituan.com/meishi/123456')
    # print(f"✅ 菜单采集完成，共 {len(menu_data[0]['dishes'])} 道菜")


if __name__ == '__main__':
    # 运行示例
    asyncio.run(example_usage())
