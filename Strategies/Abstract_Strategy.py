import inspect
from abc import ABC, abstractmethod

from Utils.Abstract_SimpleMultithreading import Abstract_SimpleMultithreading
from Utils.StatusUpdate import StatusUpdate
from Utils.Logger_Instance import logger


class Abstract_Strategy(StatusUpdate, Abstract_SimpleMultithreading):
    def __init__(self, **kwargs):
        """
        Initialization of the strategy as definition of variables only.
        :param stock_data_container_list: a list with objects of StockDataContainer - class
        :param parameter_dict: a list with parameters for the strategy
        """
        stat_num = 0
        self.result_list = []  # result list with stocks to buy or other results

        # set the given values in self
        for key, value in kwargs.items():
            setattr(self, key, value)

        if hasattr(self, "status_update"):
            stat_update = self.status_update
        else:
            stat_update = True

        if hasattr(self, "stock_data_container_list") and self.stock_data_container_list is not None:
            stat_num = len(self.stock_data_container_list)

        StatusUpdate.__init__(self, stat_num, stat_update)
        Abstract_SimpleMultithreading.__init__(self)

    def run_strategy(self, my_stock_data_container_list=None):

        if not my_stock_data_container_list is None:
            self.stock_data_container_list = my_stock_data_container_list

        stack = inspect.stack()
        # the_class = stack[0][0].f_locals["self"].__class__ #get the inherited class name
        if len(self.stock_data_container_list) > 0:
            self.map_list(self.stock_data_container_list)
        return self.result_list

    @abstractmethod
    def _method_to_execute(self, argument):
        """
        This method is abstract, implement the real list execution instead.
        :param argument: A single element of the list to execute
        :return: should return the result or add it to the list and return nothing
        """
        raise NotImplementedError("Abstractmethod")

    @staticmethod
    @abstractmethod
    def get_required_parameters_with_default_parameters():
        """
        Return a dict with required strategy parameters and default parameter values.
        :return: dict with required values and default parameters
        """
        raise NotImplementedError("Abstractmethod")
