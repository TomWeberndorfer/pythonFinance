# import pandas.io.data as web  # Package and modules for importing data; this code may change depending on pandas version
import logging
import datetime
import threading
import sys

import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import timedelta
import urllib3

stocks = []
names = []
filepath = 'C:\\Users\\Tom\\OneDrive\\Dokumente\\Thomas\\Aktien\\'


def calc_avg_vol(stock, days_skip_from_end):
    """
    Calculates the average volume of stock data except the days to skip from end.
    :param stock: stock data
    :param days_skip_from_end:  days to skip from end
    :return: Average Value
    """

    if stock is None or days_skip_from_end is None:
        raise NotImplementedError

    # t3: last vol must be higher than volume avg
    vol_avg = 0  # variable for avg
    dataLen = len(stock) - days_skip_from_end  # 2 because last entry not included
    avgCnt = 0

    # calc average
    while avgCnt < dataLen:  # add last entry too
        curr_vol = stock.iloc[avgCnt].Volume
        vol_avg += curr_vol
        avgCnt += 1

    vol_avg /= avgCnt  # calc avg
    return vol_avg


def is_volume_raising_within_check_days(stock, check_days, min_cnt):
    """
    Checks, if the volume is rising within the check days, with at least minimum value.

    Args:
        stock: stock data
        check_days: number of days to check
        min_cnt: min raising days within check days

    Returns:
        True, if volume is raising

    Raises:
        NotImplementedError: if parameters are None
    """
    if stock is None or check_days is None or min_cnt is None:
        raise NotImplementedError

    dataLen = len(stock)
    raise_cnt = 0
    i = check_days
    saveVal = False
    while i > 0:
        vol_1 = stock.iloc[dataLen - i].Volume
        if not saveVal:
            vol_2 = stock.iloc[dataLen - i - 1].Volume
        if vol_1 > vol_2:
            raise_cnt += 1
            saveVal = False
        else:
            saveVal = True

        i -= 1

    if (raise_cnt < min_cnt):
        return False

    return True


def is_last_volume_higher_than_avg(data, check_days, vol_avg, significance_factor):
    """
    Calculates the average and checks,
    if the last volume is higher than avg.

    Args:
        data: stock data
        check_days: number of days to check
        vol_avg: average volume
        significance_factor:  is a factor to show that the cur vol is significantly higher


    Returns:
        True, if last volume higher than avg

    Raises:
        NotImplementedError: if parameters are None
    """
    if data is None or check_days is None or vol_avg is None or significance_factor is None:
        raise NotImplementedError
    dataLen = len(data)
    vol_last = data.iloc[dataLen - 1].Volume
    if (vol_last < (vol_avg * significance_factor)):
        return False
    else:
        return True


def is_a_few_higher_than_avg(stock, check_days, min_cnt, volume_average):
    """
    Calculates the average and checks,
    if the a few volume values are higher than avg.

    Args:
        stock: stock data
        check_days: number of days to check
        min_cnt: min higher days within check days
        volume_average: average volume

    Returns:
        True, if last volume higher than avg

    Raises:
        NotImplementedError: if parameters are None

    """
    if stock is None or check_days is None or min_cnt is None:
        raise NotImplementedError

    # from [0] to end, without days to check above avg  ~ [datalen-15]
    cnt = check_days
    higher_than_avg = 0
    dataLen = len(stock)

    while cnt > 1:

        vol = stock.iloc[dataLen - cnt].Volume
        if (vol > volume_average):
            higher_than_avg += 1

        cnt -= 1

    if (higher_than_avg >= min_cnt):
        return True

    return False


def is_volume_raising(data, check_days, min_cnt, min_vol_dev_fact):
    """
        Uses functions, to check if stock is raising

        Args:
            data: stock data
            check_days: number of days to check
            min_cnt: min higher days within check days
            min_vol_dev_fact: factor current data within 52 w high (ex: currVal > (Max * 0.98))

        Returns:
            True, if raising

        Raises:
            NotImplementedError: if parameters are None
    """
    if data is None or check_days is None or min_cnt is None or min_vol_dev_fact is None:
        raise NotImplementedError

    if min_vol_dev_fact < 1:
        raise AttributeError("parameter min_vol_dev_fact must be higher than 1!")

    vol_avg = calc_avg_vol(data, check_days)

    # t1: minimum raising cnt within check days
    if not is_volume_raising_within_check_days(data, check_days, min_cnt):
        return False

    # t2: last volume higher than avg
    # 1.2: is significant higher than avg
    if not is_last_volume_higher_than_avg(data, check_days, vol_avg, min_vol_dev_fact):
        return False

    # t3: at least a few volume higher than avg
    if not is_a_few_higher_than_avg(data, check_days, min_cnt, vol_avg):
        return False

    return True


def is52_w_high(stock, within52w_high_fact):
    """
        Check 52 week High

        Args:
            stock: stock data
            within52w_high_fact: factor current data within 52 w high (ex: currVal > (Max * 0.98))

        Returns:
            True, if 52 week high

        Raises:
            NotImplementedError: if parameters are None
        """
    if stock is None or within52w_high_fact is None:
        raise NotImplementedError

    if within52w_high_fact > 1:
        raise AttributeError("parameter within52w_high_fact must be lower than 1!")  # should above other avg volume

    dataLen = len(stock)
    curVal = stock.iloc[dataLen - 1].High
    highest_high = stock['High'].max()

    if curVal == highest_high:
        return True

    else:
        hiMinusLimit = highest_high * within52w_high_fact
        if curVal > hiMinusLimit:
            return True
        else:
            return False


