# AlphaCodium CLI Modules

This directory contains command-line interface modules for AlphaCodium.

## Available Modules

- `solve_dataset.py`: Command-line interface for solving a dataset of programming problems
- `solve_problem.py`: Command-line interface for solving a single programming problem from a dataset
- `solve_user_problem.py`: Command-line interface for solving a user-provided programming problem

## Usage

These modules can be run directly as Python modules:

```bash
# From the root directory
python -m alpha_codium.cli.solve_problem --problem_name "factorial"
```

```bash
# Solve an entire dataset
python -m alpha_codium.cli.solve_dataset --dataset_name "valid_and_test_processed"
```

```bash
# Solve a user-provided problem
python -m alpha_codium.cli.solve_user_problem --problem_description "Write a function to calculate factorial" --test_inputs "5" "0" --test_outputs "120" "1"
```

## Module Descriptions

### solve_dataset.py

This module provides functionality to solve an entire dataset of programming problems. It uses the `dataset_solver` module to solve each problem in the dataset.

### solve_problem.py

This module provides functionality to solve a single programming problem from a dataset. It uses the `coding_competitor` module to solve the problem.

### solve_user_problem.py

This module provides functionality to solve a user-provided programming problem. It allows users to specify the problem description, test inputs, and test outputs directly from the command line.

## Note

These modules are also imported and used by the scripts in the `scripts` directory. They provide the core functionality for the command-line interfaces.