#!/usr/bin/env python3
"""
Simplified AlphaCodium solver that uses Gemini 2.0 models.
"""

import os
import sys
import logging
import argparse
from typing import Dict, Any, List, Optional

# Add the parent directory to the path so we can import from alpha_codium
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import google.generativeai as genai
from alpha_codium.settings.config_loader import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

class Gemini2Solver:
    """
    Simplified AlphaCodium solver that uses Gemini 2.0 models.
    """
    
    def __init__(self, model: str = None):
        """
        Initialize the solver.
        
        Args:
            model: The Gemini 2.0 model to use. If None, uses the model from the configuration.
        """
        self.logger = logger
        
        # Get settings
        self.settings = get_settings()
        
        # Set the model
        if model is None:
            self.model = self.settings.config.get("model", "gemini-2.0-pro")
        else:
            self.model = model
        
        # Ensure we're using a Gemini 2.0 model
        if not self.model.startswith("gemini-2.0"):
            self.logger.warning(f"Model {self.model} is not a Gemini 2.0 model. Using gemini-2.0-pro instead.")
            self.model = "gemini-2.0-pro"
        
        # Configure the Gemini API
        api_key = self._get_api_key()
        if api_key:
            genai.configure(api_key=api_key)
        else:
            self.logger.error("No Gemini API key found. Please set it in .secrets.toml or as GEMINI_API_KEY environment variable.")
    
    def _get_api_key(self) -> Optional[str]:
        """
        Get the Gemini API key from settings or environment.
        
        Returns:
            The API key, or None if not found.
        """
        # Try to get from settings
        if hasattr(self.settings, 'SECRETS') and hasattr(self.settings.SECRETS, 'gemini') and hasattr(self.settings.SECRETS.gemini, 'key'):
            return self.settings.SECRETS.gemini.key
        
        # Try to get from environment
        return os.environ.get("GEMINI_API_KEY")
    
    def _generate_text(self, prompt: str) -> str:
        """
        Generate text using the Gemini 2.0 model.
        
        Args:
            prompt: The prompt to generate text from.
            
        Returns:
            The generated text.
        """
        try:
            # Get the model
            model = genai.GenerativeModel(self.model)
            
            # Generate text
            response = model.generate_content(prompt)
            
            # Return the text
            return response.text
        except Exception as e:
            self.logger.error(f"Error generating text: {e}")
            
            # Check if it's a model availability issue
            error_str = str(e)
            if "NOT_FOUND" in error_str and "models/" in error_str:
                model_name = self.model
                fallback_message = f"""
# Error: Model {model_name} is not available
# 
# The requested Gemini 2.0 model is not available in the current API version.
# Please check the available models using the Google AI Studio or API documentation.
#
# You can try:
# 1. Using a different Gemini 2.0 model (gemini-2.0-pro or gemini-2.0-flash)
# 2. Checking if your API key has access to Gemini 2.0 models
# 3. Updating the Google Generative AI Python library
"""
                return fallback_message
            
            # Check if it's an API key issue
            if "API_KEY_INVALID" in error_str or "API key expired" in error_str:
                fallback_message = """
# Error: Invalid or expired API key
# 
# The Gemini API key is invalid or has expired.
# Please update the API key in the .secrets.toml file or set the GEMINI_API_KEY environment variable.
#
# You can update the API key by running:
# python update_api_key.py --key YOUR_API_KEY
"""
                return fallback_message
            
            return f"# Error generating text\n# {str(e)}"
    
    def solve_problem(self, problem: Dict[str, Any]) -> str:
        """
        Solve a programming problem.
        
        Args:
            problem: A dictionary containing the problem details.
                - name: The name of the problem.
                - description: The problem description.
                - public_tests: A list of test cases, each with input and output.
                
        Returns:
            The solution to the problem.
        """
        # Extract problem details
        name = problem.get("name", "Unknown")
        description = problem.get("description", "")
        public_tests = problem.get("public_tests", [])
        
        # Create the prompt
        prompt = self._create_prompt(name, description, public_tests)
        
        # Generate the solution
        solution = self._generate_text(prompt)
        
        return solution
    
    def _create_prompt(self, name: str, description: str, public_tests: List[Dict[str, str]]) -> str:
        """
        Create a prompt for the Gemini 2.0 model.
        
        Args:
            name: The name of the problem.
            description: The problem description.
            public_tests: A list of test cases, each with input and output.
            
        Returns:
            The prompt for the Gemini 2.0 model.
        """
        # Create the test cases string
        test_cases_str = ""
        for i, test in enumerate(public_tests):
            test_cases_str += f"Test {i+1}:\n"
            test_cases_str += f"Input: {test.get('input', '')}\n"
            test_cases_str += f"Expected Output: {test.get('output', '')}\n\n"
        
        # Create the prompt
        prompt = f"""
You are an expert Python programmer. Your task is to solve the following programming problem:

Problem: {name}

Description:
{description}

Test Cases:
{test_cases_str}

Please provide a Python solution to this problem. Your solution should:
1. Be correct and pass all the test cases
2. Be efficient and well-optimized
3. Include clear comments explaining your approach
4. Follow good coding practices and style guidelines

Your solution should be a complete Python function or class that can be directly used to solve the problem.

Python Solution:
```python
"""
        
        return prompt

