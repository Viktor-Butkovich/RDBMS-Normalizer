import unittest
from modules import preprocess


class test_process_input(unittest.TestCase):
    def test_functional_dependency_formatting(self):
        with self.assertRaises(ValueError) as context:
            preprocess.process_input(
                "inputs/test_inputs/functional_dependency_formatting_test.txt"
            )
        self.assertEqual(
            str(context.exception),
            "Invalid functional dependency format in relation CoffeeShopPromocodeUsedData. Format must be {attribute1, attribute2} -> {attribute1, attribute2}",
        )

    def test_multivalued_dependency_formatting(self):
        with self.assertRaises(ValueError) as context:
            preprocess.process_input(
                "inputs/test_inputs/multivalued_dependency_formatting_test.txt"
            )
        self.assertEqual(
            str(context.exception),
            "Invalid multivalued dependency format in relation CoffeeShopFoodAllergenData. Format must be {attribute1, attribute2} -->> {attribute1, attribute2}",
        )

    def test_foreign_key_formatting(self):
        with self.assertRaises(ValueError) as context:
            preprocess.process_input(
                "inputs/test_inputs/foreign_key_formatting_test.txt"
            )
        self.assertEqual(
            str(context.exception),
            "Invalid foreign key format in relation CoffeeShopPromocodeUsedData. Format must be {attribute1, attribute2} -> relation{attribute1, attribute2}",
        )

    def test_missing_braces(self):
        with self.assertRaises(ValueError) as context:
            preprocess.process_input("inputs/test_inputs/missing_braces_test.txt")
        self.assertEqual(
            str(context.exception),
            "Invalid syntax - Primary key must be formatted as {___, ___, ___} in relation CoffeeShopData",
        )

    def test_candidate_key_formatting(self):
        with self.assertRaises(ValueError) as context:
            preprocess.process_input(
                "inputs/test_inputs/candidate_key_formatting_test.txt"
            )
        self.assertEqual(
            str(context.exception),
            "Invalid syntax - Candidate keys must be formatted as {{___, ___}, {___, ___}} in relation CoffeeShopData",
        )

    def test_required_attrs(self):
        with self.assertRaises(ValueError) as context:
            preprocess.process_input(
                "inputs/test_inputs/missing_required_attr_test.txt"
            )
        self.assertEqual(
            str(context.exception),
            "Missing required field Primary key in relation CoffeeShopData",
        )

    def test_num_attrs(self):
        with self.assertRaises(ValueError) as context:
            preprocess.process_input("inputs/test_inputs/num_attrs_test.txt")
        self.assertEqual(
            str(context.exception),
            "The number of data types (4) must match the number of attributes (3) in relation CoffeeShopData",
        )

    def test_tuple_len(self):
        with self.assertRaises(ValueError) as context:
            preprocess.process_input("inputs/test_inputs/missing_tuple_attr_test.txt")
        self.assertEqual(
            str(context.exception),
            "The number of values in tuple <['1002', 'SUMMERFUN']> (2) must match the number of attributes (3) in relation CoffeeShopData",
        )


if __name__ == "__main__":
    unittest.main()
