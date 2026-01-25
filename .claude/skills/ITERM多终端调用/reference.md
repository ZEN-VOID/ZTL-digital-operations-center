# ITERM多终端调用 - 扩展参考文档

## 📚 深度技术原理

### 核心技术栈

```yaml
AppleScript:
  - 作用: macOS应用程序自动化脚本语言
  - 优势: 原生支持、权限充足、稳定可靠
  - 限制: 只能发送命令，无法直接读取终端输出

osascript:
  - 作用: 命令行执行AppleScript的工具
  - 调用方式: subprocess.run(["osascript", "-e", script])
  - 超时机制: subprocess timeout参数

文件重定向:
  - 原理: command > file 2>&1
  - stdout: > file (标准输出)
  - stderr: 2>&1 (错误输出也重定向到同一文件)
  - 优势: 解决osascript无法直接读取输出的限制
```

### 工作流程详解

#### 1. 命令执行与捕获流程

```
┌─────────────────────────────────────────────────────────┐
│ Claude调用ITERM多终端调用.execute("git status")         │
└─────────────┬───────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────┐
│ 1. 生成唯一临时文件路径                                  │
│    /tmp/iterm-capture-{timestamp}-{random}.txt          │
└─────────────┬───────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────┐
│ 2. 构建AppleScript                                      │
│    tell application "iTerm"                             │
│      tell current session of current window             │
│        write text "git status > /tmp/file 2>&1"         │
│      end tell                                           │
│    end tell                                             │
└─────────────┬───────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────┐
│ 3. 通过osascript发送到iTerm                             │
│    subprocess.run(["osascript", "-e", script])          │
└─────────────┬───────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────┐
│ 4. iTerm执行命令（异步）                                 │
│    - 命令在iTerm终端中执行                               │
│    - 用户可以在iTerm中看到执行过程                       │
│    - 输出被重定向到临时文件                              │
└─────────────┬───────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────┐
│ 5. Python等待（sleep timeout秒）                        │
│    - 默认3秒，可配置                                     │
│    - 等待命令执行完成                                    │
└─────────────┬───────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────┐
│ 6. 读取临时文件                                          │
│    output = Path(output_file).read_text()               │
└─────────────┬───────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────┐
│ 7. 删除临时文件（清理）                                  │
│    output_file.unlink()                                 │
└─────────────┬───────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────┐
│ 8. 返回结果给Claude                                      │
│    {                                                    │
│      "success": True,                                   │
│      "output": "On branch main...",                     │
│      "execution_time": 2.5                              │
│    }                                                    │
└─────────────────────────────────────────────────────────┘
```

#### 2. 多窗口管理流程

```
┌─────────────────────────────────────────┐
│ ITERM多终端调用.list_windows()                  │
└─────────┬───────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────┐
│ AppleScript查询窗口信息                  │
│ - count of windows                      │
│ - count of tabs of window i             │
│ - name of current session               │
└─────────┬───────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────┐
│ 解析返回数据                             │
│ "3|2|Frontend|1|Backend|3|Logs"        │
└─────────┬───────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────┐
│ 构造结构化数据                           │
│ {                                       │
│   "total": 3,                           │
│   "windows": [...]                      │
│ }                                       │
└─────────────────────────────────────────┘
```

### 异步执行机制

#### 为什么是异步？

```yaml
osascript特性:
  - 命令发送: 同步（等待osascript返回）
  - 命令执行: 异步（iTerm中执行，不阻塞osascript）

影响:
  - osascript立即返回（0.1-0.5秒）
  - iTerm命令可能需要数秒执行
  - 必须等待一段时间才能读取结果

解决方案:
  - 使用固定sleep等待
  - 等待时间可配置
  - 建议根据命令复杂度调整
```

#### 超时时间建议表

| 命令类型 | 复杂度 | 推荐超时 | 示例命令 |
|---------|-------|---------|----------|
| 文件系统查询 | 低 | 1-3秒 | `ls`, `pwd`, `du -sh` |
| Git本地操作 | 低-中 | 3-5秒 | `git status`, `git diff` |
| Git远程操作 | 中-高 | 5-10秒 | `git pull`, `git push` |
| 包安装 | 高 | 10-30秒 | `npm install`, `pip install` |
| 测试运行 | 高 | 30-60秒 | `npm test`, `pytest` |
| 构建任务 | 极高 | 60-120秒 | `npm run build`, `webpack` |