def main():
    """Main function to run the solver."""
    parser = argparse.ArgumentParser(description="Solve a programming problem using Gemini 2.0 models")
    parser.add_argument("--problem", type=str, required=True,
                        help="The problem to solve (e.g., 'factorial', 'fizzbuzz')")
    parser.add_argument("--model", type=str, default=None,
                        help="The Gemini 2.0 model to use (e.g., 'gemini-2.0-pro', 'gemini-2.0-flash')")
    args = parser.parse_args()
    
    # Define problems
    problems = {
        "factorial": {
            "name": "Factorial",
            "description": "Write a function called factorial that takes a non-negative integer n as input and returns n!. The factorial of n is the product of all positive integers less than or equal to n.",
            "public_tests": [
                {"input": "0", "output": "1"},
                {"input": "1", "output": "1"},
                {"input": "5", "output": "120"},
                {"input": "10", "output": "3628800"}
            ]
        },
        "fizzbuzz": {
            "name": "FizzBuzz",
            "description": "Write a function called fizzbuzz that takes a positive integer n as input and returns a list of strings representing the FizzBuzz sequence from 1 to n. For multiples of 3, use 'Fizz' instead of the number. For multiples of 5, use 'Buzz'. For multiples of both 3 and 5, use 'FizzBuzz'.",
            "public_tests": [
                {"input": "3", "output": "['1', '2', 'Fizz']"},
                {"input": "5", "output": "['1', '2', 'Fizz', '4', 'Buzz']"},
                {"input": "15", "output": "['1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8', 'Fizz', 'Buzz', '11', 'Fizz', '13', '14', 'FizzBuzz']"}
            ]
        },
        "palindrome": {
            "name": "Palindrome",
            "description": "Write a function called is_palindrome that takes a string as input and returns True if the string is a palindrome (reads the same forwards and backwards), and False otherwise. Ignore case and non-alphanumeric characters.",
            "public_tests": [
                {"input": "'racecar'", "output": "True"},
                {"input": "'A man, a plan, a canal: Panama'", "output": "True"},
                {"input": "'hello'", "output": "False"},
                {"input": "'12321'", "output": "True"}
            ]
        }
    }
    
    # Get the problem
    problem_key = args.problem.lower()
    if problem_key not in problems:
        logger.error(f"Problem '{args.problem}' not found. Available problems: {', '.join(problems.keys())}")
        return
    
    # Create the solver
    solver = Gemini2Solver(args.model)
    
    # Solve the problem
    solution = solver.solve_problem(problems[problem_key])
    
    # Print the solution
    print(solution)

if __name__ == "__main__":
    main()