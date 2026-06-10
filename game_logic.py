import pygame
import random
from path_helper import get_path

class GameEngine:
    def __init__(self):
        # Game Currency
        self.mao_mao = 0
        
        # Original Shop Data (Kept safe)
        self.furniture_items = {
            "CAT BED": [15, 0, 0, (400, 600), self.load_img("cat_bed.png", (180, 180))], 
            "PLANT":   [25, 0, 0, (160, 530), self.load_img("plant.png", (180, 180))],
        }
        
        # FIXED: Spaced out X coordinates across the screen (200, 380, 560, 740, 920)
        self.cat_items = {
            "VANILLA CAT":    [10, 0, 0, (200, 620), self.load_img("cat_vanilla.png", (180, 180))],
            "GRAPE CAT":      [20, 0, 0, (380, 620), self.load_img("cat_grape.png", (180, 180))],
            "STRAWBERRY CAT": [30, 0, 0, (560, 620), self.load_img("cat_strawberry.png", (180, 180))],
            "MATCHA CAT":     [40, 0, 0, (740, 620), self.load_img("cat_matcha.png", (180, 180))],
            "COOKIE CAT":     [50, 0, 0, (920, 620), self.load_img("cat_cookie.png", (180, 180))],
        }

        # --- NEW KITCHEN MECHANICS ENGINE ---
        # Drink configuration: [Price, Weighted Probability Range (Higher price = lower chance)]
        self.drink_menu = {
            "CHOCOLATE": {"price": 10, "weight": 50},      # 50% chance
            "STRAWBERRY": {"price": 15, "weight": 35},     # 35% chance
            "MILK TEA": {"price": 20, "weight": 15}        # 15% chance
        }
        
        self.current_order = None
        self.reroll_order()

        self.cups_stack_rect = pygame.Rect(750, 40, 250, 200)      # Pyramid stack top right
        self.dispenser_left = pygame.Rect(210, 20, 150, 240)       # Tea Dispenser
        self.dispenser_middle = pygame.Rect(365, 20, 150, 240)     # Strawberry Dispenser
        self.dispenser_right = pygame.Rect(520, 20, 150, 240)      # Chocolate Dispenser
        self.counter_drop_rect = pygame.Rect(650, 480, 400, 100)   # Flat space right side of TV
        self.bell_girl_rect = pygame.Rect(1060, 490, 80, 120)      
        # --- ADDED DRAG AND DROP RUNTIME STATE ---
        self.selected_cat = None
        self.offset_x = 0
        self.offset_y = 0

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

    # --- ADDED INTERACTION ENGINE FOR DRAGGING ---
    def handle_mouse_down(self, mouse_pos):
        """Check if we clicked on an owned cat using its visual tuple coordinates."""
        for name, data in reversed(self.cat_items.items()):
            if data[2] > 0:  # If owned
                # Match main.py center logic to check collision accurately
                img_rect = data[4].get_rect(center=data[3])
                if img_rect.collidepoint(mouse_pos):
                    self.selected_cat = name
                    self.offset_x = data[3][0] - mouse_pos[0]
                    self.offset_y = data[3][1] - mouse_pos[1]
                    break

    def handle_mouse_move(self, mouse_pos):
        """Update the coordinate tuple dynamically inside your existing list structure."""
        if self.selected_cat:
            new_x = mouse_pos[0] + self.offset_x
            new_y = mouse_pos[1] + self.offset_y
            self.cat_items[self.selected_cat][3] = (new_x, new_y)

    def handle_mouse_up(self):
        """Release tracking safely."""
        self.selected_cat = None
