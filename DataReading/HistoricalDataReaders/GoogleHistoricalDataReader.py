from DataRead_Google_Yahoo import get_ticker_data_with_webreader
from DataReading.StockDataReader import StockDataReader


class GoogleHistoricalDataReader(StockDataReader):

    def read_data(self, stock_data_container_list, weeks_delta, filepath_stock_dfs, source):
        for stock_data_container in stock_data_container_list:
            # get the last available price and compare with rating
            # TODO des is zu langsam

            stock52_w = get_ticker_data_with_webreader(stock_data_container.stock_ticker,
                                                       stock_data_container.stock_exchange,
                                                       filepath_stock_dfs, source, False, 52)

            stock_data_container.set_historical_stock_data(stock52_w)
