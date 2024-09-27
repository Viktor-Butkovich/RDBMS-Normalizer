import unittest
import argparse
from modules import preprocess


class test_process_input(unittest.TestCase):
    def test_foreign_key_formatting(self):
        with self.assertRaises(ValueError) as context:
            preprocess.process_input(
                "inputs/test_inputs/foreign_key_formatting_test.txt"
            )
        self.assertEqual(
            str(context.exception),
            "Invalid foreign key format in relation CoffeeShopPromocodeUsedData",
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
