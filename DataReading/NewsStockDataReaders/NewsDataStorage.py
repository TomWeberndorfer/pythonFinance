from abc import abstractmethod


class NewsDataStorage:
    def read(self, storage_to_create):
        storage = self.create_data_storage(storage_to_create)
        result = storage.read_data()
        return result

    @abstractmethod
    def create_data_storage(self, storage_to_create):
        raise Exception ("Abstractmethod")