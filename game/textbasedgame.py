from flask import session
import logging

logging.basicConfig(level=logging.INFO)

def initialize_game():
    session['player'] = {
        'game_over': False,
        'inventory': ['ring', 'orb', 'necklace', 'potion', 'key', 'sword'],
        'location': 'Hall of Illusions',
        'name': ''
    }
    session['rooms'] = {
        'Hall of Illusions': {
            'description': 'You are in the Hall of Illusions. There are doors to the north and east.',
            'north': 'Enchanted Garden',
            'east': 'Mystic Library'
        },
        'Enchanted Garden': {
            'description': 'You are in the Enchanted Garden. There is a door to the south.',
            'south': 'Hall of Illusions'
        },
        'Mystic Library': {
            'description': 'You are in the Mystic Library. There is a door to the west.',
            'west': 'Hall of Illusions'
        }
    }

def get_new_state(action, pllocation, rooms, player):
    action = [word.lower() for word in action]

    if player.get("game_over", False) and action[0] != "restart":
        return "Game has already ended. Please start a new game."

    if action:
        if action[0] == "go":
            return move(action[1], pllocation, rooms, player)
        elif action[0] == "get":
            if len(action) > 1:
                return get_item(action[1], player, rooms)
            else:
                return "Please specify an item to get."
        elif action[0] == "check" and action[1] == "stats":
            return show_status(player, rooms)
        elif action[0] == "quit":
            player["game_over"] = True
            return "You have quit the game."
        elif action[0] == "restart":
            reset_game()
            return "Game has been restarted."
        else:
            return "Invalid action."
    else:
        return "Please enter a valid action."

def move(direction, pllocation, rooms, player):
    if direction in rooms[pllocation]:
        new_location = rooms[pllocation][direction]
        player["location"] = new_location

        if new_location == "Hall of Illusions":
            if len(player["inventory"]) == 6:
                player["game_over"] = True
                return "You have found and defeated Divisio. You have saved the kingdom of Kalambia."
            else:
                player["game_over"] = True
                return "You have been defeated by Divisio. You must find all the items to defeat him."
        
        return f"Moved to {new_location}"
    else:
        return "You can't go that way."

def show_status(player, rooms):
    status = f"You are in the {player['location']}\n"

    if len(player["inventory"]) == 0:
        status += "Inventory: []\n"
    else:
        status += "Inventory: ["
        for item in player["inventory"]:
            if item == player["inventory"][-1]:
                status += item.capitalize()
            else:
                status += f"{item.capitalize()}, "
        status += "]\n"

    if "item" in rooms[player["location"]]:
        status += f"Items in this room: {rooms[player['location']]['item'][0]}\n"

    return status

def get_item(item, player, rooms):
    current_room_items = rooms[player["location"]].get("item", [])
    if item.capitalize() in current_room_items:
        player["inventory"].append(item)
        current_room_items.remove(item.capitalize())
        return f"You have added a {item.capitalize()} to your inventory."
    else:
        return "That item is not in this room."

def game_intro():
    return (
        "Welcome to The Pale Palace.\n"
        "You are Kalambia's final hope to save the kingdom from the evil sorcerer, Divisio.\n"
        "You must navigate through the palace, find all 6 items, and defeat Divisio to save the kingdom.\n"
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        "Move commands: 'go North', 'go South', 'go East', 'go West'\n"
        "Add an item to inventory: get 'item name'\n"
        "Check stats: 'check stats'\n"
        "Exit game: 'quit'\n"
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    )

def process_input(user_input):
    if not user_input:
        return "Please enter a command."
    
    action = user_input.split()
    player = session['player']
    rooms = session['rooms']

    if player['game_over']:
        if action[0] == 'restart':
            initialize_game()
            return "Game restarted. " + rooms[player['location']]['description']
        else:
            return "Game has already ended. Please type 'restart' to start a new game."

    command = action[0]
    if command == 'go':
        if len(action) < 2:
            return "Go where?"
        direction = action[1]
        current_location = player['location']
        if direction in rooms[current_location]:
            player['location'] = rooms[current_location][direction]
            session['player'] = player
            return rooms[player['location']]['description']
        else:
            return "You can't go that way."
    elif command == 'look':
        return rooms[player['location']]['description']
    elif command == 'inventory':
        if player['inventory']:
            return "You have: " + ", ".join(player['inventory'])
        else:
            return "You are not carrying anything."
    elif command == 'take':
        if len(action) < 2:
            return "Take what?"
        item = action[1]
        # Example logic for taking items
        if item in ['ring', 'orb', 'necklace', 'potion', 'key', 'sword'] and player['location'] == 'Hall of Illusions':
            player['inventory'].append(item)
            session['player'] = player
            return "You took the " + item + "."
        else:
            return "There is no " + item + " here."
    elif command == 'drop':
        if len(action) < 2:
            return "Drop what?"
        item = action[1]
        if item in player['inventory']:
            player['inventory'].remove(item)
            session['player'] = player
            return "You dropped the " + item + "."
        else:
            return "You don't have " + item + "."
    elif command == 'restart':
        initialize_game()
        return "Game restarted. " + rooms[player['location']]['description']
    elif command == 'check' and len(action) > 1 and action[1] == 'stats':
        return "Location: " + player['location'] + ", Inventory: " + ", ".join(player['inventory'])
    else:
        return "I don't understand that command."