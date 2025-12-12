import pygame
import time
import random
import charactermovement
import attackmechanism
from Characters.Slime import slimeconstants
from Characters.Skeletons import skeletonconstants
pygame.init()

desktop_size = pygame.display.get_desktop_sizes()
screen = pygame.display.set_mode()
clock = pygame.time.Clock()
screen.fill("white")

character = pygame.image.load("Characters/Slime/slimestandingstill.png").convert_alpha()
charactermovingright = pygame.image.load("Characters/Slime/slimemovingright.png").convert_alpha()
charactermovingleft = pygame.image.load("Characters/Slime/slimemovingleft.png").convert_alpha()
enemy = pygame.image.load("Characters/Skeletons/skeleton.png").convert_alpha()
attack = pygame.image.load("Characters/Slime/slimeattack.png").convert_alpha()

character = pygame.transform.scale(character, (slimeconstants.characterwidth, slimeconstants.characterheight))
charactermovingright = pygame.transform.scale(charactermovingright, (slimeconstants.characterwidth, slimeconstants.characterheight))
charactermovingleft = pygame.transform.scale(charactermovingleft, (slimeconstants.characterwidth, slimeconstants.characterheight))
characterstretch = pygame.transform.scale(character, (slimeconstants.characterwidth - slimeconstants.characterwidthreduction, slimeconstants.characterheight + slimeconstants.characterheightincrease))
attack = pygame.transform.scale(attack, (slimeconstants.attackwidth, slimeconstants.attackheight))
enemy = pygame.transform.scale(enemy, (skeletonconstants.skeletonwidth, skeletonconstants.skeletonheight))

character_hitbox = character.get_rect(topleft = (0,0))
charactermovingleft_hitbox = charactermovingleft.get_rect(topleft = (0,0))
charactermovingright_hitbox = charactermovingright.get_rect(topleft = (0,0))
characterstretch_hitbox = characterstretch.get_rect(topleft = (0,0))
attack_hitbox = attack.get_rect(topleft = (0,0))
enemy_hitbox = enemy.get_rect(topleft = (0,0))

attacks = []
enemies = []
prev_attack_time = 0
prev_skeleton_spawn_time = 0
prev_animation_time = 0
movementtype = "still"
animationtype = 0
running = True

#Stuff to note:
#Origin is in top left corner
#Y axis is inverted in Pygame (increasing y goes down)

#Immediate Stuff to do:
#Softcode the enemies more
#Create the map
#Create the animation of the slime jumping to the right or left for when the slime walks

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    #Update player movement
    character_hitbox.x, character_hitbox.y, prev_animation_time, movementtype, animationtype = charactermovement.updatemovement(character_hitbox.x, 
    character_hitbox.y, character, charactermovingright, charactermovingleft, characterstretch, slimeconstants.characterwidthreduction,
    slimeconstants.characterheightincrease, screen, prev_animation_time, movementtype, animationtype, slimeconstants.animation_speed)

    #Create new attacks
    if prev_attack_time < time.time() - slimeconstants.attack_cooldown:
        prev_attack_time = time.time()
        attacks.append(attackmechanism.calculate_cur_attack(character_hitbox.x, character_hitbox.y, attack, 
            slimeconstants.attack_speed, slimeconstants.characterheight, slimeconstants.characterwidth,
            slimeconstants.attackheight, slimeconstants.attackwidth))
        
    #Spawn new skeletons
    if prev_skeleton_spawn_time < time.time() - skeletonconstants.skeletonspawncd:
        prev_skeleton_spawn_time = time.time()
        enemies.append([skeletonconstants.skeletonhp, enemy_hitbox])

    #Update enemies
    alivemonsters = []
    for monster in enemies:
        if monster[0] > 0:
            alivemonsters.append(monster)
            screen.blit(enemy, enemy_hitbox)
    enemies = alivemonsters
        
    attacks = attackmechanism.update_attacks(attacks, screen, 
    slimeconstants.attack_radius, enemies)  

    clock.tick(60)
    pygame.display.update()

pygame.quit()