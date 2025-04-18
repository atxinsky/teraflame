#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
德州扑克游戏启动脚本

这个脚本是游戏的入口点，它初始化必要的组件并启动游戏。
"""

import os
import sys
import argparse

# 确保当前目录在Python路径中
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# 导入游戏模块
from src.main import main


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="德州扑克游戏")
    
    # 添加命令行参数
    parser.add_argument('--fullscreen', action='store_true', help='以全屏模式启动游戏')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    parser.add_argument('--no-sound', action='store_true', help='禁用声音')
    parser.add_argument('--players', type=int, default=5, help='AI玩家数量 (1-8)')
    parser.add_argument('--chips', type=int, default=1000, help='初始筹码数量')
    
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    
    # 设置环境变量
    if args.fullscreen:
        os.environ['FULLSCREEN'] = '1'
    
    if args.debug:
        os.environ['DEBUG_MODE'] = '1'
    
    if args.no_sound:
        os.environ['SOUND_ENABLED'] = '0'
    
    # 设置AI玩家数量
    os.environ['AI_PLAYERS'] = str(max(1, min(8, args.players)))
    
    # 设置初始筹码
    os.environ['INITIAL_CHIPS'] = str(max(100, args.chips))
    
    # 启动游戏
    main()
