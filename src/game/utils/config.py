import pygame
import os

# 字体设置
def get_font(size):
    """
    获取字体对象
    
    Args:
        size: 字体大小
    
    Returns:
        pygame.font.Font: 字体对象
    """
    # 尝试多种中文字体
    font_paths = [
        "assets/fonts/simkai.ttf",  # 楷体
        "assets/fonts/msyh.ttc",    # 微软雅黑  
        "assets/fonts/simhei.ttf",  # 黑体
        "assets/fonts/simsun.ttc",  # 宋体
        "C:/Windows/Fonts/simkai.ttf",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc"
    ]
    
    for font_path in font_paths:
        try:
            return pygame.font.Font(font_path, size)
        except:
            continue
    
    # 如果都失败，使用系统默认字体
    print("警告：未找到中文字体，使用系统默认字体")
    return pygame.font.SysFont(None, size)

# 标题字体
title_font = get_font(48)

# 游戏配置
GAME_CONFIG = {
    "screen_width": 900,
    "screen_height": 600,
    "grid_size": 80,
    "grid_rows": 5, 
    "grid_cols": 9,
    "lawn_left": 100,
    "lawn_top": 100,
    "fps": 60,
    "sun_rate": 5000,  # 阳光生成间隔（毫秒）
    "zombie_spawn_rate": {
        "easy": 0.003,
        "normal": 0.005, 
        "hard": 0.008
    },
    "zombie_health": {
        "easy": 80,
        "normal": 100,
        "hard": 150
    },
    "zombie_speed": {
        "easy": 0.3,
        "normal": 0.5,
        "hard": 0.7
    }
}

# 游戏设置
GAME_SETTINGS = {
    "difficulty": "normal",  # easy, normal, hard
    "fullscreen": False,
    "music_volume": 0.5,
    "sound_volume": 0.5,
    "music_enabled": True,
    "sound_enabled": True
}

# 颜色定义
COLORS = {
    "green": (0, 128, 0),
    "light_green": (100, 200, 100),
    "brown": (139, 69, 19),
    "yellow": (255, 255, 0),
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "gray": (200, 200, 200),
    "sky_blue": (135, 206, 235)
}

def get_zombies_per_level(difficulty, level):
    """
    根据难度和关卡获取僵尸数量
    
    Args:
        difficulty: 难度级别
        level: 关卡数
    
    Returns:
        int: 僵尸数量
    """
    multipliers = {
        "easy": 5,
        "normal": 15, 
        "hard": 25
    }
    return level * multipliers.get(difficulty, 15)

def update_game_settings(new_settings):
    """
    更新游戏设置
    
    Args:
        new_settings: 新的设置字典
    """
    global GAME_SETTINGS
    GAME_SETTINGS.update(new_settings)

def get_game_setting(key, default=None):
    """
    获取游戏设置
    
    Args:
        key: 设置键
        default: 默认值
    
    Returns:
        设置值
    """
    return GAME_SETTINGS.get(key, default)