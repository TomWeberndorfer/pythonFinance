import inspect
from talib import abstract
import numpy
import os
import talib
import pandas as pd
from datetime import datetime
from datetime import timedelta

from DataRead_Google_Yahoo import read_data_from_google_with_pandas
from DataReading.HistoricalDataReaders.HistoricalDataReader import HistoricalDataReader
from DataReading.StockDataContainer import StockDataContainer
from Utils.common_utils import calc_true_range, calc_mean_true_range


# https://github.com/mrjbq7/ta-lib/issues/13
import talib
help(talib.SMA)


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\TestData\\'
stock_data_container_file_name = "stock_data_container_file.pickle"
stock_data_container_file = filepath + stock_data_container_file_name
date_file = filepath + 'last_date_time.csv'

stock_data_container = StockDataContainer("AAPL", "AAPL", "en")
stock_data_container_list = [stock_data_container]
data_source = 'iex'
weeks_delta = 52  # one year in the past
# TODO testen der genauen ergebnisse mit einer test datei stocks_dfs --> TestData...
data_reader = HistoricalDataReader(stock_data_container_list, weeks_delta, stock_data_container_file,
                                   data_source, False)
df = data_reader._get_ticker_data_with_webreader(stock_data_container.stock_ticker,
                                                 stock_data_container.stock_exchange,
                                                 data_source, weeks_delta=52)

result_sma = talib.SMA(df.close, timeperiod=30)
#print (result_sma)

#print (talib.get_functions())
funcs = talib.get_functions()
sma = abstract.Function('sma')
test = inspect.signature(sma)
t2 = inspect.getargvalues(sma)
print (t2)

# data_len = len(stock_data)
# high_value = numpy.array(stock_data.High)
# low_value = numpy.array(stock_data.Low)
# open_value = numpy.array(stock_data.Open)
# close_value = numpy.array(stock_data.Close)
#
# output = talib.CDLHAMMER(open_value, high_value, low_value, close_value)

#print(output)
# print(numpy.where(output==100))
# print ("high_value: " + str(high_value.item(19)))
# print ("low_value: " + str(low_value.item(19)))
# print ("open_value: " + str(open_value.item(19)))
# print ("close_value: " + str(close_value.item(19)))
# print()

#TODO see doc here:
# https://cryptotrader.org/talib
# https://github.com/mrjbq7/ta-lib/tree/master/docs/func_groups

#output = talib.SMA(high_value)
#print(output)

# true_range = talib.ATR(high_value, low_value, close_value, timeperiod=1)
#
# tr = []
# i = 0
# while i < len(stock_data):
#     yesterday_close_value = stock_data.iloc[i - 1].Close
#     tday_high_value = stock_data.iloc[i].High
#     tday_low_value = stock_data.iloc[i].Low
#     tr.append(calc_true_range (tday_high_value, tday_low_value, yesterday_close_value))
#
#     i += 1
#
# print(numpy.mean(tr))
#
# print("MEAN: " + str(numpy.nanmean(true_range)))
#
# print(":" + str(calc_mean_true_range(stock_data)))


