from abc import abstractmethod

from Utils.Abstract_SimpleMultithreading import Abstract_SimpleMultithreading
from Utils.Logger_Instance import logger


class Abstract_RiskModel(Abstract_SimpleMultithreading):

    def __init__(self, **kwargs):

        # set the given values in self
        for key, value in kwargs.items():
            setattr(self, key, value)

        Abstract_SimpleMultithreading.__init__(self)

    def determine_risk(self):
        if len(self.stock_data_container_list) > 0:
            self.map_list(self.stock_data_container_list)

        logger.info("Determining risk finished.")
        # TODO return self.result_list

    @abstractmethod
    def _method_to_execute(self, argument):
        """
        This method is abstract, implement the real list execution instead.
        :param argument: A single element of the list to execute
        :return: should return the result or add it to the list and return nothing
        """
        raise Exception("Abstractmethod")
