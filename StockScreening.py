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

from MyThread import MyThread
from Utils import  is52W_High, isVolumeHighEnough, splitStockList, getSymbolFromName, \
    get52W_H_Symbols_FromExcel, \
    write_stocks_to_buy_file
from Strategies import strat_scheduler

import time
import logging

exitFlag = 0
threads = []
stocksToBuy = []
err = []

program_start_time = datetime.now()

##########################
# config
numOfStocksPerThread = 5
volumeDayDelta = 5
volumeAvgDayDelta = 15
end = datetime.now()
Ago52W = (end - timedelta(weeks=52))

#Ago5D = datetime.datetime.now() - timedelta(days=volumeDayDelta)
#Ago10D = datetime.datetime.now() - timedelta(days=volumeAvgDayDelta)
dataProvider = "google"
#dataProvider = "yahoo"

# enhanced stock messages:
# logging.basicConfig(level=logging.DEBUG)

##########################

# symbols to read
Nasdaq100_Symbols = ["AAPL", "ADBE", "ADI", "ADP", "ADSK", "AKAM", "ALXN",
                     "AMAT", "AMGN", "AMZN", "ATVI", "AVGO", "BBBY", "BIDU", "BIIB",
                     "BRCM", "CA", "CELG", "CERN", "CHKP", "CHRW", "CHTR", "CMCSA",
                     "COST", "CSCO", "CTRX", "CTSH", "CTXS", "DISCA", "DISCK", "DISH",
                     "DLTR", "EBAY", "EQIX", "ESRX", "EXPD", "EXPE", "FAST",
                     "FB", "FFIV", "FISV", "FOXA", "GILD", "GMCR", "GOOG",
                     "GRMN", "HSIC", "ILMN", "INTC", "INTU", "ISRG", "KLAC", "KRFT",
                     "LBTYA", "LLTC", "LMCA", "LMCK", "LVNTA", "MAR", "MAT", "MDLZ",
                     "MNST", "MSFT", "MU", "MXIM", "MYL", "NFLX", "NTAP", "NVDA",
                     "NXPI", "ORLY", "PAYX", "PCAR", "PCLN", "QCOM", "QVCA", "REGN",
                     "ROST", "SBAC", "SBUX", "SIAL", "SIRI", "SNDK", "SPLS", "SRCL",
                     "STX", "SYMC", "TRIP", "TSCO", "TSLA", "TXN", "VIAB", "VIP",
                     "VOD", "VRSK", "VRTX", "WDC", "WFM", "WYNN", "XLNX", "YHOO", "NOC"]

DAX_Symbols = ["ETR:ADS", "ETR:ALV", "ETR:BAS", "ETR:BAY", "ETR:BMW", "ETR:CBK", "ETR:CON", "ETR:DAI",
               "ETR:DB1", "ETR:DBK", "ETR:DPB", "ETR:DPW", "ETR:DTE", "ETR:FME", "ETR:HEN3",
               "ETR:IFX", "ETR:LHA", "ETR:LIN", "ETR:MAN", "ETR:MEO", "ETR:MRK.DE", "ETR:MUV2",
               "ETR:RWE", "ETR:SAP", "ETR:SIE", "ETR:TKA", "ETR:TUI1", "ETR:VOW", "ETR:BAYN",
               "ETR:FNTN", "ETR:O2D", "ETR:QIA", "ETR:DRI", "ETR:AM3D", "ETR:O1BC", "ETR:GFT", "ETR:NDX1",
               "ETR:SBS", "ETR:COK", "ETR:DLG", "ETR:DRW3", "ETR:SMHN", "ETR:WDI", "ETR:BC8", "ETR:MOR",
               "ETR:SOW", "ETR:AIXA", "ETR:ADV", "ETR:PFV", "ETR:JEN", "ETR:AFX", "ETR:UTDI", "ETR:NEM", "ETR:SRT3",
               "ETR:EVT", "ETR:WAF", "ETR:RIB", "ETR:S92", "ETR:COP", "ETR:TTR1", "ETR:SZG", "ETR:VT9"]

