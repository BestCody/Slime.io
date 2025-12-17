import pygame
import time
import random
import charactermovement
import attackmechanism
from Characters.Slime import slimeconstants
from Characters.Skeletons import skeletonconstants
pygame.init()

#Camera settings
camerawidth = 1000
cameraheight = 680
cameraoffsetx = -100
cameraoffsety = -50

#Screen stuff
screen_size = [camerawidth, cameraheight]
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
screen.fill("black")

character = pygame.image.load("Characters/Slime/slimestandingstill.png").convert_alpha()
charactermovingright = pygame.image.load("Characters/Slime/slimemovingright.png").convert_alpha()
charactermovingleft = pygame.image.load("Characters/Slime/slimemovingleft.png").convert_alpha()
enemy = pygame.image.load("Characters/Skeletons/skeleton.png").convert_alpha()
attack = pygame.image.load("Characters/Slime/slimeattack.png").convert_alpha()
map = pygame.image.load("Map/map.png").convert()

map = pygame.transform.scale(map, (4130, 580))
characterstill = pygame.transform.scale(character, (slimeconstants.characterwidth, slimeconstants.characterheight))
charactermovingright = pygame.transform.scale(charactermovingright, (slimeconstants.characterwidth, slimeconstants.characterheight))
charactermovingleft = pygame.transform.scale(charactermovingleft, (slimeconstants.characterwidth, slimeconstants.characterheight))
characterstretch = pygame.transform.scale(character, (slimeconstants.characterstretchwidth, slimeconstants.characterstretchheight))
attack = pygame.transform.scale(attack, (slimeconstants.attackwidth, slimeconstants.attackheight))
enemy = pygame.transform.scale(enemy, (skeletonconstants.skeletonwidth, skeletonconstants.skeletonheight))

characterstill_hitbox = character.get_rect(center = (screen_size[0]//2, screen_size[1]//2))
charactermovingleft_hitbox = charactermovingleft.get_rect(center = (screen_size[0]//2, screen_size[1]//2))
charactermovingright_hitbox = charactermovingright.get_rect(center = (screen_size[0]//2, screen_size[1]//2))
characterstretch_hitbox = characterstretch.get_rect(center = (screen_size[0]//2, screen_size[1]//2))
enemy_hitbox = enemy.get_rect(topleft = (0,0))

player = character
character_hitbox = characterstill_hitbox
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
#Fix hitbox
#Make the map infinitely generate as the player moves right

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    #Update player movement
    character, character_hitbox, cameraoffsetx, cameraoffsety, prev_animation_time = charactermovement.updatemovement(
        cameraoffsetx, 
        cameraoffsety, 
        character, 
        character_hitbox,
        characterstill,
        characterstill_hitbox,
        charactermovingright, 
        charactermovingright_hitbox,
        charactermovingleft, 
        charactermovingleft_hitbox,
        characterstretch, 
        characterstretch_hitbox, 
        prev_animation_time,
        slimeconstants.animation_speed
    )

    #Draw character and map
    screen.blit(map, (-cameraoffsetx, -cameraoffsety))
    screen.blit(character, (character_hitbox.x, character_hitbox.y))

    #Create new attacks
    if prev_attack_time < time.time() - slimeconstants.attack_cooldown:
        prev_attack_time = time.time()
        attacks.append(attackmechanism.calculate_cur_attack(character_hitbox.centerx, character_hitbox.centery, attack, 
            slimeconstants.attack_speed))
        
    #Spawn new skeletons
    if prev_skeleton_spawn_time < time.time() - skeletonconstants.skeletonspawncd:
        prev_skeleton_spawn_time = time.time()
        newskeletonhitbox = enemy.get_rect(topleft = (0, 0))
        enemies.append([skeletonconstants.skeletonhp, newskeletonhitbox])

    #Update enemies
    alivemonsters = []
    for monster in enemies:
        if monster[0] > 0:
            alivemonsters.append(monster)
            current_monster_hitbox = monster[1]
            monster_x = current_monster_hitbox.x - cameraoffsetx
            monster_y = current_monster_hitbox.y - cameraoffsety
            screen.blit(enemy, (monster_x, monster_y))
    enemies = alivemonsters

    #Update attacks
    attacks = attackmechanism.update_attacks(
        attacks, 
        screen,
        slimeconstants.attack_radius, 
        enemies
    )  

    pygame.draw.rect(screen, (0, 255, 0), character_hitbox, 2)

    clock.tick(60)
    pygame.display.update()

pygame.quit()