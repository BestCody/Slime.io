import pygame
import math

def calculate_cur_attack(playerposx, playerposy, attack, attackspeed, attackradius,
    characterheight, characterwidth, attackheight, attackwidth):
    mousepos = pygame.mouse.get_pos()
    startx = playerposx + (characterwidth - attackwidth) / 2
    starty = playerposy + (characterheight - attackheight) / 2
    attackx = mousepos[0] - startx
    attacky = mousepos[1] - starty
    angle = 180 / math.pi * math.atan2(attacky, attackx)
    rotated_attack = pygame.transform.rotate(attack, int(angle))
    normalized_x = math.cos(math.radians(angle))
    normalized_y = math.sin(math.radians(angle))
    return [rotated_attack, startx, starty, normalized_x*attackspeed, normalized_y*attackspeed, 
            startx, starty]

def update_attacks(attacks, attack, screen, attack_cooldown, attackradius, enemies):
    updated_attacks = []
    for cur_attack in attacks:
        rotated_attack, curx, cury, normalized_x, normalized_y, origx, origy = cur_attack
        curx += normalized_x
        cury += normalized_y
        screen.blit(rotated_attack, (curx, cury))
        hit = False

        for enemy in enemies:
            enemyx, enemyy= enemy[0], enemy[1]
            if (enemyx < curx < enemyx + 30) and (enemyy < cury < enemyy + 30):
                enemy[2] -= 50
                hit = True

        if math.hypot(origx - curx, origy - cury) < attackradius and hit == False:
            updated_attacks.append([rotated_attack, curx, cury, normalized_x, normalized_y, origx, origy])

    return updated_attacks