import sqlite3
from typing import List, Tuple


class relation:
    def __init__(self, input_dict: dict, relations_list: List["relation"]) -> None:
        self.relations_list = relations_list
        self.relations_list.append(self)
        self.name: str = input_dict["Name"]
        self.attrs: List[str] = input_dict["Attributes"]
        self.pk: List[str] = input_dict["Primary key"]
        self.candidate_keys: List[List[str]] = input_dict["Candidate keys"]
        self.foreign_keys: List[Tuple[List[str], str, List[str]]] = input_dict.get(
            "Foreign keys", []
        )
        self.functional_dependencies: List[
            Tuple[List[str], List[str]]
        ] = input_dict.get("Functional dependencies", [])
        self.multivalued_dependencies: List[
            Tuple[List[str], List[str]]
        ] = input_dict.get("Multivalued dependencies", [])
        self.multivalued_attrs: List[str] = input_dict.get("Multivalued attributes", [])
        self.data_types: List[str] = input_dict.get("Data types", [])
        self.tuples: List[List[str]] = input_dict.get("Tuples", [])
        self.verify_sql()

    def split_mva(self, mva: str) -> None:
        index = self.attrs.index(mva)
        self.data_types[index] = "VARCHAR"
        self.multivalued_attrs.remove(mva)
        for current_tuple in self.tuples.copy():
            if current_tuple[index] not in ["NULL", "NONE", "Null", "None"]:
                for value in current_tuple[index]:
                    new_tuple = current_tuple.copy()
                    new_tuple[index] = value
                    self.tuples.append(new_tuple)
                self.tuples.remove(current_tuple)

    def __str__(self) -> str:
        description = f"Relation: {self.name}\n"
        description += f"Attributes: {{{', '.join(self.attrs)}}}\n"
        if self.data_types:
            description += f"Data types: {{{', '.join(self.data_types)}}}\n"
        description += f"Primary key: {{{', '.join(self.pk)}}}\n"
        if self.candidate_keys:
            description += (
                f"Candidate keys: "
                + "{"
                + f"{{{'}, {'.join([', '.join(key) for key in self.candidate_keys])}}}"
                + "}\n"
            )
        if self.foreign_keys:
            for fk in self.foreign_keys:
                description += f"Foreign key: {{{', '.join(fk[0])}}} -> {fk[1]}{{{', '.join(fk[2])}}}\n"
        if self.multivalued_attrs:
            description += (
                f"Multivalued attributes: {{{', '.join(self.multivalued_attrs)}}}\n"
            )
        if self.functional_dependencies:
            for fd in self.functional_dependencies:
                description += f"Functional dependency: {{{', '.join(fd[0])}}} -> {{{', '.join(fd[1])}}}\n"
        if self.multivalued_dependencies:
            for mvd in self.multivalued_dependencies:
                description += f"Multivalued dependency: {{{', '.join(mvd[0])}}} -->> {{{', '.join(mvd[1])}}}\n"

        for tuple in self.tuples:
            description += (
                f"Tuple: {{{', '.join([str(item) for item in tuple])}}}\n".replace(
                    "[", "{"
                ).replace("]", "}")
            )
        return description.replace("'", "").replace('"', "") + "\n"

    def decompose(
        self, attrs: List[str], omit: List[str], name: str = None
    ) -> Tuple["relation", "relation"]:
        seen = set()
        decomposed_attrs = [
            x for x in self.pk + attrs if not (x in seen or seen.add(x) or x in omit)
        ]
        decomposed_data_types = [self.get_data_type(attr) for attr in decomposed_attrs]
        decomposed_candidate_keys = [
            key
            for key in self.candidate_keys
            if all([attr in decomposed_attrs for attr in key])
            and key != decomposed_attrs
        ]
        decomposed_foreign_keys = self.foreign_keys.copy()
        decomposed_foreign_keys.append(
            (self.pk.copy(), self.name, self.pk.copy())
        )  # Foreign key in format (attributes, referenced relation, referenced attributes)
        decomposed_functional_dependencies = []
        for fd in self.functional_dependencies:
            if all(
                [attr in decomposed_attrs for attr in fd[0]]
            ):  # If all determining attributes remain
                determined = [attr for attr in fd[1] if attr in decomposed_attrs]
                if determined:  # Keep any determined attributes that remain
                    decomposed_functional_dependencies.append(
                        (fd[0].copy(), determined)
                    )
        decomposed_multivalued_dependencies = []
        for fd in self.multivalued_dependencies:
            if all(
                [attr in decomposed_attrs for attr in fd[0] + fd[1]]
            ):  # If all determining/determined attributes remain
                decomposed_multivalued_dependencies.append((fd[0].copy(), fd[1].copy()))
        decomposed_multivalued_attrs = [
            attr for attr in self.multivalued_attrs if attr in decomposed_attrs
        ]
        decomposed_tuples = []
        for current_tuple in self.tuples:
            new_tuple = [
                current_tuple[self.attrs.index(attr)] for attr in decomposed_attrs
            ]
            if new_tuple not in decomposed_tuples:
                decomposed_tuples.append(new_tuple)
        if not name:
            name = f"{self.name}_decomposed"

        retained_attrs = [
            x for x in self.attrs if (x not in decomposed_attrs) or (x in self.pk)
        ]
        retained_data_types = [self.get_data_type(attr) for attr in retained_attrs]
        retained_candidate_keys = [
            key
            for key in self.candidate_keys
            if all([attr in retained_attrs for attr in key]) and key != self.pk
        ]
        retained_foreign_keys = self.foreign_keys.copy()
        retained_multivalued_attrs = [
            attr for attr in self.multivalued_attrs if attr in retained_attrs
        ]
        retained_functional_dependencies = []
        for fd in self.functional_dependencies:
            if all(
                [attr in retained_attrs for attr in fd[0]]
            ):  # If all determining attributes remain
                determined = [attr for attr in fd[1] if attr in retained_attrs]
                if determined:  # Keep any determined attributes that remain
                    retained_functional_dependencies.append((fd[0].copy(), determined))
        retained_multivalued_dependencies = []
        for fd in self.multivalued_dependencies:
            if all(
                [attr in retained_attrs for attr in fd[0] + fd[1]]
            ):  # If all determining/determined attributes remain
                retained_multivalued_dependencies.append((fd[0].copy(), fd[1].copy()))
        retained_tuples = []
        for current_tuple in self.tuples:
            new_tuple = [
                current_tuple[self.attrs.index(attr)] for attr in retained_attrs
            ]
            if new_tuple not in retained_tuples:
                retained_tuples.append(new_tuple)
        self.relations_list.remove(self)
        retained_relation = relation(
            {
                "Name": self.name,
                "Attributes": retained_attrs,
                "Primary key": self.pk,
                "Candidate keys": retained_candidate_keys,
                "Multivalued attributes": retained_multivalued_attrs,
                "Data types": retained_data_types,
                "Tuples": retained_tuples,
                "Foreign keys": retained_foreign_keys,
                "Functional dependencies": retained_functional_dependencies,
                "Multivalued dependencies": retained_multivalued_dependencies,
            },
            self.relations_list,
        )
        decomposed_relation = relation(
            {
                "Name": name,
                "Attributes": decomposed_attrs,
                "Primary key": decomposed_attrs,
                "Candidate keys": decomposed_candidate_keys,
                "Multivalued attributes": decomposed_multivalued_attrs,
                "Data types": decomposed_data_types,
                "Tuples": decomposed_tuples,
                "Foreign keys": decomposed_foreign_keys,
                "Functional dependencies": decomposed_functional_dependencies,
                "Multivalued dependencies": decomposed_multivalued_dependencies,
            },
            self.relations_list,
        )
        return (retained_relation, decomposed_relation)

    def get_data_type(self, attr: str) -> str:
        if not self.data_types:
            return "TEXT"
        return self.data_types[self.attrs.index(attr)]

    def to_sql(self) -> str:
        sql = f"CREATE TABLE {self.name} (\n"
        for attr in self.attrs:
            sql += f"    {attr} {self.get_data_type(attr)},\n"
        sql += f"    PRIMARY KEY ({', '.join(self.pk)}),\n"
        for key in self.foreign_keys:
            sql += f"    FOREIGN KEY ({', '.join(key[0])}) REFERENCES {key[1]}({', '.join(key[2])}),\n"
        sql = sql.removesuffix(",\n")  # Remove trailing comma
        sql += "\n);"
        return sql

    def verify_sql(self) -> str:
        try:
            conn = sqlite3.connect(
                ":memory:"
            )  # Create an in-memory sqlite DB to verify that this relation's to_sql() is valid
            cursor = conn.cursor()
            cursor.execute(self.to_sql())
            conn.commit()
            cursor.execute(f"PRAGMA table_info({self.name});")
            result = cursor.fetchall()
            conn.close()
            return result
        except BaseException as e:
            raise RuntimeError(
                f"Invalid CREATE TABLE command:\n\n{self.to_sql()}\n\n{e}"
            )
