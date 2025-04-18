#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Game Logic Module

Implements the core logic of Texas Hold'em Poker game.
"""

import random
from collections import deque
from src.game.deck import Deck
from src.game.player import Player
from src.game.hand import HandEvaluator, get_hand_description
from src.game.ai import PokerAI
from src.utils.constants import (
    SMALL_BLIND, BIG_BLIND, MIN_PLAYERS, MAX_PLAYERS, DEFAULT_PLAYERS,
    GAME_STATES, ACTIONS, AI_DIFFICULTIES, INITIAL_PLAYER_CHIPS
)


class Game:
    """Texas Hold'em Poker Game Class"""
    
    def __init__(self):
        """Initialize game"""
        # Game components
        self.deck = Deck()
        self.players = []
        self.human_player = None
        self.hand_evaluator = HandEvaluator()
        self.ai_controller = {}  # Mapping from player ID to AI controller
        
        # Game state
        self.state = GAME_STATES["WAITING"]
        self.active_player_index = 0
        self.dealer_index = 0
        self.community_cards = []
        self.pot = 0
        self.side_pots = []
        self.current_bet = 0
        self.min_raise = BIG_BLIND
        self.last_raise_index = -1
        
        # Game settings
        self.small_blind = SMALL_BLIND
        self.big_blind = BIG_BLIND
        
        # Game statistics
        self.hand_number = 0
        self.last_winner = None
        self.last_winning_hand = None
        
        # Initialize AI players
        self.init_default_game()
    
    def init_default_game(self):
        """Initialize default game settings"""
        # Add human player
        self.add_human_player("Player", INITIAL_PLAYER_CHIPS)
        
        # Add AI players
        self.add_ai_players(DEFAULT_PLAYERS - 1)
        
        # Initialize table positions
        self.init_positions()
    
    def add_human_player(self, name, chips=INITIAL_PLAYER_CHIPS):
        """
        Add human player
        
        Args:
            name (str): Player name
            chips (int, optional): Initial chips
        
        Returns:
            Player: Created player object
        """
        # Check if there's already a human player
        if self.human_player:
            return self.human_player
        
        # Create new human player
        player = Player(name, is_human=True, chips=chips)
        self.players.append(player)
        self.human_player = player
        
        return player
    
    def add_ai_player(self, name=None, difficulty="MEDIUM", chips=INITIAL_PLAYER_CHIPS):
        """
        Add AI player
        
        Args:
            name (str, optional): Player name. If None, generated automatically
            difficulty (str, optional): AI difficulty
            chips (int, optional): Initial chips
        
        Returns:
            Player: Created player object
        """
        if len(self.players) >= MAX_PLAYERS:
            raise ValueError(f"Maximum number of players reached ({MAX_PLAYERS})")
        
        # Generate AI name
        if name is None:
            ai_names = [
                "Alex", "Bob", "Charlie", "David", "Emma", "Frank", "Grace", "Henry",
                "Isabel", "Jack", "Karen", "Leo", "Mia", "Nathan", "Olivia"
            ]
            used_names = [p.name for p in self.players]
            available_names = [n for n in ai_names if n not in used_names]
            
            if available_names:
                name = random.choice(available_names)
            else:
                name = f"AI-{len(self.players) + 1}"
        
        # Create AI player
        player = Player(name, is_human=False, ai_difficulty=difficulty, chips=chips)
        self.players.append(player)
        
        # Create AI controller
        self.ai_controller[player.id] = PokerAI(difficulty)
        
        return player
    
    def add_ai_players(self, count, difficulty="MEDIUM"):
        """
        Add multiple AI players
        
        Args:
            count (int): Number of AI players to add
            difficulty (str, optional): AI difficulty
        """
        for _ in range(count):
            try:
                self.add_ai_player(difficulty=difficulty)
            except ValueError:
                break  # Maximum players reached
    
    def remove_player(self, player_id):
        """
        Remove player
        
        Args:
            player_id (str): ID of player to remove
        
        Returns:
            bool: Whether successfully removed
        """
        for i, player in enumerate(self.players):
            if player.id == player_id:
                # Clean up AI controller
                if player.id in self.ai_controller:
                    del self.ai_controller[player.id]
                
                # Remove player
                self.players.pop(i)
                
                # If human player, clear reference
                if player == self.human_player:
                    self.human_player = None
                
                # Adjust indices
                if self.dealer_index >= len(self.players):
                    self.dealer_index = 0
                if self.active_player_index >= len(self.players):
                    self.active_player_index = 0
                
                return True
        
        return False
    
    def init_positions(self):
        """Initialize player positions on the table"""
        # This method will calculate the position of each player on the interface
        # Typically, the human player is at the bottom center, other players arranged around the table
        
        # For simplicity, we use a predefined position list
        # In actual application, positions should be calculated based on window size
        
        # Assume window size 1024x768
        window_width = 1024
        window_height = 768
        
        # Table center position
        center_x = window_width // 2
        center_y = window_height // 2
        
        # Table radius
        radius = min(center_x, center_y) - 100
        
        # Human player position at bottom center
        human_position = (center_x, center_y + radius - 50)
        
        # Assign positions for each player
        positions = []
        player_count = len(self.players)
        
        # Generate positions
        if player_count <= 2:
            positions = [
                (center_x, center_y + radius - 50),  # Bottom center (human)
                (center_x, center_y - radius + 50),  # Top center
            ]
        elif player_count <= 4:
            positions = [
                (center_x, center_y + radius - 50),  # Bottom center (human)
                (center_x - radius + 50, center_y),  # Left
                (center_x, center_y - radius + 50),  # Top center
                (center_x + radius - 50, center_y),  # Right
            ]
        elif player_count <= 6:
            positions = [
                (center_x, center_y + radius - 50),  # Bottom center (human)
                (center_x - radius + 50, center_y + radius // 2),  # Bottom left
                (center_x - radius + 50, center_y - radius // 2),  # Top left
                (center_x, center_y - radius + 50),  # Top center
                (center_x + radius - 50, center_y - radius // 2),  # Top right
                (center_x + radius - 50, center_y + radius // 2),  # Bottom right
            ]
        else:
            # For simplicity, we only handle up to 6 players
            # In practice, should handle up to 9 players
            positions = [
                (center_x, center_y + radius - 50),  # Bottom center (human)
                (center_x - radius // 2, center_y + radius // 2),  # Bottom left
                (center_x - radius + 50, center_y),  # Left
                (center_x - radius // 2, center_y - radius // 2),  # Top left
                (center_x, center_y - radius + 50),  # Top center
                (center_x + radius // 2, center_y - radius // 2),  # Top right
                (center_x + radius - 50, center_y),  # Right
                (center_x + radius // 2, center_y + radius // 2),  # Bottom right
                (center_x, center_y + radius // 2),  # Bottom radius
            ]
        
        # Assign positions
        # Ensure human player is at bottom center
        human_index = -1
        for i, player in enumerate(self.players):
            if player.is_human:
                human_index = i
                break
        
        if human_index != -1 and human_index != 0:
            # Swap human player with first position player
            self.players[0], self.players[human_index] = self.players[human_index], self.players[0]
        
        # Set positions
        for i, player in enumerate(self.players):
            if i < len(positions):
                player.position = positions[i]
    
    def start_new_hand(self):
        """Start a new hand"""
        # Check player count
        if len(self.players) < MIN_PLAYERS:
            raise ValueError(f"At least {MIN_PLAYERS} players needed to start the game")
        
        # Reset hand state
        self.community_cards = []
        self.pot = 0
        self.side_pots = []
        self.current_bet = 0
        self.min_raise = self.big_blind
        self.last_raise_index = -1
        
        # Increase hand count
        self.hand_number += 1
        
        # Shuffle deck
        self.deck.reset()
        self.deck.shuffle()
        
        # Remove eliminated players (zero chips)
        self.players = [p for p in self.players if p.chips > 0]
        
        # Reset player states
        for player in self.players:
            player.reset_for_new_hand()
        
        # Determine dealer position (rotate)
        if self.dealer_index >= len(self.players):
            self.dealer_index = 0
        
        # Assign dealer, small blind, and big blind positions
        self.set_dealer_and_blinds()
        
        # Deal hole cards (two to each player)
        self.deal_hole_cards()
        
        # Set state to pre-flop
        self.state = GAME_STATES["PRE_FLOP"]
        
        # Set active player to the one after big blind
        self.active_player_index = (self.dealer_index + 3) % len(self.players)
        if len(self.players) == 2:  # Special case for two players
            self.active_player_index = self.dealer_index
    
    def set_dealer_and_blinds(self):
        """Set dealer and blind positions"""
        # Mark dealer
        self.players[self.dealer_index].is_dealer = True
        
        # Set small blind position
        small_blind_index = (self.dealer_index + 1) % len(self.players)
        self.players[small_blind_index].is_small_blind = True
        
        # Set big blind position
        big_blind_index = (self.dealer_index + 2) % len(self.players)
        self.players[big_blind_index].is_big_blind = True
        
        # Collect blinds
        self.players[small_blind_index].place_bet(self.small_blind)
        self.pot += self.small_blind
        
        self.players[big_blind_index].place_bet(self.big_blind)
        self.pot += self.big_blind
        
        # Set current highest bet as big blind
        self.current_bet = self.big_blind
    
    def deal_hole_cards(self):
        """Deal hole cards"""
        # Deal two cards to each player
        for player in self.players:
            for _ in range(2):
                card = self.deck.deal_one(face_up=player.is_human)
                player.receive_card(card)
    
    def deal_flop(self):
        """Deal flop"""
        # Burn one card first
        self.deck.burn()
        
        # Deal three flop cards
        for _ in range(3):
            card = self.deck.deal_one(face_up=True)
            self.community_cards.append(card)
        
        # Update state
        self.state = GAME_STATES["FLOP"]
        self.reset_betting_round()
    
    def deal_turn(self):
        """Deal turn"""
        # Burn one card
        self.deck.burn()
        
        # Deal one turn card
        card = self.deck.deal_one(face_up=True)
        self.community_cards.append(card)
        
        # Update state
        self.state = GAME_STATES["TURN"]
        self.reset_betting_round()
    
    def deal_river(self):
        """Deal river"""
        # Burn one card
        self.deck.burn()
        
        # Deal one river card
        card = self.deck.deal_one(face_up=True)
        self.community_cards.append(card)
        
        # Update state
        self.state = GAME_STATES["RIVER"]
        self.reset_betting_round()
    
    def reset_betting_round(self):
        """Reset betting round"""
        # Reset current bet and minimum raise
        self.current_bet = 0
        self.min_raise = self.big_blind
        
        # Reset all players' current bets
        for player in self.players:
            player.bet = 0
        
        # Set active player to first non-folded player after dealer
        self.active_player_index = (self.dealer_index + 1) % len(self.players)
        self.find_next_active_player()
        
        # Reset last raise index
        self.last_raise_index = -1
    
    def find_next_active_player(self):
        """Find next active (not folded and not all-in) player"""
        start_index = self.active_player_index
        index = (start_index + 1) % len(self.players)
        
        while index != start_index:
            player = self.players[index]
            if not player.folded and not player.all_in and player.chips > 0:
                self.active_player_index = index
                return True
            
            index = (index + 1) % len(self.players)
        
        # If looped back to start, check start player
        player = self.players[start_index]
        if not player.folded and not player.all_in and player.chips > 0:
            return True
        
        # No active player found
        return False
    
    def is_betting_round_complete(self):
        """Check if current betting round is complete"""
        # Count active players
        active_count = sum(1 for p in self.players if not p.folded and not p.all_in)
        
        # If only one or zero active players, betting round ends
        if active_count <= 1:
            return True
        
        # Check if all active players' bets are equal and everyone had a chance to act
        last_raise = self.last_raise_index
        current_index = self.active_player_index
        
        # If no one raised, and at least one full rotation
        if last_raise == -1:
            # Need to confirm if everyone has acted
            # Simplification: If back to position after big blind, rotation is complete
            big_blind_index = (self.dealer_index + 2) % len(self.players)
            next_index = (big_blind_index + 1) % len(self.players)
            
            # If not pre-flop, start from first position after dealer
            if self.state != GAME_STATES["PRE_FLOP"]:
                next_index = (self.dealer_index + 1) % len(self.players)
            
            # If current player index has returned to or passed the starting position, rotation complete
            if self.is_position_after_or_equal(current_index, next_index):
                return True
            
            return False
        
        # Check if all bets are equal
        expected_bet = self.current_bet
        for player in self.players:
            if player.folded or player.all_in:
                continue
            
            if player.bet != expected_bet:
                return False
        
        # Check if everyone had a chance to act after the last raise
        if last_raise != -1:
            # If current player index has returned to or passed the last raiser, rotation complete
            if self.is_position_after_or_equal(current_index, last_raise):
                return True
            
            return False
        
        return True
    
    def is_position_after_or_equal(self, current_index, target_index):
        """
        Check if current position is after or equal to target position
        Handles wrap-around cases
        """
        if current_index == target_index:
            return True
        
        # Traverse from target_index to current_index
        index = target_index
        while True:
            index = (index + 1) % len(self.players)
            if index == current_index:
                return True
            if index == target_index:
                break
        
        return False
    
    def process_player_action(self, player_index, action_type, amount=0):
        """
        Process player action
        
        Args:
            player_index (int): Player index
            action_type (str): Action type (FOLD, CHECK, CALL, RAISE, ALL_IN)
            amount (int, optional): Bet amount
        
        Returns:
            bool: Whether action is valid
        """
        if player_index != self.active_player_index:
            return False
        
        player = self.players[player_index]
        
        # Validate action type
        if action_type not in ACTIONS:
            return False
        
        # Handle different types of actions
        if action_type == "FOLD":
            player.fold()
        
        elif action_type == "CHECK":
            # Check if player can check
            if self.current_bet > player.bet:
                return False
            # No additional operation needed for check
        
        elif action_type == "CALL":
            # Calculate call amount
            call_amount = self.current_bet - player.bet
            
            # If player doesn't have enough chips, go all-in
            if call_amount >= player.chips:
                action_type = "ALL_IN"
                player.place_bet(player.chips)
                self.pot += player.chips
            else:
                player.place_bet(call_amount)
                self.pot += call_amount
        
        elif action_type == "RAISE":
            # Check if raise amount is legal
            if amount <= 0:
                return False
            
            # Calculate actual raise (considering already bet amount)
            additional_bet = amount
            total_bet = player.bet + additional_bet
            
            # Verify if it meets minimum raise requirement
            if total_bet < self.current_bet + self.min_raise and total_bet < player.chips:
                return False
            
            # If all-in but amount less than minimum raise, still allow
            if additional_bet >= player.chips:
                action_type = "ALL_IN"
                actual_bet = player.place_bet(player.chips)
            else:
                actual_bet = player.place_bet(additional_bet)
            
            # Update current highest bet and minimum raise
            raise_amount = total_bet - self.current_bet
            if total_bet > self.current_bet and not player.all_in:
                self.min_raise = max(self.min_raise, raise_amount)
                self.last_raise_index = player_index
            
            self.current_bet = max(self.current_bet, total_bet)
            self.pot += actual_bet
        
        elif action_type == "ALL_IN":
            # All-in
            actual_bet = player.place_bet(player.chips)
            
            # Update current highest bet and minimum raise
            total_bet = player.bet
            if total_bet > self.current_bet:
                raise_amount = total_bet - self.current_bet
                self.min_raise = max(self.min_raise, raise_amount)
                self.current_bet = total_bet
                self.last_raise_index = player_index
            
            self.pot += actual_bet
        
        # Move to next player
        if not self.find_next_active_player():
            # If no next active player, end current betting round
            return self.end_betting_round()
        
        return True
    
    def process_ai_actions(self):
        """Process AI player actions"""
        # If current active player is AI
        if self.active_player_index < len(self.players):
            player = self.players[self.active_player_index]
            
            if not player.is_human and not player.folded and not player.all_in:
                # Get AI controller
                ai = self.ai_controller.get(player.id)
                if ai:
                    # Prepare game state information
                    game_state = self.get_game_state_for_ai(player)
                    
                    # Get AI decision
                    action, amount = ai.make_decision(player, game_state)
                    
                    # Execute decision
                    self.process_player_action(self.active_player_index, action, amount)
    
    def get_game_state_for_ai(self, player):
        """
        Prepare game state information for AI
        
        Args:
            player (Player): AI player
        
        Returns:
            dict: Game state information
        """
        # Determine position (early, middle, late)
        positions = ["EARLY", "MIDDLE", "LATE"]
        relative_position = self.get_player_relative_position(player)
        position = positions[min(2, relative_position)]
        
        # Calculate remaining players
        players_remaining = sum(1 for p in self.players if not p.folded)
        
        # Prepare game state
        return {
            "round": self.state,
            "pot": self.pot,
            "current_bet": self.current_bet,
            "min_raise": self.min_raise,
            "community_cards": self.community_cards.copy(),
            "position": position,
            "players_remaining": players_remaining,
            "hand_number": self.hand_number
        }
    
    def get_player_relative_position(self, player):
        """
        Get player's position relative to dealer
        0 = early, 1 = middle, 2 = late
        """
        player_index = self.players.index(player)
        
        # Calculate relative position
        relative_pos = (player_index - self.dealer_index) % len(self.players)
        
        # Divide positions based on player count
        player_count = len(self.players)
        if player_count <= 3:
            # 2-3 player table
            return relative_pos  # 0=early, 1=middle, 2=late
        elif player_count <= 6:
            # 4-6 player table
            if relative_pos < player_count // 3:
                return 0  # Early
            elif relative_pos < 2 * (player_count // 3):
                return 1  # Middle
            else:
                return 2  # Late
        else:
            # 7-9 player table
            if relative_pos < player_count // 3:
                return 0  # Early
            elif relative_pos < 2 * (player_count // 3):
                return 1  # Middle
            else:
                return 2  # Late
    
    def end_betting_round(self):
        """End current betting round and enter next stage"""
        # Determine next step based on current game state
        if self.state == GAME_STATES["PRE_FLOP"]:
            # Pre-flop -> Flop
            self.deal_flop()
        elif self.state == GAME_STATES["FLOP"]:
            # Flop -> Turn
            self.deal_turn()
        elif self.state == GAME_STATES["TURN"]:
            # Turn -> River
            self.deal_river()
        elif self.state == GAME_STATES["RIVER"]:
            # River -> Showdown/End
            self.showdown()
        
        return True
    
    def showdown(self):
        """Showdown stage, determine winner"""
        # Update game state
        self.state = GAME_STATES["SHOWDOWN"]
        
        # Show all players' cards
        for player in self.players:
            if not player.folded:
                for card in player.hole_cards:
                    card.face_up = True
        
        # Evaluate all players' hands
        for player in self.players:
            if not player.folded:
                player.evaluate_hand(self.community_cards, self.hand_evaluator)
        
        # Find winners
        winners = self.determine_winners()
        
        # Distribute pot
        self.distribute_pot(winners)
        
        # Update game state to end
        self.state = GAME_STATES["END_HAND"]
        
        # Prepare for next hand
        # Move dealer position
        self.dealer_index = (self.dealer_index + 1) % len(self.players)
        
        # Delay start of new hand (controlled externally)
    
    def determine_winners(self):
        """
        Determine winners
        
        Returns:
            list: List of winners, each element is (player, won chips)
        """
        # If only one player hasn't folded, they're the winner
        active_players = [p for p in self.players if not p.folded]
        if len(active_players) == 1:
            winner = active_players[0]
            self.last_winner = winner
            self.last_winning_hand = winner.hand_description
            return [(winner, self.pot)]
        
        # Otherwise, compare hand strength
        # Sort players by hand strength (high to low)
        sorted_players = sorted(
            active_players,
            key=lambda p: (p.hand_strength, p.hand_type),
            reverse=True
        )
        
        # Find players with same hand strength (ties)
        winners = [sorted_players[0]]
        highest_strength = sorted_players[0].hand_strength
        highest_type = sorted_players[0].hand_type
        
        for player in sorted_players[1:]:
            if player.hand_strength == highest_strength and player.hand_type == highest_type:
                winners.append(player)
            else:
                break
        
        # Record last winner information
        if len(winners) == 1:
            self.last_winner = winners[0]
            self.last_winning_hand = winners[0].hand_description
        else:
            self.last_winner = None
            self.last_winning_hand = f"{len(winners)} way tie, {winners[0].hand_description}"
        
        # Return winners and distribution amounts
        return [(winner, self.pot // len(winners)) for winner in winners]
    
    def distribute_pot(self, winners):
        """
        Distribute pot to winners
        
        Args:
            winners (list): List of winners, each element is (player, won chips)
        """
        for player, amount in winners:
            player.collect_winnings(amount)
        
        # Handle possible remainder (due to integer division)
        remainder = self.pot - sum(amount for _, amount in winners)
        if remainder > 0 and winners:
            # Give remainder to first winner
            winners[0][0].collect_winnings(remainder)
    
    def update(self):
        """Update game state, process AI actions, etc."""
        # If game is in waiting state, don't update
        if self.state == GAME_STATES["WAITING"]:
            return
        
        # If game has ended, don't update
        if self.state == GAME_STATES["END_HAND"]:
            return
        
        # Check if betting round is complete
        if self.is_betting_round_complete():
            self.end_betting_round()
            return
        
        # Process AI player actions
        self.process_ai_actions()
    
    def get_active_player(self):
        """
        Get current active player
        
        Returns:
            Player: Current active player, or None if none
        """
        if 0 <= self.active_player_index < len(self.players):
            return self.players[self.active_player_index]
        return None
    
    def get_player_by_id(self, player_id):
        """
        Get player by ID
        
        Args:
            player_id (str): Player ID
        
        Returns:
            Player: Player object, or None if not found
        """
        for player in self.players:
            if player.id == player_id:
                return player
        return None
    
    def to_dict(self):
        """
        Convert game state to dictionary for serialization
        
        Returns:
            dict: Game state dictionary
        """
        return {
            "state": self.state,
            "pot": self.pot,
            "current_bet": self.current_bet,
            "min_raise": self.min_raise,
            "hand_number": self.hand_number,
            "players": [
                {
                    "id": p.id,
                    "name": p.name,
                    "is_human": p.is_human,
                    "chips": p.chips,
                    "bet": p.bet,
                    "folded": p.folded,
                    "all_in": p.all_in,
                    "is_dealer": p.is_dealer,
                    "is_small_blind": p.is_small_blind,
                    "is_big_blind": p.is_big_blind,
                    "is_active": self.active_player_index == i
                }
                for i, p in enumerate(self.players)
            ],
            "community_cards": [
                {"rank": c.rank, "suit": c.suit}
                for c in self.community_cards
            ],
            "last_winner": self.last_winner.name if self.last_winner else None,
            "last_winning_hand": self.last_winning_hand
        }
