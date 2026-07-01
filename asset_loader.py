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

    # 4. Milk Tea/Boba Cup
    try:
        cursor_assets["MILK TEA"] = pygame.image.load(get_path("cup_boba.png")).convert_alpha()
        cursor_assets["MILK TEA"] = pygame.transform.scale(cursor_assets["MILK TEA"], cursor_size)
    except:
        surf = pygame.Surface(cursor_size, pygame.SRCALPHA)
        pygame.draw.rect(surf, (245, 222, 179), (50, 50, 200, 200), border_radius=25)
        cursor_assets["MILK TEA"] = surf

    # --- LEVEL 2 CURSOR ASSET FALLBACK SURFACES ---
    # Empty cup for level 2 (teapot-style cup)
    try:
        cursor_assets["EMPTY_CUP_L2"] = pygame.image.load(get_path("emptyteapotcup.png")).convert_alpha()
        cursor_assets["EMPTY_CUP_L2"] = pygame.transform.scale(cursor_assets["EMPTY_CUP_L2"], cursor_size)
    except:
        surf = pygame.Surface(cursor_size, pygame.SRCALPHA)
        pygame.draw.rect(surf, (230, 230, 230), (50, 50, 200, 200), border_radius=25)
        cursor_assets["EMPTY_CUP_L2"] = surf

    # Coffee powder (intermediate step)
    try:
        cursor_assets["COFFEE_POWDER"] = pygame.image.load(get_path("coffeepowder.PNG")).convert_alpha()
        cursor_assets["COFFEE_POWDER"] = pygame.transform.scale(cursor_assets["COFFEE_POWDER"], cursor_size)
    except:
        surf = pygame.Surface(cursor_size, pygame.SRCALPHA)
        pygame.draw.rect(surf, (90, 50, 20), (50, 50, 200, 200), border_radius=25)
        cursor_assets["COFFEE_POWDER"] = surf

    # Tea powder (intermediate step)
    try:
        cursor_assets["TEA_POWDER"] = pygame.image.load(get_path("teapowder.PNG")).convert_alpha()
        cursor_assets["TEA_POWDER"] = pygame.transform.scale(cursor_assets["TEA_POWDER"], cursor_size)
    except:
        surf = pygame.Surface(cursor_size, pygame.SRCALPHA)
        pygame.draw.rect(surf, (140, 100, 40), (50, 50, 200, 200), border_radius=25)
        cursor_assets["TEA_POWDER"] = surf

    # Coffee (final)
    try:
        cursor_assets["COFFEE"] = pygame.image.load(get_path("coffee.PNG")).convert_alpha()
        cursor_assets["COFFEE"] = pygame.transform.scale(cursor_assets["COFFEE"], cursor_size)
    except:
        surf_coffee = pygame.Surface(cursor_size, pygame.SRCALPHA)
        pygame.draw.rect(surf_coffee, (72, 44, 25), (50, 50, 200, 200), border_radius=25)
        cursor_assets["COFFEE"] = surf_coffee

    # Tea (final)
    try:
        cursor_assets["TEA"] = pygame.image.load(get_path("tea.PNG")).convert_alpha()
        cursor_assets["TEA"] = pygame.transform.scale(cursor_assets["TEA"], cursor_size)
    except:
        surf_tea = pygame.Surface(cursor_size, pygame.SRCALPHA)
        pygame.draw.rect(surf_tea, (218, 165, 32), (50, 50, 200, 200), border_radius=25)
        cursor_assets["TEA"] = surf_tea

    # Polo Bun Butter
    surf_polo = pygame.Surface(cursor_size, pygame.SRCALPHA)
    pygame.draw.rect(surf_polo, (244, 208, 63), (50, 50, 200, 200), border_radius=25)
    cursor_assets["POLO BUN BUTTER"] = surf_polo

    # Croissant
    surf_croissant = pygame.Surface(cursor_size, pygame.SRCALPHA)
    pygame.draw.rect(surf_croissant, (211, 138, 62), (50, 50, 200, 200), border_radius=25)
    cursor_assets["CROISSANT"] = surf_croissant

    return bg_img, cursor_img, kitchen_bg, cursor_assets

def load_audio_assets():
    """Loads and returns sound effects safely with fallback silent objects if missing."""
    sfx = {}
    sfx_files = {
        "meow1": "meow1.mp3", "meow2": "meow2.mp3", "meow3": "meow3.mp3",
        "cup": "cup.mp3", "liquid": "liquid.mp3", "bell": "bell.mp3"
    }
    for key, filename in sfx_files.items():
        try:
            sfx[key] = pygame.mixer.Sound(get_path(filename))
        except:
            sfx[key] = None
    return sfx

def load_level_2_backgrounds():
    """Safely loads and returns Level 2 specific backgrounds."""
    try:
        bg_img_2 = pygame.image.load(get_path("cafe_2_background.jpg")).convert()
        bg_img_2 = pygame.transform.scale(bg_img_2, (WIDTH, HEIGHT))
    except:
        bg_img_2 = None

    try:
        kitchen_bg_2 = pygame.image.load(get_path("kitchen_2_background.png")).convert()
        kitchen_bg_2 = pygame.transform.scale(kitchen_bg_2, (WIDTH, HEIGHT))
    except:
        kitchen_bg_2 = None

    return bg_img_2, kitchen_bg_2
