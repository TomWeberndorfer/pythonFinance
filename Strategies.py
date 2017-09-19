import logging
from pandas_datareader import data
import pandas_datareader.data as web
from Utils import isVolumeHighEnough, isVolumeRaising_2, is52W_High, write_stocks_to_buy_file, gapUp
from datetime import datetime, date, time
import pandas as pd

##################################
# 52 weeks high
# high volume
# volume raising the last 3 days
# volume today must be higher then AVG last days
##################################
def replaceWrongStockMarket(stockName):
    replacePatternn = [".MU", ".DE", ".SW", ".F", ".EX", ".TI", ".MI"]

    for pattern in replacePatternn:
        if pattern in stockName:
            stockName = stockName.replace(pattern, "")
            stockName = "ETR:" + stockName
            break

    return stockName


def strat_scheduler(stocksToCheck, dataProvider, Ago52W, end):
    stocksToBuy = []

    for stockName in stocksToCheck:
        readException = False

        try:
            # read data
            newStockName = replaceWrongStockMarket(stockName)
            stockName = newStockName
            stock52W = data.DataReader(stockName, dataProvider, Ago52W.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))

        except Exception as e:
            # e = sys.exc_info()[0]
            print("strat_scheduler: Data Read exception: " + str(stockName) + " is faulty: " + str(e))
            readException = True

        if not readException and len(stock52W) > 0:
            ##############################################################
            # insert STRATEGIES here
            try:
                res = strat_52WHi_HiVolume(stockName, stock52W)
                if res != "":
                    stocksToBuy.append(res)
                    #print ("buy strat_52WHi_HiVolume: " + res)

                    # TODO canslim / Henkel

                    # TODO auswertung von chartsignalen mittels finanzen.at
                    # http://www.finanzen.net/chartsignale/index/Alle/liste/jc-1234er-long
                    ############################################################################

                # else:
                #     res = strat_GapUp_HiVolume(stockName, stock52W)
                #     if res != "":
                #         stocksToBuy.append(res)
                #         print ("buy strat_GapUp_HiVolume: " + res)
                    #TODO candlestick hammer
               # res = strat_candlestick_hammer_HiVol (stockName, stock52W)

                    #TODO negativer hammer in den letzten 10 tagen als zeichen für nicht kaufen
                    #TODO zusätzliche reihung nach:
                        # - volumen anstieg stärke

            except Exception as e:
                # e = sys.exc_info()[0]
                print("strat_scheduler: Strategy Exception: " + str(stockName) + " is faulty: " + str(e))

                # if "Unable to read URL" in str(e):
                # return stocksToBuy # return because google stops transfer

    return stocksToBuy


def strat_52WHi_HiVolume(stockName, stock52W_data):

    volumeRaising = False
    volumeHighEnough = False
    stockHas52Hi = False

    logging.debug(stockName)
    volumeHighEnough = isVolumeHighEnough(stock52W_data)
    if volumeHighEnough:
        volumeRaising = isVolumeRaising_2(stock52W_data, 5, 3)

        if volumeRaising:
            stockHas52Hi = is52W_High(stock52W_data, 0.98)

    if volumeHighEnough and stockHas52Hi and volumeRaising:
        dataLen = len(stock52W_data)
        endKurs = stock52W_data.iloc[dataLen - 1].Close
        write_stocks_to_buy_file(
            str(stockName) + ", " + str(endKurs) + ", strat_52WHi_HiVolume")  # TODO überall einbauen in jede strat
        return stockName

    # else case
    return ""

def strat_GapUp_HiVolume (stockName, stock52W):
    volumeHighEnough = False

    logging.debug(stockName)

    volumeHighEnough = isVolumeHighEnough(stock52W)
    if volumeHighEnough:
            isGapUp = gapUp(stock52W, 1.03)

    if volumeHighEnough and isGapUp:
        dataLen = len(stock52W)
        endKurs = stock52W.iloc[dataLen - 1].Close
        write_stocks_to_buy_file(
            str(stockName) + ", " + str(endKurs) + ", strat_GapUp_HiVolume")  # TODO überall einbauen in jede strat
        return stockName

    # else case
    return ""

# def strat_candlestick_hammer_HiVol (stockName, stock52W):
#     volumeHighEnough = False
#
#     logging.debug(stockName)
#
#     volumeHighEnough = isVolumeHighEnough(stock52W)
#     if volumeHighEnough:
#         isHammer = hammer(stock52W, 1.02, 3)
#
#     if volumeHighEnough and isHammer:
#         dataLen = len(stock52W)
#         endKurs = stock52W.iloc[dataLen - 1].Close
#         write_stocks_to_buy_file(
#             str(stockName) + ", " + str(endKurs) + ", strat_GapUp_HiVolume")  # TODO überall einbauen in jede strat
#         return stockName
#
#     # else case
#     return ""