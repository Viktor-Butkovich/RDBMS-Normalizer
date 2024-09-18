import unittest
import argparse
import main


class test_process_input(unittest.TestCase):
    def test_missing_normal_form(self):
        with self.assertRaises(ValueError) as context:
            main.process_input("missing_normal_form_test.txt")
        self.assertEqual(
            str(context.exception),
            "Missing normal form - normal form must be in ['0NF', '1NF', '2NF', '3NF', 'BCNF', '4NF', '5NF']",
        )

    def test_invalid_normal_form(self):
        with self.assertRaises(ValueError) as context:
            main.process_input("invalid_normal_form_test.txt")
        self.assertEqual(
            str(context.exception),
            "Invalid normal form ABC - normal form must be in ['0NF', '1NF', '2NF', '3NF', 'BCNF', '4NF', '5NF']",
        )


if __name__ == "__main__":
    unittest.main()