def gap_up(stock, min_gap_multiplier):
    """
        Check Gap Up strategy

        Args:
            stock: stock data
            min_gap_multiplier: multiplier gap up (percent to multiplier)

        Returns:
            True, if gap up

        Raises:
            NotImplementedError: if parameters are None
        """
    if stock is None or min_gap_multiplier is None:
        raise NotImplementedError

    dataLen = len(stock)
    yesterday_val = stock.iloc[dataLen - 2].Close
    curVal = stock.iloc[dataLen - 1].Open
    gapUpVal = (yesterday_val * min_gap_multiplier)
    # TODO: überprüfen ob tage hintereinander, achtung wochenende
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


def is_volume_high_enough(stock):
    if stock is None:
        raise NotImplementedError

    minReqVol = 30000  # min volume for liquid stocks
    vol_avg = calc_avg_vol(stock, 0)

    if (vol_avg > minReqVol):
        return True
    else:
        return False


def split_stock_list(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs


def get_symbol_from_name(name):
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
        print("get_symbol_from_name: ERROR symbol: " + symbol + ", Name: " + str(
            origName) + " (" + name + ") is faulty: " + str(e))
        return " "


def symbol_thread(name):
    symbol = get_symbol_from_name(name)
    if symbol != " ":
        stocks.append(symbol)
        names.append(name)


def get52_w__h__symbols__from_excel():
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
                date_from_file =  str(sh.cell(rownum, 1).value)

                # values from today contain a time (=Uhr) and not a date
                if "Uhr" in date_from_file:
                    get_symbol_threads.append_thread(threading.Thread(target=symbol_thread, kwargs={'name': name}))

        except Exception as e:
            print("Method exception in: " + get_current_function_name()
                  + ": stock name: " + str(name) + " is faulty: " + str(e))

    get_symbol_threads.execute_threads()

    cnt = 0
    while (cnt < len(names)):
        for symbol in stocks:
            f.write(names[cnt] + ",  " + symbol + "\n")  # python will convert \n to os.linesep
            cnt += 1

    f.close()  # you can omit in most cases as the destructor will call it
    return stocks


def write_stocks_to_buy_file(txt):
    #TODO add, sl, sb ...
    import datetime
    now = datetime.datetime.now()

    with open(filepath + "StocksToBuy.txt", "a") as myfile:
        myfile.write(str(txt) + ", " + str(now.strftime("%Y-%m-%d %H:%M")) + "\n")
        myfile.write("")

    myfile.close()


def calculate_stopbuy_and_stoploss(stock_data):
    """
    calculates stop buy and stop loss values
    :param stock_data: 52w stock data
    :return: stop buy and stop loss: {'sb':sb, 'sl': sl}
    """
    # values should be calc with max (real 52wHigh)
    highest_high = stock_data['High'].max()
    sb = highest_high * 1.005  # stop buy 0,5% higher than last val
    sl = sb * 0.97  # stop loss 3% lower than stop buy

    return {'sb': sb, 'sl': sl}


def print_stocks_to_buy(stocks_to_buy, num_of_stocks_per_thread, program_start_time, program_end_time):
    url_1 = "https://www.google.com/finance?q="
    url_2 = "&ei=Mby3WbnGGsjtsgHejoPwDA"
    url_3 = "http://www.finanzen.at/suchergebnisse?_type=Aktien&_search="
    tabs_for_print = "                       "

    print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Buy this stocks: ")
    print()
    if stocks_to_buy is not None:
        if len(stocks_to_buy) == 0:
            print("No stocks found")
        else:
            with open(filepath + "stockList.txt", "r") as ins:
                array = []
                for line in ins:
                    array.append(line.replace('\n', ' ').replace('\r', ''))

                for stb in stocks_to_buy:
                    stock_to_buy = stb['stock_name']
                    sb = stb['sb']
                    sl = stb ['sl']
                    found = False
                    strategy_name = stb['strategy_name']

                    # open finanzen.net and google finance
                    url = url_1 + stock_to_buy + url_2
                    url2 = url_3 + stock_to_buy

                    for line in array:
                        if ',  ' + stock_to_buy in line:
                            to_print = (str(line) + ": SB: " + str(sb) + ', SL: ' + str(sl) + ", strat: " + strategy_name + tabs_for_print + url + tabs_for_print + url2)
                            found = True
                            print(to_print)
                            write_stocks_to_buy_file(to_print)
                            break

                    if not found:
                        to_print = str(stock_to_buy) + ": SB: " + str(sb) + ', SL: ' + str(sl) + ", strat: " + strategy_name + tabs_for_print + url + tabs_for_print + url2
                        print(to_print)
                        write_stocks_to_buy_file(to_print)
                        # url_1 = "http://www.finanzen.at/suchergebnisse?_type=Aktien&_search="
                        # url = url_1 + stock_to_buy
                        # webbrowser.open(url)
                        # trace = go.Candlestick(x=df.index,
                        #                        open=df.Open,
                        #                        high=df.High,
                        #                        low=df.Low,
                        #                        close=df.Close)
                        # data = [trace]
                        #
                        # plotly.offline.plot(data, filename='simple_candlestick')

                    # write to file for backtesting and tracking

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()
    print("INFO: runtime with " + str(num_of_stocks_per_thread) + " stocks per thread: " + str(
        program_end_time - program_start_time))


def get_current_function_name ():
    """
    Returns the calling function name
    :return: calling func name
    """
    current_func_name = lambda n=0: sys._getframe(n + 1).f_code.co_name
    cf =  current_func_name()   # name of this class itself
    cf1 = current_func_name(1)  # name of calling class
    return cf1