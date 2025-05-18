# Using Custom Datasets with AlphaCodium

This guide explains how to use custom datasets with AlphaCodium.

## Custom Dataset Format

AlphaCodium now supports custom datasets in JSON format. The expected format is:

```json
{
  "split_name": [
    {
      "name": "problem_name",
      "description": "problem description",
      "public_tests": {
        "input": ["test input 1", "test input 2", ...],
        "output": ["expected output 1", "expected output 2", ...]
      },
      "private_tests": {
        "input": ["test input 1", "test input 2", ...],
        "output": ["expected output 1", "expected output 2", ...]
      },
      "solutions": {
        "language": ["python", ...],
        "solution": ["solution code", ...]
      }
    },
    ...
  ],
  ...
}
```

Where:
- `split_name` is the name of the dataset split (e.g., "train", "valid", "test")
- Each problem has:
  - `name`: A unique identifier for the problem
  - `description`: The problem statement
  - `public_tests`: Test cases that are visible to the model
  - `private_tests`: Test cases that are used for evaluation but not shown to the model
  - `solutions`: Example solutions to the problem (optional)

## Example Usage

### Solving a Single Problem

To solve a single problem from a custom dataset:

```bash
python -m alpha_codium.solve_problem \
  --dataset_name /path/to/your/dataset.json \
  --dataset_format custom_json \
  --split_name test \
  --problem_number 0
```

You can also specify a problem by name:

```bash
python -m alpha_codium.solve_problem \
  --dataset_name /path/to/your/dataset.json \
  --dataset_format custom_json \
  --split_name test \
  --problem_name "problem_name"
```

### Solving an Entire Dataset

To solve all problems in a dataset split:

```bash
python -m alpha_codium.solve_dataset \
  --dataset_name /path/to/your/dataset.json \
  --dataset_format custom_json \
  --split_name test \
  --database_solution_path /path/to/output/solutions.json
```

### Evaluating Solutions

To evaluate the solutions:

```bash
python -m alpha_codium.evaluate_dataset \
  --dataset_name /path/to/your/dataset.json \
  --dataset_format custom_json \
  --split_name test \
  --database_solution_path /path/to/output/solutions.json
```

## Example Custom Dataset

An example custom dataset is provided in the repository as `example_custom_dataset.json`. You can use it to test the functionality:

```bash
python -m alpha_codium.solve_problem \
  --dataset_name example_custom_dataset.json \
  --dataset_format custom_json \
  --split_name test \
  --problem_number 0
```

## Dataset Format Detection

If you don't specify a dataset format, AlphaCodium will try to detect it automatically:
- If the dataset path ends with `.json`, it will be treated as a custom JSON dataset
- Otherwise, it will be treated as a CodeContests dataset

You can always explicitly specify the format using the `--dataset_format` parameter.