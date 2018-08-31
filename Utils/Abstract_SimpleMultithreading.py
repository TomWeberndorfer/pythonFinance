from abc import abstractmethod
from Utils.CommonUtils import CommonUtils


class Abstract_SimpleMultithreading:
    """"
    This class implements a simple method to execute a method for every element of a list in parallel
    with pool as multithreading.
    """

    def __init__(self):
        self.pool = CommonUtils.get_threading_pool()

    @abstractmethod
    def _method_to_execute(self, argument):
        """
        This method is abstract, implement the real list execution instead.
        :param argument: A single element of the list to execute
        :return: should return the result or add it to the list and return nothing
        """
        raise Exception("Abstractmethod")

    def map_list(self, list_to_execute):
        """
        Executes the implemented method in parallel for every element of the given list.
        :param list_to_execute: List with single elements to execute by method
        :return: returns the result of all executed method results.
        """
        result = self.pool.map(self._method_to_execute, list_to_execute)
        return result
