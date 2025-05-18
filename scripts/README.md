# AlphaCodium Scripts

This directory contains utility scripts for running AlphaCodium.

## Available Scripts

- `solve.py`: Unified command-line interface for solving programming problems using the AlphaCodium approach with Gemini 2.0 models.
- `solve_problem.py`: Command-line interface for solving a single problem using the AlphaCodium approach.
- `list_models.py`: List available LLM models that can be used with AlphaCodium.
- `setup_gemini.py`: Set up Gemini API key for use with AlphaCodium.
- `gemini2_solver.py`: Solve problems using Gemini 2.0 models.
- `web_interface.py`: Web interface for solving programming problems.

## Usage Examples

### Web Interface

```bash
# From the root directory
python scripts/web_interface.py
```

Then open your browser to http://localhost:12000

### Solve a Problem

```bash
# From the root directory
python scripts/solve_problem.py --problem sample_problems/factorial.json
```

Or specify the problem details directly:

```bash
python scripts/solve_problem.py --name "Factorial" --description "Write a function to calculate factorial" --test-inputs "5" "0" --test-outputs "120" "1" --output factorial_solution.py
```

### List Available Models

```bash
# From the root directory
python scripts/list_models.py
```

### Setup Gemini API Key

```bash
# From the root directory
python scripts/setup_gemini.py
```

### Make Scripts Executable

You can make the scripts executable and run them directly:

```bash
chmod +x scripts/solve.py
./scripts/solve.py --problem sample_problems/factorial.json
```

## Note

These scripts are provided for convenience and are designed to be run from the root directory of the AlphaCodium project. They provide a simplified interface to the core functionality of AlphaCodium.

For more advanced usage, consider using the Python API directly or the CLI modules in the `alpha_codium/cli` directory.