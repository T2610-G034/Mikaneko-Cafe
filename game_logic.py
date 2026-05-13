class GameEngine:
    def __init__(self):
        self.mao_mao = 0
        self.click_value = 1 
        self.passive_income = 0  # <--- Make sure this is here
        
        # Furniture Shop Data
        self.furniture_items = {
            "CAT BED": [150, 1, 0, (400, 300), (255, 255, 255)],
            "PLANT": [250, 5, 0, (800, 350), (210, 180, 140)],
        }

        # Cat Shop Data
        self.cat_items = {
            "COOKIE CAT": [100, 50, 0, (200, 500), (255, 165, 0)],
            "VANILLA CAT": [250, 150, 0, (1000, 500), (50, 50, 50)],
        }

    def add_click(self):
        self.mao_mao += self.click_value 

    # --- THIS IS THE MISSING METHOD FOR LINE 94 ---
    def update_passive(self, dt):
        """Adds passive income based on time passed (dt is in milliseconds)"""
        # Calculate passive income based on owned cats/furniture if you like
        # For now, it just adds the total passive_income divided by time
        self.mao_mao += (self.passive_income * dt) / 1000

    def buy_item(self, item_name, shop_type="furniture"):
        shop = self.furniture_items if shop_type == "furniture" else self.cat_items
        item = shop[item_name]
        price, benefit, owned = item[0], item[1], item[2]
        
        if self.mao_mao >= price and owned < 1:
            self.mao_mao -= price
            shop[item_name][2] = 1 
            
            # If it's a cat, maybe it adds passive income instead of click power!
            if shop_type == "cats":
                self.passive_income += benefit
            else:
                self.click_value += benefit
            return True
        return False
