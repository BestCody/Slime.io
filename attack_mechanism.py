import pygame
import math

def calculate_cur_ranged_attack(object, cameraoffsetx, cameraoffsety, player_posx, player_posy, mousepos):
    if object["attack_type"] == "player":
        anglex = mousepos[0] - object["x"] + cameraoffsetx
        angley = mousepos[1] - object["y"] + cameraoffsety
    else:
        anglex = player_posx - object["x"]
        angley = player_posy - object["y"]
    angle = 180 / math.pi * math.atan2(angley, anglex)
    rotated_attack = pygame.transform.rotate(object["projectile_attack"], -angle)
    normalized_x = math.cos(math.radians(angle))
    normalized_y = math.sin(math.radians(angle))
    return {
            "attack_type": object["attack_type"], 
            "projectile_sprite": rotated_attack, 
            "x": object["x"] - object["projectile_attack"].width//2,
            "y": object["y"] - object["projectile_attack"].height//2,
            "projectile_speed_x": normalized_x*object["projectile_attack_speed"], 
            "projectile_speed_y": normalized_y*object["projectile_attack_speed"], 
            "projectile_orig_x": object["x"], 
            "projectile_orig_y": object["y"], 
            "projectile_damage": object["projectile_damage"], 
            "projectile_attack_radius": object["projectile_attack_radius"]
        }

def update_ranged_attacks(attacks, screen, cameraoffsetx, cameraoffsety, character_health, character_posx, character_posy, character_hitbox, enemies, dt):
    updated_attacks = []
    for attack in attacks:
        attack_hitbox = attack["projectile_sprite"].get_rect(topleft=(attack["x"], attack["y"]))
        screen.blit(attack["projectile_sprite"], (attack["x"] - cameraoffsetx, attack["y"] - cameraoffsety))
        #pygame.draw.rect(screen, (0, 255, 0), attack_hitbox, 2)
        
        hit = False
        if attack["attack_type"] == "enemy" or attack["attack_type"] == "obstacle":
                new_player_hitbox = character_hitbox.copy()
                new_player_hitbox.center = (character_posx, character_posy)
                if attack_hitbox.colliderect(new_player_hitbox):
                    character_health -= attack["projectile_damage"]
                    hit = True
        elif attack["attack_type"] == "player":
            for enemy in enemies:
                if attack_hitbox.colliderect(enemy["hitbox"]):
                    enemy["health"] -= attack["projectile_damage"]
                    hit = True

        attack["x"] += (attack["projectile_speed_x"] * dt)
        attack["y"] += (attack["projectile_speed_y"] * dt)

        if math.hypot(attack["projectile_orig_x"] - attack["x"], attack["projectile_orig_y"] - attack["y"]) < attack["projectile_attack_radius"] and hit == False:
            updated_attacks.append(attack)

    return character_health, updated_attacks

def update_melee_attack(attacks, character_x, character_y, character_hitbox, character_health, curtime, cameraoffsetx, cameraoffsety, screen):
    updated_attacks = []
    for attack in attacks:
        if attack["attack_type"] == "obstacle":
            if math.hypot(attack["x"] - character_x, attack["y"] - character_y) <= attack["melee_attack_radius"]:
                if curtime - attack["melee_prev_animation_upd"] >= attack["melee_animation_cd"][attack["melee_attack_animation_frame"]]:
                    attack["melee_attack_animation_frame"] += 1
                    attack["melee_prev_animation_upd"] = curtime
                if attack["melee_attack_animation_frame"] < len(attack["melee_attack_frames"]):
                    attack_img = attack["melee_attack_frames"][attack["melee_attack_animation_frame"]]
                    attack_hitbox = attack_img.get_rect(topleft=(attack["x"], attack["y"]))
                    screen.blit(attack_img, (attack["x"] - cameraoffsetx, attack["y"] - cameraoffsety))
                    new_player_hitbox = character_hitbox.copy()
                    new_player_hitbox.center = (character_x, character_y)
                    #pygame.draw.rect(screen, (0, 255, 0), attack_hitbox, 2)

                    if attack_hitbox.colliderect(new_player_hitbox):
                        character_health -= attack["melee_damage"]
                        attack["melee_damage"] = 0

                    updated_attacks.append(attack)
            else:
                screen.blit(attack["idle_frame"], (attack["x"] - cameraoffsetx, attack["y"] - cameraoffsety))
                updated_attacks.append(attack)
                
        elif attack["attack_type"] == "enemy":
            flip = False
            if attack["x"] < character_x:
                flip = True
            
            idle_hitbox = attack["idle_frame"].get_rect(topleft=(attack["x"], attack["y"]))

            if math.hypot(attack["x"] - character_x, attack["y"] - character_y) <= attack["melee_attack_radius"]:
                if curtime - attack["melee_prev_animation_upd"] >= attack["melee_animation_cd"][attack["melee_attack_animation_frame"]]:
                    attack["melee_attack_animation_frame"] += 1
                    attack["melee_prev_animation_upd"] = curtime

                deal_damage = False
                if attack["melee_attack_animation_frame"] >= len(attack["melee_attack_frames"]):
                    attack["melee_attack_animation_frame"] = 0
                    deal_damage = True

                attack_img = attack["melee_attack_frames"][attack["melee_attack_animation_frame"]]
                if flip:
                    attack_img = pygame.transform.flip(attack_img, True, False)

                attack_hitbox = attack_img.get_rect(midbottom=idle_hitbox.midbottom)
                screen.blit(attack_img, (attack_hitbox.x - cameraoffsetx, attack_hitbox.y - cameraoffsety))
                upd_player_hitbox = character_hitbox.copy()
                upd_player_hitbox.center = (character_x, character_y)

                if attack_hitbox.colliderect(upd_player_hitbox) and deal_damage:
                    character_health -= attack["melee_damage"]
                
            else:
                idle = attack["idle_frame"]
                if flip:
                    idle= pygame.transform.flip(attack["idle_frame"], True, False)
                screen.blit(idle, (attack["x"] - cameraoffsetx, attack["y"] - cameraoffsety))

            updated_attacks.append(attack)

    return character_health, updated_attacks



#atk_rect = attack_hitbox.copy()
#atk_rect.x -= (cameraoffsetx)
#atk_rect.y -= (cameraoffsety)
#pygame.draw.rect(screen, (255, 0, 0), atk_rect, 2)