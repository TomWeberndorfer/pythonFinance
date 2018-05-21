from DataReading.DataStorage import DataStorage
from DataReading.HistoricalDataReaders.GoogleHistoricalDataReader import GoogleHistoricalDataReader
from DataReading.NewsStockDataReaders.TraderfoxNewsDataReader import TraderfoxNewsDataReader

# todo umstellen auf abstract factory
# https://sourcemaking.com/design_patterns/factory_method
class DataReaderFactory(DataStorage):

    def _create_data_storage(self, storage_to_create):
        storage = ""

        if storage_to_create in "traderfox_hp_news":
            storage = TraderfoxNewsDataReader()

        elif storage_to_create in "GoogleHistoricalDataReader":
            storage = GoogleHistoricalDataReader()
        else:
            raise NotImplementedError

        return storage


