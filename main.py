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
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = WHITE

    def draw(self, screen, font, mouse_pos):
        # Hover effect
        if self.rect.collidepoint(mouse_pos):
            self.color = (245, 245, 245)
        else:
            self.color = WHITE

        # Shadow
        shadow = self.rect.copy()
        shadow.x += 5
        shadow.y += 5
        pygame.draw.rect(screen, (220, 180, 190), shadow, border_radius=15)

        # Button body
        pygame.draw.rect(screen, self.color, self.rect, border_radius=15)
        pygame.draw.rect(screen, BROWN, self.rect, 3, border_radius=15)

        # Text
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

    # State
    state = "MENU"
    CX, CY = WIDTH // 2, HEIGHT // 2

    # Main Menu Buttons
    btn_start    = MenuButton(CX - 150, CY - 40, 300, 80, "START GAME")
    btn_settings = MenuButton(CX - 150, CY + 70, 300, 80, "SETTINGS")
    btn_quit     = MenuButton(CX - 150, CY + 180, 300, 80, "QUIT")

    # Settings Buttons (aligned vertically)
    settings_buttons = [
        MenuButton(CX - 150, CY - 60, 300, 60, "- VOL"),
        MenuButton(CX - 150, CY + 20, 300, 60, "+ VOL"),
        MenuButton(CX - 150, CY + 100, 300, 60, "MUTE / UNMUTE"),
        MenuButton(CX - 150, CY + 180, 300, 60, "BACK")
    ]

    # Volume state (0.0 to 1.0)
    volume = 0.5
    muted = False
    pygame.mixer.init()

    # Load and play background music
    try:
        pygame.mixer.music.load("background.mp3")  # Place your music file here
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)  # loop forever
    except:
        print("Music file not found or failed to load.")

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
                        state = "SETTINGS"
                    if btn_quit.is_clicked(mouse_pos):
                        pygame.quit()
                        sys.exit()

                elif state == "SETTINGS":
                    for btn in settings_buttons:
                        if btn.is_clicked(mouse_pos):
                            if btn.text == "- VOL":
                                volume = max(0.0, volume - 0.1)
                                if not muted:
                                    pygame.mixer.music.set_volume(volume)
                            elif btn.text == "+ VOL":
                                volume = min(1.0, volume + 0.1)
                                if not muted:
                                    pygame.mixer.music.set_volume(volume)
                            elif btn.text == "MUTE / UNMUTE":
                                muted = not muted
                                if muted:
                                    pygame.mixer.music.set_volume(0.0)
                                else:
                                    pygame.mixer.music.set_volume(volume)
                            elif btn.text == "BACK":
                                state = "MENU"

        # DRAWING
        if state == "MENU":
            screen.fill(PASTEL_PINK)
            title_surf = title_font.render("Mika Neko Cafe", True, BROWN)
            title_rect = title_surf.get_rect(center=(CX, 180))
            screen.blit(title_surf, title_rect)

            btn_start.draw(screen, button_font, mouse_pos)
            btn_settings.draw(screen, button_font, mouse_pos)
            btn_quit.draw(screen, button_font, mouse_pos)

        elif state == "GAME_STARTED":
            screen.fill(GREEN_CAFE)
            msg = button_font.render("You have entered the Cafe!", True, WHITE)
            screen.blit(msg, (CX - msg.get_width()//2, CY))

        elif state == "SETTINGS":
            screen.fill((200, 230, 255))  # soft blue background
            title_surf = title_font.render("Settings", True, BROWN)
            title_rect = title_surf.get_rect(center=(CX, 120))
            screen.blit(title_surf, title_rect)

            # Draw all settings buttons
            for btn in settings_buttons:
                btn.draw(screen, button_font, mouse_pos)

            # Show current volume or mute state
            if muted:
                status_text = "Muted"
            else:
                status_text = f"Volume: {int(volume * 100)}%"
            status_surf = button_font.render(status_text, True, BROWN)
            screen.blit(status_surf, (CX - status_surf.get_width()//2, CY + 260))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
