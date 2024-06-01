is_alive = True

def process_input(input_data):
    global player, rooms, is_alive
    if "go" in input_data:
        direction = input_data.split(" ")[1]  # Assumes the direction is the second word in the input
        return player_move(direction, player, rooms)
    elif "get" in input_data:
        item = input_data.split(" ")[1]  # Assumes the item is the second word in the input
        return get_item(item, player, rooms)
    elif "check inventory" in input_data:
        # Check if the player has any items in their inventory
        if player["inventory"][0] == 0:
            return "You have no items in your inventory."
        # If the player has 1 item in their inventory, tell them what it is in singular form
        elif player["inventory"][0] == 1:
            return "You have a " + player["inventory"][1] + " in your inventory."
        # If the player has more than 1 item in their inventory, tell them what they are in plural form and their inventory count
        else:
            inventory_list = "You have " + str(player["inventory"][0]) + " items in your inventory.\n"
            for i in range(1, len(player["inventory"])):
                inventory_list += player["inventory"][i] + "\n"
            return inventory_list
    elif "check map" in input_data:
        return "You are in the " + player["location"]
    elif "quit" in input_data:
        is_alive = False
        return "Game over."
    else:
        return "Unknown command: " + input_data

def main():
    global player, rooms, is_alive
    game_intro()
    player_name = input("What is your name? ")
    player["name"] = player_name
    print("Hello " + player["name"] + ". You are in the " + player["location"])
    while is_alive:
        player_input = input("What would you like to do? ")
        response = process_input(player_input)
        print(response)

def game_intro():
    intro_text = (
        "Welcome to The Pale Palace.\n"
        "You are Kalambia's final hope to save the kingdom from the evil sorcerer, Divisio.\n"
        "You must navigate through the palace, find all 6 items, and defeat Divisio to save the kingdom.\n"
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        "Move commands: go North, go South, go East, go West\n"
        "Add to inventory: get 'item name'\n"
        "Check inventory: check inventory\n"
        "Check stats: check stats\n"
        "Check location: check map\n"
        "Quit: quit"
    )
    return intro_text

def player_move(direction, player, rooms):
    if direction in rooms[player["location"]]:
        player["location"] = rooms[player["location"]][direction]
        response = "You have moved to the " + player["location"]
        if "item" in rooms[player["location"]]:
            response += "\nYou see a " + rooms[player["location"]]["item"][0] + " in this room."
        if player["location"] == "Hall of Illusions":
            response += "\n" + encounter_divisio(player)
        return response
    else:
        return "You cannot go that way."

def get_item(item, player, rooms):
    if item.lower() in rooms[player["location"]]["item"][0].lower():
        player["inventory"].append(item)
        player["inventory"][0] += 1
        del rooms[player["location"]]["item"]
        return "You have added a " + item.capitalize() + " to your inventory."
    else:
        return "That item is not in this room."

def encounter_divisio(player):
    global is_alive
    if player["inventory"][0] == 6:
        is_alive = False
        return "You have defeated Divisio and saved the kingdom!\nYou have won the game!"
    else:
        is_alive = False
        return "Divisio has defeated you.\nYou have lost the game."

# Initialize player and rooms
player = {
    "name": '',
    "inventory": [0],
    "location": 'Hall of Acceptance',
}

rooms = {
    "Hall of Acceptance": {
        "north": 'Garden of Whispers',
        "south": 'Vault of Visions',
        "east": 'Gallery of Shadows',
        "west": 'Diplomatic Den',
        player["location"]: 'Hall of Acceptance',
    },
    "Diplomatic Den": {
        "east": 'Hall of Acceptance',
        "item": ["Necklace"]
    },
    "Garden of Whispers": {
        "south": 'Hall of Acceptance',
        "east": 'Beacon Tower',
        "item": ["Potion"]
    },
    "Beacon Tower": {
        "west": 'Garden of Whispers',
        "item": ["Key"]
    },
    "Gallery of Shadows": {
        "north": 'Archives of Unity',
        "west": 'Hall of Acceptance',
        "item": ["Ring"]
    },
    "Archives of Unity": {
        "south": 'Gallery of Shadows',
        "item": ["Orb"]
    },
    "Vault of Visions": {
        "north": 'Hall of Acceptance',
        "east": 'Hall of Illusions',
        "item": ["Sword"]
    },
    "Hall of Illusions": {
        "west": 'Vault of Visions',
    }
}

if __name__ == "__main__":
    main()