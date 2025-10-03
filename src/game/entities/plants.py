import pygame
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .projectiles import Pea

class Plant:
    """植物基类"""
    
    def __init__(self, row: int, col: int, lawn_left: int, lawn_top: int, grid_size: int):
        self.row = row
        self.col = col
        self.x = lawn_left + col * grid_size
        self.y = lawn_top + row * grid_size
        self.health = 100
        self.attack_cooldown = 0
        self.grid_size = grid_size
    
    def update(self, zombies: List['Zombie'], peas: List['Pea']):
        """更新植物状态"""
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
    
    def draw(self, screen: pygame.Surface, image: pygame.Surface = None):
        """绘制植物"""
        if image:
            screen.blit(image, (self.x + 10, self.y + 10))
        else:
            # 默认绘制（贴图加载失败时使用）
            pygame.draw.circle(screen, (0, 128, 0), 
                             (self.x + self.grid_size//2, self.y + self.grid_size//2), 20)


class Peashooter(Plant):
    """豌豆射手"""
    
    def __init__(self, row: int, col: int, lawn_left: int, lawn_top: int, grid_size: int):
        super().__init__(row, col, lawn_left, lawn_top, grid_size)
        self.attack_cooldown = 60  # 攻击冷却时间
    
    def update(self, zombies: List['Zombie'], peas: List['Pea']):
        """更新豌豆射手状态"""
        super().update(zombies, peas)
        
        self.attack_cooldown -= 1
        if self.attack_cooldown <= 0:
            # 检查该行是否有僵尸
            for zombie in zombies:
                if zombie.row == self.row and zombie.x > self.x:
                    # 发射豌豆
                    from .projectiles import Pea
                    peas.append(Pea(self.x + self.grid_size//2, 
                                  self.y + self.grid_size//2, 
                                  self.row))
                    self.attack_cooldown = 60
                    break
    
    def draw(self, screen: pygame.Surface, image: pygame.Surface = None):
        """绘制豌豆射手"""
        super().draw(screen, image)


class Sunflower(Plant):
    """向日葵"""
    
    def __init__(self, row: int, col: int, lawn_left: int, lawn_top: int, grid_size: int):
        super().__init__(row, col, lawn_left, lawn_top, grid_size)
        self.sun_cooldown = 300  # 阳光生成冷却时间
    
    def update(self, zombies: List['Zombie'], peas: List['Pea']):
        """更新向日葵状态"""
        super().update(zombies, peas)
        
        self.sun_cooldown -= 1
        if self.sun_cooldown <= 0:
            # 生成阳光（这里只是标记，实际生成由GameEngine处理）
            self.sun_cooldown = 300
            return 25  # 返回阳光值
        return 0
    
    def draw(self, screen: pygame.Surface, image: pygame.Surface = None):
        """绘制向日葵"""
        super().draw(screen, image)
