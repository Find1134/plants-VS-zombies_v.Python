import os
import json
import pygame

def ensure_directory(directory_path):
    """确保目录存在，如果不存在则创建"""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def load_game_data(difficulty="normal"):
    """
    加载游戏数据
    
    Args:
        difficulty: 难度级别 ('easy', 'normal', 'hard')
    
    Returns:
        dict: 游戏数据
    """
    data_file = f"data/save_data/game_save_{difficulty}.json"
    
    # 确保数据目录存在
    ensure_directory("data/save_data")
    
    if os.path.exists(data_file):
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"加载游戏数据失败: {e}")
    
    # 返回默认数据
    return {
        "current_level": 1,
        "score": 0,
        "unlocked_levels": 1,
        "total_sun_collected": 0,
        "total_zombies_killed": 0
    }

def save_game_data(game_data, difficulty="normal"):
    """
    保存游戏数据
    
    Args:
        game_data: 游戏数据字典
        difficulty: 难度级别
    """
    data_file = f"data/save_data/game_save_{difficulty}.json"
    
    try:
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(game_data, f, ensure_ascii=False, indent=2)
        return True
    except IOError as e:
        print(f"保存游戏数据失败: {e}")
        return False

def load_image(path, default_color=None, default_size=(40, 40)):
    """
    加载图片，如果失败则创建默认图形
    
    Args:
        path: 图片路径
        default_color: 默认颜色（如果图片加载失败）
        default_size: 默认尺寸
    
    Returns:
        pygame.Surface: 图片表面
    """
    try:
        image = pygame.image.load(path)
        return pygame.transform.scale(image, default_size)
    except (pygame.error, FileNotFoundError):
        print(f"警告：无法加载贴图 {path}，使用默认图形")
        # 创建默认图形
        surf = pygame.Surface(default_size, pygame.SRCALPHA)
        if default_color:
            pygame.draw.circle(surf, default_color, 
                             (default_size[0]//2, default_size[1]//2), 
                             default_size[0]//2 - 5)
        return surf

def load_config(config_file="data/config/game_config.json"):
    """
    加载游戏配置
    
    Args:
        config_file: 配置文件路径
    
    Returns:
        dict: 配置数据
    """
    ensure_directory("data/config")
    
    default_config = {
        "screen_width": 900,
        "screen_height": 600,
        "grid_size": 80,
        "grid_rows": 5,
        "grid_cols": 9,
        "lawn_left": 100,
        "lawn_top": 100,
        "fps": 60
    }
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                # 合并配置，用户配置覆盖默认配置
                return {**default_config, **user_config}
        except (json.JSONDecodeError, IOError) as e:
            print(f"加载配置文件失败: {e}")
    
    return default_config

def save_config(config_data, config_file="data/config/game_config.json"):
    """
    保存游戏配置
    
    Args:
        config_data: 配置数据
        config_file: 配置文件路径
    """
    ensure_directory("data/config")
    
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)
        return True
    except IOError as e:
        print(f"保存配置文件失败: {e}")
        return False