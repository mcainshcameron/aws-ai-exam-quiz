let questions;
let currentQuestion;
let selectedOptions = [];
let currentPlayer = '';
let streaks = {};

// Fetch initial streaks
fetch('/streaks')
    .then(response => response.json())
    .then(data => {
        streaks = data;
        if (currentPlayer) {
            updateLeaderboard();
        }
    });

// Fetch questions from server
fetch('/questions')
    .then(response => response.json())
    .then(data => {
        questions = data.questions;
    })
    .catch(error => {
        console.error('Error loading questions:', error);
        document.getElementById('question-text').textContent = 'Error loading questions. Please try again later.';
    });

// Initialize player selection
document.querySelectorAll('.player-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        currentPlayer = btn.dataset.player;
        document.getElementById('player-select').style.display = 'none';
        document.getElementById('quiz-container').style.display = 'block';
        document.getElementById('current-player').textContent = currentPlayer;
        document.getElementById('score').textContent = streaks[currentPlayer].current_streak;
        updateLeaderboard();
        showRandomQuestion();
    });
});

function updateLeaderboard() {
    const leaderboardList = document.getElementById('leaderboard-list');
    leaderboardList.innerHTML = '';
    
    // Sort players by best streak
    const sortedPlayers = Object.entries(streaks)
        .sort(([,a], [,b]) => b.best_streak - a.best_streak);
    
    sortedPlayers.forEach(([player, data]) => {
        const item = document.createElement('div');
        item.className = `leaderboard-item${player === currentPlayer ? ' current' : ''}`;
        item.innerHTML = `
            <span>${player}</span>
            <span>Current: ${data.current_streak} | Best: ${data.best_streak}</span>
        `;
        leaderboardList.appendChild(item);
    });
}

function showRandomQuestion() {
    // Reset UI state
    document.getElementById('submit-btn').style.display = 'block';
    document.getElementById('next-btn').style.display = 'none';
    const resultDiv = document.getElementById('result');
    resultDiv.textContent = ' ';
    resultDiv.className = 'result';
    selectedOptions = [];

    // Get random question
    const randomIndex = Math.floor(Math.random() * questions.length);
    currentQuestion = questions[randomIndex];

    // Show question type badge
    const questionType = document.getElementById('question-type');
    questionType.textContent = currentQuestion.type;
    questionType.className = `question-type-badge ${currentQuestion.type.toLowerCase()}`;

    // Display question
    document.getElementById('question-text').textContent = currentQuestion.question;

    // Create options
    const optionsContainer = document.getElementById('options-container');
    optionsContainer.innerHTML = '';

    Object.entries(currentQuestion.options).forEach(([key, value]) => {
        const optionDiv = document.createElement('div');
        optionDiv.className = 'option';
        optionDiv.textContent = `${key}: ${value}`;
        optionDiv.addEventListener('click', () => toggleOption(optionDiv, key));
        optionsContainer.appendChild(optionDiv);
    });
}

function toggleOption(optionDiv, key) {
    // Handle single or multiple answers
    const isArray = Array.isArray(currentQuestion.correct_answer);
    
    if (!isArray) {
        // Single answer question
        document.querySelectorAll('.option').forEach(opt => opt.classList.remove('selected'));
        selectedOptions = [key];
        optionDiv.classList.add('selected');
    } else {
        // Multiple answer question
        optionDiv.classList.toggle('selected');
        const index = selectedOptions.indexOf(key);
        if (index === -1) {
            selectedOptions.push(key);
        } else {
            selectedOptions.splice(index, 1);
        }
    }
}

function checkAnswer() {
    const correctAnswer = currentQuestion.correct_answer;
    const resultDiv = document.getElementById('result');
    let isCorrect = false;

    if (Array.isArray(correctAnswer)) {
        // Multiple correct answers
        isCorrect = selectedOptions.length === correctAnswer.length &&
                   selectedOptions.every(option => correctAnswer.includes(option));
    } else {
        // Single correct answer
        isCorrect = selectedOptions[0] === correctAnswer;
    }

    // Update streak on server
    fetch('/update_streak', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            player: currentPlayer,
            correct: isCorrect
        })
    })
    .then(response => response.json())
    .then(data => {
        streaks = data;
        updateLeaderboard();
        document.getElementById('score').textContent = streaks[currentPlayer].current_streak;
    });

    // Show correct/incorrect answers
    document.querySelectorAll('.option').forEach(optionDiv => {
        const optionKey = optionDiv.textContent.split(':')[0].trim();
        
        if (Array.isArray(correctAnswer)) {
            if (correctAnswer.includes(optionKey)) {
                optionDiv.classList.add('correct');
            }
            if (selectedOptions.includes(optionKey) && !correctAnswer.includes(optionKey)) {
                optionDiv.classList.add('incorrect');
            }
        } else {
            if (optionKey === correctAnswer) {
                optionDiv.classList.add('correct');
            }
            if (optionKey === selectedOptions[0] && optionKey !== correctAnswer) {
                optionDiv.classList.add('incorrect');
            }
        }
    });

    // Show result message
    resultDiv.textContent = isCorrect ? 'Correct! ✓' : 'Incorrect! ✗';
    resultDiv.className = `result ${isCorrect ? 'correct' : 'incorrect'}`;

    // Show next button and hide submit button
    const submitBtn = document.getElementById('submit-btn');
    const nextBtn = document.getElementById('next-btn');
    
    submitBtn.style.display = 'none';
    nextBtn.style.display = 'block';
}

// Event Listeners
document.getElementById('submit-btn').addEventListener('click', () => {
    if (selectedOptions.length > 0) {
        checkAnswer();
    }
});

document.getElementById('next-btn').addEventListener('click', showRandomQuestion);
