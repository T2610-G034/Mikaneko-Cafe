import pygame
from path_helper import get_path
from settings import WIDTH, HEIGHT

def initialize_audio(volume):
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
    try:
        bg_img = pygame.image.load(get_path("images/.cafe_1_background.png")).convert()
        bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
    except:
        bg_img = None

    try:
        cursor_img = pygame.image.load(get_path("images/paw.png")).convert_alpha()
        cursor_img = pygame.transform.scale(cursor_img, (50, 50))
    except:
        cursor_img = None

    try:
        kitchen_bg = pygame.image.load(get_path("images/background_kitchen.png")).convert()
        kitchen_bg = pygame.transform.scale(kitchen_bg, (WIDTH, HEIGHT))
    except:
        kitchen_bg = None

    # --- UPDATED: REAL PNG CURSOR ASSET LOADER ---
    cursor_assets = {}
    cursor_size = (60, 60)

    # 1. Empty Cup
    try:
        cursor_assets["EMPTY_CUP"] = pygame.image.load(get_path("images/cuponly.png")).convert_alpha()
        cursor_assets["EMPTY_CUP"] = pygame.transform.scale(cursor_assets["EMPTY_CUP"], cursor_size)
    except:
        surf = pygame.Surface(cursor_size, pygame.SRCALPHA)
        pygame.draw.rect(surf, (200, 200, 250), (10, 10, 40, 40), border_radius=5)
        cursor_assets["EMPTY_CUP"] = surf

    # 2. Chocolate Cup
    try:
        cursor_assets["CHOCOLATE"] = pygame.image.load(get_path("images/chocolatefrappe_cup.png")).convert_alpha()
        cursor_assets["CHOCOLATE"] = pygame.transform.scale(cursor_assets["CHOCOLATE"], cursor_size)
    except:
        surf = pygame.Surface(cursor_size, pygame.SRCALPHA)
        pygame.draw.rect(surf, (101, 67, 33), (10, 10, 40, 40), border_radius=5)
        cursor_assets["CHOCOLATE"] = surf

    # 3. Strawberry Cup
    try:
        cursor_assets["STRAWBERRY"] = pygame.image.load(get_path("images/strawberrysmoothie_cup.png")).convert_alpha()
        cursor_assets["STRAWBERRY"] = pygame.transform.scale(cursor_assets["STRAWBERRY"], cursor_size)
    except:
        surf = pygame.Surface(cursor_size, pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 182, 193), (10, 10, 40, 40), border_radius=5)
        cursor_assets["STRAWBERRY"] = surf

    # 4. Boba Milk Tea Cup
    try:
        cursor_assets["BOBA MILK TEA"] = pygame.image.load(get_path("images/bobatea_cup.png")).convert_alpha()
        cursor_assets["BOBA MILK TEA"] = pygame.transform.scale(cursor_assets["BOBA MILK TEA"], cursor_size)
    except:
        surf = pygame.Surface(cursor_size, pygame.SRCALPHA)
        pygame.draw.rect(surf, (245, 222, 179), (10, 10, 40, 40), border_radius=5)
        cursor_assets["BOBA MILK TEA"] = surf

    return bg_img, cursor_img, kitchen_bg, cursor_assets
