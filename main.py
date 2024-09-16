"""
Run with python3 main.py --input_file=<file_name in inputs directory>.txt
python3 main.py --input_file=test_input_1.txt=
"""

import sqlite3
import argparse

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Normalize the relations from the inputted .txt file")
    parser.add_argument('--input_file', type=str, required=True, help='Name of the .txt file in the inputs folder')
    args = parser.parse_args()

    input_data = read_input_file(f"inputs/{args.input_file}").split("\n")
    print(input_data)