### 临时文件管理

#### 命名策略

```python
# 模式
/tmp/iterm-capture-{timestamp}-{random}.txt

# 实例
/tmp/iterm-capture-1698765432-12345.txt

# 解释
timestamp = int(time.time())  # Unix时间戳，确保时序
random = $RANDOM              # Bash随机数，避免冲突
```

#### 生命周期

```yaml
创建时机: 每次execute调用前
存在时长: command执行期间 + timeout等待时间
清理时机: 读取完成后立即删除
容错机制: 如果文件不存在，返回超时错误

边界情况:
  - 命令执行失败: 文件为空或包含错误信息
  - 命令超时: 文件不存在或内容不完整
  - 权限问题: 文件无法创建或读取
```

## 🔬 高级用法

### 1. 条件执行与错误处理

```python
from pathlib import Path

# 智能检查并执行
def smart_execute(command: str, retry: int = 3):
    """带重试的智能执行"""
    for attempt in range(retry):
        result = ITERM多终端调用.execute(command, timeout=5)

        if result['success']:
            return result

        # 如果是超时，增加等待时间
        if 'timeout' in result.get('error', '').lower():
            print(f"Attempt {attempt + 1} timed out, retrying with longer timeout...")
            result = ITERM多终端调用.execute(command, timeout=10)
            if result['success']:
                return result

    # 所有尝试失败
    raise RuntimeError(f"Command failed after {retry} attempts: {command}")

# 使用示例
try:
    result = smart_execute("npm test")
    print(result['output'])
except RuntimeError as e:
    print(f"Error: {e}")
```

### 2. 批量窗口操作

```python
def setup_dev_environment():
    """设置开发环境（3个窗口）"""
    windows_info = ITERM多终端调用.list_windows()
    current_count = windows_info['total']

    # 确保至少有3个窗口
    while current_count < 3:
        ITERM多终端调用.execute_in_new_window("echo 'Window created'")
        current_count += 1

    # 窗口1: 前端开发服务器
    ITERM多终端调用.execute_in_window(
        "cd /project/frontend && npm run dev",
        window_index=1
    )

    # 窗口2: 后端API服务器
    ITERM多终端调用.execute_in_window(
        "cd /project/backend && npm start",
        window_index=2
    )

    # 窗口3: 数据库和日志监控
    ITERM多终端调用.execute_in_window(
        "cd /project && docker-compose up && tail -f logs/*.log",
        window_index=3
    )

    print("✅ Development environment setup complete!")
```

### 3. 输出解析与数据提取

```python
import re
import json

def analyze_git_status():
    """分析Git状态并提取关键信息"""
    result = ITERM多终端调用.execute("git status --short", timeout=3)

    if not result['success']:
        return {"error": result.get('error')}

    output = result['output']

    # 解析修改文件
    modified = []
    deleted = []
    untracked = []

    for line in output.strip().split('\n'):
        if not line:
            continue

        status = line[:2]
        filename = line[3:]

        if 'M' in status:
            modified.append(filename)
        elif 'D' in status:
            deleted.append(filename)
        elif '??' in status:
            untracked.append(filename)

    return {
        "modified": modified,
        "deleted": deleted,
        "untracked": untracked,
        "total_changes": len(modified) + len(deleted) + len(untracked)
    }

# 使用示例
git_info = analyze_git_status()
print(json.dumps(git_info, indent=2))
```

### 4. 命令链与依赖管理

