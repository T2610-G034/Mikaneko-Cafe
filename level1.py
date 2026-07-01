"""
Level 1 data: furniture shop, cat shop, drink menu, and kitchen layout
for the LEVEL 1 cafe/kitchen (matches kitchen_background.png).
"""
import pygame


def get_furniture(load_img):
    return {
        "CAT BED 1":          [15, 0, 0, (350, 600), load_img("cat_bed.PNG", (300, 300))],
        "CAT BED 2":          [15, 0, 0, (420, 600), load_img("cat_bed.PNG", (300, 300))],
        "CAT BED 3":          [15, 0, 0, (490, 600), load_img("cat_bed.PNG", (300, 300))],
        "PLANT":              [25, 0, 0, (160, 530), load_img("plant.PNG", (180, 180))],
        "PLANT TABLE 1":      [10, 0, 0, (280, 550), load_img("planttable.PNG", (300, 300))],
        "PLANT TABLE 2":      [10, 0, 0, (620, 550), load_img("planttable.PNG", (300, 300))],
        "SCRATCHING POST":    [35, 0, 0, (850, 530), load_img("scratchingpost.PNG", (550, 550))],
        "SKIBBLES":           [10, 0, 0, (520, 660), load_img("catfood.PNG", (350, 350))],
        "SKIBBLES PACKET":    [40, 0, 0, (720, 640), load_img("catfoodpacket.PNG", (400, 400))],
        "CAT HOUSE 1":        [40, 0, 0, (1020, 550), load_img("cathouse.PNG", (300, 200))],
        "CAT HOUSE 2":        [40, 0, 0, (1090, 550), load_img("cathouse.PNG", (300, 200))],
        "CAT HOUSE 3":        [40, 0, 0, (1160, 550), load_img("cathouse.PNG", (300, 200))],
        "GLASS BOTTLE":       [15, 0, 0, (780, 480), load_img("bottledecorations.PNG", (200, 200))],
    }


def get_cat_items(load_img):
    return {
        "VANILLA CAT":    [10, 0, 0, (200, 620), load_img("cat_vanilla.PNG", (180, 180))],
        "GRAPE CAT":      [20, 0, 0, (380, 620), load_img("cat_grape.png", (180, 180))],
        "STRAWBERRY CAT": [30, 0, 0, (560, 620), load_img("cat_strawberry.png", (180, 180))],
        "MATCHA CAT":     [40, 0, 0, (740, 620), load_img("cat_matcha.png", (180, 180))],
        "COOKIE CAT":     [50, 0, 0, (920, 620), load_img("cat_cookie.png", (180, 180))],
    }


def get_drink_menu():
    return {
        "CHOCOLATE": {"price": 10, "weight": 50},
        "STRAWBERRY": {"price": 15, "weight": 35},
        "MILK TEA": {"price": 20, "weight": 15},
    }


def get_kitchen_layout():
    """Hitbox rects matched to kitchen_background.png."""
    return {
        "cups_stack_rect": pygame.Rect(750, 40, 250, 200),
        "dispenser_left": pygame.Rect(210, 20, 150, 240),
        "dispenser_middle": pygame.Rect(365, 20, 150, 240),
        "dispenser_right": pygame.Rect(520, 20, 150, 240),
        "counter_drop_rect": pygame.Rect(650, 480, 400, 100),
        "bell_girl_rect": pygame.Rect(1060, 490, 80, 120),
        "coffee_machine_rect": None,  # not used in level 1
        "kettle_rect": None,          # not used in level 1
    }


def get_kitchen_draw_positions():
    """Where to draw the order text and the placed drink, tuned to kitchen_background.png."""
    return {
        "order_text_center_x": 445,
        "order_text_y": 420,
        "drink_placement_pos": (725, 390),
    }
