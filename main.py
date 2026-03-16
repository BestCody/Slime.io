import pygame
import random
import math

#Importing files for functions
import character_movement
import attack_mechanism
import image_process
import enemy_movement
import scores.score_functions as score_functions

#Importing constants
from characters.slime import slime_constants
from obstacles.blockage import blockage_constants
from obstacles.arrow import arrow_constants
from enemies.skeleton import skeleton_constants
from enemies.snake import snake_constants
from cards import card_constants
from cards import card_functions
from background import map_constants
from background import menu_constants
from cursors import cursor_constants
from enemies import enemies_constants
from abilities import abilities_constants

#Importing metadata for sprite sheets
from obstacles.blockage.blockage_sprite_sheet_data import(
	blockage_data
)
from enemies.skeleton.skeleton_attack.skeleton_attack_sprite_sheet_data import(
	skeleton_attack_data
)
from enemies.snake.snake_attack.snake_attack_sprite_sheet_data import(
	snake_attack_data
)

pygame.init()
pygame.mixer.init()

#Initializing the screen and clock
screen_size = [map_constants.CAMERA_WIDTH, map_constants.CAMERA_HEIGHT]
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock() 

#Slime image loading and scaling
slime_still = (
	pygame.image.load("characters/slime/slime_standing_still.png")
	.convert_alpha()
)

slime_moving_right = (
	pygame.image.load("characters/slime/slime_moving_right.png")
	.convert_alpha()
)

slime_moving_left = (
	pygame.image.load("characters/slime/slime_moving_left.png")
	.convert_alpha()
)

slime_attack = (
	pygame.image.load("characters/slime/slime_attack.png")
	.convert_alpha()
)

slime_size = (slime_constants.SLIME_WIDTH, slime_constants.SLIME_HEIGHT)
slime_still = pygame.transform.scale(slime_still, (slime_size))
slime_moving_right = pygame.transform.scale(slime_moving_right, slime_size)
slime_moving_left = pygame.transform.scale(slime_moving_left, slime_size)

slime_stretch = pygame.transform.scale(
	slime_still, 
	(
		slime_constants.SLIME_STRETCH_WIDTH, 
		slime_constants.SLIME_STRETCH_HEIGHT
	)
)

slime_attack = pygame.transform.scale(
	slime_attack, 
	(
		slime_constants.ATTACK_WIDTH, 
		slime_constants.ATTACK_HEIGHT
	)
)

