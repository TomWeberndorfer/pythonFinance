import datetime
import pickle
import sys
import os

import bs4 as bs
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy
import requests
#from matplotlib import style
import plotly.graph_objs as go
#from matplotlib.finance import candlestick_ohlc
import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd

import matplotlib.pyplot as plt
#from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
#style.use('ggplot')


def calc_avg_vol(stock_data):
    """
    Calculates the average volume of stock data except the days to skip from end.
    :param stock_data: stock data
    :return: Average Value
    """

    if stock_data is None :
        raise NotImplementedError

    vol_avg = stock_data["Volume"].mean()
    return vol_avg



def split_stock_list(arr, size):
    """
    TODO description
    :param arr:
    :param size:
    :return:
    """
    if arr is None or size is None:
        raise NotImplementedError

    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs


def append_to_file(txt, file_with_path):
    if txt is None or file_with_path is None:
        raise NotImplementedError

    with open(file_with_path, "a") as myfile:
        myfile.write(str(txt) + "\n")
        myfile.write("")

    myfile.close()


def calculate_stopbuy_and_stoploss(stock_data):
    """
    calculates stop buy and stop loss values
    :param stock_data: 52w stock data
    :return: stop buy and stop loss: {'sb':sb, 'sl': sl}
    """

    if stock_data is None:
        raise NotImplementedError

    # values should be calc with max (real 52wHigh)
    highest_high = stock_data['High'].max()
    sb = highest_high * 1.005  # stop buy 0,5% higher than last val
    sl = sb * 0.97  # stop loss 3% lower than stop buy

    return {'sb': sb, 'sl': sl}


def print_stocks_to_buy(stocks_to_buy, num_of_stocks_per_thread, program_start_time, program_end_time,
                        file_name_and_path_stock_list, file_name_and_path_stocks_to_buy):
    if stocks_to_buy is None or num_of_stocks_per_thread is None or program_start_time is None or program_end_time is None or file_name_and_path_stock_list is None or file_name_and_path_stocks_to_buy is None:
        raise NotImplementedError

    url_1 = "https://www.google.com/finance?q="
    url_2 = "&ei=Mby3WbnGGsjtsgHejoPwDA"
    url_3 = "http://www.finanzen.at/suchergebnisse?_type=Aktien&_search="
    tabs_for_print = "                       "

    print()
    print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Buy this stocks: ")
    print()
    if stocks_to_buy is not None:
        if len(stocks_to_buy) == 0:
            print("No stocks found")
        else:
            with open(file_name_and_path_stock_list, "r") as ins:
                array = []
                for line in ins:
                    array.append(line.replace('\n', ' ').replace('\r', ''))

                for stb in stocks_to_buy:
                    stock_to_buy = stb['stock_name']
                    sb = stb['sb']
                    sl = stb['sl']
                    found = False
                    strategy_name = stb['strategy_name']
                    params = stb['params']

                    # open finanzen.net and google finance
                    url = url_1 + stock_to_buy + url_2
                    url2 = url_3 + stock_to_buy
                    now = datetime.datetime.now()
                    to_print_cmd = ""

                    for line in array:
                        if ',  ' + stock_to_buy in line:
                            to_print_cmd = str(line)
                            found = True
                            break

                    if not found:
                        to_print_cmd = str(stock_to_buy)

                    to_print_file = to_print_cmd
                    to_print_cmd += "; SB: " + str(sb) + '; SL: ' + str(sl) + "; strat: " + str(
                        strategy_name) + tabs_for_print + url + tabs_for_print + url2
                    print(to_print_cmd)
                    # replace . with , for excel csv
                    to_print_file += ";" + str(sb).replace('.', ',') + ';' + str(sl).replace('.', ',') + ";" + str(
                        strategy_name) + ";" + str(params) + ";" + url + ";" + url2
                    append_to_file(str(now.strftime("%Y-%m-%d %H:%M")) + "; " + to_print_file,
                                   file_name_and_path_stocks_to_buy)

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


def get_current_function_name():
    """
    Returns the calling function name
    :return: calling func name
    """
    current_func_name = lambda n=0: sys._getframe(n + 1).f_code.co_name
    cf = current_func_name()  # name of this class itself
    cf1 = current_func_name(1)  # name of calling class
    return cf1


def replace_wrong_stock_market(stock_name):
    if stock_name is None:
        raise NotImplementedError

    replace_pattern = [".MU", ".DE", ".SW", ".F", ".EX", ".TI", ".MI"]

    for pattern in replace_pattern:
        if pattern in stock_name:
            stock_name = stock_name.replace(pattern, "")
            stock_name = "ETR:" + stock_name
            break

    return stock_name


def calc_true_range(tday_high_value, tday_low_value, yesterday_close_value):
    """
    # max of todays high - low, abs(high - yday close), abs (low - yday Close)
    :param tday_high_value:
    :param tday_low_value:
    :param yesterday_close_value:
    :return:
    """

    today_high_low = tday_high_value - tday_low_value
    high_yday_close = abs(tday_high_value - yesterday_close_value)
    low_yday_close = abs(tday_low_value - yesterday_close_value)

    true_range = max(today_high_low, high_yday_close, low_yday_close)

    return true_range


def calc_mean_true_range(stock_data):
    """
    TODO replace with atr?
    :param stock_data:
    :return:
    """
    tr = []
    i = 0
    while i < len(stock_data):
        yesterday_close_value = stock_data.iloc[i - 1].Close
        tday_high_value = stock_data.iloc[i].High
        tday_low_value = stock_data.iloc[i].Low
        tr.append(calc_true_range(tday_high_value, tday_low_value, yesterday_close_value))

        i += 1

    return numpy.mean(tr)


def plot_stock_as_candlechart_with_volume(stock_name, stock_data):
    """
    print the given stock data as candlestick OHLC chart + volume
    :param stock_name: name of the stock (for title to print)
    :param stock_data: data to print, from google or yahoo
    :return: nothing
    """
    #plotly.tools.set_credentials_file(username='webc', api_key='bWWpIIZ51DsGeqBXNb15')

    trace = go.Candlestick(x=stock_data.index,
                            open=stock_data.Open,
                            high=stock_data.High,
                            low=stock_data.Low,
                            close=stock_data.Close)
    data = [trace]
    py.plot(data, filename='simple_candlestick')
    return


def read_and_save_sp500_tickers(tickers_file):
    """
    read the sp500 tickers and saves it to given file
    :param tickers_file: file to save the sp500 tickers
    :return: nothing
    """
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)

    with open(tickers_file, "wb") as f:
        pickle.dump(tickers, f)


def read_sp500_tickers(tickers_file):
    if not os.path.exists(tickers_file):
        read_and_save_sp500_tickers(tickers_file)

    with open(tickers_file, "rb") as f:
        tickers = pickle.load(f)

    return tickers

def convert_backtrader_to_dataframe (data):
    cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    #Open, High, Low, Close, Volume, OpenInterest
    lst = []

    i = - len(data.open) + 1
    while i <= 0:
        try:

            lst.append([float(data.open[i]), float(data.high[i]), float(data.low[i]),
                        float(data.close[i]), float(data.volume[i])])

        except:
            # nothing to do
            no = []
            break
        i += 1

    df1 = pd.DataFrame(lst, columns=cols)

    return df1
