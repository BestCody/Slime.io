import pygame
import math

def calculate_cur_attack(playerposx, playerposy, attack_img, attackspeed, cameraoffsetx, cameraoffsety):
    mousepos = pygame.mouse.get_pos()
    anglex = mousepos[0] - playerposx + cameraoffsetx
    angley = mousepos[1] - playerposy + cameraoffsety
    angle = 180 / math.pi * math.atan2(angley, anglex)
    rotated_attack = pygame.transform.rotate(attack_img, int(-angle))
    normalized_x = math.cos(math.radians(angle))
    normalized_y = math.sin(math.radians(angle))

    return [rotated_attack, playerposx, playerposy, normalized_x*attackspeed, normalized_y*attackspeed, playerposx, playerposy]

def update_attacks(attacks, screen, attackradius, enemies, cameraoffsetx, cameraoffsety):
    updated_attacks = []
    for cur_attack in attacks:
        attack_img, curx, cury, normalized_x, normalized_y, origx, origy = cur_attack

        attack_hitbox = attack_img.get_rect(topleft=(curx, cury))
        screen.blit(attack_img, (curx - cameraoffsetx, cury - cameraoffsety))
        pygame.draw.rect(screen, (0, 255, 0), attack_hitbox, 2)
        
        hit = False
        for enemy in enemies:
            if attack_hitbox.colliderect(enemy[1]):
                enemy[0] -= 50
                hit = True

        curx += normalized_x
        cury += normalized_y

        if math.hypot(origx - curx, origy - cury) < attackradius and hit == False:
            updated_attacks.append([attack_img, curx, cury, normalized_x, normalized_y, origx, origy])

    return updated_attacks