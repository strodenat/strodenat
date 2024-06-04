# textbasedgame.py

# Initialize player and rooms
player = {
    "name": '',
    "inventory": [0],  # The first element is the count of items
    "location": 'Hall of Acceptance',
}

rooms = {
    "Hall of Acceptance": {
        "north": 'Garden of Whispers',
        "south": 'Vault of Visions',
        "east": 'Gallery of Shadows',
        "west": 'Diplomatic Den',
    },
    "Diplomatic Den": {
        "east": 'Hall of Acceptance',
        "item": ["Necklace of Tenacity"]
    },
    "Garden of Whispers": {
        "south": 'Hall of Acceptance',
        "east": 'Beacon Tower',
        "item": ["Potion of Energy"]
    },
    "Beacon Tower": {
        "west": 'Garden of Whispers',
        "item": ["Archives of Unity Key"]
    },
    "Gallery of Shadows": {
        "north": 'Archives of Unity',
        "west": 'Hall of Acceptance',
        "item": ["Ring of Temporal Folding"]
    },
    "Archives of Unity": {
        "south": 'Gallery of Shadows',
        "item": ["Orb of Sudden Expansion"]
    },
    "Vault of Visions": {
        "north": 'Hall of Acceptance',
        "east": 'Hall of Illusions',
        "item": ["Sword of Liberation"]
    },
    "Hall of Illusions": {
        "west": 'Vault of Visions',
    }
}

is_alive = True

def process_input(input_data):
    global player, rooms, is_alive
    print(f"Processing input: {input_data}")
    if "go" in input_data:
        direction = input_data.split(" ")[1]  # Assumes the direction is the second word in the input
        return player_move(direction, player, rooms)
    elif "get" in input_data:
        item = input_data.split(" ", 1)[1]  # Assumes the item is the rest of the input after "get"
        print(f"Getting item: {item}")
        return get_item(item, player, rooms)
    elif "check inventory" in input_data:
        if player["inventory"][0] == 0:
            return "You have no items in your inventory."
        elif player["inventory"][0] == 1:
            return "You have a " + player["inventory"][1] + " in your inventory."
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

def player_move(direction, player, rooms):
    current_room = rooms[player["location"]]
    print(f"Current room: {current_room}")
    direction_lower = direction.lower()
    
    # Ensure direction key exists
    if direction_lower in current_room:
        new_room = current_room[direction_lower]
        player["location"] = new_room
        print(f"Moved to {new_room}")
        return f"You have moved to the {new_room}."
    
    print(f"Direction {direction} not found in room.")
    return "You cannot go that way."

def get_item(item, player, rooms):
    current_room = rooms[player["location"]]
    if "item" in current_room and item in current_room["item"]:
        player["inventory"].append(item)
        player["inventory"][0] += 1
        current_room["item"].remove(item)
        return "You have picked up the " + item + "."
    else:
        return "The " + item + " is not in this room."

def encounter_divisio(player):
    global is_alive
    if player["inventory"][0] == 6:
        is_alive = False
        return "You have defeated Divisio and saved the kingdom!\nYou have won the game!"
    else:
        is_alive = False
        return "Divisio has defeated you.\nYou have lost the game."

def game_intro():
    intro_text = (
        "Welcome to The Pale Palace.\n"
        "You are Kalambia's final hope to save the kingdom from the evil sorcerer, Divisio.\n"
        "You must navigate through the palace, find all 6 items, and defeat Divisio to save the kingdom.\n"
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
    )
    return intro_text

def main():
    global player, rooms, is_alive
    print(game_intro())
    player_name = input("What is your name? ")
    player["name"] = player_name
    print("Hello " + player["name"] + ". You are in the " + player["location"])
    while is_alive:
        player_input = input("What would you like to do? ")
        response = process_input(player_input)
        print(response)

if __name__ == "__main__":
    main()