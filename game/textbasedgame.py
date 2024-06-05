import logging
from flask import session

def initialize_game():
    logging.info("Initializing game...")
    if "player" not in session or session["player"]["game_over"]:
        reset_game()
    logging.info(f"Game initialized. Player state: {session['player']}")

def reset_game():
    logging.info("Resetting game...")
    session["player"] = {
        "game_over": False,
        "inventory": [],
        "location": "Starting Room",
        "name": ""
    }
    session["rooms"] = create_rooms()
    logging.info("Game reset. New player state and rooms initialized.")

def create_rooms():
    # Your room creation logic
    return {
        "Starting Room": {
            "description": "You are in a small, dimly lit room. There is a door to the north.",
            "exits": {"north": "Hall of Acceptance"}
        },
        "Hall of Acceptance": {
            "description": "You are in a large hall filled with the sound of echoes. There is a door to the south and another to the east.",
            "exits": {"south": "Starting Room", "east": "Hall of Illusions"}
        },
        "Hall of Illusions": {
            "description": "You are in a hall with mirrors everywhere, distorting your reflection. There is a door to the west.",
            "exits": {"west": "Hall of Acceptance"}
        }
    }

def process_input(user_input):
    logging.info(f"Processing input: {user_input}")
    action = user_input.split()
    logging.info(f"Action received: {action}")

    if not action:
        return "Invalid input. Please enter a command."

    player = session["player"]
    rooms = session["rooms"]

    if player.get("game_over", False) and action[0] != "restart":
        return "Game has already ended. Please start a new game."

    if action[0] == "restart":
        reset_game()
        return "Game has been restarted."

    response = get_new_state(action, player["location"], rooms, player)
    return response

def get_new_state(action, current_location, rooms, player):
    if action[0] == "check" and action[1] == "stats":
        return f"You are in the {player['location']}<br>Inventory: {player['inventory']}<br>"

    if action[0] == "move":
        direction = action[1]
        if direction in rooms[current_location]["exits"]:
            new_location = rooms[current_location]["exits"][direction]
            player["location"] = new_location
            return rooms[new_location]["description"]
        else:
            return "You can't go that way."

    if action[0] == "take":
        item = action[1]
        if item in rooms[current_location].get("items", []):
            player["inventory"].append(item)
            rooms[current_location]["items"].remove(item)
            return f"You have taken the {item}."
        else:
            return f"There is no {item} here."

    return "Invalid action."

# Example room creation
rooms = create_rooms()