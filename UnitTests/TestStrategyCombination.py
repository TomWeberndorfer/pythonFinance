import unittest
from pandas import DataFrame

from DataContainerAndDecorator.NewsDataContainerDecorator import NewsDataContainerDecorator
from DataContainerAndDecorator.StockDataContainer import StockDataContainer
from Strategies.StrategyFactory import StrategyFactory
from Utils.GlobalVariables import *
from datetime import datetime, timedelta
from dateutil import parser

# from directory UnitTests to --> root folder with: ..\\..\\
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\'


class TestStrategyCombination(unittest.TestCase):

    def test_run_strategy_with_two_news_for_one_stock(self):
        name_idx = 0
        datetime_idx = 1
        w52hi_parameter_dict = {'check_days': 5, 'min_cnt': 3, 'min_vol_dev_fact': 1.2, 'within52w_high_fact': 0.98}
        parameter_dict = {'news_threshold': 0.7, 'german_tagger': filepath + 'nltk_german_classifier_data.pickle'}

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

        apple_stock_data_container = NewsDataContainerDecorator(StockDataContainer("Apple Inc.", "AAPL", ""), 0, 0,
                                                                "ANALYSE-FLASH: Credit Suisse nimmt Apple mit 'Underperform' wieder auf")
        apple_stock_data_container_2 = NewsDataContainerDecorator(StockDataContainer("Apple Inc.", "AAPL", ""), 0, 0,
                                                                  "ANALYSE-FLASH: Sparkasse hebt Apple auf 'Buy' und Ziel auf 97 Euro")
        apple_stock_data_container.set_historical_stock_data(df)
        apple_stock_data_container_2.set_historical_stock_data(df)
        stock_data_container_list = [apple_stock_data_container, apple_stock_data_container_2]

        stock_screener = StrategyFactory()
        news_strategy = stock_screener.prepare("SimplePatternNewsStrategy",
                                               stock_data_container_list=stock_data_container_list,
                                               analysis_parameters=parameter_dict)

        news_strategy.run_strategy()
        self.assertEqual("SELL",
                         stock_data_container_list[0].get_recommendation_strategies()["SimplePatternNewsStrategy"][
                             name_idx])

        self.assertEqual("BUY",
                         stock_data_container_list[1].get_recommendation_strategies()["SimplePatternNewsStrategy"][
                             name_idx])

        # 52 wh strat ####################################
        w52_hi_strat = stock_screener.prepare("W52HighTechnicalStrategy",
                                              stock_data_container_list=stock_data_container_list,
                                              analysis_parameters=w52hi_parameter_dict)
        w52_hi_strat.run_strategy()

        self.assertEqual(stock_data_container_list[0].get_stock_name(), "Apple Inc.")
        self.assertEqual("BUY",
                         stock_data_container_list[0].get_recommendation_strategies()["W52HighTechnicalStrategy"][
                             name_idx])
        self.assertEqual("BUY",
                         stock_data_container_list[1].get_recommendation_strategies()["W52HighTechnicalStrategy"][
                             name_idx])

        dt = parser.parse(
            stock_data_container_list[0].get_recommendation_strategies()["W52HighTechnicalStrategy"][datetime_idx])
        elapsed = datetime.now() - dt
        self.assertGreater(timedelta(seconds=0.1), elapsed)

        self.assertEqual("SELL",
                         stock_data_container_list[0].get_recommendation_strategies()["SimplePatternNewsStrategy"][
                             name_idx])

        self.assertEqual("BUY",
                         stock_data_container_list[1].get_recommendation_strategies()["SimplePatternNewsStrategy"][
                             name_idx])

    def test_run_strategy_with_two_strategies_for_one_stock(self):
        name_idx = 0
        datetime_idx = 1
        w52hi_parameter_dict = {'check_days': 5, 'min_cnt': 3, 'min_vol_dev_fact': 1.2, 'within52w_high_fact': 0.98}
        parameter_dict = {'news_threshold': 0.7, 'german_tagger': filepath + 'nltk_german_classifier_data.pickle'}

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

        apple_stock_data_container = NewsDataContainerDecorator(StockDataContainer("Apple Inc.", "AAPL", ""), 0, 0,
                                                                "ANALYSE-FLASH: Credit Suisse nimmt Apple mit 'Underperform' wieder auf")
        apple_stock_data_container.set_historical_stock_data(df)
        stock_data_container_list = [apple_stock_data_container]

        stock_screener = StrategyFactory()
        news_strategy = stock_screener.prepare("SimplePatternNewsStrategy",
                                               stock_data_container_list=stock_data_container_list,
                                               analysis_parameters=parameter_dict)
        news_strategy.run_strategy()

        # 52 wh strat ####################################
        w52_hi_strat = stock_screener.prepare("W52HighTechnicalStrategy",
                                              stock_data_container_list=stock_data_container_list,
                                              analysis_parameters=w52hi_parameter_dict)
        w52_hi_strat.run_strategy()

        self.assertEqual(stock_data_container_list[0].get_stock_name(), "Apple Inc.")
        self.assertEqual("BUY",
                         stock_data_container_list[0].get_recommendation_strategies()["W52HighTechnicalStrategy"][
                             name_idx])

        dt = parser.parse(
            stock_data_container_list[0].get_recommendation_strategies()["W52HighTechnicalStrategy"][datetime_idx])
        elapsed = datetime.now() - dt
        self.assertGreater(timedelta(seconds=0.1), elapsed)

        self.assertEqual("SELL",
                         stock_data_container_list[0].get_recommendation_strategies()["SimplePatternNewsStrategy"][
                             name_idx])
