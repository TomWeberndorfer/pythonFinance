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
import soup as soup
from bs4 import BeautifulSoup
import urllib

from Utils.file_utils import read_tickers_from_file

filepath = 'C:\\temp\\'
stock_list_name = "stockList.txt"
stocks_to_buy_name = "StocksToBuy.CSV"
excel_file_name = '52W-HochAutomatisch_Finanzen.xlsx'
tickers_file_name = "tickers.pickle"
tickers_file = filepath + tickers_file_name

from urllib.request import urlopen

#link = "https://traderfox.de/nachrichten/dpa-afx-compact/kategorie-1-2-3-4-5-6-7-8-11-12-15/"
link = "https://traderfox.de/nachrichten/dpa-afx-compact/kategorie-2-5-8/" #analysen, ad hoc, unternehmen

resp = requests.get(link)
soup = bs.BeautifulSoup(resp.text, 'lxml')

#TODO instead of h2: article --> h2 --> a href
for elm in soup.find_all("h2"):
    #print(elm.get(".h2"))
    print (str(elm.get_text(strip=True)))
    #print (str(elm.contents[3].contents))


