# RDBMS Normalizer
Automatically performing 1NF, 2NF, 3NF, BCNF, 4NF, and 5NF normalization on an inputted relational database schema

Dependencies:
```Python```, ```sqlite3``` library, ability to run ```.sh``` or ```.bat``` scripts (Unix or Windows)

To use:
In the scripts folder, the ```convert_schema.bat``` and ```convert_schema.sh``` scripts convert an input file's database schema to an output file in the desired normal form.
This output file is in the same format as the input, such that the output could be used for a subsequent normalization step.

The ```to_sql.bat``` and ```to_sql.sh``` scripts convert the schema directly to an output file of SQL commands in the desired normal form.

```.\scripts\convert_schema.bat inputs/0NF_test_1.txt outputs/comprehensive_target_1.txt 4NF```
or
```./scripts/convert_schema.sh inputs/0NF_test_1.txt outputs/comprehensive_target_1.txt 4NF```
* Converts the schema in ```0NF_target_1.txt```, the initial schema provided in the assignment description, to a 4NF schema matching the desired output.

```.\scripts\to_sql.bat inputs/0NF_test_1.txt outputs/comprehensive_target_1.txt 4NF```
or
```./scripts/to_sql.sh inputs/0NF_test_1.txt outputs/comprehensive_target_1.txt 4NF```
* Converts the schema in ```0NF_target_1.txt```, the initial schema provided in the assignment description, to a series of SQL commands implementing a 4NF schema with tuples.

Notes:
* This project implements multivalued dependency (MVD) detection, an extra credit feature allowing multivalued dependencies to be detected from tuple values even if they aren't specified in the schema. This notably allows comprehensively normalizing from 0NF input directly to 4NF/5NF, since multivalued depencies usually arise after 1NF normalization and require an intermediate step of identifying them before further normalization.
* 5NF normalization relies on analyzing the provided tuples and checking if any possible decompositions could be natural-joined without losing any data. This results in many false-positive decompositions if not many tuples are provided, since it is trivial to split a single tuple on any attribute and natural join without any data loss, but this may not work with more tuples. Normalizing directly from the provided 0NF input to 5NF results in most relations being identified as having join dependencies, which is likely not correct.
* For grading, new schema input.txt files can be created in the same format as the other files in the inputs folder.
    * Execute any new files with ```./scripts/to_sql.sh inputs/___.txt outputs/___.txt```



Sample files:

```inputs/0NF_test_1.txt``` -> ```0NF_target_1.txt```: Initial schema converted to itself

```inputs/0NF_test_1.txt``` -> ```0NF_sql_target_1.txt```: Initial schema converted to SQL version of itself

```inputs/0NF_test_1.txt``` -> ```1NF_target_1.txt```: Initial schema converted to itself

```inputs/0NF_test_1.txt``` -> ```1NF_sql_target_1.txt```: Initial schema converted to SQL version of itself

```inputs/1NF_test_1.txt``` -> ```2NF_target_1.txt```: 1NF schema from above converted to 2NF

```inputs/1NF_test_1.txt``` -> ```2NF_sql_target_1.txt```: 1NF schema from above converted to 2NF SQL

```inputs/2NF_test_1.txt``` -> ```3NF_target_1.txt```: 2NF schema from above converted to 3NF

```inputs/2NF_test_1.txt``` -> ```3NF_sql_target_1.txt```: 2NF schema from above converted to 3NF SQL

```inputs/3NF_test_1.txt``` -> ```BCNF_target_1.txt```: 3NF schema from above converted to BCNF

```inputs/3NF_test_1.txt``` -> ```BCNF_sql_target_1.txt```: 3NF schema from above converted to BCNF SQL

```inputs/BCNF_test_1.txt``` -> ```4NF_target_1.txt```: BCNF schema from above converted to 4NF

```inputs/BCNF_test_1.txt``` -> ```4NF_sql_target_1.txt```: BCNF schema from above converted to 4NF SQL

```inputs/4NF_test_1.txt``` -> ```5NF_target_1.txt```: Initial 4NF schema converted to 5NF

```inputs/4NF_test_1.txt``` -> ```5NF_sql_target_1.txt```: Initial 4NF schema conveted to 5NF SQL

```inputs/0NF_test_1.txt``` -> ```comprehensive_target_1.txt```: Initial 0NF schema converted directly to 4NF

```inputs/0NF_test_1.txt``` -> ```comprehensive_sql_target_1.txt```: Initial 0NF schema converted directly to 4NF SQL
