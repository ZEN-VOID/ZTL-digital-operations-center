"""
餐饮行业应用示例

演示如何使用Crawlee采集餐饮相关数据
"""

import asyncio
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from skills.web_crawling_advanced.scripts.crawlee_engine import (
    ZTLCrawler,
    crawl_competitor_menu,
    crawl_reviews
)


async def example_competitor_analysis():
    """示例: 竞品分析 - 采集竞品菜单和价格"""

    print("=== 竞品菜单采集示例 ===\n")

    # 注意: 这里使用示例URL，实际使用时替换为真实URL
    restaurant_url = 'https://www.meituan.com/meishi/example-restaurant'

    try:
        # 使用便捷函数采集菜单
        # results = await crawl_competitor_menu(restaurant_url, platform='meituan')

        # print(f"✅ 菜单采集完成")
        # print(f"   餐厅: {results[0]['restaurant']}")
        # print(f"   菜品数: {len(results[0]['dishes'])}")
        # print(f"   示例菜品: {results[0]['dishes'][:3]}")

        print("⚠️ 这是示例代码，请替换为实际URL后运行")

    except Exception as e:
        print(f"❌ 采集失败: {e}")


async def example_review_monitoring():
    """示例: 评价监控 - 批量采集餐厅评价"""

    print("\n=== 餐厅评价采集示例 ===\n")

    restaurant_urls = [
        'https://www.dianping.com/shop/example1',
        'https://www.dianping.com/shop/example2',
        # 添加更多餐厅URL...
    ]

    try:
        # results = await crawl_reviews(restaurant_urls, max_reviews_per_restaurant=20)

        # print(f"✅ 评价采集完成")
        # print(f"   采集餐厅数: {len(results)}")
        # for result in results:
        #     print(f"   - {result['restaurant']}: {len(result['reviews'])} 条评价")

        print("⚠️ 这是示例代码，请替换为实际URL后运行")

    except Exception as e:
        print(f"❌ 采集失败: {e}")


async def example_custom_restaurant_crawler():
    """示例: 自定义餐厅数据爬虫"""

    print("\n=== 自定义餐厅数据爬虫 ===\n")

    from crawlee.playwright_crawler import PlaywrightCrawlingContext

    crawler = ZTLCrawler(crawler_type='playwright', headless=True)

    async def restaurant_handler(context: PlaywrightCrawlingContext):
        """提取餐厅基础信息"""

        page = context.page

        # 等待页面加载
        await page.wait_for_load_state('networkidle')

        # 提取数据（根据实际网站结构调整选择器）
        try:
            # 餐厅名称
            name_el = await page.query_selector('.restaurant-name')
            name = await name_el.inner_text() if name_el else ''

            # 评分
            rating_el = await page.query_selector('.rating-score')
            rating = await rating_el.inner_text() if rating_el else ''

            # 人均消费
            price_el = await page.query_selector('.avg-price')
            avg_price = await price_el.inner_text() if price_el else ''

            # 地址
            address_el = await page.query_selector('.restaurant-address')
            address = await address_el.inner_text() if address_el else ''

            # 营业时间
            hours_el = await page.query_selector('.business-hours')
            hours = await hours_el.inner_text() if hours_el else ''

            return {
                'url': context.request.url,
                'name': name,
                'rating': rating,
                'avg_price': avg_price,
                'address': address,
                'business_hours': hours,
            }

        except Exception as e:
            print(f"提取数据失败: {e}")
            return {'url': context.request.url, 'error': str(e)}

    # 示例URL列表
    urls = [
        'https://example-restaurant-site.com/restaurant/1',
        # 添加更多URL...
    ]

    # results = await crawler.crawl(urls, restaurant_handler)
    # await crawler.export_data('output/情报组/restaurant-data.json')

    print("⚠️ 这是示例代码，请根据实际网站结构调整选择器")


async def example_price_tracking():
    """示例: 价格追踪 - 定期监控竞品价格变化"""

    print("\n=== 价格追踪示例 ===\n")

    from crawlee.beautifulsoup_crawler import BeautifulSoupCrawlingContext
    from datetime import datetime

    crawler = ZTLCrawler(crawler_type='beautifulsoup')

    async def price_handler(context: BeautifulSoupCrawlingContext):
        soup = context.soup

        # 提取商品价格（根据实际网站调整）
        prices = []
        price_elements = soup.select('.product-price')

        for el in price_elements:
            product_name = el.find_previous('.product-name')
            price_text = el.get_text(strip=True)

            prices.append({
                'product': product_name.get_text() if product_name else '',
                'price': price_text,
                'timestamp': datetime.now().isoformat()
            })

        return {
            'url': context.request.url,
            'prices': prices,
            'crawled_at': datetime.now().isoformat()
        }

    # 定期采集价格数据
    urls = ['https://example-menu-site.com']
    # results = await crawler.crawl(urls, price_handler)

    # 保存历史数据用于对比
    # output_file = f"output/情报组/price-tracking-{datetime.now().strftime('%Y%m%d')}.json"
    # await crawler.export_data(output_file)

    print("💡 提示: 可以配合cron定时任务，每天自动采集价格数据")


async def main():
    """运行所有示例"""

    # 创建输出目录
    Path('output/情报组').mkdir(parents=True, exist_ok=True)

    print("="*60)
    print("餐饮行业爬虫应用示例")
    print("="*60 + "\n")

    # 运行示例
    await example_competitor_analysis()
    await example_review_monitoring()
    await example_custom_restaurant_crawler()
    await example_price_tracking()

    print("\n" + "="*60)
    print("💡 使用提示:")
    print("1. 将示例URL替换为实际网站URL")
    print("2. 根据目标网站调整CSS选择器")
    print("3. 遵守robots.txt和网站服务条款")
    print("4. 设置合理的请求间隔，避免过载")
    print("="*60)


if __name__ == '__main__':
    asyncio.run(main())
