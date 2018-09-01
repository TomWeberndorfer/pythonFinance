import os
from pathlib import Path
from DataReading.Abstract_ReaderFactory import Abstract_ReaderFactory
from Utils.CommonUtils import CommonUtils


class DataReaderFactory(Abstract_ReaderFactory):

    @staticmethod
    def get_implemented_data_readers_dict():
        path = Path(os.path.dirname(os.path.abspath(__file__)))
        readers_dict = CommonUtils.get_implemented_items_dict(path, './*/**/**/*.py', "read")
        return readers_dict

    def _create_data_reader(self, reader_to_create, stock_data_container_list,
                            reload_stockdata, parameter_dict):
        readers_dict = DataReaderFactory.get_implemented_data_readers_dict()
        if reader_to_create in readers_dict:
            # get the class from class dict and create the concrete object then
            strat_class = readers_dict[reader_to_create]
            reader = strat_class(stock_data_container_list, reload_stockdata, parameter_dict)
            return reader
        else:
            raise NotImplementedError("Reader is not implemented: " + str(reader_to_create))
