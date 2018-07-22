import os
import unittest
from pandas import DataFrame
from DataReading.StockDataContainer import StockDataContainer
from Utils.GlobalVariables import *

# from directory UnitTests to --> root folder with: ..\\..\\
from Utils.common_utils import get_current_class_and_function_name, print_err_message

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
        self.assertEqual(3, len(result_container))
        self.assertEqual("t1", result_container["Ticker"])
        self.assertEqual("test1", result_container["Stockname"])
        self.assertEqual("en", result_container["Stock Exchange"])

    def test_StockDataContainer__str__stockname_test1__ticker_t1__exchange_en(self):
        container = StockDataContainer("test1", "t1", "en")
        self.assertEqual("test1, t1", str(container))

    def test_NewsDataContainerDecorator_append_used_strategy__stockname_test1__ticker_t1__exchange_en(self):
        container = StockDataContainer("test1", "t1", "en")
        container.append_used_strategy("TestStrategy")
        self.assertEqual(["TestStrategy"], container.get_recommendation_strategies())

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

