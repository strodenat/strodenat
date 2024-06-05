from flask import Flask, request, session, jsonify
from game.textbasedgame import initialize_game, process_input

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    if 'player' not in session:
        initialize_game()
    return render_template('index.html', intro=session['rooms'][session['player']['location']]['description'])

@app.route('/game', methods=['POST'])
def game():
    user_input = request.form.get('input')
    response = process_input(user_input)
    return jsonify({'output': response})

if __name__ == '__main__':
    app.run(debug=True)