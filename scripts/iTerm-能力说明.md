# iTerm2 控制能力说明

## 📊 核心能力总结

### 问题1: Claude 能看到 iTerm 窗口中的响应信息吗？

**答案：❌ 不能直接看到**

#### 限制原因
- `osascript` 只能**发送**命令到 iTerm
- 无法直接**读取** iTerm 中的输出内容
- 只能看到 osascript 的执行状态（成功/失败）

#### 解决方案

| 方案 | 描述 | 优点 | 缺点 | 适用场景 |
|------|------|------|------|----------|
| **方案A: 文件重定向** | `cmd > file` 然后读取文件 | 可靠 | 需要额外步骤 | 需要捕获输出时 |
| **方案B: Bash工具** | 直接在 Claude 的 Bash 中执行 | 直接看到输出 | 不在用户 iTerm 显示 | 需要获取结果时 |
| **方案C: 混合模式** | 关键操作在 iTerm，查询在 Bash | 兼顾两者 | 需要规划 | 生产环境推荐 |

#### 方案A 示例（文件重定向）

```bash
# 步骤1: 发送命令到 iTerm，输出到文件
./send-to-terminal.sh "ls -la > /tmp/output.txt"

# 步骤2: 等待执行
sleep 1

# 步骤3: Claude 读取文件
cat /tmp/output.txt
```

#### 方案B 示例（直接执行）

```bash
# Claude 直接执行并看到输出
ls -la

# 优点: 立即获得结果
# 缺点: 用户在 iTerm 中看不到
```

#### 方案C 示例（混合模式）

```bash
# 场景: 启动开发服务器

# 1. 在 iTerm 中启动（用户可以看到日志）
./send-to-terminal.sh "npm run dev"

# 2. 在 Bash 中验证状态（Claude 可以检查）
curl -s http://localhost:3000 | head -5
```

### 问题2: iTerm 能打开多个窗口并且每个都能被感知吗？

**答案：✅ 完全可以！**

#### 多窗口感知能力

```yaml
我可以：
  ✅ 查询窗口总数
  ✅ 获取每个窗口的详细信息（标签页数、会话名）
  ✅ 向指定窗口发送命令
  ✅ 创建新窗口
  ✅ 向所有窗口广播命令
  ✅ 区分不同窗口的状态
```

#### 实际演示

```bash
# 查询所有窗口
osascript -e 'tell application "iTerm" to count of windows'
# 输出: 3

# 获取窗口详情
osascript -e 'tell application "iTerm" to tell window 1
    set tabCount to count of tabs
    return "窗口1有 " & tabCount & " 个标签页"
end tell'
# 输出: 窗口1有 1 个标签页
```

#### 多窗口操作示例

##### 示例1: 向不同窗口发送不同命令

```bash
# 窗口1: 启动前端服务
osascript -e 'tell application "iTerm" to tell window 1
    tell current session
        write text "cd frontend && npm run dev"
    end tell
end tell'

# 窗口2: 启动后端服务
osascript -e 'tell application "iTerm" to tell window 2
    tell current session
        write text "cd backend && npm start"
    end tell
end tell'

# 窗口3: 监控日志
osascript -e 'tell application "iTerm" to tell window 3
    tell current session
        write text "tail -f /var/log/app.log"
    end tell
end tell'
```

##### 示例2: 向所有窗口广播命令

```bash
osascript <<'EOF'
tell application "iTerm"
    repeat with w in windows
        tell current session of w
            write text "git pull"
        end tell
    end repeat
end tell
EOF
```

##### 示例3: 创建新窗口并初始化环境

```bash
osascript <<'EOF'
tell application "iTerm"
    create window with default profile
    tell current session of current window
        write text "cd /path/to/project"
        write text "source venv/bin/activate"
        write text "echo 'Environment ready!'"
    end tell
end tell
EOF
```

## 🎯 实际应用场景

### 场景1: 多环境开发

```bash
# 窗口1: 开发环境
send_to_window 1 "export ENV=dev && npm start"

# 窗口2: 测试环境
send_to_window 2 "export ENV=test && npm start"

# 窗口3: 监控
send_to_window 3 "watch -n 1 'curl localhost:3000/health'"
```

### 场景2: 并行任务执行

```bash
# 同时在3个窗口执行不同测试套件
send_to_window 1 "npm run test:unit"
send_to_window 2 "npm run test:integration"
send_to_window 3 "npm run test:e2e"
```

