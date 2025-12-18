import pygame
import charactermovement
import attackmechanism
from Characters.Slime import slimeconstants
from Characters.Skeletons import skeletonconstants
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

characterstill = pygame.image.load("Characters/Slime/slimestandingstill.png").convert_alpha()
charactermovingright = pygame.image.load("Characters/Slime/slimemovingright.png").convert_alpha()
charactermovingleft = pygame.image.load("Characters/Slime/slimemovingleft.png").convert_alpha()
enemy = pygame.image.load("Characters/Skeletons/skeleton.png").convert_alpha()
attack = pygame.image.load("Characters/Slime/slimeattack.png").convert_alpha()
map = pygame.image.load("Map/map.png").convert()

map = pygame.transform.scale(map, (4130, 580))
characterstill = pygame.transform.scale(characterstill, (slimeconstants.characterwidth, slimeconstants.characterheight))
charactermovingright = pygame.transform.scale(charactermovingright, (slimeconstants.characterwidth, slimeconstants.characterheight))
charactermovingleft = pygame.transform.scale(charactermovingleft, (slimeconstants.characterwidth, slimeconstants.characterheight))
characterstretch = pygame.transform.scale(characterstill, (slimeconstants.characterstretchwidth, slimeconstants.characterstretchheight))
attack = pygame.transform.scale(attack, (slimeconstants.attackwidth, slimeconstants.attackheight))
enemy = pygame.transform.scale(enemy, (skeletonconstants.skeletonwidth, skeletonconstants.skeletonheight))

characterstill_hitbox = characterstill.get_rect(center = (screen_size[0]//2, screen_size[1]//2))
charactermovingleft_hitbox = charactermovingleft.get_rect(midbottom = characterstill_hitbox.midbottom)
charactermovingright_hitbox = charactermovingright.get_rect(midbottom = characterstill_hitbox.midbottom)
characterstretch_hitbox = characterstretch.get_rect(midbottom = characterstill_hitbox.midbottom)
enemy_hitbox = enemy.get_rect(topleft = (0,0))

character = characterstill
character_hitbox = characterstill_hitbox
character_posx = 0
character_posy = 0
attacks = []
enemies = []
prev_attack_time = 0
prev_skeleton_spawn_time = 0
prev_animation_time = 0
movementtype = "still"
animationtype = 0
running = True

screen.fill("black")

#Stuff to note:
#Origin is in top left corner
#Y axis is inverted in Pygame (increasing y goes down)

#Immediate Stuff to do:
#Make the map infinitely generate as the player moves right

#Long term stuff:
#Enemy pathfinding (Djirkstra's algo or A* star)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    curtime = pygame.time.get_ticks()

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
        curtime,
        slimeconstants.animation_speed
    )
    character_posx = character_hitbox.centerx + cameraoffsetx
    character_posy = character_hitbox.centery + cameraoffsety
 
    #Draw character and map
    screen.blit(map, (-cameraoffsetx, -cameraoffsety))
    screen.blit(character, character_hitbox)

    #Create new attacks
    if prev_attack_time < curtime - slimeconstants.attack_cooldown:
        prev_attack_time = curtime
        attacks.append(attackmechanism.calculate_cur_attack(character_posx - slimeconstants.attackwidth//2, character_posy - slimeconstants.attackheight//2, attack, 
            slimeconstants.attack_speed, cameraoffsetx, cameraoffsety))
        
    #Spawn new skeletons
    if prev_skeleton_spawn_time < curtime - skeletonconstants.skeletonspawncd:
        prev_skeleton_spawn_time = curtime
        newskeletonhitbox = enemy.get_rect(topleft = (0, 0))
        enemies.append([skeletonconstants.skeletonhp, newskeletonhitbox])

    #Update enemies
    alivemonsters = []
    for monster in enemies:
        if monster[0] > 0:
            alivemonsters.append(monster)
            screen.blit(enemy, (-cameraoffsetx, -cameraoffsety))
    enemies = alivemonsters

    #Update attacks
    attacks = attackmechanism.update_attacks(
        attacks, 
        screen,
        slimeconstants.attack_radius, 
        enemies,
        cameraoffsetx,
        cameraoffsety
    )  

    copy_rect = character_hitbox.copy()
    copy_rect.x = character_posx - character_hitbox.width//2
    copy_rect.y = character_posy - character_hitbox.height//2
    pygame.draw.rect(screen, (0, 255, 0), copy_rect, 2)

    clock.tick(60)
    pygame.display.update()

pygame.quit()