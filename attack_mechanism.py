import pygame
import math

def calculate_cur_ranged_attack(type, objposx, objposy, attack_img, attackspeed, attackradius, cameraoffsetx, cameraoffsety, damage, character_posx, character_posy):
    mousepos = pygame.mouse.get_pos()
    if type == "player":
        anglex = mousepos[0] - objposx + cameraoffsetx
        angley = mousepos[1] - objposy + cameraoffsety
    else:
        anglex = character_posx - objposx + cameraoffsetx
        angley = character_posy - objposy + cameraoffsety
    angle = 180 / math.pi * math.atan2(angley, anglex)
    rotated_attack = pygame.transform.rotate(attack_img, -angle)
    normalized_x = math.cos(math.radians(angle))
    normalized_y = math.sin(math.radians(angle))
    return {"attack_type": type, 
            "sprite": rotated_attack, 
            "x": objposx, 
            "y": objposy, 
            "speed_x": normalized_x*attackspeed, 
            "speed_y": normalized_y*attackspeed, 
            "orig_x": objposx, 
            "orig_y": objposy, 
            "damage": damage, 
            "attack_radius": attackradius
        }

def update_ranged_attacks(attacks, screen, cameraoffsetx, cameraoffsety, character_health, character_posx, character_posy, character_hitbox, enemies):
    updated_attacks = []
    for attack in attacks:
        attack_hitbox = attack["sprite"].get_rect(topleft=(attack["x"], attack["y"]))
        screen.blit(attack["sprite"], (attack["x"] - cameraoffsetx, attack["y"] - cameraoffsety))
        #pygame.draw.rect(screen, (0, 255, 0), attack_hitbox, 2)
        
        hit = False
        if attack["attack_type"] == "enemy" or attack["attack_type"] == "obstacle":
                new_player_hitbox = character_hitbox.copy()
                new_player_hitbox.center = (character_posx, character_posy)
                if attack_hitbox.colliderect(new_player_hitbox):
                    character_health -= attack["damage"]
                    hit = True
        elif attack["attack_type"] == "player":
            for enemy in enemies:
                if attack_hitbox.colliderect(enemy["hitbox"]):
                    enemy["health"] -= attack["damage"]
                    hit = True

        attack["x"] += attack["speed_x"]
        attack["y"] += attack["speed_y"]

        if math.hypot(attack["orig_x"] - attack["x"], attack["orig_y"] - attack["y"]) < attack["attack_radius"] and hit == False:
            updated_attacks.append(attack)

    return character_health, updated_attacks

def update_melee_attack(attacks, character_x, character_y, character_hitbox, character_health, curtime, cameraoffsetx, cameraoffsety):
    updated_attacks = []
    for attack in attacks:
        if attack["attack_type"] == "obstacle":
            if math.hypot(attack["x"] - character_x, attack["y"] - character_y) <= attack["attack_radius"]:
                if curtime - attack["prev_animation_upd"] >= attack["animation_cd"][attack["attack_animation_frame"]]:
                    attack["attack_animation_frame"] += 1
                    attack["prev_animation_upd"] = curtime
                if attack["attack_animation_frame"] < len(attack["attack_frames"]):
                    attack_img = attack["attack_frames"][attack["attack_animation_frame"]]
                    attack_hitbox = attack_img.get_rect(topleft=(attack["x"], attack["y"]))
                    attack["screen"].blit(attack_img, (attack["x"] - cameraoffsetx, attack["y"] - cameraoffsety))
                    new_player_hitbox = character_hitbox.copy()
                    new_player_hitbox.center = (character_x, character_y)
                    #pygame.draw.rect(screen, (0, 255, 0), attack_hitbox, 2)

                    if attack_hitbox.colliderect(new_player_hitbox):
                        character_health -= attack["melee_damage"]
                        attack["melee_damage"] = 0

                    updated_attacks.append(attack)
            else:
                attack["screen"].blit(attack["idle_frame"], (attack["x"] - cameraoffsetx, attack["y"] - cameraoffsety))
                updated_attacks.append(attack)
                
        elif attack["attack_type"] == "enemy":
            flip = False
            if attack["x"] < character_x:
                flip = True
            
            idle_hitbox = attack["idle_frame"].get_rect(topleft=(attack["x"], attack["y"]))

            if math.hypot(attack["x"] - character_x, attack["y"] - character_y) <= attack["attack_radius"]:
                if curtime - attack["prev_animation_upd"] >= attack["animation_cd"][attack["attack_animation_frame"]]:
                    attack["attack_animation_frame"] += 1
                    attack["prev_animation_upd"] = curtime

                deal_damage = False
                if attack["attack_animation_frame"] >= len(attack["attack_frames"]):
                    attack["attack_animation_frame"] = 0
                    deal_damage = True

                attack_img = attack["attack_frames"][attack["attack_animation_frame"]]
                if flip:
                    attack_img = pygame.transform.flip(attack_img, True, False)

                attack_hitbox = attack_img.get_rect(midbottom=idle_hitbox.midbottom)
                attack["screen"].blit(attack_img, (attack_hitbox.x - cameraoffsetx, attack_hitbox.y - cameraoffsety))
                upd_player_hitbox = character_hitbox.copy()
                upd_player_hitbox.center = (character_x, character_y)

                if attack_hitbox.colliderect(upd_player_hitbox) and deal_damage:
                    character_health -= attack["melee_damage"]
                
            else:
                idle = attack["idle_frame"]
                if flip:
                    idle= pygame.transform.flip(attack["idle_frame"], True, False)
                attack["screen"].blit(idle, (attack["x"] - cameraoffsetx, attack["y"] - cameraoffsety))

            updated_attacks.append(attack)

    return character_health, updated_attacks



#atk_rect = attack_hitbox.copy()
#atk_rect.x -= (cameraoffsetx)
#atk_rect.y -= (cameraoffsety)
#pygame.draw.rect(screen, (255, 0, 0), atk_rect, 2)