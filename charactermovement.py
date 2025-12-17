import pygame
import time

def updatemovement(cameraoffsetx, 
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
                   prevtime, 
                   animation_speed):
    
    keys = pygame.key.get_pressed()
    characterchange = False

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        cameraoffsetx += 2 
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        cameraoffsetx -= 2
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        cameraoffsety += 2
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        cameraoffsety -= 2

    if time.time() - prevtime > animation_speed:
        prevtime = time.time()
        characterchange = True

    if characterchange:
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            character = charactermovingright
            character_hitbox = charactermovingright_hitbox

        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            character = charactermovingleft
            character_hitbox = charactermovingleft_hitbox

        else:
            if character == characterstill:
                character = characterstretch
                character_hitbox = characterstretch_hitbox
            else:
                character = characterstill
                character_hitbox = characterstill_hitbox    

    return character, character_hitbox, cameraoffsetx, cameraoffsety, prevtime