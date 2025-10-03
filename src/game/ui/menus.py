import pygame
from .buttons import Button, ToggleButton
from ..utils.config import get_font, title_font, GAME_CONFIG

class BaseMenu:
    """基础菜单类"""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.buttons = []
        self.background_color = (135, 206, 235)  # 天空蓝
        
    def handle_event(self, event, mouse_pos):
        """处理事件"""
        for button in self.buttons:
            if button.is_clicked(mouse_pos, event):
                return self.on_button_click(button)
        return None
    
    def on_button_click(self, button):
        """按钮点击回调，子类需要重写"""
        raise NotImplementedError("子类必须实现 on_button_click 方法")
    
    def update(self, mouse_pos):
        """更新菜单状态"""
        for button in self.buttons:
            button.check_hover(mouse_pos)
    
    def draw(self, screen):
        """绘制菜单"""
        screen.fill(self.background_color)
        for button in self.buttons:
            button.draw(screen)


class MainMenu(BaseMenu):
    """主菜单"""
    
    def __init__(self, screen_width, screen_height, game_data):
        super().__init__(screen_width, screen_height)
        self.game_data = game_data
        self.create_buttons()
        
    def create_buttons(self):
        """创建主菜单按钮"""
        center_x = self.screen_width // 2
        
        # 标题
        self.title_text = "植物大战僵尸"
        
        # 按钮
        self.adventure_button = Button(center_x - 100, 200, 200, 50, "冒险模式")
        self.settings_button = Button(center_x - 100, 270, 200, 50, "设置")
        self.quit_button = Button(center_x - 100, 340, 200, 50, "退出游戏")
        
        self.buttons = [self.adventure_button, self.settings_button, self.quit_button]
    
    def on_button_click(self, button):
        """处理按钮点击"""
        if button == self.adventure_button:
            return "level_select"
        elif button == self.settings_button:
            return "settings"
        elif button == self.quit_button:
            return "quit"
        return None
    
    def draw(self, screen):
        """绘制主菜单"""
        super().draw(screen)
        
        # 绘制标题
        title_surface = title_font.render(self.title_text, True, (0, 128, 0))
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 100))
        screen.blit(title_surface, title_rect)
        
        # 绘制游戏数据
        font = get_font(18)
        level_text = font.render(f"当前进度: 第{self.game_data['current_level']}关", True, (0, 0, 0))
        screen.blit(level_text, (self.screen_width - 250, 20))
        
        score_text = font.render(f"总分数: {self.game_data['score']}", True, (0, 0, 0))
        screen.blit(score_text, (self.screen_width - 250, 50))
        
        # 版本信息
        version_text = font.render("当前版本号：1.00正式版", True, (0, 128, 0))
        screen.blit(version_text, (20, self.screen_height - 60))
        
        warning_text = font.render("本游戏免费，若需要付费，请找商家退还钱财并举报该商家", True, (255, 0, 0))
        screen.blit(warning_text, (20, self.screen_height - 30))


class LevelSelectMenu(BaseMenu):
    """关卡选择菜单"""
    
    def __init__(self, screen_width, screen_height, game_data, difficulty):
        super().__init__(screen_width, screen_height)
        self.game_data = game_data
        self.difficulty = difficulty
        self.level_buttons = []
        self.create_buttons()
        
    def create_buttons(self):
        """创建关卡选择按钮"""
        self.back_button = Button(20, 20, 100, 40, "返回")
        self.buttons = [self.back_button]
        
        # 创建关卡按钮 (6列5行)
        for i in range(30):
            row = i // 6
            col = i % 6
            level_button = Button(150 + col * 120, 100 + row * 60, 100, 40, f"关卡 {i+1}")
            self.level_buttons.append(level_button)
            if i + 1 <= self.game_data["unlocked_levels"]:
                self.buttons.append(level_button)
    
    def on_button_click(self, button):
        """处理按钮点击"""
        if button == self.back_button:
            return "back"
        elif button in self.level_buttons:
            level_index = self.level_buttons.index(button) + 1
            return f"level_{level_index}"
        return None
    
    def draw(self, screen):
        """绘制关卡选择菜单"""
        super().draw(screen)
        
        # 绘制标题
        title_text = get_font(24).render("选择关卡", True, (0, 128, 0))
        screen.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 50))
        
        # 显示当前难度
        difficulty_text = get_font(18).render(f"难度: {self.difficulty}", True, (0, 0, 0))
        screen.blit(difficulty_text, (self.screen_width - 200, 20))
        
        # 绘制锁定关卡
        for i, level_button in enumerate(self.level_buttons):
            if i + 1 > self.game_data["unlocked_levels"]:
                locked_rect = pygame.Rect(level_button.rect)
                pygame.draw.rect(screen, (200, 200, 200), locked_rect)
                pygame.draw.rect(screen, (0, 0, 0), locked_rect, 2)
                lock_text = get_font(18).render(f"关卡 {i+1}", True, (0, 0, 0))
                text_rect = lock_text.get_rect(center=locked_rect.center)
                screen.blit(lock_text, text_rect)


