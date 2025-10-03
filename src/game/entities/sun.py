import pygame
import random

class Sun:
    """阳光类"""
    
    def __init__(self, screen_width: int):
        self.x = random.randint(100, screen_width - 50)  # 从lawn_left开始
        self.y = 0
        self.target_y = random.randint(100, 400)
        self.speed = 1
        self.value = 25
        self.timer = 300  # 存在时间
    
    def update(self) -> bool:
        """更新阳光位置，返回是否应该被移除"""
        # 移动到目标位置
        if self.y < self.target_y:
            self.y += self.speed
        
        # 减少存在时间
        self.timer -= 1
        return self.timer <= 0
    
    def draw(self, screen: pygame.Surface, image: pygame.Surface = None):
        """绘制阳光"""
        if image:
            screen.blit(image, (self.x - 20, self.y - 20))
        else:
            # 默认绘制（贴图加载失败时使用）
            pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), 20)
    
    def is_clicked(self, mouse_x: int, mouse_y: int) -> bool:
        """检查是否被点击"""
        distance_squared = (mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2
        return distance_squared <= 400  # 20像素半径内
