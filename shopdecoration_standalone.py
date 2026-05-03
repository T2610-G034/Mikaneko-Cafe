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





