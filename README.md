# DIY AI Assistant

A modern, interactive AI-powered assistant for DIY home improvement projects. This web application helps users with their home improvement questions, providing detailed guidance, safety tips, and professional recommendations.

## Features

- 🤖 AI-powered DIY assistance using Google's Gemini API
- 💬 Interactive chat interface with real-time responses
- 🎨 Beautiful UI with Vanta.js background animations
- 🌓 Dark/Light theme support
- 📱 Responsive design for all devices
- 🔒 Secure API key handling
- 💾 Chat history persistence
- 🎯 Focused responses for DIY topics

## Technologies Used

- **Backend:**
  - Python
  - Flask
  - Google Gemini API

- **Frontend:**
  - HTML5
  - CSS3
  - JavaScript
  - Vanta.js for background effects
  - Font Awesome for icons

## Prerequisites

Before running this project, make sure you have:

1. Python 3.8 or higher installed
2. Google Gemini API key
3. Modern web browser with JavaScript enabled

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/diy-ai-assistant.git
cd diy-ai-assistant
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
```bash
# On Windows
set GEMINI_API_KEY=your_api_key_here

# On macOS/Linux
export GEMINI_API_KEY=your_api_key_here
```

## Running the Application

1. Start the Flask server:
```bash
python p1.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

1. Visit the website
2. Type your DIY home improvement question in the chat input
3. Receive detailed responses including:
   - Step-by-step instructions
   - Required materials and tools
   - Safety tips
   - Professional recommendations
   - Alternative methods

## Features in Detail

### Chat Interface
- Real-time message updates
- Message history persistence
- Clear formatting for instructions and tips
- Timestamp for each message

### Theme Support
- Light and dark mode
- Smooth transitions
- Persistent theme preference
- Adaptive UI elements

### Responsive Design
- Mobile-friendly interface
- Adaptive layout for all screen sizes
- Touch-friendly controls
- Optimized performance

## Security

- API keys are stored as environment variables
- Input validation and sanitization
- Secure session handling
- Protected routes and endpoints

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Google Gemini API for AI capabilities
- Vanta.js for beautiful background effects
- Font Awesome for icons
- Flask community for the excellent web framework

## Support

For support, please open an issue in the GitHub repository or contact us through the website's contact form.

## Future Enhancements

- Voice input/output support
- Image recognition for project assistance
- Project cost estimation
- Integration with home improvement stores
- Community features and project sharing
- Augmented reality visualization

---

Made with ❤️ by [Your Name] 