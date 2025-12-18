import pygame

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
                   curtime,
                   animation_speed):
    
    keys = pygame.key.get_pressed()

    #Update movements
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        cameraoffsetx += 2 
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        cameraoffsetx -= 2
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        cameraoffsety += 2
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        cameraoffsety -= 2

    #Update animation
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        character = charactermovingright
        character_hitbox = charactermovingright_hitbox
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        character = charactermovingleft
        character_hitbox = charactermovingleft_hitbox
    else:
        if curtime - prevtime > animation_speed:
            prevtime = curtime
            if character == characterstill:
                character = characterstretch
                character_hitbox = characterstretch_hitbox
            else:
                character = characterstill
                character_hitbox = characterstill_hitbox    

    return character, character_hitbox, cameraoffsetx, cameraoffsety, prevtime