class SettingsMenu(BaseMenu):
    """设置菜单"""
    
    def __init__(self, screen_width, screen_height, game_settings):
        super().__init__(screen_width, screen_height)
        self.game_settings = game_settings
        self.create_buttons()
        
    def create_buttons(self):
        """创建设置按钮"""
        center_x = self.screen_width // 2
        
        self.back_button = Button(20, 20, 100, 40, "返回")
        self.difficulty_button = ToggleButton(
            center_x - 150, 150, 300, 40, 
            f"难度: {self.game_settings['difficulty']}",
            on_text="难度: easy", off_text="难度: normal"
        )
        self.fullscreen_button = ToggleButton(
            center_x - 150, 210, 300, 40,
            f"全屏: {'开' if self.game_settings['fullscreen'] else '关'}",
            on_text="全屏: 开", off_text="全屏: 关"
        )
        
        self.buttons = [
            self.back_button, 
            self.difficulty_button, 
            self.fullscreen_button
        ]
        
        # 设置初始状态
        if self.game_settings['difficulty'] == 'easy':
            self.difficulty_button.is_on = True
        else:
            self.difficulty_button.is_on = False
    
    def on_button_click(self, button):
        """处理按钮点击"""
        if button == self.back_button:
            return "back"
        elif button == self.difficulty_button:
            button.toggle()
            return "toggle_difficulty"
        elif button == self.fullscreen_button:
            button.toggle()
            return "toggle_fullscreen"
        return None
    
    def draw(self, screen):
        """绘制设置菜单"""
        super().draw(screen)
        
        # 绘制标题
        title_text = get_font(24).render("游戏设置", True, (0, 128, 0))
        screen.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 50))
        
        # 提示信息
        tip_text = get_font(16).render("切换难度不会丢失进度，每个难度有独立的存档", True, (0, 0, 255))
        screen.blit(tip_text, (self.screen_width // 2 - tip_text.get_width() // 2, 400))


class PauseMenu(BaseMenu):
    """暂停菜单"""
    
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self.background_color = (0, 0, 0, 128)  # 半透明黑色
        self.create_buttons()
        
    def create_buttons(self):
        """创建暂停菜单按钮"""
        center_x = self.screen_width // 2
        
        self.restart_button = Button(center_x - 100, self.screen_height // 2 - 80, 200, 40, "重新开始游戏")
        self.settings_button = Button(center_x - 100, self.screen_height // 2 - 20, 200, 40, "更改游戏设置")
        self.resume_button = Button(center_x - 100, self.screen_height // 2 + 40, 200, 40, "回到游戏")
        self.main_menu_button = Button(center_x - 100, self.screen_height // 2 + 100, 200, 40, "返回主菜单")
        
        self.buttons = [
            self.restart_button, 
            self.settings_button, 
            self.resume_button, 
            self.main_menu_button
        ]
    
    def on_button_click(self, button):
        """处理按钮点击"""
        if button == self.restart_button:
            return "restart"
        elif button == self.settings_button:
            return "settings"
        elif button == self.resume_button:
            return "resume"
        elif button == self.main_menu_button:
            return "main_menu"
        return None
    
    def draw(self, screen):
        """绘制暂停菜单"""
        # 半透明背景
        s = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        s.fill(self.background_color)
        screen.blit(s, (0, 0))
        
        # 菜单背景
        menu_rect = pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 - 150, 300, 300)
        pygame.draw.rect(screen, (255, 255, 255), menu_rect)
        pygame.draw.rect(screen, (0, 0, 0), menu_rect, 2)
        
        # 标题
        title_text = get_font(24).render("游戏暂停", True, (0, 0, 0))
        screen.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, self.screen_height // 2 - 120))
        
        # 绘制按钮
        for button in self.buttons:
            button.draw(screen)


class LevelCompleteMenu(BaseMenu):
    """关卡完成菜单"""
    
    def __init__(self, screen_width, screen_height, current_level, zombies_killed, total_zombies):
        super().__init__(screen_width, screen_height)
        self.current_level = current_level
        self.zombies_killed = zombies_killed
        self.total_zombies = total_zombies
        self.create_buttons()
        
    def create_buttons(self):
        """创建关卡完成菜单按钮"""
        center_x = self.screen_width // 2
        
        self.next_level_button = Button(center_x - 100, self.screen_height // 2 + 20, 200, 40, "下一关")
        self.main_menu_button = Button(center_x - 100, self.screen_height // 2 + 80, 200, 40, "返回主菜单")
        
        self.buttons = [self.next_level_button, self.main_menu_button]
    
    def on_button_click(self, button):
        """处理按钮点击"""
        if button == self.next_level_button:
            return "next_level"
        elif button == self.main_menu_button:
            return "main_menu"
        return None
    
    def draw(self, screen):
        """绘制关卡完成菜单"""
        # 半透明背景
        s = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        screen.blit(s, (0, 0))
        
        # 完成菜单背景
        menu_rect = pygame.Rect(self.screen_width // 2 - 200, self.screen_height // 2 - 150, 400, 300)
        pygame.draw.rect(screen, (255, 255, 255), menu_rect)
        pygame.draw.rect(screen, (0, 128, 0), menu_rect, 4)
        
        # 标题
        title_text = get_font(24).render("关卡完成！", True, (0, 128, 0))
        screen.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, self.screen_height // 2 - 120))
        
        # 关卡信息
        level_text = get_font(20).render(f"恭喜通过第 {self.current_level} 关", True, (0, 0, 0))
        screen.blit(level_text, (self.screen_width // 2 - level_text.get_width() // 2, self.screen_height // 2 - 70))
        
        # 统计数据
        stats_text = get_font(18).render(f"本关击杀僵尸: {self.zombies_killed}/{self.total_zombies}", True, (0, 0, 0))
        screen.blit(stats_text, (self.screen_width // 2 - stats_text.get_width() // 2, self.screen_height // 2 - 30))
        
        # 绘制按钮
        for button in self.buttons:
            button.draw(screen)
