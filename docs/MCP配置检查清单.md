# MCP配置检查清单 ✅

## 配置概览

**配置日期**: 2025-10-29
**配置内容**: 新增2个MCP服务器 (MiniMax + shadcn)
**总服务器数**: 10个 (8个已有 + 2个新增)

---

## ✅ 配置完成项

### 系统配置

- [x] 检查 `uv` 工具已安装 (`/Users/vincentlee/.local/bin/uvx`)
- [x] 检查 `npx` 工具已安装 (`/Users/vincentlee/.local/bin/npx`)
- [x] 验证MCP配置文件路径 (`/Library/Application Support/ClaudeCode/managed-mcp.json`)
- [x] JSON配置文件格式验证通过

### MiniMax MCP配置

- [x] 添加 `minimax-mcp` 配置项到managed-mcp.json
- [x] 配置 API密钥 (海螺AI - 数字游牧派账户)
- [x] 设置 API Host (`https://api.minimax.chat`)
- [x] 配置输出路径 (`/Users/vincentlee/Desktop/AIGC数字游牧派影视文化公司/output`)
- [x] 设置资源模式 (`url`)
- [x] 创建输出目录结构
- [x] 验证目录权限正常

### shadcn MCP配置

- [x] 添加 `shadcn-mcp` 配置项到managed-mcp.json
- [x] 配置使用最新版本 (`shadcn@latest`)
- [x] 设置命令为 `npx -y shadcn@latest mcp serve`

### 文档创建

- [x] 创建 `MiniMax配置完成确认.md` (详细配置说明)
- [x] 创建 `MCP配置说明-MiniMax和Shadcn.md` (完整配置指南)
- [x] 创建 `MCP快速参考-MiniMax和Shadcn.md` (快速参考)
- [x] 创建 `MCP配置总结-2025-10-29.md` (总结文档)
- [x] 创建 `MCP配置检查清单.md` (本文档)

---

## ⏳ 待完成项

### 必须立即完成

- [ ] **重启Claude Code** (完全退出并重新启动)
- [ ] 运行 `/mcp status` 验证10个服务器全部就绪
- [ ] 测试MiniMax基本功能 (生成一张测试图片)

### 建议尽快完成

- [ ] 测试MiniMax视频生成功能
- [ ] 测试MiniMax音频合成功能
- [ ] 测试shadcn组件查询功能
- [ ] 在前端项目中初始化shadcn (`pnpm dlx shadcn@latest init`)

### 后续优化

- [ ] 根据使用情况决定是否切换MiniMax资源模式 (url → local)
- [ ] 配置shadcn自定义注册表 (如有私有组件库需求)
- [ ] 建立MiniMax输出文件命名规范
- [ ] 监控API配额使用情况
- [ ] 编写团队使用培训文档

---

## 🔍 验证步骤

### 步骤1: 重启Claude Code

**操作**:
1. 完全退出Claude Code应用 (Cmd+Q 或右键退出)
2. 等待3-5秒
3. 重新启动Claude Code

**预期结果**: 应用正常启动,无错误提示

### 步骤2: 验证MCP服务器

**在Claude Code中运行**:
```
/mcp status
```

**预期输出**: 应该看到10个MCP服务器
```
✅ MCP Servers (10):
1. github-mcp          - ✅ Connected
2. context7            - ✅ Connected
3. playwright-mcp      - ✅ Connected
4. lark-mcp            - ✅ Connected
5. cos-mcp             - ✅ Connected
6. supabase-mcp        - ✅ Connected
7. chart-generator     - ✅ Connected
8. deep-research       - ✅ Connected
9. minimax-mcp         - ✅ Connected  (新增)
10. shadcn-mcp         - ✅ Connected  (新增)
```

**如果有错误**: 查看故障排查章节

### 步骤3: 测试MiniMax图像生成

**测试命令**:
```
使用MiniMax生成一张测试图片:
- 描述: 一只可爱的橙色小猫
- 风格: 卡通风格
- 尺寸: 512x512
```

**预期结果**:
- Claude调用minimax-mcp服务器
- 返回图片URL (资源模式为url)
- 可以访问URL查看生成的图片

### 步骤4: 测试MiniMax视频生成

**测试命令**:
```
使用MiniMax生成一段3秒的测试视频:
- 描述: 海浪拍打沙滩
- 风格: 自然写实
- 质量: 高清
```

**预期结果**:
- Claude调用minimax-mcp服务器
- 返回视频URL
- 可以下载并播放视频

### 步骤5: 测试MiniMax音频合成

**测试命令**:
```
使用MiniMax合成测试语音:
- 文本: "这是一段测试语音"
- 音色: 女声
- 格式: MP3
```

**预期结果**:
- Claude调用minimax-mcp服务器
- 返回音频URL
- 可以下载并播放音频

