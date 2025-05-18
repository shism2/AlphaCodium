import asyncio
import json
from alpha_codium.gen.problem_solver import ProblemSolver

# Create a simple test problem
test_problem = {
    "name": "Factorial",
    "description": "Write a function called factorial that takes a non-negative integer n as input and returns n!. The factorial of n is the product of all positive integers less than or equal to n.",
    "public_tests": {
        "input": ["5", "0", "1", "10"],
        "output": ["120", "1", "1", "3628800"]
    }
}

async def main():
    # Initialize the problem solver
    solver = ProblemSolver()
    
    # Solve the problem
    print(f"Solving problem: {test_problem['name']}")
    solution = await solver.solve(test_problem)
    
    # Print the solution
    print("\nGenerated Solution:")
    print("=" * 40)
    print(solution)
    print("=" * 40)
    
    # Save the solution to a file
    with open("generated_solution.py", "w") as f:
        f.write(solution)
    
    print("\nSolution saved to generated_solution.py")

if __name__ == "__main__":
    asyncio.run(main())