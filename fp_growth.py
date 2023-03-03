import pandas as pd
import json
import openpyxl
import time
import os.path
import glob
import natsort
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth
from scipy import spatial
from preprocess import Preprocess

# algorithm parameter setting
MIN_SUPPORT = 0.2
MAX_LEN = 10
MIN_LEN = 2

# rule construction setting
MIN_TIMES = 5

# rule filter setting
K = 20

# file read setting
TRAIN = 75
TEST = 25
DATA_PATH = 'Datafile_0222/'
SHEET_NAME = 'Data_1'

# default setting
DATA_FILE_NAME = []
DATA_FILE_LIST = []


def estimate_file_fail_train():
    '''
    Estimate the file rate of training files.
    '''
    print("\n##############  1. Estimate Training File Fail Rate Process ##############\n")
    path = 'Result'
    if not os.path.isdir(path):
        os.makedirs(path)

    train_fail_rate_result_file = 'Result/train_fail_rate_result_file.json'

    # if the training files have not been estimated before
    if not os.path.isfile(train_fail_rate_result_file):
        all_train_fail_rate_result_file_dic = {}

        for a in range(TRAIN):
            cur_file = DATA_FILE_NAME[a]
            cur_path = DATA_PATH + cur_file
            print(" Estimating training file " +
                  cur_file + " ")
            # estimate the fail rate of each training file
            p = Preprocess(
                file_name=cur_path,
                min_times=MIN_TIMES,
                sheetname=SHEET_NAME)

            train_fail_rate_dic = p.estimate_fail()
            all_train_fail_rate_result_file_dic[cur_file] = train_fail_rate_dic

        # write file
        json.dump(all_train_fail_rate_result_file_dic, open(
            train_fail_rate_result_file, "w"))

    else:
        print('--------> Training fail rate has been estimated before.')
        all_train_fail_rate_result_file_dic = json.load(
            open(train_fail_rate_result_file, "r"))

    return all_train_fail_rate_result_file_dic


def estimate_file_fail_test():
    '''
    Estimate the file rate of test files.
    '''
    print("\n##############  5. Estimate testing file fail rate process ##############\n")

    all_test_fail_rate_result_file_dic = {}

    for cut_point in range(TEST):
        cur_file = DATA_FILE_NAME[cut_point+TRAIN]
        cur_path = DATA_PATH + cur_file
        print(" Estimating testing file " +
              cur_file + " ")
        # estimate the fail rate of each testing file
        p = Preprocess(
            file_name=cur_path,
            min_times=MIN_TIMES,
            sheetname=SHEET_NAME)

        test_fail_rate_dic = p.estimate_fail()
        # print('testData_' + str(a+1), test_fail_rate_dic)

        all_test_fail_rate_result_file_dic[cur_file] = test_fail_rate_dic

    # write file
    #json.dump(all_test_fail_rate_result_file_dic, open(test_fail_rate_result_file_file, "w"))
    return all_test_fail_rate_result_file_dic


def formulate_input(dic):
    '''
    Formulate fail rate dictionary to the input of the algorithm.
    '''
    print("\n##############  2. Input the dataset formula  ############################")
    input_dataset = []

    for file in list(dic):
        input_dataset.append(list(dic[file]))
    print("\n  Dataset formula process finished.  ")
    return input_dataset


def rule_mining(dataset):
    '''
    Implement fp-growth.
    '''
    print("\n##############  3. Implement FP-growth process  ##########################")
    te = TransactionEncoder()
    te_ary = te.fit(dataset).transform(dataset)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    df_rules = fpgrowth(df, min_support=MIN_SUPPORT,
                        max_len=MAX_LEN, use_colnames=True)
    # sorted by support values
    df_rules = df_rules.sort_values(by='support', ascending=False)
    # create new df
    df_filter_rules = pd.DataFrame(columns=['support', 'itemsets'])

    # filer with the minimum length
    for index, row in df_rules.iterrows():
        if len(df_filter_rules.index) < K and len(list(row['itemsets'])) >= MIN_LEN:
            df_filter_rules.loc[len(df_filter_rules.index)] = \
                [row['support'], list(row['itemsets'])]
    print("\n  FP-growth process finished.  ")
    return df_filter_rules


