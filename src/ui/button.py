#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Button Module

Provides interactive buttons used in the game.
"""

import pygame
from src.utils.constants import WHITE, BLACK
from src.utils.helpers import load_font


class Button:
    """Interactive Button Class"""
    
    def __init__(self, x, y, width, height, text, action=None, 
                 bg_color=(100, 100, 100), highlight_color=(150, 150, 150),
                 text_color=WHITE, font_size=20, font_name=None,
                 enabled=True, value=None, border_radius=5):
        """
        Initialize button
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Width
            height (int): Height
            text (str): Button text
            action (function, optional): Function to execute on click. Default is None
            bg_color (tuple, optional): Background color. Default is gray
            highlight_color (tuple, optional): Highlight color. Default is light gray
            text_color (tuple, optional): Text color. Default is white
            font_size (int, optional): Font size. Default is 20
            font_name (str, optional): Font name. Default is None (use system default font)
            enabled (bool, optional): Whether button is enabled. Default is True
            value (any, optional): Value associated with button. Default is None
            border_radius (int, optional): Border radius. Default is 5
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.action = action
        self.bg_color = bg_color
        self.original_bg_color = bg_color
        self.highlight_color = highlight_color
        self.text_color = text_color
        self.font_size = font_size
        self.enabled = enabled
        self.value = value
        self.border_radius = border_radius
        self.hovered = False
        self.clicked = False
        self.visible = True
        
        # Load font
        self.font = load_font(font_size, font_name)
        if self.font is None:
            # If no font can be loaded, create a blank text surface
            self.rendered_text = pygame.Surface((1, 1), pygame.SRCALPHA)
            print(f"Warning: Cannot render text for button '{text}', using blank text")
        else:
            # Render text
            try:
                self.rendered_text = self.font.render(text, True, text_color)
            except Exception as e:
                print(f"Text rendering failed: {e}, using blank text")
                self.rendered_text = pygame.Surface((1, 1), pygame.SRCALPHA)
        
        # Set text rectangle
        self.text_rect = self.rendered_text.get_rect()
        self.text_rect.center = (x + width // 2, y + height // 2)
        
        # Create button rectangle
        self.rect = pygame.Rect(x, y, width, height)
    
    def set_position(self, x, y):
        """
        Set button position
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
        """
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.text_rect.center = (x + self.width // 2, y + self.height // 2)
    
    def set_text(self, text):
        """
        Set button text
        
        Args:
            text (str): New text
        """
        self.text = text
        if self.font is None:
            return
            
        try:
            self.rendered_text = self.font.render(text, True, self.text_color)
            self.text_rect = self.rendered_text.get_rect()
            self.text_rect.center = (self.x + self.width // 2, self.y + self.height // 2)
        except Exception as e:
            print(f"Button text '{text}' rendering failed: {e}")
    
    def set_enabled(self, enabled):
        """
        Set whether button is enabled
        
        Args:
            enabled (bool): Whether enabled
        """
        self.enabled = enabled
        if not enabled:
            # Color when disabled
            self.bg_color = tuple(max(c - 50, 0) for c in self.original_bg_color)
        else:
            self.bg_color = self.original_bg_color
    
    def set_visible(self, visible):
        """
        Set whether button is visible
        
        Args:
            visible (bool): Whether visible
        """
        self.visible = visible
    
    def handle_event(self, event):
        """
        Handle events
        
        Args:
            event (pygame.event.Event): Pygame event
        
        Returns:
            bool: True if button was clicked
        """
        if not self.visible or not self.enabled:
            return False
        
        # Get mouse position
        pos = pygame.mouse.get_pos()
        
        # Check if mouse is over button
        self.hovered = self.rect.collidepoint(pos)
        
        # Handle click events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hovered:
                self.clicked = True
                return False
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.clicked and self.hovered:
                self.clicked = False
                if self.action:
                    if self.value is not None:
                        self.action(self.value)
                    else:
                        self.action()
                return True
            self.clicked = False
        
        return False
    
    def draw(self, surface):
        """
        Draw button
        
        Args:
            surface (pygame.Surface): Drawing surface
        """
        if not self.visible:
            return
        
        # Choose color
        color = self.highlight_color if self.hovered else self.bg_color
        if self.clicked and self.hovered:
            # Slightly darker when clicked
            color = tuple(max(c - 20, 0) for c in color)
        
        # If disabled, use darker color
        if not self.enabled:
            color = tuple(max(c - 50, 0) for c in self.bg_color)
        
        # Draw button
        if self.border_radius > 0:
            pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
            # Add border
            if self.hovered and self.enabled:
                pygame.draw.rect(surface, self.text_color, self.rect, 
                                 width=2, border_radius=self.border_radius)
        else:
            pygame.draw.rect(surface, color, self.rect)
            # Add border
            if self.hovered and self.enabled:
                pygame.draw.rect(surface, self.text_color, self.rect, width=2)
        
        # Draw text
        if self.font is not None:
            text_color = self.text_color
            if not self.enabled:
                # Darker text color when disabled
                text_color = tuple(max(c - 50, 0) for c in self.text_color)
            
            try:
                # Re-render text
                self.rendered_text = self.font.render(self.text, True, text_color)
                self.text_rect = self.rendered_text.get_rect()
                self.text_rect.center = (self.x + self.width // 2, self.y + self.height // 2)
                surface.blit(self.rendered_text, self.text_rect)
            except Exception as e:
                print(f"Drawing button text '{self.text}' failed: {e}")
                # Draw a placeholder color block in button center
                indicator_rect = pygame.Rect(0, 0, self.width // 2, self.height // 2)
                indicator_rect.center = (self.x + self.width // 2, self.y + self.height // 2)
                pygame.draw.rect(surface, self.text_color, indicator_rect)


class SliderButton(Button):
    """Slider Button Class, used to adjust values"""
    
    def __init__(self, x, y, width, height, min_value, max_value, 
                 initial_value=None, on_change=None, **kwargs):
        """
        Initialize slider button
        
        Args:
            x, y, width, height: Slider position and size
            min_value (int): Minimum value
            max_value (int): Maximum value
            initial_value (int, optional): Initial value
            on_change (function, optional): Callback when value changes
        """
        # Ensure initial value is within range
        if initial_value is None:
            initial_value = min_value
        else:
            initial_value = max(min(initial_value, max_value), min_value)
        
        # Set text as current value string
        initial_text = str(initial_value)
        super().__init__(x, y, width, height, initial_text, **kwargs)
        
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.on_change = on_change
        
        # Slider handle size
        self.handle_width = 20
        self.handle_height = height
        
        # Calculate slider position
        self.update_handle_position()
        
        # Dragging state
        self.dragging = False
    
    def update_handle_position(self):
        """Update slider handle position"""
        # Calculate value proportion within range
        value_range = self.max_value - self.min_value
        if value_range == 0:
            ratio = 0
        else:
            ratio = (self.value - self.min_value) / value_range
        
        # Calculate handle position
        usable_width = self.width - self.handle_width
        self.handle_x = self.x + int(usable_width * ratio)
        self.handle_rect = pygame.Rect(self.handle_x, self.y, 
                                      self.handle_width, self.handle_height)
    
    def update_value_from_position(self, x_pos):
        """Update value based on position"""
        # Calculate relative position
        rel_x = max(0, min(x_pos - self.x, self.width - self.handle_width))
        usable_width = self.width - self.handle_width
        
        # Calculate new value
        if usable_width == 0:
            ratio = 0
        else:
            ratio = rel_x / usable_width
        
        value_range = self.max_value - self.min_value
        new_value = int(self.min_value + ratio * value_range)
        
        # Ensure value is within range
        new_value = max(min(new_value, self.max_value), self.min_value)
        
        # If value changed, update and call callback
        if new_value != self.value:
            self.value = new_value
            self.set_text(str(self.value))
            if self.on_change:
                self.on_change(self.value)
    
    def handle_event(self, event):
        """
        Handle slider events
        
        Args:
            event (pygame.event.Event): Pygame event
        
        Returns:
            bool: Whether event was handled
        """
        if not self.visible or not self.enabled:
            return False
        
        pos = pygame.mouse.get_pos()
        
        # Slider dragging logic
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.handle_rect.collidepoint(pos):
                self.dragging = True
                return True
            elif self.rect.collidepoint(pos):
                # Click on slider track
                self.update_value_from_position(pos[0])
                self.update_handle_position()
                self.dragging = True
                return True
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.update_value_from_position(pos[0])
                self.update_handle_position()
                return True
        
        return False
    
    def draw(self, surface):
        """
        Draw slider
        
        Args:
            surface (pygame.Surface): Drawing surface
        """
        if not self.visible:
            return
        
        # Draw slider track background
        bg_color = self.bg_color
        if not self.enabled:
            bg_color = tuple(max(c - 50, 0) for c in self.bg_color)
        
        pygame.draw.rect(surface, bg_color, self.rect, 
                         border_radius=self.border_radius)
        
        # Draw selected portion
        selected_width = self.handle_x - self.x
        if selected_width > 0:
            selected_rect = pygame.Rect(self.x, self.y, selected_width, self.height)
            selected_color = self.highlight_color
            pygame.draw.rect(surface, selected_color, selected_rect, 
                             border_radius=self.border_radius)
        
        # Draw handle
        handle_color = (220, 220, 220) if self.enabled else (150, 150, 150)
        pygame.draw.rect(surface, handle_color, self.handle_rect, 
                         border_radius=self.border_radius)
        
        # Draw border
        pygame.draw.rect(surface, (100, 100, 100), self.rect, 
                         width=2, border_radius=self.border_radius)
        
        # Draw value
        if self.font is not None:
            try:
                # Re-render text
                self.rendered_text = self.font.render(self.text, True, self.text_color)
                self.text_rect = self.rendered_text.get_rect()
                self.text_rect.center = (self.x + self.width // 2, self.y + self.height // 2)
                surface.blit(self.rendered_text, self.text_rect)
            except Exception as e:
                print(f"Drawing slider text '{self.text}' failed: {e}")
