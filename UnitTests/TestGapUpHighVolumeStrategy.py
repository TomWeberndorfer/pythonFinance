import os
import unittest

from pandas import DataFrame, read_csv

from DataReading.NewsStockDataReaders.DataReaderFactory import DataReaderFactory
from DataReading.StockDataContainer import StockDataContainer

# from directory UnitTests to --> root folder with: ..\\..\\
from Strategies.StrategyFactory import StrategyFactory
from Strategies.W52HighTechnicalStrategy import W52HighTechnicalStrategy

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\'
# from directory UnitTests to --> root folder with: ..\\..\\
test_filepath = filepath + 'TestData\\'
stock_data_container_file_name = "stock_data_container_file.pickle"
stock_data_container_file = test_filepath + stock_data_container_file_name


class TestGapUpHighVolumeStrategy(unittest.TestCase):

    def test_run_strategy(self):

        raise NotImplementedError #TODO

        w52hi_parameter_dict = {'check_days': 5, 'min_cnt': 3, 'min_vol_dev_fact': 1.2, 'within52w_high_fact': 0.98}

        labels = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        data = [('2016-09-13', 23.6, 23.73, 23.15, 23.26, 31000),
                ('2016-09-14', 23.33, 23.43, 22.95, 23.11, 31000),
                ('2016-09-15', 23.15, 23.77, 23.14, 23.62, 31000),
                ('2016-09-16', 23.57, 23.68, 23.38, 23.5, 31000),
                ('2016-09-19', 23.6, 23.77, 23.46, 23.51, 31000),
                ('2016-09-20', 23.73, 23.76, 23.26, 23.31, 31000),
                ('2016-09-21', 23.36, 23.78, 23.35, 23.73, 31000),
                ('2016-09-22', 23.83, 23.89, 23.46, 23.73, 31000),
                ('2016-09-23', 23.64, 23.82, 23.54, 23.71, 31000),
                ('2016-09-26', 23.59, 23.81, 23.51, 23.73, 31000),
                ('2016-09-27', 23.73, 23.78, 23.41, 23.72, 31000),
                ('2016-09-28', 23.73, 23.77, 23.56, 23.75, 31000),
                ('2016-09-29', 23.74, 23.82, 23.16, 23.3, 31000),
                ('2016-09-30', 23.35, 23.91, 23.24, 23.8, 31000),
                ('2016-10-03', 23.68, 23.69, 23.39, 23.5, 31000),
                ('2016-10-04', 23.52, 23.64, 23.18, 23.28, 31000),
                ('2016-10-05', 23.28, 23.51, 23.27, 23.43, 31000),
                ('2016-10-06', 23.38, 23.56, 23.29, 23.48, 42000),
                ('2016-10-07', 23.58, 23.65, 23.37, 23.48, 43000),
                ('2016-10-10', 23.62, 23.88, 23.55, 23.77, 44000),
                ('2016-10-11', 23.62, 23.74, 23.01, 23.16, 45000),
                ('2016-10-12', 23.16, 26, 23.11, 23.18, 46000)]

        df = DataFrame.from_records(data, columns=labels)
        stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
        stock_data_container.set_historical_stock_data(df)
        stock_data_container_list = [stock_data_container]

        ##################################################
        # 52 w strategy
        stock_screener = StrategyFactory()
        w52_hi_strat = stock_screener.prepare_strategy("W52HighTechnicalStrategy", stock_data_container_list,
                                                       w52hi_parameter_dict)
        results = w52_hi_strat.run_strategy()
        self.assertEqual(results[0].stock_name, stock_data_container.stock_name)

