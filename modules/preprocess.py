from . import relation
from typing import List, Tuple


def read_input_file(file_path: str) -> List[str]:
    """
    Description:
        Basic utility function to read the input file
    Input:
        input_file - str: File path to the input file
    Output:
        List[str]: List of lines from the input file
    """
    with open(file_path, "r") as file:
        data = file.read()
    return data


def process_input(input_file: str) -> List[relation.relation]:
    """
    Description:
        Extract a list of relations from the input file
    Input:
        input_file - str: File path to the input file
    Output:
        List[relation]: List of extracted relations
    """
    input_data = read_input_file(f"{input_file}").split("\n")
    input_data = [line for line in input_data if line.strip()]  # Remove empty lines
    relations_list = []
    while input_data:
        extract_relation(input_data, relations_list)
    return relations_list


def braces_to_list(braces: str) -> List[str]:
    """
    Description:
        Basic utility function to convert a string of the form "{a, b, c}" into a list ["a", "b", "c"]
    Input:
        braces - str: String of the form "{a, b, c}"
    Output:
        List[str]: List of strings of the form ["a", "b", "c"]
    """
    return [
        item.strip() for item in braces.replace("{", "").replace("}", "").split(",")
    ]


def extract_relation(
    input_data: List[str], relations_list: List[relation.relation]
) -> relation.relation:
    """
    Description:
        Parses the inputted strings into a relation object, performing basic format validations
    Input:
        input_data - List[str]: List of strings representing the relation, in format:
            Relation: CoffeeShopData
            Attributes: {OrderID, Date, ...}
            Data types: {INT, DATE, ...}
            Primary key: {OrderID, ...}
            Multivalued attributes: {PromocodeUsed, DrinkIngredient}
            Functional dependency: {OrderID} -> {PromocodeUsed}
            Functional dependency: {OrderID, DrinkID} -> {DrinkName, DrinkIngredient}
            Functional dependency: {OrderID, FoodID} -> {FoodName}
            Tuple: {1001, 6/30/2024, NONE, 7.25, 7.25, 0.00, 1, Alice Brown, 1, Caffe Latte, Grande, 1, ND, {Espresso, Oat Milk}, {Oat}, 0, NULL, 0, NONE, NONE}
            Tuple: {1002, 6/30/2026, {SUMMERFUN}, 9.98, 5.99, 3.99, 2, David Miller, 2, Iced Caramel Macchiato, Tall, 2, ND, {Espresso, Vanilla Syrup, Milk, Ice}, {Dairy, Nuts}, 3, Blueberry Muffin, 1, {Flour, Sugar, Blueberries, Eggs}, {Wheat, Egg}}
        relations_list - List[relation]: List of relations to add the new relation to
    Output:
        relation: Relation object created from the input data
    """
    if not input_data[0].startswith("Relation:"):
        raise ValueError(
            f"The first field in each relation must be 'Relation: <name>', not {input_data[0]}"
        )
    name = input_data.pop(0).split(":")[1].strip()
    input_dict = {
        "Name": name,
        "Tuples": [],
        "Foreign keys": [],
        "Functional dependencies": [],
        "Multivalued dependencies": [],
    }
    relation_fields = []
    while input_data and not input_data[0].startswith("Relation:"):
        relation_fields.append(input_data.pop(0))
    valid_fields = [
        "Attributes",
        "Primary key",
        "Candidate keys",
        "Foreign key",
        "Functional dependency",
        "Multivalued dependency",
        "Multivalued attributes",
        "Data types",
        "Tuple",
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

        if field_name == "Multivalued dependency":
            if not "->" in field_value:
                raise ValueError(
                    f"Invalid multivalued dependency format in relation {name}. Format must be {{attribute1, attribute2}} -->> {{attribute1, attribute2}}"
                )
            functional_dependency_parts = field_value.split("-->>")
            if len(functional_dependency_parts) != 2:
                raise ValueError(
                    f"Invalid multivalued dependency format in relation {name}. Format must be {{attribute1, attribute2}} -->> {{attribute1, attribute2}}"
                )
            determines_attrs = (
                functional_dependency_parts[0].strip().strip("{}").split(", ")
            )
            determined_attrs = (
                functional_dependency_parts[1].strip().strip("{}").split(", ")
            )

            input_dict["Multivalued dependencies"].append(
                (determines_attrs, determined_attrs)
            )

        elif field_name == "Functional dependency":
            if not "->" in field_value:
                raise ValueError(
                    f"Invalid functional dependency format in relation {name}. Format must be {{attribute1, attribute2}} -> {{attribute1, attribute2}}"
                )
            functional_dependency_parts = field_value.split("->")
            if len(functional_dependency_parts) != 2:
                raise ValueError(
                    f"Invalid functional dependency format in relation {name}. Format must be {{attribute1, attribute2}} -> {{attribute1, attribute2}}"
                )
            determines_attrs = (
                functional_dependency_parts[0].strip().strip("{}").split(", ")
            )
            determined_attrs = (
                functional_dependency_parts[1].strip().strip("{}").split(", ")
            )

            input_dict["Functional dependencies"].append(
                (determines_attrs, determined_attrs)
            )

        elif field_name == "Foreign key":
            if not "->" in field_value:
                raise ValueError(
                    f"Invalid foreign key format in relation {name}. Format must be {{attribute1, attribute2}} -> relation{{attribute1, attribute2}}"
                )
            foreign_key_parts = field_value.split("->")
            if len(foreign_key_parts) != 2:
                raise ValueError(
                    f"Invalid foreign key format in relation {name}. Format must be {{attribute1, attribute2}} -> relation{{attribute1, attribute2}}"
                )

            key_attrs = foreign_key_parts[0].strip().strip("{}").split(", ")
            references = foreign_key_parts[1].strip().split("{")
            if len(references) != 2:
                raise ValueError(
                    f"Invalid foreign key format in relation {name}. Format must be {{attribute1, attribute2}} -> relation{{attribute1, attribute2}}"
                )

            referenced_table = references[0].strip()
            referenced_attrs = references[1].strip().strip("{}").split(", ")

            input_dict["Foreign keys"].append(
                (key_attrs, referenced_table, referenced_attrs)
            )

        elif field_name == "Tuple":
            if not (field_value.startswith("{") and field_value.endswith("}")):
                raise ValueError(
                    f"Invalid syntax - {field_name} must be formatted as {{___, ___, ___}} in relation {name}"
                )
            field_value = field_value.removeprefix("{").removesuffix("}")
            split_list = field_value.split(", ")
            field_value = []
            current_tuple = ""
            for (
                item
            ) in (
                split_list
            ):  # Split string into list of values, with any {...} sets as a single list item
                if item.startswith("{"):
                    if item.endswith("}"):
                        field_value.append(braces_to_list(item))
                    else:
                        current_tuple = item
                elif item.endswith("}"):
                    current_tuple += ", " + item
                    field_value.append(braces_to_list(current_tuple))
                    current_tuple = ""
                elif current_tuple != "":
                    current_tuple += ", " + item
                else:
                    field_value.append(item)
            input_dict["Tuples"].append(field_value)
        else:
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
                    if not (
                        field_value.startswith("{{") and field_value.endswith("}}")
                    ):
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
    for tuple in input_dict["Tuples"]:
        if len(tuple) != len(input_dict["Attributes"]):
            raise ValueError(
                f"The number of values in tuple <{tuple}> ({len(tuple)}) must match the number of attributes ({len(input_dict['Attributes'])}) in relation {name}"
            )
    return relation.relation(input_dict, relations_list)
