from flask import Flask, render_template, request, jsonify, session
import random
import os
from dotenv import load_dotenv
import google.generativeai as genai
import traceback

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session

# Ensure templates directory exists
if not os.path.exists('templates'):
    os.makedirs('templates')

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

def is_diy_related(query):
    """Check if the query is related to DIY home improvement."""
    diy_keywords = [
        'paint', 'plumb', 'pipe', 'leak', 'faucet', 'floor', 'tile', 'wood',
        'electric', 'wire', 'outlet', 'light', 'wall', 'ceiling', 'roof',
        'door', 'window', 'cabinet', 'kitchen', 'bathroom', 'repair', 'fix',
        'install', 'build', 'renovate', 'remodel', 'diy', 'home improvement',
        'tool', 'drill', 'saw', 'hammer', 'nail', 'screw', 'measure'
    ]
    
    return any(keyword in query.lower() for keyword in diy_keywords)

def get_gemini_response(prompt):
    """Get response from Gemini API using the official client library."""
    try:
        print(f"Sending to Gemini: {prompt}")  # Debug log
        
        # Add DIY context to the prompt
        diy_context = "You are a helpful assistant with expertise in DIY home improvement. While you specialize in home improvement topics, you can also answer other questions."
        
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

@app.route('/')
def home():
    # Initialize chat history in session if it doesn't exist
    if 'chat_history' not in session:
        session['chat_history'] = []
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json.get('message', '')
    print(f"Received message: {user_message}")  # Debug log
    
    # Get chat history from session
    chat_history = session.get('chat_history', [])
    
    # Add user message to history
    chat_history.append({"role": "user", "content": user_message})
    
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
        chat_history.append({"role": "assistant", "content": response})
        
        # Update session with new chat history
        session['chat_history'] = chat_history
        
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error in get_response route: {str(e)}")
        print(traceback.format_exc())  # Print full traceback
        
        # Fall back to our basic response system if Gemini fails
        print("Falling back to basic responses")  # Debug log
        if 'paint' in user_message.lower():
            response = random.choice(diy_responses['painting'])
        elif any(word in user_message.lower() for word in ['plumb', 'pipe', 'leak', 'faucet']):
            response = random.choice(diy_responses['plumbing'])
        elif any(word in user_message.lower() for word in ['floor', 'tile', 'wood']):
            response = random.choice(diy_responses['flooring'])
        elif any(word in user_message.lower() for word in ['electric', 'wire', 'outlet', 'light']):
            response = random.choice(diy_responses['electrical'])
        else:
            response = random.choice(diy_responses['default'])
        
        # Add bot response to history even for fallback responses
        chat_history.append({"role": "assistant", "content": response})
        session['chat_history'] = chat_history
        
        return jsonify({'response': response})

@app.route('/clear_history', methods=['POST'])
def clear_history():
    session['chat_history'] = []
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    print("Starting Flask server...")  # Debug log
    app.run(debug=True)
