import logging
from pandas_datareader import data
from Utils import isVolumeHighEnough, isVolumeRaising_2, is52W_High, write_stocks_to_buy_file

##################################
# 52 weeks high
# high volume
# volume raising the last 3 days
# volume today must be higher then AVG last days
##################################
def strat_scheduler(stocksToCheck, dataProvider, Ago52W, Ago5D, Ago10D, end):
    stocksToBuy = []

    for stockName in stocksToCheck:

        try:
            #read data
            stock52W = data.DataReader(stockName, dataProvider, Ago52W, end)
            stock5D = data.DataReader(stockName, dataProvider, Ago5D, end)
            stock10D = data.DataReader(stockName, dataProvider, Ago10D, end)

            ##############################################################
            # insert STRATEGIES here
            res = strat_52WHi_HiVolume(stockName, stock52W, stock5D, stock10D)
            if (res != ""):
                stocksToBuy.append(res)
            ###########################################################################

        except Exception as e:
            # e = sys.exc_info()[0]
            print("Stock: " + str(stockName) + " is faulty: " + str(e))

            #if "Unable to read URL" in str(e):
               #return stocksToBuy # return because google stops transfer

    return stocksToBuy

def strat_52WHi_HiVolume (stockName, stock52W, stock5D, stock10D):

    volumeRaising = False
    volumeHighEnough = False
    stockHas52Hi = False

    df = stock52W
    logging.debug(stockName)
    logging.debug(stock5D)

    volumeHighEnough = isVolumeHighEnough(stock5D)
    if (volumeHighEnough):
        # TODO volumeRaising = isVolumeRaising(stock5D, stockName)
        volumeRaising = isVolumeRaising_2(stock5D, stock10D, stockName)

        if (volumeRaising):
            stockHas52Hi = is52W_High(df)

    if (volumeHighEnough and stockHas52Hi and volumeRaising):

        dataLen = len(stock5D)
        endKurs = stock5D.iloc[dataLen - 1].Close
        write_stocks_to_buy_file(str(stockName) + ", " + str(endKurs))  # TODO überall einbauen in jede strat
        return stockName

    #else case
    return ""