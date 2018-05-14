from DataReading.DataStorage import DataStorage
from DataReading.NewsStockDataReaders.TraderfoxNewsDataReader import TraderfoxNewsDataReader


class NewsDataReaderFactory(DataStorage):

    def create_data_storage(self, storage_to_create, period, interval, stock_name, date_time_format):
        storage = ""

        if storage_to_create in "traderfox_hp_news":
            storage = TraderfoxNewsDataReader(period, interval, stock_name, date_time_format)
        else:
            raise NotImplementedError

        return storage

    def get_symbol_from_name(self):
        raise NotImplementedError('TODO')
