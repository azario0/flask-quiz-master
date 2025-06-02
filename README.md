# Flask Quiz Master

A dynamic web-based quiz application built with Flask that fetches questions from QuizAPI.io and provides an interactive quiz experience with score tracking and answer review.

## Features

- 🎯 Dynamic question fetching from QuizAPI.io
- 🔀 Randomized question order for engaging experience
- 📊 Real-time score tracking
- 📝 Comprehensive answer review after completion
- 🎨 Clean, responsive web interface
- 🔄 Easy quiz restart functionality
- ⚡ Session-based state management

## Prerequisites

- Python 3.7+
- Flask
- Requests library
- QuizAPI.io API key (free tier available)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/azario0/flask-quiz-master.git
   cd flask-quiz-master
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask requests
   ```

4. **Get your API key**
   - Visit [QuizAPI.io](https://quizapi.io/)
   - Sign up for a free account
   - Get your API key from the dashboard

5. **Configure the application**
   - Open `app.py`
   - Replace `"YOUR_API_KEY"` with your actual QuizAPI.io API key:
     ```python
     API_KEY = "your_actual_api_key_here"
     ```

## Usage

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Open your browser**
   Navigate to `http://localhost:5000`

3. **Take the quiz**
   - Click "Start Quiz" on the homepage
   - Answer the questions one by one
   - View your final score and review your answers

## Project Structure

```
quiz_app/
├── app.py              # Main Flask application
├── templates/          # HTML templates
│   ├── layout.html     # Base template with common structure
│   ├── index.html      # Homepage/welcome page
│   ├── question.html   # Quiz question display
│   └── score.html      # Results and answer review
├── static/
│   └── css/
│       └── style.css   # Application styles
└── README.md
```

## Configuration Options

You can customize the quiz behavior by modifying these variables in `app.py`:

```python
NUMBER_OF_QUESTIONS = 5  # Number of questions per quiz
```

The `fetch_questions()` function also supports additional parameters:
- `category`: Filter questions by category
- `difficulty`: Set difficulty level (Easy, Medium, Hard)
- `tags`: Filter by specific topics

## API Integration

This application uses [QuizAPI.io](https://quizapi.io/) to fetch quiz questions. The API provides:
- Multiple choice questions
- Various categories and difficulty levels
- Detailed explanations for answers
- Free tier with generous limits

## Features in Detail

### Question Validation
- Filters out malformed questions
- Ensures all questions have valid answers
- Handles API errors gracefully

### Session Management
- Secure session handling with random secret keys
- Persistent quiz state across page refreshes
- Automatic session cleanup

### Answer Review
- Shows all questions with user answers
- Highlights correct vs incorrect responses
- Includes explanations when available

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Potential Enhancements

- [ ] User authentication and persistent scoring
- [ ] Multiple quiz categories selection
- [ ] Difficulty level selection
- [ ] Timer functionality
- [ ] Leaderboard system
- [ ] Question bookmarking
- [ ] Social sharing of results

## Troubleshooting

### Common Issues

**API Key Error**
- Ensure your API key is correctly set in `app.py`
- Check that your QuizAPI.io account is active

**No Questions Fetched**
- Verify your internet connection
- Check QuizAPI.io service status
- Ensure you haven't exceeded API rate limits

**Session Issues**
- Clear your browser cookies
- Restart the Flask application

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [QuizAPI.io](https://quizapi.io/) for providing the quiz questions API
- Flask community for the excellent web framework
- Contributors and testers

## Author

**azario0**
- GitHub: [@azario0](https://github.com/azario0)

---

⭐ If you found this project helpful, please give it a star on GitHub!