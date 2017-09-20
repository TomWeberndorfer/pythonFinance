import logging
from pandas_datareader import data
import pandas_datareader.data as web
from Utils import isVolumeHighEnough, isVolumeRaising_2, is52W_High, write_stocks_to_buy_file, gapUp, \
    calculate_stopbuy_and_stoploss
from datetime import datetime, date, time
import pandas as pd

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
                #TODO zusätzlicher vergleich zu DAX / NASDAQ vergleich handelsplus (titel trotz schwachem dax stark)
                res = strat_52WHi_HiVolume(stockName, stock52W, 5, 3, 1.2, 0.98)
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

                    #TODO http://www.finanzen.at/analysen

            except Exception as e:
                # e = sys.exc_info()[0]
                print("strat_scheduler: Strategy Exception: " + str(stockName) + " is faulty: " + str(e))

                # if "Unable to read URL" in str(e):
                # return stocksToBuy # return because google stops transfer

    return stocksToBuy


def strat_52WHi_HiVolume(stockName, stock52W_data, check_days, min_cnt, min_vol_dev_fact, within52wHigh_fact):
    """
            Check 52 week High, raising volume, and high enough volume

            Args:
                stockName: name of the stock
                stock52W_data: stock data
                check_days: number of days to check
                min_cnt: min higher days within check days
                hiLimitMinFact: factor current data within 52 w high (ex: currVal > (Max * 0.98))

            Returns:
                True, if 52 week high

            Raises:
                NotImplementedError: if parameters are None
            """
    if stockName is None or stock52W_data is None or check_days is None or min_cnt is None or min_vol_dev_fact is None or within52wHigh_fact is None:
        raise NotImplementedError

    if min_vol_dev_fact < 1:
        raise AttributeError ("parameter min_vol_dev_fact must be higher than 1!")# should above other avg volume

    if within52wHigh_fact > 1:
        raise AttributeError ("parameter within52wHigh_fact must be lower than 1!")# should above other avg volume

    logging.debug(stockName)

    if not isVolumeHighEnough(stock52W_data):
        return ""

    if not isVolumeRaising_2(stock52W_data, check_days, min_cnt, min_vol_dev_fact):
        return ""

    if not is52W_High(stock52W_data, within52wHigh_fact):
        return ""

    result = calculate_stopbuy_and_stoploss (stock52W_data)
    write_stocks_to_buy_file(
        str(stockName) + ", " + str(result['sb']) + ", strat_52WHi_HiVolume")  # TODO überall einbauen in jede strat

    #TODO umbauen: gibt true bei kauf, stockname und sb, sl zurück
    return stockName


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