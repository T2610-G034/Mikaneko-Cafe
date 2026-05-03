import pygame

# decorations (name, cost, position, colour)
decorations = [
    ("Lamp", 200, (100, 400), (255, 255, 0)),                     # yellow lamp
    ("Plant", 150, (300, 400), (0, 200, 0)),                      # green plant
    ("Scratching Post Cat", 300, (500, 200), (150, 75, 0))        # brown scratching post
]

def draw_button(screen, font, text, x, y, w, h):              # x,y: position of the button  
    rect = pygame.Rect(x, y, w, h)                            # w,h: width and height
    pygame.draw.rect(screen, (200, 200, 200), rect)           # draw rectangle w light gray
    label = font.render(text, True, (0, 0, 0))                # true for anti-aliasing # black colour
    screen.blit(label, (x+10, y+10))                          # makes the text centered inside button
    return rect                                               # clickable

def run_shop(screen, font, coins, purchased_decorations):     # display shop window and purchasing
     deco_buttons = []
     for i, (name, cost, pos, color) in enumerate(decorations):                                         # loops thru decorations list
          rect = draw_button(screen, font, f"{name} = {coins} coins", 200, 100 + i*60, 300, 50)         
          deco_buttons.append((rect, name, cost, pos, color))                                           # stores button rectangle + item info in deco buttons
     back_button = draw_button(screen, font, "Back", 300, 400, 100, 50)                                  # createa button labelled back # position 300, 400 # size 100, 50 # exit the shop button

# show coin balance at top
     coin_text = font.render(f"coins: {coins}", True, (255, 255, 255))
     screen.blit(coin_text, (20, 20))

# draw purchased decorations as rectangles
     for name, cost, pos, color in decorations:
         if name in purchased_decorations:
             pygame.draw.rect(screen, color, (pos[0], pos[1], 50, 50))

     for event in pygame.event.get():                                                   # event loop section
         if event.type == pygame.QUIT:                                                  # sends back current coin count, purcahsed items # stop running the shop
             return coins, purchased_decorations, False
         if event.type == pygame.MOUSEBUTTONDOWN:                                            # checks if press mouse button
             for rect, name, cost, pos, color in deco_buttons:                              # each button has clickable rectangle, item name, cost of the item, pos: where to draw after purchase, color of rectangle
                 if rect.collidepoint(event.pos):                                          # check if the mouse click is in the button
                     if coins >= cost and name not in purchased_decorations:               # player has enough coins, items havent buy yet, subtract cost from coins
                         coins -= cost
                         purchased_decorations.append(name)                              # adds item tu purchased list
                         message = font.render(f"Purchased {name}!", True, (255, 255, 255))  
                         screen.blit(message, (200, 350))                                 # show a message
                     else:
                        message = font.render(f"Not enough coins or already purchased!", True, (255, 255, 255))
                        screen.blit(message, (200, 350))
             if back_button.collidepoint(event.pos):                                        # if back button clicks, return coins, purchased items
                 return coins, purchased_decorations, False                                # exit the shop
          
     return coins, purchased_decorations, True


# standalone test where we test before merge with the menu upgrade system code

if __name__ == "__main__":                                                     # only run this standalone
     pygame.init()                                                             # starts all the pygame modules
     screen = pygame.display.set_mode((700, 500))
     font = pygame.font.SysFont(None, 19)

     coins = 500
     purchased_decorations = []                                                 # empty list
     in_shop = True                                                             # shop currently open

     while in_shop:
          screen.fill((50, 50, 50))                                                                                 # background colour - dark gray
          coins, purchased_decorations, in_shop = run_shop(screen, font, coins, purchased_decorations)              # run_shop function
          pygame.display.flip()                                                  # to see changes

pygame.quit()




