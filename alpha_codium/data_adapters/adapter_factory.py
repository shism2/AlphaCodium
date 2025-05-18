import os
from typing import Optional

from alpha_codium.data_adapters.base_adapter import DatasetAdapter
from alpha_codium.data_adapters.code_contests_adapter import CodeContestsAdapter
from alpha_codium.data_adapters.custom_adapter import CustomAdapter


class DatasetAdapterFactory:
    """
    Factory class for creating dataset adapters.
    """
    
    @staticmethod
    def create_adapter(dataset_format: str, dataset_location: Optional[str] = None) -> DatasetAdapter:
        """
        Create an adapter for the specified dataset format.
        
        Args:
            dataset_format: Format of the dataset ('code_contests', 'custom_json', etc.)
            dataset_location: Path to the dataset (used for format detection if needed)
            
        Returns:
            An appropriate DatasetAdapter instance
        """
        if dataset_format == 'code_contests':
            return CodeContestsAdapter()
        elif dataset_format == 'custom_json':
            return CustomAdapter()
        else:
            # Try to detect the format based on the file extension
            if dataset_location:
                _, ext = os.path.splitext(dataset_location)
                if ext.lower() == '.json':
                    return CustomAdapter()
            
            # Default to CodeContests format
            return CodeContestsAdapter()