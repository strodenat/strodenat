from flask import Flask, request, jsonify, render_template
from game.textbasedgame import process_input, initialize_game

app = Flask(__name__)

# Initialize game state
initialize_game()

@app.route('/')
def index():
    return render_template('index.html', intro="Welcome to the game! Enter your commands below.")

@app.route('/game', methods=['POST'])
def game():
    user_input = request.get_json().get('input', '')
    if not user_input:
        return jsonify({"response": "Please enter a valid command."})

    response = process_input(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)