import pygame
from path_helper import get_path

class MenuButton:
    def __init__(self, x, y, w, h, image_filename, fallback_color=(200,200,200)):
        # Rect for click detection
        self.rect = pygame.Rect(x, y, w, h)

        # Try to load the image
        try:
            img = pygame.image.load(get_path(image_filename)).convert_alpha()
            self.image = pygame.transform.scale(img, (w, h))
        except:
            # Fallback: colored rectangle if image missing
            surf = pygame.Surface((w, h))
            surf.fill(fallback_color)
            self.image = surf

    def draw(self, screen):
        # Draw the image (or fallback surface)
        screen.blit(self.image, self.rect.topleft)

    def is_clicked(self, pos):
        # Click detection
        return self.rect.collidepoint(pos)

class TextButton:
    def __init__(self, x, y, w, h, text, color=(255,255,255), border_color=(90,60,40)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.border_color = border_color

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=15)
        pygame.draw.rect(screen, self.border_color, self.rect, 3, border_radius=15)
        txt_surf = font.render(self.text, True, self.border_color)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        screen.blit(txt_surf, txt_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
