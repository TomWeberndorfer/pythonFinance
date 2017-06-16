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
import time

def isVolumeRaising (stock):
    i = 0
    volumeRaising = True
    dataLen = len(stock)
    while i < dataLen -1:  # len because their are only 3 over the weekend
        if stock.iloc[i].Volume > stock.iloc[i + 1].Volume:
            volumeRaising = False
            break
        else:
            i += 1

    return volumeRaising

def is52W_High (stock):

    highest_high = stock['High'].max()
    hiPlus3Percent = highest_high * 1.03
    hiMinus2Percent = highest_high * 0.98
    dataLen = len(stock)
    curVal = stock.iloc[dataLen-1].Close

    if curVal > hiMinus2Percent and curVal < hiPlus3Percent:
        return True
    else:
        return False


def isVolumeHighEnough(stock):
    minReqVol = 30000
    curMinVol = stock['Volume'].min()

    if (curMinVol > minReqVol):
        return True
    else:
        return False

def splitStockList(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs

def strat_52WHi_HiVolume(stocksToCheck, dataProvider, Ago52W, Ago5D, end):
    stocksToBuy = []
    cnt = 1

    for stockName in stocksToCheck:
        volumeRaising = False
        volumeHighEnough = False
        stockHas52Hi = False

        try:
            # if ((cnt % 5) == 0):
            #   print(self.name + ":" + str(cnt) + "/" + str(len(stocksToCheck)))

            stock52W = data.DataReader(stockName, dataProvider, Ago52W, end)
            stock5D = data.DataReader(stockName, dataProvider, Ago5D, end)
            df = stock52W
            #print (stock5D)

            if (isVolumeHighEnough(df)):
                volumeRaising = isVolumeRaising(stock5D)
                if (volumeRaising):
                    stockHas52Hi = is52W_High(df)

            if (volumeHighEnough and stockHas52Hi and volumeRaising):
                stocksToBuy.append(stockName)


        except:
            e = sys.exc_info()[0]
            print("Stock: " + str(stockName) + " is faulty: " + str(e))

        cnt = cnt + 1

    return stocksToBuy