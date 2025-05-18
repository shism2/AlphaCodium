import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

class DirectSolver:
    """
    A simplified implementation that directly uses the Gemini API to solve programming problems.
    """
    
    def __init__(self):
        """Initialize the DirectSolver with the Gemini API key."""
        # Configure the Gemini API
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            # Try to read from .secrets.toml
            try:
                import toml
                secrets = toml.load("/workspace/AlphaCodium/alpha_codium/settings/.secrets.toml")
                api_key = secrets.get("gemini", {}).get("key")
            except Exception as e:
                print(f"Error loading API key: {e}")
                
        if not api_key:
            raise ValueError("Gemini API key is required. Set GEMINI_API_KEY environment variable.")
            
        genai.configure(api_key=api_key)
        
        # Set up the model
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-pro",
            generation_config={
                "temperature": 0.2,
                "top_p": 0.95,
                "top_k": 0,
                "max_output_tokens": 8192,
            },
            safety_settings={
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )
    
    def solve_problem(self, problem):
        """
        Solve a programming problem using the Gemini API.
        
        Args:
            problem: A dictionary containing the problem details
                - name: The name of the problem
                - description: The problem description
                - public_tests: A list of test cases with input and output
                
        Returns:
            The solution code as a string
        """
        # Create the prompt
        prompt = self._create_prompt(problem)
        
        # Generate the solution
        response = self.model.generate_content(prompt)
        
        # Extract the code from the response
        solution = self._extract_code(response.text)
        
        return solution
    
    def _create_prompt(self, problem):
        """Create a prompt for the Gemini API."""
        name = problem.get("name", "")
        description = problem.get("description", "")
        public_tests = problem.get("public_tests", [])
        
        # Format the test cases
        test_cases = ""
        for i, test in enumerate(public_tests):
            test_cases += f"Test {i+1}:\n"
            test_cases += f"Input: {test.get('input', '')}\n"
            test_cases += f"Expected Output: {test.get('output', '')}\n\n"
        
        # Create the prompt
        prompt = f"""
You are an expert Python programmer. Your task is to solve the following programming problem:

Problem Name: {name}

Problem Description:
{description}

Test Cases:
{test_cases}

Write a Python solution that correctly solves this problem. Your solution should:
1. Be efficient and handle all edge cases
2. Pass all the provided test cases
3. Follow good programming practices
4. Include clear comments explaining your approach

Return only the Python code without any additional explanations.
"""
        return prompt
    
    def _extract_code(self, text):
        """Extract the code from the response text."""
        # If the response contains code blocks, extract them
        if "```python" in text:
            code_blocks = text.split("```python")
            if len(code_blocks) > 1:
                code = code_blocks[1].split("```")[0].strip()
                return code
        
        # If no code blocks, return the entire text
        return text