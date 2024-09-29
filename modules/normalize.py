from modules import relation
from typing import List, Tuple
from itertools import combinations


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
                omit=sorted(list(set(current_relation.multivalued_attrs) - {mva})),
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
                remaining_attrs = sorted(
                    list(set(current_relation.attrs) - set(pfd[1]))
                )
                if any(
                    [
                        relation != current_relation
                        and set(remaining_attrs).issubset(relation.attrs)
                        for relation in relations
                    ]
                ):
                    # If remaining attributes would be redundant, just replace with decomposed relation
                    current_relation.remove_attrs(
                        sorted(list(set(current_relation.attrs) - set(pfd[0] + pfd[1])))
                    )
                    removed_original = True
                else:
                    split_relations.append(
                        current_relation.split(pfd[0] + pfd[1], name=decomposed_name)
                    )
                    current_relation.remove_attrs(pfd[1])
        if normalized and (not removed_original):
            original_relation.remove_if_redundant()

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
                decomposed_relation.remove_if_redundant()
                current_relation.remove_if_redundant()
                progress = True
    if progress:
        return third_nf(relations)
    else:
        fix_foreign_key_references(relations)
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
                decomposed_relation.remove_if_redundant()
                current_relation.remove_if_redundant()
                progress = True
    if progress:
        return bcnf(relations)
    else:
        fix_foreign_key_references(relations)
        return relations


def fourth_nf(relations: List[relation.relation]) -> List[relation.relation]:
    progress = False
    for original_relation in relations.copy():
        current_relation = original_relation
        for mvd in current_relation.multivalued_dependencies:
            decomposed_relation = current_relation.split(mvd[0] + [mvd[1][0]])
            current_relation.remove_attrs([mvd[1][0]])
            decomposed_relation.remove_if_redundant()
            current_relation.remove_if_redundant()
            if decomposed_relation in relations and not current_relation in relations:
                decomposed_relation.name = (
                    current_relation.name
                )  # If original relation removed, let the decomposed relation inherit the name
            progress = True
    if progress:
        return fourth_nf(relations)
    else:
        fix_foreign_key_references(relations)
        return relations


def fifth_nf(relations: List[relation.relation]) -> List[relation.relation]:
    progress = False
    for original_relation in relations.copy():
        lhs, rhs = find_join_dependency(original_relation)
        if lhs and rhs:
            progress = True
            lhs = original_relation.split(
                lhs, pk=lhs, name=f"{original_relation.name}Decomposed1"
            )
            rhs = original_relation.split(
                rhs, pk=rhs, name=f"{original_relation.name}Decomposed2"
            )
            original_relation.remove_if_redundant()
    if progress:
        return fifth_nf(relations)
    else:
        return relations


def find_join_dependency(
    current_relation: relation.relation,
) -> Tuple[List[str], List[str]]:
    num_attrs = len(current_relation.attrs)
    if (
        num_attrs < 4 or not current_relation.tuples
    ):  # Join dependency requires at least 4 attributes and at least 1 tuple
        return None, None
    optimal_lhs, optimal_rhs = None, None
    optimal_lhs_size, optimal_rhs_size = num_attrs * len(
        current_relation.tuples
    ), num_attrs * len(current_relation.tuples)
    for join_on in current_relation.attrs:
        other_attrs = [attr for attr in current_relation.attrs if attr != join_on]
        for length in range(1, num_attrs - 1):
            for lhs in combinations(other_attrs, length):
                rhs = list(set(current_relation.attrs) - set(lhs))
                lhs = list(lhs) + [join_on]
                lhs_indices = [current_relation.attrs.index(attr) for attr in lhs]
                rhs_indices = [current_relation.attrs.index(attr) for attr in rhs]
                lhs_tuples = []
                rhs_tuples = []
                for row in current_relation.tuples:
                    lhs_tuple = [row[lhs_index] for lhs_index in lhs_indices]
                    if not lhs_tuple in lhs_tuples:
                        lhs_tuples.append(lhs_tuple)
                    rhs_tuple = [row[rhs_index] for rhs_index in rhs_indices]
                    if not rhs_tuple in rhs_tuples:
                        rhs_tuples.append(rhs_tuple)
                reconstructed_tuples = []
                for lhs_tuple in lhs_tuples:
                    for rhs_tuple in rhs_tuples:
                        if (
                            lhs_tuple[lhs.index(join_on)]
                            == rhs_tuple[rhs.index(join_on)]
                        ):  # If the join attribute matches
                            reconstructed_tuple = [None] * num_attrs
                            for value, index in zip(lhs_tuple, lhs_indices):
                                reconstructed_tuple[index] = value
                            for value, index in zip(rhs_tuple, rhs_indices):
                                reconstructed_tuple[index] = value
                            if not reconstructed_tuple in reconstructed_tuples:
                                reconstructed_tuples.append(reconstructed_tuple)
                if len(reconstructed_tuples) == len(current_relation.tuples):
                    if (len(lhs) * len(lhs_tuples)) + (
                        len(rhs) * len(rhs_tuples)
                    ) < optimal_lhs_size + optimal_rhs_size:
                        optimal_lhs = lhs
                        optimal_lhs_size = len(lhs) * len(lhs_tuples)
                        optimal_rhs = rhs
                        optimal_rhs_size = len(rhs) * len(rhs_tuples)
    return optimal_lhs, optimal_rhs


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
            if (
                foreign_key[1] not in relation_names
            ):  # If still not resolved, assume there is no foreign key
                foreign_key[1] = current_relation.name
        current_relation.foreign_keys = []
        for other_relation in sorted(
            list(set(foreign_key[1] for foreign_key in foreign_key_tuples))
        ):
            if other_relation != current_relation.name:
                current_relation.foreign_keys.append(([], other_relation, []))
                for foreign_key_tuple in foreign_key_tuples:
                    if foreign_key_tuple[1] == other_relation:
                        if (
                            not foreign_key_tuple[0]
                            in current_relation.foreign_keys[-1][0]
                        ):
                            current_relation.foreign_keys[-1][0].append(
                                foreign_key_tuple[0]
                            )
                        if (
                            not foreign_key_tuple[2]
                            in current_relation.foreign_keys[-1][2]
                        ):
                            current_relation.foreign_keys[-1][2].append(
                                foreign_key_tuple[2]
                            )