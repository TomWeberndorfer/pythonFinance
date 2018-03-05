import numpy
import talib
import pandas as pd
from datetime import datetime
from datetime import timedelta

from DataRead_Google_Yahoo import read_data_from_google_with_pandas
from Utils.Utils import calc_true_range, calc_mean_true_range

filepath = 'C:\\Users\\Tom\\OneDrive\\Dokumente\\Thomas\\Aktien\\testData\\'
file = filepath + 'atr.csv'
#stock_data = pd.read_csv(file)
end = datetime.now()
ago52_w = (end - timedelta(weeks=52))
stock_data = read_data_from_google_with_pandas("AAPL", ago52_w, end)

data_len = len(stock_data)

high_value = numpy.array(stock_data.High)
low_value = numpy.array(stock_data.Low)
open_value = numpy.array(stock_data.Open)
close_value = numpy.array(stock_data.Close)

output = talib.CDLHAMMER(open_value, high_value, low_value, close_value)
#print(output)
print(numpy.where(output==100))
print ("high_value: " + str(high_value.item(19)))
print ("low_value: " + str(low_value.item(19)))
print ("open_value: " + str(open_value.item(19)))
print ("close_value: " + str(close_value.item(19)))
print()

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


