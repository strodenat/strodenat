# Description: This is a text based game that will be played in the terminal.
# Author: Nathaniel Strode

# The Pale Palace is a game where the player must navigate through the palace,
# Find all 6 items, and defeat Divisio to save the kingdom.
# The player can move through the palace by going North, South, East, or West.
# The player can add items to their inventory by getting the item in the room.
# The player can check their status
# The player can quit the game at any time. 
# The game ends when the player's locaton is set to the room 'exit'.

# Import flask
from flask import session

# Define a dictonary for the player's stats and inventory
player_template = {
    "name":'',
    "inventory": [],
    "location": 'Hall of Acceptance', 
}

# Define a dictionary for the rooms in the palace conataining the valid directions and items
rooms_template = {   "Hall of Acceptance": {"north": 'Garden of Whispers', "south": 'Vault of Visions',
                                    "east": 'Gallery of Shadows', "west": 'Diplomatic Den'},
            "Diplomatic Den": {"east": 'Hall of Acceptance',"item": ["Necklace"]},
            "Garden of Whispers": {"south": 'Hall of Acceptance', "east": 'Beacon Tower', "item": ["Potion"]},
            "Beacon Tower": {"west": 'Garden of Whispers', "item": ["Key"]},
            "Gallery of Shadows": {"north": 'Archives of Unity', "west": 'Hall of Acceptance', "item": ["Ring"]},
            "Archives of Unity": {"south": 'Gallery of Shadows', "item": ["Orb"]},
            "Vault of Visions": {"north": 'Hall of Acceptance', "east": 'Hall of Illusions', "item": ["Sword"]},
            "Hall of Illusions": {"west": 'Vault of Visions',}
}

# Define a variable for the status output
status_output = []

# Function definitions

# Define a function for initializing the game
def initialize_game():
    session["player"] = player_template.copy()
    session["rooms"] = rooms_template.copy()
    session["status_output"] = ["Welcome to The Pale Palace!"]

# Define a function for getting the new state of the player
def get_new_state(action, pllocation, rooms, player):
    show_status(player, rooms)
    status_output = []
    status_output = [session.get("status_output", [])]

    # Convert the player's action to lowercase
    action = [word.lower() for word in action]

    # Check if the action list is empty
    if action:
    
        # Check if the player wants to move
        if action[0] == "go":
            # Call the move function to move the player
            player["location"] = move(action[1], pllocation, rooms, player)

            # Check if the player wants to get an item
        elif action[0] == "get":
            # Check if the player is trying to get an item
            if len(action) > 1:
                # Call the get_item function to get the item
                get_item(action[1], player, rooms)

            # If the player is not trying to get an item, tell the player
            else:
                status_output.append("Please specify an item to get.")
    
        # Check if the player wants to check their stats
        elif action[0] == "check" and action[1] == "stats":
            # Call the show_status function to show the player's stats
            show_status(player, rooms)
    
        # Check if the player wants to exit the game
        elif action[0] == "quit":
            # Change the player's location to exit
            player["location"] = "exit"
    
        # If the player's action is blank tell the player
        elif action[0] == "":
            status_output.append("Please enter a valid action.")
    
        # If the player's action is invalid, tell the player
        else:
            status_output.append("Invalid action.")

    # If the action list is empty, tell the player
    else:
        status_output.append("Please enter a valid action.")
        status_output.append("----------------------")

    # Return the new state of the player only if the player's location is not exit
    return {"player": player, "status_output": status_output}

# Define a function for moving the player
def move(direction, pllocation, rooms, player):
    status_output = session.get("status_output", [])

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
                status_output.append("You have defeated Divisio and saved the kingdom!")
                player["location"] = "exit"
                return 'exit'
            # If the player does not have all the items, tell the player they need to find all the items
            else:
                status_output.append("You need to find all the items to defeat Divisio.")
                player["location"] = "exit"
                return 'exit'
        
        # Update the player's location and show the player's status
        status_output.extend(show_status(player, rooms))

    # If the direction is not valid, tell the player
    else:
        status_output.append("You cannot go that way.")
    
    # Return the new location of the player
    return player["location"]

# Define a function for checking the player's stats
# Tell the player where they are and what items are in the room if any
# Tell the player what items are in their inventory, change formatting based on the number of items
def show_status(player, rooms):
    status_output = session.get("status_output", [])

    # Initialize the status output
    status_output = []

    # Tell the player where they are
    status_output.append("You are in the " + player["location"] + ".")

    # Tell the player what items are in their inventory, change formatting based on the number of items
    if len(player["inventory"]) == 0:
        status_output.append("Inventory: None")
    elif len(player["inventory"]) == 1:
        status_output.append("Inventory: " + player["inventory"][0].capitalize() + ".")
    elif len(player["inventory"]) > 1:
        status_output.append("Inventory: [", end="")
        for item in player["inventory"]:
            if item == player["inventory"][-1]:
                status_output.append(item.capitalize() + "].")
            else:
                status_output.append(item.capitalize() + ", ", end="")
        status_output.append("]")

    # Tell the player what items are in the room if any
    if "item" in rooms[player["location"]]:
        status_output.append("Items in the room: " + rooms[player["location"]]["item"])
        
    status_output.append("----------------------")

    session["status_output"] = status_output
    
# Define a function for getting an item
def get_item(item, player, rooms):
    status_output = session.get("status_output", [])
    # Check if the item is in the room ignoring case
    if item.capitalize() in rooms[player["location"]]["item"]:
        # Add the item to the player's inventory
        player["inventory"].append(item)

        # Remove the item from the rooms dictionary and tell the player they have added the item to their inventory, 
        # capitalizing the first letter of the item
        status_output
        del rooms[player["location"]]["item"]

    # If the item is not in the room, tell the player the item is not there
    else:
        status_output.append("That item is not in this room.")
    
    status_output.append("----------------------")

    session["status_output"] = status_output