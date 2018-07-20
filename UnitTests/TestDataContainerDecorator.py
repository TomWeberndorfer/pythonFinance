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
        self.assertEqual(3, len(result_container))

        news_dec = NewsDataContainerDecorator(container, "111", "0.9", "test news", "99")
        result_news_dec = news_dec.get_names_and_values()
        self.assertEqual(7, len(result_news_dec))
        self.assertEqual("111", result_news_dec["Target Price"])
        self.assertEqual("test1", result_news_dec["Stockname"])
