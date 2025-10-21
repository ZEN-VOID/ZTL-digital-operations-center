#!/usr/bin/env python3
"""
API项目启动管理脚本
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def check_dependencies():
    """检查依赖是否安装"""
    print("🔍 检查依赖...")
    
    required_packages = ["fastapi", "uvicorn"]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} 已安装")
        except ImportError:
            print(f"❌ {package} 未安装")
            return False
    
    print("✅ 所有依赖检查通过")
    return True


def start_project(project_name: str, port: int = 8000):
    """启动指定项目"""
    project_path = Path(f"projects/{project_name}")
    
    if not project_path.exists():
        print(f"❌ 项目 {project_name} 不存在")
        return False
    
    print(f"🚀 启动项目: {project_name} (端口: {port})")
    
    # 切换到项目目录
    os.chdir(project_path)
    
    # 启动uvicorn服务器
    cmd = [
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", str(port)
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 启动失败: {e}")
        return False
    except KeyboardInterrupt:
        print(f"\n⏹️ 停止项目: {project_name}")
        return True
    
    return True


def list_projects():
    """列出所有可用项目"""
    projects_dir = Path("projects")
    
    if not projects_dir.exists():
        print("❌ projects 目录不存在")
        return []
    
    projects = []
    for item in projects_dir.iterdir():
        if item.is_dir() and (item / "app" / "main.py").exists():
            projects.append(item.name)
    
    return projects


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="ZTL API项目管理工具")
    parser.add_argument("command", choices=["start", "list", "check"], help="执行的命令")
    parser.add_argument("--project", "-p", help="项目名称")
    parser.add_argument("--port", type=int, default=8000, help="端口号")
    
    args = parser.parse_args()
    
    # 切换到API根目录
    script_dir = Path(__file__).parent
    api_dir = script_dir.parent
    os.chdir(api_dir)
    
    if args.command == "check":
        if check_dependencies():
            print("🎉 环境检查通过")
            return 0
        else:
            print("❌ 环境检查失败")
            return 1
    
    elif args.command == "list":
        projects = list_projects()
        if projects:
            print("📋 可用项目:")
            for project in projects:
                print(f"  - {project}")
        else:
            print("❌ 没有找到可用项目")
        return 0
    
    elif args.command == "start":
        if not args.project:
            projects = list_projects()
            if len(projects) == 1:
                args.project = projects[0]
                print(f"🎯 自动选择项目: {args.project}")
            else:
                print("❌ 请指定要启动的项目")
                print("可用项目:")
                for project in projects:
                    print(f"  - {project}")
                return 1
        
        if not check_dependencies():
            print("❌ 依赖检查失败，请先安装依赖")
            return 1
        
        if start_project(args.project, args.port):
            return 0
        else:
            return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
