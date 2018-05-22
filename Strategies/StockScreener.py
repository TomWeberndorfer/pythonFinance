import threading
import traceback
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

import os

from MyThread import MyThread
from Strategies.Strategy import strat_scheduler
from Utils.common_utils import split_list, print_stocks_to_buy
# from Utils.file_utils import read_tickers_from_file, append_to_file
from Utils.file_utils import FileUtils

# TODO übergeben
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\'


class StockScreener():
    def prepare_strategy(self, strategy_to_create, stock_data_container_list, parameter_list):
        strategy = self._create_strategy(strategy_to_create, stock_data_container_list, parameter_list)
        return strategy

    @abstractmethod
    def _create_strategy(self, strategy_to_create):
        raise Exception("Abstractmethod")


# # TODO maybe move to better place
# # TODO strategy scheduler soll nicht ein thread sein, jeder strategie k�nnte eigener thread mit subthreads sein
def function_for_threading_strat_scheduler(stock_names_to_check, ago52_w_time, end_l, params, result):
    """
     TODO: result ist r�ckgabe
    :param stock_names_to_check:
     :param ago52_w_time:
     :param end_l:
     :param result:
     :return:
     """
    print("Started with: " + str(stock_names_to_check))

    result.extend(strat_scheduler(stock_names_to_check, ago52_w_time, end_l, params))


def run_stock_screening(num_of_stocks_per_thread):
    screening_start_time = datetime.now()

    try:
        end = datetime.now()
        ago52_w = (end - timedelta(weeks=52))
        stock_list_name = "stockList.txt"
        stocks_to_buy_name = "StocksToBuy.CSV"
        tickers_file_name = "stock_tickers.pickle"
        stocknames_file_name = "stock_names.pickle"
        stock_exchange_file_name = "stock_exchange_file.pickle"
        tickers_file = filepath + tickers_file_name
        stocknames_file = filepath + stocknames_file_name
        stock_exchange_file = filepath + stock_exchange_file_name
        # enhanced stock messages:
        # logging.basicConfig(level=logging.DEBUG)
        all_symbols = []
        all_names = []
        params = []

        # params for strat_52_w_hi_hi_volume
        params.append({'check_days': 7, 'min_cnt': 3, 'min_vol_dev_fact': 1.2, 'within52w_high_fact': 0.98})

        # params for strat_gap_up__hi_volume
        params.append({'min_gap_factor': 1.03})
        # strat_candlestick_hammer_hi_vol
        params.append({'hammer_length_in_factor': 1.01, 'handle_bigger_than_head_factor': 2})
        ###########################################################

        # todo des mach i vorher im main schon --> ubergaben
        stock_data_container_file_name = "stock_data_container_file.pickle"
        stock_data_container_file = filepath + stock_data_container_file_name

        # TODO- eini verschieben irgendwo, ned manuell
        # TODO muss die strategie schon de daten griagn? ja schon, wanns mehrere san kinan ned alle wieder lesen

        res = FileUtils.read_tickers_from_file(stock_data_container_file)
        res = FileUtils.read_tickers_from_file(tickers_file, stocknames_file, stock_exchange_file)
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
            stock_screening_threads._append_thread(
                threading.Thread(target=function_for_threading_strat_scheduler,
                                 kwargs={'stock_names_to_check': stock_names_to_check, 'ago52_w_time': ago52_w,
                                         'end_l': end, 'params': params, 'result': result}))
            i += 1
        # Start new Threads to schedule all stocks
        FileUtils.append_to_file(
            "Start screening with " + str(len(all_symbols)) + " symbols and num_of_stocks_per_thread = " + str(
                num_of_stocks_per_thread), filepath + "Runtime.txt")
        stock_screening_threads._execute_threads()

        # print the results and plot it
        print_stocks_to_buy(result, num_of_stocks_per_thread, screening_start_time, datetime.now(),
                            filepath + stock_list_name, filepath + stocks_to_buy_name, str(num_of_threads))
        # plot_stocks_to_buy_as_candlechart_with_volume(stocks_to_buy, ago52_w, end)

    except Exception as e:
        traceback.print_exc()
