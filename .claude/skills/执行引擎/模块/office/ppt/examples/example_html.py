"""
Example: HTML to PPT Conversion

This example demonstrates converting HTML content to PowerPoint
using the HTMLtoPPTConverter class.
"""

import sys
from pathlib import Path

# Add skill to path
skill_path = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(skill_path))

from html_to_ppt_converter import convert_html_to_ppt


def create_technical_presentation():
    """Create a technical presentation from HTML content."""

    html_content = """
    <!DOCTYPE html>
    <html>
    <body>
        <section>
            <h1>ZTL数智化作战中心技术架构</h1>
            <p>基于Claude Code和MCP协议的智能体协作平台</p>
        </section>

        <section>
            <h2>核心技术栈</h2>
            <ul>
                <li>AI引擎: Claude Sonnet 4.5</li>
                <li>开发框架: Claude Code v1.0+</li>
                <li>协议标准: MCP (Model Context Protocol)</li>
                <li>编程语言: Python 3.10+, Markdown</li>
                <li>集成能力: OpenRouter API, GitHub API, 飞书API</li>
            </ul>
        </section>

        <section>
            <h2>三层架构</h2>
            <table>
                <thead>
                    <tr>
                        <th>层级</th>
                        <th>组件</th>
                        <th>功能</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Layer 1</td>
                        <td>Agents + Skills</td>
                        <td>知识层：角色决策框架和工具能力包</td>
                    </tr>
                    <tr>
                        <td>Layer 2</td>
                        <td>Claude Reasoning</td>
                        <td>决策编排层：运行时智能决策和能力组合</td>
                    </tr>
                    <tr>
                        <td>Layer 3</td>
                        <td>Tools + Output</td>
                        <td>执行输出层：工具调用和结果产出</td>
                    </tr>
                </tbody>
            </table>
        </section>

        <section>
            <h2>智能体系统</h2>
            <p>66个专业智能体覆盖6大业务组：</p>
            <ol>
                <li>战略组 (G系列): 战略规划、经营分析、产品力打造</li>
                <li>创意组 (X系列): 广告策划、文案创作、视觉设计</li>
                <li>情报组 (E系列): 数据采集、深度分析、情报研究</li>
                <li>行政组 (R系列): 财务管理、人事管理、行政协同</li>
                <li>中台组 (M系列): 美团运营、营销管理、数据报表</li>
                <li>筹建组 (Z系列): 平面设计、BIM建模、空间设计</li>
            </ol>
        </section>

        <section>
            <h2>MCP集成生态</h2>
            <table>
                <thead>
                    <tr>
                        <th>MCP服务器</th>
                        <th>功能</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>chrome-mcp</td>
                        <td>浏览器自动化操作</td>
                    </tr>
                    <tr>
                        <td>playwright-mcp</td>
                        <td>深度网页爬虫</td>
                    </tr>
                    <tr>
                        <td>context7</td>
                        <td>实时技术文档库</td>
                    </tr>
                    <tr>
                        <td>lark-mcp</td>
                        <td>飞书协同办公</td>
                    </tr>
                    <tr>
                        <td>github-mcp</td>
                        <td>代码版本管理</td>
                    </tr>
                    <tr>
                        <td>supabase-mcp</td>
                        <td>云数据库管理</td>
                    </tr>
                    <tr>
                        <td>cos-mcp</td>
                        <td>云存储管理</td>
                    </tr>
                </tbody>
            </table>
        </section>

        <section>
            <h2>技术优势</h2>
            <ul>
                <li>智能化: 基于Claude Sonnet 4.5的强大推理能力</li>
                <li>模块化: 66个专业智能体独立又协同</li>
                <li>标准化: 遵循MCP协议，易于扩展集成</li>
                <li>自包含: Skills采用自包含设计，便于维护</li>
                <li>可视化: 丰富的可视化报表和数据看板</li>
            </ul>
        </section>

        <section>
            <h2>应用场景</h2>
            <p>适用于以下餐饮行业数智化场景：</p>
            <ul>
                <li>战略规划与经营分析</li>
                <li>品牌营销与内容创作</li>
                <li>市场情报与竞品分析</li>
                <li>财务管理与行政协同</li>
                <li>运营优化与数据分析</li>
                <li>新店筹建与空间设计</li>
            </ul>
        </section>
    </body>
    </html>
    """

    # Convert HTML to PPT
    result = convert_html_to_ppt(
        html_content=html_content,
        output_path="output/行政组/技术手册/ztl-technical-architecture.pptx"
    )

    if result["success"]:
        print(f"✅ 技术演示已生成: {result['file_path']}")
        print(f"📊 幻灯片数量: {result['slide_count']}")
        print(f"📄 文件大小: {result['size_bytes']:,} bytes")
    else:
        print(f"❌ 生成失败: {result['error']}")


if __name__ == "__main__":
    create_technical_presentation()
