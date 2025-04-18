#!/bin/bash

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 切换到项目目录
cd "$SCRIPT_DIR"

# 激活虚拟环境
source venv/bin/activate

# 启动游戏
echo "启动德州扑克游戏..."
python run.py "$@"
