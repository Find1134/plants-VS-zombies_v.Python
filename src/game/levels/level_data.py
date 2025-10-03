from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class LevelData:
    """关卡数据类"""
    level: int
    description: str
    background: str = "default"
    music: str = "gameplay"
    available_plants: tuple = ("peashooter", "sunflower")

# 关卡数据配置
LEVELS_DATA = {
    1: LevelData(1, "欢迎来到植物大战僵尸！学习基础操作"),
    2: LevelData(2, "更多的僵尸来袭，准备好你的豌豆射手"),
    3: LevelData(3, "向日葵帮助你获得更多阳光"),
    4: LevelData(4, "僵尸开始变得更强壮"),
    5: LevelData(5, "第一波真正的挑战"),
    6: LevelData(6, "学会合理布置你的防线"),
    7: LevelData(7, "更多的行，更多的挑战"),
    8: LevelData(8, "僵尸速度开始加快"),
    9: LevelData(9, "坚持住，胜利就在眼前"),
    10: LevelData(10, "第一个里程碑关卡！"),
    11: LevelData(11, "新的挑战开始"),
    12: LevelData(12, "僵尸数量显著增加"),
    13: LevelData(13, "考验你的战略布局"),
    14: LevelData(14, "快速反应的时刻"),
    15: LevelData(15, "中场休息时间"),
    16: LevelData(16, "后半程开始"),
    17: LevelData(17, "僵尸变得更难对付"),
    18: LevelData(18, "优化你的植物布局"),
    19: LevelData(19, "坚持就是胜利"),
    20: LevelData(20, "第二个里程碑！"),
    21: LevelData(21, "最终挑战开始"),
    22: LevelData(22, "极限测试"),
    23: LevelData(23, "策略与速度的较量"),
    24: LevelData(24, "不要放弃希望"),
    25: LevelData(25, "四分之三的征程"),
    26: LevelData(26, "最后的冲刺"),
    27: LevelData(27, "考验你的耐心"),
    28: LevelData(28, "胜利在望"),
    29: LevelData(29, "最终准备"),
    30: LevelData(30, "最终关卡！成为真正的植物大师")
}

def get_level_data(level: int) -> Optional[LevelData]:
    """获取指定关卡的数据"""
    return LEVELS_DATA.get(level)

def get_level_description(level: int) -> str:
    """获取关卡描述"""
    level_data = get_level_data(level)
    if level_data:
        return level_data.description
    return f"关卡 {level}"

def get_level_music(level: int) -> str:
    """获取关卡背景音乐"""
    level_data = get_level_data(level)
    if level_data:
        return level_data.music
    return "gameplay"

def get_available_plants(level: int) -> tuple:
    """获取关卡可用的植物"""
    level_data = get_level_data(level)
    if level_data:
        return level_data.available_plants
    return ("peashooter", "sunflower")
