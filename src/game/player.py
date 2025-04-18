#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
玩家类模块

定义了德州扑克游戏中的玩家。
"""

import uuid
from src.utils.constants import INITIAL_PLAYER_CHIPS


class Player:
    """玩家类"""
    
    def __init__(self, name, is_human=False, ai_difficulty=None, chips=INITIAL_PLAYER_CHIPS):
        """
        初始化玩家
        
        Args:
            name (str): 玩家名称
            is_human (bool, optional): 是否为人类玩家。默认为False
            ai_difficulty (str, optional): AI难度，如果是AI玩家。默认为None
            chips (int, optional): 初始筹码。默认为constants.INITIAL_PLAYER_CHIPS
        """
        self.id = str(uuid.uuid4())[:8]  # 生成唯一ID
        self.name = name
        self.is_human = is_human
        self.ai_difficulty = ai_difficulty
        
        # 筹码相关
        self.chips = chips
        self.bet = 0  # 当前轮次的下注
        self.total_bet = 0  # 当前手牌的总下注
        
        # 手牌相关
        self.hole_cards = []  # 底牌
        self.hand_strength = 0  # 手牌强度值
        self.hand_type = 0  # 手牌类型索引
        self.hand_description = ""  # 手牌描述
        
        # 状态标志
        self.folded = False  # 是否弃牌
        self.all_in = False  # 是否全押
        self.is_active = True  # 是否参与游戏
        self.is_dealer = False  # 是否为庄家
        self.is_small_blind = False  # 是否为小盲注
        self.is_big_blind = False  # 是否为大盲注
        
        # 玩家位置（用于界面显示）
        self.position = (0, 0)
        
        # 游戏统计
        self.hands_played = 0
        self.hands_won = 0
        self.biggest_win = 0
    
    def reset_for_new_hand(self):
        """为新的一手牌重置玩家状态"""
        self.hole_cards = []
        self.bet = 0
        self.total_bet = 0
        self.hand_strength = 0
        self.hand_type = 0
        self.hand_description = ""
        self.folded = False
        self.all_in = False
        self.is_dealer = False
        self.is_small_blind = False
        self.is_big_blind = False
    
    def receive_card(self, card):
        """
        接收一张牌
        
        Args:
            card (Card): 发给玩家的牌
        """
        self.hole_cards.append(card)
    
    def place_bet(self, amount):
        """
        下注
        
        Args:
            amount (int): 下注金额
        
        Returns:
            int: 实际下注金额（可能因为筹码不足而小于请求金额）
        
        Raises:
            ValueError: 如果下注金额小于0
        """
        if amount < 0:
            raise ValueError("下注金额不能为负数")
        
        # 计算实际下注金额（考虑筹码限制）
        actual_amount = min(amount, self.chips)
        
        # 更新筹码和下注
        self.chips -= actual_amount
        self.bet += actual_amount
        self.total_bet += actual_amount
        
        # 检查是否全押
        if self.chips == 0:
            self.all_in = True
        
        return actual_amount
    
    def fold(self):
        """弃牌"""
        self.folded = True
    
    def can_raise(self, min_raise):
        """
        检查玩家是否能够加注
        
        Args:
            min_raise (int): 最小加注金额
        
        Returns:
            bool: 是否能够加注
        """
        return self.chips >= min_raise and not self.all_in
    
    def collect_winnings(self, amount):
        """
        收集赢得的筹码
        
        Args:
            amount (int): 赢得的金额
        """
        self.chips += amount
        
        # 更新统计数据
        self.hands_won += 1
        if amount > self.biggest_win:
            self.biggest_win = amount
    
    def evaluate_hand(self, community_cards, evaluator):
        """
        评估手牌强度
        
        Args:
            community_cards (list): 公共牌
            evaluator (HandEvaluator): 手牌评估器
        """
        if self.folded or not self.hole_cards:
            return
        
        # 使用评估器计算手牌强度
        self.hand_type, self.hand_strength, self.hand_description = (
            evaluator.evaluate_hand(self.hole_cards, community_cards)
        )
    
    def ai_make_decision(self, game_state, current_bet, min_raise):
        """
        AI决策逻辑
        
        Args:
            game_state (dict): 当前游戏状态
            current_bet (int): 当前最高下注
            min_raise (int): 最小加注金额
        
        Returns:
            tuple: (决策类型, 金额)
        """
        if self.is_human:
            raise ValueError("人类玩家不应该使用AI决策")
        
        # 这只是一个简单的AI逻辑示例
        # 完整的AI应该考虑更多因素，如手牌强度、位置、筹码等
        
        # 模拟AI思考...
        
        # 随机决策，但考虑难度
        import random
        
        # 计算跟注所需金额
        call_amount = current_bet - self.bet
        
        # 弃牌概率，取决于难度和手牌强度
        fold_threshold = {
            "EASY": 0.4,
            "MEDIUM": 0.3,
            "HARD": 0.2
        }.get(self.ai_difficulty, 0.3)
        
        # 加注概率，取决于难度和手牌强度
        raise_threshold = {
            "EASY": 0.7,
            "MEDIUM": 0.8,
            "HARD": 0.9
        }.get(self.ai_difficulty, 0.8)
        
        # 手牌强度影响决策
        # 实际实现中应该基于self.hand_strength调整阈值
        
        # 生成随机决策
        decision_value = random.random()
        
        # 如果当前没有下注，考虑看牌
        if current_bet == 0:
            if decision_value < 0.5:
                return ("CHECK", 0)
            else:
                # 随机加注
                raise_amount = min_raise + random.randint(0, min(self.chips, min_raise * 3))
                return ("RAISE", raise_amount)
        
        # 如果已经有下注
        if decision_value < fold_threshold:
            return ("FOLD", 0)
        elif decision_value < raise_threshold:
            return ("CALL", call_amount)
        else:
            # 随机加注
            raise_amount = call_amount + min_raise + random.randint(0, min(self.chips - call_amount, min_raise * 3))
            return ("RAISE", raise_amount)
    
    def can_make_action(self, action_type, amount=0):
        """
        检查玩家是否可以执行指定操作
        
        Args:
            action_type (str): 操作类型
            amount (int, optional): 操作金额。默认为0
        
        Returns:
            bool: 是否可以执行操作
        """
        if self.folded or self.all_in or not self.is_active:
            return False
        
        if action_type == "FOLD":
            return True
        
        if action_type == "CHECK":
            # 只有当前没有下注或者已经跟注时才能看牌
            return self.bet == self.get_table_bet()
        
        if action_type == "CALL":
            # 检查是否有足够的筹码跟注
            call_amount = self.get_table_bet() - self.bet
            return call_amount <= self.chips
        
        if action_type == "RAISE" or action_type == "ALL_IN":
            # 检查是否有足够的筹码加注
            return self.chips > self.get_table_bet() - self.bet
        
        return False
    
    def get_table_bet(self):
        """
        获取当前桌面最高下注（需要由Game类设置）
        
        Returns:
            int: 桌面最高下注
        """
        # 这个方法需要在游戏逻辑中被覆盖
        # 这里只是一个占位符
        return 0
    
    def __str__(self):
        """字符串表示"""
        status = "玩家"
        if self.is_dealer:
            status = "庄家"
        elif self.is_small_blind:
            status = "小盲"
        elif self.is_big_blind:
            status = "大盲"
        
        return f"{self.name} ({status}): 筹码 {self.chips}, 下注 {self.bet}"
