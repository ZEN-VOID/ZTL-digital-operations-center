#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片批量替换脚本 - 执行层
从配置文件读取任务参数，执行批量替换和截图

支持两种替换模式:
1. 精确模式: 使用 replace_mapping 精确指定每个URL的目标节点
2. 兼容模式: 使用 css_selector 批量匹配所有元素
"""

import asyncio
import json
import re
import sys
from pathlib import Path
from playwright.async_api import async_playwright
from datetime import datetime
from typing import Optional, Dict, List, Any

def validate_config(config: dict, schema_path: str = 'scripts/configs/batch_replace/task_config.schema.json') -> bool:
    """
    验证配置文件是否符合JSON Schema规范

    Args:
        config: 配置字典
        schema_path: Schema文件路径

    Returns:
        验证是否通过
    """
    try:
        import jsonschema
        schema_file = Path(schema_path)

        if not schema_file.exists():
            print(f'⚠️ Schema文件不存在: {schema_path}，跳过验证')
            return True

        with open(schema_file, 'r', encoding='utf-8') as f:
            schema = json.load(f)

        jsonschema.validate(instance=config, schema=schema)
        print('✅ 配置文件验证通过')
        return True

    except ImportError:
        print('⚠️ jsonschema未安装，跳过验证 (pip install jsonschema)')
        return True
    except jsonschema.ValidationError as e:
        print(f'❌ 配置文件验证失败:')
        print(f'   错误位置: {" -> ".join(str(p) for p in e.path)}')
        print(f'   错误信息: {e.message}')
        return False
    except Exception as e:
        print(f'⚠️ 配置验证异常: {e}')
        return True

def load_config(config_path: str = 'scripts/configs/batch_replace/task_config.json') -> dict:
    """
    加载任务配置文件
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        配置字典
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        raise FileNotFoundError(f'配置文件不存在: {config_path}')
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print(f'✅ 加载配置: {config.get("task_name", "未命名任务")}')
    print(f'📋 任务ID: {config.get("task_id", "N/A")}')
    
    return config

def get_page_dimensions(page_path: str) -> tuple[int, int]:
    """
    从页面的CSS模块文件中提取页面尺寸

    Args:
        page_path: 页面路径，如 'chengdu-tour'

    Returns:
        (width, height) 元组
    """
    # 尝试两种可能的CSS文件名
    possible_css_files = [
        Path(f'project/src/app/{page_path}/page.module.css'),
        Path(f'project/src/app/{page_path}/{page_path}.module.css')
    ]

    css_file = None
    for possible_file in possible_css_files:
        if possible_file.exists():
            css_file = possible_file
            break

    if not css_file:
        print(f'⚠️ CSS文件不存在，使用默认尺寸 1440×1920')
        return (1440, 1920)

    # 读取CSS文件
    css_content = css_file.read_text(encoding='utf-8')

    # 尝试提取 .pageContainer 或 .container 中的 width 和 height
    patterns = [
        (r'\.pageContainer\s*\{[^}]*width:\s*(\d+)px[^}]*height:\s*(\d+)px', 'pageContainer'),
        (r'\.container\s*\{[^}]*width:\s*(\d+)px[^}]*height:\s*(\d+)px', 'container')
    ]

    for pattern, name in patterns:
        match = re.search(pattern, css_content, re.DOTALL)
        if match:
            width = int(match.group(1))
            height = int(match.group(2))
            print(f'📐 从CSS获取页面尺寸 (.{name}): {width}×{height}')
            return (width, height)

    print(f'⚠️ 无法从CSS提取尺寸，使用默认尺寸 1440×1920')
    return (1440, 1920)

