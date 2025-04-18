#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
牌组类模块

定义了德州扑克游戏中使用的扑克牌组。
"""

import random
from src.game.card import Card
from src.utils.constants import CARD_RANKS, CARD_SUITS


class Deck:
    """扑克牌组类"""
    
    def __init__(self):
        """初始化一副新牌"""
        self.reset()
    
    def reset(self):
        """重置牌组为一副新牌"""
        # 创建一副52张牌
        self.cards = []
        for suit in CARD_SUITS:
            for rank in CARD_RANKS:
                self.cards.append(Card(rank, suit))
        
        # 已发出的牌
        self.dealt_cards = []
    
    def shuffle(self):
        """洗牌"""
        # 将已发出的牌放回牌组
        self.cards.extend(self.dealt_cards)
        self.dealt_cards = []
        
        # 随机打乱牌组
        random.shuffle(self.cards)
    
    def deal(self, count=1, face_up=True):
        """
        发牌
        
        Args:
            count (int, optional): 要发的牌数。默认为1
            face_up (bool, optional): 是否正面朝上。默认为True
        
        Returns:
            list: 发出的牌列表
        
        Raises:
            ValueError: 如果牌组中没有足够的牌
        """
        if len(self.cards) < count:
            raise ValueError(f"牌组中没有足够的牌。请求: {count}, 剩余: {len(self.cards)}")
        
        dealt = []
        for _ in range(count):
            card = self.cards.pop()
            card.face_up = face_up
            self.dealt_cards.append(card)
            dealt.append(card)
        
        return dealt
    
    def deal_one(self, face_up=True):
        """
        发一张牌
        
        Args:
            face_up (bool, optional): 是否正面朝上。默认为True
        
        Returns:
            Card: 发出的牌
        
        Raises:
            ValueError: 如果牌组为空
        """
        return self.deal(1, face_up)[0]
    
    def burn(self):
        """
        销毌一张牌（在发公共牌前通常会这样做）
        
        Returns:
            Card: 销毌的牌
        
        Raises:
            ValueError: 如果牌组为空
        """
        return self.deal(1, False)[0]
    
    def remaining(self):
        """
        获取牌组中剩余的牌数
        
        Returns:
            int: 剩余牌数
        """
        return len(self.cards)
    
    def __len__(self):
        """牌组长度"""
        return len(self.cards)
    
    def __str__(self):
        """字符串表示"""
        return f"Deck with {len(self.cards)} cards remaining"
