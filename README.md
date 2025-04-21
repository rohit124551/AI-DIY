# DIY Home Improvement AI Assistant

A Flask-based web application that provides AI-powered assistance for DIY home improvement projects using Google's Gemini AI.

## Features

- Interactive chat interface for DIY home improvement queries
- AI-powered responses using Google's Gemini API
- Support for various home improvement topics including:
  - Painting
  - Plumbing
  - Flooring
  - Electrical work
- User-friendly web interface
- Secure API key management

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- A Google Gemini API key

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-directory>
```

2. Create and activate a virtual environment (recommended):
```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
   - Create a `.env` file in the project root directory
   - Add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Running the Application

1. Make sure your virtual environment is activated

2. Start the Flask server:
```bash
python p1.py
```

3. Open your web browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
.
├── p1.py              # Main application file
├── requirements.txt   # Python dependencies
├── .env              # Environment variables (not in version control)
├── .gitignore        # Git ignore file
└── templates/        # HTML templates
    └── index.html    # Main web interface
```

## Security Notes

- The `.env` file is not tracked in version control for security reasons
- Never commit your API key to version control
- Keep your `.env` file secure and don't share it publicly

## Troubleshooting

1. If you get an error about missing dependencies:
   - Make sure you've activated your virtual environment
   - Run `pip install -r requirements.txt` again

2. If the application can't find your API key:
   - Verify that your `.env` file exists in the project root
   - Check that the `GEMINI_API_KEY` variable is set correctly

3. If the Flask server won't start:
   - Make sure no other application is using port 5000
   - Check that all dependencies are installed correctly

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemini AI for providing the AI capabilities
- Flask framework for the web application structure 