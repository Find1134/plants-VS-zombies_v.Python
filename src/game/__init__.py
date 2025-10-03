"""
植物大战僵尸 Python 版 - 游戏核心模块
"""

from .game_engine import GameEngine
from .entities.plants import Plant, Peashooter, Sunflower
from .entities.zombies import Zombie
from .entities.projectiles import Pea
from .entities.sun import Sun
from .levels.level_manager import LevelManager

__all__ = [
    'GameEngine',
    'Plant', 'Peashooter', 'Sunflower',
    'Zombie',
    'Pea',
    'Sun',
    'LevelManager'
]

__version__ = "1.0.0"
