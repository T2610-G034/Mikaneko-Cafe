import pygame
import sys
import random
from settings import *
from sprites import MenuButton
from game_logic import GameEngine
import asset_loader

def main():
    pygame.init()
    pygame.mixer.init() 
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mika Neko Cafe")
    clock = pygame.time.Clock()
    
    # --- SETUP STATE & ASSETS ---
    volume = 50 
    music_playing = asset_loader.initialize_audio(volume)
    bg_img, cursor_img, kitchen_bg, cursor_assets = asset_loader.load_visual_assets()
    sfx = asset_loader.load_audio_assets()

    font = pygame.font.SysFont("Arial", 30, bold=True)
    title_font = pygame.font.SysFont("Arial", 100, bold=True)
    tv_font = pygame.font.SysFont("Comic Sans MS", 34, bold=True)
    
    engine = GameEngine()
    state = "MENU"

    # --- INTERACTION MOUSE STATES ---
    cursor_state = "DEFAULT" 
    placed_drink_on_counter = None

    # --- BUTTON INITIALIZATION ---
    btn_start        = MenuButton(CX - 150, CY - 100, 300, 80, "START GAME")
    btn_settings     = MenuButton(CX - 150, CY + 10, 300, 80, "SETTINGS")
    btn_quit         = MenuButton(CX - 150, CY + 120, 300, 80, "QUIT")
    btn_back_to_menu = MenuButton(20, 20, 150, 50, "MENU")
    
    btn_open_furn    = MenuButton(WIDTH - 220, 20, 200, 50, "FURNITURES", (255, 182, 193))
    btn_open_cats    = MenuButton(WIDTH - 220, 85, 200, 50, "CATS", (173, 216, 230))
    
    btn_go_kitchen   = MenuButton(20, 90, 220, 50, "KITCHEN", GOLD)
    btn_leave_kitchen = MenuButton(20, 20, 220, 50, "LEAVE", (200, 100, 100))
    
    btn_set_back     = MenuButton(20, 20, 150, 50, "BACK")
    btn_music        = MenuButton(CX - 150, CY - 80, 300, 80, f"MUSIC: {'ON' if music_playing else 'OFF'}")
    btn_vol_down     = MenuButton(CX - 240, CY + 40, 80, 80, "-")
    btn_vol_up       = MenuButton(CX + 160, CY + 40, 80, 80, "+")
    btn_shop_back    = MenuButton(20, 20, 150, 50, "BACK")

    furn_buttons = {name: MenuButton(CX - 250, 220 + (i * 90), 500, 70, name) for i, name in enumerate(engine.furniture_items)}
    cat_buttons = {name: MenuButton(CX - 250, 220 + (i * 90), 500, 70, name) for i, name in enumerate(engine.cat_items)}

    def play_ui_meow():
        chosen_meow = random.choice(["meow1", "meow2", "meow3"])
        if sfx[chosen_meow]: sfx[chosen_meow].play()

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left Click Down
                    if state == "MENU":
                        if btn_start.is_clicked(mouse_pos): 
                            play_ui_meow()
                            state = "GAME"
                        elif btn_settings.is_clicked(mouse_pos): 
                            play_ui_meow()
                            state = "SETTINGS"
                        elif btn_quit.is_clicked(mouse_pos): 
                            pygame.quit(); sys.exit()
                    
                    elif state == "GAME":
                        if btn_back_to_menu.is_clicked(mouse_pos): 
                            play_ui_meow()
                            state = "MENU"
                        elif btn_open_furn.is_clicked(mouse_pos): 
                            play_ui_meow()
                            state = "FURN_SHOP"
                        elif btn_open_cats.is_clicked(mouse_pos): 
                            play_ui_meow()
                            state = "CAT_SHOP"
                        elif btn_go_kitchen.is_clicked(mouse_pos): 
                            play_ui_meow()
                            state = "KITCHEN"
                        else:
                            engine.handle_mouse_down(mouse_pos)
                    
                    elif state == "KITCHEN":
                        if btn_leave_kitchen.is_clicked(mouse_pos):
                            play_ui_meow()
                            state = "GAME"
                            cursor_state = "DEFAULT"
                            placed_drink_on_counter = None

                        # Step 2: Grab empty cup
                        elif engine.cups_stack_rect.collidepoint(mouse_pos):
                            if cursor_state == "DEFAULT":
                                cursor_state = "EMPTY_CUP"
                                if sfx["cup"]: sfx["cup"].play()

                        # Step 3: Fill empty cup
                        elif engine.dispenser_right.collidepoint(mouse_pos) and cursor_state == "EMPTY_CUP":
                            cursor_state = "CHOCOLATE"
                            if sfx["liquid"]: sfx["liquid"].play()
                        elif engine.dispenser_middle.collidepoint(mouse_pos) and cursor_state == "EMPTY_CUP":
                            cursor_state = "STRAWBERRY"
                            if sfx["liquid"]: sfx["liquid"].play()
                        elif engine.dispenser_left.collidepoint(mouse_pos) and cursor_state == "EMPTY_CUP":
                            cursor_state = "MILK TEA"
                            if sfx["liquid"]: sfx["liquid"].play()

                        # Step 4: Place filled cup onto counter
                        elif engine.counter_drop_rect.collidepoint(mouse_pos):
                            if cursor_state in ["CHOCOLATE", "STRAWBERRY", "MILK TEA"]:
                                placed_drink_on_counter = cursor_state
                                cursor_state = "DEFAULT" 
                                if sfx["cup"]: sfx["cup"].play()

                        # Step 5: Serve cup via bell girl click
                        elif engine.bell_girl_rect.collidepoint(mouse_pos):
                            if placed_drink_on_counter is not None:
                                engine.process_serving(placed_drink_on_counter)
                                placed_drink_on_counter = None 
                                if sfx["bell"]: sfx["bell"].play()

                    elif state == "SETTINGS":
                        if btn_set_back.is_clicked(mouse_pos): 
                            play_ui_meow()
                            state = "MENU"
                        elif btn_music.is_clicked(mouse_pos):
                            play_ui_meow()
                            music_playing = not music_playing
                            pygame.mixer.music.unpause() if music_playing else pygame.mixer.music.pause()
                            btn_music.text = f"MUSIC: {'ON' if music_playing else 'OFF'}"
                        elif btn_vol_up.is_clicked(mouse_pos):
                            play_ui_meow()
                            volume = min(100, volume + 10); pygame.mixer.music.set_volume(volume/100)
                        elif btn_vol_down.is_clicked(mouse_pos):
                            play_ui_meow()
                            volume = max(0, volume - 10); pygame.mixer.music.set_volume(volume/100)
                    
                    elif state in ["FURN_SHOP", "CAT_SHOP"]:
                        if btn_shop_back.is_clicked(mouse_pos): 
                            play_ui_meow()
                            state = "GAME"
                        current_shop = engine.furniture_items if state == "FURN_SHOP" else engine.cat_items
                        current_btns = furn_buttons if state == "FURN_SHOP" else cat_buttons
                        for name, btn in current_btns.items():
                            if btn.is_clicked(mouse_pos): 
                                play_ui_meow()
                                engine.buy_item(name, "furniture" if state == "FURN_SHOP" else "cats")

            # --- INTERACTION RUNTIME EVENT BINDINGS ---
            elif event.type == pygame.MOUSEMOTION:
                if state == "GAME":
                    engine.handle_mouse_move(mouse_pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if state == "GAME":
                        engine.handle_mouse_up()

        # --- DRAWING PIPELINE ---
        if state == "MENU":
            pygame.mouse.set_visible(True)
            screen.fill(PASTEL_PINK)
            title_surf = title_font.render("Mika Neko Cafe", True, BROWN)
            screen.blit(title_surf, (CX - title_surf.get_width()//2, 100))
            btn_start.draw(screen, font); btn_settings.draw(screen, font); btn_quit.draw(screen, font)
        
        elif state == "GAME":
            pygame.mouse.set_visible(True)
            if bg_img: screen.blit(bg_img, (0, 0))
            else: screen.fill(GREEN_CAFE)

            btn_back_to_menu.draw(screen, font)
            btn_open_furn.draw(screen, font)
            btn_open_cats.draw(screen, font)
            btn_go_kitchen.draw(screen, font)
            
            # Draw Furniture
            for name, data in engine.furniture_items.items():
                if data[2] > 0: 
                    screen.blit(data[4], data[4].get_rect(center=data[3]))
            
            # Draw Cats (Except the one being dragged right now)
            for name, data in engine.cat_items.items():
                if data[2] > 0 and name != engine.selected_cat: 
                    screen.blit(data[4], data[4].get_rect(center=data[3]))

            # Layer Sorting: Draw the dragged cat last so it floats above everything else
            if engine.selected_cat:
                dragged_data = engine.cat_items[engine.selected_cat]
                screen.blit(dragged_data[4], dragged_data[4].get_rect(center=dragged_data[3]))
            
            counter_txt = font.render(f"Mao-Maos: {int(engine.mao_mao)}", True, WHITE)
            screen.blit(counter_txt, (CX - counter_txt.get_width()//2, 30))

        elif state == "KITCHEN":
            if kitchen_bg: 
                screen.blit(kitchen_bg, (0, 0))
            else: 
                screen.fill((240, 200, 210))
                pygame.draw.rect(screen, (150, 150, 150), (120, 260, 900, 30)) 
                pygame.draw.rect(screen, (50, 160, 240), (240, 340, 410, 210)) 
                pygame.draw.circle(screen, (200, 80, 80), (1100, 550), 35)      

            btn_leave_kitchen.draw(screen, font)

            tv_text = tv_font.render(f"ORDER: {engine.current_order}", True, (20, 40, 80))
            screen.blit(tv_text, (445 - tv_text.get_width()//2, 420))

            # --- UPDATED: Pushed X over to 725 to perfectly strike the right-hand side cursor position ---
            if placed_drink_on_counter is not None:
                drink_surface = cursor_assets[placed_drink_on_counter]
                screen.blit(drink_surface, (725, 390))

            counter_txt = font.render(f"Mao-Maos: {int(engine.mao_mao)}", True, BROWN)
            screen.blit(counter_txt, (WIDTH - 250, 25))

            # --- HARDWARE MOUSE HANDLING FOR DEFAULT STATE ---
            if cursor_state == "DEFAULT":
                pygame.mouse.set_visible(True) 
            else:
                pygame.mouse.set_visible(False) 
                current_item_surface = cursor_assets[cursor_state]
                screen.blit(current_item_surface, (mouse_pos[0] - 150, mouse_pos[1] - 150))

        elif state == "SETTINGS":
            pygame.mouse.set_visible(True)
            screen.fill(PASTEL_PINK)
            btn_music.draw(screen, font); btn_vol_down.draw(screen, font); btn_vol_up.draw(screen, font); btn_set_back.draw(screen, font)
            vol_label = font.render(f"VOLUME: {volume}%", True, BROWN)
            screen.blit(vol_label, (CX - vol_label.get_width()//2, CY + 65))
            
        elif state in ["FURN_SHOP", "CAT_SHOP"]:
            pygame.mouse.set_visible(True)
            screen.fill(PASTEL_PINK if state == "FURN_SHOP" else PASTEL_BLUE)
            btn_shop_back.draw(screen, font)
            current_shop = engine.furniture_items if state == "FURN_SHOP" else engine.cat_items
            current_btns = furn_buttons if state == "FURN_SHOP" else cat_buttons
            
            for name, btn in current_btns.items():
                price, _, owned, _, _ = current_shop[name]
                btn.text = f"{name}: SOLD" if owned > 0 else f"{name}: {price} M"
                btn.draw(screen, font)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
