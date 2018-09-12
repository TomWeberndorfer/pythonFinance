import unittest

from DataReading.HistoricalDataReaders.HistoricalDataReader import HistoricalDataReader
from DataReading.DataReaderFactory import DataReaderFactory
from DataContainerAndDecorator.StockDataContainer import StockDataContainer
from Utils.GlobalVariables import *

test_data_filepath = GlobalVariables.get_test_data_files_path()
stock_data_container_file_name = "stock_data_container_file.pickle"
stock_data_container_file = test_data_filepath + stock_data_container_file_name
date_file = test_data_filepath + 'last_date_time.csv'

data_source = 'iex'
#data_source = 'morningstar'
weeks_delta = 52  # one year in the past

stock_list = ["DIM", "CBK", "CR"]  # "ENEL"]
stock_data_container_list_2 = []

for stock in stock_list:
    cont = StockDataContainer(stock, stock, "")
    stock_data_container_list_2.append(cont)


class TestGoogleHistoricalDataReader(unittest.TestCase):

    def test_read_data_without_factory_but_HistoricalDataReader(self):
        stock_data_container_list = []
        # Todo mit mehreren testen, auch ohne file --> fileinhalt mit übergeben --> dann kann ichs faken
        # --> file zugriff nicht im webreader drinnen
        apple_stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
        intel_container = StockDataContainer("Intel Corporation", "INTC", "")
        stock_data_container_list.append(apple_stock_data_container)
        stock_data_container_list.append(intel_container)

        self.assertEqual(len(stock_data_container_list[0].historical_stock_data()), 0)

        strategy_parameter_dict = {'Name': 'HistoricalDataReader', 'weeks_delta': 52, 'data_source': 'iex'}
        # TODO testen der genauen ergebnisse mit einer test datei stocks_dfs --> TestData...
        data_reader = HistoricalDataReader(stock_data_container_list,
                                           False, strategy_parameter_dict)
        data_reader.read_data()

        # the container must have at least 200 entry days for last and current year
        self.assertEqual(len(stock_data_container_list), 2)
        self.assertGreater(len(stock_data_container_list[0].historical_stock_data()), 200)
        self.assertGreater(len(stock_data_container_list[1].historical_stock_data()), 200)
        self.assertNotEqual(
            stock_data_container_list[1].historical_stock_data()[GlobalVariables.get_stock_data_labels_dict()['High']][0],
            stock_data_container_list[0].historical_stock_data()[GlobalVariables.get_stock_data_labels_dict()['High']][0])

    def test_read_data_without_factory_but_HistoricalDataReader_GermanStock(self):
        stock_data_container_list = []
        # Todo mit mehreren testen, auch ohne file --> fileinhalt mit übergeben --> dann kann ichs faken
        # --> file zugriff nicht im webreader drinnen
        rwe_stock_data_container = StockDataContainer("RWE AG ST O.N.", "RWE.de", "")
        stock_data_container_list.append(rwe_stock_data_container)

        self.assertEqual(len(stock_data_container_list[0].historical_stock_data()), 0)

        strategy_parameter_dict = {'Name': 'HistoricalDataReader', 'weeks_delta': 52, 'data_source': 'iex'}
        # TODO testen der genauen ergebnisse mit einer test datei stocks_dfs --> TestData...
        data_reader = HistoricalDataReader(stock_data_container_list,
                                           False, strategy_parameter_dict)
        data_reader.read_data()

        # the container must have at least 200 entry days for last and current year
        self.assertEqual(len(stock_data_container_list), 1)
        self.assertGreater(len(stock_data_container_list[0].historical_stock_data()), 200)

    def test_read_data_without_factory_t(self):

        # TODO testen der genauen ergebnisse mit einer test datei stocks_dfs --> TestData...
        strategy_parameter_dict = {'Name': 'HistoricalDataReader', 'weeks_delta': 52, 'data_source': 'iex'}
        data_reader = HistoricalDataReader(stock_data_container_list_2,
                                           True, strategy_parameter_dict)
        data_reader.read_data()

        for sd in stock_data_container_list_2:
            self.assertGreater(len(sd.historical_stock_data()), 100, str(sd.get_stock_name()))

    def test_read_data_with_DataReaderFactory__HistoricalDataReader_read_apple__read_intel(self):
        stock_data_container_list = []
        apple_stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
        intel_container = StockDataContainer("Intel Corporation", "INTC", "")
        stock_data_container_list.append(apple_stock_data_container)
        stock_data_container_list.append(intel_container)

        self.assertEqual(len(stock_data_container_list[0].historical_stock_data()), 0)

        data_storage = DataReaderFactory()
        strategy_parameter_dict = {'Name': 'HistoricalDataReader', 'weeks_delta': 52, 'data_source': 'iex'}
        stock_data_reader = data_storage.prepare("HistoricalDataReader",
                                                 stock_data_container_list=stock_data_container_list,
                                                 reload_stockdata=True, parameter_dict=strategy_parameter_dict)
        stock_data_reader.read_data()

        self.assertEqual(len(stock_data_container_list), 2)
        self.assertGreater(len(stock_data_container_list[0].historical_stock_data()), 200)
        self.assertGreater(len(stock_data_container_list[1].historical_stock_data()), 200)
