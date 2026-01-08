import pygame
import random
import math

import character_movement
import attack_mechanism
import image_process

from characters.slime import slime_constants
from obstacles.blockage import blockage_constants
from obstacles.arrow import arrow_constants
from enemies.skeleton import skeleton_constants
from enemies.snake import snake_constants
from cards import card_constants
from background import map_constants
from background import menu_constants
from cursors import cursor_constants
from enemies import enemies_constants

from obstacles.blockage.blockage_sprite_sheet_data import blockage_data
from enemies.skeleton.skeleton_attack.skeleton_attack_sprite_sheet_data import skeleton_attack_data
from enemies.snake.snake_attack.snake_attack_sprite_sheet_data import snake_attack_data
pygame.init()
pygame.mixer.init()

#Screen stuff
screen_size = [map_constants.CAMERA_WIDTH, map_constants.CAMERA_HEIGHT]
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock() 

#Character
slime_still = pygame.image.load("characters/slime/slime_standing_still.png").convert_alpha()
slime_moving_right = pygame.image.load("characters/slime/slime_moving_right.png").convert_alpha()
slime_moving_left = pygame.image.load("characters/slime/slime_moving_left.png").convert_alpha()
slime_attack = pygame.image.load("characters/slime/slime_attack.png").convert_alpha()

slime_still = pygame.transform.scale(slime_still, (slime_constants.SLIME_WIDTH, slime_constants.SLIME_HEIGHT))
slime_moving_right = pygame.transform.scale(slime_moving_right, (slime_constants.SLIME_WIDTH, slime_constants.SLIME_HEIGHT))
slime_moving_left = pygame.transform.scale(slime_moving_left, (slime_constants.SLIME_WIDTH, slime_constants.SLIME_HEIGHT))
slime_stretch = pygame.transform.scale(slime_still, (slime_constants.SLIME_STRETCH_WIDTH, slime_constants.SLIME_STRETCH_HEIGHT))
slime_attack = pygame.transform.scale(slime_attack, (slime_constants.ATTACK_WIDTH, slime_constants.ATTACK_HEIGHT))

