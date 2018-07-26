import os
import unittest
from pandas import DataFrame
from DataReading.StockDataContainer import StockDataContainer
from Strategies.StrategyFactory import StrategyFactory
from Utils.GlobalVariables import *

# from directory UnitTests to --> root folder with: ..\\..\\
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\'


class TestStrategyCombination(unittest.TestCase):

    def test_run_strategy_with_two_news_for_one_stock(self):
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [('2016-09-30', 23.35, 23.91, 23.24, 23.8, 31000),
                ('2016-10-03', 23.68, 23.69, 23.39, 23.5, 31000),
                ('2016-10-04', 23.52, 23.64, 23.18, 23.28, 31000),
                ('2016-10-05', 23.28, 23.51, 23.27, 23.43, 31000),
                ('2016-10-06', 23.38, 23.56, 23.29, 23.48, 42000),
                ('2016-10-07', 23.58, 23.65, 23.37, 23.48, 43000),
                ('2016-10-10', 23.62, 23.88, 23.55, 23.77, 44000),
                ('2016-10-11', 23.62, 23.74, 23.01, 23.16, 45000),
                ('2016-10-12', 23.16, 23.8, 23.11, 23.18, 46000)]

        df = DataFrame.from_records(data, columns=labels)

        apple_stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
        apple_stock_data_container.set_historical_stock_data(df)
        stock_data_container_list = [apple_stock_data_container]

        w52hi_parameter_dict = {'check_days': 5, 'min_cnt': 3, 'min_vol_dev_fact': 1.2, 'within52w_high_fact': 0.98}
        parameter_dict = {'news_threshold': 0.7, 'german_tagger': filepath + 'nltk_german_classifier_data.pickle'}
        all_news_text_list = ["ANALYSE-FLASH: Credit Suisse nimmt Apple mit 'Underperform' wieder auf",
                              "ANALYSE-FLASH: Sparkasse hebt Apple auf 'Buy' und Ziel auf 97 Euro"]

        stock_screener = StrategyFactory()
        news_strategy = stock_screener.prepare_strategy("SimplePatternNewsStrategy",
                                                        stock_data_container_list, parameter_dict,
                                                        all_news_text_list)

        test = news_strategy.run_strategy()

        w52_hi_strat = stock_screener.prepare_strategy("W52HighTechnicalStrategy", stock_data_container_list,
                                                       w52hi_parameter_dict)
        w52_hi_strat.run_strategy()

        self.assertEqual(stock_data_container_list[0].get_stock_name(), "Apple Inc.")
        self.assertEqual("BUY",
                         stock_data_container_list[0].get_recommendation_strategies()["W52HighTechnicalStrategy"])
        self.assertEqual("SELL",
                         stock_data_container_list[0].get_recommendation_strategies()["SimplePatternNewsStrategy"])

        self.assertEqual("BUY",
                         stock_data_container_list[0].get_recommendation_strategies()["SimplePatternNewsStrategy"])
