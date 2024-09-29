#!/bin/bash

input_file=${1:-inputs/1NF_test_1.txt}
output_file=$2
normal_form=${3:-0NF}

if [ "$output_file" == "stdio" ]; then
    python3 main.py --input_file="$input_file" --normal_form="$normal_form" --target=sql
else
    python3 main.py --input_file="$input_file" --output_file="$output_file" --normal_form="$normal_form" --target=sql
fi