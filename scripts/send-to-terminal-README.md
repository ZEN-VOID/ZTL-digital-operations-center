# 终端命令发送脚本使用指南

## 📝 脚本说明

`send-to-terminal.sh` 是一个通用的终端命令发送脚本，可以从 Claude Code 或任何地方向活动终端发送命令。

## ✨ 特性

- ✅ **智能终端检测**: 自动优先使用 iTerm2，降级到 Terminal.app
- ✅ **自动窗口管理**: 如果没有打开的窗口，自动创建新窗口
- ✅ **错误处理**: 完善的错误提示和降级机制
- ✅ **跨平台兼容**: 支持 macOS 的两大终端应用

## 🚀 使用方法

### 基础用法

```bash
./scripts/send-to-terminal.sh "命令内容"
```

### 示例

```bash
# 1. 简单命令
./scripts/send-to-terminal.sh "echo 'Hello World'"

# 2. 目录操作
./scripts/send-to-terminal.sh "cd /path/to/dir && ls -la"

# 3. 多命令组合
./scripts/send-to-terminal.sh "git status && git pull"

# 4. Python 脚本执行
./scripts/send-to-terminal.sh "python scripts/my_script.py"
```

## 🔧 与 Claude Code 集成

### 在 Slash Commands 中使用

在 `.claude/commands/your-command.md` 中:

```markdown
---
description: 执行某个任务
---

!./scripts/send-to-terminal.sh "npm test"

任务已发送到终端执行!
```

### 在 Bash 工具中使用

```bash
# Claude Code 可以直接调用
Bash(command="./scripts/send-to-terminal.sh 'npm start'")
```

## 🎯 工作原理

```
┌─────────────────────────────────────┐
│    send-to-terminal.sh              │
└─────────────────┬───────────────────┘
                  │
                  ▼
         ┌────────────────┐
         │  检测 iTerm2?   │
         └────┬────────┬───┘
              │        │
          YES │        │ NO
              ▼        ▼
      ┌─────────┐  ┌──────────────┐
      │ iTerm2  │  │ Terminal.app │
      └─────────┘  └──────────────┘
              │        │
              └────┬───┘
                   ▼
           ┌───────────────┐
           │ 命令已发送到终端 │
           └───────────────┘
```

## 📊 终端优先级

1. **iTerm2** (首选)
   - 功能更强大
   - 更好的用户体验
   - 自动创建窗口

2. **Terminal.app** (降级方案)
   - 系统自带
   - 始终可用
   - 自动创建窗口

## 🎯 高级功能: 命令输出捕获

### send-and-capture.sh

**功能**: 发送命令到iTerm并捕获其输出结果

**解决问题**: Claude无法直接看到iTerm终端的输出内容，通过文件重定向机制解决

**使用方法**:

```bash
./scripts/send-and-capture.sh "命令" [超时秒数]
```

**工作原理**:
```
1. 发送命令到iTerm (带文件重定向: command > file 2>&1)
2. 等待指定时间（默认3秒）
3. 读取输出文件内容
4. 显示结果
5. 清理临时文件
```

**使用示例**:

```bash
# 捕获目录列表
./scripts/send-and-capture.sh "ls -la"

# 捕获Git状态
./scripts/send-and-capture.sh "git status"

# 捕获复杂命令 (5秒超时)
./scripts/send-and-capture.sh "cd /path/to/dir && git status --short" 5

# 捕获命令输出用于分析
./scripts/send-and-capture.sh "npm test" 10
```

**输出格式**:

