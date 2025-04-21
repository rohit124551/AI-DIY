import requests
import json

BASE_URL = 'http://localhost:5000'

def test_login():
    print("\nTesting login...")
    response = requests.post(f'{BASE_URL}/api/login', 
                           json={'username': 'test', 'password': 'test123'})
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json().get('message') == 'Login successful'

def test_create_project():
    print("\nTesting project creation...")
    # First login to get session
    session = requests.Session()
    login_response = session.post(f'{BASE_URL}/api/login', 
                                json={'username': 'test', 'password': 'test123'})
    
    if login_response.json().get('message') != 'Login successful':
        print("Login failed, cannot create project")
        return False
    
    # Create a project
    project_data = {
        'title': 'Test Project',
        'description': 'This is a test project'
    }
    response = session.post(f'{BASE_URL}/api/projects', json=project_data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 201

def test_get_projects():
    print("\nTesting get projects...")
    # First login to get session
    session = requests.Session()
    login_response = session.post(f'{BASE_URL}/api/login', 
                                json={'username': 'test', 'password': 'test123'})
    
    if login_response.json().get('message') != 'Login successful':
        print("Login failed, cannot get projects")
        return False
    
    # Get projects
    response = session.get(f'{BASE_URL}/api/projects')
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

if __name__ == '__main__':
    print("Starting backend tests...")
    
    # Start the Flask server in a separate process
    import subprocess
    import time
    import sys
    
    # Start the Flask server
    flask_process = subprocess.Popen([sys.executable, 'p1.py'])
    
    # Wait for the server to start
    time.sleep(3)
    
    try:
        # Run tests
        login_success = test_login()
        print(f"Login test: {'Success' if login_success else 'Failed'}")
        
        create_project_success = test_create_project()
        print(f"Create project test: {'Success' if create_project_success else 'Failed'}")
        
        get_projects_success = test_get_projects()
        print(f"Get projects test: {'Success' if get_projects_success else 'Failed'}")
        
    finally:
        # Stop the Flask server
        flask_process.terminate()
        flask_process.wait() 