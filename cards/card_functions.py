import random

def get_cards(cards):
    choices = list(cards.keys())
    weights = [cards[name]["chance"] for name in choices]
    selected_hand = []
    picked = random.choices(choices, weights=weights, k=3)
    for i in range(len(picked)):
        picked[i] = cards[picked[i]]
    return picked

def buff_attack(player):
    if "projectile_damage" in player:
        player["projectile_damage"] += 1
    if "melee_damage" in player:
        player["melee_damage"] += 1

def buff_health(player):
    player["health"] += 250

def buff_defense(player):
    player["defense"] += 5

def buff_speed(player):
    player["speed"] += 40

def ghost(player, icon):
    found = False
    for ability in player["abilities"]:
        if ability["name"] == "ghost":
            ability["duration"] += 1000
            ability["total_time"] += 1000
            found = True
            break
    if not found:
        player["abilities"].append({
            "name": "ghost",
            "duration": 1000,
            "activated": False,
            "activated_time": -1,
            "total_time": 1000,
            "icon": icon
        })

def scatter(player, icon):
    found = False
    for ability in player["abilities"]:
        if ability["name"] == "scatter":
            ability["duration"] += 3000
            ability["total_time"] += 3000
            found = True
            break
    if not found:
        player["abilities"].append({
            "name": "scatter",
            "duration": 3000,
            "activated": False,
            "activated_time": -1,
            "attack_cooldown": 200,
            "prev_attack_time": -1,
            "total_time": 3000,
            "icon": icon
        })