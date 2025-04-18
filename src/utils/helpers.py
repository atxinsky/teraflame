#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Helper functions module

Contains various utility functions used in the game.
"""

import os
import pygame
from src.utils.constants import IMAGES_DIR, FONTS_DIR, SOUNDS_DIR

# Global font cache to avoid repeated loading
_font_cache = {}


def load_image(filename, scale=None, convert_alpha=True):
    """
    Load image resource
    
    Args:
        filename (str): Image filename
        scale (tuple, optional): Scale dimensions (width, height)
        convert_alpha (bool): Whether to convert Alpha channel
    
    Returns:
        pygame.Surface: Loaded image surface
    """
    path = os.path.join(IMAGES_DIR, filename)
    try:
        if convert_alpha:
            image = pygame.image.load(path).convert_alpha()
        else:
            image = pygame.image.load(path).convert()
        
        if scale:
            image = pygame.transform.scale(image, scale)
        
        return image
    except pygame.error:
        print(f"Unable to load image: {path}")
        # Return a placeholder image
        surface = pygame.Surface((50, 75))
        surface.fill((255, 0, 0))
        return surface


def load_font(size, font_name=None):
    """
    Load font resource
    
    Args:
        size (int): Font size
        font_name (str, optional): Font name
    
    Returns:
        pygame.font.Font: Loaded font object
    """
    # If already cached, return directly
    key = (font_name, size)
    if key in _font_cache:
        return _font_cache[key]
    
    loaded_font = None
    
    # Try to use system fonts
    try:
        loaded_font = pygame.font.SysFont('arial', size)
        print(f"Loaded system font 'arial'")
    except Exception as e:
        print(f"Failed to load system font 'arial': {e}")
    
    # If failed, try Pygame default font
    if loaded_font is None:
        try:
            loaded_font = pygame.font.Font(None, size)
            print("Loaded Pygame default font")
        except Exception as e:
            print(f"Failed to load Pygame default font: {e}")
            # If nothing works, return None
            return None
    
    # Cache font
    _font_cache[key] = loaded_font
    return loaded_font


def load_sound(filename):
    """
    Load sound resource
    
    Args:
        filename (str): Sound filename
    
    Returns:
        pygame.mixer.Sound: Loaded sound object
    """
    path = os.path.join(SOUNDS_DIR, filename)
    try:
        return pygame.mixer.Sound(path)
    except pygame.error:
        print(f"Unable to load sound: {path}")
        return None


def format_money(amount):
    """
    Format chip amount
    
    Args:
        amount (int): Amount value
    
    Returns:
        str: Formatted amount string
    """
    return f"${amount:,}"


def calculate_pot_distribution(players, pot):
    """
    Calculate pot distribution
    
    Args:
        players (list): Player list
        pot (int): Pot amount
    
    Returns:
        dict: Mapping from player ID to gained amount
    """
    # This is a simplified pot distribution logic
    # In actual game, complex side pots need to be handled
    active_players = [p for p in players if not p.folded]
    if not active_players:
        return {}
    
    # Sort by hand strength
    sorted_players = sorted(active_players, key=lambda p: p.hand_strength, reverse=True)
    
    # For simplicity, the strongest hand gets the entire pot
    winner = sorted_players[0]
    return {winner.id: pot}


def debug_print(message):
    """
    Print debug information
    
    Args:
        message (str): Debug message
    """
    # Can implement environment variable controlled debug output here
    import inspect
    caller_frame = inspect.currentframe().f_back
    caller_info = f"{os.path.basename(caller_frame.f_code.co_filename)}:{caller_frame.f_lineno}"
    print(f"[DEBUG] {caller_info} - {message}")
