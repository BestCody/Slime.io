import pygame

def updatemovement(character, keys, curtime, dt):
    """
    Updates the current character position and sprite

    Arg:
        character (dict): The character being updated

        keys (pygame.key.ScancodeWrapper): 
        The state of all keyboard keys from pygame.keys.get_pressed()

        curtime (int): The current time in the game in milliseconds
        dt (float): The time passed since the last frame in seconds
    
    Returns:
        None: Modifies the 'character' dict in place
    """
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
        time_req = (
            character["prev_animation_time"] 
            + character["animation_cd"]
        )
        if curtime >= time_req:
            character["prev_animation_time"] = curtime
            character["cur_idle_frame"] %= len(character["idle_anims"])
            cur_frame = character["cur_idle_frame"]
            character["sprite"] = character["idle_anims"][cur_frame]
            character["hitbox"] = character["idle_hitbox"][cur_frame]
            character["cur_idle_frame"] += 1