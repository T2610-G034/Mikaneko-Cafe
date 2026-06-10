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
        bg_img = pygame.image.load(get_path("cafe_1_background.png")).convert()
        bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
    except:
        bg_img = None

    try:
        cursor_img = pygame.image.load(get_path("cursor_hand.png")).convert_alpha()
        cursor_img = pygame.transform.scale(cursor_img, (50, 50))
    except:
        cursor_img = None

    try:
        kitchen_bg = pygame.image.load(get_path("kitchen_background.png")).convert()
        kitchen_bg = pygame.transform.scale(kitchen_bg, (WIDTH, HEIGHT))
    except:
        kitchen_bg = None

    # --- UPDATED: INCREASED SIZE BY 500% (60 * 5 = 300) ---
    cursor_assets = {}
    cursor_size = (300, 300)

    # 1. Empty Cup
    try:
        cursor_assets["EMPTY_CUP"] = pygame.image.load(get_path("cup_empty.png")).convert_alpha()
        cursor_assets["EMPTY_CUP"] = pygame.transform.scale(cursor_assets["EMPTY_CUP"], cursor_size)
    except:
        surf = pygame.Surface(cursor_size, pygame.SRCALPHA)
        pygame.draw.rect(surf, (200, 200, 250), (50, 50, 200, 200), border_radius=25)
        cursor_assets["EMPTY_CUP"] = surf

    # 2. Chocolate Cup
    try:
        cursor_assets["CHOCOLATE"] = pygame.image.load(get_path("cup_chocolate.png")).convert_alpha()
        cursor_assets["CHOCOLATE"] = pygame.transform.scale(cursor_assets["CHOCOLATE"], cursor_size)
    except:
        surf = pygame.Surface(cursor_size, pygame.SRCALPHA)
        pygame.draw.rect(surf, (101, 67, 33), (50, 50, 200, 200), border_radius=25)
        cursor_assets["CHOCOLATE"] = surf

    # 3. Strawberry Cup
    try:
        cursor_assets["STRAWBERRY"] = pygame.image.load(get_path("cup_strawberry.png")).convert_alpha()
        cursor_assets["STRAWBERRY"] = pygame.transform.scale(cursor_assets["STRAWBERRY"], cursor_size)
    except:
        surf = pygame.Surface(cursor_size, pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 182, 193), (50, 50, 200, 200), border_radius=25)
        cursor_assets["STRAWBERRY"] = surf

    # 4. Milk TeaBoba  Cup
    try:
        cursor_assets["MILK TEA"] = pygame.image.load(get_path("cup_boba.png")).convert_alpha()
        cursor_assets["MILK TEA"] = pygame.transform.scale(cursor_assets["MILK TEA"], cursor_size)
    except:
        surf = pygame.Surface(cursor_size, pygame.SRCALPHA)
        pygame.draw.rect(surf, (245, 222, 179), (50, 50, 200, 200), border_radius=25)
        cursor_assets["MILK TEA"] = surf

    return bg_img, cursor_img, kitchen_bg, cursor_assets

def load_audio_assets():
    """Loads and returns sound effects safely with fallback silent objects if missing."""
    sfx = {}
    
    sfx_files = {
        "meow1": "meow1.mp3",
        "meow2": "meow2.mp3",
        "meow3": "meow3.mp3",
        "cup": "cup.mp3",
        "liquid": "liquid.mp3",
        "bell": "bell.mp3"
    }
    
    for key, filename in sfx_files.items():
        try:
            sfx[key] = pygame.mixer.Sound(get_path(filename))
        except Exception as e:
            print(f"SFX Warning: Could not load {filename}, using silent fallback. ({e})")
            sfx[key] = None
            
    return sfx
