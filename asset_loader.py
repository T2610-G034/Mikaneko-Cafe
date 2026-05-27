import pygame
from path_helper import get_path
from settings import WIDTH, HEIGHT

def initialize_audio(volume):
    """Starts background mixer music."""
    music_playing = False
    try:
        pygame.mixer.music.load(get_path("music.mp3")) 
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(volume / 100)
        music_playing = True
    except Exception as e:
        print(f"Music Error: {e}")
    return music_playing

def load_visual_assets():
    """Loads background imagery and custom cursor pointers."""
    try:
        bg_img = pygame.image.load(get_path("cafe_1_background.png")).convert()
        bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
    except:
        bg_img = None

    try:
        cursor_img = pygame.image.load(get_path("cursor_hand.png")).convert_alpha()
        cursor_img = pygame.transform.scale(cursor_img, (50, 50))
    except:
        cursor_img = None

    return bg_img, cursor_img
