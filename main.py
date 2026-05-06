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
    
    # Font Setup
    font = pygame.font.SysFont("Arial", 30, bold=True)
    title_font = pygame.font.SysFont("Arial", 100, bold=True)
    
    engine = GameEngine()
    state = "MENU"
    CX, CY = WIDTH // 2, HEIGHT // 2

    # Create Buttons
    btn_start = MenuButton(CX - 150, CY - 40, 300, 80, "START GAME")
    btn_quit  = MenuButton(CX - 150, CY + 70, 300, 80, "QUIT")
    
    # Game Screen Buttons
    btn_back  = MenuButton(20, 20, 150, 50, "MENU")
    btn_tap   = MenuButton(CX - 150, CY + 50, 300, 100, "TAP FOR MAO-MAO", (218, 165, 32))

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "MENU":
                    if btn_start.is_clicked(mouse_pos):
                        state = "GAME"
                    if btn_quit.is_clicked(mouse_pos):
                        pygame.quit(); sys.exit()
                
                elif state == "GAME":
                    if btn_back.is_clicked(mouse_pos):
                        state = "MENU"
                    if btn_tap.is_clicked(mouse_pos):
                        engine.add_click()

        # --- DRAWING ---
        if state == "MENU":
            screen.fill(PASTEL_PINK)
            title_surf = title_font.render("Mika Neko Cafe", True, BROWN)
            screen.blit(title_surf, (CX - title_surf.get_width()//2, 150))
            btn_start.draw(screen, font)
            btn_quit.draw(screen, font)
        
        elif state == "GAME":
            screen.fill(GREEN_CAFE)
            btn_back.draw(screen, font)
            btn_tap.draw(screen, font)
            
            # Mao-Mao Display
            counter_txt = font.render(f"Mao-Maos: {engine.mao_mao}", True, WHITE)
            screen.blit(counter_txt, (CX - counter_txt.get_width()//2, CY - 50))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
