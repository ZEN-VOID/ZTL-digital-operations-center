---
name: 深渊凝视
description: iTerm终端控制与输出捕获 - 向iTerm发送任意命令并捕获执行结果，支持新建窗口、指定窗口、多窗口管理
version: 1.0.0
category: terminal-control
tags: [iterm, terminal, automation, output-capture, multi-window]
author: Claude Code + ZTL Team
created: 2025-10-30
allowed-tools: [Bash, Read, Write]
---

# 深渊凝视 (Abyss Gaze)

> "当你凝视深渊时，深渊也在凝视你" - 向终端发送命令，终端返回输出

## 📋 Quick Start

### 基础用法：发送命令并捕获输出

```python
# 场景1: 快速执行并获取结果
深渊凝视.execute("git status")

# 场景2: 复杂命令，指定超时
深渊凝视.execute("npm test", timeout=10)

# 场景3: 切换目录并执行
深渊凝视.execute("cd /path/to/project && ls -la", timeout=5)
```

### 高级用法：多窗口管理

```python
# 场景4: 在新窗口执行
深渊凝视.execute_in_new_window("npm run dev")

# 场景5: 在指定窗口执行
深渊凝视.execute_in_window("git pull", window_index=2, timeout=5)

# 场景6: 查询所有窗口
windows = 深渊凝视.list_windows()

# 场景7: 广播到所有窗口
深渊凝视.broadcast("clear")
```

## 🎯 Core Features

### 1. 命令执行与输出捕获

**核心能力**:
- ✅ 发送任意shell命令到iTerm
- ✅ 自动捕获stdout和stderr
- ✅ 可配置超时时间
- ✅ 自动清理临时文件
- ✅ 支持复杂命令（管道、重定向、逻辑运算符）

**实现原理**:
```
1. 生成唯一临时文件路径
2. 通过osascript发送重定向命令到iTerm
3. 等待指定超时时间
4. 读取临时文件内容
5. 删除临时文件
6. 返回格式化结果
```

### 2. 多窗口管理

**核心能力**:
- ✅ 查询iTerm窗口总数
- ✅ 获取每个窗口详情（标签页、会话名）
- ✅ 向指定窗口发送命令
- ✅ 创建新窗口并执行命令
- ✅ 广播命令到所有窗口

**窗口索引规则**:
- 窗口索引从1开始（不是0）
- window_index=1 表示第一个窗口
- 可通过`list_windows()`查询当前窗口列表

### 3. 智能错误处理

**错误类型**:
- iTerm未运行 → 自动启动iTerm
- 窗口不存在 → 自动创建窗口
- 命令执行超时 → 返回超时提示
- 权限不足 → 返回权限配置指南

## 📚 API Reference

### execute(command, timeout=3)

发送命令到iTerm当前窗口并捕获输出。

**参数**:
- `command` (str): 要执行的shell命令
- `timeout` (int, optional): 超时时间（秒），默认3秒

**返回**:
```python
{
    "success": True,
    "command": "git status",
    "output": "On branch main...",
    "execution_time": 2.5,
    "window": "current"
}
```

**示例**:
```python
# 简单命令
result = 深渊凝视.execute("pwd")
print(result["output"])  # /Users/username/project

# 复杂命令
result = 深渊凝视.execute(
    "cd /path && git status --short",
    timeout=5
)
```

### execute_in_new_window(command, timeout=3)

在新的iTerm窗口中执行命令。

**参数**:
- `command` (str): 要执行的shell命令
- `timeout` (int, optional): 超时时间（秒），默认3秒

**返回**:
```python
{
    "success": True,
    "command": "npm run dev",
    "window": "new",
    "window_index": 4
}
```

**使用场景**:
- 启动长时间运行的服务（开发服务器、数据库）
- 并行执行多个任务
- 隔离不同环境的操作

### execute_in_window(command, window_index, timeout=3)

在指定的iTerm窗口中执行命令。

**参数**:
- `command` (str): 要执行的shell命令
- `window_index` (int): 窗口索引（从1开始）
- `timeout` (int, optional): 超时时间（秒），默认3秒

**返回**:
```python
{
    "success": True,
    "command": "git pull",
    "output": "Already up to date.",
    "window_index": 2
}
```

**示例**:
```python
# 在窗口1启动前端服务器
深渊凝视.execute_in_window("npm run dev", window_index=1)

# 在窗口2启动后端服务器
深渊凝视.execute_in_window("npm start", window_index=2)

# 在窗口3监控日志
深渊凝视.execute_in_window("tail -f app.log", window_index=3)
```

### list_windows()

查询所有iTerm窗口信息。

