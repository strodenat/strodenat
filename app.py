from flask import Flask, render_template, request, jsonify
from TextBasedGame import process_input, game_intro

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game', methods=['POST'])
def game():
    user_input = request.form.get('user_input')
    response = process_input(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)