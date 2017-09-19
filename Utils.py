# import pandas.io.data as web  # Package and modules for importing data; this code may change depending on pandas version
import logging
import datetime
import threading

import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import timedelta
import urllib3

stocks = []
names = []

def calc_avg_vol(stock, avg_days, dataLen):
    #t3: last vol must be higher than volume avg
    vol_avg = 0 #variable for avg
    i = 2 # 2 because last entry not included
    avgCnt = 0

    #calc average
    while i <= avg_days:  # add last entry too
        curr_vol = stock.iloc[dataLen- i].Volume
        vol_avg += curr_vol
        i += 1
        avgCnt += 1

    vol_avg /= avgCnt  # calc avg
    return vol_avg

def isVolumeRaising_withinCheckDays(stock, check_days=5, min_cnt=3, dataLen=300):
    # TODO falsch geht immer vom letzten aus, sollte aber der letzte höchstwert sein
    raise_cnt = 0
    i = check_days
    new_max = 0
    while i > 1:
        vol_1 = stock.iloc[dataLen - i].Volume
        if (vol_1 > new_max):
            new_max = vol_1
        vol_2 = stock.iloc[dataLen - i - 1].Volume
        if vol_1 > vol_2:
            raise_cnt += 1
        else:
            new_max = vol_2

        i -= 1

    if (raise_cnt < min_cnt):
        return False

    return True

#############################################
# avg_days: days to calculate the average
# check_days: days to the raise and the higher than volume
# min_cnt: minimum days raising last and higher than avg volume
def isVolumeRaising_2(stock, avg_days=15, check_days=5, min_cnt=3):
    i = check_days
    dataLen = len(stock)

    #data len smaller then avg days limit days
    if (dataLen < avg_days):
        avg_days = dataLen

    #t1: minimum raising cnt within check days
    if not isVolumeRaising_withinCheckDays(stock, check_days, min_cnt, dataLen):
        return False

    vol_avg = calc_avg_vol (stock, avg_days, dataLen)

    #t2: last volume higher than avg
    vol_last = stock.iloc[dataLen - 1].Volume
    if (vol_last < vol_avg):
        return False

    #t3: at least a few volume higher than avg
    cnt = check_days
    higher_than_avg = 0

    while cnt > 1:

        vol = stock.iloc[dataLen - cnt].Volume
        if (vol > vol_avg):
            higher_than_avg +=1

        cnt-=1

    if (higher_than_avg > min_cnt):
        return True

    return False

def is52W_High(stock, hiLimitMinFact=0.98):
    dataLen = len(stock)
    curVal = stock.iloc[dataLen - 1].High
    highest_high = stock['High'].max()

    if curVal == highest_high:
        return True

    else :
        hiMinusLimit = highest_high * hiLimitMinFact
        if curVal > hiMinusLimit:
            return True
        else:
            return False


def gapUp(stock, minGapMultiplier):
    dataLen = len(stock)
    yesterday_val = stock.iloc[dataLen - 2].Close
    curVal = stock.iloc[dataLen - 1].Open
    gapUpVal = (yesterday_val * minGapMultiplier)
    #TODO: überprüfen ob tage hintereinander, achtung wochenende
    if (curVal > gapUpVal):
        return True
    else:
        return False

# def hammer(stock, hammerLengthInFactor, HeadBiggerThanHandleFactor):
#     dataLen = len(stock)
#     yesterday_val = stock.iloc[dataLen - 2].Close
#     curVal = stock.iloc[dataLen - 1].Open
#     #gapUpVal = (yesterday_val * minGapMultiplier)
#     #TODO: überprüfen ob tage hintereinander, achtung wochenende
#     if (curVal > gapUpVal):
#         return True
#     else:
#         return False


def isVolumeHighEnough(stock, avg_days=10):
    minReqVol = 30000
    vol_avg = 0
    dataLen = len(stock)
    i = 1
    avgCnt = 0

    while i <= avg_days:  # add last entry too
        curr_vol = stock.iloc[dataLen - i].Volume
        vol_avg += curr_vol
        i += 1
        avgCnt += 1

    vol_avg /= avgCnt  # calc avg

    if (vol_avg > minReqVol):
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


def getSymbolFromName(name):
    try:
        origName = name

        # TODO regex replaced = re.sub('\W', ' ', name)

        name = name.replace(" ", "+")
        name = name.replace(".", "")
        name = name.split("Inc")[0]
        nameSpl = name.split("+")
        if (len(nameSpl) > 2):
            name = nameSpl[0] + "+" + nameSpl[1]

        symbol = ""
        http = urllib3.PoolManager()
        # query: http://d.yimg.com/autoc.finance.yahoo.com/autoc?query=Priceline&region=1&lang=en&callback=YAHOO.Finance.SymbolSuggest.ssCallback"
        str1 = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query="
        str2 = "&region=1&lang=en&callback=YAHOO.Finance.SymbolSuggest.ssCallback"
        r = http.request('GET', str1 + name + str2)
        # print(r.data)
        strRes = str(r.data)
        # print(strRes.rsplit('{"symbol":"')[1].rsplit('"')[0])
        symbol = strRes.rsplit('{"symbol":"')[1].rsplit('"')[0]
        return symbol

    except Exception as e:
        print("getSymbolFromName: ERROR symbol: " + symbol + ", Name: " + str(
            origName) + " (" + name + ") is faulty: " + str(e))
        return " "


def symbol_thread(name):
    symbol = getSymbolFromName(name)
    if (symbol != " "):
        stocks.append(symbol)
        names.append(name)


def get52W_H_Symbols_FromExcel():
    import xlrd
    f = open('C:\\Users\\Tom\\OneDrive\\Dokumente\\Thomas\\Aktien\\stockList.txt', 'w')
    f.write("Name,   Symbol \n")  # python will convert \n to os.linesep

    sh = xlrd.open_workbook(
        'C:\\Users\\Tom\\OneDrive\\Dokumente\\Thomas\\Aktien\\52W-HochAutomatisch_Finanzen.xlsx').sheet_by_index(0)

    from MyThread import MyThread
    get_symbol_threads = MyThread("get_symbol_threads")

    for rownum in range(sh.nrows):
        try:
            if (rownum != 0):
                name = str(sh.cell(rownum, 0).value)
                get_symbol_threads.append_thread(threading.Thread(target=symbol_thread, kwargs={'name': name}))
                #symbol = getSymbolFromName(name)
                #if (symbol != " "):
                 #   stocks.append(symbol)

                    # print(str(rownum)+ " = " + name + ", " + symbol)
        except Exception as e:
            print("Method exception: get52W_H_Symbols_FromExcel: stock name: " + str(name) + " is faulty: " + str(e))

    get_symbol_threads.execute_threads()

    cnt = 0
    while (cnt < len(names)):
        for symbol in stocks:
            f.write(names[cnt] + ",  " + symbol + "\n")  # python will convert \n to os.linesep
            cnt+=1

    f.close()  # you can omit in most cases as the destructor will call it
    return stocks


def write_stocks_to_buy_file(txt):
    import datetime
    now = datetime.datetime.now()

    with open("C:\\Users\\Tom\\OneDrive\\Dokumente\\Thomas\\Aktien\\StocksToBuy.txt", "a") as myfile:
        # for stockToBuy in stocksToBuy:
        # myfile.write(str(stockToBuy) + ", " +  now.strftime("%Y-%m-%d %H:%M") + "\n")
        myfile.write(str(txt) + ", " + str(now.strftime("%Y-%m-%d %H:%M")) + "\n")
        myfile.write("")

    myfile.close()
