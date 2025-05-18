#!/usr/bin/env python3

import json
from alpha_codium.data_adapters.data_provider import DataProvider

def main():
    # Test with custom JSON dataset
    print("Testing custom JSON dataset...")
    data_provider = DataProvider(dataset_location="example_custom_dataset.json", dataset_format="custom_json")
    
    # Get splits
    splits = data_provider.get_splits()
    print(f"Splits: {splits}")
    
    # Get problem count
    for split in splits:
        count = data_provider.get_problem_count(split)
        print(f"Problem count in {split}: {count}")
    
    # Get problem by index
    problem = data_provider.get_problem_by_index("test", 0)
    print(f"Problem 0 name: {problem['name']}")
    print(f"Problem 0 description: {problem['description'][:50]}...")
    
    # Find problem by name
    problem = data_provider.find_problem("custom_problem_1")
    print(f"Found problem: {problem['name']}")
    
    # Print public tests
    print(f"Public tests input: {problem['public_tests']['input'][:2]}")
    print(f"Public tests output: {problem['public_tests']['output'][:2]}")
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    main()