import pygame
import sys
from sprites import MenuButton
from game_logic import GameEngine

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
    
    try:
        pygame.mixer.music.load("music.mp3") 
        pygame.mixer.music.play(-1)
    except:
        print("Music file not found, continuing without audio.")

    font = pygame.font.SysFont("Arial", 30, bold=True)
    title_font = pygame.font.SysFont("Arial", 100, bold=True)
    
    engine = GameEngine()
    state = "MENU"
    volume = 50 
    pygame.mixer.music.set_volume(volume / 100)
    
    CX, CY = WIDTH // 2, HEIGHT // 2

    # --- MENU BUTTONS ---
    btn_start    = MenuButton(CX - 150, CY - 100, 300, 80, "START GAME")
    btn_settings = MenuButton(CX - 150, CY + 10, 300, 80, "SETTINGS")
    btn_quit     = MenuButton(CX - 150, CY + 120, 300, 80, "QUIT")
    
    # --- GAME BUTTONS ---
    btn_game_back = MenuButton(20, 20, 150, 50, "MENU")
    btn_open_shop = MenuButton(WIDTH - 220, 20, 200, 50, "OPEN SHOP", (255, 182, 193))
    btn_tap       = MenuButton(CX - 150, HEIGHT - 150, 300, 100, "TAP FOR MAO-MAO", (218, 165, 32))

    # --- SETTINGS BUTTONS ---
    btn_set_back = MenuButton(20, 20, 150, 50, "BACK")
    btn_music    = MenuButton(CX - 150, CY - 80, 300, 80, "MUSIC: ON")
    btn_vol_down = MenuButton(CX - 240, CY + 40, 80, 80, "-")
    btn_vol_up   = MenuButton(CX + 160, CY + 40, 80, 80, "+")

    # --- SHOP BUTTONS ---
    btn_shop_back = MenuButton(20, 20, 150, 50, "BACK")
    item_buttons = {}
    for i, item_name in enumerate(engine.shop_items):
        item_buttons[item_name] = MenuButton(CX - 250, 220 + (i * 90), 500, 70, item_name)

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # 1. MENU STATE EVENTS
                if state == "MENU":
                    if btn_start.is_clicked(mouse_pos): 
                        state = "GAME"
                    elif btn_settings.is_clicked(mouse_pos): 
                        state = "SETTINGS"
                    elif btn_quit.is_clicked(mouse_pos): 
                        pygame.quit(); sys.exit()
                
                # 2. GAME STATE EVENTS
                elif state == "GAME":
                    if btn_game_back.is_clicked(mouse_pos): 
                        state = "MENU"
                    elif btn_open_shop.is_clicked(mouse_pos): 
                        state = "SHOP"
                    elif btn_tap.is_clicked(mouse_pos): 
                        engine.add_click()

                # 3. SETTINGS STATE EVENTS
                elif state == "SETTINGS":
                    if btn_set_back.is_clicked(mouse_pos): 
                        state = "MENU"
                    if btn_music.is_clicked(mouse_pos):
                        if btn_music.text == "MUSIC: ON":
                            btn_music.text = "MUSIC: OFF"
                            pygame.mixer.music.pause()
                        else:
                            btn_music.text = "MUSIC: ON"
                            pygame.mixer.music.unpause()
                    if btn_vol_up.is_clicked(mouse_pos):
                        volume = min(100, volume + 10)
                        pygame.mixer.music.set_volume(volume / 100)
                    if btn_vol_down.is_clicked(mouse_pos):
                        volume = max(0, volume - 10)
                        pygame.mixer.music.set_volume(volume / 100)

                # 4. SHOP STATE EVENTS
                elif state == "SHOP":
                    if btn_shop_back.is_clicked(mouse_pos): 
                        state = "GAME"
                    for name, btn in item_buttons.items():
                        if btn.is_clicked(mouse_pos):
                            engine.buy_item(name)

        # --- DRAWING ---
        if state == "MENU":
            screen.fill(PASTEL_PINK)
            title_surf = title_font.render("Mika Neko Cafe", True, BROWN)
            screen.blit(title_surf, (CX - title_surf.get_width()//2, 100))
            btn_start.draw(screen, font)
            btn_settings.draw(screen, font)
            btn_quit.draw(screen, font)
        
        elif state == "GAME":
            screen.fill(GREEN_CAFE)
            btn_game_back.draw(screen, font)
            btn_open_shop.draw(screen, font)
            
            # Draw Owned Items in the Cafe
            for name, data in engine.shop_items.items():
                if data[2] > 0: # If owned
                    pygame.draw.circle(screen, data[4], data[3], 40)
                    pygame.draw.circle(screen, BROWN, data[3], 40, 3)
                    label = font.render(name, True, WHITE)
                    screen.blit(label, (data[3][0] - label.get_width()//2, data[3][1] + 45))

            btn_tap.draw(screen, font)
            counter_txt = font.render(f"Mao-Maos: {engine.mao_mao}", True, WHITE)
            screen.blit(counter_txt, (CX - counter_txt.get_width()//2, 100))

        elif state == "SETTINGS":
            screen.fill(PASTEL_PINK)
            set_title = title_font.render("Settings", True, BROWN)
            screen.blit(set_title, (CX - set_title.get_width()//2, 80))
            btn_music.draw(screen, font)
            btn_vol_down.draw(screen, font)
            btn_vol_up.draw(screen, font)
            btn_set_back.draw(screen, font)
            vol_label = font.render(f"VOLUME: {volume}%", True, BROWN)
            screen.blit(vol_label, (CX - vol_label.get_width()//2, CY + 65))

        elif state == "SHOP":
            screen.fill(PASTEL_PINK)
            btn_shop_back.draw(screen, font)
            money_txt = font.render(f"Mao-Maos: {engine.mao_mao}", True, BROWN)
            screen.blit(money_txt, (CX - money_txt.get_width()//2, 150))
            
            for name, btn in item_buttons.items():
                price = engine.shop_items[name][0]
                owned = engine.shop_items[name][2]
                
                if owned > 0:
                    btn.text = f"{name}: SOLD OUT"
                    btn.color = (200, 200, 200) 
                else:
                    btn.text = f"{name}: {price} M"
                    btn.color = (255, 255, 255)
                
                btn.draw(screen, font)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
