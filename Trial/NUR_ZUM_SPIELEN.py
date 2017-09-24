import logging
import traceback
from urllib.request import urlopen

import urllib3
from pandas_datareader import data
import pandas_datareader.data as web


from Utils import signal_is_volume_high_enough, signal_is52_w_high, append_to_file, signal_gap_up, \
    calculate_stopbuy_and_stoploss, get_current_function_name, read_data_from_yahoo
from Signals import signal_is_volume_raising, signal_is52_w_high, signal_gap_up, signal_is_volume_high_enough
from DataRead_Google_Yahoo import read_data_from_google_with_pandas, read_data_from_yahoo
from datetime import datetime, date, time
import pandas as pd
import pandas as pd
from pandas_datareader import data, wb
# import pandas.io.data as web  # Package and modules for importing data; this code may change depending on pandas version
from datetime import datetime, date, time
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import timedelta
import sys
import threading
import webbrowser
from yahoo_finance import Share
import ystockquote
from pprint import pprint

#from googlefinance.client import get_price_data, get_prices_data, get_prices_time_data
import googlefinance.client as google_client
import pandas_datareader as pdr
from pandas_datareader import data as dreader




##########################
# config
num_of_stocks_per_thread = 5
volume_day_delta = 5
volume_avg_day_delta = 15
end = datetime.now()
ago52_w = (end - timedelta(weeks=52))
ago_w = (end - timedelta(weeks=1))
yesterday = (end -timedelta(days=1))
stock_name = 'GFT'
yahoo = Share(stock_name)
#  YYMMDD
#print (ago52_w.strftime("%y-%m-%d"))
#print(yahoo.get_historical('2014-04-25', '2014-04-29'))
#print (yahoo.get_avg_daily_volume())
#print (yahoo.get_trade_datetime())
#print(yahoo.get_price())
#print()

program_start_time = datetime.now()
# Dow Jones
param = {
    'q': "AAPL", # Stock symbol (ex: "AAPL")
    'i': "86400", # Interval size in seconds ("86400" = 1 day intervals)
    #'x': "INDEXDJX", # Stock exchange symbol on which stock is traded (ex: "NASD")
    'p': "1Y" # Period (Ex: "1Y" = 1 year)
}
# get price data (return pandas dataframe)
df = google_client.get_price_data(param)
print(df)

#stock52_w = data.DataReader("AAPL", "google", ago52_w.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
#print (stock52_w.iloc[len(stock52_w) - 1])

#stock52_w = read_data_from_google_with_pandas(stock_name, ago52_w, end)
#print(yahoo.get_historical("2017-04-25", "2017-04-25"))

#from pandas_datareader import data as pdr
#import fix_yahoo_finance as yf
#yf.pdr_override() # <== that's all it takes :-)
#data = pdr.get_data_yahoo("AAPL", start="2016-09-23", end="2017-09-21")
#print (data)

#print ("-----------")
#stock52_w = read_data_from_google_with_pandas(stock_name, ago_w, end)
#print (stock52_w)
#print (len(stock52_w))

# cols = ['Date','Open','High','Low','Close','Volume']
# lst = []
#currDate = (yahoo.get_trade_datetime())[0:10]
# lst.append([currDate, yahoo.get_price(),yahoo.get_days_high(),yahoo.get_days_low(),yahoo.get_price(),yahoo.get_volume()])
# df1 = pd.DataFrame(lst, columns=cols)
# df1.index.name = 'Date'
# #df1.set_index([str(currDate)])
# df1 = df1.set_index(['Date'])
# #print("name: " + str(df1.index.name))
# #print(df1.iloc[0])
# print('-------------')
#
# #stock52_w.loc[len(stock52_w)]=[yahoo.get_price(),yahoo.get_days_high(),yahoo.get_days_low(),yahoo.get_price(),yahoo.get_volume()]
# #stock52_w.iloc[len(stock52_w) - 1].name = datetime.utcnow()
# #print("name: " + str(stock52_w.index.name))
# stock_t = stock52_w.append(df1)
#
#print(stock52_w.iloc[0])
# print(stock_t.iloc[len(stock_t) - 1])
# print(stock_t.iloc[len(stock_t) - 2])

import sys
# try:
#     stock = []
#     stock.iloc[9]
# except Exception as e:
#    # traceback.format_exc()
#     traceback.print_exc()
#
# print("Ok")

stock52_w = data.DataReader("ETR:" + stock_name, "google", '2017-09-01', '2017-09-21')
print(str(stock52_w))