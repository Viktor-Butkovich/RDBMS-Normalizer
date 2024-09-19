import unittest
import argparse
from modules import preprocess


class test_process_input(unittest.TestCase):
    def test_missing_normal_form(self):
        with self.assertRaises(ValueError) as context:
            preprocess.process_input("test_inputs/missing_normal_form_test.txt")
        self.assertEqual(
            str(context.exception),
            "Missing normal form - normal form must be in ['0NF', '1NF', '2NF', '3NF', 'BCNF', '4NF', '5NF']",
        )

    def test_invalid_normal_form(self):
        with self.assertRaises(ValueError) as context:
            preprocess.process_input("test_inputs/invalid_normal_form_test.txt")
        self.assertEqual(
            str(context.exception),
            "Invalid normal form ABC - normal form must be in ['0NF', '1NF', '2NF', '3NF', 'BCNF', '4NF', '5NF']",
        )

    def test_missing_braces(self):
        with self.assertRaises(ValueError) as context:
            preprocess.process_input("test_inputs/missing_braces_test.txt")
        self.assertEqual(
            str(context.exception),
            "Invalid syntax - Primary key must be formatted as {___, ___, ___} in relation CoffeeShopData",
        )

    def test_candidate_key_formatting(self):
        with self.assertRaises(ValueError) as context:
            preprocess.process_input("test_inputs/candidate_key_formatting_test.txt")
        self.assertEqual(
            str(context.exception),
            "Invalid syntax - Candidate keys must be formatted as {{___, ___}, {___, ___}} in relation CoffeeShopData",
        )

    def test_required_attrs(self):
        with self.assertRaises(ValueError) as context:
            preprocess.process_input("test_inputs/missing_required_attr_test.txt")
        self.assertEqual(
            str(context.exception),
            "Missing required field Primary key in relation CoffeeShopData",
        )

    def test_num_attrs(self):
        with self.assertRaises(ValueError) as context:
            preprocess.process_input("test_inputs/num_attrs_test.txt")
        self.assertEqual(
            str(context.exception),
            "The number of data types (4) must match the number of attributes (3) in relation CoffeeShopData",
        )


if __name__ == "__main__":
    unittest.main()
