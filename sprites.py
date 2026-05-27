import pygame
from settings import BROWN

class MenuButton:
    def __init__(self, x, y, w, h, text, color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.brown = BROWN

    def draw(self, screen, font):
        # 3D Shadow
        shadow = self.rect.copy()
        shadow.x += 5
        shadow.y += 5
        pygame.draw.rect(screen, (220, 180, 190), shadow, border_radius=15)
        
        # Main Button
        pygame.draw.rect(screen, self.color, self.rect, border_radius=15)
        pygame.draw.rect(screen, self.brown, self.rect, 3, border_radius=15)
        
        # Text
        txt_surf = font.render(self.text, True, self.brown)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        screen.blit(txt_surf, txt_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
