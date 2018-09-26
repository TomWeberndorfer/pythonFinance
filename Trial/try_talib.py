import inspect

from pandas import DataFrame
from talib import abstract
import os
from Utils.GlobalVariables import *
from DataReading.HistoricalDataReaders.HistoricalDataReader import HistoricalDataReader
from DataContainerAndDecorator.StockDataContainer import StockDataContainer

# https://github.com/mrjbq7/ta-lib/issues/13
import talib

# help(talib.SMA)

test_data_filepath = GlobalVariables.get_test_data_files_path()
stock_data_container_file_name = "stock_data_container_file.pickle"
stock_data_container_file = test_data_filepath + stock_data_container_file_name
date_file = test_data_filepath + 'last_date_time.csv'

stock_data_container = StockDataContainer("AAPL", "AAPL", "en")
stock_data_container_list = [stock_data_container]
data_source = 'iex'
weeks_delta = 52  # one year in the past
# TODO testen der genauen ergebnisse mit einer test datei stocks_dfs --> TestData...
labels = []
for key, value in GlobalVariables.get_stock_data_labels_dict().items():
    labels.append(value)
data = [('2016-09-30', 23.35, 23.91, 23.24, 23.8, 31000),
        ('2016-10-03', 23.68, 23.69, 23.39, 23.5, 31000),
        ('2016-10-04', 23.52, 23.64, 23.18, 23.28, 31000),
        ('2016-10-05', 23.28, 23.51, 23.27, 23.43, 31000),
        ('2016-10-06', 23.38, 23.56, 23.29, 23.48, 42000),
        ('2016-10-07', 23.58, 23.65, 23.37, 23.48, 43000),
        ('2016-10-10', 23.62, 23.88, 23.55, 23.77, 44000),
        ('2016-10-11', 23.62, 23.74, 23.01, 23.16, 45000),
        ('2016-10-12', 23.16, 26, 23.11, 23.18, 46000)]

df = DataFrame.from_records(data, columns=labels)
stock_data_container = StockDataContainer("Apple Inc.", "AAPL", "")
stock_data_container.set_historical_stock_data(df)
stock_data_container_list = [stock_data_container]

# result_sma = talib.ROC(df.close, timeperiod=5)
result_sma = talib.SMA(df.close, timeperiod=5)
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