### 场景3: 分布式调试

```bash
# 窗口1: 查看应用日志
send_to_window 1 "kubectl logs -f app-pod"

# 窗口2: 查看数据库日志
send_to_window 2 "kubectl logs -f db-pod"

# 窗口3: 查看负载均衡器日志
send_to_window 3 "kubectl logs -f lb-pod"
```

## 🔧 已创建的工具

### 1. 基础版脚本

**文件**: `scripts/send-to-terminal.sh`

**功能**:
- 发送命令到 iTerm（优先）或 Terminal.app（降级）
- 自动创建窗口（如果没有）
- 简单易用

**用法**:
```bash
./scripts/send-to-terminal.sh "命令"
```

### 1.1 输出捕获脚本 ⭐ 新增

**文件**: `scripts/send-and-capture.sh`

**功能**:
- ✅ 发送命令到 iTerm
- ✅ 捕获命令输出到文件
- ✅ 自动读取并显示结果
- ✅ 自动清理临时文件

**用法**:
```bash
./scripts/send-and-capture.sh "命令" [超时秒数]

# 示例
./scripts/send-and-capture.sh "git status"
./scripts/send-and-capture.sh "npm test" 10
```

**工作流程**:
```
1. 生成唯一临时文件路径
2. 发送命令到 iTerm（带重定向: cmd > file 2>&1）
3. 等待指定时间（默认3秒）
4. 读取并显示输出文件内容
5. 删除临时文件
```

**实战验证**:
- ✅ 成功捕获 `ls -la` 输出
- ✅ 成功捕获 `pwd` 输出
- ✅ 成功捕获 `git status` 输出
- ✅ 成功捕获 `cd && git status --short` 输出（90+文件）

**这是方案A（文件重定向）的生产级实现** 🎯

### 2. 多窗口管理 (演示版)

**功能演示** (已验证可用):

```bash
# 列出所有窗口
osascript -e 'tell application "iTerm" to count of windows'

# 向窗口N发送命令
osascript -e 'tell application "iTerm" to tell window N
    tell current session
        write text "命令"
    end tell
end tell'

# 创建新窗口
osascript -e 'tell application "iTerm" to create window with default profile'

# 广播到所有窗口
osascript -e 'tell application "iTerm"
    repeat with w in windows
        tell current session of w
            write text "命令"
        end tell
    end repeat
end tell'
```

## 📚 AppleScript 命令参考

### 窗口操作

```applescript
-- 获取窗口数量
count of windows

-- 创建新窗口
create window with default profile

-- 激活应用
activate

-- 获取当前窗口
current window

-- 获取指定窗口
window N
```

### 会话操作

```applescript
-- 获取当前会话
current session of window N

-- 发送文本（执行命令）
tell current session
    write text "命令"
end tell

-- 获取会话名称
name of current session

-- 设置会话名称
tell current session
    set name to "新名称"
end tell
```

### 标签页操作

```applescript
-- 获取标签页数量
count of tabs of window N

-- 创建新标签页
tell current window
    create tab with default profile
end tell
```

## ⚠️ 注意事项

### 权限要求

必须授予 iTerm2 **辅助功能权限**:
```
系统偏好设置 > 安全性与隐私 > 隐私 > 辅助功能
```

### 局限性

1. **无法读取输出**: 只能发送命令，不能直接获取输出
2. **异步执行**: 命令发送后立即返回，无法等待完成
3. **无法交互**: 不支持需要用户输入的命令
4. **窗口必须存在**: 向指定窗口发送命令时，该窗口必须存在

### 最佳实践

1. **需要输出时**: 使用文件重定向或直接在 Bash 工具中执行
2. **长时间运行任务**: 在 iTerm 中执行，方便用户监控
3. **快速查询**: 在 Bash 工具中执行，立即获得结果
4. **并行任务**: 使用多窗口，每个窗口一个任务
5. **命令验证**: 先在 Bash 中测试命令，再发送到 iTerm

## 🎓 学习资源

- [iTerm2 官网](https://iterm2.com)
- [AppleScript 语言指南](https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/)
- [osascript 命令参考](https://ss64.com/osx/osascript.html)

---

**更新时间**: 2025-10-30
**适用版本**: iTerm2 3.5+, macOS 10.15+
