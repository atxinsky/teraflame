#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Game Constants Definition File

This file contains various constant values used in the game.
"""

import os

# Project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Resource paths
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")

# Game window settings
GAME_TITLE = "Texas Hold'em Poker"
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

# Color definitions (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
TABLE_GREEN = (53, 101, 77)

# Game settings
INITIAL_PLAYER_CHIPS = 1000
SMALL_BLIND = 5
BIG_BLIND = 10
MIN_PLAYERS = 2
MAX_PLAYERS = 9
DEFAULT_PLAYERS = 6

# Card face value definitions
CARD_RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
CARD_SUITS = ['♣', '♦', '♥', '♠']  # Clubs, Diamonds, Hearts, Spades

# Hand ranking definitions (in ascending order of strength)
HAND_RANKINGS = [
    "High Card",
    "One Pair",
    "Two Pair",
    "Three of a Kind",
    "Straight",
    "Flush",
    "Full House",
    "Four of a Kind",
    "Straight Flush",
    "Royal Flush"
]

# Player action definitions
ACTIONS = {
    "FOLD": "Fold",
    "CHECK": "Check",
    "CALL": "Call",
    "RAISE": "Raise",
    "ALL_IN": "All In"
}

# Game stages
GAME_STATES = {
    "WAITING": "Waiting to Start",
    "PRE_FLOP": "Pre-Flop",
    "FLOP": "Flop",
    "TURN": "Turn",
    "RIVER": "River",
    "SHOWDOWN": "Showdown",
    "END_HAND": "End Hand"
}

# AI difficulty levels
AI_DIFFICULTIES = {
    "EASY": "Easy",
    "MEDIUM": "Medium",
    "HARD": "Hard"
}
