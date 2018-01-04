import logging
import traceback
from urllib.request import urlopen

import urllib3
from pandas_datareader import data
import pandas_datareader.data as web

from datetime import datetime, date, time
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import timedelta
import sys
import threading
import webbrowser
from yahoo_finance import Share

from pprint import pprint

#from googlefinance.client import get_price_data, get_prices_data, get_prices_time_data
import googlefinance.client as google_client
import pandas_datareader as pdr
from pandas_datareader import data as dreader

# from pandas_datareader import data as pdr
# import fix_yahoo_finance as yf
# yf.pdr_override() # <== that's all it takes :-)
# data = pdr.get_data_yahoo("AAPL", start="2016-09-23", end="2017-09-21")
# print (data)

start= datetime.now()

from DataRead_Google_Yahoo import read_data_from_yahoo, read_current_day_from_yahoo

# d = read_data_from_yahoo("ADS.DE", "2017-09-20", "2017-09-22")
# print(d)
# d = read_data_from_yahoo("PUM.DE", "2017-09-20", "2017-09-22")
# print(d)
# d = read_data_from_yahoo("AAPL", "2017-09-20", "2017-09-22")
# print(d)
d = read_data_from_yahoo("BMW.DE", "2017-09-20", "2017-09-23")
print(d)
#end= datetime.now()

print("------\n")
#d= read_current_day_from_yahoo("BMW.DE")
yahoo = Share("BMW.DE")
currDate = (yahoo.get_trade_datetime())[0:10]
print(str(currDate) + ", " + str(yahoo.get_open()) + ", " + str(yahoo.get_days_high()) + ", " + str(yahoo.get_days_low())
      + ", " + str(yahoo.get_price()) + ", " + str(yahoo.get_volume()))
#print(str(end - start))
