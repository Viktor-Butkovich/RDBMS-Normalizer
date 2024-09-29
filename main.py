"""
Run with:
./scripts/main.bat inputs/input_file.txt outputs/output_file.txt 1NF
or
python3 main.py --input_file=inputs/input.txt --output_file=outputs/output.txt --normal_form=0NF --output=SQL
Test scripts:
.\scripts\convert_schema.bat inputs/0NF_test_1.txt outputs/0NF_target_1.txt 0NF
.\scripts\convert_schema.bat inputs/0NF_test_1.txt outputs/1NF_target_1.txt 1NF
.\scripts\convert_schema.bat inputs/1NF_test_1.txt outputs/2NF_target_1.txt 2NF
"""

import argparse
from modules import preprocess, normalize
from typing import List


normal_forms = {
    "0NF": normalize.zero_nf,
    "1NF": normalize.first_nf,
    "2NF": normalize.second_nf,
    "3NF": normalize.third_nf,
    "BCNF": normalize.bcnf,
    "4NF": normalize.fourth_nf,
    "5NF": normalize.fifth_nf,
}


def main(args: List[str]):
    if not args.normal_form in normal_forms.keys():
        raise ValueError(
            f"Invalid normal form {args.normal_form} - must be one of {normal_forms.keys()}"
        )

    relations = preprocess.process_input(args.input_file)
    for normal_form, function in normal_forms.items():
        relations = function(relations)
        if normal_form == args.normal_form:
            break

    if args.output_file and args.output_file != "stdio":
        output = ""
        with open(args.output_file, "w") as file:
            if args.target == "sql":
                for current_relation in relations:
                    for command in current_relation.to_sql():
                        output += command + "\n"
                    output += "\n"
            else:
                for current_relation in relations:
                    output += str(current_relation)
            file.write(output.removesuffix("\n\n"))
        print(f"Wrote output to {args.output_file}")
    else:
        for current_relation in relations:
            print(current_relation)
            for command in current_relation.to_sql():
                print(command)


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
    parser.add_argument(
        "--normal_form",
        type=str,
        required=True,
        help="Normal form to normalize the input file to - 1NF, 2NF, 3NF, BCNF, 4NF, or 5NF'",
    )
    parser.add_argument(
        "--target",
        type=str,
        required=False,
    )
    main(parser.parse_args())
