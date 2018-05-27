import os
import unittest
from pandas import DataFrame
from DataReading.StockDataContainer import StockDataContainer
from Strategies.StrategyFactory import StrategyFactory

# from directory UnitTests to --> root folder with: ..\\..\\
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\'


class TestStockDataContainer(unittest.TestCase):

    def test_eg_method(self):
        labels = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        data = [('2016-09-13', 90, 90, 100.15, 100.26, 4000),
                ('2016-09-14', 90, 90, 22.95, 100.11, 4000),
                ('2016-09-15', 90, 90, 100.14, 100.62, 4000)]

        df = DataFrame.from_records(data, columns=labels)
        apple_stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
        apple_stock_data_container.set_historical_stock_data(df)
        rwe_stock_data_container = StockDataContainer("RWE AG ST O.N.", "RWE", "")
        testag_stock_data_container = StockDataContainer("Test AG", "TestAG", "")
        rwe_stock_data_container.set_historical_stock_data(df)
        stock_data_container_list = [apple_stock_data_container, rwe_stock_data_container]

        #if apple_stock_data_container in stock_data_container_list:
        self.assertEquals(apple_stock_data_container in stock_data_container_list, True)
        self.assertEquals(rwe_stock_data_container in stock_data_container_list, True)
        self.assertEquals(testag_stock_data_container in stock_data_container_list, False)