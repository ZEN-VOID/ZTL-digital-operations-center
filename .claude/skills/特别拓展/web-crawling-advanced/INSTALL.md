# Web Crawling Advanced - 安装指南

## 📋 系统要求

- **Python**: 3.10+
- **操作系统**: macOS / Linux / Windows
- **内存**: 建议4GB以上
- **网络**: 需要访问外网（用于下载浏览器驱动）

---

## 🚀 快速安装

### 方法1: 使用pip安装（推荐）

```bash
# 1. 安装Crawlee及所有依赖
pip3 install 'crawlee[all]'

# 2. 安装Playwright浏览器驱动
playwright install chromium

# 3. 验证安装
python3 -c "from crawlee import __version__; print(f'✅ Crawlee {__version__} 安装成功')"
```

### 方法2: 使用requirements.txt安装

```bash
# 进入Skill目录
cd .claude/skills/web-crawling-advanced/

# 安装依赖
pip3 install -r requirements.txt

# 安装浏览器驱动
playwright install chromium
```

---

## ⚠️ 常见问题

### Q1: Pydantic兼容性错误

**错误信息**:
```
TypeError: cannot specify both default and default_factory
```

**解决方案**:
```bash
# 降级Pydantic到兼容版本
pip3 install 'pydantic<2.12,>=2.6'

# 或指定具体版本
pip3 install pydantic==2.11.10
```

### Q2: Playwright浏览器驱动下载失败

**错误信息**:
```
Failed to download chromium from ...
```

**解决方案**:
```bash
# 方法1: 使用国内镜像
export PLAYWRIGHT_DOWNLOAD_HOST=https://playwright.azureedge.net
playwright install chromium

# 方法2: 使用代理
export HTTP_PROXY=http://your-proxy:port
export HTTPS_PROXY=http://your-proxy:port
playwright install chromium
```

### Q3: 权限错误

**错误信息**:
```
Permission denied
```

**解决方案**:
```bash
# 使用用户级安装
pip3 install --user 'crawlee[all]'

# 或使用sudo（不推荐）
sudo pip3 install 'crawlee[all]'
```

---

## 📦 可选依赖

### Excel导出支持

```bash
pip3 install pandas openpyxl
```

### 数据验证支持

```bash
pip3 install pydantic
```

---

## ✅ 安装验证

### 验证脚本

创建一个测试文件 `test_installation.py`:

```python
import asyncio

async def test_crawlee():
    """测试Crawlee安装"""
    try:
        from crawlee.beautifulsoup_crawler import BeautifulSoupCrawler
        from crawlee.playwright_crawler import PlaywrightCrawler

        print("✅ Crawlee导入成功")

        # 测试BeautifulSoup爬虫
        bs_crawler = BeautifulSoupCrawler()
        print("✅ BeautifulSoup爬虫创建成功")

        # 测试Playwright爬虫
        pw_crawler = PlaywrightCrawler()
        print("✅ Playwright爬虫创建成功")

        print("\n🎉 所有组件安装正常！")

    except Exception as e:
        print(f"❌ 安装验证失败: {e}")

if __name__ == '__main__':
    asyncio.run(test_crawlee())
```

运行验证:
```bash
python3 test_installation.py
```

---

## 🔧 卸载

```bash
# 卸载Crawlee
pip3 uninstall crawlee

# 卸载Playwright和浏览器驱动
pip3 uninstall playwright
rm -rf ~/Library/Caches/ms-playwright  # macOS
# rm -rf ~/.cache/ms-playwright        # Linux
```

---

## 📚 相关资源

- **Crawlee官方文档**: https://crawlee.dev/python/
- **Playwright文档**: https://playwright.dev/python/
- **BeautifulSoup文档**: https://www.crummy.com/software/BeautifulSoup/

---

**最后更新**: 2025-10-21
**维护者**: ZTL数智化作战中心-情报组
