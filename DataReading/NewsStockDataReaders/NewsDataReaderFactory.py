from DataReading.DataStorage import DataStorage
from DataReading.NewsStockDataReaders.NewsDataStorage import NewsDataStorage
from DataReading.NewsStockDataReaders.TraderfoxNewsDataReader import TraderfoxNewsDataReader


class NewsDataReaderFactory(NewsDataStorage):

    def create_data_storage(self, storage_to_create):
        storage = ""

        if storage_to_create in "traderfox_hp_news":
            storage = TraderfoxNewsDataReader()
        else:
            raise NotImplementedError

        return storage


