class GameEngine:
    def __init__(self):
        self.mao_mao = 0
        self.click_value = 1 
        
        # Shop Data: [Price, (Unused Benefit), Owned, (x, y) Position, Color]
        self.furniture_items = {
            "CAT BED": [150, 0, 0, (400, 300), (255, 255, 255)],
            "PLANT": [250, 0, 0, (800, 350), (210, 180, 140)],
        }

        self.cat_items = {
            "COOKIE CAT": [100, 0, 0, (200, 500), (255, 165, 0)],
            "VANILLA CAT": [250, 0, 0, (1000, 500), (240, 240, 240)],
        }

    def add_click(self):
        # Always increases by 1 now
        self.mao_mao += self.click_value 

    def update_passive(self, dt):
        pass

    def buy_item(self, item_name, shop_type="furniture"):
        shop = self.furniture_items if shop_type == "furniture" else self.cat_items
        item = shop[item_name]
        price = item[0]
        owned = item[2]
        
        if self.mao_mao >= price and owned < 1:
            self.mao_mao -= price
            shop[item_name][2] = 1  # Mark as owned so it draws on screen
            return True
        return False
