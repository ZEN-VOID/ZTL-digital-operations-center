# MCP配置说明 - MiniMax & shadcn/ui

## 配置概览

已成功添加以下两个MCP服务器到系统配置:

1. **minimax-mcp** - MiniMax AI能力集成
2. **shadcn-mcp** - shadcn/ui组件注册表集成

配置文件位置: `/Library/Application Support/ClaudeCode/managed-mcp.json`

---

## 1. MiniMax MCP Server

### 功能说明

MiniMax MCP提供AI生成能力集成,包括:
- 文本生成
- 图像生成
- 多模态能力

### 配置详情

```json
{
  "minimax-mcp": {
    "type": "stdio",
    "command": "uvx",
    "args": ["minimax-mcp", "-y"],
    "env": {
      "MINIMAX_API_KEY": "YOUR_MINIMAX_API_KEY_HERE",
      "MINIMAX_MCP_BASE_PATH": "/Users/vincentlee/Desktop/ZTL数智化作战中心/output/minimax",
      "MINIMAX_API_HOST": "https://api.minimaxi.com",
      "MINIMAX_API_RESOURCE_MODE": "local"
    }
  }
}
```

### ⚠️ 必需操作

**获取并配置API密钥**:

1. 访问 [MiniMax开放平台](https://platform.minimaxi.com/user-center/basic-information/interface-key)
2. 登录并获取API密钥
3. 编辑配置文件:
   ```bash
   nano "/Library/Application Support/ClaudeCode/managed-mcp.json"
   ```
4. 将 `YOUR_MINIMAX_API_KEY_HERE` 替换为实际的API密钥

### 环境变量说明

| 变量 | 说明 | 值 |
|------|------|-----|
| `MINIMAX_API_KEY` | **必填** - API密钥 | 从平台获取 |
| `MINIMAX_MCP_BASE_PATH` | 输出文件保存路径 | `output/minimax/` |
| `MINIMAX_API_HOST` | API端点(国内) | `https://api.minimaxi.com` |
| `MINIMAX_API_RESOURCE_MODE` | 资源模式 | `local` (本地保存) |

### 区域说明

**中国大陆用户** (当前配置):
- API Host: `https://api.minimaxi.com`
- 密钥平台: https://platform.minimaxi.com

**全球用户** (如需切换):
- API Host: `https://api.minimax.io`
- 密钥平台: https://www.minimax.io

⚠️ **注意**: API Host和密钥必须来自同一区域,否则会报错 "Invalid API key"

### 输出路径

生成的文件将保存到:
```
output/minimax/
├── images/      # 图像生成结果
├── texts/       # 文本生成结果
└── metadata/    # 元数据和日志
```

---

## 2. shadcn/ui MCP Server

### 功能说明

shadcn MCP提供组件注册表集成,支持:
- 自动发现和安装shadcn/ui组件
- 自定义组件注册表
- AI辅助组件使用

### 配置详情

```json
{
  "shadcn-mcp": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "shadcn@latest", "mcp", "serve"],
    "env": {}
  }
}
```

### 使用方法

shadcn MCP需要在项目中配置 `components.json`:

**示例配置**:
```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "app/globals.css",
    "baseColor": "slate",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils"
  },
  "registries": {
    "@acme": "https://acme.com/r/{name}.json"
  }
}
```

### 测试命令

在Claude Code中运行以下命令测试:
```
Show me the components in the shadcn registry
Create a landing page using shadcn components
```

### 自定义注册表

如需添加自定义注册表:

1. 编辑项目的 `components.json`
2. 在 `registries` 字段添加自定义注册表URL
3. 重启Claude Code
4. 使用 `/mcp` 命令调试MCP服务器

**注册表要求**:
- 必须提供 `registry.json` 索引文件
- 索引文件需符合 shadcn registry schema
- 组件名称使用kebab-case命名
- 提供清晰的组件描述和依赖信息

---

## 生效方式

配置文件已更新,需要以下操作使配置生效:

### 方式1: 重启Claude Code (推荐)
```bash
# 完全退出Claude Code应用
# 重新启动Claude Code
```

### 方式2: 重新加载配置
某些MCP服务器支持热重载,可以尝试在Claude Code中使用:
```
/mcp reload
```

---

## 验证配置

### 检查MCP服务器状态

在Claude Code中运行:
```
/mcp status
```

应该看到以下服务器:
- ✅ minimax-mcp
- ✅ shadcn-mcp
- ✅ github-mcp
- ✅ context7
- ✅ playwright-mcp
- ✅ lark-mcp
- ✅ cos-mcp
- ✅ supabase-mcp
- ✅ chart-generator
- ✅ deep-research

### 测试MiniMax (配置API密钥后)

```python
# 请求使用MiniMax生成图像
请使用MiniMax生成一张火锅店开业海报
```

### 测试shadcn

```
# 查询可用组件
Show me the available shadcn components

# 创建示例页面
Create a landing page with shadcn button and card components
```

---

## 故障排查

### MiniMax问题

**问题1: "Invalid API key"**
- 检查API密钥是否正确
- 确认API Host和密钥来自同一区域(国内或国际)

**问题2: "uvx: command not found"**
- 安装uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- 重启终端

**问题3: 输出文件找不到**
- 检查 `MINIMAX_MCP_BASE_PATH` 路径是否存在
- 确认路径权限正确

### shadcn问题

**问题1: "Registry not found"**
- 检查 `components.json` 是否存在
- 确认注册表URL格式正确

**问题2: "npx: command not found"**
- 安装Node.js和npm
- 运行 `npm install -g npx`

**问题3: MCP服务器无响应**
- 运行 `/mcp` 命令查看日志
- 检查网络连接(注册表需要网络访问)

---

## 后续操作

### 立即行动

1. **配置MiniMax API密钥** (必须):
   ```bash
   nano "/Library/Application Support/ClaudeCode/managed-mcp.json"
   # 替换 YOUR_MINIMAX_API_KEY_HERE
   ```

2. **重启Claude Code**:
   完全退出并重新启动应用

3. **验证配置**:
   运行 `/mcp status` 检查服务器状态

### 项目集成

**如需在开发项目中使用shadcn**:

1. 进入前端项目目录
2. 运行 `pnpm dlx shadcn@latest init`
3. 配置 `components.json`
4. 重启Claude Code

---

## 相关文档

- [MiniMax GitHub](https://github.com/MiniMax-AI/MiniMax-MCP)
- [MiniMax开放平台](https://platform.minimaxi.com/)
- [shadcn/ui MCP文档](https://ui.shadcn.com/docs/registry/mcp)
- [shadcn/ui组件库](https://ui.shadcn.com/)
- [MCP协议规范](https://modelcontextprotocol.io/)

---

**配置完成时间**: 2025-10-29
**配置路径**: `/Library/Application Support/ClaudeCode/managed-mcp.json`
**输出路径**: `output/minimax/`
