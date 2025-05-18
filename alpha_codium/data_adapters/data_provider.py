import os
from typing import Optional, Dict, Any, List

import duckdb
from datasets import Dataset, DatasetDict

from alpha_codium.data_adapters.adapter_factory import DatasetAdapterFactory
from alpha_codium.data_adapters.base_adapter import DatasetAdapter


class DataProvider:
    """
    Generic data provider that can work with any dataset format.
    Uses adapters to handle different dataset formats.
    """

    def __init__(self, dataset_location: str, dataset_format: str = 'auto', connection=None):
        """
        Initialize the data provider.
        
        Args:
            dataset_location: Path to the dataset
            dataset_format: Format of the dataset ('code_contests', 'custom_json', 'auto')
            connection: Optional DuckDB connection
        """
        self.dataset_location = dataset_location
        self.adapter = DatasetAdapterFactory.create_adapter(dataset_format, dataset_location)
        self.dataset = self.adapter.load_dataset(dataset_location)
        self.connection = connection or duckdb.connect()
        self.connect(self.dataset)

    def find_problem(self, problem_name: str, split_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Find a problem in the dataset.
        
        Args:
            problem_name: Name of the problem to find
            split_name: Name of the split to search in
            
        Returns:
            A dictionary containing the problem data
        """
        if split_name is None:
            # Try each split until we find the problem
            for split in self.get_splits():
                try:
                    return self.adapter.find_problem(self.dataset, problem_name, split)
                except ValueError:
                    continue
            raise ValueError(f"Problem {problem_name} not found in any split")
        else:
            return self.adapter.find_problem(self.dataset, problem_name, split_name)

    def get_problem_count(self, split_name: str) -> int:
        """
        Get the number of problems in a split.
        
        Args:
            split_name: Name of the split
            
        Returns:
            Number of problems in the split
        """
        return self.adapter.get_problem_count(self.dataset, split_name)

    def get_problem_by_index(self, split_name: str, index: int) -> Dict[str, Any]:
        """
        Get a problem by its index in a split.
        
        Args:
            split_name: Name of the split
            index: Index of the problem
            
        Returns:
            A dictionary containing the problem data
        """
        return self.adapter.get_problem_by_index(self.dataset, split_name, index)

    def get_splits(self) -> List[str]:
        """
        Get the names of all splits in the dataset.
        
        Returns:
            A list of split names
        """
        return self.adapter.get_splits(self.dataset)

    def connect(self, ds: DatasetDict):
        """
        Register the dataset with DuckDB for SQL queries.
        
        Args:
            ds: The dataset to register
        """
        if hasattr(ds, "keys"):
            for split in ds.keys():
                split_ds = ds[split]
                table = split_ds.data.table
                self.connection.register(f"{split_ds.info.dataset_name}_{split}", table)
        else:
            self.connection.register(f"{ds.info.dataset_name}", ds.data.table)