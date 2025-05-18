import os
from typing import Dict, Any, List, Optional

from datasets import Dataset, DatasetDict, load_dataset, load_from_disk

from alpha_codium.data_adapters.base_adapter import DatasetAdapter
from alpha_codium.settings.config_loader import get_settings


class CodeContestsAdapter(DatasetAdapter):
    """
    Adapter for the CodeContests dataset.
    This is the default dataset format used by AlphaCodium.
    """

    def __init__(self):
        self.private_datasets_root = os.path.expanduser(
            get_settings().config.private_dataset_cache_dir
        )

    def parse_location(self, dataset_location: str) -> tuple:
        """Parse the dataset location and determine how to load it."""
        result_location = dataset_location
        dataset_name = dataset_location.split(os.path.sep)[-1]
        load_from_disk = True
        if load_from_disk:
            if not result_location.startswith(os.path.sep):
                result_location = os.path.join(
                    self.private_datasets_root, result_location
                )
        return result_location, dataset_name, load_from_disk

    def load_dataset(self, dataset_location: str) -> DatasetDict:
        """Load the CodeContests dataset from disk or HuggingFace."""
        location, _, load_from_disk = self.parse_location(dataset_location)
        
        if load_from_disk:
            return load_from_disk(location)
        else:
            return load_dataset(location)

    def find_problem(self, ds: DatasetDict, problem_name: str, split_name: Optional[str] = None) -> Dict[str, Any]:
        """Find a problem by name in the dataset."""
        if split_name:
            ds = ds[split_name]
        
        if not problem_name:
            # Return the first problem if no name is provided
            for example in ds:
                return example
        else:
            # Filter by problem name
            problems = ds.filter(lambda example: example['name'] == problem_name)
            if problems:
                return problems[0]
            else:
                raise ValueError(
                    f"Problem with name {problem_name} doesn't exist in dataset in split {split_name}"
                )

    def get_problem_count(self, ds: DatasetDict, split_name: str) -> int:
        """Get the number of problems in a split."""
        return len(ds[split_name])

    def get_problem_by_index(self, ds: DatasetDict, split_name: str, index: int) -> Dict[str, Any]:
        """Get a problem by its index in a split."""
        return ds[split_name][index]

    def get_splits(self, ds: DatasetDict) -> List[str]:
        """Get the names of all splits in the dataset."""
        return list(ds.keys())