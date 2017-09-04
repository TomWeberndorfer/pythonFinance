# import pandas.io.data as web  # Package and modules for importing data; this code may change depending on pandas version
import logging
import datetime
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import timedelta
import urllib3


def isVolumeRaising(stock, stockName):
    i = 0
    volumeRaising = True
    dataLen = len(stock)

    vol_1 = stock.iloc[0].Volume
    vol_x1 = stock.iloc[1].Volume
    vol_x2 = stock.iloc[2].Volume
    vol_x3 = stock.iloc[3].Volume
    vol_2 = stock.iloc[dataLen - 1].Volume
    if (vol_1 < vol_2):
        volumeRaising = True
        while i < dataLen - 1:  # len because their are only 3 over the weekend
            vol_1 = stock.iloc[i].Volume
            #vol_2 = stock.iloc[dataLen - 1].Volume
            if vol_1 > vol_2:
                volumeRaising = False
                break
            else:
                i += 1
    else :
        volumeRaising = False

    if (volumeRaising):
        print (stockName)

    return volumeRaising

def isVolumeRaising_2(stock, stock10D, stockName):
    i = 0
    dataLen = len(stock)

    while i < dataLen - 1:  # len because their are only 3 over the weekend
        vol_1 = stock.iloc[i].Volume
        vol_2 = stock.iloc[i + 1].Volume
        if vol_1 > vol_2:
            return False
        else:
            i += 1

    #last vol must be higher than volume avg
    vol_avg = 0
    data_len10_d = len(stock10D)
    vol_last = stock10D.iloc[data_len10_d - 1].Volume
    vol_last_min1 = stock10D.iloc[data_len10_d - 2].Volume
    vol_last_min2 = stock10D.iloc[data_len10_d - 3].Volume
    i = 0

    while i < data_len10_d:  # add last entry too
        curr_vol = stock10D.iloc[i].Volume
        vol_avg += curr_vol
        i += 1

    vol_avg /= data_len10_d #calc avg

    #last 3 entries must have a larger volume as avg
    if (vol_last > vol_avg and vol_last_min1 > vol_avg and vol_last_min2 > vol_avg):
        return True

    return False

def is52W_High(stock):
    highest_high = stock['High'].max()
    hiPlus3Percent = highest_high * 1.03
    hiMinus2Percent = highest_high * 0.98
    dataLen = len(stock)
    curVal = stock.iloc[dataLen - 1].Close

    if curVal > hiMinus2Percent and curVal < hiPlus3Percent:
        return True
    else:
        return False


def isVolumeHighEnough(stock):
    minReqVol = 30000

    logging.debug("\n" + str(stock['Volume']))
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


def getSymbolFromName(name):
    try:
        origName = name

        #TODO regex replaced = re.sub('\W', ' ', name)

        name = name.replace(" ", "+")
        name = name.replace(".", "")
        name = name.split("Inc")[0]
        nameSpl = name.split("+")
        if (len(nameSpl) > 2):
            name = nameSpl[0] + "+" + nameSpl[1]

        symbol =""
        http = urllib3.PoolManager()
        # query: http://d.yimg.com/autoc.finance.yahoo.com/autoc?query=Priceline&region=1&lang=en&callback=YAHOO.Finance.SymbolSuggest.ssCallback"
        str1 = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query="
        str2 = "&region=1&lang=en&callback=YAHOO.Finance.SymbolSuggest.ssCallback"
        r = http.request('GET', str1 + name + str2)
        #print(r.data)
        strRes = str(r.data)
        #print(strRes.rsplit('{"symbol":"')[1].rsplit('"')[0])
        symbol = strRes.rsplit('{"symbol":"')[1].rsplit('"')[0]
        return symbol

    except Exception as e:
        print("ERROR symbol: " + symbol + ", Name: " + str(origName) + " ("+ name + ") is faulty: " + str(e))
        return " "


def get52W_H_Symbols_FromExcel ():
    import xlrd
    f = open('C:\\Users\\Tom\\OneDrive\\Dokumente\\Thomas\\Aktien\\stockList.txt', 'w')
    f.write("Name,   Symbol \n")  # python will convert \n to os.linesep
    stocks = []
    sh = xlrd.open_workbook(
        'C:\\Users\\Tom\\OneDrive\\Dokumente\\Thomas\\Aktien\\52W-HochAutomatisch_Finanzen.xlsx').sheet_by_index(0)

    thrStart = datetime.datetime.now()

    for rownum in range(sh.nrows):
        try:
            if (rownum != 0):
                name = str(sh.cell(rownum, 0).value)
                symbol = getSymbolFromName(name)
                if (symbol != " "):
                    stocks.append(symbol)
                    f.write(name + ",  " + symbol + "\n")  # python will convert \n to os.linesep
                    # print(str(rownum)+ " = " + name + ", " + symbol)
        except Exception as e:
            print("Method exception: get52W_H_Symbols_FromExcel: stock name: " + str(name) + " is faulty: " + str(e))

    f.close()  # you can omit in most cases as the destructor will call it
    print("Runtime get52W_H_Symbols_FromExcel: " + str(datetime.datetime.now() - thrStart))
    return stocks

def write_stocks_to_buy_file (txt):
    import datetime
    now = datetime.datetime.now()

    with open("C:\\Users\\Tom\\OneDrive\\Dokumente\\Thomas\\Aktien\\StocksToBuy.txt", "a") as myfile:
        #for stockToBuy in stocksToBuy:
            #myfile.write(str(stockToBuy) + ", " +  now.strftime("%Y-%m-%d %H:%M") + "\n")
            myfile.write(str(txt) + ", " +  str(now.strftime("%Y-%m-%d %H:%M")) + "\n")
            myfile.write("")


    myfile.close()

