import urllib3

http = urllib3.PoolManager()
from Utils import isVolumeRaising, is52W_High, isVolumeHighEnough, splitStockList, strat_52WHi_HiVolume, getSymbolFromName

symbol="stanley+black"

#query: http://d.yimg.com/autoc.finance.yahoo.com/autoc?query=Priceline&region=1&lang=en&callback=YAHOO.Finance.SymbolSuggest.ssCallback"
str1 = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query="
str2="&region=1&lang=en&callback=YAHOO.Finance.SymbolSuggest.ssCallback"
r = http.request('GET', str1 + symbol +str2)
#print (r.data)
#strRes = str(r.data)
#print (strRes.rsplit('{"symbol":"')[1].rsplit('"')[0])

##################
import xlrd
stocks = []
sh = xlrd.open_workbook('C:\\Users\\Tom\\OneDrive\\Dokumente\\Thomas\\Aktien\\52W-HochAutomatisch_Finanzen.xlsx').sheet_by_index(0)
for rownum in range(sh.nrows):
    try:
        if (rownum != 0):
            name = str(sh.cell(rownum, 0).value)
            symbol = getSymbolFromName(name)
            if (symbol != " "):
                stocks.append(symbol)
            #print(str(rownum)+ " = " + name + ", " + symbol)
    except Exception as e:
        print("name: " + str(name) + " is faulty: " + str(e))

for stockToBuy in stocks:
    print(stockToBuy)