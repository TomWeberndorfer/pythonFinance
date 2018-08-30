from abc import abstractmethod

from DataContainerAndDecorator.Abstract_DataContainer import Abstract_DataContainer


class Abstract_DataContainerDecorator(Abstract_DataContainer):

    def __init__(self, shaped_data_container):
        self._shaped_data_container = shaped_data_container

    def __getattr__(self, name):
        shaped_attr = getattr(self._shaped_data_container, name)
        return shaped_attr

    @abstractmethod
    def get_names_and_values(self):
        """
        Method to return the _names and values as dictionary to insert in a treeview or else.
        Should also return the data from the wrapped shaped data container
        :return: a dict with _names as keys and values, Ex: {'Stockname': "Apple Inc"}
        """
        raise Exception("Abstractmethod")
