from . import relation
from typing import List

valid_normal_forms = ["0NF", "1NF", "2NF", "3NF", "BCNF", "4NF", "5NF"]


def read_input_file(file_path: str) -> List[str]:
    with open(file_path, "r") as file:
        data = file.read()
    return data


def process_input(input_file: str) -> List[relation.relation]:
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

    relations = []
    while input_data:
        relations.append(extract_relation(input_data))
    return relations


def braces_to_list(braces: str) -> List[str]:
    return [
        item.strip() for item in braces.replace("{", "").replace("}", "").split(",")
    ]


def extract_relation(input_data: List[str]) -> relation.relation:
    if not input_data[0].startswith("Relation:"):
        raise ValueError(
            f"The first field in each relation must be 'Relation: <name>', not {input_data[0]}"
        )
    name = input_data.pop(0).split(":")[1].strip()
    input_dict = {"Name": name}
    relation_fields = []
    while input_data and not input_data[0].startswith("Relation:"):
        relation_fields.append(input_data.pop(0))
    valid_fields = [
        "Attributes",
        "Primary key",
        "Candidate keys",
        "Multivalued attributes",
        "Data types",
    ]
    required_fields = [
        "Attributes",
        "Primary key",
    ]
    for field in relation_fields:
        if not any([field.startswith(valid_field) for valid_field in valid_fields]):
            raise ValueError(f"Invalid field {field.split(':')[0]} in relation {name}")
        field_name = field.split(":")[0].strip()
        field_value = field.split(":")[1].strip()
        if field_name in [
            "Attributes",
            "Primary key",
            "Multivalued attributes",
            "Data types",
        ]:
            if not (field_value.startswith("{") and field_value.endswith("}")):
                raise ValueError(
                    f"Invalid syntax - {field_name} must be formatted as {{___, ___, ___}} in relation {name}"
                )
            field_value = [
                attr.replace("{", "").replace("}", "").strip()
                for attr in field_value.split(",")
            ]
            # Separates "{a, b, c}" into ["a", "b", "c"]
        elif field_name == "Candidate keys":
            if field_value.strip() == "":
                field_value = []
            else:
                if not (field_value.startswith("{{") and field_value.endswith("}}")):
                    raise ValueError(
                        "Invalid syntax - "
                        + field_name
                        + " must be formatted as {{___, ___}, {___, ___}} in relation "
                        + name
                    )
                field_value = [
                    braces_to_list(braces)
                    for braces in field_value.replace("}, ", "}:").split(":")
                ]
                # Separates "{a, b}, {c}" into [["a", "b"], ["c"]]
        input_dict[field_name] = field_value
    for field in required_fields:
        if input_dict.get(field) is None:
            raise ValueError(f"Missing required field {field} in relation {name}")
    if not input_dict.get("Multivalued attributes"):
        input_dict["Multivalued attributes"] = []
    if not input_dict.get("Candidate keys"):
        input_dict["Candidate keys"] = []
    if not input_dict.get("Data types"):
        input_dict["Data types"] = []
    if len(input_dict["Data types"]) != 0 and len(input_dict["Data types"]) != len(
        input_dict["Attributes"]
    ):
        raise ValueError(
            f"The number of data types ({len(input_dict['Data types'])}) must match the number of attributes ({len(input_dict['Attributes'])}) in relation {name}"
        )
    return relation.relation(input_dict)
