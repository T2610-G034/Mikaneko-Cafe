import pygame
import sys
import random
import os
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
    btn_start        = MenuButton(CX - 150, CY - 140, 300, 70, "START GAME")
    btn_save_menu    = MenuButton(CX - 150, CY - 50, 300, 70, "MANAGE FILES", (230, 230, 250))
    btn_settings     = MenuButton(CX - 150, CY + 40, 300, 70, "SETTINGS")
    btn_quit         = MenuButton(CX - 150, CY + 130, 300, 70, "QUIT")
    
    btn_back_to_menu = MenuButton(20, 20, 150, 50, "MENU")
    
    # FIXED: Widened layout container from 150 to 240 pixels so the slot name text completely fits
    btn_save_game    = MenuButton(20, 160, 240, 50, "SAVE (SLOT 1)", (144, 238, 144))
    
    btn_open_furn    = MenuButton(WIDTH - 220, 20, 200, 50, "FURNITURES", (255, 182, 193))
    btn_open_cats    = MenuButton(WIDTH - 220, 85, 200, 50, "CATS", (173, 216, 230))
    
    btn_go_kitchen   = MenuButton(20, 90, 220, 50, "KITCHEN", GOLD)
    btn_leave_kitchen = MenuButton(20, 20, 220, 50, "LEAVE", (200, 100, 100))
    
    btn_set_back     = MenuButton(20, 20, 150, 50, "BACK")
    btn_music        = MenuButton(CX - 150, CY - 80, 300, 80, f"MUSIC: {'ON' if music_playing else 'OFF'}")
    btn_vol_down     = MenuButton(CX - 240, CY + 40, 80, 80, "-")
    btn_vol_up       = MenuButton(CX + 160, CY + 40, 80, 80, "+")
    btn_shop_back    = MenuButton(20, 20, 150, 50, "BACK")

    # Save Management Controls
    slot_buttons = {
        1: MenuButton(CX - 250, CY - 150, 320, 65, "Slot 1"),
        2: MenuButton(CX - 250, CY - 75, 320, 65, "Slot 2"),
        3: MenuButton(CX - 250, CY - 0, 320, 65, "Slot 3")
    }
    
    delete_buttons = {
        1: MenuButton(CX + 90, CY - 150, 160, 65, "WIPE", (255, 99, 71)),
        2: MenuButton(CX + 90, CY - 75, 160, 65, "WIPE", (255, 99, 71)),
        3: MenuButton(CX + 90, CY - 0, 160, 65, "WIPE", (255, 99, 71))
    }
    
    btn_manual_load   = MenuButton(CX - 250, CY + 90, 500, 65, "LOAD SELECTED SLOT", (144, 238, 144))
    btn_save_back     = MenuButton(20, 20, 150, 50, "BACK")

    furn_buttons = {name: MenuButton(CX - 250, 220 + (i * 90), 500, 70, name) for i, name in enumerate(engine.furniture_items)}
    cat_buttons = {name: MenuButton(CX - 250, 220 + (i * 90), 500, 70, name) for i, name in enumerate(engine.cat_items)}

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
                            state = "GAME"
                        elif btn_save_menu.is_clicked(mouse_pos):
                            play_ui_meow()
                            state = "SAVE_MANAGER"
                        elif btn_settings.is_clicked(mouse_pos): 
                            play_ui_meow()
                            state = "SETTINGS"
                        elif btn_quit.is_clicked(mouse_pos): 
                            pygame.quit(); sys.exit()
                    
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
                        else:
                            engine.handle_mouse_down(mouse_pos)
                    
                    elif state == "KITCHEN":
                        if btn_leave_kitchen.is_clicked(mouse_pos):
                            play_ui_meow()
                            state = "GAME"
                            cursor_state = "DEFAULT"
                            placed_drink_on_counter = None

                        elif engine.cups_stack_rect.collidepoint(mouse_pos):
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
            btn_start.draw(screen, font); btn_save_menu.draw(screen, font)
            btn_settings.draw(screen, font); btn_quit.draw(screen, font)
            
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
            if bg_img: screen.blit(bg_img, (0, 0))
            else: screen.fill(GREEN_CAFE)

            btn_back_to_menu.draw(screen, font)
            btn_open_furn.draw(screen, font)
            btn_open_cats.draw(screen, font)
            btn_go_kitchen.draw(screen, font)
            
            # Dynamically match label contents inside the clean layout box frame limits
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

            if placed_drink_on_counter is not None:
                drink_surface = cursor_assets[placed_drink_on_counter]
                screen.blit(drink_surface, (725, 390))

            counter_txt = font.render(f"Mao-Maos: {int(engine.mao_mao)}", True, BROWN)
            screen.blit(counter_txt, (WIDTH - 250, 25))

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
