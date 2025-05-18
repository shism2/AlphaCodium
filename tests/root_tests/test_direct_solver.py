from direct_solver import DirectSolver

# Create a simple test problem
test_problem = {
    "name": "Factorial",
    "description": "Write a function called factorial that takes a non-negative integer n as input and returns n!. The factorial of n is the product of all positive integers less than or equal to n.",
    "public_tests": [
        {"input": "5", "output": "120"},
        {"input": "0", "output": "1"},
        {"input": "1", "output": "1"},
        {"input": "10", "output": "3628800"}
    ]
}

def main():
    # Initialize the direct solver
    solver = DirectSolver()
    
    # Solve the problem
    print(f"Solving problem: {test_problem['name']}")
    solution = solver.solve_problem(test_problem)
    
    # Print the solution
    print("\nGenerated Solution:")
    print("=" * 40)
    print(solution)
    print("=" * 40)
    
    # Save the solution to a file
    with open("direct_solution.py", "w") as f:
        f.write(solution)
    
    print("\nSolution saved to direct_solution.py")
    
    # Test the solution
    print("\nTesting the solution...")
    try:
        # Create a temporary namespace to execute the solution
        namespace = {}
        exec(solution, namespace)
        
        # Test each test case
        for i, test in enumerate(test_problem["public_tests"]):
            input_val = eval(test["input"])
            expected_output = eval(test["output"])
            actual_output = namespace["factorial"](input_val)
            
            result = "✓" if actual_output == expected_output else "✗"
            print(f"Test {i+1}: factorial({input_val}) = {actual_output}, Expected: {expected_output} {result}")
    except Exception as e:
        print(f"Error testing solution: {e}")

if __name__ == "__main__":
    main()