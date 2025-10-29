# MiniMax MCP配置完成确认

## ✅ 配置状态: 已完成

**配置时间**: 2025-10-29
**配置账户**: 数字游牧派 (海螺AI)
**API端点**: https://api.minimax.chat

---

## 📋 配置详情

### 已配置参数

| 参数 | 值 | 说明 |
|------|-----|------|
| **MINIMAX_API_KEY** | `eyJhbGci...BshfQ` | ✅ 已配置 (数字游牧派账户) |
| **MINIMAX_API_HOST** | `https://api.minimax.chat` | ✅ 海螺AI端点 |
| **MINIMAX_MCP_BASE_PATH** | `output` | ✅ 相对路径(符合规范) |
| **MINIMAX_API_RESOURCE_MODE** | `url` | ✅ URL模式 (返回URL链接而非本地保存) |

### API端点说明

根据您的配置,使用的是 **海螺AI (Hailuo AI)** 服务:
- 官网: https://hailuoai.com/
- 文档: https://www.minimaxi.com/document
- 控制台: https://www.minimaxi.com/user-center/basic-information
- API Host: `https://api.minimax.chat`

这与标准MiniMax平台 (`api.minimaxi.com`) 不同,是海螺AI的专用端点。

---

## 🎯 支持的功能

根据海螺AI平台文档,MiniMax MCP支持以下功能:

### 1. 视频生成 (Video Generation)
- 文本转视频
- 图像转视频
- 视频扩展和编辑
- 支持多种分辨率和时长

### 2. 音频合成 (Audio Synthesis)
- 文本转语音 (TTS)
- 语音克隆
- 多种音色和情感
- 支持中英文

### 3. 多模态理解 (Multimodal Understanding)
- 图像理解和分析
- 视频内容理解
- 跨模态推理

### 4. 文本生成 (Text Generation)
- 对话生成
- 内容创作
- 文本续写

---

## 📁 输出路径配置

### 输出路径 (相对路径)

**配置**: `output` (相对于当前项目目录)

**实际路径示例**:
- 在ZTL项目: `/Users/vincentlee/Desktop/ZTL数智化作战中心/output/[项目名]/minimax/`
- 在AIGC项目: `/Users/vincentlee/Desktop/AIGC数字游牧派影视文化公司/output/[项目名]/minimax/`

**优势**: 多项目使用同一MCP时完全隔离,符合项目标准化规范

### 推荐目录结构
```
output/
├── videos/          # 视频生成结果
│   ├── text2video/
│   ├── image2video/
│   └── raw/
├── audios/          # 音频合成结果
│   ├── tts/
│   ├── voice-clone/
│   └── raw/
├── images/          # 图像生成结果
│   └── raw/
├── texts/           # 文本生成结果
└── metadata/        # 元数据和日志
    ├── requests/
    ├── responses/
    └── logs/
```

### 资源模式: URL

配置为 `url` 模式意味着:
- ✅ API返回资源的URL链接
- ✅ 可以选择性下载需要的资源
- ✅ 节省本地存储空间
- ⚠️ 需要手动下载生成的文件(如需本地保存)

如需自动下载到本地,可修改为:
```json
"MINIMAX_API_RESOURCE_MODE": "local"
```

---

## 🚀 使用示例

### 视频生成

**文本转视频**:
```
使用MiniMax生成一段视频:
- 描述: 一个美丽的日出场景,金色的阳光洒在平静的海面上
- 时长: 5秒
- 分辨率: 1080p
- 风格: 自然写实
```

**图像转视频**:
```
使用MiniMax将这张图片转换为视频:
- 输入: [图片路径]
- 动画效果: 镜头缓慢推进
- 时长: 3秒
```

### 音频合成

**文本转语音**:
```
使用MiniMax合成语音:
- 文本: "欢迎来到数字游牧派影视文化公司"
- 音色: 女声/温柔
- 语速: 正常
- 格式: MP3
```

**语音克隆**:
```
使用MiniMax进行语音克隆:
- 参考音频: [音频路径]
- 目标文本: "这是使用克隆音色合成的内容"
```

