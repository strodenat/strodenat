from flask import Flask, render_template, request, jsonify
from TextBasedGame import process_input, initialize_game, game_intro

app = Flask(__name__)

# Initialize game state
player, rooms = initialize_game()

@app.route('/')
def index():
    intro = game_intro()
    return render_template('index.html', intro=intro)

@app.route('/game', methods=['POST'])
def game():
    global player, rooms
    input_data = request.form.get('input')
    response = process_input(input_data, player, rooms)
    return jsonify({'output': response})

if __name__ == "__main__":
    app.run(debug=True)