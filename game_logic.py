class GameEngine:
    def __init__(self):
        self.mao_mao = 0
        self.click_value = 1  # How much you get per tap

    def add_click(self):
        self.mao_mao += self.click_value
