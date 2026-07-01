import pygame
import sys
import random
import os
from settings import *
from sprites import MenuButton, TextButton
from game_logic import GameEngine
import asset_loader

def main():
    pygame.init()
    pygame.mixer.init() 
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    # --- SETUP STATE & ASSETS ---
    volume = 50 
    music_playing = asset_loader.initialize_audio(volume)
    bg_img, cursor_img, kitchen_bg, cursor_assets = asset_loader.load_visual_assets()
    
    try:
        bg_img_2 = pygame.image.load(asset_loader.get_path("cafe_2_background.png")).convert()
        bg_img_2 = pygame.transform.scale(bg_img_2, (WIDTH, HEIGHT))
    except:
        bg_img_2 = None

    try:
        kitchen_bg_2 = pygame.image.load(asset_loader.get_path("kitchen_2_background.png")).convert()
        kitchen_bg_2 = pygame.transform.scale(kitchen_bg_2, (WIDTH, HEIGHT))
    except:
        kitchen_bg_2 = None
        
    sfx = asset_loader.load_audio_assets()

    font = pygame.font.SysFont("Arial", 24, bold=True)  
    title_font = pygame.font.SysFont("Arial", 100, bold=True)
    tv_font = pygame.font.SysFont("Comic Sans MS", 26, bold=True)
    
    engine = GameEngine()
    state = "MENU"

    cursor_state = "DEFAULT" 
    placed_drink_on_counter = None
    show_kitchen_tutorial = False

    # --- BUTTON INITIALIZATION ---
    # --- MAIN MENU (image buttons) ---
    btn_start     = MenuButton(CX - 700, CY - 440, 750, 400, "startgame.PNG")
    btn_save_menu = MenuButton(CX + 30, CY - 460, 750, 500, "managefiles.PNG")
    btn_settings  = MenuButton(CX - 690, CY - 20, 700, 400, "setting.PNG")
    btn_quit      = MenuButton(CX + 40, CY - 50, 700, 500, "quit.PNG")

