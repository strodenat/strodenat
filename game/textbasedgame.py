# Description: This is a text based game that will be played in the terminal.
# Author: Nathaniel Strode

# The Pale Palace is a game where the player must navigate through the palace,
# Find all 6 items, and defeat Divisio to save the kingdom.
# The player can move through the palace by going North, South, East, or West.
# The player can add items to their inventory by getting the item in the room.
# The player can check their status
# The player can quit the game at any time. 
# The game ends when the player's locaton is set to the room 'exit'.

# Define the main function
def main():

    # Define a dictonary for the player's stats and inventory
    player = {
        "name":'',
        "inventory": [],
        "location": 'Hall of Acceptance', 
    }

    # Define a dictionary for the rooms in the palace conataining the valid directions and items
    rooms = {   "Hall of Acceptance": {"north": 'Garden of Whispers', "south": 'Vault of Visions',
                                       "east": 'Gallery of Shadows', "west": 'Diplomatic Den'},
                "Diplomatic Den": {"east": 'Hall of Acceptance',"item": ["Necklace"]},
                "Garden of Whispers": {"south": 'Hall of Acceptance', "east": 'Beacon Tower', "item": ["Potion"]},
                "Beacon Tower": {"west": 'Garden of Whispers', "item": ["Key"]},
                "Gallery of Shadows": {"north": 'Archives of Unity', "west": 'Hall of Acceptance', "item": ["Ring"]},
                "Archives of Unity": {"south": 'Gallery of Shadows', "item": ["Orb"]},
                "Vault of Visions": {"north": 'Hall of Acceptance', "east": 'Hall of Illusions', "item": ["Sword"]},
                "Hall of Illusions": {"west": 'Vault of Visions',}
    }
    # Welcome the player to the game
    print("Welcome to The Pale Palace.")
    print("You are Kalambia's final hope to save the kingdom from the evil sorcerer, Divisio")
    print("You must navigate through the palace, find all 6 items, and defeat Divisio to save the kingdom.")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Move commands: 'go North', 'go South', 'go East', 'go West'")
    print("Add an item to inventory: get 'item name'")
    print("Check stats: 'check stats'")
    print("Exit game: 'quit'")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # Start the game loop
    while player["location"] != "exit":
        # Show the player's status
        show_status(player, rooms)

        # Ask the player what they would like to do
        action = input("What would you like to do? ")
        print("----------------------")

        # Call the get_new_state function to get the new state of the player
        player = get_new_state(action.split(), player["location"], rooms, player)


# Function definitions

# Define a function for getting the new state of the player
def get_new_state(action, pllocation, rooms, player):
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
                print("Please specify an item to get.")
    
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
            print("Please enter a valid action.")
    
        # If the player's action is invalid, tell the player
        else:
            print("Invalid action.")

    # If the action list is empty, tell the player
    else:
        print("Please enter a valid action.")
        print("----------------------")

    # Return the new state of the player only if the player's location is not exit
    return player

# Define a function for moving the player
def move(direction, pllocation, rooms,player):
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
                print("You have found and defeated Divisio. You have saved the kingdom of Kalambia.")
                player["location"] = "exit"
                return 'exit'
            # If the player does not have all the items, tell the player they need to find all the items
            else:
                print("You have been defeated by Divisio. You must find all the items to defeat him.")
                player["location"] = "exit"
                return 'exit'
        
        # Update the player's location and show the player's status
        show_status(player, rooms)

    # If the direction is not valid, tell the player
    else:
        print("You can't go that way.")
    
    # Return the new location of the player
    return player["location"]

# Define a function for checking the player's stats
# Tell the player where they are and what items are in the room if any
# Tell the player what items are in their inventory, change formatting based on the number of items
def show_status(player, rooms):
    # Tell the player where they are
    print("You are in the " + player["location"])

    # Tell the player what items are in their inventory, change formatting based on the number of items
    if len(player["inventory"]) == 0:
        print("Inventory: []")
    elif len(player["inventory"]) == 1:
        print("Inventory: [" + player["inventory"][0].capitalize() + "]")
    elif len(player["inventory"]) > 1:
        print("Inventory: [", end="")
        for item in player["inventory"]:
            if item == player["inventory"][-1]:
                print(item.capitalize(), end="")
            else:
                print(item.capitalize() + ", ", end="")
        print("]")

    # Tell the player what items are in the room if any
    if "item" in rooms[player["location"]]:
        print("Items in this room: " + rooms[player["location"]]["item"][0])
        
    print("----------------------")
    
# Define a function for getting an item
def get_item(item, player, rooms):

    # Check if the item is in the room ignoring case
    if item.capitalize() in rooms[player["location"]]["item"]:
        # Add the item to the player's inventory
        player["inventory"].append(item)

        # Remove the item from the rooms dictionary and tell the player they have added the item to their inventory, 
        # capitalizing the first letter of the item
        print("You have added a " + item.capitalize() + " to your inventory.")
        del rooms[player["location"]]["item"]

    # If the item is not in the room, tell the player the item is not there
    else:
        print("That item is not in this room.")
    
    print("----------------------")

# Call the main function
main()