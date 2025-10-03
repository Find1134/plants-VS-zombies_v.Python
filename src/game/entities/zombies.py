import pygame
from typing import List
from .plants import Plant

class Zombie:
    """僵尸类"""
    
    def __init__(self, row: int, screen_width: int, lawn_top: int, grid_size: int, difficulty: str = "normal"):
        self.row = row
        self.x = screen_width
        self.y = lawn_top + row * grid_size
        self.grid_size = grid_size
        
        # 根据难度调整属性
        if difficulty == "easy":
            self.health = 80
            self.speed = 0.3
        elif difficulty == "normal":
            self.health = 100
            self.speed = 0.5
        else:  # hard
            self.health = 150
            self.speed = 0.7
            
        self.attack_cooldown = 0
        self.max_health = self.health
    
    def update(self, plants: List[Plant]) -> bool:
        """更新僵尸状态，返回是否到达房子"""
        plant_in_front = False
        
        # 检查前方是否有植物
        for plant in plants:
            if plant.row == self.row and abs(plant.x - self.x) < self.grid_size:
                plant_in_front = True
                if self.attack_cooldown <= 0:
                    plant.health -= 5
                    self.attack_cooldown = 30
                break
                
        # 如果没有植物阻挡，向前移动
        if not plant_in_front:
            self.x -= self.speed
            
        # 更新攻击冷却
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        # 检查是否到达房子（左侧边界）
        return self.x < 100  # lawn_left
    
    def draw(self, screen: pygame.Surface, image: pygame.Surface = None):
        """绘制僵尸"""
        if image:
            screen.blit(image, (self.x, self.y))
        else:
            # 默认绘制（贴图加载失败时使用）
            pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, 40, self.grid_size))
        
        # 绘制生命条
        bar_width = 40
        bar_height = 5
        health_ratio = self.health / self.max_health
        
        # 背景（红色）
        pygame.draw.rect(screen, (255, 0, 0), 
                        (self.x, self.y - 10, bar_width, bar_height))
        # 生命值（绿色）
        pygame.draw.rect(screen, (0, 255, 0), 
                        (self.x, self.y - 10, bar_width * health_ratio, bar_height))
    
    def take_damage(self, damage: int):
        """受到伤害"""
        self.health -= damage
        return self.health <= 0
