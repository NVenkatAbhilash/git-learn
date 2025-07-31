# Flask API Development Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Setup and Installation](#setup-and-installation)
3. [Creating a Basic Flask API](#creating-a-basic-flask-api)
4. [Handling GET Requests](#handling-get-requests)
5. [Handling POST Requests](#handling-post-requests)
6. [Request Parameters](#request-parameters)
7. [Response Formatting](#response-formatting)
8. [Error Handling](#error-handling)
9. [Authentication](#authentication)
10. [Testing Your API](#testing-your-api)
11. [Best Practices](#best-practices)
12. [Example Project](#example-project)

## Introduction

Flask is a lightweight WSGI web application framework in Python. It's designed to make getting started quick and easy, with the ability to scale up to complex applications. This guide focuses on building RESTful APIs with Flask, specifically handling GET and POST requests with parameters.

## Setup and Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Installation

```bash
# Install Flask
pip install flask

# For JSON responses and request parsing
pip install flask-restful

# For handling CORS (Cross-Origin Resource Sharing)
pip install flask-cors
```

### Project Structure

A basic Flask API project structure:

```
my_flask_api/
├── app.py          # Main application file
├── config.py       # Configuration settings
├── requirements.txt # Dependencies
├── models/         # Data models
├── routes/         # API endpoints
├── services/       # Business logic
├── utils/          # Helper functions
└── tests/          # Test cases
```

## Creating a Basic Flask API

### Minimal Example (app.py)

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify({'message': 'Hello, World!'})

if __name__ == '__main__':
    app.run(debug=True)
```

Run the application:

```bash
python app.py
```

Access the API at `http://127.0.0.1:8000/`

## Handling GET Requests

GET requests are used to retrieve data from the server.

### Simple GET Request

```python
from flask import Flask, jsonify

app = Flask(__name__)

# Sample data
books = [
    {'id': 1, 'title': 'Flask Web Development', 'author': 'Miguel Grinberg'},
    {'id': 2, 'title': 'Python Crash Course', 'author': 'Eric Matthes'}
]

@app.route('/api/books', methods=['GET'])
def get_books():
    return jsonify({'books': books})

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book:
        return jsonify({'book': book})
    return jsonify({'message': 'Book not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
```

### GET with Query Parameters

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
books = [
    {'id': 1, 'title': 'Flask Web Development', 'author': 'Miguel Grinberg', 'year': 2018},
    {'id': 2, 'title': 'Python Crash Course', 'author': 'Eric Matthes', 'year': 2019},
    {'id': 3, 'title': 'Learning Python', 'author': 'Mark Lutz', 'year': 2013}
]

@app.route('/api/books/search', methods=['GET'])
def search_books():
    # Get query parameters
    author = request.args.get('author')
    year = request.args.get('year')
    
    results = books
    
    # Filter by author if provided
    if author:
        results = [book for book in results if author.lower() in book['author'].lower()]
    
    # Filter by year if provided
    if year:
        try:
            year = int(year)
            results = [book for book in results if book['year'] == year]
        except ValueError:
            return jsonify({'error': 'Year must be a number'}), 400
    
    return jsonify({'results': results, 'count': len(results)})

if __name__ == '__main__':
    app.run(debug=True)
```

Example usage: `http://127.0.0.1:8000/api/books/search?author=Grinberg&year=2018`

## Handling POST Requests

POST requests are used to send data to the server to create or update resources.

### Simple POST Request

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
books = [
    {'id': 1, 'title': 'Flask Web Development', 'author': 'Miguel Grinberg'},
    {'id': 2, 'title': 'Python Crash Course', 'author': 'Eric Matthes'}
]

@app.route('/api/books', methods=['POST'])
def add_book():
    if not request.json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    # Extract data from request
    new_book = {
        'id': books[-1]['id'] + 1 if books else 1,
        'title': request.json.get('title', ''),
        'author': request.json.get('author', '')
    }
    
    # Validate required fields
    if not new_book['title'] or not new_book['author']:
        return jsonify({'error': 'Title and author are required'}), 400
    
    # Add to collection
    books.append(new_book)
    
    return jsonify({'book': new_book}), 201  # 201 Created status

if __name__ == '__main__':
    app.run(debug=True)
```

## Request Parameters

Flask provides several ways to access request parameters:

### URL Parameters

```python
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # user_id is automatically converted to an integer
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        return jsonify({'user': user})
    return jsonify({'message': 'User not found'}), 404
```

### Query Parameters

```python
@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('q', '')  # Default to empty string if not provided
    limit = request.args.get('limit', 10, type=int)  # Convert to int with default 10
    
    # Perform search with parameters
    results = perform_search(query, limit)
    
    return jsonify({'results': results})
```

### JSON Body Parameters

```python
@app.route('/api/items', methods=['POST'])
def create_item():
    # Ensure request has JSON content
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    # Access JSON data
    data = request.json
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    
    # Process data
    # ...
    
    return jsonify({'success': True}), 201
```

## Response Formatting

### JSON Responses

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'roles': ['user', 'admin'],
        'settings': {
            'notifications': True,
            'theme': 'dark'
        }
    }
    
    return jsonify(data)
```

### Custom Response with Status Codes

```python
@app.route('/api/resource', methods=['GET'])
def get_resource():
    # Resource not found
    return jsonify({'error': 'Resource not found'}), 404

@app.route('/api/unauthorized', methods=['GET'])
def unauthorized():
    # Unauthorized access
    return jsonify({'error': 'Unauthorized access'}), 401

@app.route('/api/created', methods=['POST'])
def create_resource():
    # Resource created successfully
    return jsonify({'message': 'Resource created'}), 201
```

## Testing Your API

### Using curl

```bash
# GET request
curl -X GET http://127.0.0.1:8000/api/books

# GET with query parameters
curl -X GET "http://127.0.0.1:8000/api/books/search?author=Grinberg"

# POST with JSON data
curl -X POST http://127.0.0.1:8000/api/books \
  -H "Content-Type: application/json" \
  -d '{"title":"New Book", "author":"John Doe"}'

# POST with form data
curl -X POST http://127.0.0.1:8000/api/register \
  -F "username=johndoe" \
  -F "email=john@example.com" \
  -F "password=secret"
```

### Using Python Requests

```python
import requests

# GET request
response = requests.get('http://127.0.0.1:8000/api/books')
print(response.json())

# GET with query parameters
params = {'author': 'Grinberg', 'year': 2018}
response = requests.get('http://127.0.0.1:8000/api/books/search', params=params)
print(response.json())

# POST with JSON data
data = {'title': 'New Book', 'author': 'John Doe'}
response = requests.post('http://127.0.0.1:8000/api/books', json=data)
print(response.json())

# POST with form data
data = {'username': 'johndoe', 'email': 'john@example.com', 'password': 'secret'}
response = requests.post('http://127.0.0.1:8000/api/register', data=data)
print(response.json())
```

## Best Practices

1. **Use Appropriate HTTP Methods**
   - GET: Retrieve resources
   - POST: Create resources
   - PUT: Update resources (replace)
   - PATCH: Update resources (partial)
   - DELETE: Remove resources

2. **Consistent Error Handling**
   - Use appropriate HTTP status codes
   - Provide meaningful error messages
   - Include error details when helpful

3. **Input Validation**
   - Validate all user inputs
   - Use type conversion for query parameters
   - Handle validation errors gracefully

4. **Security Considerations**
   - Use HTTPS in production
   - Implement proper authentication
   - Sanitize inputs to prevent injection attacks
   - Set appropriate CORS headers

5. **API Versioning**
   - Include version in URL path (e.g., `/api/v1/resource`)
   - Or use Accept header (`Accept: application/vnd.api.v1+json`)

6. **Rate Limiting**
   - Protect your API from abuse
   - Return 429 Too Many Requests when limit is exceeded
   - Include rate limit headers

7. **Documentation**
   - Document all endpoints
   - Include example requests and responses
   - Specify required and optional parameters

## Example Project

Here's a complete example of a Flask API with GET and POST endpoints:

```python
from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory database
tasks = [
    {'id': '1', 'title': 'Learn Flask', 'completed': False},
    {'id': '2', 'title': 'Build an API', 'completed': False}
]

# GET all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    # Get query parameters for filtering
    completed = request.args.get('completed')
    
    filtered_tasks = tasks
    
    # Filter by completion status if provided
    if completed is not None:
        completed = completed.lower() == 'true'
        filtered_tasks = [task for task in tasks if task['completed'] == completed]
    
    return jsonify({'tasks': filtered_tasks})

# GET a specific task
@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
        
    return jsonify({'task': task})

# POST a new task
@app.route('/api/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        return jsonify({'error': 'Title is required'}), 400
    
    new_task = {
        'id': str(uuid.uuid4()),  # Generate unique ID
        'title': request.json['title'],
        'completed': request.json.get('completed', False)
    }
    
    tasks.append(new_task)
    
    return jsonify({'task': new_task}), 201

# PUT (update) a task
@app.route('/api/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
        
    if not request.json:
        return jsonify({'error': 'No data provided'}), 400
        
    # Update task fields
    task['title'] = request.json.get('title', task['title'])
    task['completed'] = request.json.get('completed', task['completed'])
    
    return jsonify({'task': task})

# DELETE a task
@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    initial_count = len(tasks)
    
    tasks = [task for task in tasks if task['id'] != task_id]
    
    if len(tasks) == initial_count:
        return jsonify({'error': 'Task not found'}), 404
        
    return jsonify({'message': 'Task deleted'})

if __name__ == '__main__':
    app.run(debug=True)
```

To run this example:

1. Save the code to a file named `app.py`
2. Install the required packages: `pip install flask flask-cors`
3. Run the application: `python app.py`
4. Test the API using curl, Postman, or any API client

This example demonstrates a complete RESTful API with proper error handling, parameter processing, and response formatting.