# --- OTHER MENUS (text buttons) ---
    btn_continue_instructions = TextButton(CX - 150, HEIGHT - 90, 300, 60, "CONTINUE", GOLD)
    btn_start_cooking         = TextButton(CX - 160, CY + 180, 320, 60, "START SERVING", GOLD)

    btn_back_to_menu = TextButton(20, 20, 150, 50, "MENU")
    btn_save_game    = TextButton(20, 160, 240, 50, "SAVE (SLOT 1)", (144, 238, 144))
    btn_open_furn    = TextButton(WIDTH - 220, 20, 200, 50, "FURNITURES", (255, 182, 193))
    btn_open_cats    = TextButton(WIDTH - 226, 85, 200, 50, "CATS", (173, 216, 230))
    btn_go_kitchen   = TextButton(20, 90, 220, 50, "KITCHEN", GOLD)
    btn_leave_kitchen = TextButton(20, 20, 220, 50, "LEAVE", (200, 100, 100))
    btn_set_back     = TextButton(20, 20, 150, 50, "BACK")
    btn_music        = TextButton(CX - 150, CY - 80, 300, 80, f"MUSIC: {'ON' if music_playing else 'OFF'}")
    btn_vol_down     = TextButton(CX - 240, CY + 40, 80, 80, "-")
    btn_vol_up       = TextButton(CX + 160, CY + 40, 80, 80, "+")
    btn_shop_back    = TextButton(20, 20, 150, 50, "BACK")
    btn_next_level   = TextButton(CX + 160, 20, 180, 45, "NEXT CAFE ->", GOLD)


    slot_buttons = {
    1: TextButton(CX - 250, CY - 150, 320, 65, "Slot 1"),
    2: TextButton(CX - 250, CY - 75, 320, 65, "Slot 2"),
    3: TextButton(CX - 250, CY - 0, 320, 65, "Slot 3")
}

    delete_buttons = {
    1: TextButton(CX + 90, CY - 150, 160, 65, "WIPE", (255, 99, 71)),
    2: TextButton(CX + 90, CY - 75, 160, 65, "WIPE", (255, 99, 71)),
    3: TextButton(CX + 90, CY - 0, 160, 65, "WIPE", (255, 99, 71))
}

    btn_manual_load = TextButton(CX - 250, CY + 90, 500, 65, "LOAD SELECTED")
    btn_save_back   = TextButton(20, 20, 150, 50, "BACK")


    def play_ui_meow():
        chosen_meow = random.choice(["meow1", "meow2", "meow3"])
        if sfx[chosen_meow]: sfx[chosen_meow].play()

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if state == "GAME": engine.save_game(engine.active_slot)
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    if state == "MENU":
                        if btn_start.is_clicked(mouse_pos): 
                            play_ui_meow()
                            state = "INSTRUCTIONS" 
                        elif btn_save_menu.is_clicked(mouse_pos):
                            play_ui_meow()
                            state = "SAVE_MANAGER"
                        elif btn_settings.is_clicked(mouse_pos): 
                            play_ui_meow()
                            state = "SETTINGS"
                        elif btn_quit.is_clicked(mouse_pos): 
                            pygame.quit(); sys.exit()
                    
                    elif state == "INSTRUCTIONS":
                        if btn_continue_instructions.is_clicked(mouse_pos):
                            play_ui_meow()
                            state = "GAME" 

                    elif state == "SAVE_MANAGER":
                        if btn_save_back.is_clicked(mouse_pos):
                            play_ui_meow()
                            state = "MENU"
                        for slot, btn in slot_buttons.items():
                            if btn.is_clicked(mouse_pos):
                                play_ui_meow()
                                engine.active_slot = slot
                        for slot, btn in delete_buttons.items():
                            if btn.is_clicked(mouse_pos):
                                play_ui_meow()
                                engine.delete_save(slot)
                        if btn_manual_load.is_clicked(mouse_pos):
                            play_ui_meow()
                            engine.load_game(engine.active_slot)

                    elif state == "GAME":
                        if btn_back_to_menu.is_clicked(mouse_pos): 
                            play_ui_meow()
                            state = "MENU"
                        elif btn_save_game.is_clicked(mouse_pos):
                            play_ui_meow()
                            engine.save_game(engine.active_slot) 
                        elif btn_open_furn.is_clicked(mouse_pos): 
                            play_ui_meow()
                            state = "FURN_SHOP"
                        elif btn_open_cats.is_clicked(mouse_pos): 
                            play_ui_meow()
                            state = "CAT_SHOP"
                        elif btn_go_kitchen.is_clicked(mouse_pos): 
                            play_ui_meow()
                            state = "KITCHEN"
                            if engine.current_level == 1:
                                show_kitchen_tutorial = True  
                        elif engine.get_progression_percentage() >= 1.0 and btn_next_level.is_clicked(mouse_pos):
                            play_ui_meow()
                            engine.advance_to_next_level()
                        else:
                            engine.handle_mouse_down(mouse_pos)
                    
                    elif state == "KITCHEN":
                        if show_kitchen_tutorial:
                            if btn_start_cooking.is_clicked(mouse_pos):
                                play_ui_meow()
                                show_kitchen_tutorial = False
                        else:
                            if btn_leave_kitchen.is_clicked(mouse_pos):
                                play_ui_meow()
                                state = "GAME"
                                cursor_state = "DEFAULT"
                                placed_drink_on_counter = None

                            # --- LEVEL 1 KITCHEN FLOW ---
                            if engine.current_level < 2:
                                if engine.cups_stack_rect.collidepoint(mouse_pos):
                                    if cursor_state == "DEFAULT":
                                        cursor_state = "EMPTY_CUP"
                                        if sfx["cup"]: sfx["cup"].play()
                                elif engine.dispenser_right.collidepoint(mouse_pos) and cursor_state == "EMPTY_CUP":
                                    cursor_state = "CHOCOLATE"
                                    if sfx["liquid"]: sfx["liquid"].play()
                                elif engine.dispenser_middle.collidepoint(mouse_pos) and cursor_state == "EMPTY_CUP":
                                    cursor_state = "STRAWBERRY"
                                    if sfx["liquid"]: sfx["liquid"].play()
                                elif engine.dispenser_left.collidepoint(mouse_pos) and cursor_state == "EMPTY_CUP":
                                    cursor_state = "MILK TEA"
                                    if sfx["liquid"]: sfx["liquid"].play()
                                elif engine.counter_drop_rect.collidepoint(mouse_pos):
                                    if cursor_state in ["CHOCOLATE", "STRAWBERRY", "MILK TEA"]:
                                        placed_drink_on_counter = cursor_state
                                        cursor_state = "DEFAULT"
                                        if sfx["cup"]: sfx["cup"].play()
                                elif engine.bell_girl_rect.collidepoint(mouse_pos):
                                    if placed_drink_on_counter is not None:
                                        engine.process_serving(placed_drink_on_counter)
                                        placed_drink_on_counter = None
                                        if sfx["bell"]: sfx["bell"].play()

                            # --- LEVEL 2 KITCHEN FLOW ---
                            else:
                                cm = engine.coffee_machine_rect
                                kt = engine.kettle_rect

                                # Step 1: pick up cup
                                if engine.cups_stack_rect.collidepoint(mouse_pos) and cursor_state == "DEFAULT":
                                    cursor_state = "EMPTY_CUP"
                                    if sfx["cup"]: sfx["cup"].play()

                                # Coffee: cup -> bag -> powder -> machine -> COFFEE
                                elif engine.dispenser_right.collidepoint(mouse_pos) and cursor_state == "EMPTY_CUP":
                                    cursor_state = "COFFEE_POWDER"
                                    if sfx["cup"]: sfx["cup"].play()
                                elif cm and cm.collidepoint(mouse_pos) and cursor_state == "COFFEE_POWDER":
                                    cursor_state = "COFFEE"
                                    if sfx["liquid"]: sfx["liquid"].play()

                                # Tea: cup -> bag -> powder -> kettle -> TEA
                                elif engine.dispenser_middle.collidepoint(mouse_pos) and cursor_state == "EMPTY_CUP":
                                    cursor_state = "TEA_POWDER"
                                    if sfx["cup"]: sfx["cup"].play()
                                elif kt and kt.collidepoint(mouse_pos) and cursor_state == "TEA_POWDER":
                                    cursor_state = "TEA"
                                    if sfx["liquid"]: sfx["liquid"].play()

                                # Drop on counter
                                elif engine.counter_drop_rect.collidepoint(mouse_pos):
                                    if cursor_state in ["COFFEE", "TEA", "CROISSANT", "POLO BUN BUTTER"]:
                                        placed_drink_on_counter = cursor_state
                                        cursor_state = "DEFAULT"
                                        if sfx["cup"]: sfx["cup"].play()

                                # Ring bell to serve
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
                        
                        display_index = 0
                        for name in current_shop:
                            if name in ["CAT BED 2", "CAT BED 3", "CAT BED 4", "CAT HOUSE 2", "CAT HOUSE 3", "PLANT TABLE 2"]:
                                continue
                                
                            target_buy_name = name
                            if name == "CAT BED 1": target_buy_name = "CAT BED 1"
                            elif name == "CAT HOUSE 1": target_buy_name = "CAT HOUSE 1"
                            elif name == "PLANT TABLE 1": target_buy_name = "PLANT TABLE 1"
                                
                            if state == "FURN_SHOP":
                                col = display_index % 2
                                row = display_index // 2
                                temp_btn = TextButton(CX - 270 + (col * 290), 180 + (row * 75), 260, 60, name)
                            else:
                                temp_btn = TextButton(CX - 250, 220 + (display_index * 90), 500, 70, name)

                            if temp_btn.is_clicked(mouse_pos):
                                play_ui_meow()
                                engine.buy_item(target_buy_name, "furniture" if state == "FURN_SHOP" else "cats")
                            
                            display_index += 1

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

    # Background
             try:
                 menu_bg = pygame.image.load(asset_loader.get_path("mainmenu_background.PNG")).convert()
                 menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))
                 screen.blit(menu_bg, (0, 0))
             except:
                 screen.fill((255, 228, 225))  # fallback pastel pink

    # Draw buttons
             btn_start.draw(screen)
             btn_save_menu.draw(screen)
             btn_settings.draw(screen)
             btn_quit.draw(screen)


            
        elif state == "INSTRUCTIONS":
            pygame.mouse.set_visible(True)
            screen.fill(PASTEL_PINK)
            
            instr_title = title_font.render("HOW TO PLAY", True, BROWN)
            instr_title = pygame.transform.scale(instr_title, (int(instr_title.get_width()*0.5), int(instr_title.get_height()*0.5)))
            screen.blit(instr_title, (CX - instr_title.get_width() // 2, 40))
            
            instructions_text = [
                "1. Click the 'KITCHEN' button on the left side to prepare customer orders.",
                "2. Fulfill the drink requests there to earn Mao-Mao currency!",
                "3. Use your Mao-Maos to buy upgrades from the 'CATS' menu.",
                "4. Open the 'FURNITURES' menu anytime to buy and place cute decoration items.",
                "5. Remember to click the green 'SAVE' button regularly to preserve your game progress!",
                "6. Press WIPE on a save slot to delete it if you want to start fresh.",
                "7. You cannot go back to a previous level once you advance, so make sure to save before moving on!"
            ]
            
            for index, line in enumerate(instructions_text):
                line_surface = font.render(line, True, BROWN)
                screen.blit(line_surface, (CX - line_surface.get_width() // 2, 160 + (index * 65)))
                
            btn_continue_instructions.draw(screen, font)
        
        elif state == "SAVE_MANAGER":
            pygame.mouse.set_visible(True)
            screen.fill(PASTEL_PINK)
            title_lbl = font.render(f"ACTIVE WORKING POSITION: SLOT {engine.active_slot}", True, BROWN)
            screen.blit(title_lbl, (CX - title_lbl.get_width()//2, CY - 220))
            
            for slot, btn in slot_buttons.items():
                summary = engine.get_slot_summary(slot)
                btn.color = (173, 216, 230) if slot == engine.active_slot else (230, 230, 250)
                btn.text = f"Slot {slot} ({summary})" if "EMPTY" not in summary else f"Slot {slot}: [EMPTY]"
                btn.draw(screen, font)
                
            for slot, btn in delete_buttons.items():
                btn.draw(screen, font)
            btn_manual_load.draw(screen, font)
            btn_save_back.draw(screen, font)
        
        elif state == "GAME":
            pygame.mouse.set_visible(True)
            
            if engine.current_level >= 2 and bg_img_2:
                screen.blit(bg_img_2, (0, 0))
            elif bg_img:
                screen.blit(bg_img, (0, 0))
            else:
                screen.fill(GREEN_CAFE)

            btn_back_to_menu.draw(screen, font)
            btn_open_furn.draw(screen, font)
            btn_open_cats.draw(screen, font)
            btn_go_kitchen.draw(screen, font)
                
            pct = engine.get_progression_percentage()
            bar_width, bar_height = 300, 25
            bar_x, bar_y = CX - (bar_width // 2), 25
            
            pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height), border_radius=5)
            pygame.draw.rect(screen, (100, 230, 100), (bar_x, bar_y, int(bar_width * pct), bar_height), border_radius=5)
            
            lvl_text = font.render(f"Cafe Level: {engine.current_level}", True, WHITE)
            screen.blit(lvl_text, (bar_x - lvl_text.get_width() - 15, bar_y - 3))
            
            if pct >= 1.0:
                btn_next_level.draw(screen, font)
            
            btn_save_game.text = f"SAVE (SLOT {engine.active_slot})"
            btn_save_game.draw(screen, font) 
            
            for name, data in engine.furniture_items.items():
                if data[2] > 0 and name != getattr(engine, 'selected_furniture', None): 
                    screen.blit(data[4], data[4].get_rect(center=data[3]))
            
            for name, data in engine.cat_items.items():
                if data[2] > 0 and name != engine.selected_cat: 
                    screen.blit(data[4], data[4].get_rect(center=data[3]))

            if getattr(engine, 'selected_furniture', None):
                dragged_furn_data = engine.furniture_items[engine.selected_furniture]
                screen.blit(dragged_furn_data[4], dragged_furn_data[4].get_rect(center=dragged_furn_data[3]))

            if engine.selected_cat:
                dragged_data = engine.cat_items[engine.selected_cat]
                screen.blit(dragged_data[4], dragged_data[4].get_rect(center=dragged_data[3]))
            
            counter_txt = font.render(f"Mao-Maos: {int(engine.mao_mao)}", True, WHITE)
            screen.blit(counter_txt, (CX - counter_txt.get_width()//2, 60))

        elif state == "KITCHEN":
            if engine.current_level >= 2 and kitchen_bg_2:
                screen.blit(kitchen_bg_2, (0, 0))
            elif kitchen_bg: 
                screen.blit(kitchen_bg, (0, 0))
            else: 
                screen.fill((240, 200, 210))

            btn_leave_kitchen.draw(screen, font)

            draw_pos = engine.get_kitchen_draw_positions()

            tv_text = tv_font.render(f"ORDER: {engine.current_order}", True, (20, 40, 80))
            screen.blit(tv_text, (draw_pos["order_text_center_x"] - tv_text.get_width()//2, draw_pos["order_text_y"]))

            if placed_drink_on_counter is not None:
                drink_surface = cursor_assets[placed_drink_on_counter]
                screen.blit(drink_surface, draw_pos["drink_placement_pos"])

            counter_txt = font.render(f"Mao-Maos: {int(engine.mao_mao)}", True, BROWN)
            screen.blit(counter_txt, (WIDTH - 250, 25))

            if cursor_state == "DEFAULT":
                pygame.mouse.set_visible(True)
            else:
                pygame.mouse.set_visible(False)
                render_state = cursor_state
                if cursor_state == "EMPTY_CUP" and engine.current_level >= 2:
                    render_state = "EMPTY_CUP_L2"
                current_item_surface = cursor_assets[render_state]
                screen.blit(current_item_surface, (mouse_pos[0] - 150, mouse_pos[1] - 150))
                
            if show_kitchen_tutorial:
                pygame.mouse.set_visible(True)
                
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                screen.blit(overlay, (0, 0))
                
                popup_box = pygame.Rect(CX - 540, CY - 280, 1080, 560)
                pygame.draw.rect(screen, PASTEL_PINK, popup_box, border_radius=15)
                pygame.draw.rect(screen, BROWN, popup_box, width=5, border_radius=15)
                
                popup_title = font.render("DRINK PREPARATION TUTORIAL", True, BROWN)
                screen.blit(popup_title, (CX - popup_title.get_width() // 2, CY - 240))
                
                kitchen_steps = [
                    "1. Match the drink request shown on your TV monitor screen.",
                    "2. Click the stack of empty cups found on the top-right shelving unit.",
                    "3. Click the correct beverage dispenser tubes to mix up your items.",
                    "4. Drop the prepared cup directly down onto the tray.",
                    "5. Ring the golden bell to serve and get paid!"
                ]
                
                for idx, text_step in enumerate(kitchen_steps):
                    step_surf = font.render(text_step, True, (40, 30, 25))
                    screen.blit(step_surf, (CX - step_surf.get_width() // 2, CY - 130 + (idx * 55)))
                    
                btn_start_cooking.draw(screen, font)

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
            
            display_index = 0
            for name in current_shop:
                if name in ["CAT BED 2", "CAT BED 3", "CAT BED 4", "CAT HOUSE 2", "CAT HOUSE 3", "PLANT TABLE 2"]:
                    continue
                
                price, _, owned, _, _ = current_shop[name]
                
                if name == "CAT BED 1":
                    display_name = "CAT BED"
                elif name == "CAT HOUSE 1":
                    display_name = "CAT HOUSE"
                elif name == "PLANT TABLE 1":
                    display_name = "PLANT TABLE"
                else:
                    display_name = name
                
                if state == "FURN_SHOP":
                    col = display_index % 2
                    row = display_index // 2
                    btn = TextButton(CX - 270 + (col * 290), 180 + (row * 75), 260, 60, name)
                else:
                    btn = TextButton(CX - 250, 220 + (display_index * 90), 500, 70, name)
                
                btn.text = f"{display_name}: SOLD" if owned > 0 else f"{display_name}: {price} M"
                btn.draw(screen, font)
                display_index += 1

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
