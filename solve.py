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
from alpha_codium.db.database_manager import DatabaseManager
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
    
    # Database options
    db_group = parser.add_argument_group('Database Options')
    db_group.add_argument("--db-path", type=str, help="Path to the SQLite database file")
    db_group.add_argument("--stats", action="store_true", help="Show database statistics and exit")
    db_group.add_argument("--recent", type=int, nargs="?", const=10, help="Show recent problems and exit (default: 10)")
    db_group.add_argument("--no-cache", action="store_true", help="Don't use cached solutions")
    
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

def display_models(model_manager, refresh=False):
    """Display available models."""
    print("Retrieving available Gemini models...")
    models = model_manager.get_available_models(force_refresh=refresh)
    
    if not models:
        print("No models found. Please check your Gemini API key.")
        return
    
    print("\nAvailable Gemini Models:")
    print("=" * 80)
    print(f"{'Model ID':<40} {'Display Name':<25} {'Token Limit':<15}")
    print("-" * 80)
    
    for model in models:
        model_id = model.get("id", "").replace("models/", "")
        display_name = model.get("display_name", "")
        token_limit = f"{model.get('input_token_limit', 0):,}"
        
        print(f"{model_id:<40} {display_name:<25} {token_limit:<15}")
    
    print("=" * 80)
    print(f"\nTotal models: {len(models)}")
    print("\nRecommended models for code generation:")
    
    recommended = model_manager.get_recommended_models()
    for i, model in enumerate(recommended[:5], 1):
        model_id = model.get("id", "").replace("models/", "")
        print(f"  {i}. {model_id}")

def display_stats(db_manager):
    """Display database statistics."""
    print("Retrieving database statistics...")
    stats = db_manager.get_statistics()
    
    print("\nAlphaCodium Database Statistics:")
    print("=" * 80)
    print(f"Total problems: {stats['problem_count']}")
    print(f"Total solutions: {stats['solution_count']}")
    print(f"Success rate: {stats['success_rate']:.2f}%")
    print(f"Average execution time: {stats['avg_execution_time']:.2f} seconds")
    print(f"Total models: {stats['model_count']}")
    
    if stats['most_used_model']:
        print(f"Most used model: {stats['most_used_model']} ({stats['most_used_model_count']} uses)")
    
    print("=" * 80)

def display_recent_problems(db_manager, limit=10):
    """Display recent problems."""
    print(f"Retrieving {limit} most recent problems...")
    problems = db_manager.get_recent_problems(limit=limit)
    
    if not problems:
        print("No problems found in the database.")
        return
    
    print(f"\nRecent Problems ({len(problems)}):")
    print("=" * 80)
    print(f"{'ID':<5} {'Name':<30} {'Test Cases':<10} {'Solutions':<10} {'Last Updated':<20}")
    print("-" * 80)
    
    for problem in problems:
        # Get solution count for this problem
        solutions = db_manager.get_solutions_for_problem(problem['id'])
        
        # Format the date
        updated_at = problem.get('updated_at', '')
        if updated_at:
            try:
                # Try to parse the date string
                if isinstance(updated_at, str):
                    updated_at = updated_at.split('.')[0]  # Remove microseconds
            except:
                pass
        
        print(f"{problem['id']:<5} {problem['name'][:28]:<30} {len(problem['public_tests']):<10} {len(solutions):<10} {updated_at:<20}")
    
    print("=" * 80)

def main():
    """Main function."""
    # Set up logging
    setup_logger()
    
    # Parse arguments
    args = parse_arguments()
    
    # Initialize database manager
    db_manager = DatabaseManager(db_path=args.db_path)
    
    # Handle database statistics
    if args.stats:
        display_stats(db_manager)
        return 0
    
    # Handle recent problems
    if args.recent is not None:
        display_recent_problems(db_manager, limit=args.recent)
        return 0
    
    # Initialize model manager
    model_manager = ModelManager()
    
    # Handle model listing
    if args.list_models:
        display_models(model_manager, refresh=args.refresh_models)
        return 0
    
    # Check if we have a problem to solve
    if not args.problem and not (args.name and args.description and args.test_inputs and args.test_outputs):
        print("Error: You must provide either a problem file or all of: name, description, test inputs, and test outputs")
        print("For help, run: python solve.py --help")
        return 1
    
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
    
    # Initialize the problem solver with the specified model
    solver = SimplifiedSolver(model_id=args.model, db_path=args.db_path)
    
    # Display the model being used
    print(f"\nUsing model: {solver.model}")
    
    # Solve the problem
    print("\nGenerating solution...")
    print(f"Using solution cache: {'No' if args.no_cache else 'Yes'}")
    
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