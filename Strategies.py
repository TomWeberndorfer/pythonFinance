import logging
from pandas_datareader import data
from Utils import isVolumeHighEnough, isVolumeRaising_2, is52W_High, write_stocks_to_buy_file

##################################
# 52 weeks high
# high volume
# volume raising the last 3 days
# volume today must be higher then AVG last days
##################################
def strat_52WHi_HiVolume(stocksToCheck, dataProvider, Ago52W, Ago5D, Ago10D, end):
    stocksToBuy = []

    for stockName in stocksToCheck:

        try:

            volumeRaising = False
            volumeHighEnough = False
            stockHas52Hi = False
            # if ((cnt % 5) == 0):
            #   logging.debug(self.name + ":" + str(cnt) + "/" + str(len(stocksToCheck)))

            stock52W = data.DataReader(stockName, dataProvider, Ago52W, end)
            stock5D = data.DataReader(stockName, dataProvider, Ago5D, end)
            stock10D = data.DataReader(stockName, dataProvider, Ago10D, end)

            df = stock52W
            logging.debug(stockName)
            logging.debug(stock5D)

            volumeHighEnough = isVolumeHighEnough(stock5D)
            if (volumeHighEnough):
                #TODO volumeRaising = isVolumeRaising(stock5D, stockName)
                volumeRaising = isVolumeRaising_2(stock5D, stock10D, stockName)

                if (volumeRaising):
                    stockHas52Hi = is52W_High(df)

            if (volumeHighEnough and stockHas52Hi and volumeRaising):
                stocksToBuy.append(stockName)
                dataLen = len(stock5D)
                endKurs = stock5D.iloc[dataLen - 1].Close
                write_stocks_to_buy_file(str(stockName) + ", " +  str(endKurs)) #TODO überall einbauen in jede strat

        except Exception as e:
            # e = sys.exc_info()[0]
            print("Stock: " + str(stockName) + " is faulty: " + str(e))

            #if "Unable to read URL" in str(e):
               #return stocksToBuy # return because google stops transfer

    return stocksToBuy