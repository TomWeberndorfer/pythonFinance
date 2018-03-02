import datetime
import pickle
import sys
import os

import bs4 as bs
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy
import requests
# from matplotlib import style
import plotly.graph_objs as go
# from matplotlib.finance import candlestick_ohlc
import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd

from Utils import read_tickers

filepath = 'C:\\temp\\'
stock_list_name = "stockList.txt"
stocks_to_buy_name = "StocksToBuy.CSV"
excel_file_name = '52W-HochAutomatisch_Finanzen.xlsx'
tickers_file_name = "tickers.pickle"
tickers_file = filepath + tickers_file_name

from DataRead_Google_Yahoo import __get_symbols_from_names

all_names = []
all_names.append("4SC+AG")
tickers, names_with_symbols = __get_symbols_from_names(all_names)