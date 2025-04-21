import sqlite3
import os

def init_db():
    # Remove existing database if it exists
    if os.path.exists('diy_projects.db'):
        os.remove('diy_projects.db')
        print("Removed existing database")

    # Create new database
    conn = sqlite3.connect('diy_projects.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL)''')
    
    # Create projects table
    c.execute('''CREATE TABLE IF NOT EXISTS projects
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  title TEXT NOT NULL,
                  description TEXT,
                  status TEXT DEFAULT 'in_progress',
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    # Create project steps table
    c.execute('''CREATE TABLE IF NOT EXISTS project_steps
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  project_id INTEGER,
                  step_number INTEGER,
                  description TEXT,
                  status TEXT DEFAULT 'pending',
                  FOREIGN KEY (project_id) REFERENCES projects (id))''')
    
    # Create materials table
    c.execute('''CREATE TABLE IF NOT EXISTS materials
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  project_id INTEGER,
                  name TEXT NOT NULL,
                  quantity TEXT,
                  status TEXT DEFAULT 'needed',
                  FOREIGN KEY (project_id) REFERENCES projects (id))''')
    
    # Create test user
    from werkzeug.security import generate_password_hash
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)',
             ('test', generate_password_hash('test123')))
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_db() 