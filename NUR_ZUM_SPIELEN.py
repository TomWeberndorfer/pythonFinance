import logging
from pandas_datareader import data
import pandas_datareader.data as web
from Utils import is_volume_high_enough, is_volume_raising, is52_w_high, write_stocks_to_buy_file, gap_up, \
    calculate_stopbuy_and_stoploss
from datetime import datetime, date, time
import pandas as pd


stocksToBuy = []

stocksToBuy.append({'buy': True, 'stockName':"Test", 'sb':15, 'sl': 11})
stocksToBuy.append({'buy': True, 'stockName':"t2", 'sb':12, 'sl': 11})


print (stocksToBuy)