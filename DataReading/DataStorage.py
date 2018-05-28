from abc import abstractmethod


class DataStorage:
    def prepare(self, storage_to_create, stock_data_container_list, weeks_delta, stock_data_container_file, data_source,
                            reload_stockdata):
        storage = self._create_data_storage(storage_to_create, stock_data_container_list, weeks_delta, stock_data_container_file, data_source,
                            reload_stockdata)
        #TODO checken ob des e ned vl so ghert:
        # result = storage.read_data()
        return storage

    @abstractmethod
    def _create_data_storage(self, storage_to_create, stock_data_container_list, weeks_delta, stock_data_container_file, data_source,
                            reload_stockdata):
        raise Exception ("Abstractmethod")