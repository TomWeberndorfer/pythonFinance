from DataReading.HistoricalDataReaders.GoogleHistoricalDataReader import GoogleHistoricalDataReader
from Strategies.StockScreener import StockScreener


class HistoricalDataReaderFactory (StockScreener):

    def create_data_storage(self, storage_to_create):
        storage = ""

        if storage_to_create in "GoogleHistoricalDataReader":
            storage = GoogleHistoricalDataReader()
        else:
            raise NotImplementedError

        return storage

    def read_data(self):
        raise NotImplementedError('TODO')
