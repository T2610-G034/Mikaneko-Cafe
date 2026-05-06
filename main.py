import pygame
import sys

# CONFIGURATION 
WIDTH, HEIGHT = 1280, 720
FPS = 60

# Colors
PASTEL_PINK = (255, 220, 230)
GREEN_CAFE  = (34, 139, 34)
BROWN        = (101, 67, 33)
WHITE        = (255, 255, 255)
GOLD         = (218, 165, 32)

class MenuButton:
    def _init_(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = WHITE

    def draw(self, screen, font):
        # 3D Shadow effect
        shadow = self.rect.copy()
        shadow.x += 5
        shadow.y += 5
        pygame.draw.rect(screen, (220, 180, 190), shadow, border_radius=15)
        
        # Main Button Body
        pygame.draw.rect(screen, self.color, self.rect, border_radius=15)
        pygame.draw.rect(screen, BROWN, self.rect, 3, border_radius=15)
        
        # Text Centering
        txt_surf = font.render(self.text, True, BROWN)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        screen.blit(txt_surf, txt_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def main():
    pygame.init()
    pygame.mixer.init() # Needed for Volume
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mika Neko Cafe - Main Menu")
    clock = pygame.time.Clock()

    # Audio Setup
    current_volume = 0.5
    is_muted = False
    # pygame.mixer.music.load("your_music.mp3")
    # pygame.mixer.music.play(-1)

    # Fonts
    try:
        title_font = pygame.font.SysFont("Arial", 100, bold=True)
        button_font = pygame.font.SysFont("Arial", 30, bold=True)
    except:
        title_font = pygame.font.Font(None, 100)
        button_font = pygame.font.Font(None, 40)

    # State and Positions
    state = "MENU"
    previous_state = "MENU" # Crucial for the back button
    CX, CY = WIDTH // 2, HEIGHT // 2

    # Create Buttons
    btn_start    = MenuButton(CX - 150, CY - 100, 300, 80, "START GAME")
    btn_settings = MenuButton(CX - 150, CY + 10, 300, 80, "SETTINGS")
    btn_quit     = MenuButton(CX - 150, CY + 120, 300, 80, "QUIT")
    
    # Settings Specific Buttons
    btn_back     = MenuButton(40, 40, 180, 60, "BACK")
    btn_vol_up   = MenuButton(CX + 20, CY, 100, 60, "+")
    btn_vol_down = MenuButton(CX - 120, CY, 100, 60, "-")
    btn_mute     = MenuButton(CX - 100, CY + 100, 200, 60, "MUTE")

    # In-Game Buttons
    btn_set_game = MenuButton(40, 110, 180, 60, "SETTINGS")

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "MENU":
                    if btn_start.is_clicked(mouse_pos):
                        state = "GAME_STARTED"
                    if btn_settings.is_clicked(mouse_pos):
                        previous_state = "MENU"
                        state = "SETTINGS"
                    if btn_quit.is_clicked(mouse_pos):
                        pygame.quit(); sys.exit()

                elif state == "GAME_STARTED":
                    if btn_set_game.is_clicked(mouse_pos):
                        previous_state = "GAME_STARTED"
                        state = "SETTINGS"

                elif state == "SETTINGS":
                    if btn_back.is_clicked(mouse_pos):
                        state = previous_state # Go back to where you were
                    
                    if btn_vol_up.is_clicked(mouse_pos):
                        is_muted = False
                        current_volume = min(1.0, current_volume + 0.1)
                        pygame.mixer.music.set_volume(current_volume)
                    
                    if btn_vol_down.is_clicked(mouse_pos):
                        is_muted = False
                        current_volume = max(0.0, current_volume - 0.1)
                        pygame.mixer.music.set_volume(current_volume)
                    
                    if btn_mute.is_clicked(mouse_pos):
                        is_muted = not is_muted
                        pygame.mixer.music.set_volume(0 if is_muted else current_volume)

        # DRAWING
        if state == "MENU":
            screen.fill(PASTEL_PINK)
            title_surf = title_font.render("Mika Neko Cafe", True, BROWN)
            title_rect = title_surf.get_rect(center=(CX, 180))
            screen.blit(title_surf, title_rect)
            
            btn_start.draw(screen, button_font)
            btn_settings.draw(screen, button_font)
            btn_quit.draw(screen, button_font)

        elif state == "GAME_STARTED":
            screen.fill(GREEN_CAFE)
            msg = button_font.render("You have entered the Cafe!", True, WHITE)
            screen.blit(msg, (CX - msg.get_width()//2, CY))
            btn_set_game.draw(screen, button_font)

        elif state == "SETTINGS":
            screen.fill(PASTEL_PINK)
            set_title = title_font.render("Settings", True, BROWN)
            screen.blit(set_title, set_title.get_rect(center=(CX, 150)))
            
            # Volume Text
            vol_val = "MUTED" if is_muted else f"{int(current_volume * 100)}%"
            vol_label = button_font.render(f"Volume: {vol_val}", True, BROWN)
            screen.blit(vol_label, vol_label.get_rect(center=(CX, CY - 60)))
            
            btn_back.draw(screen, button_font)
            btn_vol_up.draw(screen, button_font)
            btn_vol_down.draw(screen, button_font)
            
            btn_mute.text = "UNMUTE" if is_muted else "MUTE"
            btn_mute.draw(screen, button_font)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "_main_":
    main()