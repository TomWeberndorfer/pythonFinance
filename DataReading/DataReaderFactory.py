from DataReading.Abstract_ReaderFactory import Abstract_ReaderFactory
from DataReading.HistoricalDataReaders.HistoricalDataReader import HistoricalDataReader
from DataReading.NewsStockDataReaders.TraderfoxNewsDataReader import TraderfoxNewsDataReader


class DataReaderFactory(Abstract_ReaderFactory):

    def _create_data_reader(self, reader_to_create, stock_data_container_list,
                            reload_stockdata, parameter_dict):
        if reader_to_create in "TraderfoxNewsDataReader":
            reader = TraderfoxNewsDataReader(stock_data_container_list,
                                             reload_stockdata, parameter_dict)

        elif reader_to_create in "HistoricalDataReader":
            reader = HistoricalDataReader(stock_data_container_list,
                                          reload_stockdata, parameter_dict)
        else:
            raise NotImplementedError

        return reader
