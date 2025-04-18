#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Game Interface Module

Implements the user interface for Texas Hold'em Poker game.
"""

import pygame
from pygame.locals import *
import time

from src.ui.table import PokerTable, PlayerDisplay
from src.ui.button import Button, SliderButton
from src.ui.animation import (
    AnimationManager, CardDealAnimation, ChipsAnimation, 
    TextAnimation, WinnerAnimation
)
from src.utils.constants import (
    WHITE, BLACK, GREEN, GOLD, RED, BLUE, 
    WINDOW_WIDTH, WINDOW_HEIGHT, ACTIONS, GAME_STATES
)
from src.utils.helpers import format_money, load_font


class GameInterface:
    """Game Interface Class"""
    
    def __init__(self, screen, game):
        """
        Initialize the game interface
        
        Args:
            screen (pygame.Surface): Game window surface
            game (Game): Game logic instance
        """
        self.screen = screen
        self.game = game
        self.clock = pygame.time.Clock()
        
        # Initialize interface components
        self.table = PokerTable(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.player_displays = []
        self.buttons = []
        self.slider = None
        self.animation_manager = AnimationManager()
        
        # Game status display
        self.status_text = ""
        self.status_time = 0
        
        # Create player displays
        self.update_player_displays()
        
        # Create buttons
        self.create_action_buttons()
        self.create_game_buttons()
        
        # Create bet slider
        self.create_bet_slider()
        
        # Initial state
        self.last_state = game.state
        self.last_active_player = game.active_player_index
        self.update_buttons_state()
    
    def update_player_displays(self):
        """Update player displays"""
        self.player_displays = []
        
        # Create a display for each player
        for i, player in enumerate(self.game.players):
            position = self.table.get_player_position(i)
            is_current = (i == self.game.active_player_index)
            display = PlayerDisplay(player, position, is_current)
            self.player_displays.append(display)
    
    def create_action_buttons(self):
        """Create player action buttons"""
        # Button size and position
        button_width = 120
        button_height = 40
        spacing = 20
        start_x = WINDOW_WIDTH // 2 - (button_width * 2 + spacing * 1.5)
        y = WINDOW_HEIGHT - 80
        
        # Create buttons
        # Fold button
        self.fold_button = Button(
            start_x, y, button_width, button_height,
            "Fold", self.on_fold_click,
            bg_color=(150, 50, 50),
            highlight_color=(200, 70, 70)
        )
        
        # Check/Call button
        self.check_call_button = Button(
            start_x + button_width + spacing, y, button_width, button_height,
            "Check", self.on_check_call_click,
            bg_color=(50, 50, 150),
            highlight_color=(70, 70, 200)
        )
        
        # Raise button
        self.raise_button = Button(
            start_x + (button_width + spacing) * 2, y, button_width, button_height,
            "Raise", self.on_raise_click,
            bg_color=(50, 150, 50),
            highlight_color=(70, 200, 70)
        )
        
        # All-in button
        self.all_in_button = Button(
            start_x + (button_width + spacing) * 3, y, button_width, button_height,
            "All In", self.on_all_in_click,
            bg_color=(150, 100, 0),
            highlight_color=(200, 150, 0)
        )
        
        # Add to button list
        self.action_buttons = [
            self.fold_button,
            self.check_call_button,
            self.raise_button,
            self.all_in_button
        ]
        
        self.buttons.extend(self.action_buttons)
    
    def create_game_buttons(self):
        """Create game control buttons"""
        # New hand button
        self.new_hand_button = Button(
            WINDOW_WIDTH - 150, 10, 140, 40,
            "New Hand", self.on_new_hand_click,
            bg_color=(100, 150, 100),
            highlight_color=(120, 180, 120)
        )
        
        # Settings button
        self.settings_button = Button(
            WINDOW_WIDTH - 150, 60, 140, 40,
            "Settings", self.on_settings_click,
            bg_color=(100, 100, 150),
            highlight_color=(120, 120, 180)
        )
        
        # Help button
        self.help_button = Button(
            WINDOW_WIDTH - 150, 110, 140, 40,
            "Help", self.on_help_click,
            bg_color=(150, 100, 100),
            highlight_color=(180, 120, 120)
        )
        
        # Add to button list
        self.game_buttons = [
            self.new_hand_button,
            self.settings_button,
            self.help_button
        ]
        
        self.buttons.extend(self.game_buttons)
    
    def create_bet_slider(self):
        """Create bet slider"""
        # Slider size and position
        slider_width = 400
        slider_height = 30
        x = (WINDOW_WIDTH - slider_width) // 2
        y = WINDOW_HEIGHT - 140
        
        # Create slider
        min_value = self.game.current_bet + self.game.min_raise
        
        # Get current player
        human_player = self.game.human_player
        if human_player:
            max_value = human_player.chips
            initial_value = min(min_value, max_value)
            
            # Fix: Removed the 'text' parameter to avoid duplicate parameter error
            self.bet_slider = SliderButton(
                x, y, slider_width, slider_height,
                min_value, max_value, initial_value,
                self.on_slider_change,
                bg_color=(80, 80, 80),
                highlight_color=(120, 120, 120)
            )
            
            # Set the text after initialization
            self.bet_slider.set_text(format_money(initial_value))
    
    def update_buttons_state(self):
        """Update button states"""
        # Get current player
        active_player = self.game.get_active_player()
        human_player = self.game.human_player
        
        # If no current player or human player, disable all action buttons
        if not active_player or not human_player:
            for button in self.action_buttons:
                button.set_enabled(False)
            
            if self.bet_slider:
                self.bet_slider.set_enabled(False)
            
            # Set new hand button based on game state
            if self.game.state == GAME_STATES["END_HAND"] or self.game.state == GAME_STATES["WAITING"]:
                self.new_hand_button.set_enabled(True)
            else:
                self.new_hand_button.set_enabled(False)
            
            return
        
        # If current player is not human, disable all action buttons
        is_human_turn = active_player.id == human_player.id
        for button in self.action_buttons:
            button.set_enabled(is_human_turn and not self.animation_manager.is_playing())
        
        if self.bet_slider:
            self.bet_slider.set_enabled(is_human_turn and not self.animation_manager.is_playing())
        
        # Set new hand button based on game state
        if self.game.state == GAME_STATES["END_HAND"] or self.game.state == GAME_STATES["WAITING"]:
            self.new_hand_button.set_enabled(True)
        else:
            self.new_hand_button.set_enabled(False)
        
        # If not human player's turn, return directly
        if not is_human_turn:
            return
        
        # Update button text and enabled status based on current game state
        current_bet = self.game.current_bet
        player_bet = active_player.bet
        
        # Fold button is always available
        self.fold_button.set_enabled(True)
        
        # Check/Call button
        if current_bet == 0 or current_bet == player_bet:
            self.check_call_button.set_text("Check")
            self.check_call_button.set_enabled(True)
        elif current_bet > player_bet:
            call_amount = current_bet - player_bet
            if call_amount >= active_player.chips:
                # If call amount exceeds player chips, it's actually all-in
                self.check_call_button.set_text(f"All In {format_money(active_player.chips)}")
            else:
                self.check_call_button.set_text(f"Call {format_money(call_amount)}")
            self.check_call_button.set_enabled(True)
        else:
            self.check_call_button.set_enabled(False)
        
        # Raise button
        min_raise = current_bet + self.game.min_raise
        remaining_chips = active_player.chips - (current_bet - player_bet)
        
        if remaining_chips > self.game.min_raise:
            self.raise_button.set_text("Raise")
            self.raise_button.set_enabled(True)
            
            # Update slider
            min_slider = min_raise
            max_slider = active_player.chips + player_bet
            
            if self.bet_slider:
                # Set new min and max values
                self.bet_slider.min_value = min_slider
                self.bet_slider.max_value = max_slider
                
                # If current value is not in new range, adjust it
                if self.bet_slider.value < min_slider:
                    self.bet_slider.value = min_slider
                elif self.bet_slider.value > max_slider:
                    self.bet_slider.value = max_slider
                
                # Update slider text and position
                self.bet_slider.set_text(format_money(self.bet_slider.value))
                self.bet_slider.update_handle_position()
                self.bet_slider.set_enabled(True)
        else:
            self.raise_button.set_enabled(False)
            if self.bet_slider:
                self.bet_slider.set_enabled(False)
        
        # All-in button
        if active_player.chips > 0:
            self.all_in_button.set_text(f"All In {format_money(active_player.chips)}")
            self.all_in_button.set_enabled(True)
        else:
            self.all_in_button.set_enabled(False)
    
    def handle_event(self, event):
        """
        Handle events
        
        Args:
            event (pygame.event.Event): Pygame event
        """
        # If animation is playing, ignore most events
        if self.animation_manager.is_playing():
            # Still handle button clicks, but only for specific buttons
            if event.type == MOUSEBUTTONDOWN:
                # Check if game control buttons are clicked
                for button in self.game_buttons:
                    if button.handle_event(event):
                        break
            return
        
        # Handle button clicks
        if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP:
            # Check if any button is clicked
            for button in self.buttons:
                if button.handle_event(event):
                    break
            
            # Handle slider
            if self.bet_slider and self.bet_slider.handle_event(event):
                pass
    
    def render(self):
        """Render game interface"""
        # Clear screen
        self.screen.fill((40, 40, 40))
        
        # Draw poker table
        self.table.draw(self.screen, self.game)
        
        # Draw players
        for i, display in enumerate(self.player_displays):
            # Update current player status
            display.update(i == self.game.active_player_index)
            display.draw(self.screen)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)
        
        # Draw slider
        if self.bet_slider:
            self.bet_slider.draw(self.screen)
        
        # Draw status information
        self.draw_status()
        
        # Draw animations
        self.animation_manager.draw(self.screen)
        
        # Update animations
        self.animation_manager.update()
        
        # Check game state changes
        self.check_state_changes()
    
    def draw_status(self):
        """Draw status information"""
        # If there is status information and it's not timed out, display it
        current_time = time.time()
        if self.status_text and current_time - self.status_time < 3:
            # Create status surface
            try:
                font = load_font(28)
                text = font.render(self.status_text, True, WHITE)
                
                # Draw background
                padding = 10
                rect = pygame.Rect(
                    (WINDOW_WIDTH - text.get_width()) // 2 - padding,
                    200 - padding,
                    text.get_width() + padding * 2,
                    text.get_height() + padding * 2
                )
                
                background = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                pygame.draw.rect(background, (0, 0, 0, 180), background.get_rect(), border_radius=10)
                self.screen.blit(background, rect)
                
                # Draw text
                self.screen.blit(text, ((WINDOW_WIDTH - text.get_width()) // 2, 200))
            except Exception as e:
                print(f"Failed to draw status text: {e}")
    
    def set_status(self, text):
        """
        Set status information
        
        Args:
            text (str): Status text
        """
        self.status_text = text
        self.status_time = time.time()
    
    def check_state_changes(self):
        """Check game state changes and respond"""
        # Check if game state has changed
        if self.game.state != self.last_state:
            self.on_state_change()
            self.last_state = self.game.state
        
        # Check if current player has changed
        if self.game.active_player_index != self.last_active_player:
            self.on_active_player_change()
            self.last_active_player = self.game.active_player_index
        
        # Update button states
        self.update_buttons_state()
    
    def on_state_change(self):
        """Respond to game state changes"""
        # Execute actions based on new state
        if self.game.state == GAME_STATES["FLOP"]:
            # Flop
            self.set_status("Flop")
            self.animate_community_cards(0, 3)
        
        elif self.game.state == GAME_STATES["TURN"]:
            # Turn
            self.set_status("Turn")
            self.animate_community_cards(3, 4)
        
        elif self.game.state == GAME_STATES["RIVER"]:
            # River
            self.set_status("River")
            self.animate_community_cards(4, 5)
        
        elif self.game.state == GAME_STATES["SHOWDOWN"]:
            # Showdown
            self.set_status("Showdown")
            self.animate_showdown()
        
        elif self.game.state == GAME_STATES["END_HAND"]:
            # Game end
            if self.game.last_winner:
                self.set_status(f"Winner: {self.game.last_winner.name} - {self.game.last_winning_hand}")
                self.animate_winner(self.game.last_winner)
            else:
                self.set_status(f"Tie - {self.game.last_winning_hand}")
    
    def on_active_player_change(self):
        """Respond to current player change"""
        active_player = self.game.get_active_player()
        if active_player:
            self.set_status(f"{active_player.name}'s turn")
    
    def animate_community_cards(self, start_index, end_index):
        """
        Animate community cards display
        
        Args:
            start_index (int): Start index
            end_index (int): End index
        """
        # Get community cards
        for i in range(start_index, end_index):
            if i < len(self.game.community_cards):
                card = self.game.community_cards[i]
                
                # Set start and end positions
                # Start position is table center
                start_pos = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
                end_pos = self.table.get_community_card_position(i)
                
                # Create animation
                animation = CardDealAnimation(card, start_pos, end_pos, duration=0.5)
                self.animation_manager.add_animation(animation)
    
    def animate_showdown(self):
        """Animate showdown"""
        # Flip all players' cards
        for i, player in enumerate(self.game.players):
            if not player.folded:
                for j, card in enumerate(player.hole_cards):
                    if not card.face_up:
                        # Create card flip animation
                        animation = CardDealAnimation(
                            card, card.position, card.position, 
                            duration=0.3, flip_at=0.5
                        )
                        self.animation_manager.add_animation(animation)
    
    def animate_winner(self, winner):
        """
        Animate winner
        
        Args:
            winner (Player): Winner player object
        """
        # Find winner's display
        winner_index = self.game.players.index(winner)
        if 0 <= winner_index < len(self.player_displays):
            winner_display = self.player_displays[winner_index]
            
            # Create winner animation
            animation = WinnerAnimation(winner_display.rect, duration=3.0)
            self.animation_manager.add_animation(animation)
            
            # Create text animation
            text = f"Won {format_money(self.game.pot)}!"
            text_animation = TextAnimation(
                text, 
                (winner_display.position[0], winner_display.position[1] - 40),
                color=GOLD, font_size=24, duration=2.0
            )
            self.animation_manager.add_animation(text_animation)
            
            # Create chips movement animation
            pot_pos = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
            chips_animation = ChipsAnimation(
                pot_pos, winner_display.position, self.game.pot, duration=1.0
            )
            self.animation_manager.add_animation(chips_animation)
    
    # Button click handler functions
    def on_fold_click(self):
        """Handle fold button click"""
        active_player_index = self.game.active_player_index
        if self.game.process_player_action(active_player_index, "FOLD"):
            self.set_status(f"{self.game.players[active_player_index].name} folds")
    
    def on_check_call_click(self):
        """Handle check/call button click"""
        active_player_index = self.game.active_player_index
        active_player = self.game.players[active_player_index]
        current_bet = self.game.current_bet
        
        if current_bet == 0 or current_bet == active_player.bet:
            # Check
            if self.game.process_player_action(active_player_index, "CHECK"):
                self.set_status(f"{active_player.name} checks")
        else:
            # Call
            if self.game.process_player_action(active_player_index, "CALL"):
                call_amount = current_bet - active_player.bet
                if active_player.all_in:
                    self.set_status(f"{active_player.name} is all in with {format_money(active_player.chips)}")
                else:
                    self.set_status(f"{active_player.name} calls {format_money(call_amount)}")
    
    def on_raise_click(self):
        """Handle raise button click"""
        active_player_index = self.game.active_player_index
        active_player = self.game.players[active_player_index]
        
        # Get slider value as raise amount
        if self.bet_slider:
            raise_amount = self.bet_slider.value - active_player.bet
            if self.game.process_player_action(active_player_index, "RAISE", raise_amount):
                self.set_status(f"{active_player.name} raises to {format_money(self.bet_slider.value)}")
    
    def on_all_in_click(self):
        """Handle all-in button click"""
        active_player_index = self.game.active_player_index
        active_player = self.game.players[active_player_index]
        
        if self.game.process_player_action(active_player_index, "ALL_IN"):
            self.set_status(f"{active_player.name} is all in with {format_money(active_player.chips)}")
    
    def on_new_hand_click(self):
        """Handle new hand button click"""
        if self.game.state == GAME_STATES["END_HAND"] or self.game.state == GAME_STATES["WAITING"]:
            self.game.start_new_hand()
            self.update_player_displays()
            self.set_status("New hand starts")
            
            # Animate dealing hole cards
            self.animate_deal_hole_cards()
    
    def on_settings_click(self):
        """Handle settings button click"""
        self.set_status("Settings feature not implemented yet")
    
    def on_help_click(self):
        """Handle help button click"""
        self.set_status("Help feature not implemented yet")
    
    def on_slider_change(self, value):
        """
        Handle slider value change
        
        Args:
            value (int): New slider value
        """
        # Display slider value as money amount
        self.bet_slider.set_text(format_money(value))
    
    def animate_deal_hole_cards(self):
        """Animate dealing hole cards"""
        # Calculate deck position (table center)
        deck_pos = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        
        # Create deal animation for each player's cards
        for i, player in enumerate(self.game.players):
            for j, card in enumerate(player.hole_cards):
                # Calculate target position
                display = self.player_displays[i]
                target_x = display.card_positions[j][0]
                target_y = display.card_positions[j][1]
                
                # Create animation
                animation = CardDealAnimation(
                    card, deck_pos, (target_x, target_y), 
                    duration=0.3 + i * 0.05, 
                    flip_at=1.0 if player.is_human else 2.0
                )
                self.animation_manager.add_animation(animation)
