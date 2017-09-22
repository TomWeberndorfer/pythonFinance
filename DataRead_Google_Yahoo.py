import sys
import threading
import traceback

import urllib3
from pandas import DataFrame
from pandas_datareader import data
from yahoo_finance import Share
import googlefinance.client as google_client

from Utils import get_current_function_name

str1 = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query="
str2 = "&region=1&lang=en&callback=YAHOO.Finance.SymbolSuggest.ssCallback"

stocks = []
names = []


def read_data_from_google_with_client(stock_name, interval="86400", period="1M"):
    param = {
        'q': stock_name,  # Stock symbol (ex: "AAPL")
        'i': interval,  # Interval size in seconds ("86400" = 1 day intervals)
        # 'x': "INDEXDJX", # Stock exchange symbol on which stock is traded (ex: "NASD")
        'p': period  # Period (Ex: "1Y" = 1 year)
    }
    # get price data (return pandas dataframe)
    df = google_client.get_price_data(param)
    return df


def read_data_from_google_with_pandas(stock_name, start_time, end_time):
    """
    read data from google server
    :param stock_name: stock name
    :param start_time: start date and time
    :param end_time: end date and time
    :return: stock data
    """

    try:
        stock52_w = data.DataReader(stock_name, "google", start_time.strftime("%Y-%m-%d"),
                                    end_time.strftime("%Y-%m-%d"))

    except:
        # Try with another stock market ETR
        stock52_w = data.DataReader("ETR:" + stock_name, "google", start_time.strftime("%Y-%m-%d"),
                                    end_time.strftime("%Y-%m-%d"))

    #TODO data of today contains less volume because not finished
    # if len(stock52_w) > 0:
    #     try:
    #         stock52_w = stock52_w.append(read_current_day_from_yahoo(stock_name))
    #     except Exception as e:
    #         sys.stderr.write("Can not get stock data of stock " + stock_name + " from yahoo\n")

    # else:
    if len(stock52_w) == 0:
        sys.stderr.write("Stock: " + stock_name + " does not exist on!\n")

    return stock52_w


def read_data_from_yahoo(stock_name, start_date, end_date):
    #  see also:
    #  https: // github.com / lukaszbanasiak / yahoo - finance
    #  https://pypi.python.org/pypi/yahoo-finance

    #yahoo = Share('APPL')
    #print(yahoo.get_avg_daily_volume())
    #print(yahoo.get_open())
    # print (yahoo.get_historical('2014-04-25', '2014-04-29'))


    from pandas_datareader import data as pdr
    import fix_yahoo_finance as yf
    yf.pdr_override()  # <== that's all it takes :-)
    data = pdr.get_data_yahoo(stock_name, start= start_date, end= end_date)

    return data


def read_current_day_from_yahoo(stock_name):
    #  TODO google does not provide data from today, workarround: add yahoo data manually:
    #  maybe try this: https://pypi.python.org/pypi/googlefinance.client
    stock_name = optimize_name_for_yahoo(stock_name)
    cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    lst = []
    stock_markets_to_try = ["", ".DE"]
    for stock_market in stock_markets_to_try:

        try:
            yahoo = Share(stock_name + stock_market)
            currDate = (yahoo.get_trade_datetime())[0:10]
            lst.append([currDate, float(yahoo.get_price()), float(yahoo.get_days_high()), float(yahoo.get_days_low()),
                        float(yahoo.get_price()),
                        float(yahoo.get_volume())])
            break

        except:
            # nothing to do
            no = []


    df1 = DataFrame(lst, columns=cols)
    df1.index.name = 'Date'
    # df1.set_index([str(currDate)])
    df1 = df1.set_index(['Date'])
    return df1

    # stock52_w.loc[len(stock52_w)]=[yahoo.get_price(),yahoo.get_days_high(),yahoo.get_days_low(),yahoo.get_price(),yahoo.get_volume()]
    # stock52_w.iloc[len(stock52_w) - 1].name = datetime.utcnow()
    # print("name: " + str(stock52_w.index.name))

    return []


def get_symbol_from_name_from_yahoo(name):
    try:

        name = optimize_name_for_yahoo(name)
        http = urllib3.PoolManager()
        # query: http://d.yimg.com/autoc.finance.yahoo.com/autoc?query=Priceline&region=1&lang=en&callback=YAHOO.Finance.SymbolSuggest.ssCallback"

        try:
            r = http.request('GET', str1 + name + str2)  # build url
        except Exception as e:
            return " "

        str_res = str(r.data)
        if len(str_res) > 0:
            symbol = str_res.rsplit('{"symbol":"')[1].rsplit('"')[0]
            symbol = symbol.rsplit('.')[0]  # cut the stock exchange market from yahoo
            return symbol
        else:
            return " "  # no symbol found

    except Exception as e:
        return " "  # no symbol found


def get52_w__h__symbols__from_excel(filepath):
    import xlrd
    f = open(filepath + 'stockList.txt', 'w')
    f.write("Name,   Symbol \n")  # python will convert \n to os.linesep

    sh = xlrd.open_workbook(filepath + '52W-HochAutomatisch_Finanzen.xlsx').sheet_by_index(0)

    from MyThread import MyThread
    get_symbol_threads = MyThread("get_symbol_threads")

    for rownum in range(sh.nrows):
        try:
            if rownum != 0:
                name = str(sh.cell(rownum, 0).value)
                date_from_file = str(sh.cell(rownum, 1).value)

                # values from today contain a time (=Uhr) and not a date
                # TODO google data is from yesterday
                if not "Uhr" in date_from_file:  # but google data is from yesterday
                    get_symbol_threads.append_thread(threading.Thread(target=symbol_thread, kwargs={'name': name}))

        except Exception as e:
            sys.stderr.write("Method exception in: " + get_current_function_name()
                             + ": stock name: " + str(name) + " is faulty: " + str(e) + "\n")
            traceback.print_exc()

    get_symbol_threads.execute_threads()

    cnt = 0
    while (cnt < len(names)):
        for symbol in stocks:
            f.write(names[cnt] + ",  " + symbol + "\n")  # python will convert \n to os.linesep
            cnt += 1

    f.close()  # you can omit in most cases as the destructor will call it
    return stocks


def optimize_name_for_yahoo(name):
    # TODO regex replaced = re.sub('\W', ' ', name)
    name = name.lower()
    name = name.replace(" ", "+")
    name = name.replace(".", "")
    name = name.replace("ü", "ue")
    name = name.replace("ö", "oe")
    name = name.replace("ä", "ae")
    name = name.replace("etr:", "")
    name = name.replace("fra:", "")
    name = name.split("inc")[0]
    name = name.replace("^", "")
    nameSpl = name.split("+")
    if len(nameSpl) > 2:
        name = nameSpl[0] + "+" + nameSpl[1]
    return name


def symbol_thread(name):
    symbol = get_symbol_from_name_from_yahoo(name)
    if symbol != " ":
        stocks.append(symbol)
        names.append(name)
