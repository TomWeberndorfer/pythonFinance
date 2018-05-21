import sys

import os

from DataReading.NewsStockDataReaders.DataReaderFactory import DataReaderFactory
from Signals.Signals import signal_is_volume_high_enough, signal_is_volume_raising, signal_is52_w_high
from Strategies.Strategy import Strategy
import time
from datetime import datetime

# from DataRead_Google_Yahoo import get_ticker_data_with_webreader
# from Utils.common_utils import format_news_analysis_results, send_stock_email
# from Utils.file_utils import read_tickers_from_file, append_to_file
# from newsFeedReader.traderfox_hp_news import read_news_from_traderfox
from newsTrading.GermanTaggerAnalyseNews import GermanTaggerAnalyseNews
import threading
import traceback
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from MyThread import MyThread
from Strategies.Strategy import strat_scheduler
from Utils.common_utils import split_list, print_stocks_to_buy, calculate_stopbuy_and_stoploss, \
    get_current_function_name
# from Utils.file_utils import read_tickers_from_file, append_to_file
from Utils.file_utils import FileUtils


# TODO parameter aus self statt da oben --> parameter_dict.news_threshold
# news_threshold = 0.5
##########################

# from directory UnitTests to --> root folder with: ..\\..\\
#TODO übergeben
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = ROOT_DIR + '\\DataFiles\\'

class w52HighStrategy(Strategy):
    def run_strategy(self):
        try:
            result = []
            screening_start_time = datetime.now()
            # Create new threads
            splits = split_list(self.stock_data_container_list, self.parameter_dict['num_of_stocks_per_thread'])
            num_of_threads = len(splits)
            stock_screening_threads = MyThread("stock_screening_threads")
            end = datetime.now()
            ago52_w = (end - timedelta(weeks=52))

            # TODO weg
            stock_list_name = "stockList.txt"
            stocks_to_buy_name = "StocksToBuy.CSV"

            i = 0
            while i < len(splits):
                stock_data_container = splits[i]
                stock_screening_threads.append_thread(
                    threading.Thread(target=self.__function_for_threading_strat_scheduler,
                                     kwargs={'stock_data_container': stock_data_container, 'ago52_w_time': ago52_w,
                                             'end_l': end, 'params': self.parameter_dict, 'result': result}))
                i += 1
            # Start new Threads to schedule all stocks
            FileUtils.append_to_file(
                "Start screening with " + str(
                    len(self.stock_data_container_list)) + " symbols and num_of_stocks_per_thread = " + str(
                    self.parameter_dict['num_of_stocks_per_thread']), filepath + "Runtime.txt")
            stock_screening_threads.execute_threads()

            # print the results and plot it
            print_stocks_to_buy(result, self.parameter_dict['num_of_stocks_per_thread'], screening_start_time,
                                datetime.now(),
                                filepath + stock_list_name, filepath + stocks_to_buy_name, str(num_of_threads))
            # plot_stocks_to_buy_as_candlechart_with_volume(stocks_to_buy, ago52_w, end)

        except Exception as e:
            traceback.print_exc()

        return self.result_list

    def __function_for_threading_strat_scheduler(self, stock_data_container, ago52_w_time, end_l, params, result):
        """
        TODO: result ist r�ckgabe
       :param stock_names_to_check:
        :param ago52_w_time:
        :param end_l:
        :param result:
        :return:
        """
        print("Started with: " + str(stock_data_container))

        result.extend(self.__strat_scheduler(stock_data_container, ago52_w_time, end_l, params))

    def __strat_scheduler(self, stock_data_container, params):
        """
        function to schedule all strategies and return the stocks to buy
        :param params: parameter for strategy within structure: {'strat_52_w_hi_hi_volume': {'check_days': 5, 'min_cnt': 3, 'min_vol_dev_fact': 1.1, 'within52w_high_fact': 0.98}}
        :param stock_data_container: list with stock names to check
        :param ago52_w: date and time 52weeks ago
        :param end: end date for read (today)
        :return: stocks to buy with {'buy', 'stock_name', 'sb', 'sl'}
        """

        stocks_to_buy = []  # stocks and enhanced data

        for stock_data in stock_data_container:

            try:
                str_52w_p = params[0]
                check_days = str_52w_p['check_days']
                min_cnt = str_52w_p['min_cnt']
                min_vol_dev_fact = str_52w_p['min_vol_dev_fact']
                within52w_high_fact = str_52w_p['within52w_high_fact']
                res = self.__strat_52_w_hi_hi_volume(stock_data.stock_name, stock52_w, check_days, min_cnt, min_vol_dev_fact,
                                              within52w_high_fact)
                if res['buy']:
                    stocks_to_buy.append(
                        {'buy': True, 'stock_name': res['stock_name'], 'sb': res['sb'], 'sl': res['sl'],
                         'strategy_name': res['strategy_name'], 'params': params[0], 'data': stock52_w})

            except Exception as e:
                sys.stderr.write(
                    "strat_scheduler: Strategy Exception: " + str(stock_data.stock_name) + " is faulty: " + str(e) + "\n")
                traceback.print_exc()

        print("Finished with [" + str(stock_data.stock_name) + "]")
        return stocks_to_buy

    def __strat_52_w_hi_hi_volume(self, stock_data_container, parameter_dict):
        """
        Check 52 week High, raising volume, and high enough volume

        :param  stock_name: name of the stock
        :param  stock52_w_data: stock data
        :param  check_days: number of days to check
        :param  min_cnt: min higher days within check days
        :param min_vol_dev_fact:
        :param within52w_high_fact:: factor current data within 52 w high (ex: currVal > (Max * 0.98))

        :return: stock to buy with {'buy', 'stock_name', 'sb', 'sl'}
        """
        if stock_data_container.stock_name is None \
                or stock52_w_data is None \
                or parameter_dict['check_days'] is None \
                or parameter_dict['min_cnt'] is None \
                or parameter_dict['min_vol_dev_fact'] is None \
                or parameter_dict['within52w_high_fact'] is None:
            raise NotImplementedError

        if parameter_dict['min_vol_dev_fact'] < 1:
            raise AttributeError("parameter min_vol_dev_fact must be higher than 1!")  # should above other avg volume

        if parameter_dict['within52w_high_fact'] > 1:
            raise AttributeError("parameter within52w_high_fact must be lower than 1!")  # should above other avg volume

        if not signal_is_volume_high_enough(stock52_w_data):
            return {'buy': False}

        if not signal_is_volume_raising(stock52_w_data, check_days, min_cnt, min_vol_dev_fact):
            return {'buy': False}

        if not signal_is52_w_high(stock52_w_data, within52w_high_fact):
            return {'buy': False}

        result = calculate_stopbuy_and_stoploss(stock52_w_data)

        return {'buy': True, 'stock_name': stock_name, 'sb': result['sb'], 'sl': result['sl'],
                'strategy_name': get_current_function_name()}

