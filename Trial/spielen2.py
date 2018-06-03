import os
import unittest

from DataReading.HistoricalDataReaders.HistoricalDataReader import HistoricalDataReader
from DataReading.NewsStockDataReaders.DataReaderFactory import DataReaderFactory
from DataReading.StockDataContainer import StockDataContainer
from Utils.file_utils import read_tickers_from_file
import pandas_datareader.data as web
import datetime

import socket
socket.setdefaulttimeout(5) # Time out after 5 seconds


def split_list(self, alist, wanted_parts=1):
    length = len(alist)
    return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
            for i in range(wanted_parts)]

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\TestData\\'
stock_data_container_file_name = "stock_data_container_file.pickle"
stock_data_container_file = filepath + stock_data_container_file_name

data_source = 'quandl'
weeks_delta = 52  # one year in the past


def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
            for i in range(wanted_parts)]

stock_data_container_list = read_tickers_from_file(stock_data_container_file, reload_file=True)

stock_data_container_list = split_list(stock_data_container_list, 3)
stock_data_container_list = stock_data_container_list[0]

data_storage = DataReaderFactory()
stock_data_reader = data_storage.prepare("HistoricalDataReader", stock_data_container_list, weeks_delta,
                                         stock_data_container_file, data_source,
                                         reload_stockdata=True)
stock_data_reader.read_data()

failed_reads = 0
for stock_data_container in stock_data_container_list:
    if len(stock_data_container.historical_stock_data) <= 0:
        failed_reads += 1

print("Failed reads: " + str(failed_reads))