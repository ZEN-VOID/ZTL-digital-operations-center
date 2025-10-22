"""
Example: HTML to PDF Conversion

Demonstrates creating marketing materials using HTML and CSS.
Best for web-style documents with rich styling.
"""

import sys
from pathlib import Path

# Add skill to path
skill_path = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(skill_path))

from pdf_generator import create_pdf_from_html


def create_marketing_brochure():
    """Create a marketing brochure using HTML and CSS."""

    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <style>
            @page {
                size: A4;
                margin: 2cm;
            }

            body {
                font-family: 'SimHei', 'Microsoft YaHei', sans-serif;
                line-height: 1.6;
                color: #333;
            }

            .header {
                text-align: center;
                padding: 20px 0;
                border-bottom: 3px solid #e74c3c;
                margin-bottom: 30px;
            }

            h1 {
                color: #e74c3c;
                font-size: 32px;
                margin: 0;
            }

            .subtitle {
                color: #7f8c8d;
                font-size: 16px;
                margin-top: 10px;
            }

            .section {
                margin-bottom: 30px;
            }

            h2 {
                color: #2c3e50;
                border-left: 5px solid #e74c3c;
                padding-left: 10px;
                margin-bottom: 15px;
            }

            .highlight-box {
                background-color: #fef5e7;
                border-left: 4px solid #f39c12;
                padding: 15px;
                margin: 20px 0;
            }

            .menu-grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
                margin: 20px 0;
            }

            .menu-item {
                border: 2px solid #ecf0f1;
                border-radius: 8px;
                padding: 15px;
            }

            .menu-item h3 {
                color: #e74c3c;
                margin-top: 0;
            }

            .price {
                color: #27ae60;
                font-size: 20px;
                font-weight: bold;
            }

            .footer {
                text-align: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 2px solid #ecf0f1;
                color: #7f8c8d;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>火锅江湖</h1>
            <div class="subtitle">正宗川渝火锅 · 匠心传承</div>
        </div>

        <div class="section">
            <h2>品牌故事</h2>
            <p>
                火锅江湖成立于2015年，致力于传承正宗川渝火锅文化。我们精选优质食材，
                采用传统工艺熬制锅底，为食客呈现最地道的麻辣鲜香。
            </p>

            <div class="highlight-box">
                <strong>核心理念：</strong>用心做好每一锅火锅，让每一位顾客感受到家的温暖
            </div>
        </div>

        <div class="section">
            <h2>招牌菜品</h2>

            <div class="menu-grid">
                <div class="menu-item">
                    <h3>🌶️ 麻辣牛油锅底</h3>
                    <p>精选牛油，配以数十种香料秘制而成，麻辣鲜香，回味无穷。</p>
                    <div class="price">¥68/锅</div>
                </div>

                <div class="menu-item">
                    <h3>🥘 养生菌汤锅底</h3>
                    <p>多种珍稀菌菇熬制，清淡鲜美，营养丰富，老少皆宜。</p>
                    <div class="price">¥58/锅</div>
                </div>

                <div class="menu-item">
                    <h3>🦐 鲜切羊肉</h3>
                    <p>内蒙古新鲜羊肉，现切现涮，肉质鲜嫩，入口即化。</p>
                    <div class="price">¥48/份</div>
                </div>

                <div class="menu-item">
                    <h3>🥩 精品肥牛</h3>
                    <p>澳洲进口肥牛，大理石纹路清晰，口感细腻滑嫩。</p>
                    <div class="price">¥58/份</div>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>门店信息</h2>
            <ul>
                <li><strong>总店：</strong>成都市武侯区天府大道999号（营业时间：10:00-23:00）</li>
                <li><strong>分店：</strong>成都市高新区软件园B区（营业时间：11:00-22:00）</li>
                <li><strong>外卖电话：</strong>400-123-4567</li>
                <li><strong>微信公众号：</strong>火锅江湖Official</li>
            </ul>
        </div>

        <div class="footer">
            <p>火锅江湖 · 让每一餐都成为美好回忆</p>
            <p>www.hotpotjianghu.com | 客服热线: 400-123-4567</p>
        </div>
    </body>
    </html>
    """

    result = create_pdf_from_html(
        html_content=html_content,
        output_path="output/行政组/营销宣传/marketing-brochure.pdf"
    )

    if result["success"]:
        print(f"✅ Marketing brochure generated successfully")
        print(f"   File: {result['file_path']}")
        print(f"   Size: {result['size_bytes']:,} bytes")
        print(f"   Method: {result['method']}")
    else:
        print(f"❌ Generation failed: {result['error']}")
        if 'install_instructions' in result:
            print(f"\n📦 Installation required:")
            print(f"   {result['install_instructions']}")


if __name__ == "__main__":
    create_marketing_brochure()
