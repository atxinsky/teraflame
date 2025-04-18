#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Animation Effects Module

Provides various animation effects used in the game.
"""

import pygame
import math
import random


class Animation:
    """Base Animation Class"""
    
    def __init__(self, duration=1.0):
        """
        Initialize animation
        
        Args:
            duration (float, optional): Animation duration in seconds. Default is 1.0
        """
        self.duration = duration  # Duration in seconds
        self.elapsed = 0  # Elapsed time
        self.is_finished = False  # Whether animation is complete
        self.is_started = False  # Whether animation has started
    
    def start(self):
        """Start animation"""
        self.elapsed = 0
        self.is_finished = False
        self.is_started = True
    
    def update(self, dt):
        """
        Update animation
        
        Args:
            dt (float): Time increment in seconds
        
        Returns:
            bool: Whether animation is complete
        """
        if not self.is_started or self.is_finished:
            return self.is_finished
        
        self.elapsed += dt
        
        if self.elapsed >= self.duration:
            self.elapsed = self.duration
            self.is_finished = True
        
        # Subclasses should implement specific update logic
        self._update_animation(self.elapsed / self.duration)
        
        return self.is_finished
    
    def _update_animation(self, progress):
        """
        Update animation progress
        
        Args:
            progress (float): Animation progress (0.0 - 1.0)
        """
        # Subclasses should override this method
        pass
    
    def draw(self, surface):
        """
        Draw animation
        
        Args:
            surface (pygame.Surface): Drawing surface
        """
        # Subclasses should override this method
        pass
    
    def reset(self):
        """Reset animation"""
        self.elapsed = 0
        self.is_finished = False
        self.is_started = False


class CardDealAnimation(Animation):
    """Card Deal Animation"""
    
    def __init__(self, card, start_pos, end_pos, duration=0.3, flip_at=0.8):
        """
        Initialize card deal animation
        
        Args:
            card (Card): Card object
            start_pos (tuple): Start position (x, y)
            end_pos (tuple): End position (x, y)
            duration (float, optional): Animation duration in seconds
            flip_at (float, optional): When to flip the card in animation progress (0.0 - 1.0)
        """
        super().__init__(duration)
        self.card = card
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.flip_at = flip_at
        self.card_flipped = False
        
        # Ensure card initially faces down
        if self.card.face_up:
            self.card.flip()
    
    def _update_animation(self, progress):
        """Update card position and state"""
        # Calculate current position
        x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * progress
        y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * progress
        
        # Add a slight arc motion
        arch_height = 30
        arch_progress = math.sin(progress * math.pi)
        y -= arch_height * arch_progress
        
        # Set card position
        self.card.set_position((x, y))
        
        # Flip the card (if needed)
        if progress >= self.flip_at and not self.card_flipped and self.card.face_up == False:
            self.card.flip()
            self.card_flipped = True
    
    def draw(self, surface):
        """Draw card"""
        self.card.draw(surface)


class ChipsAnimation(Animation):
    """Chips Animation"""
    
    def __init__(self, start_pos, end_pos, amount, duration=0.5):
        """
        Initialize chips animation
        
        Args:
            start_pos (tuple): Start position (x, y)
            end_pos (tuple): End position (x, y)
            amount (int): Chip amount
            duration (float, optional): Animation duration in seconds
        """
        super().__init__(duration)
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.amount = amount
        
        # Create multiple chip sprites
        self.chips = []
        chip_count = min(10, max(3, amount // 10))  # Determine chip count based on amount
        
        # Colored chips: white($1), red($5), blue($10), green($25), black($100)
        colors = [(255, 255, 255), (255, 50, 50), (50, 50, 255), 
                 (50, 200, 50), (50, 50, 50)]
        
        for _ in range(chip_count):
            # Random offset from start position
            offset_x = random.randint(-10, 10)
            offset_y = random.randint(-10, 10)
            pos = (start_pos[0] + offset_x, start_pos[1] + offset_y)
            
            # Randomly select chip color
            color_idx = min(len(colors) - 1, int(math.log(amount / 10 + 1, 5)))
            color = colors[color_idx]
            
            # Create chip
            self.chips.append({
                'pos': pos,
                'color': color,
                'radius': random.randint(8, 12),
                'offset_x': offset_x,
                'offset_y': offset_y
            })
    
    def _update_animation(self, progress):
        """Update chip positions"""
        for chip in self.chips:
            # Use different easing curves to make each chip move slightly differently
            p = progress
            if chip['offset_x'] % 2 == 0:
                p = math.sin(progress * math.pi / 2)  # Different easing function
            else:
                p = 1 - (1 - progress) ** 2  # Different easing function
            
            # Calculate current position
            x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * p
            y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * p
            
            # Add random offset
            x += chip['offset_x'] * (1 - progress)
            y += chip['offset_y'] * (1 - progress)
            
            # Set chip position
            chip['pos'] = (x, y)
    
    def draw(self, surface):
        """Draw chips"""
        for chip in self.chips:
            pygame.draw.circle(surface, chip['color'], 
                               (int(chip['pos'][0]), int(chip['pos'][1])), 
                               chip['radius'])
            # Draw chip edge
            pygame.draw.circle(surface, (200, 200, 200), 
                               (int(chip['pos'][0]), int(chip['pos'][1])), 
                               chip['radius'], 1)


class TextAnimation(Animation):
    """Text Animation"""
    
    def __init__(self, text, pos, color=(255, 255, 255), font_size=36, 
                 duration=1.0, fade_out=True, rise=True, font_name=None):
        """
        Initialize text animation
        
        Args:
            text (str): Display text
            pos (tuple): Position (x, y)
            color (tuple, optional): Text color
            font_size (int, optional): Font size
            duration (float, optional): Animation duration in seconds
            fade_out (bool, optional): Whether to fade out
            rise (bool, optional): Whether to rise
            font_name (str, optional): Font name
        """
        super().__init__(duration)
        self.text = text
        self.pos = pos
        self.color = color
        self.font_size = font_size
        self.fade_out = fade_out
        self.rise = rise
        
        # Load font
        if font_name:
            try:
                self.font = pygame.font.Font(font_name, font_size)
            except:
                self.font = pygame.font.SysFont(None, font_size)
        else:
            self.font = pygame.font.SysFont(None, font_size)
        
        # Render initial text
        self.text_surface = self.font.render(text, True, color)
        self.text_rect = self.text_surface.get_rect(center=pos)
        
        # Current alpha
        self.alpha = 255
        
        # Current position
        self.current_pos = pos
    
    def _update_animation(self, progress):
        """Update text state"""
        # Update alpha
        if self.fade_out:
            # First fade in, then fade out
            if progress < 0.3:
                # Fade in stage
                self.alpha = int(255 * (progress / 0.3))
            else:
                # Fade out stage
                self.alpha = int(255 * (1 - (progress - 0.3) / 0.7))
        else:
            # Only fade in
            self.alpha = int(255 * min(1, progress * 2))
        
        # Update position
        if self.rise:
            rise_distance = 50  # Rise distance
            y_offset = rise_distance * progress
            self.current_pos = (self.pos[0], self.pos[1] - y_offset)
        
        # Update text rectangle
        self.text_rect.center = self.current_pos
    
    def draw(self, surface):
        """Draw text"""
        # Create transparent surface
        text_surface = self.text_surface.copy()
        
        # Set transparency
        if self.alpha < 255:
            text_surface.set_alpha(self.alpha)
        
        # Draw to main surface
        surface.blit(text_surface, self.text_rect)


class WinnerAnimation(Animation):
    """Winner Animation - Simplified version without complex particles"""
    
    def __init__(self, winner_rect, duration=2.0):
        """
        Initialize winner animation
        
        Args:
            winner_rect (pygame.Rect): Winner's area rectangle
            duration (float, optional): Animation duration in seconds
        """
        super().__init__(duration)
        self.rect = winner_rect
    
    def _update_animation(self, progress):
        """Update animation state"""
        # No internal state to update for this simplified version
        pass
    
    def draw(self, surface):
        """Draw winner highlight effect"""
        # Create a pulsing golden rectangle around the winner
        # Calculate pulsing effect
        pulse = (math.sin(self.elapsed * 10) + 1) / 2  # Pulse between 0-1
        
        # Draw outer glow with pulsing width
        glow_size = 10 + int(5 * pulse)  # Pulsing glow size
        glow_rect = pygame.Rect(
            self.rect.x - glow_size,
            self.rect.y - glow_size,
            self.rect.width + glow_size * 2,
            self.rect.height + glow_size * 2
        )
        
        # Create a golden border
        border_color = (255, 215, 0)  # Gold color
        pygame.draw.rect(surface, border_color, glow_rect, width=3, border_radius=10)
        
        # Draw simple stars effect (without complex particle physics)
        for i in range(5):
            # Position stars based on time and position
            angle = self.elapsed * (2 + i) + i * 0.5
            radius = 50 + 20 * math.sin(self.elapsed * 3 + i)
            
            star_x = int(self.rect.centerx + math.cos(angle) * radius)
            star_y = int(self.rect.centery + math.sin(angle) * radius)
            star_size = int(3 + 2 * math.sin(self.elapsed * 5 + i))
            
            # Only draw if on screen
            if 0 <= star_x < surface.get_width() and 0 <= star_y < surface.get_height():
                pygame.draw.circle(surface, border_color, (star_x, star_y), star_size)


class AnimationManager:
    """Animation Manager to manage multiple animations"""
    
    def __init__(self):
        """Initialize animation manager"""
        self.animations = []
        self.last_update_time = 0
    
    def add_animation(self, animation):
        """
        Add animation
        
        Args:
            animation (Animation): Animation object
        """
        animation.start()
        self.animations.append(animation)
    
    def update(self):
        """Update all animations"""
        # Calculate time increment
        current_time = pygame.time.get_ticks() / 1000  # Convert to seconds
        if self.last_update_time == 0:
            dt = 0
        else:
            dt = current_time - self.last_update_time
        
        self.last_update_time = current_time
        
        # Update animations and remove completed ones
        completed = []
        for anim in self.animations:
            if anim.update(dt):
                completed.append(anim)
        
        # Remove completed animations
        for anim in completed:
            if anim in self.animations:
                self.animations.remove(anim)
    
    def draw(self, surface):
        """
        Draw all animations
        
        Args:
            surface (pygame.Surface): Drawing surface
        """
        for anim in self.animations:
            anim.draw(surface)
    
    def clear(self):
        """Clear all animations"""
        self.animations.clear()
    
    def is_playing(self, animation_type=None):
        """
        Check if any animation is playing
        
        Args:
            animation_type (type, optional): Animation type; if None, check all types
        
        Returns:
            bool: Whether any animation is playing
        """
        if animation_type:
            return any(isinstance(anim, animation_type) for anim in self.animations)
        return len(self.animations) > 0
