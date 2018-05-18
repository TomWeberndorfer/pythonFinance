from DataReading.NewsStockDataReaders.NewsDataReaderFactory import NewsDataReaderFactory
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
from Utils.common_utils import split_list, print_stocks_to_buy
# from Utils.file_utils import read_tickers_from_file, append_to_file
from Utils.file_utils import FileUtils


# TODO parameter aus self statt da oben --> parameter_dict.news_threshold
# news_threshold = 0.5
##########################

class w52HighStrategy(Strategy):
    def run_strategy(self):

        hier weiter
        try:
            result = []

            # Create new threads
            splits = split_list(self.stock_data_container_list, self.parameter_dict['num_of_stocks_per_thread'])
            num_of_threads = len(splits)
            stock_screening_threads = MyThread("stock_screening_threads")

            i = 0
            while i < len(splits):
                stock_names_to_check = splits[i]
                stock_screening_threads.append_thread(
                    threading.Thread(target=self.function_for_threading_strat_scheduler,
                                     kwargs={'stock_names_to_check': stock_names_to_check, 'ago52_w_time': ago52_w,
                                             'end_l': end, 'params': params, 'result': result}))
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

    def __function_for_threading_strat_scheduler(stock_names_to_check, ago52_w_time, end_l, params, result):
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

    def __run_stock_screening(num_of_stocks_per_thread):
        screening_start_time = datetime.now()

        try:
            end = datetime.now()
            ago52_w = (end - timedelta(weeks=52))
            data_provider = "google"  # TODO
            filepath = 'C:\\temp\\'
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
                                             'end_l': end, 'params': params, 'result': result}))
                i += 1
            # Start new Threads to schedule all stocks
            FileUtils.append_to_file(
                "Start screening with " + str(len(all_symbols)) + " symbols and num_of_stocks_per_thread = " + str(
                    num_of_stocks_per_thread), filepath + "Runtime.txt")
            stock_screening_threads.execute_threads()

            # print the results and plot it
            print_stocks_to_buy(result, num_of_stocks_per_thread, screening_start_time, datetime.now(),
                                filepath + stock_list_name, filepath + stocks_to_buy_name, str(num_of_threads))
            # plot_stocks_to_buy_as_candlechart_with_volume(stocks_to_buy, ago52_w, end)

        except Exception as e:
            traceback.print_exc()
