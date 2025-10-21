from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page(viewport={'width': 1440, 'height': 1920})
    page.goto('http://localhost:3009/chengdu-attractions-guide', wait_until='networkidle')

    print('等待页面加载...')
    time.sleep(2)

    # 获取页面HTML查看实际的class名称
    html = page.content()

    # 查找包含cardImage的class
    import re
    classes = re.findall(r'class="([^"]*cardImage[^"]*)"', html)
    print(f'\n找到的cardImage相关class:')
    for cls in set(classes):
        print(f'  - {cls}')

    # 测试各种选择器
    selectors = [
        '.cardImage',
        'div[class*="cardImage"]',
        '[class*="cardImage"]',
        'div[class*="card"] div[class*="Image"]',
    ]

    print(f'\n测试选择器:')
    for sel in selectors:
        elements = page.query_selector_all(sel)
        print(f'  {sel}: {len(elements)} 个元素')

    # 获取所有div的class
    all_divs = page.query_selector_all('div')
    print(f'\n前20个div的class:')
    for i, div in enumerate(all_divs[:20]):
        cls = page.evaluate('el => el.className', div)
        if cls:
            print(f'  {i}: {cls}')

    time.sleep(10)
    browser.close()
