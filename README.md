# NXP_FPGROWTH

## Current directory
Description for each file in the directory:
- [fp_growth.py]() - Main file.
- [preprocess.py]() - Reading precess file.
- [requirements.txt]() - Required dependencies that need to be installed.
- [Datafile_0222]() - Folder of simulation files, a total of 100 records.
- [reference_result]() - Folder of the generated file example.
- [Result]() - If the folder does not exist initially, it will generate later.

## Before execution
**To edit the file for this project, follow these steps:**
1. Open the "fp_growth.py" file in the directory.
2. Make your changes to the file.
3. Save the file and exit.

**Adjust algorithm parameters :**
 
```python
# algorithm parameter setting
MIN_SUPPORT = 0.2
MAX_LEN = 10
MIN_LEN = 2

# rule construction setting
MIN_TIMES = 5

# rule filter setting
K = 20
```

**Adjust file setting :**
```python
# file read setting
TRAIN = 75      # Number of training files
TEST = 25       # Number of testing files
DATA_PATH = ''  # Put the path of dataset file dictionary
SHEET_NAME = 'Data_1' # Excel sheet name
```

## Start execution
```sh
python fp_growth.py
```
**If "Result" folder does not exist initially, it will generate :**
##### Result:
- [rankingResult.json]() - The total ranking of test files for each training file.
- [train_fail_rate_result_file.json]() - Store the name of the fail testname in each training file.
- [test_fail_rate_result_file.json]() - Store the name of the fail testname in each test file.
- [test_file_score_dic.json]() - Store K rule scores after sorting each test file pair.

# NXP_fpgrowt
