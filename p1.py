from flask import Flask, render_template, request, jsonify, session
import random
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
import traceback
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session

# Ensure templates directory exists
if not os.path.exists('templates'):
    os.makedirs('templates')

# Ensure chat history directory exists
if not os.path.exists('chat_history'):
    os.makedirs('chat_history')

# Gemini API configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')  # Get API key from environment variable
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")
    
genai.configure(api_key=GEMINI_API_KEY)

# Sample DIY home improvement responses
diy_responses = {
    "painting": [
        "For painting walls, start by cleaning the surface and applying painter's tape to edges.",
        "Use a primer before applying paint for better coverage and durability.",
        "When painting, work from top to bottom and maintain a wet edge to avoid lap marks."
    ],
    "plumbing": [
        "Always turn off the water supply before starting any plumbing work.",
        "Use plumber's tape on threaded connections to prevent leaks.",
        "Keep a bucket handy when disconnecting pipes to catch residual water."
    ],
    "flooring": [
        "Acclimate wood flooring in your home for at least 72 hours before installation.",
        "Start laying tiles from the center of the room and work outward for the best appearance.",
        "Use spacers between tiles to ensure even grout lines."
    ],
    "electrical": [
        "Always turn off power at the breaker before working on electrical projects.",
        "Use a voltage tester to confirm power is off before touching any wires.",
        "Follow local electrical codes when installing new fixtures or outlets."
    ],
    "default": [
        "What DIY project are you working on? I can help with painting, plumbing, flooring, or electrical work.",
        "Try asking about specific home improvement tasks like wall painting or fixing a leaky faucet.",
        "I can provide step-by-step instructions for many home improvement projects. What are you interested in?"
    ]
}

# Load constraints from file
def load_constraints():
    try:
        with open('constraints.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Default constraints if file doesn't exist
        return {
            "max_steps": 5,
            "max_response_length": 500,
            "allowed_topics": [
                "painting", "plumbing", "flooring", "electrical",
                "carpentry", "gardening", "renovation", "repair",
                "maintenance", "installation", "decorating", "landscaping"
            ]
        }

constraints = load_constraints()

def is_topic_allowed(topic):
    """Check if the topic is in the allowed topics list."""
    return any(allowed_topic in topic.lower() for allowed_topic in constraints["allowed_topics"])

def get_gemini_response(prompt):
    """Get response from Gemini API using the official client library."""
    try:
        print(f"Sending to Gemini: {prompt}")  # Debug log
        
        # Simplified context without strict constraints
        diy_context = """You are a helpful DIY home improvement assistant. Provide detailed, practical advice for home improvement projects. 
        Include relevant information about materials, tools, steps, safety, and alternatives when appropriate.
        Feel free to provide as much detail as needed to help the user complete their project successfully."""
        
        full_prompt = f"{diy_context}\n\nUser question: {prompt}"
        
        # Create a model instance
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Generate content
        response = model.generate_content(full_prompt)
        
        # Return the text response
        print(f"Received from Gemini: {response.text[:100]}...")  # Debug log (first 100 chars)
        return response.text
    except Exception as e:
        print(f"Error with Gemini API: {str(e)}")
        print(traceback.format_exc())  # Print full traceback
        return f"Sorry, I couldn't process your request at the moment. Error: {str(e)}"

def save_chat_history(chat_history):
    """Save chat history to a JSON file."""
    try:
        filename = f"chat_history/chat_{datetime.now().strftime('%Y%m%d')}.json"
        with open(filename, 'w') as f:
            json.dump(chat_history, f)
    except Exception as e:
        print(f"Error saving chat history: {str(e)}")

def load_chat_history():
    """Load chat history from the most recent JSON file."""
    try:
        # Get the most recent chat history file
        files = [f for f in os.listdir('chat_history') if f.startswith('chat_') and f.endswith('.json')]
        if not files:
            return []
        
        latest_file = max(files)
        with open(f'chat_history/{latest_file}', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading chat history: {str(e)}")
        return []

@app.route('/')
def home():
    # Initialize chat history in session if it doesn't exist
    if 'chat_history' not in session:
        session['chat_history'] = load_chat_history()
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json.get('message', '')
    print(f"Received message: {user_message}")  # Debug log
    
    # Get chat history from session
    chat_history = session.get('chat_history', [])
    
    # Add user message to history
    chat_history.append({
        "role": "user",
        "content": user_message,
        "timestamp": datetime.now().isoformat()
    })
    
    # Try to get a response from Gemini API
    try:
        print("Calling Gemini API...")  # Debug log
        
        # Create context from chat history
        context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history[-5:]])  # Keep last 5 messages for context
        
        # Add context to the prompt
        prompt = f"Previous conversation:\n{context}\n\nUser question: {user_message}"
        
        response = get_gemini_response(prompt)
        print("Successfully got response from Gemini")  # Debug log
        
        # Add bot response to history
        chat_history.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Update session with new chat history
        session['chat_history'] = chat_history
        
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error in get_response route: {str(e)}")
        print(traceback.format_exc())  # Print full traceback
        
        # Fall back to our basic response system if Gemini fails
        print("Falling back to basic responses")  # Debug log
        response = "I'm here to help with your DIY home improvement questions. Please ask me anything about home improvement, and I'll do my best to provide helpful information."
        
        # Add bot response to history even for fallback responses
        chat_history.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Update session
        session['chat_history'] = chat_history
        
        return jsonify({'response': response})

@app.route('/clear_history', methods=['POST'])
def clear_history():
    session['chat_history'] = []
    # Also clear the chat history file
    try:
        filename = f"chat_history/chat_{datetime.now().strftime('%Y%m%d')}.json"
        if os.path.exists(filename):
            os.remove(filename)
    except Exception as e:
        print(f"Error clearing chat history file: {str(e)}")
    return jsonify({'status': 'success'})

@app.route('/get_chat_history', methods=['GET'])
def get_chat_history():
    """Get the current chat history."""
    return jsonify(session.get('chat_history', []))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    # Run the app on all available network interfaces
    app.run(host='0.0.0.0', port=port, debug=True)
