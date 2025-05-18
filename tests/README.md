# Tests Directory

This directory contains all tests for the AlphaCodium project.

## Structure

- `alpha_codium/`: Tests for the alpha_codium package
- `root_tests/`: Tests that were originally in the root directory

## Root Tests

The `root_tests` directory contains tests that were originally in the root directory:

- `test_custom_adapter.py`: Tests for the custom JSON adapter
- `test_genai_simple.py`: Simple tests for the Google GenAI SDK
- `test_simplified.py`: Tests for the simplified AlphaCodium implementation
- `test_gemini2.py`: Tests for the Gemini 2.0 integration

## Running Tests

To run a specific test:

```bash
# From the root directory
python -m tests.root_tests.test_simplified
```

To run all tests:

```bash
# From the root directory
python -m unittest discover tests
```

## Adding New Tests

When adding new tests, please follow these guidelines:

1. Place tests for the `alpha_codium` package in the `tests/alpha_codium` directory
2. Place general tests in the `tests/root_tests` directory
3. Use meaningful names for test files and test functions
4. Include docstrings that explain what the test is checking
5. Use assertions to verify expected behavior