#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
德州扑克游戏安装脚本

这个脚本用于安装游戏依赖和准备运行环境。
"""

import os
import sys
import platform
import subprocess
import shutil


def print_header():
    """打印安装标题"""
    print("\n" + "=" * 60)
    print("           德州扑克游戏安装程序")
    print("=" * 60 + "\n")


def check_python_version():
    """检查Python版本"""
    print("检查Python版本...")
    
    if sys.version_info < (3, 6):
        print("错误: 需要Python 3.6或更高版本。")
        print(f"当前Python版本: {sys.version}")
        return False
    
    print(f"Python版本检查通过: {sys.version}")
    return True


def create_virtual_environment():
    """创建虚拟环境"""
    print("\n正在创建虚拟环境...")
    
    venv_dir = "venv"
    
    # 如果已存在，询问是否重新创建
    if os.path.exists(venv_dir):
        response = input(f"虚拟环境'{venv_dir}'已存在。是否重新创建? (y/n): ").strip().lower()
        if response == 'y':
            try:
                shutil.rmtree(venv_dir)
                print(f"已删除现有虚拟环境: {venv_dir}")
            except Exception as e:
                print(f"删除虚拟环境失败: {e}")
                return False
        else:
            print("使用现有虚拟环境。")
            return True
    
    # 创建虚拟环境
    try:
        subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
        print(f"成功创建虚拟环境: {venv_dir}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"创建虚拟环境失败: {e}")
        return False


def install_dependencies(venv_dir="venv"):
    """安装依赖包"""
    print("\n正在安装依赖包...")
    
    # 确定pip路径
    if platform.system() == "Windows":
        pip_path = os.path.join(venv_dir, "Scripts", "pip")
    else:
        pip_path = os.path.join(venv_dir, "bin", "pip")
    
    # 安装依赖
    try:
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("依赖包安装成功。")
        return True
    except subprocess.CalledProcessError as e:
        print(f"依赖包安装失败: {e}")
        return False


def create_launch_script():
    """创建启动脚本"""
    print("\n正在创建启动脚本...")
    
    if platform.system() == "Windows":
        # 创建Windows批处理文件
        script_path = "start_game.bat"
        with open(script_path, "w") as f:
            f.write("@echo off\n")
            f.write("echo 正在启动德州扑克游戏...\n")
            f.write("cd %~dp0\n")
            f.write("call venv\\Scripts\\activate\n")
            f.write("python run.py %*\n")
            f.write("pause\n")
    else:
        # 创建Unix shell脚本
        script_path = "start_game.sh"
        with open(script_path, "w") as f:
            f.write("#!/bin/bash\n\n")
            f.write("# 获取脚本所在目录\n")
            f.write("SCRIPT_DIR=\"$( cd \"$( dirname \"${BASH_SOURCE[0]}\" )\" && pwd )\"\n\n")
            f.write("# 切换到项目目录\n")
            f.write("cd \"$SCRIPT_DIR\"\n\n")
            f.write("# 激活虚拟环境\n")
            f.write("source venv/bin/activate\n\n")
            f.write("# 启动游戏\n")
            f.write("echo \"启动德州扑克游戏...\"\n")
            f.write("python run.py \"$@\"\n")
        
        # 使脚本可执行
        os.chmod(script_path, 0o755)
    
    print(f"启动脚本已创建: {script_path}")
    return True


def finalize_installation():
    """完成安装并提供说明"""
    print("\n" + "=" * 60)
    print("           安装完成")
    print("=" * 60 + "\n")
    
    print("德州扑克游戏已成功安装！您可以通过以下方式启动游戏：\n")
    
    if platform.system() == "Windows":
        print("1. 双击 'start_game.bat' 文件")
        print("2. 或在命令行中运行: python run.py")
    else:
        print("1. 运行 './start_game.sh' 命令")
        print("2. 或运行 './start_game.command' (仅限macOS)")
        print("3. 或在命令行中运行: python run.py")
    
    print("\n祝您游戏愉快！\n")


def main():
    """主安装流程"""
    print_header()
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 创建虚拟环境
    if not create_virtual_environment():
        sys.exit(1)
    
    # 安装依赖
    if not install_dependencies():
        sys.exit(1)
    
    # 创建启动脚本
    create_launch_script()
    
    # 完成安装
    finalize_installation()


if __name__ == "__main__":
    main()
