import math
import random
from background import map_constants

def occupied_free(x, y, occupied, player, num_tiles_x, num_tiles_y):
    """
    Checks if a specific coordinate is occupied or not

    Args:
        x (float): The x coord to be checked
        y (float): The y coord to be checked
        occupied (list[list[bool]]): A 2D boolean grid 
        representing all occupied locations on screen
        
        player (dict): The player dictionary
        num_tiles_x (int): The number of columns in the screen grid
        num_tiles_y (int): The number of rows in the screen grid
    
    Returns:
        bool: Whether the desired location is occupied or not
    """
    nx = x - player["camera_offsetx"]
    ny = y - player["camera_offsety"]
    tile_x = int(nx // map_constants.BOX_WIDTH)
    tile_y = int(ny // map_constants.BOX_HEIGHT)
    if (
        tile_y >= 0 
        and tile_y < num_tiles_y 
        and tile_x >= 0 
        and tile_x < num_tiles_x
    ):
        return not occupied[tile_y][tile_x]
    if x >= 0 and y >= 0 and y < map_constants.MAP_HEIGHT:
        return True
    
    return False

def find_target(enemy, available_loc, player):
    """
    Finds an unoccupied location for the enemy to go towards in its radius
    
    Args:
        enemy (dict): Dictionary of the enemy
        available_loc (list): All unoccupied locations in the screen
        player (dict): Dictionary of the player

    Returns:
        None: Finds and updates in place
    """
    if available_loc:
        valid_spots_inradius = []
        for i in range(len(available_loc)):
            loc_x = (
                available_loc[i][0] * map_constants.BOX_WIDTH 
                + player["camera_offsetx"]
            )
            loc_y = (
                available_loc[i][1] * map_constants.BOX_HEIGHT 
                + player["camera_offsety"]
            )
            dist = math.hypot(loc_x - enemy["x"], loc_y - enemy["y"])
            if dist < enemy["movement_radius"]:
                valid_spots_inradius.append(available_loc[i])
        if valid_spots_inradius:
            chosen_loc = random.choice(valid_spots_inradius)
            enemy["target_x"] = (
                 chosen_loc[0] * map_constants.BOX_WIDTH 
                 + player["camera_offsetx"]
            )
            enemy["target_y"] = (
                 chosen_loc[1] * map_constants.BOX_HEIGHT 
                 + player["camera_offsety"]
            )

def move_towards_target(
        enemy, 
        game_data, 
        player, 
        num_tiles_x, 
        num_tiles_y
    ):
    """
    Moves the enemy towards its target location

    Args:
        enemy (dict): Dictionary of the enemy
        game_data (dict): Dictionary of game data
        player (dict): Dictionary of the player
        num_tiles_x (int): The number of columns in the screen grid
        num_tiles_y (int): The number of rows in the screen grid
    
    Returns:
        bool: Whether the enemy has reached the target location or not
    """
    dx = enemy["target_x"] - enemy["x"]
    dy = enemy["target_y"] - enemy["y"]
    dist = math.hypot(dx, dy)
    if dist < 10:
        return True
    else:
        occupied = game_data["occupied"]
        enemy_x = (
            enemy["x"] 
            + (dx/dist) * enemy["movement_speed"] * game_data["dt"]
        )
        enemy_y = (
            enemy["y"] 
            + (dy/dist) * enemy["movement_speed"] * game_data["dt"]
        )

        #Checks if any movement can lead it closer to target location,
        #while not moving into a slot that is occupied
        if occupied_free(
            enemy_x, 
            enemy_y, 
            occupied, 
            player, 
            num_tiles_x, 
            num_tiles_y
        ):
            enemy["x"] = enemy_x
            enemy["y"] = enemy_y
        elif occupied_free(
            enemy_x, 
            enemy["y"], 
            occupied, 
            player, 
            num_tiles_x, 
            num_tiles_y
        ):
            enemy["x"] = enemy_x
        elif occupied_free(
            enemy["x"], 
            enemy_y, 
            occupied, 
            player, 
            num_tiles_x, 
            num_tiles_y
        ):
            enemy["y"] = enemy_y
        return False


def update_enemy_pos(game_data, player, num_tiles_x, num_tiles_y):
    """
    Calculates and applies movement logic to all enemies

    Args:
        game_data (dict): 
        A dictionary containing 'enemies', 'occupied', and 'dt'

        player (dict): 
        The player dictionary

        num_tiles_x (int): 
        The number of columns in the screen grid

        num_tiles_y (int): 
        The number of rows in the screen grid
    
    Returns:
        None: Modifies the 'enemies' list in 'game_data' in place
    """
    available_loc = []
    occupied = game_data["occupied"]
    for i in range(len(occupied)):
        for j in range(len(occupied[i])):
            if occupied[i][j] == False:
                available_loc.append((j, i))

    for enemy in game_data["enemies"]:
        if enemy["target_x"] == None:
            if enemy["wait_timer"] > game_data["dt"] * 1000:
                enemy["wait_timer"] -= game_data["dt"] * 1000
            else:
                enemy["wait_timer"] = 0
                if enemy["mob_type"] == "ranged":
                    find_target(enemy, available_loc, player)
                else:
                    enemy["target_x"] = player["x"]
                    enemy["target_y"] = player["y"]
        else:
            reached_target = move_towards_target(
                enemy, 
                game_data, 
                player, 
                num_tiles_x, 
                num_tiles_y
            )
            if reached_target:
                enemy["target_x"] = None
                enemy["wait_timer"] = random.randint(800, 1400)

        enemy["hitbox"].x = int(enemy["x"])
        enemy["hitbox"].y = int(enemy["y"])