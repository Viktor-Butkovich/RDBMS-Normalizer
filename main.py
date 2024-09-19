"""
Run with python3 main.py --input_file=<file_name in inputs directory>.txt
python3 main.py --input_file=1NF_test_1.txt=
"""

import argparse
from modules import preprocess
from typing import List


def main(args: List[str]):
    relations = preprocess.process_input(args.input_file)
    for current_relation in relations:
        current_relation.verify_sql()
        print(current_relation)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Normalize the relations from the inputted .txt file"
    )
    parser.add_argument(
        "--input_file",
        type=str,
        required=True,
        help="Name of the .txt file in the inputs folder",
    )
    main(parser.parse_args())
