import os
import unittest
from datetime import datetime

from DataReading.HistoricalDataReaders.HistoricalDataReader import HistoricalDataReader
from DataReading.StockDataContainer import StockDataContainer
from Utils.file_utils import FileUtils
from newsTrading.GermanTaggerAnalyseNews import GermanTaggerAnalyseNews


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\'


class TestGoogleHistoricalDataReader(unittest.TestCase):

    def test_get_ticker_data_with_webreader(self):
        stock_data_container_list = []

        # Todo mit mehreren testen, auch ohne file --> fileinhalt mit übergeben --> dann kann ichs faken
        # --> file zugriff nicht im webreader drinnen
        stock_data_container = StockDataContainer("BHGE", "BHGE", "en")
        stock_data_container_list.append(stock_data_container)

        self.assertEqual(len(stock_data_container_list[0].historical_stock_data), 0)

        # TODO testen der genauen ergebnisse mit einer test datei stocks_dfs --> TestData...
        data_reader = HistoricalDataReader()
        df = data_reader._get_ticker_data_with_webreader(stock_data_container.stock_ticker,
                                                         stock_data_container.stock_exchange, stock_dfs_file="",
                                                         source='yahoo', weeks_delta=52, reload_stockdata=True)

        self.assertGreater(len(df), 200)



    def test_read_data_without_factory(self):
        stock_data_container_list = []

    #Todo mit mehreren testen, auch ohne file --> fileinhalt mit übergeben --> dann kann ichs faken
    #--> file zugriff nicht im webreader drinnen
        apple_stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
        intel_container =StockDataContainer("Intel Corporation", "INTC", "")
        stock_data_container_list.append(apple_stock_data_container)
        stock_data_container_list.append(intel_container)

        self.assertEqual(len(stock_data_container_list[0].historical_stock_data), 0)

        #TODO testen der genauen ergebnisse mit einer test datei stocks_dfs --> TestData...
        data_reader = HistoricalDataReader()
        data_reader.read_data(stock_data_container_list, 52, filepath + 'TestData', "yahoo", reload_stockdata=False)

        #the container must have at least 200 entry days for last and current year
        self.assertGreater(len(stock_data_container_list[0].historical_stock_data), 200)
        self.assertGreater(len(stock_data_container_list[1].historical_stock_data), 200)
        self.assertNotEqual(stock_data_container_list[1].historical_stock_data.High[0], stock_data_container_list[0].historical_stock_data.High[0])
