import pygame
import random
from path_helper import get_path

class GameEngine:
    def __init__(self):
        # Game Currency
        self.mao_mao = 0
        
        # Original Shop Data (Kept safe)
        self.furniture_items = {
            "CAT BED": [15, 0, 0, (400, 600), self.load_img("cat_bed.png", (100, 80))], 
            "PLANT":   [25, 0, 0, (160, 530), self.load_img("plant.png", (60, 100))],
        }
        self.cat_items = {
            "COOKIE CAT":  [10, 0, 0, (200, 620), self.load_img("cookie_cat.png", (90, 90))],
            "VANILLA CAT": [25, 0, 0, (900, 620), self.load_img("vanilla_cat.png", (90, 90))],
        }

        # --- NEW KITCHEN MECHANICS ENGINE ---
        # Drink configuration: [Price, Weighted Probability Range (Higher price = lower chance)]
        self.drink_menu = {
            "CHOCOLATE": {"price": 10, "weight": 50},      # 50% chance
            "STRAWBERRY": {"price": 15, "weight": 35},     # 35% chance
            "BOBA MILK TEA": {"price": 20, "weight": 15}   # 15% chance
        }
        
        self.current_order = None
        self.reroll_order()

        # Visual Colliders directly matching your kitchen layout photo: Rect(x, y, width, height)
        self.cups_stack_rect = pygame.Rect(750, 40, 250, 200)      # Pyramid stack top right
        self.dispenser_left = pygame.Rect(210, 20, 150, 240)       # Boba Milk Tea Dispenser
        self.dispenser_middle = pygame.Rect(365, 20, 150, 240)     # Strawberry Dispenser
        self.dispenser_right = pygame.Rect(520, 20, 150, 240)      # Chocolate Dispenser
        self.counter_drop_rect = pygame.Rect(650, 480, 400, 100)   # Flat space right side of TV
        self.bell_girl_rect = pygame.Rect(1060, 490, 80, 120)      # Little girl placement spot

    def load_img(self, filename, size):
        try:
            path = get_path(filename)
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, size)
        except Exception as e:
            surf = pygame.Surface(size)
            surf.fill((255, 192, 203)) 
            return surf

    def reroll_order(self):
        """Selects a new random drink order based on weighted probability values."""
        drinks = list(self.drink_menu.keys())
        weights = [self.drink_menu[d]["weight"] for d in drinks]
        self.current_order = random.choices(drinks, weights=weights, k=1)[0]

    def process_serving(self, filled_drink_type):
        """Validates if the drink placed down matches the active television request."""
        target_drink = self.current_order
        drink_price = self.drink_menu[target_drink]["price"]

        if filled_drink_type == target_drink:
            self.mao_mao += drink_price
            success = True
        else:
            self.mao_mao = max(0, self.mao_mao - drink_price) # Penalize wallet balance
            success = False

        self.reroll_order() # Instantly change order on screen
        return success

    def buy_item(self, item_name, shop_type="furniture"):
        shop = self.furniture_items if shop_type == "furniture" else self.cat_items
        item = shop[item_name]
        if self.mao_mao >= item[0] and item[2] < 1:
            self.mao_mao -= item[0]
            item[2] = 1 
            return True
        return False
