# AlphaCodium Scripts

This directory contains command-line scripts for using AlphaCodium.

## Available Scripts

- `solve.py`: Unified command-line interface for solving programming problems
- `solve_problem.py`: Command-line interface for solving a single programming problem
- `list_models.py`: List available Gemini models
- `setup_gemini.py`: Set up Gemini API key
- `gemini2_solver.py`: Solve problems using Gemini 2.0 models
- `web_interface.py`: Web interface for solving programming problems

## Usage

Run the scripts from the root directory of the project:

```bash
python scripts/solve.py --problem sample_problems/factorial.json
```

Or make them executable and run them directly:

```bash
chmod +x scripts/solve.py
./scripts/solve.py --problem sample_problems/factorial.json
```