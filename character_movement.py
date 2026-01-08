import pygame

def updatemovement(character, keys, curtime, dt):
    #Update movements
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        character["camera_offsetx"] += (character["speed"] * dt)
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        character["camera_offsetx"] -= (character["speed"] * dt)
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        character["camera_offsety"] += (character["speed"] * dt)
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        character["camera_offsety"] -= (character["speed"] * dt)

    #Update animation
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        character["sprite"] = character["moving_right_sprite"]
        character["hitbox"] = character["moving_right_hitbox"]
        character["cur_idle_frame"] = 0
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        character["sprite"] = character["moving_left_sprite"]
        character["hitbox"] = character["moving_left_hitbox"]
        character["cur_idle_frame"] = 0
    else:
        if curtime - character["prev_animation_time"] > character["animation_cd"]:
            character["prev_animation_time"] = curtime
            character["cur_idle_frame"] %= len(character["idle_anims"])
            character["sprite"] = character["idle_anims"][character["cur_idle_frame"]]
            character["hitbox"] = character["idle_hitbox"][character["cur_idle_frame"]]
            character["cur_idle_frame"] += 1

    return character