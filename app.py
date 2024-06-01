import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add the directory containing TextBasedGame.py to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from TextBasedGame import process_input, game_intro

app = Flask(__name__)
CORS(app)  # Enable CORS

@app.route('/game', methods=['POST'])
def game():
    input_data = request.form.get('input')
    print(f"Received input: {input_data}")  # Debugging: log the received input
    if input_data:
        response = process_input(input_data)
        print(f"Response: {response}")  # Debugging: log the response
        return jsonify(output=response)
    else:
        print("No input received")
        return jsonify(output="No input received"), 400

@app.route('/game_intro', methods=['GET'])
def game_intro_route():
    intro_text = game_intro()
    return jsonify(output=intro_text)

if __name__ == '__main__':
    app.run(port=4567)