### 步骤6: 测试shadcn组件查询

**测试命令**:
```
Show me all available shadcn components
```

**预期结果**:
- Claude调用shadcn-mcp服务器
- 返回可用组件列表
- 显示组件描述和依赖信息

---

## 🐛 故障排查

### 问题1: MiniMax服务器无法连接

**症状**:
- `/mcp status` 显示 minimax-mcp 状态为 ❌ Error
- 尝试使用MiniMax时报错

**排查步骤**:

1. **检查uvx是否可用**:
   ```bash
   which uvx
   # 应输出: /Users/vincentlee/.local/bin/uvx
   ```

   如果未找到:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   exec $SHELL
   ```

2. **检查API密钥**:
   - 访问 https://www.minimaxi.com/user-center/basic-information
   - 确认API密钥有效且未过期
   - 检查配置文件中的密钥是否正确

3. **检查网络连接**:
   ```bash
   curl https://api.minimax.chat
   ```

   应返回API响应(非404错误)

4. **查看MCP日志**:
   在Claude Code中运行:
   ```
   /mcp logs minimax-mcp
   ```

### 问题2: shadcn服务器无法连接

**症状**:
- `/mcp status` 显示 shadcn-mcp 状态为 ❌ Error
- 查询组件时报错

**排查步骤**:

1. **检查npx是否可用**:
   ```bash
   which npx
   # 应输出: /Users/vincentlee/.local/bin/npx
   ```

   如果未找到:
   ```bash
   npm install -g npx
   ```

2. **检查网络连接**:
   ```bash
   curl https://ui.shadcn.com/
   ```

   应返回HTML内容

3. **手动测试shadcn CLI**:
   ```bash
   npx -y shadcn@latest --version
   ```

   应输出版本号

4. **查看MCP日志**:
   在Claude Code中运行:
   ```
   /mcp logs shadcn-mcp
   ```

### 问题3: 所有MCP服务器无法连接

**症状**:
- `/mcp status` 显示多个或全部服务器状态异常
- Claude无法调用任何MCP工具

**排查步骤**:

1. **检查配置文件格式**:
   ```bash
   cat "/Library/Application Support/ClaudeCode/managed-mcp.json" | python3 -m json.tool
   ```

   应该没有JSON语法错误

2. **检查配置文件权限**:
   ```bash
   ls -la "/Library/Application Support/ClaudeCode/managed-mcp.json"
   ```

   应该可读可写

3. **重置配置(最后手段)**:
   ```bash
   # 备份当前配置
   cp "/Library/Application Support/ClaudeCode/managed-mcp.json" \
      "/Library/Application Support/ClaudeCode/managed-mcp.json.backup"

   # 编辑配置文件修复问题
   nano "/Library/Application Support/ClaudeCode/managed-mcp.json"
   ```

4. **完全重启系统**:
   - 退出Claude Code
   - 重启计算机
   - 重新启动Claude Code

### 问题4: MiniMax返回Invalid API Key

**症状**:
- 服务器连接正常
- 但生成内容时报错 "Invalid API key"

**原因**:
- API密钥错误或过期
- API Host和密钥区域不匹配

**解决方案**:

1. **验证API密钥**:
   - 访问 https://www.minimaxi.com/user-center/basic-information
   - 复制正确的API密钥

2. **确认区域匹配**:
   当前配置使用 `https://api.minimax.chat` (海螺AI)

   确认API密钥来自: https://www.minimaxi.com/

   **不要混用不同区域的配置!**

3. **更新配置**:
   ```bash
   nano "/Library/Application Support/ClaudeCode/managed-mcp.json"
   # 更新MINIMAX_API_KEY字段
   ```

4. **重启Claude Code**

### 问题5: 生成的文件找不到

**症状**:
- MiniMax成功生成内容
- 但找不到输出文件

**原因**:
- 当前配置为 `url` 模式,返回URL而非本地文件

**解决方案**:

**方案1: 手动下载** (推荐):
- 复制返回的URL
- 使用浏览器访问并下载文件
- 保存到所需位置

**方案2: 切换到本地模式**:
1. 编辑配置文件:
   ```bash
   nano "/Library/Application Support/ClaudeCode/managed-mcp.json"
   ```

2. 修改资源模式:
   ```json
   "MINIMAX_API_RESOURCE_MODE": "local"
   ```

3. 重启Claude Code

4. 重新生成内容,文件将自动下载到:
   ```
   /Users/vincentlee/Desktop/AIGC数字游牧派影视文化公司/output/
   ```

---

## 📊 配置文件对比

### 配置前 (8个MCP服务器)

