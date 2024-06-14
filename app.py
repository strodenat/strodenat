# Description: This file contains the Flask application that serves the game to the user.

# Import the necessary modules
from flask import Flask, request, session, jsonify, render_template
from game.textbasedgame import initialize_game, get_new_state

# Create the Flask application
app = Flask(__name__)
app.secret_key = 'e1b7db05f3024b1ba762a13fb7bc9d6e2f91d2d4e4c8476fb2d24c15b276fbf8'

# Define the routes:

@app.route('/')
# Define the index route
# This route initializes the game if the player is not in the session
def index():
    if 'player' not in session:
        initialize_game()
    return render_template('index.html')

# Define the game route
# This route processes the player's input and returns the response
@app.route('/game', methods=['POST']) # Only allow POST requests
def game():
    user_input = request.json.get('input')
    action = user_input.split()

    player = session['player']
    rooms = session['rooms']

    # Process the input and update the player's state
    new_player_state, status_output = get_new_state(action, player["location"], rooms, player)
    session['player'] = new_player_state

    response = {
        'location': new_player_state['location'],
        'inventory': new_player_state['inventory'],
        'status': status_output
    }

    return jsonify(response) # Return the response as JSON

if __name__ == '__main__':
    app.run(debug=True)