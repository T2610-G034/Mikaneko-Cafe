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
    CX, CY = WIDTH // 2, HEIGHT // 2

    btn_start    = MenuButton(CX - 150, CY - 100, 300, 80, "START GAME")
    btn_settings = MenuButton(CX - 150, CY + 10, 300, 80, "SETTINGS")
    btn_quit     = MenuButton(CX - 150, CY + 120, 300, 80, "QUIT")
    
    btn_back     = MenuButton(20, 20, 150, 50, "MENU")
    btn_tap      = MenuButton(CX - 150, CY + 50, 300, 100, "TAP FOR MAO-MAO", (218, 165, 32))

    # --- ADJUSTED SETTINGS BUTTONS ---
    btn_set_back = MenuButton(20, 20, 150, 50, "BACK")
    btn_music    = MenuButton(CX - 150, CY - 80, 300, 80, "MUSIC: ON")
    btn_vol_down = MenuButton(CX - 240, CY + 40, 80, 80, "-")
    btn_vol_up   = MenuButton(CX + 160, CY + 40, 80, 80, "+")

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "MENU":
                    if btn_start.is_clicked(mouse_pos): state = "GAME"
                    elif btn_settings.is_clicked(mouse_pos): state = "SETTINGS"
                    elif btn_quit.is_clicked(mouse_pos): pygame.quit(); sys.exit()
                
                elif state == "GAME":
                    if btn_back.is_clicked(mouse_pos): state = "MENU"
                    if btn_tap.is_clicked(mouse_pos): engine.add_click()

                elif state == "SETTINGS":
                    if btn_set_back.is_clicked(mouse_pos): state = "MENU"
                    if btn_music.is_clicked(mouse_pos):
                        btn_music.text = "MUSIC: OFF" if btn_music.text == "MUSIC: ON" else "MUSIC: ON"
                    if btn_vol_up.is_clicked(mouse_pos):
                        if volume < 100: volume += 10
                    if btn_vol_down.is_clicked(mouse_pos):
                        if volume > 0: volume -= 10

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
            btn_back.draw(screen, font)
            btn_tap.draw(screen, font)
            counter_txt = font.render(f"Mao-Maos: {engine.mao_mao}", True, WHITE)
            screen.blit(counter_txt, (CX - counter_txt.get_width()//2, CY - 50))

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

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
