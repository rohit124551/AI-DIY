from flask import Flask, render_template, request, jsonify, session, send_from_directory
import random
import os
from dotenv import load_dotenv
import google.generativeai as genai
import traceback  # Added for better error tracking
import json
from datetime import datetime
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from contextlib import contextmanager
import psycopg2
from psycopg2.extras import RealDictCursor

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session

# Ensure templates directory exists
if not os.path.exists('templates'):
    os.makedirs('templates')

# Database configuration
def get_db_config():
    if os.getenv('DATABASE_URL'):  # Production (Render)
        return {
            'db_type': 'postgres',
            'connection_string': os.getenv('DATABASE_URL')
        }
    else:  # Development (SQLite)
        return {
            'db_type': 'sqlite',
            'connection_string': 'diy_projects.db'
        }

@contextmanager
def get_db_connection():
    config = get_db_config()
    if config['db_type'] == 'postgres':
        conn = psycopg2.connect(config['connection_string'], cursor_factory=RealDictCursor)
    else:
        conn = sqlite3.connect(config['connection_string'], timeout=30)
        conn.row_factory = sqlite3.Row
    
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        if get_db_config()['db_type'] == 'postgres':
            # PostgreSQL tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT DEFAULT 'in_progress',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS project_steps (
                    id SERIAL PRIMARY KEY,
                    project_id INTEGER REFERENCES projects(id),
                    step_number INTEGER,
                    description TEXT,
                    status TEXT DEFAULT 'pending'
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS materials (
                    id SERIAL PRIMARY KEY,
                    project_id INTEGER REFERENCES projects(id),
                    name TEXT NOT NULL,
                    quantity TEXT,
                    status TEXT DEFAULT 'needed'
                )
            ''')
        else:
            # SQLite tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT DEFAULT 'in_progress',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS project_steps (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    step_number INTEGER,
                    description TEXT,
                    status TEXT DEFAULT 'pending',
                    FOREIGN KEY (project_id) REFERENCES projects (id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS materials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    name TEXT NOT NULL,
                    quantity TEXT,
                    status TEXT DEFAULT 'needed',
                    FOREIGN KEY (project_id) REFERENCES projects (id)
                )
            ''')
        
        conn.commit()

# Initialize database
init_db()

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
    # Commenting out the constraint check - will always return True
    # diy_keywords = [
    #     'paint', 'plumb', 'pipe', 'leak', 'faucet', 'floor', 'tile', 'wood',
    #     'electric', 'wire', 'outlet', 'light', 'wall', 'ceiling', 'roof',
    #     'door', 'window', 'cabinet', 'kitchen', 'bathroom', 'repair', 'fix',
    #     'install', 'build', 'renovate', 'remodel', 'diy', 'home improvement',
    #     'tool', 'drill', 'saw', 'hammer', 'nail', 'screw', 'measure'
    # ]
    
    # return any(keyword in query.lower() for keyword in diy_keywords)
    return True  # Always return True to bypass the constraint

def get_gemini_response(prompt):
    """Get response from Gemini API using the official client library."""
    try:
        print(f"Sending to Gemini: {prompt}")  # Debug log
        
        # Add DIY context to the prompt but make it less restrictive
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

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                         (username, generate_password_hash(password)))
            conn.commit()
            return jsonify({'message': 'User registered successfully'}), 201
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Username already exists'}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, password FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
    
    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['id']
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/projects', methods=['POST'])
def create_project():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    title = data.get('title')
    description = data.get('description')
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('INSERT INTO projects (user_id, title, description) VALUES (?, ?, ?)',
                     (session['user_id'], title, description))
        project_id = cursor.lastrowid
        
        # Generate project steps using Gemini
        try:
            prompt = f"Generate detailed steps for this DIY project: {title}. Description: {description}"
            response = get_gemini_response(prompt)
            steps = response.split('\n')
            
            for i, step in enumerate(steps, 1):
                cursor.execute('INSERT INTO project_steps (project_id, step_number, description) VALUES (?, ?, ?)',
                             (project_id, i, step.strip()))
            
            # Generate materials list
            materials_prompt = f"List all materials and tools needed for this DIY project: {title}. Description: {description}"
            materials_response = get_gemini_response(materials_prompt)
            materials = materials_response.split('\n')
            
            for material in materials:
                if material.strip():
                    cursor.execute('INSERT INTO materials (project_id, name) VALUES (?, ?)',
                                 (project_id, material.strip()))
        
        except Exception as e:
            print(f"Error generating project details: {str(e)}")
        
        conn.commit()
    
    return jsonify({'message': 'Project created successfully', 'project_id': project_id}), 201

@app.route('/api/projects', methods=['GET'])
def get_projects():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''SELECT p.id, p.title, p.description, p.status, p.created_at,
                            COUNT(ps.id) as total_steps,
                            SUM(CASE WHEN ps.status = 'completed' THEN 1 ELSE 0 END) as completed_steps
                     FROM projects p
                     LEFT JOIN project_steps ps ON p.id = ps.project_id
                     WHERE p.user_id = ?
                     GROUP BY p.id''', (session['user_id'],))
        
        projects = []
        for row in cursor.fetchall():
            projects.append({
                'id': row['id'],
                'title': row['title'],
                'description': row['description'],
                'status': row['status'],
                'created_at': row['created_at'],
                'progress': f"{row['completed_steps']}/{row['total_steps']}" if row['total_steps'] else "0/0"
            })
    
    return jsonify(projects), 200

@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project_details(project_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Get project details
        cursor.execute('''SELECT title, description, status, created_at
                         FROM projects
                         WHERE id = ? AND user_id = ?''', (project_id, session['user_id']))
        project = cursor.fetchone()
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        # Get project steps
        cursor.execute('''SELECT id, step_number, description, status
                         FROM project_steps
                         WHERE project_id = ?
                         ORDER BY step_number''', (project_id,))
        steps = [{'id': row['id'], 'step_number': row['step_number'], 'description': row['description'], 'status': row['status']}
                 for row in cursor.fetchall()]
        
        # Get materials list
        cursor.execute('''SELECT id, name, quantity, status
                         FROM materials
                         WHERE project_id = ?''', (project_id,))
        materials = [{'id': row['id'], 'name': row['name'], 'quantity': row['quantity'], 'status': row['status']}
                    for row in cursor.fetchall()]
    
    return jsonify({
        'title': project['title'],
        'description': project['description'],
        'status': project['status'],
        'created_at': project['created_at'],
        'steps': steps,
        'materials': materials
    }), 200

@app.route('/api/projects/<int:project_id>/steps/<int:step_id>', methods=['PUT'])
def update_step_status(project_id, step_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    status = data.get('status')
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''UPDATE project_steps
                         SET status = ?
                         WHERE id = ? AND project_id IN
                         (SELECT id FROM projects WHERE id = ? AND user_id = ?)''',
                         (status, step_id, project_id, session['user_id']))
        
        conn.commit()
    
    return jsonify({'message': 'Step status updated successfully'}), 200

@app.route('/api/projects/<int:project_id>/materials/<int:material_id>', methods=['PUT'])
def update_material_status(project_id, material_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    status = data.get('status')
    quantity = data.get('quantity')
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''UPDATE materials
                         SET status = ?, quantity = ?
                         WHERE id = ? AND project_id IN
                         (SELECT id FROM projects WHERE id = ? AND user_id = ?)''',
                         (status, quantity, material_id, project_id, session['user_id']))
        
        conn.commit()
    
    return jsonify({'message': 'Material status updated successfully'}), 200

if __name__ == '__main__':
    print("Starting Flask server...")  # Debug log
    app.run(debug=True)
