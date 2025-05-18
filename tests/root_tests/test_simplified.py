#!/usr/bin/env python3
"""
Test script for the simplified AlphaCodium implementation.
This script tests the ProblemSolver class with a simple problem.
"""

import logging

from alpha_codium.gen.problem_solver import ProblemSolver
from alpha_codium.gen.utils import evaluate_solution_on_subset

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_problem_solver():
    """Test the ProblemSolver class with a simple problem."""
    
    # Define a simple problem
    problem = {
        "name": "Factorial",
        "description": "Write a function called factorial that takes a non-negative integer n as input and returns n!. The factorial of n is the product of all positive integers less than or equal to n.",
        "public_tests": {
            "input": ["5", "0", "1", "10"],
            "output": ["120", "1", "1", "3628800"]
        }
    }
    
    logger.info(f"Testing ProblemSolver with problem: {problem['name']}")
    
    # Create a solver
    solver = ProblemSolver()
    
    # Solve the problem
    solution = solver.solve_problem(problem)
    
    logger.info(f"Solution:\n{solution}")
    
    # Evaluate the solution
    logger.info("Evaluating solution on public tests...")
    test_results, test_passed, test_failed, test_timeout = evaluate_solution_on_subset(
        'public_tests', problem, solution, silent=False
    )
    
    logger.info(f"Tests passed: {test_passed}, Tests failed: {test_failed}, Tests timed out: {test_timeout}")
    
    return test_passed == len(problem['public_tests']['input'])

if __name__ == "__main__":
    success = test_problem_solver()
    if success:
        print("\n✅ Test passed! The ProblemSolver successfully solved the factorial problem.")
    else:
        print("\n❌ Test failed. The solution did not pass all test cases.")