slime_still_hitbox = slime_still.get_rect(center = (screen_size[0]//2, screen_size[1]//2))
slime_moving_left_hitbox = slime_moving_left.get_rect(midbottom = slime_still_hitbox.midbottom)
slime_moving_right_hitbox = slime_moving_right.get_rect(midbottom = slime_still_hitbox.midbottom)
slime_stretch_hitbox = slime_stretch.get_rect(midbottom = slime_still_hitbox.midbottom)

slime_idle_anims = [slime_stretch, slime_still]
slime_idle_hitbox = [slime_stretch_hitbox, slime_still_hitbox]

def create_slime_player():
    return {
        "attack_type": slime_constants.ATTACK_TYPE,
        "sprite": slime_still,
        "hitbox": slime_still_hitbox.copy(),
        "health": slime_constants.SLIME_HEALTH,
        "speed": slime_constants.SLIME_SPEED,
        "projectile_attack": slime_attack,
        "projectile_damage": slime_constants.ATTACK_DAMAGE,
        "projectile_attack_radius": slime_constants.ATTACK_RADIUS,
        "projectile_attack_cd": slime_constants.ATTACK_COOLDOWN,
        "projectile_attack_speed": slime_constants.ATTACK_SPEED,
        "x": 0,
        "y": 0,
        "animation_cd": slime_constants.SLIME_ANIMATION_SPEED,
        "prev_animation_time": 0,
        "prev_attack_time": 0,
        "camera_offsetx": 0,
        "camera_offsety": 0,
        "still_sprite": slime_still,
        "still_hitbox": slime_still_hitbox,
        "moving_right_sprite": slime_moving_right,
        "moving_right_hitbox": slime_moving_right_hitbox,
        "moving_left_sprite": slime_moving_left,
        "moving_left_hitbox": slime_moving_left_hitbox,
        "idle_anims": slime_idle_anims,
        "idle_hitbox": slime_idle_hitbox,
        "cur_idle_frame": 0
    }

player = create_slime_player()
health_font = pygame.font.Font(None, 30)

#Backgrounds
map = pygame.image.load("background/start_map.png").convert()
map_infinite_generate = pygame.image.load("background/infinite_map.png").convert()
play_screen = pygame.image.load("background/play_screen.png").convert()
manual = pygame.image.load("background/manual.png").convert()
play_screen = pygame.transform.scale(play_screen, (screen_size[0], screen_size[1]))
manual = pygame.transform.scale(manual, (screen_size[0], screen_size[1]))
map = pygame.transform.scale(map, (map_constants.MAP_WIDTH, map_constants.MAP_HEIGHT))
map_infinite_generate = pygame.transform.scale(map_infinite_generate, (map_constants.MAP_WIDTH, map_constants.MAP_HEIGHT))

#Cards
card_cover = pygame.image.load("cards/card_cover.png").convert_alpha()
card_side = pygame.image.load("cards/card_side.png").convert_alpha()
attack_card = pygame.image.load("cards/attack_card.png").convert_alpha()
heal_card = pygame.image.load("cards/heal_card.png").convert_alpha()
ghost_card = pygame.image.load("cards/ghost_card.png").convert_alpha()
shield_card = pygame.image.load("cards/shield_card.png").convert_alpha()
qi_blast_card = pygame.image.load("cards/qi_blast_card.png").convert_alpha()
speed_card = pygame.image.load("cards/speed_card.png").convert_alpha()

card_cover = pygame.transform.scale(card_cover, (card_constants.CARD_WIDTH, card_constants.CARD_HEIGHT))
card_side = pygame.transform.scale(card_side, (card_constants.CARD_WIDTH, card_constants.CARD_HEIGHT))
attack_card = pygame.transform.scale(attack_card, (card_constants.CARD_WIDTH, card_constants.CARD_HEIGHT))
heal_card = pygame.transform.scale(heal_card, (card_constants.CARD_WIDTH, card_constants.CARD_HEIGHT))
ghost_card = pygame.transform.scale(ghost_card, (card_constants.CARD_WIDTH, card_constants.CARD_HEIGHT))
shield_card = pygame.transform.scale(shield_card, (card_constants.CARD_WIDTH, card_constants.CARD_HEIGHT))
qi_blast_card = pygame.transform.scale(qi_blast_card, (card_constants.CARD_WIDTH, card_constants.CARD_HEIGHT))
speed_card = pygame.transform.scale(speed_card, (card_constants.CARD_WIDTH, card_constants.CARD_HEIGHT))

#Obstacles
arrow = pygame.image.load("obstacles/arrow/arrow_sprite.png").convert_alpha()
arrow = pygame.transform.scale(arrow, (arrow_constants.ARROW_WIDTH, arrow_constants.ARROW_HEIGHT))

blockage_sprite_sheet = pygame.image.load("obstacles/blockage/sprite_sheet.png").convert_alpha()
blockage_frames = image_process.process_img(blockage_sprite_sheet, blockage_data)
for i in range(len(blockage_frames)):
    blockage_frames[i] = pygame.transform.scale(blockage_frames[i], (blockage_constants.BLOCKAGE_WIDTH, blockage_frames[i].height * blockage_constants.BLOCKAGE_HEIGHT_SCALE_FACTOR))

#Enemies
skeleton_idle = pygame.image.load("enemies/skeleton/skeleton_idle.png").convert_alpha()
skeleton_attack_sprite_sheet = pygame.image.load("enemies/skeleton/skeleton_attack/sprite_sheet.png").convert_alpha()
skeleton_idle = pygame.transform.scale(skeleton_idle, (skeleton_idle.width*skeleton_constants.SKELETON_WIDTH_SCALE_FACTOR, skeleton_idle.height*skeleton_constants.SKELETON_HEIGHT_SCALE_FACTOR))
skeleton_attack_frames = image_process.process_img(skeleton_attack_sprite_sheet, skeleton_attack_data)
for i in range(len(skeleton_attack_frames)):
    skeleton_attack_frames[i] = pygame.transform.scale(skeleton_attack_frames[i], (skeleton_attack_frames[i].width*skeleton_constants.SKELETON_WIDTH_SCALE_FACTOR, skeleton_attack_frames[i].height*skeleton_constants.SKELETON_HEIGHT_SCALE_FACTOR))

snake_idle = pygame.image.load("enemies/snake/snake_idle.png").convert_alpha()
snake_attack_sprite_sheet = pygame.image.load("enemies/snake/snake_attack/sprite_sheet.png").convert_alpha()
snake_attack_sprite = pygame.image.load("enemies/snake/snake_attack/snake_attack_sprite.png").convert_alpha()
snake_idle = pygame.transform.scale(snake_idle, (snake_idle.width*snake_constants.SNAKE_WIDTH_SCALE_FACTOR, snake_idle.height*snake_constants.SNAKE_HEIGHT_SCALE_FACTOR))
snake_attack_sprite = pygame.transform.scale(snake_attack_sprite, (snake_constants.SNAKE_PROJECTILE_WIDTH, snake_constants.SNAKE_PROJECTILE_HEIGHT))
snake_attack_frames = image_process.process_img(snake_attack_sprite_sheet, snake_attack_data)
for i in range(len(snake_attack_frames)):
    snake_attack_frames[i] = pygame.transform.scale(snake_attack_frames[i], (snake_attack_frames[i].width*snake_constants.SNAKE_WIDTH_SCALE_FACTOR, snake_attack_frames[i].height*snake_constants.SNAKE_HEIGHT_SCALE_FACTOR))

#Other settings and stuff:
pygame.mouse.set_visible(False)
ingame_cursor = pygame.image.load("cursors/ingame_cursor.png").convert_alpha()
menu_cursor = pygame.image.load("cursors/menu_cursor.png").convert_alpha()
ingame_cursor = pygame.transform.scale(ingame_cursor, (cursor_constants.CURSOR_WIDTH, cursor_constants.CURSOR_HEIGHT))
menu_cursor = pygame.transform.scale(menu_cursor, (cursor_constants.CURSOR_WIDTH, cursor_constants.CURSOR_HEIGHT))

def create_game_data():
    return {
        "attacks": [],
        "enemies": [],
        "arrows": [],
        "blockages": [],
        "score": 0,
        "prev_score": 0,
        "prev_arrow_spawn_time": 0,
        "prev_blockage_spawn_time": 0,
        "prev_score_upd": 0,
        "game_state": "in_menu",
        "cursor": menu_cursor,
        "dt": 0
    }

screen.fill("black")
game_data = create_game_data()
running = True

score_font = pygame.font.Font(None, 30)
menu_score_font = pygame.font.Font("fonts/menu_score_font.ttf", 40)

max_score = 0
with open ("score.txt", 'r') as file:
    for line in file:
        max_score = max(max_score, int(line.strip()))

#Stuff to note:
#Origin is in top left corner
#Y axis is inverted in Pygame (increasing y goes down)
#Anything time is milliseconds

#Features to Add:
#Cards to power up the player along the way
#Enemy pathfinding (Djirkstra's algo or A* star)
#Change a bunch of stuff to maps so its better, also put all the variables that needs to be updated inside a map so its better code

#Remember to ask teacher if I can use matrix (Already implemented)

while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open("score.txt", 'a') as file:
                file.write(str(game_data["score"]) + '\n')
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_data["game_state"] == "in_menu":
                if menu_constants.PLAY_BUTTON_HITBOX.collidepoint(mouse_pos):
                    game_data["game_state"] = "play"
                elif menu_constants.MANUAL_BUTTON_HITBOX.collidepoint(mouse_pos):
                    game_data["game_state"] = "in_manual"

    if game_data["game_state"] == "in_menu":
        screen.blit(play_screen, (0, 0))
        max_score_text = menu_score_font.render(f"{max_score}", False, (0, 0, 0))
        screen.blit(max_score_text, (screen_size[0] - max_score_text.get_width() + menu_constants.SCORE_RIGHT_PADDING, screen_size[1] - max_score_text.get_height() + menu_constants.SCORE_TOP_PADDING))
        if menu_constants.PLAY_BUTTON_HITBOX.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (255, 255, 0), menu_constants.PLAY_BUTTON_HITBOX, 2)
        elif menu_constants.MANUAL_BUTTON_HITBOX.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (255, 255, 0), menu_constants.MANUAL_BUTTON_HITBOX, 2)
        elif menu_constants.SETTINGS_BUTTON_HITBOX.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (255, 255, 0), menu_constants.SETTINGS_BUTTON_HITBOX, 2)
    
    elif game_data["game_state"] == "in_manual":
        screen.blit(manual, (0,0))
        if keys[pygame.K_ESCAPE]:
            game_data["game_state"] = "in_menu"

    else:
        game_data["cursor"] = ingame_cursor
        screen.fill("black")
        curtime = pygame.time.get_ticks()

        if player["health"] <= 0 or keys[pygame.K_ESCAPE]:
            max_score = max(game_data["score"], max_score)
            with open("score.txt", 'a') as file:
                file.write(str(game_data["score"]) + '\n')
            player = create_slime_player()
            game_data = create_game_data()

        #Update player movement
        player = character_movement.updatemovement(player, keys, curtime, game_data["dt"])
        player["camera_offsetx"] = max(player["camera_offsetx"], -screen_size[0]/2 + map_constants.MAP_X_CLAMP)
        player["camera_offsety"] = max(player["camera_offsety"], -screen_size[1]/2 + map_constants.MAP_BOTTOM_Y_CLAMP)
        player["camera_offsety"] = min(player["camera_offsety"], -screen_size[1]/2 + map.height + map_constants.MAP_TOP_Y_CLAMP)
        player["x"]= player["hitbox"].centerx + player["camera_offsetx"]
        player["y"] = player["hitbox"].centery + player["camera_offsety"]
    
        starttile = int(player["camera_offsetx"] / map.width)
        for i in range(starttile, starttile + 2):
            if i == 0:
                screen.blit(map, (-player["camera_offsetx"], -player["camera_offsety"]))
            elif i > 0:
                screen.blit(map_infinite_generate, ((i * map_infinite_generate.width) - player["camera_offsetx"], -player["camera_offsety"]))
        screen.blit(player["sprite"], player["hitbox"])

        #Update score
        game_data["score"] = max(game_data["score"], int(player["camera_offsetx"]/4))
        if curtime > game_data["prev_score_upd"] + map_constants.SCORE_UPD_CD:
            game_data["prev_score_upd"] = curtime
            game_data["prev_score"] = game_data["score"]
        score_text = score_font.render(f"Score: {game_data['prev_score']}", True, (255, 255, 255))
        screen.blit(score_text, (screen_size[0] - score_text.get_width() + map_constants.SCORE_RIGHT_PADDING, map_constants.SCORE_HEIGHT))
        health_text = health_font.render(f"Health: {player['health']}", True, (255, 255, 255))
        screen.blit(health_text, (screen_size[0] - health_text.get_width() + map_constants.HEALTH_RIGHT_PADDING, map_constants.HEALTH_HEIGHT))

        #Create new attacks
        if player["prev_attack_time"] < curtime - player["projectile_attack_cd"]:
            player["prev_attack_time"] = curtime
            game_data["attacks"].append(attack_mechanism.calculate_cur_ranged_attack(
                player,
                player["camera_offsetx"], 
                player["camera_offsety"],
                player["x"],
                player["y"],
                mouse_pos
            ))

        #Update attacks
        player["health"], game_data["attacks"] = attack_mechanism.update_ranged_attacks(
            game_data["attacks"], 
            screen,
            player["camera_offsetx"],
            player["camera_offsety"],
            player["health"],
            player["x"],
            player["y"],
            player["hitbox"],
            game_data["enemies"],
            game_data["dt"]
        )  

        #Draw character hitbox for testing
        #char_rect = player["hitbox"].copy()
        #char_rect.x = player["x"] - player["hitbox"].width//2
        #char_rect.y = player["y"] - player["hitbox"].height//2
        #pygame.draw.rect(screen, (0, 255, 0), char_rect, 2)

        occupied = [[False for _ in range(map_constants.NUM_BOX_TILES_X)] for _ in range(map_constants.NUM_BOX_TILES_Y)]

        #Update obstacles
        for a in game_data["arrows"]:
            row = int((a["y"] - map_constants.MIDDLE_BOX_START_Y) // map_constants.MIDDLE_BOX_HEIGHT)
            for col in range(map_constants.NUM_BOX_TILES_X):
                occupied[row % map_constants.NUM_BOX_TILES_Y][col] = True

        for b in game_data["blockages"]:
            col = int((b["x"] - map_constants.TOP_BOX_START_X) // map_constants.TOP_BOX_WIDTH)
            for row in range(map_constants.NUM_BOX_TILES_Y):
                occupied[row][col % map_constants.NUM_BOX_TILES_X] = True

        top_box_tile_x_player = int((player["x"] - map_constants.TOP_BOX_START_X) // map_constants.TOP_BOX_WIDTH)
        middle_box_tile_y_player = int((player["y"] - map_constants.MIDDLE_BOX_START_Y) // map_constants.MIDDLE_BOX_HEIGHT)

        if len(game_data["arrows"]) < arrow_constants.ARROW_SPAWN_CAP and game_data["prev_arrow_spawn_time"] < curtime - arrow_constants.ARROW_COOLDOWN:
            game_data["prev_arrow_spawn_time"] = curtime
            boxtile = max(random.randint(middle_box_tile_y_player - 1, middle_box_tile_y_player + 1), 0)
            arrow_x = screen_size[0] + player["camera_offsetx"]
            arrow_y = map_constants.MIDDLE_BOX_START_Y + boxtile * map_constants.MIDDLE_BOX_HEIGHT
            for i in range(map_constants.NUM_BOX_TILES_X):
                occupied[boxtile % map_constants.NUM_BOX_TILES_Y][i] = True
            game_data["arrows"].append({
                            "attack_type": arrow_constants.ARROW_TYPE, 
                            "projectile_sprite": arrow,
                            "x": arrow_x,
                            "y": arrow_y,
                            "projectile_speed_x": arrow_constants.ARROW_SPEED_X,
                            "projectile_speed_y": arrow_constants.ARROW_SPEED_Y,
                            "projectile_orig_x": arrow_x,
                            "projectile_orig_y": arrow_y,
                            "projectile_damage": arrow_constants.ARROW_DAMAGE,
                            "projectile_attack_radius": arrow_constants.ARROW_ATTACK_RADIUS
                        })

        if len(game_data["blockages"]) < blockage_constants.BLOCKAGE_SPAWN_CAP and game_data["prev_blockage_spawn_time"] < curtime - blockage_constants.BLOCKAGE_COOLDOWN:
            game_data["prev_blockage_spawn_time"] = curtime
            boxtile = max(random.randint(top_box_tile_x_player + 1, top_box_tile_x_player + 3), enemies_constants.SAFE_ZONE_TILES)
            blockage_x = boxtile * map_constants.TOP_BOX_WIDTH
            blockage_y = map_constants.TOP_BOX_START_Y
            for i in range(map_constants.NUM_BOX_TILES_Y):
                occupied[i][boxtile % map_constants.NUM_BOX_TILES_X] = True
            game_data["blockages"].append({
                                "attack_type": blockage_constants.BLOCKAGE_TYPE,
                                "screen": screen,
                                "idle_frame": blockage_frames[0],
                                "melee_attack_frames": blockage_frames, 
                                "melee_attack_animation_frame": 0,
                                "melee_animation_cd": blockage_constants.BLOCKAGE_ANIMATION_COOLDOWN, 
                                "melee_damage": blockage_constants.BLOCKAGE_DAMAGE, 
                                "melee_attack_radius": blockage_constants.BLOCKAGE_ATTACK_RADIUS,
                                "x": blockage_x, 
                                "y": blockage_y, 
                                "melee_prev_animation_upd": curtime
                            })

        player["health"], game_data["blockages"] = attack_mechanism.update_melee_attack(game_data["blockages"], player["x"], player["y"], player["hitbox"], player["health"], curtime, player["camera_offsetx"], player["camera_offsety"], screen)
        player["health"], game_data["arrows"] = attack_mechanism.update_ranged_attacks(game_data["arrows"], screen, player["camera_offsetx"], player["camera_offsety"], player["health"], player["x"], player["y"], player["hitbox"], game_data["enemies"], game_data["dt"])
        
        #Update enemies
        for enemy in game_data["enemies"][:]:
            if enemy["health"] <= 0:
                game_data["enemies"].remove(enemy)
            elif math.hypot(enemy["x"] - player["x"], enemy["y"] - player["y"]) > enemies_constants.DESPAWN_DISTANCE:
                game_data["enemies"].remove(enemy)
            else:
                col = int((enemy["x"] - map_constants.MIDDLE_BOX_START_X) // map_constants.MIDDLE_BOX_WIDTH)
                row = int((enemy["y"] - map_constants.MIDDLE_BOX_START_Y) // map_constants.MIDDLE_BOX_HEIGHT)
                occupied[row % map_constants.NUM_BOX_TILES_Y][col % map_constants.NUM_BOX_TILES_X] = True

        cur_enemies_count = len(game_data["enemies"])
        available_slots = []
        for i in range(map_constants.NUM_BOX_TILES_Y):
            for j in range(map_constants.NUM_BOX_TILES_X):
                tile_x = j + int(player["camera_offsetx"] / map_constants.MIDDLE_BOX_WIDTH)
                if occupied[i][j] == False and tile_x >= enemies_constants.SAFE_ZONE_TILES:
                    available_slots.append((i, j))

        num_enemies = random.randint(enemies_constants.ENEMIES_SPAWN_MIN - cur_enemies_count, enemies_constants.ENEMIES_SPAWN_CAP - cur_enemies_count)
        for _ in range(num_enemies):
            if len(available_slots) > 0:
                idx = random.randint(0, len(available_slots) - 1)
                i, j = available_slots[idx]
                available_slots.remove(available_slots[idx])

                enemy_type = random.randint(0, 1)
                enemy_x = map_constants.MIDDLE_BOX_START_X + (j * map_constants.MIDDLE_BOX_WIDTH) + max((int(player["camera_offsetx"] / map_constants.MIDDLE_BOX_WIDTH) * map_constants.MIDDLE_BOX_WIDTH), 0)
                enemy_y = map_constants.MIDDLE_BOX_START_Y + (i * map_constants.MIDDLE_BOX_HEIGHT) + max((int(player["camera_offsety"] / map_constants.MIDDLE_BOX_HEIGHT) * map_constants.MIDDLE_BOX_HEIGHT), 0)
                if enemy_type == 0:
                    snake_hitbox = snake_idle.get_rect(topleft=(enemy_x, enemy_y))
                    game_data["enemies"].append({
                                    "attack_type": snake_constants.SNAKE_ATTACK_TYPE,
                                    "hitbox": snake_hitbox,
                                    "health": snake_constants.SNAKE_HEALTH,
                                    "movement_speed": snake_constants.SNAKE_MOVEMENT_SPEED,
                                    "mob_type": snake_constants.SNAKE_TYPE,
                                    "screen": screen,
                                    "idle_frame": snake_idle,
                                    "melee_attack_frames": snake_attack_frames,
                                    "melee_attack_animation_frame": 0,
                                    "melee_animation_cd": snake_constants.SNAKE_ATTACK_ANIMATION_COOLDOWN,
                                    "melee_damage": snake_constants.SNAKE_MELEE_DAMAGE,
                                    "melee_attack_radius": snake_constants.SNAKE_ATTACK_RADIUS,
                                    "melee_prev_animation_upd": curtime,
                                    "projectile_attack": snake_attack_sprite,
                                    "projectile_attack_speed": snake_constants.SNAKE_PROJECTILE_SPEED,
                                    "projectile_damage": snake_constants.SNAKE_PROJECTILE_DAMAGE,
                                    "projectile_attack_radius": snake_constants.SNAKE_ATTACK_RADIUS,
                                    "projectile_attack_cooldown": snake_constants.SNAKE_PROJECTILE_ATTACK_COOLDOWN,
                                    "x": enemy_x, 
                                    "y": enemy_y,                           
                                    "prev_projectile_shot": curtime
                                })
                    
                elif enemy_type == 1:
                    skeleton_hitbox = skeleton_idle.get_rect(topleft=(enemy_x, enemy_y))
                    game_data["enemies"].append({
                        "attack_type": skeleton_constants.SKELETON_ATTACK_TYPE,
                        "hitbox": skeleton_hitbox,
                        "health": skeleton_constants.SKELETON_HEALTH,
                        "movement_speed": skeleton_constants.SKELETON_MOVEMENT_SPEED,
                        "mob_type": skeleton_constants.SKELETON_TYPE,
                        "screen": screen,
                        "idle_frame": skeleton_idle,
                        "melee_attack_frames": skeleton_attack_frames,
                        "melee_attack_animation_frame": 0,
                        "melee_animation_cd": skeleton_constants.SKELETON_ATTACK_ANIMATION_COOLDOWN,
                        "melee_damage": skeleton_constants.SKELETON_DAMAGE,
                        "melee_attack_radius": skeleton_constants.SKELETON_ATTACK_RADIUS,
                        "x": enemy_x, 
                        "y": enemy_y,                           
                        "melee_prev_animation_upd": curtime
                    })

        for i in range(len(game_data["enemies"])):
            if game_data["enemies"][i]["mob_type"] == "ranged":
                if math.hypot(game_data["enemies"][i]["x"] - player["x"], game_data["enemies"][i]["y"] - player["y"]) > snake_constants.SNAKE_PROJECTILE_OUTER_RADIUS and curtime > game_data["enemies"][i]["prev_projectile_shot"] + snake_constants.SNAKE_PROJECTILE_ATTACK_COOLDOWN:
                    game_data["enemies"][i]["prev_projectile_shot"] = curtime
                    game_data["attacks"].append(attack_mechanism.calculate_cur_ranged_attack(game_data["enemies"][i],
                                                                                            player["camera_offsetx"],
                                                                                            player["camera_offsety"],
                                                                                            player["x"],
                                                                                            player["y"],
                                                                                            mouse_pos
                                                                                        ))
                    
        player["health"], game_data["enemies"] = attack_mechanism.update_melee_attack(game_data["enemies"],
                                                                                    player["x"], 
                                                                                    player["y"], 
                                                                                    player["hitbox"], 
                                                                                    player["health"], 
                                                                                    curtime, 
                                                                                    player["camera_offsetx"], 
                                                                                    player["camera_offsety"],
                                                                                    screen)

    screen.blit(game_data["cursor"], (mouse_pos[0] - cursor_constants.CURSOR_WIDTH//2, mouse_pos[1] - cursor_constants.CURSOR_HEIGHT//2))
    game_data["dt"] = clock.tick(60) / 1000
    pygame.display.update()

pygame.quit()