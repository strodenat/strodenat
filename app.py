# app.py

from flask import Flask, render_template, request, jsonify
from textbasedgame import process_input, game_intro

app = Flask(__name__)

@app.route('/')
def index():
    intro = game_intro()
    return render_template('index.html', intro=intro)

@app.route('/game', methods=['POST'])
def game():
    user_input = request.form['input']
    response = process_input(user_input)
    return jsonify({'output': response})

if __name__ == '__main__':
    app.run(debug=True)