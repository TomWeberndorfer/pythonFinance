import os
from pathlib import Path
from DataReading.Abstract_ReaderFactory import Abstract_ReaderFactory
from Utils.common_utils import class_for_name, get_recursive_module


class DataReaderFactory(Abstract_ReaderFactory):

    @staticmethod
    def get_implemented_data_readers_dict():
        readers_dict = {}

        path = Path(os.path.dirname(os.path.abspath(__file__)))
        all_files = [file for file in list(path.glob('./*/**/**/*.py'))
                     if 'Read' in file.stem or 'read' in file.stem]

        for file in all_files:
            try:
                module_and_class = get_recursive_module(file.parent, path) + '.' + file.stem
                reader_class = class_for_name(module_and_class, file.stem)
                readers_dict.update({file.stem: reader_class})
            except ImportError as ie:
                pass
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
