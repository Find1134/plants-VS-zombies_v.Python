import json
import os
from typing import Dict, Any
from .level_data import get_level_data

class LevelManager:
    """关卡管理器"""
    
    def __init__(self, save_dir: str = "data/save_data"):
        self.save_dir = save_dir
        self.ensure_save_directory()
        self.max_level = 30
    
    def ensure_save_directory(self):
        """确保保存目录存在"""
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
    
    def get_save_file_path(self, difficulty: str) -> str:
        """获取存档文件路径"""
        return os.path.join(self.save_dir, f"game_save_{difficulty}.json")
    
    def load_game_data(self, difficulty: str) -> Dict[str, Any]:
        """加载游戏数据"""
        save_file = self.get_save_file_path(difficulty)
        
        if os.path.exists(save_file):
            try:
                with open(save_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, KeyError):
                pass
        
        # 返回默认数据
        return {
            "current_level": 1,
            "score": 0,
            "unlocked_levels": 1,
            "total_sun_collected": 0,
            "total_zombies_killed": 0
        }
    
    def save_game_data(self, difficulty: str, game_data: Dict[str, Any]):
        """保存游戏数据"""
        save_file = self.get_save_file_path(difficulty)
        
        try:
            with open(save_file, 'w', encoding='utf-8') as f:
                json.dump(game_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存游戏数据失败: {e}")
            return False
    
    def complete_level(self, level: int, difficulty: str) -> bool:
        """完成关卡"""
        if level > self.max_level:
            return False
        
        game_data = self.load_game_data(difficulty)
        
        # 更新游戏数据
        game_data["current_level"] = level + 1
        game_data["unlocked_levels"] = max(game_data["unlocked_levels"], level + 1)
        
        # 保存更新后的数据
        return self.save_game_data(difficulty, game_data)
    
    def get_unlocked_levels(self, difficulty: str) -> int:
        """获取已解锁的关卡数"""
        game_data = self.load_game_data(difficulty)
        return game_data.get("unlocked_levels", 1)
    
    def get_current_level(self, difficulty: str) -> int:
        """获取当前关卡"""
        game_data = self.load_game_data(difficulty)
        return game_data.get("current_level", 1)
    
    def reset_progress(self, difficulty: str):
        """重置游戏进度"""
        default_data = {
            "current_level": 1,
            "score": 0,
            "unlocked_levels": 1,
            "total_sun_collected": 0,
            "total_zombies_killed": 0
        }
        self.save_game_data(difficulty, default_data)
    
    def get_level_info(self, level: int, difficulty: str) -> Dict[str, Any]:
        """获取关卡信息"""
        level_data = get_level_data(level)
        if not level_data:
            return None
        
        # 根据难度调整僵尸数量
        if difficulty == "easy":
            zombie_count = level * 5
        elif difficulty == "normal":
            zombie_count = level * 15
        else:  # hard
            zombie_count = level * 25
        
        return {
            "level": level,
            "zombie_count": zombie_count,
            "description": level_data.description,
            "unlocked": level <= self.get_unlocked_levels(difficulty)
        }
    
    def get_all_levels_info(self, difficulty: str) -> list:
        """获取所有关卡信息"""
        levels_info = []
        for level in range(1, self.max_level + 1):
            levels_info.append(self.get_level_info(level, difficulty))
        return levels_info
