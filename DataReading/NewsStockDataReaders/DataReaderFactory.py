from DataReading.DataStorage import DataStorage
from DataReading.HistoricalDataReaders.HistoricalDataReader import HistoricalDataReader
from DataReading.NewsStockDataReaders.TraderfoxNewsDataReader import TraderfoxNewsDataReader


# todo umstellen auf abstract factory
# https://sourcemaking.com/design_patterns/factory_method
class DataReaderFactory(DataStorage):

    def _create_data_storage(self, storage_to_create, stock_data_container_list, weeks_delta, stock_data_container_file, data_source, reload_stockdata):
        if storage_to_create in "TraderfoxNewsDataReader":
            storage = TraderfoxNewsDataReader(stock_data_container_list, weeks_delta, stock_data_container_file, data_source, reload_stockdata)

        elif storage_to_create in "HistoricalDataReader":
            storage = HistoricalDataReader(stock_data_container_list, weeks_delta, stock_data_container_file, data_source, reload_stockdata)
        else:
            raise NotImplementedError

        return storage
