# Code Generation with AlphaCodium: From Prompt Engineering to Flow Engineering

[Paper](https://arxiv.org/abs/2401.08500) |
[Dataset](https://huggingface.co/datasets/talrid/CodeContests_valid_and_test_AlphaCodium/blob/main/codecontests_valid_and_test_processed_alpha_codium.zip)

Official Implementation
> Tal Ridnik, Dedy Kredo, Itamar Friedman <br/> CodiumAI

## Table of Contents
- [Abstract](#abstract)
- [Installation](#installation)
- [How to run](#how-to-run)
  - [Web Interface](#web-interface)
  - [Command Line Interface](#command-line-interface)
  - [Python API](#python-api)
- [Gemini 2.0 Integration](#gemini-20-integration)
- [Technical Q&A](#technical-qa)
- [Broader Applicability](#broader-applicability)
- [Example Problem](#example-problem)
- [How It Works](#how-it-works)
- [Configuration](#configuration)
- [Acknowledgments](#acknowledgments)
- [Citation](#citation)

## Abstract

*Copy the abstract from the original README.md*

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Set up your Gemini API key (if using Gemini models):

```bash
python setup_gemini.py
```

*Add more installation instructions from the original README.md*

## How to run

### Web Interface

You can use the web interface to solve programming problems:

```bash
python web_interface.py
```

Then open your browser to http://localhost:12000

### Command Line Interface

You can use the command line interface to solve programming problems:

```bash
python solve_problem.py --problem sample_problems/factorial.json
```

Or specify the problem details directly:

```bash
python solve_problem.py --name "Factorial" --description "Write a function to calculate factorial" --test-inputs "5" "0" --test-outputs "120" "1" --output factorial_solution.py
```

### Python API

You can use the Python API to solve programming problems in your own code:

```python
from alpha_codium.simplified_solver import SimplifiedSolver

# Create a problem
problem = {
    "name": "Factorial",
    "description": "Write a function called factorial that takes a non-negative integer n as input and returns n!.",
    "public_tests": {
        "input": ["5", "0", "1", "10"],
        "output": ["120", "1", "1", "3628800"]
    }
}

# Initialize the solver
solver = SimplifiedSolver()

# Solve the problem
solution = solver.solve_problem(problem)

print(solution)
```

## Gemini 2.0 Integration

AlphaCodium now supports Google's Gemini 2.0 models for all stages of the solution process. The implementation has been streamlined to focus on the core functionality and remove unnecessary complexity.

### Features

- Uses Gemini 2.0 models for all stages of the solution process
- Simplified API for solving programming problems
- Improved error handling for API key and model availability issues
- Streamlined implementation that focuses on the core functionality

### Setup for Gemini 2.0

1. Set up your Gemini API key:

```bash
python setup_gemini.py
```

2. List available Gemini models:

```bash
python list_models.py
```

3. Use the Gemini 2.0 solver:

```bash
python gemini2_solver.py --problem sample_problems/factorial.json
```

*Add more content from README_GEMINI2.md*

## Technical Q&A

*Copy the Technical Q&A section from the original README.md*

## Broader Applicability

*Copy the Broader Applicability section from the original README.md*

## Example Problem

*Copy the Example Problem section from the original README.md*

## How It Works

AlphaCodium is a test-based, multi-stage, code-oriented iterative flow that improves the performance of LLMs on code problems. The process involves:

1. Problem analysis
2. Test generation
3. Initial solution generation
4. Test evaluation
5. Solution refinement
6. Final solution selection

*Add more details from README_SIMPLIFIED.md*

## Configuration

*Copy the Configuration section from README_SIMPLIFIED.md*

## Acknowledgments

*Copy the Acknowledgments section from the original README.md*

## Citation

*Copy the Citation section from the original README.md*