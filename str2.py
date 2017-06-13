
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