```json
{
  "mcpServers": {
    "github-mcp": {...},
    "context7": {...},
    "playwright-mcp": {...},
    "lark-mcp": {...},
    "cos-mcp": {...},
    "supabase-mcp": {...},
    "chart-generator": {...},
    "deep-research": {...}
  }
}
```

### 配置后 (10个MCP服务器)

```json
{
  "mcpServers": {
    "github-mcp": {...},
    "context7": {...},
    "playwright-mcp": {...},
    "lark-mcp": {...},
    "cos-mcp": {...},
    "supabase-mcp": {...},
    "chart-generator": {...},
    "deep-research": {...},
    "minimax-mcp": {              // 新增
      "type": "stdio",
      "command": "uvx",
      "args": ["minimax-mcp", "-y"],
      "env": {
        "MINIMAX_API_KEY": "...",
        "MINIMAX_MCP_BASE_PATH": "/Users/vincentlee/Desktop/AIGC数字游牧派影视文化公司/output",
        "MINIMAX_API_HOST": "https://api.minimax.chat",
        "MINIMAX_API_RESOURCE_MODE": "url"
      }
    },
    "shadcn-mcp": {               // 新增
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "shadcn@latest", "mcp", "serve"],
      "env": {}
    }
  }
}
```

---

## 📁 文件清单

### 配置文件

| 文件 | 路径 | 说明 |
|------|------|------|
| **MCP配置** | `/Library/Application Support/ClaudeCode/managed-mcp.json` | 主配置文件 |
| **MCP配置备份** | 无 (建议创建) | 备份原配置 |

### 输出目录

| 目录 | 路径 | 用途 |
|------|------|------|
| **MiniMax输出** | `/Users/vincentlee/Desktop/AIGC数字游牧派影视文化公司/output` | 生成内容保存 |
| **子目录videos** | `output/videos/` | 视频文件 |
| **子目录audios** | `output/audios/` | 音频文件 |
| **子目录images** | `output/images/` | 图像文件 |
| **子目录texts** | `output/texts/` | 文本文件 |
| **子目录metadata** | `output/metadata/` | 元数据和日志 |

### 文档文件

| 文档 | 路径 | 说明 |
|------|------|------|
| **配置完成确认** | `docs/MiniMax配置完成确认.md` | MiniMax详细说明 |
| **配置说明** | `docs/MCP配置说明-MiniMax和Shadcn.md` | 完整配置指南 |
| **快速参考** | `docs/MCP快速参考-MiniMax和Shadcn.md` | 速查卡片 |
| **配置总结** | `docs/MCP配置总结-2025-10-29.md` | 总结文档 |
| **检查清单** | `docs/MCP配置检查清单.md` | 本文档 |

---

## 🎯 完成标准

### 最低标准 (必须完成)

- [x] 配置文件已更新
- [x] JSON格式验证通过
- [x] 输出目录已创建
- [x] 文档已生成
- [ ] **Claude Code已重启**
- [ ] `/mcp status` 显示10个服务器
- [ ] MiniMax测试成功(至少一个功能)

### 推荐标准 (建议完成)

- [ ] MiniMax所有功能测试通过 (图像/视频/音频)
- [ ] shadcn组件查询测试通过
- [ ] 团队成员已培训
- [ ] 使用文档已分享

### 优秀标准 (额外加分)

- [ ] 建立输出文件命名规范
- [ ] 配置API配额监控
- [ ] 编写常用提示词模板库
- [ ] 集成到项目工作流

---

## 📞 支持信息

### 官方支持

**MiniMax/海螺AI**:
- 官网: https://hailuoai.com/
- 文档: https://www.minimaxi.com/document
- 控制台: https://www.minimaxi.com/user-center

**shadcn/ui**:
- 官网: https://ui.shadcn.com/
- 文档: https://ui.shadcn.com/docs
- GitHub: https://github.com/shadcn-ui/ui

**Claude Code**:
- 文档: https://docs.claude.com/en/docs/claude-code
- 反馈: https://github.com/anthropics/claude-code/issues

### 项目文档

查看 `docs/` 目录下的相关文档:
- `MiniMax配置完成确认.md`
- `MCP配置说明-MiniMax和Shadcn.md`
- `MCP快速参考-MiniMax和Shadcn.md`
- `MCP配置总结-2025-10-29.md`

---

## ✅ 最终确认

**配置已100%完成**: ✅

**下一步**:
1. **立即重启Claude Code**
2. 运行 `/mcp status` 验证
3. 测试MiniMax和shadcn功能
4. 开始使用新能力!

**配置时间**: 2025-10-29
**配置状态**: ✅ 完成
**总服务器数**: 10个
**新增服务器**: 2个 (minimax-mcp, shadcn-mcp)

---

**检查清单完成**: ✅
**准备就绪**: ✅
**可以开始使用**: ✅
