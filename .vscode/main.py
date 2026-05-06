import pygame
import sys

# CONFIGURATION 
WIDTH, HEIGHT = 1280, 720
FPS = 60

# Colors
PASTEL_PINK = (255, 220, 230)
GREEN_CAFE  = (34, 139, 34)
BROWN       = (101, 67, 33)
WHITE       = (255, 255, 255)

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
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mika Neko Cafe - Main Menu")
    clock = pygame.time.Clock()

    # Fonts
    try:
        title_font = pygame.font.SysFont("Arial", 100, bold=True)
        button_font = pygame.font.SysFont("Arial", 30, bold=True)
    except:
        title_font = pygame.font.Font(None, 100)
        button_font = pygame.font.Font(None, 40)

    # State and Positions
    state = "MENU"
    CX, CY = WIDTH // 2, HEIGHT // 2

    # Create Buttons
    btn_start = MenuButton(CX - 150, CY - 40, 300, 80, "START GAME")
    btn_quit  = MenuButton(CX - 150, CY + 70, 300, 80, "QUIT")

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "MENU":
                    if btn_start.is_clicked(mouse_pos):
                        state = "GAME_STARTED"          # Switches background to Green
                    if btn_quit.is_clicked(mouse_pos):  # exits the game
                        pygame.quit()
                        sys.exit()

        # DRAWING
        if state == "MENU":
            screen.fill(PASTEL_PINK)
            
            # Title Text
            title_surf = title_font.render("Mika Neko Cafe", True, BROWN)
            title_rect = title_surf.get_rect(center=(CX, 180))
            screen.blit(title_surf, title_rect)
            
            # Draw Buttons
            btn_start.draw(screen, button_font)
            btn_quit.draw(screen, button_font)

        elif state == "GAME_STARTED":
            # This is the state after pressing START
            screen.fill(GREEN_CAFE)
            
            # Simple indicator showing that we moved states
            msg = button_font.render("You have entered the Cafe! (Green State)", True, WHITE)
            screen.blit(msg, (CX - msg.get_width()//2, CY))

        pygame.display.flip()
        clock.tick(FPS)

if _name_ == "_main_":
    main()