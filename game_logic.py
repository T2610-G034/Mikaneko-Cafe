import pygame
import random
import json
import os
from path_helper import get_path

class GameEngine:
    def __init__(self):
        self.mao_mao = 0
        self.active_slot = 1
        self.current_level = 1
        
        # Base templates (Loaded by default)
        self.furniture_items = {}
        self.cat_items = {}
        self.drink_menu = {}
        
        self.load_level_data()

        self.cups_stack_rect = pygame.Rect(750, 40, 250, 200)      
        self.dispenser_left = pygame.Rect(210, 20, 150, 240)       
        self.dispenser_middle = pygame.Rect(365, 20, 150, 240)     
        self.dispenser_right = pygame.Rect(520, 20, 150, 240)      
        self.counter_drop_rect = pygame.Rect(650, 480, 400, 100)   
        self.bell_girl_rect = pygame.Rect(1060, 490, 80, 120)      
        
        self.selected_cat = None
        self.selected_furniture = None  
        self.offset_x = 0
        self.offset_y = 0

        self.load_game(slot=1)

    def load_img(self, filename, size):
        try:
            path = get_path(filename)
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, size)
        except:
            surf = pygame.Surface(size)
            surf.fill((255, 192, 203)) 
            return surf

    def load_level_data(self):
        """Replaces shop data dynamically based on the current active level."""
        if self.current_level >= 2:
            # --- LEVEL 2 FURNITURE, PRICES, & DIMENSIONS ---
            self.furniture_items = {
                "SETS OF HIGH CHAIR": [30, 0, 0, (680, 600), self.load_img("setsofhighchair.png", (280, 200))],
                "SETS OF PLANT":      [20, 0, 0, (600, 480), self.load_img("setsofplant.png", (780, 340))],
                "FAIRY LIGHTS":       [10, 0, 0, (280, 220), self.load_img("fairylights.png", (280, 90))],
            }
            # --- LEVEL 2 DRINK MENU ---
            self.drink_menu = {
                "COFFEE": {"price": 30, "weight": 35},      
                "TEA": {"price": 35, "weight": 35},     
                "POLO BUN BUTTER": {"price": 45, "weight": 15},
                "CROISSANT": {"price": 50, "weight": 15}
            }
            # --- LEVEL 2 CATS ---
            self.cat_items = {
                "BAKERY CAT": [25, 0, 0, (300, 620), self.load_img("cat_bakery.png", (180, 180))],
                "CHEF CAT":   [50, 0, 0, (600, 620), self.load_img("cat_chef.png", (180, 180))]
            }
        else:
            # --- LEVEL 1 DEFAULT FURNITURE ---
            self.furniture_items = {
                "CAT BED 1":          [15, 0, 0, (350, 600), self.load_img("cat_bed.PNG", (300, 300))], 
                "CAT BED 2":          [15, 0, 0, (420, 600), self.load_img("cat_bed.PNG", (300, 300))], 
                "CAT BED 3":          [15, 0, 0, (490, 600), self.load_img("cat_bed.PNG", (300, 300))], 
                "PLANT":              [25, 0, 0, (160, 530), self.load_img("plant.PNG", (180, 180))],
                "PLANT TABLE 1":      [10, 0, 0, (280, 550), self.load_img("planttable.PNG", (300, 300))],
                "PLANT TABLE 2":      [10, 0, 0, (620, 550), self.load_img("planttable.PNG", (300, 300))],
                "SCRATCHING POST":    [35, 0, 0, (850, 530), self.load_img("scratchingpost.PNG", (550, 550))],
                "SKIBBLES":           [10, 0, 0, (520, 660), self.load_img("catfood.PNG", (350, 350))],
                "SKIBBLES PACKET":    [40, 0, 0, (720, 640), self.load_img("catfoodpacket.PNG", (400, 400))],
                "CAT HOUSE 1":        [40, 0, 0, (1020, 550), self.load_img("cathouse.PNG", (300, 200))],
                "CAT HOUSE 2":        [40, 0, 0, (1090, 550), self.load_img("cathouse.PNG", (300, 200))],
                "CAT HOUSE 3":        [40, 0, 0, (1160, 550), self.load_img("cathouse.PNG", (300, 200))],
                "GLASS BOTTLE":       [15, 0, 0, (780, 480), self.load_img("bottledecorations.PNG", (200, 200))],
            }
            # --- LEVEL 1 DEFAULT DRINK MENU ---
            self.drink_menu = {
                "CHOCOLATE": {"price": 10, "weight": 50},      
                "STRAWBERRY": {"price": 15, "weight": 35},     
                "MILK TEA": {"price": 20, "weight": 15}        
            }
            # --- LEVEL 1 DEFAULT CATS ---
            self.cat_items = {
                "VANILLA CAT":    [10, 0, 0, (200, 620), self.load_img("cat_vanilla.PNG", (180, 180))],
                "GRAPE CAT":      [20, 0, 0, (380, 620), self.load_img("cat_grape.png", (180, 180))],
                "STRAWBERRY CAT": [30, 0, 0, (560, 620), self.load_img("cat_strawberry.png", (180, 180))],
                "MATCHA CAT":     [40, 0, 0, (740, 620), self.load_img("cat_matcha.png", (180, 180))],
                "COOKIE CAT":     [50, 0, 0, (920, 620), self.load_img("cat_cookie.png", (180, 180))],
            }
        self.reroll_order()

    def reroll_order(self):
        drinks = list(self.drink_menu.keys())
        weights = [self.drink_menu[d]["weight"] for d in drinks]
        self.current_order = random.choices(drinks, weights=weights, k=1)[0]

    def process_serving(self, filled_drink_type):
        target_drink = self.current_order
        drink_price = self.drink_menu[target_drink]["price"]
        if filled_drink_type == target_drink:
            self.mao_mao += drink_price
        else:
            self.mao_mao = max(0, self.mao_mao - drink_price) 
        self.reroll_order() 
        self.save_game(self.active_slot)    
        return True

    def buy_item(self, item_name, shop_type="furniture"):
        shop = self.furniture_items if shop_type == "furniture" else self.cat_items
        if item_name in shop:
            item = shop[item_name]
            if self.mao_mao >= item[0] and item[2] < 1:
                self.mao_mao -= item[0]
                
                # Bundle Purchase Logic
                if item_name == "CAT BED 1":
                    if "CAT BED 1" in shop: shop["CAT BED 1"][2] = 1
                    if "CAT BED 2" in shop: shop["CAT BED 2"][2] = 1
                    if "CAT BED 3" in shop: shop["CAT BED 3"][2] = 1
                elif item_name == "CAT HOUSE 1":
                    if "CAT HOUSE 1" in shop: shop["CAT HOUSE 1"][2] = 1
                    if "CAT HOUSE 2" in shop: shop["CAT HOUSE 2"][2] = 1
                    if "CAT HOUSE 3" in shop: shop["CAT HOUSE 3"][2] = 1
                elif item_name == "PLANT TABLE 1":
                    if "PLANT TABLE 1" in shop: shop["PLANT TABLE 1"][2] = 1
                    if "PLANT TABLE 2" in shop: shop["PLANT TABLE 2"][2] = 1
                else:
                    item[2] = 1 
                
                self.save_game(self.active_slot)  
                return True
        return False

    def handle_mouse_down(self, mouse_pos):
        for name, data in reversed(self.cat_items.items()):
            if data[2] > 0:  
                img_rect = data[4].get_rect(center=data[3])
                if img_rect.collidepoint(mouse_pos):
                    self.selected_cat = name
                    self.offset_x = data[3][0] - mouse_pos[0]
                    self.offset_y = data[3][1] - mouse_pos[1]
                    return  

        for name, data in reversed(self.furniture_items.items()):
            if data[2] > 0:  
                img_rect = data[4].get_rect(center=data[3])
                if img_rect.collidepoint(mouse_pos):
                    self.selected_furniture = name
                    self.offset_x = data[3][0] - mouse_pos[0]
                    self.offset_y = data[3][1] - mouse_pos[1]
                    return

    def handle_mouse_move(self, mouse_pos):
        if self.selected_cat:
            new_x = mouse_pos[0] + self.offset_x
            new_y = mouse_pos[1] + self.offset_y
            self.cat_items[self.selected_cat][3] = (new_x, new_y)
        elif self.selected_furniture:
            new_x = mouse_pos[0] + self.offset_x
            new_y = mouse_pos[1] + self.offset_y
            self.furniture_items[self.selected_furniture][3] = (new_x, new_y)

    def handle_mouse_up(self):
        if self.selected_cat or self.selected_furniture:
            self.save_game(self.active_slot)  
        self.selected_cat = None
        self.selected_furniture = None

    def get_filename(self, slot):
        return f"savegame_slot{slot}.json"

    def save_game(self, slot):
        self.active_slot = slot
        filename = self.get_filename(slot)
        save_data = {
            "mao_mao": self.mao_mao,
            "current_level": self.current_level,
            "furniture": {name: {"owned": data[2], "pos": data[3]} for name, data in self.furniture_items.items()},
            "cats": {name: {"owned": data[2], "pos": data[3]} for name, data in self.cat_items.items()}
        }
        try:
            with open(filename, "w") as f:
                json.dump(save_data, f, indent=4)
        except Exception as e:
            print(f"Failed to save slot {slot}: {e}")

    def load_game(self, slot):
        filename = self.get_filename(slot)
        if not os.path.exists(filename):
            self.current_level = 1
            self.reset_state_variables()
            self.active_slot = slot
            return False
            
        try:
            with open(filename, "r") as f:
                save_data = json.load(f)
                
            self.mao_mao = save_data.get("mao_mao", 0)
            self.current_level = save_data.get("current_level", 1)
            self.active_slot = slot
            
            self.load_level_data()
            
            saved_furn = save_data.get("furniture", {})
            for name, saved_props in saved_furn.items():
                if name in self.furniture_items:
                    self.furniture_items[name][2] = saved_props.get("owned", 0)
                    self.furniture_items[name][3] = tuple(saved_props.get("pos", self.furniture_items[name][3]))
                    
            saved_cats = save_data.get("cats", {})
            for name, saved_props in saved_cats.items():
                if name in self.cat_items:
                    self.cat_items[name][2] = saved_props.get("owned", 0)
                    self.cat_items[name][3] = tuple(saved_props.get("pos", self.cat_items[name][3]))
            return True
        except Exception as e:
            print(f"Error loading slot {slot}: {e}")
            return False

    def delete_save(self, slot):
        filename = self.get_filename(slot)
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass
        if slot == self.active_slot:
            self.current_level = 1
            self.reset_state_variables()

    def reset_state_variables(self):
        self.mao_mao = 0
        self.load_level_data()
        for name in self.furniture_items:
            self.furniture_items[name][2] = 0
        for name in self.cat_items:
            self.cat_items[name][2] = 0

    def get_slot_summary(self, slot):
        filename = self.get_filename(slot)
        if not os.path.exists(filename):
            return "EMPTY SLOT"
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                return f"Slot {slot}: {int(data.get('mao_mao', 0))} M"
        except:
            return "CORRUPTED"

    def get_progression_percentage(self):
        total_items = len(self.furniture_items) + len(self.cat_items)
        if total_items == 0:
            return 1.0
        owned_count = sum(1 for d in self.furniture_items.values() if d[2] > 0)
        owned_count += sum(1 for d in self.cat_items.values() if d[2] > 0)
        return owned_count / total_items

    def advance_to_next_level(self):
        """Advances level counters and populates the Level 2 items."""
        self.current_level += 1
        self.load_level_data()
        self.save_game(self.active_slot)
