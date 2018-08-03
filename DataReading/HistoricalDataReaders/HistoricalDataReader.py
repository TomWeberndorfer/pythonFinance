import datetime as dt
import traceback

from pandas_datareader import data

from DataReading.Abstract_DataReader import Abstract_StockDataReader
from Utils.Logger_Instance import logger
from Utils.GlobalVariables import *


class HistoricalDataReader(Abstract_StockDataReader):

    def _method_to_execute(self, stock_data_container):
        """
        Method to execute implemented for multi threading, executed for every sublist
        :param stock_data_container_sub_list: sub list of the whole stock data container (already split)
        :return: nothing, sublist in changed
        """
        if stock_data_container.stock_ticker() != "":
            if stock_data_container not in self.stock_data_container_list \
                    or len(stock_data_container.historical_stock_data()) <= 0 \
                    or self.reload_stockdata:
                stock52_w = self._get_ticker_data_with_webreader(stock_data_container.stock_ticker(),
                                                                 stock_data_container.stock_exchange(),
                                                                 self._parameter_dict['data_source'],
                                                                 self._parameter_dict['weeks_delta'])

                stock_data_container.set_historical_stock_data(stock52_w)
                try:
                    if stock52_w is not None and len(stock52_w) > 0:
                        curr_prize = stock52_w[GlobalVariables.get_stock_data_labels_dict()["Close"]][
                            len(stock52_w) - 1]
                        stock_data_container.set_stock_current_prize(curr_prize)

                except Exception as e:
                    logger.error(
                        "Could not set curr_prize of stock " + stock_data_container.get_stock_name() + " " + str(
                            e) + "\n" + str(traceback.format_exc()))

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
        assert len(ticker) < 15, "ATTENTION: ticker length is long, maybe it is a name not a ticker: " + ticker
        df = []

        if ticker == "" or ticker == '' or len(ticker) <= 0:
            logger.error("EXCEPTION reading because ticker is empty")
            return df

        # TODO 11 ticker = optimize_name_for_yahoo(ticker)  # TODO nicht nur für yahoo
        ticker_exchange = ticker

        if ticker_exchange == "" or ticker_exchange == '' or len(ticker_exchange) <= 0:
            logger.error("EXCEPTION reading because ticker is empty (2)")
            return df

        # TODO 3: yahoo does not take en, so skip
        # if _stock_exchange != '' and _stock_exchange is not None and _stock_exchange != "en" and data_source == 'yahoo':
        # ticker_exchange += "." + _stock_exchange

        # TODO autmatisieren von pandas=??
        # for i in range(0, 2): #TODO 4
        try:
            end = dt.datetime.now()
            start = (end - dt.timedelta(weeks=weeks_delta))

            df = data.DataReader(ticker_exchange, data_source, start, end, 3, 0.05)
        #        if len(df) > 0:
        #            break

        except KeyError as ke:
            logger.error("No Stock data read for: " + str(ticker_exchange))
        except Exception as e:
            logger.error(str(e) + "\n" + str(traceback.format_exc()))
            # exception but the df is filled --> ok

        #       if len(df) > 0:
        #           break

        # TODO performance: wird dann langsam
        # from time import sleep
        # sleep(0.1)  # Time in seconds.

        if len(df) <= 0:
            logger.error("EXCEPTION reading because data is empty, " +
                         'FAILED: Reading {}'.format(ticker_exchange))

        return df
