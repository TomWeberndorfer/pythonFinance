import os
import unittest

from DataReading.HistoricalDataReaders.HistoricalDataReader import HistoricalDataReader
from DataReading.NewsStockDataReaders.DataReaderFactory import DataReaderFactory
from DataReading.StockDataContainer import StockDataContainer
from Utils.file_utils import read_tickers_from_file
import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\TestData\\'
stock_data_container_file_name = "stock_data_container_file.pickle"
stock_data_container_file = filepath  + stock_data_container_file_name

reader_stocks_per_threads = 2  # TODO manchmal gehts ned mit so viele threads --> max threads ~ 800
data_source = 'yahoo'
weeks_delta = 52  # one year in the past


class TestGoogleHistoricalDataReader(unittest.TestCase):

    def test_get_ticker_data_with_webreader(self):
        stock_data_container_list = []
        # Todo mit mehreren testen, auch ohne file --> fileinhalt mit übergeben --> dann kann ichs faken
        # --> file zugriff nicht im webreader drinnen
        stock_data_container = StockDataContainer("BHGE", "BHGE", "en")
        stock_data_container_list.append(stock_data_container)

        self.assertEqual(len(stock_data_container_list[0].historical_stock_data), 0)

        # TODO testen der genauen ergebnisse mit einer test datei stocks_dfs --> TestData...
        data_reader = HistoricalDataReader(reader_stocks_per_threads)
        df = data_reader._get_ticker_data_with_webreader(stock_data_container.stock_ticker,
                                                         stock_data_container.stock_exchange,
                                                         data_source='yahoo', weeks_delta=52)

        self.assertGreater(len(df), 200)

    def test_read_data_without_factory(self):
        stock_data_container_list = []
        # Todo mit mehreren testen, auch ohne file --> fileinhalt mit übergeben --> dann kann ichs faken
        # --> file zugriff nicht im webreader drinnen
        apple_stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
        intel_container = StockDataContainer("Intel Corporation", "INTC", "")
        stock_data_container_list.append(apple_stock_data_container)
        stock_data_container_list.append(intel_container)

        self.assertEqual(len(stock_data_container_list[0].historical_stock_data), 0)

        # TODO testen der genauen ergebnisse mit einer test datei stocks_dfs --> TestData...
        data_reader = HistoricalDataReader(reader_stocks_per_threads)
        data_reader.read_data(stock_data_container_list, 52, stock_data_container_file, "yahoo", reload_stockdata=True)

        # the container must have at least 200 entry days for last and current year
        self.assertGreater(len(stock_data_container_list[0].historical_stock_data), 200)
        self.assertGreater(len(stock_data_container_list[1].historical_stock_data), 200)
        self.assertNotEqual(stock_data_container_list[1].historical_stock_data.High[0],
                            stock_data_container_list[0].historical_stock_data.High[0])

    def test_read_data(self):
        stock_data_container_list = []
        apple_stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
        intel_container = StockDataContainer("Intel Corporation", "INTC", "")
        stock_data_container_list.append(apple_stock_data_container)
        stock_data_container_list.append(intel_container)

        self.assertEqual(len(stock_data_container_list[0].historical_stock_data), 0)

        data_storage = DataReaderFactory()
        stock_data_reader = data_storage.prepare("HistoricalDataReader", reader_stocks_per_threads)
        stock_data_reader.read_data(stock_data_container_list, weeks_delta, stock_data_container_file, data_source,
                                    reload_stockdata=True)

        self.assertEqual(len(stock_data_container_list), 2)
        self.assertGreater(len(stock_data_container_list[0].historical_stock_data), 200)
        self.assertGreater(len(stock_data_container_list[1].historical_stock_data), 200)

    def test_read_data_all(self):
        stock_data_container_list = read_tickers_from_file(stock_data_container_file, reload_file=False)

        # TODO abstract factory: http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Factory.html
        # TODO eventuell als return statt als call by reference: stock_data_container_list = data_storage.read_data("HistoricalDataReader", stock_data_container_list, weeks_delta, filepath + 'stock_dfs')
        # TODO relead data
        data_storage = DataReaderFactory()
        stock_data_reader = data_storage.prepare("HistoricalDataReader", reader_stocks_per_threads)
        stock_data_reader.read_data(stock_data_container_list, weeks_delta, stock_data_container_file, data_source,
                                    reload_stockdata=True)

        failed_reads = 0
        for stock_data_container in stock_data_container_list:
            if len(stock_data_container.historical_stock_data) <= 0:
                failed_reads += 1
            # self.assertGreater(len(stock_data_container_list[0].historical_stock_data), 200)

        print ("Failed reads: " + str(failed_reads))

        self.assertEqual(len(stock_data_container_list), 818)
        self.assertGreater(len(stock_data_container_list[0].historical_stock_data), 200)
        self.assertGreater(len(stock_data_container_list[1].historical_stock_data), 200)