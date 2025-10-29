# MCP快速参考 - MiniMax & shadcn/ui

## ✅ 配置状态

| MCP服务器 | 状态 | 说明 |
|-----------|------|------|
| **minimax-mcp** | ✅ 已完成 | 海螺AI (Hailuo) - 数字游牧派账户 |
| **shadcn-mcp** | ✅ 已就绪 | 可立即使用 (项目需要 `components.json`) |

**配置完成**: 2025-10-29
**账户**: 数字游牧派
**API端点**: https://api.minimax.chat (海螺AI)

---

## 🚀 立即行动

### 1️⃣ ✅ API密钥已配置

MiniMax API密钥已成功配置:
- 账户: 数字游牧派
- 平台: 海螺AI (Hailuo)
- API Host: https://api.minimax.chat

### 2️⃣ 重启Claude Code (必须)

**完全退出并重新启动Claude Code应用**,使配置生效

### 3️⃣ 验证配置

在Claude Code中运行:
```
/mcp status
```

应该看到 `minimax-mcp` 和 `shadcn-mcp` 在列表中且状态正常

---

## 📝 使用示例

### MiniMax - AI生成

**文本生成**:
```
使用MiniMax生成一篇关于火锅店营销策略的文章
```

**图像生成**:
```
使用MiniMax生成一张火锅店开业海报:
- 主题: 喜庆开业
- 风格: 中国传统红色
- 尺寸: 2:3比例
- 输出路径: output/minimax/images/
```

**输出位置** (相对于当前项目):
```
output/[项目名]/minimax/
├── videos/           # 视频生成结果
├── audios/           # 音频合成结果
├── images/           # 图像生成结果
├── texts/            # 文本生成结果
└── metadata/         # 元数据和日志
```

**路径说明**:
- 使用**相对路径** `output`,相对于当前工作目录
- 每个项目输出到自己的output目录,完全隔离
- 符合项目标准化输出路径规范

**资源模式**: `url` (返回URL链接,需手动下载)

### shadcn - UI组件

**查询组件**:
```
Show me all available shadcn components
What components are in the shadcn button category?
```

**创建页面**:
```
Create a landing page using:
- shadcn Button component
- shadcn Card component
- shadcn Input component
```

**项目配置** (在前端项目中):
```bash
pnpm dlx shadcn@latest init
pnpm dlx shadcn@latest add button card input
```

---

## 🔧 配置文件路径

| 项目 | 路径 |
|------|------|
| **MCP配置** | `/Library/Application Support/ClaudeCode/managed-mcp.json` |
| **MiniMax输出** | `output/minimax/` |
| **shadcn项目配置** | `components.json` (项目根目录) |

---

## 📚 API密钥获取

### MiniMax (中国大陆)
1. 访问: https://platform.minimaxi.com/
2. 登录账号
3. 导航: 用户中心 → 基本信息 → 接口密钥
4. 创建或复制API密钥

### MiniMax (全球)
1. 访问: https://www.minimax.io/
2. 登录账号
3. 导航: User Center → Basic Information → Interface Key
4. 创建或复制API密钥

⚠️ **重要**:
- 中国大陆用户使用 `api.minimaxi.com`
- 全球用户使用 `api.minimax.io`
- API Host和密钥必须匹配区域

---

## 🐛 常见问题

### MiniMax

**Q: Invalid API key 错误?**
- ✅ 检查密钥格式是否正确
- ✅ 确认API Host和密钥来自同一区域
- ✅ 检查密钥是否有效(未过期)

**Q: uvx命令找不到?**
```bash
# 安装uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 重启终端
exec $SHELL
```

**Q: 输出文件保存在哪里?**
- 默认路径: `output/minimax/`
- 可通过 `MINIMAX_MCP_BASE_PATH` 环境变量修改

### shadcn

**Q: Registry not found?**
- ✅ 在项目中运行 `pnpm dlx shadcn@latest init`
- ✅ 确认 `components.json` 存在于项目根目录

**Q: 组件无法安装?**
- ✅ 检查网络连接
- ✅ 确认 `package.json` 中有 `tailwindcss` 依赖
- ✅ 运行 `pnpm install` 安装依赖

**Q: 如何使用自定义注册表?**
在 `components.json` 中添加:
```json
{
  "registries": {
    "@custom": "https://example.com/registry/{name}.json"
  }
}
```

---

## 📖 完整文档

详细说明请查看:
- `docs/MCP配置说明-MiniMax和Shadcn.md`

相关链接:
- [MiniMax GitHub](https://github.com/MiniMax-AI/MiniMax-MCP)
- [shadcn/ui MCP](https://ui.shadcn.com/docs/registry/mcp)
- [MCP协议](https://modelcontextprotocol.io/)

---

**更新时间**: 2025-10-29
**配置人**: Claude Code Agent
**状态**: ✅ 配置完成 - 已配置海螺AI (数字游牧派账户)
