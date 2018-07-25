import inspect
import platform
import smtplib
import sys
import traceback
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool

import bs4 as bs
import numpy
import pandas as pd
import plotly.graph_objs as go
import plotly.plotly as py
import requests

import Utils.Logger_Instance
from DataReading.StockDataContainer import StockDataContainer
from Utils.GlobalVariables import *


class CommonUtils:
    threadpool = None

    @staticmethod
    def send_stock_email(message_text, subject_text, from_addr='python.trading.framework@gmail.com',
                         to_addr='weberndorfer.thomas@gmail.com'):
        """
        Sends a stock email with the given message
        :param to_addr: send email to address
        :param from_addr: send mail from address
        :param message_text: message text for mail: content
        :param subject_text: mail subject text
        :return: status
        """

        if message_text is None or len(message_text) <= 0:
            raise AttributeError("arguments false")

        return send_email(from_addr=from_addr,
                          to_addr_list=[to_addr],
                          cc_addr_list=[],
                          subject=subject_text,
                          message=message_text,
                          login='python.trading.framework',
                          password='8n6Qw8YoJe8m')

    @staticmethod
    def get_threading_pool(max_number_threads=200):
        """
        Returns a thread pool with maximum number of threads or the number of list len
        :param list_len: elements in the list --> number of threads (max limited)
        :param max_number_threads: maximum number of possible threads
        :return: thread pool object
        """

        if CommonUtils.threadpool is None:
            CommonUtils.threadpool = ThreadPool(max_number_threads)

        return CommonUtils.threadpool


def send_email(from_addr, to_addr_list, cc_addr_list, subject, message, login, password,
               smtpserver='smtp.gmail.com:587'):
    """
    TODO
    :param from_addr:
    :param to_addr_list:
    :param cc_addr_list:
    :param subject:
    :param message:
    :param login:
    :param password:
    :param smtpserver:
    :return:
    """
    header = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    # message = u''.join((header, message)).encode('utf-8')
    message = (header + message).encode('latin-1', 'ignore')

    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login, password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    return problems


def calc_avg_vol(stock_data):
    """
    Calculates the average volume of stock data except the days to skip from end.
    :param stock_data: stock data
    :return: Average Value
    """

    if stock_data is None or len(stock_data) <= 0:
        raise NotImplementedError

    vol_avg = stock_data[GlobalVariables.get_stock_data_labels_dict()["Volume"]].mean()
    return vol_avg


def split_list(list_to_split, size):
    """
    Split into a sublist with given size each.
    :param list_to_split: list for split input
    :param size: size of split list
    :return: the final list of lists
    """
    if list_to_split is None or len(list_to_split) <= 0 or size is None:
        raise NotImplementedError

    list_of_lists = []
    while len(list_to_split) > size:
        pice = list_to_split[:size]
        list_of_lists.append(pice)
        list_to_split = list_to_split[size:]
    list_of_lists.append(list_to_split)
    return list_of_lists


def calculate_stopbuy_and_stoploss(stock_data):
    """
    calculates stop buy and stop loss values
    :param stock_data: 52w stock data
    :return: stop buy and stop loss: {'sb':sb, 'sl': sl}
    """

    if stock_data is None:
        raise NotImplementedError

    # values should be calc with max (real 52wHigh)
    highest_high = stock_data[GlobalVariables.get_stock_data_labels_dict()['High']].max()
    sb = highest_high * 1.005  # stop buy 0,5% higher than last val
    sl = sb * 0.97  # stop loss 3% lower than stop buy

    return {'sb': sb, 'sl': sl}


