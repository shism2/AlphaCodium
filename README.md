# Code Generation with AlphaCodium: From Prompt Engineering to Flow Engineering

[Paper](https://arxiv.org/abs/2401.08500) |
[Dataset](https://huggingface.co/datasets/talrid/CodeContests_valid_and_test_AlphaCodium/blob/main/codecontests_valid_and_test_processed_alpha_codium.zip)

Official Implementation
> Tal Ridnik, Dedy Kredo, Itamar Friedman <br/> CodiumAI

## Table of Contents
- [Abstract](#abstract)
- [Installation](#installation)
- [Project Structure](#project-structure)
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

## Project Structure

The AlphaCodium codebase is organized as follows:

```
AlphaCodium/
├── alpha_codium/         # Core implementation of AlphaCodium
│   ├── cli/              # Command-line interface scripts
│   ├── code_contests/    # Code contests dataset handling
│   ├── data_adapters/    # Data adapters for different dataset formats
│   ├── db/               # Database management for solutions
│   ├── gen/              # Core generation components
│   │   ├── stages/       # Different stages of the solution process
│   ├── llm/              # LLM integration components
│   ├── log/              # Logging utilities
│   └── settings/         # Configuration settings
├── scripts/              # Utility scripts for running AlphaCodium
├── tests/                # Test files
│   └── root_tests/       # Tests from the root directory
└── sample_problems/      # Example problems for testing
```

### Scripts Directory

The `scripts/` directory contains utility scripts for running AlphaCodium:

- `solve.py`: Unified command-line interface for solving programming problems
- `solve_problem.py`: Command-line interface for solving a single problem
- `list_models.py`: List available LLM models
- `setup_gemini.py`: Set up Gemini API key
- `gemini2_solver.py`: Solve problems using Gemini 2.0 models
- `web_interface.py`: Web interface for solving problems

### Alpha Codium CLI Directory

The `alpha_codium/cli/` directory contains command-line interface scripts:

- `solve_dataset.py`: Solve a dataset of problems
- `solve_problem.py`: Solve a single problem from a dataset
- `solve_user_problem.py`: Solve a user-provided problem

## How to run

### Web Interface

You can use the web interface to solve programming problems:

```bash
# From the root directory
python scripts/web_interface.py
```

Then open your browser to http://localhost:12000

### Command Line Interface

You can use the command line interface to solve programming problems:

#### Using the scripts directory:

```bash
# From the root directory
python scripts/solve_problem.py --problem sample_problems/factorial.json
```

Or specify the problem details directly:

```bash
python scripts/solve_problem.py --name "Factorial" --description "Write a function to calculate factorial" --test-inputs "5" "0" --test-outputs "120" "1" --output factorial_solution.py
```

#### Using the alpha_codium CLI:

```bash
# From the root directory
python -m alpha_codium.cli.solve_problem --problem_name "factorial"
```

```bash
# Solve an entire dataset
python -m alpha_codium.cli.solve_dataset --dataset_name "valid_and_test_processed"
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