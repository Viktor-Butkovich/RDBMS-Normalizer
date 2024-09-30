import sqlite3
from typing import List, Tuple


class relation:
    """
    Represents a relation in a relational database - can be extracted from/converted to .txt file format, and converted to SQl commands
    """

    def __init__(self, input_dict: dict, relations_list: List["relation"]) -> None:
        """
        Description:
            Initialize a relation object from a dictionary of attributes, and verifies that it results in valid SQL commands
        Input:
            input_dict - dict: Dictionary of attributes for the relation
                Name - str: Name of the relation
                Attributes - List[str]: List of attributes in the relation
                Primary key - List[str]: List of primary key attributes
                Candidate keys - List[List[str]]: List of candidate keys
                Foreign keys - List[Tuple[List[str], str, List[str]]]: List of foreign keys, in format ([attribute1, attribute], other_relation_name, [attribute1, attribute2])
                Functional dependencies - List[Tuple[List[str], List[str]]]: List of functional dependencies, in format ([attribute1], [attribute2, attribute3])
                Multivalued dependencies - List[Tuple[List[str], List[str]]]: List of multivalued dependencies, in format ([attribute1], [attribute2, attribute3])
                Multivalued attributes - List[str]: List of multivalued attributes
                Data types - List[str]: List of data types for each attribute, in same order as attributes
                Tuples - List[List[str]]: List of tuples in the relation, with values in same order as attributes
            relations_list - List[relation]: List of all relations, used to add this relation to the list
        """
        self.relations_list = relations_list
        self.relations_list.append(self)
        self.name: str = input_dict["Name"]
        self.attrs: List[str] = input_dict["Attributes"]
        self.pk: List[str] = input_dict["Primary key"]
        self.candidate_keys: List[List[str]] = input_dict["Candidate keys"]
        self.foreign_keys: List[Tuple[List[str], str, List[str]]] = input_dict.get(
            "Foreign keys", []
        )
        foreign_attributes = [attr for fk in self.foreign_keys for attr in fk[0]]
        self.owned_keys = sorted(list(set(self.attrs) - set(foreign_attributes)))
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

    def remove_if_redundant(self) -> None:
        """
        Description:
            Checks whether this relation is redundant (no attributes unique to it), removing it from relations list if redundant
        Input:
            None
        Output:
            None
        """
        all_attrs = []
        for relation in self.relations_list:
            if relation != self:
                all_attrs += relation.attrs
        if set(self.attrs).issubset(
            set(all_attrs)
        ):  # If no unique attributes, remove original
            self.relations_list.remove(self)

    def is_superkey(self, attrs: List[str]) -> bool:
        """
        Description:
            Checks and returns whether the inputted list of attributes is a superkey of this relation - primary key is a subset of it
        Input:
            attrs - List[str]: Possible superkey
        Output:
            bool: Whether the inputted list of attributes is a superkey of this relation
        """
        for key in [self.pk] + self.candidate_keys:
            if set(key).issubset(set(attrs)):
                return True
        return False

    def is_prime(self, attrs: List[str]) -> bool:
        """
        Description:
            Checks and returns whether the inputted list of attributes is all prime attributes - subset of the primary key and candidate keys
        Input:
            attrs - List[str]: Possible prime attributes
        Output:
            bool: Whether the inputted list of attributes are all prime attributes
        """
        for key in [self.pk] + self.candidate_keys:
            if len(attrs) > 0:
                if set(key).issubset(set(attrs)):
                    return True
            else:
                if attrs[0] in key:
                    return True
        return False

    def remove_attrs(self, attrs: List[str]) -> None:
        """
        Description:
            Removes the inputted attributes from this relation, updating all affected fields
        Input:
            attrs - List[str]: List of attributes to remove
        Output:
            None
        """
        for attr in attrs:
            index = self.attrs.index(attr)
            self.attrs.remove(attr)
            self.data_types.pop(index)
            new_tuples = []
            for current_tuple in self.tuples:
                current_tuple.pop(index)
                if not current_tuple in new_tuples:
                    new_tuples.append(current_tuple)
            self.tuples = new_tuples
            self.pk = [pk_attr for pk_attr in self.pk if pk_attr != attr]
            self.candidate_keys = [
                key.copy()
                for key in self.candidate_keys
                if not any([attr in key for attr in attrs])
            ]
            for key in self.foreign_keys:
                if attr in key[0]:
                    key[2].pop(key[0].index(attr))
                    key[0].remove(attr)
            self.foreign_keys = [
                (key[0].copy(), key[1], key[2].copy())
                for key in self.foreign_keys
                if key[0] and key[2]
            ]
            for fd in self.functional_dependencies:
                if attr in fd[0]:
                    fd[0].remove(attr)
                if attr in fd[1]:
                    fd[1].remove(attr)
            self.functional_dependencies = [
                (fd[0].copy(), fd[1].copy())
                for fd in self.functional_dependencies
                if fd[0] and fd[1]
            ]
            self.multivalued_dependencies = [
                mvd
                for mvd in self.multivalued_dependencies
                if not attr in mvd[0] + mvd[1]
            ]
            self.multivalued_attrs = [
                mva for mva in self.multivalued_attrs if mva != attr
            ]

    def detect_mvd(self) -> None:
        """
        Description:
            Detect if the primary key values of any group of 4 tuples in the relation follows this multivalued depdenency pattern:
                [other PK values match], a, b
                [other PK values match], c, d
                [other PK values match], a, d
                [other PK values match], c, b
            If so, the relation has a multivalued dependency {other PK attributes} -->> attribute 3 | attribute 4 - adds MVD to this relation's list of MVD's
            Some MVDs may be missed if the relation does not have enough tuples to reveal them
            MVD's arise after 1NF normalization
        Input:
            None
        OutpuT:
            None
        """
        for attr1 in self.pk:
            attr1_index = self.attrs.index(attr1)
            for attr2 in self.pk:
                attr2_index = self.attrs.index(attr2)
                if (
                    attr1 != attr2
                ):  # For each pair of attributes in PK, check if they are the RHS of an MVD
                    for t1 in self.tuples:
                        for t2 in self.tuples:
                            if t1 != t2 and all(
                                [
                                    pk_attr in [attr1, attr2]
                                    or t1[self.attrs.index(pk_attr)]
                                    == t2[self.attrs.index(pk_attr)]
                                    for pk_attr in self.pk
                                ]
                            ):
                                for t3 in self.tuples:
                                    if (
                                        t1 != t3
                                        and t2 != t3
                                        and all(
                                            [
                                                pk_attr in [attr1, attr2]
                                                or t1[self.attrs.index(pk_attr)]
                                                == t3[self.attrs.index(pk_attr)]
                                                for pk_attr in self.pk
                                            ]
                                        )
                                    ):
                                        for t4 in self.tuples:
                                            if (
                                                t1 != t4
                                                and t2 != t4
                                                and t3 != 4
                                                and all(
                                                    [
                                                        pk_attr in [attr1, attr2]
                                                        or t1[self.attrs.index(pk_attr)]
                                                        == t4[self.attrs.index(pk_attr)]
                                                        for pk_attr in self.pk
                                                    ]
                                                )
                                            ):
                                                if (
                                                    t1[attr1_index] == t3[attr1_index]
                                                    and t2[attr1_index]
                                                    == t2[attr1_index]
                                                ):
                                                    if (
                                                        t1[attr2_index]
                                                        == t4[attr2_index]
                                                        and t2[attr2_index]
                                                        == t3[attr2_index]
                                                    ):

                                                        mvd = (
                                                            sorted(
                                                                list(
                                                                    set(self.pk)
                                                                    - set(
                                                                        [attr1, attr2]
                                                                    )
                                                                )
                                                            ),
                                                            [attr1, attr2],
                                                        )
                                                        if not any(
                                                            set(mvd[0])
                                                            == set(existing_mvd[0])
                                                            and set(mvd[1])
                                                            == set(existing_mvd[1])
                                                            for existing_mvd in self.multivalued_dependencies
                                                        ):
                                                            self.multivalued_dependencies.append(
                                                                mvd
                                                            )

    def split_mva(self, mva: str) -> None:
        """
        Description:
            Splits the inputted multivalued attribute into a single-valued attribute, splitting each tuple into one for of the MVA's values
        Input:
            mva - str: Multivalued attribute to split
        Output:
            None
        """
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
        """
        Description:
            Returns a string version of this relation, in the same format required to recreate it from a .txt file
        Input:
            None
        Output:
            str: String version of this relation
        """
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

    def split(
        self, attrs: List[str], pk: List[str] = None, name: str = None
    ) -> "relation":
        """
        Description:
            Creates a new relation based on this one but with only the inputted attributes, leaving the original relation unchanged
        Input:
            attrs - List[str]: List of attributes to keep in the new relation
            pk - List[str]: List of primary key attributes to use in the new relation - defaults to the original primary key attributes still remaining
            name - str: Name of the new relation - defaults to the original name + "_decomposed"
        Output:
            relation: New relation with only the inputted attributes
        """
        if not name:
            name = f"{self.name}_decomposed"
        split_data_types = [self.get_data_type(attr) for attr in attrs]
        split_candidate_keys = [
            key for key in self.candidate_keys if all([attr in attrs for attr in key])
        ]
        if not pk:
            split_pk = [attr for attr in self.pk if attr in attrs]
        else:
            split_pk = pk
        split_foreign_keys = [
            (key[0].copy(), key[1], key[2].copy())
            for key in self.foreign_keys
            if all([attr in attrs for attr in key[0]])
        ]
        split_foreign_keys.append((split_pk.copy(), self.name, split_pk.copy()))
        split_functional_dependencies = [
            (fd[0].copy(), fd[1].copy())
            for fd in self.functional_dependencies
            if all([attr in attrs for attr in fd[0] + fd[1]])
        ]
        split_functional_dependencies = [
            fd for fd in split_functional_dependencies if set(fd[0]) != set(split_pk)
        ]
        split_multivalued_dependencies = [
            (mvd[0].copy(), mvd[1].copy())
            for mvd in self.multivalued_dependencies
            if all([attr in attrs for attr in mvd[0] + mvd[1]])
        ]
        split_tuples = []
        for current_tuple in self.tuples:
            new_tuple = [current_tuple[self.attrs.index(attr)] for attr in attrs]
            if new_tuple not in split_tuples:
                split_tuples.append(new_tuple)

        return relation(
            {
                "Name": name,
                "Attributes": attrs,
                "Primary key": split_pk,
                "Candidate keys": split_candidate_keys,
                "Multivalued attributes": [],
                "Data types": split_data_types,
                "Tuples": split_tuples,
                "Foreign keys": split_foreign_keys,
                "Functional dependencies": split_functional_dependencies,
                "Multivalued dependencies": split_multivalued_dependencies,
            },
            self.relations_list,
        )

    def get_data_type(self, attr: str) -> str:
        """
        Description:
            Returns the data type of the inputted attribute
        Input:
            attr - str: Attribute to find the data type of
        Output:
            str: Data type of the inputted attribute
        """
        if not self.data_types:
            return "TEXT"
        return self.data_types[self.attrs.index(attr)]

    def to_sql(self) -> List[str]:
        """
        Description:
            Converts this relation to a list of SQL commands to create the relation and insert its tuples
        Input:
            None
        Output:
            List[str]: List of SQL commands to create the relation and insert its tuples
        """
        return_list = []
        sql = f"CREATE TABLE {self.name} (\n"
        for attr in self.attrs:
            sql += f"    {attr} {self.get_data_type(attr)},\n"
        sql += f"    PRIMARY KEY ({', '.join(self.pk)}),\n"
        for key in self.foreign_keys:
            sql += f"    FOREIGN KEY ({', '.join(key[0])}) REFERENCES {key[1]}({', '.join(key[2])}),\n"
        sql = sql.removesuffix(",\n")  # Remove trailing comma
        sql += "\n);"
        return_list.append(sql)
        for current_tuple in self.tuples:
            values = []
            for item in current_tuple:
                if self.get_data_type(
                    self.attrs[current_tuple.index(item)]
                ).lower() in ["text", "varchar"]:
                    values.append(f"'{item}'")
                elif type(item) != str:
                    values.append("'" + str(item).replace("'", "") + "'")
                elif item.lower() in ["null", "none"]:
                    values.append("NULL")
                else:
                    values.append(item)
            return_list.append(f"INSERT INTO {self.name} VALUES({', '.join(values)});")
        return return_list

    def verify_sql(self) -> List[Tuple]:
        """
        Description:
            Converts this relation to SQL commands and executes them in an in-memory sqlite database, verifying their validity
        Input:
            None
        Output:
            List[Tuple]: List of tuples representing the table schema in the sqlite database
        """
        conn = sqlite3.connect(
            ":memory:"
        )  # Create an in-memory sqlite DB to verify that this relation's to_sql() is valid
        cursor = conn.cursor()
        for sql in self.to_sql():
            try:
                cursor.execute(sql)
            except BaseException as e:
                raise RuntimeError(f"Invalid SQL command:\n\n{sql}\n\n{e}")
        conn.commit()
        cursor.execute(f"PRAGMA table_info({self.name});")
        result = cursor.fetchall()
        conn.close()
        return result
