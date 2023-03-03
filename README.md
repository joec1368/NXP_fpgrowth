# NXP_FPGROWTH
## Description
Use fpgrowth to quickly find similar fail testing files and improve the traditional manual query method.
## Current directory
Description for each file in the directory:
- [fp_growth.py](https://github.com/becks9908/NXP_fpgrowt/blob/main/fp_growth.py) - Main file.
- [preprocess.py](https://github.com/becks9908/NXP_fpgrowt/blob/main/preprocess.py) - Reading precess file.
- [requirements.txt](https://github.com/becks9908/NXP_fpgrowt/blob/main/requirements.txt) - Required dependencies that need to be installed.
- [baseline.py](https://github.com/becks9908/NXP_fpgrowt/blob/main/baseline.py) - Baseline file, simulate the way of manual search.
- [Datafile_0222](https://github.com/becks9908/NXP_fpgrowt/tree/main/Datafile_0222) - Folder of simulation files, a total of 100 records.
- [reference_result](https://github.com/becks9908/NXP_fpgrowt/tree/main/reference_result) - Folder of the generated file example.
- [Result]() - If the folder does not exist initially, it will generate later.

## Before execution

**Installing :**
```ssh
pip install -r requirements.txt
```

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
**Run :**
```sh
python fp_growth.py
```
**If "Result" folder does not exist initially, it will generate :**
##### Result:
- [train_fail_rate_result_file.json]() - Store the name of the fail testname in each training file. 
(**Notice : If you need to regenerate the training results, please delete train_fail_rate_result_file.json in this folder.)**
- [test_file_score_dic.json]() - Store K rule scores after sorting each test file pair.
- [rankingResult.json]() - The total ranking of test files for each training file.
- [Baseline_similars_result.json]() - Results after Baseline simulation.


## The baseline
**If you want to compare the baseline time, please follow :**
1. Open the "baseline.py" file in the directory.
2. Make your changes to the file.
3. Save the file and exit.

**Adjust color parameters :**
 
```python
# Font color setting, default red
FAIL = "00FF0000"
```


**Adjust file setting :**
```python
# file read setting
TRAIN = 75            # Number of training files
TEST = 25             # Number of testing files
DATA_PATH = ''        # Put the path of dataset file dictionary
SHEET_NAME = 'Data_1' # Excel sheet name

START_ROW = 24      # adjust Started testcase column
TESTNUM_COLUMN = 2  # adjust Started testnum column
TESTNAME_COLUMN = 3 # adjust Started testname column
```

**Run :**
```sh
python baseline.py
```