from abc import abstractmethod


class DataStorage:
    def prepare(self, storage_to_create):
        storage = self._create_data_storage(storage_to_create)
        #TODO checken ob des e ned vl so ghert:
        # result = storage.read_data()
        return storage

    @abstractmethod
    def _create_data_storage(self, storage_to_create):
        raise Exception ("Abstractmethod")