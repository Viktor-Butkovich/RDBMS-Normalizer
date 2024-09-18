"""
Run with python3 main.py --input_file=<file_name in inputs directory>.txt
python3 main.py --input_file=1NF_test_1.txt=
"""

import sqlite3
import argparse
from typing import List

valid_normal_forms = ["0NF", "1NF", "2NF", "3NF", "BCNF", "4NF", "5NF"]


class relation:
    def __init__(
        self,
        name: str,
        attrs: List[str],
        pk: List[str],
        candidate_keys: List[List[str]],
        multivalued_attrs: List[str] = None,
    ) -> None:
        self.name = name
        self.attrs = attrs
        self.pk = pk
        self.candidate_keys = candidate_keys
        self.multivalued_attrs = multivalued_attrs
        if not self.multivalued_attrs:
            self.multivalued_attrs = []


def read_input_file(file_path: str) -> List[str]:
    with open(file_path, "r") as file:
        data = file.read()
    return data


def process_input(input_file: str) -> None:
    input_data = read_input_file(f"inputs/{input_file}").split("\n")
    input_data = [line for line in input_data if line.strip()]  # Remove empty lines

    normalize_to = input_data.pop(0)
    if not normalize_to.startswith("Normalize to:"):
        raise ValueError("First line of input file must be 'Normalize to:'")
    normalize_to = normalize_to.removeprefix(
        "Normalize to:"
    ).strip()  # 0NF, 1NF, 2NF, etc.
    if not normalize_to in valid_normal_forms:
        if normalize_to == "":
            raise ValueError(
                f"Missing normal form - normal form must be in {valid_normal_forms}"
            )
        else:
            raise ValueError(
                f"Invalid normal form {normalize_to} - normal form must be in {valid_normal_forms}"
            )

    while input_data:
        extract_relation(input_data)


def extract_relation(input_data: List[str]) -> relation:
    if not input_data[0].startswith("Relation:"):
        raise ValueError(
            f"The first field in each relation must be 'Relation: <name>', not {input_data[0]}"
        )
    name = input_data.pop(0).split(":")[1].strip()
    input_dict = {"name": name}
    relation_fields = []
    while input_data and not input_data[0].startswith("Relation:"):
        relation_fields.append(input_data.pop(0))
    valid_fields = [
        "Attributes",
        "Primary key",
        "Candidate keys",
        "Multivalued attributes",
    ]
    for field in relation_fields:
        if not any([field.startswith(valid_field) for valid_field in valid_fields]):
            raise ValueError(f"Invalid field {field.split(':')[0]} in relation {name}")
        field_name = field.split(":")[0].strip()
        field_value = field.split(":")[1].strip()
        if field_name == "Attributes":
            field_value = [attr.strip() for attr in field_value.split(",")]
        elif field_name == "Primary key":
            field_value = field_value.replace("{", "").replace("}", "")
            field_value = [pk.strip() for pk in field_value.split(",")]
        elif field_name == "Candidate keys":
            if field_value == "":
                field_value = []
            else:
                candidate_key_sets = field_value.split("},")
                print(candidate_key_sets)
                # Parse candidate key sets
        input_dict[field_name] = field_value
    print(input_dict)
    return


def main(args: List[str]):
    process_input(args.input_file)


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