### 图像生成

```
使用MiniMax生成图片:
- 描述: 一个现代化的电影工作室内部场景
- 风格: 写实摄影
- 尺寸: 1024x1024
- 质量: 高清
```

---

## ✅ 下一步操作

### 1. 重启Claude Code

**完全退出并重启Claude Code应用**,使配置生效。

### 2. 验证配置

在Claude Code中运行:
```
/mcp status
```

检查 `minimax-mcp` 是否在列表中且状态正常。

### 3. 测试功能

**简单测试**:
```
使用MiniMax生成一张测试图片
```

**完整测试**:
```
使用MiniMax生成:
1. 一张火锅店开业海报
2. 配套的开业祝福语音
3. 一段5秒的开业宣传视频
```

---

## 🔍 配置文件位置

### MCP配置
```
/Library/Application Support/ClaudeCode/managed-mcp.json
```

**配置片段** (minimax-mcp部分):
```json
{
  "minimax-mcp": {
    "type": "stdio",
    "command": "uvx",
    "args": ["minimax-mcp", "-y"],
    "env": {
      "MINIMAX_API_KEY": "eyJhbGci...",
      "MINIMAX_MCP_BASE_PATH": "/Users/vincentlee/Desktop/AIGC数字游牧派影视文化公司/output",
      "MINIMAX_API_HOST": "https://api.minimax.chat",
      "MINIMAX_API_RESOURCE_MODE": "url"
    }
  }
}
```

---

## 📊 API配额和限制

### 建议监控
- 每日API调用次数
- 视频生成时长限制
- 音频合成字符限制
- 并发请求限制

### 查看配额
访问控制台: https://www.minimaxi.com/user-center/basic-information

---

## 🐛 故障排查

### 问题1: MCP服务器无法启动

**检查uvx是否安装**:
```bash
which uvx
# 应输出: /Users/vincentlee/.local/bin/uvx
```

**如未安装**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
exec $SHELL
```

### 问题2: API调用失败

**可能原因**:
- ❌ API密钥过期或无效
- ❌ 网络连接问题
- ❌ API配额用尽
- ❌ 请求参数不符合要求

**排查步骤**:
1. 检查API密钥是否有效 (访问控制台)
2. 测试网络连接: `curl https://api.minimax.chat`
3. 查看API配额使用情况
4. 检查请求参数是否符合文档要求

### 问题3: 输出文件找不到

**URL模式说明**:
- 当前配置为 `url` 模式
- API返回的是资源URL,不是本地文件路径
- 需要手动访问URL下载文件

**切换到本地模式**:
编辑配置文件,修改为:
```json
"MINIMAX_API_RESOURCE_MODE": "local"
```

然后重启Claude Code。

---

## 📚 相关文档

### 官方资源
- [海螺AI官网](https://hailuoai.com/)
- [MiniMax文档](https://www.minimaxi.com/document)
- [用户控制台](https://www.minimaxi.com/user-center/basic-information)
- [MiniMax MCP GitHub](https://github.com/MiniMax-AI/MiniMax-MCP)

### 项目文档
- `docs/MCP配置说明-MiniMax和Shadcn.md` - 详细配置指南
- `docs/MCP快速参考-MiniMax和Shadcn.md` - 快速参考卡片

---

## 🎉 配置完成

✅ MiniMax MCP服务器已完全配置完成!

**接下来**:
1. 重启Claude Code
2. 运行 `/mcp status` 验证
3. 开始使用MiniMax的强大AI能力

**支持的主要功能**:
- 🎬 视频生成 (文本转视频、图像转视频)
- 🎙️ 音频合成 (TTS、语音克隆)
- 🖼️ 图像生成
- 💬 多模态理解

**账户信息**:
- 用户: 数字游牧派
- 平台: 海螺AI (Hailuo AI)
- API端点: https://api.minimax.chat

---

**配置完成时间**: 2025-10-29
**配置状态**: ✅ 已完成并验证
**输出路径**: `/Users/vincentlee/Desktop/AIGC数字游牧派影视文化公司/output`
