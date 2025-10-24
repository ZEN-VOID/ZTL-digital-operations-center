#!/bin/bash

# ZTL数智化作战中心 - 本地开发服务器启动脚本
# 用途: 通过HTTP服务器正确访问项目介绍页面，解决file://协议的限制

echo "🚀 启动ZTL数智化作战中心开发服务器..."
echo ""
echo "📍 服务器地址: http://localhost:8000"
echo "📍 首页地址: http://localhost:8000/pages/index.html"
echo "📍 OUTPUT页面: http://localhost:8000/pages/output.html"
echo ""
echo "💡 使用方法:"
echo "   1. 在浏览器中打开: http://localhost:8000/pages/output.html"
echo "   2. 点击图片可以放大预览"
echo "   3. 点击文档按钮可以查看/下载"
echo ""
echo "⚠️  提示: 请勿直接双击HTML文件打开，必须通过HTTP服务器访问"
echo "⚠️  停止服务器: 按 Ctrl+C"
echo ""
echo "================================"
echo ""

# 切换到project-instructions目录
cd "$(dirname "$0")" || exit

# 启动Python HTTP服务器
if command -v python3 &> /dev/null; then
    python3 -m http.server 8000
elif command -v python &> /dev/null; then
    python -m http.server 8000
else
    echo "❌ 错误: 未找到Python，无法启动服务器"
    exit 1
fi
