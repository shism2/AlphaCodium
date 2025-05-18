# AlphaCodium: Simplified

This is a simplified version of AlphaCodium that focuses on solving programming problems using Google Gemini models. The codebase has been streamlined to make it easier to use and understand.

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
  - [Web Interface](#web-interface)
  - [Command Line Interface](#command-line-interface)
  - [Python API](#python-api)
- [How It Works](#how-it-works)
- [Configuration](#configuration)

## Overview

AlphaCodium is a test-based, multi-stage, code-oriented iterative flow that improves the performance of LLMs on code problems. This simplified version removes redundant code and focuses on the core functionality, making it easier to use for solving any programming problem.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AlphaCodium.git
cd AlphaCodium
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Set up your Gemini API key:
```bash
python setup_gemini.py
```

## Usage

### Web Interface

The simplest way to use AlphaCodium is through the web interface:

```bash
python web_interface.py
```

Then open your browser and go to http://localhost:12000 to access the interface.

### Command Line Interface

You can also use AlphaCodium from the command line:

```bash
python -m alpha_codium.solve_user_problem \
  --problem_description "Write a function that calculates the factorial of a number." \
  --test_inputs "5" "0" \
  --test_outputs "120" "1" \
  --problem_name "Factorial" \
  --output_file "factorial_solution.py"
```

### Python API

You can use AlphaCodium in your Python code:

```python
from alpha_codium.solve_user_problem import solve_user_problem

solution = solve_user_problem(
    problem_description="Write a function that calculates the factorial of a number.",
    test_inputs=["5", "0"],
    test_outputs=["120", "1"],
    problem_name="Factorial"
)

print(solution)
```

## How It Works

AlphaCodium uses a multi-stage approach to solve programming problems:

1. **Self-reflection**: Analyze the problem and identify key requirements
2. **Generate possible solutions**: Create multiple solution approaches
3. **Choose the best solution**: Select the most promising approach
4. **Generate AI tests**: Create additional test cases to validate the solution
5. **Initial code generation**: Implement the chosen solution
6. **Evaluate on public tests**: Test the solution against the provided test cases
7. **Evaluate on AI tests**: Test the solution against the AI-generated test cases

This approach leads to more robust and accurate solutions compared to a single-prompt approach.

## Configuration

You can configure AlphaCodium by editing the `alpha_codium/settings/configuration.toml` file. The main settings are:

- `model`: The Gemini model to use (default is now "gemini-2.0-flash")
- `ai_timeout`: Maximum time (in seconds) to wait for the AI model to respond
- `verbosity_level`: Level of logging detail (0, 1, or 2)

For more advanced configuration options, see the comments in the configuration file.

## Updates

The codebase has been updated to:

1. **Use Gemini 2.0 models**: The default model is now "gemini-2.0-flash"
2. **Simplified API**: The API has been streamlined for easier use
3. **Improved web interface**: The web interface now provides a better user experience
4. **Better error handling**: More robust error handling for API failures
5. **New command-line interface**: Added `solve_problem.py` for a more user-friendly experience

### New Command-line Interface

You can now use the new command-line interface to solve problems:

```bash
python solve_problem.py --problem sample_problems/fibonacci.json --output fibonacci_solution.py
```

Or specify the problem details directly:

```bash
python solve_problem.py --name "Factorial" \
                       --description "Write a function called factorial that takes a non-negative integer n as input and returns n!." \
                       --test-inputs "0" "1" "5" "10" \
                       --test-outputs "1" "1" "120" "3628800" \
                       --output factorial_solution.py
```

To test the implementation, run:
```bash
python test_simple.py
```