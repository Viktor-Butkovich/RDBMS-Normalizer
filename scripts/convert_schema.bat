@echo off
set input_file=%1
if "%input_file%"=="" set input_file=inputs/1NF_test_1.txt
set output_file=%2
set normal_form=%3
if "%normal_form%"=="" set normal_form=0NF
if "%output_file%"=="stdio" python3 main.py --input_file=%input_file% --normal_form=%normal_form%
if not "%output_file%"=="" python3 main.py --input_file=%input_file% --output_file=%output_file% --normal_form=%normal_form%