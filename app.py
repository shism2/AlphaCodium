#!/usr/bin/env python3
"""
Web interface for the Gemini2Solver.
"""

import os
import logging
import toml
from flask import Flask, request, render_template, jsonify
from gemini2_solver import Gemini2Solver

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create the Flask app
app = Flask(__name__)

# Create the solver
solver = None

@app.route('/')
def index():
    """Render the index page."""
    return render_template('index.html')

@app.route('/api/solve', methods=['POST'])
def solve():
    """Solve a programming problem."""
    # Get the request data
    data = request.json
    
    # Extract the problem details
    problem = {
        "name": data.get("name", "Unknown"),
        "description": data.get("description", ""),
        "public_tests": data.get("public_tests", [])
    }
    
    # Get the API key
    api_key = data.get("api_key", "")
    
    # Update the API key if provided
    if api_key:
        update_api_key(api_key)
    
    # Create the solver if it doesn't exist
    global solver
    if solver is None:
        solver = Gemini2Solver()
    
    # Solve the problem
    solution = solver.solve_problem(problem)
    
    # Return the solution
    return jsonify({"solution": solution})

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get the available Gemini 2.0 models."""
    return jsonify({
        "models": [
            {"id": "gemini-2.0-pro", "name": "Gemini 2.0 Pro"},
            {"id": "gemini-2.0-flash", "name": "Gemini 2.0 Flash"}
        ]
    })

def update_api_key(api_key):
    """
    Update the Gemini API key in the .secrets.toml file.
    
    Args:
        api_key: The API key to use.
    """
    # Path to the secrets file
    secrets_path = 'alpha_codium/settings/.secrets.toml'
    
    # Create the secrets dictionary
    secrets = {
        'gemini': {
            'key': api_key
        }
    }
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(secrets_path), exist_ok=True)
    
    # Write the secrets to the file
    with open(secrets_path, 'w') as f:
        toml.dump(secrets, f)
    
    logger.info(f'Updated API key in {secrets_path}')
    
    # Update the solver's API key
    global solver
    if solver is not None:
        solver = Gemini2Solver()

if __name__ == '__main__':
    # Create the templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Create the index.html file if it doesn't exist
    index_path = 'templates/index.html'
    if not os.path.exists(index_path):
        with open(index_path, 'w') as f:
            f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>AlphaCodium with Gemini 2.0</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #333;
        }
        label {
            display: block;
            margin-top: 10px;
        }
        input, textarea, select {
            width: 100%;
            padding: 8px;
            margin-top: 5px;
            box-sizing: border-box;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            cursor: pointer;
            margin-top: 10px;
        }
        button:hover {
            background-color: #45a049;
        }
        pre {
            background-color: #f5f5f5;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
        .test-case {
            border: 1px solid #ddd;
            padding: 10px;
            margin-top: 10px;
            border-radius: 5px;
        }
        .remove-test-case {
            background-color: #f44336;
            color: white;
            padding: 5px 10px;
            border: none;
            cursor: pointer;
            margin-top: 5px;
        }
        .remove-test-case:hover {
            background-color: #d32f2f;
        }
    </style>
</head>
<body>
    <h1>AlphaCodium with Gemini 2.0</h1>
    
    <div>
        <label for="api-key">Gemini API Key:</label>
        <input type="text" id="api-key" placeholder="Enter your Gemini API key">
        <p><small>Your API key is stored locally and is only used to access the Gemini API.</small></p>
    </div>
    
    <div>
        <label for="model">Model:</label>
        <select id="model">
            <option value="gemini-2.0-pro">Gemini 2.0 Pro</option>
            <option value="gemini-2.0-flash">Gemini 2.0 Flash</option>
        </select>
    </div>
    
    <div>
        <label for="problem-name">Problem Name:</label>
        <input type="text" id="problem-name" placeholder="Enter the problem name">
    </div>
    
    <div>
        <label for="problem-description">Problem Description:</label>
        <textarea id="problem-description" rows="5" placeholder="Enter the problem description"></textarea>
    </div>
    
    <div>
        <h3>Test Cases:</h3>
        <div id="test-cases"></div>
        <button id="add-test-case">Add Test Case</button>
    </div>
    
    <button id="solve-button">Solve Problem</button>
    
    <div>
        <h3>Solution:</h3>
        <pre id="solution"></pre>
    </div>
    
    <script>
        // Add a test case
        document.getElementById('add-test-case').addEventListener('click', function() {
            const testCasesDiv = document.getElementById('test-cases');
            const testCaseDiv = document.createElement('div');
            testCaseDiv.className = 'test-case';
            
            testCaseDiv.innerHTML = `
                <label for="test-input">Input:</label>
                <textarea class="test-input" rows="2" placeholder="Enter the test input"></textarea>
                
                <label for="test-output">Expected Output:</label>
                <textarea class="test-output" rows="2" placeholder="Enter the expected output"></textarea>
                
                <button class="remove-test-case">Remove</button>
            `;
            
            testCasesDiv.appendChild(testCaseDiv);
            
            // Add event listener to the remove button
            testCaseDiv.querySelector('.remove-test-case').addEventListener('click', function() {
                testCasesDiv.removeChild(testCaseDiv);
            });
        });
        
        // Add an initial test case
        document.getElementById('add-test-case').click();
        
        // Solve the problem
        document.getElementById('solve-button').addEventListener('click', function() {
            // Get the problem details
            const apiKey = document.getElementById('api-key').value;
            const model = document.getElementById('model').value;
            const name = document.getElementById('problem-name').value;
            const description = document.getElementById('problem-description').value;
            
            // Get the test cases
            const testCases = [];
            const testCaseDivs = document.querySelectorAll('.test-case');
            testCaseDivs.forEach(function(testCaseDiv) {
                const input = testCaseDiv.querySelector('.test-input').value;
                const output = testCaseDiv.querySelector('.test-output').value;
                
                if (input && output) {
                    testCases.push({
                        input: input,
                        output: output
                    });
                }
            });
            
            // Check if the required fields are filled
            if (!name) {
                alert('Please enter a problem name');
                return;
            }
            
            if (!description) {
                alert('Please enter a problem description');
                return;
            }
            
            if (testCases.length === 0) {
                alert('Please add at least one test case');
                return;
            }
            
            // Show loading message
            document.getElementById('solution').textContent = 'Solving...';
            
            // Send the request to the server
            fetch('/api/solve', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    api_key: apiKey,
                    model: model,
                    name: name,
                    description: description,
                    public_tests: testCases
                })
            })
            .then(response => response.json())
            .then(data => {
                // Show the solution
                document.getElementById('solution').textContent = data.solution;
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('solution').textContent = 'Error: ' + error.message;
            });
        });
    </script>
</body>
</html>
            """)
    
    # Run the app
    app.run(host='0.0.0.0', port=12000, debug=True)