#!/usr/bin/env python3
"""
AlphaCodium Problem Solver

This script provides a command-line interface for solving programming problems
using the AlphaCodium approach with Gemini 2.0 models.
"""

import argparse
import json
import sys
import os

# Add the parent directory to the path so we can import from alpha_codium
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from alpha_codium.gen.problem_solver import ProblemSolver

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Solve programming problems using AlphaCodium")
    parser.add_argument("--problem", type=str, help="Path to a JSON file containing the problem description")
    parser.add_argument("--name", type=str, help="Name of the problem")
    parser.add_argument("--description", type=str, help="Description of the problem")
    parser.add_argument("--test-inputs", type=str, nargs="+", help="Test inputs")
    parser.add_argument("--test-outputs", type=str, nargs="+", help="Expected test outputs")
    parser.add_argument("--output", type=str, default="solution.py", help="Output file for the solution (default: solution.py)")
    
    return parser.parse_args()

def create_problem_from_args(args):
    """Create a problem dictionary from command line arguments."""
    if not args.name or not args.description or not args.test_inputs or not args.test_outputs:
        print("Error: When not using a problem file, you must provide --name, --description, --test-inputs, and --test-outputs")
        sys.exit(1)
        
    if len(args.test_inputs) != len(args.test_outputs):
        print("Error: Number of test inputs must match number of test outputs")
        sys.exit(1)
        
    return {
        "name": args.name,
        "description": args.description,
        "public_tests": {
            "input": args.test_inputs,
            "output": args.test_outputs
        }
    }

def load_problem_from_file(file_path):
    """Load a problem from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            problem = json.load(f)
            
        # Validate the problem format
        if "name" not in problem or "description" not in problem or "public_tests" not in problem:
            print("Error: Problem file must contain 'name', 'description', and 'public_tests' fields")
            sys.exit(1)
            
        # Convert public_tests to the expected format if needed
        if isinstance(problem["public_tests"], list):
            inputs = []
            outputs = []
            for test in problem["public_tests"]:
                if "input" not in test or "output" not in test:
                    print("Error: Each test case must have 'input' and 'output' fields")
                    sys.exit(1)
                inputs.append(test["input"])
                outputs.append(test["output"])
            problem["public_tests"] = {
                "input": inputs,
                "output": outputs
            }
            
        return problem
    except Exception as e:
        print(f"Error loading problem file: {e}")
        sys.exit(1)

def main():
    """Main function."""
    args = parse_arguments()
    
    # Create or load the problem
    if args.problem:
        problem = load_problem_from_file(args.problem)
    else:
        problem = create_problem_from_args(args)
    
    print(f"Solving problem: {problem['name']}")
    print(f"Description: {problem['description']}")
    print(f"Number of test cases: {len(problem['public_tests']['input'])}")
    
    # Initialize the problem solver
    solver = ProblemSolver()
    
    # Solve the problem
    print("\nGenerating solution...")
    solution = solver.solve_problem(problem)
    
    # Save the solution
    with open(args.output, "w") as f:
        f.write(solution)
    
    print(f"\nSolution saved to {args.output}")
    
    # Print a summary of the solution
    print("\nSolution Summary:")
    print("=" * 40)
    lines = solution.split("\n")
    for line in lines[:10]:  # Print first 10 lines
        print(line)
    if len(lines) > 10:
        print("...")
    print("=" * 40)
    
    print(f"\nTotal solution length: {len(solution)} characters, {len(lines)} lines")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())