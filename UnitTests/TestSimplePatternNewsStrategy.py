import os
import unittest
from pandas import DataFrame
from DataReading.StockDataContainer import StockDataContainer
from Strategies.StrategyFactory import StrategyFactory
from Utils.GlobalVariables import *

# from directory UnitTests to --> root folder with: ..\\..\\
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\'


class TestSimplePatternNewsStrategy(unittest.TestCase):

    def test_run_strategy(self):
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [('2016-09-13', 90, 90, 100.15, 100.26, 4000),
                ('2016-09-14', 90, 90, 22.95, 100.11, 4000),
                ('2016-09-15', 90, 90, 100.14, 100.62, 4000)]

        df = DataFrame.from_records(data, columns=labels)

        apple_stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
        apple_stock_data_container.set_historical_stock_data(df)
        rwe_stock_data_container = StockDataContainer("RWE AG ST O.N.", "RWE", "")
        rwe_stock_data_container.set_historical_stock_data(df)
        stock_data_container_list = [apple_stock_data_container, rwe_stock_data_container]

        parameter_dict = {'news_threshold': 0.7, 'german_tagger': filepath + 'nltk_german_classifier_data.pickle'}
        all_news_text_list = ["ANALYSE-FLASH: Credit Suisse nimmt Apple mit 'Underperform' wieder auf",
                              "ANALYSE-FLASH: Credit Suisse nimmt RWE mit 'Outperform' wieder auf"]

        stock_screener = StrategyFactory()
        news_strategy = stock_screener.prepare_strategy("SimplePatternNewsStrategy",
                                                        stock_data_container_list, parameter_dict, all_news_text_list)

        results = news_strategy.run_strategy()

        self.assertEqual(results[0] in stock_data_container_list, True)
        apple_idx = results.index(apple_stock_data_container)
        rwe_idx = results.index(rwe_stock_data_container)

        t1 = round(results[apple_idx].prob_dist().prob("neg"), 2)
        self.assertEqual(results[apple_idx].get_stock_name(), "Apple Inc.")
        self.assertGreater(t1, 0.7)

        t1 = round(results[rwe_idx].prob_dist().prob("pos"), 2)
        self.assertEqual(results[rwe_idx].get_stock_name(), "RWE AG ST O.N.")
        self.assertGreater(t1, 0.7)
