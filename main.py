import pygame
import random
import math
import character_movement
import attack_mechanism
from characters.slime import slime_constants
from obstacles.blockage import blockage_constants
from obstacles.arrow import arrow_constants
from enemies.skeleton import skeleton_constants
from enemies.snake import snake_constants
pygame.init()

#Camera settings
camerawidth = 1000
cameraheight = 680
cameraoffsetx = 0
cameraoffsety = 0

#Screen stuff
screen_size = [camerawidth, cameraheight]
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock() 

#Character
character_still = pygame.image.load("characters/slime/slime_standing_still.png").convert_alpha()
character_moving_right = pygame.image.load("characters/slime/slime_moving_right.png").convert_alpha()
character_moving_left = pygame.image.load("characters/slime/slime_moving_left.png").convert_alpha()
attack = pygame.image.load("characters/slime/slime_attack.png").convert_alpha()

character_still = pygame.transform.scale(character_still, (slime_constants.CHARACTER_WIDTH, slime_constants.CHARACTER_HEIGHT))
character_moving_right = pygame.transform.scale(character_moving_right, (slime_constants.CHARACTER_WIDTH, slime_constants.CHARACTER_HEIGHT))
character_moving_left = pygame.transform.scale(character_moving_left, (slime_constants.CHARACTER_WIDTH, slime_constants.CHARACTER_HEIGHT))
character_stretch = pygame.transform.scale(character_still, (slime_constants.CHARACTER_STRETCH_WIDTH, slime_constants.CHARACTER_STRETCH_HEIGHT))
attack = pygame.transform.scale(attack, (slime_constants.ATTACK_WIDTH, slime_constants.ATTACK_HEIGHT))
character_still_hitbox = character_still.get_rect(center = (screen_size[0]//2, screen_size[1]//2))
character_moving_left_hitbox = character_moving_left.get_rect(midbottom = character_still_hitbox.midbottom)
character_moving_right_hitbox = character_moving_right.get_rect(midbottom = character_still_hitbox.midbottom)
character_stretch_hitbox = character_stretch.get_rect(midbottom = character_still_hitbox.midbottom)

character = character_still
character_hitbox = character_still_hitbox
character_posx = 0
character_posy = 0
prev_attack_time = 0
prev_animation_time = 0
character_health = slime_constants.CHARACTER_HEALTH
health_font = pygame.font.Font(None, 30)
SAFE_ZONE_TILES = 10
attacks = []

#Backgrounds
map = pygame.image.load("background/start_map.png").convert()
map_infinite_generate = pygame.image.load("background/infinite_map.png").convert()
play_screen = pygame.image.load("background/play_screen.png").convert()
play_screen = pygame.transform.scale(play_screen, (screen_size[0], screen_size[1]))
map = pygame.transform.scale(map, (4130, 580))
map_infinite_generate = pygame.transform.scale(map_infinite_generate, (4130, 580))
NUM_BOX_TILES_X = 20
NUM_BOX_TILES_Y = 8
TOP_BOX_START_X = 55
TOP_BOX_START_Y = 0
TOP_BOX_WIDTH = 50
TOP_BOX_HEIGHT = 52
MIDDLE_BOX_START_X = 72
MIDDLE_BOX_START_Y = 50
MIDDLE_BOX_WIDTH = 75
MIDDLE_BOX_HEIGHT = 60

#Obstacles
arrow = pygame.image.load("obstacles/arrow/arrow_sprite.png").convert_alpha()
arrow = pygame.transform.scale(arrow, (arrow.width*arrow_constants.ARROW_WIDTH_SCALE_FACTOR, arrow.height*arrow_constants.ARROW_HEIGHT_SCALE_FACTOR))
arrows = []
prev_arrow_spawn_time = 0

blockage_frame_1 = pygame.image.load("obstacles/blockage/blockage_frame_1.png").convert_alpha()
blockage_frame_2 = pygame.image.load("obstacles/blockage/blockage_frame_2.png").convert_alpha()
blockage_frame_3 = pygame.image.load("obstacles/blockage/blockage_frame_3.png").convert_alpha()
blockage_frame_4 = pygame.image.load("obstacles/blockage/blockage_frame_4.png").convert_alpha()
blockage_frame_2 = pygame.transform.scale(blockage_frame_2, (blockage_frame_1.width*blockage_constants.BLOCKAGE_WIDTH_SCALE_FACTOR, blockage_frame_1.height*blockage_constants.BLOCKAGE_FRAME_2_HEIGHT_SCALE_FACTOR))
blockage_frame_3 = pygame.transform.scale(blockage_frame_3, (blockage_frame_1.width*blockage_constants.BLOCKAGE_WIDTH_SCALE_FACTOR, blockage_frame_1.height*blockage_constants.BLOCKAGE_FRAME_3_HEIGHT_SCALE_FACTOR))
blockage_frame_4 = pygame.transform.scale(blockage_frame_4, (blockage_frame_1.width*blockage_constants.BLOCKAGE_WIDTH_SCALE_FACTOR, blockage_frame_1.height*blockage_constants.BLOCKAGE_FRAME_4_HEIGHT_SCALE_FACTOR))
blockage_frame_1 = pygame.transform.scale(blockage_frame_1, (blockage_frame_1.width*blockage_constants.BLOCKAGE_WIDTH_SCALE_FACTOR, blockage_frame_1.height*blockage_constants.BLOCKAGE_FRAME_1_HEIGHT_SCALE_FACTOR))
blockage_frames = [blockage_frame_1, blockage_frame_2, blockage_frame_3, blockage_frame_4, blockage_frame_3, blockage_frame_2, blockage_frame_1]
blockages = []
prev_blockage_spawn_time = 0

#Enemies
skeleton_idle = pygame.image.load("enemies/skeleton/skeleton_idle.png").convert_alpha()
skeleton_attack_frame_1 = pygame.image.load("enemies/skeleton/skeleton_attack/skeleton_attack_frame_1.png").convert_alpha()
skeleton_attack_frame_2 = pygame.image.load("enemies/skeleton/skeleton_attack/skeleton_attack_frame_2.png").convert_alpha()
skeleton_idle = pygame.transform.scale(skeleton_idle, (skeleton_idle.width*skeleton_constants.SKELETON_WIDTH_SCALE_FACTOR, skeleton_idle.height*skeleton_constants.SKELETON_HEIGHT_SCALE_FACTOR))
skeleton_attack_frame_1 = pygame.transform.scale(skeleton_attack_frame_1, (skeleton_attack_frame_1.width*skeleton_constants.SKELETON_WIDTH_SCALE_FACTOR, skeleton_attack_frame_1.height*skeleton_constants.SKELETON_HEIGHT_SCALE_FACTOR))
skeleton_attack_frame_2 = pygame.transform.scale(skeleton_attack_frame_2, (skeleton_attack_frame_2.width*skeleton_constants.SKELETON_WIDTH_SCALE_FACTOR, skeleton_attack_frame_2.height*skeleton_constants.SKELETON_HEIGHT_SCALE_FACTOR))
skeleton_attack_frames = [skeleton_idle, skeleton_attack_frame_1, skeleton_attack_frame_2]

snake_idle = pygame.image.load("enemies/snake/snake_idle.png").convert_alpha()
snake_attack_frame_1 = pygame.image.load("enemies/snake/snake_attack/snake_attack_frame_1.png").convert_alpha()
snake_attack_sprite = pygame.image.load("enemies/snake/snake_attack/snake_attack_sprite.png").convert_alpha()
snake_idle = pygame.transform.scale(snake_idle, (snake_idle.width*snake_constants.SNAKE_WIDTH_SCALE_FACTOR, snake_idle.height*snake_constants.SNAKE_HEIGHT_SCALE_FACTOR))
snake_attack_frame_1 = pygame.transform.scale(snake_attack_frame_1, (snake_attack_frame_1.width*snake_constants.SNAKE_WIDTH_SCALE_FACTOR, snake_attack_frame_1.height*snake_constants.SNAKE_HEIGHT_SCALE_FACTOR))
snake_attack_sprite = pygame.transform.scale(snake_attack_sprite, (snake_attack_sprite.width*snake_constants.SNAKE_PROJECTILE_WIDTH_SCALE_FACTOR, snake_attack_sprite.height*snake_constants.SNAKE_PROJECTILE_HEIGHT_SCALE_FACTOR))
snake_attack_frames = [snake_idle, snake_attack_frame_1]

ENEMIES_SPAWN_MIN = 4
ENEMIES_SPAWN_CAP = 6
enemies = []

#Other settings and stuff:
pygame.mouse.set_visible(False)
CURSOR_WIDTH = 32
CURSOR_HEIGHT = 32
ingame_cursor = pygame.image.load("cursors/ingame_cursor.png").convert_alpha()
menu_cursor = pygame.image.load("cursors/menu_cursor.png").convert_alpha()
ingame_cursor = pygame.transform.scale(ingame_cursor, (CURSOR_WIDTH, CURSOR_HEIGHT))
menu_cursor = pygame.transform.scale(menu_cursor, (CURSOR_WIDTH, CURSOR_HEIGHT))
cursor = menu_cursor

play_button_hitbox = pygame.Rect(70, 270, 400, 80)
manual_button_hitbox = pygame.Rect(70, 350, 400, 80)
settings_button_hitbox = pygame.Rect(70, 430, 400, 80)

screen.fill("black")
game_state = "in_menu"
running = True

prev_score = 0
score = 0
score_upd_cd = 1000  #milliseconds
prev_score_upd = 0
score_font = pygame.font.Font(None, 30)

#Stuff to note:
#Origin is in top left corner
#Y axis is inverted in Pygame (increasing y goes down)

#Features to Add:
#Cards to power up the player along the way
#Score system
#Enemy pathfinding (Djirkstra's algo or A* star)

#Remember to ask teacher if I can use matrix (Already implemented)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open("score.txt", 'a') as file:
                file.write(str(score) + '\n')
            running = False

    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    if game_state == "in_menu":
        screen.blit(play_screen, (0, 0))
        max_score = 0
        with open ("score.txt", 'r') as file:
            for line in file:
                max_score = max(max_score, int(line.strip()))
        menu_score_font = pygame.font.Font("fonts/menu_score_font.ttf", 40)
        max_score_text = menu_score_font.render(f"{max_score}", False, (0, 0, 0))
        screen.blit(max_score_text, (screen_size[0] - max_score_text.get_width() - 20, screen_size[1] - max_score_text.get_height() - 60))
        
        if play_button_hitbox.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (255, 255, 0), play_button_hitbox, 2)
        elif manual_button_hitbox.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (255, 255, 0), manual_button_hitbox, 2)
        elif settings_button_hitbox.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (255, 255, 0), settings_button_hitbox, 2)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or mouse_pressed[0] and play_button_hitbox.collidepoint(mouse_pos):
            game_state = "play"

    else:
        cursor = ingame_cursor
        screen.fill("black")
        curtime = pygame.time.get_ticks()

        #print("Character HP " + str(character_health))
        if character_health <= 0:
            game_state = "in_menu"
            with open("score.txt", 'a') as file:
                file.write(str(score) + '\n')
            character = character_still
            character_hitbox = character_still_hitbox
            character_posx = 0
            character_posy = 0
            prev_attack_time = 0
            prev_animation_time = 0
            character_health = slime_constants.CHARACTER_HEALTH
            attacks = []
            cameraoffsetx = 0
            cameraoffsety = 0
            arrows = []
            blockages = []
            enemies = []
            occupied = [[False for _ in range(NUM_BOX_TILES_X)] for _ in range(NUM_BOX_TILES_Y)]
            prev_arrow_spawn_time = 0
            prev_blockage_spawn_time = 0
            score = 0

        #Update player movement
        character, character_hitbox, cameraoffsetx, cameraoffsety, prev_animation_time = character_movement.updatemovement(
            cameraoffsetx, 
            cameraoffsety, 
            character, 
            character_hitbox,
            character_still,
            character_still_hitbox,
            character_moving_right, 
            character_moving_right_hitbox,
            character_moving_left, 
            character_moving_left_hitbox,
            character_stretch, 
            character_stretch_hitbox, 
            prev_animation_time,
            curtime,
            slime_constants.ANIMATION_SPEED
        )
        cameraoffsetx = max(cameraoffsetx, -screen_size[0]/2 + 100)
        cameraoffsety = max(cameraoffsety, -screen_size[1]/2 + 50)
        cameraoffsety = min(cameraoffsety, -screen_size[1]/2 + map.height - 70)
        character_posx = character_hitbox.centerx + cameraoffsetx
        character_posy = character_hitbox.centery + cameraoffsety
    
        starttile = int(cameraoffsetx / map.width)
        for i in range(starttile, starttile + 2):
            if i == 0:
                screen.blit(map, (-cameraoffsetx, -cameraoffsety))
            elif i > 0:
                screen.blit(map_infinite_generate, ((i * map_infinite_generate.width) - cameraoffsetx, -cameraoffsety))
        screen.blit(character, character_hitbox)

        #Update score
        score = max(score, int(cameraoffsetx/4))
        if curtime > prev_score_upd + score_upd_cd:
            prev_score_upd = curtime
            prev_score = score
        score_text = score_font.render(f"Score: {prev_score}", True, (255, 255, 255))
        screen.blit(score_text, (screen_size[0] - score_text.get_width() - 20, 20))
        health_text = health_font.render(f"Health: {character_health}", True, (255, 255, 255))
        screen.blit(health_text, (screen_size[0] - health_text.get_width() - 20, 40))

        #Create new attacks
        if prev_attack_time < curtime - slime_constants.ATTACK_COOLDOWN:
            prev_attack_time = curtime
            attacks.append(attack_mechanism.calculate_cur_ranged_attack(
                slime_constants.ATTACK_TYPE,
                character_posx - slime_constants.ATTACK_WIDTH//2, 
                character_posy - slime_constants.ATTACK_HEIGHT//2, 
                attack, 
                slime_constants.ATTACK_SPEED,
                slime_constants.ATTACK_RADIUS, 
                cameraoffsetx, 
                cameraoffsety,
                slime_constants.ATTACK_DAMAGE,
                character_posx,
                character_posy
            ))

        #Update attacks
        character_health, attacks = attack_mechanism.update_ranged_attacks(
            attacks, 
            screen,
            cameraoffsetx,
            cameraoffsety,
            character_health,
            character_posx,
            character_posy,
            character_hitbox,
            enemies
        )  

        #Draw character hitbox for testing
        #char_rect = character_hitbox.copy()
        #char_rect.x = character_posx - character_hitbox.width//2
        #char_rect.y = character_posy - character_hitbox.height//2
        #pygame.draw.rect(screen, (0, 255, 0), char_rect, 2)

        occupied = [[False for _ in range(NUM_BOX_TILES_X)] for _ in range(NUM_BOX_TILES_Y)]

        #Update obstacles
        for a in arrows:
            row = int((a[3] - MIDDLE_BOX_START_Y) // MIDDLE_BOX_HEIGHT)
            for col in range(NUM_BOX_TILES_X):
                occupied[row % NUM_BOX_TILES_Y][col] = True

        for b in blockages:
            col = int((b[8] - TOP_BOX_START_X) // TOP_BOX_WIDTH)
            for row in range(NUM_BOX_TILES_Y):
                occupied[row][col % NUM_BOX_TILES_X] = True

        top_box_tile_x_player = int((character_posx - TOP_BOX_START_X) // TOP_BOX_WIDTH)
        middle_box_tile_y_player = int((character_posy - MIDDLE_BOX_START_Y) // MIDDLE_BOX_HEIGHT)

        if len(arrows) < arrow_constants.ARROW_SPAWN_CAP and prev_arrow_spawn_time < curtime - arrow_constants.ARROW_COOLDOWN:
            prev_arrow_spawn_time = curtime
            boxtile = max(random.randint(middle_box_tile_y_player - 1, middle_box_tile_y_player + 1), 0)
            arrow_x = screen_size[0] + cameraoffsetx
            arrow_y = MIDDLE_BOX_START_Y + boxtile * MIDDLE_BOX_HEIGHT
            for i in range(NUM_BOX_TILES_X):
                occupied[boxtile % NUM_BOX_TILES_Y][i] = True
            arrows.append([
                            arrow_constants.ARROW_TYPE, 
                            arrow,
                            arrow_x,
                            arrow_y,
                            arrow_constants.ARROW_SPEED,
                            0,
                            arrow_x,
                            arrow_y,
                            arrow_constants.ARROW_DAMAGE,
                            arrow_constants.ARROW_ATTACK_RADIUS
                        ])

        if len(blockages) < blockage_constants.BLOCKAGE_SPAWN_CAP and prev_blockage_spawn_time < curtime - blockage_constants.BLOCKAGE_COOLDOWN:
            prev_blockage_spawn_time = curtime
            boxtile = max(random.randint(top_box_tile_x_player - 1, top_box_tile_x_player + 1), SAFE_ZONE_TILES)
            blockage_x = boxtile * TOP_BOX_WIDTH
            blockage_y = TOP_BOX_START_Y
            for i in range(NUM_BOX_TILES_Y):
                occupied[i][boxtile % NUM_BOX_TILES_X] = True
            blockages.append([
                                blockage_constants.BLOCKAGE_TYPE,
                                screen,
                                blockage_frames[0],
                                blockage_frames, 
                                0,
                                blockage_constants.BLOCKAGE_ANIMATION_COOLDOWN, 
                                blockage_constants.BLOCKAGE_DAMAGE, 
                                blockage_constants.BLOCKAGE_ATTACK_RADIUS,
                                blockage_x, 
                                blockage_y, 
                                curtime
                            ])

        character_health, blockages = attack_mechanism.update_melee_attack(blockages, character_posx, character_posy, character_hitbox, character_health, curtime, cameraoffsetx, cameraoffsety)
        character_health, arrows = attack_mechanism.update_ranged_attacks(arrows, screen, cameraoffsetx, cameraoffsety, character_health, character_posx, character_posy, character_hitbox, enemies)
        
        #Update enemies
        for enemy in enemies:
            if enemy[2] <= 0:
                enemies.remove(enemy)
            else:
                if len(enemy) == 16: #Ranged
                    row = int((enemy[-3] - MIDDLE_BOX_START_Y) // MIDDLE_BOX_HEIGHT)
                    col = int((enemy[-4] - MIDDLE_BOX_START_X) // MIDDLE_BOX_WIDTH)
                    occupied[row % NUM_BOX_TILES_Y][col % NUM_BOX_TILES_X] = True
                else: #Melee
                    row = int((enemy[-2] - MIDDLE_BOX_START_Y) // MIDDLE_BOX_HEIGHT)
                    col = int((enemy[-3] - MIDDLE_BOX_START_X) // MIDDLE_BOX_WIDTH)
                    occupied[row % NUM_BOX_TILES_Y][col % NUM_BOX_TILES_X] = True

        cur_enemies_count = len(enemies)
        available_slots = []
        for i in range(NUM_BOX_TILES_Y):
            for j in range(NUM_BOX_TILES_X):
                tile_x = j + int(cameraoffsetx / MIDDLE_BOX_WIDTH)
                if occupied[i][j] == False and tile_x >= SAFE_ZONE_TILES:
                    available_slots.append((i, j))

        num_enemies = random.randint(ENEMIES_SPAWN_MIN - cur_enemies_count, ENEMIES_SPAWN_CAP - cur_enemies_count)
        for _ in range(num_enemies):
            if len(available_slots) > 0:
                idx = random.randint(0, len(available_slots) - 1)
                i, j = available_slots[idx]
                available_slots.remove(available_slots[idx])

                enemy_type = random.randint(0, 1)
                enemy_x = j * MIDDLE_BOX_WIDTH + int(cameraoffsetx/MIDDLE_BOX_WIDTH) * MIDDLE_BOX_START_X
                enemy_y = i * MIDDLE_BOX_HEIGHT + int(cameraoffsety/MIDDLE_BOX_HEIGHT) * MIDDLE_BOX_START_Y
                if enemy_type == 0:
                    snake_hitbox = snake_idle.get_rect(topleft=(enemy_x, enemy_y))
                    enemies.append([
                                    snake_constants.SNAKE_ATTACK_TYPE,
                                    snake_hitbox,
                                    snake_constants.SNAKE_HEALTH,
                                    snake_constants.SNAKE_MOVEMENT_SPEED,
                                    snake_constants.SNAKE_TYPE,
                                    screen,
                                    snake_idle,
                                    snake_attack_frames,
                                    0,
                                    snake_constants.SNAKE_ATTACK_ANIMATION_COOLDOWN,
                                    snake_constants.SNAKE_MELEE_DAMAGE,
                                    snake_constants.SNAKE_ATTACK_RADIUS,
                                    enemy_x, 
                                    enemy_y,                           
                                    curtime,
                                    curtime
                                ])
                    
                elif enemy_type == 1:
                    skeleton_hitbox = skeleton_idle.get_rect(topleft=(enemy_x, enemy_y))
                    enemies.append([
                        skeleton_constants.SKELETON_ATTACK_TYPE,
                        skeleton_hitbox,
                        skeleton_constants.SKELETON_HEALTH,
                        skeleton_constants.SKELETON_MOVEMENT_SPEED,
                        skeleton_constants.SKELETON_TYPE,
                        screen,
                        skeleton_idle,
                        skeleton_attack_frames,
                        0,
                        skeleton_constants.SKELETON_ATTACK_ANIMATION_COOLDOWN,
                        skeleton_constants.SKELETON_DAMAGE,
                        skeleton_constants.SKELETON_ATTACK_RADIUS,
                        enemy_x, 
                        enemy_y,                           
                        curtime
                    ])

        for enemy in enemies:
            if enemy[0] == "ranged":
                character_health, returned_val = attack_mechanism.update_melee_attack([enemy[4:-1]], character_posx, character_posy, character_hitbox, character_health, curtime, cameraoffsetx, cameraoffsety)
                enemy[4:-1] = returned_val[0]
                if math.hypot(enemy[-3] - character_posx, enemy[-2] - character_posy) > snake_constants.SNAKE_PROJECTILE_OUTER_RADIUS and curtime > enemy[-1] + snake_constants.SNAKE_PROJECTILE_ATTACK_COOLDOWN:
                    enemy[-1] = curtime
                    attacks.append(attack_mechanism.calculate_cur_ranged_attack(enemy[4], 
                                                                                enemy[-4], 
                                                                                enemy[-3], 
                                                                                snake_attack_sprite, 
                                                                                snake_constants.SNAKE_PROJECTILE_SPEED, 
                                                                                snake_constants.SNAKE_PROJECTILE_RADIUS, 
                                                                                0, 
                                                                                0,
                                                                                snake_constants.SNAKE_PROJECTILE_DAMAGE,
                                                                                character_posx,
                                                                                character_posy
                                                                            ))
            else:
                character_health, returned_val = attack_mechanism.update_melee_attack([enemy[4:]], character_posx, character_posy, character_hitbox, character_health, curtime, cameraoffsetx, cameraoffsety)
                enemy[4:] = returned_val[0]

                
    screen.blit(cursor, (mouse_pos[0] - CURSOR_WIDTH//2, mouse_pos[1] - CURSOR_HEIGHT//2))
    clock.tick(60)
    pygame.display.update()

pygame.quit()