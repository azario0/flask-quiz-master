from flask import Flask, render_template, request, redirect, url_for, session
import requests
import os
import random

app = Flask(__name__)
# It's crucial to set a secret key for session management
app.secret_key = os.urandom(24) # Generates a random secret key

# --- Configuration ---
API_KEY = "YOUR_API_KEY" # YOUR ACTUAL API KEY
QUIZ_API_URL = "https://quizapi.io/api/v1/questions"
NUMBER_OF_QUESTIONS = 5 # How many questions to fetch for the quiz

# --- Helper Functions ---
def fetch_questions(limit=NUMBER_OF_QUESTIONS, category=None, difficulty=None, tags=None):
    """Fetches questions from the QuizAPI."""
    params = {
        "apiKey": API_KEY,
        "limit": limit
    }
    if category:
        params["category"] = category
    if difficulty:
        params["difficulty"] = difficulty
    if tags:
        params["tags"] = tags # e.g., "JavaScript,PHP"

    try:
        response = requests.get(QUIZ_API_URL, params=params)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        questions_data = response.json()
        # Filter out questions that might not have the answers in the expected format
        # or are missing essential fields.
        valid_questions = []
        for q in questions_data:
            if q.get("question") and isinstance(q.get("answers"), dict) and isinstance(q.get("correct_answers"), dict):
                # Ensure answers are not all null
                if any(val is not None for val in q["answers"].values()):
                     valid_questions.append(q)
        return valid_questions
    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")
        return None
    except ValueError as e: # Includes JSONDecodeError
        print(f"API JSON Decode Error: {e}")
        return None

def get_correct_answer_key(question_data):
    """
    Finds the key of the correct answer (e.g., 'answer_a', 'answer_b')
    from the 'correct_answers' dictionary.
    """
    for key, is_correct in question_data.get("correct_answers", {}).items():
        if is_correct == "true":
            # 'answer_a_correct' -> 'answer_a'
            return key.replace("_correct", "")
    return None # Should not happen if data is well-formed

# --- Routes ---
@app.route('/')
def index():
    """Homepage: Shows a welcome message and a button to start the quiz."""
    session.clear() # Clear any previous quiz data
    return render_template('index.html', num_questions=NUMBER_OF_QUESTIONS)

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    """
    Fetches questions from the API and initializes the quiz session.
    Redirects to the first question.
    """
    questions = fetch_questions(limit=NUMBER_OF_QUESTIONS)

    if not questions or len(questions) < NUMBER_OF_QUESTIONS:
        # Handle case where not enough questions are fetched
        # You might want to fetch more or show an error
        # For simplicity, we'll try to use what we got, or show an error
        if not questions:
             return render_template('index.html', error="Could not fetch questions from the API. Please try again later.", num_questions=NUMBER_OF_QUESTIONS)
        # If some questions were fetched, but less than requested:
        # You could decide to proceed or error out. Here we proceed if at least 1.
        if not questions:
             return render_template('index.html', error="No questions available for the quiz. Please try again later.", num_questions=NUMBER_OF_QUESTIONS)


    # Shuffle questions to make it more engaging if desired
    random.shuffle(questions)

    session['questions'] = questions
    session['current_question_index'] = 0
    session['score'] = 0
    session['user_answers'] = [] # To store user's answers and correctness for review

    return redirect(url_for('show_question'))

@app.route('/quiz', methods=['GET', 'POST'])
def show_question():
    """
    Displays the current question and handles answer submission.
    """
    if 'questions' not in session or not session['questions']:
        return redirect(url_for('index')) # Go back if no quiz started

    current_index = session.get('current_question_index', 0)
    questions = session['questions']

    if current_index >= len(questions):
        return redirect(url_for('show_score')) # All questions answered

    current_question_data = questions[current_index]

    if request.method == 'POST':
        user_answer_key = request.form.get('answer') # e.g., 'answer_a'
        correct_answer_key = get_correct_answer_key(current_question_data)

        is_correct = (user_answer_key == correct_answer_key)
        if is_correct:
            session['score'] += 1

        # Store answer for review
        session['user_answers'].append({
            "question_text": current_question_data["question"],
            "user_answer": current_question_data["answers"].get(user_answer_key, "Not answered"),
            "correct_answer_text": current_question_data["answers"].get(correct_answer_key, "N/A"),
            "is_correct": is_correct,
            "explanation": current_question_data.get("explanation")
        })
        session.modified = True # Important when modifying mutable session objects like lists/dicts


        session['current_question_index'] += 1
        session.modified = True
        return redirect(url_for('show_question')) # Go to next question or score page

    # Prepare answers for display (filter out null answers)
    # And provide keys like 'answer_a', 'answer_b' for the radio buttons
    answers_for_template = {
        key: value for key, value in current_question_data['answers'].items() if value is not None
    }

    return render_template('question.html',
                           question_data=current_question_data,
                           question_number=current_index + 1,
                           total_questions=len(questions),
                           answers=answers_for_template)

@app.route('/score')
def show_score():
    """Displays the final score and allows restarting the quiz."""
    if 'score' not in session or 'questions' not in session:
        return redirect(url_for('index')) # No score to show, redirect to start

    score = session.get('score', 0)
    total_questions = len(session.get('questions', []))
    user_answers_review = session.get('user_answers', [])

    # Optional: Clear session after showing score if you don't want users to go back
    # session.pop('questions', None)
    # session.pop('current_question_index', None)
    # session.pop('score', None)
    # session.pop('user_answers', None)

    return render_template('score.html',
                           score=score,
                           total_questions=total_questions,
                           user_answers_review=user_answers_review)

if __name__ == '__main__':
    app.run(debug=True)