def print_stocks_to_buy(stocks_to_buy, program_start_time, program_end_time,
                        file_name_and_path_stock_list, file_name_and_path_stocks_to_buy, num_of_threads):
    if stocks_to_buy is None or program_start_time is None \
            or program_end_time is None or file_name_and_path_stock_list is None \
            or file_name_and_path_stocks_to_buy is None or num_of_threads is None:
        raise NotImplementedError

    url_1 = "https://www.google.com/finance?q="
    url_2 = "&ei=Mby3WbnGGsjtsgHejoPwDA"
    url_3 = "http://www.finanzen.at/suchergebnisse?_type=Aktien&_search="
    tabs_for_print = "                       "

    Utils.Logger_Instance.logger.info("Buy this stocks: ")
    if stocks_to_buy is not None:
        if len(stocks_to_buy) == 0:
            Utils.Logger_Instance.logger.info("No stocks found.")
        else:
            with open(file_name_and_path_stock_list, "r") as ins:
                array = []
                for line in ins:
                    array.append(line.replace('\n', ' ').replace('\r', ''))

                for stb in stocks_to_buy:
                    stock_to_buy = stb['get_stock_name']
                    sb = stb['sb']
                    sl = stb['sl']
                    found = False
                    strategy_name = stb['strategy_name']
                    params = stb['params']

                    # open finanzen.net and google finance
                    # url = url_1 + stock_to_buy + url_2 #google
                    url = 'https://finance.yahoo.com/quote/' + stock_to_buy + '/chart?p=' + stock_to_buy
                    # https: // finance.yahoo.com / quote / RSG / chart?p = RSG
                    url2 = url_3 + stock_to_buy
                    now = datetime.now()
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
                    Utils.Logger_Instance.logger.info(to_print_cmd)
                    # replace . with , for excel csv
                    to_print_file += ";" + str(sb).replace('.', ',') + ';' + str(sl).replace('.', ',') + ";" + str(
                        strategy_name) + ";" + str(params) + ";" + url + ";" + url2
                    # TODO append_to_file(str(now.strftime("%Y-%m-%d %H:%M")) + "; " + to_print_file,
                    #               file_name_and_path_stocks_to_buy)

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

                    Utils.Logger_Instance.logger.info("Runtime with " + num_of_threads + " Threads and " +
                                                      str(program_end_time - program_start_time))


def print_news_analysis_results(stocks_to_buy):
    if stocks_to_buy is not None and len(stocks_to_buy) > 0:
        Utils.Logger_Instance.logger.info("\n-------------------------\n")
        for res in stocks_to_buy:
            if res != " ":
                Utils.Logger_Instance.logger.info(
                    "pos: " + str(round(res['positive_prob_dist'].prob("pos"), 2)) + " ,neg: " + str(
                    round(res['positive_prob_dist'].prob("neg"), 2)) + " " + str(res))
    else:
        Utils.Logger_Instance.logger.info("News analysis: no news")


def get_current_class_and_function_name():
    """
    Returns the calling function name
    :return:
    :return: calling class and func name
    """

    current_func_name = lambda n=0: sys._getframe(n + 1).f_code.co_name
    # cf = current_func_name()  # name of this class itself
    cf1 = current_func_name(1)  # name of calling class
    stack = inspect.stack()
    # the_method = stack[1][0].f_code.co_name
    try:
        the_class = stack[1][0].f_locals["self"].__class__
    except Exception as e:
        return "METHOD/FUNCTION: " + str(cf1)

    return str(the_class) + ", METHOD/FUNCTION: " + str(cf1)


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
        yesterday_close_value = stock_data.iloc[i - 1][GlobalVariables.get_stock_data_labels_dict()['Close']]
        tday_high_value = stock_data.iloc[i][GlobalVariables.get_stock_data_labels_dict()['High']]
        tday_low_value = stock_data.iloc[i][GlobalVariables.get_stock_data_labels_dict()['Low']]
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
    # py.plotly.tools.set_credentials_file(username='webc', api_key='bWWpIIZ51DsGeqBXNb15')

    trace = go.Candlestick(x=stock_data.index,
                           open=stock_data[GlobalVariables.get_stock_data_labels_dict()['Open']],
                           high=stock_data[GlobalVariables.get_stock_data_labels_dict()['High']],
                           low=stock_data[GlobalVariables.get_stock_data_labels_dict()['Low']],
                           close=stock_data[GlobalVariables.get_stock_data_labels_dict()['Close']])
    data = [trace]
    py.plot(data, filename=stock_name)
    return


