"""
Level 2 data: furniture shop, cat shop, drink menu, and kitchen layout
for the LEVEL 2 cafe/kitchen (matches kitchen_2_background.png).
"""
import pygame


def get_furniture(load_img):
    return {
        "SETS OF HIGH CHAIR": [30, 0, 0, (680, 600), load_img("setsofhighchair.png", (280, 200))],
        "SETS OF PLANT":      [20, 0, 0, (600, 480), load_img("setsofplant.png", (780, 340))],
        "FAIRY LIGHTS":       [10, 0, 0, (280, 220), load_img("fairylights.png", (280, 90))],
    }


def get_cat_items(load_img):
    return {
        "COFFEE CAT":          [25, 0, 0, (200, 600), load_img("cat_coffee.png", (180, 180))],
        "TEA CAT":             [50, 0, 0, (420, 600), load_img("cat_tea.png", (180, 180))],
        "LEMONADE CAT":        [75, 0, 0, (640, 600), load_img("cat_lemonade.png", (180, 180))],
        "CARAMEL PUDDING CAT": [100, 0, 0, (860, 600), load_img("cat_caramel_pudding.png", (180, 180))],
        "CAKE CAT":            [125, 0, 0, (1080, 600), load_img("cat_cake.png", (180, 180))],
    }


def get_drink_menu():
    return {
        "COFFEE": {"price": 30, "weight": 35},
        "TEA": {"price": 35, "weight": 35},
        "POLO BUN BUTTER": {"price": 45, "weight": 15},
        "CROISSANT": {"price": 50, "weight": 15},
    }


def get_kitchen_layout():
    """Hitbox rects matched to kitchen_2_background.png."""
    return {
        "cups_stack_rect": pygame.Rect(942, 310, 107, 140),
        "dispenser_left": pygame.Rect(367, 405, 208, 140),    # pastry tray/bread
        "dispenser_middle": pygame.Rect(699, 330, 113, 110),  # tea jar
        "dispenser_right": pygame.Rect(818, 330, 106, 110),   # coffee jar
        "counter_drop_rect": pygame.Rect(1049, 480, 118, 65),
        "bell_girl_rect": pygame.Rect(1179, 480, 77, 60),
        "coffee_machine_rect": pygame.Rect(1020, 260, 150, 230),  # espresso machine
        "kettle_rect": pygame.Rect(600, 410, 95, 90),             # kettle
    }


def get_kitchen_draw_positions():
    """Where to draw the order text and the placed drink, tuned to kitchen_2_background.png."""
    return {
        "order_text_center_x": 632,
        "order_text_y": 78,
        "drink_placement_pos": (958, 362),
    }
