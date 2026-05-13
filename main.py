import pygame
import sys
import os
from sprites import MenuButton
from game_logic import GameEngine

# --- FILE PATH FIX ---
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

def get_path(filename):
    return os.path.join(BASE_PATH, filename)

# CONFIGURATION
WIDTH, HEIGHT = 1280, 720
FPS = 60
PASTEL_PINK   = (255, 220, 230)
PASTEL_BLUE   = (230, 240, 255)
GREEN_CAFE    = (34, 139, 34)
WHITE         = (255, 255, 255)
BROWN         = (101, 67, 33)

def main():
    pygame.init()
    pygame.mixer.init() 
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mika Neko Cafe")
    clock = pygame.time.Clock()
    
    # --- ASSETS ---
    music_playing = False
    try:
        pygame.mixer.music.load(get_path("music.mp3")) 
        pygame.mixer.music.play(-1)
        music_playing = True
    except Exception as e:
        print(f"Music Error: {e}")

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

    font = pygame.font.SysFont("Arial", 30, bold=True)
    title_font = pygame.font.SysFont("Arial", 100, bold=True)
    
    engine = GameEngine()
    state = "MENU"
    volume = 50 
    pygame.mixer.music.set_volume(volume / 100)
    
    CX, CY = WIDTH // 2, HEIGHT // 2
    
    # --- BUTTONS ---
    btn_start      = MenuButton(CX - 150, CY - 100, 300, 80, "START GAME")
    btn_settings   = MenuButton(CX - 150, CY + 10, 300, 80, "SETTINGS")
    btn_quit       = MenuButton(CX - 150, CY + 120, 300, 80, "QUIT")
    btn_back_to_menu = MenuButton(20, 20, 150, 50, "MENU")
    
    btn_open_furn   = MenuButton(WIDTH - 220, 20, 200, 50, "FURNITURES", (255, 182, 193))
    btn_open_cats   = MenuButton(WIDTH - 220, 85, 200, 50, "CATS", (173, 216, 230))
    btn_tap         = MenuButton(CX - 150, HEIGHT - 150, 300, 100, "TAP FOR MAO-MAO", (218, 165, 32))
    
    btn_set_back   = MenuButton(20, 20, 150, 50, "BACK")
    btn_music      = MenuButton(CX - 150, CY - 80, 300, 80, "MUSIC: ON")
    btn_vol_down   = MenuButton(CX - 240, CY + 40, 80, 80, "-")
    btn_vol_up     = MenuButton(CX + 160, CY + 40, 80, 80, "+")
    btn_shop_back  = MenuButton(20, 20, 150, 50, "BACK")

    furn_buttons = {name: MenuButton(CX - 250, 220 + (i * 90), 500, 70, name) 
                    for i, name in enumerate(engine.furniture_items)}
    cat_buttons = {name: MenuButton(CX - 250, 220 + (i * 90), 500, 70, name) 
                   for i, name in enumerate(engine.cat_items)}

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
                    if btn_back_to_menu.is_clicked(mouse_pos): state = "MENU"
                    elif btn_open_furn.is_clicked(mouse_pos): state = "FURN_SHOP"
                    elif btn_open_cats.is_clicked(mouse_pos): state = "CAT_SHOP"
                    elif btn_tap.is_clicked(mouse_pos): engine.add_click()
                
                elif state == "SETTINGS":
                    if btn_set_back.is_clicked(mouse_pos): state = "MENU"
                    elif btn_music.is_clicked(mouse_pos):
                        music_playing = not music_playing
                        pygame.mixer.music.unpause() if music_playing else pygame.mixer.music.pause()
                        btn_music.text = f"MUSIC: {'ON' if music_playing else 'OFF'}"
                    elif btn_vol_up.is_clicked(mouse_pos):
                        volume = min(100, volume + 10); pygame.mixer.music.set_volume(volume/100)
                    elif btn_vol_down.is_clicked(mouse_pos):
                        volume = max(0, volume - 10); pygame.mixer.music.set_volume(volume/100)
                
                elif state == "FURN_SHOP":
                    if btn_shop_back.is_clicked(mouse_pos): state = "GAME"
                    for name, btn in furn_buttons.items():
                        if btn.is_clicked(mouse_pos): engine.buy_item(name, "furniture")
                
                elif state == "CAT_SHOP":
                    if btn_shop_back.is_clicked(mouse_pos): state = "GAME"
                    for name, btn in cat_buttons.items():
                        if btn.is_clicked(mouse_pos): engine.buy_item(name, "cats")

        # --- DRAWING ---
        if state == "MENU":
            pygame.mouse.set_visible(True)
            screen.fill(PASTEL_PINK)
            title_surf = title_font.render("Mika Neko Cafe", True, BROWN)
            screen.blit(title_surf, (CX - title_surf.get_width()//2, 100))
            btn_start.draw(screen, font); btn_settings.draw(screen, font); btn_quit.draw(screen, font)
        
        elif state == "GAME":
            if bg_img: screen.blit(bg_img, (0, 0))
            else: screen.fill(GREEN_CAFE)

            btn_back_to_menu.draw(screen, font)
            btn_open_furn.draw(screen, font)
            btn_open_cats.draw(screen, font)
            
            # Draw owned items as images
            for shop in [engine.furniture_items, engine.cat_items]:
                for name, data in shop.items():
                    if data[2] > 0: 
                        img_rect = data[4].get_rect(center=data[3])
                        screen.blit(data[4], img_rect)
            
            btn_tap.draw(screen, font)
            
            counter_txt = font.render(f"Mao-Maos: {int(engine.mao_mao)}", True, WHITE)
            screen.blit(counter_txt, (CX - counter_txt.get_width()//2, 100))
            
            if btn_tap.rect.collidepoint(mouse_pos):
                is_hovering_tap = True; pygame.mouse.set_visible(False)
            else:
                pygame.mouse.set_visible(True)

        elif state == "SETTINGS":
            screen.fill(PASTEL_PINK)
            btn_music.draw(screen, font); btn_vol_down.draw(screen, font); btn_vol_up.draw(screen, font); btn_set_back.draw(screen, font)
            vol_label = font.render(f"VOLUME: {volume}%", True, BROWN)
            screen.blit(vol_label, (CX - vol_label.get_width()//2, CY + 65))
            
        elif state in ["FURN_SHOP", "CAT_SHOP"]:
            screen.fill(PASTEL_PINK if state == "FURN_SHOP" else PASTEL_BLUE)
            btn_shop_back.draw(screen, font)
            current_shop = engine.furniture_items if state == "FURN_SHOP" else engine.cat_items
            current_btns = furn_buttons if state == "FURN_SHOP" else cat_buttons
            
            for name, btn in current_btns.items():
                price, _, owned, _, _ = current_shop[name]
                btn.text = f"{name}: SOLD" if owned > 0 else f"{name}: {price} M"
                btn.draw(screen, font)

        if state == "GAME" and is_hovering_tap:
            if cursor_img: screen.blit(cursor_img, (mouse_pos[0]-25, mouse_pos[1]-25))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
