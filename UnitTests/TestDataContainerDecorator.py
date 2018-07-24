import os
import unittest
from pandas import DataFrame

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
        self.assertEqual(4, len(result_container))

        news_dec = NewsDataContainerDecorator(container, 111, 0.9, "test news", 99)
        result_news_dec = news_dec.get_names_and_values()
        self.assertEqual(8, len(result_news_dec))
        self.assertEqual({}, result_news_dec["StrategyAndRecommendation"])
        self.assertEqual(111, result_news_dec["Target Price"])
        self.assertEqual("test1", result_news_dec["Stockname"])
        self.assertEqual(0.9, result_news_dec["Pos. Probability Distribution"])

    def test_NewsDataContainerDecorator_updated_used_strategy_and_recommendation(self):
        container = StockDataContainer("test1", "t1", "en")
        news_dec = NewsDataContainerDecorator(container, 111, 0.9, "test news", 99)
        news_dec.updated_used_strategy_and_recommendation("TestStrategy", "BUY")
        self.assertEqual({"TestStrategy": "BUY"}, news_dec.get_recommendation_strategies())

        news_dec.updated_used_strategy_and_recommendation("TestStrategy_2", "SELL")
        self.assertEqual({"TestStrategy": "BUY", "TestStrategy_2": "SELL"}, news_dec.get_recommendation_strategies())
