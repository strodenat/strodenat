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
    return render_template('index.html', intro = "Welcome to the game!")

# Define the game route
# This route processes the player's input and returns the response
@app.route('/game', methods=['POST']) # Only allow POST requests
def game():
    user_input = request.json.get('input')
    action = user_input.split()

    player = session['player']
    rooms = session['rooms']

    # Process the input and update the player's state
    new_state = get_new_state(action, player["location"], rooms, player)
    session['player'] = new_state["player"]

    response = {
        'location': new_state['player']['location'],
        'inventory': new_state['player']['inventory'],
        'status': new_state['status_output']
    }

    return jsonify(response) # Return the response as JSON

if __name__ == '__main__':
    app.run(debug=True)