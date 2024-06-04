from flask import Flask, render_template, request, jsonify, session
from game.textbasedgame import initialize_game, process_input, game_intro
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'

logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    initialize_game()
    return render_template('index.html', intro=game_intro())

@app.route('/game', methods=['POST'])
def game():
    user_input = request.form.get('input')
    logging.info(f"User input: {user_input}")
    response = process_input(user_input)
    logging.info(f"Response: {response}")
    return jsonify({'output': response})

if __name__ == '__main__':
    app.run(debug=True)