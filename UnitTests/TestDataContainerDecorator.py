import os
import unittest
from pandas import DataFrame
from datetime import datetime, timedelta
from dateutil import parser
from DataReading.NewsDataContainerDecorator import NewsDataContainerDecorator
from DataReading.StockDataContainer import StockDataContainer
from Utils.GlobalVariables import *

# from directory UnitTests to --> root folder with: ..\\..\\
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\'


class TestDataContainerDecorator(unittest.TestCase):
    def test_NewsDataContainerDecorator_get_names_and_values__target_price_111__stockname_test1(self):
        container = StockDataContainer("test1", "t1", "en")
        result_container = container.get_names_and_values()
        self.assertEqual(9, len(result_container))

        news_dec = NewsDataContainerDecorator(container, 111, 0.9, "test news", 99)
        result_news_dec = news_dec.get_names_and_values()
        self.assertEqual(13, len(result_news_dec))
        self.assertEqual({}, result_news_dec["StrategyAndRecommendation"])
        self.assertEqual(111, result_news_dec["Target Price"])
        self.assertEqual("test1", result_news_dec["Stockname"])
        self.assertEqual(0.9, result_news_dec["Pos. Probability Distribution"])

    def test_NewsDataContainerDecorator_update_used_strategy_and_recommendation(self):
        container = StockDataContainer("test1", "t1", "en")
        news_dec = NewsDataContainerDecorator(container, 111, 0.9, "test news", 99)
        news_dec.update_used_strategy_and_recommendation("TestStrategy", "BUY")
        res_dict = news_dec.get_recommendation_strategies()
        self.assertEqual(1, len(res_dict))

        rec_and_datetime = res_dict["TestStrategy"]
        self.assertEqual(2, len(rec_and_datetime))
        rec = rec_and_datetime[0]
        dt = parser.parse(rec_and_datetime[1])
        self.assertEqual("BUY", rec)
        elapsed = datetime.now() - dt
        self.assertGreater(timedelta(seconds=0.1), elapsed)

        news_dec.update_used_strategy_and_recommendation("TestStrategy_2", "SELL")

        res_dict = news_dec.get_recommendation_strategies()
        self.assertEqual(2, len(res_dict))

        rec_and_datetime = res_dict["TestStrategy"]
        self.assertEqual(2, len(rec_and_datetime))
        rec = rec_and_datetime[0]
        dt = parser.parse(rec_and_datetime[1])
        self.assertEqual("BUY", rec)
        elapsed = datetime.now() - dt
        self.assertGreater(timedelta(seconds=0.01), elapsed)

        rec_and_datetime = res_dict["TestStrategy_2"]
        self.assertEqual(2, len(rec_and_datetime))
        rec = rec_and_datetime[0]
        dt = parser.parse(rec_and_datetime[1])
        self.assertEqual("SELL", rec)
        elapsed = datetime.now() - dt
        self.assertGreater(timedelta(seconds=0.01), elapsed)

    def test_NewsDataContainerDecorator_test_rank(self):
        container = StockDataContainer("test1", "t1", "en")
        pos_prob_dist = 0
        news_dec = NewsDataContainerDecorator(container, 111, pos_prob_dist, "test news", 99)
        news_dec.update_used_strategy_and_recommendation("TestStrategy", "SELL")
        self.assertEqual(-3, news_dec.get_rank())

        pos_prob_dist = 0.49
        news_dec = NewsDataContainerDecorator(container, 111, pos_prob_dist, "test news", 99)
        news_dec.update_used_strategy_and_recommendation("TestStrategy", "BUY")
        self.assertEqual(0, news_dec.get_rank())

        pos_prob_dist = 0.51
        news_dec = NewsDataContainerDecorator(container, 111, pos_prob_dist, "test news", 99)
        news_dec.update_used_strategy_and_recommendation("TestStrategy", "BUY")
        self.assertEqual(2, news_dec.get_rank())

        pos_prob_dist = 0.76
        news_dec = NewsDataContainerDecorator(container, 111, pos_prob_dist, "test news", 99)
        news_dec.update_used_strategy_and_recommendation("TestStrategy", "BUY")
        self.assertEqual(3, news_dec.get_rank())

        pos_prob_dist = 1
        news_dec = NewsDataContainerDecorator(container, 111, pos_prob_dist, "test news", 99)
        news_dec.update_used_strategy_and_recommendation("TestStrategy", "BUY")
        self.assertEqual(3, news_dec.get_rank())

        pos_prob_dist = 1
        news_dec = NewsDataContainerDecorator(container, 111, pos_prob_dist, "test news", 99)
        news_dec.update_used_strategy_and_recommendation("TestStrategy", "SELL")
        self.assertEqual(1, news_dec.get_rank())
