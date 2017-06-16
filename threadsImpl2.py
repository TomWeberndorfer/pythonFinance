import pandas as pd
from pandas_datareader import data, wb
#import pandas.io.data as web  # Package and modules for importing data; this code may change depending on pandas version
import datetime
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import timedelta
import sys
import threading
from str2 import isVolumeRaising, is52W_High, isVolumeHighEnough, splitStockList, strat_52WHi_HiVolume
import threading
import time

exitFlag = 0
threads = []
stocksToBuy = []
err = []

##########################
# config
numOfStocksPerThread = 5
volumeDayDelta = 5
end = datetime.datetime.now()
Ago52W = end - datetime.timedelta(weeks=52)
Ago5D = datetime.datetime.now() - timedelta(days=volumeDayDelta)
dataProvider = "google"
##########################

#sybols to read

Nasdaq100_Symbols = ["AAPL", "ADBE", "ADI", "ADP", "ADSK", "AKAM", "ALXN",
                         "AMAT", "AMGN", "AMZN", "ATVI", "AVGO", "BBBY", "BIDU", "BIIB",
                         "BRCM", "CA", "CELG", "CERN", "CHKP", "CHRW", "CHTR", "CMCSA",
                         "COST", "CSCO", "CTRX", "CTSH", "CTXS", "DISCA", "DISCK", "DISH",
                         "DLTR", "DTV", "EBAY", "EQIX", "ESRX", "EXPD", "EXPE", "FAST",
                         "FB", "FFIV", "FISV", "FOXA", "GILD", "GMCR", "GOOG", "GOOGL",
                         "GRMN", "HSIC", "ILMN", "INTC", "INTU", "ISRG", "KLAC", "KRFT",
                         "LBTYA", "LLTC", "LMCA", "LMCK", "LVNTA", "MAR", "MAT", "MDLZ",
                         "MNST", "MSFT", "MU", "MXIM", "MYL", "NFLX", "NTAP", "NVDA",
                         "NXPI", "ORLY", "PAYX", "PCAR", "PCLN", "QCOM", "QVCA", "REGN",
                         "ROST", "SBAC", "SBUX", "SIAL", "SIRI", "SNDK", "SPLS", "SRCL",
                         "STX", "SYMC", "TRIP", "TSCO", "TSLA", "TXN", "VIAB", "VIP",
                         "VOD", "VRSK", "VRTX", "WDC", "WFM", "WYNN", "XLNX", "YHOO"]

DAX30_Symbols = ["ETR:ADS", "ETR:ALV", "ETR:BAS", "ETR:BAY", "ETR:BMW", "ETR:CBK", "ETR:CON", "ETR:DAI",
                 "DB1", "ETR:DBK", "ETR:DPB", "ETR:DPW", "ETR:DTE", "ETR:EOA", "ETR:FME", "ETR:HEN3",
                 "HRX", "ETR:IFX", "ETR:LHA", "ETR:LIN", "ETR:MAN", "ETR:MEO", "ETR:MRK.DE", "ETR:MUV2",
                 "RWE", "ETR:SAP", "ETR:SIE", "ETR:TKA", "ETR:TUI1", "ETR:VOW"]

DAX30_Symbols = ["ETR:DAI", "ETR:ADS", "ETR:ALV"]

allSymbols = []

#allSymbols.extend(Nasdaq100_Symbols)
allSymbols.extend(DAX30_Symbols)


##########################################################

class myThread (threading.Thread):
    def __init__(self, stocksToCheck, name):
        threading.Thread.__init__(self)
        self.stocksToCheck = stocksToCheck
        self.name = name

    def run(self):
        print ("Starting " + self.name)
        stocksToBuy = strat_52WHi_HiVolume (self.stocksToCheck, dataProvider, Ago52W, Ago5D, end)
        #print ("Exiting " + self.name)


#####################

# Create new threads
splits= splitStockList(allSymbols, numOfStocksPerThread)
#thread1 = myThread(splits, "Thread-1: Nasdaq100_Symbols_1")

i = 0
thrToExe= []
while i < len(splits):
    ch = splits[i]
    thrToExe.append(myThread(ch, "Thread-" + str(i)))
    i += 1

# Start new Threads
thrStart= datetime.datetime.now()

for tr in thrToExe:
    tr.start()
    threads.append(tr)

# Wait for all threads to complete
for t in threads:
    t.join()

print()
print("++++++++++++++++++++")
print("Aktien kaufen: ")
if (len(stocksToBuy) == 0):
    print ("Keine gefunden")
else:
    for stockToBuy in stocksToBuy:
        print(stockToBuy)
        # trace = go.Candlestick(x=df.index,
        #                        open=df.Open,
        #                        high=df.High,
        #                        low=df.Low,
        #                        close=df.Close)
        # data = [trace]
        #
        # plotly.offline.plot(data, filename='simple_candlestick')

print()
print("Runtime mit " + str(numOfStocksPerThread) + " Stocks pro Thread: " + str(datetime.datetime.now() - thrStart))