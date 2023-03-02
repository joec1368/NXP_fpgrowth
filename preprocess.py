import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth
import json


class Preprocess():
    def __init__(self, file_name, min_times, sheetname):
        self.min_times = min_times  # the minimum times of fail
        self.file_name = file_name
        self.SHEET_NAME = sheetname

    def _read_file(self):

        self.df = pd.read_excel(
            self.file_name,
            self.SHEET_NAME,
            skiprows=range(1, 14),
            header=None)

        # drop the frist column
        self.df.drop(columns=self.df.columns[0], axis=1,  inplace=True)
        # drop the first row
        self.df = self.df.drop(index=0)
        # initialize columns
        ini_columns = ['Test Num', 'Test Name',
                       'Unit', 'Test Limit Lo', 'Test Limit Hi']
        columns = ini_columns + \
            ['Result' + str(x+1)
             for x in range(0, self.df.shape[1] - len(ini_columns))]
        # assign column name
        self.df.columns = columns

    def estimate_fail(self):

        # read file
        self._read_file()

        # fitler results column
        self.df_results = self.df.filter(regex=('Result.*'))

        # filter fail test name
        self.train_fail_rate_dic = {}

        for index, row in self.df.iterrows():
            # check each row
            row_result = list(self.df_results.iloc[index-1])[:]
            fail_result = [x for x in row_result if x <
                           row['Test Limit Lo'] or x > row['Test Limit Hi']]
            fail_rate = len(fail_result)/len(row_result)

            if fail_rate != 0 and len(fail_result) >= self.min_times:
                self.train_fail_rate_dic[row['Test Name']] = fail_rate

        return self.train_fail_rate_dic
