import pygame

# ---setup---
pygame.init()
screen = pygame.display.set_mode((700, 500))
pygame.display.set_caption("Drink system")
font = pygame.font.Font(None, 19)

# ---Drink Class ---
class Drink:
    def __init__(self, name, unlock_cost, coin_yield, pos_y):
        self.name = name
        self.unlock_cost = unlock_cost
        self.coin_yield = coin_yield
        self.unlocked = False
        self.pos_y = pos_y

    def unlock(self, coins):
        if coins >= self.unlock_cost and not self.unlocked:
            self.unlocked = True
            coins -= self.unlock_cost
            return coins, f"{self.name} unlocked!"
        elif self.unlocked:
            return coins, f"{self.name} already unlocked!"
        else:
            return coins, "Not enough coins!"
        
    def serve(self, coins):
        if self.unlocked:
            coins += self.coin_yield
            return coins, f"Served {self.name}! +{self.coin_yield} coins"
        else:
            return coins, f"{self.name} is locked."
        
# --- drink list ---
drinks = [
    Drink("Water", 0, 1, 60),
    Drink("coffee", 100, 3, 130),
    Drink("Bubble Tea", 200, 7, 200,),
    Drink("Strawberry Smoothie", 800, 15, 270),
    Drink("Chocolate Frappe", 2000, 30, 340)
]

coins = 500
message = ""

#---game loop---
running = True
while running:
    screen.fill((245, 235,220))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for drink in drinks:
                if 50 < x < 250 and drink.pos_y < y < drink.pos_y + 50:
                    coins, message = drink.unlock(coins)
                if 270 < x < 470 and drink.pos_y < y < drink.pos_y + 50:
                    coins, message = drink.serve(coins)

    #---display coins---
    coin_text = font.render(f"Coins: {coins}", True, (0, 0, 0))
    screen.blit(coin_text, (500, 30))

    #---draw buttons---
    for drink in drinks:
        pygame.draw.rect(screen, (180, 220, 180), (50, drink.pos_y, 200, 50))
        screen.blit(font.render(f"Unlock {drink.name}", True, (0, 0, 0)), (60, drink.pos_y + 10))

        pygame.draw.rect(screen, (200, 180, 220), (270, drink.pos_y, 200, 50))
        screen.blit(font.render(f"Serve {drink.name}", True, (0, 0, 0)), (280, drink.pos_y + 10))

    #---display message---
    msg_text = font.render(message, True, (0, 0, 0))
    screen.blit(msg_text, (50, 420))

    pygame.display.flip()

pygame.quit()


        