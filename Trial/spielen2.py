from pandas_datareader import data
import googlefinance.client as google_client
import numpy as np
import pandas as pd


# Define the instruments to download. We would like to see Apple, Microsoft and the S&P500 index.
#tickers = ['AAPL']

# Define which online source one should use
#data_source = 'google'

# We would like all available data from 01/01/2000 until 12/31/2016.
#start_date = '2016-12-01'
#end_date = '2016-12-31'

# User pandas_reader.data.DataReader to load the desired data. As simple as that.
#panel_data = data.DataReader(tickers, data_source, start_date, end_date)
#print(len(panel_data))

# Dow Jones
#param = {
#     'q': "ETR:PUM", # Stock symbol (ex: "AAPL")
#     'i': "86400", # Interval size in seconds ("86400" = 1 day intervals)
#     #'x': "INDEXDJX", # Stock exchange symbol on which stock is traded (ex: "NASD")
#     #'x': "INDEXDB", # Stock exchange symbol on which stock is traded (ex: "NASD")
#     'p': "1M" # Period (Ex: "1Y" = 1 year)
# }
# # get price data (return pandas dataframe)
# df = google_client.get_price_data(param)
# print(df)

import talib
# list of functions
#print (talib.get_functions())

filepath = 'C:\\Users\\Tom\\OneDrive\\Dokumente\\Thomas\\Aktien\\testData\\'
file = filepath + 'avg_below.csv'
stock_data = pd.read_csv(file)

data_len = len(stock_data)
close_value = stock_data.iloc[data_len - 1].Close
yesterday_close_value = stock_data.iloc[data_len - 2].Close
tday_open_value = stock_data.iloc[data_len - 1].Open
tday_high_value = stock_data.iloc[data_len - 1].High
tday_low_value = stock_data.iloc[data_len - 1].Low

close_value = np.array([stock_data.Close])
high_value = np.array([stock_data.High])
low_value = np.array([stock_data.Low])

# real = ATR(high, low, close, timeperiod=14)
true_range = talib.ATR(high_value, low_value, close_value, timeperiod=14)

print(true_range)

#test