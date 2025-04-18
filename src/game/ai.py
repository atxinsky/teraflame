#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI玩家决策模块

实现AI玩家的德州扑克决策逻辑。
"""

import random
from src.utils.constants import CARD_RANKS, CARD_SUITS, AI_DIFFICULTIES


class PokerAI:
    """扑克AI类"""
    
    def __init__(self, difficulty="MEDIUM"):
        """
        初始化AI
        
        Args:
            difficulty (str, optional): AI难度。默认为"MEDIUM"
        """
        if difficulty not in AI_DIFFICULTIES:
            raise ValueError(f"无效的AI难度: {difficulty}")
        
        self.difficulty = difficulty
        
        # 设置基于难度的行为参数
        self.set_behavior_params()
    
    def set_behavior_params(self):
        """设置基于难度的行为参数"""
        # 基础紧凶度（越高表示越激进）
        self.aggression = {
            "EASY": 0.3,
            "MEDIUM": 0.5,
            "HARD": 0.7
        }[self.difficulty]
        
        # 诈唬频率
        self.bluff_frequency = {
            "EASY": 0.1,
            "MEDIUM": 0.2,
            "HARD": 0.3
        }[self.difficulty]
        
        # 位置意识（越高表示越能利用位置优势）
        self.position_awareness = {
            "EASY": 0.2,
            "MEDIUM": 0.5,
            "HARD": 0.8
        }[self.difficulty]
        
        # 记忆能力（对手行为模式记忆）
        self.memory_capacity = {
            "EASY": 0.1,
            "MEDIUM": 0.3,
            "HARD": 0.7
        }[self.difficulty]
        
        # 手牌评估精确度
        self.hand_reading_accuracy = {
            "EASY": 0.5,
            "MEDIUM": 0.7,
            "HARD": 0.9
        }[self.difficulty]
    
    def make_decision(self, player, game_state):
        """
        根据游戏状态决策下一步行动
        
        Args:
            player (Player): AI控制的玩家对象
            game_state (dict): 游戏状态信息
        
        Returns:
            tuple: (决策类型, 金额)
        """
        # 提取游戏信息
        current_bet = game_state.get("current_bet", 0)
        min_raise = game_state.get("min_raise", 10)
        pot = game_state.get("pot", 0)
        community_cards = game_state.get("community_cards", [])
        game_round = game_state.get("round", "PRE_FLOP")
        position = game_state.get("position", "EARLY")
        players_remaining = game_state.get("players_remaining", 1)
        
        # 需要跟注的金额
        call_amount = current_bet - player.bet
        
        # 如果玩家已弃牌或全押
        if player.folded or player.all_in:
            return ("NONE", 0)
        
        # 计算手牌强度和胜率评估
        hand_strength = self._evaluate_hand_strength(player, community_cards, game_round)
        win_probability = self._estimate_win_probability(
            hand_strength, game_round, community_cards, players_remaining
        )
        
        # 根据位置调整策略
        position_factor = self._position_adjustment(position, players_remaining)
        
        # 根据底池赔率调整
        pot_odds = self._calculate_pot_odds(call_amount, pot)
        
        # 加上随机性和诈唬因素
        bluff_factor = self._should_bluff(game_state)
        
        # 计算最终行动分数
        action_scores = self._calculate_action_scores(
            win_probability, position_factor, pot_odds, bluff_factor,
            call_amount, min_raise, player.chips, current_bet
        )
        
        # 选择得分最高的行动
        return self._select_best_action(action_scores, player, current_bet, min_raise, call_amount)
    
    def _evaluate_hand_strength(self, player, community_cards, game_round):
        """评估手牌强度，范围0-1"""
        # 使用玩家对象中已计算的手牌强度
        # 但对于不同的游戏阶段有不同的评估权重
        
        # 归一化手牌强度基值
        base_strength = player.hand_strength / 9000000  # 假设9000000是最大可能值
        
        # 根据游戏阶段调整手牌评估标准
        if game_round == "PRE_FLOP":
            # 翻牌前，主要看底牌质量
            return self._evaluate_preflop_hand(player.hole_cards)
        elif game_round == "FLOP":
            # 翻牌后，开始给予手牌评估更多权重
            return base_strength * 0.7 + self._evaluate_preflop_hand(player.hole_cards) * 0.3
        elif game_round == "TURN":
            # 转牌后，更重视当前手牌评估
            return base_strength * 0.8 + self._evaluate_preflop_hand(player.hole_cards) * 0.2
        else:  # RIVER
            # 河牌后，几乎完全基于当前手牌评估
            return base_strength * 0.9 + self._evaluate_preflop_hand(player.hole_cards) * 0.1
    
    def _evaluate_preflop_hand(self, hole_cards):
        """评估翻牌前的手牌强度"""
        if len(hole_cards) != 2:
            return 0.1  # 默认值
        
        # 获取两张牌的点数和花色
        ranks = [card.rank for card in hole_cards]
        values = [card.value for card in hole_cards]
        suits = [card.suit for card in hole_cards]
        
        # 口袋对（两张相同点数的牌）
        if ranks[0] == ranks[1]:
            # 高对得分高
            pair_rank = values[0]
            pair_strength = (pair_rank + 1) / 13  # 归一化
            return 0.5 + 0.5 * pair_strength  # 口袋对得分范围：0.5-1.0
        
        # 同花（两张相同花色的牌）
        is_suited = suits[0] == suits[1]
        
        # 高牌
        high_card = max(values)
        low_card = min(values)
        
        # 计算牌之间的差距（连牌性）
        gap = abs(values[0] - values[1]) - 1
        
        # 基础分值
        base_score = (high_card + 1) / 26  # 高牌贡献一半分值
        
        # 连牌加分
        connectivity = max(0, (13 - gap)) / 26  # 连牌贡献另一半分值
        
        # 同花加分
        suited_bonus = 0.1 if is_suited else 0
        
        # 根据具体牌值做一些特殊调整
        # 例如：A-K比K-Q更强，即使差距相同
        special_bonus = 0
        if 'A' in ranks and 'K' in ranks:
            special_bonus = 0.1
        elif 'A' in ranks and 'Q' in ranks:
            special_bonus = 0.05
        
        # 计算最终得分 (0-0.5范围，因为口袋对占据了0.5-1.0)
        score = base_score + connectivity + suited_bonus + special_bonus
        return min(0.5, score)  # 确保非对子牌不超过0.5
    
    def _estimate_win_probability(self, hand_strength, game_round, community_cards, players_remaining):
        """估计获胜概率"""
        # 这个方法应该根据当前手牌强度、游戏阶段和剩余玩家数量
        # 估计获胜概率
        
        # 使用简化的模型：基于手牌强度，但考虑剩余玩家数和游戏阶段
        
        # 基础获胜概率是手牌强度
        base_prob = hand_strength
        
        # 根据剩余玩家数调整（玩家越多，获胜概率越低）
        player_factor = 1 / (players_remaining ** 0.5)
        
        # 根据游戏阶段调整（后期更准确）
        round_certainty = {
            "PRE_FLOP": 0.3,
            "FLOP": 0.6,
            "TURN": 0.8,
            "RIVER": 1.0
        }.get(game_round, 0.5)
        
        # 混合这些因素
        win_prob = (base_prob * round_certainty) * player_factor
        
        # 加入一点随机性，模拟AI的不完美评估
        randomness = random.uniform(-0.1, 0.1) * (1 - self.hand_reading_accuracy)
        win_prob = max(0, min(1, win_prob + randomness))
        
        return win_prob
    
    def _position_adjustment(self, position, players_remaining):
        """根据位置调整策略"""
        # 晚位置可以打得更宽松
        if position == "LATE":
            return 0.2 * self.position_awareness
        elif position == "MIDDLE":
            return 0.1 * self.position_awareness
        else:  # EARLY
            return 0
    
    def _calculate_pot_odds(self, call_amount, pot):
        """计算底池赔率，返回是否值得跟注的指标"""
        if call_amount == 0:
            return 1.0  # 不需要跟注，总是"值得"
        
        # 计算底池赔率
        pot_odds = pot / call_amount
        
        # 转换为0-1范围的指标
        # 赔率越高，指标越接近1
        return min(1.0, pot_odds / 5)
    
    def _should_bluff(self, game_state):
        """决定是否应该诈唬"""
        # 基于多种因素，生成一个诈唬倾向得分
        
        # 基础诈唬概率
        bluff_chance = self.bluff_frequency
        
        # 根据游戏阶段调整
        if game_state.get("round") == "RIVER":
            bluff_chance *= 1.5  # 河牌更容易诈唬
        
        # 根据剩余玩家数调整
        players_remaining = game_state.get("players_remaining", 1)
        if players_remaining > 2:
            bluff_chance *= 0.5  # 多人时减少诈唬
        
        # 判断是否诈唬
        return random.random() < bluff_chance
    
    def _calculate_action_scores(self, win_probability, position_factor, pot_odds, bluff_factor,
                               call_amount, min_raise, chips, current_bet):
        """计算各种行动的得分"""
        # 初始化行动得分
        scores = {
            "FOLD": 0,
            "CHECK": 0,
            "CALL": 0,
            "RAISE": 0,
            "ALL_IN": 0
        }
        
        # 跟注和加注的基础得分基于胜率
        scores["CALL"] = win_probability + position_factor
        scores["RAISE"] = win_probability * 1.2 + position_factor * 1.5
        
        # 考虑底池赔率
        if pot_odds > win_probability:
            scores["CALL"] += 0.2  # 底池赔率好，鼓励跟注
        else:
            scores["CALL"] -= 0.2  # 底池赔率差，减少跟注
        
        # 诈唬因素
        if bluff_factor:
            scores["RAISE"] += 0.3
            scores["ALL_IN"] += 0.1
        
        # 看牌选项（如果可用）
        if current_bet == 0:
            scores["CHECK"] = scores["CALL"]
            scores["CALL"] = 0  # 不能跟注
        
        # 弃牌选项
        # 当胜率低且需要跟注时
        if win_probability < 0.3 and call_amount > 0:
            scores["FOLD"] = 1 - win_probability
        
        # 全压选项
        # 当筹码较少或胜率很高时
        if chips < current_bet * 3 or win_probability > 0.8:
            scores["ALL_IN"] = win_probability * 1.5
        
        # 根据筹码量调整得分
        # 避免不必要的大注
        chip_factor = min(1.0, 5 * chips / (current_bet if current_bet > 0 else min_raise))
        scores["RAISE"] *= chip_factor
        
        # 添加AI难度相关的随机性
        randomness = 0.3 * (1 - self.hand_reading_accuracy)
        for action in scores:
            scores[action] += random.uniform(-randomness, randomness)
        
        return scores
    
    def _select_best_action(self, action_scores, player, current_bet, min_raise, call_amount):
        """选择得分最高的行动"""
        # 过滤掉不可行的行动
        valid_actions = {}
        
        # 任何情况下都可以弃牌
        valid_actions["FOLD"] = action_scores["FOLD"]
        
        # 检查是否可以看牌
        if current_bet == 0 or current_bet == player.bet:
            valid_actions["CHECK"] = action_scores["CHECK"]
        
        # 检查是否可以跟注
        if call_amount <= player.chips and call_amount > 0:
            valid_actions["CALL"] = action_scores["CALL"]
        
        # 检查是否可以加注
        raise_cost = call_amount + min_raise
        if raise_cost < player.chips:
            valid_actions["RAISE"] = action_scores["RAISE"]
        
        # 检查是否可以全押
        if player.chips > call_amount:
            valid_actions["ALL_IN"] = action_scores["ALL_IN"]
        
        # 如果没有有效行动（不应该发生），则弃牌
        if not valid_actions:
            return ("FOLD", 0)
        
        # 选择得分最高的行动
        best_action = max(valid_actions.items(), key=lambda x: x[1])[0]
        
        # 根据行动决定金额
        if best_action == "FOLD" or best_action == "CHECK":
            return (best_action, 0)
        elif best_action == "CALL":
            return (best_action, call_amount)
        elif best_action == "RAISE":
            # 决定加注金额
            # 基本策略：胜率越高加注越多
            win_prob = action_scores["RAISE"] / 2  # 归一化到0-1范围
            
            # 最小加注到最大筹码的范围
            max_raise = player.chips - call_amount
            raise_range = max_raise - min_raise
            
            # 根据胜率决定加注比例
            raise_amount = call_amount + min_raise + int(raise_range * win_prob * self.aggression)
            
            # 确保不超过全押
            raise_amount = min(raise_amount, player.chips)
            
            return (best_action, raise_amount)
        elif best_action == "ALL_IN":
            return (best_action, player.chips)
        
        # 默认情况
        return ("FOLD", 0)
