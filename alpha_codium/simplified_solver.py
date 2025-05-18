"""
Simplified AlphaCodium Problem Solver

This module provides a streamlined implementation of the AlphaCodium approach
for solving programming problems using Gemini 2.0 models.
"""

import asyncio
import logging
import time
from typing import Dict, Any, List, Optional, Tuple
import json
import os

from alpha_codium.llm.ai_handler import AiHandler
from alpha_codium.llm.model_manager import ModelManager
from alpha_codium.db.database_manager import DatabaseManager
from alpha_codium.log import get_logger
from alpha_codium.settings.config_loader import get_settings

class SimplifiedSolver:
    """
    A simplified implementation of the AlphaCodium approach to solve programming problems.
    This class focuses on the core functionality and removes unnecessary complexity.
    """
    
    def __init__(self, model_id: Optional[str] = None, db_path: Optional[str] = None, use_cache: bool = True):
        """
        Initialize the SimplifiedSolver.
        
        Args:
            model_id: The ID of the model to use. If None, uses the default from configuration.
            db_path: Path to the SQLite database file. If None, uses the default path.
            use_cache: Whether to use cached solutions from the database.
        """
        self.ai_handler = AiHandler()
        self.logger = get_logger(__name__)
        
        # Initialize model manager
        self.model_manager = ModelManager()
        
        # Initialize database manager
        self.db_manager = DatabaseManager(db_path=db_path)
        
        # Set cache usage
        self.use_cache = use_cache
        
        # Set the model to use
        if model_id:
            self.model = model_id
        else:
            # Always use Gemini 2.0 models
            config_model = get_settings().config.get('model', 'gemini-2.0-flash')
            if not config_model.startswith('gemini-2.0'):
                self.logger.warning(f"Configured model {config_model} is not a Gemini 2.0 model. Using gemini-2.0-flash instead.")
                self.model = 'gemini-2.0-flash'
            else:
                self.model = config_model
        
        # Load prompt templates
        self._load_prompts()
    
    def _load_prompts(self):
        """Load prompt templates for different stages of the solution process."""
        self.prompts = {
            "analyze": {
                "system": """You are an expert programmer and problem solver. Analyze the following programming problem carefully.
                
Your task is to understand the problem requirements, identify edge cases, and plan a solution approach.

Think step by step about:
1. What the problem is asking for
2. Input and output formats
3. Constraints and edge cases
4. Potential algorithms or data structures to use
5. Time and space complexity considerations""",
                
                "user": """# Problem: {{name}}

## Description
{{description}}

## Test Cases
{% for test in public_tests %}
Input: {{test.input}}
Expected Output: {{test.output}}
{% endfor %}

Analyze this problem and provide your insights."""
            },
            
            "solve": {
                "system": """You are an expert programmer tasked with solving a programming problem. 
                
Write clean, efficient, and well-documented code that solves the given problem. Your solution should:
1. Handle all edge cases
2. Be optimized for time and space complexity
3. Include clear comments explaining your approach
4. Pass all the provided test cases

Provide only the code solution without explanations outside the code.""",
                
                "user": """# Problem: {{name}}

## Description
{{description}}

## Test Cases
{% for test in public_tests %}
Input: {{test.input}}
Expected Output: {{test.output}}
{% endfor %}

{% if analysis %}
## Problem Analysis
{{analysis}}
{% endif %}

Write a complete solution to this problem."""
            },
            
            "test": {
                "system": """You are an expert programmer tasked with testing a solution to a programming problem.
                
Evaluate the provided solution against the test cases. For each test case:
1. Trace through the code execution
2. Determine if the solution produces the expected output
3. Identify any bugs or edge cases that aren't handled correctly""",
                
                "user": """# Problem: {{name}}

## Description
{{description}}

## Test Cases
{% for test in public_tests %}
Input: {{test.input}}
Expected Output: {{test.output}}
{% endfor %}

## Solution
```python
{{solution}}
```

Evaluate this solution against the test cases."""
            },
            
            "refine": {
                "system": """You are an expert programmer tasked with improving a solution to a programming problem.
                
The current solution has some issues or could be optimized further. Your task is to:
1. Fix any bugs in the current solution
2. Optimize the code for better time or space complexity if possible
3. Improve code readability and documentation
4. Ensure the solution passes all test cases

Provide only the improved code solution without explanations outside the code.""",
                
                "user": """# Problem: {{name}}

## Description
{{description}}

## Test Cases
{% for test in public_tests %}
Input: {{test.input}}
Expected Output: {{test.output}}
{% endfor %}

## Current Solution
```python
{{solution}}
```

## Issues
{{issues}}

Provide an improved solution that addresses these issues."""
            }
        }
    
    async def _run_prompt(self, prompt_type: str, problem: Dict[str, Any], 
                          temperature: float = 0.2) -> str:
        """
        Run a prompt through the AI model.
        
        Args:
            prompt_type: The type of prompt to use (analyze, solve, test, refine)
            problem: The problem data
            temperature: The temperature to use for generation
            
        Returns:
            The model's response
        """
        from jinja2 import Environment, StrictUndefined
        
        # Set up Jinja2 environment
        environment = Environment(undefined=StrictUndefined)
        environment.globals["zip"] = zip
        environment.globals["enumerate"] = enumerate
        
        # Render the prompts
        prompt = self.prompts.get(prompt_type, self.prompts["solve"])
        system_prompt = environment.from_string(prompt["system"]).render(problem)
        user_prompt = environment.from_string(prompt["user"]).render(problem)
        
        # Run the model
        response, _ = await self.ai_handler.chat_completion(
            model=self.model,
            system=system_prompt,
            user=user_prompt,
            temperature=temperature
        )
        
        return response
    
    async def solve(self, problem: Dict[str, Any]) -> str:
        """
        Solve a programming problem using the simplified AlphaCodium approach.
        
        Args:
            problem: The problem data including name, description, and test cases
            
        Returns:
            The solution code
        """
        self.logger.info(f"Solving problem '{problem.get('name', 'Unnamed')}' using model {self.model}")
        
        try:
            # Step 1: Analyze the problem
            self.logger.info("Step 1: Analyzing problem")
            analysis = await self._run_prompt("analyze", problem)
            problem["analysis"] = analysis
            
            # Step 2: Generate initial solution
            self.logger.info("Step 2: Generating initial solution")
            solution = await self._run_prompt("solve", problem)
            problem["solution"] = solution
            
            # Step 3: Test the solution
            self.logger.info("Step 3: Testing solution")
            test_results = await self._run_prompt("test", problem)
            
            # Step 4: Refine the solution if needed
            if "fails" in test_results.lower() or "incorrect" in test_results.lower() or "error" in test_results.lower():
                self.logger.info("Step 4: Refining solution")
                problem["issues"] = test_results
                refined_solution = await self._run_prompt("refine", problem, temperature=0.3)
                return refined_solution
            
            return solution
            
        except Exception as e:
            self.logger.error(f"Error solving problem: {e}")
            
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
                fallback_message = f"""
# Error: Invalid or expired API key
# 
# The Gemini API key is invalid or has expired.
# Please update the API key in the .secrets.toml file or set the GEMINI_API_KEY environment variable.
"""
                return fallback_message
            
            return f"# Error solving problem\n# {str(e)}"
    
    def solve_problem(self, problem: Dict[str, Any]) -> str:
        """
        Synchronous wrapper for the solve method.
        
        Args:
            problem: The problem data
            
        Returns:
            The solution code
        """
        # Normalize the problem format
        normalized_problem = self._normalize_problem_format(problem)
        
        # Save the problem to the database
        problem_id = self.db_manager.save_problem(normalized_problem)
        
        # Check if we already have a solution for this problem with the current model
        if self.use_cache and problem_id > 0:
            solutions = self.db_manager.get_solutions_for_problem(problem_id)
            for solution in solutions:
                if solution["model_id"] == self.model and solution["success"]:
                    self.logger.info(f"Found existing solution for problem {problem_id} using model {self.model}")
                    return solution["code"]
        elif not self.use_cache:
            self.logger.info("Solution cache is disabled, generating new solution")
        
        # No existing solution found, generate a new one
        start_time = time.time()
        solution = asyncio.run(self.solve(normalized_problem))
        execution_time = time.time() - start_time
        
        # Save the solution to the database
        if problem_id > 0:
            success = len(solution) > 0 and not solution.startswith("# Error")
            solution_id = self.db_manager.save_solution(
                problem_id=problem_id,
                model_id=self.model,
                code=solution,
                execution_time=execution_time,
                success=success
            )
            
            # Save model information if available
            model_info = self.model_manager.get_model_by_id(self.model)
            if model_info:
                self.db_manager.save_model_info(model_info)
        
        return solution
    
    def _normalize_problem_format(self, problem: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize the problem format to ensure consistency.
        
        Args:
            problem: The problem data in any supported format
            
        Returns:
            The normalized problem data
        """
        normalized = {
            "name": problem.get("name", "Unnamed Problem"),
            "description": problem.get("description", ""),
        }
        
        # Handle different test case formats
        if "public_tests" in problem:
            public_tests = problem["public_tests"]
            
            # Handle list format
            if isinstance(public_tests, list):
                normalized["public_tests"] = public_tests
            
            # Handle dict format with input/output lists
            elif isinstance(public_tests, dict) and "input" in public_tests and "output" in public_tests:
                inputs = public_tests["input"]
                outputs = public_tests["output"]
                
                if len(inputs) != len(outputs):
                    raise ValueError("Number of test inputs must match number of test outputs")
                
                normalized["public_tests"] = [
                    {"input": inp, "output": out} for inp, out in zip(inputs, outputs)
                ]
        else:
            # Try to extract test cases from other fields
            test_inputs = problem.get("test_inputs", [])
            test_outputs = problem.get("test_outputs", [])
            
            if test_inputs and test_outputs:
                if len(test_inputs) != len(test_outputs):
                    raise ValueError("Number of test inputs must match number of test outputs")
                
                normalized["public_tests"] = [
                    {"input": inp, "output": out} for inp, out in zip(test_inputs, test_outputs)
                ]
            else:
                normalized["public_tests"] = []
        
        return normalized