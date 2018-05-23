from abc import abstractmethod


class DataStorage:
    def prepare(self, storage_to_create, reader_stocks_per_threads):
        storage = self._create_data_storage(storage_to_create, reader_stocks_per_threads)
        #TODO checken ob des e ned vl so ghert:
        # result = storage.read_data()
        return storage

    @abstractmethod
    def _create_data_storage(self, storage_to_create, reader_stocks_per_threads):
        raise Exception ("Abstractmethod")