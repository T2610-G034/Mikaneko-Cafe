class GameEngine:
    def __init__(self):
        self.mao_mao = 0
        self.click_value = 1 
        
        # Shop Data: { "Item Name": [Price, Benefit, Quantity, (x, y) Position, Color] }
        self.shop_items = {
            "CAT BED": [150, 1, 0, (400, 300), (255, 255, 255)],
            "PLANT": [250, 5, 0, (800, 350), (210, 180, 140)],
            "SCRATCHING POST": [500, 25, 0, (600, 200), (255, 215, 0)]
        }

    def add_click(self):
        self.mao_mao += self.click_value 

    def buy_item(self, item_name):
        item = self.shop_items[item_name]
        price = item[0]
        quantity = item[2]
        
        # Only allow purchase if they have enough money AND don't own it yet
        if self.mao_mao >= price and quantity < 1:
            self.mao_mao -= price
            self.click_value += item[1]
            self.shop_items[item_name][2] = 1 
            return True
        return False
