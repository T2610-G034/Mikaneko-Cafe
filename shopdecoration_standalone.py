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
coin_text = font.render(f"coins: {coins}", true, (255, 255, 255))
screen.blit(coin_text, (20, 20))