async def replace_and_screenshot(task_item: dict, page_config: dict, output_config: dict, execution_config: dict):
    """
    替换图片并截图

    Args:
        task_item: 单个任务项配置
        page_config: 页面配置
        output_config: 输出配置
        execution_config: 执行配置
    """
    json_file = task_item['json_file']
    output_name = task_item['output_name']
    page_path = page_config['page_path']
    page_url = page_config['page_url']

    # 检测替换模式: replace_mapping (精确模式) 或 css_selector (通用模式)
    use_mapping = 'replace_mapping' in page_config and page_config['replace_mapping']

    # 读取JSON文件
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f'\n📦 处理: {output_name}')
    print(f'📄 JSON文件: {json_file}')

    if use_mapping:
        # 精确映射模式
        replace_mapping = page_config['replace_mapping']
        print(f'🎯 替换模式: 精确映射 ({len(replace_mapping)} 个节点)')
        # 构建映射字典: {json_key: {url, css_selector}}
        url_mapping = {}
        for mapping_item in replace_mapping:
            json_key = mapping_item['json_key']
            if json_key in data and data[json_key]:
                url = data[json_key][0] if isinstance(data[json_key], list) else data[json_key]
                url_mapping[mapping_item['css_selector']] = url
        print(f'🔗 准备替换 {len(url_mapping)} 个节点')
    else:
        # 通用选择器模式
        selector = page_config['css_selector']
        print(f'🎯 替换模式: 通用选择器 ({selector})')
        urls = [list(urls)[0] for urls in data.values()]
        print(f'🔗 找到 {len(urls)} 个URL')

    # 从CSS获取页面尺寸（如果启用自动尺寸）
    if output_config.get('auto_dimensions', True):
        width, height = get_page_dimensions(page_path)
    else:
        # 优先使用page_config中的尺寸
        width = page_config.get('page_width', output_config.get('width', 1440))
        height = page_config.get('page_height', output_config.get('height', 1920))

    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=execution_config.get('headless', True))
        # 使用从CSS提取的页面尺寸
        print(f'🖥️ 设置浏览器viewport: {width}×{height}')
        page = await browser.new_page(viewport={'width': width, 'height': height})

        # 导航到页面
        print(f'📄 正在打开页面 {page_url}')
        await page.goto(page_url, wait_until='load', timeout=execution_config.get('timeout', 60000))

        # 等待一下让CSS和图片加载
        await asyncio.sleep(0.5)  # 优化: 从1秒减少到0.5秒

        # 批量替换图片
        print(f'🔄 正在替换图片...')

        if use_mapping:
            # 精确映射模式: 根据css_selector精确替换每个节点
            result = await page.evaluate('''
                async (urlMapping) => {
                    let success = 0;
                    let failed = 0;
                    const mode = 'precise-mapping';

                    for (const [cssSelector, url] of Object.entries(urlMapping)) {
                        try {
                            const element = document.querySelector(cssSelector);
                            if (element) {
                                // 使用双引号包裹URL，避免单引号与URL中的特殊字符冲突
                                element.style.backgroundImage = `url("${url}")`;
                                element.style.backgroundSize = 'cover';
                                element.style.backgroundPosition = 'center';
                                element.style.backgroundRepeat = 'no-repeat';
                                console.log(`✅ Replaced ${cssSelector}: ${url.substring(0, 60)}...`);
                                success++;
                            } else {
                                console.error(`❌ Element not found: ${cssSelector}`);
                                failed++;
                            }
                        } catch (e) {
                            console.error(`❌ Error setting ${cssSelector}:`, e);
                            failed++;
                        }
                    }

                    return { success, failed, mode };
                }
            ''', url_mapping)
        else:
            # 通用选择器模式: 按DOM顺序批量替换
            result = await page.evaluate(f'''
                async ({{ urls, selector }}) => {{
                    let success = 0;
                    let failed = 0;
                    let mode = 'unknown';

                    // 先尝试查找<img>元素
                    const imgElements = document.querySelectorAll(`img${{selector}}`);

                    if (imgElements.length > 0) {{
                        // 模式1: <img>标签替换src
                        mode = 'img-src';
                        for (let i = 0; i < imgElements.length && i < urls.length; i++) {{
                            try {{
                                imgElements[i].src = urls[i];
                                await new Promise(resolve => {{
                                    if (imgElements[i].complete) {{
                                        resolve();
                                    }} else {{
                                        imgElements[i].onload = resolve;
                                        imgElements[i].onerror = resolve;
                                    }}
                                }});
                                success++;
                            }} catch (e) {{
                                console.error('Error setting img src:', e);
                                failed++;
                            }}
                        }}
                    }} else {{
                        // 模式2: <div>背景图片替换（通用选择器）
                        mode = 'div-background';
                        const elements = document.querySelectorAll(selector);
                        console.log(`找到 ${{elements.length}} 个 ${{selector}} 元素`);

                        for (let i = 0; i < elements.length && i < urls.length; i++) {{
                            try {{
                                if (elements[i]) {{
                                    // 使用双引号包裹URL，避免单引号与URL中的特殊字符冲突
                                    elements[i].style.backgroundImage = `url("${{urls[i]}}")`;
                                    elements[i].style.backgroundSize = 'cover';
                                    elements[i].style.backgroundPosition = 'center';
                                    elements[i].style.backgroundRepeat = 'no-repeat';
                                    console.log(`✅ Set background for element ${{i}}: ${{urls[i].substring(0, 60)}}...`);
                                    success++;
                                }} else {{
                                    console.error(`❌ Element ${{i}} not found`);
                                    failed++;
                                }}
                            }} catch (e) {{
                                console.error(`❌ Error setting background for element ${{i}}:`, e);
                                failed++;
                            }}
                        }}
                    }}

                    return {{ success, failed, mode }};
                }}
            ''', {'urls': urls, 'selector': selector})

        mode_map = {
            'img-src': '图片src',
            'div-background': '背景图片',
            'precise-mapping': '精确映射'
        }
        mode_text = mode_map.get(result['mode'], result['mode'])
        print(f'✅ 替换完成 ({mode_text}模式): {result["success"]} 成功, {result["failed"]} 失败')

        # 等待背景图片加载完成
        if result['mode'] in ['div-background', 'precise-mapping']:
            print('⏳ 等待背景图片加载完成...')

            # 方法1: 等待所有背景图片加载完成
            if use_mapping:
                # 精确映射模式: 等待所有映射节点的背景图片
                await page.evaluate('''
                    async (cssSelectors) => {
                        const elements = cssSelectors.map(sel => document.querySelector(sel)).filter(el => el);
                        const loadPromises = [];

                        for (let i = 0; i < elements.length; i++) {
                            const element = elements[i];
                            const bgImage = window.getComputedStyle(element).backgroundImage;
                            const urlMatch = bgImage.match(/url\\(["']?([^"')]+)["']?\\)/);
                            if (urlMatch && urlMatch[1]) {
                                const url = urlMatch[1];
                                const promise = new Promise((resolve) => {
                                    const img = new Image();
                                    img.onload = () => {
                                        console.log(`✅ Background image loaded: element ${i}`);
                                        resolve();
                                    };
                                    img.onerror = () => {
                                        console.warn(`⚠️ Background image failed: element ${i}`);
                                        resolve();
                                    };
                                    img.src = url;
                                    if (img.complete) {
                                        console.log(`✅ Background image cached: element ${i}`);
                                        resolve();
                                    }
                                });
                                loadPromises.push(promise);
                            }
                        }

                        await Promise.all(loadPromises);
                        console.log('✅ All background images loaded');
                    }
                ''', list(url_mapping.keys()))
            else:
                # 通用选择器模式: 等待selector匹配的所有元素
                await page.evaluate(f'''
                    async (selector) => {{
                        const elements = document.querySelectorAll(selector);
                    const loadPromises = [];

                    for (let i = 0; i < elements.length; i++) {{
                        const element = elements[i];
                        if (element) {{
                            const bgImage = window.getComputedStyle(element).backgroundImage;
                            // 提取URL
                            const urlMatch = bgImage.match(/url\\(["']?([^"')]+)["']?\\)/);
                            if (urlMatch && urlMatch[1]) {{
                                const url = urlMatch[1];
                                // 创建Image对象来预加载
                                const promise = new Promise((resolve) => {{
                                    const img = new Image();
                                    img.onload = () => {{
                                        console.log(`✅ Background image loaded: element ${{i}}`);
                                        resolve();
                                    }};
                                    img.onerror = () => {{
                                        console.warn(`⚠️ Background image failed: element ${{i}}`);
                                        resolve(); // 即使失败也继续
                                    }};
                                    img.src = url;

                                    // 如果图片已经在缓存中，立即resolve
                                    if (img.complete) {{
                                        console.log(`✅ Background image cached: element ${{i}}`);
                                        resolve();
                                    }}
                                }});
                                loadPromises.push(promise);
                            }}
                        }}
                    }}

                        // 等待所有图片加载完成
                        await Promise.all(loadPromises);
                        console.log('✅ All background images loaded');
                    }}
                ''', selector)

            # 方法2: 额外等待确保渲染完成
            await asyncio.sleep(2)
            print('✅ 背景图片加载完成')
        else:
            # img模式：等待网络空闲
            await page.wait_for_load_state('networkidle', timeout=10000)

        # 额外等待确保图片渲染完成
        await asyncio.sleep(execution_config.get('wait_after_replace', 3))

        # 调整页面样式，确保容器完全占满视口，消除边距
        await page.evaluate('''
            () => {
                // 移除body的默认边距
                document.body.style.margin = '0';
                document.body.style.padding = '0';
                document.body.style.overflow = 'hidden';
                
                // 找到主容器并调整样式
                const container = document.querySelector('main');
                if (container) {
                    container.style.margin = '0';
                    container.style.position = 'absolute';
                    container.style.top = '0';
                    container.style.left = '0';
                }
            }
        ''')

        # 再等待一下确保样式应用 (优化: 从0.5秒减少到0.2秒)
        await asyncio.sleep(0.2)

        # 获取container的实际位置
        container_box = await page.evaluate('''
            () => {
                const container = document.querySelector('.pageContainer');
                if (container) {
                    const box = container.getBoundingClientRect();
                    return {x: box.x, y: box.y, width: box.width, height: box.height};
                }
                return null;
            }
        ''')

        if container_box:
            print(f'📐 Container实际位置: x={container_box["x"]}, y={container_box["y"]}, width={container_box["width"]}, height={container_box["height"]}')
        else:
            print('⚠️ 未找到.pageContainer元素，使用默认clip参数')
            container_box = {'x': 0, 'y': 0, 'width': width, 'height': height}

        # 截图
        output_dir = Path(output_config.get('output_dir', 'output/model'))
        output_dir.mkdir(parents=True, exist_ok=True)

        screenshot_format = output_config.get('screenshot_format', 'png')
        output_path = output_dir / f'{output_name}.{screenshot_format}'

        print(f'📸 正在截图到: {output_path}')
        # 使用container的实际位置进行截图
        await page.screenshot(
            path=str(output_path),
            clip={'x': container_box['x'], 'y': container_box['y'], 'width': container_box['width'], 'height': container_box['height']}
        )
        print(f'✅ 截图已保存')

        await browser.close()

        return {
            'output_name': output_name,
            'success': result['success'],
            'failed': result['failed'],
            'screenshot': str(output_path)
        }

