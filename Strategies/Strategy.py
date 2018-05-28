import inspect
from abc import ABC, abstractmethod

from Utils.common_utils import CommonUtils


class Strategy(ABC):
    def __init__(self, stock_data_container_list, parameter_dict):
        """
        Initialization of the strategy as definition of variables only.
        :param stock_data_container_list: a list with objects of StockDataContainer - class
        :param parameter_dict: a list with parameters for the strategy
        """
        self.stock_data_container_list = stock_data_container_list
        self.result_list = [] # result list with stocks to buy or other results
        self.parameter_dict = parameter_dict # parameter for the strategy

    def run_strategy(self):
        stack = inspect.stack()
        the_class = stack[0][0].f_locals["self"].__class__ #get the inherited class name
        if len(self.stock_data_container_list) > 0:
            pool = CommonUtils.get_threading_pool()
            pool.map(self._method_to_execute, self.stock_data_container_list)

        print(str(the_class) + " finished.")
        return self.result_list

    @abstractmethod
    def _method_to_execute(self, stock_data_container):
        raise Exception("Abstractmethod")

