"""
Run with:
./scripts/main.bat inputs/input_file.txt outputs/output_file.txt 1NF
or
python3 main.py --input_file=inputs/input.txt --output_file=outputs/output.txt --normal_form=0NF
"""

import argparse
from modules import preprocess, relation
from typing import List


def zero_nf(relations: List[relation.relation]) -> List[relation.relation]:
    return relations


def first_nf(relations: List[relation.relation]) -> List[relation.relation]:
    for original_relation in relations.copy():
        current_relation = original_relation
        while current_relation.multivalued_attrs:
            mva = current_relation.multivalued_attrs[0]
            decomposed_name = (
                f"{current_relation.name.removesuffix('Data')}{mva}Data"
                if current_relation.name.endswith("Data")
                else f"{mva}{current_relation.name}"
            )
            current_relation, decomposed_relation = current_relation.decompose(
                [mva],
                omit=list(set(current_relation.multivalued_attrs) - {mva}),
                name=decomposed_name,
            )
            decomposed_relation.split_mva(mva)
    return relations


def second_nf(relations: List[relation.relation]) -> List[relation.relation]:
    return relations


def third_nf(relations: List[relation.relation]) -> List[relation.relation]:
    return relations


def bcnf(relations: List[relation.relation]) -> List[relation.relation]:
    return relations


def fourth_nf(relations: List[relation.relation]) -> List[relation.relation]:
    return relations


def fifth_nf(relations: List[relation.relation]) -> List[relation.relation]:
    return relations


normal_forms = {
    "0NF": zero_nf,
    "1NF": first_nf,
    "2NF": second_nf,
    "3NF": third_nf,
    "BCNF": bcnf,
    "4NF": fourth_nf,
    "5NF": fifth_nf,
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

    if args.output_file:
        output = ""
        with open(args.output_file, "w") as file:
            for current_relation in relations:
                output += str(current_relation)
            file.write(output.removesuffix("\n\n"))
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
    parser.add_argument(
        "--normal_form",
        type=str,
        required=True,
        help="Normal form to normalize the input file to - 1NF, 2NF, 3NF, BCNF, 4NF, or 5NF'",
    )
    main(parser.parse_args())
