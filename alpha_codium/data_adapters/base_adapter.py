from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

from datasets import Dataset, DatasetDict


class DatasetAdapter(ABC):
    """
    Base class for dataset adapters.
    Each adapter should convert a specific dataset format to the format expected by AlphaCodium.
    """

    @abstractmethod
    def load_dataset(self, dataset_location: str) -> DatasetDict:
        """
        Load a dataset from the given location.
        
        Args:
            dataset_location: Path to the dataset
            
        Returns:
            A DatasetDict containing the dataset
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def get_problem_count(self, ds: DatasetDict, split_name: str) -> int:
        """
        Get the number of problems in a split.
        
        Args:
            ds: The dataset
            split_name: Name of the split
            
        Returns:
            Number of problems in the split
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def get_splits(self, ds: DatasetDict) -> List[str]:
        """
        Get the names of all splits in the dataset.
        
        Args:
            ds: The dataset
            
        Returns:
            A list of split names
        """
        pass