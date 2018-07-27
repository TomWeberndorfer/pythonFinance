from abc import abstractmethod

from DataReading.Abstract_DataContainer import Abstract_DataContainer


class Abstract_DataContainerDecorator(Abstract_DataContainer):

    def __init__(self, shaped_data_container):
        self._shaped_data_container = shaped_data_container

    @abstractmethod
    def get_names_and_values(self):
        """
        Method to return the _names and values as dictionary to insert in a treeview or else.
        Should also return the data from the wrapped shaped data container
        :return: a dict with _names as keys and values, Ex: {'Stockname': "Apple Inc"}
        """
        self._shaped_data_container.get_names_and_values()

    def stock_exchange(self):
        return self._shaped_data_container.stock_exchange()

    def get_stock_name(self):
        return self._shaped_data_container.get_stock_name()

    def stock_ticker(self):
        return self._shaped_data_container.stock_ticker()

    #TODO 11: i wills eig ned in den wrapper
    def get_recommendation_strategies(self):
        return self._shaped_data_container.get_recommendation_strategies()

