import datetime as dt
import traceback

from pandas_datareader import data

from DataReading.Abstract_StockDataReader import Abstract_StockDataReader
from Utils.Logger_Instance import logger
from Utils.GlobalVariables import *

import quandl

quandl.ApiConfig.api_key = 'Gq6_HqRdHa8KWKV4r7-F'


class HistoricalDataReaderQuandl(Abstract_StockDataReader):

    def _method_to_execute(self, argument):
        pass

    def read_data(self):
        """
        Read the data and return stock data container list
        :return: stock data container list
        """
        self.curr_data_reads = 0
        # self.map_list(self.stock_data_container_list)

        start_time = dt.datetime.now()

        symbols = []
        lte = dt.datetime.now()
        gte = (lte - dt.timedelta(weeks=52))

        for s in self.stock_data_container_list:
            symbols.append(s.stock_ticker())

        time_diff = dt.datetime.now() - start_time
        print("1:" + (str(time_diff)))

        df = quandl.get_table('WIKI/PRICES',
                              qopts={'columns': ['ticker', 'date', 'open', 'high', 'low', 'close', 'volume']},
                              ticker=symbols, date={'gte': str(gte).split()[0], 'lte': str(lte).split()[0]})

        time_diff = dt.datetime.now() - start_time
        print("2:" + (str(time_diff)))

        for s in self.stock_data_container_list:
            td = df.loc[df['ticker'] == s.stock_ticker()]
            del td['ticker']
            # new = td.set_index('date')
            s.set_historical_stock_data(td)

        time_diff = dt.datetime.now() - start_time
        print("3:" + (str(time_diff)))

        return self.stock_data_container_list
