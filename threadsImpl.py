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
from Utils import isVolumeRaising, is52W_High, isVolumeHighEnough
import threading
import time

exitFlag = 0
threads = []

class myThread (threading.Thread):
    def __init__(self, stocksToCheck, name):
        threading.Thread.__init__(self)
        self.stocksToCheck = stocksToCheck
        self.name = name

    def run(self):
        print ("Starting " + self.name)
        ##########################
        volumeDayDelta = 5
        end = datetime.datetime.now()
        Ago52W = end - datetime.timedelta(weeks=52)
        Ago5D = datetime.datetime.now() - timedelta(days=volumeDayDelta)
        dataProvider = "google"
        ##########################
        stocksToBuy = []
        stocksToCheck = []
        stocksToCheck = self.stocksToCheck
        err = []
        cnt = 1

        for stockName in stocksToCheck:
            volumeRaising = False
            volumeHighEnough = False
            stockHas52Hi = False

            try:
                if ((cnt % 10) == 0):
                    print(self.name + ":" + str(cnt) + "/" + str(len(stocksToCheck)))

                stock52W = data.DataReader(stockName, dataProvider, Ago52W, end)
                stock5D = data.DataReader(stockName, dataProvider, Ago5D, end)
                df = stock52W
                # print (stock5D)
                # trace = go.Candlestick(x=df.index,
                #                        open=df.Open,
                #                        high=df.High,
                #                        low=df.Low,
                #                        close=df.Close)
                # data = [trace]
                #
                # plotly.offline.plot(data, filename='simple_candlestick')


                if (isVolumeHighEnough(df)):
                    volumeRaising = isVolumeRaising(stock5D)
                    if (volumeRaising):
                        stockHas52Hi = is52W_High(df)

                # print("volume raising: " + str(volumeRaising))
                # print("is 52W- High: " + str(stockHas52Hi))

                if (volumeHighEnough and stockHas52Hi and volumeRaising):
                    stocksToBuy.append(stockName)


            except:
                e = sys.exc_info()[0]
                err.append("Stock: " + str(stockName) + " is faulty: " + str(e))

            cnt = cnt + 1

        print()
        print("######################")
        print("Errors:")
        for er in err:
            print(er)

        print()
        print("Aktien kaufen: ")

        for stockToBuy in stocksToBuy:
            print(stockToBuy)
            print(stock52W)

        #print ("Exiting " + self.name)

#####################
Nasdaq100_Symbols_1 = ["AAPL", "ADBE", "ADI", "ADP", "ADSK", "AKAM", "ALXN",
                         "AMAT", "AMGN", "AMZN", "ATVI", "AVGO", "BBBY", "BIDU", "BIIB",
                         "BRCM", "CA", "CELG", "CERN", "CHKP", "CHRW", "CHTR", "CMCSA",
                         "COST", "CSCO", "CTRX", "CTSH", "CTXS", "DISCA", "DISCK", "DISH",
                         "DLTR", "DTV", "EBAY", "EQIX", "ESRX", "EXPD", "EXPE", "FAST",
                         "FB", "FFIV", "FISV", "FOXA", "GILD", "GMCR", "GOOG", "GOOGL",
                         "GRMN", "HSIC", "ILMN", "INTC", "INTU", "ISRG", "KLAC", "KRFT"]

Nasdaq100_Symbols_2 = ["LBTYA", "LLTC", "LMCA", "LMCK", "LVNTA", "MAR", "MAT", "MDLZ",
                         "MNST", "MSFT", "MU", "MXIM", "MYL", "NFLX", "NTAP", "NVDA",
                         "NXPI", "ORLY", "PAYX", "PCAR", "PCLN", "QCOM", "QVCA", "REGN",
                         "ROST", "SBAC", "SBUX", "SIAL", "SIRI", "SNDK", "SPLS", "SRCL",
                         "STX", "SYMC", "TRIP", "TSCO", "TSLA", "TXN", "VIAB", "VIP",
                         "VOD", "VRSK", "VRTX", "WDC", "WFM", "WYNN", "XLNX", "YHOO"]

# Create new threads
thread1 = myThread(Nasdaq100_Symbols_1, "Thread-1: Nasdaq100_Symbols_1")
thread2 = myThread(Nasdaq100_Symbols_2, "Thread-2: Nasdaq100_Symbols_2")

# Start new Threads
thrStart= datetime.datetime.now()
thread1.start()
thread2.start()

# Add threads to thread list
threads.append(thread1)
threads.append(thread2)

# Wait for all threads to complete
for t in threads:
    t.join()
print ("Exiting Main Thread")
print()
print("Runtime: " + str(datetime.datetime.now() - thrStart))