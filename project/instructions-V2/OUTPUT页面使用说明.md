# OUTPUT页面使用说明

## ⚠️ 重要提示

OUTPUT页面必须通过HTTP服务器访问，**不能直接双击HTML文件打开**！

### 为什么不能直接打开HTML文件？

当您直接双击HTML文件时，浏览器使用 `file://` 协议打开，这会导致：

1. **安全限制**: 浏览器禁止访问其他目录的文件（如 `../../output/` 路径）
2. **JavaScript限制**: 某些JavaScript功能（如动态创建元素、文件下载）被禁用
3. **相对路径失效**: 跨目录的相对路径无法正确解析

## 🚀 正确使用方法

### 方法1: 使用启动脚本（推荐）

1. **打开终端**，进入项目目录：
   ```bash
   cd "/Users/vincentlee/Desktop/ZTL数智化作战中心/project-instructions"
   ```

2. **运行启动脚本**：
   ```bash
   ./start-server.sh
   ```

3. **在浏览器中访问**：
   - 首页: http://localhost:8000/pages/index.html
   - OUTPUT页面: http://localhost:8000/pages/output.html

4. **停止服务器**: 在终端按 `Ctrl+C`

### 方法2: 手动启动Python服务器

如果启动脚本不工作，可以手动启动：

```bash
# 进入项目目录
cd "/Users/vincentlee/Desktop/ZTL数智化作战中心/project-instructions"

# 启动HTTP服务器（Python 3）
python3 -m http.server 8000

# 或者 Python 2
python -m SimpleHTTPServer 8000
```

然后在浏览器访问 http://localhost:8000/pages/output.html

## 🔧 功能说明

### 1. 图片预览功能

- **点击图片**: 在AIGC图片库中点击任意图片
- **放大预览**: 图片在全屏模态框中显示
- **关闭预览**:
  - 点击右上角 ✕ 按钮
  - 按 `ESC` 键
  - 点击图片外的暗色背景

### 2. 文档查看/下载

- **Markdown文档**: 点击"查看"按钮，在新标签页打开
- **Word文档**: 点击"下载"按钮，下载到本地
- **PDF文档**: 点击"查看"按钮，在新标签页打开

### 3. 资源筛选

- **全部资源**: 显示所有60个文件
- **图片**: 仅显示2个PNG图片文件
- **文档**: 仅显示57个Markdown和Word文档
- **PDF**: 仅显示1个PDF文件

### 4. 搜索功能

在搜索框输入关键词，实时过滤文件名匹配的资源。

## 🐛 故障排查

### 问题1: 点击图片/按钮没有反应

**原因**: 使用 `file://` 协议直接打开了HTML文件

**解决方案**:
1. 关闭当前浏览器标签页
2. 按照"正确使用方法"启动HTTP服务器
3. 通过 http://localhost:8000 访问页面

### 问题2: 图片无法加载

**检查路径**:
```bash
ls -la "/Users/vincentlee/Desktop/ZTL数智化作战中心/output/创意组/AIGC生成/images/"
```

应该看到2个PNG文件：
- `1-poster/1-poster_20251021_040057_1.png`
- `8-main-image/8-main-image_20251021_040135_1.png`

### 问题3: 文档链接失效

**检查路径**:
```bash
ls -la "/Users/vincentlee/Desktop/ZTL数智化作战中心/output/情报组/"
```

应该看到多个Markdown文件。

### 问题4: JavaScript函数未定义

**打开浏览器开发者工具**:
- Chrome/Edge: 按 `F12` 或 `Cmd+Option+I` (Mac)
- Firefox: 按 `F12` 或 `Cmd+Option+K` (Mac)
- Safari: `Cmd+Option+C` (Mac，需先在偏好设置中启用开发者菜单)

**查看Console标签页**，应该看到：
```
✅ output.js script loading...
✅ output.js fully loaded
🔧 Available functions: {
    scrollToDept: "function",
    toggleFolder: "function",
    ...
    previewImage: "function",
    viewDocument: "function",
    downloadFile: "function"
}
```

如果看到错误信息，请截图并报告。

## 📊 当前资源统计

- **总文件数**: 60个
- **图片文件**: 2个 PNG（创意组/AIGC生成）
- **Markdown文档**: 54个（主要在情报组）
- **Word文档**: 3个（行政组）
- **PDF文档**: 1个（创意组）

### 文件分布

| 业务组 | 文件数量 | 文件类型 |
|--------|---------|---------|
| 创意组 | 3 | 2个PNG + 1个PDF |
| 情报组 | 54 | 54个Markdown |
| 行政组 | 3 | 3个Word文档 |

## 🆘 获取帮助

如果按照以上步骤仍然无法正常使用，请提供以下信息：

1. 使用的浏览器和版本
2. 访问的URL（file:// 还是 http://localhost:8000）
3. 浏览器Console中的错误信息
4. 具体哪个功能不工作（图片预览/文档查看/搜索筛选）

---

**最后更新**: 2025-10-24
**维护者**: ZTL数智化作战中心
