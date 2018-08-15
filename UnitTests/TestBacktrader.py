import unittest

import backtrader as bt
import backtrader.analyzers as btanalyzer
import pandas as pd

from Backtesting.BacktraderWrapper import BacktraderWrapper
# from directory UnitTests to --> root folder with: ..\\..\\
from Utils.GlobalVariables import *

test_filepath = GlobalVariables.get_data_files_path() + 'TestData\\'


class TestBacktrader(unittest.TestCase):

    def test_backtrader_52whi_(self):
        tbt = BacktraderWrapper()
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict(False).items():
            labels.append(value)

        data_in_1 = [
            ('2016-09-30', 46.35, 46.91, 46.24, 46.8, 33900),
            ('2016-10-03', 46.68, 46.69, 46.39, 46.5, 31600),
            ('2016-10-04', 46.52, 46.64, 46.39, 46.28, 31700),
            ('2016-10-05', 46.28, 46.51, 46.27, 46.43, 31500),
            ('2016-10-06', 46.38, 46.56, 46.29, 46.48, 42000),
            ('2016-10-07', 46.58, 46.65, 46.37, 46.48, 43000),
            ('2016-10-10', 46.62, 46.88, 46.55, 46.77, 44000),
            ('2016-10-11', 46.62, 46.74, 46.01, 46.16, 45000),
            ('2016-10-12', 26.16, 27, 26.11, 26, 46000),
            ('2016-10-13', 46.52, 46.64, 46.39, 46.468, 32000),
            ('2016-10-14', 46.52, 46.64, 46.39, 46.0, 33000),
            ('2016-10-15', 39.7, 20, 17, 39.5, 33000),
            ('2016-10-16', 39, 19, 16, 15, 33000)
        ]

        data_in_2 = [
            ('2016-09-30', 23.35, 23.91, 23.24, 23.8, 31800),
            ('2016-10-03', 23.68, 23.69, 23.39, 23.5, 31600),
            ('2016-10-04', 23.52, 23.64, 23.18, 23.28, 31700),
            ('2016-10-05', 23.28, 23.51, 23.27, 23.43, 31500),
            ('2016-10-06', 23.38, 23.56, 23.29, 23.48, 42000),
            ('2016-10-07', 23.58, 23.65, 23.37, 23.48, 43000),
            ('2016-10-10', 23.62, 23.88, 23.55, 23.77, 44000),
            ('2016-10-11', 23.62, 23.74, 23.01, 23.16, 45000),
            ('2016-10-12', 26.16, 27, 26.11, 26, 46000),
            ('2016-10-13', 23.52, 23.64, 23.18, 23.238, 32000),
            ('2016-10-14', 23.52, 23.64, 23.18, 23.0, 33000),
            ('2016-10-15', 18.7, 20, 17, 18.5, 33000),
            ('2016-10-16', 18, 19, 16, 15, 33000)]

        df_1 = pd.DataFrame.from_records(data_in_1, columns=labels)
        df_2 = pd.DataFrame.from_records(data_in_2, columns=labels)

        data_list = []
        dfs = [df_1, df_2]

        for df_in in dfs:
            data_pd = bt.feeds.PandasData(
                dataname=df_in, datetime=0,
                open=1, high=2, low=3,
                close=4, volume=5,
                openinterest=-1
            )
            data_list.append(data_pd)

        analyzers = [btanalyzer.TradeAnalyzer]
        w52hi_parameter_dict = {'position_size_percents': 0.2, 'strategy_to_test': "W52HighTechnicalStrategy",
                                'check_days': 5, 'min_cnt': 3, 'min_vol_dev_fact': 1.2,
                                'within52w_high_fact': 0.99}
        tbt.run_test(data_list, 30000, 0.005, analyzers, True, w52hi_parameter_dict)