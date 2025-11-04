#!/usr/bin/env python3
"""
深渊凝视 (Abyss Gaze) - iTerm Terminal Control & Output Capture
Version: 1.0.0
Created: 2025-10-30

Core execution engine for sending commands to iTerm and capturing output.
"""

import subprocess
import time
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Union
from datetime import datetime


class AbyssGaze:
    """iTerm终端控制与输出捕获核心类"""

    def __init__(self):
        """初始化深渊凝视"""
        self.default_timeout = 3
        self.temp_dir = Path("/tmp")
        self.script_dir = Path(__file__).parent.parent.parent.parent / "scripts"

    def execute(self, command: str, timeout: int = None) -> Dict[str, Union[str, bool, float]]:
        """
        发送命令到iTerm当前窗口并捕获输出。

        Args:
            command: 要执行的shell命令
            timeout: 超时时间（秒），默认3秒

        Returns:
            Dict包含:
                - success: 是否成功
                - command: 执行的命令
                - output: 命令输出
                - execution_time: 执行时间
                - window: 窗口信息
        """
        timeout = timeout or self.default_timeout
        start_time = time.time()

        # 生成唯一临时文件
        timestamp = int(time.time())
        random_suffix = subprocess.run(
            ["bash", "-c", "echo $RANDOM"],
            capture_output=True,
            text=True
        ).stdout.strip()

        output_file = self.temp_dir / f"iterm-capture-{timestamp}-{random_suffix}.txt"

        try:
            # 发送命令到iTerm（带重定向）
            applescript = f'''
tell application "iTerm"
    activate

    -- 如果没有窗口，创建新窗口
    if (count of windows) = 0 then
        create window with default profile
    end if

    tell current session of current window
        write text "{command} > {output_file} 2>&1"
    end tell
end tell
'''

            result = subprocess.run(
                ["osascript", "-e", applescript],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode != 0:
                return {
                    "success": False,
                    "command": command,
                    "error": result.stderr or "Failed to send command to iTerm",
                    "execution_time": time.time() - start_time
                }

            # 等待命令执行
            time.sleep(timeout)

            # 读取输出
            if output_file.exists():
                output = output_file.read_text(encoding='utf-8', errors='ignore')
                output_file.unlink()  # 清理临时文件

                return {
                    "success": True,
                    "command": command,
                    "output": output,
                    "execution_time": time.time() - start_time,
                    "window": "current"
                }
            else:
                return {
                    "success": False,
                    "command": command,
                    "error": f"Output file not found. Command may have taken longer than {timeout}s",
                    "execution_time": time.time() - start_time,
                    "suggestion": f"Try increasing timeout (current: {timeout}s)"
                }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "command": command,
                "error": "osascript command timed out",
                "execution_time": time.time() - start_time
            }
        except Exception as e:
            return {
                "success": False,
                "command": command,
                "error": str(e),
                "execution_time": time.time() - start_time
            }

    def execute_in_new_window(self, command: str, timeout: int = None) -> Dict[str, Union[str, bool, int]]:
        """
        在新的iTerm窗口中执行命令。

        Args:
            command: 要执行的shell命令
            timeout: 超时时间（秒），默认3秒

        Returns:
            Dict包含:
                - success: 是否成功
                - command: 执行的命令
                - window: 窗口类型
                - window_index: 新窗口索引
        """
        try:
            applescript = f'''
tell application "iTerm"
    activate
    create window with default profile
    tell current session of current window
        write text "{command}"
    end tell
    return count of windows
end tell
'''

            result = subprocess.run(
                ["osascript", "-e", applescript],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                window_count = int(result.stdout.strip())
                return {
                    "success": True,
                    "command": command,
                    "window": "new",
                    "window_index": window_count
                }
            else:
                return {
                    "success": False,
                    "command": command,
                    "error": result.stderr or "Failed to create new window"
                }

        except Exception as e:
            return {
                "success": False,
                "command": command,
                "error": str(e)
            }

    def execute_in_window(
        self,
        command: str,
        window_index: int,
        timeout: int = None
    ) -> Dict[str, Union[str, bool, int, float]]:
        """
        在指定的iTerm窗口中执行命令并捕获输出。

        Args:
            command: 要执行的shell命令
            window_index: 窗口索引（从1开始）
            timeout: 超时时间（秒），默认3秒

        Returns:
            Dict包含:
                - success: 是否成功
                - command: 执行的命令
                - output: 命令输出（如果捕获）
                - window_index: 窗口索引
        """
        timeout = timeout or self.default_timeout
        start_time = time.time()

        # 生成唯一临时文件
        timestamp = int(time.time())
        random_suffix = subprocess.run(
            ["bash", "-c", "echo $RANDOM"],
            capture_output=True,
            text=True
        ).stdout.strip()

        output_file = self.temp_dir / f"iterm-capture-{timestamp}-{random_suffix}.txt"

        try:
            applescript = f'''
tell application "iTerm"
    activate

    set windowCount to count of windows

    if windowCount < {window_index} then
        error "Window {window_index} does not exist (total windows: " & windowCount & ")"
    end if

    tell current session of window {window_index}
        write text "{command} > {output_file} 2>&1"
    end tell
end tell
'''

            result = subprocess.run(
                ["osascript", "-e", applescript],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode != 0:
                return {
                    "success": False,
                    "command": command,
                    "window_index": window_index,
                    "error": result.stderr or f"Failed to send command to window {window_index}",
                    "execution_time": time.time() - start_time
                }

            # 等待命令执行
            time.sleep(timeout)

            # 读取输出
            if output_file.exists():
                output = output_file.read_text(encoding='utf-8', errors='ignore')
                output_file.unlink()

                return {
                    "success": True,
                    "command": command,
                    "output": output,
                    "window_index": window_index,
                    "execution_time": time.time() - start_time
                }
            else:
                return {
                    "success": False,
                    "command": command,
                    "window_index": window_index,
                    "error": f"Output file not found. Command may have taken longer than {timeout}s",
                    "execution_time": time.time() - start_time
                }

        except Exception as e:
            return {
                "success": False,
                "command": command,
                "window_index": window_index,
                "error": str(e),
                "execution_time": time.time() - start_time
            }

    def list_windows(self) -> Dict[str, Union[int, List[Dict]]]:
        """
        查询所有iTerm窗口信息。

        Returns:
            Dict包含:
                - total: 窗口总数
                - windows: 窗口列表，每个窗口包含:
                    - index: 窗口索引
                    - tabs: 标签页数量
                    - session_name: 会话名称
        """
        try:
            applescript = '''
tell application "iTerm"
    set windowCount to count of windows

    if windowCount = 0 then
        return "0"
    end if

    set output to windowCount as text

    repeat with i from 1 to windowCount
        set tabCount to count of tabs of window i
        set output to output & "|" & tabCount

        try
            set sessionName to name of current session of window i
            set output to output & "|" & sessionName
        on error
            set output to output & "|Unknown"
        end try
    end repeat

    return output
end tell
'''

            result = subprocess.run(
                ["osascript", "-e", applescript],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                parts = result.stdout.strip().split('|')
                total = int(parts[0])

                if total == 0:
                    return {"total": 0, "windows": []}

                windows = []
                for i in range(1, len(parts), 2):
                    if i + 1 < len(parts):
                        windows.append({
                            "index": len(windows) + 1,
                            "tabs": int(parts[i]),
                            "session_name": parts[i + 1]
                        })

                return {
                    "total": total,
                    "windows": windows
                }
            else:
                return {
                    "total": 0,
                    "windows": [],
                    "error": result.stderr
                }

        except Exception as e:
            return {
                "total": 0,
                "windows": [],
                "error": str(e)
            }

    def broadcast(self, command: str) -> Dict[str, Union[str, bool, int]]:
        """
        向所有iTerm窗口广播命令（不捕获输出）。

        Args:
            command: 要广播的shell命令

        Returns:
            Dict包含:
                - success: 是否成功
                - command: 广播的命令
                - windows_count: 广播到的窗口数量
        """
        try:
            applescript = f'''
tell application "iTerm"
    set windowCount to count of windows

    if windowCount = 0 then
        error "No windows available"
    end if

    repeat with i from 1 to windowCount
        tell current session of window i
            write text "{command}"
        end tell
    end repeat

    return windowCount
end tell
'''

            result = subprocess.run(
                ["osascript", "-e", applescript],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                windows_count = int(result.stdout.strip())
                return {
                    "success": True,
                    "command": command,
                    "windows_count": windows_count
                }
            else:
                return {
                    "success": False,
                    "command": command,
                    "error": result.stderr or "Failed to broadcast command"
                }

        except Exception as e:
            return {
                "success": False,
                "command": command,
                "error": str(e)
            }

    def type_text_in_window(
        self,
        text: str,
        window_index: int,
        submit: bool = False
    ) -> Dict[str, Union[str, bool, int]]:
        """
        向指定窗口输入文本（使用剪贴板方式，避免输入法和转义问题）。

        Args:
            text: 要输入的文本
            window_index: 窗口索引（从1开始）
            submit: 是否按回车提交（默认False）

        Returns:
            Dict包含:
                - success: 是否成功
                - text: 输入的文本
                - window_index: 窗口索引
                - submitted: 是否已提交
        """
        try:
            # Step 1: 将文本复制到剪贴板
            subprocess.run(
                ["pbcopy"],
                input=text.encode('utf-8'),
                check=True
            )

            # Step 2: 使用 AppleScript 粘贴并提交
            if submit:
                # 粘贴并按回车
                applescript = f'''
tell application "iTerm"
    activate

    set windowCount to count of windows

    if windowCount < {window_index} then
        error "Window {window_index} does not exist (total windows: " & windowCount & ")"
    end if

    -- 切换到指定窗口
    select window {window_index}
    delay 0.5

    tell application "System Events"
        tell process "iTerm2"
            set frontmost to true
            delay 0.3

            -- 粘贴内容 (Cmd+V)
            keystroke "v" using command down
            delay 0.5

            -- 按回车提交
            keystroke return
        end tell
    end tell
end tell
'''
            else:
                # 仅粘贴，不按回车
                applescript = f'''
tell application "iTerm"
    activate

    set windowCount to count of windows

    if windowCount < {window_index} then
        error "Window {window_index} does not exist (total windows: " & windowCount & ")"
    end if

    -- 切换到指定窗口
    select window {window_index}
    delay 0.5

    tell application "System Events"
        tell process "iTerm2"
            set frontmost to true
            delay 0.3

            -- 粘贴内容 (Cmd+V)
            keystroke "v" using command down
        end tell
    end tell
end tell
'''

            result = subprocess.run(
                ["osascript", "-e", applescript],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                return {
                    "success": True,
                    "text": text[:100] + "..." if len(text) > 100 else text,  # 截断日志输出
                    "window_index": window_index,
                    "submitted": submit
                }
            else:
                return {
                    "success": False,
                    "text": text[:100] + "..." if len(text) > 100 else text,
                    "window_index": window_index,
                    "error": result.stderr or f"Failed to type text in window {window_index}"
                }

        except Exception as e:
            return {
                "success": False,
                "text": text[:100] + "..." if len(text) > 100 else text,
                "window_index": window_index,
                "error": str(e)
            }


# 全局实例（供skill直接调用）
深渊凝视 = AbyssGaze()


# CLI Interface
if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python abyss_gaze.py <method> [args...]")
        print("\nMethods:")
        print("  execute <command> [timeout]")
        print("  execute_in_new_window <command>")
        print("  execute_in_window <command> <window_index> [timeout]")
        print("  type_text_in_window <text> <window_index> [submit:true|false]")
        print("  list_windows")
        print("  broadcast <command>")
        sys.exit(1)

    method = sys.argv[1]
    gaze = AbyssGaze()

    if method == "execute":
        command = sys.argv[2]
        timeout = int(sys.argv[3]) if len(sys.argv) > 3 else None
        result = gaze.execute(command, timeout)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif method == "execute_in_new_window":
        command = sys.argv[2]
        result = gaze.execute_in_new_window(command)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif method == "execute_in_window":
        command = sys.argv[2]
        window_index = int(sys.argv[3])
        timeout = int(sys.argv[4]) if len(sys.argv) > 4 else None
        result = gaze.execute_in_window(command, window_index, timeout)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif method == "type_text_in_window":
        text = sys.argv[2]
        window_index = int(sys.argv[3])
        submit = sys.argv[4].lower() == "true" if len(sys.argv) > 4 else False
        result = gaze.type_text_in_window(text, window_index, submit)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif method == "list_windows":
        result = gaze.list_windows()
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif method == "broadcast":
        command = sys.argv[2]
        result = gaze.broadcast(command)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    else:
        print(f"Unknown method: {method}")
        sys.exit(1)
