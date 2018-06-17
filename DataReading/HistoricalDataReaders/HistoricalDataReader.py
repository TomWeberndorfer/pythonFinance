import _pickle as pickle
import datetime as dt
import sys
from pandas_datareader import data

from DataRead_Google_Yahoo import optimize_name_for_yahoo
from DataReading.StockDataReader import StockDataReader
from Utils.GlobalVariables import *
from Utils.common_utils import get_current_function_name, CommonUtils


class HistoricalDataReader(StockDataReader):

    def _method_to_execute(self, stock_data_container):
        """
        Method to execute implemented for multi threading, executed for every sublist
        :param stock_data_container_sub_list: sub list of the whole stock data container (already split)
        :return: nothing, sublist in changed
        """
        if stock_data_container.stock_ticker != "":
            if stock_data_container not in self.stock_data_container_list \
                    or len(stock_data_container.historical_stock_data) <= 0 \
                    or self.reload_stockdata:
                stock52_w = self._get_ticker_data_with_webreader(stock_data_container.stock_ticker,
                                                                 stock_data_container.stock_exchange,
                                                                 self.data_source,
                                                                 self.weeks_delta)

                stock_data_container.set_historical_stock_data(stock52_w)
                try:
                    curr_prize = stock52_w[GlobalVariables.get_stock_data_labels_dict()["Close"]][len(stock52_w) - 1]
                    stock_data_container.set_stock_current_prize(curr_prize)

                except Exception as e :
                    print ("Exception: could not set curr_prize: " + str(e))

                self.update_status("HistoricalDataReader:")

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
        :return: a dataframe df with ticker data
        """
        assert len(ticker) < 10, "ATTENTION: ticker length is long, maybe it is a name not a ticker: " + ticker
        df = []

        if ticker == "" or ticker == '' or len(ticker) <= 0:
            sys.stderr.write("EXCEPTION reading because ticker is empty")
            return df

        #TODO 11 ticker = optimize_name_for_yahoo(ticker)  # TODO nicht nur für yahoo
        ticker_exchange = ticker

        if ticker_exchange == "" or ticker_exchange == '' or len(ticker_exchange) <= 0:
            sys.stderr.write("EXCEPTION reading because ticker is empty")
            return df

        # TODO 3: yahoo does not take en, so skip
        #if stock_exchange != '' and stock_exchange is not None and stock_exchange != "en" and data_source == 'yahoo':
        #ticker_exchange += "." + stock_exchange

        # TODO autmatisieren von pandas=??
        # for i in range(0, 2): #TODO 4
        try:
            end = dt.datetime.now()
            start = (end - dt.timedelta(weeks=weeks_delta))

            df = data.DataReader(ticker_exchange, data_source, start, end, 3, 0.05)
        #        if len(df) > 0:
        #            break

        except Exception as e:
            sys.stderr.write(str(e))
                # exception but the df is filled --> ok

         #       if len(df) > 0:
         #           break

            # TODO performance: wird dann langsam
            # from time import sleep
            #sleep(0.1)  # Time in seconds.

        if len(df) <= 0:
            sys.stderr.write("EXCEPTION reading " + get_current_function_name() + ": " + str(ticker_exchange) + "\n")
            print('FAILED: Reading {}'.format(ticker_exchange))

        return df
