#!/usr/bin/env python3
"""
AlphaCodium - Unified Problem Solver

This script provides a unified command-line interface for solving programming problems
using the AlphaCodium approach with Gemini 2.0 models.
"""

import argparse
import json
import os
import sys
import time
from alpha_codium.simplified_solver import SimplifiedSolver
from alpha_codium.llm.model_manager import ModelManager
from alpha_codium.log import setup_logger

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Solve programming problems using AlphaCodium with Gemini 2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Solve a problem from a JSON file
  python solve.py --problem sample_problems/fibonacci.json
  
  # Solve a problem with command-line arguments
  python solve.py --name "Sum Two Numbers" --description "Write a function that adds two numbers" \\
                  --test-inputs "1 2" "5 7" --test-outputs "3" "12"
  
  # Save the solution to a specific file
  python solve.py --problem sample_problems/fibonacci.json --output fibonacci_solution.py
  
  # List available models
  python solve.py --list-models
  
  # Use a specific model
  python solve.py --problem sample_problems/fibonacci.json --model "gemini-2.0-pro"
"""
    )
    
    # Input options
    input_group = parser.add_argument_group('Input Options')
    input_group.add_argument("--problem", type=str, help="Path to a JSON file containing the problem description")
    input_group.add_argument("--name", type=str, help="Name of the problem")
    input_group.add_argument("--description", type=str, help="Description of the problem")
    input_group.add_argument("--test-inputs", type=str, nargs="+", help="Test inputs")
    input_group.add_argument("--test-outputs", type=str, nargs="+", help="Expected test outputs")
    
    # Model options
    model_group = parser.add_argument_group('Model Options')
    model_group.add_argument("--list-models", action="store_true", help="List available Gemini models")
    model_group.add_argument("--model", type=str, help="Specify the model to use (e.g., gemini-2.0-flash)")
    model_group.add_argument("--refresh-models", action="store_true", help="Force refresh of the model cache")
    
    # Output options
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument("--output", type=str, help="Output file for the solution (default: generated_solution.py)")
    output_group.add_argument("--verbose", action="store_true", help="Show detailed output")
    
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
        "public_tests": [
            {"input": inp, "output": out} for inp, out in zip(args.test_inputs, args.test_outputs)
        ]
    }

def load_problem_from_file(file_path):
    """Load a problem from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            problem = json.load(f)
            
        # Basic validation
        if "name" not in problem or "description" not in problem:
            print("Error: Problem file must contain 'name' and 'description' fields")
            sys.exit(1)
            
        return problem
    except Exception as e:
        print(f"Error loading problem file: {e}")
        sys.exit(1)

def main():
    """Main function."""
    # Set up logging
    setup_logger()
    
    # Parse arguments
    args = parse_arguments()
    
    # Determine output file
    output_file = args.output
    if not output_file:
        if args.problem:
            # Use the problem name from the file
            problem_name = os.path.splitext(os.path.basename(args.problem))[0]
            output_file = f"{problem_name}_solution.py"
        else:
            output_file = "generated_solution.py"
    
    # Create or load the problem
    if args.problem:
        problem = load_problem_from_file(args.problem)
    else:
        problem = create_problem_from_args(args)
    
    print(f"Solving problem: {problem['name']}")
    print(f"Description: {problem['description']}")
    
    # Count test cases
    test_count = 0
    if "public_tests" in problem:
        if isinstance(problem["public_tests"], list):
            test_count = len(problem["public_tests"])
        elif isinstance(problem["public_tests"], dict) and "input" in problem["public_tests"]:
            test_count = len(problem["public_tests"]["input"])
    print(f"Number of test cases: {test_count}")
    
    # Initialize the problem solver
    solver = SimplifiedSolver()
    
    # Solve the problem
    print("\nGenerating solution...")
    start_time = time.time()
    solution = solver.solve_problem(problem)
    end_time = time.time()
    
    # Save the solution
    with open(output_file, "w") as f:
        f.write(solution)
    
    print(f"\nSolution saved to {output_file}")
    print(f"Solution generated in {end_time - start_time:.2f} seconds")
    
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