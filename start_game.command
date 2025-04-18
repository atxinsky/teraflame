#!/bin/bash

# 德州扑克游戏启动脚本 (macOS)

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 切换到项目目录
cd "$SCRIPT_DIR"

# 检查Python环境
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "错误: 未找到Python。请安装Python 3.6或更高版本。"
    exit 1
fi

# 检查Python版本
$PYTHON -c "import sys; sys.exit(0 if sys.version_info >= (3,6) else 1)" || {
    echo "错误: 需要Python 3.6或更高版本。"
    exit 1
}

# 检查虚拟环境
VENV_DIR="venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "首次运行，创建虚拟环境..."
    $PYTHON -m venv "$VENV_DIR" || {
        echo "创建虚拟环境失败。尝试直接运行游戏..."
        $PYTHON run.py
        exit $?
    }
fi

# 激活虚拟环境
source "$VENV_DIR/bin/activate" || {
    echo "激活虚拟环境失败。尝试直接运行游戏..."
    $PYTHON run.py
    exit $?
}

# 安装依赖
if [ ! -f "$VENV_DIR/.dependencies_installed" ]; then
    echo "安装游戏依赖..."
    pip install -r requirements.txt && touch "$VENV_DIR/.dependencies_installed" || {
        echo "安装依赖失败。"
        exit 1
    }
fi

# 启动游戏
echo "启动德州扑克游戏..."
python run.py "$@"

# 退出状态
exit $?
