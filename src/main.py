#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Texas Hold'em Poker Game - Main Entry

This file is the entry point of the poker game, responsible for initializing the game and starting the main loop.
"""

import os
import sys
import pygame
from pygame.locals import *

# Add project root directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from src.game.game import Game
from src.ui.interface import GameInterface
from src.utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, GAME_TITLE


def main():
    """Game main function"""
    # Initialize Pygame
    pygame.init()
    pygame.display.set_caption(GAME_TITLE)
    
    # Create game window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    
    # Initialize game logic and interface
    game = Game()
    interface = GameInterface(screen, game)
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            else:
                interface.handle_event(event)
        
        # Update game state
        game.update()
        
        # Render interface
        interface.render()
        
        # Control frame rate
        pygame.display.flip()
        clock.tick(FPS)
    
    # Clean up and exit
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
