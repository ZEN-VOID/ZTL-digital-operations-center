"""
基础示例 - 快速上手Crawlee爬虫

演示最基础的使用方法
"""

import asyncio
from pathlib import Path
import sys

# 添加项目路径
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from skills.web_crawling_advanced.scripts.crawlee_engine import ZTLCrawler, quick_crawl


async def example1_quick_crawl():
    """示例1: 使用便捷函数快速采集"""

    print("=== 示例1: 快速采集网页标题 ===\n")

    # 一行代码采集所有h2标题
    results = await quick_crawl(
        urls=['https://example.com'],
        selector='h2',
        output_path='output/情报组/example-quick-crawl.json'
    )

    print(f"✅ 采集完成")
    print(f"   URL: {results[0]['url']}")
    print(f"   找到 {results[0]['count']} 个标题")
    print(f"   内容: {results[0]['content'][:3]}")  # 前3个标题


async def example2_custom_static():
    """示例2: 自定义静态网页爬虫"""

    print("\n=== 示例2: 自定义静态爬虫 ===\n")

    from crawlee.beautifulsoup_crawler import BeautifulSoupCrawlingContext

    # 创建爬虫实例
    crawler = ZTLCrawler(crawler_type='beautifulsoup', max_requests=5)

    # 定义数据处理逻辑
    async def my_handler(context: BeautifulSoupCrawlingContext):
        soup = context.soup

        # 提取标题
        title = soup.find('title')

        # 提取所有段落
        paragraphs = soup.find_all('p')

        return {
            'url': context.request.url,
            'title': title.get_text() if title else '',
            'paragraph_count': len(paragraphs),
            'first_paragraph': paragraphs[0].get_text() if paragraphs else ''
        }

    # 执行爬取
    results = await crawler.crawl(['https://example.com'], my_handler)

    # 导出结果
    await crawler.export_data('output/情报组/example-custom-static.json')

    # 打印结果
    print(f"✅ 采集完成")
    print(f"   标题: {results[0]['title']}")
    print(f"   段落数: {results[0]['paragraph_count']}")

    # 打印统计信息
    stats = crawler.get_stats()
    print(f"\n📊 统计信息:")
    print(f"   总请求: {stats['total_requests']}")
    print(f"   成功: {stats['successful_requests']}")
    print(f"   失败: {stats['failed_requests']}")


async def example3_multiple_urls():
    """示例3: 批量采集多个URL"""

    print("\n=== 示例3: 批量采集 ===\n")

    from crawlee.beautifulsoup_crawler import BeautifulSoupCrawlingContext

    crawler = ZTLCrawler(crawler_type='beautifulsoup', max_requests=10)

    async def handler(context: BeautifulSoupCrawlingContext):
        soup = context.soup
        title = soup.find('title')

        return {
            'url': context.request.url,
            'title': title.get_text() if title else 'No title'
        }

    # 批量URL
    urls = [
        'https://example.com',
        'https://example.org',
        'https://example.net',
    ]

    results = await crawler.crawl(urls, handler)

    print(f"✅ 批量采集完成，共 {len(results)} 个URL")
    for i, result in enumerate(results, 1):
        print(f"   {i}. {result['title']}")

    # 导出
    await crawler.export_data('output/情报组/example-batch-crawl.json')


async def main():
    """运行所有示例"""

    # 创建输出目录
    Path('output/情报组').mkdir(parents=True, exist_ok=True)

    # 运行示例
    await example1_quick_crawl()
    await example2_custom_static()
    await example3_multiple_urls()

    print("\n" + "="*50)
    print("✅ 所有示例运行完成!")
    print("📁 结果已保存到: output/情报组/")
    print("="*50)


if __name__ == '__main__':
    asyncio.run(main())
