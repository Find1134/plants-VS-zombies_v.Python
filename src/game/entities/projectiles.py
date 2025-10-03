import pygame
from typing import List

class Pea:
    """豌豆类"""
    
    def __init__(self, x: int, y: int, row: int):
        self.x = x
        self.y = y
        self.row = row
        self.speed = 5
        self.damage = 20
    
    def update(self, zombies: List['Zombie']) -> bool:
        """更新豌豆位置，返回是否应该被移除"""
        self.x += self.speed
        
        # 检查是否击中僵尸
        for zombie in zombies:
            if (zombie.row == self.row and 
                abs(zombie.x - self.x) < 30 and 
                abs(zombie.y + 40 - self.y) < 30):  # 40是僵尸高度的一半
                zombie.take_damage(self.damage)
                return True  # 击中僵尸，移除豌豆
        
        # 检查是否超出屏幕
        if self.x > 900:  # 屏幕宽度
            return True  # 超出屏幕，移除豌豆
            
        return False
    
    def draw(self, screen: pygame.Surface, image: pygame.Surface = None):
        """绘制豌豆"""
        if image:
            screen.blit(image, (self.x - 8, self.y - 8))
        else:
            # 默认绘制（贴图加载失败时使用）
            pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), 8)
