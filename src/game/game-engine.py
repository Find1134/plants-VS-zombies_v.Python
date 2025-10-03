import pygame
import random
from typing import List, Dict, Any
from .entities.plants import Plant, Peashooter, Sunflower
from .entities.zombies import Zombie
from .entities.projectiles import Pea
from .entities.sun import Sun
from .levels.level_manager import LevelManager

class GameEngine:
    """游戏引擎核心类，负责游戏逻辑和状态管理"""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.grid_size = 80
        self.grid_rows = 5
        self.grid_cols = 9
        self.lawn_left = 100
        self.lawn_top = 100
        
        # 游戏状态
        self.plants: List[Plant] = []
        self.zombies: List[Zombie] = []
        self.peas: List[Pea] = []
        self.suns: List[Sun] = []
        
        # 游戏数据
        self.sun_count = 100
        self.score = 0
        self.game_over = False
        self.is_paused = False
        
        # 时间控制
        self.last_sun_time = pygame.time.get_ticks()
        self.sun_rate = 5000  # 5秒生成一个阳光
        
        # 关卡管理
        self.level_manager = LevelManager()
        self.current_level = 1
        self.difficulty = "normal"
        
        # 关卡进度
        self.zombies_spawned = 0
        self.zombies_killed = 0
        self.total_zombies_for_level = 0
        
        # 选中的植物
        self.selected_plant = None
        
        self._calculate_zombies_for_level()
    
    def _calculate_zombies_for_level(self):
        """根据关卡和难度计算僵尸数量"""
        if self.difficulty == "easy":
            self.total_zombies_for_level = self.current_level * 5
        elif self.difficulty == "normal":
            self.total_zombies_for_level = self.current_level * 15
        else:  # hard
            self.total_zombies_for_level = self.current_level * 25
    
    def set_difficulty(self, difficulty: str):
        """设置游戏难度"""
        self.difficulty = difficulty
        self._calculate_zombies_for_level()
    
    def set_level(self, level: int):
        """设置当前关卡"""
        self.current_level = level
        self._calculate_zombies_for_level()
        self.reset_level()
    
    def reset_level(self):
        """重置当前关卡"""
        self.plants.clear()
        self.zombies.clear()
        self.peas.clear()
        self.suns.clear()
        self.sun_count = 100
        self.game_over = False
        self.zombies_spawned = 0
        self.zombies_killed = 0
        self.selected_plant = None
        self.last_sun_time = pygame.time.get_ticks()
    
    def update(self, current_time: int):
        """更新游戏状态"""
        if self.is_paused or self.game_over:
            return
        
        self._generate_sun(current_time)
        self._generate_zombies(current_time)
        self._update_plants()
        self._update_peas()
        self._update_zombies()
        self._update_suns()
        self._remove_dead_plants()
        self._check_level_complete()
    
    def _generate_sun(self, current_time: int):
        """生成阳光"""
        if current_time - self.last_sun_time > self.sun_rate:
            self.suns.append(Sun(self.screen_width))
            self.last_sun_time = current_time
    
    def _generate_zombies(self, current_time: int):
        """生成僵尸"""
        if self.zombies_spawned >= self.total_zombies_for_level:
            return
        
        # 根据难度调整生成率
        zombie_rate = 0.005
        if self.difficulty == "easy":
            zombie_rate = 0.003
        elif self.difficulty == "hard":
            zombie_rate = 0.008
        
        # 随着进度增加生成率
        progress = self.zombies_spawned / self.total_zombies_for_level
        adjusted_rate = zombie_rate * (1 + progress * 2)
        
        if random.random() < adjusted_rate:
            row = random.randint(0, self.grid_rows - 1)
            self.zombies.append(Zombie(row, self.screen_width, self.lawn_top, self.grid_size, self.difficulty))
            self.zombies_spawned += 1
    
    def _update_plants(self):
        """更新植物状态"""
        for plant in self.plants:
            plant.update(self.zombies, self.peas)
    
    def _update_peas(self):
        """更新豌豆状态"""
        for pea in self.peas[:]:
            if pea.update(self.zombies):
                self.peas.remove(pea)
    
    def _update_zombies(self):
        """更新僵尸状态"""
        for zombie in self.zombies[:]:
            if zombie.update(self.plants):
                self.game_over = True
            if zombie.health <= 0:
                self.zombies.remove(zombie)
                self.zombies_killed += 1
                self.score += 10
    
    def _update_suns(self):
        """更新阳光状态"""
        for sun in self.suns[:]:
            if sun.update():
                self.suns.remove(sun)
    
    def _remove_dead_plants(self):
        """移除死亡的植物"""
        for plant in self.plants[:]:
            if plant.health <= 0:
                self.plants.remove(plant)
    
    def _check_level_complete(self):
        """检查关卡是否完成"""
        if (self.zombies_killed >= self.total_zombies_for_level and 
            len(self.zombies) == 0):
            self.level_manager.complete_level(self.current_level, self.difficulty)
            return True
        return False
    
    def place_plant(self, row: int, col: int, plant_type: str) -> bool:
        """在指定位置放置植物"""
        if self.sun_count < 50:
            return False
        
        # 检查位置是否被占用
        for plant in self.plants:
            if plant.row == row and plant.col == col:
                return False
        
        if plant_type == "peashooter":
            self.plants.append(Peashooter(row, col, self.lawn_left, self.lawn_top, self.grid_size))
            self.sun_count -= 50
            return True
        elif plant_type == "sunflower":
            self.plants.append(Sunflower(row, col, self.lawn_left, self.lawn_top, self.grid_size))
            self.sun_count -= 50
            return True
        
        return False
    
    def collect_sun(self, sun_index: int) -> bool:
        """收集阳光"""
        if 0 <= sun_index < len(self.suns):
            sun = self.suns.pop(sun_index)
            self.sun_count += sun.value
            return True
        return False
    
    def get_grid_position(self, x: int, y: int) -> tuple:
        """获取鼠标点击的网格位置"""
        if (self.lawn_left <= x <= self.lawn_left + self.grid_cols * self.grid_size and
            self.lawn_top <= y <= self.lawn_top + self.grid_rows * self.grid_size):
            col = (x - self.lawn_left) // self.grid_size
            row = (y - self.lawn_top) // self.grid_size
            return row, col
        return None, None
    
    def check_sun_click(self, x: int, y: int) -> int:
        """检查是否点击了阳光，返回阳光索引"""
        for i, sun in enumerate(self.suns):
            if ((x - sun.x) ** 2 + (y - sun.y) ** 2) <= 400:  # 20像素半径
                return i
        return -1
    
    def pause(self):
        """暂停游戏"""
        self.is_paused = True
    
    def resume(self):
        """恢复游戏"""
        self.is_paused = False
    
    def get_game_state(self) -> Dict[str, Any]:
        """获取游戏状态"""
        return {
            'sun_count': self.sun_count,
            'score': self.score,
            'current_level': self.current_level,
            'zombies_killed': self.zombies_killed,
            'total_zombies': self.total_zombies_for_level,
            'game_over': self.game_over,
            'is_paused': self.is_paused,
            'difficulty': self.difficulty
        }