async def main(config_path: str = 'scripts/configs/batch_replace/task_config.json'):
    """
    主函数 - 从配置文件读取任务并执行(并发版本)

    Args:
        config_path: 配置文件路径
    """
    # 加载配置
    config = load_config(config_path)

    page_config = config.get('page_config', {})
    output_config = config.get('output_config', {})
    execution_config = config.get('execution_config', {})
    input_files = config.get('input_files', [])

    # 并发配置: 同时处理的任务数
    CONCURRENT_TASKS = 1  # 串行执行(Next.js开发服务器无法承受并发)

    results = []

    print('=' * 60)
    print(f'🚀 开始批量处理 {len(input_files)} 组图片 (并发数: {CONCURRENT_TASKS})')
    print('=' * 60)

    # 并发处理任务
    async def process_task(task_item):
        try:
            result = await replace_and_screenshot(
                task_item,
                page_config,
                output_config,
                execution_config
            )
            return {
                **result,
                'status': 'success'
            }
        except Exception as e:
            print(f'❌ 处理失败: {e}')
            return {
                'output_name': task_item.get('output_name', 'unknown'),
                'error': str(e),
                'status': 'failed'
            }

    # 分批并发处理
    for i in range(0, len(input_files), CONCURRENT_TASKS):
        batch = input_files[i:i+CONCURRENT_TASKS]
        print(f'\n📦 处理批次 {i//CONCURRENT_TASKS + 1}/{(len(input_files)-1)//CONCURRENT_TASKS + 1} ({len(batch)} 组)')

        # 并发执行当前批次
        batch_results = await asyncio.gather(*[process_task(task) for task in batch])
        results.extend(batch_results)

    # 输出总结
    print('\n' + '=' * 60)
    print('📊 处理总结')
    print('=' * 60)

    for i, result in enumerate(results, 1):
        print(f'\n第{i}组 - {result["output_name"]}:')
        if result['status'] == 'success':
            print(f'  ✅ 成功: {result["success"]} 张')
            print(f'  ❌ 失败: {result["failed"]} 张')
            print(f'  📸 截图: {result["screenshot"]}')
        else:
            print(f'  ❌ 错误: {result["error"]}')

    print('\n' + '=' * 60)
    print('🎉 全部完成!')
    print('=' * 60)

if __name__ == '__main__':
    # 支持命令行参数指定配置文件
    config_path = sys.argv[1] if len(sys.argv) > 1 else 'scripts/configs/batch_replace/task_config.json'
    asyncio.run(main(config_path))

