import pygame
import math

def calculate_cur_ranged_attack(object, player, mousepos):
    """
    Calculates the target and rotation of a fired projectile
    
    Args:
        object (dict): The entity firing the projectile
        player (dict): The player dictionary
        mousepos (tuple): The (x, y) position of the mouse on the screen
    
    Returns:
        dict: A dictionary representing the newly calculated 
        projectile and contains all the information
        needed for the function update_ranged_attacks
    """

    #Calculate angle of projectil and rotate the attack sprite
    if object["attack_type"] == "player":
        anglex = mousepos[0] - object["x"] + player["camera_offsetx"]
        angley = mousepos[1] - object["y"] + player["camera_offsety"]
    else:
        anglex = player["x"] - object["x"]
        angley = player["y"] - object["y"]
    angle = 180 / math.pi * math.atan2(angley, anglex)
    rotated_attack = pygame.transform.rotate(
        object["projectile_attack"], -angle
    )

    #Calculate the x and y direction the projectile must move
    normalized_x = math.cos(math.radians(angle))
    normalized_y = math.sin(math.radians(angle))

    return {
            "attack_type": object["attack_type"], 
            "projectile_sprite": rotated_attack, 
            "x": object["x"] - object["projectile_attack"].width//2,
            "y": object["y"] - object["projectile_attack"].height//2,
            "projectile_speed_x": (
                normalized_x
                * object["projectile_attack_speed"]
            ), 
            "projectile_speed_y": (
                normalized_y
                * object["projectile_attack_speed"]
            ), 
            "projectile_orig_x": object["x"], 
            "projectile_orig_y": object["y"], 
            "projectile_damage": object["projectile_damage"], 
            "projectile_attack_radius": object["projectile_attack_radius"]
        }

def update_ranged_attacks(attacks, screen, player, game_data):
    """
    Handles collisions, updates positions, 
    and rendering for all projectiles in the game

    Args:
        attacks (list): A list of dictionaries 
        containing active projectiles in the game

        screen (pygame.Surface): The surface 
        inwhich the projectile is rendered

        player (dict): The player dictionary
        game_data (dict): The dictionary containing the list of enemies

    Returns:
        -A list of dictionaries containing projectiles 
        that are still active from 'attacks'
    """
    updated_attacks = []
    for attack in attacks:
        attack_hitbox = attack["projectile_sprite"].get_rect(
            topleft=(attack["x"], attack["y"])
        )
        screen.blit(
            attack["projectile_sprite"], 
            (
                attack["x"] - player["camera_offsetx"], 
                attack["y"] - player["camera_offsety"]
            )
        )
        
        hit = False
        if (attack["attack_type"] == "enemy" 
            or attack["attack_type"] == "obstacle"
        ):
            new_player_hitbox = player["hitbox"].copy()
            new_player_hitbox.center = (player["x"], player["y"])
            if attack_hitbox.colliderect(new_player_hitbox):
                if player["invincible"] == False:
                    player["health"] -= (
                        attack["projectile_damage"] 
                        - player["defense"]
                    )
                hit = True
        elif attack["attack_type"] == "player":
            for enemy in game_data["enemies"]:
                if attack_hitbox.colliderect(enemy["hitbox"]):
                    enemy["health"] -= attack["projectile_damage"]
                    hit = True

        attack["x"] += (attack["projectile_speed_x"] * game_data["dt"])
        attack["y"] += (attack["projectile_speed_y"] * game_data["dt"])
        dx = attack["projectile_orig_x"] - attack["x"]
        dy = attack["projectile_orig_y"] - attack["y"]
        if math.hypot(dx, dy) < attack["projectile_attack_radius"] and not hit:
            updated_attacks.append(attack)

    return updated_attacks

def update_melee_attack(attacks, player, curtime, screen):
    """
    Manages animation states, collisions, and rendering 
    for all attacks which are not moving / only extending

    Args:
        attacks (list): A list of dictionaries of entities 
        which have melee attacks
        
        player (dict): The player dictionary
        curtime (int): The current game time in milliseconds
        screen (pygame.Surface): The surface in which the 
        attacking animations and sprites are drawn onto
    
    Returns:
        updated_attacks (list): A list of dictionaries
        of updated attacks from 'attacks'
    """
    updated_attacks = []
    player_hitbox = player["hitbox"].copy()
    player_hitbox.center = (player["x"], player["y"])

    for attack in attacks:
        dx = attack["x"] - player["x"]
        dy = attack["y"] - player["y"]
        dist = math.hypot(dx, dy)
        if dist <= attack["melee_attack_radius"]:
            frame = attack["melee_attack_animation_frame"]
            cd = attack["melee_animation_cd"][frame]
            req_time = attack["melee_prev_animation_upd"] + cd
            if curtime >= req_time:
                attack["melee_attack_animation_frame"] += 1
                attack["melee_prev_animation_upd"] = curtime
            
            deal_damage = False
            if(attack["melee_attack_animation_frame"] 
               >= len(attack["melee_attack_frames"])):
                if attack["attack_type"] == "obstacle":
                    continue
                attack["melee_attack_animation_frame"] = 0
                deal_damage = True
            
            frame = attack["melee_attack_animation_frame"]
            img = attack["melee_attack_frames"][frame]

            if attack["attack_type"] == "enemy":
                if attack["x"] < player["x"]:
                    img = pygame.transform.flip(img, True, False)
                idle_rect = attack["idle_frame"].get_rect(
                    topleft=(attack["x"], attack["y"])
                )
                hitbox = img.get_rect(midbottom=idle_rect.midbottom)
            else:
                deal_damage = True
                hitbox = img.get_rect(topleft=(attack["x"], attack["y"]))
            
            #deal_damage is mainly used for calculating whether the sprite
            #should deal damage in the current frame if a collision occurs
            #between the player and sprite
            #- Enemies only deal damage in last attack frame
            #- Obstacles deal damage in any frame
            
            if deal_damage and not player["invincible"]:
                if hitbox.colliderect(player_hitbox):
                    damage = max(attack["melee_damage"] - player["defense"], 0)
                    player["health"] -= damage
                    if attack["attack_type"] == "obstacle":
                        attack["melee_damage"] = 0
        else:
            img = attack["idle_frame"]
            if attack["attack_type"] == "enemy" and attack["x"] < player["x"]:
                img = pygame.transform.flip(img, True, False)

        screen.blit(
            img, 
            (
                attack["x"] - player["camera_offsetx"], 
                attack["y"] - player["camera_offsety"]
            )
        )
        updated_attacks.append(attack)
    
    return updated_attacks