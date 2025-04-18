#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
游戏配置文件

定义游戏的全局配置选项。
"""

# 游戏基本设置
GAME_TITLE = "德州扑克"
VERSION = "1.0.0"
DEBUG_MODE = False

# 窗口设置
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FULLSCREEN = False
FPS = 60
VSYNC = True

# 游戏设置
DEFAULT_PLAYER_NAME = "玩家"
INITIAL_PLAYER_CHIPS = 1000
DEFAULT_AI_PLAYERS = 5
DEFAULT_AI_DIFFICULTY = "MEDIUM"  # "EASY", "MEDIUM", "HARD"

# 盲注设置
SMALL_BLIND = 5
BIG_BLIND = 10
AUTO_INCREASE_BLINDS = False  # 是否自动增加盲注
BLINDS_INCREASE_HANDS = 10  # 每过多少手牌增加盲注
BLINDS_INCREASE_RATIO = 1.5  # 盲注增加比例

# 游戏速度设置
AI_DECISION_DELAY = 1.0  # AI决策延迟（秒）
CARD_DEAL_DELAY = 0.3  # 发牌延迟（秒）
ANIMATION_SPEED = 1.0  # 动画速度倍率

# 声音设置
SOUND_ENABLED = True
MUSIC_ENABLED = True
SOUND_VOLUME = 0.7  # 0.0 - 1.0
MUSIC_VOLUME = 0.5  # 0.0 - 1.0

# 高级设置
AUTO_SAVE = True  # 自动保存游戏状态
AUTO_SAVE_INTERVAL = 5  # 自动保存间隔（分钟）
SHOW_HINTS = True  # 显示游戏提示
SHOW_HAND_STRENGTH = False  # 显示手牌强度（调试用）

# 路径设置
SAVE_GAME_PATH = "savegames/"
LOG_FILE_PATH = "logs/game.log"
