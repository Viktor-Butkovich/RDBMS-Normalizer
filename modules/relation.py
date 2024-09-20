import sqlite3
from typing import List, Tuple


class relation:
    def __init__(self, input_dict: dict, relations_list: List["relation"]) -> None:
        self.relations_list = relations_list
        self.relations_list.append(self)
        self.name = input_dict["Name"]
        self.attrs = input_dict["Attributes"]
        self.pk = input_dict["Primary key"]
        self.candidate_keys = input_dict["Candidate keys"]
        self.multivalued_attrs = input_dict.get("Multivalued attributes", [])
        self.data_types = input_dict.get("Data types", [])
        self.tuples = input_dict.get("Tuples", [])

    def __str__(self) -> str:
        description = f"\n\nRelation: {self.name}\n"
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
        if self.multivalued_attrs:
            description += (
                f"Multivalued attributes: {{{', '.join(self.multivalued_attrs)}}}\n"
            )

        for tuple in self.tuples:
            description += (
                f"Tuple: {{{', '.join([str(item) for item in tuple])}}}\n".replace(
                    "[", "{"
                ).replace("]", "}")
            )
        return description.replace("'", "").replace('"', "").removesuffix("\n")

    def decompose(self, attrs: List[str]) -> Tuple["relation", "relation"]:
        seen = set()
        decomposed_attrs = [
            x for x in self.pk + attrs if not (x in seen or seen.add(x))
        ]
        decomposed_data_types = [self.get_data_type(attr) for attr in decomposed_attrs]
        decomposed_candidate_keys = [
            key
            for key in self.candidate_keys
            if all([attr in decomposed_attrs for attr in key])
            and key != decomposed_attrs
        ]
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

        retained_attrs = [
            x for x in self.attrs if (x not in decomposed_attrs) or (x in self.pk)
        ]
        retained_data_types = [self.get_data_type(attr) for attr in retained_attrs]
        retained_candidate_keys = [
            key
            for key in self.candidate_keys
            if all([attr in retained_attrs for attr in key]) and key != self.pk
        ]
        retained_multivalued_attrs = [
            attr for attr in self.multivalued_attrs if attr in retained_attrs
        ]
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
            },
            self.relations_list,
        )
        decomposed_relation = relation(
            {
                "Name": f"{self.name}_decomposed",
                "Attributes": decomposed_attrs,
                "Primary key": decomposed_attrs,
                "Candidate keys": decomposed_candidate_keys,
                "Multivalued attributes": decomposed_multivalued_attrs,
                "Data types": decomposed_data_types,
                "Tuples": decomposed_tuples,
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
        sql += f"    PRIMARY KEY ({', '.join(self.pk)})\n"
        sql += ");"
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
