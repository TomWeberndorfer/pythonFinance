from abc import abstractmethod


class DataStorage:
    def read(self, storage_to_create, period, interval, stock_name, date_time_format):
        storage = self.create_data_storage(storage_to_create, period, interval, stock_name, date_time_format)
        result = storage.read_data()
        return result

    @abstractmethod
    def create_data_storage(self, storage_to_create):
        raise Exception ("Abstractmethod")