```python
from typing import List, Tuple

def execute_chain(
    commands: List[Tuple[str, int]],
    stop_on_error: bool = True
) -> List[Dict]:
    """
    执行命令链。

    Args:
        commands: [(command, timeout), ...]
        stop_on_error: 遇到错误时是否停止

    Returns:
        所有命令的执行结果列表
    """
    results = []

    for i, (command, timeout) in enumerate(commands):
        print(f"[{i+1}/{len(commands)}] Executing: {command}")

        result = ITERM多终端调用.execute(command, timeout=timeout)
        results.append(result)

        if not result['success'] and stop_on_error:
            print(f"❌ Command failed: {result.get('error')}")
            break

        print(f"✅ Completed in {result['execution_time']:.2f}s")

    return results

# 使用示例：完整的部署流程
deploy_chain = [
    ("git pull", 5),
    ("npm install", 30),
    ("npm run test", 60),
    ("npm run build", 120),
    ("npm run deploy", 60)
]

results = execute_chain(deploy_chain, stop_on_error=True)

# 检查是否全部成功
all_success = all(r['success'] for r in results)
print(f"\n{'✅' if all_success else '❌'} Deployment {'succeeded' if all_success else 'failed'}")
```

## 🛠️ 故障排查

### 常见问题诊断

#### 问题1: 命令发送成功但无输出

**症状**:
```python
result = ITERM多终端调用.execute("git status")
# result['success'] = False
# result['error'] = "Output file not found. Command may have taken longer than 3s"
```

**可能原因**:
1. ⏱️ 超时时间不足
2. 🔒 命令需要权限（如sudo）
3. ❓ 命令需要交互输入
4. 💥 命令语法错误

**解决方案**:
```python
# 1. 增加超时
result = ITERM多终端调用.execute("git status", timeout=10)

# 2. 先在iTerm中手动测试命令
# 3. 使用非交互参数（-y, --force）
# 4. 检查命令语法（在iTerm中验证）
```

#### 问题2: 权限被拒绝

**症状**:
```
osascript: execution error: iTerm got an error: Not authorized to send Apple events to iTerm
```

**解决方案**:
```
1. 打开系统偏好设置
2. 安全性与隐私 > 隐私 > 辅助功能
3. 添加 iTerm.app
4. 重启iTerm和Python进程
```

#### 问题3: 窗口索引错误

**症状**:
```python
result = ITERM多终端调用.execute_in_window("ls", window_index=5)
# result['error'] = "Window 5 does not exist (total windows: 3)"
```

**解决方案**:
```python
# 先查询可用窗口
windows = ITERM多终端调用.list_windows()
print(f"Total windows: {windows['total']}")

# 使用有效的窗口索引
if windows['total'] >= 2:
    ITERM多终端调用.execute_in_window("ls", window_index=2)
```

### 调试技巧

#### 1. 启用详细日志

```python
import logging

logging.basicConfig(level=logging.DEBUG)

# 执行命令
result = ITERM多终端调用.execute("git status", timeout=5)

# 查看详细信息
print(f"Command: {result.get('command')}")
print(f"Success: {result.get('success')}")
print(f"Execution time: {result.get('execution_time')}s")
if not result['success']:
    print(f"Error: {result.get('error')}")
```

#### 2. 手动验证命令

```bash
# 在iTerm中手动测试命令
git status > /tmp/test-output.txt 2>&1

# 检查输出文件
cat /tmp/test-output.txt

# 清理
rm /tmp/test-output.txt
```

#### 3. 检查iTerm状态

```python
# 检查iTerm是否运行
import subprocess

result = subprocess.run(
    ["osascript", "-e", 'tell application "iTerm" to exists'],
    capture_output=True,
    text=True
)

if "true" in result.stdout:
    print("✅ iTerm is running")
else:
    print("❌ iTerm is not running")
```

## 📊 性能优化

### 并行执行策略

```python
import concurrent.futures
from typing import List, Dict

def execute_parallel(commands: List[str], timeout: int = 5) -> List[Dict]:
    """
    并行执行多个命令（在不同窗口）。

    注意: 需要先创建足够的窗口
    """
    windows = ITERM多终端调用.list_windows()
    if windows['total'] < len(commands):
        print(f"⚠️ 需要 {len(commands)} 个窗口，当前只有 {windows['total']} 个")
        # 创建额外窗口
        for _ in range(len(commands) - windows['total']):
            ITERM多终端调用.execute_in_new_window("echo 'Ready'")

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(commands)) as executor:
        futures = []
        for i, command in enumerate(commands):
            future = executor.submit(
                ITERM多终端调用.execute_in_window,
                command,
                i + 1,
                timeout
            )
            futures.append(future)

        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    return results

# 使用示例：并行测试
test_commands = [
    "npm run test:unit",
    "npm run test:integration",
    "npm run test:e2e"
]

results = execute_parallel(test_commands, timeout=60)

# 汇总结果
for i, result in enumerate(results):
    print(f"Test {i+1}: {'✅ PASS' if result['success'] else '❌ FAIL'}")
```

