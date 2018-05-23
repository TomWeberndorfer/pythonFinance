from DataReading.DataStorage import DataStorage
from DataReading.HistoricalDataReaders.HistoricalDataReader import HistoricalDataReader
from DataReading.NewsStockDataReaders.TraderfoxNewsDataReader import TraderfoxNewsDataReader

# todo umstellen auf abstract factory
# https://sourcemaking.com/design_patterns/factory_method
class DataReaderFactory(DataStorage):

    def _create_data_storage(self, storage_to_create, reader_stocks_per_threads):
        storage = ""

        if storage_to_create in "TraderfoxNewsDataReader":
            #TODO: reader_stocks_per_threads brauch i da ned
            storage = TraderfoxNewsDataReader()

        elif storage_to_create in "HistoricalDataReader":
            storage = HistoricalDataReader(reader_stocks_per_threads)
        else:
            raise NotImplementedError

        return storage


