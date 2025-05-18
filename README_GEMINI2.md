# AlphaCodium with Gemini 2.0

This is a simplified version of AlphaCodium that uses Gemini 2.0 models to solve programming problems. The implementation has been streamlined to focus on the core functionality and remove unnecessary complexity.

## Features

- Uses Gemini 2.0 models for all stages of the solution process
- Simplified API for solving programming problems
- Improved error handling for API key and model availability issues
- Streamlined implementation that focuses on the core functionality

## Setup

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Set up your Gemini API key:

```bash
python update_api_key.py --key YOUR_API_KEY
```

You can get a Gemini API key from the [Google AI Studio](https://ai.google.dev/).

## Usage

### Using the SimplifiedSolver

```python
from alpha_codium.simplified_solver import SimplifiedSolver

# Create a problem dictionary
problem = {
    "name": "Factorial",
    "description": "Write a function called factorial that takes a non-negative integer n as input and returns n!. The factorial of n is the product of all positive integers less than or equal to n.",
    "public_tests": [
        {"input": "0", "output": "1"},
        {"input": "1", "output": "1"},
        {"input": "5", "output": "120"},
        {"input": "10", "output": "3628800"}
    ]
}

# Create the solver
solver = SimplifiedSolver()

# Solve the problem
solution = solver.solve_problem(problem)

print(solution)
```

### Using the Test Script

You can use the test script to solve predefined problems:

```bash
python test_gemini2.py --problem Factorial
```

Available problems:
- Factorial
- FizzBuzz
- Palindrome

## Troubleshooting

### API Key Issues

If you encounter API key issues, you can update your API key using the `update_api_key.py` script:

```bash
python update_api_key.py --key YOUR_API_KEY
```

### Model Availability Issues

If you encounter model availability issues, you can try using a different Gemini 2.0 model by updating the configuration:

```python
from alpha_codium.settings.config_loader import update_settings

# Use Gemini 2.0 Pro instead of Gemini 2.0 Flash
update_settings('config', 'model', 'gemini-2.0-pro')
```

### Checking Available Models

You can check which Gemini models are available using the `list_models.py` script:

```bash
python list_models.py
```

## Implementation Details

The SimplifiedSolver class implements a streamlined version of the AlphaCodium approach:

1. **Analyze the problem**: The solver first analyzes the problem to understand the requirements and constraints.
2. **Generate a solution**: Based on the analysis, the solver generates a solution to the problem.
3. **Test the solution**: The solver tests the solution against the provided test cases.
4. **Refine the solution**: If the solution fails any tests, the solver refines it to fix the issues.

The implementation uses Gemini 2.0 models for all stages of the solution process, with fallback mechanisms for handling API key and model availability issues.

## License

This project is licensed under the MIT License - see the LICENSE file for details.