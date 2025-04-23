# AI DIY Home Improvement Assistant 🏠

An intelligent web application that provides step-by-step guidance for home improvement projects using Google's Gemini AI. Get expert advice for your DIY projects anytime, anywhere!

## ✨ Features

- 🤖 **AI-Powered Assistance**
  - Natural language understanding
  - Detailed step-by-step instructions
  - Safety precautions and warnings
  - Material and tool requirements
  - Alternative methods and troubleshooting

- 🎨 **User Interface**
  - Clean, modern design
  - Dark/Light mode toggle
  - Responsive layout for all devices
  - Interactive chat interface
  - Clear navigation and footer

- 🔧 **Supported Projects**
  - Painting and decorating
  - Plumbing repairs
  - Flooring installation
  - Electrical work
  - Carpentry
  - Home maintenance
  - And much more!

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/diy-ai-assistant.git
cd diy-ai-assistant
```

2. Create a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
   - Create `.env` file in project root
   - Add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

### Running the Application

1. Start the Flask server:
```bash
python p1.py
```

2. Open your browser:
```
http://localhost:5000
```

## 📁 Project Structure

```
diy-ai-assistant/
├── templates/
│   ├── base.html      # Base template with navigation
│   ├── index.html     # Main chat interface
│   └── about.html     # About page
├── static/
│   └── logo.png       # Project logo
├── p1.py              # Main Flask application
├── requirements.txt   # Python dependencies
└── README.md         # Documentation
```

## 🔒 Security

- Never commit your `.env` file or API keys
- Keep sensitive information secure
- Use environment variables for configuration
- Regular security updates

## 🛠️ Troubleshooting

### Common Issues

1. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **API Key Issues**
   - Verify `.env` file exists
   - Check API key format
   - Ensure key has proper permissions

3. **Port Conflicts**
   - Change port in `p1.py` if 5000 is in use
   - Check for other running Flask applications

### Error Messages

- **"Database is locked"**: Wait a few seconds and try again
- **"API Key not found"**: Verify `.env` file configuration
- **"Module not found"**: Reinstall requirements

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add AmazingFeature'`
4. Push to branch: `git push origin feature/AmazingFeature`
5. Open Pull Request

## 📝 Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Follow the project's coding standards
- Document your changes

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Google Gemini AI Team
- Flask Framework Contributors
- Open Source Community
- All Project Contributors

## 🎯 Roadmap

- [ ] User authentication system
- [ ] Project saving functionality
- [ ] Image recognition for DIY problems
- [ ] Mobile app development
- [ ] Voice input support
- [ ] Multi-language support
- [ ] Community forum integration

## 📞 Support

For support, please:
1. Check [existing issues](https://github.com/yourusername/diy-ai-assistant/issues)
2. Create a new issue with detailed information
3. Contact the maintainers

## 📧 Contact

Project Maintainer: [Your Name]
- Email: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername)
- Twitter: [@yourusername](https://twitter.com/yourusername)

---

Made with ❤️ by [Your Name/Organization] 