from abc import ABC, abstractmethod
import _pickle as pickle

from Utils.Abstract_SimpleMultithreading import Abstract_SimpleMultithreading
from Utils.StatusUpdate import StatusUpdate
from Utils.common_utils import CommonUtils


class Abstract_StockDataReader(StatusUpdate, Abstract_SimpleMultithreading):

    @abstractmethod
    def _method_to_execute(self, argument):
        """
        This method is abstract, implement the real list execution instead.
        :param argument: A single element of the list to execute
        :return: should return the result or add it to the list and return nothing
        """
        raise Exception("Abstractmethod")

    def __init__(self, stock_data_container_list, weeks_delta, stock_data_container_file, data_source, reload_stockdata, date_file=""):
        self.stock_data_container_list = stock_data_container_list
        self.reload_stockdata = reload_stockdata
        self.data_source = data_source
        self.stock_data_container_file = stock_data_container_file
        self.weeks_delta = weeks_delta
        if date_file is not None and len(date_file) > 0:
            self.date_file = date_file

        StatusUpdate.__init__(self, len(stock_data_container_list))
        Abstract_SimpleMultithreading.__init__(self)

    def read_data(self):
        self.curr_data_reads = 0
        self.map_list(self.stock_data_container_list)

        with open(self.stock_data_container_file, "wb") as f:
            pickle.dump(self.stock_data_container_list, f)

        return self.stock_data_container_list
