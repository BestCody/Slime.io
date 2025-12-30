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
    return [type, rotated_attack, objposx, objposy, normalized_x*attackspeed, normalized_y*attackspeed, objposx, objposy, damage, attackradius]

def update_ranged_attacks(attacks, screen, cameraoffsetx, cameraoffsety, character_health, character_posx, character_posy, character_hitbox, enemies):
    updated_attacks = []
    for cur_attack in attacks:
        type, attack_img, curx, cury, normalized_x, normalized_y, origx, origy, damage, attack_radius = cur_attack

        attack_hitbox = attack_img.get_rect(topleft=(curx, cury))
        screen.blit(attack_img, (curx - cameraoffsetx, cury - cameraoffsety))
        #pygame.draw.rect(screen, (0, 255, 0), attack_hitbox, 2)
        
        hit = False
        if type == "enemy" or type == "obstacle":
                new_player_hitbox = character_hitbox.copy()
                new_player_hitbox.center = (character_posx, character_posy)
                if attack_hitbox.colliderect(new_player_hitbox):
                    character_health -= damage
                    hit = True
        elif type == "player":
            for enemy in enemies:
                if attack_hitbox.colliderect(enemy[1]):
                    enemy[2] -= damage
                    hit = True

        curx += normalized_x
        cury += normalized_y

        if math.hypot(origx - curx, origy - cury) < attack_radius and hit == False:
            updated_attacks.append([type, attack_img, curx, cury, normalized_x, normalized_y, origx, origy, damage, attack_radius])

    return character_health, updated_attacks

def update_melee_attack(attacks, character_x, character_y, character_hitbox, character_health, curtime, cameraoffsetx, cameraoffsety):
    updated_attacks = []
    for attack in attacks:
        type, screen, idleanims, frames, cur_frame, animation_cooldown, damage, attack_radius, attack_x, attack_y, prevtime = attack
        if type == "obstacle":
            if math.hypot(attack_x - character_x, attack_y - character_y) <= attack_radius:
                if curtime - prevtime >= animation_cooldown[cur_frame]:
                    cur_frame += 1
                    prevtime = curtime
                if cur_frame < len(frames):
                    attack_img = frames[cur_frame]
                    attack_hitbox = attack_img.get_rect(topleft=(attack_x, attack_y))
                    screen.blit(attack_img, (attack_x - cameraoffsetx, attack_y - cameraoffsety))
                    new_player_hitbox = character_hitbox.copy()
                    new_player_hitbox.center = (character_x, character_y)
                    #pygame.draw.rect(screen, (0, 255, 0), attack_hitbox, 2)

                    if attack_hitbox.colliderect(new_player_hitbox):
                        character_health -= damage
                        updated_attacks.append([type, screen, idleanims, frames, cur_frame, animation_cooldown, 0, attack_radius, attack_x, attack_y, prevtime])
                    else:
                        updated_attacks.append([type, screen, idleanims, frames, cur_frame, animation_cooldown, damage, attack_radius, attack_x, attack_y, prevtime])
            else:
                screen.blit(idleanims, (attack_x - cameraoffsetx, attack_y - cameraoffsety))
                updated_attacks.append([type, screen, idleanims, frames, cur_frame, animation_cooldown, damage, attack_radius, attack_x, attack_y, prevtime])
                
        elif type == "enemy":
            flip = False
            if attack_x < character_x:
                flip = True
            
            idle_hitbox = idleanims.get_rect(topleft=(attack_x, attack_y))

            if math.hypot(attack_x - character_x, attack_y - character_y) <= attack_radius:
                if curtime - prevtime >= animation_cooldown[cur_frame]:
                    cur_frame += 1
                    prevtime = curtime

                deal_damage = False
                if cur_frame >= len(frames):
                    cur_frame = 0
                    deal_damage = True

                attack_img = frames[cur_frame]
                if flip:
                    attack_img = pygame.transform.flip(attack_img, True, False)

                attack_hitbox = attack_img.get_rect(midbottom=idle_hitbox.midbottom)
                screen.blit(attack_img, (attack_x - cameraoffsetx, attack_y - cameraoffsety))
                upd_player_hitbox = character_hitbox.copy()
                upd_player_hitbox.center = (character_x, character_y)

                atk_rect = attack_hitbox.copy()
                atk_rect.x -= (cameraoffsetx)
                atk_rect.y -= (cameraoffsety)
                pygame.draw.rect(screen, (255, 0, 0), atk_rect, 2)

                if attack_hitbox.colliderect(upd_player_hitbox) and deal_damage:
                    character_health -= damage
                
            else:
                idle = idleanims
                if flip:
                    idle= pygame.transform.flip(idleanims, True, False)
                screen.blit(idle, (attack_x - cameraoffsetx, attack_y - cameraoffsety))

            updated_attacks.append([type, screen, idleanims, frames, cur_frame, animation_cooldown, damage, attack_radius, attack_x, attack_y, prevtime])

    return character_health, updated_attacks