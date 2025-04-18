#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Poker Table Module

Provides rendering and layout functions for the poker table.
"""

import pygame
from src.utils.constants import TABLE_GREEN, WHITE, GOLD, BLACK
from src.utils.helpers import load_font, format_money


class PokerTable:
    """Poker Table Class"""
    
    def __init__(self, width, height):
        """
        Initialize poker table
        
        Args:
            width (int): Poker table width
            height (int): Poker table height
        """
        self.width = width
        self.height = height
        
        # Table position and size
        self.table_width = int(width * 0.8)
        self.table_height = int(height * 0.7)
        self.x = (width - self.table_width) // 2
        self.y = (height - self.table_height) // 2
        
        # Create table shape
        self.table_rect = pygame.Rect(self.x, self.y, self.table_width, self.table_height)
        
        # Poker table shape (ellipse)
        self.table_surface = pygame.Surface((self.table_width, self.table_height), pygame.SRCALPHA)
        self.felt_color = TABLE_GREEN
        self.border_color = (72, 43, 15)  # Wooden border color
        self.border_width = 20
        
        # Pot area
        self.pot_rect = pygame.Rect(
            self.table_width // 2 - 60,
            self.table_height // 2 - 30,
            120, 60
        )
        
        # Load table image
        try:
            self.table_image = None  # Replace with load_image when available
            # self.table_image = load_image("poker_table.png", 
            #                              (self.table_width, self.table_height),
            #                              convert_alpha=True)
        except:
            # Create default table
            self._create_default_table()
        
        # Create default table if no image was loaded
        if not hasattr(self, 'table_image') or self.table_image is None:
            self._create_default_table()
        
        # Player positions
        self.player_positions = self._calculate_player_positions()
        
        # Community card area
        self.community_card_positions = []
        card_width = 70  # Assume card width
        card_spacing = 10  # Spacing between cards
        total_width = 5 * card_width + 4 * card_spacing
        start_x = (self.table_width - total_width) // 2
        for i in range(5):
            self.community_card_positions.append(
                (start_x + i * (card_width + card_spacing), 
                 self.table_height // 2 - 50)
            )
        
        # Dealer button positions
        self.dealer_button_positions = self._calculate_dealer_positions()
    
    def _create_default_table(self):
        """Create default table image"""
        # Create transparent surface
        self.table_image = pygame.Surface((self.table_width, self.table_height), pygame.SRCALPHA)
        
        # Draw border ellipse
        pygame.draw.ellipse(self.table_image, self.border_color, 
                           (0, 0, self.table_width, self.table_height))
        
        # Draw table ellipse
        inner_rect = pygame.Rect(
            self.border_width, 
            self.border_width, 
            self.table_width - 2 * self.border_width, 
            self.table_height - 2 * self.border_width
        )
        pygame.draw.ellipse(self.table_image, self.felt_color, inner_rect)
        
        # Add decorations
        # Dots on outer border
        dots_count = 24
        for i in range(dots_count):
            angle = i * (360 / dots_count)
            radius = min(self.table_width, self.table_height) / 2 - 5
            import math
            x = self.table_width / 2 + radius * math.cos(math.radians(angle))
            y = self.table_height / 2 + radius * math.sin(math.radians(angle))
            pygame.draw.circle(self.table_image, GOLD, (int(x), int(y)), 3)
    
    def _calculate_player_positions(self):
        """Calculate player positions"""
        positions = [
            # Bottom center (human player)
            (self.table_width // 2, self.table_height - 20),
            # Bottom left
            (self.table_width // 4, self.table_height - 50),
            # Left
            (20, self.table_height // 2),
            # Top left
            (self.table_width // 4, 50),
            # Top center
            (self.table_width // 2, 20),
            # Top right
            (self.table_width * 3 // 4, 50),
            # Right
            (self.table_width - 20, self.table_height // 2),
            # Bottom right
            (self.table_width * 3 // 4, self.table_height - 50),
            # Bottom right offset (extra position)
            (self.table_width * 2 // 3, self.table_height - 35),
        ]
        return positions
    
    def _calculate_dealer_positions(self):
        """Calculate dealer button positions"""
        dealer_positions = []
        for pos in self.player_positions:
            # Dealer button position is slightly offset
            dealer_positions.append((pos[0] - 30, pos[1] - 15))
        return dealer_positions
    
    def get_player_position(self, index):
        """
        Get player position at specified index
        
        Args:
            index (int): Player index
        
        Returns:
            tuple: Position coordinates (x, y)
        """
        if 0 <= index < len(self.player_positions):
            return (self.x + self.player_positions[index][0], 
                    self.y + self.player_positions[index][1])
        return (self.x + self.table_width // 2, self.y + self.table_height // 2)
    
    def get_community_card_position(self, index):
        """
        Get community card position
        
        Args:
            index (int): Community card index (0-4)
        
        Returns:
            tuple: Position coordinates (x, y)
        """
        if 0 <= index < len(self.community_card_positions):
            return (self.x + self.community_card_positions[index][0], 
                    self.y + self.community_card_positions[index][1])
        return (self.x + self.table_width // 2, self.y + self.table_height // 2)
    
    def get_dealer_button_position(self, player_index):
        """
        Get dealer button position
        
        Args:
            player_index (int): Player index
        
        Returns:
            tuple: Position coordinates (x, y)
        """
        if 0 <= player_index < len(self.dealer_button_positions):
            return (self.x + self.dealer_button_positions[player_index][0], 
                    self.y + self.dealer_button_positions[player_index][1])
        return (0, 0)
    
    def draw(self, surface, game):
        """
        Draw poker table
        
        Args:
            surface (pygame.Surface): Drawing surface
            game (Game): Game instance
        """
        # Draw table
        surface.blit(self.table_image, (self.x, self.y))
        
        # Draw pot
        self._draw_pot(surface, game.pot)
        
        # Draw community cards
        for i, card in enumerate(game.community_cards):
            if i < 5:  # Display at most 5 community cards
                card_pos = self.get_community_card_position(i)
                card.set_position(card_pos)
                card.draw(surface)
        
        # Draw dealer button
        self._draw_dealer_button(surface, game.dealer_index)
        
        # Draw game state
        self._draw_game_state(surface, game.state)
        
        # Draw current bet
        if game.current_bet > 0:
            self._draw_current_bet(surface, game.current_bet)
    
    def _draw_pot(self, surface, pot):
        """
        Draw pot
        
        Args:
            surface (pygame.Surface): Drawing surface
            pot (int): Pot amount
        """
        if pot <= 0:
            return
        
        # Create pot surface
        pot_surface = pygame.Surface((120, 60), pygame.SRCALPHA)
        pygame.draw.rect(pot_surface, (0, 0, 0, 128), pot_surface.get_rect(), border_radius=10)
        
        # Draw pot text
        try:
            font = load_font(28)
            pot_text = font.render(f"Pot: {format_money(pot)}", True, WHITE)
            text_rect = pot_text.get_rect(center=(60, 30))
            pot_surface.blit(pot_text, text_rect)
        except Exception as e:
            print(f"Failed to render pot text: {e}")
            # Create a fallback indicator
            pygame.draw.rect(pot_surface, WHITE, pygame.Rect(20, 20, 80, 20))
        
        # Draw to main surface
        pot_rect = pot_surface.get_rect(center=(self.x + self.table_width // 2, 
                                                self.y + self.table_height // 2))
        surface.blit(pot_surface, pot_rect)
    
    def _draw_dealer_button(self, surface, dealer_index):
        """
        Draw dealer button
        
        Args:
            surface (pygame.Surface): Drawing surface
            dealer_index (int): Dealer player index
        """
        # Get dealer button position
        button_pos = self.get_dealer_button_position(dealer_index)
        
        # Draw dealer button
        pygame.draw.circle(surface, WHITE, button_pos, 15)
        pygame.draw.circle(surface, BLACK, button_pos, 15, 2)
        
        # Draw "D" text
        try:
            font = load_font(24)
            text = font.render("D", True, BLACK)
            text_rect = text.get_rect(center=button_pos)
            surface.blit(text, text_rect)
        except Exception as e:
            print(f"Failed to render dealer button text: {e}")
            # Draw a fallback indicator
            pygame.draw.line(surface, BLACK, 
                           (button_pos[0]-5, button_pos[0]-5),
                           (button_pos[0]+5, button_pos[0]+5), 3)
    
    def _draw_game_state(self, surface, state):
        """
        Draw game state
        
        Args:
            surface (pygame.Surface): Drawing surface
            state (str): Game state
        """
        # Create state surface
        state_surface = pygame.Surface((200, 40), pygame.SRCALPHA)
        pygame.draw.rect(state_surface, (0, 0, 0, 128), state_surface.get_rect(), border_radius=10)
        
        # Draw state text
        try:
            font = load_font(24)
            state_text = font.render(f"State: {state}", True, WHITE)
            text_rect = state_text.get_rect(center=(100, 20))
            state_surface.blit(state_text, text_rect)
        except Exception as e:
            print(f"Failed to render state text: {e}")
            # Create a fallback indicator
            pygame.draw.rect(state_surface, WHITE, pygame.Rect(20, 15, 160, 10))
        
        # Draw to main surface
        state_rect = state_surface.get_rect(topleft=(self.x + 20, self.y + 20))
        surface.blit(state_surface, state_rect)
    
    def _draw_current_bet(self, surface, current_bet):
        """
        Draw current bet
        
        Args:
            surface (pygame.Surface): Drawing surface
            current_bet (int): Current bet amount
        """
        # Create bet surface
        bet_surface = pygame.Surface((150, 40), pygame.SRCALPHA)
        pygame.draw.rect(bet_surface, (0, 0, 0, 128), bet_surface.get_rect(), border_radius=10)
        
        # Draw bet text
        try:
            font = load_font(24)
            bet_text = font.render(f"Bet: {format_money(current_bet)}", True, WHITE)
            text_rect = bet_text.get_rect(center=(75, 20))
            bet_surface.blit(bet_text, text_rect)
        except Exception as e:
            print(f"Failed to render bet text: {e}")
            # Create a fallback indicator
            pygame.draw.rect(bet_surface, WHITE, pygame.Rect(20, 15, 110, 10))
        
        # Draw to main surface
        bet_rect = bet_surface.get_rect(topright=(self.x + self.table_width - 20, self.y + 20))
        surface.blit(bet_surface, bet_rect)


class PlayerDisplay:
    """Player Display Class, used to display player information on the table"""
    
    def __init__(self, player, position, is_current=False):
        """
        Initialize player display
        
        Args:
            player (Player): Player object
            position (tuple): Display position
            is_current (bool, optional): Whether this is the current active player
        """
        self.player = player
        self.position = position
        self.is_current = is_current
        
        # Display size
        self.width = 180
        self.height = 100
        
        # Calculate display position
        self.x = position[0] - self.width // 2
        self.y = position[1] - self.height // 2
        
        # Card positions
        self.card_positions = [
            (self.x + 40, self.y + 50),
            (self.x + 80, self.y + 50)
        ]
        
        # Create display area
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Load avatar
        self.avatar = None
        self._load_avatar()
    
    def _load_avatar(self):
        """Load player avatar"""
        try:
            if self.player.is_human:
                self.avatar = None  # Replace with load_image when available
                # self.avatar = load_image("human_avatar.png", (40, 40), convert_alpha=True)
            else:
                self.avatar = None  # Replace with load_image when available
                # self.avatar = load_image("ai_avatar.png", (40, 40), convert_alpha=True)
        except:
            # Create default avatar
            self.avatar = pygame.Surface((40, 40), pygame.SRCALPHA)
            avatar_color = (0, 120, 200) if self.player.is_human else (200, 50, 50)
            pygame.draw.circle(self.avatar, avatar_color, (20, 20), 20)
            pygame.draw.circle(self.avatar, WHITE, (20, 20), 20, 2)
    
    def update(self, is_current=None):
        """
        Update display state
        
        Args:
            is_current (bool, optional): Whether this is the current active player
        """
        if is_current is not None:
            self.is_current = is_current
    
    def draw(self, surface):
        """
        Draw player display
        
        Args:
            surface (pygame.Surface): Drawing surface
        """
        # Create player display surface
        player_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Background color changes based on player status
        bg_color = (0, 0, 0, 180)
        if self.player.folded:
            bg_color = (100, 0, 0, 180)  # Folded
        elif self.player.all_in:
            bg_color = (0, 100, 100, 180)  # All-in
        elif self.is_current:
            bg_color = (0, 100, 0, 180)  # Current player
        
        # Draw background
        pygame.draw.rect(player_surface, bg_color, player_surface.get_rect(), border_radius=10)
        
        # If current player, add highlight border
        if self.is_current:
            pygame.draw.rect(player_surface, GOLD, player_surface.get_rect(), 
                            width=3, border_radius=10)
        
        # Draw player name
        try:
            font_name = load_font(20)
            name_text = font_name.render(self.player.name, True, WHITE)
            player_surface.blit(name_text, (10, 10))
        except Exception as e:
            print(f"Failed to render player name: {e}")
        
        # Draw chips
        try:
            font_chips = load_font(20)
            chips_text = font_chips.render(format_money(self.player.chips), True, GOLD)
            player_surface.blit(chips_text, (10, 30))
        except Exception as e:
            print(f"Failed to render player chips: {e}")
        
        # Draw bet amount
        if self.player.bet > 0:
            try:
                font_bet = load_font(18)
                bet_text = font_bet.render(f"Bet: {format_money(self.player.bet)}", True, WHITE)
                player_surface.blit(bet_text, (10, 50))
            except Exception as e:
                print(f"Failed to render player bet: {e}")
        
        # Draw special status
        status_text = ""
        if self.player.folded:
            status_text = "Folded"
        elif self.player.all_in:
            status_text = "All In"
        elif self.player.is_dealer:
            status_text = "Dealer"
        elif self.player.is_small_blind:
            status_text = "Small Blind"
        elif self.player.is_big_blind:
            status_text = "Big Blind"
        
        if status_text:
            try:
                font_status = load_font(18)
                status_surface = font_status.render(status_text, True, WHITE)
                player_surface.blit(status_surface, (10, 70))
            except Exception as e:
                print(f"Failed to render player status: {e}")
        
        # Draw avatar
        if self.avatar:
            player_surface.blit(self.avatar, (self.width - 50, 10))
        
        # Draw to main surface
        surface.blit(player_surface, (self.x, self.y))
        
        # Draw player's cards
        for i, card in enumerate(self.player.hole_cards):
            if i < 2:  # Only display two hole cards
                card.set_position(self.card_positions[i])
                card.draw(surface)
        
        # If at showdown stage, draw hand description
        if self.player.hand_description and not self.player.folded:
            self._draw_hand_description(surface)
    
    def _draw_hand_description(self, surface):
        """
        Draw hand description
        
        Args:
            surface (pygame.Surface): Drawing surface
        """
        # Create hand description surface
        desc_surface = pygame.Surface((160, 30), pygame.SRCALPHA)
        pygame.draw.rect(desc_surface, (0, 0, 0, 200), desc_surface.get_rect(), border_radius=5)
        
        # Draw description text
        try:
            font = load_font(18)
            desc_text = font.render(self.player.hand_description, True, WHITE)
            text_rect = desc_text.get_rect(center=(80, 15))
            desc_surface.blit(desc_text, text_rect)
        except Exception as e:
            print(f"Failed to render hand description: {e}")
            # Create a fallback indicator
            pygame.draw.rect(desc_surface, WHITE, pygame.Rect(20, 10, 120, 10))
        
        # Calculate display position (below player area)
        desc_x = self.x + (self.width - 160) // 2
        desc_y = self.y + self.height + 5
        
        # Draw to main surface
        surface.blit(desc_surface, (desc_x, desc_y))
