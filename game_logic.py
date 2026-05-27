import pygame
from path_helper import get_path

class GameEngine:
    def __init__(self):
        self.mao_mao = 0
        self.click_value = 1 
        
        # Shop Data: [Price, (Unused) Benefit, Owned, (x, y) Position, Image_Surface]
        self.furniture_items = {
            "CAT BED": [15, 0, 0, (400, 600), self.load_img("cat_bed.png", (100, 80))], 
            "PLANT":   [25, 0, 0, (160, 530), self.load_img("plant.png", (60, 100))],
        }

        self.cat_items = {
            "COOKIE CAT":  [10, 0, 0, (200, 620), self.load_img("cookie_cat.png", (90, 90))],
            "VANILLA CAT": [25, 0, 0, (900, 620), self.load_img("vanilla_cat.png", (90, 90))],
        }

    def load_img(self, filename, size):
        """Loads, optimizes, and scales images for the main loop."""
        try:
            path = get_path(filename)
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, size)
        except Exception as e:
            print(f"Could not load {filename}: {e}")
            # Placeholder surface if image is missing
            surf = pygame.Surface(size)
            surf.fill((255, 192, 203)) 
            return surf

    def add_click(self):
        """Increases currency via manual clicks."""
        self.mao_mao += self.click_value 

    def buy_item(self, item_name, shop_type="furniture"):
        """Handles the transaction logic."""
        shop = self.furniture_items if shop_type == "furniture" else self.cat_items
        item = shop[item_name]
        
        if self.mao_mao >= item[0] and item[2] < 1:
            self.mao_mao -= item[0]
            item[2] = 1 
            return True
        return False