**返回**:
```python
{
    "total": 3,
    "windows": [
        {
            "index": 1,
            "tabs": 2,
            "session_name": "Project Frontend"
        },
        {
            "index": 2,
            "tabs": 1,
            "session_name": "Project Backend"
        },
        {
            "index": 3,
            "tabs": 3,
            "session_name": "Logs Monitor"
        }
    ]
}
```

### broadcast(command)

向所有iTerm窗口广播命令（不捕获输出）。

**参数**:
- `command` (str): 要广播的shell命令

**返回**:
```python
{
    "success": True,
    "command": "clear",
    "windows_count": 3
}
```

**使用场景**:
- 批量清屏
- 批量更新代码（git pull）
- 批量环境切换

## 🎨 Usage Examples

### 示例1: Git工作流自动化

```python
# 检查Git状态
status = 深渊凝视.execute("git status --short", timeout=3)
print(f"Modified files: {status['output']}")

# 如果有修改，提交
if status['output']:
    深渊凝视.execute('git add . && git commit -m "Auto commit"')
    深渊凝视.execute("git push")
```

### 示例2: 多环境并行开发

```python
# 窗口1: 开发环境
深渊凝视.execute_in_window(
    "cd /project && export ENV=dev && npm start",
    window_index=1
)

# 窗口2: 测试环境
深渊凝视.execute_in_window(
    "cd /project && export ENV=test && npm start",
    window_index=2
)

# 窗口3: 监控日志
深渊凝视.execute_in_window(
    "cd /project && tail -f logs/*.log",
    window_index=3
)
```

### 示例3: 自动化测试流程

```python
# 运行测试并捕获结果
test_result = 深渊凝视.execute("npm test", timeout=30)

# 分析测试结果
if "PASS" in test_result['output']:
    print("✅ All tests passed")
    # 自动部署
    深渊凝视.execute("npm run deploy")
else:
    print("❌ Tests failed")
    # 记录失败信息
    with open("test-failures.log", "w") as f:
        f.write(test_result['output'])
```

### 示例4: 系统信息收集

```python
# 收集系统信息
info = {
    "pwd": 深渊凝视.execute("pwd")['output'],
    "node_version": 深渊凝视.execute("node --version")['output'],
    "npm_version": 深渊凝视.execute("npm --version")['output'],
    "git_branch": 深渊凝视.execute("git branch --show-current")['output'],
    "disk_space": 深渊凝视.execute("df -h .")['output']
}

# 生成环境报告
print("=== Environment Report ===")
for key, value in info.items():
    print(f"{key}: {value.strip()}")
```

## ⚙️ Configuration

### 默认配置

```yaml
default_timeout: 3          # 默认超时时间（秒）
temp_file_prefix: /tmp/iterm-capture-
auto_cleanup: true          # 自动清理临时文件
create_window_if_none: true # 无窗口时自动创建
```

### 超时时间建议

| 命令类型 | 推荐超时 | 示例 |
|---------|---------|------|
| 简单查询 | 3秒 | `pwd`, `ls`, `git branch` |
| Git操作 | 5秒 | `git status`, `git pull` |
| 包管理 | 10秒 | `npm install`, `pip install` |
| 测试运行 | 30秒 | `npm test`, `pytest` |
| 构建任务 | 60秒 | `npm run build`, `make` |

## ⚠️ Important Notes

### 权限要求

**必需**: iTerm2必须获得辅助功能权限

**配置路径**:
```
系统偏好设置 > 安全性与隐私 > 隐私 > 辅助功能
→ 添加 iTerm.app
```

### 限制说明

1. **异步执行**: 命令发送后立即返回，通过固定等待时间捕获输出
2. **无交互支持**: 不支持需要用户输入的命令（如`sudo`密码、交互式提示）
3. **超时依赖**: 复杂命令需要合理设置超时时间
4. **窗口依赖**: 向指定窗口发送命令时，该窗口必须存在

### 最佳实践

✅ **推荐**:
- 使用合理的超时时间
- 简单命令优先使用`execute()`
- 长时间任务使用新窗口
- 定期清理不用的iTerm窗口

❌ **避免**:
- 需要交互输入的命令
- 超时时间设置过短
- 在同一窗口频繁切换目录
- 依赖命令执行顺序而不等待

## 🔗 Related Resources

- [iTerm2 官网](https://iterm2.com)
- [osascript 文档](https://ss64.com/osx/osascript.html)
- [项目脚本文档](../../../scripts/send-to-terminal-README.md)
- [iTerm能力说明](../../../scripts/iTerm-能力说明.md)

## 📝 Changelog

### v1.0.0 (2025-10-30)
- ✅ 初始版本发布
- ✅ 基础命令执行和输出捕获
- ✅ 多窗口管理能力
- ✅ 完整的错误处理
- ✅ 生产级测试验证

---

**Skill Category**: Terminal Control & Automation
**Maintenance**: Active
**Status**: Production Ready ✅
