"""
基础功能测试 - 验证Crawlee安装和核心功能

这是一个简单的测试脚本，用于验证Crawlee是否正确安装和配置
"""

import asyncio
from pathlib import Path


async def test_import():
    """测试1: 验证模块导入"""
    print("=" * 60)
    print("测试1: 验证模块导入")
    print("=" * 60)

    try:
        from crawlee.beautifulsoup_crawler import BeautifulSoupCrawler, BeautifulSoupCrawlingContext
        from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext
        from crawlee.storages import Dataset

        print("✅ Crawlee核心模块导入成功")
        print("  - BeautifulSoupCrawler")
        print("  - PlaywrightCrawler")
        print("  - Dataset")

        return True

    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        print("\n解决方案:")
        print("  pip3 install 'crawlee[all]'")
        print("  playwright install chromium")
        return False


async def test_beautifulsoup_crawler():
    """测试2: BeautifulSoup爬虫"""
    print("\n" + "=" * 60)
    print("测试2: BeautifulSoup爬虫 (快速静态爬取)")
    print("=" * 60)

    try:
        from crawlee.beautifulsoup_crawler import BeautifulSoupCrawler, BeautifulSoupCrawlingContext

        crawler = BeautifulSoupCrawler(max_requests_per_crawl=1)

        results = []

        @crawler.router.default_handler
        async def handler(context: BeautifulSoupCrawlingContext):
            soup = context.soup
            title = soup.find('title')

            data = {
                'url': context.request.url,
                'title': title.get_text() if title else 'No title',
                'status': 'success'
            }

            results.append(data)
            await context.push_data(data)

        # 爬取示例网站
        await crawler.run(['https://example.com'])

        if results:
            print(f"✅ BeautifulSoup爬虫测试成功")
            print(f"  - URL: {results[0]['url']}")
            print(f"  - 标题: {results[0]['title']}")
            return True
        else:
            print("⚠️ 爬取成功但未获取到数据")
            return False

    except Exception as e:
        print(f"❌ BeautifulSoup爬虫测试失败: {e}")
        return False


async def test_playwright_crawler():
    """测试3: Playwright爬虫 (需要浏览器驱动)"""
    print("\n" + "=" * 60)
    print("测试3: Playwright爬虫 (动态网页爬取)")
    print("=" * 60)

    try:
        from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext

        crawler = PlaywrightCrawler(
            headless=True,
            max_requests_per_crawl=1
        )

        results = []

        @crawler.router.default_handler
        async def handler(context: PlaywrightCrawlingContext):
            page = context.page

            data = {
                'url': context.request.url,
                'title': await page.title(),
                'status': 'success'
            }

            results.append(data)
            await context.push_data(data)

        # 爬取示例网站
        await crawler.run(['https://example.com'])

        if results:
            print(f"✅ Playwright爬虫测试成功")
            print(f"  - URL: {results[0]['url']}")
            print(f"  - 标题: {results[0]['title']}")
            return True
        else:
            print("⚠️ 爬取成功但未获取到数据")
            return False

    except Exception as e:
        print(f"❌ Playwright爬虫测试失败: {e}")
        print("\n可能原因:")
        print("  1. 浏览器驱动未安装: playwright install chromium")
        print("  2. 权限问题: 检查文件系统权限")
        return False


async def test_data_export():
    """测试4: 数据导出功能"""
    print("\n" + "=" * 60)
    print("测试4: 数据导出功能")
    print("=" * 60)

    try:
        from crawlee.storages import Dataset

        # 创建测试数据
        test_data = [
            {'name': '测试1', 'value': 100},
            {'name': '测试2', 'value': 200},
        ]

        dataset = await Dataset.open()
        await dataset.push_data(test_data)

        # 导出为JSON
        output_dir = Path('output/情报组/test-export')
        output_dir.mkdir(parents=True, exist_ok=True)

        await dataset.export_to('output/情报组/test-export/test-data.json')

        print("✅ 数据导出测试成功")
        print(f"  - 导出路径: output/情报组/test-export/test-data.json")
        print(f"  - 数据条数: {len(test_data)}")

        return True

    except Exception as e:
        print(f"❌ 数据导出测试失败: {e}")
        return False


async def main():
    """运行所有测试"""
    print("\n🧪 Crawlee功能测试套件\n")

    results = {
        '模块导入': await test_import(),
        'BeautifulSoup爬虫': await test_beautifulsoup_crawler(),
        'Playwright爬虫': await test_playwright_crawler(),
        '数据导出': await test_data_export(),
    }

    # 统计结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, passed_flag in results.items():
        status = "✅ 通过" if passed_flag else "❌ 失败"
        print(f"{test_name:20} {status}")

    print("=" * 60)
    print(f"总计: {passed}/{total} 测试通过")
    print("=" * 60)

    if passed == total:
        print("\n🎉 所有测试通过！Crawlee已正确安装和配置。")
    else:
        print(f"\n⚠️ 有 {total - passed} 个测试失败，请检查安装和配置。")
        print("\n参考文档: .claude/skills/web-crawling-advanced/INSTALL.md")

    return passed == total


if __name__ == '__main__':
    asyncio.run(main())
