import json
import os
from typing import Dict, Any, List, Optional

from datasets import Dataset, DatasetDict

from alpha_codium.data_adapters.base_adapter import DatasetAdapter


class CustomAdapter(DatasetAdapter):
    """
    Adapter for custom datasets.
    This adapter can handle JSON files with a custom format.
    
    Expected format:
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
    """

    def load_dataset(self, dataset_location: str) -> DatasetDict:
        """
        Load a custom dataset from a JSON file.
        
        Args:
            dataset_location: Path to the JSON file
            
        Returns:
            A DatasetDict containing the dataset
        """
        if not os.path.exists(dataset_location):
            raise FileNotFoundError(f"Dataset file not found: {dataset_location}")
        
        with open(dataset_location, 'r') as f:
            data = json.load(f)
        
        dataset_dict = {}
        for split_name, problems in data.items():
            dataset_dict[split_name] = Dataset.from_list(problems)
        
        return DatasetDict(dataset_dict)

    def find_problem(self, ds: DatasetDict, problem_name: str, split_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Find a problem in the dataset.
        
        Args:
            ds: The dataset
            problem_name: Name of the problem to find
            split_name: Name of the split to search in
            
        Returns:
            A dictionary containing the problem data
        """
        if split_name:
            ds = ds[split_name]
        
        if not problem_name:
            # Return the first problem if no name is provided
            for example in ds:
                return example
        else:
            # Filter by problem name
            problems = ds.filter(lambda example: example['name'] == problem_name)
            if len(problems) > 0:
                # Convert to list to get the first item
                problem_list = list(problems)
                if problem_list:
                    return problem_list[0]
            
            raise ValueError(
                f"Problem with name {problem_name} doesn't exist in dataset in split {split_name}"
            )

    def get_problem_count(self, ds: DatasetDict, split_name: str) -> int:
        """
        Get the number of problems in a split.
        
        Args:
            ds: The dataset
            split_name: Name of the split
            
        Returns:
            Number of problems in the split
        """
        return len(ds[split_name])

    def get_problem_by_index(self, ds: DatasetDict, split_name: str, index: int) -> Dict[str, Any]:
        """
        Get a problem by its index in a split.
        
        Args:
            ds: The dataset
            split_name: Name of the split
            index: Index of the problem
            
        Returns:
            A dictionary containing the problem data
        """
        return ds[split_name][index]

    def get_splits(self, ds: DatasetDict) -> List[str]:
        """
        Get the names of all splits in the dataset.
        
        Args:
            ds: The dataset
            
        Returns:
            A list of split names
        """
        return list(ds.keys())