slime_still_hitbox = slime_still.get_rect(
	center = (screen_size[0]//2, screen_size[1]//2)
)
slime_moving_left_hitbox = slime_moving_left.get_rect(
	midbottom = slime_still_hitbox.midbottom
)
slime_moving_right_hitbox = slime_moving_right.get_rect(
	midbottom = slime_still_hitbox.midbottom
)
slime_stretch_hitbox = slime_stretch.get_rect(
	midbottom = slime_still_hitbox.midbottom
)

slime_idle_anims = [slime_stretch, slime_still]
slime_idle_hitbox = [slime_stretch_hitbox, slime_still_hitbox]

def create_slime_player():
	"""
	Initializes all data for the slime

	Args:
		None
	Returns:
		A dictionary containing all data for the slime
	"""
	return {
		"attack_type": slime_constants.ATTACK_TYPE,
		"sprite": slime_still,
		"hitbox": slime_still_hitbox.copy(),
		"health": slime_constants.SLIME_HEALTH,
		"orig_health": slime_constants.SLIME_HEALTH,
		"defense": 0,
		"speed": slime_constants.SLIME_SPEED,
		"base_speed": slime_constants.SLIME_SPEED,
		"sprint_speed": slime_constants.SLIME_SPEED * 1.5,
		"stamina": slime_constants.SLIME_MAX_STAMINA,
		"max_stamina": slime_constants.SLIME_MAX_STAMINA,
		"stamina_drain": slime_constants.SLIME_STAMINA_DRAIN,
		"stamina_regen": slime_constants.SLIME_STAMINA_REGEN,
		"projectile_attack": slime_attack,
		"projectile_damage": slime_constants.ATTACK_DAMAGE,
		"projectile_attack_radius": slime_constants.ATTACK_RADIUS,
		"projectile_attack_cd": slime_constants.ATTACK_COOLDOWN,
		"projectile_attack_speed": slime_constants.ATTACK_SPEED,
		"x": 0,
		"y": 0,
		"animation_cd": slime_constants.SLIME_ANIMATION_SPEED,
		"prev_animation_time": 0,
		"prev_attack_time": 0,
		"camera_offsetx": 0,
		"camera_offsety": 0,
		"still_sprite": slime_still,
		"still_hitbox": slime_still_hitbox,
		"moving_right_sprite": slime_moving_right,
		"moving_right_hitbox": slime_moving_right_hitbox,
		"moving_left_sprite": slime_moving_left,
		"moving_left_hitbox": slime_moving_left_hitbox,
		"idle_anims": slime_idle_anims,
		"idle_hitbox": slime_idle_hitbox,
		"cur_idle_frame": 0,
		"abilities": [],
		"invisible": False,
		"invincible": False
	}

player = create_slime_player()
health_bar = (
	pygame.image.load(
		"characters/general_assets/health_bar.png"
	)
)
stamina_bar = (
	pygame.image.load("characters/slime/stamina_bar.png")
	.convert_alpha()
)

health_bar = pygame.transform.scale(
	health_bar, 
	(
		slime_constants.SLIME_HEALTH_BAR_WIDTH, 
		slime_constants.SLIME_HEALTH_BAR_HEIGHT
	)
)

stamina_bar = pygame.transform.scale(
	stamina_bar, 
	(
		slime_constants.SLIME_STAMINA_BAR_WIDTH, 
		slime_constants.SLIME_STAMINA_BAR_HEIGHT
	)
)

#Backgrounds image loading and scaling
map = pygame.image.load("background/start_map.png").convert()
map_infinite_generate = (
	pygame.image.load("background/infinite_map.png").convert()
)
play_screen = (
	pygame.image.load("background/play_screen.png").convert()
)
manual = pygame.image.load("background/manual.png").convert()
settings = pygame.image.load("background/settings.png").convert()
play_screen = pygame.transform.scale(
	play_screen, 
	(
		screen_size[0], 
		screen_size[1]
	)
)
manual = pygame.transform.scale(
	manual, 
	(
		screen_size[0], 
		screen_size[1]
	)
)
settings = pygame.transform.scale(
	settings,
	(
		screen_size[0],
		screen_size[1]
	)
)
map = pygame.transform.scale(
	map, 
	(
		map_constants.MAP_WIDTH, 
		map_constants.MAP_HEIGHT
	)
)
map_infinite_generate = pygame.transform.scale(map_infinite_generate, 
											   (map_constants.MAP_WIDTH, 
												map_constants.MAP_HEIGHT))
num_box_tiles_x = int(screen_size[0] / map_constants.BOX_WIDTH)
num_box_tiles_y = int(map_constants.MAP_HEIGHT / map_constants.BOX_HEIGHT) - 2

#Abilities image loading and scaling
abilities_bar = (
	pygame.image.load("abilities/abilities_bar.png")
	.convert_alpha()
)
card_picker = (
	pygame.image.load("abilities/card_picker.png")
	.convert_alpha()
)
ghost_ability_icon = (
	pygame.image.load("abilities/ghost_ability_icon.png")
	.convert_alpha()
)
scatter_ability_icon = (
	pygame.image.load("abilities/scatter_ability_icon.png")
	.convert_alpha()
)

abilities_bar = pygame.transform.scale(
	abilities_bar,                                    
	(
		abilities_constants.ABILITIES_BAR_WIDTH, 
		abilities_constants.ABILITIES_BAR_HEIGHT
	)
)

card_picker = pygame.transform.scale(
	card_picker, 
	(
		card_constants.CARD_PICKER_WIDTH, 
		card_constants.CARD_PICKER_HEIGHT
	)
)

ghost_ability_icon = pygame.transform.scale(
	ghost_ability_icon, 
	(
		abilities_constants.ABILITY_ICON_WIDTH, 
		abilities_constants.ABILITY_ICON_HEIGHT
	)
)

scatter_ability_icon = pygame.transform.scale(
	scatter_ability_icon, 
	(
		abilities_constants.ABILITY_ICON_WIDTH, 
		abilities_constants.ABILITY_ICON_HEIGHT
	)
)

card_picker_rect = card_picker.get_rect(
	midtop=(
		screen_size[0] // 2,                                             
		card_constants.CARD_PICKER_Y_PADDING
	)
)

#Cards image loading and scaling
card_cover = pygame.image.load("cards/card_cover.png").convert_alpha()
card_side = pygame.image.load("cards/card_side.png").convert_alpha()
attack_card = pygame.image.load("cards/attack_card.png").convert_alpha()
heal_card = pygame.image.load("cards/heal_card.png").convert_alpha()
ghost_card = pygame.image.load("cards/ghost_card.png").convert_alpha()
shield_card = pygame.image.load("cards/shield_card.png").convert_alpha()
scatter_card = pygame.image.load("cards/scatter_card.png").convert_alpha()
speed_card = pygame.image.load("cards/speed_card.png").convert_alpha()

card_cover = pygame.transform.scale(
	card_cover, 
	(
		card_constants.CARD_WIDTH, 
		card_constants.CARD_HEIGHT
	)
)

card_size = (card_constants.CARD_WIDTH, card_constants.CARD_HEIGHT)
card_side = pygame.transform.scale(card_side, card_size)
attack_card = pygame.transform.scale(attack_card, card_size)
heal_card = pygame.transform.scale(heal_card, card_size)
shield_card = pygame.transform.scale(shield_card, card_size)
speed_card = pygame.transform.scale(speed_card, card_size)
ghost_card = pygame.transform.scale(ghost_card, card_size)
scatter_card = pygame.transform.scale(scatter_card, card_size)

cards = {
	"attack_card": {
		"sprite": attack_card,
		"command": card_functions.buff_attack,
		"chance": 10,
		"have_icon": False
	}, 
	"heal_card": {
		"sprite": heal_card,
		"command": card_functions.buff_health,
		"chance": 10,
		"have_icon": False
	},
	"shield_card": {
		"sprite": shield_card,
		"command": card_functions.buff_defense,
		"chance": 10,
		"have_icon": False
	},
	"speed_card": {
		"sprite": speed_card,
		"command": card_functions.buff_speed,
		"chance": 10,
		"have_icon": False
	},
	"ghost_card": {
		"name": "ghost",
		"sprite": ghost_card,
		"command": card_functions.ghost,
		"chance": 5,
		"icon": ghost_ability_icon,
		"have_icon": True
	},
	"scatter_card": {
		"name": "scatter",
		"sprite": scatter_card,
		"command": card_functions.scatter,
		"chance": 9999,
		"icon": scatter_ability_icon,
		"have_icon": True
	}
}
card_animation = [card_cover, card_side]

#Obstacles

#Arrow image loading and scaling
arrow = (
	pygame.image.load("obstacles/arrow/arrow_sprite.png")
	.convert_alpha()
)
arrow = pygame.transform.scale(
	arrow, 
	(
		arrow_constants.ARROW_WIDTH, 
		arrow_constants.ARROW_HEIGHT
	)
)

#Blockage image loading and scaling
blockage_sprite_sheet = (
	pygame.image.load("obstacles/blockage/sprite_sheet.png")
	.convert_alpha()
)
blockage_frames = image_process.process_img(
	blockage_sprite_sheet, blockage_data
)
for i in range(len(blockage_frames)):
	blockage_frames[i] = pygame.transform.scale(
			blockage_frames[i], 
			(
				blockage_constants.BLOCKAGE_WIDTH, 
				blockage_frames[i].height 
				* blockage_constants.BLOCKAGE_HEIGHT_SCALE_FACTOR
			)
	)

#Enemies
#Skeleton image loading and scaling
skeleton_idle = (
	pygame.image.load("enemies/skeleton/skeleton_idle.png")
	.convert_alpha()
)
skeleton_attack_sprite_sheet = (
	pygame.image.load("enemies/skeleton/skeleton_attack/sprite_sheet.png")
	.convert_alpha()
)

skeleton_attack_frames = image_process.process_img(
	skeleton_attack_sprite_sheet, 
	skeleton_attack_data
)

skeleton_idle = pygame.transform.scale(
	skeleton_idle, 
	(
		skeleton_idle.width
		* skeleton_constants.SKELETON_WIDTH_SCALE_FACTOR, 
		skeleton_idle.height
		* skeleton_constants.SKELETON_HEIGHT_SCALE_FACTOR
	)
)

for i in range(len(skeleton_attack_frames)):
	skeleton_attack_frames[i] = pygame.transform.scale(
		skeleton_attack_frames[i], 
		(
			skeleton_attack_frames[i].width
			* skeleton_constants.SKELETON_WIDTH_SCALE_FACTOR, 
			skeleton_attack_frames[i].height
			* skeleton_constants.SKELETON_HEIGHT_SCALE_FACTOR
		)
	)

#Snake image loading and scaling
snake_idle = (
	pygame.image.load("enemies/snake/snake_idle.png")
	.convert_alpha()
)
snake_attack_sprite_sheet = (
	pygame.image.load("enemies/snake/snake_attack/sprite_sheet.png")
	.convert_alpha()
)
snake_attack_sprite = (
	pygame.image.load("enemies/snake/snake_attack/snake_attack_sprite.png")
	.convert_alpha()
)
snake_attack_frames = image_process.process_img(
	snake_attack_sprite_sheet, 
	snake_attack_data
)

snake_idle = pygame.transform.scale(
	snake_idle, 
	(
		snake_idle.width
		* snake_constants.SNAKE_WIDTH_SCALE_FACTOR, 
		snake_idle.height
		* snake_constants.SNAKE_HEIGHT_SCALE_FACTOR
	)
)

snake_attack_sprite = pygame.transform.scale(
	snake_attack_sprite, 
	(
		snake_constants.SNAKE_PROJECTILE_WIDTH, 
		snake_constants.SNAKE_PROJECTILE_HEIGHT
	)
)

for i in range(len(snake_attack_frames)):
	snake_attack_frames[i] = pygame.transform.scale(
		snake_attack_frames[i], 
		(
			snake_attack_frames[i].width
			* snake_constants.SNAKE_WIDTH_SCALE_FACTOR, 
			snake_attack_frames[i].height
			* snake_constants.SNAKE_HEIGHT_SCALE_FACTOR
		)
	)

#Cursor image loading and scaling
pygame.mouse.set_visible(False)
ingame_cursor = pygame.image.load("cursors/ingame_cursor.png").convert_alpha()
menu_cursor = pygame.image.load("cursors/menu_cursor.png").convert_alpha()
ingame_cursor = pygame.transform.scale(
	ingame_cursor, 
	(
		cursor_constants.CURSOR_WIDTH, 
		cursor_constants.CURSOR_HEIGHT
	)
)
menu_cursor = pygame.transform.scale(
	menu_cursor, 
	(
		cursor_constants.CURSOR_WIDTH, 
		cursor_constants.CURSOR_HEIGHT
	)
)

#Initializing game data
def create_game_data():
	"""
	Initializes all important data for the game

	Args:
		None
	Returns:
		A dictionary containing all important data
	"""
	return {
		"attacks": [],
		"enemies": [],
		"arrows": [],
		"blockages": [],
		"score": 0,
		"prev_score": 0,
		"prev_arrow_spawn_time": 0,
		"prev_blockage_spawn_time": 0,
		"prev_score_upd": 0,
		"game_state": "in_menu",
		"cursor": menu_cursor,
		"dt": 0,
		"occupied": [
			[False for _ in range(num_box_tiles_x)] 
			for _ in range(num_box_tiles_y)
		],
		"obstacle_occupied": [
			[False for _ in range(num_box_tiles_x)] 
			for _ in range(num_box_tiles_y)
		],
		"enemies_killed": 0,
		"show_cards": False,
		"card_displayed": [],
		"card_animation_index": 0,
		"prev_card_animation_time": 0,
		"pending_card_picks": 0
	}

screen.fill("black")
game_data = create_game_data()
running = True

#Score calculations
score_font = pygame.font.Font(None, 30)
menu_score_font = pygame.font.Font("fonts/menu_score_font.ttf", 40)

SCORE_FILES = {
	"easy": "scores/score_easy.txt",
	"medium": "scores/score_medium.txt",
	"hard": "scores/score_hard.txt"
}

SCORE_HEALTH_SCALERS = {
	"easy": 4,
	"medium": 1,
	"hard": 0.5
}

cur_diff = "medium"
max_score = score_functions.calc_max_score(cur_diff, SCORE_FILES)

while running:
	#Getting needed input for future calculations
	left_click = False
	mouse_pos = pygame.mouse.get_pos()
	keys = pygame.key.get_pressed()
	is_shifting = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]                                       

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			max_score = max(game_data["score"], max_score)
			with open(SCORE_FILES[cur_diff], 'w') as file:
				file.write(str(max_score) + '\n')
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				left_click = True
			if game_data["game_state"] == "in_menu":
				if menu_constants.PLAY_BUTTON_HITBOX.collidepoint(mouse_pos):
					game_data["game_state"] = "play"
					left_click = False
					scaler = SCORE_HEALTH_SCALERS[cur_diff]
					player["health"] *= scaler
					player["orig_health"] = player["health"]
				elif menu_constants.MANUAL_BUTTON_HITBOX.collidepoint(mouse_pos):
					game_data["game_state"] = "in_manual"
					left_click = False
				elif menu_constants.SETTINGS_BUTTON_HITBOX.collidepoint(mouse_pos):
					game_data["game_state"] = "in_settings"
					left_click = False

	if game_data["game_state"] == "in_menu":
		screen.blit(play_screen, (0, 0))

		#Draw max score
		max_score_text = menu_score_font.render(
			f"{max_score}", False, (0, 0, 0)
		)
		screen.blit(max_score_text, (screen_size[0]
									 - max_score_text.width 
									 + menu_constants.SCORE_RIGHT_PADDING, 
									 screen_size[1]
									 - max_score_text.height
									 + menu_constants.SCORE_TOP_PADDING))
		
		#Draw highlighting for menu buttons if mouse hovers
		if menu_constants.PLAY_BUTTON_HITBOX.collidepoint(mouse_pos):
			pygame.draw.rect(screen, (255, 255, 0), 
							 menu_constants.PLAY_BUTTON_HITBOX, 2)
			
		elif menu_constants.MANUAL_BUTTON_HITBOX.collidepoint(mouse_pos):
			pygame.draw.rect(screen, (255, 255, 0), 
							 menu_constants.MANUAL_BUTTON_HITBOX, 2)
			
		elif menu_constants.SETTINGS_BUTTON_HITBOX.collidepoint(mouse_pos):
			pygame.draw.rect(screen, (255, 255, 0),
							 menu_constants.SETTINGS_BUTTON_HITBOX, 2)
	
	elif game_data["game_state"] == "in_manual":
		screen.blit(manual, (0, 0))
		if keys[pygame.K_ESCAPE]:
			game_data["game_state"] = "in_menu"

	elif game_data["game_state"] == "in_settings":
		screen.blit(settings, (0, 0))
		easy_diff_hitbox = menu_constants.EASY_DIFFICULTY_HITBOX
		med_diff_hitbox = menu_constants.MEDIUM_DIFFICULTY_HITBOX
		hard_diff_hitbox = menu_constants.HARD_DIFFICULTY_HITBOX
		if easy_diff_hitbox.collidepoint(mouse_pos):
			pygame.draw.rect(
				screen, 
				(0, 0, 0), 
				easy_diff_hitbox, 
				2
			)
			if left_click:
				cur_diff = "easy"
				max_score = score_functions.calc_max_score(
					cur_diff,
					SCORE_FILES
				)
				game_data["game_state"] = "in_menu"
			
		elif med_diff_hitbox.collidepoint(mouse_pos):
			pygame.draw.rect(
				screen, 
				(0, 0, 0), 
				med_diff_hitbox, 
				2
			)
			if left_click:
				cur_diff = "medium"
				max_score = score_functions.calc_max_score(
					cur_diff,
					SCORE_FILES
				)
				game_data["game_state"] = "in_menu"     
			
		elif hard_diff_hitbox.collidepoint(mouse_pos):
			pygame.draw.rect(
				screen, 
				(0, 0, 0), 
				hard_diff_hitbox, 
				2
			)
			if left_click:
				cur_diff = "hard"
				max_score = score_functions.calc_max_score(
					cur_diff,
					SCORE_FILES
				)
				game_data["game_state"] = "in_menu"
			
		if keys[pygame.K_ESCAPE]:
			game_data["game_state"] = "in_menu"

	else:
		game_data["cursor"] = ingame_cursor
		screen.fill("black")
		curtime = pygame.time.get_ticks()

		if player["health"] <= 0 or keys[pygame.K_ESCAPE]:
			max_score = max(game_data["score"], max_score)
			with open(SCORE_FILES[cur_diff], 'w') as file:
				file.write(str(max_score) + '\n')
			player = create_slime_player()
			game_data = create_game_data()

		#Update player movement
		enough_stamina = (
			player["stamina"] 
			>= player["stamina_drain"] * game_data["dt"]
		)

		if is_shifting and enough_stamina:
			player["speed"] = player["sprint_speed"]
			player["stamina"] -= player["stamina_drain"] * game_data["dt"]
		else:
			player["speed"] = player["base_speed"]
			player["stamina"] += player["stamina_regen"] * game_data["dt"]

		player["stamina"] = max(0, player["stamina"])
		player["stamina"] = min(player["stamina"], player["max_stamina"])

		character_movement.updatemovement(
			player, 
			keys, 
			curtime, 
			game_data["dt"]
		)

		#Clamping camera
		player["camera_offsetx"] = max(
			player["camera_offsetx"], 
			- screen_size[0]/2 + map_constants.MAP_X_CLAMP
		)
		player["camera_offsety"] = max(
			player["camera_offsety"], 
			- screen_size[1]/2 + map_constants.MAP_BOTTOM_Y_CLAMP
		)
		player["camera_offsety"] = min(
			player["camera_offsety"], 
			- screen_size[1]/2 
			+ map.height
			+ map_constants.MAP_TOP_Y_CLAMP
		)
		
		player["x"]= player["hitbox"].centerx + player["camera_offsetx"]
		player["y"] = player["hitbox"].centery + player["camera_offsety"]
	
		#Drawing map or the infinite map version
		starttile = int(player["camera_offsetx"] / map.width)
		for i in range(starttile, starttile + 2):
			if i == 0:
				screen.blit(map, 
							(- player["camera_offsetx"], 
							 - player["camera_offsety"]))
			elif i > 0:
				screen.blit(
					map_infinite_generate, 
					(
						(i * map_infinite_generate.width) 
						- player["camera_offsetx"], 
						- player["camera_offsety"]
					)
				)

		#Drawing health and stamina bar
		if player["invisible"] == False:
			screen.blit(player["sprite"], player["hitbox"])
			health_bar_x = (
				player["hitbox"].x 
				+ (player["hitbox"].width - health_bar.width)//2
			)
			health_bar_y = player["hitbox"].y - health_bar.height - 5
			screen.blit(health_bar, (health_bar_x, health_bar_y))
			health_ratio = player["health"]/player["orig_health"]
			bar_width = health_ratio * (health_bar.width - 2)
			pygame.draw.rect(
				screen, 
				(255, 255, 0), 
				(
					health_bar_x + 1, 
					health_bar_y + 1, 
					bar_width,
					health_bar.height - 2
				)
			)
			
			if is_shifting or player["stamina"] < player["max_stamina"]:
				stamina_bar_x = health_bar_x
				stamina_bar_y = health_bar_y - health_bar.height - 10
				screen.blit(stamina_bar, (stamina_bar_x, stamina_bar_y))
				stamina_bar_width = (
					(player["stamina"]/player["max_stamina"])
					* (stamina_bar.width - 2)
				)
				pygame.draw.rect(screen, (0, 200, 255), 
								 (stamina_bar_x+1, 
								  stamina_bar_y+1, 
								  stamina_bar_width, 
								  stamina_bar.height-2), 0)

		#score calculations
		game_data["score"] = max(
			game_data["score"], 
			int(player["camera_offsetx"]/4)
		)

		if (curtime > 
			game_data["prev_score_upd"] 
			+ map_constants.SCORE_UPD_CD
		):
			game_data["prev_score_upd"] = curtime
			game_data["prev_score"] = game_data["score"]

		score_text = score_font.render(
			f"Score: {game_data['prev_score']}", 
			True, 
			(255, 255, 255)
		)
		
		screen.blit(
			score_text, 
			(
				screen_size[0] 
				- score_text.width
				+ map_constants.SCORE_RIGHT_PADDING, 
				map_constants.SCORE_HEIGHT
			)
		)

		#Create new attacks
		attack_req_time = (
			player["prev_attack_time"] 
			+ player["projectile_attack_cd"]
		)
		if attack_req_time < curtime:
			player["prev_attack_time"] = curtime
			game_data["attacks"].append(
				attack_mechanism.calculate_cur_ranged_attack(
					player, 
					player, 
					mouse_pos
				)
			)

		#Calculate and update the player's attacks
		game_data["attacks"] = (
			attack_mechanism.update_ranged_attacks(
				game_data["attacks"], 
				screen,
				player,
				game_data
			)
		)  

		#Update occupied list of already occupied locations
		for row in game_data["occupied"]:
			for i in range(len(row)):
				row[i] = False
		
		for row in game_data["obstacle_occupied"]:
			for i in range(len(row)):
				row[i] = False

		start_tile_x = int(
			player["camera_offsetx"] / map_constants.BOX_WIDTH
		)

		box_tile_x_player = int(
			(player["x"] - map_constants.BOX_START_X) 
			/ map_constants.BOX_WIDTH
		)
		
		box_tile_y_player = int(
			(player["y"] - map_constants.BOX_START_Y) 
			/ map_constants.BOX_HEIGHT
		)

		for a in game_data["arrows"]:
			row = int(
				(a["y"] - map_constants.BOX_START_Y) 
				/ map_constants.BOX_HEIGHT
			)
			if 0 <= row < num_box_tiles_y:
				for col in range(num_box_tiles_x):
					game_data["occupied"][row][col] = True
					game_data["obstacle_occupied"][row][col] = True

		for b in game_data["blockages"]:
			col = (
				int(
					(b["x"] - map_constants.BOX_START_X) 
					/ map_constants.BOX_WIDTH
				) 
				- start_tile_x
			)
			if 0 <= col < num_box_tiles_x:
				for row in range(num_box_tiles_y):
					game_data["occupied"][row][col] = True
					game_data["obstacle_occupied"][row][col] = True

		for enemy in game_data["enemies"][:]:
			enemy_tile_x = (
				int(
					(enemy["x"] - map_constants.BOX_START_X)
					/ map_constants.BOX_WIDTH
				)
				- start_tile_x
			)
			enemy_tile_y = (
				int(
					(enemy["y"] - map_constants.BOX_START_Y) 
					/ map_constants.BOX_HEIGHT
				)
			)
			dx = enemy["x"] - player["x"]
			dy = enemy["y"] - player["y"]
			if enemy["health"] <= 0:
				game_data["enemies"].remove(enemy)
				game_data["enemies_killed"] += 1
			elif math.hypot(dx, dy) > enemies_constants.DESPAWN_DISTANCE:
				game_data["enemies"].remove(enemy)
			elif(
				enemy_tile_x >= 0 
				and enemy_tile_x < num_box_tiles_x 
				and enemy_tile_y >= 0 
				and enemy_tile_y < num_box_tiles_y
			):
				game_data["occupied"][enemy_tile_y][enemy_tile_x] = True

		#Add new arrow obstacle if possible
		add_arrows = len(game_data["arrows"]) < arrow_constants.ARROW_SPAWN_CAP
		req_time = (
			game_data["prev_arrow_spawn_time"] 
			+ arrow_constants.ARROW_COOLDOWN
		)
		if add_arrows and curtime >= req_time:
			game_data["prev_arrow_spawn_time"] = curtime
			arrow_locs = []
			l_bound = (box_tile_y_player 
					   - arrow_constants.ARROW_SPAWN_RANGE//2)
			l_bound = max(l_bound, 0)
			for i in range(l_bound, box_tile_y_player):
				available = True
				for j in range(len(game_data["occupied"][i])):
					if(game_data["occupied"][i][j] == True
					   and not game_data["obstacle_occupied"][i][j]):
						available = False
				if available:
					arrow_locs.append(i)
			r_bound = (box_tile_y_player 
					   + arrow_constants.ARROW_SPAWN_RANGE//2)
			r_bound = min(r_bound, num_box_tiles_y)
			for i in range(box_tile_y_player, r_bound):
				available = True
				for j in range(len(game_data["occupied"][i])):
					if game_data["occupied"][i][j] == True:
						available = False
				if available:
					arrow_locs.append(i)

			if not arrow_locs:
				continue

			boxtile = random.choice(arrow_locs)
			arrow_x = screen_size[0] + player["camera_offsetx"]
			arrow_y = (
				map_constants.BOX_START_Y 
				+ boxtile * map_constants.BOX_HEIGHT
			)
			for i in range(num_box_tiles_x):
				game_data["occupied"][boxtile][i] = True
			game_data["arrows"].append({
				"attack_type": arrow_constants.ARROW_TYPE, 
				"projectile_sprite": arrow,
				"x": arrow_x,
				"y": arrow_y,
				"projectile_speed_x": arrow_constants.ARROW_SPEED_X,
				"projectile_speed_y": arrow_constants.ARROW_SPEED_Y,
				"projectile_orig_x": arrow_x,
				"projectile_orig_y": arrow_y,
				"projectile_damage": arrow_constants.ARROW_DAMAGE,
				"projectile_attack_radius": (
					arrow_constants.
					ARROW_ATTACK_RADIUS
				)
			})

		#Adds new blockage obstacle if possible
		add_blockage = (
			len(game_data["blockages"]) 
			< blockage_constants.BLOCKAGE_SPAWN_CAP
		)
		blockage_req_time = (
			game_data["prev_blockage_spawn_time"]
			+ blockage_constants.BLOCKAGE_COOLDOWN
		)
		if add_blockage and curtime >= blockage_req_time:
			game_data["prev_blockage_spawn_time"] = curtime
			l_bound = box_tile_x_player + 1
			l_bound = min(l_bound, start_tile_x + num_box_tiles_x - 1)
			l_bound = max(l_bound, enemies_constants.SAFE_ZONE_TILES)

			r_bound = (box_tile_x_player 
					   + blockage_constants.BLOCKAGE_SPAWN_RANGE + 1)
			r_bound = min(r_bound, start_tile_x + num_box_tiles_x - 1)
			r_bound = max(r_bound, enemies_constants.SAFE_ZONE_TILES)

			blockage_locs = []
			for i in range(l_bound, r_bound):
				available = True
				for j in range(num_box_tiles_y):
					idx = i - start_tile_x
					if(game_data["occupied"][j][idx]
					   and not game_data["obstacle_occupied"][j][idx]):
						available = False
				if available:
					blockage_locs.append(i)
			
			if not blockage_locs:
				continue

			boxtile = random.choice(blockage_locs)
			blockage_x = (
				map_constants.BOX_START_X 
				+ boxtile * map_constants.BOX_WIDTH
			)
			blockage_y = 0
			for i in range(num_box_tiles_y):
				game_data["occupied"][i][boxtile - start_tile_x] = True

			game_data["blockages"].append({
				"attack_type": (
					blockage_constants.
					BLOCKAGE_TYPE
				),
				"screen": screen,
				"idle_frame": blockage_frames[0],
				"melee_attack_frames": blockage_frames, 
				"melee_attack_animation_frame": 0,
				"melee_animation_cd": (
					blockage_constants.
					BLOCKAGE_ANIMATION_COOLDOWN
				), 
				"melee_damage": (
					blockage_constants.
					BLOCKAGE_DAMAGE
				), 
				"melee_attack_radius": (
					blockage_constants.
					BLOCKAGE_ATTACK_RADIUS
				),
				"x": blockage_x, 
				"y": blockage_y, 
				"melee_prev_animation_upd": curtime
			})

		#Updating obstacles for collisions, etc
		game_data["blockages"] = attack_mechanism.update_melee_attack(
			game_data["blockages"], 
			player, 
			curtime, 
			screen
		)

		game_data["arrows"] = (
			attack_mechanism.update_ranged_attacks(
				game_data["arrows"], 
				screen, 
				player, 
				game_data
			)
		)
		
		#Add new enemies
		cur_enemies_count = len(game_data["enemies"])
		available_slots = []
		for i in range(num_box_tiles_y):
			for j in range(num_box_tiles_x):
				tile_x = start_tile_x + j
				danger_zone = tile_x >= enemies_constants.SAFE_ZONE_TILES
				if game_data["occupied"][i][j] == False and danger_zone:
					available_slots.append((i, j))

		num_enemies = random.randint(
			enemies_constants.ENEMIES_SPAWN_MIN 
			- cur_enemies_count, 
			enemies_constants.ENEMIES_SPAWN_CAP 
			- cur_enemies_count
		)
		for _ in range(num_enemies):
			if len(available_slots) > 0:
				idx = random.randint(0, len(available_slots) - 1)
				i, j = available_slots[idx]
				available_slots.remove(available_slots[idx])
				game_data["occupied"][i][j] = True

				enemy_type = random.randint(0, 1)
				enemy_x = (
					map_constants.BOX_START_X 
					+ ((start_tile_x + j) * map_constants.BOX_WIDTH)
				)
				enemy_y = (
					map_constants.BOX_START_Y 
					+ (i * map_constants.BOX_HEIGHT)
				)
				if enemy_type == 0:
					snake_hitbox = snake_idle.get_rect(
						topleft=(enemy_x, enemy_y)
					)
					game_data["enemies"].append({
						"attack_type": (
							snake_constants.
							SNAKE_ATTACK_TYPE
						),
						"hitbox": (
							snake_hitbox
						),
						"health": (
							snake_constants.
							SNAKE_HEALTH
						),
						"movement_speed": (
							snake_constants.
							SNAKE_MOVEMENT_SPEED
						),
						"mob_type": (
							snake_constants.
							SNAKE_TYPE
						),
						"screen": (
							screen
						),
						"idle_frame": (
							snake_idle
						),
						"melee_attack_frames": (
							snake_attack_frames
						),
						"melee_attack_animation_frame": 0,
						"melee_animation_cd": (
							snake_constants.
							SNAKE_ATTACK_ANIMATION_COOLDOWN
						),
						"melee_damage": (
							snake_constants.
							SNAKE_MELEE_DAMAGE
						),
						"melee_attack_radius": (
							snake_constants.
							SNAKE_ATTACK_RADIUS
						),
						"melee_prev_animation_upd": (
							curtime
						),
						"projectile_attack": (
							snake_attack_sprite
						),
						"projectile_attack_speed": (
							snake_constants.
							SNAKE_PROJECTILE_SPEED
						),
						"projectile_damage": (
							snake_constants.
							SNAKE_PROJECTILE_DAMAGE
						),
						"projectile_attack_radius": (
							snake_constants.
							SNAKE_ATTACK_RADIUS
						),
						"projectile_attack_cd": (
							snake_constants.
							SNAKE_PROJECTILE_ATTACK_COOLDOWN
						),
						"x": (
							enemy_x
						), 
						"y": (
							enemy_y
						),     
						"target_x": None,
						"target_y": None,   
						"movement_radius": (
							snake_constants.
							SNAKE_MOVEMENT_RADIUS
						),   
						"wait_timer": 0,                
						"prev_projectile_shot": (
							curtime
						)
					})
					
				elif enemy_type == 1:
					skeleton_hitbox = skeleton_idle.get_rect(
						topleft=(enemy_x, enemy_y)
					)
					
					game_data["enemies"].append({
						"attack_type": (
							skeleton_constants.
							SKELETON_ATTACK_TYPE
						),
						"hitbox": skeleton_hitbox,
						"health": (
							skeleton_constants.
							SKELETON_HEALTH
						),
						"movement_speed": (
							skeleton_constants.
							SKELETON_MOVEMENT_SPEED
						),
						"mob_type": (
							skeleton_constants.
							SKELETON_TYPE
						),
						"screen": screen,
						"idle_frame": skeleton_idle,
						"melee_attack_frames": skeleton_attack_frames,
						"melee_attack_animation_frame": 0,
						"melee_animation_cd": (
							skeleton_constants.
							SKELETON_ATTACK_ANIMATION_COOLDOWN
						),
						"melee_damage": (
							skeleton_constants.
							SKELETON_DAMAGE
						),
						"melee_attack_radius": (
							skeleton_constants.
							SKELETON_ATTACK_RADIUS
						),
						"x": enemy_x, 
						"y": enemy_y,         
						"target_x": None,
						"target_y": None, 
						"wait_timer": 0,                 
						"melee_prev_animation_upd": curtime
					})
	
		enemy_movement.update_enemy_pos(
			game_data, 
			player, 
			num_box_tiles_x, 
			num_box_tiles_y
		)

		#Retrieve new projectiles shot by ranged enemies
		for enemy in game_data["enemies"]:
			if enemy["mob_type"] == "ranged":
				dx = enemy["x"] - player["x"]
				dy = enemy["y"] - player["y"]
				in_range = (
					math.hypot(dx, dy) 
					> snake_constants.SNAKE_PROJECTILE_OUTER_RADIUS
				)
				req_time = (
					enemy["prev_projectile_shot"] 
					+ snake_constants.SNAKE_PROJECTILE_ATTACK_COOLDOWN
				) 
				if in_range and curtime > req_time:
					enemy["prev_projectile_shot"] = curtime
					game_data["attacks"].append(
						attack_mechanism.calculate_cur_ranged_attack(
							enemy, 
							player, 
							mouse_pos
						)
					)

		#Update enemy's close range attacks for collisions with player, etc
		game_data["enemies"] = attack_mechanism.update_melee_attack(
			game_data["enemies"], 
			player, 
			curtime, 
			screen
		)

		#Display logic and retrieving all new cards the player has earned
		while game_data["enemies_killed"] >= card_constants.ENEMIES_REQ:
			game_data["enemies_killed"] -= card_constants.ENEMIES_REQ
			game_data["card_displayed"].append(card_functions.get_cards(cards))
			game_data["pending_card_picks"] += 1

		if game_data["pending_card_picks"] > 0:
			screen.blit(card_picker, card_picker_rect)
			if card_picker_rect.collidepoint(mouse_pos) and left_click:
				left_click = False
				game_data["show_cards"] = not game_data["show_cards"]
				if game_data["show_cards"]:
					game_data["card_animation_index"] = 0
					game_data["prev_card_animation_time"] = curtime

		if game_data["show_cards"]:
			card_rect = []
			cur_cards = game_data["card_displayed"][0]       
			if game_data["card_animation_index"] < len(card_animation):
				cur_idx = game_data["card_animation_index"]
				cur_delay = card_constants.CARD_DISPLAY_ANIMATION_CD[cur_idx]
				time_req = cur_delay + game_data["prev_card_animation_time"]
				if curtime >= time_req:
					game_data["prev_card_animation_time"] = curtime
					game_data["card_animation_index"] += 1

			next_card_anims = False
			for i in range(len(cur_cards)):
				card_x = (
					card_constants.CARD_DISPLAY_X 
					+ card_constants.CARD_DISPLAY_GAP*i 
					+ card_constants.CARD_WIDTH*i
				)
				card_y = card_constants.CARD_DISPLAY_Y
				cur_card_sprite = cur_cards[i]["sprite"]
				cur_idx = game_data["card_animation_index"]
				if cur_idx < len(card_animation):
					cur_card_sprite = card_animation[cur_idx]
				screen.blit(cur_card_sprite, (card_x, card_y))
				card_rect.append(
					pygame.Rect(
						card_x, 
						card_y, 
						card_constants.CARD_WIDTH, 
						card_constants.CARD_HEIGHT
					)
				)

			for i in range(len(card_rect)):
				if card_rect[i].collidepoint(mouse_pos) and left_click:
					left_click = False
					game_data["show_cards"] = False
					if cur_cards[i]["have_icon"]:
						cur_cards[i]["command"](player, cur_cards[i]["icon"])
					else:
						cur_cards[i]["command"](player)
					game_data["pending_card_picks"] -= 1
					game_data["card_displayed"].pop(0)
					game_data["card_animation_index"] = 0
					if game_data["pending_card_picks"] > 0:
						game_data["show_cards"] = True
					break
		
		#See if player has used any abilities
		for i in range(len(abilities_constants.ABILITY_SELECTION_KEYS)):
			key_clicked = keys[abilities_constants.ABILITY_SELECTION_KEYS[i]]
			if key_clicked and i < len(player["abilities"]):
				ability = player["abilities"][i]
				if ability["activated"] == False:
					ability["activated"] = True
					ability["activated_time"] = curtime
					if ability["name"] == "ghost":
						player["invincible"] = True
						player["invisible"] = True
					elif ability["name"] == "scatter":
						ability["prev_attack_time"] = (
							curtime 
							- ability["attack_cooldown"]
						)

		#Update effects and remaining duration for all used abilities
		for i in range(len(player["abilities"]) - 1, -1, -1):
			ability = player["abilities"][i]
			if ability["activated"]:
				if curtime - ability["activated_time"] >= ability["duration"]:
					if ability["name"] == "ghost":
						player["invincible"] = False
						player["invisible"] = False
					player["abilities"].pop(i)
					continue

				if ability["name"] == "scatter":
					req_time = (
						ability["attack_cooldown"] 
						+ ability["prev_attack_time"]
					)
					if curtime >= req_time:
						ability["prev_attack_time"] = curtime
						for angle in range(0, 360, 15):
							angle_rad = math.radians(angle)
							speed = player["projectile_attack_speed"]
							norm_x = math.cos(angle_rad) * speed
							norm_y = math.sin(angle_rad) * speed
							game_data["attacks"].append({
								"attack_type": player["attack_type"],
								"projectile_sprite": (
									player["projectile_attack"]
								),
								"x": (
									player["x"] 
									- player["projectile_attack"].width//2
								),
								"y": (
									player["y"] 
									- player["projectile_attack"].height//2
								),
								"projectile_speed_x": norm_x,
								"projectile_speed_y": norm_y,
								"projectile_orig_x": player["x"],
								"projectile_orig_y": player["y"],
								"projectile_damage": (
									player["projectile_damage"]
								),
								"projectile_attack_radius": (
									player["projectile_attack_radius"]
								)
							})

		#Draw UI and duration bar of all abilities the player has used
		total_abilities = len(player["abilities"])
		for i in range(total_abilities):
			ability = player["abilities"][i]
			order = total_abilities - i
			abilities_display_x = abilities_constants.ABILITIES_DISPLAY_X
			abilities_display_y = (
				screen_size[1] 
				- abilities_constants.ABILITY_ICON_HEIGHT*order 
				- 10*order
			)
			abilities_bar_x = abilities_display_x + ability["icon"].width
			abilities_bar_y = (
				abilities_display_y 
				+ (
					abilities_constants.ABILITY_ICON_HEIGHT 
					- abilities_constants.ABILITIES_BAR_HEIGHT
				)//2
			)
			screen.blit(
				ability["icon"], 
				(
					abilities_display_x, 
					abilities_display_y
				)
			)
			screen.blit(
				abilities_bar, 
				(
					abilities_bar_x, 
					abilities_bar_y
				)
			)

			ratio = 1
			if ability["activated"]:
				time_passed = curtime - ability["activated_time"]
				remaining_time = ability["duration"] - time_passed
				ratio = max(0, remaining_time) / ability["total_time"]

			bar_width = (abilities_constants.ABILITIES_BAR_WIDTH - 2) * ratio
			pygame.draw.rect(screen, (0, 255, 255), (
				abilities_bar_x + 1, 
				abilities_bar_y + 1, 
				bar_width - 1, 
				abilities_constants.ABILITIES_BAR_HEIGHT - 2
			), 0)

	screen.blit(
		game_data["cursor"], 
		(
			mouse_pos[0] - cursor_constants.CURSOR_WIDTH//2, 
			mouse_pos[1] - cursor_constants.CURSOR_HEIGHT//2
		)
	)
	game_data["dt"] = clock.tick(60) / 1000
	pygame.display.update()

pygame.quit()