def train_score_calculation(df_filter_rules, fail_result_dic):
    '''
    Estimate the score of training files.
    '''
    print("\n##############  4. Estimate the score of training files  ##################")

    training_file_score_dic = {}
    for r in range(TRAIN):
        cur_file = DATA_FILE_NAME[r]
        scoreList = []
        # print(fail_result_dic.get(cur_file))
        for j in range(K):
            score = 1
            for i in range(len(df_filter_rules['itemsets'][j])):
                tmp = df_filter_rules['itemsets'][j][i]
                if fail_result_dic.get(cur_file).get(tmp) is not None:
                    score *= fail_result_dic.get(cur_file).get(tmp)
                else:
                    score = 0.0
            scoreList.append(score)
        training_file_score_dic[cur_file] = scoreList
    print("\n  Estimation training score Finished.  ")

    return training_file_score_dic


def test_score_calculation(df_filter_rules, fail_result_dic):
    '''
    Estimate the score of testing files.
    '''

    print("\n##############  6. Estimate the score of testing files  ###################")
    test_file_score_dic = {}
    for r in range(TEST):
        cur_file = DATA_FILE_NAME[r+TRAIN]
        scoreList = []
        for j in range(K):
            score = 1
            for i in range(len(df_filter_rules['itemsets'][j])):
                tmp = df_filter_rules['itemsets'][j][i]
                if fail_result_dic.get(cur_file).get(tmp) is not None:
                    score *= fail_result_dic.get(cur_file).get(tmp)
                else:
                    score = 0.0
            scoreList.append(score)
        test_file_score_dic[cur_file] = scoreList

    print("\n  Estimation testing score Finished.  ")

    return test_file_score_dic


def similar(score_file_score_dic, test_file_score_dic):
    '''
    Similarity comparison and ranking.
    '''

    print("\n##############  7. Estimate the similarity between the Training/Testing file #####################")
    training_file_score = score_file_score_dic
    totalRanking_dic = {}
    for w in range(TEST):
        cur_file = DATA_FILE_NAME[w+TRAIN]
        dataSetI = test_file_score_dic.get(cur_file)
        rankingList = {}
        for p in range(TRAIN):
            train_file = DATA_FILE_NAME[p]
            dataSetII = training_file_score.get(train_file)
            result = 1 - spatial.distance.cosine(dataSetI, dataSetII)
            rankingList[train_file] = result
        afterRanking = dict(sorted(rankingList.items(),
                                   key=lambda item: item[1], reverse=True))
        totalRanking_dic[cur_file] = afterRanking

    jsonFile = open("Result/rankingResult.json", "w")
    jsonFile.write(json.dumps(totalRanking_dic, indent=2))
    jsonFile.close()
    print("\n  Estimation of similarity finished. \n ")


def main():
    #================== Sort the file names first ==================#
    DATA_FILE_LIST = glob.glob(os.path.join(DATA_PATH, "*.xlsx"))
    DATA_FILE_LIST = natsort.natsorted(DATA_FILE_LIST)
    for file_path in DATA_FILE_LIST:
        DATA_FILE_NAME.append(os.path.basename(file_path))

    #========================= TRAIN ===============================#
    # Estimate fail rates of training files
    all_train_fail_rate_result_file_dic = estimate_file_fail_train()
    # Transfer the dictionary to algorithm input
    input_dataset_train = formulate_input(all_train_fail_rate_result_file_dic)
    # Run fp-grwoth
    df_rules = rule_mining(input_dataset_train)
    # Estimate the score of training files.
    score_cal_train = train_score_calculation(
        df_rules, all_train_fail_rate_result_file_dic)

    #=========================== TEST ==============================#
    start_time = time.time()
    # Estimate fail rates of testing files
    all_test_fail_rate_result_file_dic = estimate_file_fail_test()
    # Estimate the score of testing files
    score_cal_test = test_score_calculation(
        df_rules, all_test_fail_rate_result_file_dic)
    # Estimate the similarity between the Training/Testing file
    similar_cal = similar(score_cal_train, score_cal_test)
    # Calculate the time required for Testing
    print("*********************************************\n*                                           *\n*         %s mins           *\n*                                           *\n*********************************************" % ((time.time() - start_time) / 60))


if __name__ == "__main__":
    main()
