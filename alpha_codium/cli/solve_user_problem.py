import argparse
import json
import os
import tempfile
from typing import Dict, Any, List, Optional

from alpha_codium.gen.problem_solver import ProblemSolver
from alpha_codium.gen.utils import evaluate_solution_on_subset
from alpha_codium.log import setup_logger, get_logger
from alpha_codium.settings.config_loader import get_settings


def create_problem_json(problem_description: str, 
                       test_inputs: List[str], 
                       test_outputs: List[str],
                       problem_name: str = "User Problem") -> Dict[str, Any]:
    """
    Create a problem JSON object from user inputs.
    
    Args:
        problem_description: The problem description
        test_inputs: List of test inputs
        test_outputs: List of test outputs
        problem_name: Name of the problem
        
    Returns:
        A dictionary containing the problem data
    """
    return {
        "name": problem_name,
        "description": problem_description,
        "public_tests": {
            "input": test_inputs,
            "output": test_outputs
        }
    }


def create_temp_dataset(problem: Dict[str, Any]) -> str:
    """
    Create a temporary dataset file containing the problem.
    
    Args:
        problem: The problem data
        
    Returns:
        Path to the temporary dataset file
    """
    dataset = {
        "user": [problem]
    }
    
    # Create a temporary file
    fd, path = tempfile.mkstemp(suffix='.json')
    with os.fdopen(fd, 'w') as f:
        json.dump(dataset, f)
    
    return path


def solve_user_problem(problem_description: str, 
                     test_inputs: List[str], 
                     test_outputs: List[str],
                     problem_name: str = "User Problem") -> str:
    """
    Solve a problem provided by the user.
    
    Args:
        problem_description: The problem description
        test_inputs: List of test inputs
        test_outputs: List of test outputs
        problem_name: Name of the problem
        
    Returns:
        The solution code
    """
    logger = get_logger(__name__)
    
    # Create problem JSON
    problem = create_problem_json(
        problem_description=problem_description,
        test_inputs=test_inputs,
        test_outputs=test_outputs,
        problem_name=problem_name
    )
    
    # Solve the problem
    solver = ProblemSolver()
    solution = solver.solve_problem(problem)
    
    # Evaluate the solution
    logger.info(f"Evaluating solution on provided tests...")
    test_results, test_passed, test_failed, test_timeout = evaluate_solution_on_subset(
        'public_tests', problem, solution, silent=False
    )
    
    logger.info(f"\nTests passed: {test_passed}, Tests failed: {test_failed}, Tests timed out: {test_timeout}")
    
    return solution


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve a programming problem provided by the user")
    parser.add_argument("--problem_description", type=str, required=True,
                       help="Description of the problem")
    parser.add_argument("--test_inputs", type=str, nargs='+', required=True,
                       help="List of test inputs")
    parser.add_argument("--test_outputs", type=str, nargs='+', required=True,
                       help="List of expected test outputs")
    parser.add_argument("--problem_name", type=str, default="User Problem",
                       help="Name of the problem")
    parser.add_argument("--output_file", type=str, default="",
                       help="Path to save the solution (if not provided, solution will be printed to stdout)")
    
    args = parser.parse_args()
    
    # Validate inputs
    if len(args.test_inputs) != len(args.test_outputs):
        raise ValueError("Number of test inputs must match number of test outputs")
    
    setup_logger()
    
    # Solve the problem
    solution = solve_user_problem(
        problem_description=args.problem_description,
        test_inputs=args.test_inputs,
        test_outputs=args.test_outputs,
        problem_name=args.problem_name
    )
    
    # Output the solution
    if args.output_file:
        with open(args.output_file, 'w') as f:
            f.write(solution)
        print(f"Solution saved to {args.output_file}")
    else:
        print("\n=== SOLUTION ===\n")
        print(solution)