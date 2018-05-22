import datetime as dt
import os
import sys

import pandas as pd
from pandas_datareader import data

from DataRead_Google_Yahoo import optimize_name_for_yahoo
from DataReading.StockDataReader import StockDataReader
from MyThread import MyThread
from Utils.common_utils import get_current_function_name


class HistoricalDataReader(StockDataReader, MyThread):

    def read_data(self, stock_data_container_list, weeks_delta, filepath_stock_dfs, data_source, reload_stockdata):

        self.weeks_delta = weeks_delta
        self.filepath_stock_dfs = filepath_stock_dfs
        self.data_source = data_source
        self.reload_stockdata = reload_stockdata

        self._append_list(stock_data_container_list)
        self._execute_threads()

    def _method_to_execute(self, stock_data_container_sub_list):
        """
        Method to execute implemented for multi threading, executed for every sublist
        :param stock_data_container_sub_list: sub list of the whole stock data container (already split)
        :return: nothing, sublist in changed
        """

        for stock_data_container in stock_data_container_sub_list:
            stock52_w = self._get_ticker_data_with_webreader(stock_data_container.stock_ticker,
                                                             stock_data_container.stock_exchange,
                                                             self.filepath_stock_dfs, self.data_source,
                                                             self.weeks_delta,
                                                             self.reload_stockdata)

            stock_data_container.set_historical_stock_data(stock52_w)

    def _get_ticker_data_with_webreader(self, ticker, stock_exchange, stock_dfs_file, data_source,
                                        weeks_delta, reload_stockdata):
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

        try:
            if not os.path.exists(stock_dfs_file + '/{}.csv'.format(ticker_exchange)) or reload_stockdata:
                end = dt.datetime.now()
                start = (end - dt.timedelta(weeks=weeks_delta))

                df = data.DataReader(ticker_exchange, data_source, start, end)
                if len(df) > 0:
                    df.to_csv(stock_dfs_file + '/{}.csv'.format(ticker_exchange))
                else:
                    print('FAILED: Reading {}'.format(ticker_exchange))
                    raise Exception
            else:
                df = pd.read_csv(stock_dfs_file + '/{}.csv'.format(ticker_exchange))

        except Exception as e:
            # exception but the df is filled --> ok
            if len(df) <= 0:
                sys.stderr.write(
                    "EXCEPTION reading " + get_current_function_name() + ": " + str(ticker_exchange) + ", " + str(
                        e) + "\n")

        return df
