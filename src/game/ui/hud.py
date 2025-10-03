import pygame
from ..utils.config import get_font

class GameHUD:
    """游戏内HUD（抬头显示）"""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = get_font(20)
        
        # HUD元素位置
        self.hud_left = 20
        self.hud_top = 160
        self.line_height = 30
        
    def draw(self, screen, sun_count, score, current_level, zombies_killed, total_zombies, difficulty):
        """绘制HUD"""
        # 阳光计数
        sun_text = self.font.render(f"阳光: {sun_count}", True, (0, 0, 0))
        screen.blit(sun_text, (self.hud_left, self.hud_top))
        
        # 分数
        score_text = self.font.render(f"分数: {score}", True, (0, 0, 0))
        screen.blit(score_text, (self.hud_left, self.hud_top + self.line_height))
        
        # 关卡
        level_text = self.font.render(f"关卡: {current_level}", True, (0, 0, 0))
        screen.blit(level_text, (self.hud_left, self.hud_top + self.line_height * 2))
        
        # 僵尸进度
        zombies_text = self.font.render(f"僵尸: {zombies_killed}/{total_zombies}", True, (0, 0, 0))
        screen.blit(zombies_text, (self.hud_left, self.hud_top + self.line_height * 3))
        
        # 难度
        difficulty_text = self.font.render(f"难度: {difficulty}", True, (0, 0, 0))
        screen.blit(difficulty_text, (self.hud_left, self.hud_top + self.line_height * 4))
    
    def draw_plant_selection(self, screen, selected_plant, plant_images):
        """绘制植物选择区域"""
        # 豌豆射手选择框
        pygame.draw.rect(screen, (0, 128, 0), (20, 20, 50, 50))
        screen.blit(plant_images["peashooter"], (25, 25))
        
        # 向日葵选择框
        pygame.draw.rect(screen, (255, 255, 0), (20, 90, 50, 50))
        screen.blit(plant_images["sunflower"], (25, 95))
        
        # 绘制选中的植物边框
        if selected_plant == "peashooter":
            pygame.draw.rect(screen, (255, 255, 255), (15, 15, 60, 60), 3)
        elif selected_plant == "sunflower":
            pygame.draw.rect(screen, (255, 255, 255), (15, 85, 60, 60), 3)
    
    def draw_game_over(self, screen):
        """绘制游戏结束画面"""
        # 半透明背景
        s = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        screen.blit(s, (0, 0))
        
        # 游戏结束文本
        game_over_font = get_font(36)
        game_over_text = game_over_font.render("游戏结束! 僵尸吃掉了你的脑子!", True, (255, 0, 0))
        screen.blit(game_over_text, (self.screen_width // 2 - game_over_text.get_width() // 2, self.screen_height // 2))
        
        # 重新开始提示
        restart_font = get_font(20)
        restart_text = restart_font.render("按 R 键重新开始游戏", True, (255, 255, 255))
        screen.blit(restart_text, (self.screen_width // 2 - restart_text.get_width() // 2, self.screen_height // 2 + 50))