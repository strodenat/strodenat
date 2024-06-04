# Description: This is a text based game that will be played in the terminal.
# Author: Nathaniel Strode

# The Pale Palace is a game where the player must navigate through the palace,
# Find all 6 items, and defeat Divisio to save the kingdom.
# The player can move through the palace by going North, South, East, or West.
# The player can add items to their inventory by getting the item in the room.
# The player can check their status
# The player can quit the game at any time. 
# The game ends when the player's location is set to the room 'exit'.

# Import flask
from flask import session

def initialize_game():
    if "player" not in session:
        session["player"] = {
            "name": '',
            "inventory": [],
            "location": 'Hall of Acceptance',
        }

    if "rooms" not in session:
        session["rooms"] = {
            "Hall of Acceptance": {"north": 'Garden of Whispers', "south": 'Vault of Visions',
                                   "east": 'Gallery of Shadows', "west": 'Diplomatic Den'},
            "Diplomatic Den": {"east": 'Hall of Acceptance', "item": ["Necklace"]},
            "Garden of Whispers": {"south": 'Hall of Acceptance', "east": 'Beacon Tower', "item": ["Potion"]},
            "Beacon Tower": {"west": 'Garden of Whispers', "item": ["Key"]},
            "Gallery of Shadows": {"north": 'Archives of Unity', "west": 'Hall of Acceptance', "item": ["Ring"]},
            "Archives of Unity": {"south": 'Gallery of Shadows', "item": ["Orb"]},
            "Vault of Visions": {"north": 'Hall of Acceptance', "east": 'Hall of Illusions', "item": ["Sword"]},
            "Hall of Illusions": {"west": 'Vault of Visions'}
        }

# Function definitions

# Define a function for getting the new state of the player
def get_new_state(action, pllocation, rooms, player):
    # Convert the player's action to lowercase
    action = [word.lower() for word in action]
    
    print(f"Action received: {action}")

    # Check if the action list is empty
    if action:
        # Check if the player wants to move
        if action[0] == "go":
            # Call the move function to move the player
            return move(action[1], pllocation, rooms, player)
        # Check if the player wants to get an item
        elif action[0] == "get":
            # Check if the player is trying to get an item
            if len(action) > 1:
                return get_item(action[1], player, rooms)
            else:
                return "Please specify an item to get."
        # Check if the player wants to check their stats
        elif action[0] == "check" and len(action) > 1 and action[1] == "stats":
            return show_status(player, rooms)
        # Check if the player wants to exit the game
        elif action[0] == "quit":
            # Change the player's location to exit
            player["location"] = "exit"
            return "You have quit the game."
        # If the player's action is blank tell the player
        elif action[0] == "":
            return "Please enter a valid action."
        # If the player's action is invalid, tell the player
        else:
            return "Invalid action."
    # If the action list is empty, tell the player
    else:
        return "Please enter a valid action."

# Define a function for moving the player
def move(direction, pllocation, rooms, player):
    print(f"Attempting to move {direction} from {pllocation}")
    # Check if the direction is valid
    if direction in rooms[pllocation]:
        # Get the new location of the player
        new_location = rooms[pllocation][direction]

        # Move the player to the new location
        player["location"] = new_location
        
        # If the player is in the Hall of Illusions check if they have all the items
        if new_location == "Hall of Illusions":
            # Check if the player has all the items
            if len(player["inventory"]) == 6:
                return "You have found and defeated Divisio. You have saved the kingdom of Kalambia."
            # If the player does not have all the items, tell the player they need to find all the items
            else:
                return "You have been defeated by Divisio. You must find all the items to defeat him."
        
        # Update the player's location and show the player's status
        return f"Moved to {new_location}"
    # If the direction is not valid, tell the player
    else:
        return "You can't go that way."

# Define a function for checking the player's stats
def show_status(player, rooms):
    # Tell the player where they are
    status = f"You are in the {player['location']}<br>"

    # Tell the player what items are in their inventory, change formatting based on the number of items
    if len(player["inventory"]) == 0:
        status += "Inventory: []<br>"
    elif len(player["inventory"]) == 1:
        status += f"Inventory: [{player['inventory'][0].capitalize()}]<br>"
    elif len(player["inventory"]) > 1:
        status += "Inventory: ["
        for item in player["inventory"]:
            if item == player["inventory"][-1]:
                status += item.capitalize()
            else:
                status += f"{item.capitalize()}, "
        status += "]<br>"

    # Tell the player what items are in the room if any
    if "item" in rooms[player["location"]]:
        status += f"Items in this room: {rooms[player['location']]['item'][0]}<br>"

    return status
    
# Define a function for getting an item
def get_item(item, player, rooms):
    print(f"Attempting to get item: {item}")
    current_room_items = rooms[player["location"]].get("item", [])
    # Check if the item is in the room ignoring case
    if item.capitalize() in current_room_items:
        # Add the item to the player's inventory
        player["inventory"].append(item)

        # Remove the item from the rooms dictionary and tell the player they have added the item to their inventory, 
        # capitalizing the first letter of the item
        current_room_items.remove(item.capitalize())
        return f"You have added a {item.capitalize()} to your inventory."
    # If the item is not in the room, tell the player the item is not there
    else:
        return "That item is not in this room."

def game_intro():
    return (
        "Welcome to The Pale Palace.<br>"
        "You are Kalambia's final hope to save the kingdom from the evil sorcerer, Divisio.<br>"
        "You must navigate through the palace, find all 6 items, and defeat Divisio to save the kingdom.<br>"
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<br>"
        "Move commands: 'go North', 'go South', 'go East', 'go West'<br>"
        "Add an item to inventory: get 'item name'<br>"
        "Check stats: 'check stats'<br>"
        "Exit game: 'quit'<br>"
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    )

def process_input(input_data):
    initialize_game()
    player = session["player"]
    rooms = session["rooms"]

    action = input_data.split()
    print(f"Processing input: {action}")
    response = get_new_state(action, player["location"], rooms, player)
    session["player"] = player
    print(f"Response: {response}")
    return response