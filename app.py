import os
import json
import logging
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import openai
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, static_folder='.')
app.secret_key = 'aws-exam-secret-key-2024'  # Fixed secret key for sessions

# Load environment variables
load_dotenv()

# Initialize OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

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

# Password protection from environment variable
PASSWORD = os.getenv("APP_PASSWORD", "aws2024")  # Default password for development

from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        error = 'Invalid password'
    return render_template('login.html', error=error)

@app.route('/')
@login_required
def index():
    return app.send_static_file('index.html')

@app.route('/styles.css')
@login_required
def styles():
    return app.send_static_file('styles.css')

@app.route('/script.js')
@login_required
def scripts():
    return app.send_static_file('script.js')

@app.route('/questions')
@login_required
def get_questions():
    app.logger.debug('Loading questions from questions.json')
    file_path = 'questions.json'
    
    if not os.path.exists(file_path):
        app.logger.error(f'questions.json not found in path: {os.path.abspath(file_path)}')
        return jsonify({'error': 'Questions file not found'}), 404
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            questions = json.load(f)
            question_count = len(questions.get('questions', []))
            app.logger.debug(f'Successfully loaded {question_count} questions')
            return jsonify(questions)
    except json.JSONDecodeError as e:
        app.logger.error(f'Error decoding questions.json: {str(e)}')
        return jsonify({'error': 'Invalid JSON format in questions file'}), 500
    except Exception as e:
        app.logger.error(f'Unexpected error loading questions: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/streaks')
@login_required
def get_streaks():
    with open(STREAKS_FILE, 'r') as f:
        streaks = json.load(f)
    return jsonify(streaks)

@app.route('/update_streak', methods=['POST'])
@login_required
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

@app.route('/explain', methods=['POST'])
@login_required
def explain():
    data = request.json
    question = data['question']
    options = data['options']
    correct_answer = data['correct_answer']

    prompt = f"""
    You are an AWS Cloud Practitioner exam assistant. Please provide an accurate, clear, and detailed explanation of the following exam question. Format the response using markdown.

    Question: {question}

    Options:
    {' '.join(options)}

    Correct answer: {', '.join(correct_answer)}

    Your response should:
    1. **Explain clearly** why the correct answer is the best choice.
    2. **Briefly explain** why the other options are incorrect, focusing on key AWS concepts.
    3. Use **precise AWS terminology** and **real-world examples** where relevant.
    4. Provide **a helpful tip** for learning the key concept related to this question, including any **best practices** or important AWS services.
    5. Ensure the explanation is concise and easy to understand for someone preparing for the AWS Cloud Practitioner exam.
    6. Use markdown formatting, including headings, lists, and code blocks when appropriate.
    """

    try:
        response = openai.ChatCompletion.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": "You are a helpful assistant explaining AWS Cloud Practitioner exam questions. Provide detailed, yet concise explanations using markdown."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        explanation = response['choices'][0]['message']['content'].strip()
        return jsonify({'explanation': explanation})
    except Exception as e:
        app.logger.error(f"Error calling OpenAI API: {str(e)}")
        return jsonify({'error': 'Failed to generate explanation'}), 500

if __name__ == '__main__':
    app.run(debug=True)
