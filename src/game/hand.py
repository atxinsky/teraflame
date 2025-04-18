#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
手牌评估模块

负责评估德州扑克牌型的强度。
"""

from collections import Counter
from src.utils.constants import CARD_RANKS, HAND_RANKINGS


class HandEvaluator:
    """手牌评估器类"""
    
    @staticmethod
    def evaluate_hand(hole_cards, community_cards):
        """
        评估玩家手牌的强度
        
        Args:
            hole_cards (list): 玩家的底牌 (2张牌)
            community_cards (list): 公共牌 (最多5张牌)
        
        Returns:
            tuple: (手牌类型索引, 手牌强度值, 牌型描述)
        """
        # 合并底牌和公共牌
        all_cards = hole_cards + community_cards
        
        # 从7张牌中选出最强的5张
        hand_strength, hand_type, description = HandEvaluator._find_best_hand(all_cards)
        
        return hand_type, hand_strength, description
    
    @staticmethod
    def _find_best_hand(cards):
        """
        从给定牌中寻找最强的5张牌组合
        
        Args:
            cards (list): 牌列表
        
        Returns:
            tuple: (手牌强度值, 手牌类型索引, 描述)
        """
        # 确保我们只考虑最多7张牌
        if len(cards) > 7:
            cards = cards[:7]
        
        # 检查各种可能的牌型
        # 从最强到最弱的顺序检查
        
        # 检查皇家同花顺
        royal_flush = HandEvaluator._check_royal_flush(cards)
        if royal_flush:
            return (9000000, 9, "皇家同花顺")
        
        # 检查同花顺
        straight_flush = HandEvaluator._check_straight_flush(cards)
        if straight_flush:
            return (8000000 + straight_flush, 8, f"同花顺，顶牌 {straight_flush}")
        
        # 检查四条
        four_of_a_kind = HandEvaluator._check_four_of_a_kind(cards)
        if four_of_a_kind:
            return (7000000 + four_of_a_kind[0]*1000 + four_of_a_kind[1], 7, 
                    f"四条 {four_of_a_kind[0]}，踢牌 {four_of_a_kind[1]}")
        
        # 检查葫芦
        full_house = HandEvaluator._check_full_house(cards)
        if full_house:
            return (6000000 + full_house[0]*1000 + full_house[1], 6, 
                    f"葫芦 {full_house[0]} 带 {full_house[1]}")
        
        # 检查同花
        flush = HandEvaluator._check_flush(cards)
        if flush:
            return (5000000 + flush, 5, f"同花，顶牌 {flush}")
        
        # 检查顺子
        straight = HandEvaluator._check_straight(cards)
        if straight:
            return (4000000 + straight, 4, f"顺子，顶牌 {straight}")
        
        # 检查三条
        three_of_a_kind = HandEvaluator._check_three_of_a_kind(cards)
        if three_of_a_kind:
            return (3000000 + three_of_a_kind[0]*1000 + three_of_a_kind[1]*10 + three_of_a_kind[2], 
                    3, f"三条 {three_of_a_kind[0]}")
        
        # 检查两对
        two_pair = HandEvaluator._check_two_pair(cards)
        if two_pair:
            return (2000000 + two_pair[0]*1000 + two_pair[1]*10 + two_pair[2], 
                    2, f"两对 {two_pair[0]} 和 {two_pair[1]}，踢牌 {two_pair[2]}")
        
        # 检查一对
        one_pair = HandEvaluator._check_one_pair(cards)
        if one_pair:
            return (1000000 + one_pair[0]*1000 + one_pair[1]*100 + 
                    one_pair[2]*10 + one_pair[3], 1, 
                    f"一对 {one_pair[0]}")
        
        # 高牌
        high_card = HandEvaluator._check_high_card(cards)
        return (high_card[0]*10000 + high_card[1]*1000 + high_card[2]*100 + 
                high_card[3]*10 + high_card[4], 0, 
                f"高牌 {high_card[0]}")
    
    @staticmethod
    def _get_ranks_and_suits(cards):
        """提取牌的点数和花色"""
        ranks = [card.value for card in cards]
        suits = [card.suit for card in cards]
        return ranks, suits
    
    @staticmethod
    def _check_royal_flush(cards):
        """检查是否有皇家同花顺"""
        # 按花色分组
        suit_groups = {}
        for card in cards:
            if card.suit not in suit_groups:
                suit_groups[card.suit] = []
            suit_groups[card.suit].append(card)
        
        # 检查每个花色组
        for suit, suit_cards in suit_groups.items():
            if len(suit_cards) < 5:
                continue
            
            # 检查是否有A、K、Q、J、10
            ranks = set(card.rank for card in suit_cards)
            if all(rank in ranks for rank in ['10', 'J', 'Q', 'K', 'A']):
                return True
        
        return False
    
    @staticmethod
    def _check_straight_flush(cards):
        """检查是否有同花顺"""
        # 按花色分组
        suit_groups = {}
        for card in cards:
            if card.suit not in suit_groups:
                suit_groups[card.suit] = []
            suit_groups[card.suit].append(card)
        
        # 检查每个花色组
        for suit, suit_cards in suit_groups.items():
            if len(suit_cards) < 5:
                continue
            
            # 排序并检查是否有顺子
            suit_cards.sort(key=lambda card: card.value)
            
            # 检查普通顺子
            for i in range(len(suit_cards) - 4):
                if all(suit_cards[i+j].value == suit_cards[i].value + j 
                       for j in range(5)):
                    return suit_cards[i+4].value
            
            # 检查A-5-4-3-2顺子
            if (any(card.rank == 'A' for card in suit_cards) and
                any(card.rank == '2' for card in suit_cards) and
                any(card.rank == '3' for card in suit_cards) and
                any(card.rank == '4' for card in suit_cards) and
                any(card.rank == '5' for card in suit_cards)):
                return 3  # 5高顺子 (A算作1)
        
        return False
    
    @staticmethod
    def _check_four_of_a_kind(cards):
        """检查是否有四条"""
        # 计算每个点数的出现次数
        rank_counter = Counter(card.value for card in cards)
        
        # 查找出现了4次的点数
        for rank, count in rank_counter.items():
            if count == 4:
                # 找出剩余最高牌作为踢牌
                kickers = [r for r in rank_counter.keys() if r != rank]
                if not kickers:
                    return (rank, 0)
                kicker = max(kickers)
                return (rank, kicker)
        
        return False
    
    @staticmethod
    def _check_full_house(cards):
        """检查是否有葫芦"""
        # 计算每个点数的出现次数
        rank_counter = Counter(card.value for card in cards)
        
        # 查找三条和对子的组合
        three_of_a_kind = None
        pair = None
        
        # 先查找最大的三条
        for rank, count in sorted(rank_counter.items(), key=lambda x: (x[1], x[0]), reverse=True):
            if count >= 3 and three_of_a_kind is None:
                three_of_a_kind = rank
            elif count >= 2 and pair is None:
                pair = rank
        
        if three_of_a_kind is not None and pair is not None:
            return (three_of_a_kind, pair)
        
        return False
    
    @staticmethod
    def _check_flush(cards):
        """检查是否有同花"""
        # 按花色分组
        suit_counter = Counter(card.suit for card in cards)
        
        # 查找同花
        for suit, count in suit_counter.items():
            if count >= 5:
                # 提取同一花色的牌
                flush_cards = [card for card in cards if card.suit == suit]
                # 排序并取最高的5张
                flush_cards.sort(key=lambda card: card.value, reverse=True)
                top_5 = flush_cards[:5]
                
                # 计算同花的权重
                weight = 0
                for i, card in enumerate(top_5):
                    weight += card.value * (10 ** (4 - i))
                return weight
        
        return False
    
    @staticmethod
    def _check_straight(cards):
        """检查是否有顺子"""
        # 提取牌值并去重
        values = sorted(set(card.value for card in cards))
        
        # 如果有A，添加值为-1作为顺子A-5-4-3-2的一部分
        if 12 in values:  # A的值是12
            values.append(-1)
        
        # 检查连续5个数
        for i in range(len(values) - 4):
            if values[i:i+5] == list(range(values[i], values[i] + 5)):
                return values[i+4]  # 返回顺子中的最高牌
        
        return False
    
    @staticmethod
    def _check_three_of_a_kind(cards):
        """检查是否有三条"""
        # 计算每个点数的出现次数
        rank_counter = Counter(card.value for card in cards)
        
        # 查找出现了3次的点数
        for rank, count in rank_counter.items():
            if count == 3:
                # 找出剩余最高两张牌作为踢牌
                kickers = [r for r in rank_counter.keys() if r != rank]
                kickers.sort(reverse=True)
                if len(kickers) < 2:
                    kickers.extend([0] * (2 - len(kickers)))
                return (rank, kickers[0], kickers[1])
        
        return False
    
    @staticmethod
    def _check_two_pair(cards):
        """检查是否有两对"""
        # 计算每个点数的出现次数
        rank_counter = Counter(card.value for card in cards)
        
        # 查找所有对子
        pairs = [rank for rank, count in rank_counter.items() if count >= 2]
        if len(pairs) >= 2:
            # 排序对子并取最高的两对
            pairs.sort(reverse=True)
            high_pair, low_pair = pairs[0], pairs[1]
            
            # 找出剩余最高牌作为踢牌
            kickers = [r for r in rank_counter.keys() if r != high_pair and r != low_pair]
            kicker = max(kickers) if kickers else 0
            
            return (high_pair, low_pair, kicker)
        
        return False
    
    @staticmethod
    def _check_one_pair(cards):
        """检查是否有一对"""
        # 计算每个点数的出现次数
        rank_counter = Counter(card.value for card in cards)
        
        # 查找对子
        for rank, count in rank_counter.items():
            if count == 2:
                # 找出剩余最高三张牌作为踢牌
                kickers = [r for r in rank_counter.keys() if r != rank]
                kickers.sort(reverse=True)
                if len(kickers) < 3:
                    kickers.extend([0] * (3 - len(kickers)))
                return (rank, kickers[0], kickers[1], kickers[2])
        
        return False
    
    @staticmethod
    def _check_high_card(cards):
        """检查高牌"""
        # 排序并取最高的5张
        values = sorted([card.value for card in cards], reverse=True)
        top_5 = values[:5]
        
        # 如果不足5张，用0补充
        if len(top_5) < 5:
            top_5.extend([0] * (5 - len(top_5)))
        
        return tuple(top_5)


def get_hand_description(hand_type, cards):
    """
    获取手牌的描述
    
    Args:
        hand_type (int): 手牌类型索引
        cards (list): 构成牌型的牌列表
    
    Returns:
        str: 手牌描述
    """
    type_name = HAND_RANKINGS[hand_type]
    
    # 根据牌型提供更详细的描述
    if hand_type == 9:  # 皇家同花顺
        suit = cards[0].suit
        return f"{type_name} ({suit})"
    
    if hand_type == 8:  # 同花顺
        top_card = max(cards, key=lambda c: c.value)
        return f"{type_name} ({top_card.rank}高)"
    
    if hand_type == 7:  # 四条
        # 找出四条的牌值
        rank_counter = Counter(card.rank for card in cards)
        four_rank = [rank for rank, count in rank_counter.items() if count == 4][0]
        return f"{type_name} ({four_rank})"
    
    if hand_type == 6:  # 葫芦
        # 找出三条和对子的牌值
        rank_counter = Counter(card.rank for card in cards)
        three_rank = [rank for rank, count in rank_counter.items() if count == 3][0]
        pair_rank = [rank for rank, count in rank_counter.items() if count == 2][0]
        return f"{type_name} ({three_rank}带{pair_rank})"
    
    if hand_type == 5:  # 同花
        top_card = max(cards, key=lambda c: c.value)
        return f"{type_name} ({top_card.rank}高)"
    
    if hand_type == 4:  # 顺子
        top_card = max(cards, key=lambda c: c.value)
        return f"{type_name} ({top_card.rank}高)"
    
    if hand_type == 3:  # 三条
        # 找出三条的牌值
        rank_counter = Counter(card.rank for card in cards)
        three_rank = [rank for rank, count in rank_counter.items() if count == 3][0]
        return f"{type_name} ({three_rank})"
    
    if hand_type == 2:  # 两对
        # 找出两对的牌值
        rank_counter = Counter(card.rank for card in cards)
        pairs = [rank for rank, count in rank_counter.items() if count == 2]
        pairs.sort(key=lambda r: CARD_RANKS.index(r), reverse=True)
        return f"{type_name} ({pairs[0]}和{pairs[1]})"
    
    if hand_type == 1:  # 一对
        # 找出对子的牌值
        rank_counter = Counter(card.rank for card in cards)
        pair_rank = [rank for rank, count in rank_counter.items() if count == 2][0]
        return f"{type_name} ({pair_rank})"
    
    # 高牌
    top_card = max(cards, key=lambda c: c.value)
    return f"{type_name} ({top_card.rank})"
