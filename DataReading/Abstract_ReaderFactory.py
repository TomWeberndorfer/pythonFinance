from abc import abstractmethod


class Abstract_ReaderFactory:
    def prepare(self, reader_to_create, stock_data_container_list,
                reload_stockdata, parameter_dict):
        storage = self._create_data_reader(reader_to_create, stock_data_container_list,
                                           reload_stockdata, parameter_dict)
        # TODO checken ob des e ned vl so ghert:
        # result = storage.read_data()
        return storage

    @abstractmethod
    def _create_data_reader(self, reader_to_create, stock_data_container_list,
                            reload_stockdata, parameter_dict):
        raise Exception("Abstractmethod")
