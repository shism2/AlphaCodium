import argparse

from alpha_codium.gen.dataset_solver import solve_dataset
from alpha_codium.log import get_logger, setup_logger

logger = get_logger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument("--dataset_name", type=str, default="valid_and_test_processed",
                   help="Path to the dataset file or directory")
parser.add_argument("--dataset_format", type=str, default="auto",
                   help="Format of the dataset: 'code_contests', 'custom_json', or 'auto'")
parser.add_argument("--split_name", type=str, default="valid",
                   help="Name of the dataset split to use")
parser.add_argument("--database_solution_path", type=str, default="",
                   help="Path to save the solution database")

if __name__ == "__main__":
    args = parser.parse_args()
    setup_logger()

    # set default database_solution_path
    args.database_solution_path = args.database_solution_path
    if not args.database_solution_path:
        dataset_name_base = args.dataset_name.split('/')[-1].split('.')[0]
        args.database_solution_path = f"./{dataset_name_base}_{args.split_name}_solution_database.json"
        logger.info(f"args.database_solution_path: {args.database_solution_path}")

    solve_dataset(dataset_name=args.dataset_name,
                  dataset_format=args.dataset_format,
                  split_name=args.split_name,
                  database_solution_path=args.database_solution_path)
