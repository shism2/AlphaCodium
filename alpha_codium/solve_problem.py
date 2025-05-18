import argparse

from alpha_codium.gen.coding_competitor import solve_problem
from alpha_codium.log import setup_logger
from alpha_codium.settings.config_loader import get_settings

parser = argparse.ArgumentParser()
parser.add_argument("--dataset_name", type=str, default="valid_and_test_processed",
                   help="Path to the dataset file or directory")
parser.add_argument("--dataset_format", type=str, default="auto",
                   help="Format of the dataset: 'code_contests', 'custom_json', or 'auto'")
parser.add_argument("--split_name", type=str, default="valid",
                   help="Name of the dataset split to use")
parser.add_argument("--problem_number", type=int, default=0,
                   help="Index of the problem to solve (zero-based)")
parser.add_argument("--problem_name", type=str, default="",
                   help="Name of the problem to solve (takes precedence over problem_number)")

if __name__ == "__main__":
    args = parser.parse_args()
    setup_logger()
    solve_problem(dataset_name=args.dataset_name,
                  dataset_format=args.dataset_format,
                  split_name=args.split_name,
                  problem_number=args.problem_number,
                  problem_name=args.problem_name)
