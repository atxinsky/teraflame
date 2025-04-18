#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
扑克牌类模块

定义了扑克牌的基本属性和行为。
"""

import os
import pygame
from src.utils.constants import CARD_RANKS, CARD_SUITS, IMAGES_DIR
from src.utils.helpers import load_image, load_font


class Card:
    """扑克牌类"""
    
    def __init__(self, rank, suit, face_up=True):
        """
        初始化扑克牌
        
        Args:
            rank (str): 牌面值 ('2', '3', ..., 'A')
            suit (str): 花色 ('♣', '♦', '♥', '♠')
            face_up (bool, optional): 是否正面朝上。默认为True
        """
        if rank not in CARD_RANKS:
            raise ValueError(f"无效的牌面值: {rank}")
        if suit not in CARD_SUITS:
            raise ValueError(f"无效的花色: {suit}")
        
        self.rank = rank
        self.suit = suit
        self.face_up = face_up
        
        # 加载卡牌图像
        self._load_images()
        
        # 卡牌数值 (用于比较)
        self.value = CARD_RANKS.index(rank)
        
        # 卡牌的显示位置
        self.position = (0, 0)
        
        # 动画状态
        self.is_animating = False
        self.animation_target = None
        self.animation_speed = 0
    
    def _load_images(self):
        """加载卡牌图像"""
        # 正面图像名称格式如: "hearts_A.png", "clubs_10.png"
        suit_name = {
            '♣': 'clubs',
            '♦': 'diamonds', 
            '♥': 'hearts', 
            '♠': 'spades'
        }[self.suit]
        
        # 尝试加载卡牌图像
        try:
            self.face_image = load_image(f"{suit_name}_{self.rank}.png")
        except:
            # 创建一个基本的卡牌表面
            self.face_image = self._create_default_card_face()
        
        # 背面图像
        try:
            self.back_image = load_image("card_back.png")
        except:
            # 创建一个基本的卡牌背面
            self.back_image = self._create_default_card_back()
        
        # 设置卡片尺寸
        self.width = self.face_image.get_width()
        self.height = self.face_image.get_height()
    
    def _create_default_card_face(self):
        """创建默认卡牌正面"""
        card = pygame.Surface((70, 100))
        card.fill((255, 255, 255))
        
        # 添加边框
        pygame.draw.rect(card, (0, 0, 0), pygame.Rect(0, 0, 70, 100), 2)
        
        # 添加花色和数值
        try:
            font = load_font(24)
            rank_text = font.render(self.rank, True, (0, 0, 0))
            
            # 设置花色颜色
            suit_color = (0, 0, 0)  # 黑色默认
            if self.suit in ['♦', '♥']:
                suit_color = (255, 0, 0)  # 红色
                
            suit_text = font.render(self.suit, True, suit_color)
            
            # 绘制文本
            card.blit(rank_text, (5, 5))
            card.blit(suit_text, (5, 35))
            # 调整右下角文本位置以适应不同字体
            rank_text_rect = rank_text.get_rect()
            rank_text_rect.bottomright = (65, 95)
            card.blit(rank_text, rank_text_rect)
            
        except Exception as e:
            print(f"绘制默认卡牌正面失败: {e}")
            
        return card
    
    def _create_default_card_back(self):
        """创建默认卡牌背面"""
        card = pygame.Surface((70, 100))
        card.fill((30, 100, 200))  # 蓝色背景
        
        # 添加网格图案
        for x in range(0, 70, 10):
            for y in range(0, 100, 10):
                pygame.draw.rect(card, (20, 60, 120), pygame.Rect(x, y, 5, 5))
        
        # 添加边框
        pygame.draw.rect(card, (0, 0, 0), pygame.Rect(0, 0, 70, 100), 2)
        
        return card
    
    def flip(self):
        """翻转卡牌"""
        self.face_up = not self.face_up
    
    def set_position(self, pos):
        """
        设置卡牌位置
        
        Args:
            pos (tuple): 位置坐标 (x, y)
        """
        self.position = pos
    
    def move_to(self, target_pos, speed=5):
        """
        设置卡牌移动动画
        
        Args:
            target_pos (tuple): 目标位置 (x, y)
            speed (int, optional): 移动速度
        """
        self.is_animating = True
        self.animation_target = target_pos
        self.animation_speed = speed
    
    def update(self):
        """更新卡牌状态（处理动画等）"""
        if self.is_animating and self.animation_target:
            current_x, current_y = self.position
            target_x, target_y = self.animation_target
            
            # 计算移动方向和距离
            dx = target_x - current_x
            dy = target_y - current_y
            distance = (dx**2 + dy**2) ** 0.5
            
            if distance < self.animation_speed:
                # 到达目标
                self.position = self.animation_target
                self.is_animating = False
            else:
                # 继续移动
                move_x = dx * self.animation_speed / distance
                move_y = dy * self.animation_speed / distance
                self.position = (current_x + move_x, current_y + move_y)
    
    def draw(self, surface):
        """
        在指定表面上绘制卡牌
        
        Args:
            surface (pygame.Surface): 绘制表面
        """
        image = self.face_image if self.face_up else self.back_image
        surface.blit(image, self.position)
    
    def contains_point(self, point):
        """
        检查指定点是否在卡牌内
        
        Args:
            point (tuple): 坐标点 (x, y)
        
        Returns:
            bool: 点是否在卡牌内
        """
        x, y = point
        card_x, card_y = self.position
        
        return (card_x <= x <= card_x + self.width and 
                card_y <= y <= card_y + self.height)
    
    def __str__(self):
        """字符串表示"""
        return f"{self.rank}{self.suit}"
    
    def __repr__(self):
        """正式字符串表示"""
        return f"Card('{self.rank}', '{self.suit}')"
    
    def __eq__(self, other):
        """相等比较"""
        if not isinstance(other, Card):
            return False
        return self.rank == other.rank and self.suit == other.suit