### 缓存与复用

```python
from functools import lru_cache
import time

@lru_cache(maxsize=128)
def cached_execute(command: str, cache_ttl: int = 60) -> Dict:
    """
    带缓存的命令执行（适用于频繁查询相同命令）。

    Args:
        command: 要执行的命令
        cache_ttl: 缓存有效期（秒）

    Returns:
        执行结果
    """
    cache_key = f"{command}_{int(time.time() / cache_ttl)}"
    return ITERM多终端调用.execute(command)

# 使用示例：频繁查询Git分支
for _ in range(10):
    # 只执行一次，后续从缓存读取
    result = cached_execute("git branch --show-current", cache_ttl=300)
    print(result['output'])
```

## 🔐 安全考虑

### 命令注入防护

```python
import shlex

def safe_execute(command: str, **kwargs) -> Dict:
    """
    安全的命令执行（基本的命令注入防护）。

    警告: 这不是完整的安全方案，仅用于演示
    """
    # 检查危险字符
    dangerous_chars = [';', '|', '&', '$', '`', '\n', '\r']

    for char in dangerous_chars:
        if char in command:
            return {
                "success": False,
                "error": f"Dangerous character detected: {char}",
                "command": command
            }

    # 执行命令
    return ITERM多终端调用.execute(command, **kwargs)

# 使用示例
safe_execute("git status")  # ✅ 安全
safe_execute("git status; rm -rf /")  # ❌ 被拒绝
```

### 敏感信息保护

```python
import re

def sanitize_output(output: str) -> str:
    """
    清理输出中的敏感信息。
    """
    # 移除可能的密码、token
    output = re.sub(r'password[=:]\s*\S+', 'password=***', output, flags=re.IGNORECASE)
    output = re.sub(r'token[=:]\s*\S+', 'token=***', output, flags=re.IGNORECASE)
    output = re.sub(r'api[_-]?key[=:]\s*\S+', 'api_key=***', output, flags=re.IGNORECASE)

    return output

# 使用示例
result = ITERM多终端调用.execute("env | grep SECRET")
clean_output = sanitize_output(result['output'])
print(clean_output)
```

## 📈 监控与日志

### 执行统计

```python
from collections import defaultdict
from datetime import datetime

class ExecutionMonitor:
    """命令执行监控器"""

    def __init__(self):
        self.stats = defaultdict(lambda: {
            "count": 0,
            "success": 0,
            "failure": 0,
            "total_time": 0.0
        })

    def log_execution(self, command: str, result: Dict):
        """记录执行统计"""
        stats = self.stats[command]
        stats["count"] += 1
        stats["total_time"] += result.get("execution_time", 0)

        if result.get("success"):
            stats["success"] += 1
        else:
            stats["failure"] += 1

    def report(self):
        """生成统计报告"""
        print("\n=== Execution Statistics ===")
        for command, stats in self.stats.items():
            avg_time = stats["total_time"] / stats["count"]
            success_rate = stats["success"] / stats["count"] * 100

            print(f"\nCommand: {command}")
            print(f"  Executions: {stats['count']}")
            print(f"  Success rate: {success_rate:.1f}%")
            print(f"  Avg time: {avg_time:.2f}s")

# 使用示例
monitor = ExecutionMonitor()

commands = ["git status", "npm test", "git pull"]
for cmd in commands:
    result = ITERM多终端调用.execute(cmd, timeout=10)
    monitor.log_execution(cmd, result)

monitor.report()
```

---

**文档版本**: v1.0.0
**最后更新**: 2025-10-30
**维护状态**: Active