```
✅ 命令已发送到 iTerm: ls -la
⏳ 等待 3 秒...

📄 命令输出:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
total 128
drwxr-xr-x  15 user  staff   480 Oct 30 10:30 .
drwxr-xr-x   8 user  staff   256 Oct 29 15:20 ..
-rw-r--r--   1 user  staff  1234 Oct 30 10:25 file.txt
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**实际应用场景**:

1. **验证命令执行结果**:
   ```bash
   # Claude发送命令后验证是否成功
   ./scripts/send-and-capture.sh "npm install"
   ```

2. **获取系统信息**:
   ```bash
   # 获取当前目录信息
   ./scripts/send-and-capture.sh "pwd"

   # 获取环境变量
   ./scripts/send-and-capture.sh "env | grep NODE"
   ```

3. **分析日志输出**:
   ```bash
   # 捕获测试结果
   ./scripts/send-and-capture.sh "pytest --verbose" 10
   ```

4. **Git操作验证**:
   ```bash
   # 查看修改文件
   ./scripts/send-and-capture.sh "git status --short"

   # 查看提交历史
   ./scripts/send-and-capture.sh "git log --oneline -5"
   ```

**配置参数**:

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 命令 | 要执行的shell命令 | 必填 |
| 超时 | 等待命令执行的秒数 | 3秒 |

**注意事项**:

- ⏱️ 超时时间应根据命令复杂度调整（简单命令3秒，复杂命令5-10秒）
- 📁 输出文件自动生成唯一名称（避免冲突）
- 🧹 执行完成后自动清理临时文件
- ⚠️ 长时间运行的命令可能需要更长超时
- 🔒 仅捕获标准输出和错误输出（stdout + stderr）

## ⚠️ 注意事项

### 权限要求

首次使用时，macOS 可能会请求权限:

```
系统偏好设置 > 安全性与隐私 > 隐私 > 辅助功能
```

将 `Terminal.app` 或 `iTerm.app` 添加到允许列表。

### 命令引号处理

```bash
# ✅ 正确: 使用双引号包裹命令
./scripts/send-to-terminal.sh "echo 'test'"

# ✅ 正确: 转义内部引号
./scripts/send-to-terminal.sh "echo \"test\""

# ❌ 错误: 不使用引号
./scripts/send-to-terminal.sh echo test
```

### 特殊字符

对于包含特殊字符的命令，需要适当转义:

```bash
# 包含 $ 符号
./scripts/send-to-terminal.sh "echo \$HOME"

# 包含反引号
./scripts/send-to-terminal.sh "echo \`date\`"
```

## 🔍 调试

如果命令未执行，检查:

1. **终端应用是否打开**: 脚本会自动创建窗口，但需要应用已安装
2. **权限设置**: 检查辅助功能权限
3. **命令语法**: 确保命令本身是正确的

### 调试模式

```bash
# 查看详细执行过程
bash -x ./scripts/send-to-terminal.sh "echo 'debug'"
```

## 📚 实际应用场景

### 场景1: 自动化测试

```bash
./scripts/send-to-terminal.sh "npm test && echo '测试完成'"
```

### 场景2: 批量部署

```bash
./scripts/send-to-terminal.sh "git pull && npm install && npm run build"
```

### 场景3: 开发服务器启动

```bash
./scripts/send-to-terminal.sh "npm run dev"
```

### 场景4: 在 Claude Code 中触发 Git 操作

```bash
./scripts/send-to-terminal.sh "git status && git diff"
```

## 🎓 高级用法

### 结合 Claude Code Hooks

在 `.claude/hooks/SessionStart.md` 中:

```markdown
!./scripts/send-to-terminal.sh "echo '会话开始: $(date)'"
```

### 批量命令执行

```bash
# 创建批量脚本
cat > batch-commands.sh << 'EOF'
#!/bin/bash
./scripts/send-to-terminal.sh "echo '开始部署...'"
sleep 2
./scripts/send-to-terminal.sh "git pull"
sleep 2
./scripts/send-to-terminal.sh "npm install"
sleep 2
./scripts/send-to-terminal.sh "npm run build"
sleep 2
./scripts/send-to-terminal.sh "echo '部署完成!'"
EOF

chmod +x batch-commands.sh
./batch-commands.sh
```

## 🐛 问题排查

### 问题1: "❌ 无法发送到终端应用"

**原因**: 终端应用未安装或权限不足

**解决**:
1. 确认 iTerm2 或 Terminal.app 已安装
2. 检查辅助功能权限
3. 尝试手动打开终端应用

### 问题2: 命令发送了但未执行

**原因**: 命令语法错误或需要交互式输入

**解决**:
1. 先在终端中手动测试命令
2. 确保命令不需要用户输入
3. 使用 `-y` 等标志跳过确认

### 问题3: 特殊字符显示异常

**原因**: emoji 或中文编码问题

**解决**:
1. 确保终端使用 UTF-8 编码
2. iTerm2 默认支持 emoji
3. Terminal.app 需要在偏好设置中启用

## 📖 相关资源

- [iTerm2 官网](https://iterm2.com)
- [osascript 文档](https://ss64.com/osx/osascript.html)
- [AppleScript 语言指南](https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/)

---

**脚本位置**: `scripts/send-to-terminal.sh`
**版本**: 1.0.0
**最后更新**: 2025-10-30
**维护者**: Claude Code + ZTL 开发团队
