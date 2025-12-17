import pygame
import math

def calculate_cur_attack(playerposx, playerposy, attack_img, attackspeed):
    mousepos = pygame.mouse.get_pos()
    attackx = mousepos[0] - playerposx
    attacky = mousepos[1] - playerposy

    angle = 180 / math.pi * math.atan2(attacky, attackx)
    rotated_attack = pygame.transform.rotate(attack_img, int(-angle))
    normalized_x = math.cos(math.radians(angle))
    normalized_y = math.sin(math.radians(angle))
    
    return [rotated_attack, playerposx, playerposy, normalized_x*attackspeed, normalized_y*attackspeed, playerposx, playerposy]

def update_attacks(attacks, screen, attackradius, enemies):
    updated_attacks = []
    for cur_attack in attacks:
        attack_img, curx, cury, normalized_x, normalized_y, origx, origy = cur_attack
        curx += normalized_x
        cury += normalized_y

        attack_hitbox = attack_img.get_rect(topleft=(curx, cury))
        screen.blit(attack_img, (curx, cury))
        pygame.draw.rect(screen, (0, 255, 0), attack_hitbox, 2)
        
        hit = False
        for enemy in enemies:
            if attack_hitbox.colliderect(enemy[1]):
                enemy[0] -= 50
                hit = True

        if math.hypot(origx - curx, origy - cury) < attackradius and hit == False:
            updated_attacks.append([attack_img, curx, cury, normalized_x, normalized_y, origx, origy])

    return updated_attacks