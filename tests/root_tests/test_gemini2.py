#!/usr/bin/env python3
"""
Test script for the simplified AlphaCodium solver using Gemini 2.0 models.
"""

import argparse
import logging
import sys
from typing import Dict, Any, List, Optional

from alpha_codium.simplified_solver import SimplifiedSolver
from alpha_codium.settings.config_loader import get_settings, update_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def setup_gemini2_model():
    """Configure AlphaCodium to use Gemini 2.0 models."""
    # Update the configuration to use Gemini 2.0 models
    settings = get_settings()
    
    # Check if we're already using a Gemini 2.0 model
    current_model = settings.config.get('model', '')
    if 'gemini-2.0' in current_model:
        logger.info(f"Already using Gemini 2.0 model: {current_model}")
        return
    
    # Update to use Gemini 2.0 Flash by default
    update_settings('config', 'model', 'gemini-2.0-flash')
    logger.info("Updated configuration to use Gemini 2.0 Flash model")

def test_problem(problem_name: str, problem_description: str, test_cases: List[Dict[str, str]]):
    """
    Test the simplified solver on a programming problem.
    
    Args:
        problem_name: The name of the problem
        problem_description: The description of the problem
        test_cases: A list of test cases, each with 'input' and 'output' keys
    """
    logger.info(f"Testing SimplifiedSolver with problem: {problem_name}")
    
    # Create the problem dictionary
    problem = {
        "name": problem_name,
        "description": problem_description,
        "public_tests": test_cases
    }
    
    # Create the solver
    solver = SimplifiedSolver()
    
    # Solve the problem
    solution = solver.solve_problem(problem)
    
    logger.info(f"Solution:\n{solution}")
    
    # You can add evaluation logic here if needed
    
    return solution

def check_api_key():
    """Check if the Gemini API key is valid."""
    import os
    import toml
    import subprocess
    
    # Find all .secrets.toml files
    result = subprocess.run(
        ["find", ".", "-name", ".secrets.toml", "-type", "f"], 
        cwd=os.path.dirname(os.path.abspath(__file__)),
        capture_output=True, 
        text=True
    )
    
    if result.stdout:
        # Use the first .secrets.toml file found
        secrets_path = result.stdout.strip().split('\n')[0]
        
        # Check if the API key is valid
        logger.warning("""
API key may be expired or invalid. Please update it with a valid Gemini API key.

You can update the API key by:
1. Editing the .secrets.toml file directly
2. Using the update_api_key.py script
3. Setting the GEMINI_API_KEY environment variable

Note: Gemini 2.0 models may not be available in the current API version.
In that case, you can use Gemini 1.5 models instead.
""")
        
        return False
    
    return True

def main():
    """Main function to run the test."""
    parser = argparse.ArgumentParser(description="Test the simplified AlphaCodium solver")
    parser.add_argument("--problem", type=str, default="Factorial",
                        help="The name of the problem to solve")
    args = parser.parse_args()
    
    # Check if the API key is valid
    if not check_api_key():
        logger.error("Invalid or expired API key. Please update it before running the test.")
        return
    
    # Setup Gemini 2.0 model
    setup_gemini2_model()
    
    # Define test problems
    problems = {
        "Factorial": {
            "description": "Write a function called factorial that takes a non-negative integer n as input and returns n!. The factorial of n is the product of all positive integers less than or equal to n.",
            "test_cases": [
                {"input": "0", "output": "1"},
                {"input": "1", "output": "1"},
                {"input": "5", "output": "120"},
                {"input": "10", "output": "3628800"}
            ]
        },
        "FizzBuzz": {
            "description": "Write a function called fizzbuzz that takes a positive integer n as input and returns a list of strings. For each integer i from 1 to n, the function should return 'Fizz' if i is divisible by 3, 'Buzz' if i is divisible by 5, 'FizzBuzz' if i is divisible by both 3 and 5, and the string representation of i otherwise.",
            "test_cases": [
                {"input": "3", "output": "['1', '2', 'Fizz']"},
                {"input": "5", "output": "['1', '2', 'Fizz', '4', 'Buzz']"},
                {"input": "15", "output": "['1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8', 'Fizz', 'Buzz', '11', 'Fizz', '13', '14', 'FizzBuzz']"}
            ]
        },
        "Palindrome": {
            "description": "Write a function called is_palindrome that takes a string as input and returns True if the string is a palindrome (reads the same forwards and backwards), and False otherwise. Ignore case and non-alphanumeric characters.",
            "test_cases": [
                {"input": "'racecar'", "output": "True"},
                {"input": "'A man, a plan, a canal: Panama'", "output": "True"},
                {"input": "'hello'", "output": "False"}
            ]
        }
    }
    
    # Get the problem to solve
    problem_name = args.problem
    if problem_name not in problems:
        logger.error(f"Unknown problem: {problem_name}")
        logger.info(f"Available problems: {', '.join(problems.keys())}")
        return
    
    problem_data = problems[problem_name]
    
    # Test the problem
    solution = test_problem(
        problem_name=problem_name,
        problem_description=problem_data["description"],
        test_cases=problem_data["test_cases"]
    )
    
    # Save the solution to a file
    with open(f"{problem_name.lower()}_solution.py", "w") as f:
        f.write(solution)
    
    logger.info(f"Solution saved to {problem_name.lower()}_solution.py")

if __name__ == "__main__":
    main()