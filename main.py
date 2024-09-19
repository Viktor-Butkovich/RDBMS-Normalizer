"""
Run with:
./scripts/main.bat inputs/input_file.txt outputs/output_file.txt
or
python3 main.py --input_file=inputs/input_file.txt --output_file=outputs/output_file.txt
"""

import argparse
from modules import preprocess
from typing import List


def main(args: List[str]):
    normalize_to, relations = preprocess.process_input(args.input_file)
    for current_relation in relations:
        current_relation.verify_sql()

    if args.output_file:
        output = ""
        with open(args.output_file, "w") as file:
            output = f"Normalize to: {normalize_to}\n\n"
            for current_relation in relations:
                output += str(current_relation)
            file.write(output)
        print(f"Wrote output to {args.output_file}")
    else:
        for current_relation in relations:
            print(current_relation)
            print(current_relation.to_sql())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Normalize the relations from the inputted .txt file"
    )
    parser.add_argument(
        "--input_file",
        type=str,
        required=True,
        help="Name of the .txt file to input, like 'inputs/1NF_test_1.txt'",
    )
    parser.add_argument(
        "--output_file",
        type=str,
        required=False,
        help="Name of the .txt file to output to, like 'outputs/1NF_output_1.txt'",
    )
    main(parser.parse_args())
