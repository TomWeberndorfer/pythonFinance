import os
import unittest

from pandas import DataFrame

from DataReading.StockDataContainer import StockDataContainer
# from directory UnitTests to --> root folder with: ..\\..\\
from Strategies.StrategyFactory import StrategyFactory
from Utils.GlobalVariables import GlobalVariables

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\'
# from directory UnitTests to --> root folder with: ..\\..\\
test_filepath = filepath + 'TestData\\'
stock_data_container_file_name = "stock_data_container_file.pickle"
stock_data_container_file = test_filepath + stock_data_container_file_name


class TestGapUpHighVolumeStrategy(unittest.TestCase):

    def test_run_strategy__gap_up_STOCK_AS_RESULT__no_gap_EMPTY_RESULT(self):

        parameter_dict = {'min_gap_factor': 1.1}
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)

        data = [('2016-09-13', 23.6, 23.73, 23.15, 23.26, 31000),
                ('2016-09-14', 23.33, 23.43, 22.95, 23.11, 31000),
                ('2016-09-15', 23.15, 23.77, 23.14, 23.62, 31000),
                ('2016-09-16', 23.57, 23.68, 23.38, 23.5, 31000),
                ('2016-09-19', 23.6, 23.77, 23.46, 23.51, 31000),
                ('2016-09-20', 23.73, 23.76, 23.26, 23.31, 31000),
                ('2016-09-21', 23.36, 23.78, 23.35, 23.73, 31000),
                ('2016-09-22', 33.83, 33.89, 33.46, 33.73, 31000),]

        df = DataFrame.from_records(data, columns=labels)
        stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
        stock_data_container.set_historical_stock_data(df)
        stock_data_container_list = [stock_data_container]

        ##################################################
        stock_screener = StrategyFactory()
        strat = stock_screener.prepare_strategy("GapUpHighVolumeStrategy", stock_data_container_list,
                                                       parameter_dict)
        results = strat.run_strategy()
        self.assertEqual(results[0].get_stock_name(), stock_data_container.get_stock_name())

        #################
        data = [('2016-09-13', 23.6, 23.73, 23.15, 23.26, 31000),
                ('2016-09-14', 23.33, 23.43, 22.95, 23.11, 31000),
                ('2016-09-15', 23.15, 23.77, 23.14, 23.62, 31000),
                ('2016-09-16', 23.57, 23.68, 23.38, 23.5, 31000),
                ('2016-09-19', 23.6, 23.77, 23.46, 23.51, 31000),
                ('2016-09-20', 23.73, 23.76, 23.26, 23.31, 31000),
                ('2016-09-21', 23.36, 23.78, 23.35, 23.73, 31000),
                ('2016-09-22', 23.36, 23.78, 23.35, 23.73, 31000), ]

        df = DataFrame.from_records(data, columns=labels)
        stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
        stock_data_container.set_historical_stock_data(df)
        stock_data_container_list = [stock_data_container]

        ##################################################
        stock_screener = StrategyFactory()
        strat = stock_screener.prepare_strategy("GapUpHighVolumeStrategy", stock_data_container_list,
                                                parameter_dict)
        results = strat.run_strategy()
        self.assertEqual(len(results), 0)

