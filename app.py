from flask import Flask, request, session, render_template
from game.textbasedgame import initialize_game, process_input

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    initialize_game()
    return render_template('index.html')

@app.route('/game', methods=['POST'])
def game():
    user_input = request.form.get('user_input')
    response = process_input(user_input)
    return response

if __name__ == '__main__':
    app.run(debug=True)