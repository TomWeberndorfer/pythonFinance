import _pickle as pickle
import datetime as dt
import sys

from pandas_datareader import data

from DataRead_Google_Yahoo import optimize_name_for_yahoo
from DataReading.StockDataReader import StockDataReader
from MyThread import MyThread
from Utils.common_utils import get_current_function_name


class HistoricalDataReader(StockDataReader, MyThread):

    def read_data(self, stock_data_container_list, weeks_delta, filepath_stock_dfs, data_source, reload_stockdata):
        # TODO filepath_stock_dfs missbraucht für stock_data_container_file --> umbennennen

        self.weeks_delta = weeks_delta
        self.filepath_stock_dfs = filepath_stock_dfs
        self.data_source = data_source
        self.reload_stockdata = reload_stockdata
        self.stock_data_container_list = stock_data_container_list

        self._append_list(stock_data_container_list)
        print ("Reading started...")
        self._execute_threads()

        with open(filepath_stock_dfs, "wb") as f:
            pickle.dump(stock_data_container_list, f)

    def _method_to_execute(self, start_idx, end_idx):
        """
        Method to execute implemented for multi threading, executed for every sublist
        :param stock_data_container_sub_list: sub list of the whole stock data container (already split)
        :return: nothing, sublist in changed
        """

        for i in range(start_idx, end_idx + 1): # + 1 because range exclude the upper index
            if self.stock_data_container_list[i] not in self.stock_data_container_list \
                    or len(self.stock_data_container_list[i].historical_stock_data) <= 0 \
                    or self.reload_stockdata:
                stock52_w = self._get_ticker_data_with_webreader(self.stock_data_container_list[i].stock_ticker,
                                                                 self.stock_data_container_list[i].stock_exchange,
                                                                 self.data_source,
                                                                 self.weeks_delta)

                self.stock_data_container_list[i].set_historical_stock_data(stock52_w)

    def _get_ticker_data_with_webreader(self, ticker, stock_exchange, data_source,
                                        weeks_delta):
        """
        Method to read the data from the web or from temp file.
        :param stock_exchange: current stock exchange place (de, en..)
        :param ticker: ticker of the stock
        :param stock_dfs_file: file to load data or save the data from web
        :param data_source: google or yahoo
        :param reload_stockdata: true, to load from web, otherwise from temp file
        :param weeks_delta: delta from now to read the past: 52 means 52 weeks in the past
        :return:
        """
        df = []
        ticker = optimize_name_for_yahoo(ticker)  # TODO nicht nur für yahoo
        ticker_exchange = ticker

        # TODO 3: yahoo does not take en, so skip
        if stock_exchange != "" and stock_exchange is not None and stock_exchange != "en":
            ticker_exchange += "." + stock_exchange

        # TODO autmatisieren von pandas=??
        for i in range(0, 2): #TODO 4
            try:
                end = dt.datetime.now()
                start = (end - dt.timedelta(weeks=weeks_delta))

                df = data.DataReader(ticker_exchange, data_source, start, end)
                if len(df) > 0:
                    break

            except Exception as e:
                # exception but the df is filled --> ok
                if len(df) > 0:
                    break

            # TODO performance: wird dann langsam
            # from time import sleep
            #sleep(0.1)  # Time in seconds.

        if len(df) <= 0:
            sys.stderr.write(
                "EXCEPTION reading " + get_current_function_name() + ": " + str(ticker_exchange) + ", num od retries: " + str(i) + "\n")
            print('FAILED: Reading {}'.format(ticker_exchange))

        return df