def read_table_columns_from_webpage_list(page_list):
    """
    TODO
    :param page_list:
    :return:
    """
    return read_table_columns_from_webpage(page_list[0], page_list[1], page_list[2], page_list[3], page_list[4],
                                           page_list[5], page_list[6])


def read_table_columns_from_webpage(websource_address, find_name, class_name, table_class, ticker_column_to_read,
                                    name_column_to_read, stock_exchange):
    """
    read the sp500 tickers and saves it to given file
    :param find_name:
    :param ticker_column_to_read: 0 for sp500, 2 for cdax
    :param table_class: like 'wikitable sortable' or 'wikitable sortable zebra'
    :param websource_address: like wikepedia: 'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    :return: stock data container list
    """
    resp = requests.get(websource_address)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find(find_name, {class_name: table_class})
    stock_data_container_list = []

    if table is None or len(table) <= 0:
        raise ConnectionError("Error establishing a database connection")

    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[ticker_column_to_read].text
        name = row.findAll('td')[name_column_to_read].text
        ticker = ticker.replace("\n", "")
        name = name.replace("\n", "")
        stock_data_container_list.append(StockDataContainer(name, ticker, stock_exchange))

        Utils.Logger_Instance.logger.info("Tickers from " + websource_address + " read.")
    return stock_data_container_list


def read_table_column_from_webpage(websource_address, find_name, class_name, table_class, ticker_name_col):
    """
    read the sp500 tickers and saves it to given file
    :param find_name:
    :param class_name:
    :return:
    :param ticker_name_col: 0 for sp500, 2 for cdax
    :param table_class: like 'wikitable sortable' or 'wikitable sortable zebra'
    :param websource_address: like wikepedia: 'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    :return: nothing
    """
    resp = requests.get(websource_address)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find(find_name, {class_name: table_class})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[ticker_name_col].text
        ticker = ticker.replace("\n", "")
        tickers.append(ticker)

    return tickers


def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


def convert_backtrader_to_dataframe(data):
    """
    TODO
    :param data:
    :return:
    """
    cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    lst = []

    i = - len(data.open) + 1
    while i <= 0:
        try:

            lst.append([float(data[GlobalVariables.get_stock_data_labels_dict()['Open']][i]),
                        float(data[GlobalVariables.get_stock_data_labels_dict()['High']][i]),
                        float(data[GlobalVariables.get_stock_data_labels_dict()['Low']][i]),
                        float(data[GlobalVariables.get_stock_data_labels_dict()['Close']][i]),
                        float(data[GlobalVariables.get_stock_data_labels_dict()['Volume']][i])])

        except:
            # nothing to do
            no = []
            break
        i += 1

    df1 = pd.DataFrame(lst, columns=cols)

    return df1


def is_date_today(date_to_check):
    """
    TODO
    :param date_to_check:
    :return:
    """
    if date_to_check is None:
        raise NotImplementedError

    today_date_str = datetime.now().strftime("%d.%m.%Y")
    today_date = datetime.strptime(today_date_str, "%d.%m.%Y")

    date_to_check_str = date_to_check.strftime("%d.%m.%Y")
    date_to_check_today = datetime.strptime(date_to_check_str, "%d.%m.%Y")

    is_today = today_date == date_to_check_today
    return is_today


def is_float(n):
    try:
        float_n = float(n)
    except ValueError:
        return False
    else:
        return True


def plot_stocks_to_buy_as_candlechart_with_volume(stocks_to_buy):
    """
    plots alist with stock _names
    :param stocks_to_buy:
    :param start_date:
    :param end_date:
    :return:
    """
    for stock in stocks_to_buy:
        try:
            stock_name = stock['get_stock_name']
            stock_data = stock['data']
            plot_stock_as_candlechart_with_volume(stock_name, stock_data)

        except Exception as e:
            GUI.logger.error("Unexpected Exception : " + str(e) + "\n" + str(traceback.format_exc()))
