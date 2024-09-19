import sqlite3


class relation:
    def __init__(self, input_dict: dict) -> None:
        self.name = input_dict["Name"]
        self.attrs = input_dict["Attributes"]
        self.pk = input_dict["Primary key"]
        self.candidate_keys = input_dict["Candidate keys"]
        self.multivalued_attrs = input_dict.get("Multivalued attributes", [])
        self.data_types = input_dict.get("Data types", [])

    def __str__(self) -> str:
        description = f"Relation: {self.name}\nAttributes: {self.attrs}\nPrimary key: {self.pk}\nCandidate keys: {self.candidate_keys}\nMultivalued attributes: {self.multivalued_attrs}"
        description += f"\n{self.to_sql()}"
        return description

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
