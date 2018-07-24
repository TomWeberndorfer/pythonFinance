import os
import unittest
from pandas import DataFrame

from DataReading.NewsDataContainerDecorator import NewsDataContainerDecorator
from DataReading.StockDataContainer import StockDataContainer
from MvcModel import MvcModel
from Utils.GlobalVariables import *

# from directory UnitTests to --> root folder with: ..\\..\\
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\'


class TestMvcModel(unittest.TestCase):
    def test_update_column_list__add_several_columns__add_redundant_columns(self):
        model = MvcModel(None)
        self.assertEqual([], model.get_column_list())

        columns_to_add = ['StrategyAndRecommendation', 'Stockname']
        is_updated = model.update_column_list(columns_to_add)
        self.assertTrue(is_updated)
        self.assertEqual(columns_to_add, model.get_column_list())

        columns_to_add_2 = ["Ticker", "Exchange"]
        is_updated = model.update_column_list(columns_to_add_2)
        self.assertTrue(is_updated)
        cols = columns_to_add
        cols.extend(columns_to_add_2)
        self.assertEqual(cols, model.get_column_list())

        # redundant columns should not be added again
        redundant_cols = ['Stockname', "Ticker"]
        is_updated = model.update_column_list(redundant_cols)
        self.assertFalse(is_updated)
        self.assertEqual(cols, model.get_column_list())
