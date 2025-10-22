#!/usr/bin/env python3
"""
智能自动输入Hook - Python版本
自动检测用户输入意图并优化prompt，触发对应技能/智能体

基于突破性自动化发现，实现Layer 3到Layer 1/2的间接通路
通过UI自动化间接触发AI决策层
"""

import sys
import json
import subprocess
import time
import re
import os

# 日志文件路径
LOG_DIR = os.path.expanduser("~/.claude/logs")
LOG_FILE = os.path.join(LOG_DIR, "improve-prompt.log")

def log_message(message):
    """记录日志"""
    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {message}\n")

def send_notification(message):
    """发送通知消息（通过stderr输出）"""
    notification = {"message": message}
    print(json.dumps(notification), file=sys.stderr)

def detect_intent(prompt):
    """
    检测用户输入意图，返回优化的prompt
    """
    auto_text = ""

    # 规则1: 检测图片生成意图
    if re.search(r"(生成.*图|create.*image|generate.*image|海报|banner|封面)", prompt, re.IGNORECASE):
        auto_text = "请使用text-to-image skill生成一张16:9比例的专业海报图片，风格现代简约，使用橙色和白色作为主色调，提供专业的设计建议"
        log_message(f"触发规则: 图片生成 | 原始输入: {prompt[:50]}...")

    # 规则2: 检测分析需求
    elif re.search(r"(分析|analyze|数据|报表|统计)", prompt, re.IGNORECASE):
        auto_text = "请使用G1-经营分析优化师进行深度数据分析，提供详细的数据洞察、趋势分析和可操作的建议"
        log_message(f"触发规则: 数据分析 | 原始输入: {prompt[:50]}...")

    # 规则3: 检测文档生成
    elif re.search(r"(生成.*文档|readme|readme\.md|文档|overview|总结)", prompt, re.IGNORECASE):
        auto_text = "请使用专业文档生成工具生成完整的README文档，包含项目概述、安装说明、使用指南、API文档和贡献指南"
        log_message(f"触发规则: 文档生成 | 原始输入: {prompt[:50]}...")

    # 规则4: 检测代码相关
    elif re.search(r"(代码|code|编程|开发|function|class)", prompt, re.IGNORECASE):
        auto_text = "请使用专业编程专家进行代码开发，提供最佳实践的代码实现、注释说明和单元测试"
        log_message(f"触发规则: 代码开发 | 原始输入: {prompt[:50]}...")

    # 规则5: 检测设计相关
    elif re.search(r"(设计|design|ui|ux|界面|页面)", prompt, re.IGNORECASE):
        auto_text = "请使用专业的设计师进行UI/UX设计，提供现代化的设计方案、配色方案和交互流程"
        log_message(f"触发规则: 设计任务 | 原始输入: {prompt[:50]}...")

    return auto_text

def get_clipboard_command(text):
    """生成复制到剪贴板的命令"""
    # 使用pbcopy将文本复制到剪贴板
    return f'echo -n "{text.replace(chr(34), chr(92)+chr(34))}" | pbcopy'

def get_paste_command(delay=2):
    """生成粘贴并提交的AppleScript命令"""
    script = f"""
    delay {delay}
    tell application "System Events"
        keystroke "a" using command down  -- 全选
        delay 0.1
        keystroke "v" using command down  -- 粘贴
    end tell
    """

    return f"osascript -e '{script}'"

def main():
    """主函数"""
    try:
        # 读取Hook输入
        input_data = sys.stdin.read().strip()
        log_message(f"Hook触发 | 输入: {input_data[:200]}...")

        if not input_data:
            log_message("无输入内容，跳过处理")
            print("{}")
            return

        # 解析JSON输入
        try:
            data = json.loads(input_data)
            prompt = data.get('prompt', '').strip()
        except json.JSONDecodeError:
            # 如果不是JSON格式，假设整个输入就是prompt
            prompt = input_data.strip()

        if not prompt:
            log_message("无prompt内容，跳过处理")
            print("{}")
            return

        log_message(f"解析得到prompt: {prompt[:100]}...")

        # 检测意图并生成优化文本
        auto_text = detect_intent(prompt)

        if auto_text:
            # 显示通知
            send_notification(f"🤖 智能助手检测到需求\\n\\n建议输入:\\n{auto_text}\\n\\n将在2秒后自动输入...")

            # 延迟确保通知被看到
            time.sleep(0.5)

            # 异步执行UI自动化
            try:
                # 复制到剪贴板
                subprocess.run(get_clipboard_command(auto_text), shell=True, check=True)
                log_message("文本已复制到剪贴板")

                # 模拟粘贴
                paste_process = subprocess.Popen(get_paste_command().split())
                paste_process.wait()

                if paste_process.returncode == 0:
                    log_message("✅ 自动输入成功")
                else:
                    log_message("⚠️ 自动输入失败")

            except subprocess.CalledProcessError as e:
                log_message(f"❌ UI自动化执行失败: {e}")
                send_notification("❌ 自动输入失败，请手动输入")

        else:
            log_message("未匹配到任何规则，保持原输入不变")

        # 返回空JSON表示成功，不阻塞Claude
        print("{}")

    except Exception as e:
        log_message(f"❌ Hook执行异常: {str(e)}")
        # 发生异常时也返回空JSON，避免阻塞
        print("{}")

if __name__ == "__main__":
    main()
