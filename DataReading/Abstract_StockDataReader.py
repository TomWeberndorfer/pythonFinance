from abc import ABC, abstractmethod
import _pickle as pickle

from Utils.Abstract_SimpleMultithreading import Abstract_SimpleMultithreading
from Utils.StatusUpdate import StatusUpdate
from Utils.CommonUtils import CommonUtils


class Abstract_StockDataReader(StatusUpdate, Abstract_SimpleMultithreading):

    @abstractmethod
    def _method_to_execute(self, argument):
        """
        This method is abstract, implement the real list execution instead.
        :param argument: A single element of the list to execute
        :return: should return the result or add it to the list and return nothing
        """
        raise Exception("Abstractmethod")

    def __init__(self, stock_data_container_list, reload_stockdata, parameter_dict):
        """
        Init method for stock data reader
        :param stock_data_container_list: list with all stock containers
        :param data_source: data reader source
        :param reload_stockdata: True: reload from web, or False: take from file
        :param parameter_dict: dict with all related reader parameters, dependent on the reader
        """
        self.stock_data_container_list = stock_data_container_list
        self.reload_stockdata = reload_stockdata
        self._parameter_dict = parameter_dict

        StatusUpdate.__init__(self, len(stock_data_container_list))
        Abstract_SimpleMultithreading.__init__(self)

    def read_data(self):
        """
        Read the data and return stock data container list
        :return: stock data container list
        """
        self.curr_data_reads = 0
        self.map_list(self.stock_data_container_list)

        return self.stock_data_container_list
