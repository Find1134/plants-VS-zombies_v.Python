import pygame
from ..utils.config import get_font

class Button:
    """按钮类，用于创建可交互的UI按钮"""
    
    def __init__(self, x, y, width, height, text, 
                 color=(0, 128, 0), 
                 hover_color=(100, 200, 100),
                 text_color=(0, 0, 0),
                 border_color=(0, 0, 0),
                 border_width=2):
        """
        初始化按钮
        
        Args:
            x, y: 按钮位置
            width, height: 按钮尺寸
            text: 按钮文本
            color: 正常状态颜色
            hover_color: 悬停状态颜色
            text_color: 文本颜色
            border_color: 边框颜色
            border_width: 边框宽度
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width
        self.is_hovered = False
        self.font = get_font(20)
        
    def draw(self, screen):
        """绘制按钮"""
        # 绘制按钮背景
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        
        # 绘制边框
        if self.border_width > 0:
            pygame.draw.rect(screen, self.border_color, self.rect, self.border_width)
        
        # 绘制文本
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        """检查鼠标是否悬停在按钮上"""
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def is_clicked(self, pos, event):
        """检查按钮是否被点击"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False
    
    def update_text(self, new_text):
        """更新按钮文本"""
        self.text = new_text


class ToggleButton(Button):
    """切换按钮，可以在两种状态之间切换"""
    
    def __init__(self, x, y, width, height, text, 
                 on_text=None, off_text=None,
                 on_color=(100, 200, 100), 
                 off_color=(200, 100, 100),
                 **kwargs):
        """
        初始化切换按钮
        
        Args:
            on_text: 开启状态文本
            off_text: 关闭状态文本
            on_color: 开启状态颜色
            off_color: 关闭状态颜色
        """
        super().__init__(x, y, width, height, text, **kwargs)
        self.on_text = on_text or text
        self.off_text = off_text or text
        self.on_color = on_color
        self.off_color = off_color
        self.is_on = True
        
    def toggle(self):
        """切换按钮状态"""
        self.is_on = not self.is_on
        self.text = self.on_text if self.is_on else self.off_text
        self.color = self.on_color if self.is_on else self.off_color
        
    def draw(self, screen):
        """绘制切换按钮"""
        self.color = self.on_color if self.is_on else self.off_color
        super().draw(screen)
