"""
Run with:
./scripts/main.bat inputs/input_file.txt outputs/output_file.txt 1NF
or
python3 main.py --input_file=inputs/input.txt --output_file=outputs/output.txt --normal_form=0NF
Test scripts:
.\scripts\main.bat inputs/0NF_test_1.txt outputs/0NF_target_1.txt 0NF
.\scripts\main.bat inputs/0NF_test_1.txt outputs/1NF_target_1.txt 1NF
.\scripts\main.bat inputs/1NF_test_1.txt outputs/2NF_target_1.txt 2NF
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
            decomposed_relation.detect_mvd()
    return relations


def second_nf(relations: List[relation.relation]) -> List[relation.relation]:
    for original_relation in relations.copy():
        current_relation = original_relation
        normalized = False
        removed_original = False
        pfds = []
        for fd in current_relation.functional_dependencies:
            if (
                any([attr in original_relation.pk for attr in fd[0]])
                and set(fd[0]) != original_relation.pk
            ):  # PFD if any attributes of LHS are in PK but equal to the full PK
                normalized = True
                pfds.append(fd)
        original_foreign_keys = [
            attr for fk in current_relation.foreign_keys for attr in fk[0]
        ]
        split_relations = []
        for pfd in pfds:
            if pfd in current_relation.functional_dependencies:
                decomposed_name = (
                    f"{current_relation.name.removesuffix('Data')}{pfd[0][-1].removesuffix('ID')}Data"
                    if current_relation.name.endswith("Data")
                    else f"{fd[0][-1].removesuffix('ID')}{current_relation.name}"
                )
                remaining_attrs = list(set(current_relation.attrs) - set(pfd[1]))
                if any(
                    [
                        relation != current_relation
                        and set(remaining_attrs).issubset(relation.attrs)
                        for relation in relations
                    ]
                ):
                    # If remaining attributes would be redundant, just replace with decomposed relation
                    current_relation.remove_attrs(
                        list(set(current_relation.attrs) - set(pfd[0] + pfd[1]))
                    )
                    removed_original = True
                else:
                    split_relations.append(
                        current_relation.split(pfd[0] + pfd[1], name=decomposed_name)
                    )
                    current_relation.remove_attrs(pfd[1])
        if normalized and (not removed_original):
            all_attrs = []
            for relation in relations:
                if relation != original_relation:
                    all_attrs += relation.attrs
            if set(current_relation.attrs).issubset(
                all_attrs
            ):  # If no unique attributes, remove original
                relations.remove(original_relation)

        inherited_keys = []
        if (
            not original_relation in relations
        ):  # If original removed, inherit foreign keys
            for split_relation in split_relations:
                for attr in split_relation.pk:
                    if (
                        not attr in inherited_keys + original_foreign_keys
                    ):  # If this PFD should inherit the attribute
                        split_relation.owned_keys.append(attr)
                        for foreign_key in split_relation.foreign_keys:
                            if attr in foreign_key[0]:
                                foreign_key[2].pop(foreign_key[0].index(attr))
                                foreign_key[0].remove(attr)
                        split_relation.foreign_keys = [
                            fk for fk in split_relation.foreign_keys if fk[0] and fk[1]
                        ]
                        inherited_keys.append(attr)
                    elif attr in inherited_keys:
                        if not any(
                            [attr in fk[0] for fk in split_relation.foreign_keys]
                        ):
                            split_relation.foreign_keys.append(
                                ([attr], current_relation.name, [attr])
                            )
    fix_foreign_key_references(relations)
    return relations


def third_nf(
    relations: List[relation.relation],
) -> List[
    relation.relation
]:  # Note - anomaly in 3NF output due to incorrect FD label in initial input: OrderID -/> PromocodeUsed
    progress = False
    for original_relation in relations.copy():
        current_relation = original_relation
        for fd in current_relation.functional_dependencies:
            if not (
                current_relation.is_superkey(fd[0]) or current_relation.is_prime(fd[1])
            ):
                decomposed_relation = current_relation.split(
                    fd[0] + fd[1],
                    pk=fd[0],
                    name=f"{current_relation.name.removesuffix('Data')}{fd[0][0].removesuffix('ID')}Data",
                )
                current_relation.remove_attrs(fd[1])
                progress = True
    if progress:
        return third_nf(relations)
    else:
        return relations


def bcnf(relations: List[relation.relation]) -> List[relation.relation]:
    progress = False
    for original_relation in relations.copy():
        current_relation = original_relation
        for fd in current_relation.functional_dependencies:
            if not current_relation.is_superkey(fd[0]):
                decomposed_relation = current_relation.split(
                    fd[0] + fd[1],
                    pk=fd[0],
                    name=f"{current_relation.name.removesuffix('Data')}{fd[0][0].removesuffix('ID')}Data",
                )
                current_relation.remove_attrs(fd[1])
                progress = True
    if progress:
        return bcnf(relations)
    else:
        return relations


def fourth_nf(relations: List[relation.relation]) -> List[relation.relation]:
    # Complete next
    return relations


def fifth_nf(relations: List[relation.relation]) -> List[relation.relation]:
    return relations


def fix_foreign_key_references(
    relations: List[relation.relation],
) -> List[relation.relation]:
    relation_names = [relation.name for relation in relations]
    for current_relation in relations:
        foreign_key_tuples = []
        for fk in current_relation.foreign_keys:
            for i in range(len(fk[0])):
                foreign_key_tuples.append([fk[0][i], fk[1], fk[2][i]])
        for foreign_key in foreign_key_tuples:
            if foreign_key[1] not in relation_names:
                for other_relation in relations:
                    if (
                        current_relation != other_relation
                        and foreign_key[0] in other_relation.owned_keys
                    ):
                        foreign_key[1] = other_relation.name
        current_relation.foreign_keys = []
        for other_relation in sorted(
            list(set(foreign_key[1] for foreign_key in foreign_key_tuples))
        ):
            current_relation.foreign_keys.append(([], other_relation, []))
            for foreign_key_tuple in foreign_key_tuples:
                if foreign_key_tuple[1] == other_relation:
                    current_relation.foreign_keys[-1][0].append(foreign_key_tuple[0])
                    current_relation.foreign_keys[-1][2].append(foreign_key_tuple[2])


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

    if args.output_file and args.output_file != "stdio":
        output = ""
        with open(args.output_file, "w") as file:
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
    main(parser.parse_args())
