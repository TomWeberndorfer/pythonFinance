import unittest
from time import sleep
from dateutil import parser
from pandas import DataFrame
from datetime import datetime, timedelta

from DataContainerAndDecorator.NewsDataContainerDecorator import NewsDataContainerDecorator
from DataContainerAndDecorator.StockDataContainer import StockDataContainer
from Strategies.StrategyFactory import StrategyFactory
from Utils.GlobalVariables import *

# from directory UnitTests to --> root folder with: ..\\..\\

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\'


class TestStockDataContainer(unittest.TestCase):

    def test_eg_method(self):
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [('2016-09-13', 90, 90, 100.15, 100.26, 4000)]

        df = DataFrame.from_records(data, columns=labels)
        apple_stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
        apple_stock_data_container.set_historical_stock_data(df)
        rwe_stock_data_container = StockDataContainer("RWE AG ST O.N.", "RWE", "")
        testag_stock_data_container = StockDataContainer("Test AG", "TestAG", "")
        rwe_stock_data_container.set_historical_stock_data(df)
        stock_data_container_list = [apple_stock_data_container, rwe_stock_data_container]

        # if apple_stock_data_container in stock_data_container_list:
        self.assertEqual(apple_stock_data_container in stock_data_container_list, True)
        self.assertEqual(rwe_stock_data_container in stock_data_container_list, True)
        self.assertEqual(testag_stock_data_container in stock_data_container_list, False)

    def test_StockDataContainer_get_names_and_values__stockname_test1__ticker_t1__exchange_en(self):
        container = StockDataContainer("test1", "t1", "en")
        result_container = container.get_names_and_values()
        self.assertEqual(10, len(result_container))
        self.assertEqual({}, result_container["StrategyAndRecommendation"])
        self.assertEqual("t1", result_container["Ticker"])
        self.assertEqual("test1", result_container["Stockname"])
        self.assertEqual("en", result_container["Exchange"])

    def test_StockDataContainer__str__stockname_test1__ticker_t1__exchange_en(self):
        container = StockDataContainer("test1", "t1", "en")
        self.assertEqual("test1, t1", str(container))

    def test_NewsDataContainerDecorator_update_used_strategy_and_recommendation__stockname_test1__ticker_t1__exchange_en(
            self):
        container = StockDataContainer("test1", "t1", "en")
        container.update_used_strategy_and_recommendation("TestStrategy", "BUY")
        self.assertEqual("BUY", container.get_recommendation_strategies()["TestStrategy"][0])
        dt = parser.parse(container.get_recommendation_strategies()["TestStrategy"][1])
        elapsed = datetime.now() - dt
        self.assertGreater(timedelta(seconds=0.01), elapsed)
        sleep(0.05)

        container.update_used_strategy_and_recommendation("TestStrategy_2", "SELL")
        self.assertEqual("SELL", container.get_recommendation_strategies()["TestStrategy_2"][0])
        dt = parser.parse(container.get_recommendation_strategies()["TestStrategy_2"][1])
        elapsed = datetime.now() - dt
        self.assertGreater(timedelta(seconds=0.01), elapsed)

        container.update_used_strategy_and_recommendation("TestStrategy_3", "SELL")
        self.assertEqual("SELL", container.get_recommendation_strategies()["TestStrategy_3"][0])

        dt = parser.parse(container.get_recommendation_strategies()["TestStrategy_3"][1])
        sleep(0.05)
        elapsed = datetime.now() - dt
        self.assertGreater(elapsed, timedelta(seconds=0.01))

    def test_StockDataContainer_run_and_fill_with__W52HighTechnicalStrategy_BUY__and_SimplePatternNewsStrategy_BUY(
            self):
        w52hi_parameter_dict = {'check_days': 5, 'min_cnt': 3, 'min_vol_dev_fact': 1.2, 'within52w_high_fact': 0.98}

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
                ('2016-10-12', 23.16, 26, 23.11, 23.18, 46000)]

        df = DataFrame.from_records(data, columns=labels)
        stock_data_container = NewsDataContainerDecorator(StockDataContainer("Apple Inc.", "AAPL", ""), 0, 0,
                                                          "ANALYSE-FLASH: Credit Suisse nimmt Apple mit 'Outperform' wieder auf, BUY")
        stock_data_container.set_historical_stock_data(df)
        stock_data_container_list = [stock_data_container]
        ##################################################
        # 52 w strategy
        stock_screener = StrategyFactory()
        w52_hi_strat = stock_screener.prepare("W52HighTechnicalStrategy",
                                              stock_data_container_list=stock_data_container_list,
                                              analysis_parameters=w52hi_parameter_dict)
        # results = w52_hi_strat.run_strategy()
        w52_hi_strat.run_strategy()
        self.assertGreater(len(stock_data_container_list), 0)
        self.assertEqual("BUY",
                         stock_data_container_list[0].get_recommendation_strategies()["W52HighTechnicalStrategy"][0])

        dt = parser.parse(stock_data_container_list[0].get_recommendation_strategies()["W52HighTechnicalStrategy"][1])
        elapsed = datetime.now() - dt
        self.assertGreater(timedelta(seconds=0.01), elapsed)
        # stock_data_container_list = results

        ##############################
        # SimplePatternNewsStrategy
        parameter_dict = {'news_threshold': 0.7, 'german_tagger': filepath + 'nltk_german_classifier_data.pickle'}

        stock_screener = StrategyFactory()
        news_strategy = stock_screener.prepare("SimplePatternNewsStrategy",
                                               stock_data_container_list=stock_data_container_list,
                                               analysis_parameters=parameter_dict)

        news_strategy.run_strategy()
        self.assertEqual(stock_data_container_list[0].get_stock_name(), "Apple Inc.")
        self.assertEqual("BUY",
                         stock_data_container_list[0].get_recommendation_strategies()["W52HighTechnicalStrategy"][0])
        self.assertEqual("BUY",
                         stock_data_container_list[0].get_recommendation_strategies()["SimplePatternNewsStrategy"][0])

    def test_StockDataContainer__historical_stock_data(self):
        container = StockDataContainer("test1", "t1", "en")
        self.assertEqual([], container.historical_stock_data())

        cols = list(GlobalVariables.get_stock_data_labels_dict().values())
        data = [('2016-09-13', 90, 80, 100, 110, 4000)]

        df = DataFrame.from_records(data, columns=cols)
        container2 = StockDataContainer("Apple Inc.", "AAPL", "", df)
        sd = container2.historical_stock_data()

        self.assertEqual(sd[GlobalVariables.get_stock_data_labels_dict()['Date']][0], '2016-09-13')
        self.assertEqual(sd[GlobalVariables.get_stock_data_labels_dict()['Open']][0], 90)
        self.assertEqual(sd[GlobalVariables.get_stock_data_labels_dict()['High']][0], 80)
        self.assertEqual(sd[GlobalVariables.get_stock_data_labels_dict()['Low']][0], 100)
        self.assertEqual(sd[GlobalVariables.get_stock_data_labels_dict()['Close']][0], 110)
        self.assertEqual(sd[GlobalVariables.get_stock_data_labels_dict()['Volume']][0], 4000)

    def test_StockDataContainer__set_and_get_historical_stock_data(self):
        container = StockDataContainer("test1", "t1", "en")
        self.assertEqual([], container.historical_stock_data())

        cols = list(GlobalVariables.get_stock_data_labels_dict().values())
        data = [('2016-09-13', 90, 80, 100, 110, 4000)]

        df = DataFrame.from_records(data, columns=cols)
        apple_stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
        apple_stock_data_container.set_historical_stock_data(df)
        sd = apple_stock_data_container.historical_stock_data()

        self.assertEqual(sd[GlobalVariables.get_stock_data_labels_dict()['Date']][0], '2016-09-13')
        self.assertEqual(sd[GlobalVariables.get_stock_data_labels_dict()['Open']][0], 90)
        self.assertEqual(sd[GlobalVariables.get_stock_data_labels_dict()['High']][0], 80)
        self.assertEqual(sd[GlobalVariables.get_stock_data_labels_dict()['Low']][0], 100)
        self.assertEqual(sd[GlobalVariables.get_stock_data_labels_dict()['Close']][0], 110)
        self.assertEqual(sd[GlobalVariables.get_stock_data_labels_dict()['Volume']][0], 4000)

    def test_StockDataContainer__set_and_get_stock_current_prize(self):
        container = StockDataContainer("test1", "t1", "en" , [], 10)
        self.assertEqual(container.stock_current_prize(), 10)

        container2 = StockDataContainer("test1", "t1", "en")
        container2.set_stock_current_prize(20)
        self.assertEqual(container2.stock_current_prize(), 20)

