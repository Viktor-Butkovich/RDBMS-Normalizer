:: Takes an optional input file argument, defaulting to 1NF_test_1.txt
@echo off
set input_file=%1
if "%input_file%"=="" set input_file=inputs/1NF_test_1.txt
set output_file=%2
if "%output_file%"=="" python3 main.py --input_file=%input_file%
if not "%output_file%"=="" python3 main.py --input_file=%input_file% --output_file=%output_file%