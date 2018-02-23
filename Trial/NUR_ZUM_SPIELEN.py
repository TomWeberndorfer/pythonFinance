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
def read_and_save_sp500_tickers(tickers_file):
    """
    read the sp500 tickers and saves it to given file
    :param tickers_file: file to save the sp500 tickers
    :return: nothing
    """
    resp = requests.get('https://de.wikipedia.org/wiki/Liste_der_im_CDAX_gelisteten_Aktien')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable zebra'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[2].text
        tickers.append(ticker)

    with open(tickers_file, "wb") as f:
        pickle.dump(tickers, f)

#read_and_save_sp500_tickers(tickers_file)

read_tickers(tickers_file, True)