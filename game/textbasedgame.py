from flask import session
import logging

logging.basicConfig(level=logging.INFO)

def initialize_game():
    if "player" not in session:
        reset_game()
        logging.info("Game initialized with player: %s", session["player"])

def reset_game():
    session.clear()  # Clear the session to avoid residual data
    session["player"] = {
        "name": '',
        "inventory": [],
        "location": 'Hall of Acceptance',  # Initial location
        "game_over": False,
    }
    session["rooms"] = {
        "Hall of Acceptance": {"north": 'Garden of Whispers', "south": 'Vault of Visions', "east": 'Gallery of Shadows', "west": 'Diplomatic Den'},
        "Diplomatic Den": {"east": 'Hall of Acceptance', "item": ["Necklace"]},
        "Garden of Whispers": {"south": 'Hall of Acceptance', "east": 'Beacon Tower', "item": ["Potion"]},
        "Beacon Tower": {"west": 'Garden of Whispers', "item": ["Key"]},
        "Gallery of Shadows": {"north": 'Archives of Unity', "west": 'Hall of Acceptance', "item": ["Ring"]},
        "Archives of Unity": {"south": 'Gallery of Shadows', "item": ["Orb"]},
        "Vault of Visions": {"north": 'Hall of Acceptance', "east": 'Hall of Illusions', "item": ["Sword"]},
        "Hall of Illusions": {"west": 'Vault of Visions'}
    }
    logging.info("Game reset with player: %s", session["player"])

def get_new_state(action, pllocation, rooms, player):
    logging.info("Processing action: %s", action)
    action = [word.lower() for word in action]

    if player.get("game_over", False) and action[0] != "restart":
        return "Game has already ended. Please start a new game."

    if action:
        if action[0] == "go":
            move_result = move(action[1], pllocation, rooms, player)
            return f"{move_result}\n{show_status(player, rooms)}"
        elif action[0] == "get":
            if len(action) > 1:
                get_result = get_item(action[1], player, rooms)
                return f"{get_result}\n{show_status(player, rooms)}"
            else:
                return "Please specify an item to get.\n" + show_status(player, rooms)
        elif action[0] == "check" and action[1] == "stats":
            return show_status(player, rooms)
        elif action[0] == "quit":
            player["game_over"] = True
            return "You have quit the game."
        elif action[0] == "restart":
            reset_game()
            return "Game has been restarted.\n" + show_status(player, rooms)
        else:
            return "Invalid action.\n" + show_status(player, rooms)
    else:
        return "Please enter a valid action.\n" + show_status(player, rooms)

def move(direction, pllocation, rooms, player):
    logging.info("Attempting to move %s from %s", direction, pllocation)
    if direction in rooms[pllocation]:
        new_location = rooms[pllocation][direction]
        player["location"] = new_location
        logging.info("Moved to %s", new_location)

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
        "You start your journey in the Hall of Acceptance.\n"
        "You must navigate through the palace, find all 6 items, and defeat Divisio to save the kingdom.\n"
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        "Move commands: 'go North', 'go South', 'go East', 'go West'\n"
        "Add an item to inventory: get 'item name'\n"
        "Check stats: 'check stats'\n"
        "Exit game: 'quit'\n"
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    )

def process_input(input_data):
    initialize_game()
    player = session["player"]
    rooms = session["rooms"]

    action = input_data.split()
    response = get_new_state(action, player["location"], rooms, player)
    session["player"] = player
    logging.info("Processed input: %s", response)
    logging.info("Player location after input: %s", player["location"])
    return response