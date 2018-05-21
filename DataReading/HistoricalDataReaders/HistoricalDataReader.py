import os
import datetime as dt

import sys

from DataRead_Google_Yahoo import optimize_name_for_yahoo
from DataReading.StockDataReader import StockDataReader
from MyThread import MyThread
import urllib3
from numpy import unicode
from pandas import DataFrame
from pandas_datareader import data, data
# TODO from yahoo_finance import Share
import googlefinance.client as google_client
import xlrd
import pandas as pd
import pandas_datareader.data as web

from Utils.common_utils import get_current_function_name


class HistoricalDataReader(StockDataReader, MyThread):

    def read_data(self, stock_data_container_list, weeks_delta, filepath_stock_dfs, source, reload_stockdata):

        self.weeks_delta = weeks_delta
        self.filepath_stock_dfs = filepath_stock_dfs
        self.source = source
        self.reload_stockdata = reload_stockdata

        self._append_list(stock_data_container_list)
        self._execute_threads()

    def _method_to_execute(self, stock_data_container_sub_list):

        # TODO des muas vl nu in thread eini
        for stock_data_container in stock_data_container_sub_list:
            stock52_w = self._get_ticker_data_with_webreader(stock_data_container.stock_ticker,
                                                             stock_data_container.stock_exchange,
                                                             self.filepath_stock_dfs, self.source, self.weeks_delta,
                                                             self.reload_stockdata)

            stock_data_container.set_historical_stock_data(stock52_w)

    def _get_ticker_data_with_webreader(self, ticker, stock_exchange, stock_dfs_file, source,
                                        weeks_delta, reload_stockdata):
        """
        TODO
        :param stock_exchange:
        :param ticker:
        :param stock_dfs_file:
        :param source:
        :param reload_stockdata:
        :param weeks_delta:
        :return:
        """
        df = []
        # TODO in klasse? basis klasse heißt google reader :)
        ticker = optimize_name_for_yahoo(ticker)
        ticker_exchange = ticker

        # TODO 3: yahoo does not take en, so skip
        if stock_exchange != "" and stock_exchange is not None and stock_exchange != "en":
            ticker_exchange += "." + stock_exchange

        try:
            # TODO does not reload new data
            if not os.path.exists(stock_dfs_file + '/{}.csv'.format(ticker_exchange)) or reload_stockdata:
                end = dt.datetime.now()
                start = (end - dt.timedelta(weeks=weeks_delta))

                df = data.DataReader(ticker_exchange, source, start, end)
                if len(df) > 0:
                    df.to_csv(stock_dfs_file + '/{}.csv'.format(ticker_exchange))
                else:
                    print('FAILED: Reading {}'.format(ticker_exchange))
                    raise Exception
            else:
                df = pd.read_csv(stock_dfs_file + '/{}.csv'.format(ticker_exchange))

        except Exception as e:
            # traceback.print_exc()
            # append_to_file(str(ticker_exchange), filepath + "failedReads.txt")

            sys.stderr.write(
                "EXCEPTION reading " + get_current_function_name() + ": " + str(ticker_exchange) + ", " + str(e) + "\n")

        return df
