import pygame
import sys
import os  # ADDED: This helps find your files
from sprites import MenuButton
from game_logic import GameEngine

# --- FILE PATH FIX ---
# This finds the folder where this script is saved
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

def get_path(filename):
    """Helper function to find files in the same folder as main.py"""
    return os.path.join(BASE_PATH, filename)

# CONFIGURATION
WIDTH, HEIGHT = 1280, 720
FPS = 60
PASTEL_PINK = (255, 220, 230)
GREEN_CAFE  = (34, 139, 34)
WHITE       = (255, 255, 255)
BROWN       = (101, 67, 33)

def main():
    pygame.init()
    pygame.mixer.init() 
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mika Neko Cafe")
    clock = pygame.time.Clock()
    
    # --- MUSIC LOAD (Using Absolute Path) ---
    music_playing = False
    try:
        pygame.mixer.music.load(get_path("music.mp3")) 
        pygame.mixer.music.play(-1)
        music_playing = True
    except Exception as e:
        print(f"Music Error: {e}. Searched at: {get_path('music.mp3')}")

    # --- CURSOR LOAD (Using Absolute Path) ---
    try:
        cursor_img = pygame.image.load(get_path("cursor_hand.png")).convert_alpha()
        cursor_img = pygame.transform.scale(cursor_img, (50, 50))
    except Exception as e:
        cursor_img = None
        print(f"Cursor Error: {e}. Searched at: {get_path('cursor_hand.png')}")

    font = pygame.font.SysFont("Arial", 30, bold=True)
    title_font = pygame.font.SysFont("Arial", 100, bold=True)
    
    engine = GameEngine()
    state = "MENU"
    volume = 50 
    pygame.mixer.music.set_volume(volume / 100)
    
    CX, CY = WIDTH // 2, HEIGHT // 2

    # --- BUTTONS ---
    btn_start    = MenuButton(CX - 150, CY - 100, 300, 80, "START GAME")
    btn_settings = MenuButton(CX - 150, CY + 10, 300, 80, "SETTINGS")
    btn_quit     = MenuButton(CX - 150, CY + 120, 300, 80, "QUIT")
    btn_game_back = MenuButton(20, 20, 150, 50, "MENU")
    btn_open_shop = MenuButton(WIDTH - 220, 20, 200, 50, "OPEN SHOP", (255, 182, 193))
    btn_tap       = MenuButton(CX - 150, HEIGHT - 150, 300, 100, "TAP FOR MAO-MAO", (218, 165, 32))
    btn_set_back = MenuButton(20, 20, 150, 50, "BACK")
    btn_music    = MenuButton(CX - 150, CY - 80, 300, 80, "MUSIC: ON")
    btn_vol_down = MenuButton(CX - 240, CY + 40, 80, 80, "-")
    btn_vol_up   = MenuButton(CX + 160, CY + 40, 80, 80, "+")
    btn_shop_back = MenuButton(20, 20, 150, 50, "BACK")

    item_buttons = {}
    for i, item_name in enumerate(engine.shop_items):
        item_buttons[item_name] = MenuButton(CX - 250, 220 + (i * 90), 500, 70, item_name)

    is_hovering_tap = False

    while True:
        mouse_pos = pygame.mouse.get_pos()
        is_hovering_tap = False 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "MENU":
                    if btn_start.is_clicked(mouse_pos): state = "GAME"
                    elif btn_settings.is_clicked(mouse_pos): state = "SETTINGS"
                    elif btn_quit.is_clicked(mouse_pos): pygame.quit(); sys.exit()
                elif state == "GAME":
                    if btn_game_back.is_clicked(mouse_pos): state = "MENU"
                    elif btn_open_shop.is_clicked(mouse_pos): state = "SHOP"
                    elif btn_tap.is_clicked(mouse_pos): engine.add_click()
                elif state == "SETTINGS":
                    if btn_set_back.is_clicked(mouse_pos): state = "MENU"
                    elif btn_music.is_clicked(mouse_pos):
                        if music_playing:
                            pygame.mixer.music.pause(); btn_music.text = "MUSIC: OFF"; music_playing = False
                        else:
                            pygame.mixer.music.unpause(); btn_music.text = "MUSIC: ON"; music_playing = True
                    elif btn_vol_up.is_clicked(mouse_pos):
                        volume = min(100, volume + 10); pygame.mixer.music.set_volume(volume/100)
                    elif btn_vol_down.is_clicked(mouse_pos):
                        volume = max(0, volume - 10); pygame.mixer.music.set_volume(volume/100)
                elif state == "SHOP":
                    if btn_shop_back.is_clicked(mouse_pos): state = "GAME"
                    for name, btn in item_buttons.items():
                        if btn.is_clicked(mouse_pos): engine.buy_item(name)

        # --- DRAWING ---
        if state == "MENU":
            pygame.mouse.set_visible(True)
            screen.fill(PASTEL_PINK)
            title_surf = title_font.render("Mika Neko Cafe", True, BROWN)
            screen.blit(title_surf, (CX - title_surf.get_width()//2, 100))
            btn_start.draw(screen, font); btn_settings.draw(screen, font); btn_quit.draw(screen, font)
        
        elif state == "GAME":
            screen.fill(GREEN_CAFE)
            btn_game_back.draw(screen, font)
            btn_open_shop.draw(screen, font)
            for name, data in engine.shop_items.items():
                if data[2] > 0:
                    pygame.draw.circle(screen, data[4], data[3], 40)
                    pygame.draw.circle(screen, BROWN, data[3], 40, 3)
            btn_tap.draw(screen, font)
            counter_txt = font.render(f"Mao-Maos: {engine.mao_mao}", True, WHITE)
            screen.blit(counter_txt, (CX - counter_txt.get_width()//2, 100))
            if btn_tap.rect.collidepoint(mouse_pos):
                is_hovering_tap = True; pygame.mouse.set_visible(False)
            else:
                pygame.mouse.set_visible(True)

        elif state == "SETTINGS":
            pygame.mouse.set_visible(True)
            screen.fill(PASTEL_PINK)
            
            # Draw the title
            set_title = title_font.render("Settings", True, BROWN)
            screen.blit(set_title, (CX - set_title.get_width()//2, 80))
            
            # Draw the control buttons
            btn_music.draw(screen, font)
            btn_vol_down.draw(screen, font)
            btn_vol_up.draw(screen, font)
            btn_set_back.draw(screen, font)
            
            # --- THE MISSING PART: Draw the Volume Percentage ---
            vol_label = font.render(f"VOLUME: {volume}%", True, BROWN)
            screen.blit(vol_label, (CX - vol_label.get_width()//2, CY + 65))
            
        elif state == "SHOP":
            pygame.mouse.set_visible(True); screen.fill(PASTEL_PINK)
            btn_shop_back.draw(screen, font)
            for name, btn in item_buttons.items():
                price, benefit, owned, pos, color = engine.shop_items[name]
                btn.text = f"{name}: SOLD OUT" if owned > 0 else f"{name}: {price} M"
                btn.draw(screen, font)

        # --- FINAL CURSOR DRAW ---
        if state == "GAME" and is_hovering_tap:
            if cursor_img:
                screen.blit(cursor_img, (mouse_pos[0] - 25, mouse_pos[1] - 25))
            else:
                pygame.draw.circle(screen, (255, 0, 0), mouse_pos, 15)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
