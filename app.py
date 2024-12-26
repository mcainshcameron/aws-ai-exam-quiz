from flask import Flask, jsonify, request, send_from_directory
import json
import os

app = Flask(__name__)

STREAKS_FILE = 'streaks.json'

# Initialize streaks file if it doesn't exist
if not os.path.exists(STREAKS_FILE):
    initial_streaks = {
        'Cameron': {'best_streak': 0, 'current_streak': 0},
        'Stefano': {'best_streak': 0, 'current_streak': 0},
        'Wissam': {'best_streak': 0, 'current_streak': 0},
        'Ludovico': {'best_streak': 0, 'current_streak': 0},
        'Luca': {'best_streak': 0, 'current_streak': 0},
        'Team AI': {'best_streak': 0, 'current_streak': 0}
    }
    with open(STREAKS_FILE, 'w') as f:
        json.dump(initial_streaks, f)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/questions')
def get_questions():
    with open('questions.json', 'r') as f:
        questions = json.load(f)
    return jsonify(questions)

@app.route('/styles.css')
def styles():
    return send_from_directory('.', 'styles.css')

@app.route('/script.js')
def script():
    return send_from_directory('.', 'script.js')

@app.route('/streaks')
def get_streaks():
    with open(STREAKS_FILE, 'r') as f:
        streaks = json.load(f)
    return jsonify(streaks)

@app.route('/update_streak', methods=['POST'])
def update_streak():
    data = request.json
    player = data['player']
    is_correct = data['correct']
    
    with open(STREAKS_FILE, 'r') as f:
        streaks = json.load(f)
    
    if is_correct:
        streaks[player]['current_streak'] += 1
        if streaks[player]['current_streak'] > streaks[player]['best_streak']:
            streaks[player]['best_streak'] = streaks[player]['current_streak']
    else:
        streaks[player]['current_streak'] = 0
    
    with open(STREAKS_FILE, 'w') as f:
        json.dump(streaks, f)
    
    return jsonify(streaks)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
