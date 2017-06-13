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
from str2 import isVolumeRaising, is52W_High, isVolumeHighEnough

##########################
volumeDayDelta = 5
end = datetime.datetime.now()
Ago52W = end - datetime.timedelta(weeks=52)
Ago5D = datetime.datetime.now() - timedelta(days=volumeDayDelta)
dataProvider = "google"
##########################
stocksToBuy = []
stocksToCheck = []
err = []
cnt = 1

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

#Nasdaq100_Symbols = ["COST"]

stocksToCheck.append(Nasdaq100_Symbols)


for stockName in stocksToCheck:
    volumeRaising = False
    volumeHighEnough = False
    stockHas52Hi = False

    try:
        if ((cnt % 5) == 0):
            print(str(cnt) + "/" + str(len(stocksToCheck)))

        stock52W = data.DataReader(stockName, dataProvider, Ago52W, end)
        stock5D = data.DataReader(stockName, dataProvider, Ago5D, end)
        df = stock52W
        #print (stock5D)
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
                stockHas52Hi = is52W_High (df)

        #print("volume raising: " + str(volumeRaising))
        #print("is 52W- High: " + str(stockHas52Hi))

        if (volumeHighEnough and stockHas52Hi and volumeRaising):
            stocksToBuy.append(stockName)


    except:
        e = sys.exc_info()[0]
        err.append("Stock: " + str(stockName) + " is faulty: " + str(e))

    cnt = cnt + 1

print ()
print ("######################")
print ("Errors:")
for er in err:
    print (er)

print ()
print ("Runtime: " + str(datetime.datetime.now() -end))
print ()
print ("Aktien kaufen: ")

for stockToBuy in stocksToBuy:
    print(stockToBuy)
    print (stock52W)

    if (len(stocksToBuy)<5):
        stock52W = data.DataReader(stockToBuy, dataProvider, Ago52W, end)
        df = stock52W
        trace = go.Candlestick(x=df.index,
                                open=df.Open,
                                high=df.High,
                                low=df.Low,
                                close=df.Close)
        data = [trace]
        plotly.offline.plot(data, filename='simple_candlestick')