allSymbols = []

###############################################################################################
# enter stock filter options
# 0 = alles (Dax + nasdaq + excel)
# 1 = VERSUCH DAX
# 2 = VERSUCH NASDAQ
# 3 = nur finanzen excel
# 4 = NORMAL nur DAX und NASDAQ
option = 0
###########################################################

# versuch DAX
if (option == 1):
    DAX_Symbols = ["BSX", "MU", "CNP"]
    allSymbols.extend(DAX_Symbols)

# versuch NASDAQ
if (option == 2):
    Nasdaq100_Symbols = ["AAPL"]
    allSymbols.extend(Nasdaq100_Symbols)

# ----------------------------------------------
# alles Dax + nasdaq + excel
if (option == 0):
    symbols52W_Hi = get52W_H_Symbols_FromExcel()
    allSymbols.extend(symbols52W_Hi)
    allSymbols.extend(Nasdaq100_Symbols)
    allSymbols.extend(DAX_Symbols)

# nur finanzen excel
if (option == 3):
    symbols52W_Hi = get52W_H_Symbols_FromExcel()
    allSymbols.extend(symbols52W_Hi)

# NORMAL: nur DAX und NASDAQ
if (option == 4):
    allSymbols.extend(Nasdaq100_Symbols)
    allSymbols.extend(DAX_Symbols)

# Create new threads
splits = splitStockList(allSymbols, numOfStocksPerThread)
stock_screening_threads = MyThread("stock_screening_threads")


def function_for_threading_strat_scheduler(ch, dataProvider, Ago52W, end):
    print("Started with: " + str(ch))
    stocksToBuy.extend(strat_scheduler(ch, dataProvider, Ago52W, end))


i = 0
while i < len(splits):
    ch = splits[i]
    stock_screening_threads.append_thread(
        threading.Thread(target=function_for_threading_strat_scheduler, kwargs={'ch': ch, 'dataProvider': dataProvider,
                                                                                'Ago52W': Ago52W, 'end': end}))
    i += 1

# Start new Threads
stock_screening_threads.execute_threads()

print()
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("Aktien kaufen: ")
print()
if (stocksToBuy is not None):
    if (len(stocksToBuy) == 0):
        print("Keine gefunden")
    else:
        with open("C:\\Users\\Tom\\OneDrive\\Dokumente\\Thomas\\Aktien\\stockList.txt", "r") as ins:
            array = []
            for line in ins:
                array.append(line.replace('\n', ' ').replace('\r', ''))

            for stockToBuy in stocksToBuy:
                found = False
                #print(stockToBuy)

                # open a public URL, in this case, the webbrowser docs
                url_1 = "https://www.google.com/finance?q="
                url_2 = "&ei=Mby3WbnGGsjtsgHejoPwDA"
                url = url_1 + stockToBuy + url_2

                url_3 = "http://www.finanzen.at/suchergebnisse?_type=Aktien&_search="
                url2 = url_3 + stockToBuy

                for line in array:
                    if ',  ' + stockToBuy in line:
                        print (str(line) + ":                       " + url + "             " + url2)
                        found = True
                        break

                if not found:
                    print(str(stockToBuy) + ":                              " + url + "             " + url2)
                    #url_1 = "http://www.finanzen.at/suchergebnisse?_type=Aktien&_search="
                    #url = url_1 + stockToBuy
                    #webbrowser.open(url)
            # trace = go.Candlestick(x=df.index,
            #                        open=df.Open,
            #                        high=df.High,
            #                        low=df.Low,
            #                        close=df.Close)
            # data = [trace]
            #
            # plotly.offline.plot(data, filename='simple_candlestick')

print()
print("Runtime mit " + str(numOfStocksPerThread) + " Stocks pro Thread: " + str(
    datetime.now() - program_start_time))
