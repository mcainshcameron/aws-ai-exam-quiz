# AWS AI Exam Quiz

An interactive quiz application for AWS AI certification exam preparation.

## Features

- Multiple player support with individual score tracking
- Real-time streak tracking (current and best streaks)
- Question types clearly labeled (REAL, PRACTICE)
- AI-powered explanations using OpenAI's GPT-4
- Interactive UI with immediate feedback
- Support for both single and multiple-choice questions
- Comprehensive question bank with 383 AWS AI exam questions

## Setup

1. Clone the repository
2. Create a Python virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4-0125-preview
```

5. Run the application:
```bash
python app.py
```

6. Open http://localhost:5000 in your browser

## Usage

1. Select a player to start the quiz
2. Read the question and select your answer(s)
3. Click "Submit Answer" to check your response
4. View the correct answer and your current streak
5. Click "Explain" to get an AI-powered explanation of the answer
6. Click "Next Question" to continue

## Features in Detail

### Player System
- Individual tracking for multiple players
- Current streak tracking
- Best streak leaderboard

### Question Types
- REAL: Questions from actual AWS exams
- PRACTICE: Practice questions for exam preparation

### AI Explanations
- Detailed explanations provided by GPT-4
- Includes:
  - Why the correct answer is right
  - Why other options are incorrect
  - AWS terminology and concepts
  - Best practices and tips
  - Real-world examples

### UI Features
- Clean, intuitive interface
- Clear feedback on correct/incorrect answers
- Easy navigation between questions
- Responsive design

## Technical Stack

- Backend: Python/Flask
- Frontend: HTML, CSS, JavaScript
- AI: OpenAI GPT-4
- Database: JSON-based storage for questions and streaks

## Contributing

Feel free to submit issues and enhancement requests!
