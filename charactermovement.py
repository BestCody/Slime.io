import pygame
import time

def updatemovement(playerposx, playerposy, character, charactermovingright, charactermovingleft,
                   characterstretch, characterwidthreduction, characterheightincrease, 
                   screen, prevtime, movementtype, animationtype, animation_speed):
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        playerposx += 2 
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        playerposx -= 2
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        playerposy += 2
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        playerposy -= 2

    if time.time() - prevtime > animation_speed:
        prevtime = time.time()
        animationtype = (animationtype + 1) % 2

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        #if movementtype != "right":
        #    movementtype = "right"
        #    animationtype = 0
        #    prevtime = time.time()

        #if animationtype == 0:
        #    screen.blit(charactermovingright, (playerposx, playerposy))
        #else:
        screen.blit(charactermovingright, (playerposx, playerposy))

    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        #if movementtype != "left":
        #    movementtype = "left"
        #    animationtype = 0
        #    prevtime = time.time()
            
        #if animationtype == 0:
        #    screen.blit(charactermovingleft, (playerposx, playerposy))
        #else:
        screen.blit(charactermovingleft, (playerposx, playerposy))

    else:
        if movementtype != "still":
            movementtype = "still"
            animationtype = 0
            prevtime = time.time()
            
        if animationtype == 0:
            screen.blit(character, (playerposx, playerposy))
        else:
            screen.blit(characterstretch, (playerposx, playerposy-characterheightincrease))

    return playerposx, playerposy, prevtime, movementtype, animationtype