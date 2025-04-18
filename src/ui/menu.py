#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
菜单类模块

提供游戏中使用的各种菜单界面。
"""

import pygame
from src.ui.button import Button
from src.utils.constants import WHITE, BLACK, GREEN, GOLD, WINDOW_WIDTH, WINDOW_HEIGHT


class Menu:
    """菜单基类"""
    
    def __init__(self, screen):
        """
        初始化菜单
        
        Args:
            screen (pygame.Surface): 游戏窗口表面
        """
        self.screen = screen
        self.buttons = []
        self.is_active = False
        
        # 创建半透明背景表面
        self.background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.background.fill((0, 0, 0, 180))  # 半透明黑色
        
        # 创建菜单面板
        panel_width = 600
        panel_height = 400
        panel_x = (WINDOW_WIDTH - panel_width) // 2
        panel_y = (WINDOW_HEIGHT - panel_height) // 2
        
        self.panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        self.panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        self.panel.fill((30, 30, 50, 240))  # 半透明深蓝色
        
        # 菜单标题
        self.title = "菜单"
        self.title_font = pygame.font.SysFont(None, 48)
        
        # 关闭按钮
        close_button = Button(
            panel_x + panel_width - 50, panel_y + 10, 40, 40,
            "X", self.on_close,
            bg_color=(200, 50, 50),
            highlight_color=(255, 100, 100),
            text_color=WHITE
        )
        self.buttons.append(close_button)
    
    def show(self):
        """显示菜单"""
        self.is_active = True
    
    def hide(self):
        """隐藏菜单"""
        self.is_active = False
    
    def handle_event(self, event):
        """
        处理事件
        
        Args:
            event (pygame.event.Event): Pygame事件
        
        Returns:
            bool: 事件是否被处理
        """
        if not self.is_active:
            return False
        
        # 处理按钮点击
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            for button in self.buttons:
                if button.handle_event(event):
                    return True
        
        return True  # 菜单活跃时吞噬所有事件
    
    def render(self):
        """渲染菜单"""
        if not self.is_active:
            return
        
        # 绘制半透明背景
        self.screen.blit(self.background, (0, 0))
        
        # 绘制菜单面板
        pygame.draw.rect(self.panel, (50, 50, 70), self.panel.get_rect(), border_radius=10)
        pygame.draw.rect(self.panel, GOLD, self.panel.get_rect(), width=2, border_radius=10)
        self.screen.blit(self.panel, self.panel_rect)
        
        # 绘制标题
        title_surface = self.title_font.render(self.title, True, WHITE)
        title_rect = title_surface.get_rect(center=(self.panel_rect.centerx, self.panel_rect.y + 40))
        self.screen.blit(title_surface, title_rect)
        
        # 绘制按钮
        for button in self.buttons:
            button.draw(self.screen)
    
    def on_close(self):
        """关闭按钮点击处理"""
        self.hide()


class MainMenu(Menu):
    """主菜单类"""
    
    def __init__(self, screen, start_game_callback=None, 
                 settings_callback=None, help_callback=None, quit_callback=None):
        """
        初始化主菜单
        
        Args:
            screen (pygame.Surface): 游戏窗口表面
            start_game_callback (function, optional): 开始游戏回调
            settings_callback (function, optional): 设置回调
            help_callback (function, optional): 帮助回调
            quit_callback (function, optional): 退出回调
        """
        super().__init__(screen)
        self.title = "德州扑克"
        
        # 按钮尺寸和位置
        button_width = 200
        button_height = 50
        button_spacing = 20
        start_y = self.panel_rect.y + 120
        
        # 开始游戏按钮
        self.buttons.append(Button(
            self.panel_rect.centerx - button_width // 2, start_y,
            button_width, button_height,
            "开始游戏", start_game_callback or self.on_close,
            bg_color=(50, 150, 50),
            highlight_color=(70, 200, 70)
        ))
        
        # 设置按钮
        self.buttons.append(Button(
            self.panel_rect.centerx - button_width // 2, start_y + button_height + button_spacing,
            button_width, button_height,
            "设置", settings_callback or self.on_close,
            bg_color=(50, 50, 150),
            highlight_color=(70, 70, 200)
        ))
        
        # 帮助按钮
        self.buttons.append(Button(
            self.panel_rect.centerx - button_width // 2, 
            start_y + (button_height + button_spacing) * 2,
            button_width, button_height,
            "帮助", help_callback or self.on_close,
            bg_color=(150, 50, 50),
            highlight_color=(200, 70, 70)
        ))
        
        # 退出按钮
        self.buttons.append(Button(
            self.panel_rect.centerx - button_width // 2, 
            start_y + (button_height + button_spacing) * 3,
            button_width, button_height,
            "退出", quit_callback or self.on_close,
            bg_color=(100, 100, 100),
            highlight_color=(150, 150, 150)
        ))
    
    def render(self):
        """渲染主菜单"""
        super().render()
        
        if not self.is_active:
            return
        
        # 绘制游戏标题
        title_font = pygame.font.SysFont(None, 72)
        title_surface = title_font.render(self.title, True, GOLD)
        title_rect = title_surface.get_rect(center=(self.panel_rect.centerx, self.panel_rect.y + 50))
        self.screen.blit(title_surface, title_rect)
        
        # 绘制版权信息
        font = pygame.font.SysFont(None, 20)
        copyright_text = "© 2023 Your Name - All Rights Reserved"
        copyright_surface = font.render(copyright_text, True, WHITE)
        copyright_rect = copyright_surface.get_rect(
            center=(self.panel_rect.centerx, self.panel_rect.bottom - 30)
        )
        self.screen.blit(copyright_surface, copyright_rect)


class SettingsMenu(Menu):
    """设置菜单类"""
    
    def __init__(self, screen, save_callback=None):
        """
        初始化设置菜单
        
        Args:
            screen (pygame.Surface): 游戏窗口表面
            save_callback (function, optional): 保存设置回调
        """
        super().__init__(screen)
        self.title = "游戏设置"
        
        # 保存按钮
        self.buttons.append(Button(
            self.panel_rect.centerx - 100, self.panel_rect.bottom - 70,
            200, 50,
            "保存设置", save_callback or self.on_close,
            bg_color=(50, 150, 50),
            highlight_color=(70, 200, 70)
        ))
        
        # TODO: 添加更多设置控件（滑块、选择框等）
    
    def render(self):
        """渲染设置菜单"""
        super().render()
        
        if not self.is_active:
            return
        
        # 绘制设置选项
        font = pygame.font.SysFont(None, 28)
        
        # 音效设置
        text = font.render("音效音量:", True, WHITE)
        self.screen.blit(text, (self.panel_rect.x + 50, self.panel_rect.y + 100))
        
        # 音乐设置
        text = font.render("音乐音量:", True, WHITE)
        self.screen.blit(text, (self.panel_rect.x + 50, self.panel_rect.y + 150))
        
        # 游戏速度
        text = font.render("游戏速度:", True, WHITE)
        self.screen.blit(text, (self.panel_rect.x + 50, self.panel_rect.y + 200))
        
        # AI难度
        text = font.render("AI难度:", True, WHITE)
        self.screen.blit(text, (self.panel_rect.x + 50, self.panel_rect.y + 250))


class PauseMenu(Menu):
    """暂停菜单类"""
    
    def __init__(self, screen, resume_callback=None, quit_callback=None):
        """
        初始化暂停菜单
        
        Args:
            screen (pygame.Surface): 游戏窗口表面
            resume_callback (function, optional): 继续游戏回调
            quit_callback (function, optional): 退出游戏回调
        """
        super().__init__(screen)
        self.title = "游戏暂停"
        
        # 继续游戏按钮
        self.buttons.append(Button(
            self.panel_rect.centerx - 100, self.panel_rect.y + 120,
            200, 50,
            "继续游戏", resume_callback or self.on_close,
            bg_color=(50, 150, 50),
            highlight_color=(70, 200, 70)
        ))
        
        # 设置按钮
        self.buttons.append(Button(
            self.panel_rect.centerx - 100, self.panel_rect.y + 190,
            200, 50,
            "设置", None,  # TODO: 打开设置菜单
            bg_color=(50, 50, 150),
            highlight_color=(70, 70, 200)
        ))
        
        # 退出游戏按钮
        self.buttons.append(Button(
            self.panel_rect.centerx - 100, self.panel_rect.y + 260,
            200, 50,
            "退出游戏", quit_callback or self.on_close,
            bg_color=(150, 50, 50),
            highlight_color=(200, 70, 70)
        ))
    
    def render(self):
        """渲染暂停菜单"""
        super().render()
        
        if not self.is_active:
            return
        
        # 绘制暂停图标
        icon_size = 80
        pause_icon = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
        bar_width = 20
        bar_height = 60
        bar_spacing = 20
        
        # 绘制两个暂停条
        pygame.draw.rect(pause_icon, WHITE, 
                        (bar_spacing, (icon_size - bar_height) // 2, 
                         bar_width, bar_height))
        pygame.draw.rect(pause_icon, WHITE, 
                        (bar_spacing * 2 + bar_width, (icon_size - bar_height) // 2, 
                         bar_width, bar_height))
        
        # 绘制到屏幕
        icon_rect = pause_icon.get_rect(midtop=(self.panel_rect.centerx, self.panel_rect.y + 20))
        self.screen.blit(pause_icon, icon_rect)


class HelpMenu(Menu):
    """帮助菜单类"""
    
    def __init__(self, screen):
        """
        初始化帮助菜单
        
        Args:
            screen (pygame.Surface): 游戏窗口表面
        """
        super().__init__(screen)
        self.title = "游戏帮助"
        
        # 返回按钮
        self.buttons.append(Button(
            self.panel_rect.centerx - 100, self.panel_rect.bottom - 70,
            200, 50,
            "返回", self.on_close,
            bg_color=(50, 150, 50),
            highlight_color=(70, 200, 70)
        ))
        
        # 帮助内容
        self.help_text = [
            "德州扑克规则:",
            "1. 每位玩家发两张底牌。",
            "2. 进行第一轮下注。",
            "3. 发三张公共牌（翻牌）。",
            "4. 进行第二轮下注。",
            "5. 发第四张公共牌（转牌）。",
            "6. 进行第三轮下注。",
            "7. 发第五张公共牌（河牌）。",
            "8. 最后一轮下注。",
            "9. 摊牌，最强手牌获胜。",
            "",
            "牌型（从高到低）:",
            "皇家同花顺 > 同花顺 > 四条 > 葫芦 > 同花 > 顺子 > 三条 > 两对 > 一对 > 高牌"
        ]
    
    def render(self):
        """渲染帮助菜单"""
        super().render()
        
        if not self.is_active:
            return
        
        # 绘制帮助内容
        font = pygame.font.SysFont(None, 24)
        line_height = 28
        start_y = self.panel_rect.y + 90
        
        for i, text in enumerate(self.help_text):
            if text:  # 跳过空行
                text_surface = font.render(text, True, WHITE)
                self.screen.blit(text_surface, (self.panel_rect.x + 40, start_y + i * line_height))
            else:
                # 空行只增加半行距
                start_y -= line_height // 2


class GameOverMenu(Menu):
    """游戏结束菜单类"""
    
    def __init__(self, screen, is_win=False, restart_callback=None, quit_callback=None):
        """
        初始化游戏结束菜单
        
        Args:
            screen (pygame.Surface): 游戏窗口表面
            is_win (bool, optional): 是否胜利
            restart_callback (function, optional): 重新开始回调
            quit_callback (function, optional): 退出游戏回调
        """
        super().__init__(screen)
        self.is_win = is_win
        self.title = "游戏结束"
        
        # 重新开始按钮
        self.buttons.append(Button(
            self.panel_rect.centerx - 100, self.panel_rect.y + 180,
            200, 50,
            "重新开始", restart_callback or self.on_close,
            bg_color=(50, 150, 50),
            highlight_color=(70, 200, 70)
        ))
        
        # 退出游戏按钮
        self.buttons.append(Button(
            self.panel_rect.centerx - 100, self.panel_rect.y + 250,
            200, 50,
            "退出游戏", quit_callback or self.on_close,
            bg_color=(150, 50, 50),
            highlight_color=(200, 70, 70)
        ))
    
    def render(self):
        """渲染游戏结束菜单"""
        super().render()
        
        if not self.is_active:
            return
        
        # 显示结果信息
        result_text = "恭喜你赢了！" if self.is_win else "游戏结束，你输了！"
        font = pygame.font.SysFont(None, 36)
        result_surface = font.render(result_text, True, GOLD if self.is_win else WHITE)
        result_rect = result_surface.get_rect(center=(self.panel_rect.centerx, self.panel_rect.y + 120))
        self.screen.blit(result_surface, result_rect)
