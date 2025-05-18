import os
import sys
import json
import asyncio
from flask import Flask, request, jsonify, render_template

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from alpha_codium.simplified_solver import SimplifiedSolver
from alpha_codium.llm.model_manager import ModelManager
from alpha_codium.log import setup_logger

app = Flask(__name__)
setup_logger()

# Initialize model manager to get available models
model_manager = ModelManager()

# Create templates directory if it doesn't exist
os.makedirs('templates', exist_ok=True)

# Create a simple HTML template for the web interface
with open('templates/index.html', 'w') as f:
    f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>AlphaCodium - Problem Solver</title>
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
        textarea, input {
            width: 100%;
            padding: 8px;
            margin: 8px 0;
            box-sizing: border-box;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        .test-case {
            border: 1px solid #ddd;
            padding: 10px;
            margin: 10px 0;
        }
        #solution {
            white-space: pre-wrap;
            background-color: #f5f5f5;
            padding: 15px;
            border: 1px solid #ddd;
            display: none;
        }
        #loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <h1>AlphaCodium - Problem Solver</h1>
    <p>Enter your programming problem details below:</p>
    
    <form id="problemForm">
        <div>
            <label for="problemName">Problem Name:</label>
            <input type="text" id="problemName" name="problemName" required>
        </div>
        
        <div>
            <label for="problemDescription">Problem Description:</label>
            <textarea id="problemDescription" name="problemDescription" rows="10" required></textarea>
        </div>
        
        <div id="testCases">
            <h3>Test Cases</h3>
            <div class="test-case">
                <label for="testInput0">Test Input:</label>
                <textarea id="testInput0" name="testInputs[]" rows="3" required></textarea>
                
                <label for="testOutput0">Expected Output:</label>
                <textarea id="testOutput0" name="testOutputs[]" rows="3" required></textarea>
            </div>
        </div>
        
        <button type="button" id="addTestCase">Add Test Case</button>
        <button type="submit">Solve Problem</button>
    </form>
    
    <div id="loading">
        <p>Solving problem... This may take a few minutes.</p>
        <p>The AlphaCodium approach involves multiple steps including problem analysis, test generation, and code refinement.</p>
    </div>
    
    <div id="solutionContainer" style="display: none;">
        <h2>Solution:</h2>
        <pre id="solution"></pre>
    </div>
    
    <script>
        document.getElementById('addTestCase').addEventListener('click', function() {
            const testCases = document.getElementById('testCases');
            const testCaseCount = testCases.getElementsByClassName('test-case').length;
            
            const newTestCase = document.createElement('div');
            newTestCase.className = 'test-case';
            newTestCase.innerHTML = `
                <label for="testInput${testCaseCount}">Test Input:</label>
                <textarea id="testInput${testCaseCount}" name="testInputs[]" rows="3" required></textarea>
                
                <label for="testOutput${testCaseCount}">Expected Output:</label>
                <textarea id="testOutput${testCaseCount}" name="testOutputs[]" rows="3" required></textarea>
            `;
            
            testCases.appendChild(newTestCase);
        });
        
        document.getElementById('problemForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const problemName = document.getElementById('problemName').value;
            const problemDescription = document.getElementById('problemDescription').value;
            
            const testInputs = [];
            const testOutputs = [];
            
            document.querySelectorAll('[name="testInputs[]"]').forEach(input => {
                testInputs.push(input.value);
            });
            
            document.querySelectorAll('[name="testOutputs[]"]').forEach(output => {
                testOutputs.push(output.value);
            });
            
            // Show loading indicator
            document.getElementById('loading').style.display = 'block';
            document.getElementById('solutionContainer').style.display = 'none';
            
            // Send request to the server
            fetch('/solve', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    problemName: problemName,
                    problemDescription: problemDescription,
                    testInputs: testInputs,
                    testOutputs: testOutputs
                })
            })
            .then(response => response.json())
            .then(data => {
                // Hide loading indicator
                document.getElementById('loading').style.display = 'none';
                
                // Show solution
                document.getElementById('solutionContainer').style.display = 'block';
                document.getElementById('solution').textContent = data.solution;
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('loading').style.display = 'none';
                alert('An error occurred while solving the problem. Please try again.');
            });
        });
    </script>
</body>
</html>
''')

@app.route('/')
def index():
    # Get available models
    models = model_manager.get_available_models(refresh=False)
    # Filter to only include Gemini 2.0 models
    gemini_models = [model for model in models if model.get('id', '').startswith('gemini-2.0')]
    
    # Convert models to a format suitable for the template
    model_options = []
    for model in gemini_models:
        model_id = model.get('id', '').replace('models/', '')
        model_options.append({
            'id': model_id,
            'name': model.get('displayName', model_id)
        })
    
    # Pass models to the template
    return render_template('index.html', models=model_options)

@app.route('/models', methods=['GET'])
def get_models():
    # Get available models
    models = model_manager.get_available_models(refresh=True)
    # Filter to only include Gemini 2.0 models
    gemini_models = [model for model in models if model.get('id', '').startswith('gemini-2.0')]
    
    # Convert models to a format suitable for the template
    model_options = []
    for model in gemini_models:
        model_id = model.get('id', '').replace('models/', '')
        model_options.append({
            'id': model_id,
            'name': model.get('displayName', model_id)
        })
    
    return jsonify({'models': model_options})

@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    
    problem_name = data.get('problemName', 'User Problem')
    problem_description = data.get('problemDescription', '')
    test_inputs = data.get('testInputs', [])
    test_outputs = data.get('testOutputs', [])
    model_id = data.get('modelId', None)
    
    # Validate inputs
    if not problem_description:
        return jsonify({'error': 'Problem description is required'}), 400
    
    if len(test_inputs) != len(test_outputs):
        return jsonify({'error': 'Number of test inputs must match number of test outputs'}), 400
    
    if len(test_inputs) == 0:
        return jsonify({'error': 'At least one test case is required'}), 400
    
    try:
        # Create problem dictionary
        problem = {
            'name': problem_name,
            'description': problem_description,
            'public_tests': [
                {'input': inp, 'output': out} for inp, out in zip(test_inputs, test_outputs)
            ]
        }
        
        # Initialize the solver with the selected model
        solver = SimplifiedSolver(model_id=model_id)
        
        # Solve the problem
        solution = solver.solve_problem(problem)
        
        return jsonify({'solution': solution})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 12000))
    app.run(host='0.0.0.0', port=port, debug=True)