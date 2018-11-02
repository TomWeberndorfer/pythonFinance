import unittest
from datetime import datetime
from DataReading.HistoricalDataReaders.HistoricalDataReader import HistoricalDataReader
from DataReading.DataReaderFactory import DataReaderFactory
from DataContainerAndDecorator.StockDataContainer import StockDataContainer
from Utils.GlobalVariables import *

########################################################################
# source code to evaluate the performance of ASTA-Framework
# Load 5 Stocks repetitive, 5 times and print the time for each loop
# Section 4.4 Bewertung - Performance
########################################################################

stock_data_container_list = []
apple_stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
fb_cont = StockDataContainer("Facebook, Inc.", "FB", "")
gis_cont = StockDataContainer("General Mills, Inc.", "GIS", "")
ge_cont = StockDataContainer("General Electric Company.", "GE", "")
xom_cont = StockDataContainer("Exxon Mobile Corporation", "XOM", "")

stock_data_container_list.append(apple_stock_data_container)
stock_data_container_list.append(fb_cont)
stock_data_container_list.append(gis_cont)
stock_data_container_list.append(ge_cont)
stock_data_container_list.append(xom_cont)

for i in range(0, 5):
    start_time = datetime.now()

    data_storage = DataReaderFactory()
    strategy_parameter_dict = {'Name': 'HistoricalDataReader', 'weeks_delta': 52, 'data_source': 'iex'}
    data_reader = HistoricalDataReader(stock_data_container_list,
                                       True, strategy_parameter_dict)
    data_reader.read_data()

    end_time = datetime.now()
    time_diff = end_time - start_time
    print("Time to get the stocks:" + (str(time_diff)))

# self.assertEqual(len(stock_data_container_list), 5)
# self.assertGreater(len(stock_data_container_list[0].historical_stock_data()), 200)
# self.assertGreater(len(stock_data_container_list[1].historical_stock_data()), 200)