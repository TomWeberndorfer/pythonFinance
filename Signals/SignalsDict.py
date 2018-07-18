from abc import abstractmethod

from Utils.Abstract_SimpleMultithreading import Abstract_SimpleMultithreading


class StockSignalsList(Abstract_SimpleMultithreading):
    def __init__(self, signals):
        Abstract_SimpleMultithreading.__init__(self)
        self.signals = signals

    def execute_signals(self):
        """"
        Calculates all stock signals of the list and returns the result.
        """
        result = self.pool.map(self._method_to_execute, self.stock_data_container_list)
        return result

    @abstractmethod
    def _method_to_execute(self, argument):
        """
        This method is abstract, implement the real list execution instead.
        :param argument: A single element of the list to execute
        :return: should return the result or add it to the list and return nothing
        """
        raise NotImplementedError("Implement this method!")
