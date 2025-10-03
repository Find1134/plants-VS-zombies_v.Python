import pygame
import os

# 音乐文件路径
MUSIC_FILES = {
    "main_menu": "lawnbgm(1).mp3",
    "settings": "lawnbgm(2).mp3", 
    "game": "lawnbgm(3).mp3"
}

# 全局音乐状态
music_loaded = False
current_music = None

def load_music():
    """
    加载音乐文件
    
    Returns:
        bool: 是否成功加载音乐
    """
    global music_loaded
    
    try:
        # 检查音乐文件是否存在
        for music_type, file_path in MUSIC_FILES.items():
            if not os.path.exists(file_path):
                print(f"警告：音乐文件 {file_path} 不存在")
                music_loaded = False
                return False
        
        music_loaded = True
        return True
    except Exception as e:
        print(f"加载音乐失败: {e}")
        music_loaded = False
        return False

def play_music(music_type, loop=True):
    """
    播放音乐
    
    Args:
        music_type: 音乐类型 ('main_menu', 'settings', 'game')
        loop: 是否循环播放
    """
    global current_music
    
    if not music_loaded:
        return
    
    if music_type not in MUSIC_FILES:
        print(f"错误：未知的音乐类型 {music_type}")
        return
    
    try:
        # 停止当前音乐
        pygame.mixer.music.stop()
        
        # 加载并播放新音乐
        music_file = MUSIC_FILES[music_type]
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1 if loop else 0)
        current_music = music_type
        
    except pygame.error as e:
        print(f"播放音乐失败: {e}")

def stop_music():
    """停止当前音乐"""
    pygame.mixer.music.stop()

def set_music_volume(volume):
    """
    设置音乐音量
    
    Args:
        volume: 音量 (0.0 到 1.0)
    """
    pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))

def set_sound_volume(volume):
    """
    设置音效音量
    
    Args:
        volume: 音量 (0.0 到 1.0)
    """
    # 这里可以设置音效的音量
    # 注意：pygame.mixer.Sound 对象需要单独设置音量
    pass

def is_music_playing():
    """检查音乐是否正在播放"""
    return pygame.mixer.music.get_busy()

def get_current_music():
    """获取当前播放的音乐类型"""
    return current_music