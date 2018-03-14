import threading
import traceback
from datetime import datetime
from datetime import timedelta
import sys

from MyThread import MyThread
from Strategies import strat_scheduler
from Utils.common_utils import split_list, print_stocks_to_buy, plot_stock_as_candlechart_with_volume
from Utils.file_utils import append_to_file, read_tickers_from_file

#TODO remove:
threads = []
err = []
program_start_time = datetime.now()
params = []
stocks_per_thread = 10


# TODO maybe move to better place
#TODO strategy scheduler soll nicht ein thread sein, jeder strategie könnte eigener thread mit subthreads sein 
def function_for_threading_strat_scheduler(stock_names_to_check, ago52_w_time, end_l, result):
    """
    TODO: result ist rückgabe
    :param stock_names_to_check:
    :param ago52_w_time:
    :param end_l:
    :param result:
    :return:
    """
    print("Started with: " + str(stock_names_to_check))

    result.extend(strat_scheduler(stock_names_to_check, ago52_w_time, end_l, params))


def plot_stocks_to_buy_as_candlechart_with_volume(stocks_to_buy):
    """
    plots alist with stock names
    :param stocks_to_buy:
    :param start_date:
    :param end_date:
    :return:
    """
    for stock in stocks_to_buy:
        try:
            stock_name = stock['stock_name']
            stock_data = stock['data']
            plot_stock_as_candlechart_with_volume(stock_name, stock_data)

        except Exception as e:
            sys.stderr.write("EXCEPTION execute_threads: " + str(e) + "\n")
            traceback.print_exc()


def run_stock_screening(num_of_stocks_per_thread):
    try:
        end = datetime.now()
        ago52_w = (end - timedelta(weeks=52))

        data_provider = "google"  # TODO
        filepath = 'C:\\temp\\'
        stock_list_name = "stockList.txt"
        stocks_to_buy_name = "StocksToBuy.CSV"
        tickers_file_name = "stock_tickers.pickle"
        stocknames_file_name = "stock_names.pickle"
        tickers_file = filepath + tickers_file_name
        stocknames_file = filepath + stocknames_file_name

        # enhanced stock messages:
        # logging.basicConfig(level=logging.DEBUG)
        all_symbols = []
        all_names = []

        # params for strat_52_w_hi_hi_volume
        params.append({'check_days': 7, 'min_cnt': 3, 'min_vol_dev_fact': 1.2, 'within52w_high_fact': 0.98})

        # params for strat_gap_up__hi_volume
        params.append({'min_gap_factor': 1.03})

        # strat_candlestick_hammer_hi_vol
        params.append({'hammer_length_in_factor': 1.01, 'handle_bigger_than_head_factor': 2})
        ###########################################################

        res = read_tickers_from_file(tickers_file, stocknames_file)
        all_symbols.extend(res['tickers'])
        all_names.extend(res['names'])
        result = []

        # Create new threads
        splits = split_list(all_symbols, num_of_stocks_per_thread)
        num_of_threads = len(splits)
        stock_screening_threads = MyThread("stock_screening_threads")

        i = 0
        while i < len(splits):
            stock_names_to_check = splits[i]
            stock_screening_threads.append_thread(
                threading.Thread(target=function_for_threading_strat_scheduler,
                                 kwargs={'stock_names_to_check': stock_names_to_check, 'ago52_w_time': ago52_w,
                                         'end_l': end, 'result': result}))
            i += 1

        # Start new Threads to schedule all stocks
        append_to_file(
            "Start screening with " + str(len(all_symbols)) + " symbols and num_of_stocks_per_thread = " + str(
                num_of_stocks_per_thread), filepath + "Runtime.txt")
        stock_screening_threads.execute_threads()

        # print the results and plot it
        print_stocks_to_buy(result, num_of_stocks_per_thread, program_start_time, datetime.now(),
                            filepath + stock_list_name, filepath + stocks_to_buy_name, str(num_of_threads))
        # plot_stocks_to_buy_as_candlechart_with_volume(stocks_to_buy, ago52_w, end)

    except Exception as e:
        traceback.print_exc()

